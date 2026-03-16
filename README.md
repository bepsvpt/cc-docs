# cc-docs

Automated tracking and PDF generation for [Claude Code](https://code.claude.com/docs) documentation.

## What this does

- **Tracks changes**: Downloads all Claude Code doc pages as markdown and commits them to git, creating a full change history
- **Generates PDFs**: Produces professionally formatted A5 e-books in English and Traditional Chinese
- **Publishes changelog**: Detects added, modified, and removed pages, and generates a diff summary
- **Runs daily**: GitHub Actions checks for updates every day and only rebuilds when content changes

## How it works

```
check_sitemap.py    → Has anything changed on code.claude.com/docs?
download_md.py      → Fetch all markdown pages (64 en + 59 zh-TW)
generate_changelog  → Diff against last commit → CHANGES.md + PDF
merge_docs.py       → Combine pages into structured document (13 parts)
generate_pdf.py     → Pandoc + WeasyPrint → A5 PDF with styling
```

The CI pipeline commits updated markdown to `main` (so git history captures every doc change) and deploys PDFs + changelog to GitHub Pages.

## Generate PDFs locally

**Prerequisites**: `pandoc`, `weasyprint`, `PyMuPDF` — the script checks and prints install commands if missing.

```bash
# English
python3 scripts/download_md.py --basedir .
python3 scripts/merge_docs.py --basedir .
python3 scripts/generate_pdf.py --basedir .

# Traditional Chinese
python3 scripts/download_md.py --lang zh-TW --basedir .
python3 scripts/merge_docs.py --lang zh-TW --basedir .
python3 scripts/generate_pdf.py --lang zh-TW --basedir .
```

Output: `output/claude_code_documentation.pdf` (~795 pages, ~5 MB)

## Licensing

The documentation content is sourced from [code.claude.com/docs](https://code.claude.com/docs) and is owned by Anthropic. This project provides tooling for personal/educational use. Check Anthropic's terms for redistribution rights.
