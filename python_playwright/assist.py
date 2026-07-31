from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def abs_path_from_project(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)
