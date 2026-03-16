> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code-Einstellungen

> Konfigurieren Sie Claude Code mit globalen und projektbezogenen Einstellungen sowie Umgebungsvariablen.

Claude Code bietet eine Vielzahl von Einstellungen, um sein Verhalten an Ihre Anforderungen anzupassen. Sie können Claude Code konfigurieren, indem Sie den Befehl `/config` in der interaktiven REPL ausführen, wodurch eine Einstellungsoberfläche mit Registerkarten geöffnet wird, auf der Sie Statusinformationen anzeigen und Konfigurationsoptionen ändern können.

## Konfigurationsbereiche

Claude Code verwendet ein **Bereichssystem**, um zu bestimmen, wo Konfigurationen gelten und wer sie teilt. Das Verständnis von Bereichen hilft Ihnen zu entscheiden, wie Sie Claude Code für persönliche Nutzung, Teamzusammenarbeit oder Unternehmensbereitstellung konfigurieren.

### Verfügbare Bereiche

| Bereich       | Speicherort                                                                               | Wer ist betroffen                     | Mit Team geteilt?          |
| :------------ | :---------------------------------------------------------------------------------------- | :------------------------------------ | :------------------------- |
| **Verwaltet** | Serververwaltete Einstellungen, plist / Registry oder systemweite `managed-settings.json` | Alle Benutzer auf dem Computer        | Ja (von IT bereitgestellt) |
| **Benutzer**  | `~/.claude/` Verzeichnis                                                                  | Sie, über alle Projekte hinweg        | Nein                       |
| **Projekt**   | `.claude/` im Repository                                                                  | Alle Mitarbeiter in diesem Repository | Ja (in Git eingecheckt)    |
| **Lokal**     | `.claude/settings.local.json`                                                             | Sie, nur in diesem Repository         | Nein (gitignored)          |

### Wann Sie jeden Bereich verwenden sollten

Der **Verwaltungsbereich** ist für:

* Sicherheitsrichtlinien, die organisationsweit durchgesetzt werden müssen
* Compliance-Anforderungen, die nicht überschrieben werden können
* Standardisierte Konfigurationen, die von IT/DevOps bereitgestellt werden

Der **Benutzerbereich** ist am besten für:

* Persönliche Voreinstellungen, die Sie überall haben möchten (Designs, Editor-Einstellungen)
* Tools und Plugins, die Sie in allen Projekten verwenden
* API-Schlüssel und Authentifizierung (sicher gespeichert)

Der **Projektbereich** ist am besten für:

* Teamübergreifende Einstellungen (Berechtigungen, Hooks, MCP-Server)
* Plugins, die das ganze Team haben sollte
* Standardisierung von Tools über Mitarbeiter hinweg

Der **lokale Bereich** ist am besten für:

* Persönliche Überschreibungen für ein bestimmtes Projekt
* Testen von Konfigurationen vor dem Teilen mit dem Team
* Maschinenspezifische Einstellungen, die für andere nicht funktionieren

### Wie Bereiche interagieren

Wenn die gleiche Einstellung in mehreren Bereichen konfiguriert ist, haben spezifischere Bereiche Vorrang:

1. **Verwaltet** (höchste) - kann von nichts überschrieben werden
2. **Befehlszeilenargumente** - temporäre Sitzungsüberschreibungen
3. **Lokal** - überschreibt Projekt- und Benutzereinstellungen
4. **Projekt** - überschreibt Benutzereinstellungen
5. **Benutzer** (niedrigste) - gilt, wenn nichts anderes die Einstellung angibt

Wenn beispielsweise eine Berechtigung in Benutzereinstellungen erlaubt ist, aber in Projekteinstellungen verweigert wird, hat die Projekteinstellung Vorrang und die Berechtigung wird blockiert.

### Was Bereiche verwendet

Bereiche gelten für viele Claude Code-Funktionen:

| Funktion          | Benutzerort               | Projektort                           | Lokaler Ort                    |
| :---------------- | :------------------------ | :----------------------------------- | :----------------------------- |
| **Einstellungen** | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json`  |
| **Subagents**     | `~/.claude/agents/`       | `.claude/agents/`                    | —                              |
| **MCP-Server**    | `~/.claude.json`          | `.mcp.json`                          | `~/.claude.json` (pro Projekt) |
| **Plugins**       | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json`  |
| **CLAUDE.md**     | `~/.claude/CLAUDE.md`     | `CLAUDE.md` oder `.claude/CLAUDE.md` | —                              |

***

## Einstellungsdateien

Die `settings.json` Datei ist unser offizieller Mechanismus zum Konfigurieren von Claude Code durch hierarchische Einstellungen:

* **Benutzereinstellungen** werden in `~/.claude/settings.json` definiert und gelten für alle Projekte.
* **Projekteinstellungen** werden in Ihrem Projektverzeichnis gespeichert:
  * `.claude/settings.json` für Einstellungen, die in die Versionskontrolle eingecheckt und mit Ihrem Team geteilt werden
  * `.claude/settings.local.json` für Einstellungen, die nicht eingecheckt werden, nützlich für persönliche Voreinstellungen und Experimente. Claude Code konfiguriert Git so, dass `.claude/settings.local.json` ignoriert wird, wenn sie erstellt wird.
* **Verwaltete Einstellungen**: Für Organisationen, die zentrale Kontrolle benötigen, unterstützt Claude Code mehrere Bereitstellungsmechanismen für verwaltete Einstellungen. Alle verwenden das gleiche JSON-Format und können nicht durch Benutzer- oder Projekteinstellungen überschrieben werden:

  * **Serververwaltete Einstellungen**: von Anthropics Servern über die Claude.ai Admin-Konsole bereitgestellt. Siehe [serververwaltete Einstellungen](/de/server-managed-settings).
  * **MDM/OS-Richtlinien**: über native Geräteverwaltung auf macOS und Windows bereitgestellt:
    * macOS: `com.anthropic.claudecode` verwaltete Präferenzen-Domain (bereitgestellt über Konfigurationsprofile in Jamf, Kandji oder anderen MDM-Tools)
    * Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` Registry-Schlüssel mit einem `Settings` Wert (REG\_SZ oder REG\_EXPAND\_SZ) mit JSON (bereitgestellt über Gruppenrichtlinie oder Intune)
    * Windows (Benutzerebene): `HKCU\SOFTWARE\Policies\ClaudeCode` (niedrigste Richtlinienpriorität, wird nur verwendet, wenn keine Admin-Quelle vorhanden ist)
  * **Dateibasiert**: `managed-settings.json` und `managed-mcp.json` in Systemverzeichnissen bereitgestellt:
    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux und WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

  Siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings) und [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration) für Details.

  <Note>
    Verwaltete Bereitstellungen können auch **Plugin-Marketplace-Ergänzungen** mit `strictKnownMarketplaces` einschränken. Weitere Informationen finden Sie unter [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Andere Konfiguration** wird in `~/.claude.json` gespeichert. Diese Datei enthält Ihre Voreinstellungen (Design, Benachrichtigungseinstellungen, Editor-Modus), OAuth-Sitzung, [MCP-Server](/de/mcp) Konfigurationen für Benutzer- und lokale Bereiche, projektbezogene Zustände (zulässige Tools, Vertrauenseinstellungen) und verschiedene Caches. Projektbezogene MCP-Server werden separat in `.mcp.json` gespeichert.

<Note>
  Claude Code erstellt automatisch zeitgestempelte Sicherungen von Konfigurationsdateien und behält die fünf neuesten Sicherungen bei, um Datenverlust zu verhindern.
</Note>

```JSON Beispiel settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

Die `$schema` Zeile im obigen Beispiel verweist auf das [offizielle JSON-Schema](https://json.schemastore.org/claude-code-settings.json) für Claude Code-Einstellungen. Das Hinzufügen zu Ihrer `settings.json` ermöglicht Autovervollständigung und Inline-Validierung in VS Code, Cursor und jedem anderen Editor, der JSON-Schema-Validierung unterstützt.

### Verfügbare Einstellungen

`settings.json` unterstützt eine Reihe von Optionen:

| Schlüssel                         | Beschreibung                                                                                                                                                                                                                                                                                                                                                          | Beispiel                                                                |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Benutzerdefiniertes Skript, das in `/bin/sh` ausgeführt werden soll, um einen Auth-Wert zu generieren. Dieser Wert wird als `X-Api-Key` und `Authorization: Bearer` Header für Modellanfragen gesendet                                                                                                                                                                | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | Sitzungen, die länger als dieser Zeitraum inaktiv sind, werden beim Start gelöscht. Wenn auf `0` gesetzt, werden alle Sitzungen sofort gelöscht. (Standard: 30 Tage)                                                                                                                                                                                                  | `20`                                                                    |
| `companyAnnouncements`            | Ankündigung, die Benutzern beim Start angezeigt wird. Wenn mehrere Ankündigungen bereitgestellt werden, werden sie zufällig durchlaufen.                                                                                                                                                                                                                              | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Umgebungsvariablen, die auf jede Sitzung angewendet werden                                                                                                                                                                                                                                                                                                            | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Passen Sie die Zuschreibung für Git-Commits und Pull Requests an. Siehe [Zuschreibungseinstellungen](#attribution-settings)                                                                                                                                                                                                                                           | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Veraltet**: Verwenden Sie stattdessen `attribution`. Ob die `co-authored-by Claude` Byline in Git-Commits und Pull Requests einbezogen werden soll (Standard: `true`)                                                                                                                                                                                               | `false`                                                                 |
| `includeGitInstructions`          | Integrierte Commit- und PR-Workflow-Anweisungen in Claudes System-Prompt einbeziehen (Standard: `true`). Auf `false` setzen, um diese Anweisungen zu entfernen, z. B. wenn Sie Ihre eigenen Git-Workflow-Skills verwenden. Die Umgebungsvariable `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` hat Vorrang vor dieser Einstellung, wenn gesetzt                              | `false`                                                                 |
| `permissions`                     | Siehe Tabelle unten für die Struktur der Berechtigungen.                                                                                                                                                                                                                                                                                                              |                                                                         |
| `hooks`                           | Konfigurieren Sie benutzerdefinierte Befehle, die bei Lebenszyklusereignissen ausgeführt werden. Siehe [Hooks-Dokumentation](/de/hooks) für das Format                                                                                                                                                                                                                | Siehe [Hooks](/de/hooks)                                                |
| `disableAllHooks`                 | Deaktivieren Sie alle [Hooks](/de/hooks) und alle benutzerdefinierten [Statuszeilen](/de/statusline)                                                                                                                                                                                                                                                                  | `true`                                                                  |
| `allowManagedHooksOnly`           | (Nur verwaltete Einstellungen) Verhindern Sie das Laden von Benutzer-, Projekt- und Plugin-Hooks. Erlaubt nur verwaltete Hooks und SDK-Hooks. Siehe [Hook-Konfiguration](#hook-configuration)                                                                                                                                                                         | `true`                                                                  |
| `allowedHttpHookUrls`             | Whitelist von URL-Mustern, auf die HTTP-Hooks abzielen können. Unterstützt `*` als Wildcard. Wenn gesetzt, werden Hooks mit nicht übereinstimmenden URLs blockiert. Undefined = keine Einschränkung, leeres Array = alle HTTP-Hooks blockieren. Arrays werden über Einstellungsquellen zusammengeführt. Siehe [Hook-Konfiguration](#hook-configuration)               | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Whitelist von Umgebungsvariablennamen, die HTTP-Hooks in Header interpolieren können. Wenn gesetzt, ist die effektive `allowedEnvVars` jedes Hooks der Schnittpunkt mit dieser Liste. Undefined = keine Einschränkung. Arrays werden über Einstellungsquellen zusammengeführt. Siehe [Hook-Konfiguration](#hook-configuration)                                        | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Nur verwaltete Einstellungen) Verhindern Sie, dass Benutzer- und Projekteinstellungen `allow`, `ask` oder `deny` Berechtigungsregeln definieren. Nur Regeln in verwalteten Einstellungen gelten. Siehe [Nur verwaltete Einstellungen](/de/permissions#managed-only-settings)                                                                                         | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Nur verwaltete Einstellungen) Nur `allowedMcpServers` aus verwalteten Einstellungen werden berücksichtigt. `deniedMcpServers` wird weiterhin aus allen Quellen zusammengeführt. Benutzer können weiterhin MCP-Server hinzufügen, aber nur die von Admin definierten Allowlist gilt. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)          | `true`                                                                  |
| `model`                           | Überschreiben Sie das Standard-Modell für Claude Code                                                                                                                                                                                                                                                                                                                 | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Beschränken Sie, welche Modelle Benutzer über `/model`, `--model`, Config-Tool oder `ANTHROPIC_MODEL` auswählen können. Beeinflusst nicht die Standard-Option. Siehe [Modellauswahl einschränken](/de/model-config#restrict-model-selection)                                                                                                                          | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Ordnen Sie Anthropic-Modell-IDs Anbieter-spezifischen Modell-IDs wie Bedrock-Inferenzprofil-ARNs zu. Jeder Modellwähler-Eintrag verwendet seinen zugeordneten Wert beim Aufrufen der Anbieter-API. Siehe [Modell-IDs pro Version überschreiben](/de/model-config#override-model-ids-per-version)                                                                      | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | Skript zum Generieren dynamischer OpenTelemetry-Header. Wird beim Start und regelmäßig ausgeführt (siehe [Dynamische Header](/de/monitoring-usage#dynamic-headers))                                                                                                                                                                                                   | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Konfigurieren Sie eine benutzerdefinierte Statuszeile zur Anzeige von Kontext. Siehe [`statusLine` Dokumentation](/de/statusline)                                                                                                                                                                                                                                     | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Konfigurieren Sie ein benutzerdefiniertes Skript für `@` Datei-Autovervollständigung. Siehe [Dateivorschlag-Einstellungen](#file-suggestion-settings)                                                                                                                                                                                                                 | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Steuern Sie, ob der `@` Datei-Picker `.gitignore` Muster respektiert. Wenn `true` (Standard), werden Dateien, die `.gitignore` Mustern entsprechen, von Vorschlägen ausgeschlossen                                                                                                                                                                                    | `false`                                                                 |
| `outputStyle`                     | Konfigurieren Sie einen Ausgabestil, um den System-Prompt anzupassen. Siehe [Ausgabestil-Dokumentation](/de/output-styles)                                                                                                                                                                                                                                            | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Verwenden Sie `claudeai`, um die Anmeldung auf Claude.ai-Konten zu beschränken, `console`, um die Anmeldung auf Claude Console (API-Nutzungsabrechnung) Konten zu beschränken                                                                                                                                                                                         | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Geben Sie die UUID einer Organisation an, um sie während der Anmeldung automatisch auszuwählen und den Organisationsauswahlschritt zu umgehen. Erfordert, dass `forceLoginMethod` gesetzt ist                                                                                                                                                                         | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Genehmigen Sie automatisch alle MCP-Server, die in Projekt `.mcp.json` Dateien definiert sind                                                                                                                                                                                                                                                                         | `true`                                                                  |
| `enabledMcpjsonServers`           | Liste spezifischer MCP-Server aus `.mcp.json` Dateien zum Genehmigen                                                                                                                                                                                                                                                                                                  | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Liste spezifischer MCP-Server aus `.mcp.json` Dateien zum Ablehnen                                                                                                                                                                                                                                                                                                    | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Wenn in managed-settings.json gesetzt, Whitelist von MCP-Servern, die Benutzer konfigurieren können. Undefined = keine Einschränkungen, leeres Array = Lockdown. Gilt für alle Bereiche. Denylist hat Vorrang. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Wenn in managed-settings.json gesetzt, Denylist von MCP-Servern, die explizit blockiert sind. Gilt für alle Bereiche einschließlich verwalteter Server. Denylist hat Vorrang vor Allowlist. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                                   | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Wenn in managed-settings.json gesetzt, Whitelist von Plugin-Marketplaces, die Benutzer hinzufügen können. Undefined = keine Einschränkungen, leeres Array = Lockdown. Gilt nur für Marketplace-Ergänzungen. Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                  | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Nur verwaltete Einstellungen) Blocklist von Marketplace-Quellen. Blockierte Quellen werden vor dem Download überprüft, sodass sie das Dateisystem nie berühren. Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                                             | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Nur verwaltete Einstellungen) Benutzerdefinierte Nachricht, die der vor der Installation angezeigten Plugin-Vertrauenswarnung angehängt wird. Verwenden Sie dies, um organisationsspezifischen Kontext hinzuzufügen, z. B. um zu bestätigen, dass Plugins aus Ihrem internen Marketplace überprüft sind.                                                             | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Benutzerdefiniertes Skript, das das `.aws` Verzeichnis ändert (siehe [erweiterte Anmeldedaten-Konfiguration](/de/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                   | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Benutzerdefiniertes Skript, das JSON mit AWS-Anmeldedaten ausgibt (siehe [erweiterte Anmeldedaten-Konfiguration](/de/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                               | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Aktivieren Sie [erweitertes Denken](/de/common-workflows#use-extended-thinking-thinking-mode) standardmäßig für alle Sitzungen. Normalerweise über den Befehl `/config` konfiguriert, anstatt direkt zu bearbeiten                                                                                                                                                    | `true`                                                                  |
| `plansDirectory`                  | Passen Sie an, wo Plandateien gespeichert werden. Der Pfad ist relativ zum Projektstamm. Standard: `~/.claude/plans`                                                                                                                                                                                                                                                  | `"./plans"`                                                             |
| `showTurnDuration`                | Zeigen Sie Nachrichten zur Dauer der Runde nach Antworten an (z. B. "Cooked for 1m 6s"). Auf `false` setzen, um diese Nachrichten auszublenden                                                                                                                                                                                                                        | `true`                                                                  |
| `spinnerVerbs`                    | Passen Sie die Aktionsverben an, die im Spinner und in Nachrichten zur Dauer der Runde angezeigt werden. Setzen Sie `mode` auf `"replace"`, um nur Ihre Verben zu verwenden, oder `"append"`, um sie zu den Standardwerten hinzuzufügen                                                                                                                               | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Konfigurieren Sie Claudes bevorzugte Antwortsprache (z. B. `"japanese"`, `"spanish"`, `"french"`). Claude wird standardmäßig in dieser Sprache antworten                                                                                                                                                                                                              | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Release-Kanal zum Folgen von Updates. Verwenden Sie `"stable"` für eine Version, die normalerweise etwa eine Woche alt ist und Versionen mit großen Regressionen überspringt, oder `"latest"` (Standard) für die neueste Version                                                                                                                                      | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Zeigen Sie Tipps im Spinner an, während Claude arbeitet. Auf `false` setzen, um Tipps zu deaktivieren (Standard: `true`)                                                                                                                                                                                                                                              | `false`                                                                 |
| `spinnerTipsOverride`             | Überschreiben Sie Spinner-Tipps mit benutzerdefinierten Strings. `tips`: Array von Tip-Strings. `excludeDefault`: wenn `true`, nur benutzerdefinierte Tipps anzeigen; wenn `false` oder nicht vorhanden, werden benutzerdefinierte Tipps mit integrierten Tipps zusammengeführt                                                                                       | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Aktivieren Sie die Terminal-Fortschrittsleiste, die den Fortschritt in unterstützten Terminals wie Windows Terminal und iTerm2 anzeigt (Standard: `true`)                                                                                                                                                                                                             | `false`                                                                 |
| `prefersReducedMotion`            | Reduzieren oder deaktivieren Sie UI-Animationen (Spinner, Shimmer, Flash-Effekte) für Barrierefreiheit                                                                                                                                                                                                                                                                | `true`                                                                  |
| `fastModePerSessionOptIn`         | Wenn `true`, bleibt der schnelle Modus nicht über Sitzungen hinweg bestehen. Jede Sitzung startet mit ausgeschaltetem schnellen Modus und erfordert, dass Benutzer ihn mit `/fast` aktivieren. Die Voreinstellung des Benutzers für den schnellen Modus wird weiterhin gespeichert. Siehe [Opt-in pro Sitzung erforderlich](/de/fast-mode#require-per-session-opt-in) | `true`                                                                  |
| `teammateMode`                    | Wie [Agent-Team](/de/agent-teams) Teamkollegen angezeigt werden: `auto` (wählt geteilte Fenster in tmux oder iTerm2, ansonsten in-process), `in-process` oder `tmux`. Siehe [Agent-Teams einrichten](/de/agent-teams#set-up-agent-teams)                                                                                                                              | `"in-process"`                                                          |

### Berechtigungseinstellungen

| Schlüssel                      | Beschreibung                                                                                                                                                                                                                                                                                   | Beispiel                                                               |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Array von Berechtigungsregeln, um Tool-Nutzung zu erlauben. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) unten für Details zum Musterabgleich                                                                                                                                     | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Array von Berechtigungsregeln, um bei Tool-Nutzung um Bestätigung zu fragen. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) unten                                                                                                                                                   | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Array von Berechtigungsregeln, um Tool-Nutzung zu verweigern. Verwenden Sie dies, um sensible Dateien vom Claude Code-Zugriff auszuschließen. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) und [Bash-Berechtigungsbeschränkungen](/de/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | Zusätzliche [Arbeitsverzeichnisse](/de/permissions#working-directories), auf die Claude Zugriff hat                                                                                                                                                                                            | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | Standard-[Berechtigungsmodus](/de/permissions#permission-modes) beim Öffnen von Claude Code                                                                                                                                                                                                    | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Auf `"disable"` setzen, um zu verhindern, dass der `bypassPermissions` Modus aktiviert wird. Dies deaktiviert das Befehlszeilenargument `--dangerously-skip-permissions`. Siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings)                                              | `"disable"`                                                            |

### Berechtigungsregelsyntax

Berechtigungsregeln folgen dem Format `Tool` oder `Tool(specifier)`. Regeln werden in Reihenfolge ausgewertet: zuerst Deny-Regeln, dann Ask, dann Allow. Die erste übereinstimmende Regel gewinnt.

Schnelle Beispiele:

| Regel                          | Effekt                                        |
| :----------------------------- | :-------------------------------------------- |
| `Bash`                         | Passt auf alle Bash-Befehle                   |
| `Bash(npm run *)`              | Passt auf Befehle, die mit `npm run` beginnen |
| `Read(./.env)`                 | Passt auf das Lesen der `.env` Datei          |
| `WebFetch(domain:example.com)` | Passt auf Abrufanfragen an example.com        |

Für die vollständige Referenz der Regelsyntax, einschließlich Wildcard-Verhalten, Tool-spezifischer Muster für Read, Edit, WebFetch, MCP und Agent-Regeln sowie Sicherheitsbeschränkungen von Bash-Mustern, siehe [Berechtigungsregelsyntax](/de/permissions#permission-rule-syntax).

### Sandbox-Einstellungen

Konfigurieren Sie erweitertes Sandbox-Verhalten. Sandboxing isoliert Bash-Befehle von Ihrem Dateisystem und Netzwerk. Siehe [Sandboxing](/de/sandboxing) für Details.

| Schlüssel                         | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                     | Beispiel                        |
| :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | Aktivieren Sie Bash-Sandboxing (macOS, Linux und WSL2). Standard: false                                                                                                                                                                                                                                                                                                                                          | `true`                          |
| `autoAllowBashIfSandboxed`        | Genehmigen Sie Bash-Befehle automatisch, wenn sie in einer Sandbox ausgeführt werden. Standard: true                                                                                                                                                                                                                                                                                                             | `true`                          |
| `excludedCommands`                | Befehle, die außerhalb der Sandbox ausgeführt werden sollten                                                                                                                                                                                                                                                                                                                                                     | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Erlauben Sie Befehlen, außerhalb der Sandbox über den Parameter `dangerouslyDisableSandbox` auszuführen. Wenn auf `false` gesetzt, ist die Escape-Hatch `dangerouslyDisableSandbox` vollständig deaktiviert und alle Befehle müssen in einer Sandbox ausgeführt werden (oder in `excludedCommands` sein). Nützlich für Unternehmensrichtlinien, die striktes Sandboxing erfordern. Standard: true                | `false`                         |
| `filesystem.allowWrite`           | Zusätzliche Pfade, in die Sandbox-Befehle schreiben können. Arrays werden über alle Einstellungsbereiche zusammengeführt: Benutzer-, Projekt- und verwaltete Pfade werden kombiniert, nicht ersetzt. Auch zusammengeführt mit Pfaden aus `Edit(...)` Berechtigungsregeln. Siehe [Pfad-Präfixe](#sandbox-path-prefixes) unten.                                                                                    | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Pfade, in die Sandbox-Befehle nicht schreiben können. Arrays werden über alle Einstellungsbereiche zusammengeführt. Auch zusammengeführt mit Pfaden aus `Edit(...)` Berechtigungsregeln.                                                                                                                                                                                                                         | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Pfade, aus denen Sandbox-Befehle nicht lesen können. Arrays werden über alle Einstellungsbereiche zusammengeführt. Auch zusammengeführt mit Pfaden aus `Read(...)` Berechtigungsregeln.                                                                                                                                                                                                                          | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Unix-Socket-Pfade, auf die in der Sandbox zugegriffen werden kann (für SSH-Agenten usw.)                                                                                                                                                                                                                                                                                                                         | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Erlauben Sie alle Unix-Socket-Verbindungen in der Sandbox. Standard: false                                                                                                                                                                                                                                                                                                                                       | `true`                          |
| `network.allowLocalBinding`       | Erlauben Sie das Binden an Localhost-Ports (nur macOS). Standard: false                                                                                                                                                                                                                                                                                                                                          | `true`                          |
| `network.allowedDomains`          | Array von Domänen, um ausgehenden Netzwerkverkehr zu erlauben. Unterstützt Wildcards (z. B. `*.example.com`).                                                                                                                                                                                                                                                                                                    | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Nur verwaltete Einstellungen) Nur `allowedDomains` und `WebFetch(domain:...)` Berechtigungsregeln aus verwalteten Einstellungen werden berücksichtigt. Domänen aus Benutzer-, Projekt- und lokalen Einstellungen werden ignoriert. Nicht zulässige Domänen werden automatisch blockiert, ohne den Benutzer zu fragen. Verweigerte Domänen werden weiterhin aus allen Quellen berücksichtigt. Standard: false    | `true`                          |
| `network.httpProxyPort`           | HTTP-Proxy-Port, der verwendet wird, wenn Sie Ihren eigenen Proxy verwenden möchten. Wenn nicht angegeben, führt Claude seinen eigenen Proxy aus.                                                                                                                                                                                                                                                                | `8080`                          |
| `network.socksProxyPort`          | SOCKS5-Proxy-Port, der verwendet wird, wenn Sie Ihren eigenen Proxy verwenden möchten. Wenn nicht angegeben, führt Claude seinen eigenen Proxy aus.                                                                                                                                                                                                                                                              | `8081`                          |
| `enableWeakerNestedSandbox`       | Aktivieren Sie schwächere Sandbox für unprivilegierte Docker-Umgebungen (nur Linux und WSL2). **Reduziert Sicherheit.** Standard: false                                                                                                                                                                                                                                                                          | `true`                          |
| `enableWeakerNetworkIsolation`    | (Nur macOS) Erlauben Sie den Zugriff auf den System-TLS-Vertrauensdienst (`com.apple.trustd.agent`) in der Sandbox. Erforderlich für Go-basierte Tools wie `gh`, `gcloud` und `terraform`, um TLS-Zertifikate zu überprüfen, wenn `httpProxyPort` mit einem MITM-Proxy und benutzerdefinierter CA verwendet wird. **Reduziert Sicherheit** durch Öffnen eines möglichen Datenexfiltrationspfads. Standard: false | `true`                          |

#### Sandbox-Pfad-Präfixe

Pfade in `filesystem.allowWrite`, `filesystem.denyWrite` und `filesystem.denyRead` unterstützen diese Präfixe:

| Präfix                | Bedeutung                                         | Beispiel                               |
| :-------------------- | :------------------------------------------------ | :------------------------------------- |
| `//`                  | Absoluter Pfad vom Dateisystem-Root               | `//tmp/build` wird zu `/tmp/build`     |
| `~/`                  | Relativ zum Home-Verzeichnis                      | `~/.kube` wird zu `$HOME/.kube`        |
| `/`                   | Relativ zum Verzeichnis der Einstellungsdatei     | `/build` wird zu `$SETTINGS_DIR/build` |
| `./` oder kein Präfix | Relativer Pfad (aufgelöst durch Sandbox-Laufzeit) | `./output`                             |

**Konfigurationsbeispiel:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**Dateisystem- und Netzwerkbeschränkungen** können auf zwei Arten konfiguriert werden, die zusammengeführt werden:

* **`sandbox.filesystem` Einstellungen** (oben gezeigt): Steuern Sie Pfade an der OS-Sandbox-Grenze. Diese Einschränkungen gelten für alle Subprozess-Befehle (z. B. `kubectl`, `terraform`, `npm`), nicht nur für Claudes Datei-Tools.
* **Berechtigungsregeln**: Verwenden Sie `Edit` Allow/Deny-Regeln, um Claude's Datei-Tool-Zugriff zu steuern, `Read` Deny-Regeln, um Lesevorgänge zu blockieren, und `WebFetch` Allow/Deny-Regeln, um Netzwerk-Domänen zu steuern. Pfade aus diesen Regeln werden auch in die Sandbox-Konfiguration zusammengeführt.

### Zuschreibungseinstellungen

Claude Code fügt Zuschreibung zu Git-Commits und Pull Requests hinzu. Diese werden separat konfiguriert:

* Commits verwenden [Git-Trailer](https://git-scm.com/docs/git-interpret-trailers) (wie `Co-Authored-By`) standardmäßig, die angepasst oder deaktiviert werden können
* Pull-Request-Beschreibungen sind Klartext

| Schlüssel | Beschreibung                                                                                           |
| :-------- | :----------------------------------------------------------------------------------------------------- |
| `commit`  | Zuschreibung für Git-Commits, einschließlich aller Trailer. Leerer String verbirgt Commit-Zuschreibung |
| `pr`      | Zuschreibung für Pull-Request-Beschreibungen. Leerer String verbirgt Pull-Request-Zuschreibung         |

**Standard-Commit-Zuschreibung:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Standard-Pull-Request-Zuschreibung:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Beispiel:**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  Die `attribution` Einstellung hat Vorrang vor der veralteten `includeCoAuthoredBy` Einstellung. Um alle Zuschreibungen auszublenden, setzen Sie `commit` und `pr` auf leere Strings.
</Note>

### Dateivorschlag-Einstellungen

Konfigurieren Sie einen benutzerdefinierten Befehl für `@` Dateipath-Autovervollständigung. Der integrierte Dateivorschlag verwendet schnelle Dateisystem-Durchquerung, aber große Monorepos können von projektspezifischer Indizierung wie einem vorgebauten Dateiindex oder benutzerdefinierten Tools profitieren.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Der Befehl wird mit den gleichen Umgebungsvariablen wie [Hooks](/de/hooks) ausgeführt, einschließlich `CLAUDE_PROJECT_DIR`. Er empfängt JSON über stdin mit einem `query` Feld:

```json  theme={null}
{"query": "src/comp"}
```

Geben Sie zeilengetrennte Dateipfade zu stdout aus (derzeit auf 15 begrenzt):

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Beispiel:**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Hook-Konfiguration

Diese Einstellungen steuern, welche Hooks ausgeführt werden dürfen und worauf HTTP-Hooks zugreifen können. Die `allowManagedHooksOnly` Einstellung kann nur in [verwalteten Einstellungen](#settings-files) konfiguriert werden. Die URL- und Env-Var-Whitelists können auf jeder Einstellungsebene gesetzt werden und werden über Quellen zusammengeführt.

**Verhalten, wenn `allowManagedHooksOnly` `true` ist:**

* Verwaltete Hooks und SDK-Hooks werden geladen
* Benutzer-Hooks, Projekt-Hooks und Plugin-Hooks werden blockiert

**HTTP-Hook-URLs einschränken:**

Begrenzen Sie, auf welche URLs HTTP-Hooks abzielen können. Unterstützt `*` als Wildcard zum Abgleichen. Wenn das Array definiert ist, werden HTTP-Hooks, die auf nicht übereinstimmende URLs abzielen, stillschweigend blockiert.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**HTTP-Hook-Umgebungsvariablen einschränken:**

Begrenzen Sie, welche Umgebungsvariablennamen HTTP-Hooks in Header-Werte interpolieren können. Die effektive `allowedEnvVars` jedes Hooks ist der Schnittpunkt seiner eigenen Liste und dieser Einstellung.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Einstellungspriorität

Einstellungen werden in Prioritätsreihenfolge angewendet. Von höchster zu niedrigster:

1. **Verwaltete Einstellungen** ([serververwaltete](/de/server-managed-settings), [MDM/OS-Richtlinien](#configuration-scopes) oder [verwaltete Einstellungen](/de/settings#settings-files))
   * Richtlinien, die von IT über Server-Bereitstellung, MDM-Konfigurationsprofile, Registry-Richtlinien oder verwaltete Einstellungsdateien bereitgestellt werden
   * Können nicht durch andere Ebenen überschrieben werden, einschließlich Befehlszeilenargumenten
   * Innerhalb der verwalteten Ebene ist die Priorität: serververwaltete > MDM/OS-Richtlinien > `managed-settings.json` > HKCU Registry (nur Windows). Nur eine verwaltete Quelle wird verwendet; Quellen werden nicht zusammengeführt.

2. **Befehlszeilenargumente**
   * Temporäre Überschreibungen für eine bestimmte Sitzung

3. **Lokale Projekteinstellungen** (`.claude/settings.local.json`)
   * Persönliche projektspezifische Einstellungen

4. **Gemeinsame Projekteinstellungen** (`.claude/settings.json`)
   * Teamübergreifende Projekteinstellungen in der Versionskontrolle

5. **Benutzereinstellungen** (`~/.claude/settings.json`)
   * Persönliche globale Einstellungen

Diese Hierarchie stellt sicher, dass Organisationsrichtlinien immer durchgesetzt werden, während Teams und Einzelpersonen ihre Erfahrung anpassen können.

Wenn beispielsweise Ihre Benutzereinstellungen `Bash(npm run *)` erlauben, aber die gemeinsamen Einstellungen eines Projekts es verweigern, hat die Projekteinstellung Vorrang und der Befehl wird blockiert.

<Note>
  **Array-Einstellungen werden über Bereiche zusammengeführt.** Wenn die gleiche Array-wertige Einstellung (wie `sandbox.filesystem.allowWrite` oder `permissions.allow`) in mehreren Bereichen erscheint, werden die Arrays **verkettet und dedupliziert**, nicht ersetzt. Dies bedeutet, dass Bereiche mit niedrigerer Priorität Einträge hinzufügen können, ohne diejenigen mit höherer Priorität zu überschreiben, und umgekehrt. Wenn beispielsweise verwaltete Einstellungen `allowWrite` auf `["//opt/company-tools"]` setzen und ein Benutzer `["~/.kube"]` hinzufügt, sind beide Pfade in der endgültigen Konfiguration enthalten.
</Note>

### Aktive Einstellungen überprüfen

Führen Sie `/status` in Claude Code aus, um zu sehen, welche Einstellungsquellen aktiv sind und woher sie stammen. Die Ausgabe zeigt jede Konfigurationsebene (verwaltet, Benutzer, Projekt) zusammen mit ihrem Ursprung, wie `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)` oder `Enterprise managed settings (file)`. Wenn eine Einstellungsdatei Fehler enthält, meldet `/status` das Problem, damit Sie es beheben können.

### Wichtige Punkte zum Konfigurationssystem

* **Memory-Dateien (`CLAUDE.md`)**: Enthalten Anweisungen und Kontext, die Claude beim Start lädt
* **Einstellungsdateien (JSON)**: Konfigurieren Sie Berechtigungen, Umgebungsvariablen und Tool-Verhalten
* **Skills**: Benutzerdefinierte Prompts, die mit `/skill-name` aufgerufen oder von Claude automatisch geladen werden können
* **MCP-Server**: Erweitern Sie Claude Code mit zusätzlichen Tools und Integrationen
* **Priorität**: Höherrangige Konfigurationen (Verwaltet) überschreiben niedrigere (Benutzer/Projekt)
* **Vererbung**: Einstellungen werden zusammengeführt, wobei spezifischere Einstellungen breitere ergänzen oder überschreiben

### System-Prompt

Claudes interner System-Prompt wird nicht veröffentlicht. Um benutzerdefinierte Anweisungen hinzuzufügen, verwenden Sie `CLAUDE.md` Dateien oder das Flag `--append-system-prompt`.

### Sensible Dateien ausschließen

Um zu verhindern, dass Claude Code auf Dateien mit sensiblen Informationen wie API-Schlüsseln, Geheimnissen und Umgebungsdateien zugreift, verwenden Sie die `permissions.deny` Einstellung in Ihrer `.claude/settings.json` Datei:

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Dies ersetzt die veraltete `ignorePatterns` Konfiguration. Dateien, die diesen Mustern entsprechen, werden von der Dateiermittlung und Suchergebnissen ausgeschlossen, und Lesevorgänge auf diesen Dateien werden verweigert.

## Subagent-Konfiguration

Claude Code unterstützt benutzerdefinierte KI-Subagents, die auf Benutzer- und Projektebene konfiguriert werden können. Diese Subagents werden als Markdown-Dateien mit YAML-Frontmatter gespeichert:

* **Benutzer-Subagents**: `~/.claude/agents/` - Verfügbar über alle Ihre Projekte
* **Projekt-Subagents**: `.claude/agents/` - Spezifisch für Ihr Projekt und können mit Ihrem Team geteilt werden

Subagent-Dateien definieren spezialisierte KI-Assistenten mit benutzerdefinierten Prompts und Tool-Berechtigungen. Erfahren Sie mehr über das Erstellen und Verwenden von Subagents in der [Subagents-Dokumentation](/de/sub-agents).

## Plugin-Konfiguration

Claude Code unterstützt ein Plugin-System, das es Ihnen ermöglicht, die Funktionalität mit Skills, Agents, Hooks und MCP-Servern zu erweitern. Plugins werden über Marketplaces verteilt und können auf Benutzer- und Repository-Ebene konfiguriert werden.

### Plugin-Einstellungen

Plugin-bezogene Einstellungen in `settings.json`:

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

Steuert, welche Plugins aktiviert sind. Format: `"plugin-name@marketplace-name": true/false`

**Bereiche**:

* **Benutzereinstellungen** (`~/.claude/settings.json`): Persönliche Plugin-Voreinstellungen
* **Projekteinstellungen** (`.claude/settings.json`): Projektspezifische Plugins, die mit dem Team geteilt werden
* **Lokale Einstellungen** (`.claude/settings.local.json`): Pro-Maschinen-Überschreibungen (nicht eingecheckt)

**Beispiel**:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Definiert zusätzliche Marketplaces, die für das Repository verfügbar gemacht werden sollten. Normalerweise in Repository-Ebenen-Einstellungen verwendet, um sicherzustellen, dass Teamkollegen Zugriff auf erforderliche Plugin-Quellen haben.

**Wenn ein Repository `extraKnownMarketplaces` enthält**:

1. Teamkollegen werden aufgefordert, den Marketplace zu installieren, wenn sie den Ordner vertrauen
2. Teamkollegen werden dann aufgefordert, Plugins aus diesem Marketplace zu installieren
3. Benutzer können unerwünschte Marketplaces oder Plugins überspringen (in Benutzereinstellungen gespeichert)
4. Die Installation respektiert Vertrauensgrenzen und erfordert explizite Zustimmung

**Beispiel**:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Marketplace-Quellentypen**:

* `github`: GitHub-Repository (verwendet `repo`)
* `git`: Beliebige Git-URL (verwendet `url`)
* `directory`: Lokaler Dateisystem-Pfad (verwendet `path`, nur für Entwicklung)
* `hostPattern`: Regex-Muster zum Abgleichen von Marketplace-Hosts (verwendet `hostPattern`)

#### `strictKnownMarketplaces`

**Nur verwaltete Einstellungen**: Steuert, welche Plugin-Marketplaces Benutzer hinzufügen dürfen. Diese Einstellung kann nur in [verwalteten Einstellungen](/de/settings#settings-files) konfiguriert werden und bietet Administratoren strikte Kontrolle über Marketplace-Quellen.

**Verwaltete Einstellungsdatei-Speicherorte**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux und WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Wichtige Merkmale**:

* Nur in verwalteten Einstellungen verfügbar (`managed-settings.json`)
* Kann nicht durch Benutzer- oder Projekteinstellungen überschrieben werden (höchste Priorität)
* Durchgesetzt VOR Netzwerk-/Dateisystem-Operationen (blockierte Quellen werden nie ausgeführt)
* Verwendet exakten Abgleich für Quellspezifikationen (einschließlich `ref`, `path` für Git-Quellen), außer `hostPattern`, das Regex-Abgleich verwendet

**Allowlist-Verhalten**:

* `undefined` (Standard): Keine Einschränkungen - Benutzer können jeden Marketplace hinzufügen
* Leeres Array `[]`: Vollständiger Lockdown - Benutzer können keine neuen Marketplaces hinzufügen
* Liste von Quellen: Benutzer können nur Marketplaces hinzufügen, die genau übereinstimmen

**Alle unterstützten Quellentypen**:

Die Allowlist unterstützt sieben Marketplace-Quellentypen. Die meisten Quellen verwenden exakten Abgleich, während `hostPattern` Regex-Abgleich gegen den Marketplace-Host verwendet.

1. **GitHub-Repositories**:

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Felder: `repo` (erforderlich), `ref` (optional: Branch/Tag/SHA), `path` (optional: Unterverzeichnis)

2. **Git-Repositories**:

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Felder: `url` (erforderlich), `ref` (optional: Branch/Tag/SHA), `path` (optional: Unterverzeichnis)

3. **URL-basierte Marketplaces**:

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Felder: `url` (erforderlich), `headers` (optional: HTTP-Header für authentifizierten Zugriff)

<Note>
  URL-basierte Marketplaces laden nur die `marketplace.json` Datei herunter. Sie laden keine Plugin-Dateien vom Server herunter. Plugins in URL-basierten Marketplaces müssen externe Quellen (GitHub, npm oder Git-URLs) verwenden, anstatt relative Pfade. Für Plugins mit relativen Pfaden verwenden Sie stattdessen einen Git-basierten Marketplace. Siehe [Troubleshooting](/de/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) für Details.
</Note>

4. **NPM-Pakete**:

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Felder: `package` (erforderlich, unterstützt scoped Pakete)

5. **Dateipfade**:

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Felder: `path` (erforderlich: absoluter Pfad zur marketplace.json Datei)

6. **Verzeichnispfade**:

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Felder: `path` (erforderlich: absoluter Pfad zum Verzeichnis mit `.claude-plugin/marketplace.json`)

7. **Host-Muster-Abgleich**:

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Felder: `hostPattern` (erforderlich: Regex-Muster zum Abgleich gegen den Marketplace-Host)

Verwenden Sie Host-Muster-Abgleich, wenn Sie alle Marketplaces von einem bestimmten Host erlauben möchten, ohne jedes Repository einzeln aufzuzählen. Dies ist nützlich für Organisationen mit internen GitHub Enterprise oder GitLab-Servern, auf denen Entwickler ihre eigenen Marketplaces erstellen.

Host-Extraktion nach Quellentyp:

* `github`: passt immer gegen `github.com`
* `git`: extrahiert Hostname aus der URL (unterstützt sowohl HTTPS als auch SSH-Formate)
* `url`: extrahiert Hostname aus der URL
* `npm`, `file`, `directory`: nicht unterstützt für Host-Muster-Abgleich

**Konfigurationsbeispiele**:

Beispiel: Nur bestimmte Marketplaces erlauben:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Beispiel - Alle Marketplace-Ergänzungen deaktivieren:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Beispiel: Alle Marketplaces von einem internen Git-Server erlauben:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Anforderungen für exakten Abgleich**:

Marketplace-Quellen müssen **genau** übereinstimmen, damit eine Benutzer-Ergänzung erlaubt wird. Für Git-basierte Quellen (`github` und `git`) umfasst dies alle optionalen Felder:

* Das `repo` oder `url` muss genau übereinstimmen
* Das `ref` Feld muss genau übereinstimmen (oder beide sind undefined)
* Das `path` Feld muss genau übereinstimmen (oder beide sind undefined)

Beispiele von Quellen, die **NICHT übereinstimmen**:

```json  theme={null}
// Diese sind UNTERSCHIEDLICHE Quellen:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Diese sind auch UNTERSCHIEDLICH:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Vergleich mit `extraKnownMarketplaces`**:

| Aspekt                        | `strictKnownMarketplaces`                 | `extraKnownMarketplaces`                         |
| ----------------------------- | ----------------------------------------- | ------------------------------------------------ |
| **Zweck**                     | Durchsetzung von Organisationsrichtlinien | Team-Komfort                                     |
| **Einstellungsdatei**         | Nur `managed-settings.json`               | Beliebige Einstellungsdatei                      |
| **Verhalten**                 | Blockiert nicht-whitelisted Ergänzungen   | Auto-installiert fehlende Marketplaces           |
| **Wann durchgesetzt**         | Vor Netzwerk-/Dateisystem-Operationen     | Nach Benutzer-Vertrauens-Prompt                  |
| **Kann überschrieben werden** | Nein (höchste Priorität)                  | Ja (durch höherrangige Einstellungen)            |
| **Quellenformat**             | Direktes Quellobjekt                      | Benannter Marketplace mit verschachtelter Quelle |
| **Anwendungsfall**            | Compliance, Sicherheitsbeschränkungen     | Onboarding, Standardisierung                     |

**Format-Unterschied**:

`strictKnownMarketplaces` verwendet direkte Quellobjekte:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` erfordert benannte Marketplaces:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Wichtige Hinweise**:

* Einschränkungen werden VOR Netzwerkanfragen oder Dateisystem-Operationen überprüft
* Wenn blockiert, sehen Benutzer klare Fehlermeldungen, die angeben, dass die Quelle durch verwaltete Richtlinie blockiert ist
* Die Einschränkung gilt nur für das Hinzufügen von NEUEN Marketplaces; zuvor installierte Marketplaces bleiben zugänglich
* Verwaltete Einstellungen haben die höchste Priorität und können nicht überschrieben werden

Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions) für Dokumentation für Benutzer.

### Plugins verwalten

Verwenden Sie den `/plugin` Befehl, um Plugins interaktiv zu verwalten:

* Durchsuchen Sie verfügbare Plugins aus Marketplaces
* Installieren/Deinstallieren Sie Plugins
* Aktivieren/Deaktivieren Sie Plugins
* Zeigen Sie Plugin-Details an (bereitgestellte Befehle, Agents, Hooks)
* Fügen Sie Marketplaces hinzu/entfernen Sie sie

Erfahren Sie mehr über das Plugin-System in der [Plugins-Dokumentation](/de/plugins).

## Umgebungsvariablen

Claude Code unterstützt die folgenden Umgebungsvariablen, um sein Verhalten zu steuern:

<Note>
  Alle Umgebungsvariablen können auch in [`settings.json`](#available-settings) konfiguriert werden. Dies ist nützlich, um Umgebungsvariablen automatisch für jede Sitzung zu setzen oder einen Satz von Umgebungsvariablen für Ihr ganzes Team oder Ihre ganze Organisation bereitzustellen.
</Note>

| Variable                                       | Zweck                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | API-Schlüssel, der als `X-Api-Key` Header gesendet wird, normalerweise für das Claude SDK (für interaktive Nutzung führen Sie `/login` aus)                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `ANTHROPIC_AUTH_TOKEN`                         | Benutzerdefinierter Wert für den `Authorization` Header (der Wert, den Sie hier setzen, wird mit `Bearer ` vorangestellt)                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | Benutzerdefinierte Header, die zu Anfragen hinzugefügt werden sollen (`Name: Value` Format, zeilengetrennt für mehrere Header)                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | Siehe [Modellkonfiguration](/de/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | Siehe [Modellkonfiguration](/de/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | Siehe [Modellkonfiguration](/de/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | API-Schlüssel für Microsoft Foundry-Authentifizierung (siehe [Microsoft Foundry](/de/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | Vollständige Basis-URL für die Foundry-Ressource (z. B. `https://my-resource.services.ai.azure.com/anthropic`). Alternative zu `ANTHROPIC_FOUNDRY_RESOURCE` (siehe [Microsoft Foundry](/de/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Foundry-Ressourcenname (z. B. `my-resource`). Erforderlich, wenn `ANTHROPIC_FOUNDRY_BASE_URL` nicht gesetzt ist (siehe [Microsoft Foundry](/de/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_MODEL`                              | Name der zu verwendenden Modelleinstellung (siehe [Modellkonfiguration](/de/model-config#environment-variables))                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[VERALTET] Name des [Haiku-Klasse-Modells für Hintergrundaufgaben](/de/costs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Überschreiben Sie die AWS-Region für das Haiku-Klasse-Modell bei Verwendung von Bedrock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Bedrock API-Schlüssel für Authentifizierung (siehe [Bedrock API-Schlüssel](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | Standard-Timeout für lang laufende Bash-Befehle                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | Maximale Anzahl von Zeichen in Bash-Ausgaben, bevor sie in der Mitte gekürzt werden                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `BASH_MAX_TIMEOUT_MS`                          | Maximales Timeout, das das Modell für lang laufende Bash-Befehle setzen kann                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | Setzen Sie den Prozentsatz der Kontextkapazität (1-100), bei dem Auto-Komprimierung ausgelöst wird. Standardmäßig wird Auto-Komprimierung bei etwa 95% Kapazität ausgelöst. Verwenden Sie niedrigere Werte wie `50`, um früher zu komprimieren. Werte über dem Standard-Schwellenwert haben keine Auswirkung. Gilt für Hauptkonversationen und Subagents. Dieser Prozentsatz entspricht dem Feld `context_window.used_percentage`, das in [Statuszeile](/de/statusline) verfügbar ist                                                                                            |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | Kehren Sie nach jedem Bash-Befehl zum ursprünglichen Arbeitsverzeichnis zurück                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | Konto-UUID für den authentifizierten Benutzer. Wird von SDK-Aufrufern verwendet, um Kontoinformationen synchron bereitzustellen und eine Racebedingung zu vermeiden, bei der frühe Telemetrie-Ereignisse keine Kontometadaten haben. Erfordert, dass auch `CLAUDE_CODE_USER_EMAIL` und `CLAUDE_CODE_ORGANIZATION_UUID` gesetzt sind                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Auf `1` setzen, um CLAUDE.md Dateien aus Verzeichnissen zu laden, die mit `--add-dir` angegeben sind. Standardmäßig laden zusätzliche Verzeichnisse keine Memory-Dateien                                                                                                                                                                                                                                                                                                                                                                                                         | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | Intervall in Millisekunden, in dem Anmeldedaten aktualisiert werden sollten (bei Verwendung von `apiKeyHelper`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | Pfad zur Client-Zertifikatsdatei für mTLS-Authentifizierung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | Pfad zur privaten Client-Schlüsseldatei für mTLS-Authentifizierung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | Passphrase für verschlüsselten CLAUDE\_CODE\_CLIENT\_KEY (optional)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | Auf `1` setzen, um die Unterstützung des [1M-Kontextfensters](/de/model-config#extended-context) zu deaktivieren. Wenn gesetzt, sind 1M-Modellvarianten im Modellwähler nicht verfügbar. Nützlich für Unternehmensumgebungen mit Compliance-Anforderungen                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Auf `1` setzen, um [adaptives Denken](/de/model-config#adjust-effort-level) für Opus 4.6 und Sonnet 4.6 zu deaktivieren. Wenn deaktiviert, fallen diese Modelle auf das feste Denk-Budget zurück, das von `MAX_THINKING_TOKENS` gesteuert wird                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | Auf `1` setzen, um [Auto-Memory](/de/memory#auto-memory) zu deaktivieren. Auf `0` setzen, um Auto-Memory während des schrittweisen Rollouts zu erzwingen. Wenn deaktiviert, erstellt oder lädt Claude keine Auto-Memory-Dateien                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Auf `1` setzen, um integrierte Commit- und PR-Workflow-Anweisungen aus Claudes System-Prompt zu entfernen. Nützlich bei Verwendung Ihrer eigenen Git-Workflow-Skills. Hat Vorrang vor der [`includeGitInstructions`](#available-settings) Einstellung, wenn gesetzt                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | Auf `1` setzen, um alle Hintergrundaufgaben-Funktionalität zu deaktivieren, einschließlich des Parameters `run_in_background` auf Bash- und Subagent-Tools, Auto-Backgrounding und der Ctrl+B-Verknüpfung                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | Auf `1` setzen, um [geplante Aufgaben](/de/scheduled-tasks) zu deaktivieren. Der `/loop` Skill und Cron-Tools werden nicht verfügbar und alle bereits geplanten Aufgaben stoppen, einschließlich Aufgaben, die bereits mitten in der Sitzung laufen                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Auf `1` setzen, um Anthropic API-spezifische `anthropic-beta` Header zu deaktivieren. Verwenden Sie dies, wenn Sie Probleme wie "Unexpected value(s) for the `anthropic-beta` header" bei Verwendung eines LLM-Gateways mit Drittanbieter-Providern haben                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | Auf `1` setzen, um [schnellen Modus](/de/fast-mode) zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | Auf `1` setzen, um die Umfragen zur Sitzungsqualität "How is Claude doing?" zu deaktivieren. Auch deaktiviert bei Verwendung von Drittanbieter-Providern oder wenn Telemetrie deaktiviert ist. Siehe [Umfragen zur Sitzungsqualität](/de/data-usage#session-quality-surveys)                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | Äquivalent zum Setzen von `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING` und `DISABLE_TELEMETRY`                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | Auf `1` setzen, um automatische Terminal-Titel-Updates basierend auf Konversationskontext zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | Setzen Sie die Anstrengungsebene für unterstützte Modelle. Werte: `low`, `medium`, `high`. Niedrigere Anstrengung ist schneller und billiger, höhere Anstrengung bietet tieferes Denken. Unterstützt auf Opus 4.6 und Sonnet 4.6. Siehe [Anstrengungsebene anpassen](/de/model-config#adjust-effort-level)                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | Auf `false` setzen, um Prompt-Vorschläge zu deaktivieren (der Umschalter "Prompt suggestions" in `/config`). Dies sind die ausgegraut angezeigten Vorhersagen, die nach Claudes Antwort in Ihrer Prompt-Eingabe erscheinen. Siehe [Prompt-Vorschläge](/de/interactive-mode#prompt-suggestions)                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | Auf `false` setzen, um vorübergehend zur vorherigen TODO-Liste anstelle des Task-Tracking-Systems zurückzukehren. Standard: `true`. Siehe [Task-Liste](/de/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | Auf `1` setzen, um OpenTelemetry-Datenerfassung für Metriken und Protokollierung zu aktivieren. Erforderlich, bevor OTel-Exporter konfiguriert werden. Siehe [Monitoring](/de/monitoring-usage)                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | Zeit in Millisekunden, die nach dem Leerlaufen der Abfrageschleife gewartet werden soll, bevor automatisch beendet wird. Nützlich für automatisierte Workflows und Skripte mit SDK-Modus                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | Auf `1` setzen, um [Agent-Teams](/de/agent-teams) zu aktivieren. Agent-Teams sind experimentell und standardmäßig deaktiviert                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | Überschreiben Sie das Standard-Token-Limit für Dateilesevorgänge. Nützlich, wenn Sie größere Dateien vollständig lesen müssen                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Auf `1` setzen, um Ihre E-Mail-Adresse und Organisationsnamen aus der Claude Code-Benutzeroberfläche auszublenden. Nützlich beim Streamen oder Aufzeichnen                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | Überspringen Sie die automatische Installation von IDE-Erweiterungen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | Setzen Sie die maximale Anzahl von Ausgabe-Tokens für die meisten Anfragen. Standard: 32.000. Maximum: 64.000. Das Erhöhen dieses Wertes reduziert das verfügbare effektive Kontextfenster, bevor [Auto-Komprimierung](/de/costs#reduce-token-usage) ausgelöst wird.                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | Organisations-UUID für den authentifizierten Benutzer. Wird von SDK-Aufrufern verwendet, um Kontoinformationen synchron bereitzustellen. Erfordert, dass auch `CLAUDE_CODE_ACCOUNT_UUID` und `CLAUDE_CODE_USER_EMAIL` gesetzt sind                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | Intervall zum Aktualisieren dynamischer OpenTelemetry-Header in Millisekunden (Standard: 1740000 / 29 Minuten). Siehe [Dynamische Header](/de/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | Auto-gesetzt auf `true` auf [Agent-Team](/de/agent-teams) Teamkollegen, die Plan-Genehmigung erfordern. Schreibgeschützt: wird von Claude Code beim Spawnen von Teamkollegen gesetzt. Siehe [Plan-Genehmigung erforderlich](/de/agent-teams#require-plan-approval-for-teammates)                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | Timeout in Millisekunden für Git-Operationen beim Installieren oder Aktualisieren von Plugins (Standard: 120000). Erhöhen Sie diesen Wert für große Repositories oder langsame Netzwerkverbindungen. Siehe [Git-Operationen Timeout](/de/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | Auf `true` setzen, um dem Proxy zu erlauben, DNS-Auflösung durchzuführen, anstatt des Aufrufers. Opt-in für Umgebungen, in denen der Proxy die Hostname-Auflösung durchführen sollte                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_SHELL`                            | Überschreiben Sie die automatische Shell-Erkennung. Nützlich, wenn sich Ihre Login-Shell von Ihrer bevorzugten Arbeits-Shell unterscheidet (z. B. `bash` vs `zsh`)                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | Befehlspräfix zum Umhüllen aller Bash-Befehle (z. B. für Protokollierung oder Auditing). Beispiel: `/path/to/logger.sh` führt `/path/to/logger.sh <command>` aus                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SIMPLE`                           | Auf `1` setzen, um mit einem minimalen System-Prompt und nur den Tools Bash, Dateilesevorgänge und Dateibearbeitung auszuführen. Deaktiviert MCP-Tools, Anhänge, Hooks und CLAUDE.md Dateien                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Überspringen Sie die AWS-Authentifizierung für Bedrock (z. B. bei Verwendung eines LLM-Gateways)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Überspringen Sie die Azure-Authentifizierung für Microsoft Foundry (z. B. bei Verwendung eines LLM-Gateways)                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Überspringen Sie die Google-Authentifizierung für Vertex (z. B. bei Verwendung eines LLM-Gateways)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | Siehe [Modellkonfiguration](/de/model-config)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | Teilen Sie eine Task-Liste über Sitzungen hinweg. Setzen Sie die gleiche ID in mehreren Claude Code-Instanzen, um an einer gemeinsamen Task-Liste zu koordinieren. Siehe [Task-Liste](/de/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_TEAM_NAME`                        | Name des Agent-Teams, zu dem dieser Teamkollege gehört. Wird automatisch auf [Agent-Team](/de/agent-teams) Mitgliedern gesetzt                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_TMPDIR`                           | Überschreiben Sie das Temp-Verzeichnis, das für interne Temp-Dateien verwendet wird. Claude Code hängt `/claude/` an diesen Pfad an. Standard: `/tmp` auf Unix/macOS, `os.tmpdir()` auf Windows                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_USER_EMAIL`                       | E-Mail-Adresse für den authentifizierten Benutzer. Wird von SDK-Aufrufern verwendet, um Kontoinformationen synchron bereitzustellen. Erfordert, dass auch `CLAUDE_CODE_ACCOUNT_UUID` und `CLAUDE_CODE_ORGANIZATION_UUID` gesetzt sind                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | Verwenden Sie [Bedrock](/de/amazon-bedrock)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | Verwenden Sie [Microsoft Foundry](/de/microsoft-foundry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_USE_VERTEX`                       | Verwenden Sie [Vertex](/de/google-vertex-ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CONFIG_DIR`                            | Passen Sie an, wo Claude Code seine Konfiguration und Datendateien speichert                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `DISABLE_AUTOUPDATER`                          | Auf `1` setzen, um automatische Updates zu deaktivieren.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_BUG_COMMAND`                          | Auf `1` setzen, um den `/bug` Befehl zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_COST_WARNINGS`                        | Auf `1` setzen, um Kostenwarnnachrichten zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_ERROR_REPORTING`                      | Auf `1` setzen, um sich von Sentry-Fehlerberichten abzumelden                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_INSTALLATION_CHECKS`                  | Auf `1` setzen, um Installationswarnungen zu deaktivieren. Verwenden Sie nur, wenn Sie den Installationsort manuell verwalten, da dies Probleme mit Standardinstallationen maskieren kann                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | Auf `1` setzen, um Modellaufrufe für nicht kritische Pfade wie Flavor-Text zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `DISABLE_PROMPT_CACHING`                       | Auf `1` setzen, um Prompt-Caching für alle Modelle zu deaktivieren (hat Vorrang vor Pro-Modell-Einstellungen)                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Auf `1` setzen, um Prompt-Caching für Haiku-Modelle zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Auf `1` setzen, um Prompt-Caching für Opus-Modelle zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Auf `1` setzen, um Prompt-Caching für Sonnet-Modelle zu deaktivieren                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_TELEMETRY`                            | Auf `1` setzen, um sich von Statsig-Telemetrie abzumelden (beachten Sie, dass Statsig-Ereignisse keine Benutzerdaten wie Code, Dateipfade oder Bash-Befehle enthalten)                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Auf `false` setzen, um [claude.ai MCP-Server](/de/mcp#use-mcp-servers-from-claudeai) in Claude Code zu deaktivieren. Standardmäßig für angemeldete Benutzer aktiviert                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `ENABLE_TOOL_SEARCH`                           | Steuert [MCP-Tool-Suche](/de/mcp#scale-with-mcp-tool-search). Werte: `auto` (Standard, aktiviert bei 10% Kontext), `auto:N` (benutzerdefinierter Schwellenwert, z. B. `auto:5` für 5%), `true` (immer an), `false` (deaktiviert)                                                                                                                                                                                                                                                                                                                                                 |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | Auf `true` setzen, um Plugin-Auto-Updates zu erzwingen, auch wenn der Haupt-Auto-Updater über `DISABLE_AUTOUPDATER` deaktiviert ist                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `HTTP_PROXY`                                   | Geben Sie den HTTP-Proxy-Server für Netzwerkverbindungen an                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `HTTPS_PROXY`                                  | Geben Sie den HTTPS-Proxy-Server für Netzwerkverbindungen an                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `IS_DEMO`                                      | Auf `true` setzen, um Demo-Modus zu aktivieren: verbirgt E-Mail und Organisation aus der Benutzeroberfläche, überspringt Onboarding und verbirgt interne Befehle. Nützlich zum Streamen oder Aufzeichnen von Sitzungen                                                                                                                                                                                                                                                                                                                                                           |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | Maximale Anzahl von Tokens, die in MCP-Tool-Antworten zulässig sind. Claude Code zeigt eine Warnung an, wenn die Ausgabe 10.000 Tokens überschreitet (Standard: 25000)                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `MAX_THINKING_TOKENS`                          | Überschreiben Sie das [erweitertes Denken](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) Token-Budget. Denken ist standardmäßig mit maximalem Budget (31.999 Tokens) aktiviert. Verwenden Sie dies, um das Budget zu begrenzen (z. B. `MAX_THINKING_TOKENS=10000`) oder Denken vollständig zu deaktivieren (`MAX_THINKING_TOKENS=0`). Für Opus 4.6 wird die Denk-Tiefe durch [Anstrengungsebene](/de/model-config#adjust-effort-level) gesteuert, und diese Variable wird ignoriert, es sei denn, sie ist auf `0` gesetzt, um Denken zu deaktivieren. |     |
| `MCP_CLIENT_SECRET`                            | OAuth-Client-Secret für MCP-Server, die [vorkonfigurierte Anmeldedaten](/de/mcp#use-pre-configured-oauth-credentials) erfordern. Vermeidet die interaktive Eingabeaufforderung beim Hinzufügen eines Servers mit `--client-secret`                                                                                                                                                                                                                                                                                                                                               |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | Fester Port für den OAuth-Redirect-Callback, als Alternative zu `--callback-port` beim Hinzufügen eines MCP-Servers mit [vorkonfigurierten Anmeldedaten](/de/mcp#use-pre-configured-oauth-credentials)                                                                                                                                                                                                                                                                                                                                                                           |     |
| `MCP_TIMEOUT`                                  | Timeout in Millisekunden für MCP-Server-Start                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `MCP_TOOL_TIMEOUT`                             | Timeout in Millisekunden für MCP-Tool-Ausführung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `NO_PROXY`                                     | Liste von Domänen und IPs, an die Anfragen direkt gestellt werden, wobei der Proxy umgangen wird                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | Überschreiben Sie das Zeichen-Budget für Skill-Metadaten, die dem [Skill-Tool](/de/skills#control-who-invokes-a-skill) angezeigt werden. Das Budget skaliert dynamisch bei 2% des Kontextfensters, mit einem Fallback von 16.000 Zeichen. Legacy-Name für Rückwärtskompatibilität beibehalten                                                                                                                                                                                                                                                                                    |     |
| `USE_BUILTIN_RIPGREP`                          | Auf `0` setzen, um das systeminstallierte `rg` anstelle des mit Claude Code enthaltenen `rg` zu verwenden                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Überschreiben Sie die Region für Claude 3.5 Haiku bei Verwendung von Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Überschreiben Sie die Region für Claude 3.7 Sonnet bei Verwendung von Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Überschreiben Sie die Region für Claude 4.0 Opus bei Verwendung von Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Überschreiben Sie die Region für Claude 4.0 Sonnet bei Verwendung von Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Überschreiben Sie die Region für Claude 4.1 Opus bei Verwendung von Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |

## Tools, die Claude zur Verfügung stehen

Claude Code hat Zugriff auf eine Reihe leistungsstarker Tools, die ihm helfen, Ihre Codebasis zu verstehen und zu ändern:

| Tool                     | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                       | Berechtigung erforderlich |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------ |
| **Agent**                | Spawnt einen [Subagent](/de/sub-agents) mit eigenem Kontextfenster, um eine Aufgabe zu bewältigen                                                                                                                                                                                                                                                                                                                  | Nein                      |
| **AskUserQuestion**      | Stellt Multiple-Choice-Fragen, um Anforderungen zu sammeln oder Mehrdeutigkeit zu klären                                                                                                                                                                                                                                                                                                                           | Nein                      |
| **Bash**                 | Führt Shell-Befehle in Ihrer Umgebung aus. Siehe [Bash-Tool-Verhalten](#bash-tool-behavior)                                                                                                                                                                                                                                                                                                                        | Ja                        |
| **CronCreate**           | Plant eine wiederkehrende oder einmalige Eingabeaufforderung innerhalb der aktuellen Sitzung (weg, wenn Claude beendet wird). Siehe [geplante Aufgaben](/de/scheduled-tasks)                                                                                                                                                                                                                                       | Nein                      |
| **CronDelete**           | Bricht eine geplante Aufgabe nach ID ab                                                                                                                                                                                                                                                                                                                                                                            | Nein                      |
| **CronList**             | Listet alle geplanten Aufgaben in der Sitzung auf                                                                                                                                                                                                                                                                                                                                                                  | Nein                      |
| **Edit**                 | Nimmt gezielte Bearbeitungen an bestimmten Dateien vor                                                                                                                                                                                                                                                                                                                                                             | Ja                        |
| **EnterPlanMode**        | Wechselt in den Plan-Modus, um einen Ansatz vor dem Codieren zu entwerfen                                                                                                                                                                                                                                                                                                                                          | Nein                      |
| **EnterWorktree**        | Erstellt einen isolierten [Git-Worktree](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) und wechselt hinein                                                                                                                                                                                                                                                                            | Nein                      |
| **ExitPlanMode**         | Präsentiert einen Plan zur Genehmigung und beendet den Plan-Modus                                                                                                                                                                                                                                                                                                                                                  | Ja                        |
| **ExitWorktree**         | Beendet eine Worktree-Sitzung und kehrt zum ursprünglichen Verzeichnis zurück                                                                                                                                                                                                                                                                                                                                      | Nein                      |
| **Glob**                 | Findet Dateien basierend auf Musterabgleich                                                                                                                                                                                                                                                                                                                                                                        | Nein                      |
| **Grep**                 | Sucht nach Mustern in Dateiinhalten                                                                                                                                                                                                                                                                                                                                                                                | Nein                      |
| **ListMcpResourcesTool** | Listet Ressourcen auf, die von verbundenen [MCP-Servern](/de/mcp) bereitgestellt werden                                                                                                                                                                                                                                                                                                                            | Nein                      |
| **LSP**                  | Code-Intelligenz über Sprachserver. Meldet Typfehler und Warnungen automatisch nach Dateibearbeitungen. Unterstützt auch Navigationsvorgänge: Sprung zu Definitionen, Suche nach Referenzen, Typinformationen abrufen, Symbole auflisten, Implementierungen finden, Call-Hierarchien verfolgen. Erfordert ein [Code-Intelligence-Plugin](/de/discover-plugins#code-intelligence) und seine Sprachserver-Binärdatei | Nein                      |
| **NotebookEdit**         | Ändert Jupyter-Notebook-Zellen                                                                                                                                                                                                                                                                                                                                                                                     | Ja                        |
| **Read**                 | Liest den Inhalt von Dateien                                                                                                                                                                                                                                                                                                                                                                                       | Nein                      |
| **ReadMcpResourceTool**  | Liest eine bestimmte MCP-Ressource nach URI                                                                                                                                                                                                                                                                                                                                                                        | Nein                      |
| **Skill**                | Führt einen [Skill](/de/skills#control-who-invokes-a-skill) innerhalb der Hauptkonversation aus                                                                                                                                                                                                                                                                                                                    | Ja                        |
| **TaskCreate**           | Erstellt eine neue Aufgabe in der Task-Liste                                                                                                                                                                                                                                                                                                                                                                       | Nein                      |
| **TaskGet**              | Ruft vollständige Details für eine bestimmte Aufgabe ab                                                                                                                                                                                                                                                                                                                                                            | Nein                      |
| **TaskList**             | Listet alle Aufgaben mit ihrem aktuellen Status auf                                                                                                                                                                                                                                                                                                                                                                | Nein                      |
| **TaskOutput**           | Ruft Ausgabe von einer Hintergrundaufgabe ab                                                                                                                                                                                                                                                                                                                                                                       | Nein                      |
| **TaskStop**             | Beendet eine laufende Hintergrundaufgabe nach ID                                                                                                                                                                                                                                                                                                                                                                   | Nein                      |
| **TaskUpdate**           | Aktualisiert Task-Status, Abhängigkeiten, Details oder löscht Aufgaben                                                                                                                                                                                                                                                                                                                                             | Nein                      |
| **TodoWrite**            | Verwaltet die Session-Task-Checkliste. Verfügbar im nicht-interaktiven Modus und dem [Agent SDK](/de/headless); interaktive Sitzungen verwenden stattdessen TaskCreate, TaskGet, TaskList und TaskUpdate                                                                                                                                                                                                           | Nein                      |
| **ToolSearch**           | Sucht nach und lädt aufgeschobene Tools, wenn [Tool-Suche](/de/mcp#scale-with-mcp-tool-search) aktiviert ist                                                                                                                                                                                                                                                                                                       | Nein                      |
| **WebFetch**             | Ruft Inhalte von einer angegebenen URL ab                                                                                                                                                                                                                                                                                                                                                                          | Ja                        |
| **WebSearch**            | Führt Web-Suchen durch                                                                                                                                                                                                                                                                                                                                                                                             | Ja                        |
| **Write**                | Erstellt oder überschreibt Dateien                                                                                                                                                                                                                                                                                                                                                                                 | Ja                        |

Berechtigungsregeln können mit `/allowed-tools` oder in [Berechtigungseinstellungen](/de/settings#available-settings) konfiguriert werden. Siehe auch [Tool-spezifische Berechtigungsregeln](/de/permissions#tool-specific-permission-rules).

### Bash-Tool-Verhalten

Das Bash-Tool führt Shell-Befehle mit folgendem Persistenz-Verhalten aus:

* **Arbeitsverzeichnis bleibt bestehen**: Wenn Claude das Arbeitsverzeichnis ändert (z. B. `cd /path/to/dir`), werden nachfolgende Bash-Befehle in diesem Verzeichnis ausgeführt. Sie können `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` verwenden, um nach jedem Befehl zum Projektverzeichnis zurückzukehren.
* **Umgebungsvariablen bleiben NICHT bestehen**: Umgebungsvariablen, die in einem Bash-Befehl gesetzt werden (z. B. `export MY_VAR=value`), sind **nicht** in nachfolgenden Bash-Befehlen verfügbar. Jeder Bash-Befehl wird in einer frischen Shell-Umgebung ausgeführt.

Um Umgebungsvariablen in Bash-Befehlen verfügbar zu machen, haben Sie **drei Optionen**:

**Option 1: Aktivieren Sie die Umgebung vor dem Start von Claude Code** (einfachster Ansatz)

Aktivieren Sie Ihre virtuelle Umgebung in Ihrem Terminal, bevor Sie Claude Code starten:

```bash  theme={null}
conda activate myenv
# oder: source /path/to/venv/bin/activate
claude
```

Dies funktioniert für Shell-Umgebungen, aber Umgebungsvariablen, die in Claudes Bash-Befehlen gesetzt werden, bleiben nicht zwischen Befehlen bestehen.

**Option 2: Setzen Sie CLAUDE\_ENV\_FILE vor dem Start von Claude Code** (persistente Umgebungseinrichtung)

Exportieren Sie den Pfad zu einem Shell-Skript, das Ihre Umgebungseinrichtung enthält:

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Wobei `/path/to/env-setup.sh` enthält:

```bash  theme={null}
conda activate myenv
# oder: source /path/to/venv/bin/activate
# oder: export MY_VAR=value
```

Claude Code wird dieses Skript vor jedem Bash-Befehl sourcing, wodurch die Umgebung über alle Befehle hinweg persistent wird.

**Option 3: Verwenden Sie einen SessionStart-Hook** (projektspezifische Konfiguration)

Konfigurieren Sie in `.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

Der Hook schreibt in `$CLAUDE_ENV_FILE`, das dann vor jedem Bash-Befehl gesourced wird. Dies ist ideal für teamübergreifende Projektkonfigurationen.

Siehe [SessionStart-Hooks](/de/hooks#persist-environment-variables) für weitere Details zu Option 3.

### Tools mit Hooks erweitern

Sie können benutzerdefinierte Befehle vor oder nach der Ausführung eines Tools ausführen, indem Sie [Claude Code Hooks](/de/hooks-guide) verwenden.

Sie könnten beispielsweise automatisch einen Python-Formatter ausführen, nachdem Claude Python-Dateien ändert, oder Änderungen an Produktionskonfigurationsdateien blockieren, indem Sie Write-Operationen auf bestimmte Pfade blockieren.

## Siehe auch

* [Berechtigungen](/de/permissions): Berechtigungssystem, Regelsyntax, Tool-spezifische Muster und verwaltete Richtlinien
* [Authentifizierung](/de/authentication): Richten Sie Benutzerzugriff auf Claude Code ein
* [Troubleshooting](/de/troubleshooting): Lösungen für häufige Konfigurationsprobleme
