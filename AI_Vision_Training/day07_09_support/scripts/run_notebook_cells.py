"""Execute every code cell of every Day 7-9 notebook offline (deterministic).

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\run_notebook_cells.py
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
FOLDERS = ("Day07_Automation_Concept_Mechanics", "Day08_Electrical_PLC",
           "Day09_AI_Camera_Imaging")


def run_all(show: bool = False) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    os.environ["MPLBACKEND"] = "Agg"
    failures = 0
    for folder in FOLDERS:
        for path in sorted((NOTEBOOKS / folder).glob("*.ipynb")):
            notebook = json.loads(path.read_text(encoding="utf-8"))
            namespace: dict = {"__name__": "__main__"}
            code_index = 0
            old_cwd = Path.cwd()
            os.chdir(path.parent)
            try:
                for cell in notebook["cells"]:
                    if cell["cell_type"] != "code":
                        continue
                    code_index += 1
                    source = "".join(cell["source"])
                    buffer = io.StringIO()
                    try:
                        with contextlib.redirect_stdout(buffer):
                            exec(compile(source, f"{path.name}:cell{code_index}", "exec"), namespace)
                        if show:
                            print(f"--- {path.stem} cell {code_index} ---")
                            print(buffer.getvalue().rstrip())
                    except Exception as error:  # noqa: BLE001
                        failures += 1
                        print(f"FAIL {path.name} cell {code_index}: {type(error).__name__}: {error}")
                        print(buffer.getvalue()[-1500:])
                        break
            finally:
                os.chdir(old_cwd)
            print(f"OK   {path.name}: {code_index} code cells")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(run_all(show="--show" in sys.argv))
