"""Markdown transformation pipeline for cleaning Mintlify/MDX content.

Extracted from merge_docs.py's clean_md() function. Each transform is a
pure function (str → str) that handles one category of cleanup. The pipeline
order matches the original clean_md() exactly — reordering can produce
different output.

Pipeline:
    strip_metadata → protect_code_spans → convert_jsx_components →
    clean_html_tags → resolve_links → restore_code_spans →
    dedent_blocks → finalize
"""

import os
import re
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import LANGUAGES

# Dynamic regex alternation for all supported language codes
_LANG_ALTERNATION = '|'.join(re.escape(l) for l in LANGUAGES)


# ---------------------------------------------------------------------------
# 1. strip_metadata — remove doc headers, frontmatter, comments, imports
# ---------------------------------------------------------------------------

def strip_metadata(md):
    """Remove doc index header, frontmatter, HTML comments, imports, exports."""
    # Remove doc index header
    md = re.sub(r'^>\s*##\s*Documentation Index.*?(?=\n#)', '', md, flags=re.DOTALL)
    # Remove frontmatter
    md = re.sub(r'^---\s*\n.*?\n---\s*\n', '', md, flags=re.DOTALL)
    # Remove HTML comments
    md = re.sub(r'<!--.*?-->', '', md, flags=re.DOTALL)
    # Remove import statements
    md = re.sub(r'^import\s+.*$', '', md, flags=re.MULTILINE)
    # Remove exported JSX component definitions
    md = re.sub(r'^export\s+const\s+\w+\s*=.*?^};', '', md, flags=re.DOTALL | re.MULTILINE)
    return md


# ---------------------------------------------------------------------------
# 1b. protect/restore code spans — shield code from HTML/link transforms
# ---------------------------------------------------------------------------

def protect_code_spans(md):
    """Extract code spans into placeholders to shield them from HTML/link transforms.

    Phase 1 extracts fenced code blocks (``` or longer), Phase 2 extracts
    inline code spans (single and double backtick).  Returns (md, store)
    where store[i] is the original text for placeholder i.
    """
    store = []

    def _placeholder(original):
        idx = len(store)
        store.append(original)
        return f'\x00CODE{idx}\x00'

    # -- Phase 1: fenced code blocks (line-by-line) --
    lines = md.split('\n')
    out = []
    block_lines = []
    fence_marker = None

    for line in lines:
        if fence_marker is None:
            m = re.match(r'^(\s*)(`{3,})(\w*)(.*)', line)
            if m:
                fence_marker = m.group(2)
                indent, lang, rest = m.group(1), m.group(3), m.group(4)
                # Clean annotations from the opening fence line (moved from
                # clean_html_tags lines 217-219 — they can't run there because
                # fenced blocks are placeholders by then).
                if rest:
                    rest = re.sub(r'[ \t]+theme=\{null\}', '', rest)
                    if lang and rest.strip():
                        rest = ''
                block_lines = [f'{indent}{fence_marker}{lang}{rest}']
            else:
                out.append(line)
        else:
            block_lines.append(line)
            stripped = line.strip()
            close_m = re.match(r'^(`{3,})\s*$', stripped)
            if close_m and len(close_m.group(1)) >= len(fence_marker):
                out.append(_placeholder('\n'.join(block_lines)))
                fence_marker = None
                block_lines = []

    # Unclosed fence — keep original lines unprotected
    if block_lines:
        out.extend(block_lines)

    md = '\n'.join(out)

    # -- Phase 2: inline code spans --
    # Double-backtick first (can contain single backticks), then single-backtick.
    md = re.sub(r'``[^`]+``', lambda m: _placeholder(m.group(0)), md)
    md = re.sub(r'`[^`\n]+`', lambda m: _placeholder(m.group(0)), md)

    return md, store


def restore_code_spans(md, store):
    """Replace placeholders with their original code span content."""
    return re.sub(r'\x00CODE(\d+)\x00', lambda m: store[int(m.group(1))], md)


# ---------------------------------------------------------------------------
# 2. convert_jsx_components — MCPServersTable, img, Steps, Card, Tab, callouts
# ---------------------------------------------------------------------------

MCP_SERVERS_TABLE = """
| Server | Description | Command |
|--------|-------------|---------|
| **Notion** | Connect your Notion workspace to search, update, and power workflows across tools | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Canva** | Search, create, autofill, and export Canva designs | `claude mcp add --transport http canva https://mcp.canva.com/mcp` |
| **Figma** | Generate diagrams and better code from Figma context | `claude mcp add --transport http figma-remote-mcp https://mcp.figma.com/mcp` |
| **Atlassian** | Access Jira & Confluence from Claude | `claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp` |
| **Linear** | Manage issues, projects & team workflows in Linear | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| **monday.com** | Manage projects, boards, and workflows in monday.com | `claude mcp add --transport http monday https://mcp.monday.com/mcp` |
| **Intercom** | Access to Intercom data for better customer insights | `claude mcp add --transport http intercom https://mcp.intercom.com/mcp` |
| **Vercel** | Analyze, debug, and manage projects and deployments | `claude mcp add --transport http vercel https://mcp.vercel.com` |
| **Granola** | The AI notepad for meetings | `claude mcp add --transport http granola https://mcp.granola.ai/mcp` |
| **Asana** | Connect to Asana to coordinate tasks, projects, and goals | `claude mcp add --transport streamable-http asana https://mcp.asana.com/v2/mcp` |
| **Miro** | Access and create new content on Miro boards | `claude mcp add --transport http miro https://mcp.miro.com/` |
| **Sentry** | Search, query, and debug errors intelligently | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **Supabase** | Manage databases, authentication, and storage | `claude mcp add --transport http supabase https://mcp.supabase.com/mcp` |
| **Hugging Face** | Access the Hugging Face Hub and thousands of Gradio Apps | `claude mcp add --transport http hugging-face https://huggingface.co/mcp` |
| **Context7** | Up-to-date docs for LLMs and AI code editors | `claude mcp add --transport http context7 https://mcp.context7.com/mcp` |
| **Stripe** | Payment processing and financial infrastructure tools | `claude mcp add --transport http stripe https://mcp.stripe.com` |
| **Microsoft Learn** | Search trusted Microsoft docs to power your development | `claude mcp add --transport http microsoft-learn https://learn.microsoft.com/api/mcp` |
| **Clay** | Find prospects. Research accounts. Personalize outreach | `claude mcp add --transport http clay https://api.clay.com/v3/mcp` |
| **Webflow** | Manage Webflow CMS, pages, assets and sites | `claude mcp add --transport http webflow https://mcp.webflow.com/mcp` |
| **Cloudflare** | Build applications with compute, storage, and AI | `claude mcp add --transport http cloudflare https://bindings.mcp.cloudflare.com/mcp` |
| **Ramp** | Search, access, and analyze your Ramp financial data | `claude mcp add --transport http ramp https://ramp-mcp-remote.ramp.com/mcp` |
| **ZoomInfo** | Enrich contacts & accounts with GTM intelligence | `claude mcp add --transport http zoominfo https://mcp.zoominfo.com/mcp` |
| **Netlify** | Create, deploy, manage, and secure websites on Netlify | `claude mcp add --transport http netlify https://netlify-mcp.netlify.app/mcp` |
| **Make** | Run Make scenarios and manage your Make account | `claude mcp add --transport http make https://mcp.make.com` |
| **GoDaddy** | Search domains and check availability | `claude mcp add --transport http godaddy https://api.godaddy.com/v1/domains/mcp` |
| **Google Cloud BigQuery** | BigQuery: Advanced analytical insights for agents | `claude mcp add --transport http bigquery https://bigquery.googleapis.com/mcp` |
| **PayPal** | Access PayPal payments platform | `claude mcp add --transport http paypal https://mcp.paypal.com/mcp` |
| **PostHog** | Query, analyze, and manage your PostHog insights | `claude mcp add --transport http posthog https://mcp.posthog.com/mcp` |
| **Similarweb** | Real time web, mobile app, and market data | `claude mcp add --transport http similarweb https://mcp.similarweb.com` |
| **Crypto.com** | Real time prices, orders, charts, and more for crypto | `claude mcp add --transport http crypto.com https://mcp.crypto.com/market-data/mcp` |
| **Attio** | Search, manage, and update your Attio CRM from Claude | `claude mcp add --transport http attio https://mcp.attio.com/mcp` |
| **Trivago** | Find your ideal hotel at the best price | `claude mcp add --transport http trivago https://mcp.trivago.com/mcp` |
| **Jam** | Record screen and collect automatic context for issues | `claude mcp add --transport http jam https://mcp.jam.dev/mcp` |
| **Consensus** | Explore scientific research | `claude mcp add --transport http consensus https://mcp.consensus.app/mcp` |
| **Clockwise** | Advanced scheduling and time management for work | `claude mcp add --transport http clockwise https://mcp.getclockwise.com/mcp` |
| **Square** | Search and manage transaction, merchant, and payment data | `claude mcp add --transport sse square https://mcp.squareup.com/sse` |
| **Egnyte** | Securely access and analyze Egnyte content | `claude mcp add --transport http egnyte https://mcp-server.egnyte.com/mcp` |
| **Pylon** | Search and manage Pylon support issues | `claude mcp add --transport http pylon https://mcp.usepylon.com/` |
| **Honeycomb** | Query and explore observability data and SLOs | `claude mcp add --transport http honeycomb https://mcp.honeycomb.io/mcp` |
"""


def convert_jsx_components(md, images_dir):
    """Convert Mintlify/MDX components to markdown equivalents."""
    # Replace <MCPServersTable> with static server list
    md = re.sub(r'<MCPServersTable\s[^>]*/>', MCP_SERVERS_TABLE, md)
    # Remove other self-closing JSX invocations
    md = re.sub(r'<[A-Z]\w+\s[^>]*/>', '', md)

    # Convert <img> tags to markdown images with local paths
    def replace_img(m):
        tag = m.group(0)
        if 'dark:block' in tag or 'className="hidden ' in tag:
            return ''
        alt_m = re.search(r'alt="([^"]*)"', tag)
        alt = alt_m.group(1) if alt_m else ''
        dp = re.search(r'data-path="images/([^"]+)"', tag)
        if dp:
            local_path = os.path.abspath(os.path.join(images_dir, dp.group(1)))
            if os.path.exists(local_path):
                return f'\n\n![{alt}]({local_path})\n\n'
        return f'*[Image: {alt}]*' if alt else ''
    md = re.sub(r'<img\s[^>]*?/?>', replace_img, md, flags=re.DOTALL)

    # Convert <Steps>/<Step> tags
    step_counter = [0]
    def replace_steps_or_step(m):
        tag = m.group(0)
        if tag.startswith('<Steps'):
            step_counter[0] = 0
            return ''
        title_m = re.search(r'title="([^"]*)"', tag)
        step_counter[0] += 1
        if title_m:
            return f'\n\n**Step {step_counter[0]}: {title_m.group(1)}**\n\n'
        return f'\n\n**Step {step_counter[0]}**\n\n'
    md = re.sub(r'<Steps[^>]*>|<Step\s[^>]*>', replace_steps_or_step, md)

    # Convert <Card> tags
    def replace_card(m):
        tag = m.group(0)
        title_m = re.search(r'title="([^"]*)"', tag)
        href_m = re.search(r'href="([^"]*)"', tag)
        title = title_m.group(1) if title_m else ''
        if title and href_m:
            return f'\n- [{title}]({href_m.group(1)})'
        elif title:
            return f'\n- **{title}**'
        return ''
    md = re.sub(r'<Card\s[^>]*?/?>', replace_card, md)

    # Convert <Tab> tags
    def replace_tab(m):
        tag = m.group(0)
        title_m = re.search(r'title="([^"]*)"', tag)
        if title_m:
            return f'\n\n**{title_m.group(1)}**\n\n'
        return ''
    md = re.sub(r'<Tab\s[^>]*>', replace_tab, md)

    # Callout divs
    for tag, css_class in [('Note', 'callout-note'), ('Info', 'callout-info'),
                            ('Tip', 'callout-tip'), ('Warning', 'callout-warning')]:
        md = re.sub(rf'<{tag}[^>]*>', f'\n\n<div class="{css_class}">\n\n**{tag}:**\n\n', md)
        md = re.sub(rf'</{tag}>', '\n\n</div>\n\n', md)

    return md


# ---------------------------------------------------------------------------
# 3. clean_html_tags — strip remaining HTML/MDX tags, validate images
# ---------------------------------------------------------------------------

def clean_html_tags(md, images_dir):
    """Strip remaining HTML/MDX tags, handle <br>, validate markdown images."""
    # Remove Mintlify/MDX component tags (keep content)
    custom_tags = (
        'Tabs|Tab|Accordion|AccordionGroup|Info|Tip|Warning|Note|'
        'CardGroup|Steps|Step|Frame|Snippet|CodeGroup|'
        'ResponseField|ParamField|Expandable|Update|CodeBlock'
    )
    md = re.sub(rf'</?(?:{custom_tags})[^>]*?/?>', '', md)

    # Remove HTML div tags (keep content), preserve callout divs
    def strip_div(m):
        tag = m.group(0)
        if 'class="callout-' in tag:
            return tag
        if tag == '</div>':
            return tag
        return ''
    md = re.sub(r'</?div[^>]*>', strip_div, md)
    md = re.sub(r'</?(?:span|strong|em|sup|sub|details|summary|section|article|aside|figure|figcaption|picture|source|video|audio|iframe)[^>]*>', '', md)

    # Replace <br> with space inside table rows, newline elsewhere
    lines = md.split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('|') and '<br' in line:
            lines[i] = re.sub(r'<br\s*/?>', ' ', line)
    md = '\n'.join(lines)
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'</?(?:table|thead|tbody|tfoot|tr|td|th|caption|colgroup|col)[^>]*>', '', md)

    # Remove remaining non-standard HTML tags (preserve callout divs)
    def strip_remaining_open(m):
        if 'class="callout-' in m.group(0):
            return m.group(0)
        return ''
    def strip_remaining_close(m):
        if m.group(0) == '</div>':
            return m.group(0)
        return ''
    md = re.sub(r'<(?!http)[a-zA-Z][a-zA-Z0-9_-]*(?:\s[^>]*)?\s*/?>', strip_remaining_open, md)
    md = re.sub(r'</[a-zA-Z][a-zA-Z0-9_-]*\s*>', strip_remaining_close, md)

    # Keep markdown images that point to local files
    def handle_md_img(m):
        alt = m.group(1)
        path = m.group(2)
        if images_dir in path or path.startswith('/'):
            if os.path.exists(path):
                return m.group(0)
        return f'*[Image: {alt}]*' if alt else ''
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', handle_md_img, md)

    return md


# ---------------------------------------------------------------------------
# 4. resolve_links — convert internal doc links to PDF anchors
# ---------------------------------------------------------------------------

def resolve_links(md, slug_to_anchor, base_url, lang_path, fragment_map=None):
    """Resolve internal doc links to PDF anchor references.

    fragment_map: optional dict mapping local-language heading anchors to English
    (ASCII) anchors. Used by non-English builds so all PDF fragment references
    target ASCII heading IDs (WeasyPrint requires ASCII named destinations).
    """
    def _to_ascii(fragment):
        """Translate local fragment to ASCII English anchor if mapping exists."""
        if fragment_map:
            return fragment_map.get(fragment, fragment)
        return fragment

    def resolve_link(m):
        text = m.group(1)
        url = m.group(2).replace('\\&', '&')
        if url.startswith('http://') or url.startswith('https://'):
            internal_m = re.match(rf'https://code\.claude\.com/docs/(?:{_LANG_ALTERNATION})/([^#)]+)(?:#(.+))?', url)
            if internal_m:
                slug = internal_m.group(1)
                fragment = internal_m.group(2)
                if fragment:
                    return f'[{text}](#{fragment})'
                elif slug in slug_to_anchor:
                    return f'[{text}](#{slug_to_anchor[slug]})'
            return f'[{text}]({url})'
        if os.path.exists(url):
            return f'[{text}]({url})'
        if url.startswith('#'):
            fragment = url[1:]
            return f'[{text}](#{_to_ascii(fragment)})'
        path = url.lstrip('/')
        for _lang in LANGUAGES:
            if path.startswith(f'{_lang}/'):
                path = path[len(_lang) + 1:]
                break
        if '#' in path:
            slug, fragment = path.split('#', 1)
            return f'[{text}](#{fragment})'
        else:
            slug = path
            if slug in slug_to_anchor:
                return f'[{text}](#{slug_to_anchor[slug]})'
        if url.startswith('/'):
            return f'[{text}]({base_url}{url})'
        return f'[{text}]({base_url}/{lang_path}/{url})'
    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', resolve_link, md)
    return md


# ---------------------------------------------------------------------------
# 5. dedent_blocks — fix indentation from MDX nesting
# ---------------------------------------------------------------------------

def dedent_blocks(md):
    """Dedent code blocks and MDX-nested content."""
    # Pass 1: Dedent code block contents
    lines = md.split('\n')
    new_lines = []
    code_lines = []
    fence_marker = None

    for line in lines:
        stripped = line.strip()
        if fence_marker is None:
            m = re.match(r'^(\s*)((`{3,})\w*.*)', line)
            if m:
                fence_marker = m.group(3)
                code_lines = [line]
            else:
                new_lines.append(line)
        else:
            code_lines.append(line)
            close_m = re.match(r'^\s*(`{3,})\s*$', stripped)
            if close_m and len(close_m.group(1)) >= len(fence_marker):
                if len(code_lines) > 2:
                    header = code_lines[0].strip()
                    footer = code_lines[-1].strip()
                    code = '\n'.join(code_lines[1:-1])
                    code = textwrap.dedent(code)
                    new_lines.append(header)
                    new_lines.extend(code.split('\n'))
                    new_lines.append(footer)
                else:
                    new_lines.extend(code_lines)
                fence_marker = None
                code_lines = []

    if code_lines:
        new_lines.extend(code_lines)
    md = '\n'.join(new_lines)

    # Pass 2: Dedent lines from MDX component nesting
    lines = md.split('\n')
    result_lines = []
    fence_marker2 = None
    for line in lines:
        stripped_line = line.strip()
        if fence_marker2 is None:
            fence_m = re.match(r'^(`{3,})', stripped_line)
            if fence_m:
                fence_marker2 = fence_m.group(1)
                result_lines.append(stripped_line)
                continue
        else:
            close_m = re.match(r'^(`{3,})\s*$', stripped_line)
            if close_m and len(close_m.group(1)) >= len(fence_marker2):
                fence_marker2 = None
                result_lines.append(stripped_line)
                continue
            result_lines.append(line.rstrip())
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent >= 4 and stripped:
            if re.match(r'[-*+]\s', stripped) or re.match(r'\d+[.)]\s', stripped):
                result_lines.append('  ' + stripped)
            else:
                result_lines.append(stripped)
        else:
            result_lines.append(line.rstrip())
    md = '\n'.join(result_lines)

    return md


# ---------------------------------------------------------------------------
# 6. finalize — collapse blank lines, strip
# ---------------------------------------------------------------------------

def finalize(md):
    """Collapse excessive blank lines and strip trailing whitespace."""
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def clean_md(md, *, images_dir, slug_to_anchor, base_url, lang_path,
             fragment_map=None):
    """Run the full transformation pipeline on a markdown document."""
    md = strip_metadata(md)
    md, code_store = protect_code_spans(md)
    md = convert_jsx_components(md, images_dir)
    md = clean_html_tags(md, images_dir)
    md = resolve_links(md, slug_to_anchor, base_url, lang_path, fragment_map)
    md = restore_code_spans(md, code_store)
    md = dedent_blocks(md)
    md = finalize(md)
    return md
