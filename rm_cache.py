#!/usr/bin/env python3
"""
clean_pycache.py
Scans the repository for __pycache__ directories and nukes them.
Safe to run from the repo root; ignores .git and other VCS folders.
"""

from pathlib import Path
import shutil
import sys

def main() -> None:
    repo_root = Path(__file__).resolve().parent
    removed = 0

    for pycache in repo_root.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            removed += 1
            print(f"Removed {pycache.relative_to(repo_root)}")

    if removed:
        print(f"\n✅ Cleaned {removed} __pycache__ folder(s).")
    else:
        print("🧹 No __pycache__ folders found.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nAborted.")

