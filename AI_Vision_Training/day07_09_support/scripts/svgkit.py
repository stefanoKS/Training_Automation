"""Small, dependency-free SVG builder used to author the Day 7-9 teaching diagrams.

Every diagram is an editable SVG with ``<title>``, ``<desc>`` and bilingual text labels.
Text is wrapped and auto-shrunk inside its card, and the builder refuses to save a
diagram whose shapes or text would extend past the canvas (clipping check).
"""

from __future__ import annotations

import html
import math
from dataclasses import dataclass, field

FONT = "Arial, 'Noto Sans JP', 'Yu Gothic', Meiryo, sans-serif"

INK = "#142B3F"
MUTED = "#526378"
ACCENT = "#2563A6"
PALE = "#F5F8FC"
CARD = "#FFFFFF"
WARN = "#B4541E"
GOOD = "#1B7A4B"
BAD = "#A32B2B"
SAFE = "#6B3FA0"
JP_BG = "#E8F1FA"
EN_BG = "#EAF6EE"


def char_width(ch: str, size: float) -> float:
    return size * (1.0 if ord(ch) > 0x2E7F else 0.55)


def text_width(text: str, size: float) -> float:
    return sum(char_width(ch, size) for ch in text)


def wrap(text: str, max_width: float, size: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        if current and text_width(current + ch, size) > max_width:
            cut = current.rfind(" ")
            if cut > 0 and text_width(current[:cut], size) > max_width * 0.22 and ord(ch) < 0x2E7F:
                lines.append(current[:cut])
                current = current[cut + 1 :] + ch
            else:
                lines.append(current)
                current = ch
        else:
            current += ch
    if current:
        lines.append(current)
    return lines


@dataclass
class Svg:
    fid: str
    title: str
    desc: str
    width: int
    height: int
    parts: list[str] = field(default_factory=list)
    _max_x: float = 0.0
    _max_y: float = 0.0

    def __post_init__(self) -> None:
        self.parts.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">'
            f"<title id=\"title\">{html.escape(self.title)}</title>"
            f"<desc id=\"desc\">{html.escape(self.desc)}</desc>"
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" '
            'markerHeight="9" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#2563A6"/></marker>'
            '<marker id="arrow-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" '
            'markerHeight="9" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#A32B2B"/></marker>'
            '<marker id="arrow-green" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" '
            'markerHeight="9" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#1B7A4B"/></marker>'
            "</defs>"
            f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="#F5F8FC"/>'
            f'<rect x="0" y="0" width="{self.width}" height="12" fill="#2563A6"/>'
        )

    # ---------------------------------------------------------------- checks
    def _track(self, x: float, y: float) -> None:
        self._max_x = max(self._max_x, x)
        self._max_y = max(self._max_y, y)

    # ---------------------------------------------------------------- shapes
    def rect(self, x, y, w, h, fill=CARD, stroke=ACCENT, sw=2, rx=12, dash=None) -> None:
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'
        )
        self._track(x + w, y + h)

    def circle(self, cx, cy, r, fill="white", stroke=ACCENT, sw=2) -> None:
        self.parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )
        self._track(cx + r, cy + r)

    def line(self, x1, y1, x2, y2, stroke=ACCENT, sw=2, dash=None, marker=True) -> None:
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        mark = ' marker-end="url(#arrow)"' if marker else ""
        self.parts.append(
            f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" fill="none" stroke="{stroke}" '
            f'stroke-width="{sw}"{extra}{mark}/>'
        )
        self._track(max(x1, x2), max(y1, y2))

    def poly(self, points, stroke=ACCENT, sw=2, marker=True, fill="none") -> None:
        mark = ' marker-end="url(#arrow)"' if marker else ""
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.parts.append(
            f'<polyline points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{mark}/>'
        )
        for x, y in points:
            self._track(x, y)

    def text(self, x, y, value, size=18, weight=400, fill=INK, anchor="start", italic=False) -> None:
        style = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{style}>{html.escape(value)}</text>'
        )
        width = text_width(value, size)
        left = x - width if anchor == "end" else (x - width / 2 if anchor == "middle" else x)
        self._track(left + width, y)

    def text_block(self, x, y, ja, en, width, size_ja=20, size_en=17, ja_fill=INK, en_fill=MUTED) -> float:
        """Draw a Japanese line group above its English translation; returns next y."""
        for line in wrap(ja, width, size_ja):
            y += size_ja * 1.25
            self.text(x, y, line, size_ja, 700 if size_ja >= 20 else 600, ja_fill)
        for line in wrap(en, width, size_en):
            y += size_en * 1.3
            self.text(x, y, line, size_en, 400, en_fill)
        return y

    def card(self, x, y, w, h, ja, en, fill=CARD, stroke=ACCENT, accent=None, sub=None, min_size=14) -> None:
        """Card with Japanese then English text fitted inside the box."""
        pad = 14
        accent = accent or stroke
        self.rect(x, y, w, h, fill=fill, stroke=stroke)
        self.rect(x, y + 10, 7, h - 20, fill=accent, stroke=accent, sw=0, rx=3)
        size_ja, size_en = 21.0, 17.0
        while True:
            ja_lines = wrap(ja, w - 2 * pad - 14, size_ja)
            en_lines = wrap(en, w - 2 * pad - 14, size_en)
            total = len(ja_lines) * size_ja * 1.22 + len(en_lines) * size_en * 1.28
            if sub:
                sub_lines = wrap(sub, w - 2 * pad - 14, 15)
                total += len(sub_lines) * 15 * 1.3
            else:
                sub_lines = []
            if total <= h - 2 * pad + 4 or size_ja <= min_size:
                break
            size_ja -= 1
            size_en = max(min_size, size_en - 0.8)
        budget = len(ja_lines) * size_ja * 1.22 + len(en_lines) * size_en * 1.28
        budget += len(sub_lines) * 15 * 1.3 if sub else 0
        cursor = y + (h - budget) / 2
        for line in ja_lines:
            cursor += size_ja * 1.1
            self.text(x + pad + 8, cursor, line, size_ja, 700)
        cursor += 2
        for line in en_lines:
            cursor += size_en * 1.16
            self.text(x + pad + 8, cursor, line, size_en, 400, MUTED)
        for line in sub_lines:
            cursor += 15 * 1.2
            self.text(x + pad + 8, cursor, line, 15, 400, MUTED, italic=True)

    def chip(self, x, y, w, h, ja, en, fill=JP_BG, stroke=ACCENT) -> None:
        self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=8)
        self.text(x + w / 2, y + h / 2 - 3, ja, min(18, h * 0.42), 700, INK, "middle")
        self.text(x + w / 2, y + h / 2 + 17, en, min(15, h * 0.34), 400, MUTED, "middle")

    def legend(self, x, y, items) -> None:
        for index, (fill, stroke, ja, en) in enumerate(items):
            top = y + index * 34
            self.rect(x, top, 26, 20, fill=fill, stroke=stroke, sw=2, rx=4)
            self.text(x + 36, top + 16, f"{ja} / {en}", 16, 400, MUTED)

    def header(self, eyebrow: str, ja: str, en: str) -> None:
        self.text(56, 56, eyebrow, 19, 700, ACCENT)
        self.text(56, 104, ja, 32, 700, INK)
        self.text(56, 144, en, 26, 400, MUTED)

    def footer(self, caption_ja: str = "", caption_en: str = "") -> None:
        if self._max_y > self.height - 132:
            grown = int(math.ceil((self._max_y + 146) / 20.0) * 20)
            self.parts[0] = self.parts[0].replace(
                f'width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}"',
                f'width="{self.width}" height="{grown}" viewBox="0 0 {self.width} {grown}"',
                1,
            )
            self.parts[0] = self.parts[0].replace(
                f'width="{self.width}" height="{self.height}" fill="#F5F8FC"',
                f'width="{self.width}" height="{grown}" fill="#F5F8FC"',
                1,
            )
            self.height = grown
        assert self._max_y <= self.height - 132, (
            f"{self.fid}: content ({self._max_y:.0f}) would collide with the footer band"
        )
        if not caption_en and " / " in caption_ja:
            caption_ja, caption_en = caption_ja.split(" / ", 1)
        avail = self.width - 152
        size_ja, size_en = 17.0, 14.5
        while text_width(caption_ja, size_ja) > avail and size_ja > 10:
            size_ja -= 0.5
        while text_width(caption_en, size_en) > avail and size_en > 10:
            size_en -= 0.5
        self.rect(56, self.height - 116, self.width - 112, 60, fill=JP_BG, stroke=ACCENT, sw=1, rx=10)
        self.text(76, self.height - 82, caption_ja, size_ja, 700, INK)
        self.text(76, self.height - 60, caption_en, size_en, 400, MUTED)

    def save(self, path) -> None:
        self.parts.append(
            f'<text x="{self.width - 40}" y="{self.height - 8}" font-family="{FONT}" font-size="15" '
            f'fill="#526378" text-anchor="end">{html.escape(self.fid)} • 編集可能な図 / editable SVG</text>'
        )
        assert self._max_x <= self.width - 8, f"{self.fid}: content overflows width ({self._max_x:.0f})"
        assert self._max_y <= self.height - 4, f"{self.fid}: content overflows height ({self._max_y:.0f})"
        self.parts.append("</svg>")
        path.write_text("\n".join(self.parts) + "\n", encoding="utf-8")


def new_diagram(fid, ja_title, en_title, day_label, height, width=1440, desc_extra="") -> Svg:
    svg = Svg(
        fid=fid,
        title=f"{ja_title} / {en_title}",
        desc=f"{ja_title} / {en_title} — editable bilingual training diagram for {day_label}. {desc_extra}".strip(),
        width=width,
        height=height,
    )
    svg.header(day_label, ja_title, en_title)
    return svg
