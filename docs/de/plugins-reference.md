> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugins-Referenz

> Vollständige technische Referenz für das Claude Code Plugin-System, einschließlich Schemas, CLI-Befehle und Komponentenspezifikationen.

<Tip>
  Möchten Sie Plugins installieren? Siehe [Plugins entdecken und installieren](/de/discover-plugins). Zum Erstellen von Plugins siehe [Plugins](/de/plugins). Zum Verteilen von Plugins siehe [Plugin-Marktplätze](/de/plugin-marketplaces).
</Tip>

Diese Referenz bietet vollständige technische Spezifikationen für das Claude Code Plugin-System, einschließlich Komponentenschemas, CLI-Befehle und Entwicklungstools.

Ein **Plugin** ist ein eigenständiges Verzeichnis von Komponenten, das Claude Code mit benutzerdefinierten Funktionen erweitert. Plugin-Komponenten umfassen Skills, Agents, Hooks, MCP-Server und LSP-Server.

## Plugin-Komponenten-Referenz

### Skills

Plugins fügen Skills zu Claude Code hinzu und erstellen `/name` Verknüpfungen, die Sie oder Claude aufrufen können.

**Speicherort**: `skills/` oder `commands/` Verzeichnis im Plugin-Root

**Dateiformat**: Skills sind Verzeichnisse mit `SKILL.md`; Befehle sind einfache Markdown-Dateien

**Skill-Struktur**:

```text  theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

**Integrationverhalten**:

* Skills und Befehle werden automatisch erkannt, wenn das Plugin installiert wird
* Claude kann sie automatisch basierend auf dem Task-Kontext aufrufen
* Skills können unterstützende Dateien neben SKILL.md enthalten

Vollständige Details finden Sie unter [Skills](/de/skills).

### Agents

Plugins können spezialisierte Subagents für spezifische Aufgaben bereitstellen, die Claude automatisch aufrufen kann, wenn dies angemessen ist.

**Speicherort**: `agents/` Verzeichnis im Plugin-Root

**Dateiformat**: Markdown-Dateien, die Agent-Fähigkeiten beschreiben

**Agent-Struktur**:

```markdown  theme={null}
---
name: agent-name
description: Worauf sich dieser Agent spezialisiert und wann Claude ihn aufrufen sollte
---

Detailliertes System-Prompt für den Agent, das seine Rolle, Expertise und sein Verhalten beschreibt.
```

**Integrationspunkte**:

* Agents erscheinen in der `/agents` Schnittstelle
* Claude kann Agents automatisch basierend auf dem Task-Kontext aufrufen
* Agents können manuell von Benutzern aufgerufen werden
* Plugin-Agents funktionieren neben integrierten Claude-Agents

Vollständige Details finden Sie unter [Subagents](/de/sub-agents).

### Hooks

Plugins können Event-Handler bereitstellen, die automatisch auf Claude Code Events reagieren.

**Speicherort**: `hooks/hooks.json` im Plugin-Root oder inline in plugin.json

**Format**: JSON-Konfiguration mit Event-Matchern und Aktionen

**Hook-Konfiguration**:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Verfügbare Events**:

* `PreToolUse`: Bevor Claude ein beliebiges Tool verwendet
* `PostToolUse`: Nachdem Claude ein beliebiges Tool erfolgreich verwendet hat
* `PostToolUseFailure`: Nachdem die Tool-Ausführung von Claude fehlgeschlagen ist
* `PermissionRequest`: Wenn ein Berechtigungsdialog angezeigt wird
* `UserPromptSubmit`: Wenn der Benutzer einen Prompt einreicht
* `Notification`: Wenn Claude Code Benachrichtigungen sendet
* `Stop`: Wenn Claude versucht zu stoppen
* `SubagentStart`: Wenn ein Subagent gestartet wird
* `SubagentStop`: Wenn ein Subagent versucht zu stoppen
* `SessionStart`: Am Anfang von Sessions
* `SessionEnd`: Am Ende von Sessions
* `TeammateIdle`: Wenn ein Agent-Team-Teamkollege im Begriff ist, untätig zu werden
* `TaskCompleted`: Wenn eine Aufgabe als abgeschlossen markiert wird
* `PreCompact`: Bevor die Konversationshistorie komprimiert wird

**Hook-Typen**:

* `command`: Shell-Befehle oder Skripte ausführen
* `prompt`: Ein Prompt mit einem LLM evaluieren (verwendet `$ARGUMENTS` Platzhalter für Kontext)
* `agent`: Einen agentic Verifier mit Tools für komplexe Verifikationsaufgaben ausführen

### MCP-Server

Plugins können Model Context Protocol (MCP) Server bündeln, um Claude Code mit externen Tools und Services zu verbinden.

**Speicherort**: `.mcp.json` im Plugin-Root oder inline in plugin.json

**Format**: Standard MCP-Server-Konfiguration

**MCP-Server-Konfiguration**:

```json  theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Integrationverhalten**:

* Plugin MCP-Server starten automatisch, wenn das Plugin aktiviert wird
* Server erscheinen als Standard MCP-Tools in Claudes Toolkit
* Server-Fähigkeiten integrieren sich nahtlos mit Claudes vorhandenen Tools
* Plugin-Server können unabhängig von Benutzer MCP-Servern konfiguriert werden

### LSP-Server

<Tip>
  Möchten Sie LSP-Plugins verwenden? Installieren Sie sie vom offiziellen Marktplatz: Suchen Sie nach „lsp" im `/plugin` Discover-Tab. Dieser Abschnitt dokumentiert, wie Sie LSP-Plugins für Sprachen erstellen, die nicht vom offiziellen Marktplatz abgedeckt werden.
</Tip>

Plugins können [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) Server bereitstellen, um Claude Echtzeit-Code-Intelligenz beim Arbeiten an Ihrer Codebasis zu geben.

LSP-Integration bietet:

* **Sofortige Diagnose**: Claude sieht Fehler und Warnungen sofort nach jeder Bearbeitung
* **Code-Navigation**: Gehe zu Definition, finde Referenzen und Hover-Informationen
* **Sprachbewusstsein**: Typinformationen und Dokumentation für Code-Symbole

**Speicherort**: `.lsp.json` im Plugin-Root oder inline in `plugin.json`

**Format**: JSON-Konfiguration, die Language Server Namen ihren Konfigurationen zuordnet

**`.lsp.json` Dateiformat**:

```json  theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Inline in `plugin.json`**:

```json  theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Erforderliche Felder:**

| Feld                  | Beschreibung                                         |
| :-------------------- | :--------------------------------------------------- |
| `command`             | Die auszuführende LSP-Binärdatei (muss in PATH sein) |
| `extensionToLanguage` | Ordnet Dateierweiterungen Sprachbezeichnern zu       |

**Optionale Felder:**

| Feld                    | Beschreibung                                                                |
| :---------------------- | :-------------------------------------------------------------------------- |
| `args`                  | Befehlszeilenargumente für den LSP-Server                                   |
| `transport`             | Kommunikationstransport: `stdio` (Standard) oder `socket`                   |
| `env`                   | Umgebungsvariablen, die beim Starten des Servers gesetzt werden             |
| `initializationOptions` | Optionen, die während der Initialisierung an den Server übergeben werden    |
| `settings`              | Einstellungen, die über `workspace/didChangeConfiguration` übergeben werden |
| `workspaceFolder`       | Workspace-Ordnerpfad für den Server                                         |
| `startupTimeout`        | Maximale Zeit zum Warten auf Server-Startup (Millisekunden)                 |
| `shutdownTimeout`       | Maximale Zeit zum Warten auf ordnungsgemäßes Herunterfahren (Millisekunden) |
| `restartOnCrash`        | Ob der Server automatisch neu gestartet werden soll, wenn er abstürzt       |
| `maxRestarts`           | Maximale Anzahl von Neustartversuchen, bevor aufgegeben wird                |

<Warning>
  **Sie müssen die Language Server Binärdatei separat installieren.** LSP-Plugins konfigurieren, wie Claude Code sich mit einem Language Server verbindet, aber sie enthalten den Server selbst nicht. Wenn Sie `Executable not found in $PATH` im `/plugin` Errors-Tab sehen, installieren Sie die erforderliche Binärdatei für Ihre Sprache.
</Warning>

**Verfügbare LSP-Plugins:**

| Plugin           | Language Server            | Installationsbefehl                                                                          |
| :--------------- | :------------------------- | :------------------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` oder `npm install -g pyright`                                          |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                       |
| `rust-lsp`       | rust-analyzer              | [Siehe rust-analyzer Installation](https://rust-analyzer.github.io/manual.html#installation) |

Installieren Sie zuerst den Language Server, dann installieren Sie das Plugin vom Marktplatz.

***

## Plugin-Installationsbereiche

Wenn Sie ein Plugin installieren, wählen Sie einen **Bereich**, der bestimmt, wo das Plugin verfügbar ist und wer es sonst noch verwenden kann:

| Bereich   | Einstellungsdatei                                       | Anwendungsfall                                                        |
| :-------- | :------------------------------------------------------ | :-------------------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                               | Persönliche Plugins, die in allen Projekten verfügbar sind (Standard) |
| `project` | `.claude/settings.json`                                 | Team-Plugins, die über Versionskontrolle geteilt werden               |
| `local`   | `.claude/settings.local.json`                           | Projektspezifische Plugins, gitignoriert                              |
| `managed` | [Verwaltete Einstellungen](/de/settings#settings-files) | Verwaltete Plugins (schreibgeschützt, nur aktualisierbar)             |

Plugins verwenden das gleiche Bereichssystem wie andere Claude Code Konfigurationen. Installationsanweisungen und Bereichs-Flags finden Sie unter [Plugins installieren](/de/discover-plugins#install-plugins). Eine vollständige Erklärung der Bereiche finden Sie unter [Konfigurationsbereiche](/de/settings#configuration-scopes).

***

## Plugin-Manifest-Schema

Die `.claude-plugin/plugin.json` Datei definiert die Metadaten und Konfiguration Ihres Plugins. Dieser Abschnitt dokumentiert alle unterstützten Felder und Optionen.

Das Manifest ist optional. Wenn es weggelassen wird, erkennt Claude Code Komponenten automatisch in [Standardspeicherorten](#file-locations-reference) und leitet den Plugin-Namen aus dem Verzeichnisnamen ab. Verwenden Sie ein Manifest, wenn Sie Metadaten oder benutzerdefinierte Komponentenpfade bereitstellen müssen.

### Vollständiges Schema

```json  theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Erforderliche Felder

Wenn Sie ein Manifest einschließen, ist `name` das einzige erforderliche Feld.

| Feld   | Typ    | Beschreibung                                           | Beispiel             |
| :----- | :----- | :----------------------------------------------------- | :------------------- |
| `name` | string | Eindeutiger Bezeichner (kebab-case, keine Leerzeichen) | `"deployment-tools"` |

Dieser Name wird für die Namensgebung von Komponenten verwendet. Beispielsweise wird der Agent `agent-creator` für das Plugin mit dem Namen `plugin-dev` in der Benutzeroberfläche als `plugin-dev:agent-creator` angezeigt.

### Metadaten-Felder

| Feld          | Typ    | Beschreibung                                                                                                                       | Beispiel                                           |
| :------------ | :----- | :--------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `version`     | string | Semantische Version. Wenn auch im Marktplatz-Eintrag gesetzt, hat `plugin.json` Vorrang. Sie müssen es nur an einer Stelle setzen. | `"2.1.0"`                                          |
| `description` | string | Kurze Erklärung des Plugin-Zwecks                                                                                                  | `"Deployment automation tools"`                    |
| `author`      | object | Autoreninformationen                                                                                                               | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | Dokumentations-URL                                                                                                                 | `"https://docs.example.com"`                       |
| `repository`  | string | Quellcode-URL                                                                                                                      | `"https://github.com/user/plugin"`                 |
| `license`     | string | Lizenzbezeichner                                                                                                                   | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Discovery-Tags                                                                                                                     | `["deployment", "ci-cd"]`                          |

### Komponentenpfad-Felder

| Feld           | Typ                   | Beschreibung                                                                                                                                                        | Beispiel                                 |
| :------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------- |
| `commands`     | string\|array         | Zusätzliche Befehlsdateien/Verzeichnisse                                                                                                                            | `"./custom/cmd.md"` oder `["./cmd1.md"]` |
| `agents`       | string\|array         | Zusätzliche Agent-Dateien                                                                                                                                           | `"./custom/agents/reviewer.md"`          |
| `skills`       | string\|array         | Zusätzliche Skill-Verzeichnisse                                                                                                                                     | `"./custom/skills/"`                     |
| `hooks`        | string\|array\|object | Hook-Konfigurationspfade oder Inline-Konfiguration                                                                                                                  | `"./my-extra-hooks.json"`                |
| `mcpServers`   | string\|array\|object | MCP-Konfigurationspfade oder Inline-Konfiguration                                                                                                                   | `"./my-extra-mcp-config.json"`           |
| `outputStyles` | string\|array         | Zusätzliche Output-Style-Dateien/Verzeichnisse                                                                                                                      | `"./styles/"`                            |
| `lspServers`   | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) Konfigurationen für Code-Intelligenz (Gehe zu Definition, finde Referenzen, etc.) | `"./.lsp.json"`                          |

### Pfad-Verhaltensregeln

**Wichtig**: Benutzerdefinierte Pfade ergänzen Standardverzeichnisse - sie ersetzen sie nicht.

* Wenn `commands/` existiert, wird es zusätzlich zu benutzerdefinierten Befehlspfaden geladen
* Alle Pfade müssen relativ zum Plugin-Root sein und mit `./` beginnen
* Befehle aus benutzerdefinierten Pfaden verwenden die gleichen Benennungs- und Namensgebungsregeln
* Mehrere Pfade können als Arrays für Flexibilität angegeben werden

**Pfad-Beispiele**:

```json  theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Umgebungsvariablen

**`${CLAUDE_PLUGIN_ROOT}`**: Enthält den absoluten Pfad zu Ihrem Plugin-Verzeichnis. Verwenden Sie dies in Hooks, MCP-Servern und Skripten, um korrekte Pfade unabhängig vom Installationsort sicherzustellen.

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

***

## Plugin-Caching und Dateiauflösung

Plugins werden auf eine von zwei Arten angegeben:

* Durch `claude --plugin-dir`, für die Dauer einer Session.
* Durch einen Marktplatz, installiert für zukünftige Sessions.

Aus Sicherheits- und Verifizierungsgründen kopiert Claude Code *Marktplatz*-Plugins in den lokalen **Plugin-Cache** des Benutzers (`~/.claude/plugins/cache`), anstatt sie an Ort und Stelle zu verwenden. Das Verständnis dieses Verhaltens ist wichtig, wenn Sie Plugins entwickeln, die auf externe Dateien verweisen.

### Pfad-Traversal-Einschränkungen

Installierte Plugins können nicht auf Dateien außerhalb ihres Verzeichnisses verweisen. Pfade, die außerhalb des Plugin-Root traversieren (wie `../shared-utils`), funktionieren nach der Installation nicht, da diese externen Dateien nicht in den Cache kopiert werden.

### Arbeiten mit externen Abhängigkeiten

Wenn Ihr Plugin auf Dateien außerhalb seines Verzeichnisses zugreifen muss, können Sie symbolische Links zu externen Dateien in Ihrem Plugin-Verzeichnis erstellen. Symlinks werden während des Kopiervorgangs berücksichtigt:

```bash  theme={null}
# Innerhalb Ihres Plugin-Verzeichnisses
ln -s /path/to/shared-utils ./shared-utils
```

Der verlinkte Inhalt wird in den Plugin-Cache kopiert. Dies bietet Flexibilität bei Beibehaltung der Sicherheitsvorteile des Caching-Systems.

***

## Plugin-Verzeichnisstruktur

### Standard-Plugin-Layout

Ein vollständiges Plugin folgt dieser Struktur:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # Metadaten-Verzeichnis (optional)
│   └── plugin.json             # Plugin-Manifest
├── commands/                 # Standard-Befehlsspeicherort
│   ├── status.md
│   └── logs.md
├── agents/                   # Standard-Agent-Speicherort
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook-Konfigurationen
│   ├── hooks.json           # Haupt-Hook-Konfiguration
│   └── security-hooks.json  # Zusätzliche Hooks
├── settings.json            # Standardeinstellungen für das Plugin
├── .mcp.json                # MCP-Server-Definitionen
├── .lsp.json                # LSP-Server-Konfigurationen
├── scripts/                 # Hook- und Utility-Skripte
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # Lizenzdatei
└── CHANGELOG.md             # Versionsverlauf
```

<Warning>
  Das `.claude-plugin/` Verzeichnis enthält die `plugin.json` Datei. Alle anderen Verzeichnisse (commands/, agents/, skills/, hooks/) müssen sich im Plugin-Root befinden, nicht innerhalb von `.claude-plugin/`.
</Warning>

### Datei-Speicherorte-Referenz

| Komponente        | Standard-Speicherort         | Zweck                                                                                                                                              |
| :---------------- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**      | `.claude-plugin/plugin.json` | Plugin-Metadaten und Konfiguration (optional)                                                                                                      |
| **Befehle**       | `commands/`                  | Skill Markdown-Dateien (veraltet; verwenden Sie `skills/` für neue Skills)                                                                         |
| **Agents**        | `agents/`                    | Subagent Markdown-Dateien                                                                                                                          |
| **Skills**        | `skills/`                    | Skills mit `<name>/SKILL.md` Struktur                                                                                                              |
| **Hooks**         | `hooks/hooks.json`           | Hook-Konfiguration                                                                                                                                 |
| **MCP-Server**    | `.mcp.json`                  | MCP-Server-Definitionen                                                                                                                            |
| **LSP-Server**    | `.lsp.json`                  | Language Server Konfigurationen                                                                                                                    |
| **Einstellungen** | `settings.json`              | Standardkonfiguration, die angewendet wird, wenn das Plugin aktiviert wird. Derzeit werden nur [`agent`](/de/sub-agents) Einstellungen unterstützt |

***

## CLI-Befehle-Referenz

Claude Code bietet CLI-Befehle für nicht-interaktive Plugin-Verwaltung, nützlich für Scripting und Automatisierung.

### plugin install

Installieren Sie ein Plugin aus verfügbaren Marktplätzen.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name` für einen bestimmten Marktplatz

**Optionen:**

| Option                | Beschreibung                                         | Standard |
| :-------------------- | :--------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Installationsbereich: `user`, `project` oder `local` | `user`   |
| `-h, --help`          | Hilfe für Befehl anzeigen                            |          |

Der Bereich bestimmt, welche Einstellungsdatei das installierte Plugin hinzugefügt wird. Beispielsweise schreibt --scope project zu `enabledPlugins` in .claude/settings.json, wodurch das Plugin für alle verfügbar wird, die das Projekt-Repository klonen.

**Beispiele:**

```bash  theme={null}
# Installieren Sie im Benutzerbereich (Standard)
claude plugin install formatter@my-marketplace

# Installieren Sie im Projektbereich (geteilt mit Team)
claude plugin install formatter@my-marketplace --scope project

# Installieren Sie im lokalen Bereich (gitignoriert)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Entfernen Sie ein installiertes Plugin.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name`

**Optionen:**

| Option                | Beschreibung                                               | Standard |
| :-------------------- | :--------------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Deinstallieren aus Bereich: `user`, `project` oder `local` | `user`   |
| `-h, --help`          | Hilfe für Befehl anzeigen                                  |          |

**Aliase:** `remove`, `rm`

### plugin enable

Aktivieren Sie ein deaktiviertes Plugin.

```bash  theme={null}
claude plugin enable <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name`

**Optionen:**

| Option                | Beschreibung                                           | Standard |
| :-------------------- | :----------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Bereich zum Aktivieren: `user`, `project` oder `local` | `user`   |
| `-h, --help`          | Hilfe für Befehl anzeigen                              |          |

### plugin disable

Deaktivieren Sie ein Plugin, ohne es zu deinstallieren.

```bash  theme={null}
claude plugin disable <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name`

**Optionen:**

| Option                | Beschreibung                                             | Standard |
| :-------------------- | :------------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Bereich zum Deaktivieren: `user`, `project` oder `local` | `user`   |
| `-h, --help`          | Hilfe für Befehl anzeigen                                |          |

### plugin update

Aktualisieren Sie ein Plugin auf die neueste Version.

```bash  theme={null}
claude plugin update <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name`

**Optionen:**

| Option                | Beschreibung                                                         | Standard |
| :-------------------- | :------------------------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Bereich zum Aktualisieren: `user`, `project`, `local` oder `managed` | `user`   |
| `-h, --help`          | Hilfe für Befehl anzeigen                                            |          |

***

## Debugging- und Entwicklungstools

### Debugging-Befehle

Verwenden Sie `claude --debug` (oder `/debug` innerhalb der TUI), um Plugin-Lade-Details zu sehen:

Dies zeigt:

* Welche Plugins geladen werden
* Alle Fehler in Plugin-Manifesten
* Befehls-, Agent- und Hook-Registrierung
* MCP-Server-Initialisierung

### Häufige Probleme

| Problem                             | Ursache                           | Lösung                                                                                        |
| :---------------------------------- | :-------------------------------- | :-------------------------------------------------------------------------------------------- |
| Plugin wird nicht geladen           | Ungültige `plugin.json`           | Validieren Sie JSON-Syntax mit `claude plugin validate` oder `/plugin validate`               |
| Befehle erscheinen nicht            | Falsche Verzeichnisstruktur       | Stellen Sie sicher, dass `commands/` im Root ist, nicht in `.claude-plugin/`                  |
| Hooks werden nicht ausgelöst        | Skript nicht ausführbar           | Führen Sie `chmod +x script.sh` aus                                                           |
| MCP-Server schlägt fehl             | Fehlender `${CLAUDE_PLUGIN_ROOT}` | Verwenden Sie Variable für alle Plugin-Pfade                                                  |
| Pfadfehler                          | Absolute Pfade verwendet          | Alle Pfade müssen relativ sein und mit `./` beginnen                                          |
| LSP `Executable not found in $PATH` | Language Server nicht installiert | Installieren Sie die Binärdatei (z.B. `npm install -g typescript-language-server typescript`) |

### Beispiel-Fehlermeldungen

**Manifest-Validierungsfehler**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: Überprüfen Sie auf fehlende Kommas, zusätzliche Kommas oder nicht zitierte Strings
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: Ein erforderliches Feld fehlt
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON-Syntaxfehler

**Plugin-Ladefehler**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: Befehlspfad existiert, enthält aber keine gültigen Befehlsdateien
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: Der `source` Pfad in marketplace.json verweist auf ein nicht existierendes Verzeichnis
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: Entfernen Sie doppelte Komponentendefinitionen oder entfernen Sie `strict: false` im Marktplatz-Eintrag

### Hook-Fehlerbehebung

**Hook-Skript wird nicht ausgeführt**:

1. Überprüfen Sie, dass das Skript ausführbar ist: `chmod +x ./scripts/your-script.sh`
2. Überprüfen Sie die Shebang-Zeile: Erste Zeile sollte `#!/bin/bash` oder `#!/usr/bin/env bash` sein
3. Überprüfen Sie, dass der Pfad `${CLAUDE_PLUGIN_ROOT}` verwendet: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Testen Sie das Skript manuell: `./scripts/your-script.sh`

**Hook wird nicht bei erwarteten Events ausgelöst**:

1. Überprüfen Sie, dass der Event-Name korrekt ist (Groß-/Kleinschreibung beachten): `PostToolUse`, nicht `postToolUse`
2. Überprüfen Sie, dass das Matcher-Muster Ihre Tools passt: `"matcher": "Write|Edit"` für Dateivorgänge
3. Bestätigen Sie, dass der Hook-Typ gültig ist: `command`, `prompt` oder `agent`

### MCP-Server-Fehlerbehebung

**Server wird nicht gestartet**:

1. Überprüfen Sie, dass der Befehl existiert und ausführbar ist
2. Überprüfen Sie, dass alle Pfade die `${CLAUDE_PLUGIN_ROOT}` Variable verwenden
3. Überprüfen Sie die MCP-Server-Logs: `claude --debug` zeigt Initialisierungsfehler
4. Testen Sie den Server manuell außerhalb von Claude Code

**Server-Tools erscheinen nicht**:

1. Stellen Sie sicher, dass der Server ordnungsgemäß in `.mcp.json` oder `plugin.json` konfiguriert ist
2. Überprüfen Sie, dass der Server das MCP-Protokoll ordnungsgemäß implementiert
3. Überprüfen Sie auf Verbindungs-Timeouts in der Debug-Ausgabe

### Verzeichnisstruktur-Fehler

**Symptome**: Plugin wird geladen, aber Komponenten (Befehle, Agents, Hooks) fehlen.

**Korrekte Struktur**: Komponenten müssen sich im Plugin-Root befinden, nicht innerhalb von `.claude-plugin/`. Nur `plugin.json` gehört in `.claude-plugin/`.

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Nur Manifest hier
├── commands/            ← Auf Root-Ebene
├── agents/              ← Auf Root-Ebene
└── hooks/               ← Auf Root-Ebene
```

Wenn sich Ihre Komponenten in `.claude-plugin/` befinden, verschieben Sie sie in den Plugin-Root.

**Debug-Checkliste**:

1. Führen Sie `claude --debug` aus und suchen Sie nach „loading plugin" Meldungen
2. Überprüfen Sie, dass jedes Komponentenverzeichnis in der Debug-Ausgabe aufgelistet ist
3. Überprüfen Sie Dateiberechtigungen, die das Lesen der Plugin-Dateien ermöglichen

***

## Verteilungs- und Versionierungs-Referenz

### Versionsverwaltung

Folgen Sie semantischer Versionierung für Plugin-Releases:

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Versionsformat**: `MAJOR.MINOR.PATCH`

* **MAJOR**: Breaking Changes (inkompatible API-Änderungen)
* **MINOR**: Neue Features (abwärtskompatible Ergänzungen)
* **PATCH**: Bugfixes (abwärtskompatible Fixes)

**Best Practices**:

* Beginnen Sie mit `1.0.0` für Ihr erstes stabiles Release
* Aktualisieren Sie die Version in `plugin.json`, bevor Sie Änderungen verteilen
* Dokumentieren Sie Änderungen in einer `CHANGELOG.md` Datei
* Verwenden Sie Pre-Release-Versionen wie `2.0.0-beta.1` zum Testen

<Warning>
  Claude Code verwendet die Version, um zu bestimmen, ob Ihr Plugin aktualisiert werden soll. Wenn Sie den Code Ihres Plugins ändern, aber die Version in `plugin.json` nicht erhöhen, werden Ihre bestehenden Plugin-Benutzer Ihre Änderungen aufgrund von Caching nicht sehen.

  Wenn sich Ihr Plugin in einem [Marktplatz](/de/plugin-marketplaces) Verzeichnis befindet, können Sie die Version stattdessen über `marketplace.json` verwalten und das `version` Feld aus `plugin.json` weglassen.
</Warning>

***

## Siehe auch

* [Plugins](/de/plugins) - Tutorials und praktische Verwendung
* [Plugin-Marktplätze](/de/plugin-marketplaces) - Erstellen und Verwalten von Marktplätzen
* [Skills](/de/skills) - Skill-Entwicklungsdetails
* [Subagents](/de/sub-agents) - Agent-Konfiguration und Fähigkeiten
* [Hooks](/de/hooks) - Event-Handling und Automatisierung
* [MCP](/de/mcp) - Integration externer Tools
* [Einstellungen](/de/settings) - Konfigurationsoptionen für Plugins
