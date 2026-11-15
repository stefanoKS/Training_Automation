"""時間割の整合性テスト / Schedule consistency tests.

`COURSE_SYLLABUS.md` を **時間割の唯一の正** として読み、次を検証します。
`COURSE_SYLLABUS.md` is treated as the **single source of truth** and this module checks that:

* 各日の自習枠が 09:00–12:00 と 13:50–16:50 にちょうど収まる
  each day's self-study rows fill exactly 09:00–12:00 and 13:50–16:50
* 1 日の合計が 360 分で、必須が 270〜300 分に収まる
  the day totals 360 minutes with 270-300 minutes of required work
* 参照している `DayNN_NN` と `Part N` が実在する
  every referenced notebook and part really exists
* ノートブック側の所要時間がシラバスと一致する
  the duration in each notebook header matches the syllabus
* どのノートブックも 1 日の時間割を自前で持たない
  no notebook keeps its own full-day timetable
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
SYLLABUS = COURSE_ROOT / "COURSE_SYLLABUS.md"
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"
sys.path.insert(0, str(COURSE_ROOT / "assets" / "scripts"))
from course_notebooks import course_notebooks  # noqa: E402

SELF_STUDY_BLOCKS = (("09:00", "12:00"), ("13:50", "16:50"))
REQUIRED_RANGE = (270, 300)
BUFFER_RANGE = (60, 90)
DAY_TOTAL = 360

ANCHOR_RE = re.compile(r'<a id="(day\d)"></a>')
TIME_RE = re.compile(r"^(\d{2}):(\d{2})[–-](\d{2}):(\d{2})$")
NOTEBOOK_TOKEN_RE = re.compile(r"`?(Day\d{2}_\d{2})`?")
PART_RE = re.compile(r"Part\s*(\d+)\s*(?:[–-]\s*(\d+))?")
DURATION_ROW_RE = re.compile(r"(?:学習時間|所要時間)（目安）\s*/\s*Estimated duration\s*\|\s*(\d+)\s*分")
SCHEDULE_LINK = "COURSE_SYLLABUS.md#"


def _minutes(value: str) -> int:
    hours, minutes = value.split(":")
    return int(hours) * 60 + int(minutes)


def _table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        rows.append(cells)
    return rows


def _split_days(text: str) -> dict[str, str]:
    matches = list(ANCHOR_RE.finditer(text))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[match.end():end]
    return sections


def _schedule_rows(section: str) -> list[dict]:
    """時間割の表だけを取り出す / pull only the timetable tables out of one day."""
    rows = []
    for cells in _table_rows(section):
        if len(cells) < 4:
            continue
        time_match = TIME_RE.match(cells[0])
        if not time_match:
            continue
        if not cells[2] in {"必須", "任意", "休憩", "予備", "提出"}:
            continue
        rows.append(
            {
                "start": f"{time_match.group(1)}:{time_match.group(2)}",
                "end": f"{time_match.group(3)}:{time_match.group(4)}",
                "minutes": int(cells[1]),
                "type": cells[2],
                "content": cells[3],
            }
        )
    return rows


def _notebook_durations(section: str) -> dict[str, int]:
    durations: dict[str, int] = {}
    for cells in _table_rows(section):
        if len(cells) < 4:
            continue
        token = NOTEBOOK_TOKEN_RE.search(cells[1])
        if not token:
            continue
        duration = re.search(r"(\d+)\s*分", cells[2])
        if duration:
            durations[token.group(1)] = int(duration.group(1))
    return durations


@pytest.fixture(scope="module")
def syllabus_text() -> str:
    assert SYLLABUS.is_file(), "COURSE_SYLLABUS.md is missing"
    return SYLLABUS.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def days(syllabus_text: str) -> dict[str, str]:
    sections = _split_days(syllabus_text)
    assert sorted(sections) == ["day1", "day2", "day3", "day4", "day5"], sections.keys()
    return sections


# ---------------------------------------------------------------------------
# 時間の計算 / arithmetic
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("day", ["day1", "day2", "day3", "day4", "day5"])
def test_day_totals_360_minutes(day, days) -> None:
    rows = _schedule_rows(days[day])
    assert rows, f"{day}: no timetable rows parsed"
    total = sum(row["minutes"] for row in rows)
    assert total == DAY_TOTAL, f"{day}: total is {total} minutes, expected {DAY_TOTAL}"


@pytest.mark.parametrize("day", ["day1", "day2", "day3", "day4", "day5"])
def test_required_minutes_within_budget(day, days) -> None:
    rows = _schedule_rows(days[day])
    required = sum(row["minutes"] for row in rows if row["type"] == "必須")
    low, high = REQUIRED_RANGE
    assert low <= required <= high, f"{day}: required work is {required} minutes, expected {low}-{high}"


@pytest.mark.parametrize("day", ["day1", "day2", "day3", "day4", "day5"])
def test_buffer_minutes_within_budget(day, days) -> None:
    rows = _schedule_rows(days[day])
    buffer = sum(row["minutes"] for row in rows if row["type"] in {"休憩", "予備", "提出"})
    low, high = BUFFER_RANGE
    assert low <= buffer <= high, f"{day}: buffer is {buffer} minutes, expected {low}-{high}"


@pytest.mark.parametrize("day", ["day1", "day2", "day3", "day4", "day5"])
def test_rows_tile_the_self_study_blocks(day, days) -> None:
    rows = _schedule_rows(days[day])
    expected_start = SELF_STUDY_BLOCKS[0][0]
    block_index = 0
    cursor = expected_start
    for row in rows:
        if cursor == SELF_STUDY_BLOCKS[0][1] and block_index == 0:
            block_index = 1
            cursor = SELF_STUDY_BLOCKS[1][0]
        assert row["start"] == cursor, f"{day}: row starts at {row['start']}, expected {cursor}"
        span = _minutes(row["end"]) - _minutes(row["start"])
        assert span == row["minutes"], (
            f"{day}: {row['start']}-{row['end']} spans {span} minutes but the table says {row['minutes']}"
        )
        cursor = row["end"]
    assert cursor == SELF_STUDY_BLOCKS[1][1], f"{day}: last row ends at {cursor}"


def test_fixed_instructor_and_lunch_times(syllabus_text: str) -> None:
    for window in ("08:00–09:00", "12:00–12:50", "12:50–13:50"):
        assert window in syllabus_text, f"fixed window {window} is missing from the daily rhythm"
    assert "360 分" in syllabus_text or "360 minutes" in syllabus_text


# ---------------------------------------------------------------------------
# 参照の実在 / references exist
# ---------------------------------------------------------------------------


def _notebook_path(token: str) -> Path:
    matches = course_notebooks(NOTEBOOK_DIR, f"{token}_*.ipynb")
    assert len(matches) == 1, f"{token}: expected exactly one notebook, found {matches}"
    return matches[0]


def _parts_in(path: Path) -> set[int]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    parts: set[int] = set()
    for cell in notebook["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell["source"])
        for line in source.splitlines():
            if line.startswith("## Part"):
                match = re.search(r"Part\s*(\d+)", line)
                if match:
                    parts.add(int(match.group(1)))
    return parts


@pytest.mark.parametrize("day", ["day1", "day2", "day3", "day4", "day5"])
def test_referenced_notebooks_and_parts_exist(day, days) -> None:
    problems = []
    for row in _schedule_rows(days[day]):
        tokens = NOTEBOOK_TOKEN_RE.findall(row["content"])
        if not tokens:
            continue
        assert len(set(tokens)) == 1, f"{day}: row mixes notebooks: {row['content']}"
        path = _notebook_path(tokens[0])
        available = _parts_in(path)
        for low, high in PART_RE.findall(row["content"]):
            low_int = int(low)
            high_int = int(high) if high else low_int
            for part in range(low_int, high_int + 1):
                if part not in available:
                    problems.append(f"{day}: {tokens[0]} has no Part {part} (row: {row['content']})")
    assert not problems, "\n".join(problems)


@pytest.mark.parametrize("day", ["day1", "day2", "day3", "day4", "day5"])
def test_notebook_durations_match_required_minutes(day, days) -> None:
    rows = _schedule_rows(days[day])
    required = sum(row["minutes"] for row in rows if row["type"] == "必須")
    durations = _notebook_durations(days[day])
    assert durations, f"{day}: no notebook durations listed"
    # 準備確認のようなノートブック以外の必須枠があるため、合計は必須以下であること
    # A required row may not belong to a notebook (e.g. the readiness check).
    assert sum(durations.values()) <= required, (
        f"{day}: notebooks claim {sum(durations.values())} minutes but only {required} are required"
    )
    assert sum(durations.values()) >= required - 15, (
        f"{day}: notebooks claim {sum(durations.values())} minutes, {required} are required; "
        "unaccounted required time should be at most 15 minutes"
    )


# ---------------------------------------------------------------------------
# ノートブック側 / notebook side
# ---------------------------------------------------------------------------


def _all_notebooks() -> list[Path]:
    return course_notebooks(NOTEBOOK_DIR)


def test_discovery_ignores_checkpoints_but_rejects_real_duplicates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    directory = tmp_path / "notebooks"
    lesson = directory / "Day01_AI_Fundamentals" / "Day01_01_Example.ipynb"
    checkpoint = lesson.parent / ".ipynb_checkpoints" / "Day01_01_Example-checkpoint.ipynb"
    root_checkpoint = directory / ".ipynb_checkpoints" / lesson.name
    unrelated = directory / "learner_notes" / lesson.name
    for path in (lesson, checkpoint, root_checkpoint, unrelated):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "NOTEBOOK_DIR", directory)
    assert _all_notebooks() == [lesson]
    assert _notebook_path("Day01_01") == lesson
    duplicate = lesson.with_name("Day01_01_Duplicate.ipynb")
    duplicate.write_text("{}", encoding="utf-8")
    with pytest.raises(AssertionError, match="expected exactly one notebook"):
        _notebook_path("Day01_01")
    assert checkpoint.read_text(encoding="utf-8") == "{}"


@pytest.mark.parametrize("path", _all_notebooks(), ids=lambda p: p.stem)
def test_duration_and_schedule_link_present(path: Path, days) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    header = "".join(notebook["cells"][0]["source"])
    assert DURATION_ROW_RE.search(header), f"{path.name}: no duration row in the header"
    assert SCHEDULE_LINK in header, f"{path.name}: header does not link to the daily schedule"
    assert "本日の学習タイムライン" not in header, f"{path.name}: header still has its own timeline"
    assert "Learning timeline for today" not in header


@pytest.mark.parametrize("path", _all_notebooks(), ids=lambda p: p.stem)
def test_no_notebook_keeps_a_full_day_timetable(path: Path) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "markdown":
            continue
        source = "".join(cell["source"])
        has_day_start = "08:00" in source
        has_day_end = "16:50" in source
        assert not (has_day_start and has_day_end), (
            f"{path.name} cell {index}: contains a full-day timetable; "
            "the only timetable lives in COURSE_SYLLABUS.md"
        )


@pytest.mark.parametrize("path", _all_notebooks(), ids=lambda p: p.stem)
def test_header_duration_matches_syllabus(path: Path, days) -> None:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    header = "".join(notebook["cells"][0]["source"])
    match = DURATION_ROW_RE.search(header)
    assert match, f"{path.name}: no duration row"
    declared = int(match.group(1))

    located = None
    for day in days.values():
        for token, minutes in _notebook_durations(day).items():
            if path.stem.startswith(token):
                located = (token, minutes)
    if located is None:
        # 準備用ノートブック（00_Setup）は 5 日間の時間割に含まれない
        # The preparatory notebook is not part of the five-day timetable.
        assert path.parent.name == "00_Setup", f"{path.name}: not listed in any day's timetable"
        return
    token, minutes = located
    assert declared == minutes, f"{path.name}: header says {declared} minutes, syllabus says {minutes}"
