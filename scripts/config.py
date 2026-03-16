"""Shared constants and utilities for the cc-docs-pdf pipeline."""

import re

BASE_URL = "https://code.claude.com/docs"

# ── Language configuration ──────────────────────────────────────────────
# Every supported language lives here. Adding a new language = one dict entry.
# "dir" is the local filesystem directory name (lowercase).
# "cjk" controls whether CJK fonts are used for PDF generation.

LANGUAGES = {
    "de":    {"dir": "de",    "label": "Deutsch",            "cjk": False},
    "en":    {"dir": "en",    "label": "English",            "cjk": False},
    "es":    {"dir": "es",    "label": "Español",            "cjk": False},
    "fr":    {"dir": "fr",    "label": "Français",           "cjk": False},
    "id":    {"dir": "id",    "label": "Bahasa Indonesia",   "cjk": False},
    "it":    {"dir": "it",    "label": "Italiano",           "cjk": False},
    "ja":    {"dir": "ja",    "label": "日本語",              "cjk": True},
    "ko":    {"dir": "ko",    "label": "한국어",              "cjk": True},
    "pt":    {"dir": "pt",    "label": "Português",          "cjk": False},
    "ru":    {"dir": "ru",    "label": "Русский",            "cjk": False},
    "zh-CN": {"dir": "zh-cn", "label": "简体中文",            "cjk": True},
    "zh-TW": {"dir": "zh-tw", "label": "繁體中文",            "cjk": True},
}

LANG_CODES = list(LANGUAGES.keys())


def lang_to_dir(lang):
    """Map language code to local directory name (e.g. 'zh-TW' → 'zh-tw')."""
    return LANGUAGES[lang]["dir"]


# ── Slugs and sections ──────────────────────────────────────────────────
# Canonical page list. English has all 64; every other language is missing 5.

SLUGS = [
    "overview", "quickstart", "desktop-quickstart", "setup",
    "how-claude-code-works", "features-overview", "interactive-mode",
    "best-practices", "common-workflows", "commands", "cli-reference",
    "tools-reference", "keybindings", "permissions", "memory", "settings",
    "env-vars", "model-config", "output-styles", "fast-mode", "costs",
    "hooks", "hooks-guide", "mcp", "skills", "plugins", "plugins-reference",
    "plugin-marketplaces", "discover-plugins", "sub-agents", "agent-teams",
    "headless", "remote-control", "scheduled-tasks", "code-review",
    "github-actions", "gitlab-ci-cd", "vs-code", "jetbrains", "desktop",
    "chrome", "slack", "claude-code-on-the-web", "authentication",
    "security", "sandboxing", "checkpointing", "data-usage",
    "legal-and-compliance", "zero-data-retention", "analytics",
    "monitoring-usage", "amazon-bedrock", "google-vertex-ai",
    "microsoft-foundry", "llm-gateway", "network-config",
    "server-managed-settings", "devcontainer", "terminal-config",
    "statusline", "third-party-integrations", "troubleshooting", "changelog",
]

# These 5 slugs only exist in English (not in any translated language's sitemap)
EN_ONLY_SLUGS = {"commands", "tools-reference", "env-vars", "authentication", "changelog"}

SECTIONS = [
    ("Getting Started", [
        "overview", "quickstart", "desktop-quickstart", "setup", "how-claude-code-works",
    ]),
    ("Core Usage", [
        "features-overview", "interactive-mode", "best-practices", "common-workflows",
    ]),
    ("Commands & Reference", [
        "commands", "cli-reference", "tools-reference", "keybindings",
    ]),
    ("Configuration", [
        "permissions", "memory", "settings", "env-vars", "model-config",
        "output-styles", "fast-mode", "costs",
    ]),
    ("Extensibility", [
        "hooks", "hooks-guide", "mcp", "skills", "plugins", "plugins-reference",
        "plugin-marketplaces", "discover-plugins",
    ]),
    ("Advanced & Automation", [
        "sub-agents", "agent-teams", "headless", "remote-control",
        "scheduled-tasks", "code-review",
    ]),
    ("CI/CD & Integrations", [
        "github-actions", "gitlab-ci-cd",
    ]),
    ("IDE & Platform Integration", [
        "vs-code", "jetbrains", "desktop", "chrome", "slack", "claude-code-on-the-web",
    ]),
    ("Security & Privacy", [
        "authentication", "security", "sandboxing", "checkpointing",
        "data-usage", "legal-and-compliance", "zero-data-retention",
    ]),
    ("Enterprise & Monitoring", [
        "analytics", "monitoring-usage", "third-party-integrations", "server-managed-settings",
    ]),
    ("Cloud Providers", [
        "amazon-bedrock", "google-vertex-ai", "microsoft-foundry", "llm-gateway", "network-config",
    ]),
    ("Environment Setup", [
        "devcontainer", "terminal-config", "statusline",
    ]),
    ("Troubleshooting & Changelog", [
        "troubleshooting", "changelog",
    ]),
]


# ── Cover page text per language ────────────────────────────────────────

COVER_TEXT = {
    "de": {
        "subtitle": "Vollständige Dokumentation",
        "date_label": "Erstellungsdatum",
        "desc": "Ein agentisches Programmierwerkzeug in Ihrem Terminal,<br>\n    das Ihre Codebasis versteht und Ihnen hilft, schneller zu programmieren.",
        "note": "Kompiliert von code.claude.com/docs/de<br>\n    Für die neueste Version besuchen Sie die Website.",
    },
    "en": {
        "subtitle": "Complete Documentation",
        "date_label": "Production date",
        "desc": "An agentic coding tool that lives in your terminal,<br>\n    understands your codebase, and helps you code faster.",
        "note": "Compiled from code.claude.com/docs<br>\n    For the latest version, visit the website.",
    },
    "es": {
        "subtitle": "Documentación Completa",
        "date_label": "Fecha de producción",
        "desc": "Una herramienta de codificación agéntica en su terminal,<br>\n    que entiende su código y le ayuda a programar más rápido.",
        "note": "Compilado de code.claude.com/docs/es<br>\n    Para la versión más reciente, visite el sitio web.",
    },
    "fr": {
        "subtitle": "Documentation Complète",
        "date_label": "Date de production",
        "desc": "Un outil de codage agentique dans votre terminal,<br>\n    qui comprend votre code et vous aide à programmer plus vite.",
        "note": "Compilé depuis code.claude.com/docs/fr<br>\n    Pour la dernière version, visitez le site web.",
    },
    "id": {
        "subtitle": "Dokumentasi Lengkap",
        "date_label": "Tanggal produksi",
        "desc": "Alat pengkodean agentik di terminal Anda,<br>\n    memahami basis kode Anda, dan membantu Anda membuat kode lebih cepat.",
        "note": "Dikompilasi dari code.claude.com/docs/id<br>\n    Untuk versi terbaru, kunjungi situs web.",
    },
    "it": {
        "subtitle": "Documentazione Completa",
        "date_label": "Data di produzione",
        "desc": "Uno strumento di codifica agentico nel tuo terminale,<br>\n    che comprende il tuo codice e ti aiuta a programmare più velocemente.",
        "note": "Compilato da code.claude.com/docs/it<br>\n    Per l'ultima versione, visita il sito web.",
    },
    "ja": {
        "subtitle": "完全ドキュメント",
        "date_label": "作成日",
        "desc": "ターミナルで動作するエージェント型コーディングツール。<br>\n    コードベースを理解し、より速くコーディングできるよう支援します。",
        "note": "code.claude.com/docs/ja からコンパイル<br>\n    最新版はウェブサイトをご覧ください。",
    },
    "ko": {
        "subtitle": "전체 문서",
        "date_label": "제작일",
        "desc": "터미널에서 작동하는 에이전틱 코딩 도구로,<br>\n    코드베이스를 이해하고 더 빠르게 코딩할 수 있도록 도와줍니다.",
        "note": "code.claude.com/docs/ko 에서 컴파일<br>\n    최신 버전은 웹사이트를 방문하세요.",
    },
    "pt": {
        "subtitle": "Documentação Completa",
        "date_label": "Data de produção",
        "desc": "Uma ferramenta de codificação agêntica no seu terminal,<br>\n    que entende seu código e ajuda você a programar mais rápido.",
        "note": "Compilado de code.claude.com/docs/pt<br>\n    Para a versão mais recente, visite o site.",
    },
    "ru": {
        "subtitle": "Полная документация",
        "date_label": "Дата создания",
        "desc": "Агентный инструмент кодирования в вашем терминале,<br>\n    который понимает вашу кодовую базу и помогает программировать быстрее.",
        "note": "Скомпилировано с code.claude.com/docs/ru<br>\n    Для последней версии посетите сайт.",
    },
    "zh-CN": {
        "subtitle": "完整技术文档",
        "date_label": "制作日期",
        "desc": "一个在终端中运行的 AI 编码工具，<br>\n    理解您的代码库，帮助您更快地编写程序。",
        "note": "内容编译自 code.claude.com/docs/zh-CN<br>\n    如需最新版本，请访问网站。",
    },
    "zh-TW": {
        "subtitle": "完整技術文件",
        "date_label": "製作日期",
        "desc": "一個在終端機中運行的 AI 編碼工具，<br>\n    理解您的程式碼庫，幫助您更快地編寫程式。",
        "note": "內容編譯自 code.claude.com/docs/zh-TW<br>\n    如需最新版本，請造訪網站。",
    },
}

HTML_TITLES = {
    "de": "Claude Code Dokumentation",
    "en": "Claude Code Documentation",
    "es": "Documentación de Claude Code",
    "fr": "Documentation Claude Code",
    "id": "Dokumentasi Claude Code",
    "it": "Documentazione Claude Code",
    "ja": "Claude Code ドキュメント",
    "ko": "Claude Code 문서",
    "pt": "Documentação Claude Code",
    "ru": "Документация Claude Code",
    "zh-CN": "Claude Code 技术文档",
    "zh-TW": "Claude Code 技術文件",
}


# ── Utility functions ───────────────────────────────────────────────────

def heading_to_anchor(text):
    """Convert heading text to a URL-safe anchor ID.

    Uses the same algorithm as merge_docs.py (3-step):
    strip non-word chars (except spaces/hyphens) → spaces to hyphens → collapse hyphens.
    """
    anchor = re.sub(r'[^\w\s-]', '', text.lower())
    anchor = re.sub(r'[\s]+', '-', anchor.strip())
    return re.sub(r'-+', '-', anchor)


def slugs_for_lang(lang):
    """Return the slug list for the given language."""
    if lang != "en":
        return [s for s in SLUGS if s not in EN_ONLY_SLUGS]
    return list(SLUGS)


def sections_for_lang(lang):
    """Return SECTIONS filtered for the given language."""
    if lang != "en":
        result = []
        for title, slugs in SECTIONS:
            filtered = [s for s in slugs if s not in EN_ONLY_SLUGS]
            if filtered:
                result.append((title, filtered))
        return result
    return list(SECTIONS)
