"""Render every Day 7-9 SVG diagram to PNG with Inkscape.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\render_diagrams.py

The PNGs are inspection artefacts, not course deliverables.  Rendering with a
real SVG engine is deliberate: it catches missing fonts, clipped Japanese text
and layout problems that an XML check cannot see.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS = ROOT / "assets" / "diagrams"
OUTPUT = ROOT / "day07_09_support" / "reference_data" / "diagram_png"
INKSCAPE_CANDIDATES = (
    Path("C:/Program Files/Inkscape/bin/inkscape.com"),
    Path("C:/Program Files/Inkscape/bin/inkscape.exe"),
    Path("/usr/bin/inkscape"),
)
SIZE_RE = re.compile(r'<svg[^>]*width="(\d+)"[^>]*height="(\d+)"')
COUNTS = {"day07": 9, "day08": 11, "day09": 9}


def expected_sources() -> list[Path]:
    paths: list[Path] = []
    for folder, count in COUNTS.items():
        for index in range(1, count + 1):
            paths.append(DIAGRAMS / folder / f"D{folder[3:]}-{index:02d}.svg")
    return paths


def find_inkscape() -> Path:
    for candidate in INKSCAPE_CANDIDATES:
        if candidate.exists():
            return candidate
    raise RuntimeError("Inkscape is required to render the diagrams")


def render(svg_path: Path, inkscape: Path) -> Path:
    match = SIZE_RE.search(svg_path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"cannot read size from {svg_path}")
    width = int(match.group(1))
    target = OUTPUT / svg_path.parent.name / f"{svg_path.stem}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(inkscape),
        f"--export-filename={target}",
        f"--export-width={int(width * 1.6)}",
        "--export-background=#FFFFFF",
        "--export-background-opacity=255",
        str(svg_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=120)
    if not target.is_file():
        raise RuntimeError(f"render failed for {svg_path}: {(result.stderr or result.stdout)[-800:]}")
    return target


def main() -> int:
    inkscape = find_inkscape()
    sources = expected_sources()
    missing = [path for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing diagrams: {[str(p) for p in missing]}")
    for path in sources:
        target = render(path, inkscape)
        print(f"Rendered {target.relative_to(ROOT)}")
    print(f"Rendered {len(sources)} diagrams with Inkscape")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
