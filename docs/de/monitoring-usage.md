> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Überwachung

> Erfahren Sie, wie Sie OpenTelemetry für Claude Code aktivieren und konfigurieren.

Verfolgen Sie die Nutzung, Kosten und Toolaktivität von Claude Code in Ihrer Organisation, indem Sie Telemetriedaten über OpenTelemetry (OTel) exportieren. Claude Code exportiert Metriken als Zeitreihendaten über das Standard-Metriken-Protokoll, Ereignisse über das Logs/Events-Protokoll und optional verteilte Traces über das [Traces-Protokoll](#traces-beta). Konfigurieren Sie Ihre Metriken-, Logs- und Traces-Backends, um Ihre Überwachungsanforderungen zu erfüllen.

## Schnellstart

Konfigurieren Sie OpenTelemetry mit Umgebungsvariablen:

```bash theme={null}
# 1. Telemetrie aktivieren
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Exporter auswählen (beide sind optional - konfigurieren Sie nur das, was Sie benötigen)
export OTEL_METRICS_EXPORTER=otlp       # Optionen: otlp, prometheus, console, none
export OTEL_LOGS_EXPORTER=otlp          # Optionen: otlp, console, none

# 3. OTLP-Endpunkt konfigurieren (für OTLP-Exporter)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Authentifizierung festlegen (falls erforderlich)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Zum Debuggen: Exportintervalle reduzieren
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 Sekunden (Standard: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 Sekunden (Standard: 5000ms)

# 6. Claude Code ausführen
claude
```

<Note>
  Die Standard-Exportintervalle betragen 60 Sekunden für Metriken und 5 Sekunden für Logs. Während der Einrichtung möchten Sie möglicherweise kürzere Intervalle für Debugging-Zwecke verwenden. Denken Sie daran, diese für die Produktionsnutzung zurückzusetzen.
</Note>

Für vollständige Konfigurationsoptionen siehe die [OpenTelemetry-Spezifikation](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Administratorkonfiguration

Administratoren können OpenTelemetry-Einstellungen für alle Benutzer über die [verwaltete Einstellungsdatei](/de/settings#settings-files) konfigurieren. Dies ermöglicht eine zentrale Kontrolle der Telemetrie-Einstellungen in einer Organisation. Weitere Informationen zur Anwendung von Einstellungen finden Sie unter [Einstellungspriorität](/de/settings#settings-precedence).

Beispiel für verwaltete Einstellungskonfiguration:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  Verwaltete Einstellungen können über MDM (Mobile Device Management) oder andere Geräteverwaltungslösungen verteilt werden. Umgebungsvariablen, die in der verwalteten Einstellungsdatei definiert sind, haben hohe Priorität und können von Benutzern nicht überschrieben werden.
</Note>

## Konfigurationsdetails

### Allgemeine Konfigurationsvariablen

| Umgebungsvariable                                   | Beschreibung                                                                                                                                                                                | Beispielwerte                           |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Aktiviert die Telemetrieerfassung (erforderlich)                                                                                                                                            | `1`                                     |
| `OTEL_METRICS_EXPORTER`                             | Metriken-Exporter-Typ(en), kommagetrennt. Verwenden Sie `none` zum Deaktivieren                                                                                                             | `console`, `otlp`, `prometheus`, `none` |
| `OTEL_LOGS_EXPORTER`                                | Logs/Events-Exporter-Typ(en), kommagetrennt. Verwenden Sie `none` zum Deaktivieren                                                                                                          | `console`, `otlp`, `none`               |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protokoll für OTLP-Exporter, gilt für alle Signale                                                                                                                                          | `grpc`, `http/json`, `http/protobuf`    |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | OTLP-Collector-Endpunkt für alle Signale                                                                                                                                                    | `http://localhost:4317`                 |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protokoll für Metriken, überschreibt allgemeine Einstellung                                                                                                                                 | `grpc`, `http/json`, `http/protobuf`    |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | OTLP-Metriken-Endpunkt, überschreibt allgemeine Einstellung                                                                                                                                 | `http://localhost:4318/v1/metrics`      |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protokoll für Logs, überschreibt allgemeine Einstellung                                                                                                                                     | `grpc`, `http/json`, `http/protobuf`    |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | OTLP-Logs-Endpunkt, überschreibt allgemeine Einstellung                                                                                                                                     | `http://localhost:4318/v1/logs`         |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Authentifizierungsheader für OTLP                                                                                                                                                           | `Authorization=Bearer token`            |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Client-Schlüssel für mTLS-Authentifizierung                                                                                                                                                 | Pfad zur Client-Schlüsseldatei          |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Client-Zertifikat für mTLS-Authentifizierung                                                                                                                                                | Pfad zur Client-Zertifikatsdatei        |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Exportintervall in Millisekunden (Standard: 60000)                                                                                                                                          | `5000`, `60000`                         |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Logs-Exportintervall in Millisekunden (Standard: 5000)                                                                                                                                      | `1000`, `10000`                         |
| `OTEL_LOG_USER_PROMPTS`                             | Aktiviert die Protokollierung von Benutzer-Prompt-Inhalten (Standard: deaktiviert)                                                                                                          | `1` zum Aktivieren                      |
| `OTEL_LOG_TOOL_DETAILS`                             | Aktiviert die Protokollierung von Tool-Parametern und Eingabeargumenten in Tool-Ereignissen: Bash-Befehle, MCP-Server- und Tool-Namen, Skill-Namen und Tool-Eingabe (Standard: deaktiviert) | `1` zum Aktivieren                      |
| `OTEL_LOG_TOOL_CONTENT`                             | Aktiviert die Protokollierung von Tool-Eingabe- und Ausgabeinhalten in Span-Ereignissen (Standard: deaktiviert). Erfordert [Tracing](#traces-beta). Der Inhalt wird bei 60 KB gekürzt       | `1` zum Aktivieren                      |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Metriken-Temporalitätspräferenz (Standard: `delta`). Setzen Sie auf `cumulative`, wenn Ihr Backend kumulative Temporalität erwartet                                                         | `delta`, `cumulative`                   |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Intervall zum Aktualisieren dynamischer Header (Standard: 1740000ms / 29 Minuten)                                                                                                           | `900000`                                |

### Metriken-Kardinalitätskontrolle

Die folgenden Umgebungsvariablen steuern, welche Attribute in Metriken enthalten sind, um die Kardinalität zu verwalten:

| Umgebungsvariable                   | Beschreibung                                                               | Standardwert | Beispiel zum Deaktivieren |
| ----------------------------------- | -------------------------------------------------------------------------- | ------------ | ------------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Attribut session.id in Metriken einschließen                               | `true`       | `false`                   |
| `OTEL_METRICS_INCLUDE_VERSION`      | Attribut app.version in Metriken einschließen                              | `false`      | `true`                    |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Attribute user.account\_uuid und user.account\_id in Metriken einschließen | `true`       | `false`                   |

Diese Variablen helfen, die Kardinalität von Metriken zu kontrollieren, was sich auf die Speicheranforderungen und die Abfrageleistung in Ihrem Metriken-Backend auswirkt. Eine niedrigere Kardinalität bedeutet in der Regel bessere Leistung und niedrigere Speicherkosten, aber weniger granulare Daten für die Analyse.

### Traces (Beta)

Verteiltes Tracing exportiert Spans, die jeden Benutzer-Prompt mit den API-Anfragen und Tool-Ausführungen verknüpfen, die er auslöst, sodass Sie eine vollständige Anfrage als einzelnen Trace in Ihrem Tracing-Backend anzeigen können.

Tracing ist standardmäßig deaktiviert. Um es zu aktivieren, setzen Sie sowohl `CLAUDE_CODE_ENABLE_TELEMETRY=1` als auch `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, und setzen Sie dann `OTEL_TRACES_EXPORTER`, um auszuwählen, wohin Spans gesendet werden. Traces verwenden die [allgemeine OTLP-Konfiguration](#allgemeine-konfigurationsvariablen) für Endpunkt, Protokoll und Header erneut.

| Umgebungsvariable                     | Beschreibung                                                                                 | Beispielwerte                        |
| ------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Aktiviert Span-Tracing (erforderlich). `ENABLE_ENHANCED_TELEMETRY_BETA` wird auch akzeptiert | `1`                                  |
| `OTEL_TRACES_EXPORTER`                | Traces-Exporter-Typ(en), kommagetrennt. Verwenden Sie `none` zum Deaktivieren                | `console`, `otlp`, `none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | Protokoll für Traces, überschreibt `OTEL_EXPORTER_OTLP_PROTOCOL`                             | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | OTLP-Traces-Endpunkt, überschreibt `OTEL_EXPORTER_OTLP_ENDPOINT`                             | `http://localhost:4318/v1/traces`    |
| `OTEL_TRACES_EXPORT_INTERVAL`         | Span-Batch-Exportintervall in Millisekunden (Standard: 5000)                                 | `1000`, `10000`                      |

Spans schwärzen Benutzer-Prompt-Text und Tool-Inhalte standardmäßig. Setzen Sie `OTEL_LOG_USER_PROMPTS=1` und `OTEL_LOG_TOOL_CONTENT=1`, um sie einzubeziehen.

### Dynamische Header

Für Unternehmensumgebungen, die eine dynamische Authentifizierung erfordern, können Sie ein Skript konfigurieren, um Header dynamisch zu generieren:

#### Einstellungskonfiguration

Fügen Sie zu Ihrer `.claude/settings.json` hinzu:

```json theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Skriptanforderungen

Das Skript muss gültiges JSON mit Zeichenketten-Schlüssel-Wert-Paaren ausgeben, die HTTP-Header darstellen:

```bash theme={null}
#!/bin/bash
# Beispiel: Mehrere Header
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Aktualisierungsverhalten

Das Headers-Helper-Skript wird beim Start und danach regelmäßig ausgeführt, um Token-Aktualisierung zu unterstützen. Standardmäßig wird das Skript alle 29 Minuten ausgeführt. Passen Sie das Intervall mit der Umgebungsvariable `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` an.

### Unterstützung für Multi-Team-Organisationen

Organisationen mit mehreren Teams oder Abteilungen können benutzerdefinierte Attribute hinzufügen, um zwischen verschiedenen Gruppen zu unterscheiden, indem sie die Umgebungsvariable `OTEL_RESOURCE_ATTRIBUTES` verwenden:

```bash theme={null}
# Benutzerdefinierte Attribute für Team-Identifikation hinzufügen
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Diese benutzerdefinierten Attribute werden in alle Metriken und Ereignisse einbezogen, sodass Sie:

* Metriken nach Team oder Abteilung filtern können
* Kosten pro Kostenstelle verfolgen können
* Team-spezifische Dashboards erstellen können
* Warnungen für bestimmte Teams einrichten können

<Warning>
  **Wichtige Formatierungsanforderungen für OTEL\_RESOURCE\_ATTRIBUTES:**

  Die Umgebungsvariable `OTEL_RESOURCE_ATTRIBUTES` verwendet kommagetrennte Schlüssel=Wert-Paare mit strikten Formatierungsanforderungen:

  * **Keine Leerzeichen erlaubt**: Werte dürfen keine Leerzeichen enthalten. Zum Beispiel ist `user.organizationName=My Company` ungültig
  * **Format**: Muss kommagetrennte Schlüssel=Wert-Paare sein: `key1=value1,key2=value2`
  * **Zulässige Zeichen**: Nur US-ASCII-Zeichen ohne Steuerzeichen, Leerzeichen, doppelte Anführungszeichen, Kommas, Semikola und Backslashes
  * **Sonderzeichen**: Zeichen außerhalb des zulässigen Bereichs müssen prozentcodiert sein

  **Beispiele:**

  ```bash theme={null}
  # ❌ Ungültig - enthält Leerzeichen
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Gültig - verwenden Sie stattdessen Unterstriche oder camelCase
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Gültig - prozentcodieren Sie Sonderzeichen, falls erforderlich
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Hinweis: Das Einschließen von Werten in Anführungszeichen entkommt keine Leerzeichen. Zum Beispiel führt `org.name="My Company"` zum Literalwert `"My Company"` (mit Anführungszeichen enthalten), nicht zu `My Company`.
</Warning>

### Beispielkonfigurationen

Setzen Sie diese Umgebungsvariablen vor dem Ausführen von `claude`. Jeder Block zeigt eine vollständige Konfiguration für einen anderen Exporter oder ein anderes Bereitstellungsszenario:

```bash theme={null}
# Console-Debugging (1-Sekunden-Intervalle)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Mehrere Exporter
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Unterschiedliche Endpunkte/Backends für Metriken und Logs
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Nur Metriken (keine Ereignisse/Logs)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Nur Ereignisse/Logs (keine Metriken)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Verfügbare Metriken und Ereignisse

### Standardattribute

Alle Metriken und Ereignisse teilen diese Standardattribute:

| Attribut            | Beschreibung                                                                                                      | Gesteuert durch                                      |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| `session.id`        | Eindeutige Sitzungskennung                                                                                        | `OTEL_METRICS_INCLUDE_SESSION_ID` (Standard: true)   |
| `app.version`       | Aktuelle Claude Code-Version                                                                                      | `OTEL_METRICS_INCLUDE_VERSION` (Standard: false)     |
| `organization.id`   | Organisations-UUID (wenn authentifiziert)                                                                         | Immer enthalten, wenn verfügbar                      |
| `user.account_uuid` | Konto-UUID (wenn authentifiziert)                                                                                 | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (Standard: true) |
| `user.account_id`   | Konto-ID im getaggten Format, das Anthropic-Admin-APIs entspricht (wenn authentifiziert), wie `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (Standard: true) |
| `user.id`           | Anonyme Geräte-/Installationskennung, generiert pro Claude Code-Installation                                      | Immer enthalten                                      |
| `user.email`        | E-Mail-Adresse des Benutzers (wenn über OAuth authentifiziert)                                                    | Immer enthalten, wenn verfügbar                      |
| `terminal.type`     | Terminal-Typ, wie `iTerm.app`, `vscode`, `cursor` oder `tmux`                                                     | Immer enthalten, wenn erkannt                        |

Ereignisse enthalten zusätzlich die folgenden Attribute. Diese werden niemals an Metriken angehängt, da sie zu unbegrenzter Kardinalität führen würden:

* `prompt.id`: UUID, die einen Benutzer-Prompt mit allen nachfolgenden Ereignissen bis zum nächsten Prompt korreliert. Siehe [Ereigniskorrelationsattribute](#ereigniskorrelationsattribute).
* `workspace.host_paths`: Host-Workspace-Verzeichnisse, die in der Desktop-App ausgewählt wurden, als String-Array

### Metriken

Claude Code exportiert die folgenden Metriken:

| Metrikname                            | Beschreibung                                                          | Einheit |
| ------------------------------------- | --------------------------------------------------------------------- | ------- |
| `claude_code.session.count`           | Anzahl der gestarteten CLI-Sitzungen                                  | count   |
| `claude_code.lines_of_code.count`     | Anzahl der geänderten Codezeilen                                      | count   |
| `claude_code.pull_request.count`      | Anzahl der erstellten Pull Requests                                   | count   |
| `claude_code.commit.count`            | Anzahl der erstellten Git-Commits                                     | count   |
| `claude_code.cost.usage`              | Kosten der Claude Code-Sitzung                                        | USD     |
| `claude_code.token.usage`             | Anzahl der verwendeten Token                                          | tokens  |
| `claude_code.code_edit_tool.decision` | Anzahl der Entscheidungen zur Berechtigung des Code-Bearbeitungstools | count   |
| `claude_code.active_time.total`       | Gesamte aktive Zeit in Sekunden                                       | s       |

### Metrik-Details

Jede Metrik enthält die oben aufgeführten Standardattribute. Metriken mit zusätzlichen kontextspezifischen Attributen werden nachfolgend vermerkt.

#### Sitzungszähler

Wird zu Beginn jeder Sitzung erhöht.

**Attribute**:

* Alle [Standardattribute](#standardattribute)

#### Codezeilen-Zähler

Wird erhöht, wenn Code hinzugefügt oder entfernt wird.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `type`: (`"added"`, `"removed"`)

#### Pull-Request-Zähler

Wird erhöht, wenn Pull Requests über Claude Code erstellt werden.

**Attribute**:

* Alle [Standardattribute](#standardattribute)

#### Commit-Zähler

Wird erhöht, wenn Git-Commits über Claude Code erstellt werden.

**Attribute**:

* Alle [Standardattribute](#standardattribute)

#### Kostenzähler

Wird nach jeder API-Anfrage erhöht.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `model`: Modellkennung (zum Beispiel "claude-sonnet-4-6")

#### Token-Zähler

Wird nach jeder API-Anfrage erhöht.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Modellkennung (zum Beispiel "claude-sonnet-4-6")

#### Code-Edit-Tool-Entscheidungszähler

Wird erhöht, wenn der Benutzer die Verwendung des Edit-, Write- oder NotebookEdit-Tools akzeptiert oder ablehnt.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `tool_name`: Tool-Name (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Benutzerentscheidung (`"accept"`, `"reject"`)
* `source`: Entscheidungsquelle - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` oder `"user_reject"`
* `language`: Programmiersprache der bearbeiteten Datei, wie `"TypeScript"`, `"Python"`, `"JavaScript"` oder `"Markdown"`. Gibt `"unknown"` für nicht erkannte Dateierweiterungen zurück.

#### Aktive-Zeit-Zähler

Verfolgt die tatsächliche Zeit, die aktiv Claude Code verwendet wird, ohne Leerlaufzeit. Diese Metrik wird während Benutzerinteraktionen (Eingabe, Lesen von Antworten) und während CLI-Verarbeitung (Tool-Ausführung, KI-Antwortgenerierung) erhöht.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `type`: `"user"` für Tastaturinteraktionen, `"cli"` für Tool-Ausführung und KI-Antworten

### Ereignisse

Claude Code exportiert die folgenden Ereignisse über OpenTelemetry Logs/Events (wenn `OTEL_LOGS_EXPORTER` konfiguriert ist):

#### Ereigniskorrelationsattribute

Wenn ein Benutzer einen Prompt einreicht, kann Claude Code mehrere API-Aufrufe tätigen und mehrere Tools ausführen. Das Attribut `prompt.id` ermöglicht es Ihnen, alle diese Ereignisse an den einzelnen Prompt zu binden, der sie ausgelöst hat.

| Attribut    | Beschreibung                                                                                                                 |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `prompt.id` | UUID v4-Kennung, die alle Ereignisse verknüpft, die während der Verarbeitung eines einzelnen Benutzer-Prompts erzeugt werden |

Um alle Aktivitäten zu verfolgen, die durch einen einzelnen Prompt ausgelöst werden, filtern Sie Ihre Ereignisse nach einem bestimmten `prompt.id`-Wert. Dies gibt das user\_prompt-Ereignis, alle api\_request-Ereignisse und alle tool\_result-Ereignisse zurück, die während der Verarbeitung dieses Prompts aufgetreten sind.

<Note>
  `prompt.id` ist absichtlich aus Metriken ausgeschlossen, da jeder Prompt eine eindeutige ID generiert, was zu einer ständig wachsenden Anzahl von Zeitreihen führen würde. Verwenden Sie es nur für Ereignisanalyse und Audit-Trails.
</Note>

#### Benutzer-Prompt-Ereignis

Protokolliert, wenn ein Benutzer einen Prompt einreicht.

**Ereignisname**: `claude_code.user_prompt`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"user_prompt"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `prompt_length`: Länge des Prompts
* `prompt`: Prompt-Inhalt (standardmäßig geschwärzt, aktivieren Sie mit `OTEL_LOG_USER_PROMPTS=1`)

#### Tool-Ergebnis-Ereignis

Protokolliert, wenn ein Tool die Ausführung abgeschlossen hat.

**Ereignisname**: `claude_code.tool_result`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"tool_result"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `tool_name`: Name des Tools
* `success`: `"true"` oder `"false"`
* `duration_ms`: Ausführungszeit in Millisekunden
* `error`: Fehlermeldung (falls fehlgeschlagen)
* `decision_type`: Entweder `"accept"` oder `"reject"`
* `decision_source`: Entscheidungsquelle - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` oder `"user_reject"`
* `tool_result_size_bytes`: Größe des Tool-Ergebnisses in Bytes
* `mcp_server_scope`: MCP-Server-Scope-Kennung (für MCP-Tools)
* `tool_parameters` (wenn `OTEL_LOG_TOOL_DETAILS=1`): JSON-Zeichenkette mit Tool-spezifischen Parametern:
  * Für Bash-Tool: enthält `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox` und `git_commit_id` (der Commit-SHA, wenn ein `git commit`-Befehl erfolgreich ist)
  * Für MCP-Tools: enthält `mcp_server_name`, `mcp_tool_name`
  * Für Skill-Tool: enthält `skill_name`
* `tool_input` (wenn `OTEL_LOG_TOOL_DETAILS=1`): JSON-serialisierte Tool-Argumente. Einzelne Werte über 512 Zeichen werden gekürzt, und die gesamte Nutzlast ist auf etwa 4 K Zeichen begrenzt. Gilt für alle Tools einschließlich MCP-Tools.

#### API-Anfrage-Ereignis

Protokolliert für jede API-Anfrage an Claude.

**Ereignisname**: `claude_code.api_request`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"api_request"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `model`: Verwendetes Modell (zum Beispiel "claude-sonnet-4-6")
* `cost_usd`: Geschätzte Kosten in USD
* `duration_ms`: Anfragedauer in Millisekunden
* `input_tokens`: Anzahl der Eingabe-Token
* `output_tokens`: Anzahl der Ausgabe-Token
* `cache_read_tokens`: Anzahl der aus dem Cache gelesenen Token
* `cache_creation_tokens`: Anzahl der Token, die für die Cache-Erstellung verwendet werden
* `speed`: `"fast"` oder `"normal"`, was angibt, ob der schnelle Modus aktiv war

#### API-Fehler-Ereignis

Protokolliert, wenn eine API-Anfrage an Claude fehlschlägt.

**Ereignisname**: `claude_code.api_error`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"api_error"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `model`: Verwendetes Modell (zum Beispiel "claude-sonnet-4-6")
* `error`: Fehlermeldung
* `status_code`: HTTP-Statuscode als Zeichenkette oder `"undefined"` für Nicht-HTTP-Fehler
* `duration_ms`: Anfragedauer in Millisekunden
* `attempt`: Versuchsnummer (für wiederholte Anfragen)
* `speed`: `"fast"` oder `"normal"`, was angibt, ob der schnelle Modus aktiv war

#### Tool-Entscheidungs-Ereignis

Protokolliert, wenn eine Tool-Berechtigungsentscheidung getroffen wird (akzeptieren/ablehnen).

**Ereignisname**: `claude_code.tool_decision`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"tool_decision"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `tool_name`: Name des Tools (zum Beispiel "Read", "Edit", "Write", "NotebookEdit")
* `decision`: Entweder `"accept"` oder `"reject"`
* `source`: Entscheidungsquelle - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` oder `"user_reject"`

## Interpretation von Metriken- und Ereignisdaten

Die exportierten Metriken und Ereignisse unterstützen eine Reihe von Analysen:

### Nutzungsüberwachung

| Metrik                                                        | Analysemöglichkeit                                                             |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `claude_code.token.usage`                                     | Aufschlüsselung nach `type` (input/output), Benutzer, Team oder Modell         |
| `claude_code.session.count`                                   | Verfolgung der Akzeptanz und des Engagements im Laufe der Zeit                 |
| `claude_code.lines_of_code.count`                             | Messung der Produktivität durch Verfolgung von Code-Hinzufügungen/Entfernungen |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Verständnis der Auswirkungen auf Entwicklungs-Workflows                        |

### Kostenüberwachung

Die Metrik `claude_code.cost.usage` hilft bei:

* Verfolgung von Nutzungstrends über Teams oder Einzelpersonen hinweg
* Identifikation von Sitzungen mit hoher Nutzung zur Optimierung

<Note>
  Kostenmetriken sind Näherungswerte. Für offizielle Abrechnungsdaten konsultieren Sie Ihren API-Anbieter (Claude Console, AWS Bedrock oder Google Cloud Vertex).
</Note>

### Warnungen und Segmentierung

Häufige Warnungen, die Sie in Betracht ziehen sollten:

* Kostensteigerungen
* Ungewöhnlicher Token-Verbrauch
* Hohes Sitzungsvolumen von bestimmten Benutzern

Alle Metriken können nach `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model` und `app.version` segmentiert werden.

### Ereignisanalyse

Die Ereignisdaten bieten detaillierte Einblicke in Claude Code-Interaktionen:

**Tool-Nutzungsmuster**: Analysieren Sie Tool-Ergebnis-Ereignisse, um zu identifizieren:

* Am häufigsten verwendete Tools
* Tool-Erfolgsquoten
* Durchschnittliche Tool-Ausführungszeiten
* Fehlermuster nach Tool-Typ

**Leistungsüberwachung**: Verfolgen Sie API-Anfrage-Dauern und Tool-Ausführungszeiten, um Leistungsengpässe zu identifizieren.

## Backend-Überlegungen

Ihre Wahl des Metriken-, Logs- und Traces-Backends bestimmt die Arten von Analysen, die Sie durchführen können:

### Für Metriken

* **Zeitreihendatenbanken (zum Beispiel Prometheus)**: Ratenberechnungen, aggregierte Metriken
* **Spaltenorientierte Speicher (zum Beispiel ClickHouse)**: Komplexe Abfragen, eindeutige Benutzeranalyse
* **Vollständige Observability-Plattformen (zum Beispiel Honeycomb, Datadog)**: Erweiterte Abfragen, Visualisierung, Warnungen

### Für Ereignisse/Logs

* **Log-Aggregationssysteme (zum Beispiel Elasticsearch, Loki)**: Volltextsuche, Log-Analyse
* **Spaltenorientierte Speicher (zum Beispiel ClickHouse)**: Strukturierte Ereignisanalyse
* **Vollständige Observability-Plattformen (zum Beispiel Honeycomb, Datadog)**: Korrelation zwischen Metriken und Ereignissen

### Für Traces

Wählen Sie ein Backend, das verteilte Trace-Speicherung und Span-Korrelation unterstützt:

* **Verteilte Tracing-Systeme (zum Beispiel Jaeger, Zipkin, Grafana Tempo)**: Span-Visualisierung, Request-Waterfalls, Latenzanalyse
* **Vollständige Observability-Plattformen (zum Beispiel Honeycomb, Datadog)**: Trace-Suche und Korrelation mit Metriken und Logs

Für Organisationen, die Daily/Weekly/Monthly Active User (DAU/WAU/MAU) Metriken benötigen, sollten Sie Backends in Betracht ziehen, die effiziente Abfragen eindeutiger Werte unterstützen.

## Dienstinformationen

Alle Metriken und Ereignisse werden mit den folgenden Ressourcenattributen exportiert:

* `service.name`: `claude-code`
* `service.version`: Aktuelle Claude Code-Version
* `os.type`: Betriebssystemtyp (zum Beispiel `linux`, `darwin`, `windows`)
* `os.version`: Betriebssystem-Versionsnummer
* `host.arch`: Host-Architektur (zum Beispiel `amd64`, `arm64`)
* `wsl.version`: WSL-Versionsnummer (nur vorhanden, wenn auf Windows Subsystem for Linux ausgeführt)
* Meter-Name: `com.anthropic.claude_code`

## ROI-Messung-Ressourcen

Für einen umfassenden Leitfaden zur Messung der Kapitalrendite für Claude Code, einschließlich Telemetrie-Setup, Kostenanalyse, Produktivitätsmetriken und automatisierter Berichterstattung, siehe den [Claude Code ROI Measurement Guide](https://github.com/anthropics/claude-code-monitoring-guide). Dieses Repository bietet einsatzbereite Docker Compose-Konfigurationen, Prometheus- und OpenTelemetry-Setups sowie Vorlagen zur Generierung von Produktivitätsberichten, die in Tools wie Linear integriert sind.

## Sicherheit und Datenschutz

* Telemetrie ist opt-in und erfordert explizite Konfiguration
* Rohe Dateiinhalte und Code-Snippets sind nicht in Metriken oder Ereignissen enthalten. Trace-Spans sind ein separater Datenpfad: siehe die Aufzählung `OTEL_LOG_TOOL_CONTENT` unten
* Wenn über OAuth authentifiziert, ist `user.email` in Telemetrie-Attributen enthalten. Wenn dies ein Problem für Ihre Organisation darstellt, arbeiten Sie mit Ihrem Telemetrie-Backend zusammen, um dieses Feld zu filtern oder zu schwärzen
* Benutzer-Prompt-Inhalte werden standardmäßig nicht erfasst. Nur die Prompt-Länge wird aufgezeichnet. Um Benutzer-Prompt-Inhalte einzubeziehen, setzen Sie `OTEL_LOG_USER_PROMPTS=1`
* Tool-Eingabeargumente und Parameter werden standardmäßig nicht protokolliert. Um sie einzubeziehen, setzen Sie `OTEL_LOG_TOOL_DETAILS=1`. Wenn aktiviert, enthalten `tool_result`-Ereignisse ein `tool_parameters`-Attribut mit Bash-Befehlen, MCP-Server- und Tool-Namen sowie Skill-Namen, plus ein `tool_input`-Attribut mit Dateipfaden, URLs, Suchmustern und anderen Argumenten. Einzelne Werte über 512 Zeichen werden gekürzt und die Gesamtmenge ist auf etwa 4 K Zeichen begrenzt, aber die Argumente können immer noch vertrauliche Werte enthalten. Konfigurieren Sie Ihr Telemetrie-Backend, um diese Attribute nach Bedarf zu filtern oder zu schwärzen
* Tool-Eingabe- und Ausgabeinhalte werden in Trace-Spans standardmäßig nicht protokolliert. Um sie einzubeziehen, setzen Sie `OTEL_LOG_TOOL_CONTENT=1`. Wenn aktiviert, enthalten Span-Ereignisse vollständige Tool-Eingabe- und Ausgabeinhalte, gekürzt bei 60 KB pro Span. Dies kann rohe Dateiinhalte aus Read-Tool-Ergebnissen und Bash-Befehlsausgabe enthalten. Konfigurieren Sie Ihr Telemetrie-Backend, um diese Attribute nach Bedarf zu filtern oder zu schwärzen

## Überwachung von Claude Code auf Amazon Bedrock

Für detaillierte Anleitung zur Überwachung der Claude Code-Nutzung für Amazon Bedrock siehe [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
