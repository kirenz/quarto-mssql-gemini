#!/usr/bin/env python3
"""Render the sales dashboard Quarto document."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "examples" / "sales-dashboard" / "sales-dashboard.qmd"


def main() -> int:
    print("Rendering sales dashboard...")
    result = subprocess.run(["quarto", "render", str(DOC_PATH)], cwd=REPO_ROOT)
    if result.returncode == 0:
        output_html = REPO_ROOT / "examples" / "sales-dashboard" / "outputs" / "sales-dashboard.html"
        print(f"✔ Dashboard rebuilt at {output_html}")
    return result.returncode


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    raise SystemExit(main())
