> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI-Referenz

> Vollständige Referenz für die Claude Code Befehlszeilenschnittstelle, einschließlich Befehle und Flags.

## CLI-Befehle

Sie können Sitzungen starten, Inhalte weiterleiten, Gespräche fortsetzen und Updates verwalten mit diesen Befehlen:

| Befehl                          | Beschreibung                                                                                                                                                                                                            | Beispiel                                            |
| :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| `claude`                        | Interaktive Sitzung starten                                                                                                                                                                                             | `claude`                                            |
| `claude "query"`                | Interaktive Sitzung mit initialem Prompt starten                                                                                                                                                                        | `claude "explain this project"`                     |
| `claude -p "query"`             | Abfrage über SDK, dann beenden                                                                                                                                                                                          | `claude -p "explain this function"`                 |
| `cat file \| claude -p "query"` | Weitergeleitete Inhalte verarbeiten                                                                                                                                                                                     | `cat logs.txt \| claude -p "explain"`               |
| `claude -c`                     | Letzte Konversation im aktuellen Verzeichnis fortsetzen                                                                                                                                                                 | `claude -c`                                         |
| `claude -c -p "query"`          | Über SDK fortsetzen                                                                                                                                                                                                     | `claude -c -p "Check for type errors"`              |
| `claude -r "<session>" "query"` | Sitzung nach ID oder Name fortsetzen                                                                                                                                                                                    | `claude -r "auth-refactor" "Finish this PR"`        |
| `claude update`                 | Auf neueste Version aktualisieren                                                                                                                                                                                       | `claude update`                                     |
| `claude auth login`             | Melden Sie sich bei Ihrem Anthropic-Konto an. Verwenden Sie `--email`, um Ihre E-Mail-Adresse vorauszufüllen, und `--sso`, um SSO-Authentifizierung zu erzwingen                                                        | `claude auth login --email user@example.com --sso`  |
| `claude auth logout`            | Abmelden von Ihrem Anthropic-Konto                                                                                                                                                                                      | `claude auth logout`                                |
| `claude auth status`            | Authentifizierungsstatus als JSON anzeigen. Verwenden Sie `--text` für benutzerfreundliche Ausgabe. Beendet mit Code 0, wenn angemeldet, 1, wenn nicht                                                                  | `claude auth status`                                |
| `claude agents`                 | Alle konfigurierten [subagents](/de/sub-agents) auflisten, gruppiert nach Quelle                                                                                                                                        | `claude agents`                                     |
| `claude mcp`                    | Model Context Protocol (MCP) Server konfigurieren                                                                                                                                                                       | Siehe die [Claude Code MCP-Dokumentation](/de/mcp). |
| `claude remote-control`         | Starten Sie eine [Remote Control-Sitzung](/de/remote-control), um Claude Code von Claude.ai oder der Claude-App aus zu steuern, während sie lokal ausgeführt wird. Siehe [Remote Control](/de/remote-control) für Flags | `claude remote-control`                             |

## CLI-Flags

Passen Sie das Verhalten von Claude Code mit diesen Befehlszeilenflags an:

| Flag                                   | Beschreibung                                                                                                                                                                                                                                        | Beispiel                                                                                           |
| :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Zusätzliche Arbeitsverzeichnisse hinzufügen, auf die Claude zugreifen kann (validiert, dass jeder Pfad als Verzeichnis vorhanden ist)                                                                                                               | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Geben Sie einen Agent für die aktuelle Sitzung an (überschreibt die `agent`-Einstellung)                                                                                                                                                            | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Definieren Sie benutzerdefinierte [subagents](/de/sub-agents) dynamisch über JSON (siehe unten für das Format)                                                                                                                                      | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Aktivieren Sie das Umgehen von Berechtigungen als Option, ohne es sofort zu aktivieren. Ermöglicht die Zusammensetzung mit `--permission-mode` (mit Vorsicht verwenden)                                                                             | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Tools, die ohne Aufforderung zur Berechtigung ausgeführt werden. Siehe [Syntax der Berechtigungsregel](/de/settings#permission-rule-syntax) für Musterabgleich. Um einzuschränken, welche Tools verfügbar sind, verwenden Sie stattdessen `--tools` | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Benutzerdefinierten Text am Ende des Standard-Systemprompts anhängen                                                                                                                                                                                | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Zusätzlichen Systemprompt-Text aus einer Datei laden und an den Standard-Prompt anhängen                                                                                                                                                            | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | Beta-Header, die in API-Anfragen einbezogen werden sollen (nur API-Schlüsselbenutzer)                                                                                                                                                               | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Aktivieren Sie [Chrome-Browserintegration](/de/chrome) für Web-Automatisierung und Tests                                                                                                                                                            | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Laden Sie die letzte Konversation im aktuellen Verzeichnis                                                                                                                                                                                          | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Alle Berechtigungsaufforderungen überspringen (mit Vorsicht verwenden)                                                                                                                                                                              | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Debug-Modus mit optionaler Kategoriefilterung aktivieren (z. B. `"api,hooks"` oder `"!statsig,!file"`)                                                                                                                                              | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Alle skills und Befehle für diese Sitzung deaktivieren                                                                                                                                                                                              | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Tools, die aus dem Kontext des Modells entfernt werden und nicht verwendet werden können                                                                                                                                                            | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Automatisches Fallback auf das angegebene Modell aktivieren, wenn das Standardmodell überlastet ist (nur Druckmodus)                                                                                                                                | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | Beim Fortsetzen eine neue Sitzungs-ID erstellen, anstatt die ursprüngliche wiederzuverwenden (mit `--resume` oder `--continue` verwenden)                                                                                                           | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Sitzungen fortsetzen, die mit einem bestimmten GitHub PR verknüpft sind. Akzeptiert eine PR-Nummer oder URL. Sitzungen werden automatisch verknüpft, wenn sie über `gh pr create` erstellt werden                                                   | `claude --from-pr 123`                                                                             |
| `--ide`                                | Automatisch mit IDE beim Start verbinden, wenn genau eine gültige IDE verfügbar ist                                                                                                                                                                 | `claude --ide`                                                                                     |
| `--init`                               | Initialisierungs-Hooks ausführen und interaktiven Modus starten                                                                                                                                                                                     | `claude --init`                                                                                    |
| `--init-only`                          | Initialisierungs-Hooks ausführen und beenden (keine interaktive Sitzung)                                                                                                                                                                            | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Partielle Streaming-Ereignisse in die Ausgabe einbeziehen (erfordert `--print` und `--output-format=stream-json`)                                                                                                                                   | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Eingabeformat für Druckmodus angeben (Optionen: `text`, `stream-json`)                                                                                                                                                                              | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Validierte JSON-Ausgabe abrufen, die einem JSON-Schema entspricht, nachdem der Agent seinen Workflow abgeschlossen hat (nur Druckmodus, siehe [strukturierte Ausgaben](https://platform.claude.com/docs/en/agent-sdk/structured-outputs))           | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Wartungs-Hooks ausführen und beenden                                                                                                                                                                                                                | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Maximaler Dollarbetrag, der für API-Aufrufe ausgegeben werden kann, bevor gestoppt wird (nur Druckmodus)                                                                                                                                            | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Begrenzen Sie die Anzahl der agentischen Wendungen (nur Druckmodus). Beendet mit einem Fehler, wenn das Limit erreicht wird. Standardmäßig kein Limit                                                                                               | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Laden Sie MCP-Server aus JSON-Dateien oder Strings (durch Leerzeichen getrennt)                                                                                                                                                                     | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Legt das Modell für die aktuelle Sitzung mit einem Alias für das neueste Modell (`sonnet` oder `opus`) oder den vollständigen Namen eines Modells fest                                                                                              | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Deaktivieren Sie [Chrome-Browserintegration](/de/chrome) für diese Sitzung                                                                                                                                                                          | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Deaktivieren Sie die Sitzungspersistenz, sodass Sitzungen nicht auf der Festplatte gespeichert werden und nicht fortgesetzt werden können (nur Druckmodus)                                                                                          | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Ausgabeformat für Druckmodus angeben (Optionen: `text`, `json`, `stream-json`)                                                                                                                                                                      | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Beginnen Sie in einem angegebenen [Berechtigungsmodus](/de/permissions#permission-modes)                                                                                                                                                            | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Geben Sie ein MCP-Tool an, um Berechtigungsaufforderungen im nicht-interaktiven Modus zu verarbeiten                                                                                                                                                | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Laden Sie Plugins aus Verzeichnissen nur für diese Sitzung (wiederholbar)                                                                                                                                                                           | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Antwort ohne interaktiven Modus drucken (siehe [Agent SDK-Dokumentation](https://platform.claude.com/docs/en/agent-sdk/overview) für Details zur programmgesteuerten Verwendung)                                                                    | `claude -p "query"`                                                                                |
| `--remote`                             | Erstellen Sie eine neue [Web-Sitzung](/de/claude-code-on-the-web) auf claude.ai mit der bereitgestellten Aufgabenbeschreibung                                                                                                                       | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Setzen Sie eine bestimmte Sitzung nach ID oder Name fort, oder zeigen Sie eine interaktive Auswahl an, um eine Sitzung auszuwählen                                                                                                                  | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Verwenden Sie eine bestimmte Sitzungs-ID für die Konversation (muss eine gültige UUID sein)                                                                                                                                                         | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Durch Kommas getrennte Liste von Einstellungsquellen zum Laden (`user`, `project`, `local`)                                                                                                                                                         | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Pfad zu einer Einstellungs-JSON-Datei oder eine JSON-Zeichenkette zum Laden zusätzlicher Einstellungen                                                                                                                                              | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Verwenden Sie nur MCP-Server aus `--mcp-config`, ignorieren Sie alle anderen MCP-Konfigurationen                                                                                                                                                    | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Ersetzen Sie den gesamten Systemprompt durch benutzerdefinierten Text                                                                                                                                                                               | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Laden Sie den Systemprompt aus einer Datei, um den Standard-Prompt zu ersetzen                                                                                                                                                                      | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Setzen Sie eine [Web-Sitzung](/de/claude-code-on-the-web) in Ihrem lokalen Terminal fort                                                                                                                                                            | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Legen Sie fest, wie [Agent-Team](/de/agent-teams)-Teamkollegen angezeigt werden: `auto` (Standard), `in-process` oder `tmux`. Siehe [Agent-Teams einrichten](/de/agent-teams#set-up-agent-teams)                                                    | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Beschränken Sie, welche integrierten Tools Claude verwenden kann. Verwenden Sie `""`, um alle zu deaktivieren, `"default"` für alle oder Tool-Namen wie `"Bash,Edit,Read"`                                                                          | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Ausführliches Logging aktivieren, zeigt vollständige Ausgabe für jeden Wendung                                                                                                                                                                      | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Versionsnummer ausgeben                                                                                                                                                                                                                             | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Starten Sie Claude in einem isolierten [git worktree](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) bei `<repo>/.claude/worktrees/<name>`. Wenn kein Name angegeben wird, wird einer automatisch generiert             | `claude -w feature-auth`                                                                           |

<Tip>
  Das Flag `--output-format json` ist besonders nützlich für Scripting und
  Automatisierung und ermöglicht es Ihnen, Claudes Antworten programmgesteuert zu analysieren.
</Tip>

### Format des Agents-Flags

Das Flag `--agents` akzeptiert ein JSON-Objekt, das einen oder mehrere benutzerdefinierte Subagents definiert. Jeder Subagent erfordert einen eindeutigen Namen (als Schlüssel) und ein Definitionsobjekt mit den folgenden Feldern:

| Feld              | Erforderlich | Beschreibung                                                                                                                                                                                                                          |
| :---------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description`     | Ja           | Natürlichsprachige Beschreibung, wann der Subagent aufgerufen werden sollte                                                                                                                                                           |
| `prompt`          | Ja           | Der Systemprompt, der das Verhalten des Subagents lenkt                                                                                                                                                                               |
| `tools`           | Nein         | Array von spezifischen Tools, die der Subagent verwenden kann, z. B. `["Read", "Edit", "Bash"]`. Falls weggelassen, erbt alle Tools. Unterstützt [`Agent(agent_type)`](/de/sub-agents#restrict-which-subagents-can-be-spawned)-Syntax |
| `disallowedTools` | Nein         | Array von Tool-Namen, die für diesen Subagent explizit verweigert werden                                                                                                                                                              |
| `model`           | Nein         | Modell-Alias zur Verwendung: `sonnet`, `opus`, `haiku` oder `inherit`. Falls weggelassen, wird standardmäßig `inherit` verwendet                                                                                                      |
| `skills`          | Nein         | Array von [skill](/de/skills)-Namen, die in den Kontext des Subagents vorgeladen werden sollen                                                                                                                                        |
| `mcpServers`      | Nein         | Array von [MCP-Servern](/de/mcp) für diesen Subagent. Jeder Eintrag ist eine Server-Namenszeichenkette oder ein `{name: config}`-Objekt                                                                                               |
| `maxTurns`        | Nein         | Maximale Anzahl von agentischen Wendungen, bevor der Subagent stoppt                                                                                                                                                                  |

Beispiel:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Weitere Details zum Erstellen und Verwenden von Subagents finden Sie in der [Subagents-Dokumentation](/de/sub-agents).

### Systemprompt-Flags

Claude Code bietet vier Flags zum Anpassen des Systemprompts. Alle vier funktionieren sowohl im interaktiven als auch im nicht-interaktiven Modus.

| Flag                          | Verhalten                                    | Anwendungsfall                                                                                      |
| :---------------------------- | :------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| `--system-prompt`             | **Ersetzt** den gesamten Standard-Prompt     | Vollständige Kontrolle über Claudes Verhalten und Anweisungen                                       |
| `--system-prompt-file`        | **Ersetzt** mit Dateiinhalten                | Laden Sie Prompts aus Dateien für Reproduzierbarkeit und Versionskontrolle                          |
| `--append-system-prompt`      | **Hängt** an Standard-Prompt an              | Fügen Sie spezifische Anweisungen hinzu, während Sie das Standard-Claude Code-Verhalten beibehalten |
| `--append-system-prompt-file` | **Hängt** Dateiinhalte an Standard-Prompt an | Laden Sie zusätzliche Anweisungen aus Dateien, während Sie die Standardwerte beibehalten            |

**Wann jedes verwendet werden sollte:**

* **`--system-prompt`**: Verwenden Sie, wenn Sie vollständige Kontrolle über Claudes Systemprompt benötigen. Dies entfernt alle Standard-Claude Code-Anweisungen und gibt Ihnen eine leere Leinwand.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: Verwenden Sie, wenn Sie einen benutzerdefinierten Prompt aus einer Datei laden möchten, nützlich für Team-Konsistenz oder versionskontrollierte Prompt-Vorlagen.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: Verwenden Sie, wenn Sie spezifische Anweisungen hinzufügen möchten, während Sie die Standard-Funktionen von Claude Code beibehalten. Dies ist die sicherste Option für die meisten Anwendungsfälle.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: Verwenden Sie, wenn Sie Anweisungen aus einer Datei anhängen möchten, während Sie die Claude Code-Standardwerte beibehalten. Nützlich für versionskontrollierte Ergänzungen.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` und `--system-prompt-file` schließen sich gegenseitig aus. Die Append-Flags können zusammen mit einem der Ersetzungs-Flags verwendet werden.

Für die meisten Anwendungsfälle wird `--append-system-prompt` oder `--append-system-prompt-file` empfohlen, da sie die integrierten Funktionen von Claude Code beibehalten und gleichzeitig Ihre benutzerdefinierten Anforderungen hinzufügen. Verwenden Sie `--system-prompt` oder `--system-prompt-file` nur, wenn Sie vollständige Kontrolle über den Systemprompt benötigen.

## Siehe auch

* [Chrome-Erweiterung](/de/chrome) - Browser-Automatisierung und Web-Tests
* [Interaktiver Modus](/de/interactive-mode) - Tastenkombinationen, Eingabemodi und interaktive Funktionen
* [Schnellstart-Anleitung](/de/quickstart) - Erste Schritte mit Claude Code
* [Häufige Workflows](/de/common-workflows) - Erweiterte Workflows und Muster
* [Einstellungen](/de/settings) - Konfigurationsoptionen
* [Agent SDK-Dokumentation](https://platform.claude.com/docs/en/agent-sdk/overview) - Programmgesteuerte Verwendung und Integrationen
