#!/usr/bin/env python3
"""Render the sales dashboard Quarto document."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
import webbrowser

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "examples" / "sales-dashboard" / "sales-dashboard.qmd"
OUTPUT_DIR = DOC_PATH.parent / "outputs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render the sales dashboard Quarto document.")
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the rendered dashboard in your default web browser after a successful build.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("Rendering sales dashboard...")
    result = subprocess.run(
        ["quarto", "render", str(DOC_PATH), "--output-dir", str(OUTPUT_DIR)],
        cwd=REPO_ROOT,
    )
    if result.returncode == 0:
        output_html = OUTPUT_DIR / DOC_PATH.with_suffix(".html").name
        print(f"✔ Dashboard rebuilt at {output_html}")
        if args.open:
            url = output_html.resolve().as_uri()
            print(f"Opening in browser: {url}")
            webbrowser.open(url, new=2)
    return result.returncode


if __name__ == "__main__":  # pragma: no cover - script entrypoint
    raise SystemExit(main())
