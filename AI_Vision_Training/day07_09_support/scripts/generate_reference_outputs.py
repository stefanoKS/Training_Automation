"""Capture deterministic reference output for every executable notebook cell.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\generate_reference_outputs.py

The result is stored in ``reference_data/reference_outputs.json``.  The PDF
exporter reads this file instead of executing cells during export, so a PDF build
never runs student code.  The outputs are reference outputs of an offline model,
not measurements from a real machine.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = ROOT / "notebooks"
OUTPUT = ROOT / "day07_09_support" / "reference_data" / "reference_outputs.json"
FOLDERS = (
    "Day07_Automation_Concept_Mechanics",
    "Day08_Electrical_PLC",
    "Day09_AI_Camera_Imaging",
)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    os.environ["MPLBACKEND"] = "Agg"
    results: dict[str, dict] = {}
    for folder in FOLDERS:
        for path in sorted((NOTEBOOKS / folder).glob("*.ipynb")):
            notebook = json.loads(path.read_text(encoding="utf-8"))
            namespace: dict = {"__name__": "__main__"}
            cells: dict[str, dict] = {}
            old_cwd = Path.cwd()
            os.chdir(path.parent)
            try:
                for cell in notebook["cells"]:
                    if cell["cell_type"] != "code":
                        continue
                    exec_id = cell.get("metadata", {}).get("day07_09_exercise", "?")
                    source = "".join(cell["source"])
                    buffer = io.StringIO()
                    with contextlib.redirect_stdout(buffer):
                        exec(compile(source, f"{path.name}:{exec_id}", "exec"), namespace)
                    cells[exec_id] = {"source": source, "output": buffer.getvalue().rstrip()}
            finally:
                os.chdir(old_cwd)
            results[path.stem] = cells
            print(f"Captured {path.stem}: {len(cells)} cells")
    OUTPUT.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
