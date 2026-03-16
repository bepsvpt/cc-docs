#!/usr/bin/env python3
"""Merge all Claude Code markdown docs into a single file for Pandoc.

Usage:
    python3 merge_docs.py --basedir /path/to/workdir
    python3 merge_docs.py --lang zh-TW --basedir /path/to/workdir
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BASE_URL, LANG_CODES, lang_to_dir, heading_to_anchor, sections_for_lang
from md_transforms import clean_md

parser = argparse.ArgumentParser(description="Merge Claude Code docs")
parser.add_argument("--lang", default="en", choices=LANG_CODES,
                    help="Language to merge (default: en)")
parser.add_argument("--basedir", required=True,
                    help="Base working directory for all files")
args = parser.parse_args()

LANG = args.lang
BASEDIR = args.basedir
LANG_DIR = lang_to_dir(LANG)
DOCS_DIR = os.path.join(BASEDIR, "docs", LANG_DIR)
IMAGES_DIR = os.path.join(BASEDIR, "docs", "images")
OUTPUT = os.path.join(BASEDIR, "build", f"merged_{LANG_DIR}.md")
LANG_PATH = LANG  # URL path uses original lang code (e.g. "zh-TW")

def extract_all_headings(filepath):
    """Extract all heading texts from a markdown file, skipping frontmatter."""
    headings = []
    in_frontmatter = False
    with open(filepath) as f:
        for line in f:
            stripped = line.strip()
            if stripped == '---':
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter:
                continue
            if stripped.startswith('#'):
                text = re.sub(r'^#+\s*', '', stripped)
                text = re.sub(r'[*_`\[\]]', '', text)
                text = re.sub(r'\s*\{[^}]*\}\s*$', '', text)
                if text:
                    headings.append(text)
    return headings


def _first_heading(filepath):
    """Extract first heading text from a markdown file."""
    headings = extract_all_headings(filepath)
    return headings[0] if headings else None


# Build local→English fragment map for non-English languages.
# WeasyPrint PDF named destinations only work with ASCII IDs, so all heading
# IDs must use English anchors. This reverse map translates local-language
# heading anchors to their English equivalents.
FRAGMENT_MAP = {}  # local_anchor → english_anchor (reverse direction)
if LANG != "en":
    EN_DOCS_DIR = os.path.join(BASEDIR, "docs", "en")
    for _section_name, _slugs in sections_for_lang(LANG):
        for _slug in _slugs:
            _en_path = os.path.join(EN_DOCS_DIR, f"{_slug}.md")
            _local_path = os.path.join(DOCS_DIR, f"{_slug}.md")
            if os.path.exists(_en_path) and os.path.exists(_local_path):
                _en_headings = extract_all_headings(_en_path)
                _local_headings = extract_all_headings(_local_path)
                for _en_h, _local_h in zip(_en_headings, _local_headings):
                    _en_anchor = heading_to_anchor(_en_h)
                    _local_anchor = heading_to_anchor(_local_h)
                    if _en_anchor != _local_anchor:
                        FRAGMENT_MAP[_local_anchor] = _en_anchor
    if FRAGMENT_MAP:
        print(f"  Fragment map: {len(FRAGMENT_MAP)} local→English translations")
        # Save for generate_pdf.py to use when injecting heading IDs
        _map_path = os.path.join(BASEDIR, "build", f"fragment_map_{LANG_DIR}.json")
        os.makedirs(os.path.dirname(_map_path), exist_ok=True)
        with open(_map_path, 'w') as _f:
            json.dump(FRAGMENT_MAP, _f, ensure_ascii=False)

# Build mapping from doc slug to chapter heading anchor ID.
# For non-English, use the ENGLISH title anchor (ASCII) so PDF links work.
SLUG_TO_ANCHOR = {}
EN_DOCS_DIR = os.path.join(BASEDIR, "docs", "en")
for _section_name, _slugs in sections_for_lang(LANG):
    for _slug in _slugs:
        # Always use English heading for the anchor (ASCII-safe)
        _en_path = os.path.join(EN_DOCS_DIR, f"{_slug}.md")
        if os.path.exists(_en_path):
            _heading = _first_heading(_en_path)
            if _heading:
                SLUG_TO_ANCHOR[_slug] = heading_to_anchor(_heading)
                continue
        # Fallback to local heading
        _path = os.path.join(DOCS_DIR, f"{_slug}.md")
        if os.path.exists(_path):
            _heading = _first_heading(_path)
            if _heading:
                SLUG_TO_ANCHOR[_slug] = heading_to_anchor(_heading)


def extract_title(md):
    """Extract first H1 and remove it."""
    m = re.match(r'^#\s+(.+?)(?:\s*\{[^}]*\})?\s*\n', md)
    if m:
        return m.group(1).strip(), md[m.end():]
    return None, md


def bump_headings(md, levels=1):
    """Increase heading levels by N."""
    def bump(m):
        hashes = m.group(1)
        new_level = min(len(hashes) + levels, 6)
        return '#' * new_level + m.group(2)
    return re.sub(r'^(#{1,6})([ \t]+)', bump, md, flags=re.MULTILINE)


# Build the merged document
output_parts = []

for section_idx, (section_title, slugs) in enumerate(sections_for_lang(LANG), 1):
    output_parts.append(f'\n\\newpage\n\n# Part {section_idx}: {section_title}\n\n')

    for slug in slugs:
        md_path = os.path.join(DOCS_DIR, f"{slug}.md")
        if not os.path.exists(md_path):
            print(f"WARNING: {slug}.md not found")
            continue

        with open(md_path, 'r') as f:
            md = f.read()

        md = clean_md(md, images_dir=IMAGES_DIR, slug_to_anchor=SLUG_TO_ANCHOR,
                       base_url=BASE_URL, lang_path=LANG_PATH,
                       fragment_map=FRAGMENT_MAP)
        title, md = extract_title(md)
        if not title:
            title = slug.replace('-', ' ').title()

        md = bump_headings(md, levels=1)

        if slug == 'changelog':
            lines = md.split('\n')
            if len(lines) > 200:
                md = '\n'.join(lines[:200])
                md += f'\n\n*Earlier changelog entries omitted. See [full changelog](https://code.claude.com/docs/{LANG_PATH}/changelog) for complete history.*\n'

        output_parts.append(f'\\newpage\n\n## {title}\n\n{md}\n\n')
        print(f"  [{section_idx}] {title}")

merged = '\n'.join(output_parts)

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, 'w') as f:
    f.write(merged)

print(f"\nDone! Merged document: {OUTPUT} ({len(merged)} chars)")
