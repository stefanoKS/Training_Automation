"""研修ノートブック共通の部品 / Shared helpers for the course notebooks.

このモジュールは **表示と環境** だけを担当します。
The module handles **display and environment** only. The lesson algorithms —
thresholding, contour finding, IoU, scoring — stay in the notebooks where the
learner can read them.

使い方 / Usage（ノートブックの Part 0 で 1 回だけ / once, in Part 0 of a notebook）::

    import sys
    sys.path.insert(0, str(COURSE_ROOT / "assets" / "helpers"))
    import aivision

    aivision.configure_japanese_font()
    aivision.show_asset(ASSETS, ["diagrams", "diagram_pixel_grid.png"], "8x8 pixels")

ウィジェット / widgets
---------------------
``widgets_available()`` は ipywidgets が使えるかを返します。使えないときは
``False`` を返すだけで、例外は投げません。ノートブック側には必ず「ウィジェットなしでも
動く」パラメータセルを用意してください。
``widgets_available()`` returns ``False`` instead of raising when ipywidgets is missing.
Every notebook block that uses a widget must also have a plain parameter cell that
works without one.
"""

from __future__ import annotations

import platform
from pathlib import Path

JP_FONT_CANDIDATES = (
    "C:/Windows/Fonts/NotoSansJP-Regular.ttf",
    "C:/Windows/Fonts/YuGothR.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
)

JP_FONT_KEYWORDS = (
    "NotoSansJP-Regular", "NotoSansCJK-Regular", "YuGothR", "meiryo", "msgothic",
    "BIZ-UDGothicR", "NotoSansJP", "HiraginoSans",
)


# ---------------------------------------------------------------------------
# 日本語表示 / Japanese text in figures
# ---------------------------------------------------------------------------


def find_japanese_font() -> Path | None:
    """日本語を描けるフォントを 1 つ返す。無ければ ``None``。

    Returns one font that can draw Japanese, or ``None``.
    """
    for candidate in JP_FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            return path

    if platform.system() == "Windows":
        folders = [Path("C:/Windows/Fonts")]
    elif platform.system() == "Darwin":
        folders = [Path("/System/Library/Fonts"), Path("/Library/Fonts"),
                   Path.home() / "Library/Fonts"]
    else:
        folders = [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts"]

    for folder in folders:
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*")):
            if path.suffix.lower() not in {".ttf", ".ttc", ".otf"}:
                continue
            name = path.stem.lower()
            if "bold" in name or "italic" in name:
                continue
            if any(keyword.lower() in name for keyword in JP_FONT_KEYWORDS):
                return path
    return None


def configure_japanese_font() -> str | None:
    """Matplotlib に日本語フォントを設定する。設定したファミリ名を返す。

    Configures Matplotlib for Japanese text and returns the family name, or ``None``
    when no Japanese font is installed.
    """
    from matplotlib import font_manager, rcParams

    path = find_japanese_font()
    if path is None:
        rcParams["font.family"] = ["DejaVu Sans"]
        return None
    try:
        font_manager.fontManager.addfont(str(path))
        family = font_manager.FontProperties(fname=str(path)).get_name()
    except Exception:  # pragma: no cover - a broken font file must not stop the lesson
        rcParams["font.family"] = ["DejaVu Sans"]
        return None
    rcParams["font.family"] = [family, "DejaVu Sans"]
    rcParams["font.monospace"] = [family, "DejaVu Sans Mono"]
    rcParams["axes.unicode_minus"] = False
    return family


def set_plot_style() -> None:
    """図の見た目をそろえる / keep every figure visually consistent."""
    from matplotlib import rcParams

    rcParams["figure.figsize"] = (9.5, 4.2)
    rcParams["figure.dpi"] = 110
    rcParams["axes.grid"] = True
    rcParams["grid.alpha"] = 0.25
    rcParams["axes.titlesize"] = 10
    rcParams["axes.labelsize"] = 9
    rcParams["legend.fontsize"] = 8


# ---------------------------------------------------------------------------
# 画像表示 / displaying course assets
# ---------------------------------------------------------------------------


def show_asset(assets_root: Path, parts, caption: str = "", figsize=(11, 5)):
    """``assets/<parts>`` の画像を 1 枚表示する。無ければ理由を出す。

    Shows one image from the course assets folder, or explains what is missing.
    """
    import matplotlib.pyplot as plt
    from PIL import Image

    path = Path(assets_root).joinpath(*parts)
    if not path.is_file():
        print("画像がありません / file not found:", path)
        print("実行してください / run: python assets\\scripts\\generate_training_assets.py")
        print("                       python assets\\scripts\\generate_teaching_diagrams.py")
        return None
    image = Image.open(path)
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(image)
    ax.set_xticks([])
    ax.set_yticks([])
    if caption:
        ax.set_title(caption, fontsize=9)
    plt.tight_layout()
    plt.show()
    return image


# ---------------------------------------------------------------------------
# ウィジェット / widgets
# ---------------------------------------------------------------------------


def widgets_available() -> bool:
    """ipywidgets が使えるか。使えなくても例外にしない。

    Returns whether ipywidgets can be used. Never raises: a missing widget package is a
    normal situation on a locked-down machine, and the parameter fallback still works.
    """
    try:
        import ipywidgets  # noqa: F401
    except Exception:
        return False
    return True


def explain_widget_requirement() -> None:
    """ウィジェットが無いときに、代わりに何をすればよいか伝える。"""
    print("ipywidgets が見つかりません / ipywidgets is not installed.")
    print("この節は下の「パラメータセル」で同じ実験ができます。")
    print("Use the parameter cell below this one: it runs the same experiment.")
    print("導入する場合 / to install it:  python -m pip install ipywidgets")


def auto_update_label(continuous: bool) -> str:
    """スライダーの更新方法を日本語と英語で説明する。"""
    if continuous:
        return "動かすと自動で更新されます / updates while you drag"
    return "「実行」ボタンを押したときだけ更新されます / updates only when you press Run"
