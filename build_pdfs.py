#!/usr/bin/env python3
"""Render all topic HTML cheat sheets into matching print-ready A4 PDFs."""

import glob
import os
import shutil
import subprocess
import sys

CANDIDATES = [
    os.environ.get("CHROME_BIN", ""),
    "/ms-playwright/chrome-headless-shell-linux64/chrome-headless-shell",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("chrome-headless-shell") or "",
]


def find_browser() -> str:
    for path in CANDIDATES:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    # Also check playwright cache if installed
    matches = sorted(glob.glob("/ms-playwright/**/chrome-headless-shell", recursive=True))
    if matches:
        return matches[0]
    raise RuntimeError(
        "No Chromium/Chrome executable found. Set CHROME_BIN or install Chromium."
    )


def render_pdf(browser: str, html_path: str, pdf_path: str) -> None:
    url = "file://" + os.path.abspath(html_path)
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        url,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    browser = find_browser()
    html_files = sorted(
        f for f in glob.glob(os.path.join(root, "*.html"))
        if os.path.basename(f) != "index.html"
    )
    if not html_files:
        print("No topic HTML files found.", file=sys.stderr)
        return 1

    for html_file in html_files:
        pdf_file = os.path.splitext(html_file)[0] + ".pdf"
        render_pdf(browser, html_file, pdf_file)
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"Built {os.path.basename(pdf_file)} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
