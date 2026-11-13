"""言語ラベルの整理テスト / Language-label cleanup tests.

`assets/scripts/normalize_language_labels.py` が、次の 2 つを両立することを確かめます。
These tests check that the cleanup tool does both jobs at once:

* 繰り返しの言語ラベルを消す / removes the repetitive ``日本語：`` / ``English:`` prefixes
* 日本語と英語の本文、順序、コード、数式、URL を壊さない
  keeps both languages, their order, code, math and URLs intact

fixture には「整形済みラベル」「コードフェンス」「引用」「意味のある日本語の語」を入れています。
The fixtures cover formatted labels, code fences, blockquotes and legitimate Japanese terms.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = COURSE_ROOT / "assets" / "scripts"

sys.path.insert(0, str(SCRIPTS))

import normalize_language_labels as nll  # noqa: E402


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

PLAIN = (
    "**日本語：** 画像は画素の集まりです。\n"
    "**English:** An image is a collection of pixels.\n"
)
PLAIN_CLEAN = "画像は画素の集まりです。\nAn image is a collection of pixels.\n"


def test_plain_bold_labels_are_removed() -> None:
    assert nll.clean_markdown_text(PLAIN) == PLAIN_CLEAN


def test_unbolded_and_alternate_colon_labels_are_removed() -> None:
    text = "日本語: 一枚の画像。\nEnglish： One image.\n"
    assert nll.clean_markdown_text(text) == "一枚の画像。\nOne image.\n"


def test_heading_labels_are_removed_but_title_kept() -> None:
    text = "#### 日本語：画素とは\n本文 / body\n\n#### English: What is a pixel\nBody.\n"
    cleaned = nll.clean_markdown_text(text)
    assert "#### 画素とは" in cleaned
    assert "#### What is a pixel" in cleaned
    assert "日本語：" not in cleaned
    assert "English:" not in cleaned


def test_english_heading_after_english_paragraph_is_moved_up() -> None:
    text = (
        "#### 日本語：同じにできない\n"
        "**日本語：** 2 つは違います。\n"
        "\n"
        "**English:** The two differ.\n"
        "#### English: Do not pretend they are the same\n"
    )
    cleaned = nll.clean_markdown_text(text)
    lines = cleaned.split("\n")
    heading_index = lines.index("#### Do not pretend they are the same")
    body_index = lines.index("The two differ.")
    assert heading_index < body_index


def test_duplicate_english_heading_is_dropped() -> None:
    text = (
        "#### 日本語：理解度チェック / Understanding questions\n"
        "**日本語：**\n"
        "1. 問い\n"
        "\n"
        "**English:**\n"
        "1. Question?\n"
        "#### English: Understanding questions\n"
    )
    cleaned = nll.clean_markdown_text(text)
    assert cleaned.count("Understanding questions") == 1
    assert cleaned.startswith("#### 理解度チェック / Understanding questions")


def test_blockquote_labels_are_removed_and_quote_kept() -> None:
    text = "> **日本語：** 昼休みです。\n>\n> **English:** It is the lunch break.\n"
    cleaned = nll.clean_markdown_text(text)
    assert cleaned == "> 昼休みです。\n>\n> It is the lunch break.\n"


def test_list_marker_labels_are_removed() -> None:
    text = "- **日本語：** 項目\n- **English:** item\n"
    assert nll.clean_markdown_text(text) == "- 項目\n- item\n"


def test_label_only_paragraph_disappears_without_breaking_structure() -> None:
    text = "見出し\n\n**日本語：**\n\n1. あ\n\n**English:**\n\n1. a\n"
    cleaned = nll.clean_markdown_text(text)
    assert "**日本語：**" not in cleaned
    assert "**English:**" not in cleaned
    assert cleaned == "見出し\n\n1. あ\n\n1. a\n"


def test_code_fences_are_never_touched() -> None:
    text = (
        "```python\n"
        "# 日本語： これはコメント\n"
        "label = 'English: keep me'\n"
        "\n"
        "\n"
        "print(label)\n"
        "```\n"
    )
    assert nll.clean_markdown_text(text) == text


def test_inline_code_and_urls_are_not_touched() -> None:
    text = (
        "`日本語：` という書き方と `English:` という書き方は、説明の中では残します。\n"
        "https://example.com/日本語：page もそのまま。\n"
    )
    assert nll.clean_markdown_text(text) == text


def test_meaningful_language_terms_are_preserved() -> None:
    text = (
        "日本語フォントを設定します。\n"
        "Set the Japanese font.\n"
        "\n"
        "この教材は 日本語 と English の両方で書かれています。\n"
        "This material is written in both Japanese and English.\n"
    )
    assert nll.clean_markdown_text(text) == text


def test_table_cells_are_not_mistaken_for_labels() -> None:
    text = "| 日本語 | English |\n| --- | --- |\n| あ | a |\n"
    assert nll.clean_markdown_text(text) == text


def _heading_text() -> str:
    return "#### 日本語：見出し\n**日本語：** 本文\n\n**English:** Body.\n#### English: Heading\n"


def _mixed_text() -> str:
    return (
        "## 学習目標 / Learning objectives\n"
        "**日本語：** 目標\n"
        "\n"
        "**English:** Goal\n"
        "> **日本語：** 引用\n"
        "> **English:** quote\n"
        "```text\n"
        "日本語： keep\n"
        "```\n"
    )


def test_cleanup_is_idempotent() -> None:
    samples = [PLAIN, _heading_text(), _mixed_text()]
    for sample in samples:
        once = nll.clean_markdown_text(sample)
        assert nll.clean_markdown_text(once) == once, sample


def test_statistics_are_reported() -> None:
    record = nll.Change(path="<test>")
    nll.clean_markdown_text(PLAIN, record)
    assert record.lines_changed == 2
    assert record.changed


# ---------------------------------------------------------------------------
# リポジトリ全体 / the whole repository
# ---------------------------------------------------------------------------


def test_repository_has_no_language_labels_left() -> None:
    changes = [c for c in nll.run(COURSE_ROOT, write=False) if c.changed]
    assert not changes, "language labels still present: " + ", ".join(c.path for c in changes[:5])


def test_clean_notebook_touches_markdown_only(tmp_path: Path) -> None:
    import nbformat

    notebook = nbformat.v4.new_notebook()
    notebook.cells.append(nbformat.v4.new_markdown_cell("**日本語：** あ\n\n**English:** a\n"))
    code_cell = nbformat.v4.new_code_cell("label = '日本語： keep'\n")
    code_cell["metadata"]["aivision_role"] = "run-only"
    notebook.cells.append(code_cell)
    path = tmp_path / "fixture.ipynb"
    nbformat.write(notebook, str(path))

    record = nll.clean_notebook(path, write=True)
    assert record.cells_changed == 1

    reread = nbformat.read(str(path), as_version=4)
    assert reread.cells[0].source == "あ\n\na\n"
    assert reread.cells[1].source == "label = '日本語： keep'\n"
    assert reread.cells[1]["metadata"]["aivision_role"] == "run-only"


@pytest.mark.parametrize("suffix", [".ipynb", ".md"])
def test_targets_cover_notebooks_and_documents(suffix: str) -> None:
    targets = nll.iter_targets(COURSE_ROOT)
    assert any(path.suffix == suffix for path in targets)
    assert all(".venv" not in path.parts for path in targets)
