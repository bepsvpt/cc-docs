#!/usr/bin/env python3
"""Generate PDF by splitting markdown into sections, converting each to HTML
with Pandoc, combining them, and rendering to PDF with WeasyPrint.

Usage:
    python3 generate_pdf.py --basedir /path/to/workdir
    python3 generate_pdf.py --lang zh-TW --basedir /path/to/workdir
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LANGUAGES, LANG_CODES, lang_to_dir, COVER_TEXT, HTML_TITLES, sections_for_lang, heading_to_anchor


def check_dependencies():
    """Check all required dependencies and print actionable install commands if missing."""
    import platform
    is_mac = platform.system() == "Darwin"
    is_linux = platform.system() == "Linux"

    errors = []
    pip_missing = []

    # System: pandoc
    if not shutil.which("pandoc"):
        if is_mac:
            errors.append("  pandoc not found. Install: brew install pandoc")
        else:
            errors.append("  pandoc not found. Install: apt-get install -y pandoc")

    # weasyprint (CLI binary — works with both brew and pip installs)
    if not shutil.which("weasyprint"):
        if is_mac:
            errors.append("  weasyprint not found. Install: brew install weasyprint")
        else:
            pip_missing.append("weasyprint")
            errors.append("  weasyprint not found.")

    # Python: PyMuPDF (imported as fitz)
    try:
        import fitz
    except ImportError:
        errors.append("  PyMuPDF not found. Install: brew install pymupdf" if is_mac else "  PyMuPDF not found.")
        if not is_mac:
            pip_missing.append("PyMuPDF")

    if errors:
        print("ERROR: Missing dependencies:\n" + "\n".join(errors))
        print("\nFix all at once:")
        pip_flag = " --break-system-packages" if is_linux else ""
        pip_cmd = f"pip install {' '.join(pip_missing)}{pip_flag}" if pip_missing else ""
        if is_mac:
            pandoc_cmd = "brew install pandoc" if not shutil.which("pandoc") else ""
            parts = [p for p in [pandoc_cmd, pip_cmd] if p]
            print("  " + " && ".join(parts))
        else:
            pandoc_cmd = "apt-get install -y pandoc" if not shutil.which("pandoc") else ""
            parts = [p for p in [pandoc_cmd, pip_cmd] if p]
            print("  " + " && ".join(parts))
        sys.exit(1)


check_dependencies()

parser = argparse.ArgumentParser(description="Generate Claude Code PDF")
parser.add_argument("--lang", default="en", choices=LANG_CODES,
                    help="Language to generate (default: en)")
parser.add_argument("--basedir", required=True,
                    help="Base working directory for all files")
args = parser.parse_args()

# Resolve bundled font paths for @font-face src: url()
SCRIPT_DIR = Path(__file__).resolve().parent
FONTS_DIR = SCRIPT_DIR.parent / "assets" / "fonts"
EMOJI_FONT_PATH = FONTS_DIR / "NotoColorEmoji.ttf"
CJK_FONT_PATH = FONTS_DIR / "NotoSansCJKtc-Regular.otf"
CJK_BOLD_FONT_PATH = FONTS_DIR / "NotoSansCJKtc-Bold.otf"
MONO_FONT_PATH = FONTS_DIR / "JetBrainsMono-Regular.ttf"
MONO_BOLD_FONT_PATH = FONTS_DIR / "JetBrainsMono-Bold.ttf"

LANG = args.lang
BASEDIR = args.basedir
IS_CJK = LANGUAGES[LANG]["cjk"]
TODAY = date.today().strftime("%Y-%m-%d")

LANG_DIR = lang_to_dir(LANG)
LANG_SUFFIX = f"_{LANG_DIR}" if LANG != "en" else ""
MERGED_MD = os.path.join(BASEDIR, "build", f"merged_{LANG_DIR}.md")
WORK_DIR = os.path.join(BASEDIR, "build", f"html_{LANG_DIR}")
OUTPUT_DIR = os.path.join(BASEDIR, "output")
OUTPUT_PDF = os.path.join(OUTPUT_DIR, f"claude_code_documentation{LANG_SUFFIX}.pdf")
DOCS_DIR = os.path.join(BASEDIR, "docs", LANG_DIR)

if not os.path.isfile(MERGED_MD):
    print(f"ERROR: Merged markdown not found: {MERGED_MD}")
    print(f"Run merge_docs.py first: python3 {SCRIPT_DIR / 'merge_docs.py'} --lang {LANG} --basedir {BASEDIR}")
    sys.exit(1)
if not os.path.isdir(DOCS_DIR):
    print(f"ERROR: Docs directory not found: {DOCS_DIR}")
    print(f"Run download_md.py first: python3 {SCRIPT_DIR / 'download_md.py'} --lang {LANG} --basedir {BASEDIR}")
    sys.exit(1)

os.makedirs(WORK_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Split merged markdown by Part headings
print("Step 1: Splitting merged markdown into sections...")
with open(MERGED_MD, 'r') as f:
    content = f.read()

parts = re.split(r'\\newpage\s*\n+(?=# Part \d+:)', content)
parts = [p.strip() for p in parts if p.strip()]
print(f"  Found {len(parts)} sections")

# Step 2: Convert each part to HTML with Pandoc
print("Step 2: Converting each section to HTML with Pandoc...")
html_bodies = []

for i, part in enumerate(parts):
    md_path = os.path.join(WORK_DIR, f"part_{i:02d}.md")
    html_path = os.path.join(WORK_DIR, f"part_{i:02d}.html")

    part_clean = part.replace('\\newpage', '')

    with open(md_path, 'w') as f:
        f.write(part_clean)

    result = subprocess.run([
        "pandoc", md_path,
        "-o", html_path,
        "--to=html5",
        "--highlight-style=tango",
    ], capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        print(f"  Part {i} failed: {result.stderr[:200]}")
        with open(html_path, 'w') as f:
            f.write(f"<h1>Part {i}</h1><pre>{part_clean[:5000]}</pre>")
    else:
        print(f"  Part {i}: OK ({os.path.getsize(html_path) // 1024} KB)")

    with open(html_path, 'r') as f:
        html_bodies.append(f.read())

# Step 3: Build TOC
print("Step 3: Building Table of Contents...")

SECTIONS = sections_for_lang(LANG)

# Load local→English fragment map for non-English (produced by merge_docs.py).
# WeasyPrint PDF named destinations require ASCII IDs, so all heading anchors
# must be English (ASCII). This map translates local heading anchors to English.
_fmap_path = os.path.join(BASEDIR, "build", f"fragment_map_{LANG_DIR}.json")
if LANG != "en" and os.path.isfile(_fmap_path):
    import json
    with open(_fmap_path) as _f:
        _local_to_english = json.load(_f)
    print(f"  Loaded fragment map: {len(_local_to_english)} local→English translations")
else:
    _local_to_english = {}

def _ascii_anchor(text):
    """Compute an ASCII-safe heading anchor. For non-English, translates to English."""
    anchor = heading_to_anchor(text)
    return _local_to_english.get(anchor, anchor)

# For non-English, also read English doc titles for chapter anchors
EN_DOCS_DIR = os.path.join(BASEDIR, "docs", "en")

toc_entries = []
for section_idx, (section_title, slugs) in enumerate(SECTIONS, 1):
    part_title = f"Part {section_idx}: {section_title}"
    anchor = heading_to_anchor(part_title)
    toc_entries.append(('part', part_title, anchor))

    for slug in slugs:
        md_path = os.path.join(DOCS_DIR, f"{slug}.md")
        if not os.path.exists(md_path):
            continue
        with open(md_path, 'r') as f:
            first_lines = f.read(500)
        m2 = re.search(r'^#\s+(.+?)(?:\s*\{[^}]*\})?$', first_lines, re.MULTILINE)
        title = m2.group(1).strip() if m2 else slug.replace('-', ' ').title()
        # Use English anchor (ASCII) for non-English PDFs
        if LANG != "en":
            en_md_path = os.path.join(EN_DOCS_DIR, f"{slug}.md")
            if os.path.exists(en_md_path):
                with open(en_md_path, 'r') as f:
                    en_first = f.read(500)
                en_m = re.search(r'^#\s+(.+?)(?:\s*\{[^}]*\})?$', en_first, re.MULTILINE)
                en_title = en_m.group(1).strip() if en_m else slug.replace('-', ' ').title()
                anchor = heading_to_anchor(en_title)
            else:
                anchor = _ascii_anchor(title)
        else:
            anchor = heading_to_anchor(title)
        toc_entries.append(('chapter', title, anchor))

toc_html = '<nav id="toc"><h1>Table of Contents</h1>\n'
for kind, title, anchor in toc_entries:
    if kind == 'part':
        toc_html += f'<p class="toc-part"><a href="#{anchor}">{title}</a></p>\n'
    else:
        toc_html += f'<p class="toc-chapter"><a href="#{anchor}">{title}</a></p>\n'
toc_html += '</nav>\n'

# Inject explicit id attributes into HTML headings for reliable TOC linking.
# Pandoc generates its own IDs which may not match our heading_to_anchor() output.
# Replace (not append) to avoid duplicate id attributes in the output HTML.
for i, body in enumerate(html_bodies):
    for _, title, anchor in toc_entries:
        def _replace_toc_id(m, _anchor=anchor):
            tag, attrs, inner = m.group(1), m.group(2), m.group(3)
            attrs = re.sub(r'\s*id="[^"]*"', '', attrs)
            return f'{tag}{attrs} id="{_anchor}">{inner}{title}'
        body = re.sub(
            rf'(<h[12])([^>]*)>((?:<[^>]+>)*){re.escape(title)}',
            _replace_toc_id, body, count=1
        )
    html_bodies[i] = body

# Second pass: normalize ALL heading IDs (h1-h6) to ASCII-safe anchors.
# For English: uses heading_to_anchor() directly (already ASCII).
# For non-English: translates local anchor to English via fragment map.
# Skip headings whose id was already set by the TOC pass above.
toc_anchors = {anchor for _, _, anchor in toc_entries}
for i, body in enumerate(html_bodies):
    def _normalize_heading_id(m):
        tag, attrs, inner, closing = m.group(1), m.group(2), m.group(3), m.group(4)
        plain_text = re.sub(r'<[^>]+>', '', inner)
        anchor = _ascii_anchor(plain_text)
        if anchor in toc_anchors:
            return m.group(0)
        attrs = re.sub(r'\s*id="[^"]*"', '', attrs)
        return f'{tag}{attrs} id="{anchor}">{inner}{closing}'
    body = re.sub(r'(<h[1-6])([^>]*)>(.*?)(</h[1-6]>)', _normalize_heading_id, body)
    html_bodies[i] = body

# Step 4: Assemble full HTML
print("Step 4: Assembling full HTML document...")

CSS_FONTS = f"""
@font-face {{
    font-family: 'EmojiOnly';
    src: url('{EMOJI_FONT_PATH}');
    unicode-range: U+200D, U+2049, U+20E3, U+2139, U+2194-2199, U+21A9-21AA, U+231A-231B, U+2328, U+23CF, U+23E9-23F3, U+23F8-23FA, U+24C2, U+25AA-25AB, U+25B6, U+25C0, U+25FB-25FE, U+2600-27BF, U+2934-2935, U+2B05-2B07, U+2B1B-2B1C, U+2B50, U+2B55, U+3030, U+303D, U+3297, U+3299, U+FE00-FE0F, U+1F000-1FFFF;
}}
@font-face {{
    font-family: 'Noto Sans CJK TC';
    src: url('{CJK_FONT_PATH}');
}}
@font-face {{
    font-family: 'Noto Sans CJK TC';
    src: url('{CJK_BOLD_FONT_PATH}');
    font-weight: bold;
}}
@font-face {{
    font-family: 'JetBrains Mono';
    src: url('{MONO_FONT_PATH}');
}}
@font-face {{
    font-family: 'JetBrains Mono';
    src: url('{MONO_BOLD_FONT_PATH}');
    font-weight: bold;
}}
"""

if IS_CJK:
    FONT_BODY = "'Noto Sans CJK TC', 'DejaVu Serif', 'EmojiOnly', Georgia, serif"
    FONT_SANS = "'Noto Sans CJK TC', 'DejaVu Sans', 'EmojiOnly', sans-serif"
    FONT_MONO = "'JetBrains Mono', 'Noto Sans CJK TC', 'EmojiOnly', monospace"
else:
    FONT_BODY = "'DejaVu Serif', 'EmojiOnly', Georgia, serif"
    FONT_SANS = "'DejaVu Sans', 'EmojiOnly', sans-serif"
    FONT_MONO = "'JetBrains Mono', 'EmojiOnly', monospace"

CSS_PAGE = f"""
@page {{
    size: A5;
    margin: 15mm 12mm 18mm 12mm;
    @bottom-center {{
        content: "— " counter(page) " —";
        font-size: 7pt;
        color: #999;
        font-family: {FONT_SANS};
    }}
    @top-left {{
        content: string(chapter-title);
        font-size: 6.5pt;
        color: #999;
        font-family: {FONT_SANS};
    }}
}}
@page :first {{
    @bottom-center {{ content: none; }}
    @top-left {{ content: none; }}
}}
@page toc-page {{
    @top-left {{ content: none; }}
}}
"""

CSS_COVER = f"""
.cover {{
    page-break-after: always;
    text-align: center;
    padding-top: 35mm;
}}
.cover h1 {{
    font-family: {FONT_SANS};
    font-size: 26pt;
    color: #1a1a2e;
    border: none;
    margin-bottom: 6mm;
}}
.cover .subtitle {{ font-size: 12pt; color: #555; margin: 3mm 0; }}
.cover .author {{ font-size: 11pt; color: #666; margin: 5mm 0; }}
.cover .date {{ font-size: 10pt; color: #888; margin: 8mm 0; }}
.cover .desc {{ font-size: 8.5pt; color: #888; margin-top: 12mm; line-height: 1.5; }}
.cover .note {{ font-size: 7pt; color: #aaa; margin-top: 8mm; }}
"""

CSS_TOC = f"""
#toc {{
    page-break-after: always;
    page: toc-page;
}}
#toc h1 {{
    font-family: {FONT_SANS};
    font-size: 18pt;
    color: #1a1a2e;
    border-bottom: 1.5pt solid #D97706;
    padding-bottom: 2mm;
    margin-bottom: 4mm;
}}
.toc-part {{
    font-family: {FONT_SANS};
    font-weight: bold;
    font-size: 9pt;
    color: #1a1a2e;
    margin-top: 3mm;
    margin-bottom: 0.5mm;
}}
.toc-chapter {{
    font-size: 7.5pt;
    color: #444;
    margin: 0.3mm 0 0.3mm 5mm;
}}
#toc a {{ color: #333; text-decoration: none; }}
#toc a:hover {{ color: #1a6dcc; }}
.toc-part a::after, .toc-chapter a::after {{
    content: target-counter(attr(href), page);
    float: right;
    font-weight: normal;
    color: #999;
}}
"""

CSS_TYPOGRAPHY = f"""
body {{
    font-family: {FONT_BODY};
    font-size: 8.5pt;
    line-height: 1.5;
    color: #1a1a1a;
    orphans: 3;
    widows: 3;
    hyphens: auto;
    -webkit-hyphens: auto;
}}

h1 {{
    font-family: {FONT_SANS};
    font-size: 16pt;
    color: #1a1a2e;
    margin-top: 0;
    margin-bottom: 5mm;
    padding-bottom: 2mm;
    border-bottom: 1.5pt solid #D97706;
    page-break-before: always;
    hyphens: none;
    string-set: chapter-title "";
}}

h2 {{
    font-family: {FONT_SANS};
    font-size: 12pt;
    color: white;
    background-color: #D97706;
    padding: 2mm 3mm;
    border-radius: 1.5mm;
    margin-top: 6mm;
    margin-bottom: 3mm;
    page-break-before: always;
    page-break-after: avoid;
    hyphens: none;
    string-set: chapter-title content();
}}
h1 + h2 {{
    page-break-before: avoid;
}}

h3 {{
    font-family: {FONT_SANS};
    font-size: 10pt;
    color: #1a1a2e;
    margin-top: 4mm;
    margin-bottom: 2mm;
    page-break-after: avoid;
    hyphens: none;
}}

h4, h5, h6 {{
    font-family: {FONT_SANS};
    font-size: 8.5pt;
    color: #444;
    margin-top: 3mm;
    margin-bottom: 1.5mm;
    page-break-after: avoid;
    hyphens: none;
}}

p {{ margin: 0 0 2mm 0; }}
a {{ color: #1a6dcc; text-decoration: underline; text-decoration-color: #aaccee; text-underline-offset: 1pt; }}

ul, ol {{ margin: 1mm 0 2mm 0; padding-left: 5mm; }}
li {{ margin-bottom: 0.8mm; orphans: 2; widows: 2; }}
li > p {{ margin-bottom: 0.5mm; }}
"""

CSS_CODE = f"""
code {{
    font-family: {FONT_MONO};
    font-size: 7pt;
    color: #c7254e;
    background-color: #f9f2f4;
    padding: 0.2mm 0.8mm;
    border-radius: 0.8mm;
    hyphens: none;
}}

pre {{
    background-color: #f4f4ef;
    border: 0.3pt solid #e0e0d8;
    border-radius: 1.5mm;
    padding: 3mm;
    margin: 2mm 0 3mm 0;
    page-break-inside: avoid;
    hyphens: none;
}}
pre code {{
    font-size: 6.5pt;
    line-height: 1.35;
    color: #333;
    background: none;
    padding: 0;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: normal;
}}

code span.kw {{ color: #204a87; font-weight: bold; }}
code span.dt {{ color: #204a87; }}
code span.dv, code span.bn, code span.fl {{ color: #0000cf; }}
code span.ch, code span.st {{ color: #4e9a06; }}
code span.co {{ color: #8f5902; font-style: italic; }}
code span.ot {{ color: #8f5902; }}
code span.al {{ color: #ef2929; }}
code span.fu {{ color: #000000; }}
code span.er {{ color: #a40000; font-weight: bold; }}
code span.cf {{ color: #204a87; font-weight: bold; }}
code span.op {{ color: #ce5c00; font-weight: bold; }}
code span.va {{ color: #000000; }}

blockquote {{
    border-left: 2mm solid #D97706;
    margin: 2mm 0;
    padding: 1.5mm 3mm;
    color: #555;
    font-style: italic;
    background-color: #fdf8f3;
}}
blockquote p {{ margin: 0; }}
"""

CSS_CALLOUTS = """
.callout-note, .callout-info, .callout-tip, .callout-warning {
    margin: 3mm 0;
    padding: 2.5mm 3mm;
    border-radius: 1.5mm;
    font-size: 7.5pt;
    line-height: 1.4;
}
.callout-note {
    border-left: 2mm solid #3B82F6;
    background-color: #EFF6FF;
    color: #1E3A5F;
}
.callout-info {
    border-left: 2mm solid #6366F1;
    background-color: #EEF2FF;
    color: #312E81;
}
.callout-tip {
    border-left: 2mm solid #10B981;
    background-color: #ECFDF5;
    color: #064E3B;
}
.callout-warning {
    border-left: 2mm solid #F59E0B;
    background-color: #FFFBEB;
    color: #78350F;
}
"""

CSS_TABLES = f"""
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 2mm 0;
    font-size: 7.5pt;
    page-break-inside: auto;
}}
tr {{
    page-break-inside: avoid;
}}
thead {{
    display: table-header-group;
}}
th, td {{
    border: 0.3pt solid #ddd;
    padding: 1.5mm 2mm;
    text-align: left;
    overflow-wrap: break-word;
    word-wrap: break-word;
}}
td:last-child {{
    word-break: break-all;
    overflow-wrap: break-word;
}}
td:last-child code {{
    word-break: break-all;
    overflow-wrap: break-word;
}}
td code {{
    overflow-wrap: break-word;
    word-wrap: break-word;
}}
th {{
    background-color: #f0f0ea;
    font-family: {FONT_SANS};
    font-weight: bold;
}}
"""

CSS_MEDIA = """
hr { border: none; border-top: 0.5pt solid #ddd; margin: 4mm 0; }

figure {
    margin: 3mm 0;
    padding: 0;
    width: 100%;
}
figcaption {
    font-size: 6.5pt;
    color: #666;
    text-align: center;
    margin-top: 1mm;
}

img {
    max-width: 100%;
    max-height: 180mm;
    height: auto;
    width: auto;
    display: block;
    margin: 0 auto;
    border: 0.3pt solid #e0e0d8;
    border-radius: 1.5mm;
    object-fit: contain;
}
p > img { margin: 3mm 0; }
"""

CSS = "\n".join([CSS_FONTS, CSS_PAGE, CSS_COVER, CSS_TOC, CSS_TYPOGRAPHY,
                 CSS_CODE, CSS_CALLOUTS, CSS_TABLES, CSS_MEDIA])

_cover = COVER_TEXT[LANG]
cover_html = f"""
<div class="cover">
    <h1 style="border:none; page-break-before:avoid;">Claude Code</h1>
    <p class="subtitle">{_cover['subtitle']}</p>
    <p class="author">By Anthropic</p>
    <p class="date">{_cover['date_label']}：{TODAY}</p>
    <p class="desc">{_cover['desc']}</p>
    <p class="note">{_cover['note']}</p>
    <p class="note">Generated by: github.com/bepsvpt/cc-docs</p>
</div>
"""

html_lang = LANG
html_title = HTML_TITLES[LANG]

full_html = f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<title>{html_title}</title>
<style>{CSS}</style>
</head>
<body>
{cover_html}
{toc_html}
{''.join(html_bodies)}
</body>
</html>
"""

combined_path = os.path.join(WORK_DIR, "combined.html")

# Post-process: unescape \| inside <code> tags
def unescape_code_pipes(m):
    return m.group(0).replace('\\|', '|')
full_html = re.sub(r'<code>[^<]+</code>', unescape_code_pipes, full_html)

# Post-process: replace colgroup for multi-column tables
def fix_colgroup(m):
    table_html = m.group(0)
    col_count = len(re.findall(r'<col\s', table_html))
    new_colgroup = None
    if col_count == 3:
        new_colgroup = '<colgroup><col style="width:30%"/><col style="width:40%"/><col style="width:30%"/></colgroup>\n'
    elif col_count == 4:
        new_colgroup = '<colgroup><col style="width:15%"/><col style="width:35%"/><col style="width:25%"/><col style="width:25%"/></colgroup>\n'
    elif col_count == 5:
        new_colgroup = '<colgroup><col style="width:12%"/><col style="width:28%"/><col style="width:20%"/><col style="width:20%"/><col style="width:20%"/></colgroup>\n'
    if new_colgroup:
        table_html = re.sub(r'<colgroup>.*?</colgroup>\s*', '', table_html, flags=re.DOTALL)
        table_html = re.sub(r'(<table[^>]*>)\s*', r'\1\n' + new_colgroup, table_html, count=1)
        table_html = re.sub(r'<table([^>]*)>', r'<table\1 style="table-layout:fixed">', table_html, count=1)
    return table_html

full_html = re.sub(r'<table[^>]*>.*?</table>', fix_colgroup, full_html, flags=re.DOTALL)

with open(combined_path, 'w') as f:
    f.write(full_html)
print(f"  Combined HTML: {os.path.getsize(combined_path) / 1024:.0f} KB")

# Step 5: Generate PDF with WeasyPrint
print("Step 5: Generating PDF with WeasyPrint...")
result = subprocess.run(["weasyprint", combined_path, OUTPUT_PDF],
                        capture_output=True, text=True, timeout=300)
if result.returncode != 0:
    print(f"  WeasyPrint failed: {result.stderr[:500]}")
    sys.exit(1)

size_mb = os.path.getsize(OUTPUT_PDF) / (1024 * 1024)
print(f"\nDone! {OUTPUT_PDF} ({size_mb:.1f} MB)")

# Count pages
import fitz
doc = fitz.open(OUTPUT_PDF)
print(f"Total pages: {doc.page_count}")
doc.close()
