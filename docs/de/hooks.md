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

Hooks werden an bestimmten Punkten während einer Claude Code-Sitzung ausgelöst. Wenn ein Ereignis ausgelöst wird und ein Matcher passt, übergibt Claude Code JSON-Kontext über das Ereignis an Ihren Hook-Handler. Für Command-Hooks kommt die Eingabe über stdin an. Für HTTP-Hooks kommt sie als POST-Request-Body an. Ihr Handler kann dann die Eingabe überprüfen, Maßnahmen ergreifen und optional eine Entscheidung zurückgeben. Ereignisse fallen in drei Rhythmen: einmal pro Sitzung (`SessionStart`, `SessionEnd`), einmal pro Runde (`UserPromptSubmit`, `Stop`, `StopFailure`) und bei jedem Tool-Aufruf innerhalb der agentengesteuerten Schleife (`PreToolUse`, `PostToolUse`):

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/ZIW26Z9pnpsXLhbS/images/hooks-lifecycle.svg?fit=max&auto=format&n=ZIW26Z9pnpsXLhbS&q=85&s=ee23691324deb6501df09bfdae560b64" alt="Hook-Lebenszyklus-Diagramm, das optionales Setup zeigt, das in SessionStart führt, dann eine Pro-Runde-Schleife mit UserPromptSubmit, UserPromptExpansion für Slash-Befehle, die verschachtelte agentengesteuerte Schleife (PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart/Stop, TaskCreated, TaskCompleted) und Stop oder StopFailure, gefolgt von TeammateIdle, PreCompact, PostCompact und SessionEnd, mit Elicitation und ElicitationResult verschachtelt in MCP-Tool-Ausführung, PermissionDenied als Seitenzweig von PermissionRequest für Auto-Mode-Ablehnungen und WorktreeCreate, WorktreeRemove, Notification, ConfigChange, InstructionsLoaded, CwdChanged und FileChanged als eigenständige asynchrone Ereignisse" width="520" height="1228" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

Die folgende Tabelle fasst zusammen, wann jedes Ereignis ausgelöst wird. Der Abschnitt [Hook-Ereignisse](#hook-events) dokumentiert das vollständige Eingabeschema und die Optionen zur Entscheidungskontrolle für jedes Ereignis.

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

### Wie ein Hook aufgelöst wird

Um zu sehen, wie diese Teile zusammenpassen, betrachten Sie diesen `PreToolUse`-Hook, der destruktive Shell-Befehle blockiert. Der `matcher` grenzt auf Bash-Tool-Aufrufe ein und die `if`-Bedingung grenzt weiter auf Bash-Unterbefehle ein, die mit `rm *` übereinstimmen, daher wird `block-rm.sh` nur ausgeführt, wenn beide Filter passen:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

Das Skript liest die JSON-Eingabe von stdin, extrahiert den Befehl und gibt eine `permissionDecision` von `"deny"` zurück, wenn es `rm -rf` enthält:

```bash theme={null}
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
  <img src="https://mintcdn.com/claude-code/-tYw1BD_DEqfyyOZ/images/hook-resolution.svg?fit=max&auto=format&n=-tYw1BD_DEqfyyOZ&q=85&s=c73ebc1eeda2037570427d7af1e0a891" alt="Hook-Auflösungsfluss: PreToolUse-Ereignis wird ausgelöst, Matcher prüft auf Bash-Übereinstimmung, if-Bedingung prüft auf Bash(rm *)-Übereinstimmung, Hook-Handler wird ausgeführt, Ergebnis wird an Claude Code zurückgegeben" width="930" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Ereignis wird ausgelöst">
    Das `PreToolUse`-Ereignis wird ausgelöst. Claude Code sendet die Tool-Eingabe als JSON über stdin an den Hook:

    ```json theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="Matcher prüft">
    Der Matcher `"Bash"` passt zum Tool-Namen, daher wird diese Hook-Gruppe aktiviert. Wenn Sie den Matcher weglassen oder `"*"` verwenden, wird die Gruppe bei jedem Auftreten des Ereignisses aktiviert.
  </Step>

  <Step title="If-Bedingung prüft">
    Die `if`-Bedingung `"Bash(rm *)"` passt, weil `rm -rf /tmp/build` ein Unterbefehl ist, der mit `rm *` übereinstimmt, daher wird dieser Handler ausgeführt. Wenn der Befehl `npm test` gewesen wäre, würde die `if`-Prüfung fehlschlagen und `block-rm.sh` würde nie ausgeführt, wodurch der Prozess-Spawn-Overhead vermieden wird. Das Feld `if` ist optional; ohne es wird jeder Handler in der passenden Gruppe ausgeführt.
  </Step>

  <Step title="Hook-Handler wird ausgeführt">
    Das Skript überprüft den vollständigen Befehl und findet `rm -rf`, daher gibt es eine Entscheidung auf stdout aus:

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Wenn der Befehl eine sicherere `rm`-Variante gewesen wäre, wie `rm file.txt`, würde das Skript stattdessen `exit 0` treffen, was Claude Code mitteilt, den Tool-Aufruf zuzulassen, ohne weitere Maßnahmen zu ergreifen.
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
  Diese Seite verwendet spezifische Begriffe für jede Ebene: **Hook-Ereignis** für den Lebenszyklus-Punkt, **Matcher-Gruppe** für den Filter und **Hook-Handler** für den Shell-Befehl, HTTP-Endpunkt, MCP-Tool, Prompt oder Agent, der ausgeführt wird. „Hook" allein bezieht sich auf die allgemeine Funktion.
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

Weitere Informationen zur Auflösung von Einstellungsdateien finden Sie unter [Einstellungen](/de/settings). Enterprise-Administratoren können `allowManagedHooksOnly` verwenden, um Benutzer-, Projekt- und Plugin-Hooks zu blockieren. Hooks von Plugins, die in verwalteten Einstellungen `enabledPlugins` erzwungen aktiviert sind, sind ausgenommen, daher können Administratoren überprüfte Hooks über einen Organisations-Marketplace verteilen. Siehe [Hook-Konfiguration](/de/settings#hook-configuration).

### Matcher-Muster

Das Feld `matcher` filtert, wann Hooks ausgelöst werden. Wie ein Matcher evaluiert wird, hängt von den Zeichen ab, die er enthält:

| Matcher-Wert                          | Evaluiert als                                                           | Beispiel                                                                                                             |
| :------------------------------------ | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| `"*"`, `""` oder weggelassen          | Alle treffen                                                            | wird bei jedem Auftreten des Ereignisses ausgelöst                                                                   |
| Nur Buchstaben, Ziffern, `_` und `\|` | Exakte Zeichenkette oder `\|`-getrennte Liste von exakten Zeichenketten | `Bash` passt nur zum Bash-Tool; `Edit\|Write` passt zu beiden Tools genau                                            |
| Enthält ein anderes Zeichen           | JavaScript-Regex                                                        | `^Notebook` passt zu jedem Tool, das mit Notebook beginnt; `mcp__memory__.*` passt zu jedem Tool vom `memory`-Server |

Das Ereignis `FileChanged` folgt diesen Regeln nicht, wenn es seine Überwachungsliste erstellt. Siehe [FileChanged](#filechanged).

Jeder Ereignistyp passt auf ein anderes Feld:

| Ereignis                                                                                                                        | Worauf der Matcher filtert                                    | Beispiel-Matcher-Werte                                                                                                                             |
| :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`                                      | Tool-Name                                                     | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                                                   |
| `SessionStart`                                                                                                                  | Wie die Sitzung gestartet wurde                               | `startup`, `resume`, `clear`, `compact`                                                                                                            |
| `Setup`                                                                                                                         | Welches CLI-Flag das Setup ausgelöst hat                      | `init`, `maintenance`                                                                                                                              |
| `SessionEnd`                                                                                                                    | Warum die Sitzung endete                                      | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                                           |
| `Notification`                                                                                                                  | Benachrichtigungstyp                                          | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`                           |
| `SubagentStart`                                                                                                                 | Agent-Typ                                                     | `general-purpose`, `Explore`, `Plan` oder benutzerdefinierte Agent-Namen                                                                           |
| `PreCompact`, `PostCompact`                                                                                                     | Was die Komprimierung ausgelöst hat                           | `manual`, `auto`                                                                                                                                   |
| `SubagentStop`                                                                                                                  | Agent-Typ                                                     | gleiche Werte wie `SubagentStart`                                                                                                                  |
| `ConfigChange`                                                                                                                  | Konfigurationsquelle                                          | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                                                 |
| `CwdChanged`                                                                                                                    | Keine Matcher-Unterstützung                                   | wird immer bei jedem Verzeichniswechsel ausgelöst                                                                                                  |
| `FileChanged`                                                                                                                   | Dateinamen zum Überwachen (siehe [FileChanged](#filechanged)) | `.envrc\|.env`                                                                                                                                     |
| `StopFailure`                                                                                                                   | Fehlertyp                                                     | `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                                            | Ladegrund                                                     | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                                                       |
| `UserPromptExpansion`                                                                                                           | Befehlsname                                                   | Ihre Skill- oder Befehlsnamen                                                                                                                      |
| `Elicitation`                                                                                                                   | MCP-Server-Name                                               | Ihre konfigurierten MCP-Server-Namen                                                                                                               |
| `ElicitationResult`                                                                                                             | MCP-Server-Name                                               | gleiche Werte wie `Elicitation`                                                                                                                    |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | Keine Matcher-Unterstützung                                   | wird immer bei jedem Auftreten ausgelöst                                                                                                           |

Der Matcher wird gegen ein Feld aus der [JSON-Eingabe](#hook-input-and-output) ausgeführt, die Claude Code an Ihren Hook über stdin sendet. Für Tool-Ereignisse ist dieses Feld `tool_name`. Jeder Abschnitt [Hook-Ereignis](#hook-events) listet den vollständigen Satz von Matcher-Werten und das Eingabeschema für dieses Ereignis auf.

Dieses Beispiel führt ein Linting-Skript nur aus, wenn Claude eine Datei schreibt oder bearbeitet:

```json theme={null}
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

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` und `CwdChanged` unterstützen keine Matcher und werden immer bei jedem Auftreten ausgelöst. Wenn Sie ein `matcher`-Feld zu diesen Ereignissen hinzufügen, wird es stillschweigend ignoriert.

Für Tool-Ereignisse können Sie enger filtern, indem Sie das Feld [`if`](#common-fields) auf einzelnen Hook-Handlern setzen. `if` verwendet [Berechtigungsregel-Syntax](/de/permissions), um gegen den Tool-Namen und die Argumente zusammen zu passen, daher wird `"Bash(git *)"` ausgeführt, wenn ein Bash-Befehl mit `git *` übereinstimmt und `"Edit(*.ts)"` wird nur für TypeScript-Dateien ausgeführt.

#### MCP-Tools abgleichen

[MCP](/de/mcp) Server-Tools erscheinen als reguläre Tools in Tool-Ereignissen (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), daher können Sie sie auf die gleiche Weise abgleichen wie jeden anderen Tool-Namen.

MCP-Tools folgen dem Benennungsmuster `mcp__<server>__<tool>`, zum Beispiel:

* `mcp__memory__create_entities`: Memory-Server-Tool zum Erstellen von Entitäten
* `mcp__filesystem__read_file`: Filesystem-Server-Tool zum Lesen von Dateien
* `mcp__github__search_repositories`: GitHub-Server-Suchtool

Um jedes Tool von einem Server zu treffen, fügen Sie `.*` zum Server-Präfix hinzu. Das `.*` ist erforderlich: Ein Matcher wie `mcp__memory` enthält nur Buchstaben und Unterstriche, daher wird er als exakte Zeichenkette verglichen und passt zu keinem Tool.

* `mcp__memory__.*` passt zu allen Tools vom `memory`-Server
* `mcp__.*__write.*` passt zu jedem Tool, dessen Name mit `write` beginnt, von jedem Server

Dieses Beispiel protokolliert alle Memory-Server-Operationen und validiert Schreibvorgänge von jedem MCP-Server:

```json theme={null}
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

Jedes Objekt im inneren `hooks`-Array ist ein Hook-Handler: der Shell-Befehl, HTTP-Endpunkt, MCP-Tool, LLM-Prompt oder Agent, der ausgeführt wird, wenn der Matcher passt. Es gibt fünf Typen:

* **[Command-Hooks](#command-hook-fields)** (`type: "command"`): führen einen Shell-Befehl aus. Ihr Skript erhält die [JSON-Eingabe](#hook-input-and-output) des Ereignisses über stdin und kommuniziert Ergebnisse über Exit-Codes und stdout zurück.
* **[HTTP-Hooks](#http-hook-fields)** (`type: "http"`): senden die [JSON-Eingabe](#hook-input-and-output) des Ereignisses als HTTP-POST-Request an eine URL. Der Endpunkt kommuniziert Ergebnisse über den Response-Body mit dem gleichen [JSON-Ausgabeformat](#json-output) wie Command-Hooks zurück.
* **[MCP-Tool-Hooks](#mcp-tool-hook-fields)** (`type: "mcp_tool"`): rufen ein Tool auf einem bereits verbundenen [MCP-Server](/de/mcp) auf. Die Textausgabe des Tools wird wie Command-Hook-stdout behandelt.
* **[Prompt-Hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): senden einen Prompt an ein Claude-Modell für eine Single-Turn-Evaluierung. Das Modell gibt eine Ja/Nein-Entscheidung als JSON zurück. Siehe [Prompt-basierte Hooks](#prompt-based-hooks).
* **[Agent-Hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): spawnen einen Subagenten, der Tools wie Read, Grep und Glob verwenden kann, um Bedingungen zu überprüfen, bevor eine Entscheidung zurückgegeben wird. Agent-Hooks sind experimentell und können sich ändern. Siehe [Agent-basierte Hooks](#agent-based-hooks).

#### Gemeinsame Felder

Diese Felder gelten für alle Hook-Typen:

| Feld            | Erforderlich | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :-------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`          | ja           | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"` oder `"agent"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `if`            | nein         | Berechtigungsregel-Syntax zum Filtern, wann dieser Hook ausgeführt wird, wie `"Bash(git *)"` oder `"Edit(*.ts)"`. Der Hook wird nur ausgeführt, wenn der Tool-Aufruf dem Muster entspricht, oder wenn ein Bash-Befehl zu komplex zum Analysieren ist. Wird nur auf Tool-Ereignisse evaluiert: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` und `PermissionDenied`. Bei anderen Ereignissen wird ein Hook mit `if` gesetzt nie ausgeführt. Verwendet die gleiche Syntax wie [Berechtigungsregeln](/de/permissions) |
| `timeout`       | nein         | Sekunden vor dem Abbruch. Standardwerte: 600 für `command`, `http` und `mcp_tool`; 30 für `prompt`; 60 für `agent`. [`UserPromptSubmit`](#userpromptsubmit) senkt den Standardwert für `command`, `http` und `mcp_tool` auf 30                                                                                                                                                                                                                                                                                                              |
| `statusMessage` | nein         | Benutzerdefinierte Spinner-Nachricht, die angezeigt wird, während der Hook ausgeführt wird                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `once`          | nein         | Wenn `true`, wird nur einmal pro Sitzung ausgeführt und dann entfernt. Nur für Hooks, die in [Skill-Frontmatter](#hooks-in-skills-and-agents) deklariert sind; wird in Einstellungsdateien und Agent-Frontmatter ignoriert                                                                                                                                                                                                                                                                                                                  |

Das Feld `if` enthält genau eine Berechtigungsregel. Es gibt keine `&&`-, `||`- oder List-Syntax zum Kombinieren von Regeln; um mehrere Bedingungen anzuwenden, definieren Sie einen separaten Hook-Handler für jeden. Für Bash wird die Regel gegen jeden Subbefehl der Tool-Eingabe abgeglichen, nachdem führende `VAR=value`-Zuweisungen entfernt wurden, daher passt `if: "Bash(git push *)"` sowohl zu `FOO=bar git push` als auch zu `npm test && git push`. Der Hook wird ausgeführt, wenn ein Subbefehl passt, und wird immer ausgeführt, wenn der Befehl zu komplex zum Analysieren ist.

#### Command-Hook-Felder

Zusätzlich zu den [gemeinsamen Feldern](#common-fields) akzeptieren Command-Hooks diese Felder:

| Feld          | Erforderlich | Beschreibung                                                                                                                                                                                                                                                                                              |
| :------------ | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`     | ja           | Shell-Befehl zum Ausführen. Mit `args` die ausführbare Datei zum direkten Spawnen. Siehe [Exec-Form und Shell-Form](#exec-form-and-shell-form)                                                                                                                                                            |
| `args`        | nein         | Argumentliste. Wenn vorhanden, wird `command` als ausführbare Datei aufgelöst und direkt mit `args` als Argumentvektor gespawnt, ohne Shell. Siehe [Exec-Form und Shell-Form](#exec-form-and-shell-form)                                                                                                  |
| `async`       | nein         | Wenn `true`, wird im Hintergrund ausgeführt, ohne zu blockieren. Siehe [Hooks im Hintergrund ausführen](#run-hooks-in-the-background)                                                                                                                                                                     |
| `asyncRewake` | nein         | Wenn `true`, wird im Hintergrund ausgeführt und weckt Claude bei Exit-Code 2 auf. Impliziert `async`. Der stderr des Hooks oder stdout, wenn stderr leer ist, wird Claude als Systemerinnerung angezeigt, damit es auf einen lang laufenden Hintergrund-Fehler reagieren kann                             |
| `shell`       | nein         | Shell zum Verwenden für diesen Hook. Akzeptiert `"bash"` (Standard) oder `"powershell"`. Das Setzen von `"powershell"` führt den Befehl über PowerShell unter Windows aus. Erfordert nicht `CLAUDE_CODE_USE_POWERSHELL_TOOL`, da Hooks PowerShell direkt spawnen. Wird ignoriert, wenn `args` gesetzt ist |

<a id="exec-form-and-shell-form" />

##### Exec-Form und Shell-Form

Ein Command-Hook wird als Exec-Form ausgeführt, wenn `args` gesetzt ist, und als Shell-Form, wenn `args` weggelassen ist. Setzen Sie `args`, wenn der Hook auf einen [Pfad-Platzhalter](#reference-scripts-by-path) verweist, da jedes Element als ein Argument ohne Anführungszeichen übergeben wird. Lassen Sie `args` weg, wenn Sie Shell-Funktionen wie Pipes oder `&&` benötigen, oder wenn keine dieser Bedenken zutrifft.

**Exec-Form** wird ausgeführt, wenn `args` vorhanden ist. Claude Code löst `command` als ausführbare Datei auf `PATH` auf und spawnt sie direkt mit `args` als Argumentvektor. Es gibt keine Shell, daher ist jedes `args`-Element genau ein Argument, wie geschrieben, und Pfad-Platzhalter wie `${CLAUDE_PLUGIN_ROOT}` werden als einfache Zeichenketten in `command` und in jedes `args`-Element ersetzt. Sonderzeichen wie Apostrophe, `$` und Backticks werden wörtlich durchgeleitet, da es keine Shell gibt, die sie interpretiert. Auf keiner Plattform findet Shell-Tokenisierung statt.

**Shell-Form** wird ausgeführt, wenn `args` fehlt. Die `command`-Zeichenkette wird an eine Shell übergeben: `sh -c` auf macOS und Linux, Git Bash unter Windows oder PowerShell, wenn Git Bash nicht installiert ist. Setzen Sie das Feld `shell`, um explizit zu wählen. Die Shell tokenisiert die Zeichenkette, erweitert Variablen und interpretiert Pipes, `&&`, Umleitungen und Globs.

<Note>
  Unter Windows erfordert die Exec-Form, dass `command` zu einer echten ausführbaren Datei wie `.exe` aufgelöst wird. Die `.cmd` und `.bat` Shims, die npm, npx, eslint und andere Tools in `node_modules/.bin` installieren, sind keine ausführbaren Dateien und können ohne Shell nicht gespawnt werden. Um sie in Exec-Form auszuführen, rufen Sie das zugrunde liegende Skript direkt mit `node` auf, zum Beispiel `"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/node_modules/eslint/bin/eslint.js"]`. Das `node` plus Skript-Pfad-Muster funktioniert auf jeder Plattform, da `node.exe` eine echte Binärdatei ist. Um einen `.cmd` oder `.bat` Shim nach Name auszuführen, verwenden Sie Shell-Form.
</Note>

Dieses Beispiel führt ein Node-Skript aus, das mit einem Plugin gebündelt ist. Exec-Form übergibt den aufgelösten Skript-Pfad als ein Argument ohne Anführungszeichen:

```json theme={null}
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]
}
```

Die äquivalente Shell-Form benötigt Anführungszeichen, um Pfade mit Leerzeichen oder Sonderzeichen zu handhaben:

```json theme={null}
{
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"
}
```

Beide Formen unterstützen die gleichen [Pfad-Platzhalter](#reference-scripts-by-path), und beide exportieren sie als Umgebungsvariablen `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT` und `CLAUDE_PLUGIN_DATA` auf dem gespawnten Prozess, daher kann ein Skript `process.env.CLAUDE_PLUGIN_ROOT` lesen, unabhängig davon, wie es gestartet wurde. Plugin-Hooks ersetzen zusätzlich `${user_config.*}` Werte; siehe [Benutzerkonfiguration](/de/plugins-reference#user-configuration).

<Note>
  In Exec-Form ist `command` nur der ausführbare Name oder Pfad. Wenn `command` ein bloßer Name ohne Pfad-Trennzeichen ist und Leerzeichen neben `args` enthält, protokolliert Claude Code eine Warnung, da das Spawn fehlschlagen wird: Es gibt keine ausführbare Datei namens `node script.js`. Verschieben Sie die zusätzlichen Token in `args`. Absolute Pfade mit Leerzeichen, wie `C:\Program Files\nodejs\node.exe`, sind eine einzelne gültige ausführbare Datei und lösen die Warnung nicht aus.
</Note>

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

```json theme={null}
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

#### MCP-Tool-Hook-Felder

Zusätzlich zu den [gemeinsamen Feldern](#common-fields) akzeptieren MCP-Tool-Hooks diese Felder:

| Feld     | Erforderlich | Beschreibung                                                                                                                                                                            |
| :------- | :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `server` | ja           | Name eines konfigurierten MCP-Servers. Der Server muss bereits verbunden sein; der Hook löst niemals einen OAuth- oder Verbindungsfluss aus                                             |
| `tool`   | ja           | Name des Tools, das auf diesem Server aufgerufen werden soll                                                                                                                            |
| `input`  | nein         | Argumente, die an das Tool übergeben werden. String-Werte unterstützen `${path}`-Substitution aus der [JSON-Eingabe](#hook-input-and-output) des Hooks, wie `"${tool_input.file_path}"` |

Die Textausgabe des Tools wird wie Command-Hook-stdout behandelt: Wenn sie als gültige [JSON-Ausgabe](#json-output) geparst wird, wird sie als Entscheidung verarbeitet, andernfalls wird sie als Klartext angezeigt. Wenn der benannte Server nicht verbunden ist oder das Tool `isError: true` zurückgibt, erzeugt der Hook einen nicht-blockierenden Fehler und die Ausführung wird fortgesetzt.

MCP-Tool-Hooks sind auf jedem Hook-Ereignis verfügbar, sobald Claude Code sich mit Ihren MCP-Servern verbunden hat. `SessionStart` und `Setup` werden normalerweise ausgelöst, bevor Server die Verbindung beenden, daher sollten Hooks auf diesen Ereignissen beim ersten Ausführen den Fehler „nicht verbunden" erwarten.

Dieses Beispiel ruft das Tool `security_scan` auf dem MCP-Server `my_server` nach jedem `Write` oder `Edit` auf und übergibt den Pfad der bearbeiteten Datei:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
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

Alle passenden Hooks werden parallel ausgeführt, und identische Handler werden automatisch dedupliziert. Command-Hooks werden nach Befehlszeichenkette und `args` dedupliziert, und HTTP-Hooks werden nach URL dedupliziert. Handler werden im aktuellen Verzeichnis mit der Umgebung von Claude Code ausgeführt. Die Umgebungsvariable `$CLAUDE_CODE_REMOTE` wird in Remote-Web-Umgebungen auf `"true"` gesetzt und ist in der lokalen CLI nicht gesetzt.

### Skripte nach Pfad referenzieren

Verwenden Sie diese Platzhalter, um Hook-Skripte relativ zum Projekt- oder Plugin-Root zu referenzieren, unabhängig vom Arbeitsverzeichnis, wenn der Hook ausgeführt wird:

* `${CLAUDE_PROJECT_DIR}`: das Projekt-Root.
* `${CLAUDE_PLUGIN_ROOT}`: das Installationsverzeichnis des Plugins, für Skripte, die mit einem [Plugin](/de/plugins) gebündelt sind. Ändert sich bei jedem Plugin-Update.
* `${CLAUDE_PLUGIN_DATA}`: das [persistente Datenverzeichnis](/de/plugins-reference#persistent-data-directory) des Plugins, für Abhängigkeiten und Zustand, die Plugin-Updates überstehen sollten.

Bevorzugen Sie [Exec-Form](#exec-form-and-shell-form) für jeden Hook, der auf einen Pfad-Platzhalter verweist. Exec-Form übergibt jedes `args`-Element als ein Argument ohne Shell-Tokenisierung, daher benötigen Pfade mit Leerzeichen oder Sonderzeichen keine Anführungszeichen. In Shell-Form wickeln Sie jeden Platzhalter in doppelte Anführungszeichen ein.

<Tabs>
  <Tab title="Projekt-Skripte">
    Dieses Beispiel verwendet `${CLAUDE_PROJECT_DIR}`, um einen Style-Checker aus dem `.claude/hooks/`-Verzeichnis des Projekts nach jedem `Write`- oder `Edit`-Tool-Aufruf auszuführen:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh",
                "args": []
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

    ```json theme={null}
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
                "args": [],
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

```yaml theme={null}
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

Das Menü zeigt alle fünf Hook-Typen an: `command`, `prompt`, `agent`, `http` und `mcp_tool`. Jeder Hook ist mit einem `[type]`-Präfix und einer Quelle gekennzeichnet, die angibt, wo er definiert wurde:

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

Auf macOS und Linux werden Command-Hooks seit v2.1.139 in ihrer eigenen Sitzung ohne steuerndes Terminal ausgeführt. Der Hook-Prozess und alle untergeordneten Prozesse können `/dev/tty` nicht öffnen oder Escape-Sequenzen direkt an die Claude Code-Benutzeroberfläche senden. Windows hat kein `/dev/tty`. Um eine Nachricht dem Benutzer auf jeder Plattform anzuzeigen, geben Sie [`systemMessage`](#json-output) in der JSON-Ausgabe zurück. Um eine Desktop-Benachrichtigung auszulösen, einen Fenstertitel zu setzen oder die Glocke zu läuten, geben Sie stattdessen [`terminalSequence`](#emit-terminal-notifications) zurück.

### Gemeinsame Eingabefelder

Hook-Ereignisse erhalten diese Felder als JSON, zusätzlich zu ereignisspezifischen Feldern, die in jedem Abschnitt [Hook-Ereignis](#hook-events) dokumentiert sind. Für Command-Hooks kommt diese JSON über stdin an. Für HTTP-Hooks kommt sie als POST-Request-Body an.

| Feld              | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | Aktuelle Sitzungs-ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `transcript_path` | Pfad zur Gesprächs-JSON                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `cwd`             | Aktuelles Arbeitsverzeichnis, wenn der Hook aufgerufen wird                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `permission_mode` | Aktueller [Berechtigungsmodus](/de/permissions#permission-modes): `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` oder `"bypassPermissions"`. Nicht alle Ereignisse erhalten dieses Feld: siehe jedes Ereignis-JSON-Beispiel unten, um zu prüfen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `effort`          | Objekt mit einem `level`-Feld, das die aktive [Anstrengungsstufe](/de/model-config#adjust-effort-level) für den Zug enthält: `"low"`, `"medium"`, `"high"`, `"xhigh"` oder `"max"`. Wenn die angeforderte Anstrengung das überschreitet, was das aktuelle Modell unterstützt, ist dies die herabgestufte Stufe, die das Modell tatsächlich verwendet hat, nicht die Stufe, die Sie angefordert haben. Das Objekt entspricht dem [Statuszeilen](/de/statusline#available-data)-Feld `effort`. Vorhanden für Ereignisse, die innerhalb eines Tool-Use-Kontexts ausgelöst werden, wie `PreToolUse`, `PostToolUse`, `Stop` und `SubagentStop`, wenn das aktuelle Modell den Anstrengungsparameter unterstützt. Die Stufe ist auch für Hook-Befehle und das Bash-Tool als die Umgebungsvariable `$CLAUDE_EFFORT` verfügbar. |
| `hook_event_name` | Name des ausgelösten Ereignisses                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

Wenn mit `--agent` oder innerhalb eines Subagenten ausgeführt, sind zwei zusätzliche Felder enthalten:

| Feld         | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                        |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Eindeutige Kennung für den Subagenten. Nur vorhanden, wenn der Hook innerhalb eines Subagenten-Aufrufs ausgelöst wird. Verwenden Sie dies, um Subagenten-Hook-Aufrufe von Main-Thread-Aufrufen zu unterscheiden.                                                                                                                                                                                    |
| `agent_type` | Agent-Name (zum Beispiel `"Explore"` oder `"security-reviewer"`). Vorhanden, wenn die Sitzung `--agent` verwendet oder der Hook innerhalb eines Subagenten ausgelöst wird. Für Subagenten hat der Typ des Subagenten Vorrang vor dem `--agent`-Wert der Sitzung. Für [benutzerdefinierte Subagenten](/de/sub-agents) ist dies das `name`-Feld aus dem Frontmatter des Agenten, nicht der Dateiname. |

Nur [`SessionStart`](#sessionstart)-Hooks erhalten ein `model`-Feld. Es gibt keine `$CLAUDE_MODEL`-Umgebungsvariable. Ein Hook-Prozess erbt die übergeordnete Umgebung, sodass er `$ANTHROPIC_MODEL` lesen kann, wenn Sie sie in Ihrer Shell setzen, aber dieser Wert ändert sich nicht, wenn Sie während einer Sitzung mit `/model` Modelle wechseln.

Zum Beispiel erhält ein `PreToolUse`-Hook für einen Bash-Befehl dies über stdin:

```json theme={null}
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

**Exit 0** bedeutet Erfolg. Claude Code analysiert stdout auf [JSON-Ausgabefelder](#json-output). JSON-Ausgabe wird nur bei Exit 0 verarbeitet. Für die meisten Ereignisse wird stdout in das Debug-Log geschrieben, aber nicht im Transkript angezeigt. Die Ausnahmen sind `UserPromptSubmit`, `UserPromptExpansion` und `SessionStart`, wo stdout als Kontext hinzugefügt wird, den Claude sehen und darauf reagieren kann.

**Exit 2** bedeutet ein blockierender Fehler. Claude Code ignoriert stdout und jede JSON darin. Stattdessen wird der stderr-Text an Claude als Fehlermeldung zurückgegeben. Die Auswirkung hängt vom Ereignis ab: `PreToolUse` blockiert den Tool-Aufruf, `UserPromptSubmit` lehnt den Prompt ab, und so weiter. Siehe [Exit-Code-2-Verhalten pro Ereignis](#exit-code-2-behavior-per-event) für die vollständige Liste.

**Jeder andere Exit-Code** ist ein nicht-blockierender Fehler für die meisten Hook-Ereignisse. Das Transkript zeigt eine `<hook name> hook error`-Benachrichtigung gefolgt von der ersten Zeile von stderr, damit Sie die Ursache ohne `--debug` identifizieren können. Die Ausführung wird fortgesetzt und der vollständige stderr wird in das Debug-Log geschrieben.

Zum Beispiel ein Hook-Befehlsskript, das gefährliche Bash-Befehle blockiert:

```bash theme={null}
#!/bin/bash
# Liest JSON-Eingabe von stdin, prüft den Befehl
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blockierender Fehler: Tool-Aufruf wird verhindert
fi

exit 0  # Erfolg: Tool-Aufruf wird fortgesetzt
```

<Warning>
  Für die meisten Hook-Ereignisse blockiert nur Exit-Code 2 die Aktion. Claude Code behandelt Exit-Code 1 als nicht-blockierenden Fehler und setzt die Aktion fort, obwohl 1 der konventionelle Unix-Fehlercode ist. Wenn Ihr Hook eine Richtlinie durchsetzen soll, verwenden Sie `exit 2`. Die Ausnahme ist `WorktreeCreate`, wo jeder Nicht-Null-Exit-Code die Worktree-Erstellung abbricht.
</Warning>

#### Exit-Code-2-Verhalten pro Ereignis

Exit-Code 2 ist die Art, wie ein Hook signalisiert „Stopp, mach das nicht." Die Auswirkung hängt vom Ereignis ab, da einige Ereignisse Aktionen darstellen, die blockiert werden können (wie ein Tool-Aufruf, der noch nicht stattgefunden hat), und andere Dinge darstellen, die bereits passiert sind oder nicht verhindert werden können.

| Hook-Ereignis         | Kann blockiert werden? | Was passiert bei Exit 2                                                                                                                                                                          |
| :-------------------- | :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`          | Ja                     | Blockiert den Tool-Aufruf                                                                                                                                                                        |
| `PermissionRequest`   | Ja                     | Verweigert die Berechtigung                                                                                                                                                                      |
| `UserPromptSubmit`    | Ja                     | Blockiert die Prompt-Verarbeitung und löscht den Prompt                                                                                                                                          |
| `UserPromptExpansion` | Ja                     | Blockiert die Erweiterung                                                                                                                                                                        |
| `Stop`                | Ja                     | Verhindert, dass Claude stoppt, setzt das Gespräch fort                                                                                                                                          |
| `SubagentStop`        | Ja                     | Verhindert, dass der Subagent stoppt                                                                                                                                                             |
| `TeammateIdle`        | Ja                     | Verhindert, dass der Teammate untätig wird (Teammate arbeitet weiter)                                                                                                                            |
| `TaskCreated`         | Ja                     | Rollback der Aufgabenerstellung                                                                                                                                                                  |
| `TaskCompleted`       | Ja                     | Verhindert, dass die Aufgabe als abgeschlossen markiert wird                                                                                                                                     |
| `ConfigChange`        | Ja                     | Blockiert die Konfigurationsänderung von der Anwendung (außer `policy_settings`)                                                                                                                 |
| `StopFailure`         | Nein                   | Ausgabe und Exit-Code werden ignoriert                                                                                                                                                           |
| `PostToolUse`         | Nein                   | Zeigt stderr Claude an (Tool wurde bereits ausgeführt)                                                                                                                                           |
| `PostToolUseFailure`  | Nein                   | Zeigt stderr Claude an (Tool ist bereits fehlgeschlagen)                                                                                                                                         |
| `PostToolBatch`       | Ja                     | Stoppt die agentengesteuerte Schleife vor dem nächsten Modellaufruf                                                                                                                              |
| `PermissionDenied`    | Nein                   | Exit-Code und stderr werden ignoriert (Ablehnung ist bereits erfolgt). Verwenden Sie JSON `hookSpecificOutput.retry: true`, um dem Modell zu sagen, dass es möglicherweise erneut versuchen kann |
| `Notification`        | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `SubagentStart`       | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `SessionStart`        | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `Setup`               | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `SessionEnd`          | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `CwdChanged`          | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `FileChanged`         | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `PreCompact`          | Ja                     | Blockiert die Komprimierung                                                                                                                                                                      |
| `PostCompact`         | Nein                   | Zeigt stderr nur dem Benutzer an                                                                                                                                                                 |
| `Elicitation`         | Ja                     | Verweigert die Elicitation                                                                                                                                                                       |
| `ElicitationResult`   | Ja                     | Blockiert die Antwort (Aktion wird Ablehnung)                                                                                                                                                    |
| `WorktreeCreate`      | Ja                     | Jeder Nicht-Null-Exit-Code führt zu Fehler bei der Worktree-Erstellung                                                                                                                           |
| `WorktreeRemove`      | Nein                   | Fehler werden nur im Debug-Modus protokolliert                                                                                                                                                   |
| `InstructionsLoaded`  | Nein                   | Exit-Code wird ignoriert                                                                                                                                                                         |

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

Hook-Ausgabe-Strings, einschließlich `additionalContext`, `systemMessage` und Plain-stdout, sind auf 10.000 Zeichen begrenzt. Ausgabe, die dieses Limit überschreitet, wird in einer Datei gespeichert und durch eine Vorschau und einen Dateipfad ersetzt, auf die gleiche Weise wie große Tool-Ergebnisse behandelt werden.

Das JSON-Objekt unterstützt drei Arten von Feldern:

* **Universelle Felder** wie `continue` funktionieren über alle Ereignisse hinweg. Diese sind in der Tabelle unten aufgelistet.
* **Top-Level `decision` und `reason`** werden von einigen Ereignissen verwendet, um zu blockieren oder Feedback zu geben.
* **`hookSpecificOutput`** ist ein verschachteltes Objekt für Ereignisse, die reichere Kontrolle benötigen. Es erfordert ein `hookEventName`-Feld, das auf den Ereignisnamen gesetzt ist.

| Feld               | Standard | Beschreibung                                                                                                                                                                                                                                                                                                                                                                             |
| :----------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `continue`         | `true`   | Wenn `false`, stoppt Claude die Verarbeitung vollständig, nachdem der Hook ausgeführt wurde. Hat Vorrang vor allen ereignisspezifischen Entscheidungsfeldern                                                                                                                                                                                                                             |
| `stopReason`       | keine    | Nachricht, die dem Benutzer angezeigt wird, wenn `continue` `false` ist. Wird Claude nicht angezeigt                                                                                                                                                                                                                                                                                     |
| `suppressOutput`   | `false`  | Wenn `true`, verbirgt stdout aus dem Debug-Log                                                                                                                                                                                                                                                                                                                                           |
| `systemMessage`    | keine    | Warnmeldung, die dem Benutzer angezeigt wird                                                                                                                                                                                                                                                                                                                                             |
| `terminalSequence` | keine    | Eine Terminal-Escape-Sequenz, die Claude Code in Ihrem Namen ausgeben soll, wie eine Desktop-Benachrichtigung, ein Fenstertitel oder eine Glocke. Beschränkt auf OSC `0`/`1`/`2`/`9`/`99`/`777` und BEL. Wenn der Wert etwas außerhalb der Zulassungsliste enthält, wird das Feld ignoriert. Verwenden Sie dies anstelle des Schreibens zu `/dev/tty`, das für Hooks nicht verfügbar ist |

Um Claude unabhängig vom Ereignistyp vollständig zu stoppen:

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Terminal-Benachrichtigungen ausgeben

Das Feld `terminalSequence` erfordert Claude Code v2.1.141 oder später.

Hooks werden ohne steuerndes Terminal ausgeführt, daher schlägt das direkte Schreiben von Escape-Sequenzen zu `/dev/tty` fehl. Geben Sie stattdessen die Escape-Sequenz im Feld `terminalSequence` zurück und Claude Code gibt sie für Sie über seinen eigenen Terminal-Schreibpfad aus. Dies ist race-frei, funktioniert innerhalb von tmux und GNU screen und funktioniert unter Windows, wo es kein `/dev/tty` gibt.

Das Feld akzeptiert einen String aus einer oder mehreren zugelassenen Escape-Sequenzen:

* OSC `0`, `1`, `2`: Fenster- und Symboltitel
* OSC `9`: iTerm2-, ConEmu-, Windows Terminal- und WezTerm-Benachrichtigungen, einschließlich `9;4` Taskleisten-Fortschritt
* OSC `99`: Kitty-Benachrichtigungen
* OSC `777`: urxvt-, Ghostty- und Warp-Benachrichtigungen
* Bare BEL

Sequenzen können mit BEL oder mit ST beendet werden. Alles außerhalb der Zulassungsliste, einschließlich CSI-Cursor- und Farbsequenzen, OSC-Palettensequenzen, OSC-8-Hyperlinks, OSC-52-Zwischenablage-Schreibvorgänge und OSC-1337, wird abgelehnt und das Feld wird ignoriert.

Das folgende Beispiel löst eine Desktop-Benachrichtigung aus einem `Notification`-Hook aus. Die Escape-Sequenz wird mit `printf`-Oktalescapes erstellt, sodass die Steuerbytes niemals auf der Shell-Befehlszeile erscheinen, und `jq -n --arg` erstellt die JSON-Ausgabe, sodass Anführungszeichen, Backslashes und Zeilenumbrüche in der Benachrichtigungsmeldung korrekt escaped werden:

```bash theme={null}
#!/bin/bash
# Notification-Hook: Ping des Desktops, wenn Claude Code Aufmerksamkeit benötigt.
input=$(cat)
title="Claude Code'
body=$(jq -r '.message // 'Needs your attention"' <<<"$input")
seq=$(printf '\033]777;notify;%s;%s\007' "$title" "$body")
jq -nc --arg seq "$seq" '{terminalSequence: $seq}'
```

Die Form `{ "terminalSequence": "..." }` ist die gleiche aus jeder Shell oder Sprache. Unter Windows erstellen Sie die Escape-Zeichenkette in PowerShell oder einem Skript und geben das gleiche JSON-Objekt aus.

<Note>
  `terminalSequence` ist der unterstützte Ersatz für Hooks, die zuvor Escape-Sequenzen direkt zu `/dev/tty` schrieben. Die Zulassungsliste ist auf Sequenzen beschränkt, die den Cursor nicht bewegen oder Farben ändern können, sodass ein Hook niemals eine On-Screen-Eingabeaufforderung beschädigen kann.
</Note>

#### Kontext für Claude hinzufügen

Das Feld `additionalContext` übergibt einen String aus Ihrem Hook in Claudes Kontextfenster. Claude Code umhüllt den String in eine Systemerinnerung und fügt ihn in das Gespräch an dem Punkt ein, an dem der Hook ausgelöst wurde. Claude liest die Erinnerung bei der nächsten Modellanfrage, aber sie wird nicht als Chat-Nachricht in der Benutzeroberfläche angezeigt.

Geben Sie `additionalContext` innerhalb von `hookSpecificOutput` neben dem Ereignisnamen zurück:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

Wo die Erinnerung angezeigt wird, hängt vom Ereignis ab:

* [SessionStart](#sessionstart), [Setup](#setup) und [SubagentStart](#subagentstart): am Anfang des Gesprächs, vor der ersten Eingabeaufforderung
* [UserPromptSubmit](#userpromptsubmit) und [UserPromptExpansion](#userpromptexpansion): neben der eingereichten Eingabeaufforderung
* [PreToolUse](#pretooluse), [PostToolUse](#posttooluse), [PostToolUseFailure](#posttoolusefailure) und [PostToolBatch](#posttoolbatch): neben dem Tool-Ergebnis

Wenn mehrere Hooks `additionalContext` für das gleiche Ereignis zurückgeben, erhält Claude alle Werte. Wenn ein Wert 10.000 Zeichen überschreitet, schreibt Claude Code den vollständigen Text in eine Datei im Sitzungsverzeichnis und übergibt Claude stattdessen den Dateipfad mit einer kurzen Vorschau.

Verwenden Sie `additionalContext` für Informationen, die Claude über den aktuellen Zustand Ihrer Umgebung oder die gerade ausgeführte Operation wissen sollte:

* **Umgebungszustand**: der aktuelle Branch, das Bereitstellungsziel oder aktive Feature-Flags
* **Bedingte Projektregeln**: welcher Test-Befehl für die gerade bearbeitete Datei gilt, welche Verzeichnisse in diesem Worktree schreibgeschützt sind
* **Externe Daten**: offene Probleme, die Ihnen zugewiesen sind, aktuelle CI-Ergebnisse, Inhalte, die von einem internen Service abgerufen wurden

Für Anweisungen, die sich nie ändern, bevorzugen Sie [CLAUDE.md](/de/memory). Es wird ohne Ausführung eines Skripts geladen und ist der Standardort für statische Projektkonventionen.

Schreiben Sie den Text als sachliche Aussagen statt als imperative Systembefehle. Formulierungen wie „Das Bereitstellungsziel ist Produktion" oder „Dieses Repo verwendet `bun test`" werden als Projektinformationen gelesen. Text, der als Out-of-Band-Systembefehle formuliert ist, kann Claudes Prompt-Injection-Abwehr auslösen, was dazu führt, dass Claude den Text an Sie zurückgibt, anstatt ihn als Kontext zu behandeln.

Nach der Injektion wird der Text im Sitzungstranskript gespeichert. Für Mid-Session-Ereignisse wie `PostToolUse` oder `UserPromptSubmit` wird beim Fortsetzen mit `--continue` oder `--resume` der gespeicherte Text erneut abgespielt, anstatt den Hook für vergangene Umdrehungen erneut auszuführen, sodass Werte wie Zeitstempel oder Commit-SHAs beim Fortsetzen veraltet werden. `SessionStart`-Hooks werden beim Fortsetzen mit `source` auf `"resume"` gesetzt erneut ausgeführt, sodass sie ihren Kontext aktualisieren können.

#### Entscheidungskontrolle

Nicht jedes Ereignis unterstützt das Blockieren oder Steuern des Verhaltens durch JSON. Die Ereignisse, die dies tun, verwenden jeweils einen anderen Satz von Feldern, um diese Entscheidung auszudrücken. Verwenden Sie diese Tabelle als schnelle Referenz, bevor Sie einen Hook schreiben:

| Ereignisse                                                                                                                          | Entscheidungsmuster              | Schlüsselfelder                                                                                                                                                                      |
| :---------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | Top-Level `decision`             | `decision: "block"`, `reason`                                                                                                                                                        |
| TeammateIdle, TaskCreated, TaskCompleted                                                                                            | Exit-Code oder `continue: false` | Exit-Code 2 blockiert die Aktion mit stderr-Feedback. JSON `{"continue": false, "stopReason": "..."}` stoppt auch den Teammate vollständig, was dem `Stop`-Hook-Verhalten entspricht |
| PreToolUse                                                                                                                          | `hookSpecificOutput`             | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`                                                                                                              |
| PermissionRequest                                                                                                                   | `hookSpecificOutput`             | `decision.behavior` (allow/deny)                                                                                                                                                     |
| PermissionDenied                                                                                                                    | `hookSpecificOutput`             | `retry: true` teilt dem Modell mit, dass es möglicherweise den verweigerten Tool-Aufruf erneut versuchen kann                                                                        |
| WorktreeCreate                                                                                                                      | Pfad-Rückgabe                    | Command-Hook gibt Pfad auf stdout aus; HTTP-Hook gibt `hookSpecificOutput.worktreePath` zurück. Hook-Fehler oder fehlender Pfad schlägt die Erstellung fehl                          |
| Elicitation                                                                                                                         | `hookSpecificOutput`             | `action` (accept/decline/cancel), `content` (Formularfeldwerte für accept)                                                                                                           |
| ElicitationResult                                                                                                                   | `hookSpecificOutput`             | `action` (accept/decline/cancel), `content` (Formularfeldwerte überschreiben)                                                                                                        |
| WorktreeRemove, Notification, SessionEnd, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged                     | Keine                            | Keine Entscheidungskontrolle. Wird für Nebenwirkungen wie Protokollierung oder Bereinigung verwendet                                                                                 |

Hier sind Beispiele für jedes Muster in Aktion:

<Tabs>
  <Tab title="Top-Level-Entscheidung">
    Wird von `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange` und `PreCompact` verwendet. Der einzige Wert ist `"block"`. Um die Aktion fortzusetzen, lassen Sie `decision` aus Ihrem JSON weg, oder beenden Sie mit 0 ohne jede JSON:

    ```json theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Verwendet `hookSpecificOutput` für reichere Kontrolle: zulassen, verweigern oder an den Benutzer eskalieren. Sie können auch die Tool-Eingabe vor der Ausführung ändern oder zusätzlichen Kontext für Claude injizieren. Siehe [PreToolUse-Entscheidungskontrolle](#pretooluse-decision-control) für den vollständigen Satz von Optionen.

    ```json theme={null}
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

    ```json theme={null}
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

SessionStart wird bei jeder Sitzung ausgeführt, daher halten Sie diese Hooks schnell. Nur `type: "command"` und `type: "mcp_tool"` Hooks werden unterstützt.

Der Matcher-Wert entspricht der Art, wie die Sitzung initiiert wurde:

| Matcher   | Wann es ausgelöst wird                  |
| :-------- | :-------------------------------------- |
| `startup` | Neue Sitzung                            |
| `resume`  | `--resume`, `--continue` oder `/resume` |
| `clear`   | `/clear`                                |
| `compact` | Auto- oder manuelle Komprimierung       |

#### SessionStart-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten SessionStart-Hooks `source`, `model` und optional `agent_type`. Das Feld `source` gibt an, wie die Sitzung gestartet wurde: `"startup"` für neue Sitzungen, `"resume"` für fortgesetzte Sitzungen, `"clear"` nach `/clear` oder `"compact"` nach Komprimierung. Das Feld `model` enthält die Modell-ID. Wenn Sie Claude Code mit `claude --agent <name>` starten, enthält ein Feld `agent_type` den Agent-Namen.

```json theme={null}
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

| Feld                | Beschreibung                                                                                                                                                                                                                                              |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext am Anfang des Gesprächs hinzugefügt wird, vor dem ersten Prompt. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude), um zu erfahren, wie der Text bereitgestellt wird und was Sie darin einfügen sollten |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2"
  }
}
```

Da einfacher stdout bereits Claude für dieses Ereignis erreicht, kann ein Hook, der nur Kontext lädt, direkt auf stdout drucken, ohne JSON zu erstellen. Verwenden Sie die JSON-Form, wenn Sie Kontext mit anderen Feldern wie `suppressOutput` kombinieren müssen.

#### Umgebungsvariablen beibehalten

SessionStart-Hooks haben Zugriff auf die Umgebungsvariable `CLAUDE_ENV_FILE`, die einen Dateipfad bereitstellt, in dem Sie Umgebungsvariablen für nachfolgende Bash-Befehle beibehalten können.

Um einzelne Umgebungsvariablen zu setzen, schreiben Sie `export`-Anweisungen in `CLAUDE_ENV_FILE`. Verwenden Sie Anhängen (`>>`), um Variablen zu bewahren, die von anderen Hooks gesetzt wurden:

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Um alle Umgebungsänderungen von Setup-Befehlen zu erfassen, vergleichen Sie die exportierten Variablen vorher und nachher:

```bash theme={null}
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
  `CLAUDE_ENV_FILE` ist für SessionStart-, [Setup](#setup)-, [CwdChanged](#cwdchanged)- und [FileChanged](#filechanged)-Hooks verfügbar. Andere Hook-Typen haben keinen Zugriff auf diese Variable.
</Note>

### Setup

Wird nur ausgelöst, wenn Sie Claude Code mit `--init-only` starten oder mit `--init` oder `--maintenance` im Print-Modus (`-p`). Es wird nicht beim normalen Start ausgelöst. Verwenden Sie es für einmalige Abhängigkeitsinstallation oder geplante Bereinigung, die Sie explizit von CI oder Skripten aus auslösen, getrennt vom normalen Sitzungsstart. Für Initialisierung pro Sitzung verwenden Sie stattdessen [SessionStart](#sessionstart).

Der Matcher-Wert entspricht dem CLI-Flag, das den Hook ausgelöst hat:

| Matcher       | Wann es ausgelöst wird                       |
| :------------ | :------------------------------------------- |
| `init`        | `claude --init-only` oder `claude -p --init` |
| `maintenance` | `claude -p --maintenance`                    |

`--init-only` führt Setup-Hooks und SessionStart-Hooks mit dem `startup`-Matcher aus und beendet sich dann, ohne ein Gespräch zu starten. `--init` und `--maintenance` lösen Setup-Hooks nur aus, wenn sie mit `-p` (Print-Modus) kombiniert werden; in einer interaktiven Sitzung lösen diese beiden Flags derzeit keine Setup-Hooks aus.

Da Setup nicht bei jedem Start ausgelöst wird, kann ein Plugin, das eine Abhängigkeit installiert benötigt, sich nicht allein auf Setup verlassen. Das praktische Muster ist, die Abhängigkeit bei der ersten Verwendung zu überprüfen und bei Fehlen zu installieren, zum Beispiel ein Hook oder eine Skill, die auf `${CLAUDE_PLUGIN_DATA}/node_modules` testet und `npm install` ausführt, wenn es fehlt. Siehe das [Verzeichnis für persistente Daten](/de/plugins-reference#persistent-data-directory), um zu erfahren, wo Sie installierte Abhängigkeiten speichern können.

#### Setup-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten Setup-Hooks ein Feld `trigger`, das auf `"init"` oder `"maintenance"` gesetzt ist:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

#### Setup-Entscheidungskontrolle

Setup-Hooks können nicht blockieren. Bei Exit-Code 2 wird stderr dem Benutzer angezeigt; bei jedem anderen Nicht-Null-Exit-Code wird stderr nur angezeigt, wenn Sie mit `--verbose` starten. In beiden Fällen wird die Ausführung fortgesetzt. Um Informationen in Claudes Kontext zu übergeben, geben Sie `additionalContext` in der JSON-Ausgabe zurück; einfacher stdout wird nur in das Debug-Protokoll geschrieben. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, können Sie diese ereignisspezifischen Felder zurückgeben:

| Feld                | Beschreibung                                                                                 |
| :------------------ | :------------------------------------------------------------------------------------------- |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext hinzugefügt wird. Werte mehrerer Hooks werden verkettet |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Setup",
    "additionalContext": "Dependencies installed: node_modules, .venv"
  }
}
```

Setup-Hooks haben Zugriff auf `CLAUDE_ENV_FILE`. Variablen, die in diese Datei geschrieben werden, bleiben in nachfolgenden Bash-Befehlen für die Sitzung erhalten, genau wie in [SessionStart-Hooks](#persist-environment-variables). Nur `type: "command"` und `type: "mcp_tool"` Hooks werden unterstützt.

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

```json theme={null}
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

`UserPromptSubmit`-Hooks haben ein Standard-Timeout von 30 Sekunden für `command`-, `http`- und `mcp_tool`-Typen, kürzer als das 600-Sekunden-Standard für diese Typen bei anderen Ereignissen. Da dieser Hook vor jedem Prompt ausgeführt wird und die Modellverarbeitung blockiert, bis er abgeschlossen ist, stellt ein feststeckender Hook die Sitzung still. Wenn Ihr Hook mehr Zeit benötigt, setzen Sie das Feld `timeout` im Hook-Eintrag.

#### UserPromptSubmit-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten UserPromptSubmit-Hooks das Feld `prompt`, das den Text enthält, den der Benutzer eingereicht hat.

```json theme={null}
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

| Feld                | Beschreibung                                                                                                                                                 |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` verhindert die Verarbeitung des Prompts und löscht ihn aus dem Kontext. Weglassen, um den Prompt fortzusetzen                                      |
| `reason`            | Wird dem Benutzer angezeigt, wenn `decision` `"block"` ist. Wird nicht zum Kontext hinzugefügt                                                               |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext hinzugefügt wird, zusammen mit dem eingereichten Prompt. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude) |
| `sessionTitle`      | Setzt den Sitzungstitel. Verwenden Sie, um Sitzungen automatisch basierend auf dem Prompt-Inhalt zu benennen                                                 |

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title"
  }
}
```

<Note>
  Das JSON-Format ist nicht erforderlich für einfache Anwendungsfälle. Um Kontext hinzuzufügen, können Sie einfach Plain-Text auf stdout mit Exit-Code 0 ausgeben. Verwenden Sie JSON, wenn Sie Prompts blockieren oder mehr strukturierte Kontrolle benötigen.
</Note>

### UserPromptExpansion

Wird ausgeführt, wenn ein vom Benutzer eingegebener Slash-Befehl vor Erreichen von Claude in einen Prompt erweitert wird. Verwenden Sie dies, um bestimmte Befehle von direkter Aufrufe zu blockieren, Kontext für eine bestimmte Skill einzufügen oder zu protokollieren, welche Befehle Benutzer aufrufen. Zum Beispiel kann ein Hook, der `deploy` passt, `/deploy` blockieren, es sei denn, eine Genehmigungsdatei ist vorhanden, oder ein Hook, der eine Review-Skill passt, kann die Review-Checkliste des Teams als `additionalContext` anhängen.

Dieses Ereignis deckt den Pfad ab, den `PreToolUse` nicht abdeckt: Ein `PreToolUse`-Hook, der das `Skill`-Tool passt, wird nur ausgelöst, wenn Claude das Tool aufruft, aber das direkte Eingeben von `/skillname` umgeht `PreToolUse`. `UserPromptExpansion` wird auf diesem direkten Pfad ausgelöst.

Passt auf `command_name`. Lassen Sie den Matcher leer, um auf jedem Prompt-Typ-Slash-Befehl zu feuern.

#### UserPromptExpansion-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten UserPromptExpansion-Hooks `expansion_type`, `command_name`, `command_args`, `command_source` und die ursprüngliche `prompt`-Zeichenkette. Das Feld `expansion_type` ist `slash_command` für Skill- und benutzerdefinierte Befehle oder `mcp_prompt` für MCP-Server-Prompts.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/example-skill arg1 arg2"
}
```

#### UserPromptExpansion-Entscheidungskontrolle

`UserPromptExpansion`-Hooks können die Erweiterung blockieren oder Kontext hinzufügen. Alle [JSON-Ausgabefelder](#json-output) sind verfügbar.

| Feld                | Beschreibung                                                                                                                                              |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` verhindert die Erweiterung des Slash-Befehls. Weglassen, um ihn fortzusetzen                                                                    |
| `reason`            | Wird dem Benutzer angezeigt, wenn `decision` `"block"` ist                                                                                                |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext zusammen mit dem erweiterten Prompt hinzugefügt wird. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude) |

```json theme={null}
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

### PreToolUse

Wird ausgeführt, nachdem Claude Tool-Parameter erstellt hat und bevor der Tool-Aufruf verarbeitet wird. Passt auf Tool-Namen: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode` und alle [MCP-Tool-Namen](#match-mcp-tools).

Verwenden Sie [PreToolUse-Entscheidungskontrolle](#pretooluse-decision-control), um die Verwendung des Tools zuzulassen, zu verweigern, um Berechtigung zu bitten oder zu verschieben.

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

In `PostToolUse` trägt `tool_response` für einen abgeschlossenen Agent-Aufruf den abschließenden Text des Subagenten zusammen mit Nutzungstelemetrie. Lesen Sie diese Felder, um Pro-Subagent-Kosten aus einem Hook zu erfassen:

| Feld                | Typ          | Beispiel                                              | Beschreibung                                                                                                             |
| :------------------ | :----------- | :---------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `status`            | Zeichenkette | `"completed"`                                         | `"completed"` für synchrone Aufrufe, `"async_launched"` für `run_in_background: true`                                    |
| `agentId`           | Zeichenkette | `"a4d2c8f1e0b3a297"`                                  | Kennung für die Subagenten-Ausführung                                                                                    |
| `content`           | Array        | `[{"type": "text", "text": "Found 12 endpoints..."}]` | Die abschließenden Textblöcke des Subagenten                                                                             |
| `totalTokens`       | Zahl         | `12450`                                               | Gesamttokens, die über die Runden des Subagenten abgerechnet werden                                                      |
| `totalDurationMs`   | Zahl         | `48211`                                               | Wanduhr-Dauer der Subagenten-Ausführung                                                                                  |
| `totalToolUseCount` | Zahl         | `7`                                                   | Anzahl der Tool-Aufrufe, die der Subagent gemacht hat                                                                    |
| `usage`             | Objekt       | `{"input_tokens": 8320, ...}`                         | Pro-Typ-Token-Aufschlüsselung: `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens` |

Für `run_in_background: true`-Aufrufe gibt das Tool sofort nach dem Starten des Subagenten zurück, daher trägt `tool_response` keine Nutzungsfelder. Es hat stattdessen `status: "async_launched"`, `agentId`, `description`, `prompt` und `outputFile`.

##### AskUserQuestion

Stellt dem Benutzer eine bis vier Multiple-Choice-Fragen.

| Feld        | Typ    | Beispiel                                                                                                           | Beschreibung                                                                                                                                                                                                                      |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `questions` | Array  | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | Fragen zum Präsentieren, jeweils mit einer `question`-Zeichenkette, kurzem `header`, `options`-Array und optionalem `multiSelect`-Flag                                                                                            |
| `answers`   | Objekt | `{"Which framework?": "React"}`                                                                                    | Optional. Ordnet Fragetext der ausgewählten Option-Bezeichnung zu. Multi-Select-Antworten verbinden Bezeichnungen mit Kommas. Claude setzt dieses Feld nicht; geben Sie es über `updatedInput` an, um programmatisch zu antworten |

##### ExitPlanMode

Präsentiert einen Plan und fordert den Benutzer auf, ihn zu genehmigen, bevor Claude den [Plan-Modus](/de/permission-modes#analyze-before-you-edit-with-plan-mode) verlässt. Claude schreibt den Plan vor dem Aufruf des Tools in eine Datei auf der Festplatte, daher trägt die wörtliche `tool_input` vom Modell nur `allowedPrompts`. Claude Code injiziert den Plan-Inhalt und den Dateipfad, bevor die Eingabe an Hooks übergeben wird.

| Feld             | Typ          | Beispiel                                    | Beschreibung                                                                                                                                                                              |
| :--------------- | :----------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan`           | Zeichenkette | `"## Refactor auth\n1. Extract..."`         | Plan-Inhalt in Markdown. Injiziert aus der Plan-Datei auf der Festplatte                                                                                                                  |
| `planFilePath`   | Zeichenkette | `"/Users/.../plans/refactor-auth.md"`       | Pfad zur Plan-Datei. Injiziert                                                                                                                                                            |
| `allowedPrompts` | Array        | `[{"tool": "Bash", "prompt": "run tests"}]` | Optional. Prompt-basierte Berechtigungen, die Claude anfordert, um den Plan zu implementieren, jeweils mit einem `tool`-Namen und einem `prompt`, der die Kategorie der Aktion beschreibt |

In `PostToolUse` ist `tool_response` ein Objekt mit `plan`- und `filePath`-Feldern, die den genehmigten Plan enthalten, plus interne Status-Flags. Lesen Sie `tool_response.plan` für den Plan-Inhalt, anstatt die Datei von der Festplatte neu zu lesen.

#### PreToolUse-Entscheidungskontrolle

`PreToolUse`-Hooks können steuern, ob ein Tool-Aufruf fortgesetzt wird. Im Gegensatz zu anderen Hooks, die ein Top-Level-Feld `decision` verwenden, gibt PreToolUse seine Entscheidung in einem `hookSpecificOutput`-Objekt zurück. Dies gibt ihm reichere Kontrolle: vier Ergebnisse (zulassen, verweigern, fragen oder verschieben) plus die Möglichkeit, die Tool-Eingabe vor der Ausführung zu ändern.

| Feld                       | Beschreibung                                                                                                                                                                                                                                                                                                                              |
| :------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` umgeht die Berechtigungsaufforderung. `"deny"` verhindert den Tool-Aufruf. `"ask"` fordert den Benutzer zur Bestätigung auf. `"defer"` beendet den Hook elegant, damit das Tool später fortgesetzt werden kann. [Deny- und Ask-Regeln](/de/permissions#manage-permissions) gelten weiterhin, wenn ein Hook `"allow"` zurückgibt |
| `permissionDecisionReason` | Für `"allow"` und `"ask"`, dem Benutzer angezeigt, aber nicht Claude. Für `"deny"`, Claude angezeigt. Für `"defer"`, ignoriert                                                                                                                                                                                                            |
| `updatedInput`             | Ändert die Tool-Eingabeparameter vor der Ausführung. Ersetzt das gesamte Eingabeobjekt, daher müssen Sie unveränderte Felder zusammen mit geänderten einbeziehen. Kombinieren Sie mit `"allow"`, um automatisch zu genehmigen, oder mit `"ask"`, um die geänderte Eingabe dem Benutzer zu zeigen. Für `"defer"`, ignoriert                |
| `additionalContext`        | Zeichenkette, die zu Claudes Kontext vor der Tool-Ausführung hinzugefügt wird. Für `"defer"`, ignoriert. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude)                                                                                                                                                                   |

Wenn mehrere PreToolUse-Hooks unterschiedliche Entscheidungen zurückgeben, ist die Priorität `deny` > `defer` > `ask` > `allow`.

Wenn ein Hook `"ask"` zurückgibt, enthält der dem Benutzer angezeigte Berechtigungsprompt ein Label, das angibt, woher der Hook stammt: zum Beispiel `[User]`, `[Project]`, `[Plugin]` oder `[Local]`. Dies hilft Benutzern zu verstehen, welche Konfigurationsquelle eine Bestätigung anfordert.

```json theme={null}
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

`AskUserQuestion` und `ExitPlanMode` erfordern Benutzerinteraktion und blockieren normalerweise im [nicht-interaktiven Modus](/de/headless) mit dem `-p`-Flag. Das Zurückgeben von `permissionDecision: "allow"` zusammen mit `updatedInput` erfüllt diese Anforderung: Der Hook liest die Tool-Eingabe von stdin, erfasst die Antwort über Ihre eigene Benutzeroberfläche und gibt sie in `updatedInput` zurück, damit das Tool ohne Aufforderung ausgeführt wird. Das Zurückgeben von `"allow"` allein ist nicht ausreichend für diese Tools. Für `AskUserQuestion` geben Sie das ursprüngliche `questions`-Array zurück und fügen Sie ein [`answers`](#askuserquestion)-Objekt hinzu, das jede Frage auf die gewählte Antwort abbildet.

<Note>
  PreToolUse verwendete zuvor Top-Level-Felder `decision` und `reason`, diese sind jedoch für dieses Ereignis veraltet. Verwenden Sie stattdessen `hookSpecificOutput.permissionDecision` und `hookSpecificOutput.permissionDecisionReason`. Die veralteten Werte `"approve"` und `"block"` werden auf `"allow"` und `"deny"` abgebildet. Andere Ereignisse wie PostToolUse und Stop verwenden weiterhin Top-Level-Felder `decision` und `reason` als ihr aktuelles Format.
</Note>

#### Ein Tool-Aufruf verschieben

`"defer"` ist für Integrationen, die `claude -p` als Subprozess ausführen und seine JSON-Ausgabe lesen, wie eine Agent SDK-App oder eine benutzerdefinierte Benutzeroberfläche, die auf Claude Code aufgebaut ist. Es ermöglicht diesem aufrufenden Prozess, Claude bei einem Tool-Aufruf zu pausieren, Eingaben über seine eigene Schnittstelle zu erfassen und dort fortzufahren, wo er aufgehört hat. Claude Code respektiert diesen Wert nur im [nicht-interaktiven Modus](/de/headless) mit dem `-p`-Flag. In interaktiven Sitzungen protokolliert es eine Warnung und ignoriert das Hook-Ergebnis.

<Note>
  Der Wert `defer` erfordert Claude Code v2.1.89 oder später. Frühere Versionen erkennen ihn nicht und das Tool wird durch den normalen Berechtigungsfluss fortgesetzt.
</Note>

Das Tool `AskUserQuestion` ist der typische Fall: Claude möchte den Benutzer etwas fragen, aber es gibt kein Terminal zum Antworten. Der Roundtrip funktioniert so:

1. Claude ruft `AskUserQuestion` auf. Der `PreToolUse`-Hook wird ausgelöst.
2. Der Hook gibt `permissionDecision: "defer"` zurück. Das Tool wird nicht ausgeführt. Der Prozess beendet sich mit `stop_reason: "tool_deferred"` und dem ausstehenden Tool-Aufruf, der im Transkript erhalten bleibt.
3. Der aufrufende Prozess liest `deferred_tool_use` aus dem SDK-Ergebnis, zeigt die Frage in seiner eigenen Benutzeroberfläche an und wartet auf eine Antwort.
4. Der aufrufende Prozess führt `claude -p --resume <session-id>` aus. Der gleiche Tool-Aufruf löst `PreToolUse` erneut aus.
5. Der Hook gibt `permissionDecision: "allow"` mit der Antwort in `updatedInput` zurück. Das Tool wird ausgeführt und Claude setzt fort.

Das Feld `deferred_tool_use` trägt die `id`, den `name` und die `input` des Tools. Die `input` sind die Parameter, die Claude für den Tool-Aufruf generiert hat, erfasst vor der Ausführung:

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

Es gibt kein Timeout oder Wiederholungslimit. Die Sitzung bleibt auf der Festplatte, bis Sie sie fortsetzen, unterliegt aber der [`cleanupPeriodDays`](/de/settings#available-settings)-Aufbewahrungssweep, die Sitzungsdateien nach 30 Tagen standardmäßig löscht. Wenn die Antwort nicht bereit ist, wenn Sie fortsetzen, kann der Hook erneut `"defer"` zurückgeben und der Prozess beendet sich auf die gleiche Weise. Der aufrufende Prozess steuert, wann die Schleife unterbrochen wird, indem er schließlich `"allow"` oder `"deny"` vom Hook zurückgibt.

`"defer"` funktioniert nur, wenn Claude einen einzelnen Tool-Aufruf in der Runde macht. Wenn Claude mehrere Tool-Aufrufe gleichzeitig macht, wird `"defer"` mit einer Warnung ignoriert und das Tool wird durch den normalen Berechtigungsfluss fortgesetzt. Die Einschränkung existiert, weil Resume nur einen Tool-Aufruf erneut ausführen kann: Es gibt keine Möglichkeit, einen Aufruf aus einem Batch zu verschieben, ohne die anderen ungelöst zu lassen.

Wenn das verschobene Tool nicht mehr verfügbar ist, wenn Sie fortsetzen, beendet sich der Prozess mit `stop_reason: "tool_deferred_unavailable"` und `is_error: true` bevor der Hook ausgelöst wird. Dies geschieht, wenn ein MCP-Server, der das Tool bereitgestellt hat, für die fortgesetzte Sitzung nicht verbunden ist. Die Nutzlast `deferred_tool_use` ist immer noch enthalten, damit Sie identifizieren können, welches Tool fehlte.

<Note>
  `--resume` stellt den Berechtigungsmodus wieder her, der aktiv war, als das Tool verschoben wurde, daher müssen Sie `--permission-mode` nicht erneut übergeben. Die Ausnahmen sind `plan` und `bypassPermissions`, die niemals übertragen werden. Das explizite Übergeben von `--permission-mode` bei der Wiederaufnahme überschreibt den wiederhergestellten Wert.
</Note>

### PermissionRequest

Wird ausgeführt, wenn dem Benutzer ein Berechtigungsdialog angezeigt wird.
Verwenden Sie [PermissionRequest-Entscheidungskontrolle](#permissionrequest-decision-control), um im Namen des Benutzers zuzulassen oder zu verweigern.

Passt auf Tool-Namen, gleiche Werte wie PreToolUse.

#### PermissionRequest-Eingabe

PermissionRequest-Hooks erhalten `tool_name`- und `tool_input`-Felder wie PreToolUse-Hooks, aber ohne `tool_use_id`. Ein optionales Array `permission_suggestions` enthält die Optionen „Immer zulassen", die der Benutzer normalerweise im Berechtigungsdialog sehen würde. Der Unterschied liegt darin, wann der Hook ausgelöst wird: PermissionRequest-Hooks werden ausgeführt, wenn ein Berechtigungsdialog dem Benutzer angezeigt werden soll, während PreToolUse-Hooks vor der Tool-Ausführung unabhängig vom Berechtigungsstatus ausgeführt werden.

```json theme={null}
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

| Feld                 | Beschreibung                                                                                                                                                                                                                                                |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` gewährt die Berechtigung, `"deny"` verweigert sie. [Deny- und Ask-Regeln](/de/permissions#manage-permissions) gelten weiterhin, daher überschreibt ein Hook, der `"allow"` zurückgibt, keine passende Deny-Regel                                  |
| `updatedInput`       | Nur für `"allow"`: ändert die Tool-Eingabeparameter vor der Ausführung. Ersetzt das gesamte Eingabeobjekt, daher müssen Sie unveränderte Felder zusammen mit geänderten einbeziehen. Die geänderte Eingabe wird erneut gegen Deny- und Ask-Regeln evaluiert |
| `updatedPermissions` | Nur für `"allow"`: Array von [Berechtigungsupdate-Einträgen](#permission-update-entries) zum Anwenden, wie das Hinzufügen einer Allow-Regel oder das Ändern des Session-Berechtigungsmodus                                                                  |
| `message`            | Nur für `"deny"`: teilt Claude mit, warum die Berechtigung verweigert wurde                                                                                                                                                                                 |
| `interrupt`          | Nur für `"deny"`: wenn `true`, stoppt Claude                                                                                                                                                                                                                |

```json theme={null}
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

<Note>
  `setMode` mit `bypassPermissions` nimmt nur Auswirkungen an, wenn die Sitzung mit Bypass-Modus bereits verfügbar gestartet wurde: `--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `--allow-dangerously-skip-permissions` oder `permissions.defaultMode: "bypassPermissions"` in Einstellungen, und der Modus ist nicht durch [`permissions.disableBypassPermissionsMode`](/de/permissions#managed-settings) deaktiviert. Andernfalls ist das Update ein No-Op. `bypassPermissions` wird niemals als `defaultMode` persistiert, unabhängig von `destination`.
</Note>

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

```json theme={null}
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
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| Feld          | Beschreibung                                                                                                                               |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `duration_ms` | Optional. Tool-Ausführungszeit in Millisekunden. Schließt Zeit aus, die in Berechtigungsaufforderungen und PreToolUse-Hooks verbracht wird |

#### PostToolUse-Entscheidungskontrolle

`PostToolUse`-Hooks können Claude nach der Tool-Ausführung Feedback geben. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript diese ereignisspezifischen Felder zurückgeben:

| Feld                   | Beschreibung                                                                                                                                                        |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `decision`             | `"block"` fügt den `reason` neben dem Tool-Ergebnis hinzu. Claude sieht immer noch die ursprüngliche Ausgabe; um sie zu ersetzen, verwenden Sie `updatedToolOutput` |
| `reason`               | Erklärung, die Claude angezeigt wird, wenn `decision` `"block"` ist                                                                                                 |
| `additionalContext`    | Zeichenkette, die zu Claudes Kontext zusammen mit dem Tool-Ergebnis hinzugefügt wird. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude)                |
| `updatedToolOutput`    | Ersetzt die Ausgabe des Tools durch den bereitgestellten Wert vor dem Senden an Claude. Der Wert muss der Ausgabeform des Tools entsprechen                         |
| `updatedMCPToolOutput` | Ersetzt die Ausgabe nur für [MCP-Tools](#match-mcp-tools). Bevorzugen Sie `updatedToolOutput`, das für alle Tools funktioniert                                      |

Das Beispiel unten ersetzt die Ausgabe eines `Bash`-Aufrufs. Der Ersatzwert entspricht der Ausgabeform des `Bash`-Tools:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

<Warning>
  `updatedToolOutput` ändert nur das, was Claude sieht. Das Tool ist bereits ausgeführt worden, wenn der Hook ausgelöst wird, daher haben alle geschriebenen Dateien, ausgeführten Befehle oder gesendeten Netzwerkanfragen bereits Auswirkungen. Telemetrie wie OpenTelemetry-Tool-Spans und Analyseereignisse erfassen auch die ursprüngliche Ausgabe, bevor der Hook ausgeführt wird. Um einen Tool-Aufruf zu verhindern oder zu ändern, bevor er ausgeführt wird, verwenden Sie stattdessen einen [PreToolUse](#pretooluse)-Hook.

  Der Ersatzwert muss der Ausgabeform des Tools entsprechen. Eingebaute Tools geben strukturierte Objekte anstelle von einfachen Zeichenketten zurück. Zum Beispiel gibt `Bash` ein Objekt mit `stdout`-, `stderr`-, `interrupted`- und `isImage`-Feldern zurück. Für eingebaute Tools wird ein Wert, der nicht dem Ausgabeschema des Tools entspricht, ignoriert und die ursprüngliche Ausgabe wird verwendet. MCP-Tool-Ausgabe wird ohne Schema-Validierung durchgeleitet. Das Entfernen von Fehlerdetails, die Claude benötigt, kann dazu führen, dass er bei einer falschen Annahme fortfährt.
</Warning>

### PostToolUseFailure

Wird ausgeführt, wenn eine Tool-Ausführung fehlschlägt. Dieses Ereignis wird für Tool-Aufrufe ausgelöst, die Fehler werfen oder Fehlerergebnisse zurückgeben. Verwenden Sie dies, um Fehler zu protokollieren, Warnungen zu senden oder korrektes Feedback an Claude zu geben.

Passt auf Tool-Namen, gleiche Werte wie PreToolUse.

#### PostToolUseFailure-Eingabe

PostToolUseFailure-Hooks erhalten die gleichen `tool_name`- und `tool_input`-Felder wie PostToolUse, zusammen mit Fehlerinformationen als Top-Level-Felder:

```json theme={null}
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
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| Feld           | Beschreibung                                                                                                                               |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `error`        | Zeichenkette, die beschreibt, was schief gelaufen ist                                                                                      |
| `is_interrupt` | Optionaler Boolesch, der angibt, ob der Fehler durch Benutzerunterbrechung verursacht wurde                                                |
| `duration_ms`  | Optional. Tool-Ausführungszeit in Millisekunden. Schließt Zeit aus, die in Berechtigungsaufforderungen und PreToolUse-Hooks verbracht wird |

#### PostToolUseFailure-Entscheidungskontrolle

`PostToolUseFailure`-Hooks können Claude nach einem Tool-Fehler Kontext geben. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript diese ereignisspezifischen Felder zurückgeben:

| Feld                | Beschreibung                                                                                                                                  |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext zusammen mit dem Fehler hinzugefügt wird. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PostToolBatch

Wird einmal ausgeführt, nachdem jeder Tool-Aufruf in einem Batch aufgelöst wurde, bevor Claude Code die nächste Anfrage an das Modell sendet. `PostToolUse` wird einmal pro Tool ausgeführt, was bedeutet, dass es gleichzeitig ausgeführt wird, wenn Claude parallele Tool-Aufrufe macht. `PostToolBatch` wird genau einmal mit dem vollständigen Batch ausgeführt, daher ist es der richtige Ort, um Kontext einzufügen, der von der Menge der Tools abhängt, die ausgeführt wurden, anstatt von einem einzelnen Tool. Es gibt keinen Matcher für dieses Ereignis.

#### PostToolBatch-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten PostToolBatch-Hooks `tool_calls`, ein Array, das jeden Tool-Aufruf im Batch beschreibt:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    }
  ]
}
```

`tool_response` enthält den gleichen Inhalt, den das Modell im entsprechenden `tool_result`-Block erhält. Der Wert ist eine serialisierte Zeichenkette oder ein Content-Block-Array, genau wie das Tool es ausgegeben hat. Für `Read` bedeutet das Zeilennummern-Präfix-Text anstelle von rohen Dateiinhalten. Antworten können groß sein, daher analysieren Sie nur die Felder, die Sie benötigen.

<Note>
  Die Form von `tool_response` unterscheidet sich von der von `PostToolUse`. `PostToolUse` übergibt das strukturierte `Output`-Objekt des Tools, wie `{filePath: "...", success: true}` für `Write`; `PostToolBatch` übergibt den serialisierten `tool_result`-Inhalt, den das Modell sieht.
</Note>

#### PostToolBatch-Entscheidungskontrolle

`PostToolBatch`-Hooks können Kontext für Claude einfügen. Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, kann Ihr Hook-Skript diese ereignisspezifischen Felder zurückgeben:

| Feld                | Beschreibung                                                                                                                                                                                                                                               |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | Kontext-Zeichenkette, die einmal vor dem nächsten Modell-Aufruf eingefügt wird. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude) für Lieferdetails, was Sie darin einfügen sollten und wie fortgesetzte Sitzungen vergangene Werte handhaben |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

Das Zurückgeben von `decision: "block"` oder `continue: false` stoppt die agentengesteuerte Schleife vor dem nächsten Modell-Aufruf.

### PermissionDenied

Wird ausgeführt, wenn der [Auto-Mode](/de/permission-modes#eliminate-prompts-with-auto-mode)-Klassifizierer einen Tool-Aufruf verweigert. Dieser Hook wird nur im Auto-Mode ausgelöst: Er wird nicht ausgeführt, wenn Sie einen Berechtigungsdialog manuell verweigern, wenn ein `PreToolUse`-Hook einen Aufruf blockiert oder wenn eine `deny`-Regel passt. Verwenden Sie ihn, um Klassifizierer-Ablehnungen zu protokollieren, die Konfiguration anzupassen oder dem Modell zu sagen, dass es den Tool-Aufruf möglicherweise erneut versuchen kann.

Passt auf Tool-Namen, gleiche Werte wie PreToolUse.

#### PermissionDenied-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten PermissionDenied-Hooks `tool_name`, `tool_input`, `tool_use_id` und `reason`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| Feld     | Beschreibung                                                              |
| :------- | :------------------------------------------------------------------------ |
| `reason` | Die Erklärung des Klassifizierers, warum der Tool-Aufruf verweigert wurde |

#### PermissionDenied-Entscheidungskontrolle

PermissionDenied-Hooks können dem Modell sagen, dass es den verweigerten Tool-Aufruf möglicherweise erneut versuchen kann. Geben Sie ein JSON-Objekt mit `hookSpecificOutput.retry` auf `true` zurück:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

Wenn `retry` `true` ist, fügt Claude Code eine Nachricht zum Gespräch hinzu, die dem Modell mitteilt, dass es den Tool-Aufruf möglicherweise erneut versuchen kann. Die Ablehnung selbst wird nicht rückgängig gemacht. Wenn Ihr Hook keine JSON zurückgibt oder `retry: false` zurückgibt, bleibt die Ablehnung bestehen und das Modell erhält die ursprüngliche Ablehnungsmeldung.

### Notification

Wird ausgeführt, wenn Claude Code Benachrichtigungen sendet. Passt auf Benachrichtigungstyp: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`. Matcher weglassen, um Hooks für alle Benachrichtigungstypen auszuführen.

Verwenden Sie separate Matcher, um verschiedene Handler je nach Benachrichtigungstyp auszuführen. Diese Konfiguration löst ein berechtigungsspezifisches Warnungsskript aus, wenn Claude Genehmigung benötigt, und eine andere Benachrichtigung, wenn Claude untätig war:

```json theme={null}
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

```json theme={null}
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

Notification-Hooks können Benachrichtigungen nicht blockieren oder ändern. Sie sind für Nebenwirkungen wie das Weiterleiten der Benachrichtigung an einen externen Service vorgesehen. Die [gemeinsamen JSON-Ausgabefelder](#json-output) wie `systemMessage` gelten.

### SubagentStart

Wird ausgeführt, wenn ein Claude Code-Subagent über das Agent-Tool spawnt wird. Unterstützt Matcher zum Filtern nach Agent-Typname. Für eingebaute Agents ist dies der Agent-Name wie `general-purpose`, `Explore` oder `Plan`. Für [benutzerdefinierte Subagenten](/de/sub-agents) ist dies das Feld `name` aus dem Frontmatter des Agenten, nicht der Dateiname.

#### SubagentStart-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten SubagentStart-Hooks `agent_id` mit der eindeutigen Kennung für den Subagenten und `agent_type` mit dem Agent-Namen (eingebaute Agents wie `"general-purpose"`, `"Explore"`, `"Plan"` oder benutzerdefinierte Agent-Namen).

```json theme={null}
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

| Feld                | Beschreibung                                                                                                                                                                           |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | Zeichenkette, die zu Claudes Kontext am Anfang des Gesprächs des Subagenten hinzugefügt wird, vor seinem ersten Prompt. Siehe [Kontext für Claude hinzufügen](#add-context-for-claude) |

```json theme={null}
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

```json theme={null}
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

SubagentStop-Hooks verwenden das gleiche Entscheidungskontrollformat wie [Stop-Hooks](#stop-decision-control). Sie unterstützen keine `additionalContext`. Das Zurückgeben von `decision: "block"` mit einem `reason` hält den Subagenten am Laufen und liefert `reason` an den Subagenten als nächste Anweisung. Um Kontext in die übergeordnete Sitzung nach der Rückkehr eines Subagenten einzufügen, verwenden Sie stattdessen einen [`PostToolUse`](#posttooluse)-Hook auf dem `Agent`-Tool.

### TaskCreated

Wird ausgeführt, wenn eine Aufgabe über das `TaskCreate`-Tool erstellt wird. Verwenden Sie dies, um Benennungskonventionen durchzusetzen, Aufgabenbeschreibungen zu erfordern oder zu verhindern, dass bestimmte Aufgaben erstellt werden.

Wenn ein `TaskCreated`-Hook mit Code 2 beendet wird, wird die Aufgabe nicht erstellt und die stderr-Nachricht wird dem Modell als Feedback zurückgegeben. Um den Teammate stattdessen vollständig zu stoppen, geben Sie JSON mit `{"continue": false, "stopReason": "..."}` zurück. TaskCreated-Hooks unterstützen keine Matcher und werden bei jedem Auftreten ausgelöst.

#### TaskCreated-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten TaskCreated-Hooks `task_id`, `task_subject` und optional `task_description`, `teammate_name` und `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Feld               | Beschreibung                                              |
| :----------------- | :-------------------------------------------------------- |
| `task_id`          | Kennung der zu erstellenden Aufgabe                       |
| `task_subject`     | Titel der Aufgabe                                         |
| `task_description` | Detaillierte Beschreibung der Aufgabe. Kann fehlen        |
| `teammate_name`    | Name des Teammates, das die Aufgabe erstellt. Kann fehlen |
| `team_name`        | Name des Teams. Kann fehlen                               |

#### TaskCreated-Entscheidungskontrolle

TaskCreated-Hooks unterstützen zwei Möglichkeiten, die Aufgabenerstellung zu steuern:

* **Exit-Code 2**: Die Aufgabe wird nicht erstellt und die stderr-Nachricht wird dem Modell als Feedback zurückgegeben.
* **JSON `{"continue": false, "stopReason": "..."}`**: Stoppt den Teammate vollständig, was dem `Stop`-Hook-Verhalten entspricht. Der `stopReason` wird dem Benutzer angezeigt.

Dieses Beispiel blockiert Aufgaben, deren Betreff nicht dem erforderlichen Format entspricht:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Wird ausgeführt, wenn eine Aufgabe als abgeschlossen markiert wird. Dies wird in zwei Situationen ausgelöst: wenn ein Agent eine Aufgabe explizit über das TaskUpdate-Tool als abgeschlossen markiert, oder wenn ein [Agent-Team](/de/agent-teams)-Teammate seine Runde mit laufenden Aufgaben beendet. Verwenden Sie dies, um Abschluss-Kriterien wie bestandene Tests oder Lint-Checks durchzusetzen, bevor eine Aufgabe geschlossen werden kann.

Wenn ein `TaskCompleted`-Hook mit Code 2 beendet wird, wird die Aufgabe nicht als abgeschlossen markiert und die stderr-Nachricht wird dem Modell als Feedback zurückgegeben. Um den Teammate stattdessen vollständig zu stoppen, geben Sie JSON mit `{"continue": false, "stopReason": "..."}` zurück. TaskCompleted-Hooks unterstützen keine Matcher und werden bei jedem Auftreten ausgelöst.

#### TaskCompleted-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten TaskCompleted-Hooks `task_id`, `task_subject` und optional `task_description`, `teammate_name` und `team_name`.

```json theme={null}
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

```bash theme={null}
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

### Stop

Wird ausgeführt, wenn der Haupt-Claude Code-Agent fertig mit der Antwort ist. Wird nicht ausgeführt, wenn der Stopp durch eine Benutzerunterbrechung verursacht wurde. API-Fehler lösen stattdessen [StopFailure](#stopfailure) aus.

<Tip>
  Der Befehl [`/goal`](/de/goal) ist eine eingebaute Verknüpfung für einen sitzungsspezifischen Prompt-basierten Stop-Hook. Verwenden Sie ihn, wenn Sie möchten, dass Claude weiterarbeitet, bis eine Bedingung erfüllt ist, ohne Hook-Konfiguration zu schreiben.
</Tip>

#### Stop-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten Stop-Hooks `stop_hook_active` und `last_assistant_message`. Das Feld `stop_hook_active` ist `true`, wenn Claude Code bereits als Ergebnis eines Stop-Hooks fortgesetzt wird. Überprüfen Sie diesen Wert oder verarbeiten Sie das Transkript, um zu verhindern, dass Claude Code unbegrenzt läuft. Das Feld `last_assistant_message` enthält den Textinhalt von Claudes letzter Antwort, daher können Hooks darauf zugreifen, ohne die Transkript-Datei zu analysieren.

```json theme={null}
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

```json theme={null}
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
| `error`                  | Fehlertyp: `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens` oder `unknown`                                                                                                    |
| `error_details`          | Zusätzliche Details zum Fehler, falls verfügbar                                                                                                                                                                                                                      |
| `last_assistant_message` | Der gerenderte Fehlertext, der in der Konversation angezeigt wird. Im Gegensatz zu `Stop` und `SubagentStop`, wo dieses Feld Claudes Gesprächsausgabe enthält, enthält es für `StopFailure` die API-Fehlerzeichenkette selbst, wie `"API Error: Rate limit reached"` |

```json theme={null}
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

```json theme={null}
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

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
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

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/audit-config-change.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

#### ConfigChange-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten ConfigChange-Hooks `source` und optional `file_path`. Das Feld `source` gibt an, welche Konfigurationsart sich geändert hat, und `file_path` gibt den Pfad zur spezifischen Datei an, die geändert wurde.

```json theme={null}
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

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings`-Änderungen können nicht blockiert werden. Hooks werden immer noch für `policy_settings`-Quellen ausgelöst, daher können Sie sie für Audit-Protokollierung verwenden, aber jede Blockierungsentscheidung wird ignoriert. Dies stellt sicher, dass von Unternehmen verwaltete Einstellungen immer wirksam werden.

### CwdChanged

Wird ausgeführt, wenn das Arbeitsverzeichnis während einer Sitzung wechselt, zum Beispiel wenn Claude einen `cd`-Befehl ausführt. Verwenden Sie dies, um auf Verzeichniswechsel zu reagieren: Laden Sie Umgebungsvariablen neu, aktivieren Sie projektspezifische Toolchains oder führen Sie Setup-Skripte automatisch aus. Paare mit [FileChanged](#filechanged) für Tools wie [direnv](https://direnv.net/), die verzeichnisspezifische Umgebungen verwalten.

CwdChanged-Hooks haben Zugriff auf `CLAUDE_ENV_FILE`. Variablen, die in diese Datei geschrieben werden, bleiben in nachfolgenden Bash-Befehlen für die Sitzung erhalten, genau wie in [SessionStart-Hooks](#persist-environment-variables).

CwdChanged unterstützt keine Matcher und wird bei jedem Verzeichniswechsel ausgelöst.

#### CwdChanged-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten CwdChanged-Hooks `old_cwd` und `new_cwd`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### CwdChanged-Ausgabe

Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, können CwdChanged-Hooks `watchPaths` zurückgeben, um dynamisch zu setzen, welche Dateipfade [FileChanged](#filechanged) überwacht:

| Feld         | Beschreibung                                                                                                                                                                                                                                                              |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `watchPaths` | Array von absoluten Pfaden. Ersetzt die aktuelle dynamische Überwachungsliste (Pfade aus Ihrer `matcher`-Konfiguration werden immer überwacht). Das Zurückgeben eines leeren Arrays löscht die dynamische Liste, was typisch ist, wenn Sie ein neues Verzeichnis betreten |

CwdChanged-Hooks haben keine Entscheidungskontrolle. Sie können den Verzeichniswechsel nicht blockieren.

### FileChanged

Wird ausgeführt, wenn sich eine überwachte Datei auf der Festplatte ändert. Nützlich zum Neuladen von Umgebungsvariablen, wenn Projekt-Konfigurationsdateien geändert werden.

Das Feld `matcher` für dieses Ereignis dient zwei Zwecken:

* **Erstellen Sie die Überwachungsliste**: Der Wert wird auf `|` aufgeteilt und jedes Segment wird als Dateiname im Arbeitsverzeichnis registriert, daher überwacht `".envrc|.env"` genau diese zwei Dateien. Regex-Muster sind hier nicht nützlich: Ein Wert wie `^\.env` würde eine Datei überwachen, die buchstäblich `^\.env` heißt.
* **Filtern Sie, welche Hooks ausgeführt werden**: Wenn sich eine überwachte Datei ändert, wird der gleiche Wert verwendet, um zu filtern, welche Hook-Gruppen ausgeführt werden, wobei die Standard-[Matcher-Regeln](#matcher-patterns) gegen den Basename der geänderten Datei verwendet werden.

FileChanged-Hooks haben Zugriff auf `CLAUDE_ENV_FILE`. Variablen, die in diese Datei geschrieben werden, bleiben in nachfolgenden Bash-Befehlen für die Sitzung erhalten, genau wie in [SessionStart-Hooks](#persist-environment-variables).

#### FileChanged-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten FileChanged-Hooks `file_path` und `event`.

| Feld        | Beschreibung                                                                                             |
| :---------- | :------------------------------------------------------------------------------------------------------- |
| `file_path` | Absoluter Pfad zur Datei, die sich geändert hat                                                          |
| `event`     | Was passiert ist: `"change"` (Datei geändert), `"add"` (Datei erstellt) oder `"unlink"` (Datei gelöscht) |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### FileChanged-Ausgabe

Zusätzlich zu den [JSON-Ausgabefeldern](#json-output), die für alle Hooks verfügbar sind, können FileChanged-Hooks `watchPaths` zurückgeben, um dynamisch zu aktualisieren, welche Dateipfade überwacht werden:

| Feld         | Beschreibung                                                                                                                                                                                                                                                            |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Array von absoluten Pfaden. Ersetzt die aktuelle dynamische Überwachungsliste (Pfade aus Ihrer `matcher`-Konfiguration werden immer überwacht). Verwenden Sie dies, wenn Ihr Hook-Skript basierend auf der geänderten Datei zusätzliche Dateien zum Überwachen entdeckt |

FileChanged-Hooks haben keine Entscheidungskontrolle. Sie können die Dateiänderung nicht blockieren.

### WorktreeCreate

Wenn Sie `claude --worktree` ausführen oder ein [Subagent `isolation: "worktree"` verwendet](/de/sub-agents#choose-the-subagent-scope), erstellt Claude Code eine isolierte Arbeitskopie mit `git worktree`. Wenn Sie einen WorktreeCreate-Hook konfigurieren, ersetzt er das Standard-Git-Verhalten und ermöglicht es Ihnen, ein anderes Versionskontrollsystem wie SVN, Perforce oder Mercurial zu verwenden.

Da der Hook das Standard-Verhalten vollständig ersetzt, wird [`.worktreeinclude`](/de/worktrees#copy-gitignored-files-into-worktrees) nicht verarbeitet. Wenn Sie lokale Konfigurationsdateien wie `.env` in den neuen Worktree kopieren müssen, tun Sie dies in Ihrem Hook-Skript.

Der Hook muss den absoluten Pfad zum erstellten Worktree-Verzeichnis zurückgeben. Claude Code verwendet diesen Pfad als Arbeitsverzeichnis für die isolierte Sitzung. Command-Hooks geben ihn auf stdout aus; HTTP-Hooks geben ihn über `hookSpecificOutput.worktreePath` zurück.

Dieses Beispiel erstellt eine SVN-Arbeitskopie und gibt den Pfad aus, damit Claude Code ihn verwenden kann. Ersetzen Sie die Repository-URL durch Ihre eigene:

```json theme={null}
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

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate-Ausgabe

WorktreeCreate-Hooks verwenden nicht das Standard-Allow/Block-Entscheidungsmodell. Stattdessen bestimmt der Erfolg oder Misserfolg des Hooks das Ergebnis. Der Hook muss den absoluten Pfad zum erstellten Worktree-Verzeichnis zurückgeben:

* **Command-Hooks** (`type: "command"`): geben den Pfad auf stdout aus.
* **HTTP-Hooks** (`type: "http"`): geben `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` im Response-Body zurück.

Wenn der Hook fehlschlägt oder keinen Pfad erzeugt, schlägt die Worktree-Erstellung mit einem Fehler fehl.

### WorktreeRemove

Das Bereinigungspendant zu [WorktreeCreate](#worktreecreate). Dieser Hook wird ausgelöst, wenn ein Worktree entfernt wird, entweder wenn Sie eine `--worktree`-Sitzung beenden und wählen, sie zu entfernen, oder wenn ein Subagent mit `isolation: "worktree"` fertig ist. Für Git-basierte Worktrees handhabt Claude die Bereinigung automatisch mit `git worktree remove`. Wenn Sie einen WorktreeCreate-Hook für ein nicht-Git-Versionskontrollsystem konfiguriert haben, koppeln Sie ihn mit einem WorktreeRemove-Hook, um die Bereinigung zu handhaben. Ohne einen wird das Worktree-Verzeichnis auf der Festplatte belassen.

Claude Code übergibt den Pfad, den WorktreeCreate auf stdout ausgegeben hat, als `worktree_path` in der Hook-Eingabe. Dieses Beispiel liest diesen Pfad und entfernt das Verzeichnis:

```json theme={null}
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

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove-Hooks haben keine Entscheidungskontrolle. Sie können die Worktree-Entfernung nicht blockieren, können aber Bereinigungsaufgaben wie das Entfernen von Versionskontrollstatus oder das Archivieren von Änderungen durchführen. Hook-Fehler werden nur im Debug-Modus protokolliert.

### PreCompact

Wird ausgeführt, bevor Claude Code einen Komprimierungsvorgang ausführen soll.

Der Matcher-Wert gibt an, ob die Komprimierung manuell oder automatisch ausgelöst wurde:

| Matcher  | Wann es ausgelöst wird                               |
| :------- | :--------------------------------------------------- |
| `manual` | `/compact`                                           |
| `auto`   | Auto-Komprimierung, wenn das Kontextfenster voll ist |

Exit mit Code 2, um die Komprimierung zu blockieren. Für ein manuelles `/compact` wird die stderr-Nachricht dem Benutzer angezeigt. Sie können auch blockieren, indem Sie JSON mit `"decision": "block"` zurückgeben.

Das Blockieren der automatischen Komprimierung hat unterschiedliche Auswirkungen, je nachdem, wann es ausgelöst wird. Wenn die Komprimierung proaktiv ausgelöst wurde, bevor das Kontextlimit erreicht wurde, überspringt Claude Code sie und das Gespräch wird unkomprimiert fortgesetzt. Wenn die Komprimierung ausgelöst wurde, um sich von einem Kontextlimit-Fehler zu erholen, der bereits von der API zurückgegeben wurde, wird der zugrunde liegende Fehler angezeigt und die aktuelle Anfrage schlägt fehl.

#### PreCompact-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten PreCompact-Hooks `trigger` und `custom_instructions`. Für `manual` enthält `custom_instructions` das, was der Benutzer in `/compact` übergibt. Für `auto` ist `custom_instructions` leer.

```json theme={null}
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

```json theme={null}
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

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd-Hooks haben keine Entscheidungskontrolle. Sie können die Sitzungsbeendigung nicht blockieren, können aber Bereinigungsaufgaben durchführen.

SessionEnd-Hooks haben ein Standard-Timeout von 1,5 Sekunden. Dies gilt sowohl für den Sitzungsausstieg als auch für `/clear` und das Wechseln von Sitzungen über interaktives `/resume`. Wenn ein Hook mehr Zeit benötigt, setzen Sie eine Pro-Hook-`timeout` in der Hook-Konfiguration. Das Gesamtbudget wird automatisch auf das höchste Pro-Hook-Timeout erhöht, das in Einstellungsdateien konfiguriert ist, bis zu 60 Sekunden. Timeouts, die auf Plugin-bereitgestellten Hooks gesetzt sind, erhöhen das Budget nicht. Um das Budget explizit zu überschreiben, setzen Sie die Umgebungsvariable `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` in Millisekunden.

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

Wird ausgeführt, wenn ein MCP-Server Benutzereingaben während einer Aufgabe anfordert. Standardmäßig zeigt Claude Code einen interaktiven Dialog für die Benutzerantwort an. Hooks können diese Anfrage abfangen und programmatisch antworten, wodurch der Dialog vollständig übersprungen wird.

Das Matcher-Feld passt auf den MCP-Server-Namen.

#### Elicitation-Eingabe

Zusätzlich zu den [gemeinsamen Eingabefeldern](#common-input-fields) erhalten Elicitation-Hooks `mcp_server_name`, `message` und optionale Felder `mode`, `url`, `elicitation_id` und `requested_schema`.

Für Form-Mode-Elicitation (der häufigste Fall):

```json theme={null}
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

```json theme={null}
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

```json theme={null}
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

```json theme={null}
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

```json theme={null}
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

Exit-Code 2 blockiert die Antwort, wodurch die effektive Aktion zu `decline` wird.

## Prompt-basierte Hooks

Zusätzlich zu Command-, HTTP- und MCP-Tool-Hooks unterstützt Claude Code Prompt-basierte Hooks (`type: "prompt"`), die ein LLM verwenden, um zu evaluieren, ob eine Aktion zuzulassen oder zu blockieren ist, und Agent-Hooks (`type: "agent"`), die einen agentengesteuerten Verifizierer mit Tool-Zugriff spawnen. Nicht alle Ereignisse unterstützen jeden Hook-Typ.

Ereignisse, die alle fünf Hook-Typen unterstützen (`command`, `http`, `mcp_tool`, `prompt` und `agent`):

* `PermissionRequest`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `UserPromptExpansion`
* `UserPromptSubmit`

Ereignisse, die `command`, `http` und `mcp_tool` Hooks unterstützen, aber nicht `prompt` oder `agent`:

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PermissionDenied`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` und `Setup` unterstützen `command` und `mcp_tool` Hooks. Sie unterstützen keine `http`, `prompt` oder `agent` Hooks.

### Wie Prompt-basierte Hooks funktionieren

Anstatt einen Bash-Befehl auszuführen, Prompt-basierte Hooks:

1. Senden die Hook-Eingabe und Ihren Prompt an ein Claude-Modell, standardmäßig Haiku
2. Das LLM antwortet mit strukturiertem JSON, das eine Entscheidung enthält
3. Claude Code verarbeitet die Entscheidung automatisch

### Prompt-Hook-Konfiguration

Setzen Sie `type` auf `"prompt"` und geben Sie eine `prompt`-Zeichenkette anstelle eines `command` an. Verwenden Sie den Platzhalter `$ARGUMENTS`, um die Hook-Eingabedaten in Ihren Prompt-Text einzufügen. Claude Code sendet den kombinierten Prompt und die Eingabe an ein schnelles Claude-Modell, das eine JSON-Entscheidung zurückgibt.

Dieser `Stop`-Hook fragt das LLM, ob Claude stoppen sollte, bevor Claude beendet wird:

```json theme={null}
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

| Feld              | Erforderlich | Beschreibung                                                                                                                                                                                                                                                                                                     |
| :---------------- | :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`            | ja           | Muss `"prompt"` sein                                                                                                                                                                                                                                                                                             |
| `prompt`          | ja           | Der Prompt-Text zum Senden an das LLM. Verwenden Sie `$ARGUMENTS` als Platzhalter für die Hook-Eingabe JSON. Wenn `$ARGUMENTS` nicht vorhanden ist, wird die Eingabe JSON an den Prompt angehängt                                                                                                                |
| `model`           | nein         | Modell zur Verwendung für die Evaluierung. Standardwert ist ein schnelles Modell                                                                                                                                                                                                                                 |
| `timeout`         | nein         | Timeout in Sekunden. Standard: 30                                                                                                                                                                                                                                                                                |
| `continueOnBlock` | nein         | Wenn der Prompt `ok: false` zurückgibt, wird der Grund an Claude zurückgegeben und der Turn wird fortgesetzt, anstatt zu stoppen. Standard: `false`. Implementiert als `continue: true` auf der resultierenden `decision: "block"`. Siehe [Response-Schema](#response-schema) für ereignisspezifisches Verhalten |

### Response-Schema

Das LLM muss mit JSON antworten, das Folgendes enthält:

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Feld     | Beschreibung                                                                                                       |
| :------- | :----------------------------------------------------------------------------------------------------------------- |
| `ok`     | `true` erlaubt die Aktion. `false` erzeugt eine `decision: "block"`. Siehe das ereignisspezifische Verhalten unten |
| `reason` | Erforderlich, wenn `ok` `false` ist. Wird als Blockierungsgrund verwendet                                          |

Was bei `ok: false` passiert, hängt vom Ereignis ab:

* `Stop` und `SubagentStop`: der Grund wird an Claude als nächste Anweisung zurückgegeben und der Turn wird fortgesetzt
* `PreToolUse`: der Tool-Aufruf wird verweigert und der Grund wird an Claude als Tool-Fehler zurückgegeben, gleichbedeutend mit einem Command-Hook mit `permissionDecision: "deny"`
* `PostToolUse`: standardmäßig endet der Turn und der Grund wird im Chat als Warnzeile angezeigt. Setzen Sie `continueOnBlock: true`, um den Grund an Claude zurückzugeben und den Turn stattdessen fortzusetzen
* `PostToolBatch`, `UserPromptSubmit` und `UserPromptExpansion`: der Turn endet und der Grund wird als Warnzeile angezeigt. Diese Ereignisse beenden den Turn bei `decision: "block"` unabhängig von `continue`
* `PostToolUseFailure`, `TaskCreated` und `TaskCompleted`: der Grund wird an Claude als Tool-Fehler zurückgegeben, ähnlich wie `PreToolUse`
* `PermissionRequest`: `ok: false` hat keine Auswirkung. Um eine Genehmigung von einem Hook zu verweigern, verwenden Sie einen [Command-Hook](#command-hook-fields) mit `hookSpecificOutput.decision.behavior: "deny"`

Wenn Sie eine feinere Kontrolle bei einem Ereignis benötigen, verwenden Sie einen [Command-Hook](#command-hook-fields) mit den ereignisspezifischen Feldern, die in [Entscheidungskontrolle](#decision-control) beschrieben sind.

### Beispiel: Multi-Kriterien-Stop-Hook

Dieser `Stop`-Hook verwendet einen detaillierten Prompt, um drei Bedingungen zu überprüfen, bevor Claude stoppen darf. Wenn `"ok"` `false` ist, setzt Claude die Arbeit mit dem bereitgestellten Grund als nächste Anweisung fort. `SubagentStop`-Hooks verwenden das gleiche Format, um zu evaluieren, ob ein [Subagent](/de/sub-agents) stoppen sollte:

```json theme={null}
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

<Warning>
  Agent-Hooks sind experimentell. Das Verhalten und die Konfiguration können sich in zukünftigen Versionen ändern. Für Produktions-Workflows bevorzugen Sie [Command Hooks](#command-hook-fields).
</Warning>

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

```json theme={null}
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

```json theme={null}
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

Nachdem der Hintergrund-Prozess beendet ist, wenn der Hook eine JSON-Response mit einem `additionalContext`-Feld erzeugt hat, wird dieser Inhalt Claude beim nächsten Gesprächsturn als Kontext geliefert. Ein `systemMessage`-Feld wird Ihnen angezeigt, nicht Claude.

Benachrichtigungen über den Abschluss asynchroner Hooks werden standardmäßig unterdrückt. Um sie zu sehen, aktivieren Sie den ausführlichen Modus mit `Ctrl+O` oder starten Sie Claude Code mit `--verbose`.

### Beispiel: Tests nach Dateiänderungen ausführen

Dieser Hook startet eine Test-Suite im Hintergrund, wenn Claude eine Datei schreibt, und meldet die Ergebnisse Claude, wenn die Tests fertig sind. Speichern Sie dieses Skript unter `.claude/hooks/run-tests-async.sh` in Ihrem Projekt und machen Sie es mit `chmod +x` ausführbar:

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# Hook-Eingabe von stdin lesen
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Tests nur für Quelldateien ausführen
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Tests ausführen und Ergebnisse über additionalContext an Claude melden
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  MSG="Tests passed after editing $FILE_PATH"
else
  MSG="Tests failed after editing $FILE_PATH: $RESULT"
fi
jq -nc --arg msg "$MSG" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
```

Fügen Sie dann diese Konfiguration zu `.claude/settings.json` im Projekt-Root hinzu. Das Flag `async: true` ermöglicht es Claude, weiterarbeiten zu können, während Tests ausgeführt werden:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/run-tests-async.sh",
            "args": [],
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
* Hook-Ausgabe wird beim nächsten Gesprächsturn geliefert. Wenn die Sitzung untätig ist, wartet die Response, bis die nächste Benutzerinteraktion erfolgt. Ausnahme: Ein `asyncRewake`-Hook, der mit Code 2 beendet wird, weckt Claude sofort auf, auch wenn die Sitzung untätig ist.
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
* **Verwenden Sie absolute Pfade**: Geben Sie vollständige Pfade für Skripte an. In der Exec-Form verwenden Sie `${CLAUDE_PROJECT_DIR}` und der Pfad benötigt keine Anführungszeichen. In der Shell-Form wickeln Sie ihn in doppelte Anführungszeichen ein
* **Überspringen Sie sensible Dateien**: Vermeiden Sie `.env`, `.git/`, Schlüssel, etc.

## Windows PowerShell-Tool

Unter Windows können Sie einzelne Hooks in PowerShell ausführen, indem Sie `"shell": "powershell"` auf einem Command-Hook setzen. Hooks spawnen PowerShell direkt, daher funktioniert dies unabhängig davon, ob `CLAUDE_CODE_USE_POWERSHELL_TOOL` gesetzt ist. Claude Code erkennt automatisch `pwsh.exe` (PowerShell 7+) mit einem Fallback auf `powershell.exe` (5.1).

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

## Debug-Hooks

Hook-Ausführungsdetails, einschließlich welche Hooks passten, ihre Exit-Codes und vollständige stdout und stderr, werden in die Debug-Log-Datei geschrieben. Starten Sie Claude Code mit `claude --debug-file <path>`, um das Log in einen bekannten Speicherort zu schreiben, oder führen Sie `claude --debug` aus und lesen Sie das Log unter `~/.claude/debug/<session-id>.txt`. Das Flag `--debug` gibt nicht auf dem Terminal aus.

```text theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Für granularere Hook-Matching-Details setzen Sie `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose`, um zusätzliche Log-Zeilen wie Hook-Matcher-Zählungen und Query-Matching zu sehen.

Zur Fehlerbehebung häufiger Probleme wie Hooks, die nicht ausgelöst werden, unendliche Stop-Hook-Schleifen oder Konfigurationsfehler, siehe [Einschränkungen und Fehlerbehebung](/de/hooks-guide#limitations-and-troubleshooting) in der Anleitung. Für eine umfassendere diagnostische Anleitung, die `/context`, `/doctor` und Einstellungspriorität abdeckt, siehe [Debug your config](/de/debug-your-config).
