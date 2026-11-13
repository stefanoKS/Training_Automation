"""ノートブック検証 / Notebook validation.

2 種類の検証を行います。
Two kinds of validation are performed:

1. **構造検証 / structural**  (default, always fast)
   - すべての `.ipynb` が存在するか / every required notebook exists
   - JSON と nbformat が正しいか / valid notebook JSON
   - Markdown セルが空でないか / markdown cells are populated
   - 日本語と英語が両方あるか（日本語が先か） / Japanese and English, Japanese first
   - 必須セクション（演習・質問・トラブルシューティング等）があるか
   - 参照している素材ファイルが実在するか / referenced assets exist
   - 提出テンプレートが存在するか / submission templates exist
   - コードセルが構文として正しいか / code cells compile
   - 禁止パターン（`cv2.imshow`、絶対パス）が無いか

2. **実行検証 / execution**  (``--execute``)
   - nbclient で実際にセルを実行する / really execute the cells with nbclient
   - 失敗したセル、タイムアウト、未検証セルを正直に報告する
     honestly report failed, timed-out and unverified cells

使い方 / Usage
--------------
    python validate_notebooks.py
    python validate_notebooks.py --execute lightweight
    python validate_notebooks.py --execute all --report ../../validation_report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import traceback
from pathlib import Path

import nbformat

# ---------------------------------------------------------------------------
# 期待するファイル一覧 / expected files
# ---------------------------------------------------------------------------

NOTEBOOKS = [
    ("00_Setup/00_Environment_Setup.ipynb", 0, "lightweight"),
    ("Day01_AI_Fundamentals/Day01_01_Introduction_to_AI.ipynb", 1, "lightweight"),
    ("Day01_AI_Fundamentals/Day01_02_Pixels_and_Images.ipynb", 1, "lightweight"),
    ("Day01_AI_Fundamentals/Day01_03_Computer_Vision_Tasks.ipynb", 1, "lightweight"),
    ("Day02_Python_OpenCV/Day02_01_Python_Basics.ipynb", 2, "lightweight"),
    ("Day02_Python_OpenCV/Day02_02_Conditions_Loops_Functions.ipynb", 2, "lightweight"),
    ("Day02_Python_OpenCV/Day02_03_OpenCV_Image_Processing.ipynb", 2, "lightweight"),
    ("Day03_YOLO_Basics/Day03_01_YOLO_Concepts.ipynb", 3, "lightweight"),
    ("Day03_YOLO_Basics/Day03_02_YOLO_Inference.ipynb", 3, "download"),
    ("Day03_YOLO_Basics/Day03_03_YOLO_Experiments.ipynb", 3, "download"),
    ("Day04_YOLO_Training/Day04_01_YOLO_Dataset_Annotation.ipynb", 4, "lightweight"),
    ("Day04_YOLO_Training/Day04_02_YOLO_Training.ipynb", 4, "training"),
    ("Day04_YOLO_Training/Day04_03_YOLO_Evaluation.ipynb", 4, "training"),
    ("Day05_PatchCore/Day05_01_Anomaly_Detection_Concepts.ipynb", 5, "lightweight"),
    ("Day05_PatchCore/Day05_02_PatchCore_Training.ipynb", 5, "anomalib"),
    ("Day05_PatchCore/Day05_03_YOLO_vs_PatchCore.ipynb", 5, "anomalib"),
]

REQUIRED_SECTIONS = [
    ("学習目標", "Learning objectives"),
    ("演習 / Exercises", None),
    ("理解度チェック", "Understanding questions"),
    ("困ったときは / Troubleshooting", None),
    ("完了チェックリスト / Completion checklist", None),
    ("さらに学ぶ / Further learning", None),
]

SUBMISSION_FILES = [
    "submissions/day01/Day01_Report_Template.md",
    "submissions/day02/Day02_Report_Template.md",
    "submissions/day03/Day03_Report_Template.md",
    "submissions/day04/Day04_Report_Template.md",
    "submissions/day05/Day05_Report_Template.md",
]

DOC_FILES = [
    "README.md",
    "START_HERE.md",
    "COURSE_SYLLABUS.md",
    "docs/reference_materials.md",
    "docs/implementation_report.md",
    "docs/instructor/day01_instructor_guide.md",
    "docs/instructor/day02_instructor_guide.md",
    "docs/instructor/day03_instructor_guide.md",
    "docs/instructor/day04_instructor_guide.md",
    "docs/instructor/day05_instructor_guide.md",
    "docs/troubleshooting/installation.md",
    "requirements/tested_versions.md",
    "assets/helpers/aivision.py",
]

ASSET_FILES = [
    "assets/diagrams/diagram_pixel_grid.png",
    "assets/diagrams/diagram_grayscale_values.png",
    "assets/diagrams/diagram_coordinate_system.png",
    "assets/diagrams/diagram_classification.png",
    "assets/diagrams/diagram_detection.png",
    "assets/diagrams/diagram_segmentation.png",
    "assets/diagrams/diagram_anomaly_heatmap.png",
    "assets/diagrams/diagram_control_flow.png",
    "assets/diagrams/diagram_dataset_split.png",
    "assets/diagrams/diagram_yolo_annotation.png",
    "assets/diagrams/diagram_pixel_distance.png",
    "assets/diagrams/calibration_image.png",
    "assets/diagrams/diagram_patchcore_concept.png",
    "assets/diagrams/diagram_yolo_vs_patchcore.png",
    "assets/diagrams/teach_setup_jupyter_ui.png",
    "assets/diagrams/teach_brightness_shift.png",
    "assets/diagrams/teach_iou_rects.png",
    "assets/diagrams/teach_score_map_overlay.png",
    "assets/yolo_dataset/data.yaml",
    "assets/anomaly_dataset/pvc_sheet/dataset_layout.json",
]

FORBIDDEN_CODE = [
    ("cv2.imshow", "cv2.imshow() freezes Jupyter; use Matplotlib instead"),
    ("C:\\\\Users", "hard-coded user path"),
    ("C:/Users", "hard-coded user path"),
]

JP_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9fff]")
EN_RE = re.compile(r"[A-Za-z]{3,}")
ASSET_REF_RE = re.compile(r'ASSETS\s*/\s*((?:"[^"]+"\s*(?:/\s*)*)+)')
STR_RE = re.compile(r'"([^"]+)"')
# Markdown の画像参照 / markdown image references
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
# 言語ラベルだけの接頭辞（残っていてはいけない）/ a standalone language label that must be gone
LANG_LABEL_RE = re.compile(
    r"^[ \t]*(?:>[ \t]*)*(?:\*\*)?(?:日本語|English)(?:\*\*)?[ \t]*[：:]",
    re.M,
)
# コードセルの指示バナー / the instruction banner of a code cell
BANNER_MARK = "# ▸ "
ROLE_BANNERS = {
    "run-only": "実行のみ / Run only",
    "change-value": "この値を変更 / Change this value",
    "write-code": "自分でコードを書く / Write your code",
}
LONG_ENGLISH_LINE_LENGTH = 60


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


class Result:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.failed: list[str] = []
        self.skipped: list[str] = []
        self.details: list[dict] = []

    def ok(self, msg: str) -> None:
        self.passed.append(msg)

    def fail(self, msg: str) -> None:
        self.failed.append(msg)

    def skip(self, msg: str) -> None:
        self.skipped.append(msg)


def _markdown_text(nb) -> str:
    return "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")


def _code_text(nb) -> str:
    return "\n".join(c.source for c in nb.cells if c.cell_type == "code")


def check_notebook(path: Path, result: Result) -> dict:
    """1 つのノートブックを検証する / validate one notebook."""
    info = {"path": str(path), "checks": {}, "cells": 0, "code_cells": 0}
    if not path.is_file():
        result.fail(f"missing notebook: {path}")
        info["checks"]["exists"] = False
        return info
    info["checks"]["exists"] = True

    try:
        nb = nbformat.read(str(path), as_version=4)
        nbformat.validate(nb)
        info["checks"]["valid_json"] = True
    except Exception as exc:
        result.fail(f"{path.name}: invalid notebook JSON ({exc})")
        info["checks"]["valid_json"] = False
        return info

    info["cells"] = len(nb.cells)
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    md_cells = [c for c in nb.cells if c.cell_type == "markdown"]
    info["code_cells"] = len(code_cells)

    # --- markdown cells are populated ---
    empty = [i for i, c in enumerate(md_cells) if not c.source.strip()]
    if empty:
        result.fail(f"{path.name}: {len(empty)} empty markdown cell(s)")
    else:
        result.ok(f"{path.name}: markdown cells populated")

    text = _markdown_text(nb)

    # --- 言語ラベルが残っていない / no standalone language labels remain ---
    leftover = [m.group(0).strip() for m in LANG_LABEL_RE.finditer(text)]
    if leftover:
        result.fail(f"{path.name}: language label(s) still present -> {leftover[:3]}")
    else:
        result.ok(f"{path.name}: no language labels")

    # --- 日本語と英語がそろい、日本語が先 / bilingual and Japanese first ---
    bilingual_problems = []
    for idx, cell in enumerate(md_cells):
        src = cell.source
        has_japanese = bool(JP_RE.search(src))
        has_english = bool(EN_RE.search(src))
        if not has_japanese and not has_english:
            continue
        if has_japanese and not has_english:
            bilingual_problems.append(f"cell {idx}: Japanese without English")
            continue
        if has_english and not has_japanese:
            bilingual_problems.append(f"cell {idx}: English without Japanese")
            continue
        lines = src.split("\n")
        first_japanese = next(k for k, line in enumerate(lines) if JP_RE.search(line))
        first_long_english = next(
            (k for k, line in enumerate(lines)
             if not JP_RE.search(line)
             and len(line.strip()) >= LONG_ENGLISH_LINE_LENGTH
             and EN_RE.search(line)),
            None,
        )
        if first_long_english is not None and first_long_english < first_japanese:
            bilingual_problems.append(f"cell {idx}: English paragraph before Japanese")
    if bilingual_problems:
        result.fail(f"{path.name}: bilingual problems -> {bilingual_problems[:4]}")
    else:
        result.ok(f"{path.name}: bilingual Japanese-first")

    # --- コードセルの指示バナー / instruction banner in every code cell ---
    banner_problems = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        role = cell.get("metadata", {}).get("aivision_role")
        first_lines = cell.source.split("\n")
        marks = [line for line in first_lines if line.startswith(BANNER_MARK)]
        if role not in ROLE_BANNERS:
            banner_problems.append(f"cell {idx}: no aivision_role metadata")
            continue
        if len(marks) != 2:
            banner_problems.append(f"cell {idx}: expected 2 banner lines, found {len(marks)}")
            continue
        if ROLE_BANNERS[role] not in marks[0]:
            banner_problems.append(f"cell {idx}: banner does not match role {role!r}")
    if banner_problems:
        result.fail(f"{path.name}: banner problems -> {banner_problems[:4]}")
    else:
        result.ok(f"{path.name}: every code cell has a role banner")

    # --- required sections ---
    missing_sections = [
        label for label, alt in REQUIRED_SECTIONS
        if label not in text and (alt is None or alt not in text)
    ]
    if missing_sections:
        result.fail(f"{path.name}: missing sections {missing_sections}")
    else:
        result.ok(f"{path.name}: required sections present")

    # --- at least three exercises, and expected-output guidance ---
    exercise_numbers = {n for n in (1, 2, 3) if f"演習 {n}" in text}
    if len(exercise_numbers) < 3:
        result.fail(f"{path.name}: fewer than 3 exercises found ({sorted(exercise_numbers)})")
    else:
        result.ok(f"{path.name}: 3 exercises")
    if "実行結果の例" not in text:
        result.fail(f"{path.name}: no expected-output section")
    else:
        result.ok(f"{path.name}: expected-output section")

    # --- code cells compile ---
    compile_errors = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        src = cell.source
        if src.lstrip().startswith(("%", "!")):
            continue
        try:
            compile(src, f"{path.name}[cell {idx}]", "exec")
        except SyntaxError as exc:
            compile_errors.append(f"cell {idx}: {exc.msg} (line {exc.lineno})")
    if compile_errors:
        result.fail(f"{path.name}: code compile errors -> {compile_errors[:3]}")
    else:
        result.ok(f"{path.name}: all code cells compile")

    # --- forbidden patterns ---
    code_text = _code_text(nb)
    hits = [f"{token} ({why})" for token, why in FORBIDDEN_CODE if token in code_text]
    if hits:
        result.fail(f"{path.name}: forbidden pattern(s) {hits}")
    else:
        result.ok(f"{path.name}: no forbidden patterns")

    # --- referenced assets exist ---
    course_root = path.parents[2]          # .../AI_Vision_Training
    unresolved = []
    for match in ASSET_REF_RE.finditer(code_text):
        parts = STR_RE.findall(match.group(1))
        if not parts:
            continue
        candidate = course_root / "assets"
        for part in parts:
            candidate = candidate / part
        if not candidate.exists():
            unresolved.append(str(candidate))
    info["unresolved_assets"] = unresolved
    if unresolved:
        result.fail(f"{path.name}: referenced assets missing -> {unresolved[:3]}")
    else:
        result.ok(f"{path.name}: referenced assets exist")

    # --- Markdown の画像が、ノートブックの場所から解決できるか ---
    # every image referenced from Markdown must exist relative to this notebook
    markdown_images = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "markdown":
            continue
        for target in MD_IMAGE_RE.findall(cell.source):
            if target.startswith(("http://", "https://", "data:")):
                continue
            resolved = (path.parent / target).resolve()
            markdown_images.append((idx, target, resolved))
    broken = [f"cell {idx}: {target}" for idx, target, resolved in markdown_images
              if not resolved.is_file()]
    if broken:
        result.fail(f"{path.name}: broken markdown image(s) -> {broken[:3]}")
    else:
        result.ok(f"{path.name}: markdown images resolve ({len(markdown_images)})")
    info["markdown_images"] = [target for _idx, target, _resolved in markdown_images]

    # --- 図が、その Part のコードより先に見えるか ---
    # A figure must sit between its Part heading and that Part's first code cell.
    part_headings = []
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type == "markdown" and re.search(r"^## Part ", cell.source, re.M):
            part_headings.append(idx)
    order_problems = []
    for cell_index, target, _resolved in markdown_images:
        heading = max((p for p in part_headings if p <= cell_index), default=None)
        if heading is None:
            continue
        between = [i for i in range(heading + 1, cell_index)
                   if nb.cells[i].cell_type == "code"]
        if between:
            order_problems.append(f"cell {cell_index} ({target}) comes after code in the same Part")
    if order_problems:
        result.fail(f"{path.name}: figure after code -> {order_problems[:2]}")
    elif markdown_images:
        result.ok(f"{path.name}: every figure comes before its Part's code")

    return info


# ---------------------------------------------------------------------------
# execution
# ---------------------------------------------------------------------------


def execute_notebook(path: Path, course_root: Path, timeout: int = 1800) -> dict:
    """nbclient で実行する / run the notebook with nbclient.

    ``tags: ["raises-exception"]`` が付いたセルだけ、エラーを許します。
    それ以外のセルでエラーが出たら失敗として扱います。

    Errors are tolerated ONLY in cells tagged ``raises-exception``. Anywhere else they fail the run.
    """
    import nbclient

    nb = nbformat.read(str(path), as_version=4)
    kernel = nb.metadata.get("kernelspec", {}).get("name", "aivision")
    started = time.time()
    record = {"path": str(path), "kernel": kernel, "status": "unknown",
              "seconds": None, "error": None, "failed_cell": None,
              "unverified_cells": [], "expected_error_cells": []}
    try:
        client = nbclient.NotebookClient(
            nb,
            kernel_name=kernel,
            timeout=timeout,
            allow_errors=True,          # 判定は下で自前に行う / we judge the errors ourselves
            resources={"metadata": {"path": str(course_root)}},
        )
        client.execute()

        unexpected = []
        for index, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            errors = [o for o in cell.get("outputs", []) if o.get("output_type") == "error"]
            if not errors:
                continue
            if "raises-exception" in cell.metadata.get("tags", []):
                record["expected_error_cells"].append(index)
                continue
            unexpected.append((index, errors[0].get("ename"), errors[0].get("evalue")))

        if unexpected:
            record["status"] = "failed"
            record["failed_cell"] = unexpected[0][0]
            record["error"] = "; ".join(
                f"cell {index}: {ename}: {evalue}" for index, ename, evalue in unexpected[:3]
            )
        else:
            record["status"] = "passed"
    except Exception as exc:
        record["status"] = "failed"
        record["error"] = f"{type(exc).__name__}: {exc}"
        record["traceback"] = traceback.format_exc()[-3000:]
        for idx, cell in enumerate(nb.cells):
            if cell.cell_type == "code" and cell.get("outputs"):
                if any(o.get("output_type") == "error" for o in cell["outputs"]):
                    record["failed_cell"] = idx
                    break
        executed = {i for i, c in enumerate(nb.cells)
                    if c.cell_type == "code" and c.get("execution_count") is not None}
        record["unverified_cells"] = [
            i for i, c in enumerate(nb.cells) if c.cell_type == "code" and i not in executed
        ]
    record["seconds"] = round(time.time() - started, 1)
    return record


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Week 1 course notebooks.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--execute", choices=["none", "lightweight", "download", "training",
                                              "anomalib", "all"], default="none")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    nb_dir = root / "notebooks"
    result = Result()

    # --- expected file inventory ---
    for rel, _day, _cat in NOTEBOOKS:
        if not (nb_dir / rel).is_file():
            result.fail(f"missing notebook: notebooks/{rel}")
    if not result.failed:
        result.ok(f"all {len(NOTEBOOKS)} notebooks exist")

    for rel in DOC_FILES:
        if not (root / rel).is_file():
            result.fail(f"missing document: {rel}")
    for rel in SUBMISSION_FILES:
        if not (root / rel).is_file():
            result.fail(f"missing submission template: {rel}")
    for rel in ASSET_FILES:
        if not (root / rel).exists():
            result.fail(f"missing asset: {rel}")
    if not any("missing asset" in m for m in result.failed):
        result.ok("all required assets exist")

    # --- per-notebook structural checks ---
    notebook_info = []
    for rel, _day, category in NOTEBOOKS:
        notebook_info.append(check_notebook(nb_dir / rel, result))

    # --- execution ---
    execution = []
    if args.execute != "none":
        if args.execute == "all":
            wanted = {category for _rel, _day, category in NOTEBOOKS}
        else:
            wanted = {args.execute}
        for rel, _day, category in NOTEBOOKS:
            path = nb_dir / rel
            if not path.is_file():
                continue
            if category not in wanted:
                result.skip(f"execution skipped ({category}): {rel}")
                continue
            timeout = args.timeout if category == "lightweight" else max(args.timeout, 3600)
            record = execute_notebook(path, root, timeout=timeout)
            execution.append(record)
            if record["status"] == "passed":
                result.ok(f"executed: {rel} ({record['seconds']}s)")
            else:
                result.fail(f"execution failed: {rel} -> {record['error']}")

    summary = {
        "notebooks": notebook_info,
        "execution": execution,
        "passed": result.passed,
        "failed": result.failed,
        "skipped": result.skipped,
        "ok": not result.failed,
    }

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("=" * 70)
        print("NOTEBOOK VALIDATION")
        print("=" * 70)
        for msg in result.passed:
            print(f"  [PASS] {msg}")
        for msg in result.skipped:
            print(f"  [SKIP] {msg}")
        for msg in result.failed:
            print(f"  [FAIL] {msg}")
        print("-" * 70)
        print(f"passed={len(result.passed)} failed={len(result.failed)} skipped={len(result.skipped)}")
        print("RESULT:", "OK" if not result.failed else "PROBLEMS FOUND")
    return 0 if not result.failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
