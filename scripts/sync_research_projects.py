"""Copy research project folders to a local destination.

This script is intentionally generic: it can mirror the three canonical research
projects to Google Drive, another checked-out repository, or a local folder such
as `/Users/itsgennymac/GitHub/machine-learning-for-trading`.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_PROJECT_FOLDERS = ["company_valuation", "pead_european_banks_ifrs9", "portfolio_analysis"]
OPTIONAL_SUPPORT_FILES = ["RESEARCH_PROJECTS.md", "prompts", "scripts", "Company_Valuatio.ipynb"]
GENERATED_OUTPUT_NAMES = {"output", ".ipynb_checkpoints", "__pycache__"}
DEFAULT_LOCAL_DESTINATION = Path("/Users/itsgennymac/GitHub/machine-learning-for-trading")


def _ignore_generated(_: str, names: list[str]) -> set[str]:
    """Skip generated artifacts by default so mirrors stay lightweight."""
    return {name for name in names if name in GENERATED_OUTPUT_NAMES}


def copy_path(src: Path, dst: Path, *, include_output: bool = False) -> Path:
    """Copy one file or directory, replacing any existing destination path."""
    if not src.exists():
        raise FileNotFoundError(f"Source path does not exist: {src}")
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        ignore = None if include_output else _ignore_generated
        shutil.copytree(src, dst, ignore=ignore)
    else:
        shutil.copy2(src, dst)
    return dst


def sync_research_projects(
    destination: Path,
    *,
    include_output: bool = False,
    include_support_files: bool = True,
    repo_root: Path = REPO_ROOT,
) -> list[Path]:
    """Mirror the three research project folders into a local destination."""
    copied: list[Path] = []
    for relative in RESEARCH_PROJECT_FOLDERS:
        copied.append(copy_path(repo_root / relative, destination / relative, include_output=include_output))
    if include_support_files:
        for relative in OPTIONAL_SUPPORT_FILES:
            source = repo_root / relative
            if source.exists():
                copied.append(copy_path(source, destination / relative, include_output=include_output))
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Mirror the canonical research project folders to a local destination.")
    parser.add_argument("--destination", type=Path, default=DEFAULT_LOCAL_DESTINATION)
    parser.add_argument("--include-output", action="store_true", help="Also copy generated output/ folders and notebook checkpoints.")
    parser.add_argument("--no-support-files", action="store_true", help="Copy only the three project folders, without RESEARCH_PROJECTS.md/prompts/scripts/top-level notebook mirror.")
    args = parser.parse_args()
    copied = sync_research_projects(
        args.destination,
        include_output=args.include_output,
        include_support_files=not args.no_support_files,
    )
    print(f"✅ Synced {len(copied)} research paths to {args.destination}")
    for path in copied:
        print(f"   {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
