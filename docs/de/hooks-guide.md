> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatisieren Sie Workflows mit Hooks

> Führen Sie Shell-Befehle automatisch aus, wenn Claude Code Dateien bearbeitet, Aufgaben abschließt oder Eingaben benötigt. Formatieren Sie Code, senden Sie Benachrichtigungen, validieren Sie Befehle und erzwingen Sie Projektregeln.

Hooks sind benutzerdefinierte Shell-Befehle, die an bestimmten Punkten im Lebenszyklus von Claude Code ausgeführt werden. Sie bieten deterministische Kontrolle über das Verhalten von Claude Code und stellen sicher, dass bestimmte Aktionen immer stattfinden, anstatt sich darauf zu verlassen, dass das LLM sie ausführt. Verwenden Sie Hooks, um Projektregeln durchzusetzen, sich wiederholende Aufgaben zu automatisieren und Claude Code mit Ihren vorhandenen Tools zu integrieren.

Für Entscheidungen, die Urteilsvermögen erfordern, anstatt deterministischer Regeln, können Sie auch [Prompt-basierte Hooks](#prompt-based-hooks) oder [Agent-basierte Hooks](#agent-based-hooks) verwenden, die ein Claude-Modell zur Bewertung von Bedingungen nutzen.

Für andere Möglichkeiten, Claude Code zu erweitern, siehe [skills](/de/skills) zum Geben zusätzlicher Anweisungen und ausführbarer Befehle, [subagents](/de/sub-agents) zum Ausführen von Aufgaben in isolierten Kontexten und [plugins](/de/plugins) zum Verpacken von Erweiterungen, die über Projekte hinweg freigegeben werden können.

<Tip>
  Dieser Leitfaden behandelt häufige Anwendungsfälle und wie Sie beginnen. Für vollständige Event-Schemas, JSON-Ein-/Ausgabeformate und erweiterte Funktionen wie asynchrone Hooks und MCP-Tool-Hooks siehe die [Hooks-Referenz](/de/hooks).
</Tip>

## Richten Sie Ihren ersten Hook ein

Der schnellste Weg, einen Hook zu erstellen, ist über das interaktive Menü `/hooks` in Claude Code. Diese Anleitung erstellt einen Desktop-Benachrichtigungs-Hook, damit Sie benachrichtigt werden, wenn Claude auf Ihre Eingabe wartet, anstatt das Terminal zu beobachten.

<Steps>
  <Step title="Öffnen Sie das Hooks-Menü">
    Geben Sie `/hooks` in die Claude Code CLI ein. Sie sehen eine Liste aller verfügbaren Hook-Events sowie eine Option zum Deaktivieren aller Hooks. Jedes Event entspricht einem Punkt im Lebenszyklus von Claude, an dem Sie benutzerdefinierten Code ausführen können. Wählen Sie `Notification` aus, um einen Hook zu erstellen, der aktiviert wird, wenn Claude Ihre Aufmerksamkeit benötigt.
  </Step>

  <Step title="Konfigurieren Sie den Matcher">
    Das Menü zeigt eine Liste von Matchern, die filtern, wann der Hook aktiviert wird. Setzen Sie den Matcher auf `*`, um bei allen Benachrichtigungstypen aktiviert zu werden. Sie können ihn später eingrenzen, indem Sie den Matcher auf einen bestimmten Wert wie `permission_prompt` oder `idle_prompt` ändern.
  </Step>

  <Step title="Fügen Sie Ihren Befehl hinzu">
    Wählen Sie `+ Add new hook…`. Das Menü fordert Sie auf, einen Shell-Befehl einzugeben, der ausgeführt wird, wenn das Event aktiviert wird. Hooks führen jeden Shell-Befehl aus, den Sie bereitstellen, sodass Sie das integrierte Benachrichtigungstool Ihrer Plattform verwenden können. Kopieren Sie den Befehl für Ihr Betriebssystem:

    <Tabs>
      <Tab title="macOS">
        Verwendet [`osascript`](https://ss64.com/mac/osascript.html), um eine native macOS-Benachrichtigung über AppleScript auszulösen:

        ```bash  theme={null}
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Verwendet `notify-send`, das auf den meisten Linux-Desktops mit einem Benachrichtigungsdaemon vorinstalliert ist:

        ```bash  theme={null}
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Verwendet PowerShell, um ein natives Meldungsfeld über .NET Windows Forms anzuzeigen:

        ```powershell  theme={null}
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Wählen Sie einen Speicherort">
    Das Menü fragt, wo die Hook-Konfiguration gespeichert werden soll. Wählen Sie `User settings` aus, um sie in `~/.claude/settings.json` zu speichern, was den Hook auf alle Ihre Projekte anwendet. Sie könnten auch `Project settings` wählen, um ihn auf das aktuelle Projekt zu beschränken. Siehe [Hook-Speicherort konfigurieren](#configure-hook-location) für alle verfügbaren Bereiche.
  </Step>

  <Step title="Testen Sie den Hook">
    Drücken Sie `Esc`, um zur CLI zurückzukehren. Bitten Sie Claude, etwas zu tun, das eine Berechtigung erfordert, und wechseln Sie dann weg vom Terminal. Sie sollten eine Desktop-Benachrichtigung erhalten.
  </Step>
</Steps>

## Was Sie automatisieren können

Hooks ermöglichen es Ihnen, Code an Schlüsselpunkten im Lebenszyklus von Claude Code auszuführen: Dateien nach Bearbeitungen formatieren, Befehle vor der Ausführung blockieren, Benachrichtigungen senden, wenn Claude Eingaben benötigt, Kontext beim Sitzungsstart injizieren und vieles mehr. Für die vollständige Liste der Hook-Events siehe die [Hooks-Referenz](/de/hooks#hook-lifecycle).

Jedes Beispiel enthält einen einsatzbereiten Konfigurationsblock, den Sie einer [Einstellungsdatei](#configure-hook-location) hinzufügen. Die häufigsten Muster:

* [Benachrichtigung erhalten, wenn Claude Eingaben benötigt](#get-notified-when-claude-needs-input)
* [Code nach Bearbeitungen automatisch formatieren](#auto-format-code-after-edits)
* [Bearbeitungen geschützter Dateien blockieren](#block-edits-to-protected-files)
* [Kontext nach Komprimierung erneut injizieren](#re-inject-context-after-compaction)
* [Konfigurationsänderungen prüfen](#audit-configuration-changes)

### Benachrichtigung erhalten, wenn Claude Eingaben benötigt

Erhalten Sie eine Desktop-Benachrichtigung, wenn Claude die Arbeit beendet und Ihre Eingabe benötigt, damit Sie zu anderen Aufgaben wechseln können, ohne das Terminal zu überprüfen.

Dieser Hook verwendet das `Notification`-Event, das aktiviert wird, wenn Claude auf Eingaben oder Berechtigungen wartet. Jede Registerkarte unten verwendet den nativen Benachrichtigungsbefehl der Plattform. Fügen Sie dies zu `~/.claude/settings.json` hinzu, oder verwenden Sie die [interaktive Anleitung](#set-up-your-first-hook) oben, um es mit `/hooks` zu konfigurieren:

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### Code nach Bearbeitungen automatisch formatieren

Führen Sie [Prettier](https://prettier.io/) automatisch auf jeder Datei aus, die Claude bearbeitet, damit die Formatierung konsistent bleibt, ohne manuelle Eingriffe.

Dieser Hook verwendet das `PostToolUse`-Event mit einem `Edit|Write`-Matcher, sodass er nur nach Datei-Bearbeitungs-Tools ausgeführt wird. Der Befehl extrahiert den bearbeiteten Dateipfad mit [`jq`](https://jqlang.github.io/jq/) und übergibt ihn an Prettier. Fügen Sie dies zu `.claude/settings.json` in Ihrem Projektverzeichnis hinzu:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  Die Bash-Beispiele auf dieser Seite verwenden `jq` zum JSON-Parsing. Installieren Sie es mit `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), oder siehe [`jq`-Downloads](https://jqlang.github.io/jq/download/).
</Note>

### Bearbeitungen geschützter Dateien blockieren

Verhindern Sie, dass Claude sensible Dateien wie `.env`, `package-lock.json` oder alles in `.git/` ändert. Claude erhält Feedback, das erklärt, warum die Bearbeitung blockiert wurde, sodass es seinen Ansatz anpassen kann.

Dieses Beispiel verwendet eine separate Skriptdatei, die der Hook aufruft. Das Skript überprüft den Zieldateipfad gegen eine Liste geschützter Muster und beendet sich mit Code 2, um die Bearbeitung zu blockieren.

<Steps>
  <Step title="Erstellen Sie das Hook-Skript">
    Speichern Sie dies unter `.claude/hooks/protect-files.sh`:

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="Machen Sie das Skript ausführbar (macOS/Linux)">
    Hook-Skripte müssen ausführbar sein, damit Claude Code sie ausführen kann:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Registrieren Sie den Hook">
    Fügen Sie einen `PreToolUse`-Hook zu `.claude/settings.json` hinzu, der das Skript vor jedem `Edit`- oder `Write`-Tool-Aufruf ausführt:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### Kontext nach Komprimierung erneut injizieren

Wenn Claudes Kontextfenster voll wird, fasst die Komprimierung das Gespräch zusammen, um Platz freizugeben. Dies kann wichtige Details verlieren. Verwenden Sie einen `SessionStart`-Hook mit einem `compact`-Matcher, um nach jeder Komprimierung kritischen Kontext erneut zu injizieren.

Jeder Text, den Ihr Befehl auf stdout schreibt, wird zu Claudes Kontext hinzugefügt. Dieses Beispiel erinnert Claude an Projektkonventionen und aktuelle Arbeiten. Fügen Sie dies zu `.claude/settings.json` in Ihrem Projektverzeichnis hinzu:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

Sie können das `echo` durch jeden Befehl ersetzen, der dynamische Ausgabe erzeugt, wie `git log --oneline -5`, um aktuelle Commits anzuzeigen. Zum Injizieren von Kontext bei jedem Sitzungsstart sollten Sie stattdessen [CLAUDE.md](/de/memory) verwenden. Für Umgebungsvariablen siehe [`CLAUDE_ENV_FILE`](/de/hooks#persist-environment-variables) in der Referenz.

### Konfigurationsänderungen prüfen

Verfolgen Sie, wenn sich Einstellungs- oder Skills-Dateien während einer Sitzung ändern. Das `ConfigChange`-Event wird aktiviert, wenn ein externer Prozess oder Editor eine Konfigurationsdatei ändert, sodass Sie Änderungen für Compliance protokollieren oder nicht autorisierte Änderungen blockieren können.

Dieses Beispiel hängt jede Änderung an ein Audit-Protokoll an. Fügen Sie dies zu `~/.claude/settings.json` hinzu:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

Der Matcher filtert nach Konfigurationstyp: `user_settings`, `project_settings`, `local_settings`, `policy_settings` oder `skills`. Um eine Änderung zu blockieren, beenden Sie mit Code 2 oder geben Sie `{"decision": "block"}` zurück. Siehe die [ConfigChange-Referenz](/de/hooks#configchange) für das vollständige Eingabe-Schema.

## Wie Hooks funktionieren

Hook-Events werden an bestimmten Lebenszykluspunkten in Claude Code aktiviert. Wenn ein Event aktiviert wird, werden alle übereinstimmenden Hooks parallel ausgeführt, und identische Hook-Befehle werden automatisch dedupliziert. Die folgende Tabelle zeigt jedes Event und wann es ausgelöst wird:

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

Jeder Hook hat einen `type`, der bestimmt, wie er ausgeführt wird. Die meisten Hooks verwenden `"type": "command"`, was einen Shell-Befehl ausführt. Drei weitere Typen sind verfügbar:

* `"type": "http"`: POST-Event-Daten an eine URL. Siehe [HTTP-Hooks](#http-hooks).
* `"type": "prompt"`: Single-Turn-LLM-Bewertung. Siehe [Prompt-basierte Hooks](#prompt-based-hooks).
* `"type": "agent"`: Multi-Turn-Verifizierung mit Tool-Zugriff. Siehe [Agent-basierte Hooks](#agent-based-hooks).

### Eingabe lesen und Ausgabe zurückgeben

Hooks kommunizieren mit Claude Code über stdin, stdout, stderr und Exit-Codes. Wenn ein Event aktiviert wird, übergibt Claude Code ereignisspezifische Daten als JSON an stdin Ihres Skripts. Ihr Skript liest diese Daten, führt seine Arbeit aus und teilt Claude Code mit, was als nächstes zu tun ist, über den Exit-Code.

#### Hook-Eingabe

Jedes Event enthält gemeinsame Felder wie `session_id` und `cwd`, aber jeder Event-Typ fügt unterschiedliche Daten hinzu. Wenn Claude beispielsweise einen Bash-Befehl ausführt, erhält ein `PreToolUse`-Hook etwa folgendes auf stdin:

```json  theme={null}
{
  "session_id": "abc123",          // unique ID for this session
  "cwd": "/Users/sarah/myproject", // working directory when the event fired
  "hook_event_name": "PreToolUse", // which event triggered this hook
  "tool_name": "Bash",             // the tool Claude is about to use
  "tool_input": {                  // the arguments Claude passed to the tool
    "command": "npm test"          // for Bash, this is the shell command
  }
}
```

Ihr Skript kann dieses JSON analysieren und auf alle diese Felder reagieren. `UserPromptSubmit`-Hooks erhalten stattdessen den `prompt`-Text, `SessionStart`-Hooks erhalten die `source` (startup, resume, clear, compact) und so weiter. Siehe [Gemeinsame Eingabefelder](/de/hooks#common-input-fields) in der Referenz für gemeinsame Felder und jeden Event-Abschnitt für ereignisspezifische Schemas.

#### Hook-Ausgabe

Ihr Skript teilt Claude Code mit, was als nächstes zu tun ist, indem es auf stdout oder stderr schreibt und mit einem bestimmten Code beendet wird. Beispielsweise ein `PreToolUse`-Hook, der einen Befehl blockieren möchte:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr becomes Claude's feedback
  exit 2 # exit 2 = block the action
fi

exit 0  # exit 0 = let it proceed
```

Der Exit-Code bestimmt, was als nächstes passiert:

* **Exit 0**: Die Aktion wird fortgesetzt. Für `UserPromptSubmit`- und `SessionStart`-Hooks wird alles, was Sie auf stdout schreiben, zu Claudes Kontext hinzugefügt.
* **Exit 2**: Die Aktion wird blockiert. Schreiben Sie einen Grund auf stderr, und Claude erhält ihn als Feedback, sodass er sich anpassen kann.
* **Jeder andere Exit-Code**: Die Aktion wird fortgesetzt. Stderr wird protokolliert, aber nicht Claude angezeigt. Schalten Sie den ausführlichen Modus mit `Ctrl+O` um, um diese Meldungen im Transkript zu sehen.

#### Strukturierte JSON-Ausgabe

Exit-Codes geben Ihnen zwei Optionen: Zulassen oder Blockieren. Für mehr Kontrolle beenden Sie mit 0 und geben stattdessen ein JSON-Objekt auf stdout aus.

<Note>
  Verwenden Sie Exit 2, um mit einer stderr-Meldung zu blockieren, oder Exit 0 mit JSON für strukturierte Kontrolle. Mischen Sie sie nicht: Claude Code ignoriert JSON, wenn Sie mit 2 beenden.
</Note>

Beispielsweise kann ein `PreToolUse`-Hook einen Tool-Aufruf ablehnen und Claude mitteilen, warum, oder ihn dem Benutzer zur Genehmigung eskalieren:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code liest `permissionDecision` und bricht den Tool-Aufruf ab, dann gibt `permissionDecisionReason` an Claude als Feedback zurück. Diese drei Optionen sind spezifisch für `PreToolUse`:

* `"allow"`: Fortfahren ohne Berechtigungsaufforderung anzuzeigen
* `"deny"`: Tool-Aufruf abbrechen und den Grund an Claude senden
* `"ask"`: Berechtigungsaufforderung dem Benutzer wie gewohnt anzeigen

Andere Events verwenden unterschiedliche Entscheidungsmuster. Beispielsweise verwenden `PostToolUse`- und `Stop`-Hooks ein Top-Level-Feld `decision: "block"`, während `PermissionRequest` `hookSpecificOutput.decision.behavior` verwendet. Siehe die [Zusammenfassungstabelle](/de/hooks#decision-control) in der Referenz für eine vollständige Aufschlüsselung nach Event.

Für `UserPromptSubmit`-Hooks verwenden Sie stattdessen `additionalContext`, um Text in Claudes Kontext zu injizieren. Prompt-basierte Hooks (`type: "prompt"`) handhaben die Ausgabe anders: siehe [Prompt-basierte Hooks](#prompt-based-hooks).

### Hooks mit Matchern filtern

Ohne einen Matcher wird ein Hook bei jedem Auftreten seines Events aktiviert. Matcher ermöglichen es Ihnen, das einzugrenzen. Wenn Sie beispielsweise einen Formatter nur nach Datei-Bearbeitungen ausführen möchten (nicht nach jedem Tool-Aufruf), fügen Sie einen Matcher zu Ihrem `PostToolUse`-Hook hinzu:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

Der `"Edit|Write"`-Matcher ist ein Regex-Muster, das den Tool-Namen abgleicht. Der Hook wird nur aktiviert, wenn Claude das `Edit`- oder `Write`-Tool verwendet, nicht wenn es `Bash`, `Read` oder ein anderes Tool verwendet.

Jeder Event-Typ gleicht ein bestimmtes Feld ab. Matcher unterstützen exakte Strings und Regex-Muster:

| Event                                                                                           | Was der Matcher filtert             | Beispiel-Matcher-Werte                                                             |
| :---------------------------------------------------------------------------------------------- | :---------------------------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | Tool-Name                           | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                  | Wie die Sitzung gestartet wurde     | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                    | Warum die Sitzung endete            | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                  | Benachrichtigungstyp                | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                 | Agent-Typ                           | `Bash`, `Explore`, `Plan` oder benutzerdefinierte Agent-Namen                      |
| `PreCompact`                                                                                    | Was die Komprimierung ausgelöst hat | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | Agent-Typ                           | gleiche Werte wie `SubagentStart`                                                  |
| `ConfigChange`                                                                                  | Konfigurationsquelle                | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | Keine Matcher-Unterstützung         | Wird immer bei jedem Auftreten aktiviert                                           |

Ein paar weitere Beispiele, die Matcher auf verschiedene Event-Typen zeigen:

<Tabs>
  <Tab title="Jeden Bash-Befehl protokollieren">
    Gleichen Sie nur `Bash`-Tool-Aufrufe ab und protokollieren Sie jeden Befehl in einer Datei. Das `PostToolUse`-Event wird aktiviert, nachdem der Befehl abgeschlossen ist, sodass `tool_input.command` enthält, was ausgeführt wurde. Der Hook erhält die Event-Daten als JSON auf stdin, und `jq -r '.tool_input.command'` extrahiert nur die Befehlszeichenfolge, die `>>` an die Protokolldatei anhängt:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="MCP-Tools abgleichen">
    MCP-Tools verwenden eine andere Namenskonvention als integrierte Tools: `mcp__<server>__<tool>`, wobei `<server>` der MCP-Servername und `<tool>` das Tool ist, das er bereitstellt. Beispielsweise `mcp__github__search_repositories` oder `mcp__filesystem__read_file`. Verwenden Sie einen Regex-Matcher, um alle Tools von einem bestimmten Server zu erfassen, oder gleichen Sie Server übergreifend mit einem Muster wie `mcp__.*__write.*` ab. Siehe [MCP-Tools abgleichen](/de/hooks#match-mcp-tools) in der Referenz für die vollständige Liste der Beispiele.

    Der folgende Befehl extrahiert den Tool-Namen aus der Hook-JSON-Eingabe mit `jq` und schreibt ihn auf stderr, wo er im ausführlichen Modus (`Ctrl+O`) angezeigt wird:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Beim Sitzungsende aufräumen">
    Das `SessionEnd`-Event unterstützt Matcher auf den Grund, warum die Sitzung endete. Dieser Hook wird nur bei `clear` aktiviert (wenn Sie `/clear` ausführen), nicht bei normalen Exits:

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

Für die vollständige Matcher-Syntax siehe die [Hooks-Referenz](/de/hooks#configuration).

### Hook-Speicherort konfigurieren

Wo Sie einen Hook hinzufügen, bestimmt seinen Bereich:

| Speicherort                                                  | Bereich                                | Freigegeben                           |
| :----------------------------------------------------------- | :------------------------------------- | :------------------------------------ |
| `~/.claude/settings.json`                                    | Alle Ihre Projekte                     | Nein, lokal auf Ihrem Computer        |
| `.claude/settings.json`                                      | Einzelnes Projekt                      | Ja, kann im Repo committed werden     |
| `.claude/settings.local.json`                                | Einzelnes Projekt                      | Nein, gitignoriert                    |
| Verwaltete Richtlinieneinstellungen                          | Organisationsweit                      | Ja, von Admin kontrolliert            |
| [Plugin](/de/plugins) `hooks/hooks.json`                     | Wenn Plugin aktiviert ist              | Ja, mit dem Plugin gebündelt          |
| [Skill](/de/skills) oder [Agent](/de/sub-agents) Frontmatter | Während der Skill oder Agent aktiv ist | Ja, in der Komponentendatei definiert |

Sie können auch das Menü [`/hooks`](/de/hooks#the-hooks-menu) in Claude Code verwenden, um Hooks interaktiv hinzuzufügen, zu löschen und anzuzeigen. Um alle Hooks auf einmal zu deaktivieren, verwenden Sie den Schalter am unteren Ende des Menüs `/hooks` oder setzen Sie `"disableAllHooks": true` in Ihrer Einstellungsdatei.

Hooks, die über das Menü `/hooks` hinzugefügt werden, werden sofort wirksam. Wenn Sie Einstellungsdateien direkt bearbeiten, während Claude Code ausgeführt wird, werden die Änderungen erst wirksam, wenn Sie sie im Menü `/hooks` überprüfen oder Ihre Sitzung neu starten.

## Prompt-basierte Hooks

Für Entscheidungen, die Urteilsvermögen erfordern, anstatt deterministischer Regeln, verwenden Sie `type: "prompt"`-Hooks. Anstatt einen Shell-Befehl auszuführen, sendet Claude Code Ihren Prompt und die Hook-Eingabedaten an ein Claude-Modell (standardmäßig Haiku), um die Entscheidung zu treffen. Sie können ein anderes Modell mit dem Feld `model` angeben, wenn Sie mehr Leistung benötigen.

Die einzige Aufgabe des Modells ist, eine Ja/Nein-Entscheidung als JSON zurückzugeben:

* `"ok": true`: Die Aktion wird fortgesetzt
* `"ok": false`: Die Aktion wird blockiert. Der `"reason"` des Modells wird an Claude zurückgegeben, sodass es sich anpassen kann.

Dieses Beispiel verwendet einen `Stop`-Hook, um das Modell zu fragen, ob alle angeforderten Aufgaben abgeschlossen sind. Wenn das Modell `"ok": false` zurückgibt, arbeitet Claude weiter und verwendet den `reason` als nächste Anweisung:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

Für vollständige Konfigurationsoptionen siehe [Prompt-basierte Hooks](/de/hooks#prompt-based-hooks) in der Referenz.

## Agent-basierte Hooks

Wenn die Verifizierung das Inspizieren von Dateien oder das Ausführen von Befehlen erfordert, verwenden Sie `type: "agent"`-Hooks. Im Gegensatz zu Prompt-Hooks, die einen einzelnen LLM-Aufruf tätigen, spawnen Agent-Hooks einen Subagent, der Dateien lesen, Code durchsuchen und andere Tools verwenden kann, um Bedingungen zu überprüfen, bevor eine Entscheidung zurückgegeben wird.

Agent-Hooks verwenden das gleiche `"ok"` / `"reason"`-Antwortformat wie Prompt-Hooks, aber mit einem längeren Standard-Timeout von 60 Sekunden und bis zu 50 Tool-Use-Turns.

Dieses Beispiel überprüft, dass Tests bestanden werden, bevor Claude beendet werden darf:

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

Verwenden Sie Prompt-Hooks, wenn die Hook-Eingabedaten allein ausreichen, um eine Entscheidung zu treffen. Verwenden Sie Agent-Hooks, wenn Sie etwas gegen den tatsächlichen Zustand der Codebasis überprüfen müssen.

Für vollständige Konfigurationsoptionen siehe [Agent-basierte Hooks](/de/hooks#agent-based-hooks) in der Referenz.

## HTTP-Hooks

Verwenden Sie `type: "http"`-Hooks, um Event-Daten per POST an einen HTTP-Endpunkt zu senden, anstatt einen Shell-Befehl auszuführen. Der Endpunkt erhält die gleichen JSON-Daten, die ein Command-Hook auf stdin erhalten würde, und gibt Ergebnisse über den HTTP-Antwortkörper mit dem gleichen JSON-Format zurück.

HTTP-Hooks sind nützlich, wenn Sie möchten, dass ein Webserver, eine Cloud-Funktion oder ein externer Service die Hook-Logik handhabt: Beispielsweise ein gemeinsamer Audit-Service, der Tool-Use-Events über ein Team hinweg protokolliert.

Dieses Beispiel postet jeden Tool-Use an einen lokalen Logging-Service:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
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

Der Endpunkt sollte einen JSON-Antwortkörper mit dem gleichen [Ausgabeformat](/de/hooks#json-output) wie Command-Hooks zurückgeben. Um einen Tool-Aufruf zu blockieren, geben Sie eine 2xx-Antwort mit den entsprechenden `hookSpecificOutput`-Feldern zurück. HTTP-Statuscodes allein können Aktionen nicht blockieren.

Header-Werte unterstützen Umgebungsvariablen-Interpolation mit `$VAR_NAME` oder `${VAR_NAME}`-Syntax. Nur Variablen, die in der `allowedEnvVars`-Liste aufgeführt sind, werden aufgelöst; alle anderen `$VAR`-Referenzen bleiben leer.

<Note>
  HTTP-Hooks müssen durch direktes Bearbeiten Ihrer Einstellungs-JSON konfiguriert werden. Das interaktive Menü `/hooks` unterstützt nur das Hinzufügen von Command-Hooks.
</Note>

Für vollständige Konfigurationsoptionen und Response-Handling siehe [HTTP-Hooks](/de/hooks#http-hook-fields) in der Referenz.

## Einschränkungen und Fehlerbehebung

### Einschränkungen

* Command-Hooks kommunizieren nur über stdout, stderr und Exit-Codes. Sie können Befehle oder Tool-Aufrufe nicht direkt auslösen. HTTP-Hooks kommunizieren stattdessen über den Response-Body.
* Hook-Timeout beträgt standardmäßig 10 Minuten, konfigurierbar pro Hook mit dem Feld `timeout` (in Sekunden).
* `PostToolUse`-Hooks können Aktionen nicht rückgängig machen, da das Tool bereits ausgeführt wurde.
* `PermissionRequest`-Hooks werden nicht im [nicht-interaktiven Modus](/de/headless) (`-p`) aktiviert. Verwenden Sie `PreToolUse`-Hooks für automatisierte Berechtigungsentscheidungen.
* `Stop`-Hooks werden aktiviert, wenn Claude antwortet, nicht nur bei Aufgabenabschluss. Sie werden nicht bei Benutzerunterbrechungen aktiviert.

### Hook wird nicht aktiviert

Der Hook ist konfiguriert, wird aber nie ausgeführt.

* Führen Sie `/hooks` aus und bestätigen Sie, dass der Hook unter dem richtigen Event angezeigt wird
* Überprüfen Sie, dass das Matcher-Muster den Tool-Namen genau abgleicht (Matcher sind case-sensitiv)
* Überprüfen Sie, dass Sie den richtigen Event-Typ auslösen (z. B. `PreToolUse` wird vor der Tool-Ausführung aktiviert, `PostToolUse` wird danach aktiviert)
* Wenn Sie `PermissionRequest`-Hooks im nicht-interaktiven Modus (`-p`) verwenden, wechseln Sie stattdessen zu `PreToolUse`

### Hook-Fehler in der Ausgabe

Sie sehen eine Meldung wie "PreToolUse hook error: ..." im Transkript.

* Ihr Skript wurde unerwartet mit einem Nicht-Null-Code beendet. Testen Sie es manuell, indem Sie Beispiel-JSON pipen:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* Wenn Sie "command not found" sehen, verwenden Sie absolute Pfade oder `$CLAUDE_PROJECT_DIR`, um Skripte zu referenzieren
* Wenn Sie "jq: command not found" sehen, installieren Sie `jq` oder verwenden Sie Python/Node.js zum JSON-Parsing
* Wenn das Skript überhaupt nicht ausgeführt wird, machen Sie es ausführbar: `chmod +x ./my-hook.sh`

### `/hooks` zeigt keine konfigurierten Hooks

Sie haben eine Einstellungsdatei bearbeitet, aber die Hooks werden nicht im Menü angezeigt.

* Starten Sie Ihre Sitzung neu oder öffnen Sie `/hooks`, um neu zu laden. Hooks, die über das Menü `/hooks` hinzugefügt werden, werden sofort wirksam, aber manuelle Datei-Bearbeitungen erfordern ein Neuladen.
* Überprüfen Sie, dass Ihr JSON gültig ist (nachfolgende Kommas und Kommentare sind nicht zulässig)
* Bestätigen Sie, dass die Einstellungsdatei am richtigen Speicherort ist: `.claude/settings.json` für Projekt-Hooks, `~/.claude/settings.json` für globale Hooks

### Stop-Hook läuft endlos

Claude arbeitet in einer Endlosschleife weiter, anstatt zu stoppen.

Ihr Stop-Hook-Skript muss überprüfen, ob es bereits eine Fortsetzung ausgelöst hat. Analysieren Sie das Feld `stop_hook_active` aus der JSON-Eingabe und beenden Sie früh, wenn es `true` ist:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### JSON-Validierung fehlgeschlagen

Claude Code zeigt einen JSON-Parsing-Fehler an, obwohl Ihr Hook-Skript gültiges JSON ausgibt.

Wenn Claude Code einen Hook ausführt, spawnt es eine Shell, die Ihr Profil sourced (`~/.zshrc` oder `~/.bashrc`). Wenn Ihr Profil bedingungslose `echo`-Anweisungen enthält, wird diese Ausgabe Ihrem Hook-JSON vorangestellt:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code versucht, dies als JSON zu analysieren, und schlägt fehl. Um dies zu beheben, wickeln Sie Echo-Anweisungen in Ihrem Shell-Profil ein, sodass sie nur in interaktiven Shells ausgeführt werden:

```bash  theme={null}
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

Die Variable `$-` enthält Shell-Flags, und `i` bedeutet interaktiv. Hooks werden in nicht-interaktiven Shells ausgeführt, sodass das Echo übersprungen wird.

### Debug-Techniken

Schalten Sie den ausführlichen Modus mit `Ctrl+O` um, um Hook-Ausgabe im Transkript zu sehen, oder führen Sie `claude --debug` aus, um vollständige Ausführungsdetails einschließlich der Hooks zu sehen, die abgeglichen wurden, und ihrer Exit-Codes.

## Weitere Informationen

* [Hooks-Referenz](/de/hooks): Vollständige Event-Schemas, JSON-Ausgabeformat, asynchrone Hooks und MCP-Tool-Hooks
* [Sicherheitsüberlegungen](/de/hooks#security-considerations): Überprüfen Sie vor der Bereitstellung von Hooks in gemeinsamen oder Produktionsumgebungen
* [Bash-Befehlsvalidator-Beispiel](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): Vollständige Referenzimplementierung
