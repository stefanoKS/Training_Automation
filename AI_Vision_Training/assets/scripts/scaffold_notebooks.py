"""ノートブックの足場づくり / Notebook scaffolding.

このスクリプトは 16 冊のノートブックに、初心者向けの共通構造を入れます。
This script gives the 16 notebooks their shared beginner scaffolding:

1. ヘッダの所要時間をシラバスと一致させ、その日の時間割へのリンクを入れる
   keep the header duration in step with the syllabus and link to the day's timetable
2. ノートブック自身が持っている 1 日の時間割を「この日の位置」に置き換える
   replace a notebook's own full-day timetable with its position in the day
3. すべてのコードセルの先頭に、日本語 → 英語の指示バナーを付ける
   put a Japanese-then-English instruction banner at the top of every code cell

使い方 / Usage
--------------
    python assets\\scripts\\scaffold_notebooks.py --report
    python assets\\scripts\\scaffold_notebooks.py

``--report`` は書き換えず、割り当てる役割を表示します。
``--report`` classifies the cells without writing anything.

役割 / Roles
------------
``run-only``      実行のみ / Run only
``change-value``  この値を変更 / Change this value
``write-code``    自分でコードを書く / Write your code

割り当てはセルの ``metadata["aivision_role"]`` に保存されます。次回以降はそれを使うため、
手で直した割り当てが上書きされることはありません。
The role is stored in ``metadata["aivision_role"]``; later runs reuse it, so a manual correction is
never overwritten by the heuristic.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import nbformat

SENTINEL = "# ▸ "

BANNERS = {
    "run-only": [
        "# ▸ 実行のみ / Run only：このまま実行します。書き換えません。",
        "# ▸ Run only: press Shift + Enter and leave the code as it is.",
    ],
    "change-value": [
        "# ▸ この値を変更 / Change this value：値を変えて、結果を予想してから実行します。",
        "# ▸ Change this value: edit it below, predict the result, then run.",
    ],
    "write-code": [
        "# ▸ 自分でコードを書く / Write your code：空欄を自分で埋めてから実行します。",
        "# ▸ Write your code: fill in the blanks, then run.",
    ],
}

ROLE_LABEL = {
    "run-only": "実行のみ / Run only",
    "change-value": "この値を変更 / Change this value",
    "write-code": "自分でコードを書く / Write your code",
}

# ノートブックごとの時間割情報 / per-notebook schedule facts
# minutes は COURSE_SYLLABUS.md と一致していなければならない（test_schedule.py が検証）。
SCHEDULE = {
    "00_Environment_Setup": {
        "minutes": 60,
        "kind": "準備（授業時間外）/ preflight, outside lesson hours",
        "anchor": "preflight",
        "link_text": "準備 / preflight",
        "position": "—",
        "prerequisites": "なし / none",
    },
    "Day01_01_Introduction_to_AI": {
        "minutes": 115, "day": 1, "position": "1 / 3",
        "anchor": "day1", "link_text": "第1日 / Day 1",
        "prerequisites": "`00_Environment_Setup.ipynb`",
    },
    "Day01_02_Pixels_and_Images": {
        "minutes": 110, "day": 1, "position": "2 / 3",
        "anchor": "day1", "link_text": "第1日 / Day 1",
        "prerequisites": "`Day01_01_Introduction_to_AI.ipynb`",
    },
    "Day01_03_Computer_Vision_Tasks": {
        "minutes": 65, "day": 1, "position": "3 / 3",
        "anchor": "day1", "link_text": "第1日 / Day 1",
        "prerequisites": "`Day01_02_Pixels_and_Images.ipynb`",
    },
    "Day02_01_Python_Basics": {
        "minutes": 125, "day": 2, "position": "1 / 3",
        "anchor": "day2", "link_text": "第2日 / Day 2",
        "prerequisites": "第1日 / Day 1",
    },
    "Day02_02_Conditions_Loops_Functions": {
        "minutes": 115, "day": 2, "position": "2 / 3",
        "anchor": "day2", "link_text": "第2日 / Day 2",
        "prerequisites": "`Day02_01_Python_Basics.ipynb`",
    },
    "Day02_03_OpenCV_Image_Processing": {
        "minutes": 60, "day": 2, "position": "3 / 3",
        "anchor": "day2", "link_text": "第2日 / Day 2",
        "prerequisites": "`Day02_02_Conditions_Loops_Functions.ipynb`",
    },
    "Day03_01_YOLO_Concepts": {
        "minutes": 80, "day": 3, "position": "1 / 3",
        "anchor": "day3", "link_text": "第3日 / Day 3",
        "prerequisites": "第2日 / Day 2",
    },
    "Day03_02_YOLO_Inference": {
        "minutes": 85, "day": 3, "position": "2 / 3",
        "anchor": "day3", "link_text": "第3日 / Day 3",
        "prerequisites": "`Day03_01_YOLO_Concepts.ipynb`、`yolo11n.pt` のダウンロード完了",
    },
    "Day03_03_YOLO_Experiments": {
        "minutes": 110, "day": 3, "position": "3 / 3",
        "anchor": "day3", "link_text": "第3日 / Day 3",
        "prerequisites": "`Day03_02_YOLO_Inference.ipynb`",
    },
    "Day04_01_YOLO_Dataset_Annotation": {
        "minutes": 80, "day": 4, "position": "1 / 3",
        "anchor": "day4", "link_text": "第4日 / Day 4",
        "prerequisites": "第3日 / Day 3",
    },
    "Day04_02_YOLO_Training": {
        "minutes": 115, "day": 4, "position": "2 / 3",
        "anchor": "day4", "link_text": "第4日 / Day 4",
        "prerequisites": "`Day04_01_YOLO_Dataset_Annotation.ipynb`、`assets/yolo_dataset` 生成済み",
    },
    "Day04_03_YOLO_Evaluation": {
        "minutes": 95, "day": 4, "position": "3 / 3",
        "anchor": "day4", "link_text": "第4日 / Day 4",
        "prerequisites": "`Day04_02_YOLO_Training.ipynb` の学習済みモデル",
    },
    "Day05_01_Anomaly_Detection_Concepts": {
        "minutes": 70, "day": 5, "position": "1 / 3",
        "anchor": "day5", "link_text": "第5日 / Day 5",
        "prerequisites": "第4日 / Day 4",
    },
    "Day05_02_PatchCore_Training": {
        "minutes": 130, "day": 5, "position": "2 / 3",
        "anchor": "day5", "link_text": "第5日 / Day 5",
        "prerequisites": "`Day05_01_Anomaly_Detection_Concepts.ipynb`、`aivision-anomalib` カーネル",
    },
    "Day05_03_YOLO_vs_PatchCore": {
        "minutes": 100, "day": 5, "position": "3 / 3",
        "anchor": "day5", "link_text": "第5日 / Day 5",
        "prerequisites": "`Day04_03` と `Day05_02` の保存済み結果",
    },
}

# 手で決めた役割（ヒューリスティクスより優先）/ hand-assigned roles beat the heuristic
ROLE_OVERRIDES: dict[str, dict[str, str]] = {}

TIMELINE_MARKERS = ("## 本日の学習タイムライン", "## このノートブックの位置")
DURATION_ROW_RE = re.compile(r"^\| 学習時間（目安） / Estimated duration \|.*$", re.M)
KERNEL_ROW_RE = re.compile(r"^\| 使用カーネル / Jupyter kernel \|.*$", re.M)
TIMETABLE_ROW_RE = re.compile(r"^\| (?:この日の)?時間割 / Today's timetable \|.*$", re.M)

EXERCISE_RE = re.compile(r"^#\s*演習\s*\d", re.M)
EDIT_MARKER_RE = re.compile(r"ここを書き換えて|値を変えて|ここを変えて|edit these|change these")
PREDICT_RE = re.compile(r"予想|predict", re.I)
ASSIGN_RE = re.compile(
    r"^(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
    r"(?:-?\d+(?:\.\d+)?|\"[^\"]*\"|\[[-0-9.,\s]+\]|\([-0-9.,\s]+\))\s*$"
)
ANY_ASSIGN_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*=\s*.+$")
TUNABLE_KW_RE = re.compile(
    r"\b(?:conf|iou|imgsz|epochs|batch|lr0|threshold|thresholds|sigma|k|seed|size|tolerance)\s*=\s*-?\d"
)


# ---------------------------------------------------------------------------
# cells
# ---------------------------------------------------------------------------


def source_text(cell) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def set_source(cell, text: str) -> None:
    if not text:
        cell["source"] = []
        return
    parts = text.split("\n")
    cell["source"] = [line + "\n" for line in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def strip_banner(text: str) -> str:
    lines = [line for line in text.split("\n") if not line.startswith(SENTINEL)]
    return "\n".join(lines)


def classify(cell, part: int | None, previous_markdown: str = "") -> str:
    text = strip_banner(source_text(cell))
    tags = cell.get("metadata", {}).get("tags", [])
    if "raises-exception" in tags:
        return "run-only"
    if EXERCISE_RE.search(text):
        return "write-code"
    if EDIT_MARKER_RE.search(text):
        return "change-value"
    body = [line for line in text.split("\n") if line.strip() and not line.lstrip().startswith("#")]
    assignments = [line for line in body if ASSIGN_RE.match(line)]
    if (
        assignments
        and len(body) <= 20
        and part is not None
        and part >= 1
        and not any(line.startswith(("def ", "class ", "for ", "while ", "if ")) for line in body)
    ):
        return "change-value"
    if (
        previous_markdown
        and PREDICT_RE.search(previous_markdown)
        and any(ANY_ASSIGN_RE.match(line) for line in body)
    ):
        return "change-value"
    if TUNABLE_KW_RE.search("\n".join(body)) and part is not None and part >= 1:
        return "change-value"
    return "run-only"


def apply_banner(cell, role: str) -> bool:
    """バナーと役割を書き込む。変更があれば True / write the banner and role; return whether it changed."""
    text = strip_banner(source_text(cell))
    lines = text.split("\n")
    insert_at = 0
    while insert_at < len(lines) and lines[insert_at].lstrip().startswith(("%", "!")):
        insert_at += 1
    banner = list(BANNERS[role])
    set_source(cell, "\n".join(lines[:insert_at] + banner + lines[insert_at:]))
    metadata = cell.setdefault("metadata", {})
    metadata_changed = metadata.get("aivision_role") != role
    metadata["aivision_role"] = role
    return metadata_changed


# ---------------------------------------------------------------------------
# markdown
# ---------------------------------------------------------------------------


def position_markdown(name: str, info: dict, depth_links: str) -> str:
    link = f"[`COURSE_SYLLABUS.md` {info['link_text']}]({depth_links}COURSE_SYLLABUS.md#{info['anchor']})"
    if info["anchor"] == "preflight":
        return (
            "## このノートブックの位置 / Where this notebook sits\n"
            "\n"
            "| 項目 / Item | 内容 / Details |\n"
            "| --- | --- |\n"
            f"| 区分 / Kind | {info['kind']} |\n"
            f"| 所要時間 / Duration | {info['minutes']} 分 / {info['minutes']} minutes |\n"
            f"| 前提 / Prerequisites | {info['prerequisites']} |\n"
            f"| 時間割 / Timetable | {link} |\n"
            "\n"
            "このノートブックは授業時間の外で行います。5 日間の 360 分には含めません。\n"
            "\n"
            "This notebook is done outside the lesson hours and is not part of any day's 360 minutes.\n"
        )
    return (
        "## このノートブックの位置 / Where this notebook sits\n"
        "\n"
        "| 項目 / Item | 内容 / Details |\n"
        "| --- | --- |\n"
        f"| 日 / Day | {info['link_text']} |\n"
        f"| この日の順番 / Position today | {info['position']}（この日のノートブックのうち）/ of today's notebooks |\n"
        f"| 所要時間 / Duration | {info['minutes']} 分 / {info['minutes']} minutes |\n"
        f"| 前提 / Prerequisites | {info['prerequisites']} |\n"
        f"| この日の時間割 / Today's timetable | {link} |\n"
        "\n"
        "1 日の時間割は `COURSE_SYLLABUS.md` に 1 つだけあります。このノートブックはその一部で、\n"
        "自分の時間割を持ちません。時刻が分からなくなったら、まずそこを見てください。\n"
        "\n"
        "The day's timetable exists once, in `COURSE_SYLLABUS.md`. This notebook is one part of it and\n"
        "does not keep its own schedule; look there first when you are unsure of the time.\n"
    )


def update_header(header: str, info: dict, depth_links: str) -> str:
    link = f"[`COURSE_SYLLABUS.md` {info['link_text']}]({depth_links}COURSE_SYLLABUS.md#{info['anchor']})"
    duration = f"| 学習時間（目安） / Estimated duration | {info['minutes']} 分 / {info['minutes']} minutes |"
    header = DURATION_ROW_RE.sub(lambda _match: duration, header, count=1)
    if "COURSE_SYLLABUS.md#" not in header:
        row_label = "時間割 / Timetable" if info["anchor"] == "preflight" else "この日の時間割 / Today's timetable"
        row = f"| {row_label} | {link} |"
        match = KERNEL_ROW_RE.search(header)
        if match:
            header = header[: match.end()] + "\n" + row + header[match.end():]
        else:
            header = header.rstrip("\n") + "\n" + row + "\n"
    return header


# ---------------------------------------------------------------------------
# per notebook
# ---------------------------------------------------------------------------


def scaffold(path: Path, course_root: Path, write: bool = True) -> dict:
    name = path.stem
    info = SCHEDULE[name]
    depth_links = "../../"
    notebook = nbformat.read(str(path), as_version=4)
    report = {"notebook": name, "roles": {}, "changed": 0}

    # --- header ---
    header_cell = notebook.cells[0]
    header = source_text(header_cell)
    new_header = update_header(header, info, depth_links)
    if new_header != header:
        set_source(header_cell, new_header)
        report["changed"] += 1

    # --- timeline cell -> position cell ---
    for cell in notebook.cells:
        if cell.cell_type != "markdown":
            continue
        text = source_text(cell)
        if text.startswith(TIMELINE_MARKERS[0]) or text.startswith(TIMELINE_MARKERS[1]):
            replacement = position_markdown(name, info, depth_links)
            if text != replacement:
                set_source(cell, replacement)
                report["changed"] += 1
            break

    # --- code cell banners ---
    overrides = ROLE_OVERRIDES.get(name, {})
    part = None
    previous_markdown = ""
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            text = source_text(cell)
            match = re.search(r"^## Part (\d+)", text, re.M)
            if match:
                part = int(match.group(1))
            previous_markdown = text
            continue
        role = (
            overrides.get(cell.get("id", ""))
            or cell.get("metadata", {}).get("aivision_role")
            or classify(cell, part, previous_markdown)
        )
        before = source_text(cell)
        metadata_changed = apply_banner(cell, role)
        report["roles"][role] = report["roles"].get(role, 0) + 1
        if source_text(cell) != before or metadata_changed:
            report["changed"] += 1
        previous_markdown = ""

    if write and report["changed"]:
        nbformat.write(notebook, str(path))
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Apply beginner scaffolding to the course notebooks.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--report", action="store_true", help="classify only; never write")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    from course_notebooks import course_notebooks

    reports = [scaffold(path, root, write=not args.report)
               for path in course_notebooks(root / "notebooks")]

    if args.json:
        print(json.dumps(reports, indent=2, ensure_ascii=False))
    else:
        totals: dict[str, int] = {}
        for report in reports:
            roles = report["roles"]
            for role, count in roles.items():
                totals[role] = totals.get(role, 0) + count
            detail = " ".join(f"{role}={count}" for role, count in sorted(roles.items()))
            print(f"{report['notebook']:<40} changed={report['changed']:<3} {detail}")
        print("-" * 70)
        print("totals:", totals)
        print("RESULT:", "REPORT ONLY" if args.report else "OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
