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
| **Lokal**     | `.claude/settings.local.json`                                                             | Sie, nur in diesem Repository         | Nein (gitignoriert)        |

### Wann sollte jeder Bereich verwendet werden

Der **Verwaltungsbereich** ist für:

* Sicherheitsrichtlinien, die organisationsweit durchgesetzt werden müssen
* Compliance-Anforderungen, die nicht überschrieben werden können
* Standardisierte Konfigurationen, die von IT/DevOps bereitgestellt werden

Der **Benutzerbereich** ist am besten für:

* Persönliche Voreinstellungen, die Sie überall haben möchten (Designs, Editor-Einstellungen)
* Tools und Plugins, die Sie in allen Projekten verwenden
* API-Schlüssel und Authentifizierung (sicher gespeichert)

Der **Projektbereich** ist am besten für:

* Teamübergreifend gemeinsame Einstellungen (Berechtigungen, Hooks, MCP-Server)
* Plugins, die das gesamte Team haben sollte
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

Wenn beispielsweise eine Berechtigung in Benutzereinstellungen erlaubt, aber in Projekteinstellungen verweigert wird, hat die Projekteinstellung Vorrang und die Berechtigung wird blockiert.

### Was verwendet Bereiche

Bereiche gelten für viele Claude Code-Funktionen:

| Funktion          | Benutzerort               | Projektort                           | Lokaler Ort                    |
| :---------------- | :------------------------ | :----------------------------------- | :----------------------------- |
| **Einstellungen** | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json`  |
| **Subagents**     | `~/.claude/agents/`       | `.claude/agents/`                    | Keine                          |
| **MCP-Server**    | `~/.claude.json`          | `.mcp.json`                          | `~/.claude.json` (pro Projekt) |
| **Plugins**       | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json`  |
| **CLAUDE.md**     | `~/.claude/CLAUDE.md`     | `CLAUDE.md` oder `.claude/CLAUDE.md` | Keine                          |

***

## Einstellungsdateien

Die Datei `settings.json` ist der offizielle Mechanismus zur Konfiguration von Claude Code durch hierarchische Einstellungen:

* **Benutzereinstellungen** werden in `~/.claude/settings.json` definiert und gelten für alle Projekte.
* **Projekteinstellungen** werden in Ihrem Projektverzeichnis gespeichert:
  * `.claude/settings.json` für Einstellungen, die in die Versionskontrolle eingecheckt und mit Ihrem Team geteilt werden
  * `.claude/settings.local.json` für Einstellungen, die nicht eingecheckt werden, nützlich für persönliche Voreinstellungen und Experimente. Claude Code konfiguriert Git so, dass `.claude/settings.local.json` ignoriert wird, wenn sie erstellt wird.
* **Verwaltete Einstellungen**: Für Organisationen, die zentrale Kontrolle benötigen, unterstützt Claude Code mehrere Bereitstellungsmechanismen für verwaltete Einstellungen. Alle verwenden das gleiche JSON-Format und können nicht durch Benutzer- oder Projekteinstellungen überschrieben werden:

  * **Serververwaltete Einstellungen**: von Anthropics Servern über die Claude.ai-Administratorkonsole bereitgestellt. Siehe [serververwaltete Einstellungen](/de/server-managed-settings).
  * **MDM/OS-Richtlinien**: über native Geräteverwaltung auf macOS und Windows bereitgestellt:
    * macOS: `com.anthropic.claudecode` verwaltete Präferenzdomäne (bereitgestellt über Konfigurationsprofile in Jamf, Kandji oder anderen MDM-Tools)
    * Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` Registrierungsschlüssel mit einem `Settings`-Wert (REG\_SZ oder REG\_EXPAND\_SZ) mit JSON (bereitgestellt über Gruppenrichtlinie oder Intune)
    * Windows (Benutzerebene): `HKCU\SOFTWARE\Policies\ClaudeCode` (niedrigste Richtlinienpriorität, wird nur verwendet, wenn keine Admin-Quelle vorhanden ist)
  * **Dateibasiert**: `managed-settings.json` und `managed-mcp.json` in Systemverzeichnissen bereitgestellt:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux und WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      Der veraltete Windows-Pfad `C:\ProgramData\ClaudeCode\managed-settings.json` wird ab v2.1.75 nicht mehr unterstützt. Administratoren, die Einstellungen an diesem Speicherort bereitgestellt haben, müssen Dateien zu `C:\Program Files\ClaudeCode\managed-settings.json` migrieren.
    </Warning>

  Siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings) und [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration) für Details.

  <Note>
    Verwaltete Bereitstellungen können auch **Plugin-Marketplace-Ergänzungen** mit `strictKnownMarketplaces` einschränken. Weitere Informationen finden Sie unter [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Andere Konfiguration** wird in `~/.claude.json` gespeichert. Diese Datei enthält Ihre Voreinstellungen (Design, Benachrichtigungseinstellungen, Editor-Modus), OAuth-Sitzung, [MCP-Server](/de/mcp)-Konfigurationen für Benutzer- und lokale Bereiche, projektbezogenen Status (zulässige Tools, Vertrauenseinstellungen) und verschiedene Caches. Projektbezogene MCP-Server werden separat in `.mcp.json` gespeichert.

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

Die Zeile `$schema` im obigen Beispiel verweist auf das [offizielle JSON-Schema](https://json.schemastore.org/claude-code-settings.json) für Claude Code-Einstellungen. Das Hinzufügen zu Ihrer `settings.json` ermöglicht Autovervollständigung und Inline-Validierung in VS Code, Cursor und jedem anderen Editor, der JSON-Schema-Validierung unterstützt.

### Verfügbare Einstellungen

`settings.json` unterstützt eine Reihe von Optionen:

| Schlüssel                         | Beschreibung                                                                                                                                                                                                                                                                                                                                                                        | Beispiel                                                                |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Benutzerdefiniertes Skript, das in `/bin/sh` ausgeführt werden soll, um einen Auth-Wert zu generieren. Dieser Wert wird als `X-Api-Key` und `Authorization: Bearer` Header für Modellanfragen gesendet                                                                                                                                                                              | `/bin/generate_temp_api_key.sh`                                         |
| `autoMemoryDirectory`             | Benutzerdefiniertes Verzeichnis für [automatisches Speichern](/de/memory#storage-location). Akzeptiert `~/`-erweiterte Pfade. Nicht in Projekteinstellungen (`.claude/settings.json`) akzeptiert, um zu verhindern, dass gemeinsame Repos Speicherschreibvorgänge an sensible Orte umleiten. Akzeptiert von Richtlinien-, lokalen und Benutzereinstellungen                         | `"~/my-memory-dir"`                                                     |
| `cleanupPeriodDays`               | Sitzungen, die länger als dieser Zeitraum inaktiv sind, werden beim Start gelöscht (Standard: 30 Tage).<br /><br />Das Setzen auf `0` löscht alle vorhandenen Transkripte beim Start und deaktiviert die Sitzungspersistenz vollständig. Es werden keine neuen `.jsonl`-Dateien geschrieben, `/resume` zeigt keine Gespräche an, und Hooks erhalten einen leeren `transcript_path`. | `20`                                                                    |
| `companyAnnouncements`            | Ankündigung, die Benutzern beim Start angezeigt werden soll. Wenn mehrere Ankündigungen bereitgestellt werden, werden sie zufällig durchlaufen.                                                                                                                                                                                                                                     | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Umgebungsvariablen, die auf jede Sitzung angewendet werden                                                                                                                                                                                                                                                                                                                          | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Passen Sie die Zuschreibung für Git-Commits und Pull Requests an. Siehe [Zuschreibungseinstellungen](#attribution-settings)                                                                                                                                                                                                                                                         | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Veraltet**: Verwenden Sie stattdessen `attribution`. Ob die `co-authored-by Claude` Byline in Git-Commits und Pull Requests einbezogen werden soll (Standard: `true`)                                                                                                                                                                                                             | `false`                                                                 |
| `includeGitInstructions`          | Integrierte Commit- und PR-Workflow-Anweisungen in Claudes Systemaufforderung einbeziehen (Standard: `true`). Setzen Sie auf `false`, um diese Anweisungen zu entfernen, z. B. wenn Sie Ihre eigenen Git-Workflow-Skills verwenden. Die Umgebungsvariable `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` hat Vorrang vor dieser Einstellung, wenn sie gesetzt ist                           | `false`                                                                 |
| `permissions`                     | Siehe Tabelle unten für die Struktur der Berechtigungen.                                                                                                                                                                                                                                                                                                                            |                                                                         |
| `hooks`                           | Konfigurieren Sie benutzerdefinierte Befehle, die bei Lebenszyklusereignissen ausgeführt werden. Siehe [Hooks-Dokumentation](/de/hooks) für das Format                                                                                                                                                                                                                              | Siehe [Hooks](/de/hooks)                                                |
| `disableAllHooks`                 | Deaktivieren Sie alle [Hooks](/de/hooks) und alle benutzerdefinierten [Statuszeilen](/de/statusline)                                                                                                                                                                                                                                                                                | `true`                                                                  |
| `allowManagedHooksOnly`           | (Nur verwaltete Einstellungen) Verhindern Sie das Laden von Benutzer-, Projekt- und Plugin-Hooks. Erlaubt nur verwaltete Hooks und SDK-Hooks. Siehe [Hook-Konfiguration](#hook-configuration)                                                                                                                                                                                       | `true`                                                                  |
| `allowedHttpHookUrls`             | Allowlist von URL-Mustern, auf die HTTP-Hooks abzielen können. Unterstützt `*` als Platzhalter. Wenn gesetzt, werden Hooks mit nicht übereinstimmenden URLs blockiert. Undefined = keine Einschränkung, leeres Array = alle HTTP-Hooks blockieren. Arrays werden über Einstellungsquellen zusammengeführt. Siehe [Hook-Konfiguration](#hook-configuration)                          | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Allowlist von Umgebungsvariablennamen, die HTTP-Hooks in Header interpolieren können. Wenn gesetzt, ist die effektive `allowedEnvVars` jedes Hooks der Schnittpunkt mit dieser Liste. Undefined = keine Einschränkung. Arrays werden über Einstellungsquellen zusammengeführt. Siehe [Hook-Konfiguration](#hook-configuration)                                                      | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Nur verwaltete Einstellungen) Verhindern Sie, dass Benutzer- und Projekteinstellungen `allow`, `ask` oder `deny` Berechtigungsregeln definieren. Nur Regeln in verwalteten Einstellungen gelten. Siehe [Nur verwaltete Einstellungen](/de/permissions#managed-only-settings)                                                                                                       | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Nur verwaltete Einstellungen) Nur `allowedMcpServers` aus verwalteten Einstellungen werden berücksichtigt. `deniedMcpServers` wird weiterhin aus allen Quellen zusammengeführt. Benutzer können weiterhin MCP-Server hinzufügen, aber nur die von Admin definierte Allowlist gilt. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                         | `true`                                                                  |
| `model`                           | Überschreiben Sie das Standardmodell für Claude Code                                                                                                                                                                                                                                                                                                                                | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Beschränken Sie, welche Modelle Benutzer über `/model`, `--model`, Config-Tool oder `ANTHROPIC_MODEL` auswählen können. Beeinflusst nicht die Standardoption. Siehe [Modellauswahl einschränken](/de/model-config#restrict-model-selection)                                                                                                                                         | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Ordnen Sie Anthropic-Modell-IDs Anbieter-spezifischen Modell-IDs wie Bedrock-Inferenzprofil-ARNs zu. Jeder Modellwähler-Eintrag verwendet seinen zugeordneten Wert beim Aufrufen der Anbieter-API. Siehe [Modell-IDs pro Version überschreiben](/de/model-config#override-model-ids-per-version)                                                                                    | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `effortLevel`                     | Persistieren Sie die [Anstrengungsstufe](/de/model-config#adjust-effort-level) über Sitzungen hinweg. Akzeptiert `"low"`, `"medium"` oder `"high"`. Wird automatisch geschrieben, wenn Sie `/effort low`, `/effort medium` oder `/effort high` ausführen. Unterstützt auf Opus 4.6 und Sonnet 4.6                                                                                   | `"medium"`                                                              |
| `otelHeadersHelper`               | Skript zum Generieren dynamischer OpenTelemetry-Header. Wird beim Start und regelmäßig ausgeführt (siehe [Dynamische Header](/de/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                 | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Konfigurieren Sie eine benutzerdefinierte Statuszeile zur Anzeige von Kontext. Siehe [`statusLine`-Dokumentation](/de/statusline)                                                                                                                                                                                                                                                   | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Konfigurieren Sie ein benutzerdefiniertes Skript für `@` Datei-Autovervollständigung. Siehe [Dateivorschlag-Einstellungen](#file-suggestion-settings)                                                                                                                                                                                                                               | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Steuern Sie, ob der `@` Datei-Picker `.gitignore`-Muster respektiert. Wenn `true` (Standard), werden Dateien, die `.gitignore`-Mustern entsprechen, aus Vorschlägen ausgeschlossen                                                                                                                                                                                                  | `false`                                                                 |
| `outputStyle`                     | Konfigurieren Sie einen Ausgabestil, um die Systemaufforderung anzupassen. Siehe [Ausgabestil-Dokumentation](/de/output-styles)                                                                                                                                                                                                                                                     | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Verwenden Sie `claudeai`, um die Anmeldung auf Claude.ai-Konten zu beschränken, `console`, um die Anmeldung auf Claude Console (API-Nutzungsabrechnung) Konten zu beschränken                                                                                                                                                                                                       | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Geben Sie die UUID einer Organisation an, um sie während der Anmeldung automatisch auszuwählen und den Organisationsauswahlschritt zu umgehen. Erfordert, dass `forceLoginMethod` gesetzt ist                                                                                                                                                                                       | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Genehmigen Sie automatisch alle MCP-Server, die in Projekt-`.mcp.json`-Dateien definiert sind                                                                                                                                                                                                                                                                                       | `true`                                                                  |
| `enabledMcpjsonServers`           | Liste spezifischer MCP-Server aus `.mcp.json`-Dateien zum Genehmigen                                                                                                                                                                                                                                                                                                                | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Liste spezifischer MCP-Server aus `.mcp.json`-Dateien zum Ablehnen                                                                                                                                                                                                                                                                                                                  | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Wenn in managed-settings.json gesetzt, Allowlist von MCP-Servern, die Benutzer konfigurieren können. Undefined = keine Einschränkungen, leeres Array = Lockdown. Gilt für alle Bereiche. Denylist hat Vorrang. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                              | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Wenn in managed-settings.json gesetzt, Denylist von MCP-Servern, die explizit blockiert sind. Gilt für alle Bereiche einschließlich verwalteter Server. Denylist hat Vorrang vor Allowlist. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                                                 | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Wenn in managed-settings.json gesetzt, Allowlist von Plugin-Marketplaces, die Benutzer hinzufügen können. Undefined = keine Einschränkungen, leeres Array = Lockdown. Gilt nur für Marketplace-Ergänzungen. Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Nur verwaltete Einstellungen) Blocklist von Marketplace-Quellen. Blockierte Quellen werden vor dem Download überprüft, sodass sie das Dateisystem nie berühren. Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                           | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Nur verwaltete Einstellungen) Benutzerdefinierte Nachricht, die der vor der Installation angezeigten Plugin-Vertrauenswarnung angehängt wird. Verwenden Sie dies, um organisationsspezifischen Kontext hinzuzufügen, z. B. um zu bestätigen, dass Plugins aus Ihrem internen Marketplace überprüft sind.                                                                           | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Benutzerdefiniertes Skript, das das `.aws`-Verzeichnis ändert (siehe [erweiterte Anmeldedatenkonfiguration](/de/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                  | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Benutzerdefiniertes Skript, das JSON mit AWS-Anmeldedaten ausgibt (siehe [erweiterte Anmeldedatenkonfiguration](/de/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                              | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Aktivieren Sie [erweitertes Denken](/de/common-workflows#use-extended-thinking-thinking-mode) standardmäßig für alle Sitzungen. Normalerweise über den Befehl `/config` konfiguriert, anstatt direkt zu bearbeiten                                                                                                                                                                  | `true`                                                                  |
| `plansDirectory`                  | Passen Sie an, wo Plandateien gespeichert werden. Der Pfad ist relativ zum Projektstamm. Standard: `~/.claude/plans`                                                                                                                                                                                                                                                                | `"./plans"`                                                             |
| `showTurnDuration`                | Zeigen Sie Nachrichten zur Dauer der Runde nach Antworten an (z. B. "Cooked for 1m 6s"). Setzen Sie auf `false`, um diese Nachrichten auszublenden                                                                                                                                                                                                                                  | `true`                                                                  |
| `spinnerVerbs`                    | Passen Sie die Aktionsverben an, die im Spinner und in Nachrichten zur Dauer der Runde angezeigt werden. Setzen Sie `mode` auf `"replace"`, um nur Ihre Verben zu verwenden, oder `"append"`, um sie zu den Standardwerten hinzuzufügen                                                                                                                                             | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Konfigurieren Sie Claudes bevorzugte Antwortsprache (z. B. `"japanese"`, `"spanish"`, `"french"`). Claude wird standardmäßig in dieser Sprache antworten                                                                                                                                                                                                                            | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Release-Kanal zum Folgen von Updates. Verwenden Sie `"stable"` für eine Version, die normalerweise etwa eine Woche alt ist und Versionen mit großen Regressionen überspringt, oder `"latest"` (Standard) für die neueste Version                                                                                                                                                    | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Zeigen Sie Tipps im Spinner an, während Claude arbeitet. Setzen Sie auf `false`, um Tipps zu deaktivieren (Standard: `true`)                                                                                                                                                                                                                                                        | `false`                                                                 |
| `spinnerTipsOverride`             | Überschreiben Sie Spinner-Tipps mit benutzerdefinierten Zeichenketten. `tips`: Array von Tipp-Zeichenketten. `excludeDefault`: wenn `true`, nur benutzerdefinierte Tipps anzeigen; wenn `false` oder nicht vorhanden, werden benutzerdefinierte Tipps mit integrierten Tipps zusammengeführt                                                                                        | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Aktivieren Sie die Terminal-Fortschrittsleiste, die den Fortschritt in unterstützten Terminals wie Windows Terminal und iTerm2 anzeigt (Standard: `true`)                                                                                                                                                                                                                           | `false`                                                                 |
| `prefersReducedMotion`            | Reduzieren oder deaktivieren Sie UI-Animationen (Spinner, Shimmer, Flash-Effekte) für Barrierefreiheit                                                                                                                                                                                                                                                                              | `true`                                                                  |
| `fastModePerSessionOptIn`         | Wenn `true`, bleibt der schnelle Modus nicht über Sitzungen hinweg bestehen. Jede Sitzung startet mit ausgeschaltetem schnellen Modus und erfordert, dass Benutzer ihn mit `/fast` aktivieren. Die Voreinstellung des Benutzers für den schnellen Modus wird weiterhin gespeichert. Siehe [Opt-in pro Sitzung erforderlich](/de/fast-mode#require-per-session-opt-in)               | `true`                                                                  |
| `teammateMode`                    | Wie [Agent-Team](/de/agent-teams) Teamkollegen angezeigt werden: `auto` (wählt geteilte Bereiche in tmux oder iTerm2, ansonsten In-Process), `in-process` oder `tmux`. Siehe [Agent-Teams einrichten](/de/agent-teams#set-up-agent-teams)                                                                                                                                           | `"in-process"`                                                          |
| `feedbackSurveyRate`              | Wahrscheinlichkeit (0–1), dass die [Sitzungsqualitätsumfrage](/de/data-usage#session-quality-surveys) angezeigt wird, wenn berechtigt. Setzen Sie auf `0`, um vollständig zu unterdrücken. Nützlich bei Verwendung von Bedrock, Vertex oder Foundry, wo die Standard-Stichprobenquote nicht gilt                                                                                    | `0.05`                                                                  |

### Worktree-Einstellungen

Konfigurieren Sie, wie `--worktree` Git-Worktrees erstellt und verwaltet. Verwenden Sie diese Einstellungen, um Speicherplatz und Startzeit in großen Monorepos zu reduzieren.

| Schlüssel                     | Beschreibung                                                                                                                                                                                            | Beispiel                              |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------ |
| `worktree.symlinkDirectories` | Verzeichnisse, die vom Haupt-Repository in jeden Worktree symlinkt werden, um große Verzeichnisse auf der Festplatte zu duplizieren. Standardmäßig werden keine Verzeichnisse symlinkt                  | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Verzeichnisse, die in jedem Worktree über Git Sparse-Checkout (Cone-Modus) ausgecheckt werden. Nur die aufgelisteten Pfade werden auf die Festplatte geschrieben, was in großen Monorepos schneller ist | `["packages/my-app", "shared/utils"]` |

### Berechtigungseinstellungen

| Schlüssel                      | Beschreibung                                                                                                                                                                                                                                                                                          | Beispiel                                                               |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Array von Berechtigungsregeln, um die Werkzeugnutzung zu erlauben. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) unten für Details zur Mustererkennung                                                                                                                                    | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Array von Berechtigungsregeln, um bei der Werkzeugnutzung um Bestätigung zu bitten. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) unten                                                                                                                                                   | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Array von Berechtigungsregeln, um die Werkzeugnutzung zu verweigern. Verwenden Sie dies, um sensible Dateien vom Claude Code-Zugriff auszuschließen. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) und [Bash-Berechtigungsbeschränkungen](/de/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | Zusätzliche [Arbeitsverzeichnisse](/de/permissions#working-directories), auf die Claude Zugriff hat                                                                                                                                                                                                   | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | Standard-[Berechtigungsmodus](/de/permissions#permission-modes) beim Öffnen von Claude Code                                                                                                                                                                                                           | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Setzen Sie auf `"disable"`, um zu verhindern, dass der `bypassPermissions`-Modus aktiviert wird. Dies deaktiviert das Befehlszeilenflag `--dangerously-skip-permissions`. Siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings)                                                     | `"disable"`                                                            |

### Berechtigungsregelsyntax

Berechtigungsregeln folgen dem Format `Tool` oder `Tool(specifier)`. Regeln werden in der Reihenfolge ausgewertet: zuerst Deny-Regeln, dann Ask, dann Allow. Die erste übereinstimmende Regel gewinnt.

Schnelle Beispiele:

| Regel                          | Effekt                                        |
| :----------------------------- | :-------------------------------------------- |
| `Bash`                         | Passt auf alle Bash-Befehle                   |
| `Bash(npm run *)`              | Passt auf Befehle, die mit `npm run` beginnen |
| `Read(./.env)`                 | Passt auf das Lesen der `.env`-Datei          |
| `WebFetch(domain:example.com)` | Passt auf Abrufanfragen an example.com        |

Für die vollständige Referenz der Regelsyntax, einschließlich Platzhalterverhalten, werkzeugspezifischer Muster für Read, Edit, WebFetch, MCP und Agent-Regeln sowie Sicherheitsbeschränkungen von Bash-Mustern, siehe [Berechtigungsregelsyntax](/de/permissions#permission-rule-syntax).

### Sandbox-Einstellungen

Konfigurieren Sie erweitertes Sandbox-Verhalten. Sandboxing isoliert Bash-Befehle von Ihrem Dateisystem und Netzwerk. Siehe [Sandboxing](/de/sandboxing) für Details.

| Schlüssel                         | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                         | Beispiel                        |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | Aktivieren Sie Bash-Sandboxing (macOS, Linux und WSL2). Standard: false                                                                                                                                                                                                                                                                                                                                              | `true`                          |
| `autoAllowBashIfSandboxed`        | Genehmigen Sie Bash-Befehle automatisch, wenn sie in einer Sandbox ausgeführt werden. Standard: true                                                                                                                                                                                                                                                                                                                 | `true`                          |
| `excludedCommands`                | Befehle, die außerhalb der Sandbox ausgeführt werden sollten                                                                                                                                                                                                                                                                                                                                                         | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Erlauben Sie Befehlen, außerhalb der Sandbox über den Parameter `dangerouslyDisableSandbox` ausgeführt zu werden. Wenn auf `false` gesetzt, ist die Fluchtluke `dangerouslyDisableSandbox` vollständig deaktiviert und alle Befehle müssen in einer Sandbox ausgeführt werden (oder in `excludedCommands` sein). Nützlich für Unternehmensrichtlinien, die striktes Sandboxing erfordern. Standard: true             | `false`                         |
| `filesystem.allowWrite`           | Zusätzliche Pfade, in die Sandbox-Befehle schreiben können. Arrays werden über alle Einstellungsbereiche zusammengeführt: Benutzer-, Projekt- und verwaltete Pfade werden kombiniert, nicht ersetzt. Auch zusammengeführt mit Pfaden aus `Edit(...)` Allow-Berechtigungsregeln. Siehe [Pfadpräfixe](#sandbox-path-prefixes) unten.                                                                                   | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Pfade, in die Sandbox-Befehle nicht schreiben können. Arrays werden über alle Einstellungsbereiche zusammengeführt. Auch zusammengeführt mit Pfaden aus `Edit(...)` Deny-Berechtigungsregeln.                                                                                                                                                                                                                        | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Pfade, aus denen Sandbox-Befehle nicht lesen können. Arrays werden über alle Einstellungsbereiche zusammengeführt. Auch zusammengeführt mit Pfaden aus `Read(...)` Deny-Berechtigungsregeln.                                                                                                                                                                                                                         | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Unix-Socket-Pfade, auf die in der Sandbox zugegriffen werden kann (für SSH-Agenten usw.)                                                                                                                                                                                                                                                                                                                             | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Erlauben Sie alle Unix-Socket-Verbindungen in der Sandbox. Standard: false                                                                                                                                                                                                                                                                                                                                           | `true`                          |
| `network.allowLocalBinding`       | Erlauben Sie das Binden an Localhost-Ports (nur macOS). Standard: false                                                                                                                                                                                                                                                                                                                                              | `true`                          |
| `network.allowedDomains`          | Array von Domänen, um ausgehenden Netzwerkverkehr zu erlauben. Unterstützt Platzhalter (z. B. `*.example.com`).                                                                                                                                                                                                                                                                                                      | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Nur verwaltete Einstellungen) Nur `allowedDomains` und `WebFetch(domain:...)` Allow-Regeln aus verwalteten Einstellungen werden berücksichtigt. Domänen aus Benutzer-, Projekt- und lokalen Einstellungen werden ignoriert. Nicht zulässige Domänen werden automatisch blockiert, ohne den Benutzer zu fragen. Verweigerte Domänen werden weiterhin aus allen Quellen berücksichtigt. Standard: false               | `true`                          |
| `network.httpProxyPort`           | HTTP-Proxy-Port, der verwendet wird, wenn Sie Ihren eigenen Proxy verwenden möchten. Wenn nicht angegeben, führt Claude seinen eigenen Proxy aus.                                                                                                                                                                                                                                                                    | `8080`                          |
| `network.socksProxyPort`          | SOCKS5-Proxy-Port, der verwendet wird, wenn Sie Ihren eigenen Proxy verwenden möchten. Wenn nicht angegeben, führt Claude seinen eigenen Proxy aus.                                                                                                                                                                                                                                                                  | `8081`                          |
| `enableWeakerNestedSandbox`       | Aktivieren Sie schwächere Sandbox für unprivilegierte Docker-Umgebungen (nur Linux und WSL2). **Reduziert die Sicherheit.** Standard: false                                                                                                                                                                                                                                                                          | `true`                          |
| `enableWeakerNetworkIsolation`    | (Nur macOS) Erlauben Sie den Zugriff auf den System-TLS-Vertrauensdienst (`com.apple.trustd.agent`) in der Sandbox. Erforderlich für Go-basierte Tools wie `gh`, `gcloud` und `terraform`, um TLS-Zertifikate zu überprüfen, wenn `httpProxyPort` mit einem MITM-Proxy und benutzerdefinierter CA verwendet wird. **Reduziert die Sicherheit** durch Öffnen eines möglichen Datenexfiltrationspfads. Standard: false | `true`                          |

#### Sandbox-Pfadpräfixe

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

* **`sandbox.filesystem`-Einstellungen** (oben gezeigt): Steuern Sie Pfade an der OS-Level-Sandbox-Grenze. Diese Einschränkungen gelten für alle Subprozess-Befehle (z. B. `kubectl`, `terraform`, `npm`), nicht nur für Claudes Datei-Tools.
* **Berechtigungsregeln**: Verwenden Sie `Edit` Allow/Deny-Regeln, um den Zugriff auf Claudes Datei-Tool zu steuern, `Read` Deny-Regeln, um Lesevorgänge zu blockieren, und `WebFetch` Allow/Deny-Regeln, um Netzwerk-Domänen zu steuern. Pfade aus diesen Regeln werden auch in die Sandbox-Konfiguration zusammengeführt.

### Zuschreibungseinstellungen

Claude Code fügt Git-Commits und Pull Requests Zuschreibungen hinzu. Diese werden separat konfiguriert:

* Commits verwenden [Git-Trailer](https://git-scm.com/docs/git-interpret-trailers) (wie `Co-Authored-By`) standardmäßig, die angepasst oder deaktiviert werden können
* Pull-Request-Beschreibungen sind Klartext

| Schlüssel | Beschreibung                                                                                                   |
| :-------- | :------------------------------------------------------------------------------------------------------------- |
| `commit`  | Zuschreibung für Git-Commits, einschließlich aller Trailer. Leere Zeichenkette blendet Commit-Zuschreibung aus |
| `pr`      | Zuschreibung für Pull-Request-Beschreibungen. Leere Zeichenkette blendet Pull-Request-Zuschreibung aus         |

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
  Die Einstellung `attribution` hat Vorrang vor der veralteten Einstellung `includeCoAuthoredBy`. Um alle Zuschreibungen auszublenden, setzen Sie `commit` und `pr` auf leere Zeichenketten.
</Note>

### Dateivorschlag-Einstellungen

Konfigurieren Sie einen benutzerdefinierten Befehl für `@` Dateipath-Autovervollständigung. Der integrierte Dateivorschlag verwendet schnelle Dateisystem-Durchquerung, aber große Monorepos können von projektspezifischer Indizierung wie einem vorgefertigten Dateiindex oder benutzerdefinierten Tools profitieren.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Der Befehl wird mit den gleichen Umgebungsvariablen wie [Hooks](/de/hooks) ausgeführt, einschließlich `CLAUDE_PROJECT_DIR`. Er empfängt JSON über stdin mit einem `query`-Feld:

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

Diese Einstellungen steuern, welche Hooks ausgeführt werden dürfen und worauf HTTP-Hooks zugreifen können. Die Einstellung `allowManagedHooksOnly` kann nur in [verwalteten Einstellungen](#settings-files) konfiguriert werden. Die URL- und Umgebungsvariablen-Allowlists können auf jeder Einstellungsebene gesetzt werden und werden über Quellen zusammengeführt.

**Verhalten, wenn `allowManagedHooksOnly` `true` ist:**

* Verwaltete Hooks und SDK-Hooks werden geladen
* Benutzer-Hooks, Projekt-Hooks und Plugin-Hooks werden blockiert

**HTTP-Hook-URLs einschränken:**

Begrenzen Sie, auf welche URLs HTTP-Hooks abzielen können. Unterstützt `*` als Platzhalter zum Abgleichen. Wenn das Array definiert ist, werden HTTP-Hooks, die auf nicht übereinstimmende URLs abzielen, stillschweigend blockiert.

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
   * Innerhalb der verwalteten Ebene ist die Priorität: serververwaltete > MDM/OS-Richtlinien > `managed-settings.json` > HKCU-Registry (nur Windows). Nur eine verwaltete Quelle wird verwendet; Quellen werden nicht zusammengeführt.

2. **Befehlszeilenargumente**
   * Temporäre Überschreibungen für eine bestimmte Sitzung

3. **Lokale Projekteinstellungen** (`.claude/settings.local.json`)
   * Persönliche projektspezifische Einstellungen

4. **Gemeinsame Projekteinstellungen** (`.claude/settings.json`)
   * Teamübergreifend gemeinsame Projekteinstellungen in der Versionskontrolle

5. **Benutzereinstellungen** (`~/.claude/settings.json`)
   * Persönliche globale Einstellungen

Diese Hierarchie stellt sicher, dass Organisationsrichtlinien immer durchgesetzt werden, während Teams und Einzelpersonen ihre Erfahrung weiterhin anpassen können.

Wenn beispielsweise Ihre Benutzereinstellungen `Bash(npm run *)` erlauben, aber die gemeinsamen Einstellungen eines Projekts dies verweigern, hat die Projekteinstellung Vorrang und der Befehl wird blockiert.

<Note>
  **Array-Einstellungen werden über Bereiche zusammengeführt.** Wenn die gleiche Array-wertige Einstellung (wie `sandbox.filesystem.allowWrite` oder `permissions.allow`) in mehreren Bereichen erscheint, werden die Arrays **verkettet und dedupliziert**, nicht ersetzt. Dies bedeutet, dass Bereiche mit niedrigerer Priorität Einträge hinzufügen können, ohne diejenigen mit höherer Priorität zu überschreiben, und umgekehrt. Wenn beispielsweise verwaltete Einstellungen `allowWrite` auf `["//opt/company-tools"]` setzen und ein Benutzer `["~/.kube"]` hinzufügt, sind beide Pfade in der endgültigen Konfiguration enthalten.
</Note>

### Aktive Einstellungen überprüfen

Führen Sie `/status` in Claude Code aus, um zu sehen, welche Einstellungsquellen aktiv sind und woher sie stammen. Die Ausgabe zeigt jede Konfigurationsebene (verwaltet, Benutzer, Projekt) zusammen mit ihrem Ursprung, wie `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)` oder `Enterprise managed settings (file)`. Wenn eine Einstellungsdatei Fehler enthält, meldet `/status` das Problem, damit Sie es beheben können.

### Wichtige Punkte zum Konfigurationssystem

* **Speicherdateien (`CLAUDE.md`)**: Enthalten Anweisungen und Kontext, die Claude beim Start lädt
* **Einstellungsdateien (JSON)**: Konfigurieren Sie Berechtigungen, Umgebungsvariablen und Werkzeugverhalten
* **Skills**: Benutzerdefinierte Aufforderungen, die mit `/skill-name` aufgerufen oder von Claude automatisch geladen werden können
* **MCP-Server**: Erweitern Sie Claude Code mit zusätzlichen Tools und Integrationen
* **Priorität**: Höherrangige Konfigurationen (Verwaltet) überschreiben niedrigere (Benutzer/Projekt)
* **Vererbung**: Einstellungen werden zusammengeführt, wobei spezifischere Einstellungen breitere ergänzen oder überschreiben

### Systemaufforderung

Claudes interne Systemaufforderung wird nicht veröffentlicht. Um benutzerdefinierte Anweisungen hinzuzufügen, verwenden Sie `CLAUDE.md`-Dateien oder das Flag `--append-system-prompt`.

### Ausschließen sensibler Dateien

Um zu verhindern, dass Claude Code auf Dateien mit sensiblen Informationen wie API-Schlüsseln, Geheimnissen und Umgebungsdateien zugreift, verwenden Sie die Einstellung `permissions.deny` in Ihrer `.claude/settings.json`-Datei:

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

Dies ersetzt die veraltete Konfiguration `ignorePatterns`. Dateien, die diesen Mustern entsprechen, werden von der Dateiermittlung und Suchergebnissen ausgeschlossen, und Lesevorgänge auf diesen Dateien werden verweigert.

## Subagent-Konfiguration

Claude Code unterstützt benutzerdefinierte KI-Subagents, die auf Benutzer- und Projektebene konfiguriert werden können. Diese Subagents werden als Markdown-Dateien mit YAML-Frontmatter gespeichert:

* **Benutzer-Subagents**: `~/.claude/agents/` - Verfügbar über alle Ihre Projekte
* **Projekt-Subagents**: `.claude/agents/` - Spezifisch für Ihr Projekt und können mit Ihrem Team geteilt werden

Subagent-Dateien definieren spezialisierte KI-Assistenten mit benutzerdefinierten Aufforderungen und Werkzeugberechtigungen. Erfahren Sie mehr über das Erstellen und Verwenden von Subagents in der [Subagents-Dokumentation](/de/sub-agents).

## Plugin-Konfiguration

Claude Code unterstützt ein Plugin-System, mit dem Sie die Funktionalität mit Skills, Agents, Hooks und MCP-Servern erweitern können. Plugins werden über Marketplaces verteilt und können auf Benutzer- und Repository-Ebene konfiguriert werden.

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
* Verwendet exakte Übereinstimmung für Quellspezifikationen (einschließlich `ref`, `path` für Git-Quellen), außer `hostPattern`, das Regex-Abgleich verwendet

**Allowlist-Verhalten**:

* `undefined` (Standard): Keine Einschränkungen - Benutzer können jeden Marketplace hinzufügen
* Leeres Array `[]`: Vollständiger Lockdown - Benutzer können keine neuen Marketplaces hinzufügen
* Liste von Quellen: Benutzer können nur Marketplaces hinzufügen, die genau übereinstimmen

**Alle unterstützten Quellentypen**:

Die Allowlist unterstützt sieben Marketplace-Quellentypen. Die meisten Quellen verwenden exakte Übereinstimmung, während `hostPattern` Regex-Abgleich gegen den Marketplace-Host verwendet.

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
  URL-basierte Marketplaces laden nur die `marketplace.json`-Datei herunter. Sie laden keine Plugin-Dateien vom Server herunter. Plugins in URL-basierten Marketplaces müssen externe Quellen (GitHub, npm oder Git-URLs) verwenden, anstatt relative Pfade. Für Plugins mit relativen Pfaden verwenden Sie stattdessen einen Git-basierten Marketplace. Siehe [Troubleshooting](/de/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) für Details.
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

Felder: `path` (erforderlich: absoluter Pfad zur marketplace.json-Datei)

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

**Anforderungen für exakte Übereinstimmung**:

Marketplace-Quellen müssen **genau** übereinstimmen, damit eine Benutzer-Ergänzung erlaubt wird. Für Git-basierte Quellen (`github` und `git`) umfasst dies alle optionalen Felder:

* Das `repo` oder `url` muss genau übereinstimmen
* Das `ref`-Feld muss genau übereinstimmen (oder beide sind undefined)
* Das `path`-Feld muss genau übereinstimmen (oder beide sind undefined)

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
| **Verhalten**                 | Blockiert nicht-allowlisted Ergänzungen   | Auto-installiert fehlende Marketplaces           |
| **Wann durchgesetzt**         | Vor Netzwerk-/Dateisystem-Operationen     | Nach Benutzer-Vertrauensaufforderung             |
| **Kann überschrieben werden** | Nein (höchste Priorität)                  | Ja (durch höherrangige Einstellungen)            |
| **Quellenformat**             | Direktes Quellobjekt                      | Benannter Marketplace mit verschachtelter Quelle |
| **Anwendungsfall**            | Compliance, Sicherheitsbeschränkungen     | Onboarding, Standardisierung                     |

**Formatunterschied**:

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

**Beide zusammen verwenden**:

`strictKnownMarketplaces` ist ein Richtlinien-Gate: Es steuert, was Benutzer hinzufügen dürfen, registriert aber keine Marketplaces. Um einen Marketplace sowohl einzuschränken als auch für alle Benutzer vorzuregistrieren, setzen Sie beide in `managed-settings.json`:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Mit nur `strictKnownMarketplaces` gesetzt, können Benutzer den erlaubten Marketplace weiterhin manuell über `/plugin marketplace add` hinzufügen, aber er ist nicht automatisch verfügbar.

**Wichtige Hinweise**:

* Einschränkungen werden VOR Netzwerkanfragen oder Dateisystem-Operationen überprüft
* Wenn blockiert, sehen Benutzer klare Fehlermeldungen, die angeben, dass die Quelle durch verwaltete Richtlinie blockiert ist
* Die Einschränkung gilt nur für das Hinzufügen NEUER Marketplaces; zuvor installierte Marketplaces bleiben zugänglich
* Verwaltete Einstellungen haben die höchste Priorität und können nicht überschrieben werden

Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions) für Dokumentation für Benutzer.

### Verwalten von Plugins

Verwenden Sie den Befehl `/plugin`, um Plugins interaktiv zu verwalten:

* Durchsuchen Sie verfügbare Plugins aus Marketplaces
* Installieren/Deinstallieren Sie Plugins
* Aktivieren/Deaktivieren Sie Plugins
* Zeigen Sie Plugin-Details an (bereitgestellte Befehle, Agents, Hooks)
* Fügen Sie Marketplaces hinzu/entfernen Sie sie

Erfahren Sie mehr über das Plugin-System in der [Plugins-Dokumentation](/de/plugins).

## Umgebungsvariablen

Umgebungsvariablen ermöglichen es Ihnen, das Verhalten von Claude Code zu steuern, ohne Einstellungsdateien zu bearbeiten. Jede Variable kann auch in [`settings.json`](#available-settings) unter dem Schlüssel `env` konfiguriert werden, um sie auf jede Sitzung anzuwenden oder für Ihr Team bereitzustellen.

Siehe die [Umgebungsvariablen-Referenz](/de/env-vars) für die vollständige Liste.

## Tools, die Claude zur Verfügung stehen

Claude Code hat Zugriff auf eine Reihe von Tools zum Lesen, Bearbeiten, Suchen, Ausführen von Befehlen und Orchestrieren von Subagents. Tool-Namen sind die genauen Zeichenketten, die Sie in Berechtigungsregeln und Hook-Matchern verwenden.

Siehe die [Tools-Referenz](/de/tools-reference) für die vollständige Liste und Details zum Bash-Tool-Verhalten.

## Siehe auch

* [Berechtigungen](/de/permissions): Berechtigungssystem, Regelsyntax, werkzeugspezifische Muster und verwaltete Richtlinien
* [Authentifizierung](/de/authentication): Richten Sie Benutzerzugriff auf Claude Code ein
* [Troubleshooting](/de/troubleshooting): Lösungen für häufige Konfigurationsprobleme
