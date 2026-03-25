> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hooks-Referenz

> Referenz für Claude Code Hook-Ereignisse, Konfigurationsschema, JSON-Ein-/Ausgabeformate, Exit-Codes, asynchrone Hooks, HTTP-Hooks, Prompt-Hooks und MCP-Tool-Hooks.

<Tip>
  Eine Schnellstartanleitung mit Beispielen finden Sie unter [Workflows mit Hooks automatisieren](/de/hooks-guide).
</Tip>

Hooks sind benutzerdefinierte Shell-Befehle, HTTP-Endpunkte oder LLM-Prompts, die automatisch an bestimmten Punkten im Lebenszyklus von Claude Code ausgeführt werden. Verwenden Sie diese Referenz, um Ereignisschemas, Konfigurationsoptionen, JSON-Ein-/Ausgabeformate und erweiterte Funktionen wie asynchrone Hooks, HTTP-Hooks und MCP-Tool-Hooks nachzuschlagen. Wenn Sie Hooks zum ersten Mal einrichten, beginnen Sie stattdessen mit der [Anleitung](/de/hooks-guide).

## Hook-Lebenszyklus

Hooks werden an bestimmten Punkten während einer Claude Code-Sitzung ausgelöst. Wenn ein Ereignis ausgelöst wird und ein Matcher passt, übergibt Claude Code JSON-Kontext über das Ereignis an Ihren Hook-Handler. Für Command-Hooks kommt die Eingabe über stdin an. Für HTTP-Hooks kommt sie als POST-Request-Body an. Ihr Handler kann dann die Eingabe überprüfen, Maßnahmen ergreifen und optional eine Entscheidung zurückgeben. Einige Ereignisse werden einmal pro Sitzung ausgelöst, während andere wiederholt in der agentengesteuerten Schleife ausgelöst werden:

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/2YzYcIR7V1VggfgF/images/hooks-lifecycle.svg?fit=max&auto=format&n=2YzYcIR7V1VggfgF&q=85&s=3004e6c5dc95c4fe7fa3eb40fdc4176c" alt="Hook-Lebenszyklus-Diagramm, das die Abfolge von Hooks von SessionStart durch die agentengesteuerte Schleife (PreToolUse, PermissionRequest, PostToolUse, SubagentStart/Stop, TaskCompleted) bis Stop oder StopFailure, TeammateIdle, PreCompact, PostCompact und SessionEnd zeigt, mit Elicitation und ElicitationResult verschachtelt in MCP-Tool-Ausführung und WorktreeCreate, WorktreeRemove, Notification, ConfigChange und InstructionsLoaded als eigenständige asynchrone Ereignisse" width="520" height="1100" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

Die folgende Tabelle fasst zusammen, wann jedes Ereignis ausgelöst wird. Der Abschnitt [Hook-Ereignisse](#hook-events) dokumentiert das vollständige Eingabeschema und die Optionen zur Entscheidungskontrolle für jedes Ereignis.

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

### Wie ein Hook aufgelöst wird

Um zu sehen, wie diese Teile zusammenpassen, betrachten Sie diesen `PreToolUse`-Hook, der destruktive Shell-Befehle blockiert. Der Hook führt `block-rm.sh` vor jedem Bash-Tool-Aufruf aus:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

Das Skript liest die JSON-Eingabe von stdin, extrahiert den Befehl und gibt eine `permissionDecision` von `"deny"` zurück, wenn es `rm -rf` enthält:

```bash  theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

Angenommen, Claude Code entscheidet sich, `Bash "rm -rf /tmp/build"` auszuführen. Hier ist, was passiert:

<Frame>
  <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/hook-resolution.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=ad667ee6d86ab2276aa48a4e73e220df" alt="Hook-Auflösungsfluss: PreToolUse-Ereignis wird ausgelöst, Matcher prüft auf Bash-Übereinstimmung, Hook-Handler wird ausgeführt, Ergebnis wird an Claude Code zurückgegeben" width="780" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Ereignis wird ausgelöst">
    Das `PreToolUse`-Ereignis wird ausgelöst. Claude Code sendet die Tool-Eingabe als JSON über stdin an den Hook:

    ```json  theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="Matcher prüft">
    Der Matcher `"Bash"` passt zum Tool-Namen, daher wird `block-rm.sh` ausgeführt. Wenn Sie den Matcher weglassen oder `"*"` verwenden, wird der Hook bei jedem Auftreten des Ereignisses ausgeführt. Hooks werden nur übersprungen, wenn ein Matcher definiert ist und nicht passt.
  </Step>

  <Step title="Hook-Handler wird ausgeführt">
    Das Skript extrahiert `"rm -rf /tmp/build"` aus der Eingabe und findet `rm -rf`, daher gibt es eine Entscheidung auf stdout aus:

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Wenn der Befehl sicher gewesen wäre (wie `npm test`), würde das Skript stattdessen `exit 0` treffen, was Claude Code mitteilt, den Tool-Aufruf zuzulassen, ohne weitere Maßnahmen zu ergreifen.
  </Step>

  <Step title="Claude Code handelt nach dem Ergebnis">
    Claude Code liest die JSON-Entscheidung, blockiert den Tool-Aufruf und zeigt Claude den Grund an.
  </Step>
</Steps>

Der Abschnitt [Konfiguration](#configuration) unten dokumentiert das vollständige Schema, und jeder Abschnitt [Hook-Ereignis](#hook-events) dokumentiert, welche Eingabe Ihr Befehl erhält und welche Ausgabe er zurückgeben kann.

## Konfiguration

Hooks werden in JSON-Einstellungsdateien definiert. Die Konfiguration hat drei Verschachtelungsebenen:

1. Wählen Sie ein [Hook-Ereignis](#hook-events) aus, auf das Sie reagieren möchten, wie `PreToolUse` oder `Stop`
2. Fügen Sie eine [Matcher-Gruppe](#matcher-patterns) hinzu, um zu filtern, wann es ausgelöst wird, wie 'nur für das Bash-Tool"
3. Definieren Sie einen oder mehrere [Hook-Handler](#hook-handler-fields), die ausgeführt werden, wenn sie passen

Siehe [Wie ein Hook aufgelöst wird](#how-a-hook-resolves) oben für eine vollständige Anleitung mit einem kommentierten Beispiel.

<Note>
  Diese Seite verwendet spezifische Begriffe für jede Ebene: **Hook-Ereignis** für den Lebenszyklus-Punkt, **Matcher-Gruppe** für den Filter und **Hook-Handler** für den Shell-Befehl, HTTP-Endpunkt, Prompt oder Agent, der ausgeführt wird. „Hook" allein bezieht sich auf die allgemeine Funktion.
</Note>

### Hook-Speicherorte

Der Ort, an dem Sie einen Hook definieren, bestimmt seinen Umfang:

| Speicherort                                                  | Umfang                           | Freigegeben                           |
| :----------------------------------------------------------- | :------------------------------- | :------------------------------------ |
| `~/.claude/settings.json`                                    | Alle Ihre Projekte               | Nein, lokal auf Ihrem Computer        |
| `.claude/settings.json`                                      | Einzelnes Projekt                | Ja, kann im Repo committed werden     |
| `.claude/settings.local.json`                                | Einzelnes Projekt                | Nein, gitignored                      |
| Verwaltete Richtlinieneinstellungen                          | Organisationsweit                | Ja, von Admin kontrolliert            |
| [Plugin](/de/plugins) `hooks/hooks.json`                     | Wenn Plugin aktiviert ist        | Ja, mit dem Plugin gebündelt          |
| [Skill](/de/skills) oder [Agent](/de/sub-agents) Frontmatter | Während die Komponente aktiv ist | Ja, in der Komponentendatei definiert |

Weitere Informationen zur Auflösung von Einstellungsdateien finden Sie unter [Einstellungen](/de/settings). Enterprise-Administratoren können `allowManagedHooksOnly` verwenden, um Benutzer-, Projekt- und Plugin-Hooks zu blockieren. Siehe [Hook-Konfiguration](/de/settings#hook-configuration).

### Matcher-Muster

Das Feld `matcher` ist eine Regex-Zeichenkette, die filtert, wann Hooks ausgelöst werden. Verwenden Sie `"*"`, `""` oder lassen Sie `matcher` ganz weg, um alle Vorkommen zu treffen. Jeder Ereignistyp passt auf ein anderes Feld:

| Ereignis                                                                                        | Worauf der Matcher filtert          | Beispiel-Matcher-Werte                                                                                                    |
| :---------------------------------------------------------------------------------------------- | :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | Tool-Name                           | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                          |
| `SessionStart`                                                                                  | Wie die Sitzung gestartet wurde     | `startup`, `resume`, `clear`, `compact`                                                                                   |
| `SessionEnd`                                                                                    | Warum die Sitzung endete            | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                  |
| `Notification`                                                                                  | Benachrichtigungstyp                | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`                                                  |
| `SubagentStart`                                                                                 | Agent-Typ                           | `Bash`, `Explore`, `Plan` oder benutzerdefinierte Agent-Namen                                                             |
| `PreCompact`, `PostCompact`                                                                     | Was die Komprimierung ausgelöst hat | `manual`, `auto`                                                                                                          |
| `SubagentStop`                                                                                  | Agent-Typ                           | gleiche Werte wie `SubagentStart`                                                                                         |
| `ConfigChange`                                                                                  | Konfigurationsquelle                | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                        |
| `StopFailure`                                                                                   | Fehlertyp                           | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                            | Ladegrund                           | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                              |
| `Elicitation`                                                                                   | MCP-Server-Name                     | Ihre konfigurierten MCP-Server-Namen                                                                                      |
| `ElicitationResult`                                                                             | MCP-Server-Name                     | gleiche Werte wie `Elicitation`                                                                                           |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | Keine Matcher-Unterstützung         | wird immer bei jedem Auftreten ausgelöst                                                                                  |

Der Matcher ist ein Regex, daher passt `Edit|Write` zu beiden Tools und `Notebook.*` passt zu jedem Tool, das mit Notebook beginnt. Der Matcher wird gegen ein Feld aus der [JSON-Eingabe](#hook-input-and-output) ausgeführt, die Claude Code an Ihren Hook über stdin sendet. Für Tool-Ereignisse ist dieses Feld `tool_name`. Jeder Abschnitt [Hook-Ereignis](#hook-events) listet den vollständigen Satz von Matcher-Werten und das Eingabeschema für dieses Ereignis auf.

Dieses Beispiel führt ein Linting-Skript nur aus, wenn Claude eine Datei schreibt oder bearbeitet:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate` und `WorktreeRemove` unterstützen keine Matcher und werden immer bei jedem Auftreten ausgelöst. Wenn Sie ein `matcher`-Feld zu diesen Ereignissen hinzufügen, wird es stillschweigend ignoriert.

#### MCP-Tools abgleichen

[MCP](/de/mcp) Server-Tools erscheinen als reguläre Tools in Tool-Ereignissen (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`), daher können Sie sie auf die gleiche Weise abgleichen wie jeden anderen Tool-Namen.

MCP-Tools folgen dem Benennungsmuster `mcp__<server>__<tool>`, zum Beispiel:

* `mcp__memory__create_entities`: Memory-Server-Tool zum Erstellen von Entitäten
* `mcp__filesystem__read_file`: Filesystem-Server-Tool zum Lesen von Dateien
* `mcp__github__search_repositories`: GitHub-Server-Suchtool

Verwenden Sie Regex-Muster, um bestimmte MCP-Tools oder Gruppen von Tools anzusteuern:

* `mcp__memory__.*` passt zu allen Tools vom `memory`-Server
* `mcp__.*__write.*` passt zu jedem Tool, das „write" enthält, von jedem Server

Dieses Beispiel protokolliert alle Memory-Server-Operationen und validiert Schreibvorgänge von jedem MCP-Server:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Hook-Handler-Felder

Jedes Objekt im inneren `hooks`-Array ist ein Hook-Handler: der Shell-Befehl, HTTP-Endpunkt, LLM-Prompt oder Agent, der ausgeführt wird, wenn der Matcher passt. Es gibt vier Typen:

* **[Command-Hooks](#command-hook-fields)** (`type: "command"`): führen einen Shell-Befehl aus. Ihr Skript erhält die [JSON-Eingabe](#hook-input-and-output) des Ereignisses über stdin und kommuniziert Ergebnisse über Exit-Codes und stdout zurück.
* **[HTTP-Hooks](#http-hook-fields)** (`type: "http"`): senden die [JSON-Eingabe](#hook-input-and-output) des Ereignisses als HTTP-POST-Request an eine URL. Der Endpunkt kommuniziert Ergebnisse über den Response-Body mit dem gleichen [JSON-Ausgabeformat](#json-output) wie Command-Hooks zurück.
* **[Prompt-Hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): senden einen Prompt an ein Claude-Modell für eine Single-Turn-Evaluierung. Das Modell gibt eine Ja/Nein-Entscheidung als JSON zurück. Siehe [Prompt-basierte Hooks](#prompt-based-hooks).
* **[Agent-Hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): spawnen einen Subagenten, der Tools wie Read, Grep und Glob verwenden kann, um Bedingungen zu überprüfen, bevor eine Entscheidung zurückgegeben wird. Siehe [Agent-basierte Hooks](#agent-based-hooks).

#### Gemeinsame Felder

Diese Felder gelten für alle Hook-Typen:

| Feld            | Erforderlich | Beschreibung                                                                                                                                                     |
| :-------------- | :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | ja           | `"command"`, `"http"`, `"prompt"` oder `"agent"`                                                                                                                 |
| `timeout`       | nein         | Sekunden vor dem Abbruch. Standardwerte: 600 für Command, 30 für Prompt, 60 für Agent                                                                            |
| `statusMessage` | nein         | Benutzerdefinierte Spinner-Nachricht, die angezeigt wird, während der Hook ausgeführt wird                                                                       |
| `once`          | nein         | Wenn `true`, wird nur einmal pro Sitzung ausgeführt und dann entfernt. Nur Skills, nicht Agents. Siehe [Hooks in Skills und Agents](#hooks-in-skills-and-agents) |

#### Command-Hook-Felder

Zusätzlich zu den [gemeinsamen Feldern](#common-fields) akzeptieren Command-Hooks diese Felder:

| Feld      | Erforderlich | Beschreibung                                                                                                                          |
| :-------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `command` | ja           | Shell-Befehl zum Ausführen                                                                                                            |
| `async`   | nein         | Wenn `true`, wird im Hintergrund ausgeführt, ohne zu blockieren. Siehe [Hooks im Hintergrund ausführen](#run-hooks-in-the-background) |

#### HTTP-Hook-Felder

Zusätzlich zu den [gemeinsamen Feldern](#common-fields) akzeptieren HTTP-Hooks diese Felder:

| Feld             | Erforderlich | Beschreibung                                                                                                                                                                                                                  |
| :--------------- | :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | ja           | URL, an die der POST-Request gesendet werden soll                                                                                                                                                                             |
| `headers`        | nein         | Zusätzliche HTTP-Header als Schlüssel-Wert-Paare. Werte unterstützen Umgebungsvariablen-Interpolation mit `$VAR_NAME` oder `${VAR_NAME}` Syntax. Nur Variablen, die in `allowedEnvVars` aufgelistet sind, werden aufgelöst    |
| `allowedEnvVars` | nein         | Liste von Umgebungsvariablennamen, die in Header-Werte interpoliert werden dürfen. Verweise auf nicht aufgelistete Variablen werden durch leere Zeichenketten ersetzt. Erforderlich für jede Umgebungsvariablen-Interpolation |

Claude Code sendet die [JSON-Eingabe](#hook-input-and-output) des Hooks als POST-Request-Body mit `Content-Type: application/json`. Der Response-Body verwendet das gleiche [JSON-Ausgabeformat](#json-output) wie Command-Hooks.

Die Fehlerbehandlung unterscheidet sich von Command-Hooks: Nicht-2xx-Antworten, Verbindungsfehler und Timeouts führen alle zu nicht-blockierenden Fehlern, die die Ausführung fortsetzen lassen. Um einen Tool-Aufruf zu blockieren oder eine Berechtigung zu verweigern, geben Sie eine 2xx-Antwort mit einem JSON-Body zurück, der `decision: "block"` oder ein `hookSpecificOutput` mit `permissionDecision: "deny"` enthält.

Dieses Beispiel sendet `PreToolUse`-Ereignisse an einen lokalen Validierungsdienst und authentifiziert sich mit einem Token aus der `MY_TOKEN`-Umgebungsvariable:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### Prompt- und Agent-Hook-Felder

Zusätzlich zu den [gemeinsamen Feldern](#common-fields) akzeptieren Prompt- und Agent-Hooks diese Felder:

| Feld     | Erforderlich | Beschreibung                                                                                               |
| :------- | :----------- | :--------------------------------------------------------------------------------------------------------- |
| `prompt` | ja           | Prompt-Text zum Senden an das Modell. Verwenden Sie `$ARGUMENTS` als Platzhalter für die Hook-Eingabe JSON |
| `model`  | nein         | Modell zur Verwendung für die Evaluierung. Standardwert ist ein schnelles Modell                           |

Alle passenden Hooks werden parallel ausgeführt, und identische Handler werden automatisch dedupliziert. Command-Hooks werden nach Befehlszeichenkette dedupliziert, und HTTP-Hooks werden nach URL dedupliziert. Handler werden im aktuellen Verzeichnis mit der Umgebung von Claude Code ausgeführt. Die Umgebungsvariable `$CLAUDE_CODE_REMOTE` wird in Remote-Web-Umgebungen auf `"true"` gesetzt und ist in der lokalen CLI nicht gesetzt.

### Hooks nach Pfad referenzieren

Verwenden Sie Umgebungsvariablen, um Hook-Skripte relativ zum Projekt- oder Plugin-Root zu referenzieren, unabhängig vom Arbeitsverzeichnis, wenn der Hook ausgeführt wird:

* `$CLAUDE_PROJECT_DIR`: das Projekt-Root. In Anführungszeichen setzen, um Pfade mit Leerzeichen zu handhaben.
* `${CLAUDE_PLUGIN_ROOT}`: das Root-Verzeichnis des Plugins, für Skripte, die mit einem [Plugin](/de/plugins) gebündelt sind. Ändert sich bei jedem Plugin-Update.
* `${CLAUDE_PLUGIN_DATA}`: das [persistente Datenverzeichnis](/de/plugins-reference#persistent-data-directory) des Plugins, für Abhängigkeiten und Zustand, die Plugin-Updates überstehen sollten.

<Tabs>
  <Tab title="Projekt-Skripte">
    Dieses Beispiel verwendet `$CLAUDE_PROJECT_DIR`, um einen Style-Checker aus dem `.claude/hooks/`-Verzeichnis des Projekts nach jedem `Write`- oder `Edit`-Tool-Aufruf auszuführen:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Plugin-Skripte">
    Definieren Sie Plugin-Hooks in `hooks/hooks.json` mit einem optionalen Top-Level-Feld `description`. Wenn ein Plugin aktiviert ist, werden seine Hooks mit Ihren Benutzer- und Projekt-Hooks zusammengeführt.

    Dieses Beispiel führt ein Formatierungsskript aus, das mit dem Plugin gebündelt ist:

    ```json  theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    Siehe die [Plugin-Komponenten-Referenz](/de/plugins-reference#hooks) für Details zum Erstellen von Plugin-Hooks.
  </Tab>
</Tabs>

### Hooks in Skills und Agents

Zusätzlich zu Einstellungsdateien und Plugins können Hooks direkt in [Skills](/de/skills) und [Subagenten](/de/sub-agents) mit Frontmatter definiert werden. Diese Hooks sind auf den Lebenszyklus der Komponente beschränkt und werden nur ausgeführt, wenn diese Komponente aktiv ist.

Alle Hook-Ereignisse werden unterstützt. Für Subagenten werden `Stop`-Hooks automatisch in `SubagentStop` konvertiert, da dies das Ereignis ist, das ausgelöst wird, wenn ein Subagent fertig ist.

Hooks verwenden das gleiche Konfigurationsformat wie einstellungsbasierte Hooks, sind aber auf die Lebensdauer der Komponente beschränkt und werden bereinigt, wenn sie fertig ist.

Dieser Skill definiert einen `PreToolUse`-Hook, der ein Sicherheitsvalidierungsskript vor jedem `Bash`-Befehl ausführt:

```yaml  theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Agents verwenden das gleiche Format in ihrem YAML-Frontmatter.

### Das Menü `/hooks`

Geben Sie `/hooks` in Claude Code ein, um einen schreibgeschützten Browser für Ihre konfigurierten Hooks zu öffnen. Das Menü zeigt jedes Hook-Ereignis mit einer Anzahl konfigurierter Hooks, ermöglicht es Ihnen, in Matcher zu bohren, und zeigt die vollständigen Details jedes Hook-Handlers. Verwenden Sie es, um die Konfiguration zu überprüfen, zu prüfen, aus welcher Einstellungsdatei ein Hook stammt, oder einen Hook-Befehl, Prompt oder URL zu überprüfen.

Das Menü zeigt alle vier Hook-Typen an: `command`, `prompt`, `agent` und `http`. Jeder Hook ist mit einem `[type]`-Präfix und einer Quelle gekennzeichnet, die angibt, wo er definiert wurde:

* `User`: aus `~/.claude/settings.json`
* `Project`: aus `.claude/settings.json`
* `Local`: aus `.claude/settings.local.json`
* `Plugin`: aus `hooks/hooks.json` eines Plugins
* `Session`: in Speicher für die aktuelle Sitzung registriert
* `Built-in`: intern von Claude Code registriert

Wenn Sie einen Hook auswählen, wird eine Detailansicht geöffnet, die sein Ereignis, Matcher, Typ, Quelldatei und den vollständigen Befehl, Prompt oder URL zeigt. Das Menü ist schreibgeschützt: Um Hooks hinzuzufügen, zu ändern oder zu entfernen, bearbeiten Sie die Einstellungs-JSON direkt oder bitten Sie Claude, die Änderung vorzunehmen.

### Hooks deaktivieren oder entfernen

Um einen Hook zu entfernen, löschen Sie seinen Eintrag aus der Einstellungs-JSON-Datei.

Um alle Hooks vorübergehend zu deaktivieren, ohne sie zu entfernen, setzen Sie `"disableAllHooks": true` in Ihrer Einstellungsdatei. Es gibt keine Möglichkeit, einen einzelnen Hook zu deaktivieren, während er in der Konfiguration bleibt.

Die Einstellung `disableAllHooks` respektiert die Hierarchie der verwalteten Einstellungen. Wenn ein Administrator Hooks durch verwaltete Richtlinieneinstellungen konfiguriert hat, kann `disableAllHooks`, das in Benutzer-, Projekt- oder lokalen Einstellungen gesetzt ist, diese verwalteten Hooks nicht deaktivieren. Nur `disableAllHooks`, das auf der Ebene der verwalteten Einstellungen gesetzt ist, kann verwaltete Hooks deaktivieren.

Direkte Bearbeitungen von Hooks in Einstellungsdateien werden normalerweise automatisch vom Datei-Watcher aufgegriffen.

## Hook-Eingabe und -Ausgabe

Command-Hooks erhalten JSON-Daten über stdin und kommunizieren Ergebnisse über Exit-Codes, stdout und stderr. HTTP-Hooks erhalten die gleiche JSON als POST-Request-Body und kommunizieren Ergebnisse über den HTTP-Response-Body. Dieser Abschnitt behandelt Felder und Verhalten, die allen Ereignissen gemeinsam sind. Jeder Abschnitt eines Ereignisses unter [Hook-Ereignisse](#hook-events) enthält sein spezifisches Eingabeschema und Optionen zur Entscheidungskontrolle.

### Gemeinsame Eingabefelder

Alle Hook-Ereignisse erhalten diese Felder als JSON, zusätzlich zu ereignisspezifischen Feldern, die in jedem Abschnitt [Hook-Ereignis](#hook-events) dokumentiert sind. Für Command-Hooks kommt diese JSON über stdin an. Für HTTP-Hooks kommt sie als POST-Request-Body an.

| Feld              | Beschreibung                                                                                                                                                                                                                                                   |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | Aktuelle Sitzungs-ID                                                                                                                                                                                                                                           |
| `transcript_path` | Pfad zur Gesprächs-JSON                                                                                                                                                                                                                                        |
| `cwd`             | Aktuelles Arbeitsverzeichnis, wenn der Hook aufgerufen wird                                                                                                                                                                                                    |
| `permission_mode` | Aktueller [Berechtigungsmodus](/de/permissions#permission-modes): `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` oder `"bypassPermissions"`. Nicht alle Ereignisse erhalten dieses Feld: siehe jedes Ereignis-JSON-Beispiel unten, um zu prüfen |
| `hook_event_name` | Name des ausgelösten Ereignisses                                                                                                                                                                                                                               |

Wenn mit `--agent` oder innerhalb eines Subagenten ausgeführt, sind zwei zusätzliche Felder enthalten:

| Feld         | Beschreibung                                                                                                                                                                                                                                                     |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Eindeutige Kennung für den Subagenten. Nur vorhanden, wenn der Hook innerhalb eines Subagenten-Aufrufs ausgelöst wird. Verwenden Sie dies, um Subagenten-Hook-Aufrufe von Main-Thread-Aufrufen zu unterscheiden.                                                 |
| `agent_type` | Agent-Name (zum Beispiel `"Explore"` oder `"security-reviewer"`). Vorhanden, wenn die Sitzung `--agent` verwendet oder der Hook innerhalb eines Subagenten ausgelöst wird. Für Subagenten hat der Typ des Subagenten Vorrang vor dem `--agent`-Wert der Sitzung. |

Zum Beispiel erhält ein `PreToolUse`-Hook für einen Bash-Befehl dies über stdin:

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Die Felder `tool_name` und `tool_input` sind ereignisspezifisch. Jeder Abschnitt [Hook-Ereignis](#hook-events) dokumentiert die zusätzlichen Felder für dieses Ereignis.

### Exit-Code-Ausgabe

Der Exit-Code aus Ihrem Hook-Befehl teilt Claude Code mit, ob die Aktion fortgesetzt, blockiert oder ignoriert werden soll.

**Exit 0** bedeutet Erfolg. Claude Code analysiert stdout auf [JSON-Ausgabefelder](#json-output). JSON-Ausgabe wird nur bei Exit 0 verarbeitet. Für die meisten Ereignisse wird stdout nur im ausführlichen Modus (`Ctrl+O`) angezeigt. Die Ausnahmen sind `UserPromptSubmit` und `SessionStart`, wo stdout als Kontext hinzugefügt wird, den Claude sehen und darauf reagieren kann.

**Exit 2** bedeutet ein blockierender Fehler. Claude Code ignoriert stdout und jede JSON darin. Stattdessen wird der stderr-Text an Claude als Fehlermeldung zurückgegeben. Die Auswirkung hängt vom Ereignis ab: `PreToolUse` blockiert den Tool-Aufruf, `UserPromptSubmit` lehnt den Prompt ab, und so weiter. Siehe [Exit-Code-2-Verhalten](#exit-code-2-behavior-per-event) für die vollständige Liste.

**Jeder andere Exit-Code** ist ein nicht-blockierender Fehler. stderr wird im ausführlichen Modus (`Ctrl+O`) angezeigt und die Ausführung wird fortgesetzt.

Zum Beispiel ein Hook-Befehlsskript, das gefährliche Bash-Befehle blockiert:

```bash  theme={null}
#!/bin/bash
# Liest JSON-Eingabe von stdin, prüft den Befehl
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blockierender Fehler: Tool-Aufruf wird verhindert
fi

exit 0  # Erfolg: Tool-Aufruf wird fortgesetzt
```

#### Exit-Code-2-Verhalten pro Ereignis

Exit-Code 2 ist die Art, wie ein Hook signalisiert „Stopp, mach das nicht." Die Auswirkung hängt vom Ereignis ab, da einige Ereignisse Aktionen darstellen, die blockiert werden können (wie ein Tool-Aufruf, der noch nicht stattgefunden hat), und andere Dinge darstellen, die bereits passiert sind oder nicht verhindert werden können.

| Hook-Ereignis        | Kann blockiert werden? | Was passiert bei Exit 2                                                          |
| :------------------- | :--------------------- | :------------------------------------------------------------------------------- |
| `PreToolUse`         | Ja                     | Blockiert den Tool-Aufruf                                                        |
| `PermissionRequest`  | Ja                     | Verweigert die Berechtigung                                                      |
| `UserPromptSubmit`   | Ja                     | Blockiert die Prompt-Verarbeitung und löscht den Prompt                          |
| `Stop`               | Ja                     | Verhindert, dass Claude stoppt, setzt das Gespräch fort                          |
| `SubagentStop`       | Ja                     | Verhindert, dass der Subagent stoppt                                             |
| `TeammateIdle`       | Ja                     | Verhindert, dass der Teammate untätig wird (Teammate arbeitet weiter)            |
| `TaskCompleted`      | Ja                     | Verhindert, dass die Aufgabe als abgeschlossen markiert wird                     |
| `ConfigChange`       | Ja                     | Blockiert die Konfigurationsänderung von der Anwendung (außer `policy_settings`) |
| `StopFailure`        | Nein                   | Ausgabe und Exit-Code werden ignoriert                                           |
| `PostToolUse`        | Nein                   | Zeigt stderr Claude an (Tool wurde bereits ausgeführt)                           |
| `PostToolUseFailure` | Nein                   | Zeigt stderr Claude an (Tool ist bereits fehlgeschlagen)                         |
| `Notification`       | Nein                   | Zeigt stderr nur dem Benutzer an                                                 |
| `SubagentStart`      | Nein                   | Zeigt stderr nur dem Benutzer an                                                 |
| `SessionStart`       | Nein                   | Zeigt stderr nur dem Benutzer an                                                 |
| `SessionEnd`         | Nein                   | Zeigt stderr nur dem Benutzer an                                                 |
| `PreCompact`         | Nein                   | Zeigt stderr nur dem Benutzer an                                                 |
| `PostCompact`        | Nein                   | Zeigt stderr nur dem Benutzer an                                                 |
| `Elicitation`        | Ja                     | Verweigert die Elicitation                                                       |
| `ElicitationResult`  | Ja                     | Blockiert die Antwort (Aktion wird Ablehnung)                                    |
| `WorktreeCreate`     | Ja                     | Jeder Nicht-Null-Exit-Code führt zu Fehler bei der Worktree-Erstellung           |
| `WorktreeRemove`     | Nein                   | Fehler werden nur im Debug-Modus protokolliert                                   |
| `InstructionsLoaded` | Nein                   | Exit-Code wird ignoriert                                                         |

### HTTP-Response-Behandlung

HTTP-Hooks verwenden HTTP-Statuscodes und Response-Bodies anstelle von Exit-Codes und stdout:

* **2xx mit leerem Body**: Erfolg, äquivalent zu Exit-Code 0 ohne Ausgabe
* **2xx mit Plain-Text-Body**: Erfolg, der Text wird als Kontext hinzugefügt
* **2xx mit JSON-Body**: Erfolg, analysiert mit dem gleichen [JSON-Ausgabe](#json-output)-Schema wie Command-Hooks
* **Nicht-2xx-Status**: Nicht-blockierender Fehler, Ausführung wird fortgesetzt
* **Verbindungsfehler oder Timeout**: Nicht-blockierender Fehler, Ausführung wird fortgesetzt

Im Gegensatz zu Command-Hooks können HTTP-Hooks nicht allein durch Statuscodes einen blockierenden Fehler signalisieren. Um einen Tool-Aufruf zu blockieren oder eine Berechtigung zu verweigern, geben Sie eine 2xx-Antwort mit einem JSON-Body zurück, der die entsprechenden Entscheidungsfelder enthält.

### JSON-Ausgabe

Exit-Codes ermöglichen es Ihnen, zuzulassen oder zu blockieren, aber JSON-Ausgabe gibt Ihnen eine feinere Kontrolle. Anstatt mit Code 2 zu beenden, um zu blockieren, beenden Sie mit 0 und geben Sie ein JSON-Objekt auf stdout aus. Claude Code liest spezifische Felder aus diesem JSON, um das Verhalten zu steuern, einschließlich [Entscheidungskontrolle](#decision-control) zum Blockieren, Zulassen oder Eskalieren an den Benutzer.

<Note>
  Sie müssen einen Ansatz pro Hook wählen, nicht beide: Verwenden Sie entweder Exit-Codes allein zum Signalisieren, oder beenden Sie mit 0 und geben Sie JSON für strukturierte Kontrolle aus. Claude Code verarbeitet JSON nur bei Exit 0. Wenn Sie mit 2 beenden, wird jede JSON ignoriert.
</Note>

Die stdout Ihres Hooks darf nur das JSON-Objekt enthalten. Wenn Ihr Shell-Profil beim Start Text ausgibt, kann dies die JSON-Analyse beeinträchtigen. Siehe [JSON-Validierung fehlgeschlagen](/de/hooks-guide#json-validation-failed) in der Fehlerbehebungsanleitung.

Das JSON-Objekt unterstützt drei Arten von Feldern:

* **Universelle Felder** wie `continue` funktionieren über alle Ereignisse hinweg. Diese sind in der Tabelle unten aufgelistet.
* **Top-Level `decision` und `reason`** werden von einigen Ereignissen verwendet, um zu blockieren oder Feedback zu geben.
* **`hookSpecificOutput`** ist ein verschachteltes Objekt für Ereignisse, die reichere Kontrolle benötigen. Es erfordert ein `hookEventName`-Feld, das auf den Ereignisnamen gesetzt ist.

| Feld             | Standard | Beschreibung                                                                                                                                                 |
| :--------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `continue`       | `true`   | Wenn `false`, stoppt Claude die Verarbeitung vollständig, nachdem der Hook ausgeführt wurde. Hat Vorrang vor allen ereignisspezifischen Entscheidungsfeldern |
| `stopReason`     | keine    | Nachricht, die dem Benutzer angezeigt wird, wenn `continue` `false` ist. Wird Claude nicht angezeigt                                                         |
| `suppressOutput` | `false`  | Wenn `true`, verbirgt stdout aus der Ausgabe des ausführlichen Modus                                                                                         |
| `systemMessage`  | keine    | Warnmeldung, die dem Benutzer angezeigt wird                                                                                                                 |

Um Claude unabhängig vom Ereignistyp vollständig zu stoppen:

```json  theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Entscheidungskontrolle

Nicht jedes Ereignis unterstützt das Blockieren oder Steuern des Verhaltens durch JSON. Die Ereignisse, die dies tun, verwenden jeweils einen anderen Satz von Feldern, um diese Entscheidung auszudrücken. Verwenden Sie diese Tabelle als schnelle Referenz, bevor Sie einen Hook schreiben:

| Ereignisse                                                                                         | Entscheidungsmuster              | Schlüsselfelder                                                                                                                                                                      |
| :------------------------------------------------------------------------------------------------- | :------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange                | Top-Level `decision`             | `decision: "block"`, `reason`                                                                                                                                                        |
| TeammateIdle, TaskCompleted                                                                        | Exit-Code oder `continue: false` | Exit-Code 2 blockiert die Aktion mit stderr-Feedback. JSON `{"continue": false, "stopReason": "..."}` stoppt auch den Teammate vollständig, was dem `Stop`-Hook-Verhalten entspricht |
| PreToolUse                                                                                         | `hookSpecificOutput`             | `permissionDecision` (allow/deny/ask), `permissionDecisionReason`                                                                                                                    |
| PermissionRequest                                                                                  | `hookSpecificOutput`             | `decision.behavior` (allow/deny)                                                                                                                                                     |
| WorktreeCreate                                                                                     | stdout-Pfad                      | Hook gibt absoluten Pfad zum erstellten Worktree aus. Nicht-Null-Exit schlägt die Erstellung fehl                                                                                    |
| Elicitation                                                                                        | `hookSpecificOutput`             | `action` (accept/decline/cancel), `content` (Formularfeldwerte für accept)                                                                                                           |
| ElicitationResult                                                                                  | `hookSpecificOutput`             | `action` (accept/decline/cancel), `content` (Formularfeldwerte überschreiben)                                                                                                        |
| WorktreeRemove, Notification, SessionEnd, PreCompact, PostCompact, InstructionsLoaded, StopFailure | Keine                            | Keine Entscheidungskontrolle. Wird für Nebenwirkungen wie Protokollierung oder Bereinigung verwendet                                                                                 |

Hier sind Beispiele für jedes Muster in Aktion:

<Tabs>
  <Tab title="Top-Level-Entscheidung">
    Wird von `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop` und `ConfigChange` verwendet. Der einzige Wert ist `"block"`. Um die Aktion fortzusetzen, lassen Sie `decision` aus Ihrem JSON weg, oder beenden Sie mit 0 ohne jede JSON:

    ```json  theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Verwendet `hookSpecificOutput` für reichere Kontrolle: zulassen, verweigern oder an den Benutzer eskalieren. Sie können auch die Tool-Eingabe vor der Ausführung ändern oder zusätzlichen Kontext für Claude injizieren. Siehe [PreToolUse-Entscheidungskontrolle](#pretooluse-decision-control) für den vollständigen Satz von Optionen.

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    Verwendet `hookSpecificOutput`, um eine Berechtigungsanfrage im Namen des Benutzers zuzulassen oder zu verweigern. Beim Zulassen können Sie auch die Eingabe des Tools ändern oder Berechtigungsregeln anwenden, damit der Benutzer nicht erneut aufgefordert wird. Siehe [PermissionRequest-Entscheidungskontrolle](#permissionrequest-decision-control) für den vollständigen Satz von Optionen.

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Erweiterte Beispiele einschließlich Bash-Befehlsvalidierung, Prompt-Filterung und Auto-Genehmigungsskripte finden Sie unter [Was Sie automatisieren können](/de/hooks-guide#what-you-can-automate) in der Anleitung und der [Bash-Befehlsvalidierungs-Referenzimplementierung](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## Hook-Ereignisse

Jedes Ereignis entspricht einem Punkt im Lebenszyklus von Claude Code, an dem Hooks ausgeführt werden können. Die folgenden Abschnitte sind in der Reihenfolge des Lebenszyklus angeordnet: von der Sitzungseinrichtung durch die agentengesteuerte Schleife bis zum Sitzungsende. Jeder Abschnitt beschreibt, wann das Ereignis ausgelöst wird, welche Matcher es unterstützt, die JSON-Eingabe, die es erhält, und wie das Verhalten durch die Ausgabe gesteuert wird.

### SessionStart

Wird ausgeführt, wenn Claude Code eine neue Sitzung startet oder eine vorhandene Sitzung fortsetzt. Nützlich zum Laden von Entwicklungskontext wie vorhandenen Problemen oder kürzlichen Änderungen an Ihrer Codebasis oder zum Einrichten von Umgebungsvariablen. Für statischen Kontext, der kein Skript erfordert, verwenden Sie stattdessen [CLAUDE.md](/de/memory).

SessionStart wird bei jeder Sitzung ausgeführt, daher halten Sie diese Hooks schnell. Nur `type: "command"`-Hooks werden unterstützt.

Der Matcher-Wert entspricht der Art, wie die Sitzung initiiert wurde:

| Matcher   | Wann es ausgelöst wird                  |
| :-------- | :-------------------------------------- |
| `startup` | Neue Sitzung                            |
| `resume`  | `--resume`, `--continue` oder `/resume` |
| `clear`   | `/clear`                                |
| `compact` | Auto- oder manuelle Komprimierung       |

#### SessionStart-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten SessionStart-Hooks `source`, `model` und optional `agent_type`. Das Feld `source` gibt an, wie die Sitzung gestartet wurde: `"startup"` für neue Sitzungen, `"resume"` für fortgesetzte Sitzungen, `"clear"` nach `/clear` oder `"compact"` nach Komprimierung. Das Feld `model` enthält die Modell-ID. Wenn Sie Claude Code mit `claude --agent <name>` starten, enthält ein Feld `agent_type` den Agent-Namen.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart-Entscheidungskontrolle

Jeder Text, den Ihr Hook-Skript auf stdout ausgibt, wird als Kontext für Claude hinzugefügt. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, können Sie diese ereignisspezifischen Felder zurückgeben:

| Feld                | Beschreibung                                                                                 |
| :------------------ | :------------------------------------------------------------------------------------------- |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext hinzugefügt wird. Werte mehrerer Hooks werden verkettet |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### Umgebungsvariablen beibehalten

SessionStart-Hooks haben Zugriff auf die Umgebungsvariable `CLAUDE_ENV_FILE`, die einen Dateipfad bereitstellt, in dem Sie Umgebungsvariablen für nachfolgende Bash-Befehle beibehalten können.

Um einzelne Umgebungsvariablen zu setzen, schreiben Sie `export`-Anweisungen in `CLAUDE_ENV_FILE`. Verwenden Sie Anhängen (`>>`), um Variablen zu bewahren, die von anderen Hooks gesetzt wurden:

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Um alle Umgebungsänderungen von Setup-Befehlen zu erfassen, vergleichen Sie die exportierten Variablen vorher und nachher:

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Führen Sie Ihre Setup-Befehle aus, die die Umgebung ändern
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Alle Variablen, die in diese Datei geschrieben werden, sind in allen nachfolgenden Bash-Befehlen verfügbar, die Claude Code während der Sitzung ausführt.

<Note>
  `CLAUDE_ENV_FILE` ist für SessionStart-Hooks verfügbar. Andere Hook-Typen haben keinen Zugriff auf diese Variable.
</Note>

### InstructionsLoaded

Wird ausgelöst, wenn eine `CLAUDE.md`- oder `.claude/rules/*.md`-Datei in den Kontext geladen wird. Dieses Ereignis wird beim Sitzungsstart für eifrig geladene Dateien ausgelöst und später erneut, wenn Dateien träge geladen werden, zum Beispiel wenn Claude auf ein Unterverzeichnis zugreift, das eine verschachtelte `CLAUDE.md` enthält, oder wenn bedingte Regeln mit `paths:`-Frontmatter passen. Der Hook unterstützt keine Blockierung oder Entscheidungskontrolle. Er wird asynchron zu Beobachtungszwecken ausgeführt.

Der Matcher wird gegen `load_reason` ausgeführt. Verwenden Sie zum Beispiel `"matcher": "session_start"`, um nur für Dateien zu feuern, die beim Sitzungsstart geladen werden, oder `"matcher": "path_glob_match|nested_traversal"`, um nur für träge Ladevorgänge zu feuern.

#### InstructionsLoaded-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten InstructionsLoaded-Hooks diese Felder:

| Feld                | Beschreibung                                                                                                                                                                                                                                |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `file_path`         | Absoluter Pfad zur Anweisungsdatei, die geladen wurde                                                                                                                                                                                       |
| `memory_type`       | Umfang der Datei: `"User"`, `"Project"`, `"Local"` oder `"Managed"`                                                                                                                                                                         |
| `load_reason`       | Warum die Datei geladen wurde: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"` oder `"compact"`. Der Wert `"compact"` wird ausgelöst, wenn Anweisungsdateien nach einem Komprimierungsereignis neu geladen werden |
| `globs`             | Pfad-Glob-Muster aus dem `paths:`-Frontmatter der Datei, falls vorhanden. Nur für `path_glob_match`-Ladevorgänge vorhanden                                                                                                                  |
| `trigger_file_path` | Pfad zur Datei, deren Zugriff diesen Ladevorgang ausgelöst hat, für träge Ladevorgänge                                                                                                                                                      |
| `parent_file_path`  | Pfad zur übergeordneten Anweisungsdatei, die diese eingebunden hat, für `include`-Ladevorgänge                                                                                                                                              |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### InstructionsLoaded-Entscheidungskontrolle

InstructionsLoaded-Hooks haben keine Entscheidungskontrolle. Sie können das Laden von Anweisungen nicht blockieren oder ändern. Verwenden Sie dieses Ereignis für Audit-Protokollierung, Compliance-Tracking oder Beobachtbarkeit.

### UserPromptSubmit

Wird ausgeführt, wenn der Benutzer einen Prompt einreicht, bevor Claude ihn verarbeitet. Dies ermöglicht es Ihnen, zusätzlichen Kontext basierend auf dem Prompt/Gespräch hinzuzufügen, Prompts zu validieren oder bestimmte Arten von Prompts zu blockieren.

#### UserPromptSubmit-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten UserPromptSubmit-Hooks das Feld `prompt`, das den Text enthält, den der Benutzer eingereicht hat.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### UserPromptSubmit-Entscheidungskontrolle

`UserPromptSubmit`-Hooks können steuern, ob ein Benutzer-Prompt verarbeitet wird und Kontext hinzufügen. Alle [JSON-Ausgabefelder](#json-output) sind verfügbar.

Es gibt zwei Möglichkeiten, Kontext zum Gespräch bei Exit-Code 0 hinzuzufügen:

* **Plain-Text-stdout**: Jeder Nicht-JSON-Text, der auf stdout geschrieben wird, wird als Kontext hinzugefügt
* **JSON mit `additionalContext`**: Verwenden Sie das JSON-Format unten für mehr Kontrolle. Das Feld `additionalContext` wird als Kontext hinzugefügt

Plain-stdout wird als Hook-Ausgabe im Transkript angezeigt. Das Feld `additionalContext` wird diskreter hinzugefügt.

Um einen Prompt zu blockieren, geben Sie ein JSON-Objekt mit `decision` auf `"block"` zurück:

| Feld                | Beschreibung                                                                                                            |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` verhindert die Verarbeitung des Prompts und löscht ihn aus dem Kontext. Weglassen, um den Prompt fortzusetzen |
| `reason`            | Wird dem Benutzer angezeigt, wenn `decision` `"block"` ist. Wird nicht zum Kontext hinzugefügt                          |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext hinzugefügt wird                                                                   |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

<Note>
  Das JSON-Format ist nicht erforderlich für einfache Anwendungsfälle. Um Kontext hinzuzufügen, können Sie einfach Plain-Text auf stdout mit Exit-Code 0 ausgeben. Verwenden Sie JSON, wenn Sie Prompts blockieren oder mehr strukturierte Kontrolle benötigen.
</Note>

### PreToolUse

Wird ausgeführt, nachdem Claude Tool-Parameter erstellt hat und bevor der Tool-Aufruf verarbeitet wird. Passt auf Tool-Namen: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch` und alle [MCP-Tool-Namen](#match-mcp-tools).

Verwenden Sie [PreToolUse-Entscheidungskontrolle](#pretooluse-decision-control), um die Verwendung des Tools zuzulassen, zu verweigern oder um Berechtigung zu bitten.

#### PreToolUse-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten PreToolUse-Hooks `tool_name`, `tool_input` und `tool_use_id`. Die Felder `tool_input` hängen vom Tool ab:

##### Bash

Führt Shell-Befehle aus.

| Feld                | Typ          | Beispiel           | Beschreibung                                        |
| :------------------ | :----------- | :----------------- | :-------------------------------------------------- |
| `command`           | Zeichenkette | `"npm test"`       | Der auszuführende Shell-Befehl                      |
| `description`       | Zeichenkette | `"Run test suite"` | Optionale Beschreibung, was der Befehl tut          |
| `timeout`           | Zahl         | `120000`           | Optionales Timeout in Millisekunden                 |
| `run_in_background` | Boolesch     | `false`            | Ob der Befehl im Hintergrund ausgeführt werden soll |

##### Write

Erstellt oder überschreibt eine Datei.

| Feld        | Typ          | Beispiel              | Beschreibung                             |
| :---------- | :----------- | :-------------------- | :--------------------------------------- |
| `file_path` | Zeichenkette | `"/path/to/file.txt"` | Absoluter Pfad zur zu schreibenden Datei |
| `content`   | Zeichenkette | `"file content"`      | Inhalt zum Schreiben in die Datei        |

##### Edit

Ersetzt eine Zeichenkette in einer vorhandenen Datei.

| Feld          | Typ          | Beispiel              | Beschreibung                              |
| :------------ | :----------- | :-------------------- | :---------------------------------------- |
| `file_path`   | Zeichenkette | `"/path/to/file.txt"` | Absoluter Pfad zur zu bearbeitenden Datei |
| `old_string`  | Zeichenkette | `"original text"`     | Text zum Suchen und Ersetzen              |
| `new_string`  | Zeichenkette | `"replacement text"`  | Ersatztext                                |
| `replace_all` | Boolesch     | `false`               | Ob alle Vorkommen ersetzt werden sollen   |

##### Read

Liest Dateiinhalte.

| Feld        | Typ          | Beispiel              | Beschreibung                                  |
| :---------- | :----------- | :-------------------- | :-------------------------------------------- |
| `file_path` | Zeichenkette | `"/path/to/file.txt"` | Absoluter Pfad zur zu lesenden Datei          |
| `offset`    | Zahl         | `10`                  | Optionale Zeilennummer zum Starten des Lesens |
| `limit`     | Zahl         | `50`                  | Optionale Anzahl der zu lesenden Zeilen       |

##### Glob

Findet Dateien, die einem Glob-Muster entsprechen.

| Feld      | Typ          | Beispiel         | Beschreibung                                                                          |
| :-------- | :----------- | :--------------- | :------------------------------------------------------------------------------------ |
| `pattern` | Zeichenkette | `"**/*.ts"`      | Glob-Muster zum Abgleichen von Dateien                                                |
| `path`    | Zeichenkette | `"/path/to/dir"` | Optionales Verzeichnis zum Durchsuchen. Standardwert ist aktuelles Arbeitsverzeichnis |

##### Grep

Durchsucht Dateiinhalte mit regulären Ausdrücken.

| Feld          | Typ          | Beispiel         | Beschreibung                                                                                |
| :------------ | :----------- | :--------------- | :------------------------------------------------------------------------------------------ |
| `pattern`     | Zeichenkette | `"TODO.*fix"`    | Regex-Muster zum Suchen                                                                     |
| `path`        | Zeichenkette | `"/path/to/dir"` | Optionale Datei oder Verzeichnis zum Durchsuchen                                            |
| `glob`        | Zeichenkette | `"*.ts"`         | Optionales Glob-Muster zum Filtern von Dateien                                              |
| `output_mode` | Zeichenkette | `"content"`      | `"content"`, `"files_with_matches"` oder `"count"`. Standardwert ist `"files_with_matches"` |
| `-i`          | Boolesch     | `true`           | Groß-/Kleinschreibung ignorieren                                                            |
| `multiline`   | Boolesch     | `false`          | Mehrzeiliges Matching aktivieren                                                            |

##### WebFetch

Ruft Web-Inhalte ab und verarbeitet sie.

| Feld     | Typ          | Beispiel                      | Beschreibung                                    |
| :------- | :----------- | :---------------------------- | :---------------------------------------------- |
| `url`    | Zeichenkette | `"https://example.com/api"`   | URL zum Abrufen von Inhalten                    |
| `prompt` | Zeichenkette | `"Extract the API endpoints"` | Prompt zum Ausführen auf dem abgerufenen Inhalt |

##### WebSearch

Durchsucht das Web.

| Feld              | Typ          | Beispiel                       | Beschreibung                                            |
| :---------------- | :----------- | :----------------------------- | :------------------------------------------------------ |
| `query`           | Zeichenkette | `"react hooks best practices"` | Suchanfrage                                             |
| `allowed_domains` | Array        | `["docs.example.com"]`         | Optional: Nur Ergebnisse von diesen Domains einbeziehen |
| `blocked_domains` | Array        | `["spam.example.com"]`         | Optional: Ergebnisse von diesen Domains ausschließen    |

##### Agent

Spawnt einen [Subagenten](/de/sub-agents).

| Feld            | Typ          | Beispiel                   | Beschreibung                                            |
| :-------------- | :----------- | :------------------------- | :------------------------------------------------------ |
| `prompt`        | Zeichenkette | `"Find all API endpoints"` | Die Aufgabe für den Agent                               |
| `description`   | Zeichenkette | `"Find API endpoints"`     | Kurze Beschreibung der Aufgabe                          |
| `subagent_type` | Zeichenkette | `"Explore"`                | Typ des zu verwendenden spezialisierten Agenten         |
| `model`         | Zeichenkette | `"sonnet"`                 | Optionaler Modell-Alias zum Überschreiben des Standards |

#### PreToolUse-Entscheidungskontrolle

`PreToolUse`-Hooks können steuern, ob ein Tool-Aufruf fortgesetzt wird. Im Gegensatz zu anderen Hooks, die ein Top-Level-Feld `decision` verwenden, gibt PreToolUse seine Entscheidung in einem `hookSpecificOutput`-Objekt zurück. Dies gibt ihm reichere Kontrolle: drei Ergebnisse (zulassen, verweigern oder fragen) plus die Möglichkeit, die Tool-Eingabe vor der Ausführung zu ändern.

| Feld                       | Beschreibung                                                                                                                                                                                                                                     |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` umgeht das Berechtigungssystem, `"deny"` verhindert den Tool-Aufruf, `"ask"` fordert den Benutzer zur Bestätigung auf. [Deny- und Ask-Regeln](/de/permissions#manage-permissions) gelten weiterhin, wenn ein Hook `"allow"` zurückgibt |
| `permissionDecisionReason` | Für `"allow"` und `"ask"`, dem Benutzer angezeigt, aber nicht Claude. Für `"deny"`, Claude angezeigt                                                                                                                                             |
| `updatedInput`             | Ändert die Tool-Eingabeparameter vor der Ausführung. Kombinieren Sie mit `"allow"`, um automatisch zu genehmigen, oder mit `"ask"`, um die geänderte Eingabe dem Benutzer zu zeigen                                                              |
| `additionalContext`        | Zeichenkette, die zu Claudes Kontext vor der Tool-Ausführung hinzugefügt wird                                                                                                                                                                    |

Wenn ein Hook `"ask"` zurückgibt, enthält der dem Benutzer angezeigte Berechtigungsprompt ein Label, das angibt, woher der Hook stammt: zum Beispiel `[User]`, `[Project]`, `[Plugin]` oder `[Local]`. Dies hilft Benutzern zu verstehen, welche Konfigurationsquelle eine Bestätigung anfordert.

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

<Note>
  PreToolUse verwendete zuvor Top-Level-Felder `decision` und `reason`, diese sind jedoch für dieses Ereignis veraltet. Verwenden Sie stattdessen `hookSpecificOutput.permissionDecision` und `hookSpecificOutput.permissionDecisionReason`. Die veralteten Werte `"approve"` und `"block"` werden auf `"allow"` und `"deny"` abgebildet. Andere Ereignisse wie PostToolUse und Stop verwenden weiterhin Top-Level-Felder `decision` und `reason` als ihr aktuelles Format.
</Note>

### PermissionRequest

Wird ausgeführt, wenn dem Benutzer ein Berechtigungsdialog angezeigt wird.
Verwenden Sie [PermissionRequest-Entscheidungskontrolle](#permissionrequest-decision-control), um im Namen des Benutzers zuzulassen oder zu verweigern.

Passt auf Tool-Namen, gleiche Werte wie PreToolUse.

#### PermissionRequest-Eingabe

PermissionRequest-Hooks erhalten `tool_name`- und `tool_input`-Felder wie PreToolUse-Hooks, aber ohne `tool_use_id`. Ein optionales Array `permission_suggestions` enthält die Optionen „Immer zulassen", die der Benutzer normalerweise im Berechtigungsdialog sehen würde. Der Unterschied liegt darin, wann der Hook ausgelöst wird: PermissionRequest-Hooks werden ausgeführt, wenn ein Berechtigungsdialog dem Benutzer angezeigt werden soll, während PreToolUse-Hooks vor der Tool-Ausführung unabhängig vom Berechtigungsstatus ausgeführt werden.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### PermissionRequest-Entscheidungskontrolle

`PermissionRequest`-Hooks können Berechtigungsanfragen zulassen oder verweigern. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript ein `decision`-Objekt mit diesen ereignisspezifischen Feldern zurückgeben:

| Feld                 | Beschreibung                                                                                                                                                                               |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` gewährt die Berechtigung, `"deny"` verweigert sie                                                                                                                                |
| `updatedInput`       | Nur für `"allow"`: ändert die Tool-Eingabeparameter vor der Ausführung                                                                                                                     |
| `updatedPermissions` | Nur für `"allow"`: Array von [Berechtigungsupdate-Einträgen](#permission-update-entries) zum Anwenden, wie das Hinzufügen einer Allow-Regel oder das Ändern des Session-Berechtigungsmodus |
| `message`            | Nur für `"deny"`: teilt Claude mit, warum die Berechtigung verweigert wurde                                                                                                                |
| `interrupt`          | Nur für `"deny"`: wenn `true`, stoppt Claude                                                                                                                                               |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### Berechtigungsupdate-Einträge

Das Ausgabefeld `updatedPermissions` und das [`permission_suggestions`-Eingabefeld](#permissionrequest-input) verwenden beide das gleiche Array von Einträgen. Jeder Eintrag hat einen `type`, der seine anderen Felder bestimmt, und ein `destination`, das steuert, wo die Änderung geschrieben wird.

| `type`              | Felder                             | Effekt                                                                                                                                                                                                     |
| :------------------ | :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`, `behavior`, `destination` | Fügt Berechtigungsregeln hinzu. `rules` ist ein Array von `{toolName, ruleContent?}` Objekten. Lassen Sie `ruleContent` weg, um das ganze Tool zu treffen. `behavior` ist `"allow"`, `"deny"` oder `"ask"` |
| `replaceRules`      | `rules`, `behavior`, `destination` | Ersetzt alle Regeln des gegebenen `behavior` am `destination` mit den bereitgestellten `rules`                                                                                                             |
| `removeRules`       | `rules`, `behavior`, `destination` | Entfernt passende Regeln des gegebenen `behavior`                                                                                                                                                          |
| `setMode`           | `mode`, `destination`              | Ändert den Berechtigungsmodus. Gültige Modi sind `default`, `acceptEdits`, `dontAsk`, `bypassPermissions` und `plan`                                                                                       |
| `addDirectories`    | `directories`, `destination`       | Fügt Arbeitsverzeichnisse hinzu. `directories` ist ein Array von Pfad-Zeichenketten                                                                                                                        |
| `removeDirectories` | `directories`, `destination`       | Entfernt Arbeitsverzeichnisse                                                                                                                                                                              |

Das Feld `destination` auf jedem Eintrag bestimmt, ob die Änderung im Speicher bleibt oder in einer Einstellungsdatei persistiert wird.

| `destination`     | Schreibt zu                                             |
| :---------------- | :------------------------------------------------------ |
| `session`         | Nur im Speicher, wird verworfen, wenn die Sitzung endet |
| `localSettings`   | `.claude/settings.local.json`                           |
| `projectSettings` | `.claude/settings.json`                                 |
| `userSettings`    | `~/.claude/settings.json`                               |

Ein Hook kann eines der `permission_suggestions` widerspiegeln, die er als seine eigene `updatedPermissions`-Ausgabe erhalten hat, was gleichbedeutend mit der Auswahl dieser Option „Immer zulassen" durch den Benutzer im Dialog ist.

### PostToolUse

Wird unmittelbar nach erfolgreichem Abschluss eines Tools ausgeführt.

Passt auf Tool-Namen, gleiche Werte wie PreToolUse.

#### PostToolUse-Eingabe

`PostToolUse`-Hooks werden ausgelöst, nachdem ein Tool bereits erfolgreich ausgeführt wurde. Die Eingabe enthält sowohl `tool_input`, die an das Tool gesendeten Argumente, als auch `tool_response`, das Ergebnis, das es zurückgegeben hat. Das genaue Schema für beide hängt vom Tool ab.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

#### PostToolUse-Entscheidungskontrolle

`PostToolUse`-Hooks können Claude nach der Tool-Ausführung Feedback geben. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript diese ereignisspezifischen Felder zurückgeben:

| Feld                   | Beschreibung                                                                                         |
| :--------------------- | :--------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` fordert Claude mit dem `reason` auf. Weglassen, um die Aktion fortzusetzen                 |
| `reason`               | Erklärung, die Claude angezeigt wird, wenn `decision` `"block"` ist                                  |
| `additionalContext`    | Zusätzlicher Kontext für Claude zu berücksichtigen                                                   |
| `updatedMCPToolOutput` | Nur für [MCP-Tools](#match-mcp-tools): ersetzt die Ausgabe des Tools durch den bereitgestellten Wert |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### PostToolUseFailure

Wird ausgeführt, wenn eine Tool-Ausführung fehlschlägt. Dieses Ereignis wird für Tool-Aufrufe ausgelöst, die Fehler werfen oder Fehlerergebnisse zurückgeben. Verwenden Sie dies, um Fehler zu protokollieren, Warnungen zu senden oder korrektes Feedback an Claude zu geben.

Passt auf Tool-Namen, gleiche Werte wie PreToolUse.

#### PostToolUseFailure-Eingabe

PostToolUseFailure-Hooks erhalten die gleichen `tool_name`- und `tool_input`-Felder wie PostToolUse, zusammen mit Fehlerinformationen als Top-Level-Felder:

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

| Feld           | Beschreibung                                                                                |
| :------------- | :------------------------------------------------------------------------------------------ |
| `error`        | Zeichenkette, die beschreibt, was schief gelaufen ist                                       |
| `is_interrupt` | Optionaler Boolesch, der angibt, ob der Fehler durch Benutzerunterbrechung verursacht wurde |

#### PostToolUseFailure-Entscheidungskontrolle

`PostToolUseFailure`-Hooks können Claude nach einem Tool-Fehler Kontext geben. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript diese ereignisspezifischen Felder zurückgeben:

| Feld                | Beschreibung                                                        |
| :------------------ | :------------------------------------------------------------------ |
| `additionalContext` | Zusätzlicher Kontext für Claude zu berücksichtigen neben dem Fehler |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### Notification

Wird ausgeführt, wenn Claude Code Benachrichtigungen sendet. Passt auf Benachrichtigungstyp: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`. Matcher weglassen, um Hooks für alle Benachrichtigungstypen auszuführen.

Verwenden Sie separate Matcher, um verschiedene Handler je nach Benachrichtigungstyp auszuführen. Diese Konfiguration löst ein berechtigungsspezifisches Warnungsskript aus, wenn Claude Genehmigung benötigt, und eine andere Benachrichtigung, wenn Claude untätig war:

```json  theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Notification-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten Notification-Hooks `message` mit dem Benachrichtigungstext, ein optionales `title` und `notification_type`, das angibt, welcher Typ ausgelöst wurde.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification-Hooks können Benachrichtigungen nicht blockieren oder ändern. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, können Sie `additionalContext` zurückgeben, um Kontext zum Gespräch hinzuzufügen:

| Feld                | Beschreibung                                          |
| :------------------ | :---------------------------------------------------- |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext hinzugefügt wird |

### SubagentStart

Wird ausgeführt, wenn ein Claude Code-Subagent über das Agent-Tool spawnt wird. Unterstützt Matcher zum Filtern nach Agent-Typname (eingebaute Agents wie `Bash`, `Explore`, `Plan` oder benutzerdefinierte Agent-Namen aus `.claude/agents/`).

#### SubagentStart-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten SubagentStart-Hooks `agent_id` mit der eindeutigen Kennung für den Subagenten und `agent_type` mit dem Agent-Namen (eingebaute Agents wie `"Bash"`, `"Explore"`, `"Plan"` oder benutzerdefinierte Agent-Namen).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart-Hooks können die Subagenten-Erstellung nicht blockieren, können aber Kontext in den Subagenten injizieren. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, können Sie zurückgeben:

| Feld                | Beschreibung                                                  |
| :------------------ | :------------------------------------------------------------ |
| `additionalContext` | Zeichenkette, die zum Kontext des Subagenten hinzugefügt wird |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Wird ausgeführt, wenn ein Claude Code-Subagent fertig mit der Antwort ist. Passt auf Agent-Typ, gleiche Werte wie SubagentStart.

#### SubagentStop-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten SubagentStop-Hooks `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` und `last_assistant_message`. Das Feld `agent_type` ist der Wert, der zum Filtern von Matchern verwendet wird. Der `transcript_path` ist das Transkript der Hauptsitzung, während `agent_transcript_path` das eigene Transkript des Subagenten ist, das in einem verschachtelten `subagents/`-Ordner gespeichert ist. Das Feld `last_assistant_message` enthält den Textinhalt der letzten Antwort des Subagenten, daher können Hooks darauf zugreifen, ohne die Transkript-Datei zu analysieren.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

SubagentStop-Hooks verwenden das gleiche Entscheidungskontrollformat wie [Stop-Hooks](#stop-decision-control).

### Stop

Wird ausgeführt, wenn der Haupt-Claude Code-Agent fertig mit der Antwort ist. Wird nicht ausgeführt, wenn der Stopp durch eine Benutzerunterbrechung verursacht wurde. API-Fehler lösen stattdessen [StopFailure](#stopfailure) aus.

#### Stop-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten Stop-Hooks `stop_hook_active` und `last_assistant_message`. Das Feld `stop_hook_active` ist `true`, wenn Claude Code bereits als Ergebnis eines Stop-Hooks fortgesetzt wird. Überprüfen Sie diesen Wert oder verarbeiten Sie das Transkript, um zu verhindern, dass Claude Code unbegrenzt läuft. Das Feld `last_assistant_message` enthält den Textinhalt von Claudes letzter Antwort, daher können Hooks darauf zugreifen, ohne die Transkript-Datei zu analysieren.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Stop-Entscheidungskontrolle

`Stop`- und `SubagentStop`-Hooks können steuern, ob Claude fortgesetzt wird. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript diese ereignisspezifischen Felder zurückgeben:

| Feld       | Beschreibung                                                                                      |
| :--------- | :------------------------------------------------------------------------------------------------ |
| `decision` | `"block"` verhindert, dass Claude stoppt. Weglassen, um Claude zu stoppen                         |
| `reason`   | Erforderlich, wenn `decision` `"block"` ist. Teilt Claude mit, warum es fortgesetzt werden sollte |

```json  theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

Wird stattdessen von [Stop](#stop) ausgeführt, wenn die Runde aufgrund eines API-Fehlers endet. Ausgabe und Exit-Code werden ignoriert. Verwenden Sie dies, um Fehler zu protokollieren, Warnungen zu senden oder Wiederherstellungsmaßnahmen zu ergreifen, wenn Claude aufgrund von Ratenlimits, Authentifizierungsproblemen oder anderen API-Fehlern keine Antwort abschließen kann.

#### StopFailure-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten StopFailure-Hooks `error`, optionales `error_details` und optionales `last_assistant_message`. Das Feld `error` identifiziert den Fehlertyp und wird zum Filtern von Matchern verwendet.

| Feld                     | Beschreibung                                                                                                                                                                                                                                                         |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | Fehlertyp: `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens` oder `unknown`                                                                                                                             |
| `error_details`          | Zusätzliche Details zum Fehler, falls verfügbar                                                                                                                                                                                                                      |
| `last_assistant_message` | Der gerenderte Fehlertext, der in der Konversation angezeigt wird. Im Gegensatz zu `Stop` und `SubagentStop`, wo dieses Feld Claudes Gesprächsausgabe enthält, enthält es für `StopFailure` die API-Fehlerzeichenkette selbst, wie `"API Error: Rate limit reached"` |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

StopFailure-Hooks haben keine Entscheidungskontrolle. Sie werden nur zu Benachrichtigungs- und Protokollierungszwecken ausgeführt.

### TeammateIdle

Wird ausgeführt, wenn ein [Agent-Team](/de/agent-teams)-Teammate nach Abschluss seiner Runde untätig werden soll. Verwenden Sie dies, um Qualitätsgates vor dem Stoppen eines Teammates durchzusetzen, wie das Erfordern von bestandenen Lint-Checks oder das Überprüfen, dass Ausgabedateien vorhanden sind.

Wenn ein `TeammateIdle`-Hook mit Code 2 beendet wird, erhält der Teammate die stderr-Nachricht als Feedback und arbeitet weiter, anstatt untätig zu werden. Um den Teammate stattdessen vollständig zu stoppen, geben Sie JSON mit `{"continue": false, "stopReason": "..."}` zurück. TeammateIdle-Hooks unterstützen keine Matcher und werden bei jedem Auftreten ausgelöst.

#### TeammateIdle-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten TeammateIdle-Hooks `teammate_name` und `team_name`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| Feld            | Beschreibung                                |
| :-------------- | :------------------------------------------ |
| `teammate_name` | Name des Teammates, das untätig werden soll |
| `team_name`     | Name des Teams                              |

#### TeammateIdle-Entscheidungskontrolle

TeammateIdle-Hooks unterstützen zwei Möglichkeiten, das Teammate-Verhalten zu steuern:

* **Exit-Code 2**: Der Teammate erhält die stderr-Nachricht als Feedback und arbeitet weiter, anstatt untätig zu werden.
* **JSON `{"continue": false, "stopReason": "..."}`**: Stoppt den Teammate vollständig, was dem `Stop`-Hook-Verhalten entspricht. Der `stopReason` wird dem Benutzer angezeigt.

Dieses Beispiel prüft, dass ein Build-Artefakt vorhanden ist, bevor ein Teammate untätig werden darf:

```bash  theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Wird ausgeführt, wenn eine Aufgabe als abgeschlossen markiert wird. Dies wird in zwei Situationen ausgelöst: wenn ein Agent eine Aufgabe explizit über das TaskUpdate-Tool als abgeschlossen markiert, oder wenn ein [Agent-Team](/de/agent-teams)-Teammate seine Runde mit laufenden Aufgaben beendet. Verwenden Sie dies, um Abschluss-Kriterien wie bestandene Tests oder Lint-Checks durchzusetzen, bevor eine Aufgabe geschlossen werden kann.

Wenn ein `TaskCompleted`-Hook mit Code 2 beendet wird, wird die Aufgabe nicht als abgeschlossen markiert und die stderr-Nachricht wird dem Modell als Feedback zurückgegeben. Um den Teammate stattdessen vollständig zu stoppen, geben Sie JSON mit `{"continue": false, "stopReason": "..."}` zurück. TaskCompleted-Hooks unterstützen keine Matcher und werden bei jedem Auftreten ausgelöst.

#### TaskCompleted-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten TaskCompleted-Hooks `task_id`, `task_subject` und optional `task_description`, `teammate_name` und `team_name`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Feld               | Beschreibung                                                |
| :----------------- | :---------------------------------------------------------- |
| `task_id`          | Kennung der abgeschlossenen Aufgabe                         |
| `task_subject`     | Titel der Aufgabe                                           |
| `task_description` | Detaillierte Beschreibung der Aufgabe. Kann fehlen          |
| `teammate_name`    | Name des Teammates, das die Aufgabe abschließt. Kann fehlen |
| `team_name`        | Name des Teams. Kann fehlen                                 |

#### TaskCompleted-Entscheidungskontrolle

TaskCompleted-Hooks unterstützen zwei Möglichkeiten, den Aufgabenabschluss zu steuern:

* **Exit-Code 2**: Die Aufgabe wird nicht als abgeschlossen markiert und die stderr-Nachricht wird dem Modell als Feedback zurückgegeben.
* **JSON `{"continue": false, "stopReason": "..."}`**: Stoppt den Teammate vollständig, was dem `Stop`-Hook-Verhalten entspricht. Der `stopReason` wird dem Benutzer angezeigt.

Dieses Beispiel führt Tests aus und blockiert den Aufgabenabschluss, wenn sie fehlschlagen:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Führen Sie die Test-Suite aus
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### ConfigChange

Wird ausgeführt, wenn sich eine Konfigurationsdatei während einer Sitzung ändert. Verwenden Sie dies, um Einstellungsänderungen zu überprüfen, Sicherheitsrichtlinien durchzusetzen oder nicht autorisierte Änderungen an Konfigurationsdateien zu blockieren.

ConfigChange-Hooks werden für Änderungen an Einstellungsdateien, verwalteten Richtlinieneinstellungen und Skill-Dateien ausgelöst. Das Feld `source` in der Eingabe teilt Ihnen mit, welche Art von Konfiguration sich geändert hat, und das optionale Feld `file_path` gibt den Pfad zur geänderten Datei an.

Der Matcher filtert auf die Konfigurationsquelle:

| Matcher            | Wann es ausgelöst wird                            |
| :----------------- | :------------------------------------------------ |
| `user_settings`    | `~/.claude/settings.json` ändert sich             |
| `project_settings` | `.claude/settings.json` ändert sich               |
| `local_settings`   | `.claude/settings.local.json` ändert sich         |
| `policy_settings`  | Verwaltete Richtlinieneinstellungen ändern sich   |
| `skills`           | Eine Skill-Datei in `.claude/skills/` ändert sich |

Dieses Beispiel protokolliert alle Konfigurationsänderungen für Sicherheitsaudits:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### ConfigChange-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten ConfigChange-Hooks `source` und optional `file_path`. Das Feld `source` gibt an, welche Konfigurationsart sich geändert hat, und `file_path` gibt den Pfad zur spezifischen Datei an, die geändert wurde.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange-Entscheidungskontrolle

ConfigChange-Hooks können Konfigurationsänderungen von der Anwendung blockieren. Verwenden Sie Exit-Code 2 oder ein JSON `decision`, um die Änderung zu verhindern. Wenn blockiert, werden die neuen Einstellungen nicht auf die laufende Sitzung angewendet.

| Feld       | Beschreibung                                                                                         |
| :--------- | :--------------------------------------------------------------------------------------------------- |
| `decision` | `"block"` verhindert die Anwendung der Konfigurationsänderung. Weglassen, um die Änderung zuzulassen |
| `reason`   | Erklärung, die dem Benutzer angezeigt wird, wenn `decision` `"block"` ist                            |

```json  theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings`-Änderungen können nicht blockiert werden. Hooks werden immer noch für `policy_settings`-Quellen ausgelöst, daher können Sie sie für Audit-Protokollierung verwenden, aber jede Blockierungsentscheidung wird ignoriert. Dies stellt sicher, dass von Unternehmen verwaltete Einstellungen immer wirksam werden.

### WorktreeCreate

Wenn Sie `claude --worktree` ausführen oder ein [Subagent `isolation: "worktree"` verwendet](/de/sub-agents#choose-the-subagent-scope), erstellt Claude Code eine isolierte Arbeitskopie mit `git worktree`. Wenn Sie einen WorktreeCreate-Hook konfigurieren, ersetzt er das Standard-Git-Verhalten und ermöglicht es Ihnen, ein anderes Versionskontrollsystem wie SVN, Perforce oder Mercurial zu verwenden.

Der Hook muss den absoluten Pfad zum erstellten Worktree-Verzeichnis auf stdout ausgeben. Claude Code verwendet diesen Pfad als Arbeitsverzeichnis für die isolierte Sitzung.

Dieses Beispiel erstellt eine SVN-Arbeitskopie und gibt den Pfad aus, damit Claude Code ihn verwenden kann. Ersetzen Sie die Repository-URL durch Ihre eigene:

```json  theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Der Hook liest den Worktree-`name` aus der JSON-Eingabe auf stdin, checkt eine frische Kopie in ein neues Verzeichnis aus und gibt den Verzeichnispath aus. Das `echo` in der letzten Zeile ist das, was Claude Code als Worktree-Pfad liest. Leiten Sie jede andere Ausgabe zu stderr um, damit sie nicht mit dem Pfad interferiert.

#### WorktreeCreate-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten WorktreeCreate-Hooks das Feld `name`. Dies ist eine Slug-Kennung für den neuen Worktree, entweder vom Benutzer angegeben oder automatisch generiert (zum Beispiel `bold-oak-a3f2`).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate-Ausgabe

Der Hook muss den absoluten Pfad zum erstellten Worktree-Verzeichnis auf stdout ausgeben. Wenn der Hook fehlschlägt oder keine Ausgabe erzeugt, schlägt die Worktree-Erstellung mit einem Fehler fehl.

WorktreeCreate-Hooks verwenden nicht das Standard-Allow/Block-Entscheidungsmodell. Stattdessen bestimmt der Erfolg oder Misserfolg des Hooks das Ergebnis. Nur `type: "command"`-Hooks werden unterstützt.

### WorktreeRemove

Das Bereinigungspendant zu [WorktreeCreate](#worktreecreate). Dieser Hook wird ausgelöst, wenn ein Worktree entfernt wird, entweder wenn Sie eine `--worktree`-Sitzung beenden und wählen, sie zu entfernen, oder wenn ein Subagent mit `isolation: "worktree"` fertig ist. Für Git-basierte Worktrees handhabt Claude die Bereinigung automatisch mit `git worktree remove`. Wenn Sie einen WorktreeCreate-Hook für ein nicht-Git-Versionskontrollsystem konfiguriert haben, koppeln Sie ihn mit einem WorktreeRemove-Hook, um die Bereinigung zu handhaben. Ohne einen wird das Worktree-Verzeichnis auf der Festplatte belassen.

Claude Code übergibt den Pfad, den WorktreeCreate auf stdout ausgegeben hat, als `worktree_path` in der Hook-Eingabe. Dieses Beispiel liest diesen Pfad und entfernt das Verzeichnis:

```json  theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### WorktreeRemove-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten WorktreeRemove-Hooks das Feld `worktree_path`, das der absolute Pfad zum entfernten Worktree ist.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove-Hooks haben keine Entscheidungskontrolle. Sie können die Worktree-Entfernung nicht blockieren, können aber Bereinigungsaufgaben wie das Entfernen von Versionskontrollstatus oder das Archivieren von Änderungen durchführen. Hook-Fehler werden nur im Debug-Modus protokolliert. Nur `type: "command"`-Hooks werden unterstützt.

### PreCompact

Wird ausgeführt, bevor Claude Code einen Komprimierungsvorgang ausführen soll.

Der Matcher-Wert gibt an, ob die Komprimierung manuell oder automatisch ausgelöst wurde:

| Matcher  | Wann es ausgelöst wird                               |
| :------- | :--------------------------------------------------- |
| `manual` | `/compact`                                           |
| `auto`   | Auto-Komprimierung, wenn das Kontextfenster voll ist |

#### PreCompact-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten PreCompact-Hooks `trigger` und `custom_instructions`. Für `manual` enthält `custom_instructions` das, was der Benutzer in `/compact` übergibt. Für `auto` ist `custom_instructions` leer.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

Wird ausgeführt, nachdem Claude Code einen Komprimierungsvorgang abgeschlossen hat. Verwenden Sie dieses Ereignis, um auf den neuen komprimierten Zustand zu reagieren, zum Beispiel um die generierte Zusammenfassung zu protokollieren oder den externen Zustand zu aktualisieren.

Die gleichen Matcher-Werte gelten wie für `PreCompact`:

| Matcher  | Wann es ausgelöst wird                                    |
| :------- | :-------------------------------------------------------- |
| `manual` | Nach `/compact`                                           |
| `auto`   | Nach Auto-Komprimierung, wenn das Kontextfenster voll ist |

#### PostCompact-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten PostCompact-Hooks `trigger` und `compact_summary`. Das Feld `compact_summary` enthält die Gesprächszusammenfassung, die durch den Komprimierungsvorgang generiert wurde.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact-Hooks haben keine Entscheidungskontrolle. Sie können das Komprimierungsergebnis nicht beeinflussen, können aber Folgaufgaben durchführen.

### SessionEnd

Wird ausgeführt, wenn eine Claude Code-Sitzung endet. Nützlich für Bereinigungsaufgaben, Protokollierung von Sitzungsstatistiken oder Speicherung des Sitzungsstatus. Unterstützt Matcher zum Filtern nach Ausstiegsgrund.

Das Feld `reason` in der Hook-Eingabe gibt an, warum die Sitzung endete:

| Grund                         | Beschreibung                                                  |
| :---------------------------- | :------------------------------------------------------------ |
| `clear`                       | Sitzung mit `/clear`-Befehl gelöscht                          |
| `resume`                      | Sitzung über interaktives `/resume` gewechselt                |
| `logout`                      | Benutzer hat sich abgemeldet                                  |
| `prompt_input_exit`           | Benutzer hat beendet, während die Prompt-Eingabe sichtbar war |
| `bypass_permissions_disabled` | Bypass-Berechtigungsmodus wurde deaktiviert                   |
| `other`                       | Andere Ausstiegsgründe                                        |

#### SessionEnd-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten SessionEnd-Hooks ein Feld `reason`, das angibt, warum die Sitzung endete. Siehe die [Grundtabelle](#sessionend) oben für alle Werte.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd-Hooks haben keine Entscheidungskontrolle. Sie können die Sitzungsbeendigung nicht blockieren, können aber Bereinigungsaufgaben durchführen.

SessionEnd-Hooks haben ein Standard-Timeout von 1,5 Sekunden. Dies gilt sowohl für den Sitzungsausstieg als auch für `/clear` und das Wechseln von Sitzungen über interaktives `/resume`. Wenn Ihre Hooks mehr Zeit benötigen, setzen Sie die Umgebungsvariable `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` auf einen höheren Wert in Millisekunden. Jede Pro-Hook-Einstellung `timeout` wird auch durch diesen Wert begrenzt.

```bash  theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

Wird ausgeführt, wenn ein MCP-Server Benutzereingaben während einer Aufgabe anfordert. Standardmäßig zeigt Claude Code einen interaktiven Dialog für die Benutzerantwort an. Hooks können diese Anfrage abfangen und programmatisch antworten, wodurch der Dialog vollständig übersprungen wird.

Das Matcher-Feld passt auf den MCP-Server-Namen.

#### Elicitation-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten Elicitation-Hooks `mcp_server_name`, `message` und optionale Felder `mode`, `url`, `elicitation_id` und `requested_schema`.

Für Form-Mode-Elicitation (der häufigste Fall):

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

Für URL-Mode-Elicitation (Browser-basierte Authentifizierung):

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Elicitation-Ausgabe

Um programmatisch ohne Anzeige des Dialogs zu antworten, geben Sie ein JSON-Objekt mit `hookSpecificOutput` zurück:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| Feld      | Werte                         | Beschreibung                                                                     |
| :-------- | :---------------------------- | :------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Ob die Anfrage akzeptiert, abgelehnt oder abgebrochen werden soll                |
| `content` | Objekt                        | Formularfeldwerte zum Einreichen. Wird nur verwendet, wenn `action` `accept` ist |

Exit-Code 2 verweigert die Elicitation und zeigt stderr dem Benutzer an.

### ElicitationResult

Wird ausgeführt, nachdem ein Benutzer auf eine MCP-Elicitation antwortet. Hooks können die Antwort beobachten, ändern oder blockieren, bevor sie an den MCP-Server zurückgesendet wird.

Das Matcher-Feld passt auf den MCP-Server-Namen.

#### ElicitationResult-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten ElicitationResult-Hooks `mcp_server_name`, `action` und optionale Felder `mode`, `elicitation_id` und `content`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### ElicitationResult-Ausgabe

Um die Antwort des Benutzers zu überschreiben, geben Sie ein JSON-Objekt mit `hookSpecificOutput` zurück:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| Feld      | Werte                         | Beschreibung                                                                   |
| :-------- | :---------------------------- | :----------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Überschreibt die Aktion des Benutzers                                          |
| `content` | Objekt                        | Überschreibt Formularfeldwerte. Nur aussagekräftig, wenn `action` `accept` ist |

Exit-Code 2 blockiert die Antwort und ändert die effektive Aktion in `decline`.

## Prompt-basierte Hooks

Zusätzlich zu Command- und HTTP-Hooks unterstützt Claude Code Prompt-basierte Hooks (`type: "prompt"`), die ein LLM verwenden, um zu evaluieren, ob eine Aktion zuzulassen oder zu blockieren ist, und Agent-Hooks (`type: "agent"`), die einen agentengesteuerten Verifizierer mit Tool-Zugriff spawnen. Nicht alle Ereignisse unterstützen jeden Hook-Typ.

Ereignisse, die alle vier Hook-Typen unterstützen (`command`, `http`, `prompt` und `agent`):

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `UserPromptSubmit`

Ereignisse, die nur `type: "command"`-Hooks unterstützen:

* `ConfigChange`
* `Elicitation`
* `ElicitationResult`
* `InstructionsLoaded`
* `Notification`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `SessionStart`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

### Wie Prompt-basierte Hooks funktionieren

Anstatt einen Bash-Befehl auszuführen, Prompt-basierte Hooks:

1. Senden die Hook-Eingabe und Ihren Prompt an ein Claude-Modell, standardmäßig Haiku
2. Das LLM antwortet mit strukturiertem JSON, das eine Entscheidung enthält
3. Claude Code verarbeitet die Entscheidung automatisch

### Prompt-Hook-Konfiguration

Setzen Sie `type` auf `"prompt"` und geben Sie eine `prompt`-Zeichenkette anstelle eines `command` an. Verwenden Sie den Platzhalter `$ARGUMENTS`, um die Hook-Eingabedaten in Ihren Prompt-Text einzufügen. Claude Code sendet den kombinierten Prompt und die Eingabe an ein schnelles Claude-Modell, das eine JSON-Entscheidung zurückgibt.

Dieser `Stop`-Hook fragt das LLM, ob Claude stoppen sollte:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Feld      | Erforderlich | Beschreibung                                                                                                                                                                                      |
| :-------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`    | ja           | Muss `"prompt"` sein                                                                                                                                                                              |
| `prompt`  | ja           | Der Prompt-Text zum Senden an das LLM. Verwenden Sie `$ARGUMENTS` als Platzhalter für die Hook-Eingabe JSON. Wenn `$ARGUMENTS` nicht vorhanden ist, wird die Eingabe JSON an den Prompt angehängt |
| `model`   | nein         | Modell zur Verwendung für die Evaluierung. Standardwert ist ein schnelles Modell                                                                                                                  |
| `timeout` | nein         | Timeout in Sekunden. Standard: 30                                                                                                                                                                 |

### Response-Schema

Das LLM muss mit JSON antworten, das Folgendes enthält:

```json  theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Feld     | Beschreibung                                                              |
| :------- | :------------------------------------------------------------------------ |
| `ok`     | `true` erlaubt die Aktion, `false` verhindert sie                         |
| `reason` | Erforderlich, wenn `ok` `false` ist. Erklärung, die Claude angezeigt wird |

### Beispiel: Multi-Kriterien-Stop-Hook

Dieser `Stop`-Hook verwendet einen detaillierten Prompt, um drei Bedingungen zu überprüfen, bevor Claude stoppen darf. Wenn `"ok"` `false` ist, setzt Claude die Arbeit mit dem bereitgestellten Grund als nächste Anweisung fort. `SubagentStop`-Hooks verwenden das gleiche Format, um zu evaluieren, ob ein [Subagent](/de/sub-agents) stoppen sollte:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Agent-basierte Hooks

Agent-basierte Hooks (`type: "agent"`) sind wie Prompt-basierte Hooks, aber mit Multi-Turn-Tool-Zugriff. Anstelle eines einzelnen LLM-Aufrufs spawnt ein Agent-Hook einen Subagenten, der Dateien lesen, Code durchsuchen und die Codebasis überprüfen kann, um Bedingungen zu überprüfen. Agent-Hooks unterstützen die gleichen Ereignisse wie Prompt-basierte Hooks.

### Wie Agent-Hooks funktionieren

Wenn ein Agent-Hook ausgelöst wird:

1. Claude Code spawnt einen Subagenten mit Ihrem Prompt und der Hook-Eingabe
2. Der Subagent kann Tools wie Read, Grep und Glob verwenden, um zu untersuchen
3. Nach bis zu 50 Turns gibt der Subagent eine strukturierte `{ "ok": true/false }`-Entscheidung zurück
4. Claude Code verarbeitet die Entscheidung auf die gleiche Weise wie ein Prompt-Hook

Agent-Hooks sind nützlich, wenn die Überprüfung das Überprüfen tatsächlicher Dateien oder Test-Ausgabe erfordert, nicht nur die Evaluierung der Hook-Eingabedaten allein.

### Agent-Hook-Konfiguration

Setzen Sie `type` auf `"agent"` und geben Sie eine `prompt`-Zeichenkette an. Die Konfigurationsfelder sind die gleichen wie [Prompt-Hooks](#prompt-hook-configuration), mit einem längeren Standard-Timeout:

| Feld      | Erforderlich | Beschreibung                                                                                                        |
| :-------- | :----------- | :------------------------------------------------------------------------------------------------------------------ |
| `type`    | ja           | Muss `"agent"` sein                                                                                                 |
| `prompt`  | ja           | Prompt, der beschreibt, was zu überprüfen ist. Verwenden Sie `$ARGUMENTS` als Platzhalter für die Hook-Eingabe JSON |
| `model`   | nein         | Modell zur Verwendung. Standardwert ist ein schnelles Modell                                                        |
| `timeout` | nein         | Timeout in Sekunden. Standard: 60                                                                                   |

Das Response-Schema ist das gleiche wie Prompt-Hooks: `{ "ok": true }` zum Zulassen oder `{ "ok": false, "reason": "..." }` zum Blockieren.

Dieser `Stop`-Hook überprüft, dass alle Unit-Tests bestanden sind, bevor Claude fertig ist:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## Hooks im Hintergrund ausführen

Standardmäßig blockieren Hooks die Ausführung von Claude, bis sie abgeschlossen sind. Für lang laufende Aufgaben wie Bereitstellungen, Test-Suites oder externe API-Aufrufe setzen Sie `"async": true`, um den Hook im Hintergrund auszuführen, während Claude weiterarbeitet. Asynchrone Hooks können nicht blockieren oder das Verhalten von Claude steuern: Response-Felder wie `decision`, `permissionDecision` und `continue` haben keine Auswirkung, da die Aktion, die sie steuern würden, bereits abgeschlossen ist.

### Konfigurieren Sie einen asynchronen Hook

Fügen Sie `"async": true` zur Konfiguration eines Command-Hooks hinzu, um ihn im Hintergrund auszuführen, ohne Claude zu blockieren. Dieses Feld ist nur auf `type: "command"`-Hooks verfügbar.

Dieser Hook führt ein Test-Skript nach jedem `Write`-Tool-Aufruf aus. Claude arbeitet sofort weiter, während `run-tests.sh` bis zu 120 Sekunden ausgeführt wird. Wenn das Skript fertig ist, wird seine Ausgabe beim nächsten Gesprächsturn geliefert:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Das Feld `timeout` setzt die maximale Zeit in Sekunden für den Hintergrund-Prozess. Wenn nicht angegeben, verwenden asynchrone Hooks das gleiche 10-Minuten-Standard wie synchrone Hooks.

### Wie asynchrone Hooks ausgeführt werden

Wenn ein asynchroner Hook ausgelöst wird, startet Claude Code den Hook-Prozess und setzt sofort fort, ohne auf den Abschluss zu warten. Der Hook erhält die gleiche JSON-Eingabe über stdin wie ein synchroner Hook.

Nachdem der Hintergrund-Prozess beendet ist, wenn der Hook eine JSON-Response mit einem `systemMessage`- oder `additionalContext`-Feld erzeugt hat, wird dieser Inhalt Claude beim nächsten Gesprächsturn als Kontext geliefert.

Benachrichtigungen über den Abschluss asynchroner Hooks werden standardmäßig unterdrückt. Um sie zu sehen, aktivieren Sie den ausführlichen Modus mit `Ctrl+O` oder starten Sie Claude Code mit `--verbose`.

### Beispiel: Tests nach Dateiänderungen ausführen

Dieser Hook startet eine Test-Suite im Hintergrund, wenn Claude eine Datei schreibt, und meldet die Ergebnisse Claude, wenn die Tests fertig sind. Speichern Sie dieses Skript unter `.claude/hooks/run-tests-async.sh` in Ihrem Projekt und machen Sie es mit `chmod +x` ausführbar:

```bash  theme={null}
#!/bin/bash
# run-tests-async.sh

# Hook-Eingabe von stdin lesen
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Tests nur für Quelldateien ausführen
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Tests ausführen und Ergebnisse über systemMessage melden
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Fügen Sie dann diese Konfiguration zu `.claude/settings.json` im Projekt-Root hinzu. Das Flag `async: true` ermöglicht es Claude, weiterarbeiten zu können, während Tests ausgeführt werden:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### Einschränkungen

Asynchrone Hooks haben mehrere Einschränkungen im Vergleich zu synchronen Hooks:

* Nur `type: "command"`-Hooks unterstützen `async`. Prompt-basierte Hooks können nicht asynchron ausgeführt werden.
* Asynchrone Hooks können nicht blockieren oder Entscheidungen zurückgeben. Zu dem Zeitpunkt, an dem der Hook abgeschlossen ist, hat die auslösende Aktion bereits stattgefunden.
* Hook-Ausgabe wird beim nächsten Gesprächsturn geliefert. Wenn die Sitzung untätig ist, wartet die Response, bis die nächste Benutzerinteraktion erfolgt.
* Jede Ausführung erstellt einen separaten Hintergrund-Prozess. Es gibt keine Deduplizierung über mehrere Auslösungen des gleichen asynchronen Hooks.

## Sicherheitsüberlegungen

### Haftungsausschluss

Command-Hooks werden mit den vollständigen Berechtigungen Ihres System-Benutzers ausgeführt.

<Warning>
  Command-Hooks führen Shell-Befehle mit Ihren vollständigen Benutzerberechtigungen aus. Sie können alle Dateien ändern, löschen oder zugreifen, auf die Ihr Benutzerkonto zugreifen kann. Überprüfen und testen Sie alle Hook-Befehle, bevor Sie sie zu Ihrer Konfiguration hinzufügen.
</Warning>

### Best Practices für Sicherheit

Beachten Sie diese Praktiken beim Schreiben von Hooks:

* **Validieren und bereinigen Sie Eingaben**: Vertrauen Sie niemals blind auf Eingabedaten
* **Zitieren Sie immer Shell-Variablen**: Verwenden Sie `"$VAR"` nicht `$VAR`
* **Blockieren Sie Pfad-Traversal**: Prüfen Sie auf `..` in Dateipfaden
* **Verwenden Sie absolute Pfade**: Geben Sie vollständige Pfade für Skripte an, verwenden Sie `"$CLAUDE_PROJECT_DIR"` für das Projekt-Root
* **Überspringen Sie sensible Dateien**: Vermeiden Sie `.env`, `.git/`, Schlüssel, etc.

## Debug-Hooks

Führen Sie `claude --debug` aus, um Hook-Ausführungsdetails zu sehen, einschließlich welche Hooks passten, ihre Exit-Codes und Ausgabe. Schalten Sie den ausführlichen Modus mit `Ctrl+O` um, um Hook-Fortschritt im Transkript zu sehen.

```text  theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Zur Fehlerbehebung häufiger Probleme wie Hooks, die nicht ausgelöst werden, unendliche Stop-Hook-Schleifen oder Konfigurationsfehler, siehe [Einschränkungen und Fehlerbehebung](/de/hooks-guide#limitations-and-troubleshooting) in der Anleitung.
