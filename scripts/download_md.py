#!/usr/bin/env python3
"""Download all Claude Code docs in .md format.

Usage:
    python3 download_md.py --basedir /path/to/workdir
    python3 download_md.py --lang zh-TW --basedir /path/to/workdir
    python3 download_md.py --lang zh-TW --basedir /path/to/workdir --force
"""

import argparse
import os
import re
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LANG_CODES, lang_to_dir, slugs_for_lang

parser = argparse.ArgumentParser(description="Download Claude Code docs")
parser.add_argument("--lang", default="en", choices=LANG_CODES,
                    help="Language to download (default: en)")
parser.add_argument("--basedir", required=True,
                    help="Base working directory for all files")
parser.add_argument("--force", action="store_true",
                    help="Re-download even if files exist")
args = parser.parse_args()

lang = args.lang
slugs = slugs_for_lang(lang)
docs_dir = os.path.join(args.basedir, "docs", lang_to_dir(lang))
images_dir = os.path.join(args.basedir, "docs", "images")
os.makedirs(docs_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

print(f"Downloading {lang} docs ({len(slugs)} pages) → {docs_dir}")

success = 0
failed = []

for i, slug in enumerate(slugs):
    out_path = os.path.join(docs_dir, f"{slug}.md")
    # Skip if already downloaded and non-trivial (unless --force)
    if not args.force and os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        print(f"[{i+1}/{len(slugs)}] {slug}... SKIP (exists)")
        success += 1
        continue

    url = f"https://code.claude.com/docs/{lang}/{slug}.md"
    print(f"[{i+1}/{len(slugs)}] {slug}...", end=" ", flush=True)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; DocFetcher/1.0)',
                'Accept': 'text/markdown, text/plain, */*',
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read().decode('utf-8', errors='replace')

            with open(out_path, 'w') as f:
                f.write(content)

            # Extract and download images referenced in this doc
            for img_match in re.finditer(r'data-path="images/([^"]+)"', content):
                img_name = img_match.group(1)
                img_path = os.path.join(images_dir, img_name)
                if not os.path.exists(img_path):
                    img_url = f"https://code.claude.com/docs/images/{img_name}"
                    try:
                        img_req = urllib.request.Request(img_url, headers={
                            'User-Agent': 'Mozilla/5.0 (compatible; DocFetcher/1.0)',
                        })
                        with urllib.request.urlopen(img_req, timeout=30) as img_resp:
                            with open(img_path, 'wb') as img_f:
                                img_f.write(img_resp.read())
                    except Exception:
                        pass  # Non-critical: image may not exist

            print(f"OK ({len(content)} chars)")
            success += 1
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                wait = 2 ** attempt * 5  # 5s, 10s
                print(f"RATE LIMITED, retrying in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
                continue
            print(f"FAILED: {e}")
            failed.append(slug)
            break
        except Exception as e:
            print(f"FAILED: {e}")
            failed.append(slug)
            break
    time.sleep(0.3)

print(f"\nDone: {success}/{len(slugs)} downloaded, {len(failed)} failed")
if failed:
    print(f"Failed: {', '.join(failed)}")
