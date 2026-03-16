#!/usr/bin/env python3
"""Check sitemap for documentation updates since last run.

Fetches the sitemap from code.claude.com/docs/sitemap.xml, compares <lastmod>
timestamps against a stored checkpoint, and detects removed pages.

Exit codes:
    0 — changes detected (new/updated/removed pages)
    1 — no changes since last check
    2 — error (network, parse, etc.)

Usage:
    python3 check_sitemap.py --basedir .
"""

import argparse
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LANGUAGES, SLUGS

SITEMAP_URL = "https://code.claude.com/docs/sitemap.xml"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
CHECKPOINT_FILE = ".last_sitemap_check"


def fetch_sitemap():
    """Fetch and parse the sitemap XML. Returns list of (loc, lastmod) tuples."""
    req = urllib.request.Request(SITEMAP_URL, headers={
        "User-Agent": "Mozilla/5.0 (compatible; DocTracker/1.0)",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    entries = []
    for url_el in root.findall("sm:url", SITEMAP_NS):
        loc_el = url_el.find("sm:loc", SITEMAP_NS)
        lastmod_el = url_el.find("sm:lastmod", SITEMAP_NS)
        if loc_el is not None and lastmod_el is not None:
            entries.append((loc_el.text.strip(), lastmod_el.text.strip()))
    return entries


def extract_slug(loc, lang_prefix):
    """Extract slug from a sitemap URL like .../docs/en/overview → overview."""
    prefix = f"https://code.claude.com/docs/{lang_prefix}/"
    if loc.startswith(prefix):
        return loc[len(prefix):]
    return None


def parse_lastmod(ts):
    """Parse ISO 8601 timestamp from sitemap."""
    # Handle formats like 2026-03-12T19:27:46.572Z
    ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def main():
    parser = argparse.ArgumentParser(description="Check sitemap for doc updates")
    parser.add_argument("--basedir", required=True, help="Base working directory")
    args = parser.parse_args()

    checkpoint_path = os.path.join(args.basedir, CHECKPOINT_FILE)

    # Load previous checkpoint
    last_check = None
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path) as f:
            stored = f.read().strip()
            if stored:
                try:
                    last_check = parse_lastmod(stored)
                except ValueError:
                    print(f"WARNING: Could not parse stored timestamp: {stored}")

    # Fetch sitemap
    print(f"Fetching sitemap from {SITEMAP_URL}...")
    try:
        entries = fetch_sitemap()
    except Exception as e:
        print(f"ERROR: Failed to fetch sitemap: {e}")
        sys.exit(2)

    print(f"  Found {len(entries)} URLs in sitemap")

    # Filter to all supported languages
    lang_entries = {lang: {} for lang in LANGUAGES}
    latest_mod = None

    for loc, lastmod_str in entries:
        ts = parse_lastmod(lastmod_str)
        if latest_mod is None or ts > latest_mod:
            latest_mod = ts

        for lang in LANGUAGES:
            slug = extract_slug(loc, lang)
            if slug:
                lang_entries[lang][slug] = ts
                break

    for lang in LANGUAGES:
        count = len(lang_entries[lang])
        if count:
            print(f"  {lang}: {count} pages")
    print(f"  Latest modification: {latest_mod.isoformat() if latest_mod else 'N/A'}")

    # Detect removed pages (in our config but not in sitemap)
    removed = []
    for slug in SLUGS:
        if slug not in lang_entries["en"]:
            removed.append(slug)

    if removed:
        print(f"\n  Potentially removed pages ({len(removed)}):")
        for slug in removed:
            print(f"    - {slug}")

    # Compare against last check
    has_changes = False

    if last_check is None:
        print("\n  No previous checkpoint — treating as first run (changes detected)")
        has_changes = True
    elif latest_mod and latest_mod > last_check:
        # Find which pages changed
        print(f"\n  Changes since {last_check.isoformat()}:")
        for lang in LANGUAGES:
            updated = [s for s, ts in lang_entries[lang].items() if ts > last_check]
            if updated:
                print(f"    {lang}: {len(updated)} pages updated")
        has_changes = True
    else:
        print(f"\n  No changes since {last_check.isoformat()}")

    if removed:
        has_changes = True

    # Update checkpoint
    if has_changes and latest_mod:
        with open(checkpoint_path, "w") as f:
            f.write(latest_mod.isoformat())
        print(f"\n  Updated checkpoint to {latest_mod.isoformat()}")

    if has_changes:
        print("\nResult: CHANGES DETECTED")
        sys.exit(0)
    else:
        print("\nResult: NO CHANGES")
        sys.exit(1)


if __name__ == "__main__":
    main()
