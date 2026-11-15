"""Current learner commands are CMD-only; historical evidence is explicitly scoped out."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import venv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "assets" / "scripts"))
from course_notebooks import course_notebooks  # noqa: E402

ARCHIVES = {
    ROOT / "docs" / "test_report.md",  # Explicitly dated 12 November execution log.
    ROOT / "docs" / "implementation_report.md",  # Dated prior implementation runs.
}
INCOMPATIBLE = re.compile(
    r"powershell|Activate\.ps1|Set-ExecutionPolicy|Set-Location|Get-ChildItem|Select-String"
    r"|\$env:|\$HOME|\bPS [A-Z]:\\",
    re.I,
)


def current_sources() -> list[tuple[str, str]]:
    documents = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").rglob("*.md"))
    documents += sorted((ROOT / "requirements").glob("*.txt"))
    sources = []
    for path in documents:
        if path in ARCHIVES or path.parent == ROOT / "docs" / "reviews":
            continue
        if ".ipynb_checkpoints" not in path.parts:
            sources.append((str(path.relative_to(ROOT)), path.read_text(encoding="utf-8")))
    for path in course_notebooks(ROOT / "notebooks"):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for index, cell in enumerate(notebook["cells"]):
            sources.append((f"{path.name}:cell {index}", "".join(cell["source"])))
    return sources


def test_current_instructions_have_no_incompatible_shell_tokens() -> None:
    problems = []
    for location, source in current_sources():
        match = INCOMPATIBLE.search(source)
        if match:
            problems.append(f"{location}: {match.group()}")
    assert not problems, "\n".join(problems)


def test_cmd_fences_have_copyable_commands_not_other_shell_comments() -> None:
    for location, source in current_sources():
        for block in re.findall(r"^```cmd\s*\n(.*?)^```", source, re.M | re.S):
            for line in block.splitlines():
                assert "#" not in line, (location, line)
                assert "`" not in line and not line.rstrip().endswith("\\"), (location, line)
                assert not line.lstrip().startswith(("PS ", "$ ", "%pip", "pwd")), (location, line)
                assert "<actual " not in line, (location, "placeholder in runnable block")


def test_preflight_has_one_cmd_sequence_and_correct_environment_boundaries() -> None:
    guide = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
    assert [int(n) for n in re.findall(r"^## ステップ (\d+)", guide, re.M)] == list(range(1, 12))
    for command in (
        'cd /d "%USERPROFILE%\\Documents"',
        r".\.venv\Scripts\activate.bat",
        r".\.venv-anomalib\Scripts\activate.bat",
        "where python",
        r'".\.venv\Scripts\python.exe" -m jupyter lab',
    ):
        assert command in guide
    assert "OneDrive" in guide and "placeholder" in guide
    troubleshooting = (ROOT / "docs" / "troubleshooting" / "installation.md").read_text(encoding="utf-8")
    assert 'set "HTTP_PROXY=http://proxy.example.co.jp:8080"' in troubleshooting
    assert 'set "HTTPS_PROXY=http://proxy.example.co.jp:8080"' in troubleshooting
    assert "example addresses, not company configuration" in troubleshooting
    assert "findstr /I opencv" in troubleshooting


def test_launcher_is_portable_and_does_not_prepare_or_modify_the_course() -> None:
    source = (ROOT / "start_training.cmd").read_text(encoding="utf-8")
    assert 'cd /d "%~dp0"' in source
    assert 'if not exist "%~dp0.venv\\Scripts\\python.exe"' in source
    assert '"%~dp0.venv\\Scripts\\python.exe" -m jupyter lab' in source
    assert 'set "LAUNCH_EXIT=%ERRORLEVEL%"' in source
    assert "exit /b %LAUNCH_EXIT%" in source
    assert "START_HERE.md" in source and "pause" in source
    assert not re.search(r"^\s*(?:del|erase|rd|rmdir|curl|pip|powershell)\b|"
                         r"-m pip|download_|generate_|train\(", source, re.M | re.I)
    if "activate.bat" in source.lower():
        assert re.search(r"^\s*call .*activate\.bat", source, re.M | re.I)


@pytest.mark.skipif(sys.platform != "win32", reason="requires real Windows cmd.exe")
@pytest.mark.parametrize("mode,exit_code", [("missing", 1), ("broken", 1), ("stub", 0), ("stub", 23)])
def test_launcher_in_real_cmd_with_spaces(tmp_path: Path, mode: str, exit_code: int) -> None:
    course = tmp_path / "course folder with spaces"
    course.mkdir()
    launcher = course / "start_training.cmd"
    shutil.copyfile(ROOT / "start_training.cmd", launcher)
    if mode != "missing":
        venv.EnvBuilder(with_pip=False).create(course / ".venv")
    if mode == "stub":
        package = course / "jupyter"
        package.mkdir()
        (course / ".venv" / "Scripts" / "jupyter-lab.cmd").write_text("@exit /b 0\n", encoding="ascii")
        (package / "__main__.py").write_text(
            "import os, shutil, sys\n"
            "from pathlib import Path\n"
            "assert sys.argv[1:] == ['lab']\n"
            "assert Path(shutil.which('jupyter-lab')).parent == Path.cwd() / '.venv' / 'Scripts'\n"
            "print('SMOKE_ROOT=' + str(Path.cwd()))\n"
            "sys.exit(int(os.environ['TRAINING_SMOKE_EXIT']))\n",
            encoding="utf-8",
        )
    comspec = os.environ.get("COMSPEC", "cmd.exe")
    result = subprocess.run(
        f'"{comspec}" /d /c call "{launcher}"',
        cwd=tmp_path, input="\n", capture_output=True, encoding="utf-8", errors="replace",
        env=dict(os.environ, TRAINING_SMOKE_EXIT=str(exit_code)), timeout=60,
    )
    assert result.returncode == exit_code, result.stdout + result.stderr
    if mode == "stub":
        assert f"SMOKE_ROOT={course}" in result.stdout
    if exit_code:
        assert "START_HERE.md" in result.stdout


def test_remediation_generator_keeps_current_setup_in_cmd() -> None:
    from remediate_notebooks import correct_notebook

    sample = {"cells": [{"cell_type": "markdown", "id": "legacy-preflight", "metadata": {},
                         "source": ["#### 手順 3：古い準備\n"]},
                        {"cell_type": "markdown", "id": "part4", "metadata": {},
                         "source": ["## Part 4\n"]}]}
    correct_notebook("00_Environment_Setup", sample)
    text = "\n".join("".join(c["source"]) for c in sample["cells"])
    assert "CMD activation requires no policy changes" in text
    assert INCOMPATIBLE.search(text) is None
