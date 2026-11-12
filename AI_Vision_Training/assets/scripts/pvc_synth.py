"""合成PVCシート表面画像ジェネレータ / Synthetic PVC sheet surface generator.

このモジュールは研修教材用の「PVC シートらしい」合成画像を作るための共通部品です。
実際の工場画像ではありません。見た目の傾向（明るさ・テクスチャ・ノイズ・欠陥）を
学習用に簡略化して再現しているだけです。

This module is the shared helper that renders "PVC-sheet-like" synthetic images for
the training course. These are NOT real factory images. Only the general appearance
(brightness, texture, noise, defects) is simplified for teaching purposes.

設計方針 / Design rules
-----------------------
* すべての画像は明示的な seed から決定的に生成されます。
  Every image is produced deterministically from an explicit seed.
* 欠陥のバウンディングボックスは、実際に描画したマスクから計算します。
  Bounding boxes are computed FROM the drawn mask, so they always match the pixels.
* 依存関係は NumPy と Pillow のみです。
  Only NumPy and Pillow are required.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, asdict
from typing import Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------------
# クラス定義 / Class definitions
# ---------------------------------------------------------------------------

# YOLO 検出データセットで使用する 3 クラス / the three classes used by the YOLO dataset
YOLO_CLASSES: tuple[str, ...] = ("black_spot", "scratch", "streak")

# 異常検知データセットで使用する 4 種類 / the four defect types used by the anomaly dataset
ANOMALY_DEFECTS: tuple[str, ...] = ("black_spot", "scratch", "streak", "irregular_mark")

CLASS_NAMES_JA: dict[str, str] = {
    "black_spot": "黒点",
    "scratch": "傷",
    "streak": "スジ",
    "irregular_mark": "不定形なしみ",
}


@dataclass
class Defect:
    """1 つの欠陥の記録 / record of a single defect.

    bbox は (x1, y1, x2, y2) のピクセル座標で、x2 / y2 は「含まない」端です。
    bbox uses pixel coordinates (x1, y1, x2, y2) where x2 / y2 are exclusive.
    """

    cls: str
    bbox: tuple[int, int, int, int]

    @property
    def width(self) -> int:
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self) -> int:
        return self.bbox[3] - self.bbox[1]

    def to_yolo(self, image_width: int, image_height: int) -> tuple[float, float, float, float]:
        """YOLO 形式 (xc, yc, w, h) へ正規化して変換 / convert to normalized YOLO values."""
        x1, y1, x2, y2 = self.bbox
        cx = (x1 + x2) / 2.0 / image_width
        cy = (y1 + y2) / 2.0 / image_height
        w = (x2 - x1) / image_width
        h = (y2 - y1) / image_height
        return cx, cy, w, h

    def as_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# 小さな画像処理ヘルパ / small image-processing helpers (NumPy only)
# ---------------------------------------------------------------------------


def _gaussian_kernel(sigma: float) -> np.ndarray:
    radius = max(1, int(round(3.0 * sigma)))
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma) ** 2)
    return k / k.sum()


def _convolve1d(array: np.ndarray, kernel: np.ndarray, axis: int) -> np.ndarray:
    radius = len(kernel) // 2
    pad = [(0, 0)] * array.ndim
    pad[axis] = (radius, radius)
    padded = np.pad(array, pad, mode="edge")
    out = np.zeros(array.shape, dtype=np.float64)
    for offset, weight in enumerate(kernel):
        window = [slice(None)] * array.ndim
        window[axis] = slice(offset, offset + array.shape[axis])
        out += weight * padded[tuple(window)]
    return out


def gaussian_blur(array: np.ndarray, sigma: float) -> np.ndarray:
    """2 次元ガウスぼかし / separable 2-D Gaussian blur for a 2-D float array."""
    if sigma <= 0:
        return array.astype(np.float64, copy=True)
    kernel = _gaussian_kernel(sigma)
    return _convolve1d(_convolve1d(array, kernel, 0), kernel, 1)


def smooth_noise(shape: tuple[int, int], rng: np.random.Generator, sigma: float) -> np.ndarray:
    """ぼかしたノイズ（低周波のムラ）/ blurred noise used for low-frequency mottling."""
    raw = rng.normal(0.0, 1.0, size=shape)
    return gaussian_blur(raw, sigma)


def _normalize01(array: np.ndarray) -> np.ndarray:
    lo, hi = float(array.min()), float(array.max())
    if hi - lo < 1e-9:
        return np.zeros_like(array)
    return (array - lo) / (hi - lo)


# ---------------------------------------------------------------------------
# 表面（正常）画像 / normal surface rendering
# ---------------------------------------------------------------------------


def make_base_surface(
    height: int,
    width: int,
    rng: np.random.Generator,
    *,
    base_level: float = 205.0,
    shading_strength: float = 7.0,
    texture_strength: float = 2.6,
    grain_strength: float = 3.4,
    tint: Sequence[float] = (1.0, 1.0, 1.005),
) -> np.ndarray:
    """正常な PVC シート表面を float32 の HxWx3 配列 (0-255) で返す。

    Render a normal PVC-like surface as a float32 HxWx3 array in the 0-255 range.
    """
    yy, xx = np.mgrid[0:height, 0:width]

    # 1) ゆるやかな明るさムラ（シート全体の照度差）/ low-frequency illumination variation
    shading = _normalize01(smooth_noise((height, width), rng, sigma=18.0)) - 0.5
    shading += 0.45 * (_normalize01(smooth_noise((height, width), rng, sigma=6.0)) - 0.5)
    surface = base_level + shading_strength * shading * 2.0

    # 2) カレンダー加工方向（横方向）の細い筋 / faint calendering-direction lines
    phase = rng.uniform(0, 2 * np.pi)
    period = rng.uniform(5.0, 11.0)          # px
    wobble = 0.6 * np.sin(2 * np.pi * yy / rng.uniform(70.0, 140.0) + phase)
    lines = np.sin(2 * np.pi * (yy + wobble) / period + phase)
    surface += texture_strength * lines

    # 3) 細かいざらつき（粒状ノイズ）/ fine grain noise
    grain = rng.normal(0.0, 1.0, size=(height, width))
    surface += grain_strength * grain

    # 4) ごく弱い斜めのムラ / a very weak diagonal gradient
    surface += shading_strength * 0.35 * ((xx / max(width - 1, 1)) - 0.5)

    surface = np.clip(surface, 0.0, 255.0)
    rgb = np.stack([surface * float(t) for t in tint], axis=-1)
    return np.clip(rgb, 0.0, 255.0).astype(np.float32)


# ---------------------------------------------------------------------------
# 欠陥の描画 / defect drawing
# ---------------------------------------------------------------------------


def _empty_mask(height: int, width: int) -> Image.Image:
    return Image.new("L", (width, height), 0)


def _draw_black_spot(draw: ImageDraw.ImageDraw, height: int, width: int, rng: np.random.Generator) -> None:
    radius = int(rng.integers(3, 10))
    x = int(rng.integers(radius + 6, width - radius - 6))
    y = int(rng.integers(radius + 6, height - radius - 6))
    # 楕円はわずかにつぶす（完全な円は人工的に見えるため）
    # squash the ellipse slightly; a perfect circle looks artificial
    ry = max(2, int(radius * rng.uniform(0.7, 1.0)))
    draw.ellipse([x - radius, y - ry, x + radius, y + ry], fill=255)
    if rng.random() < 0.45:
        # 周囲への薄い広がり / a faint halo around the spot
        halo = int(radius * rng.uniform(1.2, 1.8))
        draw.ellipse([x - halo, y - halo, x + halo, y + halo], fill=110)


def _draw_scratch(draw: ImageDraw.ImageDraw, height: int, width: int, rng: np.random.Generator) -> None:
    length = float(rng.uniform(22.0, 70.0))
    # 傷はランダムな向き。完全な水平/垂直は避ける。
    # scratches have a random direction; avoid exactly horizontal or vertical
    angle = float(rng.uniform(0.35, np.pi - 0.35))
    margin = 10
    cx = float(rng.uniform(margin + length / 2, width - margin - length / 2))
    cy = float(rng.uniform(margin + length / 2, height - margin - length / 2))
    dx, dy = np.cos(angle) * length / 2.0, np.sin(angle) * length / 2.0
    draw.line([(cx - dx, cy - dy), (cx + dx, cy + dy)], fill=255, width=int(rng.integers(1, 3)))


def _draw_streak(draw: ImageDraw.ImageDraw, height: int, width: int, rng: np.random.Generator) -> None:
    # スジはカレンダー加工方向（ほぼ横）に長く伸びる
    # streaks run long in the calendering direction (nearly horizontal)
    length = float(rng.uniform(70.0, min(width - 24, 170.0)))
    margin = 10
    cy = float(rng.uniform(margin + 6, height - margin - 6))
    cx = float(rng.uniform(margin + length / 2, width - margin - length / 2))
    slope = float(rng.uniform(-0.06, 0.06))
    draw.line(
        [(cx - length / 2, cy + slope * length / 2), (cx + length / 2, cy - slope * length / 2)],
        fill=255,
        width=int(rng.integers(1, 3)),
    )


def _draw_irregular_mark(draw: ImageDraw.ImageDraw, height: int, width: int, rng: np.random.Generator) -> None:
    """不定形なしみ / an irregular blotch built from a random polygon."""
    margin = 14
    cx = float(rng.uniform(margin, width - margin))
    cy = float(rng.uniform(margin, height - margin))
    n_points = int(rng.integers(6, 10))
    base_r = float(rng.uniform(4.0, 11.0))
    angles = np.sort(rng.uniform(0, 2 * np.pi, size=n_points))
    radii = base_r * rng.uniform(0.55, 1.35, size=n_points)
    points = [
        (float(np.clip(cx + r * np.cos(a), 1, width - 2)), float(np.clip(cy + r * np.sin(a), 1, height - 2)))
        for a, r in zip(angles, radii)
    ]
    draw.polygon(points, fill=255)


_DRAWERS = {
    "black_spot": _draw_black_spot,
    "scratch": _draw_scratch,
    "streak": _draw_streak,
    "irregular_mark": _draw_irregular_mark,
}

# 欠陥タイプ別の濃さ / contrast per defect type (fraction of brightness removed)
_CONTRAST = {
    "black_spot": (0.55, 0.95),
    "scratch": (0.45, 0.85),
    "streak": (0.22, 0.45),
    "irregular_mark": (0.30, 0.60),
}


def _bbox_from_mask(mask: np.ndarray, threshold: float = 0.10) -> tuple[int, int, int, int]:
    ys, xs = np.nonzero(mask >= threshold)
    if len(xs) == 0:                      # pragma: no cover - defensive
        raise ValueError("mask is empty; no defect was drawn")
    x1, x2 = int(xs.min()), int(xs.max()) + 1
    y1, y2 = int(ys.min()), int(ys.max()) + 1
    return x1, y1, x2, y2


def _overlaps(a: tuple[int, int, int, int], others: Iterable[tuple[int, int, int, int]], pad: int = 6) -> bool:
    ax1, ay1, ax2, ay2 = a
    for bx1, by1, bx2, by2 in others:
        if ax1 - pad < bx2 and bx1 - pad < ax2 and ay1 - pad < by2 and by1 - pad < ay2:
            return True
    return False


def render_defective(
    height: int,
    width: int,
    seed: int,
    defect_types: Sequence[str] = ("black_spot", "scratch", "streak"),
    *,
    count: int | None = None,
    max_attempts: int = 60,
    **surface_kwargs,
) -> tuple[np.ndarray, np.ndarray, list[Defect]]:
    """欠陥入り画像・マスク・欠陥記録を返す / render a defective image, its mask and records.

    Returns
    -------
    image : float32 ndarray, shape (H, W, 3), values 0-255
    mask  : uint8 ndarray, shape (H, W), values 0 or 255
    defects : list[Defect]
        実際に描画したマスクから計算したバウンディングボックス。
        Bounding boxes computed from the mask that was actually drawn.
    """
    rng = np.random.default_rng(seed)
    image = make_base_surface(height, width, rng, **surface_kwargs)

    if count is None:
        count = int(rng.integers(1, min(3, len(defect_types)) + 1))
    count = max(1, min(count, len(defect_types)))

    chosen = list(rng.choice(list(defect_types), size=count, replace=False))

    combined = np.zeros((height, width), dtype=np.float64)
    defects: list[Defect] = []
    accepted_boxes: list[tuple[int, int, int, int]] = []

    for cls in chosen:
        placed = False
        for _ in range(max_attempts):
            canvas = _empty_mask(height, width)
            drawer = ImageDraw.Draw(canvas)
            _DRAWERS[cls](drawer, height, width, rng)
            mask = np.asarray(canvas, dtype=np.float64) / 255.0
            mask = gaussian_blur(mask, sigma=0.8)
            if mask.max() < 0.5:          # nothing drawn
                continue
            bbox = _bbox_from_mask(mask)
            if bbox[0] < 3 or bbox[1] < 3 or bbox[2] > width - 3 or bbox[3] > height - 3:
                continue
            if _overlaps(bbox, accepted_boxes):
                continue
            low, high = _CONTRAST[cls]
            contrast = float(rng.uniform(low, high))
            combined = np.maximum(combined, mask * contrast)
            accepted_boxes.append(bbox)
            defects.append(Defect(cls=cls, bbox=bbox))
            placed = True
            break
        if not placed:                    # pragma: no cover - defensive
            raise RuntimeError(f"could not place a {cls!r} defect in a {width}x{height} image")

    image = image * (1.0 - combined[..., None])
    image = np.clip(image, 0.0, 255.0).astype(np.float32)

    mask_uint8 = (np.clip(combined, 0.0, 1.0) * 255).astype(np.uint8)
    return image, mask_uint8, defects


def render_normal(height: int, width: int, seed: int, **surface_kwargs) -> np.ndarray:
    """正常画像のみを返す / render a normal (defect-free) image."""
    rng = np.random.default_rng(seed)
    return make_base_surface(height, width, rng, **surface_kwargs)


# ---------------------------------------------------------------------------
# 保存・検証ユーティリティ / persistence and verification helpers
# ---------------------------------------------------------------------------


def to_pil(image: np.ndarray) -> Image.Image:
    """float32 の 0-255 配列を RGB の PIL 画像へ / float32 0-255 array -> RGB PIL image."""
    return Image.fromarray(np.clip(image, 0, 255).astype(np.uint8), mode="RGB")


def save_rgb(image: np.ndarray, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    to_pil(image).save(path)


def save_mask(mask: np.ndarray, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mask.astype(np.uint8), mode="L").save(path)


def file_digest(path) -> str:
    """ファイル内容の SHA-256 / SHA-256 of a file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_unique_images(paths: Sequence, label: str = "images") -> None:
    """訓練・検証・試験セット間で同一画像が無いことを確認する。

    Fail loudly if the same image content appears in more than one split.
    """
    seen: dict[str, object] = {}
    duplicates = []
    for path in paths:
        digest = file_digest(path)
        if digest in seen:
            duplicates.append((seen[digest], path))
        else:
            seen[digest] = path
    if duplicates:
        raise RuntimeError(f"duplicate {label} detected across splits: {duplicates}")


__all__ = [
    "ANOMALY_DEFECTS",
    "CLASS_NAMES_JA",
    "YOLO_CLASSES",
    "Defect",
    "assert_unique_images",
    "file_digest",
    "gaussian_blur",
    "make_base_surface",
    "render_defective",
    "render_normal",
    "save_mask",
    "save_rgb",
    "to_pil",
]
