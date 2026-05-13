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

PROJECT_FOLDERS = ["company_valuation", "pead_european_banks_ifrs9", "portfolio_analysis", "prompts"]


def sync_to_drive(destination: Path, folders: list[str]) -> list[Path]:
    if not destination.parent.exists():
        raise FileNotFoundError(
            f"Drive parent folder does not exist: {destination.parent}. "
            "Mount Google Drive in Colab first: from google.colab import drive; drive.mount('/content/drive')"
        )
    destination.mkdir(parents=True, exist_ok=True)
    copied = []
    for folder in folders:
        src = Path(folder)
        if not src.exists():
            continue
        dst = destination / src.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        copied.append(dst)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", default="/content/drive/MyDrive/ml-trading-thesis-bot_research_exports")
    parser.add_argument("--folders", nargs="*", default=PROJECT_FOLDERS)
    args = parser.parse_args()
    destination = Path(args.destination)
    try:
        copied = sync_to_drive(destination, args.folders)
    except Exception as exc:
        print(f"⚠️ Drive sync skipped: {exc}")
        return 0
    print("✅ Synced folders to Drive:")
    for path in copied:
        print(f"   {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
