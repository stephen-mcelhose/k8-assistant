#!/usr/bin/env python3
"""
extract.py — fetch a kubernetes.io tutorial page and write verbatim plain text to raw/tutorials/

Usage:
    python3 docs/wiki/raw/extract.py <URL> <slug>

Example:
    python3 docs/wiki/raw/extract.py \
        https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/ \
        deploy-app

Output:
    docs/wiki/raw/tutorials/<slug>.md

The script:
  1. curl-fetches the URL
  2. Extracts the <main data-pagefind-body> element
  3. Strips script/style/feedback blocks, then all remaining HTML tags
  4. Normalises whitespace
  5. Writes plain text with an attribution header (CC BY 4.0)

The resulting file is immutable — do not edit after creation.
"""

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def fetch_html(url: str) -> str:
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")
    return result.stdout


def extract_main(html: str) -> str:
    m = re.search(r'<main\b[^>]*data-pagefind-body[^>]*>(.*?)</main>', html, re.DOTALL)
    if not m:
        raise RuntimeError("Could not find <main data-pagefind-body> in page")
    content = m.group(1)

    # Strip noise blocks
    for tag in ("script", "style"):
        content = re.sub(rf'<{tag}[^>]*>.*?</{tag}>', ' ', content,
                         flags=re.DOTALL | re.IGNORECASE)
    # Feedback widget divs
    content = re.sub(r'<div[^>]*feedback[^>]*>.*?</div>', ' ', content,
                     flags=re.DOTALL | re.IGNORECASE)

    # Strip remaining tags
    text = re.sub(r'<[^>]+>', ' ', content)

    # Decode common HTML entities
    replacements = [
        ('&lt;', '<'), ('&gt;', '>'), ('&amp;', '&'),
        ('&#39;', "'"), ('&quot;', '"'), ('&nbsp;', ' '),
    ]
    for entity, char in replacements:
        text = text.replace(entity, char)

    # Normalise whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def write_raw(slug: str, url: str, text: str, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.md"

    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    header = (
        f"<!--\n"
        f"  Source : {url}\n"
        f"  Fetched: {fetched}\n"
        f"  License: CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/\n"
        f"  This file is an unedited verbatim extraction of the <main> element.\n"
        f"  Do NOT edit. Re-fetch to update; diff against previous to detect changes.\n"
        f"-->\n\n"
    )

    out_path.write_text(header + text, encoding="utf-8")
    return out_path


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    url, slug = sys.argv[1], sys.argv[2]
    out_dir = Path(__file__).parent / "tutorials"

    print(f"Fetching {url} …", file=sys.stderr)
    html = fetch_html(url)

    print("Extracting <main data-pagefind-body> …", file=sys.stderr)
    text = extract_main(html)

    out_path = write_raw(slug, url, text, out_dir)
    char_count = len(text)
    word_count = len(text.split())
    print(f"Written: {out_path}  ({char_count:,} chars, {word_count:,} words)", file=sys.stderr)


if __name__ == "__main__":
    main()
