> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugins-Referenz

> Vollständige technische Referenz für das Claude Code Plugin-System, einschließlich Schemas, CLI-Befehle und Komponentenspezifikationen.

<Tip>
  Möchten Sie Plugins installieren? Siehe [Plugins entdecken und installieren](/de/discover-plugins). Zum Erstellen von Plugins siehe [Plugins](/de/plugins). Zum Verteilen von Plugins siehe [Plugin-Marktplätze](/de/plugin-marketplaces).
</Tip>

Diese Referenz bietet vollständige technische Spezifikationen für das Claude Code Plugin-System, einschließlich Komponentenschemas, CLI-Befehle und Entwicklungstools.

Ein **Plugin** ist ein eigenständiges Verzeichnis von Komponenten, das Claude Code mit benutzerdefinierten Funktionen erweitert. Plugin-Komponenten umfassen Skills, Agents, Hooks, MCP-Server, LSP-Server und Monitore.

## Plugin-Komponenten-Referenz

### Skills

Plugins fügen Skills zu Claude Code hinzu und erstellen `/name` Verknüpfungen, die Sie oder Claude aufrufen können.

**Speicherort**: `skills/` oder `commands/` Verzeichnis im Plugin-Root, oder eine einzelne `SKILL.md` Datei im Plugin-Root

**Dateiformat**: Skills sind Verzeichnisse mit `SKILL.md`; Befehle sind einfache Markdown-Dateien

**Skill-Struktur**:

```text theme={null}
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

```markdown theme={null}
---
name: agent-name
description: Worauf sich dieser Agent spezialisiert und wann Claude ihn aufrufen sollte
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Detailliertes System-Prompt für den Agent, das seine Rolle, Expertise und sein Verhalten beschreibt.
```

Plugin-Agents unterstützen `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background` und `isolation` Frontmatter-Felder. Der einzige gültige `isolation` Wert ist `"worktree"`. Aus Sicherheitsgründen werden `hooks`, `mcpServers` und `permissionMode` für von Plugins bereitgestellte Agents nicht unterstützt.

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

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Plugin-Hooks reagieren auf die gleichen Lifecycle-Events wie [benutzerdefinierte Hooks](/de/hooks):

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

**Hook-Typen**:

* `command`: Shell-Befehle oder Skripte ausführen
* `http`: Das Event JSON als POST-Anfrage an eine URL senden
* `mcp_tool`: Ein Tool auf einem konfigurierten [MCP-Server](/de/mcp) aufrufen
* `prompt`: Ein Prompt mit einem LLM evaluieren (verwendet `$ARGUMENTS` Platzhalter für Kontext)
* `agent`: Einen agentic Verifier mit Tools für komplexe Verifikationsaufgaben ausführen

### MCP-Server

Plugins können Model Context Protocol (MCP) Server bündeln, um Claude Code mit externen Tools und Services zu verbinden.

**Speicherort**: `.mcp.json` im Plugin-Root oder inline in plugin.json

**Format**: Standard MCP-Server-Konfiguration

**MCP-Server-Konfiguration**:

```json theme={null}
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

```json theme={null}
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

```json theme={null}
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

| Plugin              | Language Server            | Installationsbefehl                                                                          |
| :------------------ | :------------------------- | :------------------------------------------------------------------------------------------- |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` oder `npm install -g pyright`                                          |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                       |
| `rust-analyzer-lsp` | rust-analyzer              | [Siehe rust-analyzer Installation](https://rust-analyzer.github.io/manual.html#installation) |

Installieren Sie zuerst den Language Server, dann installieren Sie das Plugin vom Marktplatz.

### Monitore

Plugins können Hintergrund-Monitore deklarieren, die Claude Code automatisch startet, wenn das Plugin aktiv ist. Jeder Monitor führt einen Shell-Befehl für die Lebensdauer der Session aus und liefert jede stdout-Zeile an Claude als Benachrichtigung, damit Claude auf Log-Einträge, Statusänderungen oder abgerufene Events reagieren kann, ohne aufgefordert zu werden, die Überwachung selbst zu starten.

Plugin-Monitore verwenden den gleichen Mechanismus wie das [Monitor-Tool](/de/tools-reference#monitor-tool) und teilen seine Verfügbarkeitsbeschränkungen. Sie laufen nur in interaktiven CLI-Sessions, laufen unsandboxed auf der gleichen Vertrauensebene wie [Hooks](#hooks) und werden auf Hosts übersprungen, wo das Monitor-Tool nicht verfügbar ist.

<Note>
  Plugin-Monitore erfordern Claude Code v2.1.105 oder später.
</Note>

**Speicherort**: `monitors/monitors.json` im Plugin-Root oder inline in `plugin.json`

**Format**: JSON-Array von Monitor-Einträgen

Die folgende `monitors/monitors.json` überwacht einen Deployment-Status-Endpunkt und ein lokales Error-Log:

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

Um Monitore inline zu deklarieren, setzen Sie `experimental.monitors` in `plugin.json` auf das gleiche Array. Um von einem nicht-Standard-Pfad zu laden, setzen Sie `experimental.monitors` auf einen relativen Pfad-String wie `"./config/monitors.json"`. Monitore sind eine [experimentelle Komponente](#experimental-components).

**Erforderliche Felder:**

| Feld          | Beschreibung                                                                                                                                     |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Bezeichner eindeutig innerhalb des Plugins. Verhindert doppelte Prozesse, wenn das Plugin neu geladen wird oder ein Skill erneut aufgerufen wird |
| `command`     | Shell-Befehl, der als persistenter Hintergrund-Prozess im Session-Arbeitsverzeichnis ausgeführt wird                                             |
| `description` | Kurze Zusammenfassung dessen, was überwacht wird. Wird im Task-Panel und in Benachrichtigungszusammenfassungen angezeigt                         |

**Optionale Felder:**

| Feld   | Beschreibung                                                                                                                                                                                                                                    |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `when` | Steuert, wann der Monitor startet. `"always"` startet ihn beim Session-Start und beim Plugin-Reload und ist der Standard. `"on-skill-invoke:<skill-name>"` startet ihn beim ersten Mal, wenn der benannte Skill in diesem Plugin versendet wird |

Der `command` Wert unterstützt die gleichen [Variablenersetzungen](#environment-variables) wie MCP- und LSP-Server-Konfigurationen: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.*}` und alle `${ENV_VAR}` aus der Umgebung. Stellen Sie dem Befehl `cd "${CLAUDE_PLUGIN_ROOT}" && ` voran, wenn das Skript aus dem Plugin-eigenen Verzeichnis ausgeführt werden muss.

Das Deaktivieren eines Plugins während einer Session stoppt nicht die Monitore, die bereits laufen. Sie stoppen, wenn die Session endet.

### Themes

Plugins können Farbthemes versenden, die in `/theme` neben den integrierten Voreinstellungen und den lokalen Themes des Benutzers angezeigt werden. Ein Theme ist eine JSON-Datei in `themes/` mit einer `base` Voreinstellung und einer sparsamen `overrides` Map von Farb-Tokens. Themes sind eine [experimentelle Komponente](#experimental-components).

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Das Auswählen eines Plugin-Themes speichert `custom:<plugin-name>:<slug>` in der Konfiguration des Benutzers. Plugin-Themes sind schreibgeschützt; das Drücken von `Ctrl+E` auf einem in `/theme` kopiert es in `~/.claude/themes/`, damit der Benutzer die Kopie bearbeiten kann.

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

```json theme={null}
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
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
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Erforderliche Felder

Wenn Sie ein Manifest einschließen, ist `name` das einzige erforderliche Feld.

| Feld   | Typ    | Beschreibung                                           | Beispiel             |
| :----- | :----- | :----------------------------------------------------- | :------------------- |
| `name` | string | Eindeutiger Bezeichner (kebab-case, keine Leerzeichen) | `"deployment-tools"` |

Dieser Name wird für die Namensgebung von Komponenten verwendet. Beispielsweise wird der Agent `agent-creator` für das Plugin mit dem Namen `plugin-dev` in der Benutzeroberfläche als `plugin-dev:agent-creator` angezeigt.

### Metadaten-Felder

| Feld          | Typ    | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                      | Beispiel                                                          |
| :------------ | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`     | string | JSON-Schema-URL für Editor-Autovervollständigung und Validierung. Claude Code ignoriert dieses Feld beim Laden.                                                                                                                                                                                                                                                                                                   | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `displayName` | string | {/* min-version: 2.1.143 */}Benutzerfreundlicher Name, der in der `/plugin` Auswahl und anderen UI-Oberflächen angezeigt wird. Fällt auf `name` zurück, wenn weggelassen. Im Gegensatz zu `name` kann es Leerzeichen und beliebige Groß-/Kleinschreibung enthalten. Wird nicht für Namensgebung oder Suche verwendet. Erfordert Claude Code v2.1.143 oder später.                                                 | `"Deployment Tools"`                                              |
| `version`     | string | Optional. Semantische Version. Das Setzen dieser Version fixiert das Plugin auf diese Versionsnummer, sodass Benutzer nur Updates erhalten, wenn Sie diese erhöhen. Wenn weggelassen, greift Claude Code auf den Git-Commit-SHA zurück, sodass jeder Commit als neue Version behandelt wird. Wenn auch im Marktplatz-Eintrag gesetzt, hat `plugin.json` Vorrang. Siehe [Versionsverwaltung](#version-management). | `"2.1.0"`                                                         |
| `description` | string | Kurze Erklärung des Plugin-Zwecks                                                                                                                                                                                                                                                                                                                                                                                 | `"Deployment automation tools"`                                   |
| `author`      | object | Autoreninformationen                                                                                                                                                                                                                                                                                                                                                                                              | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | Dokumentations-URL                                                                                                                                                                                                                                                                                                                                                                                                | `"https://docs.example.com"`                                      |
| `repository`  | string | Quellcode-URL                                                                                                                                                                                                                                                                                                                                                                                                     | `"https://github.com/user/plugin"`                                |
| `license`     | string | Lizenzbezeichner                                                                                                                                                                                                                                                                                                                                                                                                  | `"MIT"`, `"Apache-2.0"`                                           |
| `keywords`    | array  | Discovery-Tags                                                                                                                                                                                                                                                                                                                                                                                                    | `["deployment", "ci-cd"]`                                         |

### Komponentenpfad-Felder

| Feld                    | Typ                   | Beschreibung                                                                                                                                                        | Beispiel                                             |
| :---------------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------- |
| `skills`                | string\|array         | Benutzerdefinierte Skill-Verzeichnisse mit `<name>/SKILL.md` Struktur (zusätzlich zum Standard `skills/`)                                                           | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | Benutzerdefinierte flache `.md` Skill-Dateien oder Verzeichnisse (ersetzt Standard `commands/`)                                                                     | `"./custom/cmd.md"` oder `["./cmd1.md"]`             |
| `agents`                | string\|array         | Benutzerdefinierte Agent-Dateien (ersetzt Standard `agents/`)                                                                                                       | `"./custom/agents/reviewer.md"`                      |
| `hooks`                 | string\|array\|object | Hook-Konfigurationspfade oder Inline-Konfiguration                                                                                                                  | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | MCP-Konfigurationspfade oder Inline-Konfiguration                                                                                                                   | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | Benutzerdefinierte Output-Style-Dateien/Verzeichnisse (ersetzt Standard `output-styles/`)                                                                           | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) Konfigurationen für Code-Intelligenz (Gehe zu Definition, finde Referenzen, etc.) | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | Farbthema-Dateien/Verzeichnisse (ersetzt Standard `themes/`). Siehe [Designs](#themes)                                                                              | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | Hintergrund-[Monitor](/de/tools-reference#monitor-tool) Konfigurationen, die automatisch starten, wenn das Plugin aktiv ist. Siehe [Monitore](#monitors)            | `"./monitors.json"`                                  |
| `userConfig`            | object                | Benutzerkonfigurierbare Werte, die bei der Aktivierung abgefragt werden. Siehe [Benutzerkonfiguration](#user-configuration)                                         | Siehe unten                                          |
| `channels`              | array                 | Kanal-Deklarationen für Nachrichteninjection (Telegram, Slack, Discord Stil). Siehe [Kanäle](#channels)                                                             | Siehe unten                                          |
| `dependencies`          | array                 | Andere Plugins, die dieses Plugin benötigt, optional mit semver Versionsbeschränkungen. Siehe [Plugin-Abhängigkeitsversionen einschränken](/de/plugin-dependencies) | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Experimentelle Komponenten

Komponenten unter dem `experimental` Schlüssel, `themes` und `monitors`, haben ein Manifest-Schema, das sich zwischen Releases ändern kann, während sie stabilisieren. Wo Sie sie deklarieren, ist eine separate Migration: das Top-Level funktioniert immer noch, `claude plugin validate` warnt, und eine zukünftige Version wird `experimental.*` erfordern.

### Benutzerkonfiguration

Das `userConfig` Feld deklariert Werte, die Claude Code den Benutzer abfragt, wenn das Plugin aktiviert wird. Verwenden Sie dies, anstatt Benutzer zu zwingen, `settings.json` manuell zu bearbeiten.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

Schlüssel müssen gültige Bezeichner sein. Jede Option unterstützt diese Felder:

| Feld          | Erforderlich | Beschreibung                                                                                               |
| :------------ | :----------- | :--------------------------------------------------------------------------------------------------------- |
| `type`        | Ja           | Einer von `string`, `number`, `boolean`, `directory` oder `file`                                           |
| `title`       | Ja           | Beschriftung im Konfigurationsdialog                                                                       |
| `description` | Ja           | Hilfetext unter dem Feld                                                                                   |
| `sensitive`   | Nein         | Wenn `true`, maskiert die Eingabe und speichert den Wert im sicheren Speicher anstelle von `settings.json` |
| `required`    | Nein         | Wenn `true`, schlägt die Validierung fehl, wenn das Feld leer ist                                          |
| `default`     | Nein         | Wert, der verwendet wird, wenn der Benutzer nichts bereitstellt                                            |
| `multiple`    | Nein         | Für `string` Typ, erlaubt ein Array von Strings                                                            |
| `min` / `max` | Nein         | Grenzen für `number` Typ                                                                                   |

Jeder Wert ist für die Substitution als `${user_config.KEY}` in MCP- und LSP-Server-Konfigurationen, Hook-Befehlen und Monitor-Befehlen verfügbar. Nicht-sensitive Werte können auch in Skill- und Agent-Inhalten ersetzt werden. Alle Werte werden an Plugin-Subprozesse als `CLAUDE_PLUGIN_OPTION_<KEY>` Umgebungsvariablen exportiert.

Nicht-sensitive Werte werden in `settings.json` unter `pluginConfigs[<plugin-id>].options` gespeichert. Sensitive Werte gehen zum System-Keychain (oder `~/.claude/.credentials.json`, wo der Keychain nicht verfügbar ist). Keychain-Speicher wird mit OAuth-Tokens geteilt und hat ein ungefähres Gesamtlimit von 2 KB, daher halten Sie sensitive Werte klein.

### Kanäle

Das `channels` Feld ermöglicht es einem Plugin, einen oder mehrere Nachrichtenkanäle zu deklarieren, die Inhalte in die Konversation injizieren. Jeder Kanal bindet sich an einen MCP-Server, den das Plugin bereitstellt.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

Das `server` Feld ist erforderlich und muss einem Schlüssel in den `mcpServers` des Plugins entsprechen. Das optionale Pro-Kanal `userConfig` verwendet das gleiche Schema wie das Top-Level-Feld, wodurch das Plugin Bot-Tokens oder Owner-IDs abfragen kann, wenn das Plugin aktiviert wird.

### Pfad-Verhaltensregeln

Ob ein benutzerdefinierter Pfad das Standard-Verzeichnis des Plugins ersetzt oder erweitert, hängt vom Feld ab:

* **Ersetzt den Standard**: `commands`, `agents`, `outputStyles`, `experimental.themes`, `experimental.monitors`. Beispielsweise wird das Standard-Verzeichnis `commands/` nicht gescannt, wenn das Manifest `commands` angibt. Um den Standard zu behalten und mehr hinzuzufügen, listen Sie ihn explizit auf: `"commands": ["./commands/", "./extras/"]`
* **Fügt zum Standard hinzu**: `skills`. Das Standard-Verzeichnis `skills/` wird immer gescannt, und Verzeichnisse, die in `skills` aufgelistet sind, werden zusammen mit ihm geladen
* **Eigene Merge-Regeln**: [hooks](#hooks), [MCP-Server](#mcp-servers) und [LSP-Server](#lsp-servers). Siehe jeden Abschnitt für die Kombinationsweise mehrerer Quellen

Wenn ein Plugin sowohl einen Standard-Ordner als auch den entsprechenden Manifest-Schlüssel hat, kennzeichnet Claude Code v2.1.140 und später den ignorierten Ordner in `/doctor`, `claude plugin list` und der `/plugin` Detailansicht. Das Plugin wird weiterhin mit den Manifest-Pfaden geladen. Es wird keine Warnung angezeigt, wenn der Manifest-Schlüssel auf den Standard-Ordner verweist, beispielsweise `"commands": ["./commands/deploy.md"]`, da der Ordner in diesem Fall explizit adressiert wird.

Für alle Pfadfelder:

* Alle Pfade müssen relativ zum Plugin-Root sein und mit `./` beginnen
* Komponenten aus benutzerdefinierten Pfaden verwenden die gleichen Benennungs- und Namensgebungsregeln
* Mehrere Pfade können als Arrays angegeben werden
* Wenn ein Skill-Pfad auf ein Verzeichnis verweist, das direkt ein `SKILL.md` enthält, beispielsweise `"skills": ["./"]` verweist auf den Plugin-Root, bestimmt das Frontmatter-Feld `name` in `SKILL.md` den Aufrufen-Namen des Skills. Dies gibt einen stabilen Namen unabhängig vom Installationsverzeichnis. Wenn `name` nicht im Frontmatter gesetzt ist, wird der Verzeichnis-Basename als Fallback verwendet.

Ein Plugin, das ein `SKILL.md` in seinem Root hat, kein `skills/` Unterverzeichnis und kein `skills` Manifest-Feld hat, wird automatisch als Single-Skill-Plugin in Claude Code v2.1.142 und später geladen. Sie müssen `"skills": ["./"]` in `plugin.json` für dieses Layout nicht setzen. Der Aufrufen-Name des Skills folgt der gleichen Regel wie oben: das Frontmatter-Feld `name` oder der Verzeichnis-Basename als Fallback.

**Pfad-Beispiele**:

```json theme={null}
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

Claude Code bietet drei Variablen zum Referenzieren von Pfaden. Alle werden überall dort inline ersetzt, wo sie in Skill-Inhalten, Agent-Inhalten, Hook-Befehlen, Monitor-Befehlen und MCP- oder LSP-Server-Konfigurationen erscheinen. Alle werden auch als Umgebungsvariablen an Hook-Prozesse und MCP- oder LSP-Server-Subprozesse exportiert.

**`${CLAUDE_PLUGIN_ROOT}`**: Der absolute Pfad zum Installationsverzeichnis Ihres Plugins. Verwenden Sie dies, um auf Skripte, Binärdateien und Konfigurationsdateien zu verweisen, die mit dem Plugin gebündelt sind. In Hook-Befehlen verwenden Sie [Exec-Form](/de/hooks#exec-form-and-shell-form) mit `args`, damit der Pfad als ein Argument ohne Anführungszeichen übergeben wird. In Shell-Form-Hooks und Monitor-Befehlen wickeln Sie ihn in doppelte Anführungszeichen ein, wie in `"${CLAUDE_PLUGIN_ROOT}"`. Dieser Pfad ändert sich, wenn das Plugin aktualisiert wird. Das Verzeichnis der vorherigen Version bleibt etwa sieben Tage nach einem Update auf der Festplatte, bevor es bereinigt wird, aber behandeln Sie es als kurzlebig und schreiben Sie keinen Status hier.

Wenn ein Plugin während einer Sitzung aktualisiert wird, verwenden Hook-Befehle, Monitore, MCP-Server und LSP-Server weiterhin den Pfad der vorherigen Version. Führen Sie `/reload-plugins` aus, um Hooks, MCP-Server und LSP-Server auf den neuen Pfad umzuschalten; Monitore erfordern einen Neustart der Sitzung.

**`${CLAUDE_PLUGIN_DATA}`**: Ein persistentes Verzeichnis für Plugin-Status, das Updates überlebt. Verwenden Sie dies für installierte Abhängigkeiten wie `node_modules` oder Python-Umgebungen, generierte Code, Caches und alle anderen Dateien, die über Plugin-Versionen hinweg bestehen bleiben sollten. Das Verzeichnis wird automatisch erstellt, wenn diese Variable zum ersten Mal referenziert wird.

**`${CLAUDE_PROJECT_DIR}`**: Das Projekt-Root-Verzeichnis. Dies ist das gleiche Verzeichnis, das Hooks in ihrer `CLAUDE_PROJECT_DIR` Variable erhalten. Verwenden Sie dies, um auf projektlokale Skripte oder Konfigurationsdateien zu verweisen. Wickeln Sie es in Anführungszeichen ein, um Pfade mit Leerzeichen zu handhaben, beispielsweise `"${CLAUDE_PROJECT_DIR}/scripts/server.sh"`. MCP-Server können auch die MCP `roots/list` Anfrage aufrufen, die das Verzeichnis zurückgibt, aus dem Claude Code gestartet wurde.

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### Persistentes Datenverzeichnis

Das `${CLAUDE_PLUGIN_DATA}` Verzeichnis wird zu `~/.claude/plugins/data/{id}/` aufgelöst, wobei `{id}` der Plugin-Bezeichner mit Zeichen außerhalb von `a-z`, `A-Z`, `0-9`, `_` und `-` ist, die durch `-` ersetzt werden. Für ein Plugin, das als `formatter@my-marketplace` installiert ist, ist das Verzeichnis `~/.claude/plugins/data/formatter-my-marketplace/`.

Eine häufige Verwendung ist die einmalige Installation von Sprachabhängigkeiten und deren Wiederverwendung über Sessions und Plugin-Updates hinweg. Da das Datenverzeichnis länger lebt als jede einzelne Plugin-Version, kann eine Überprüfung auf Verzeichnisexistenz allein nicht erkennen, wenn ein Update das Abhängigkeitsmanifest des Plugins ändert. Das empfohlene Muster vergleicht das gebündelte Manifest mit einer Kopie im Datenverzeichnis und installiert neu, wenn sie sich unterscheiden.

Dieser `SessionStart` Hook installiert `node_modules` beim ersten Durchlauf und erneut, wenn ein Plugin-Update ein geändertes `package.json` enthält:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

Der `diff` beendet sich mit Nonzero, wenn die gespeicherte Kopie fehlt oder sich vom gebündelten unterscheidet, was sowohl den ersten Durchlauf als auch abhängigkeitsändernde Updates abdeckt. Wenn `npm install` fehlschlägt, entfernt das nachfolgende `rm` das kopierte Manifest, damit die nächste Session erneut versucht.

Skripte, die in `${CLAUDE_PLUGIN_ROOT}` gebündelt sind, können dann gegen die persistierten `node_modules` ausgeführt werden:

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

Das Datenverzeichnis wird automatisch gelöscht, wenn Sie das Plugin aus dem letzten Bereich deinstallieren, in dem es installiert ist. Die `/plugin` Schnittstelle zeigt die Verzeichnisgröße an und fragt vor dem Löschen. Die CLI löscht standardmäßig; übergeben Sie [`--keep-data`](#plugin-uninstall), um es zu bewahren.

***

## Plugin-Caching und Dateiauflösung

Plugins werden auf eine von zwei Arten angegeben:

* Durch `claude --plugin-dir` oder `claude --plugin-url`, für die Dauer einer Session.
* Durch einen Marktplatz, installiert für zukünftige Sessions.

Aus Sicherheits- und Verifizierungsgründen kopiert Claude Code *Marktplatz*-Plugins in den lokalen **Plugin-Cache** des Benutzers (`~/.claude/plugins/cache`), anstatt sie an Ort und Stelle zu verwenden. Das Verständnis dieses Verhaltens ist wichtig, wenn Sie Plugins entwickeln, die auf externe Dateien verweisen.

Jede installierte Version ist ein separates Verzeichnis im Cache. Wenn Sie ein Plugin aktualisieren oder deinstallieren, wird das vorherige Versionsverzeichnis als verwaist markiert und automatisch 7 Tage später entfernt. Die Gnadenfrist ermöglicht es gleichzeitigen Claude Code Sessions, die bereits die alte Version geladen haben, ohne Fehler weiter zu laufen.

Claudes Glob- und Grep-Tools überspringen verwaiste Versionsverzeichnisse während Suchen, daher enthalten Dateiergebnisse keinen veralteten Plugin-Code.

### Pfad-Traversal-Einschränkungen

Installierte Plugins können nicht auf Dateien außerhalb ihres Verzeichnisses verweisen. Pfade, die außerhalb des Plugin-Root traversieren (wie `../shared-utils`), funktionieren nach der Installation nicht, da diese externen Dateien nicht in den Cache kopiert werden.

### Dateien innerhalb eines Marktplatzes mit Symlinks freigeben

Wenn Ihr Plugin Dateien mit anderen Teilen desselben Marktplatzes freigeben muss, können Sie symbolische Links in Ihrem Plugin-Verzeichnis erstellen. Wie ein Symlink behandelt wird, wenn das Plugin in den Cache kopiert wird, hängt davon ab, wo sein Ziel aufgelöst wird:

* **Innerhalb des eigenen Verzeichnisses des Plugins:** Der Symlink wird als relativer Symlink im Cache beibehalten, sodass er zur Laufzeit weiterhin zum kopierten Ziel aufgelöst wird.
* **Anderswo innerhalb desselben Marktplatzes:** Der Symlink wird dereferenziert. Der Inhalt des Ziels wird stattdessen in den Cache kopiert. Dies ermöglicht es einem Meta-Plugin, sein `skills/`-Verzeichnis mit Skills zu verknüpfen, die von anderen Plugins im Marktplatz definiert werden.
* **Außerhalb des Marktplatzes:** Der Symlink wird aus Sicherheitsgründen übersprungen. Dies verhindert, dass Plugins beliebige Host-Dateien wie Systempfade in den Cache ziehen.

Für Plugins, die mit `--plugin-dir` installiert oder aus einem lokalen Pfad installiert werden, werden nur Symlinks beibehalten, die sich innerhalb des eigenen Verzeichnisses des Plugins auflösen. Alle anderen werden übersprungen.

Der folgende Befehl erstellt einen Link von innerhalb eines Marktplatz-Plugins zu einem gemeinsamen Skill, der von einem Geschwister-Plugin definiert wird. Verwenden Sie unter Windows `mklink /D` von einer erhöhten Eingabeaufforderung oder aktivieren Sie den Entwicklermodus:

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

Dies bietet Flexibilität bei Beibehaltung der Sicherheitsvorteile des Caching-Systems.

***

## Plugin-Verzeichnisstruktur

### Standard-Plugin-Layout

Ein vollständiges Plugin folgt dieser Struktur:

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Metadaten-Verzeichnis (optional)
│   └── plugin.json             # Plugin-Manifest
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills als flache .md Dateien
│   ├── status.md
│   └── logs.md
├── agents/                   # Subagent-Definitionen
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # Output-Style-Definitionen
│   └── terse.md
├── themes/                   # Farbschema-Definitionen
│   └── dracula.json
├── monitors/                 # Hintergrund-Monitor-Konfigurationen
│   └── monitors.json
├── hooks/                    # Hook-Konfigurationen
│   ├── hooks.json           # Haupt-Hook-Konfiguration
│   └── security-hooks.json  # Zusätzliche Hooks
├── bin/                      # Plugin-Ausführbare Dateien, die zu PATH hinzugefügt werden
│   └── my-tool               # Aufrufbar als bloßer Befehl im Bash-Tool
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
  Das `.claude-plugin/` Verzeichnis enthält die `plugin.json` Datei. Alle anderen Verzeichnisse (commands/, agents/, skills/, output-styles/, themes/, monitors/, hooks/) müssen sich im Plugin-Root befinden, nicht innerhalb von `.claude-plugin/`.
</Warning>

Eine `CLAUDE.md` Datei im Plugin-Root wird nicht als Projektkontext geladen. Plugins tragen Kontext durch Skills, Agents und Hooks bei, anstatt durch CLAUDE.md. Um Anweisungen bereitzustellen, die in Claudes Kontext geladen werden, fügen Sie diese in einen [Skill](#skills) ein.

### Datei-Speicherorte-Referenz

| Komponente              | Standard-Speicherort         | Zweck                                                                                                                                                                                                               |
| :---------------------- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Manifest**            | `.claude-plugin/plugin.json` | Plugin-Metadaten und Konfiguration (optional)                                                                                                                                                                       |
| **Skills**              | `skills/`                    | Skills mit `<name>/SKILL.md` Struktur                                                                                                                                                                               |
| **Befehle**             | `commands/`                  | Skills als flache Markdown-Dateien. Verwenden Sie `skills/` für neue Plugins                                                                                                                                        |
| **Agents**              | `agents/`                    | Subagent Markdown-Dateien                                                                                                                                                                                           |
| **Output-Styles**       | `output-styles/`             | Output-Style-Definitionen                                                                                                                                                                                           |
| **Themes**              | `themes/`                    | Farbschema-Definitionen                                                                                                                                                                                             |
| **Hooks**               | `hooks/hooks.json`           | Hook-Konfiguration                                                                                                                                                                                                  |
| **MCP-Server**          | `.mcp.json`                  | MCP-Server-Definitionen                                                                                                                                                                                             |
| **LSP-Server**          | `.lsp.json`                  | Language Server Konfigurationen                                                                                                                                                                                     |
| **Monitore**            | `monitors/monitors.json`     | Hintergrund-Monitor-Konfigurationen                                                                                                                                                                                 |
| **Ausführbare Dateien** | `bin/`                       | Ausführbare Dateien, die zum Bash-Tool `PATH` hinzugefügt werden. Dateien hier sind als bloße Befehle in jedem Bash-Tool-Aufruf aufrufbar, während das Plugin aktiviert ist                                         |
| **Einstellungen**       | `settings.json`              | Standardkonfiguration, die angewendet wird, wenn das Plugin aktiviert wird. Derzeit werden nur die [`agent`](/de/sub-agents) und [`subagentStatusLine`](/de/statusline#subagent-status-lines) Schlüssel unterstützt |

***

## CLI-Befehle-Referenz

Claude Code bietet CLI-Befehle für nicht-interaktive Plugin-Verwaltung, nützlich für Scripting und Automatisierung.

### plugin install

Installieren Sie ein Plugin aus verfügbaren Marktplätzen.

```bash theme={null}
claude plugin install <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name` für einen bestimmten Marktplatz

**Optionen:**

| Option                | Beschreibung                                         | Standard |
| :-------------------- | :--------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Installationsbereich: `user`, `project` oder `local` | `user`   |
| `-h, --help`          | Hilfe für Befehl anzeigen                            |          |

Der Bereich bestimmt, welche Einstellungsdatei das installierte Plugin hinzugefügt wird. Beispielsweise schreibt `--scope project` zu `enabledPlugins` in .claude/settings.json, wodurch das Plugin für alle verfügbar wird, die das Projekt-Repository klonen.

**Beispiele:**

```bash theme={null}
# Installieren Sie im Benutzerbereich (Standard)
claude plugin install formatter@my-marketplace

# Installieren Sie im Projektbereich (geteilt mit Team)
claude plugin install formatter@my-marketplace --scope project

# Installieren Sie im lokalen Bereich (gitignoriert)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Entfernen Sie ein installiertes Plugin.

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumente:**

* `<plugin>`: Plugin-Name oder `plugin-name@marketplace-name`

**Optionen:**

| Option                | Beschreibung                                                                                                                      | Standard |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Deinstallieren aus Bereich: `user`, `project` oder `local`                                                                        | `user`   |
| `--keep-data`         | Bewahren Sie das [persistente Datenverzeichnis](#persistent-data-directory) des Plugins                                           |          |
| `--prune`             | Entfernen Sie auch automatisch installierte Abhängigkeiten, die kein anderes Plugin benötigt. Siehe [plugin prune](#plugin-prune) |          |
| `-y, --yes`           | Überspringen Sie die `--prune` Bestätigungsaufforderung. Erforderlich, wenn stdin oder stdout kein TTY ist                        |          |
| `-h, --help`          | Hilfe für Befehl anzeigen                                                                                                         |          |

**Aliase:** `remove`, `rm`

Standardmäßig löscht das Deinstallieren aus dem letzten verbleibenden Bereich auch das `${CLAUDE_PLUGIN_DATA}` Verzeichnis des Plugins. Verwenden Sie `--keep-data`, um es zu bewahren, beispielsweise beim Neuinstallieren nach dem Testen einer neuen Version.

### plugin prune

Entfernen Sie automatisch installierte Plugin-Abhängigkeiten, die nicht mehr von einem installierten Plugin benötigt werden. Abhängigkeiten, die Claude Code eingezogen hat, um das [`dependencies`](/de/plugin-dependencies) Feld eines anderen Plugins zu erfüllen, werden entfernt; Plugins, die Sie direkt installiert haben, werden niemals berührt.

```bash theme={null}
claude plugin prune [options]
```

**Optionen:**

| Option                | Beschreibung                                                                                     | Standard |
| :-------------------- | :----------------------------------------------------------------------------------------------- | :------- |
| `-s, --scope <scope>` | Bereinigen im Bereich: `user`, `project` oder `local`                                            | `user`   |
| `--dry-run`           | Listet auf, was entfernt würde, ohne etwas zu entfernen                                          |          |
| `-y, --yes`           | Überspringen Sie die Bestätigungsaufforderung. Erforderlich, wenn stdin oder stdout kein TTY ist |          |
| `-h, --help`          | Hilfe für Befehl anzeigen                                                                        |          |

**Aliase:** `autoremove`

Der Befehl listet verwaiste Abhängigkeiten auf und fragt vor dem Entfernen um Bestätigung. Um ein Plugin zu entfernen und seine Abhängigkeiten in einem Schritt zu bereinigen, führen Sie `claude plugin uninstall <plugin> --prune` aus.

<Note>
  `claude plugin prune` erfordert Claude Code v2.1.121 oder später.
</Note>

### plugin enable

Aktivieren Sie ein deaktiviertes Plugin. Wenn das Plugin [Abhängigkeiten](/de/plugin-dependencies) deklariert, aktiviert Claude Code diese transitiv im gleichen Bereich, und der Befehl schlägt fehl, wenn eine Abhängigkeit nicht installiert ist.

```bash theme={null}
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

Deaktivieren Sie ein Plugin, ohne es zu deinstallieren. Schlägt fehl, wenn ein anderes aktiviertes Plugin [von](/de/plugin-dependencies#enable-or-disable-a-plugin-with-dependencies) dem Ziel abhängt. Die Fehlermeldung enthält einen verketteten Befehl, der zuerst alle abhängigen Plugins deaktiviert.

```bash theme={null}
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

```bash theme={null}
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

### plugin list

Listet installierte Plugins mit ihrer Version, Quell-Marktplatz und Aktivierungsstatus auf.

```bash theme={null}
claude plugin list [options]
```

**Optionen:**

| Option        | Beschreibung                                                         | Standard |
| :------------ | :------------------------------------------------------------------- | :------- |
| `--json`      | Ausgabe als JSON                                                     |          |
| `--available` | Verfügbare Plugins von Marktplätzen einschließen. Erfordert `--json` |          |
| `-h, --help`  | Hilfe für Befehl anzeigen                                            |          |

### plugin details

Zeigen Sie das Komponenten-Inventar eines Plugins und die geschätzten Token-Kosten an. Die Ausgabe listet alle Komponenten auf, die das Plugin bereitstellt, gruppiert als Skills, Agents, Hooks, MCP-Server und LSP-Server, zusammen mit einer Schätzung, wie viele Token es jeder Sitzung hinzufügt. Die Skills-Gruppe umfasst sowohl `skills/` als auch `commands/` Einträge.

```bash theme={null}
claude plugin details <name>
```

**Argumente:**

* `<name>`: Plugin-Name oder `plugin-name@marketplace-name`

**Optionen:**

| Option       | Beschreibung              | Standard |
| :----------- | :------------------------ | :------- |
| `-h, --help` | Hilfe für Befehl anzeigen |          |

Die Ausgabe zeigt zwei Kostenzahlen für jede Komponente:

* **Always-on:** Token, die jeder Sitzung durch den Auflistungstext des Plugins hinzugefügt werden, wie Skill-Beschreibungen, Agent-Beschreibungen und Befehlsnamen, unabhängig davon, ob eine Komponente ausgelöst wird.
* **On-invoke:** Token, die eine Komponente kostet, wenn sie ausgelöst wird. Wird pro Komponente angezeigt, nicht als Plugin-Gesamtsumme, da eine typische Sitzung nur eine Teilmenge von Komponenten aufruft.

Dieses Beispiel zeigt, wie die Ausgabe für ein Plugin mit zwei Skills aussieht:

```
security-guidance 1.2.0
  Real-time security analysis for Claude Code sessions
  Source: security-guidance@claude-code-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)
  LSP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

Die Always-on-Gesamtsumme wird über die `count_tokens` API für Ihr aktives Modell berechnet. Pro-Komponenten-Zahlen werden proportional von dieser Gesamtsumme skaliert. Wenn die API nicht erreichbar ist, greift der Befehl auf eine zeichenbasierte Schätzung zurück.

### plugin tag

Erstellen Sie ein Release-Git-Tag für das Plugin im aktuellen Verzeichnis. Führen Sie es im Ordner des Plugins aus. Siehe [Tag-Plugin-Releases](/de/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```bash theme={null}
claude plugin tag [options]
```

**Optionen:**

| Option        | Beschreibung                                                                                 | Standard |
| :------------ | :------------------------------------------------------------------------------------------- | :------- |
| `--push`      | Pushen Sie das Tag zum Remote nach dem Erstellen                                             |          |
| `--dry-run`   | Drucken Sie aus, was getaggt würde, ohne das Tag zu erstellen                                |          |
| `-f, --force` | Erstellen Sie das Tag auch wenn der Arbeitsbaum schmutzig ist oder das Tag bereits existiert |          |
| `-h, --help`  | Hilfe für Befehl anzeigen                                                                    |          |

***

## Debugging- und Entwicklungstools

### Debugging-Befehle

Verwenden Sie `claude --debug`, um Plugin-Lade-Details zu sehen:

Dies zeigt:

* Welche Plugins geladen werden
* Alle Fehler in Plugin-Manifesten
* Skill-, Agent- und Hook-Registrierung
* MCP-Server-Initialisierung

### Häufige Probleme

| Problem                             | Ursache                           | Lösung                                                                                                                                                                                |
| :---------------------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Plugin wird nicht geladen           | Ungültige `plugin.json`           | Führen Sie `claude plugin validate` oder `/plugin validate` aus, um `plugin.json`, Skill/Agent/Command Frontmatter und `hooks/hooks.json` auf Syntax- und Schema-Fehler zu überprüfen |
| Skills nicht erscheinend            | Falsche Verzeichnisstruktur       | Stellen Sie sicher, dass `skills/` oder `commands/` im Plugin-Root ist, nicht in `.claude-plugin/`                                                                                    |
| Hooks werden nicht ausgelöst        | Skript nicht ausführbar           | Führen Sie `chmod +x script.sh` aus                                                                                                                                                   |
| MCP-Server schlägt fehl             | Fehlender `${CLAUDE_PLUGIN_ROOT}` | Verwenden Sie Variable für alle Plugin-Pfade                                                                                                                                          |
| Pfadfehler                          | Absolute Pfade verwendet          | Alle Pfade müssen relativ sein und mit `./` beginnen                                                                                                                                  |
| LSP `Executable not found in $PATH` | Language Server nicht installiert | Installieren Sie die Binärdatei (z.B. `npm install -g typescript-language-server typescript`)                                                                                         |

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
3. Bestätigen Sie, dass der Hook-Typ gültig ist: `command`, `http`, `mcp_tool`, `prompt` oder `agent`

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

**Symptome**: Plugin wird geladen, aber Komponenten (Skills, Agents, Hooks) fehlen.

**Korrekte Struktur**: Komponenten müssen sich im Plugin-Root befinden, nicht innerhalb von `.claude-plugin/`. Nur `plugin.json` gehört in `.claude-plugin/`.

```text theme={null}
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

Claude Code verwendet die Version des Plugins als Cache-Schlüssel, der bestimmt, ob ein Update verfügbar ist. Wenn Sie `/plugin update` ausführen oder Auto-Update aktiviert ist, berechnet Claude Code die aktuelle Version und überspringt das Update, wenn es mit der bereits installierten Version übereinstimmt.

Die Version wird aus dem ersten dieser Felder aufgelöst, das gesetzt ist:

1. Das Feld `version` in der `plugin.json` des Plugins
2. Das Feld `version` im Marketplace-Eintrag des Plugins in `marketplace.json`
3. Der Git-Commit-SHA des Plugin-Quellcodes für `github`, `url`, `git-subdir` und relative-path-Quellen in einem Git-gehosteten Marketplace
4. `unknown`, für `npm`-Quellen oder lokale Verzeichnisse, die sich nicht in einem Git-Repository befinden

Dies gibt Ihnen zwei Möglichkeiten, ein Plugin zu versionieren:

| Ansatz                 | Wie                                                                              | Update-Verhalten                                                                                                                                                                          | Am besten für                                       |
| :--------------------- | :------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| **Explizite Version**  | Setzen Sie `"version": "2.1.0"` in `plugin.json`                                 | Benutzer erhalten Updates nur, wenn Sie dieses Feld erhöhen. Das Pushen neuer Commits ohne Erhöhung hat keine Auswirkung, und `/plugin update` meldet „bereits auf der neuesten Version". | Veröffentlichte Plugins mit stabilen Release-Zyklen |
| **Commit-SHA-Version** | Lassen Sie `version` sowohl in `plugin.json` als auch im Marketplace-Eintrag weg | Benutzer erhalten Updates bei jedem neuen Commit zur Git-Quelle des Plugins                                                                                                               | Interne oder Team-Plugins unter aktiver Entwicklung |

<Warning>
  Wenn Sie `version` in `plugin.json` setzen, müssen Sie es jedes Mal erhöhen, wenn Benutzer Änderungen erhalten sollen. Das bloße Pushen neuer Commits reicht nicht aus, da Claude Code die gleiche Versionszeichenkette sieht und die zwischengespeicherte Kopie behält. Wenn Sie schnell iterieren, lassen Sie `version` ungesetzt, damit stattdessen der Git-Commit-SHA verwendet wird.
</Warning>

Wenn Sie explizite Versionen verwenden, folgen Sie [semantischer Versionierung](https://semver.org) (`MAJOR.MINOR.PATCH`): Erhöhen Sie MAJOR für Breaking Changes, MINOR für neue Features, PATCH für Bugfixes. Dokumentieren Sie Änderungen in einer `CHANGELOG.md`.

***

## Siehe auch

* [Plugins](/de/plugins) - Tutorials und praktische Verwendung
* [Plugin-Marktplätze](/de/plugin-marketplaces) - Erstellen und Verwalten von Marktplätzen
* [Skills](/de/skills) - Skill-Entwicklungsdetails
* [Subagents](/de/sub-agents) - Agent-Konfiguration und Fähigkeiten
* [Hooks](/de/hooks) - Event-Handling und Automatisierung
* [MCP](/de/mcp) - Integration externer Tools
* [Einstellungen](/de/settings) - Konfigurationsoptionen für Plugins
