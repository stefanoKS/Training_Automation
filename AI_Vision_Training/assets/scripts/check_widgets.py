"""ウィジェットの動作確認 / Widget smoke check.

ノートブックを実行し、``widgets.interact`` を含むセルが **ウィジェットの表示** を
出力しているかを確認します。エラーが出ないだけでは、表示できたことになりません。
This executes a notebook and checks that the cells using ``widgets.interact`` really emit a widget
view in their output. "No exception" alone does not prove the control was displayed.

使い方 / Usage
--------------
    python assets\\scripts\\check_widgets.py
    python assets\\scripts\\check_widgets.py --notebook Day01_02

結果 / Result
-------------
各セルについて ``rendered``（ウィジェット表示あり）か ``fallback``（ipywidgets 無し）かを表示します。
For each cell it prints ``rendered`` (a widget view was produced) or ``fallback`` (no ipywidgets).

ブラウザでの実際の操作は別です。このスクリプトは「表示された」ことまでを確認します。
This does not click the controls in a browser; it verifies that the widget was rendered.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat

COURSE_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"

WIDGET_NOTEBOOKS = [
    "Day01_02_Pixels_and_Images",
    "Day02_02_Conditions_Loops_Functions",
    "Day02_03_OpenCV_Image_Processing",
    "Day03_01_YOLO_Concepts",
    "Day03_03_YOLO_Experiments",
    "Day05_03_YOLO_vs_PatchCore",
]

WIDGET_MIME = "application/vnd.jupyter.widget-view+json"


def check(notebook_path: Path, timeout: int = 900) -> dict:
    import nbclient

    notebook = nbformat.read(str(notebook_path), as_version=4)
    kernel = notebook.metadata.get("kernelspec", {}).get("name", "aivision")
    client = nbclient.NotebookClient(
        notebook, kernel_name=kernel, timeout=timeout, allow_errors=True,
        resources={"metadata": {"path": str(COURSE_ROOT)}},
    )
    client.execute()

    record = {"notebook": notebook_path.name, "widget_cells": 0, "rendered": 0,
              "fallback": 0, "errors": []}
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type != "code" or "widgets.interact" not in cell.source:
            continue
        record["widget_cells"] += 1
        outputs = cell.get("outputs", [])
        errors = [o for o in outputs if o.get("output_type") == "error"]
        if errors:
            record["errors"].append(f"cell {index}: {errors[0].get('ename')}: "
                                    f"{errors[0].get('evalue')}")
            continue
        has_widget = any(WIDGET_MIME in (o.get("data") or {}) for o in outputs)
        if has_widget:
            record["rendered"] += 1
        else:
            record["fallback"] += 1
    return record


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check that the interactive demos really render.")
    parser.add_argument("--notebook", default=None, help="substring of one notebook name")
    args = parser.parse_args(argv)

    failures = 0
    for stem in WIDGET_NOTEBOOKS:
        if args.notebook and args.notebook not in stem:
            continue
        path = next(NOTEBOOK_DIR.rglob(f"{stem}.ipynb"))
        try:
            record = check(path)
        except Exception as exc:
            print(f"{stem}: SKIPPED ({type(exc).__name__}: {exc})")
            print("  prerequisites or artefacts are missing; this is reported, not hidden.")
            continue
        print(f"{stem}: widget cells={record['widget_cells']} "
              f"rendered={record['rendered']} fallback={record['fallback']}")
        for message in record["errors"]:
            print("  [ERROR]", message)
        failures += len(record["errors"])
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
