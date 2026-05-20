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

Wenn die gleiche Einstellung in mehreren Bereichen konfiguriert ist, wendet Claude Code sie in Prioritätsreihenfolge an:

1. **Verwaltet** (höchste) - kann von nichts überschrieben werden
2. **Befehlszeilenargumente** - temporäre Sitzungsüberschreibungen
3. **Lokal** - überschreibt Projekt- und Benutzereinstellungen
4. **Projekt** - überschreibt Benutzereinstellungen
5. **Benutzer** (niedrigste) - gilt, wenn nichts anderes die Einstellung angibt

Wenn beispielsweise Ihre Benutzereinstellungen `spinnerTipsEnabled` auf `true` setzen und Projekteinstellungen es auf `false` setzen, gilt der Projektwert. Berechtigungsregeln verhalten sich anders, da sie über Bereiche hinweg zusammengeführt werden, anstatt sich zu überschreiben. Siehe [Einstellungspriorität](#settings-precedence).

### Was verwendet Bereiche

Bereiche gelten für viele Claude Code-Funktionen:

| Funktion          | Benutzerort               | Projektort                           | Lokaler Ort                    |
| :---------------- | :------------------------ | :----------------------------------- | :----------------------------- |
| **Einstellungen** | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json`  |
| **Subagents**     | `~/.claude/agents/`       | `.claude/agents/`                    | Keine                          |
| **MCP-Server**    | `~/.claude.json`          | `.mcp.json`                          | `~/.claude.json` (pro Projekt) |
| **Plugins**       | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json`  |
| **CLAUDE.md**     | `~/.claude/CLAUDE.md`     | `CLAUDE.md` oder `.claude/CLAUDE.md` | `CLAUDE.local.md`              |

Unter Windows werden Pfade, die als `~/.claude` angezeigt werden, zu `%USERPROFILE%\.claude` aufgelöst.

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
    * macOS: `com.anthropic.claudecode` verwaltete Präferenzdomäne. Die Schlüssel der obersten Ebene der plist spiegeln `managed-settings.json` wider, mit verschachtelten Einstellungen als Wörterbücher und Arrays als plist-Arrays. Bereitstellung über Konfigurationsprofile in Jamf, Iru (Kandji) oder ähnlichen MDM-Tools.
    * Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` Registrierungsschlüssel mit einem `Settings`-Wert (REG\_SZ oder REG\_EXPAND\_SZ) mit JSON (bereitgestellt über Gruppenrichtlinie oder Intune)
    * Windows (Benutzerebene): `HKCU\SOFTWARE\Policies\ClaudeCode` (niedrigste Richtlinienpriorität, wird nur verwendet, wenn keine Admin-Quelle vorhanden ist)
  * **Dateibasiert**: `managed-settings.json` und `managed-mcp.json` in Systemverzeichnissen bereitgestellt:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux und WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      Der veraltete Windows-Pfad `C:\ProgramData\ClaudeCode\managed-settings.json` wird ab v2.1.75 nicht mehr unterstützt. Administratoren, die Einstellungen an diesem Speicherort bereitgestellt haben, müssen Dateien zu `C:\Program Files\ClaudeCode\managed-settings.json` migrieren.
    </Warning>

    Dateibasierte verwaltete Einstellungen unterstützen auch ein Drop-in-Verzeichnis unter `managed-settings.d/` im gleichen Systemverzeichnis neben `managed-settings.json`. Dies ermöglicht es separaten Teams, unabhängige Richtlinienfragmente bereitzustellen, ohne Änderungen an einer einzelnen Datei zu koordinieren.

    Nach der systemd-Konvention wird `managed-settings.json` zuerst als Basis zusammengeführt, dann werden alle `*.json`-Dateien im Drop-in-Verzeichnis alphabetisch sortiert und oben zusammengeführt. Spätere Dateien überschreiben frühere für Skalarwerte; Arrays werden verkettet und dedupliziert; Objekte werden tiefgreifend zusammengeführt. Versteckte Dateien, die mit `.` beginnen, werden ignoriert.

    Verwenden Sie numerische Präfixe, um die Zusammenführungsreihenfolge zu steuern, z. B. `10-telemetry.json` und `20-security.json`.

  Siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings) und [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration) für Details.

  Dieses [Repository](https://github.com/anthropics/claude-code/tree/main/examples/mdm) enthält Starter-Bereitstellungsvorlagen für Jamf, Iru (Kandji), Intune und Gruppenrichtlinie. Verwenden Sie diese als Ausgangspunkte und passen Sie sie an Ihre Anforderungen an.

  <Note>
    Verwaltete Bereitstellungen können auch **Plugin-Marketplace-Ergänzungen** mit `strictKnownMarketplaces` einschränken. Weitere Informationen finden Sie unter [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Andere Konfiguration** wird in `~/.claude.json` gespeichert. Diese Datei enthält Ihre OAuth-Sitzung, [MCP-Server](/de/mcp)-Konfigurationen für Benutzer- und lokale Bereiche, projektbezogenen Status (zulässige Tools, Vertrauenseinstellungen) und verschiedene Caches. Projektbezogene MCP-Server werden separat in `.mcp.json` gespeichert.

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

Das veröffentlichte Schema wird regelmäßig aktualisiert und enthält möglicherweise keine Einstellungen, die in den neuesten CLI-Versionen hinzugefügt wurden. Eine Validierungswarnung zu einem kürzlich dokumentierten Feld bedeutet daher nicht unbedingt, dass Ihre Konfiguration ungültig ist.

### Wenn Änderungen wirksam werden

Claude Code überwacht Ihre Einstellungsdateien und lädt sie neu, wenn sie sich ändern, sodass Änderungen an den meisten Schlüsseln ohne Neustart auf die laufende Sitzung angewendet werden. Dies umfasst `permissions`, `hooks` und Anmeldedaten-Helper wie `apiKeyHelper`. Das Neuladen umfasst Benutzer-, Projekt-, lokale und verwaltete Einstellungen, und der [`ConfigChange` Hook](/de/hooks#configchange) wird für jede erkannte Änderung ausgelöst.

Einige wenige Schlüssel werden einmal beim Sitzungsstart gelesen und gelten stattdessen beim nächsten Neustart:

* `model`: Verwenden Sie [`/model`](/de/model-config#setting-your-model), um während der Sitzung zu wechseln
* [`outputStyle`](/de/output-styles): Teil der Systemaufforderung, die beim `/clear` oder Neustart neu erstellt wird

### Verfügbare Einstellungen

`settings.json` unterstützt eine Reihe von Optionen:

| Schlüssel                         | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Beispiel                                                                                                                         |
| :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | Führen Sie den Haupt-Thread als benannten Subagent aus. Wendet den Systemaufforderung, die Werkzeugbeschränkungen und das Modell des Subagent an. Siehe [Rufen Sie Subagents explizit auf](/de/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `"code-reviewer"`                                                                                                                |
| `allowedChannelPlugins`           | (Nur verwaltete Einstellungen) Allowlist von Channel-Plugins, die Nachrichten pushen dürfen. Ersetzt die Standard-Anthropic-Allowlist, wenn gesetzt. Undefined = auf Standard zurückfallen, leeres Array = alle Channel-Plugins blockieren. Erfordert `channelsEnabled: true`. Siehe [Einschränken Sie, welche Channel-Plugins ausgeführt werden können](/de/channels#restrict-which-channel-plugins-can-run)                                                                                                                                                                                                                                                                                                                            | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                           |
| `allowedHttpHookUrls`             | Allowlist von URL-Mustern, auf die HTTP-Hooks abzielen können. Unterstützt `*` als Platzhalter. Wenn gesetzt, werden Hooks mit nicht übereinstimmenden URLs blockiert. Undefined = keine Einschränkung, leeres Array = alle HTTP-Hooks blockieren. Arrays werden über Einstellungsquellen zusammengeführt. Siehe [Hook-Konfiguration](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                               | `["https://hooks.example.com/*"]`                                                                                                |
| `allowedMcpServers`               | Wenn in managed-settings.json gesetzt, Allowlist von MCP-Servern, die Benutzer konfigurieren können. Undefined = keine Einschränkungen, leeres Array = Lockdown. Gilt für alle Bereiche. Denylist hat Vorrang. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `[{ "serverName": "github" }]`                                                                                                   |
| `allowManagedHooksOnly`           | (Nur verwaltete Einstellungen) Nur verwaltete Hooks, SDK-Hooks und Hooks von Plugins, die in verwalteten Einstellungen `enabledPlugins` erzwungen aktiviert sind, werden geladen. Benutzer-, Projekt- und alle anderen Plugin-Hooks werden blockiert. Siehe [Hook-Konfiguration](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                           |
| `allowManagedMcpServersOnly`      | (Nur verwaltete Einstellungen) Nur `allowedMcpServers` aus verwalteten Einstellungen werden berücksichtigt. `deniedMcpServers` wird weiterhin aus allen Quellen zusammengeführt. Benutzer können weiterhin MCP-Server hinzufügen, aber nur die von Admin definierte Allowlist gilt. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                           |
| `allowManagedPermissionRulesOnly` | (Nur verwaltete Einstellungen) Verhindern Sie, dass Benutzer- und Projekteinstellungen `allow`, `ask` oder `deny` Berechtigungsregeln definieren. Nur Regeln in verwalteten Einstellungen gelten. Siehe [Nur verwaltete Einstellungen](/de/permissions#managed-only-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `true`                                                                                                                           |
| `alwaysThinkingEnabled`           | Aktivieren Sie [erweitertes Denken](/de/model-config#extended-thinking) standardmäßig für alle Sitzungen. Normalerweise über den Befehl `/config` konfiguriert, anstatt direkt zu bearbeiten. Um das Denken unabhängig von dieser Einstellung auszuschalten, setzen Sie [`CLAUDE_CODE_DISABLE_THINKING`](/de/env-vars) in `env`                                                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                           |
| `apiKeyHelper`                    | Benutzerdefiniertes Skript, das in `/bin/sh` ausgeführt werden soll, um einen Auth-Wert zu generieren. Dieser Wert wird als `X-Api-Key` und `Authorization: Bearer` Header für Modellanfragen gesendet. Setzen Sie das Aktualisierungsintervall mit [`CLAUDE_CODE_API_KEY_HELPER_TTL_MS`](/de/env-vars)                                                                                                                                                                                                                                                                                                                                                                                                                                  | `/bin/generate_temp_api_key.sh`                                                                                                  |
| `attribution`                     | Passen Sie die Zuschreibung für Git-Commits und Pull Requests an. Siehe [Zuschreibungseinstellungen](#attribution-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                          |
| `autoMemoryDirectory`             | Benutzerdefiniertes Verzeichnis für [automatisches Speichern](/de/memory#storage-location). Akzeptiert einen absoluten Pfad oder einen `~/`-erweiterten Pfad. Akzeptiert von Richtlinien- und Benutzereinstellungen sowie vom Flag `--settings`. Nicht akzeptiert von Projekt- oder lokalen Einstellungen, da ein geklontes Repository eine Datei bereitstellen könnte, um Speicherschreibvorgänge an sensible Orte umzuleiten                                                                                                                                                                                                                                                                                                           | `"~/my-memory-dir"`                                                                                                              |
| `autoMemoryEnabled`               | Aktivieren Sie [automatisches Speichern](/de/memory#enable-or-disable-auto-memory). Wenn `false`, liest Claude nicht aus dem oder schreibt nicht in das automatische Speicherverzeichnis. Standard: `true`. Sie können dies auch während einer Sitzung mit `/memory` umschalten. Um dies über eine Umgebungsvariable zu deaktivieren, setzen Sie [`CLAUDE_CODE_DISABLE_AUTO_MEMORY`](/de/env-vars) in `env`                                                                                                                                                                                                                                                                                                                              | `false`                                                                                                                          |
| `autoMode`                        | Passen Sie an, was der [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode)-Klassifizierer blockiert und erlaubt. Enthält `environment`, `allow`, `soft_deny` und `hard_deny` Arrays von Prosa-Regeln. Schließen Sie die Literalzeichenkette `"$defaults"` in ein Array ein, um die integrierten Regeln an dieser Position zu erben. Siehe [Konfigurieren Sie den Auto-Modus](/de/auto-mode-config). Nicht aus gemeinsamen Projekteinstellungen gelesen                                                                                                                                                                                                                                                                   | `{"soft_deny": ["$defaults", "Never run terraform apply"]}`                                                                      |
| `autoScrollEnabled`               | Im [Fullscreen-Rendering](/de/fullscreen) folgen Sie neuer Ausgabe zum unteren Ende des Gesprächs. Standard: `true`. Wird in `/config` als **Auto-scroll** angezeigt. Berechtigungsaufforderungen scrollen weiterhin in die Ansicht, wenn dies ausgeschaltet ist                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `false`                                                                                                                          |
| `autoUpdatesChannel`              | Release-Kanal zum Folgen von Updates. Verwenden Sie `"stable"` für eine Version, die normalerweise etwa eine Woche alt ist und Versionen mit großen Regressionen überspringt, oder `"latest"` (Standard) für die neueste Version. Um Auto-Updates vollständig zu deaktivieren, setzen Sie [`DISABLE_AUTOUPDATER`](/de/setup#disable-auto-updates) in `env`                                                                                                                                                                                                                                                                                                                                                                               | `"stable"`                                                                                                                       |
| `availableModels`                 | Beschränken Sie, welche Modelle Benutzer über `/model`, `--model` oder `ANTHROPIC_MODEL` auswählen können. Beeinflusst nicht die Standardoption. Siehe [Modellauswahl einschränken](/de/model-config#restrict-model-selection)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `["sonnet", "haiku"]`                                                                                                            |
| `awaySummaryEnabled`              | Zeigen Sie eine einzeilige Sitzungszusammenfassung an, wenn Sie nach einigen Minuten zur Befehlszeile zurückkehren. Setzen Sie auf `false` oder deaktivieren Sie Sitzungszusammenfassung in `/config`, um zu deaktivieren. Gleich wie [`CLAUDE_CODE_ENABLE_AWAY_SUMMARY`](/de/env-vars)                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `true`                                                                                                                           |
| `awsAuthRefresh`                  | Benutzerdefiniertes Skript, das das `.aws`-Verzeichnis ändert (siehe [erweiterte Anmeldedatenkonfiguration](/de/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `aws sso login --profile myprofile`                                                                                              |
| `awsCredentialExport`             | Benutzerdefiniertes Skript, das JSON mit AWS-Anmeldedaten ausgibt (siehe [erweiterte Anmeldedatenkonfiguration](/de/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `/bin/generate_aws_grant.sh`                                                                                                     |
| `blockedMarketplaces`             | (Nur verwaltete Einstellungen) Blocklist von Marketplace-Quellen. Erzwungen bei Marketplace-Hinzufügung und bei Plugin-Installation, Update, Aktualisierung und Auto-Update, sodass ein Marketplace, der vor dem Setzen der Richtlinie hinzugefügt wurde, nicht zum Abrufen von Plugins verwendet werden kann. Blockierte Quellen werden vor dem Download überprüft, sodass sie das Dateisystem nie berühren. Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                   | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                          |
| `channelsEnabled`                 | (Nur verwaltete Einstellungen) Erlauben Sie [Kanäle](/de/channels) für die Organisation. Bei Claude.ai Team- und Enterprise-Plänen werden Kanäle blockiert, wenn dies nicht gesetzt oder `false` ist. Für [Anthropic Console](/de/authentication#claude-console-authentication)-Konten mit API-Schlüssel-Authentifizierung sind Kanäle standardmäßig zulässig, es sei denn, Ihre Organisation stellt verwaltete Einstellungen bereit. In diesem Fall muss dieser Schlüssel auf `true` gesetzt werden                                                                                                                                                                                                                                     | `true`                                                                                                                           |
| `claudeMd`                        | (Nur verwaltete Einstellungen) CLAUDE.md-ähnliche Anweisungen, die als organisationsverwalteter Speicher eingespritzt werden. Wird nur berücksichtigt, wenn in verwalteten oder Richtlinieneinstellungen gesetzt, und ignoriert in Benutzer-, Projekt- und lokalen Einstellungen. Siehe [organisationsweite CLAUDE.md](/de/memory#deploy-organization-wide-claude-md)                                                                                                                                                                                                                                                                                                                                                                    | `"Always run make lint before committing."`                                                                                      |
| `claudeMdExcludes`                | Glob-Muster oder absolute Pfade von `CLAUDE.md`-Dateien, die beim Laden von [Speicher](/de/memory) übersprungen werden sollen. Muster werden gegen absolute Dateipfade abgeglichen. Gilt nur für Benutzer-, Projekt- und lokalen Speicher; verwaltete Richtliniendateien können nicht ausgeschlossen werden                                                                                                                                                                                                                                                                                                                                                                                                                              | `["**/vendor/**/CLAUDE.md"]`                                                                                                     |
| `cleanupPeriodDays`               | Sitzungsdateien, die älter als dieser Zeitraum sind, werden beim Start gelöscht (Standard: 30 Tage, Minimum 1). Das Setzen auf `0` wird mit einem Validierungsfehler abgelehnt. Steuert auch den Altersgrenzwert für die automatische Entfernung von [verwaisten Subagent-Worktrees](/de/worktrees#clean-up-worktrees) beim Start. Um Transkriptschreibvorgänge vollständig zu deaktivieren, setzen Sie die Umgebungsvariable [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/de/env-vars) oder verwenden Sie im nicht-interaktiven Modus (`-p`) das Flag `--no-session-persistence` oder die SDK-Option `persistSession: false`.                                                                                                                   | `20`                                                                                                                             |
| `companyAnnouncements`            | Ankündigung, die Benutzern beim Start angezeigt werden soll. Wenn mehrere Ankündigungen bereitgestellt werden, werden sie zufällig durchlaufen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                          |
| `defaultShell`                    | Standard-Shell für Input-Box `!` Befehle. Akzeptiert `"bash"` (Standard) oder `"powershell"`. Das Setzen auf `"powershell"` leitet interaktive `!` Befehle über PowerShell unter Windows. Erfordert `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Siehe [PowerShell-Tool](/de/tools-reference#powershell-tool)                                                                                                                                                                                                                                                                                                                                                                                                                                    | `"powershell"`                                                                                                                   |
| `deniedMcpServers`                | Wenn in managed-settings.json gesetzt, Denylist von MCP-Servern, die explizit blockiert sind. Gilt für alle Bereiche einschließlich verwalteter Server. Denylist hat Vorrang vor Allowlist. Siehe [Verwaltete MCP-Konfiguration](/de/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `[{ "serverName": "filesystem" }]`                                                                                               |
| `disableAgentView`                | Setzen Sie auf `true`, um [Hintergrund-Agenten und Agent-Ansicht](/de/agent-view) auszuschalten: `claude agents`, `--bg`, `/background` und den On-Demand-Supervisor. Normalerweise in [verwalteten Einstellungen](/de/permissions#managed-settings) gesetzt. Entspricht dem Setzen von `CLAUDE_CODE_DISABLE_AGENT_VIEW` auf `1`                                                                                                                                                                                                                                                                                                                                                                                                         | `true`                                                                                                                           |
| `disableAllHooks`                 | Deaktivieren Sie alle [Hooks](/de/hooks) und alle benutzerdefinierten [Statuszeilen](/de/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                           |
| `disableAutoMode`                 | Setzen Sie auf `"disable"`, um zu verhindern, dass der [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode) aktiviert wird. Entfernt `auto` aus dem `Shift+Tab`-Zyklus und lehnt `--permission-mode auto` beim Start ab. Am nützlichsten in [verwalteten Einstellungen](/de/permissions#managed-settings), wo Benutzer es nicht überschreiben können                                                                                                                                                                                                                                                                                                                                                                      | `"disable"`                                                                                                                      |
| `disableDeepLinkRegistration`     | Setzen Sie auf `"disable"`, um zu verhindern, dass Claude Code den `claude-cli://` Protokoll-Handler beim Start mit dem Betriebssystem registriert. [Deep Links](/de/deep-links) ermöglichen es externen Tools, eine Claude Code-Sitzung mit einer vorausgefüllten Aufforderung zu öffnen. Nützlich in Umgebungen, in denen die Protokoll-Handler-Registrierung eingeschränkt oder separat verwaltet wird                                                                                                                                                                                                                                                                                                                                | `"disable"`                                                                                                                      |
| `disabledMcpjsonServers`          | Liste spezifischer MCP-Server aus `.mcp.json`-Dateien zum Ablehnen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `["filesystem"]`                                                                                                                 |
| `disableRemoteControl`            | {/* min-version: 2.1.128 */}Deaktivieren Sie [Remote Control](/de/remote-control): blockiert `claude remote-control`, das Flag `--remote-control`, Auto-Start und den In-Session-Toggle. Normalerweise in [verwalteten Einstellungen](/de/permissions#managed-settings) für die Pro-Gerät-MDM-Durchsetzung platziert, funktioniert aber aus jedem Bereich. Erfordert Claude Code v2.1.128 oder später                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                           |
| `disableSkillShellExecution`      | Deaktivieren Sie die Inline-Shell-Ausführung für `` !`...` `` und ` ```! ` Blöcke in [Skills](/de/skills) und benutzerdefinierten Befehlen aus Benutzer-, Projekt-, Plugin- oder zusätzlichen Verzeichnisquellen. Befehle werden durch `[shell command execution disabled by policy]` ersetzt, anstatt ausgeführt zu werden. Gebündelte und verwaltete Skills sind nicht betroffen. Am nützlichsten in [verwalteten Einstellungen](/de/permissions#managed-settings), wo Benutzer es nicht überschreiben können                                                                                                                                                                                                                          | `true`                                                                                                                           |
| `editorMode`                      | Tastaturkürzel-Modus für die Eingabeaufforderung: `"normal"` oder `"vim"`. Standard: `"normal"`. Wird in `/config` als **Editor mode** angezeigt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `"vim"`                                                                                                                          |
| `effortLevel`                     | Persistieren Sie die [Anstrengungsstufe](/de/model-config#adjust-effort-level) über Sitzungen hinweg. Akzeptiert `"low"`, `"medium"`, `"high"` oder `"xhigh"`. Wird automatisch geschrieben, wenn Sie `/effort` mit einem dieser Werte ausführen. `--effort` und [`CLAUDE_CODE_EFFORT_LEVEL`](/de/env-vars) überschreiben dies für eine Sitzung. Siehe [Anstrengungsstufe anpassen](/de/model-config#adjust-effort-level) für unterstützte Modelle                                                                                                                                                                                                                                                                                       | `"xhigh"`                                                                                                                        |
| `enableAllProjectMcpServers`      | Genehmigen Sie automatisch alle MCP-Server, die in Projekt-`.mcp.json`-Dateien definiert sind                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `true`                                                                                                                           |
| `enabledMcpjsonServers`           | Liste spezifischer MCP-Server aus `.mcp.json`-Dateien zum Genehmigen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `["memory", "github"]`                                                                                                           |
| `env`                             | Umgebungsvariablen, die auf jede Sitzung und auf Subprozesse angewendet werden, die Claude Code von ihr aus startet. {/* min-version: 2.1.143 */}Ab v2.1.143 werden `NO_COLOR` und `FORCE_COLOR`, die hier gesetzt sind, an Subprozesse übergeben, ändern aber nicht die Farben der Claude Code-Oberfläche selbst. Setzen Sie diese in Ihrer Shell, bevor Sie `claude` starten, um die Oberflächenfarben zu ändern                                                                                                                                                                                                                                                                                                                       | `{"FOO": "bar"}`                                                                                                                 |
| `fastModePerSessionOptIn`         | Wenn `true`, bleibt der schnelle Modus nicht über Sitzungen hinweg bestehen. Jede Sitzung startet mit ausgeschaltetem schnellen Modus und erfordert, dass Benutzer ihn mit `/fast` aktivieren. Die Voreinstellung des Benutzers für den schnellen Modus wird weiterhin gespeichert. Siehe [Opt-in pro Sitzung erforderlich](/de/fast-mode#require-per-session-opt-in)                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                           |
| `feedbackSurveyRate`              | Wahrscheinlichkeit (0–1), dass die [Sitzungsqualitätsumfrage](/de/data-usage#session-quality-surveys) angezeigt wird, wenn berechtigt. Setzen Sie auf `0`, um vollständig zu unterdrücken, oder setzen Sie [`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`](/de/env-vars) in `env`. Nützlich bei Verwendung von Bedrock, Vertex oder Foundry, wo die Standard-Stichprobenquote nicht gilt                                                                                                                                                                                                                                                                                                                                                         | `0.05`                                                                                                                           |
| `fileSuggestion`                  | Konfigurieren Sie ein benutzerdefiniertes Skript für `@` Datei-Autovervollständigung. Siehe [Dateivorschlag-Einstellungen](#file-suggestion-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                                 |
| `forceLoginMethod`                | Verwenden Sie `claudeai`, um die Anmeldung auf Claude.ai-Konten zu beschränken, `console`, um die Anmeldung auf Claude Console (API-Nutzungsabrechnung) Konten zu beschränken                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `claudeai`                                                                                                                       |
| `forceLoginOrgUUID`               | Geben Sie die UUID einer Organisation an, um sie während der Anmeldung automatisch auszuwählen und den Organisationsauswahlschritt zu umgehen, oder akzeptieren Sie ein Array von UUIDs, wobei jede aufgelistete Organisation ohne Vorauswahl akzeptiert wird. Wenn in verwalteten Einstellungen gesetzt, schlägt die Anmeldung fehl, wenn das authentifizierte Konto nicht zu einer aufgelisteten Organisation gehört; ein leeres Array schlägt geschlossen fehl und blockiert die Anmeldung mit einer Fehlkonfigurationsmeldung                                                                                                                                                                                                        | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` oder `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `forceRemoteSettingsRefresh`      | (Nur verwaltete Einstellungen) Blockieren Sie den CLI-Start, bis verwaltete Einstellungen aus der Ferne vom Server abgerufen werden. Wenn der Abruf fehlschlägt, wird die CLI beendet, anstatt mit zwischengespeicherten oder keinen Einstellungen fortzufahren. Wenn nicht gesetzt, wird der Start ohne Warten auf Remote-Einstellungen fortgesetzt. Siehe [Fail-Closed-Durchsetzung](/de/server-managed-settings#enforce-fail-closed-startup)                                                                                                                                                                                                                                                                                          | `true`                                                                                                                           |
| `gcpAuthRefresh`                  | Benutzerdefiniertes Skript, das GCP Application Default Credentials aktualisiert, wenn sie ablaufen oder nicht geladen werden können. Siehe [erweiterte Anmeldedatenkonfiguration](/de/google-vertex-ai#advanced-credential-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `gcloud auth application-default login`                                                                                          |
| `hooks`                           | Konfigurieren Sie benutzerdefinierte Befehle, die bei Lebenszyklusereignissen ausgeführt werden. Siehe [Hooks-Dokumentation](/de/hooks) für das Format                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Siehe [Hooks](/de/hooks)                                                                                                         |
| `httpHookAllowedEnvVars`          | Allowlist von Umgebungsvariablennamen, die HTTP-Hooks in Header interpolieren können. Wenn gesetzt, ist die effektive `allowedEnvVars` jedes Hooks der Schnittpunkt mit dieser Liste. Undefined = keine Einschränkung. Arrays werden über Einstellungsquellen zusammengeführt. Siehe [Hook-Konfiguration](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                           | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                    |
| `includeCoAuthoredBy`             | **Veraltet**: Verwenden Sie stattdessen `attribution`. Ob die `co-authored-by Claude` Byline in Git-Commits und Pull Requests einbezogen werden soll (Standard: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `false`                                                                                                                          |
| `includeGitInstructions`          | Integrierte Commit- und PR-Workflow-Anweisungen und den Git-Status-Snapshot in Claudes Systemaufforderung einbeziehen (Standard: `true`). Setzen Sie auf `false`, um beide zu entfernen, z. B. wenn Sie Ihre eigenen Git-Workflow-Skills verwenden. Die Umgebungsvariable `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` hat Vorrang vor dieser Einstellung, wenn sie gesetzt ist                                                                                                                                                                                                                                                                                                                                                                | `false`                                                                                                                          |
| `language`                        | Konfigurieren Sie Claudes bevorzugte Antwortsprache (z. B. `"japanese"`, `"spanish"`, `"french"`). Claude wird standardmäßig in dieser Sprache antworten. Legt auch die [Sprachdiktiersprache](/de/voice-dictation#change-the-dictation-language) fest                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `"japanese"`                                                                                                                     |
| `maxSkillDescriptionChars`        | {/* min-version: 2.1.105 */}Pro-Skill-Zeichenbegrenzung für den kombinierten `description` und `when_to_use` Text in der [Skill-Auflistung](/de/skills#skill-descriptions-are-cut-short), die Claude jede Runde sieht (Standard: `1536`). Text, der länger als dies ist, wird gekürzt. Erhöhen Sie, um lange Beschreibungen intakt zu halten, auf Kosten von mehr Kontext pro Runde; senken Sie, um mehr Skills unter [`skillListingBudgetFraction`](#available-settings) zu passen. Erfordert Claude Code v2.1.105 oder später                                                                                                                                                                                                          | `2048`                                                                                                                           |
| `minimumVersion`                  | Verhindern Sie, dass der Auto-Updater und `claude update` eine Version unter dieser installieren. Das Wechseln vom `"latest"`-Kanal zu `"stable"` über `/config` fordert Sie auf, auf der aktuellen Version zu bleiben oder das Downgrade zu erlauben. Wenn Sie sich entscheiden zu bleiben, wird dieser Wert gesetzt. Auch nützlich in [verwalteten Einstellungen](/de/permissions#managed-settings) um eine organisationsweite Mindestversion festzulegen                                                                                                                                                                                                                                                                              | `"2.1.100"`                                                                                                                      |
| `model`                           | Überschreiben Sie das Standardmodell für Claude Code. `--model` und [`ANTHROPIC_MODEL`](/de/model-config#environment-variables) überschreiben dies für eine Sitzung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `"claude-sonnet-4-6"`                                                                                                            |
| `modelOverrides`                  | Ordnen Sie Anthropic-Modell-IDs Anbieter-spezifischen Modell-IDs wie Bedrock-Inferenzprofil-ARNs zu. Jeder Modellwähler-Eintrag verwendet seinen zugeordneten Wert beim Aufrufen der Anbieter-API. Siehe [Modell-IDs pro Version überschreiben](/de/model-config#override-model-ids-per-version)                                                                                                                                                                                                                                                                                                                                                                                                                                         | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                     |
| `otelHeadersHelper`               | Skript zum Generieren dynamischer OpenTelemetry-Header. Wird beim Start und regelmäßig ausgeführt. Setzen Sie das Aktualisierungsintervall mit [`CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`](/de/env-vars). Siehe [Dynamische Header](/de/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `/bin/generate_otel_headers.sh`                                                                                                  |
| `outputStyle`                     | Konfigurieren Sie einen Ausgabestil, um die Systemaufforderung anzupassen. Siehe [Ausgabestil-Dokumentation](/de/output-styles)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `"Explanatory"`                                                                                                                  |
| `parentSettingsBehavior`          | {/* min-version: 2.1.133 */}(Nur verwaltete Einstellungen) Steuert, ob verwaltete Einstellungen, die programmgesteuert von einem eingebetteten Host-Prozess wie dem Agent SDK oder einer IDE-Erweiterung bereitgestellt werden, gelten, wenn auch eine von Admin bereitgestellte verwaltete Ebene vorhanden ist. `"first-wins"`: die von Parent bereitgestellten Einstellungen werden verworfen und nur die Admin-Ebene gilt. `"merge"`: die von Parent bereitgestellten Einstellungen gelten unter der Admin-Ebene, gefiltert, sodass sie die Richtlinie verschärfen, aber nicht lockern können. Hat keine Auswirkung, wenn keine Admin-Ebene bereitgestellt wird. Standard: `"first-wins"`. Erfordert Claude Code v2.1.133 oder später | `"merge"`                                                                                                                        |
| `permissions`                     | Siehe Tabelle unten für die Struktur der Berechtigungen.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                  |
| `plansDirectory`                  | Passen Sie an, wo Plandateien gespeichert werden. Der Pfad ist relativ zum Projektstamm. Standard: `~/.claude/plans`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `"./plans"`                                                                                                                      |
| `pluginTrustMessage`              | (Nur verwaltete Einstellungen) Benutzerdefinierte Nachricht, die der vor der Installation angezeigten Plugin-Vertrauenswarnung angehängt wird. Verwenden Sie dies, um organisationsspezifischen Kontext hinzuzufügen, z. B. um zu bestätigen, dass Plugins aus Ihrem internen Marketplace überprüft sind.                                                                                                                                                                                                                                                                                                                                                                                                                                | `"All plugins from our marketplace are approved by IT"`                                                                          |
| `policyHelper`                    | {/* min-version: 2.1.136 */}Von Admin bereitgestellte ausführbare Datei, die verwaltete Einstellungen dynamisch beim Start berechnet. Wird nur von MDM oder einer System-`managed-settings.json`-Datei berücksichtigt. Siehe [Berechnen Sie verwaltete Einstellungen mit einem Policy Helper](#compute-managed-settings-with-a-policy-helper). Erfordert Claude Code v2.1.136 oder später                                                                                                                                                                                                                                                                                                                                                | `{"path": "/usr/local/bin/claude-policy"}`                                                                                       |
| `preferredNotifChannel`           | Methode für Task-Complete- und Berechtigungsaufforderungs-Benachrichtigungen: `"auto"`, `"terminal_bell"`, `"iterm2"`, `"iterm2_with_bell"`, `"kitty"`, `"ghostty"` oder `"notifications_disabled"`. Standard: `"auto"`, das eine Desktop-Benachrichtigung in iTerm2, Ghostty und Kitty sendet und in anderen Terminals nichts tut. Setzen Sie `"terminal_bell"`, um das Glockenzeichen in jedem Terminal zu klingeln. Wird in `/config` als **Notifications** angezeigt. Siehe [Erhalten Sie einen Terminal-Glockenzeichen oder eine Benachrichtigung](/de/terminal-config#get-a-terminal-bell-or-notification)                                                                                                                         | `"terminal_bell"`                                                                                                                |
| `prefersReducedMotion`            | Reduzieren oder deaktivieren Sie UI-Animationen (Spinner, Shimmer, Flash-Effekte) für Barrierefreiheit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `true`                                                                                                                           |
| `prUrlTemplate`                   | URL-Vorlage für das PR-Badge, das in der Fußzeile und in Tool-Ergebnis-Zusammenfassungen angezeigt wird. Ersetzt `{host}`, `{owner}`, `{repo}`, `{number}` und `{url}` aus der von `gh` gemeldeten PR-URL. Verwenden Sie dies, um PR-Links auf ein internes Code-Review-Tool statt auf `github.com` zu verweisen. Beeinflusst nicht `#123` Autolinks in Claudes Prosa                                                                                                                                                                                                                                                                                                                                                                    | `"https://reviews.example.com/{owner}/{repo}/pull/{number}"`                                                                     |
| `respectGitignore`                | Steuern Sie, ob der `@` Datei-Picker `.gitignore`-Muster respektiert. Wenn `true` (Standard), werden Dateien, die `.gitignore`-Mustern entsprechen, aus Vorschlägen ausgeschlossen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `false`                                                                                                                          |
| `showClearContextOnPlanAccept`    | Zeigen Sie die Option "Kontext löschen" auf dem Plan-Akzeptanz-Bildschirm an. Standardmäßig `false`. Setzen Sie auf `true`, um die Option wiederherzustellen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `true`                                                                                                                           |
| `showThinkingSummaries`           | Zeigen Sie [erweitertes Denken](/de/model-config#extended-thinking) Zusammenfassungen in interaktiven Sitzungen an. Wenn nicht gesetzt oder `false` (Standard im interaktiven Modus), werden Denk-Blöcke von der API redigiert und als zusammengeklappter Stub angezeigt. Redaktion ändert nur, was Sie sehen, nicht was das Modell generiert: Um Denk-Ausgaben zu reduzieren, [senken Sie das Budget oder deaktivieren Sie das Denken](/de/model-config#extended-thinking) stattdessen. Dieser Einstellung hat keine Auswirkung im nicht-interaktiven Modus (`-p`), dem Agent SDK oder IDE-Erweiterungen wie VS Code                                                                                                                    | `true`                                                                                                                           |
| `showTurnDuration`                | Zeigen Sie Nachrichten zur Dauer der Runde nach Antworten an, z. B. "Cooked for 1m 6s". Standard: `true`. Wird in `/config` als **Show turn duration** angezeigt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `false`                                                                                                                          |
| `skillListingBudgetFraction`      | {/* min-version: 2.1.105 */}Anteil des Kontextfensters des Modells, das für die [Skill-Auflistung](/de/skills#skill-descriptions-are-cut-short) reserviert ist, die Claude jede Runde sieht (Standard: `0.01` = 1%). Wenn die Auflistung das Budget überschreitet, werden Beschreibungen für die am wenigsten verwendeten Skills auf bloße Namen reduziert, sodass Claude sie weiterhin aufrufen kann, aber nicht sieht, warum. Erhöhen Sie, um mehr Beschreibungen sichtbar zu halten, auf Kosten von mehr Kontext pro Runde. `/doctor` zeigt die aktuelle Kürzungsanzahl und welche Skills betroffen sind. Erfordert Claude Code v2.1.105 oder später                                                                                  | `0.02`                                                                                                                           |
| `skillOverrides`                  | {/* min-version: 2.1.129 */}Pro-Skill-Sichtbarkeitsüberschreibungen, die nach Skill-Name verschlüsselt sind. Der Wert ist `"on"`, `"name-only"`, `"user-invocable-only"` oder `"off"`. Ermöglicht es Ihnen, einen Skill auszublenden oder zu reduzieren, ohne seine SKILL.md zu bearbeiten. Gilt nicht für Plugin-Skills, die über `/plugin` verwaltet werden. Das Menü `/skills` schreibt diese in `.claude/settings.local.json`. Siehe [Skill-Sichtbarkeit aus Einstellungen überschreiben](/de/skills#override-skill-visibility-from-settings). Erfordert Claude Code v2.1.129 oder später                                                                                                                                            | `{"legacy-context": "name-only", "deploy": "off"}`                                                                               |
| `skipWebFetchPreflight`           | Überspringen Sie die [WebFetch-Domänensicherheitsprüfung](/de/data-usage#webfetch-domain-safety-check), die jeden angeforderten Hostnamen an `api.anthropic.com` sendet, bevor Sie abrufen. Setzen Sie auf `true` in Umgebungen, die den Datenverkehr zu Anthropic blockieren, wie Bedrock, Vertex AI oder Foundry-Bereitstellungen mit restriktivem Ausgang. Wenn übersprungen, versucht WebFetch jede URL, ohne die Blocklist zu konsultieren                                                                                                                                                                                                                                                                                          | `true`                                                                                                                           |
| `spinnerTipsEnabled`              | Zeigen Sie Tipps im Spinner an, während Claude arbeitet. Setzen Sie auf `false`, um Tipps zu deaktivieren (Standard: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `false`                                                                                                                          |
| `spinnerTipsOverride`             | Überschreiben Sie Spinner-Tipps mit benutzerdefinierten Zeichenketten. `tips`: Array von Tipp-Zeichenketten. `excludeDefault`: wenn `true`, nur benutzerdefinierte Tipps anzeigen; wenn `false` oder nicht vorhanden, werden benutzerdefinierte Tipps mit integrierten Tipps zusammengeführt                                                                                                                                                                                                                                                                                                                                                                                                                                             | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                                |
| `spinnerVerbs`                    | Passen Sie die Aktionsverben an, die im Spinner angezeigt werden, während eine Runde läuft. Setzen Sie `mode` auf `"replace"`, um nur Ihre Verben zu verwenden, oder `"append"`, um sie zu den Standardwerten hinzuzufügen                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                         |
| `sshConfigs`                      | SSH-Verbindungen, die in der [Desktop](/de/desktop#pre-configure-ssh-connections-for-your-team)-Umgebungs-Dropdown angezeigt werden. Jeder Eintrag erfordert `id`, `name` und `sshHost`; `sshPort`, `sshIdentityFile` und `startDirectory` sind optional. Wenn in verwalteten Einstellungen gesetzt, sind Verbindungen für Benutzer schreibgeschützt. Nur aus verwalteten und Benutzereinstellungen gelesen                                                                                                                                                                                                                                                                                                                              | `[{"id": "dev-vm", "name": "Dev VM", "sshHost": "user@dev.example.com"}]`                                                        |
| `statusLine`                      | Konfigurieren Sie eine benutzerdefinierte Statuszeile zur Anzeige von Kontext. Siehe [`statusLine`-Dokumentation](/de/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                      |
| `strictKnownMarketplaces`         | (Nur verwaltete Einstellungen) Allowlist von Plugin-Marketplace-Quellen. Undefined = keine Einschränkungen, leeres Array = Lockdown. Erzwungen bei Marketplace-Hinzufügung und bei Plugin-Installation, Update, Aktualisierung und Auto-Update, sodass ein Marketplace, der vor dem Setzen der Richtlinie hinzugefügt wurde, nicht zum Abrufen von Plugins verwendet werden kann. Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                               | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                          |
| `syntaxHighlightingDisabled`      | Deaktivieren Sie Syntax-Hervorhebung in Diffs, Code-Blöcken und Dateivorschau                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `true`                                                                                                                           |
| `teammateMode`                    | Wie [Agent-Team](/de/agent-teams) Teamkollegen angezeigt werden: `auto` (wählt geteilte Bereiche in tmux oder iTerm2, ansonsten In-Process), `in-process` oder `tmux`. `--teammate-mode` überschreibt dies für eine Sitzung. Siehe [Wählen Sie einen Anzeigemodus](/de/agent-teams#choose-a-display-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                | `"in-process"`                                                                                                                   |
| `terminalProgressBarEnabled`      | Zeigen Sie die Terminal-Fortschrittsleiste in unterstützten Terminals an: ConEmu, Ghostty 1.2.0+ und iTerm2 3.6.6+. Standard: `true`. Wird in `/config` als **Terminal progress bar** angezeigt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `false`                                                                                                                          |
| `tui`                             | Terminal-UI-Renderer. Verwenden Sie `"fullscreen"` für den flimmerfreien [Alt-Screen-Renderer](/de/fullscreen) mit virtualisiertem Scrollback. Verwenden Sie `"default"` für den klassischen Main-Screen-Renderer. Setzen Sie über `/tui`. Sie können auch die Umgebungsvariable [`CLAUDE_CODE_NO_FLICKER`](/de/env-vars) setzen                                                                                                                                                                                                                                                                                                                                                                                                         | `"fullscreen"`                                                                                                                   |
| `useAutoModeDuringPlan`           | Ob Plan Mode Auto-Mode-Semantik verwendet, wenn Auto Mode verfügbar ist. Standard: `true`. Nicht aus gemeinsamen Projekteinstellungen gelesen. Wird in `/config` als "Use auto mode during plan" angezeigt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                          |
| `viewMode`                        | Standard-Transkript-Ansichtsmodus beim Start: `"default"`, `"verbose"` oder `"focus"`. Überschreibt die klebrige `/focus`-Auswahl, wenn gesetzt. Das Flag `--verbose` überschreibt dies für eine Sitzung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `"verbose"`                                                                                                                      |
| `voice`                           | [Sprachdiktier](/de/voice-dictation)-Einstellungen: `enabled` aktiviert Diktieren, `mode` wählt `"hold"` oder `"tap"`, und `autoSubmit` sendet die Aufforderung bei Tastenfreigabe im Hold-Modus. Wird automatisch geschrieben, wenn Sie `/voice` ausführen. Erfordert ein Claude.ai-Konto                                                                                                                                                                                                                                                                                                                                                                                                                                               | `{ "enabled": true, "mode": "tap" }`                                                                                             |
| `voiceEnabled`                    | Veralteter Alias für `voice.enabled`. Bevorzugen Sie das `voice`-Objekt                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `true`                                                                                                                           |
| `wslInheritsWindowsSettings`      | (Nur Windows verwaltete Einstellungen) Wenn `true`, liest Claude Code auf WSL verwaltete Einstellungen aus der Windows-Richtlinienkette zusätzlich zu `/etc/claude-code`, wobei Windows-Quellen Vorrang haben. Wird nur berücksichtigt, wenn in der HKLM-Registrierungsschlüssel oder `C:\Program Files\ClaudeCode\managed-settings.json` gesetzt, beide erfordern Windows-Admin zum Schreiben. Damit die HKCU-Richtlinie auch auf WSL gilt, muss das Flag zusätzlich in HKCU selbst gesetzt werden. Hat keine Auswirkung auf natives Windows                                                                                                                                                                                            | `true`                                                                                                                           |

### Globale Konfigurationseinstellungen

Diese Einstellungen werden in `~/.claude.json` statt in `settings.json` gespeichert. Das Hinzufügen zu `settings.json` löst einen Schema-Validierungsfehler aus.

<Note>
  Versionen vor v2.1.119 speichern auch `autoScrollEnabled`, `editorMode`, `showTurnDuration`, `teammateMode` und `terminalProgressBarEnabled` hier statt in `settings.json`.
</Note>

| Schlüssel                 | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                  | Beispiel   |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- |
| `autoConnectIde`          | Verbinden Sie sich automatisch mit einer laufenden IDE, wenn Claude Code von einem externen Terminal aus startet. Standard: `false`. Wird in `/config` als **Auto-connect to IDE (external terminal)** angezeigt, wenn außerhalb eines VS Code oder JetBrains-Terminals ausgeführt wird. Die Umgebungsvariable [`CLAUDE_CODE_AUTO_CONNECT_IDE`](/de/env-vars) überschreibt dies, wenn gesetzt | `true`     |
| `autoInstallIdeExtension` | Installieren Sie die Claude Code IDE-Erweiterung automatisch, wenn Sie von einem VS Code-Terminal aus ausgeführt werden. Standard: `true`. Wird in `/config` als **Auto-install IDE extension** angezeigt, wenn Sie in einem VS Code oder JetBrains-Terminal ausgeführt werden. Sie können auch die Umgebungsvariable [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/de/env-vars) setzen              | `false`    |
| `externalEditorContext`   | Stellen Sie Claudes vorherige Antwort als `#`-kommentierter Kontext voran, wenn Sie den externen Editor mit `Ctrl+G` öffnen. Standard: `false`. Wird in `/config` als **Show last response in external editor** angezeigt                                                                                                                                                                     | `true`     |
| `teammateDefaultModel`    | Standardmodell für [Agent-Team](/de/agent-teams) Teamkollegen, wenn die Spawn-Aufforderung keinen angibt. Setzen Sie auf einen Modellalias wie `"sonnet"` oder `null`, um das aktuelle `/model`-Modell des Leads zu erben. Wird in `/config` als **Default teammate model** angezeigt                                                                                                         | `"sonnet"` |

### Worktree-Einstellungen

Konfigurieren Sie, wie `--worktree` Git-Worktrees erstellt und verwaltet.

| Schlüssel                     | Beschreibung                                                                                                                                                                                                                                                                                                                                                                | Beispiel                              |
| :---------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.baseRef`            | Welcher Ref neue Worktrees branchen von. `"fresh"` (Standard) brancht von `origin/<default-branch>` für einen sauberen Baum, der dem Remote entspricht. `"head"` brancht von Ihrem aktuellen lokalen `HEAD`, sodass nicht gepushte Commits und Feature-Branch-Status im Worktree vorhanden sind. Gilt für `--worktree`, das `EnterWorktree`-Tool und die Subagent-Isolation | `"head"`                              |
| `worktree.symlinkDirectories` | Verzeichnisse, die vom Haupt-Repository in jeden Worktree symlinkt werden, um große Verzeichnisse auf der Festplatte zu duplizieren. Standardmäßig werden keine Verzeichnisse symlinkt                                                                                                                                                                                      | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Verzeichnisse, die in jedem Worktree über Git Sparse-Checkout (Cone-Modus) ausgecheckt werden. Nur die aufgelisteten Pfade werden auf die Festplatte geschrieben, was in großen Monorepos schneller ist                                                                                                                                                                     | `["packages/my-app", "shared/utils"]` |
| `worktree.bgIsolation`        | {/* min-version: 2.1.143 */}Isolationsmodus für [Hintergrund-Sitzungen](/de/agent-view#how-file-edits-are-isolated). `"worktree"` (Standard) blockiert `Edit`/`Write` im Haupt-Checkout, bis `EnterWorktree` aufgerufen wird. `"none"` ermöglicht es Hintergrund-Jobs, die Arbeitskopie direkt zu bearbeiten. Erfordert Claude Code v2.1.143 oder später                    | `"none"`                              |

Um gitignorierte Dateien wie `.env` in neue Worktrees zu kopieren, verwenden Sie stattdessen eine [`.worktreeinclude`-Datei](/de/worktrees#copy-gitignored-files-into-worktrees) in Ihrem Projektstamm.

### Berechtigungseinstellungen

| Schlüssel                           | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Beispiel                                                               |
| :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| `allow`                             | Array von Berechtigungsregeln, um die Werkzeugnutzung zu erlauben. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) unten für Details zur Mustererkennung                                                                                                                                                                                                                                                                                                                                                                                                                                | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | Array von Berechtigungsregeln, um bei der Werkzeugnutzung um Bestätigung zu bitten. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) unten                                                                                                                                                                                                                                                                                                                                                                                                                                               | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | Array von Berechtigungsregeln, um die Werkzeugnutzung zu verweigern. Verwenden Sie dies, um sensible Dateien vom Claude Code-Zugriff auszuschließen. Siehe [Berechtigungsregelsyntax](#permission-rule-syntax) und [Bash-Berechtigungsbeschränkungen](/de/permissions#tool-specific-permission-rules)                                                                                                                                                                                                                                                                                             | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | Zusätzliche [Arbeitsverzeichnisse](/de/permissions#working-directories) für Dateizugriff. Die meisten `.claude/`-Konfigurationen werden [nicht erkannt](/de/permissions#additional-directories-grant-file-access-not-configuration) aus diesen Verzeichnissen                                                                                                                                                                                                                                                                                                                                     | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | Standard-[Berechtigungsmodus](/de/permission-modes) beim Öffnen von Claude Code. Gültige Werte: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. {/* min-version: 2.1.142 */}Ab Claude Code v2.1.142 wird `auto` ignoriert, wenn es in Projekt- oder lokalen Einstellungen (`.claude/settings.json`, `.claude/settings.local.json`) gesetzt ist, sodass ein Repository sich nicht selbst den Auto-Modus gewähren kann. Setzen Sie es stattdessen in `~/.claude/settings.json`. Das CLI-Flag `--permission-mode` überschreibt diese Einstellung für eine einzelne Sitzung | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | Setzen Sie auf `"disable"`, um zu verhindern, dass der `bypassPermissions`-Modus aktiviert wird. Dies deaktiviert das Befehlszeilenflag `--dangerously-skip-permissions`. Normalerweise in [verwalteten Einstellungen](/de/permissions#managed-settings) platziert, um Organisationsrichtlinien durchzusetzen, funktioniert aber aus jedem Bereich                                                                                                                                                                                                                                                | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | Überspringen Sie die Bestätigungsaufforderung, die vor dem Betreten des Bypass-Berechtigungsmodus über `--dangerously-skip-permissions` oder `defaultMode: "bypassPermissions"` angezeigt wird. Wird ignoriert, wenn in Projekteinstellungen (`.claude/settings.json`) gesetzt, um zu verhindern, dass nicht vertrauenswürdige Repositories die Aufforderung automatisch umgehen                                                                                                                                                                                                                  | `true`                                                                 |

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

| Schlüssel                              | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                                         | Beispiel                          |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- |
| `enabled`                              | Aktivieren Sie Bash-Sandboxing (macOS, Linux und WSL2). Standard: false                                                                                                                                                                                                                                                                                                                                              | `true`                            |
| `failIfUnavailable`                    | Beenden Sie mit einem Fehler beim Start, wenn `sandbox.enabled` true ist, aber die Sandbox nicht gestartet werden kann (fehlende Abhängigkeiten oder nicht unterstützte Plattform). Wenn false (Standard), wird eine Warnung angezeigt und Befehle werden unsandboxed ausgeführt. Vorgesehen für verwaltete Einstellungsbereitstellungen, die Sandboxing als Hard Gate erfordern                                     | `true`                            |
| `autoAllowBashIfSandboxed`             | Genehmigen Sie Bash-Befehle automatisch, wenn sie in einer Sandbox ausgeführt werden. Standard: true                                                                                                                                                                                                                                                                                                                 | `true`                            |
| `excludedCommands`                     | Befehle, die außerhalb der Sandbox ausgeführt werden sollten                                                                                                                                                                                                                                                                                                                                                         | `["docker *"]`                    |
| `allowUnsandboxedCommands`             | Erlauben Sie Befehlen, außerhalb der Sandbox über den Parameter `dangerouslyDisableSandbox` ausgeführt zu werden. Wenn auf `false` gesetzt, ist die Fluchtluke `dangerouslyDisableSandbox` vollständig deaktiviert und alle Befehle müssen in einer Sandbox ausgeführt werden (oder in `excludedCommands` sein). Nützlich für Unternehmensrichtlinien, die striktes Sandboxing erfordern. Standard: true             | `false`                           |
| `filesystem.allowWrite`                | Zusätzliche Pfade, in die Sandbox-Befehle schreiben können. Arrays werden über alle Einstellungsbereiche zusammengeführt: Benutzer-, Projekt- und verwaltete Pfade werden kombiniert, nicht ersetzt. Auch zusammengeführt mit Pfaden aus `Edit(...)` Allow-Berechtigungsregeln. Siehe [Pfadpräfixe](#sandbox-path-prefixes) unten.                                                                                   | `["/tmp/build", "~/.kube"]`       |
| `filesystem.denyWrite`                 | Pfade, in die Sandbox-Befehle nicht schreiben können. Arrays werden über alle Einstellungsbereiche zusammengeführt. Auch zusammengeführt mit Pfaden aus `Edit(...)` Deny-Berechtigungsregeln.                                                                                                                                                                                                                        | `["/etc", "/usr/local/bin"]`      |
| `filesystem.denyRead`                  | Pfade, aus denen Sandbox-Befehle nicht lesen können. Arrays werden über alle Einstellungsbereiche zusammengeführt. Auch zusammengeführt mit Pfaden aus `Read(...)` Deny-Berechtigungsregeln.                                                                                                                                                                                                                         | `["~/.aws/credentials"]`          |
| `filesystem.allowRead`                 | Pfade zum erneuten Erlauben des Lesens innerhalb von `denyRead`-Regionen. Hat Vorrang vor `denyRead`. Arrays werden über alle Einstellungsbereiche zusammengeführt. Verwenden Sie dies, um Workspace-only-Lesezugriffsmuster zu erstellen.                                                                                                                                                                           | `["."]`                           |
| `filesystem.allowManagedReadPathsOnly` | (Nur verwaltete Einstellungen) Nur `filesystem.allowRead` Pfade aus verwalteten Einstellungen werden berücksichtigt. `denyRead` wird weiterhin aus allen Quellen zusammengeführt. Standard: false                                                                                                                                                                                                                    | `true`                            |
| `network.allowUnixSockets`             | (Nur macOS) Unix-Socket-Pfade, auf die in der Sandbox zugegriffen werden kann. Wird unter Linux und WSL2 ignoriert, wo der Seccomp-Filter `socket(AF_UNIX, ...)` Aufrufe nicht überprüfen kann; verwenden Sie stattdessen `allowAllUnixSockets`.                                                                                                                                                                     | `["~/.ssh/agent-socket"]`         |
| `network.allowAllUnixSockets`          | Erlauben Sie alle Unix-Socket-Verbindungen in der Sandbox. Unter Linux und WSL2 ist dies die einzige Möglichkeit, Unix-Sockets zu erlauben, da der Seccomp-Filter übersprungen wird, der ansonsten `socket(AF_UNIX, ...)` Aufrufe blockiert. Standard: false                                                                                                                                                         | `true`                            |
| `network.allowLocalBinding`            | Erlauben Sie das Binden an Localhost-Ports (nur macOS). Standard: false                                                                                                                                                                                                                                                                                                                                              | `true`                            |
| `network.allowMachLookup`              | Zusätzliche XPC/Mach-Servicenamen, die die Sandbox nachschlagen darf (nur macOS). Unterstützt ein einzelnes nachfolgendes `*` für Präfix-Abgleich. Erforderlich für Tools, die über XPC kommunizieren, wie der iOS-Simulator oder Playwright.                                                                                                                                                                        | `["com.apple.coresimulator.*"]`   |
| `network.allowedDomains`               | Array von Domänen, um ausgehenden Netzwerkverkehr zu erlauben. Unterstützt Platzhalter (z. B. `*.example.com`).                                                                                                                                                                                                                                                                                                      | `["github.com", "*.npmjs.org"]`   |
| `network.deniedDomains`                | Array von Domänen, um ausgehenden Netzwerkverkehr zu blockieren. Unterstützt die gleiche Platzhaltersyntax wie `allowedDomains`. Hat Vorrang vor `allowedDomains`, wenn beide übereinstimmen. Wird aus allen Einstellungsquellen unabhängig von `allowManagedDomainsOnly` zusammengeführt.                                                                                                                           | `["sensitive.cloud.example.com"]` |
| `network.allowManagedDomainsOnly`      | (Nur verwaltete Einstellungen) Nur `allowedDomains` und `WebFetch(domain:...)` Allow-Regeln aus verwalteten Einstellungen werden berücksichtigt. Domänen aus Benutzer-, Projekt- und lokalen Einstellungen werden ignoriert. Nicht zulässige Domänen werden automatisch blockiert, ohne den Benutzer zu fragen. Verweigerte Domänen werden weiterhin aus allen Quellen berücksichtigt. Standard: false               | `true`                            |
| `network.httpProxyPort`                | HTTP-Proxy-Port, der verwendet wird, wenn Sie Ihren eigenen Proxy verwenden möchten. Wenn nicht angegeben, führt Claude seinen eigenen Proxy aus.                                                                                                                                                                                                                                                                    | `8080`                            |
| `network.socksProxyPort`               | SOCKS5-Proxy-Port, der verwendet wird, wenn Sie Ihren eigenen Proxy verwenden möchten. Wenn nicht angegeben, führt Claude seinen eigenen Proxy aus.                                                                                                                                                                                                                                                                  | `8081`                            |
| `enableWeakerNestedSandbox`            | Aktivieren Sie schwächere Sandbox für unprivilegierte Docker-Umgebungen (nur Linux und WSL2). **Reduziert die Sicherheit.** Standard: false                                                                                                                                                                                                                                                                          | `true`                            |
| `enableWeakerNetworkIsolation`         | (Nur macOS) Erlauben Sie den Zugriff auf den System-TLS-Vertrauensdienst (`com.apple.trustd.agent`) in der Sandbox. Erforderlich für Go-basierte Tools wie `gh`, `gcloud` und `terraform`, um TLS-Zertifikate zu überprüfen, wenn `httpProxyPort` mit einem MITM-Proxy und benutzerdefinierter CA verwendet wird. **Reduziert die Sicherheit** durch Öffnen eines möglichen Datenexfiltrationspfads. Standard: false | `true`                            |
| `bwrapPath`                            | (Nur verwaltete Einstellungen, Linux/WSL2) Absoluter Pfad zur bubblewrap (`bwrap`) Binärdatei. Überschreibt automatische Erkennung über `PATH`. Wird nur aus [verwalteten Einstellungen](/de/settings#settings-files) berücksichtigt, nicht aus Benutzer- oder Projekteinstellungen. Nützlich, wenn `bwrap` an einem nicht standardmäßigen Ort in verwalteten Umgebungen installiert ist.                            | `/opt/admin/bwrap`                |
| `socatPath`                            | (Nur verwaltete Einstellungen, Linux/WSL2) Absoluter Pfad zur `socat` Binärdatei, die für den Sandbox-Netzwerk-Proxy verwendet wird. Überschreibt automatische Erkennung über `PATH`. Wird nur aus verwalteten Einstellungen berücksichtigt.                                                                                                                                                                         | `/opt/admin/socat`                |

#### Sandbox-Pfadpräfixe

Pfade in `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead` und `filesystem.allowRead` unterstützen diese Präfixe:

| Präfix                | Bedeutung                                                                                       | Beispiel                                                              |
| :-------------------- | :---------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| `/`                   | Absoluter Pfad vom Dateisystem-Root                                                             | `/tmp/build` bleibt `/tmp/build`                                      |
| `~/`                  | Relativ zum Home-Verzeichnis                                                                    | `~/.kube` wird zu `$HOME/.kube`                                       |
| `./` oder kein Präfix | Relativ zum Projektstamm für Projekteinstellungen oder zu `~/.claude` für Benutzereinstellungen | `./output` in `.claude/settings.json` wird zu `<project-root>/output` |

Das ältere `//path`-Präfix für absolute Pfade funktioniert weiterhin. Wenn Sie zuvor ein einzelnes Schrägstrich `/path` erwartet haben, um projektrelativ aufgelöst zu werden, wechseln Sie zu `./path`. Diese Syntax unterscheidet sich von [Read- und Edit-Berechtigungsregeln](/de/permissions#read-and-edit), die `//path` für absolut und `/path` für projektrelativ verwenden. Sandbox-Dateisystempfade verwenden Standard-Konventionen: `/tmp/build` ist ein absoluter Pfad.

**Konfigurationsbeispiel:**

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "deniedDomains": ["uploads.github.com"],
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

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Standard-Pull-Request-Zuschreibung:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Beispiel:**

```json theme={null}
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

```json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Der Befehl wird mit den gleichen Umgebungsvariablen wie [Hooks](/de/hooks) ausgeführt, einschließlich `CLAUDE_PROJECT_DIR`. Er empfängt JSON über stdin mit einem `query`-Feld:

```json theme={null}
{"query": "src/comp"}
```

Geben Sie zeilengetrennte Dateipfade zu stdout aus (derzeit auf 15 begrenzt):

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Beispiel:**

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Hook-Konfiguration

Diese Einstellungen steuern, welche Hooks ausgeführt werden dürfen und worauf HTTP-Hooks zugreifen können. Die Einstellung `allowManagedHooksOnly` kann nur in [verwalteten Einstellungen](#settings-files) konfiguriert werden. Die URL- und Umgebungsvariablen-Allowlists können auf jeder Einstellungsebene gesetzt werden und werden über Quellen zusammengeführt.

**Verhalten, wenn `allowManagedHooksOnly` `true` ist:**

* Verwaltete Hooks und SDK-Hooks werden geladen
* Hooks von Plugins, die in verwalteten Einstellungen `enabledPlugins` erzwungen aktiviert sind, werden geladen. Dies ermöglicht es Administratoren, überprüfte Hooks über einen Organisations-Marketplace zu verteilen, während alles andere blockiert wird. Vertrauen wird durch vollständige `plugin@marketplace` ID gewährt, daher bleibt ein Plugin mit dem gleichen Namen aus einem anderen Marketplace blockiert
* Benutzer-Hooks, Projekt-Hooks und alle anderen Plugin-Hooks werden blockiert

**HTTP-Hook-URLs einschränken:**

Begrenzen Sie, auf welche URLs HTTP-Hooks abzielen können. Unterstützt `*` als Platzhalter zum Abgleichen. Wenn das Array definiert ist, werden HTTP-Hooks, die auf nicht übereinstimmende URLs abzielen, stillschweigend blockiert. Der Hostname-Abgleich ist case-insensitiv und ignoriert einen nachfolgenden FQDN-Punkt, was DNS-Semantik entspricht.

```json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**HTTP-Hook-Umgebungsvariablen einschränken:**

Begrenzen Sie, welche Umgebungsvariablennamen HTTP-Hooks in Header-Werte interpolieren können. Die effektive `allowedEnvVars` jedes Hooks ist der Schnittpunkt seiner eigenen Liste und dieser Einstellung.

```json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Berechnen Sie verwaltete Einstellungen mit einem Policy Helper

Die Einstellung `policyHelper` verweist auf eine ausführbare Datei, die verwaltete Einstellungen beim Start dynamisch berechnet, sodass Administratoren Richtlinien von Geräteposition, Identität oder einem Remote-Service ableiten können, anstatt eine statische Datei zu verwenden. Konfigurieren Sie sie von MDM oder einer System-`managed-settings.json`-Datei. Claude Code ignoriert `policyHelper`, wenn es in einem anderen Bereich erscheint, einschließlich Benutzereinstellungen, Projekteinstellungen, der HKCU-Registry-Struktur und [serververwalteten Einstellungen](/de/server-managed-settings).

Die Einstellung akzeptiert diese Schlüssel:

| Schlüssel           | Typ    | Beschreibung                                                                                                                                            |
| ------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path`              | string | Absoluter Pfad zur Helper-Ausführungsdatei                                                                                                              |
| `timeoutMs`         | number | Wie lange auf den Helper gewartet werden soll, bevor die Ausführung als fehlgeschlagen behandelt wird                                                   |
| `refreshIntervalMs` | number | Wie oft der Helper im Hintergrund erneut ausgeführt werden soll. Setzen Sie auf `0`, um die Aktualisierung zu deaktivieren, oder auf mindestens `60000` |

Der Helper schreibt eine JSON-Umschlag zu stdout. Setzen Sie die Einstellungen unter einen `managedSettings`-Schlüssel, anstatt auf der obersten Ebene, da ein bloßes Einstellungsobjekt mit `managedSettings` undefined analysiert wird und nichts anwendet:

```json theme={null}
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  },
  "claudeMd": "# Organization context\n...",
  "appendSystemPrompt": "Always cite the internal style guide."
}
```

Wenn der Helper `managedSettings` ausgibt, ersetzt dieses Objekt die dateibasierten verwalteten Einstellungen für die Ausführung. Wenn der Helper beim Start mit einem Fehler beendet wird, druckt Claude Code den Fehler und weigert sich zu starten, daher sollte ein Helper, der Ausfallsicherheit benötigt, aus seinem eigenen Cache bedienen und mit `0` beenden.

### Einstellungspriorität

Einstellungen werden in Prioritätsreihenfolge angewendet. Von höchster zu niedrigster:

1. **Verwaltete Einstellungen** ([serververwaltete](/de/server-managed-settings), [MDM/OS-Richtlinien](#configuration-scopes) oder [verwaltete Einstellungen](/de/settings#settings-files))
   * Richtlinien, die von IT über Server-Bereitstellung, MDM-Konfigurationsprofile, Registry-Richtlinien oder verwaltete Einstellungsdateien bereitgestellt werden
   * Können nicht durch andere Ebenen überschrieben werden, einschließlich Befehlszeilenargumenten
   * Innerhalb der verwalteten Ebene ist die Priorität: serververwaltete > MDM/OS-Richtlinien > dateibasierte (`managed-settings.d/*.json` + `managed-settings.json`) > HKCU-Registry (nur Windows). Nur eine verwaltete Quelle wird verwendet; Quellen werden nicht zusammengeführt. Innerhalb der dateibasierten Ebene werden Drop-in-Dateien und die Basisdatei zusammengeführt.

2. **Befehlszeilenargumente**
   * Temporäre Überschreibungen für eine bestimmte Sitzung. JSON, das über `--settings <file-or-json>` übergeben wird, wird mit dateibasierten Einstellungen unter Verwendung der gleichen Regeln wie die anderen Ebenen zusammengeführt: Ein hier gesetzter Schlüssel überschreibt den gleichen Schlüssel in lokalen, Projekt- oder Benutzereinstellungen, und das Weglassen eines Schlüssels lässt den Wert der niedrigeren Ebene bestehen

3. **Lokale Projekteinstellungen** (`.claude/settings.local.json`)
   * Persönliche projektspezifische Einstellungen

4. **Gemeinsame Projekteinstellungen** (`.claude/settings.json`)
   * Teamübergreifend gemeinsame Projekteinstellungen in der Versionskontrolle

5. **Benutzereinstellungen** (`~/.claude/settings.json`)
   * Persönliche globale Einstellungen

Diese Hierarchie stellt sicher, dass Organisationsrichtlinien immer durchgesetzt werden, während Teams und Einzelpersonen ihre Erfahrung weiterhin anpassen können. Die gleiche Priorität gilt, ob Sie Claude Code von der CLI, der [VS Code-Erweiterung](/de/vs-code) oder einer [JetBrains IDE](/de/jetbrains) ausführen.

Wenn beispielsweise Ihre Benutzereinstellungen `permissions.defaultMode` auf `acceptEdits` setzen und die gemeinsamen Einstellungen eines Projekts es auf `default` setzen, gilt der Projektwert. Das folgende Beispiel zeigt, wie Array-wertige Einstellungen wie Berechtigungsregeln stattdessen kombiniert werden.

<Note>
  **Array-Einstellungen werden über Bereiche zusammengeführt.** Wenn die gleiche Array-wertige Einstellung (wie `sandbox.filesystem.allowWrite` oder `permissions.allow`) in mehreren Bereichen erscheint, werden die Arrays **verkettet und dedupliziert**, nicht ersetzt. Dies bedeutet, dass Bereiche mit niedrigerer Priorität Einträge hinzufügen können, ohne diejenigen mit höherer Priorität zu überschreiben, und umgekehrt. Wenn beispielsweise verwaltete Einstellungen `allowWrite` auf `["/opt/company-tools"]` setzen und ein Benutzer `["~/.kube"]` hinzufügt, sind beide Pfade in der endgültigen Konfiguration enthalten.
</Note>

### Aktive Einstellungen überprüfen

Führen Sie `/status` in Claude Code aus, um zu sehen, welche Einstellungsquellen aktiv sind. Die Registerkarte Status enthält eine Zeile `Setting sources`, die jede Ebene auflistet, die Claude Code für die aktuelle Sitzung geladen hat, z. B. `User settings` oder `Project local settings`. Wenn [verwaltete Einstellungen](/de/managed-settings) wirksam sind, zeigt der Eintrag den Bereitstellungskanal in Klammern an, z. B. `Enterprise managed settings (remote)`, `(plist)`, `(HKLM)`, `(HKCU)` oder `(file)`. Eine Ebene wird in der Liste nur angezeigt, wenn diese Quelle mit mindestens einem Schlüssel geladen wird, daher bedeutet eine leere Liste, dass keine Einstellungsquellen gefunden wurden.

Die Zeile `Setting sources` bestätigt, welche Quellen gelesen werden. Sie zeigt nicht, welche Ebene jeden einzelnen Schlüssel bereitgestellt hat. Die Registerkarte Config im gleichen Dialog ist ein Editor für einen festen Satz von Umschaltern wie Thema und ausführliche Ausgabe, nicht eine Ansicht Ihrer `settings.json`-Inhalte. Wenn eine Einstellungsdatei Fehler enthält, z. B. ungültiges JSON oder einen Wert, der die Validierung nicht besteht, meldet `/status` das Problem, damit Sie es beheben können.

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

```json theme={null}
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

```json theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
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
* **Verwaltete Einstellungen** (`managed-settings.json`): Organisationsweite Richtlinien-Überschreibungen, die die Installation auf allen Ebenen blockieren und das Plugin aus dem Marketplace ausblenden

<Note>
  Projekteinstellungen haben Vorrang vor Benutzereinstellungen, daher führt das Setzen eines Plugins auf `false` in `~/.claude/settings.json` nicht dazu, dass ein Plugin deaktiviert wird, das die `.claude/settings.json` des Projekts aktiviert. Um sich von einem projektaktivierten Plugin auf Ihrem Computer abzumelden, setzen Sie es stattdessen auf `false` in `.claude/settings.local.json`.

  Plugins, die durch verwaltete Einstellungen erzwungen aktiviert sind, können auf diese Weise nicht deaktiviert werden, da verwaltete Einstellungen lokale Einstellungen überschreiben.
</Note>

**Beispiel**:

```json theme={null}
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

1. Teamkollegen werden aufgefordert, den Marketplace zu installieren, wenn sie dem Ordner vertrauen
2. Teamkollegen werden dann aufgefordert, Plugins aus diesem Marketplace zu installieren
3. Benutzer können unerwünschte Marketplaces oder Plugins überspringen (in Benutzereinstellungen gespeichert)
4. Die Installation respektiert Vertrauensgrenzen und erfordert explizite Zustimmung

**Beispiel**:

```json theme={null}
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
* `settings`: Inline-Marketplace, der direkt in settings.json deklariert wird, ohne ein separates gehostetes Repository (verwendet `name` und `plugins`)

Jeder Marketplace-Eintrag akzeptiert auch einen optionalen `autoUpdate` Boolean. Setzen Sie `"autoUpdate": true` neben `source`, um Claude Code zu veranlassen, diesen Marketplace beim Start zu aktualisieren und seine installierten Plugins zu aktualisieren. Wenn nicht angegeben, verwenden offizielle Anthropic-Marketplaces standardmäßig `true` und alle anderen Marketplaces standardmäßig `false`. Siehe [Automatische Aktualisierungen konfigurieren](/de/discover-plugins#configure-auto-updates).

Verwenden Sie `source: 'settings'`, um einen kleinen Satz von Plugins inline zu deklarieren, ohne ein gehostetes Marketplace-Repository einzurichten. Plugins, die hier aufgelistet sind, müssen externe Quellen wie GitHub oder npm referenzieren. Sie müssen weiterhin jedes Plugin separat in `enabledPlugins` aktivieren.

```json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Nur verwaltete Einstellungen**: Steuert, welche Plugin-Marketplaces Benutzer hinzufügen und Plugins installieren dürfen. Diese Einstellung kann nur in [verwalteten Einstellungen](/de/settings#settings-files) konfiguriert werden und bietet Administratoren strikte Kontrolle über Marketplace-Quellen.

**Verwaltete Einstellungsdatei-Speicherorte**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux und WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Wichtige Merkmale**:

* Nur in verwalteten Einstellungen verfügbar (`managed-settings.json`)
* Kann nicht durch Benutzer- oder Projekteinstellungen überschrieben werden (höchste Priorität)
* Durchgesetzt VOR Netzwerk-/Dateisystem-Operationen (blockierte Quellen werden nie ausgeführt)
* Verwendet exakte Übereinstimmung für Quellspezifikationen (einschließlich `ref`, `path` für Git-Quellen), außer `hostPattern` und `pathPattern`, die Regex-Abgleich verwenden

**Allowlist-Verhalten**:

* `undefined` (Standard): Keine Einschränkungen - Benutzer können jeden Marketplace hinzufügen
* Leeres Array `[]`: Vollständiger Lockdown - Benutzer können keine neuen Marketplaces hinzufügen
* Liste von Quellen: Benutzer können nur Marketplaces hinzufügen, die genau übereinstimmen

**Alle unterstützten Quellentypen**:

Die Allowlist unterstützt mehrere Marketplace-Quellentypen. Die meisten Quellen verwenden exakte Übereinstimmung, während `hostPattern` und `pathPattern` Regex-Abgleich gegen den Marketplace-Host und den Dateisystem-Pfad verwenden.

1. **GitHub-Repositories**:

```json theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Felder: `repo` (erforderlich), `ref` (optional: Branch/Tag/SHA), `path` (optional: Unterverzeichnis)

2. **Git-Repositories**:

```json theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Felder: `url` (erforderlich), `ref` (optional: Branch/Tag/SHA), `path` (optional: Unterverzeichnis)

3. **URL-basierte Marketplaces**:

```json theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Felder: `url` (erforderlich), `headers` (optional: HTTP-Header für authentifizierten Zugriff)

<Note>
  URL-basierte Marketplaces laden nur die `marketplace.json`-Datei herunter. Sie laden keine Plugin-Dateien vom Server herunter. Plugins in URL-basierten Marketplaces müssen externe Quellen (GitHub, npm oder Git-URLs) verwenden, anstatt relative Pfade. Für Plugins mit relativen Pfaden verwenden Sie stattdessen einen Git-basierten Marketplace. Siehe [Troubleshooting](/de/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) für Details.
</Note>

4. **NPM-Pakete**:

```json theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Felder: `package` (erforderlich, unterstützt scoped Pakete)

5. **Dateipfade**:

```json theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Felder: `path` (erforderlich: absoluter Pfad zur marketplace.json-Datei)

6. **Verzeichnispfade**:

```json theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Felder: `path` (erforderlich: absoluter Pfad zum Verzeichnis mit `.claude-plugin/marketplace.json`)

7. **Host-Muster-Abgleich**:

```json theme={null}
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

8. **Pfad-Muster-Abgleich**:

```json theme={null}
{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }
{ "source": "pathPattern", "pathPattern": ".*" }
```

Felder: `pathPattern` (erforderlich: Regex-Muster, das gegen das `path`-Feld von `file` und `directory`-Quellen abgeglichen wird)

Verwenden Sie Pfad-Muster-Abgleich, um dateisystem-basierte Marketplaces neben `hostPattern`-Einschränkungen für Netzwerk-Quellen zu erlauben. Setzen Sie `".*"` auf alle lokalen Pfade, oder ein engeres Muster, um auf bestimmte Verzeichnisse zu beschränken.

**Konfigurationsbeispiele**:

Beispiel: Nur bestimmte Marketplaces erlauben:

```json theme={null}
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

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Beispiel: Alle Marketplaces von einem internen Git-Server erlauben:

```json theme={null}
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

```json theme={null}
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

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` erfordert benannte Marketplaces:

```json theme={null}
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

```json theme={null}
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
* Die Einschränkung wird beim Hinzufügen und beim Installieren, Aktualisieren, Aktualisieren und automatischen Aktualisieren von Plugins durchgesetzt. Ein Marketplace, der vor dem Festlegen der Richtlinie hinzugefügt wurde, kann nicht mehr zum Installieren oder Aktualisieren von Plugins verwendet werden, sobald seine Quelle nicht mehr mit der Allowlist übereinstimmt
* Verwaltete Einstellungen haben die höchste Priorität und können nicht überschrieben werden

Siehe [Verwaltete Marketplace-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions) für Dokumentation für Benutzer.

### Verwalten von Plugins

Verwenden Sie den Befehl `/plugin`, um Plugins interaktiv zu verwalten:

* Durchsuchen Sie verfügbare Plugins aus Marketplaces
* Installieren/Deinstallieren Sie Plugins
* Aktivieren/Deaktivieren Sie Plugins
* Zeigen Sie Plugin-Details an (bereitgestellte Skills, Agents, Hooks)
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
* [Konfiguration debuggen](/de/debug-your-config): Diagnostizieren Sie, warum eine Einstellung, ein Hook oder ein MCP-Server nicht wirksam wird
* [Troubleshooting bei Installation und Anmeldung](/de/troubleshoot-install): Installations-, Authentifizierungs- und Plattformprobleme
