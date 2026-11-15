"""Discover lesson sources, never Jupyter checkpoints or arbitrary learner notebooks."""

from pathlib import Path

COURSE_FOLDERS = (
    "00_Setup",
    "Day01_AI_Fundamentals",
    "Day02_Python_OpenCV",
    "Day03_YOLO_Basics",
    "Day04_YOLO_Training",
    "Day05_PatchCore",
)


def course_notebooks(directory: Path, pattern: str = "*.ipynb") -> list[Path]:
    return sorted(
        path
        for folder in COURSE_FOLDERS
        for path in (directory / folder).glob(pattern)
        if path.is_file() and ".ipynb_checkpoints" not in path.parts
    )
