"""ノートブックの構造検証テスト / Notebook structural validation tests.

`assets/scripts/validate_notebooks.py` の構造検証を pytest から呼びます。
（実行を伴う検証は重いので、ここでは構造だけを見ます。）

Calls the structural checks from `validate_notebooks.py`. Execution tests are too heavy for the
default test run, so only structure is verified here.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

COURSE_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = COURSE_ROOT / "assets" / "scripts"
NOTEBOOK_DIR = COURSE_ROOT / "notebooks"

sys.path.insert(0, str(SCRIPTS))

import validate_notebooks as vn  # noqa: E402


@pytest.fixture(scope="module")
def structural_result():
    result = vn.Result()
    infos = [vn.check_notebook(NOTEBOOK_DIR / rel, result) for rel, _day, _cat in vn.NOTEBOOKS]
    return result, infos


def test_all_sixteen_notebooks_exist() -> None:
    missing = [rel for rel, _d, _c in vn.NOTEBOOKS if not (NOTEBOOK_DIR / rel).is_file()]
    assert not missing, f"missing notebooks: {missing}"
    assert len(vn.NOTEBOOKS) == 16


def test_structural_checks_pass(structural_result) -> None:
    result, _infos = structural_result
    assert not result.failed, "structural problems:\n" + "\n".join(result.failed)


def test_every_notebook_has_code_and_markdown(structural_result) -> None:
    _result, infos = structural_result
    for info in infos:
        if not info["checks"].get("exists"):
            continue
        assert info["code_cells"] >= 8, f"{info['path']} has only {info['code_cells']} code cells"
        assert info["cells"] >= 20, f"{info['path']} has only {info['cells']} cells"


def test_every_notebook_has_three_exercises(structural_result) -> None:
    result, _infos = structural_result
    for message in result.passed:
        if "3 exercises" in message:
            continue
    # 失敗が無ければ、すべてのノートブックに演習 1〜3 がある
    assert not [m for m in result.failed if "fewer than 3 exercises" in m]


def test_no_notebook_references_missing_assets(structural_result) -> None:
    _result, infos = structural_result
    for info in infos:
        assert not info.get("unresolved_assets"), (
            f"{info['path']} references missing assets: {info.get('unresolved_assets')}"
        )


@pytest.mark.parametrize("rel,_day,_cat", vn.NOTEBOOKS)
def test_notebook_kernel_is_one_of_the_course_kernels(rel, _day, _cat) -> None:
    import json

    path = NOTEBOOK_DIR / rel
    if not path.is_file():
        pytest.skip("notebook not built yet")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    kernel = notebook.get("metadata", {}).get("kernelspec", {}).get("name")
    assert kernel in {"aivision", "aivision-anomalib"}, f"{rel} uses kernel {kernel!r}"
