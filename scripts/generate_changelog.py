#!/usr/bin/env python3
"""Generate a changelog from git diff of documentation files.

Compares the working tree against the last commit to detect added, modified,
and removed documentation pages. Outputs CHANGES.md and optionally a PDF.

Usage:
    python3 generate_changelog.py --basedir .
    python3 generate_changelog.py --basedir . --no-pdf
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LANGUAGES, lang_to_dir


def get_title_from_file(filepath):
    """Extract the H1 title from a markdown file."""
    try:
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line == "---":
                    continue
                if re.match(r"^[a-zA-Z_-]+:", line) and not line.startswith("#"):
                    continue
                m = re.match(r"^#\s+(.+?)(?:\s*\{[^}]*\})?$", line)
                if m:
                    return m.group(1).strip()
    except FileNotFoundError:
        pass
    return None


def get_title_from_diff_lines(removed_lines):
    """Extract H1 title from removed diff lines (for deleted files)."""
    for line in removed_lines:
        m = re.match(r"^#\s+(.+?)(?:\s*\{[^}]*\})?$", line)
        if m:
            return m.group(1).strip()
    return None


def slug_from_filename(filename):
    """Extract slug from a path like docs/en/overview.md → overview."""
    base = os.path.basename(filename)
    return os.path.splitext(base)[0]


def lang_from_path(filepath):
    """Determine language from file path."""
    for lang, info in LANGUAGES.items():
        if f"docs/{info['dir']}/" in filepath:
            return lang
    return "en"


def parse_git_diff(basedir):
    """Run git diff and parse the output into structured change data."""
    result = subprocess.run(
        ["git", "diff", "HEAD", "--"] + [f"docs/{info['dir']}/" for info in LANGUAGES.values()],
        capture_output=True, text=True, cwd=basedir,
    )

    # Also check for untracked new files (use -uall to list individual files, not directories)
    status_result = subprocess.run(
        ["git", "status", "--porcelain", "-uall", "--"] + [f"docs/{info['dir']}/" for info in LANGUAGES.values()],
        capture_output=True, text=True, cwd=basedir,
    )

    changes = {lang: {"added": [], "modified": [], "removed": []} for lang in LANGUAGES}

    # Parse git status for new/deleted files
    for line in status_result.stdout.strip().split("\n"):
        if not line:
            continue
        status = line[:2].strip()
        filepath = line[3:].strip()

        # Skip directory entries and non-.md files
        if filepath.endswith("/") or not filepath.endswith(".md"):
            continue

        if status == "??" or status == "A":
            lang = lang_from_path(filepath)
            slug = slug_from_filename(filepath)
            title = get_title_from_file(os.path.join(basedir, filepath))
            if not title:
                title = slug.replace("-", " ").title()
            changes[lang]["added"].append({"slug": slug, "title": title, "file": filepath})

        elif status == "D":
            lang = lang_from_path(filepath)
            slug = slug_from_filename(filepath)
            changes[lang]["removed"].append({"slug": slug, "title": slug.replace("-", " ").title(), "file": filepath})

    # Parse git diff for modifications and deleted content
    if result.stdout:
        current_file = None
        added_count = 0
        removed_count = 0
        removed_lines = []
        changed_headings = []
        is_new_file = False
        is_deleted_file = False
        in_fenced_block = False

        for line in result.stdout.split("\n"):
            # New file in diff
            if line.startswith("diff --git"):
                # Save previous file's data
                if current_file and not is_new_file:
                    _save_file_change(changes, current_file, added_count, removed_count,
                                      removed_lines, changed_headings, is_deleted_file, basedir)

                m = re.search(r"b/(.+)$", line)
                current_file = m.group(1) if m else None
                added_count = 0
                removed_count = 0
                removed_lines = []
                changed_headings = []
                is_new_file = False
                is_deleted_file = False
                in_fenced_block = False

            elif line.startswith("new file"):
                is_new_file = True

            elif line.startswith("deleted file"):
                is_deleted_file = True

            elif line.startswith("+") and not line.startswith("+++"):
                added_count += 1
                # Toggle fenced code block state (``` or ~~~)
                if re.match(r"^\+\s*(`{3,}|~{3,})", line):
                    in_fenced_block = not in_fenced_block
                # Track changed headings (skip inside fenced code blocks)
                elif not in_fenced_block:
                    heading_m = re.match(r"^\+\s*(#{1,6}\s+.+)$", line)
                    if heading_m:
                        changed_headings.append(heading_m.group(1))

            elif line.startswith("-") and not line.startswith("---"):
                removed_count += 1
                removed_lines.append(line[1:])  # Strip the leading -

        # Save last file
        if current_file and not is_new_file:
            _save_file_change(changes, current_file, added_count, removed_count,
                              removed_lines, changed_headings, is_deleted_file, basedir)

    return changes


def _save_file_change(changes, filepath, added_count, removed_count,
                      removed_lines, changed_headings, is_deleted, basedir):
    """Record a file's changes into the changes dict."""
    lang = lang_from_path(filepath)
    slug = slug_from_filename(filepath)

    if is_deleted:
        title = get_title_from_diff_lines(removed_lines)
        if not title:
            title = slug.replace("-", " ").title()
        # Avoid duplicates from git status
        existing_slugs = [r["slug"] for r in changes[lang]["removed"]]
        if slug not in existing_slugs:
            changes[lang]["removed"].append({"slug": slug, "title": title, "file": filepath})
    elif added_count > 0 or removed_count > 0:
        title = get_title_from_file(os.path.join(basedir, filepath))
        if not title:
            title = slug.replace("-", " ").title()
        # Avoid duplicates from git status
        existing_slugs = [m["slug"] for m in changes[lang]["modified"]]
        if slug not in existing_slugs:
            changes[lang]["modified"].append({
                "slug": slug, "title": title, "file": filepath,
                "added": added_count, "removed": removed_count,
                "headings": changed_headings[:5],  # Limit to 5 headings
            })


def generate_entry_md(changes):
    """Generate a single dated changelog entry from structured change data."""
    today = date.today().strftime("%Y-%m-%d")

    total_added = sum(len(changes[l]["added"]) for l in changes)
    total_modified = sum(len(changes[l]["modified"]) for l in changes)
    total_removed = sum(len(changes[l]["removed"]) for l in changes)

    if total_added == 0 and total_modified == 0 and total_removed == 0:
        return None  # Nothing to record

    lines = [f"## {today}\n"]

    # Summary line
    summary_parts = []
    if total_modified:
        summary_parts.append(f"{total_modified} page{'s' if total_modified != 1 else ''} modified")
    if total_added:
        summary_parts.append(f"{total_added} page{'s' if total_added != 1 else ''} added")
    if total_removed:
        summary_parts.append(f"{total_removed} page{'s' if total_removed != 1 else ''} removed")

    lines.append(f"{', '.join(summary_parts)}\n")

    # Per-language sections
    for lang, info in LANGUAGES.items():
        label = info["label"]
        lang_changes = changes[lang]
        if not any(lang_changes.values()):
            continue

        lines.append(f"\n### {label}\n")

        # Removed pages first (most important)
        if lang_changes["removed"]:
            lines.append("\n**Removed**\n")
            for page in lang_changes["removed"]:
                lines.append(f'- **{page["title"]}** (`{page["slug"]}.md`) — page no longer exists in documentation')

        # Added pages
        if lang_changes["added"]:
            lines.append("\n**Added**\n")
            for page in lang_changes["added"]:
                lines.append(f'- **{page["title"]}** (`{page["slug"]}.md`)')

        # Modified pages
        if lang_changes["modified"]:
            lines.append("\n**Modified**\n")
            for page in lang_changes["modified"]:
                detail = f'{page["added"]} lines added, {page["removed"]} removed'
                lines.append(f'- **{page["title"]}** (`{page["slug"]}.md`): {detail}')
                for heading in page.get("headings", []):
                    lines.append(f"  - New section: \"{heading}\"")

    lines.append("")
    return "\n".join(lines)


def prepend_to_changes_md(entry_md, changes_path):
    """Prepend a new entry to CHANGES.md, creating the file if needed.

    Skips if today's date already has an entry (prevents duplicates from
    repeated runs on the same day).
    """
    today = date.today().strftime("%Y-%m-%d")
    header = "# Documentation Changes\n\n"

    if os.path.exists(changes_path):
        with open(changes_path) as f:
            existing = f.read()
        # Skip if today's entry already exists
        if f"## {today}" in existing:
            print(f"  Entry for {today} already exists, skipping prepend")
            return
        # Strip the top-level heading if present (we re-add it)
        existing = re.sub(r"^# Documentation Changes\s*\n*", "", existing).strip()
    else:
        existing = ""

    parts = [header, entry_md]
    if existing:
        parts.append("\n---\n\n")
        parts.append(existing)
    parts.append("\n")

    with open(changes_path, "w") as f:
        f.write("".join(parts))


def generate_changelog_pdf(changes_md_path, output_dir):
    """Convert CHANGES.md to a PDF via pandoc + weasyprint."""
    if not shutil.which("pandoc") or not shutil.which("weasyprint"):
        print("  WARNING: pandoc or weasyprint not found, skipping PDF generation")
        return None

    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, "changes.html")
    pdf_path = os.path.join(output_dir, "changes.pdf")

    # CSS for A5 changelog
    css = """
    @page { size: A5; margin: 15mm 12mm 18mm 12mm; }
    body { font-family: sans-serif; font-size: 9pt; line-height: 1.5; color: #1a1a1a; }
    h1 { font-size: 16pt; color: #1a1a2e; border-bottom: 1.5pt solid #D97706; padding-bottom: 2mm; }
    h2 { font-size: 12pt; color: #D97706; margin-top: 6mm; }
    h3 { font-size: 10pt; color: #1a1a2e; margin-top: 4mm; }
    code { font-size: 7.5pt; background: #f9f2f4; padding: 0.2mm 0.8mm; border-radius: 0.8mm; color: #c7254e; }
    ul { padding-left: 5mm; }
    li { margin-bottom: 1mm; }
    """

    css_path = os.path.join(output_dir, "changelog.css")
    with open(css_path, "w") as f:
        f.write(css)

    # Pandoc: md → html
    result = subprocess.run(
        ["pandoc", changes_md_path, "-o", html_path, "--to=html5",
         "--standalone", "--css", css_path],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        print(f"  Pandoc failed: {result.stderr[:200]}")
        return None

    # WeasyPrint: html → pdf
    result = subprocess.run(
        ["weasyprint", html_path, pdf_path],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        print(f"  WeasyPrint failed: {result.stderr[:200]}")
        return None

    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"  Changelog PDF: {pdf_path} ({size_kb:.0f} KB)")
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="Generate documentation changelog")
    parser.add_argument("--basedir", required=True, help="Base working directory (repo root)")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation")
    args = parser.parse_args()

    basedir = os.path.abspath(args.basedir)

    print("Analyzing documentation changes...")
    changes = parse_git_diff(basedir)

    # Generate entry and prepend to CHANGES.md
    entry_md = generate_entry_md(changes)
    changes_path = os.path.join(basedir, "CHANGES.md")

    if entry_md is None:
        print("\nNo documentation changes detected.")
    else:
        prepend_to_changes_md(entry_md, changes_path)
        print(f"\nChangelog updated: {changes_path}")

        # Summary
        for lang in LANGUAGES:
            c = changes[lang]
            total = len(c["added"]) + len(c["modified"]) + len(c["removed"])
            if total:
                print(f"  {lang}: {len(c['added'])} added, {len(c['modified'])} modified, {len(c['removed'])} removed")

    # Generate PDF (from full CHANGES.md including history)
    if not args.no_pdf and os.path.exists(changes_path):
        output_dir = os.path.join(basedir, "output")
        print("\nGenerating changelog PDF...")
        generate_changelog_pdf(changes_path, output_dir)

    print("\nDone!")


if __name__ == "__main__":
    main()
