"""Sync research project folders to Google Drive when running in Colab.

Default destination:
    /content/drive/MyDrive/ml-trading-thesis-bot_research_exports

The script is safe outside Colab: it exits with a clear warning if Drive is not
mounted instead of failing silently.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_FOLDERS = ["company_valuation", "pead_european_banks_ifrs9", "portfolio_analysis", "prompts"]
GENERATED_OUTPUT_NAMES = {"output", ".ipynb_checkpoints", "__pycache__"}


def _ignore_generated(_: str, names: list[str]) -> set[str]:
    """Skip generated artifacts by default so Drive syncs remain reviewable."""
    return {name for name in names if name in GENERATED_OUTPUT_NAMES}


def sync_to_drive(destination: Path, folders: list[str], *, include_output: bool = False, repo_root: Path = REPO_ROOT) -> list[Path]:
    """Copy selected research folders to Drive from any current working directory."""
    if not destination.parent.exists():
        raise FileNotFoundError(
            f"Drive parent folder does not exist: {destination.parent}. "
            "Mount Google Drive in Colab first: from google.colab import drive; drive.mount('/content/drive')"
        )
    destination.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    ignore = None if include_output else _ignore_generated
    for folder in folders:
        src = (repo_root / folder).resolve()
        if not src.exists():
            print(f"⚠️ Skipping missing folder: {src}")
            continue
        if not src.is_dir():
            print(f"⚠️ Skipping non-directory path: {src}")
            continue
        dst = destination / src.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=ignore)
        copied.append(dst)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync research project folders to a mounted Google Drive directory.")
    parser.add_argument("--destination", default="/content/drive/MyDrive/ml-trading-thesis-bot_research_exports")
    parser.add_argument("--folders", nargs="*", default=PROJECT_FOLDERS)
    parser.add_argument("--include-output", action="store_true", help="Also copy generated output/ folders and notebook checkpoints.")
    args = parser.parse_args()
    destination = Path(args.destination)
    try:
        copied = sync_to_drive(destination, args.folders, include_output=args.include_output)
    except Exception as exc:
        print(f"⚠️ Drive sync skipped: {exc}")
        return 0
    print("✅ Synced folders to Drive:")
    for path in copied:
        print(f"   {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
