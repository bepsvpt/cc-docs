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

Claude Code übergibt `OTEL_*` Umgebungsvariablen nicht an die Subprozesse, die es erzeugt, einschließlich des Bash-Tools, Hooks, MCP-Server und Sprachserver. Eine OpenTelemetry-instrumentierte Anwendung, die Sie über das Bash-Tool ausführen, erbt nicht den Exporter-Endpunkt oder die Header von Claude Code, daher setzen Sie diese Variablen direkt im Befehl, wenn diese Anwendung ihre eigene Telemetrie exportieren muss.

## Konfigurationsdetails

### Allgemeine Konfigurationsvariablen

| Umgebungsvariable                                   | Beschreibung                                                                                                                                                                                                                                                                                                                                                        | Beispielwerte                                                                                                                             |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Aktiviert die Telemetrieerfassung (erforderlich)                                                                                                                                                                                                                                                                                                                    | `1`                                                                                                                                       |
| `OTEL_METRICS_EXPORTER`                             | Metriken-Exporter-Typ(en), kommagetrennt. Verwenden Sie `none` zum Deaktivieren                                                                                                                                                                                                                                                                                     | `console`, `otlp`, `prometheus`, `none`                                                                                                   |
| `OTEL_LOGS_EXPORTER`                                | Logs/Events-Exporter-Typ(en), kommagetrennt. Verwenden Sie `none` zum Deaktivieren                                                                                                                                                                                                                                                                                  | `console`, `otlp`, `none`                                                                                                                 |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protokoll für OTLP-Exporter, gilt für alle Signale                                                                                                                                                                                                                                                                                                                  | `grpc`, `http/json`, `http/protobuf`                                                                                                      |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | OTLP-Collector-Endpunkt für alle Signale                                                                                                                                                                                                                                                                                                                            | `http://localhost:4317`                                                                                                                   |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protokoll für Metriken, überschreibt allgemeine Einstellung                                                                                                                                                                                                                                                                                                         | `grpc`, `http/json`, `http/protobuf`                                                                                                      |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | OTLP-Metriken-Endpunkt, überschreibt allgemeine Einstellung                                                                                                                                                                                                                                                                                                         | `http://localhost:4318/v1/metrics`                                                                                                        |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protokoll für Logs, überschreibt allgemeine Einstellung                                                                                                                                                                                                                                                                                                             | `grpc`, `http/json`, `http/protobuf`                                                                                                      |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | OTLP-Logs-Endpunkt, überschreibt allgemeine Einstellung                                                                                                                                                                                                                                                                                                             | `http://localhost:4318/v1/logs`                                                                                                           |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Authentifizierungsheader für OTLP                                                                                                                                                                                                                                                                                                                                   | `Authorization=Bearer token`                                                                                                              |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Exportintervall in Millisekunden (Standard: 60000)                                                                                                                                                                                                                                                                                                                  | `5000`, `60000`                                                                                                                           |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Logs-Exportintervall in Millisekunden (Standard: 5000)                                                                                                                                                                                                                                                                                                              | `1000`, `10000`                                                                                                                           |
| `OTEL_LOG_USER_PROMPTS`                             | Aktiviert die Protokollierung von Benutzer-Prompt-Inhalten (Standard: deaktiviert)                                                                                                                                                                                                                                                                                  | `1` zum Aktivieren                                                                                                                        |
| `OTEL_LOG_TOOL_DETAILS`                             | Aktiviert die Protokollierung von Tool-Parametern und Eingabeargumenten in Tool-Ereignissen und Trace-Span-Attributen: Bash-Befehle, MCP-Server- und Tool-Namen, Skill-Namen und Tool-Eingabe. Aktiviert auch benutzerdefinierte, Plugin- und MCP-Befehlsnamen bei `user_prompt`-Ereignissen (Standard: deaktiviert)                                                | `1` zum Aktivieren                                                                                                                        |
| `OTEL_LOG_TOOL_CONTENT`                             | Aktiviert die Protokollierung von Tool-Eingabe- und Ausgabeinhalten in Span-Ereignissen (Standard: deaktiviert). Erfordert [Tracing](#traces-beta). Der Inhalt wird bei 60 KB gekürzt                                                                                                                                                                               | `1` zum Aktivieren                                                                                                                        |
| `OTEL_LOG_RAW_API_BODIES`                           | Gibt die vollständige Anthropic Messages API-Anfrage und Antwort JSON als `api_request_body` / `api_response_body` Log-Ereignisse aus (Standard: deaktiviert). Texte enthalten die gesamte Konversationshistorie. Das Aktivieren impliziert Zustimmung zu allem, was `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS` und `OTEL_LOG_TOOL_CONTENT` offenbaren würden | `1` für Inline-Texte gekürzt bei 60 KB, oder `file:<dir>` für ungekürzte Texte auf der Festplatte mit einem `body_ref`-Zeiger im Ereignis |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Metriken-Temporalitätspräferenz (Standard: `delta`). Setzen Sie auf `cumulative`, wenn Ihr Backend kumulative Temporalität erwartet                                                                                                                                                                                                                                 | `delta`, `cumulative`                                                                                                                     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Intervall zum Aktualisieren dynamischer Header (Standard: 1740000ms / 29 Minuten)                                                                                                                                                                                                                                                                                   | `900000`                                                                                                                                  |

### mTLS-Authentifizierung

Wie Sie Client-Zertifikate für den OTLP-Exporter konfigurieren, hängt vom OTLP-Protokoll ab, das für dieses Signal verwendet wird, das über `OTEL_EXPORTER_OTLP_PROTOCOL` oder die Pro-Signal-Überschreibung gesetzt wird. Die gleiche Konfiguration gilt für Metriken, Logs und Traces.

| Protokoll                    | Client-Zertifikat-Variablen                                                                                                                                                                               | Vertrauen Sie dem Collector-CA mit |
| :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------- |
| `http/protobuf`, `http/json` | `CLAUDE_CODE_CLIENT_CERT`, `CLAUDE_CODE_CLIENT_KEY` und optional `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`. Siehe [Netzwerkkonfiguration](/de/network-config#mtls-authentication)                               | `NODE_EXTRA_CA_CERTS`              |
| `grpc`                       | `OTEL_EXPORTER_OTLP_CLIENT_KEY` und `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`, oder die Pro-Signal-Varianten wie `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`, um ein anderes Zertifikat pro Signal zu verwenden | `OTEL_EXPORTER_OTLP_CERTIFICATE`   |

Für `grpc` liest das OpenTelemetry SDK die Standard-OTLP-Variablen direkt, daher funktionieren bestehende Konfigurationen, die die Pro-Signal-Metriken-Variablen setzen, weiterhin.

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

Tracing ist standardmäßig deaktiviert. Um es zu aktivieren, setzen Sie sowohl `CLAUDE_CODE_ENABLE_TELEMETRY=1` als auch `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, und setzen Sie dann `OTEL_TRACES_EXPORTER`, um auszuwählen, wohin Spans gesendet werden. Traces verwenden die [allgemeine OTLP-Konfiguration](#allgemeine-konfigurationsvariablen) für Endpunkt, Protokoll, Header und [mTLS](#mtls-authentifizierung) erneut.

| Umgebungsvariable                     | Beschreibung                                                                                 | Beispielwerte                        |
| ------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Aktiviert Span-Tracing (erforderlich). `ENABLE_ENHANCED_TELEMETRY_BETA` wird auch akzeptiert | `1`                                  |
| `OTEL_TRACES_EXPORTER`                | Traces-Exporter-Typ(en), kommagetrennt. Verwenden Sie `none` zum Deaktivieren                | `console`, `otlp`, `none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | Protokoll für Traces, überschreibt `OTEL_EXPORTER_OTLP_PROTOCOL`                             | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | OTLP-Traces-Endpunkt, überschreibt `OTEL_EXPORTER_OTLP_ENDPOINT`                             | `http://localhost:4318/v1/traces`    |
| `OTEL_TRACES_EXPORT_INTERVAL`         | Span-Batch-Exportintervall in Millisekunden (Standard: 5000)                                 | `1000`, `10000`                      |

Spans schwärzen Benutzer-Prompt-Text, Tool-Eingabedetails und Tool-Inhalte standardmäßig. Setzen Sie `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1` und `OTEL_LOG_TOOL_CONTENT=1`, um sie einzubeziehen.

Wenn Tracing aktiv ist, erben Bash- und PowerShell-Subprozesse automatisch eine `TRACEPARENT`-Umgebungsvariable, die den W3C-Trace-Kontext des aktiven Tool-Ausführungs-Spans enthält. Dies ermöglicht jedem Subprozess, der `TRACEPARENT` liest, seine eigenen Spans unter demselben Trace zu verschachteln, was eine End-to-End-verteilte Tracing durch Skripte und Befehle ermöglicht, die Claude ausführt.

Wenn Tracing aktiv ist und Claude Code direkt mit der Anthropic API verbunden ist, trägt jede Modellanfrage einen W3C `traceparent` Header, der auf den Kontext des `claude_code.llm_request` Spans gesetzt ist, und der `traceresponse` Header der API wird als Span-Link aufgezeichnet. Zusammen verbinden diese Claude Code's clientseitige Spans mit dem serverseitigen Trace durch jeden konformen Vermittler. Der Header wird nicht an Drittanbieter gesendet.

In Agent SDK und nicht-interaktiven Sitzungen, die mit `-p` gestartet werden, liest Claude Code auch `TRACEPARENT` und `TRACESTATE` aus seiner eigenen Umgebung, wenn jeder Interaktions-Span gestartet wird. Dies ermöglicht einem Embedding-Prozess, seinen aktiven W3C-Trace-Kontext in den Subprozess zu übergeben, sodass Claude Code's Spans als untergeordnete Elemente des Aufrufers verteilter Trace erscheinen. Interaktive Sitzungen ignorieren eingehende `TRACEPARENT`, um zu vermeiden, dass versehentlich Umgebungswerte aus CI oder Container-Umgebungen geerbt werden.

#### Span-Hierarchie

Jeder Benutzer-Prompt startet einen `claude_code.interaction` Root-Span. API-Aufrufe, Tool-Aufrufe und Hook-Ausführungen werden als untergeordnete Elemente aufgezeichnet. Tool-Spans haben zwei untergeordnete Spans: einen für die Zeit, die auf eine Berechtigungsentscheidung gewartet wird, und einen für die Ausführung selbst. Wenn das Task-Tool einen Subagenten erzeugt, werden die API- und Tool-Spans des Subagenten unter dem `claude_code.tool`-Span des übergeordneten Elements verschachtelt.

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (erfordert detailliertes Beta-Tracing)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (Task-Tool) Subagent claude_code.llm_request / claude_code.tool Spans
```

In Agent SDK und `claude -p` Sitzungen wird `claude_code.interaction` selbst ein untergeordnetes Element des Aufrufers-Spans, wenn `TRACEPARENT` in der Umgebung gesetzt ist.

#### Span-Attribute

Jeder Span trägt die [Standardattribute](#standardattribute) plus ein `span.type`-Attribut, das seinem Namen entspricht. Die folgenden Tabellen listen die zusätzlichen Attribute auf, die auf jedem Span gesetzt sind. Die Spans `llm_request`, `tool.execution` und `hook` setzen OpenTelemetry-Status `ERROR`, wenn sie einen Fehler aufzeichnen; die anderen Spans enden immer mit Status `UNSET`.

**`claude_code.interaction`**

| Attribut                  | Beschreibung                                                              | Gated durch             |
| ------------------------- | ------------------------------------------------------------------------- | ----------------------- |
| `user_prompt`             | Prompt-Text. Der Wert ist `<REDACTED>`, es sei denn, das Gate ist gesetzt | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length`      | Prompt-Länge in Zeichen                                                   |                         |
| `interaction.sequence`    | 1-basierter Zähler von Interaktionen in dieser Sitzung                    |                         |
| `interaction.duration_ms` | Wanduhr-Dauer des Durchgangs                                              |                         |

**`claude_code.llm_request`**

| Attribut                         | Beschreibung                                                                                                               | Gated durch |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------- |
| `model`                          | Modellkennung                                                                                                              |             |
| `gen_ai.system`                  | Immer `anthropic`. OpenTelemetry GenAI semantische Konvention                                                              |             |
| `gen_ai.request.model`           | Gleicher Wert wie `model`. OpenTelemetry GenAI semantische Konvention                                                      |             |
| `query_source`                   | Subsystem, das die Anfrage gestellt hat, wie `repl_main_thread` oder ein Subagent-Name                                     |             |
| `agent_id`                       | Kennung des Subagenten oder Teamkollegen, der die Anfrage gestellt hat. Fehlt in der Hauptsitzung                          |             |
| `parent_agent_id`                | Kennung des Agenten, der diesen erzeugt hat. Fehlt für die Hauptsitzung und für Agenten, die direkt von ihr erzeugt wurden |             |
| `speed`                          | `fast` oder `normal`                                                                                                       |             |
| `llm_request.context`            | `interaction`, `tool` oder `standalone` je nach übergeordnetem Span                                                        |             |
| `duration_ms`                    | Wanduhr-Dauer einschließlich Wiederholungen                                                                                |             |
| `ttft_ms`                        | Zeit bis zum ersten Token in Millisekunden                                                                                 |             |
| `input_tokens`                   | Eingabe-Token-Anzahl aus dem API-Nutzungsblock                                                                             |             |
| `output_tokens`                  | Ausgabe-Token-Anzahl                                                                                                       |             |
| `cache_read_tokens`              | Aus dem Prompt-Cache gelesene Token                                                                                        |             |
| `cache_creation_tokens`          | In den Prompt-Cache geschriebene Token                                                                                     |             |
| `request_id`                     | Anthropic API-Anfrage-ID aus dem `request-id` Response-Header                                                              |             |
| `gen_ai.response.id`             | Gleicher Wert wie `request_id`. OpenTelemetry GenAI semantische Konvention                                                 |             |
| `client_request_id`              | Client-generierte `x-client-request-id` des letzten Versuchs                                                               |             |
| `attempt`                        | Gesamtzahl der Versuche für diese Anfrage                                                                                  |             |
| `success`                        | `true` oder `false`                                                                                                        |             |
| `status_code`                    | HTTP-Statuscode, wenn die Anfrage fehlgeschlagen ist                                                                       |             |
| `error`                          | Fehlermeldung, wenn die Anfrage fehlgeschlagen ist                                                                         |             |
| `response.has_tool_call`         | `true`, wenn die Antwort Tool-Use-Blöcke enthielt                                                                          |             |
| `stop_reason`                    | API-Antwort `stop_reason`, wie `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn` oder `refusal`          |             |
| `gen_ai.response.finish_reasons` | Gleicher Wert wie `stop_reason`, in einem String-Array verpackt. OpenTelemetry GenAI semantische Konvention                |             |

Jeder Wiederholungsversuch wird auch als `gen_ai.request.attempt` Span-Ereignis mit `attempt` und `client_request_id` Attributen aufgezeichnet.

**`claude_code.tool`**

| Attribut          | Beschreibung                                                                                                               | Gated durch             |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `tool_name`       | Tool-Name                                                                                                                  |                         |
| `duration_ms`     | Wanduhr-Dauer einschließlich Berechtigungswartung und Ausführung                                                           |                         |
| `result_tokens`   | Ungefähre Token-Größe des Tool-Ergebnisses                                                                                 |                         |
| `agent_id`        | Kennung des Subagenten oder Teamkollegen, der das Tool ausgeführt hat. Fehlt in der Hauptsitzung                           |                         |
| `parent_agent_id` | Kennung des Agenten, der diesen erzeugt hat. Fehlt für die Hauptsitzung und für Agenten, die direkt von ihr erzeugt wurden |                         |
| `file_path`       | Zieldateipfad für Read-, Edit- und Write-Tools                                                                             | `OTEL_LOG_TOOL_DETAILS` |
| `full_command`    | Befehlszeichenkette für das Bash-Tool                                                                                      | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name`      | Skill-Name für das Skill-Tool                                                                                              | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type`   | Subagent-Typ für das Task-Tool                                                                                             | `OTEL_LOG_TOOL_DETAILS` |

Wenn `OTEL_LOG_TOOL_CONTENT=1`, zeichnet dieser Span auch ein `tool.output` Span-Ereignis auf, dessen Attribute die Tool-Eingabe- und Ausgabetexte enthalten, gekürzt bei 60 KB pro Attribut.

**`claude_code.tool.blocked_on_user`**

| Attribut      | Beschreibung                                                                              | Gated durch |
| ------------- | ----------------------------------------------------------------------------------------- | ----------- |
| `duration_ms` | Zeit, die auf die Berechtigungsentscheidung gewartet wird                                 |             |
| `decision`    | `accept` oder `reject`                                                                    |             |
| `source`      | Entscheidungsquelle, entsprechend dem [Tool-Entscheidungs-Ereignis](#tool-decision-event) |             |

**`claude_code.tool.execution`**

| Attribut      | Beschreibung                                                                                                                                                                  | Gated durch             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `duration_ms` | Zeit, die für die Ausführung des Tool-Body aufgewendet wird                                                                                                                   |                         |
| `success`     | `true` oder `false`                                                                                                                                                           |                         |
| `error`       | Fehler-Kategoriezeichenkette, wenn die Ausführung fehlgeschlagen ist, wie `Error:ENOENT` oder `ShellError`. Enthält die vollständige Fehlermeldung, wenn das Gate gesetzt ist | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**

Dieser Span wird nur ausgegeben, wenn detailliertes Beta-Tracing aktiv ist, was `ENABLE_BETA_TRACING_DETAILED=1` und `BETA_TRACING_ENDPOINT` zusätzlich zur obigen Trace-Exporter-Konfiguration erfordert. In interaktiven CLI-Sitzungen erfordert dies auch, dass Ihre Organisation für die Funktion auf die Whitelist gesetzt ist. Agent SDK und nicht-interaktive `-p` Sitzungen sind nicht gated. Es wird nicht ausgegeben, wenn nur `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` gesetzt ist.

| Attribut                 | Beschreibung                                                            | Gated durch             |
| ------------------------ | ----------------------------------------------------------------------- | ----------------------- |
| `hook_event`             | Hook-Ereignistyp, wie `PreToolUse`                                      |                         |
| `hook_name`              | Vollständiger Hook-Name, wie `PreToolUse:Write`                         |                         |
| `num_hooks`              | Anzahl der ausgeführten übereinstimmenden Hook-Befehle                  |                         |
| `hook_definitions`       | JSON-serialisierte Hook-Konfiguration                                   | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms`            | Wanduhr-Dauer aller übereinstimmenden Hooks                             |                         |
| `num_success`            | Anzahl der Hooks, die erfolgreich abgeschlossen wurden                  |                         |
| `num_blocking`           | Anzahl der Hooks, die eine Blockierungsentscheidung zurückgegeben haben |                         |
| `num_non_blocking_error` | Anzahl der Hooks, die ohne Blockierung fehlgeschlagen sind              |                         |
| `num_cancelled`          | Anzahl der Hooks, die vor Abschluss abgebrochen wurden                  |                         |

<Note>
  Zusätzliche inhaltshaltige Attribute wie `new_context`, `system_prompt_preview`, `user_system_prompt`, `tool_input` und `response.model_output` werden nur ausgegeben, wenn detailliertes Beta-Tracing aktiv ist. Sie sind nicht Teil des stabilen Span-Schemas. `user_system_prompt` erfordert zusätzlich `OTEL_LOG_USER_PROMPTS=1`. Es trägt nur den System-Prompt-Text, den Sie über die `systemPrompt` SDK-Option oder die Flags `--system-prompt` und `--append-system-prompt` bereitstellen, gekürzt bei 60 KB, und wird einmal pro Sitzung statt pro Anfrage ausgegeben.
</Note>

### Dynamische Header

Für Unternehmensumgebungen, die eine dynamische Authentifizierung erfordern, können Sie ein Skript konfigurieren, um Header dynamisch zu generieren. Dynamische Header gelten nur für die Protokolle `http/protobuf` und `http/json`. Der `grpc` Exporter verwendet nur den statischen `OTEL_EXPORTER_OTLP_HEADERS` Wert.

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
* `start_type`: Wie die Sitzung gestartet wurde. Einer von `"fresh"`, `"resume"` oder `"continue"`

#### Codezeilen-Zähler

Wird erhöht, wenn Code hinzugefügt oder entfernt wird.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `type`: (`"added"`, `"removed"`)

#### Pull-Request-Zähler

Wird erhöht, wenn Claude Code einen Pull Request oder Merge Request über einen Shell-Befehl oder ein MCP-Tool erstellt.

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
* `query_source`: Kategorie des Subsystems, das die Anfrage gestellt hat. Einer von `"main"`, `"subagent"` oder `"auxiliary"`
* `speed`: `"fast"`, wenn die Anfrage den schnellen Modus verwendet hat. Andernfalls nicht vorhanden
* `effort`: [Anstrengungsstufe](/de/model-config#adjust-effort-level), die auf die Anfrage angewendet wird: `"low"`, `"medium"`, `"high"`, `"xhigh"` oder `"max"`. Nicht vorhanden, wenn das Modell Anstrengung nicht unterstützt.
* `agent.name`: Subagent-Typ, der die Anfrage gestellt hat. Integrierte Agent-Namen und Agents aus offiziellen Marketplace-Plugins werden wörtlich angezeigt. Andere benutzerdefinierte Agent-Namen werden durch `"custom"` ersetzt. Nicht vorhanden, wenn die Anfrage nicht von einem benannten Subagent-Typ gestellt wurde.
* `skill.name`: Skill, der für die Anfrage aktiv ist, gesetzt durch das Skill-Tool, einen `/` Befehl oder geerbt von einem erzeugten Subagent. Integrierte, gebündelte, benutzerdefinierte und offizielle Marketplace-Plugin-Skill-Namen werden wörtlich angezeigt. Drittanbieter-Plugin-Skill-Namen werden durch `"third-party"` ersetzt. Nicht vorhanden, wenn kein Skill aktiv ist.
* `plugin.name`: Besitzendes Plugin, wenn der aktive Skill oder Subagent von einem Plugin bereitgestellt wird. Offizielle Marketplace-Plugin-Namen werden wörtlich angezeigt. Drittanbieter-Plugin-Namen werden durch `"third-party"` ersetzt. Nicht vorhanden, wenn weder der Skill noch der Subagent ein besitzendes Plugin hat.
* `marketplace.name`: Marketplace, von dem das besitzende Plugin installiert wurde. Nur für offizielle Marketplace-Plugins ausgegeben. Andernfalls nicht vorhanden.

#### Token-Zähler

Wird nach jeder API-Anfrage erhöht.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Modellkennung (zum Beispiel "claude-sonnet-4-6")
* `query_source`: Kategorie des Subsystems, das die Anfrage gestellt hat. Einer von `"main"`, `"subagent"` oder `"auxiliary"`
* `speed`: `"fast"`, wenn die Anfrage den schnellen Modus verwendet hat. Andernfalls nicht vorhanden
* `effort`: [Anstrengungsstufe](/de/model-config#adjust-effort-level), die auf die Anfrage angewendet wird. Siehe [Kostenzähler](#kostenzähler) für Details.
* `agent.name`, `skill.name`, `plugin.name`, `marketplace.name`: Skill-, Plugin- und Agent-Zuordnung für die Anfrage. Siehe [Kostenzähler](#kostenzähler) für Definitionen und Schwärzungsverhalten.

#### Code-Edit-Tool-Entscheidungszähler

Wird erhöht, wenn der Benutzer die Verwendung des Edit-, Write- oder NotebookEdit-Tools akzeptiert oder ablehnt.

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `tool_name`: Tool-Name (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Benutzerentscheidung (`"accept"`, `"reject"`)
* `source`: Entscheidungsquelle. Einer von `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` oder `"user_reject"`. Siehe das [Tool-Entscheidungs-Ereignis](#tool-decision-event) für die Bedeutung jedes Wertes.
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
* `command_name`: Befehlsname, wenn der Prompt einen aufruft. Integrierte und gebündelte Befehlsnamen wie `compact` oder `debug` werden wie geschrieben ausgegeben; Aliase wie `reset` werden wie eingegeben ausgegeben, nicht der kanonische Name. Benutzerdefinierte, Plugin- und MCP-Befehlsnamen werden zu `custom` oder `mcp` zusammengefasst, es sei denn, `OTEL_LOG_TOOL_DETAILS=1` ist gesetzt
* `command_source`: Ursprung des Befehls, wenn vorhanden: `builtin`, `custom` oder `mcp`. Von Plugins bereitgestellte Befehle werden als `custom` gemeldet

#### Tool-Ergebnis-Ereignis

Protokolliert, wenn ein Tool die Ausführung abgeschlossen hat.

**Ereignisname**: `claude_code.tool_result`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"tool_result"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `tool_name`: Name des Tools
* `tool_use_id`: Eindeutige Kennung für diese Tool-Invokation. Entspricht der `tool_use_id`, die an Hooks übergeben wird, und ermöglicht die Korrelation zwischen OTel-Ereignissen und Hook-erfassten Daten.
* `success`: `"true"` oder `"false"`
* `duration_ms`: Ausführungszeit in Millisekunden
* `error_type`: Fehler-Kategoriezeichenkette, wenn das Tool fehlgeschlagen ist, wie `"Error:ENOENT"` oder `"ShellError"`
* `error` (wenn `OTEL_LOG_TOOL_DETAILS=1`): Vollständige Fehlermeldung, wenn das Tool fehlgeschlagen ist
* `decision_type`: Entweder `"accept"` oder `"reject"`
* `decision_source`: Entscheidungsquelle. Einer von `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` oder `"user_reject"`. Siehe das [Tool-Entscheidungs-Ereignis](#tool-decision-event) für die Bedeutung jedes Wertes.
* `tool_input_size_bytes`: Größe der JSON-serialisierten Tool-Eingabe in Bytes
* `tool_result_size_bytes`: Größe des Tool-Ergebnisses in Bytes
* `mcp_server_scope`: MCP-Server-Scope-Kennung (für MCP-Tools)
* `tool_parameters` (wenn `OTEL_LOG_TOOL_DETAILS=1`): JSON-Zeichenkette mit Tool-spezifischen Parametern:
  * Für Bash-Tool: enthält `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox` und `git_commit_id` (der Commit-SHA, wenn ein `git commit`-Befehl erfolgreich ist)
  * Für MCP-Tools: enthält `mcp_server_name`, `mcp_tool_name`
  * Für Skill-Tool: enthält `skill_name`
  * Für Task-Tool: enthält `subagent_type`
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
* `request_id`: Anthropic API-Anfrage-ID aus dem Response-Header `request-id`, wie `"req_011..."`. Nur vorhanden, wenn die API eine zurückgibt.
* `speed`: `"fast"` oder `"normal"`, was angibt, ob der schnelle Modus aktiv war
* `query_source`: Subsystem, das die Anfrage gestellt hat, wie `"repl_main_thread"`, `"compact"` oder ein Subagent-Name
* `effort`: [Anstrengungsstufe](/de/model-config#adjust-effort-level), die auf die Anfrage angewendet wird: `"low"`, `"medium"`, `"high"`, `"xhigh"` oder `"max"`. Nicht vorhanden, wenn das Modell Anstrengung nicht unterstützt.

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
* `status_code`: HTTP-Statuscode als Zahl. Nicht vorhanden für Nicht-HTTP-Fehler wie Verbindungsfehler.
* `duration_ms`: Anfragedauer in Millisekunden
* `attempt`: Gesamtzahl der Versuche, einschließlich der ursprünglichen Anfrage (`1` bedeutet, dass keine Wiederholungen aufgetreten sind)
* `request_id`: Anthropic API-Anfrage-ID aus dem Response-Header `request-id`, wie `"req_011..."`. Nur vorhanden, wenn die API eine zurückgibt.
* `speed`: `"fast"` oder `"normal"`, was angibt, ob der schnelle Modus aktiv war
* `query_source`: Subsystem, das die Anfrage gestellt hat, wie `"repl_main_thread"`, `"compact"` oder ein Subagent-Name
* `effort`: [Anstrengungsstufe](/de/model-config#adjust-effort-level), die auf die Anfrage angewendet wird. Nicht vorhanden, wenn das Modell Anstrengung nicht unterstützt.

#### API-Anfrage-Text-Ereignis

Protokolliert für jeden API-Anfrage-Versuch, wenn `OTEL_LOG_RAW_API_BODIES` gesetzt ist. Ein Ereignis wird pro Versuch ausgegeben, daher erzeugen Wiederholungen mit angepassten Parametern jeweils ihr eigenes Ereignis.

**Ereignisname**: `claude_code.api_request_body`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"api_request_body"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `body`: JSON-serialisierte Messages API-Anfrageparameter (Systemprompt, Nachrichten, Tools usw.), gekürzt bei 60 KB. Extended-Thinking-Inhalte in vorherigen Assistent-Durchgängen werden geschwärzt. Nur im Inline-Modus ausgegeben (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Absoluter Pfad zu einer `<dir>/<uuid>.request.json` Datei, die den ungekürzte Text enthält. Nur im Datei-Modus ausgegeben (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Ungekürzte Text-Länge. UTF-8-Bytes, wenn `OTEL_LOG_RAW_API_BODIES=file:<dir>`, oder UTF-16-Code-Einheiten, wenn `=1`
* `body_truncated`: `"true"`, wenn Inline-Kürzung aufgetreten ist. Nicht vorhanden im Datei-Modus und wenn keine Kürzung aufgetreten ist.
* `model`: Modellkennung aus den Anfrageparametern
* `query_source`: Subsystem, das die Anfrage gestellt hat (zum Beispiel `"compact"`)

#### API-Antwort-Text-Ereignis

Protokolliert für jede erfolgreiche API-Antwort, wenn `OTEL_LOG_RAW_API_BODIES` gesetzt ist.

**Ereignisname**: `claude_code.api_response_body`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"api_response_body"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `body`: JSON-serialisierte Messages API-Antwort (id, Inhaltsblöcke, Nutzung, Stoppgrund), gekürzt bei 60 KB. Extended-Thinking-Inhalte werden geschwärzt. Nur im Inline-Modus ausgegeben (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Absoluter Pfad zu einer `<dir>/<request_id>.response.json` Datei, die den ungekürzte Text enthält. Nur im Datei-Modus ausgegeben (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Ungekürzte Text-Länge. UTF-8-Bytes, wenn `OTEL_LOG_RAW_API_BODIES=file:<dir>`, oder UTF-16-Code-Einheiten, wenn `=1`
* `body_truncated`: `"true"`, wenn Inline-Kürzung aufgetreten ist. Nicht vorhanden im Datei-Modus und wenn keine Kürzung aufgetreten ist.
* `model`: Modellkennung
* `query_source`: Subsystem, das die Anfrage gestellt hat
* `request_id`: Anthropic API-Anfrage-ID aus dem Response-Header `request-id`, wie `"req_011..."`. Nur vorhanden, wenn die API eine zurückgibt.

#### Tool-Entscheidungs-Ereignis

Protokolliert, wenn eine Tool-Berechtigungsentscheidung getroffen wird (akzeptieren/ablehnen).

**Ereignisname**: `claude_code.tool_decision`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"tool_decision"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `tool_name`: Name des Tools (zum Beispiel "Read", "Edit", "Write", "NotebookEdit")
* `tool_use_id`: Eindeutige Kennung für diese Tool-Invokation. Entspricht der `tool_use_id`, die an Hooks übergeben wird, und ermöglicht die Korrelation zwischen OTel-Ereignissen und Hook-erfassten Daten.
* `decision`: Entweder `"accept"` oder `"reject"`
* `source`: Entscheidungsquelle:
  * `"config"`: Automatisch entschieden, ohne Aufforderung, basierend auf Projekteinstellungen, Zulassungsregeln in den persönlichen Einstellungen des Benutzers, verwalteter Unternehmensrichtlinie, `--allowedTools` oder `--disallowedTools` Flags, dem aktiven Berechtigungsmodus, einer sitzungsbegrenzten Zulassung aus einem früheren Prompt in der gleichen interaktiven CLI-Sitzung oder weil das Tool inhärent sicher ist. Das Ereignis gibt nicht an, welche dieser Quellen übereinstimmte.
  * `"hook"`: Ein `PreToolUse` oder `PermissionRequest` Hook hat die Entscheidung zurückgegeben.
  * `"user_permanent"`: Wird ausgegeben, wenn der Benutzer "Ja, und nicht mehr fragen für ..." bei einer Berechtigungsaufforderung wählte, was eine Zulassungsregel in seinen persönlichen Einstellungen speichert. In der interaktiven CLI wird dies nur für diese Wahl selbst ausgegeben; spätere Aufrufe, die der gespeicherten Regel entsprechen, geben stattdessen `"config"` aus. In Agent SDK oder nicht-interaktiven `-p` Sitzungen geben sowohl die ursprüngliche Wahl als auch spätere Regelübereinstimmungen `"user_permanent"` aus. Wird als Akzeptanz behandelt.
  * `"user_temporary"`: Wird ausgegeben, wenn der Benutzer "Ja" bei einer Berechtigungsaufforderung wählte, oder eine der Optionen "... während dieser Sitzung" bei einer Dateibearbeitungs- oder Leseanforderung wählte. In der interaktiven CLI wird dies nur für die Wahl selbst ausgegeben; spätere Aufrufe, die durch diese sitzungsbegrenzte Zulassung zulässig sind, geben stattdessen `"config"` aus. In Agent SDK oder nicht-interaktiven `-p` Sitzungen geben sowohl die Wahl als auch spätere Übereinstimmungen `"user_temporary"` aus. Wird als Akzeptanz behandelt.
  * `"user_abort"`: Wird ausgegeben, wenn der Benutzer die Berechtigungsaufforderung geschlossen hat, ohne zu antworten. Wird als Ablehnung behandelt.
  * `"user_reject"`: Wird ausgegeben, wenn der Benutzer "Nein" wählte, wenn aufgefordert, oder ein Aufruf einer Ablehnungsregel in seinen persönlichen Einstellungen entsprach. Wird als Ablehnung behandelt.

#### Berechtigungsmodus-Änderungs-Ereignis

Protokolliert, wenn sich der Berechtigungsmodus ändert, zum Beispiel durch Shift+Tab-Zyklus, Beendigung des Plan-Modus oder eine Auto-Modus-Gate-Prüfung.

**Ereignisname**: `claude_code.permission_mode_changed`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"permission_mode_changed"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `from_mode`: Der vorherige Berechtigungsmodus, zum Beispiel `"default"`, `"plan"`, `"acceptEdits"`, `"auto"` oder `"bypassPermissions"`
* `to_mode`: Der neue Berechtigungsmodus
* `trigger`: Was die Änderung verursacht hat. Einer von `"shift_tab"`, `"exit_plan_mode"`, `"auto_gate_denied"` oder `"auto_opt_in"`. Nicht vorhanden, wenn der Übergang vom SDK oder Bridge stammt

#### Auth-Ereignis

Protokolliert, wenn `/login` oder `/logout` abgeschlossen ist.

**Ereignisname**: `claude_code.auth`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"auth"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `action`: `"login"` oder `"logout"`
* `success`: `"true"` oder `"false"`
* `auth_method`: Authentifizierungsmethode, wie `"oauth"`
* `error_category`: Kategorische Fehlerart, wenn die Aktion fehlgeschlagen ist. Die rohe Fehlermeldung ist nie enthalten
* `status_code`: HTTP-Statuscode als Zeichenkette, wenn die Aktion mit einem HTTP-Fehler fehlgeschlagen ist

#### MCP-Server-Verbindungs-Ereignis

Protokolliert, wenn ein MCP-Server verbunden wird, getrennt wird oder keine Verbindung herstellen kann.

**Ereignisname**: `claude_code.mcp_server_connection`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"mcp_server_connection"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `status`: `"connected"`, `"failed"` oder `"disconnected"`
* `transport_type`: Server-Transport, wie `"stdio"`, `"sse"` oder `"http"`
* `server_scope`: Bereich, in dem der Server konfiguriert ist, wie `"user"`, `"project"` oder `"local"`
* `duration_ms`: Verbindungsversuch-Dauer in Millisekunden
* `error_code`: Fehlercode, wenn die Verbindung fehlgeschlagen ist
* `server_name` (wenn `OTEL_LOG_TOOL_DETAILS=1`): Konfigurierter Server-Name
* `error` (wenn `OTEL_LOG_TOOL_DETAILS=1`): Vollständige Fehlermeldung, wenn die Verbindung fehlgeschlagen ist

#### Interner Fehler-Ereignis

Protokolliert, wenn Claude Code einen unerwarteten internen Fehler abfängt. Nur der Fehlerklassenname und ein errno-ähnlicher Code werden aufgezeichnet. Die Fehlermeldung und Stack-Trace sind nie enthalten. Dieses Ereignis wird nicht ausgegeben, wenn gegen Bedrock, Vertex oder Foundry ausgeführt wird, oder wenn `DISABLE_ERROR_REPORTING` gesetzt ist.

**Ereignisname**: `claude_code.internal_error`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"internal_error"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `error_name`: Fehlerklassenname, wie `"TypeError"` oder `"SyntaxError"`
* `error_code`: Node.js errno-Code wie `"ENOENT"`, wenn auf dem Fehler vorhanden

#### Plugin-Installiert-Ereignis

Protokolliert, wenn ein Plugin die Installation abgeschlossen hat, sowohl vom `claude plugin install` CLI-Befehl als auch von der interaktiven `/plugin` UI.

**Ereignisname**: `claude_code.plugin_installed`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"plugin_installed"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `marketplace.is_official`: `"true"`, wenn der Marketplace ein offizieller Anthropic-Marketplace ist, `"false"` andernfalls
* `install.trigger`: `"cli"` oder `"ui"`
* `plugin.name`: Name des installierten Plugins. Für Drittanbieter-Marketplaces ist dies nur enthalten, wenn `OTEL_LOG_TOOL_DETAILS=1`
* `plugin.version`: Plugin-Version, wenn in der Marketplace-Eintrag deklariert. Für Drittanbieter-Marketplaces ist dies nur enthalten, wenn `OTEL_LOG_TOOL_DETAILS=1`
* `marketplace.name`: Marketplace, von dem das Plugin installiert wurde. Für Drittanbieter-Marketplaces ist dies nur enthalten, wenn `OTEL_LOG_TOOL_DETAILS=1`

#### Plugin-Geladen-Ereignis

Protokolliert einmal pro aktiviertem Plugin beim Sitzungsstart. Verwenden Sie dieses Ereignis, um zu inventarisieren, welche Plugins über Ihre gesamte Flotte hinweg aktiv sind, als Ergänzung zu `plugin_installed`, das die Installationsaktion selbst aufzeichnet.

**Ereignisname**: `claude_code.plugin_loaded`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"plugin_loaded"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `plugin.name`: Name des Plugins. Für Plugins außerhalb des offiziellen Marketplace und des integrierten Bundles ist der Wert `"third-party"`, es sei denn, `OTEL_LOG_TOOL_DETAILS=1`
* `marketplace.name`: Marketplace, von dem das Plugin installiert wurde, wenn bekannt. Auf `"third-party"` unter der gleichen Bedingung wie `plugin.name` geschwärzt
* `plugin.version`: Version aus dem Plugin-Manifest. Nur enthalten, wenn der Name nicht geschwärzt ist und das Manifest eine Version deklariert
* `plugin.scope`: Herkunftskategorie für das Plugin: `"official"`, `"org"`, `"user-local"` oder `"default-bundle"`
* `enabled_via`: Wie das Plugin aktiviert wurde: `"default-enable"`, `"org-policy"`, `"seed-mount"` oder `"user-install"`
* `plugin_id_hash`: Deterministische Hash des Plugin-Namens und des Marketplace, nur an Ihren konfigurierten Exporter gesendet. Ermöglicht es Ihnen, zu zählen, wie viele unterschiedliche Drittanbieter-Plugins über Ihre gesamte Flotte hinweg geladen sind, ohne ihre Namen aufzuzeichnen
* `has_hooks`: Ob das Plugin Hooks beiträgt
* `has_mcp`: Ob das Plugin MCP-Server beiträgt
* `skill_path_count`: Anzahl der Skill-Verzeichnisse, die das Plugin deklariert
* `command_path_count`: Anzahl der Befehlsverzeichnisse, die das Plugin deklariert
* `agent_path_count`: Anzahl der Agent-Verzeichnisse, die das Plugin deklariert

#### Skill-Aktiviert-Ereignis

Protokolliert, wenn ein Skill aufgerufen wird, ob Claude ihn über das Skill-Tool aufruft oder Sie ihn als `/` Befehl ausführen.

**Ereignisname**: `claude_code.skill_activated`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"skill_activated"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `skill.name`: Name des Skills. Für benutzerdefinierte und Drittanbieter-Plugin-Skills ist der Wert der Platzhalter `"custom_skill"`, es sei denn, `OTEL_LOG_TOOL_DETAILS=1`
* `invocation_trigger`: Wie der Skill ausgelöst wurde (`"user-slash"`, `"claude-proactive"` oder `"nested-skill"`)
* `skill.source`: Wo der Skill geladen wurde (zum Beispiel `"bundled"`, `"userSettings"`, `"projectSettings"`, `"plugin"`)
* `plugin.name` (wenn `OTEL_LOG_TOOL_DETAILS=1` oder das Plugin ist von einem offiziellen Marketplace): Name des besitzenden Plugins, wenn der Skill von einem Plugin bereitgestellt wird
* `marketplace.name` (wenn `OTEL_LOG_TOOL_DETAILS=1` oder das Plugin ist von einem offiziellen Marketplace): Marketplace des besitzenden Plugins, wenn der Skill von einem Plugin bereitgestellt wird

#### At-Mention-Ereignis

Protokolliert, wenn Claude Code ein `@`-Mention in einem Prompt auflöst. Nicht jedes Mention gibt ein Ereignis aus: Early-Exit-Pfade wie Berechtigungsverweigerungen, übergroße Dateien, PDF-Referenz-Anhänge und Fehler beim Auflisten von Verzeichnissen werden zurückgegeben, ohne zu protokollieren.

**Ereignisname**: `claude_code.at_mention`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"at_mention"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `mention_type`: Typ des Mentions (`"file"`, `"directory"`, `"agent"`, `"mcp_resource"`)
* `success`: Ob das Mention erfolgreich aufgelöst wurde (`"true"` oder `"false"`)

#### API-Wiederholungen-Erschöpft-Ereignis

Protokolliert einmal, wenn eine API-Anfrage nach mehr als einem Versuch fehlschlägt. Wird zusammen mit dem letzten `api_error` Ereignis ausgegeben.

**Ereignisname**: `claude_code.api_retries_exhausted`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"api_retries_exhausted"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `model`: Verwendetes Modell
* `error`: Letzte Fehlermeldung
* `status_code`: HTTP-Statuscode als Zahl. Nicht vorhanden für Nicht-HTTP-Fehler.
* `total_attempts`: Gesamtzahl der Versuche
* `total_retry_duration_ms`: Gesamte Wanduhr-Zeit über alle Versuche
* `speed`: `"fast"` oder `"normal"`

#### Hook-Registriert-Ereignis

Protokolliert einmal pro konfiguriertem Hook beim Sitzungsstart. Verwenden Sie dieses Ereignis, um zu inventarisieren, welche Hooks über Ihre gesamte Flotte hinweg aktiv sind, als Ergänzung zu den Pro-Ausführungs-Ereignissen `hook_execution_start` und `hook_execution_complete`.

**Ereignisname**: `claude_code.hook_registered`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"hook_registered"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `hook_event`: Hook-Ereignistyp, wie `"PreToolUse"` oder `"PostToolUse"`
* `hook_type`: Hook-Implementierungstyp: `"command"`, `"prompt"`, `"mcp_tool"`, `"http"` oder `"agent"`
* `hook_source`: Wo der Hook definiert ist: `"userSettings"`, `"projectSettings"`, `"localSettings"`, `"flagSettings"`, `"policySettings"` oder `"pluginHook"`
* `hook_matcher` (wenn `OTEL_LOG_TOOL_DETAILS=1`): Die Matcher-Zeichenkette aus der Hook-Konfiguration, wenn eine gesetzt ist
* `plugin.name` (wenn `hook_source` `"pluginHook"` ist): Name des beitragenden Plugins. Für Plugins außerhalb des offiziellen Marketplace und des integrierten Bundles ist der Wert `"third-party"`, es sei denn, `OTEL_LOG_TOOL_DETAILS=1`
* `plugin_id_hash` (wenn `hook_source` `"pluginHook"` ist): Deterministische Hash des Plugin-Namens und des Marketplace, nur an Ihren konfigurierten Exporter gesendet. Ermöglicht es Ihnen, unterschiedliche beitragende Plugins zu zählen, ohne ihre Namen aufzuzeichnen

#### Hook-Ausführungs-Start-Ereignis

Protokolliert, wenn ein oder mehrere Hooks für ein Hook-Ereignis beginnen auszuführen.

**Ereignisname**: `claude_code.hook_execution_start`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"hook_execution_start"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `hook_event`: Hook-Ereignistyp, wie `"PreToolUse"` oder `"PostToolUse"`
* `hook_name`: Vollständiger Hook-Name einschließlich Matcher, wie `"PreToolUse:Write"`
* `num_hooks`: Anzahl der übereinstimmenden Hook-Befehle
* `managed_only`: `"true"`, wenn nur verwaltete Richtlinien-Hooks zulässig sind
* `hook_source`: `"policySettings"` oder `"merged"`
* `hook_definitions`: JSON-serialisierte Hook-Konfiguration. Nur enthalten, wenn sowohl detailliertes Beta-Tracing als auch `OTEL_LOG_TOOL_DETAILS=1` aktiviert sind

#### Hook-Ausführungs-Abschluss-Ereignis

Protokolliert, wenn alle Hooks für ein Hook-Ereignis abgeschlossen sind.

**Ereignisname**: `claude_code.hook_execution_complete`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"hook_execution_complete"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `hook_event`: Hook-Ereignistyp
* `hook_name`: Vollständiger Hook-Name einschließlich Matcher
* `num_hooks`: Anzahl der übereinstimmenden Hook-Befehle
* `num_success`: Anzahl, die erfolgreich abgeschlossen wurde
* `num_blocking`: Anzahl, die eine Blockierungsentscheidung zurückgegeben hat
* `num_non_blocking_error`: Anzahl, die ohne Blockierung fehlgeschlagen ist
* `num_cancelled`: Anzahl, die vor Abschluss abgebrochen wurde
* `total_duration_ms`: Wanduhr-Dauer aller übereinstimmenden Hooks
* `managed_only`: `"true"`, wenn nur verwaltete Richtlinien-Hooks zulässig sind
* `hook_source`: `"policySettings"` oder `"merged"`
* `hook_definitions`: JSON-serialisierte Hook-Konfiguration. Nur enthalten, wenn sowohl detailliertes Beta-Tracing als auch `OTEL_LOG_TOOL_DETAILS=1` aktiviert sind

#### Hook-Plugin-Metriken-Ereignis

Protokolliert, wenn ein offizieller Marketplace-Plugin-Hook Pro-Invokations-Metriken ausgibt. Nur Plugins, die von einem offiziellen Anthropic-Marketplace installiert wurden, können diese ausgeben. Drittanbieter-Marketplace-Plugins und benutzerdefinierte Hooks geben nicht zu diesem Ereignis aus. Verwenden Sie dieses Ereignis, um Plugin-Verhalten wie Findungsraten, Kosten und Dauern aus Ihrem eigenen Observability-Stack zu überwachen.

**Ereignisname**: `claude_code.hook_plugin_metrics`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"hook_plugin_metrics"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `plugin_id`: Plugin-Kennung in `<name>@<marketplace>` Form
* `hook_event`: Hook-Ereignistyp, der die Metriken ausgegeben hat
* Bis zu 20 Plugin-ausgegebene Metrik-Schlüssel. Namen entsprechen `^[a-z][a-z0-9_]{0,39}$`. Werte sind boolescher Wert oder Zahl.

#### Kompaktierungs-Ereignis

Protokolliert, wenn die Konversationskompaktierung abgeschlossen ist.

**Ereignisname**: `claude_code.compaction`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"compaction"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `trigger`: `"auto"` oder `"manual"`
* `success`: `"true"` oder `"false"`
* `duration_ms`: Kompaktierungs-Dauer
* `pre_tokens`: Ungefähre Token-Anzahl vor Kompaktierung
* `post_tokens`: Ungefähre Token-Anzahl nach Kompaktierung
* `error`: Fehlermeldung, wenn Kompaktierung fehlgeschlagen ist

#### Feedback-Umfrage-Ereignis

Protokolliert, wenn eine Sitzungsqualitäts-Umfrage angezeigt oder beantwortet wird. Siehe [Sitzungsqualitäts-Umfragen](/de/data-usage#session-quality-surveys) für das, was die Umfragen erfassen und wie Sie sie steuern.

**Ereignisname**: `claude_code.feedback_survey`

**Attribute**:

* Alle [Standardattribute](#standardattribute)
* `event.name`: `"feedback_survey"`
* `event.timestamp`: ISO 8601-Zeitstempel
* `event.sequence`: monoton steigende Zähler zur Sortierung von Ereignissen innerhalb einer Sitzung
* `event_type`: Umfrage-Lebenszyklusereignis, zum Beispiel `"appeared"`, `"responded"` oder `"transcript_prompt_appeared"`
* `appearance_id`: Eindeutige ID, die die Ereignisse verknüpft, die für eine Umfrage-Instanz ausgegeben werden
* `survey_type`: Welche Umfrage das Ereignis erzeugt hat. `"session"` ist die Aufforderung "Wie macht sich Claude?" Bewertung
* `response`: Die Auswahl des Benutzers bei `responded` Ereignissen
* `enabled_via_override`: `true`, wenn [`CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`](/de/env-vars) gesetzt ist. Wird als boolescher Wert ausgegeben, nicht als Zeichenkette. Vorhanden bei `session` Umfrage-Ereignissen. Filtern Sie nach diesem Attribut, um zu bestätigen, dass die Überschreibung über eine Flotte angewendet wird

## Interpretation von Metriken- und Ereignisdaten

Die exportierten Metriken und Ereignisse unterstützen eine Reihe von Analysen:

### Nutzungsüberwachung

| Metrik                                                        | Analysemöglichkeit                                                                                                |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `claude_code.token.usage`                                     | Aufschlüsselung nach `type` (input/output), Benutzer, Team, Modell, `skill.name`, `plugin.name` oder `agent.name` |
| `claude_code.session.count`                                   | Verfolgung der Akzeptanz und des Engagements im Laufe der Zeit                                                    |
| `claude_code.lines_of_code.count`                             | Messung der Produktivität durch Verfolgung von Code-Hinzufügungen/Entfernungen                                    |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Verständnis der Auswirkungen auf Entwicklungs-Workflows                                                           |

### Kostenüberwachung

Die Metrik `claude_code.cost.usage` hilft bei:

* Verfolgung von Nutzungstrends über Teams oder Einzelpersonen hinweg
* Identifikation von Sitzungen mit hoher Nutzung zur Optimierung
* Zuordnung von Ausgaben zu spezifischen Skills, Plugins oder Subagent-Typen über die Attribute `skill.name`, `plugin.name` und `agent.name`

<Note>
  Kostenmetriken sind Näherungswerte. Für offizielle Abrechnungsdaten konsultieren Sie Ihren API-Anbieter (Claude Console, Amazon Bedrock oder Google Cloud Vertex).
</Note>

### Warnungen und Segmentierung

Häufige Warnungen, die Sie in Betracht ziehen sollten:

* Kostensteigerungen
* Ungewöhnlicher Token-Verbrauch
* Hohes Sitzungsvolumen von bestimmten Benutzern

Alle Metriken können nach `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model` und `app.version` segmentiert werden.

### Wiederholungserschöpfung erkennen

Claude Code wiederholt fehlgeschlagene API-Anfragen intern und gibt nur nach dem Aufgeben ein einzelnes `claude_code.api_error` Ereignis aus, daher ist das Ereignis selbst das Endsignal für diese Anfrage. Zwischenzeitliche Wiederholungsversuche werden nicht als separate Ereignisse protokolliert.

Das Attribut `attempt` auf dem Ereignis zeichnet auf, wie viele Versuche insgesamt unternommen wurden. Ein Wert größer als `CLAUDE_CODE_MAX_RETRIES` (Standard `10`) zeigt an, dass die Anfrage alle Wiederholungen bei einem vorübergehenden Fehler erschöpft hat. Ein niedrigerer Wert zeigt einen nicht wiederholbaren Fehler wie eine `400` Antwort an.

Um eine Sitzung zu unterscheiden, die sich von einer, die steckengeblieben ist, erholt hat, gruppieren Sie Ereignisse nach `session.id` und prüfen Sie, ob ein späteres `api_request` Ereignis nach dem Fehler vorhanden ist.

### Ereignisanalyse

Die Ereignisdaten bieten detaillierte Einblicke in Claude Code-Interaktionen:

**Tool-Nutzungsmuster**: Analysieren Sie Tool-Ergebnis-Ereignisse, um zu identifizieren:

* Am häufigsten verwendete Tools
* Tool-Erfolgsquoten
* Durchschnittliche Tool-Ausführungszeiten
* Fehlermuster nach Tool-Typ

**Leistungsüberwachung**: Verfolgen Sie API-Anfrage-Dauern und Tool-Ausführungszeiten, um Leistungsengpässe zu identifizieren.

## Audit-Sicherheitsereignisse

OpenTelemetry-Ereignisse sind die Audit-Datenquelle für Claude Code-Aktivität. Jedes Ereignis trägt Identitätsattribute, die Tool-Aufrufe, MCP-Aktivität und Berechtigungsentscheidungen an den Benutzer zurückbinden, der sie ausgelöst hat, und der OTLP-Logs-Exporter kann diese Ereignisse an jede Security Information and Event Management (SIEM)-Plattform mit einem OTLP-Receiver oder an einen OpenTelemetry Collector liefern, der an Ihr SIEM weiterleitet.

### Attribut-Aktionen an Benutzer

Die [Standardattribute](#standardattribute) auf jedem Ereignis enthalten die Identität des authentifizierten Benutzers: `user.email`, `user.account_uuid`, `user.account_id` und `organization.id`, wenn mit einem Claude-Konto angemeldet, plus die installationsbegrenzte `user.id` und die pro-Sitzung `session.id`.

MCP-Tool-Aufrufe, Bash-Befehle und Dateibearbeitungen werden daher dem Entwickler zugeordnet, der die Sitzung gestartet hat. Claude Code handelt nicht unter einem separaten Service-Konto; die Identität, die auf jedem Ereignis aufgezeichnet wird, ist das Claude-Konto des Entwicklers selbst.

Wenn Claude Code sich mit einem direkten API-Schlüssel authentifiziert oder gegen Bedrock, Vertex AI oder Microsoft Foundry, gibt es kein Claude-Konto in der Sitzung und nur `user.id` und `session.id` werden gefüllt. In diesen Bereitstellungen fügen Sie die Benutzeridentität selbst mit `OTEL_RESOURCE_ATTRIBUTES` hinzu, die pro Benutzer über die [verwaltete Einstellungsdatei](#administratorkonfiguration) oder einen Launch-Wrapper gesetzt wird:

```bash theme={null}
export OTEL_RESOURCE_ATTRIBUTES="enduser.id=jdoe@example.com,enduser.directory_id=S-1-5-21-..."
```

### Audit MCP-Aktivität

Um MCP-Server-Aktivität mit vollständiger Call-Detail zu erfassen, aktivieren Sie den Logs-Exporter und setzen Sie `OTEL_LOG_TOOL_DETAILS=1`. Jede MCP-Operation erzeugt dann strukturierte Ereignisse, die den Server-Namen, Tool-Namen und Call-Argumente zusammen mit den Standard-Identitätsattributen tragen:

| Ereignis                | Was es für MCP aufzeichnet                                                                                                                                                                      |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mcp_server_connection` | Server-Verbindung, Trennung und Verbindungsfehler mit `server_name`, `transport_type`, `server_scope` und Fehlerdetail                                                                          |
| `tool_result`           | Jeder MCP-Tool-Aufruf mit `tool_name` und `mcp_server_scope`, eine `tool_parameters` Nutzlast mit `mcp_server_name` und `mcp_tool_name`, und eine `tool_input` Nutzlast mit den Call-Argumenten |
| `tool_decision`         | Ob der Aufruf zulässig oder verweigert wurde, und ob die Entscheidung von Config, einem Hook oder dem Benutzer kam                                                                              |

Ohne `OTEL_LOG_TOOL_DETAILS` tragen `tool_result` Ereignisse immer noch `tool_name` und `mcp_server_scope`, aber lassen die `mcp_server_name`/`mcp_tool_name` Aufschlüsselung und die Argumente weg, und `mcp_server_connection` Ereignisse lassen `server_name` und die Fehlermeldung weg.

### Sicherheitsfragen zu Ereignissen zuordnen

Beim Erstellen von Erkennungsregeln schlagen Sie das Signal auf, das Sie überwachen möchten, und fragen Sie Ihr Backend nach dem entsprechenden Ereignis und den Attributen ab:

| Signal                                            | Ereignis                                    | Schlüsselattribute                                           |
| ------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------ |
| Tool-Aufruf zulässig oder verweigert, und von wem | `tool_decision`                             | `decision`, `source`, `tool_name`                            |
| Berechtigungsmodus-Eskalation                     | `permission_mode_changed`                   | `from_mode`, `to_mode`, `trigger`                            |
| Policy-Hook blockierte eine Aktion                | `hook_execution_complete`                   | `hook_event`, `num_blocking`                                 |
| Login, Logout und Authentifizierungsfehler        | `auth`                                      | `action`, `success`, `error_category`                        |
| MCP-Server-Verbindung oder Fehler                 | `mcp_server_connection`                     | `status`, `server_name`, `error_code`                        |
| Plugin installiert und seine Quelle               | `plugin_installed`                          | `plugin.name`, `marketplace.name`, `marketplace.is_official` |
| Befehle ausgeführt und Dateien berührt            | `tool_result` mit `OTEL_LOG_TOOL_DETAILS=1` | `tool_parameters`, `tool_input`                              |

Claude Code gibt nur den rohen Ereignisstrom aus. Anomalieerkennung, Baselining, Korrelation über Sitzungen hinweg und Warnungen sind die Verantwortung Ihres SIEM oder Observability-Backends.

### Ereignisse an ein SIEM senden

Zeigen Sie `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` auf den OTLP-Receiver Ihres SIEM oder auf einen OpenTelemetry Collector, der an die native Ingest-API Ihres SIEM weiterleitet. Das folgende verwaltete Einstellungsbeispiel exportiert nur Ereignisse, mit vollständiger Tool-Detail-Aktivierung für MCP- und Bash-Auditing:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_EXPORTER_OTLP_LOGS_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "https://siem.example.com:4318/v1/logs",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer your-siem-token"
  }
}
```

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

* OpenTelemetry-Export zu Ihrem Backend ist opt-in und erfordert explizite Konfiguration. Informationen zu Anthropics separater operativer Telemetrie und wie Sie diese deaktivieren, finden Sie unter [Datennutzung](/de/data-usage#telemetry-services)
* Rohe Dateiinhalte und Code-Snippets sind nicht in Metriken oder Ereignissen enthalten. Trace-Spans sind ein separater Datenpfad: siehe die Aufzählung `OTEL_LOG_TOOL_CONTENT` unten
* Wenn über OAuth authentifiziert, ist `user.email` in Telemetrie-Attributen enthalten. Wenn dies ein Problem für Ihre Organisation darstellt, arbeiten Sie mit Ihrem Telemetrie-Backend zusammen, um dieses Feld zu filtern oder zu schwärzen
* Benutzer-Prompt-Inhalte werden standardmäßig nicht erfasst. Nur die Prompt-Länge wird aufgezeichnet. Um Benutzer-Prompt-Inhalte einzubeziehen, setzen Sie `OTEL_LOG_USER_PROMPTS=1`
* Tool-Eingabeargumente und Parameter werden standardmäßig nicht protokolliert. Um sie einzubeziehen, setzen Sie `OTEL_LOG_TOOL_DETAILS=1`. Wenn aktiviert, enthalten `tool_result`-Ereignisse ein `tool_parameters`-Attribut mit Bash-Befehlen, MCP-Server- und Tool-Namen sowie Skill-Namen, plus ein `tool_input`-Attribut mit Dateipfaden, URLs, Suchmustern und anderen Argumenten. `user_prompt`-Ereignisse enthalten den wörtlichen `command_name` für benutzerdefinierte, Plugin- und MCP-Befehle. Trace-Spans enthalten das gleiche `tool_input`-Attribut und eingabebezogene Attribute wie `file_path`. Einzelne Werte über 512 Zeichen werden gekürzt und die Gesamtmenge ist auf etwa 4 K Zeichen begrenzt, aber die Argumente können immer noch vertrauliche Werte enthalten. Konfigurieren Sie Ihr Telemetrie-Backend, um diese Attribute nach Bedarf zu filtern oder zu schwärzen
* Tool-Eingabe- und Ausgabeinhalte werden in Trace-Spans standardmäßig nicht protokolliert. Um sie einzubeziehen, setzen Sie `OTEL_LOG_TOOL_CONTENT=1`. Wenn aktiviert, enthalten Span-Ereignisse vollständige Tool-Eingabe- und Ausgabeinhalte, gekürzt bei 60 KB pro Span. Dies kann rohe Dateiinhalte aus Read-Tool-Ergebnissen und Bash-Befehlsausgabe enthalten. Konfigurieren Sie Ihr Telemetrie-Backend, um diese Attribute nach Bedarf zu filtern oder zu schwärzen
* Rohe Anthropic Messages API-Anfrage- und Antwort-Texte werden standardmäßig nicht protokolliert. Um sie einzubeziehen, setzen Sie `OTEL_LOG_RAW_API_BODIES`. Mit `=1` gibt jeder API-Aufruf `api_request_body` und `api_response_body` Log-Ereignisse aus, deren `body`-Attribut die JSON-serialisierte Nutzlast ist, gekürzt bei 60 KB. Mit `=file:<dir>` werden ungekürzte Texte unter diesem Verzeichnis in `.request.json` und `.response.json` Dateien geschrieben und die Ereignisse tragen einen `body_ref` Pfad statt des Inline-Textes. Versenden Sie das Verzeichnis mit einem Log-Collector oder Sidecar statt über den Telemetrie-Stream. In beiden Modi enthalten Texte die gesamte Konversationshistorie (Systemprompt, jeder vorherige Benutzer- und Assistent-Durchgang, Tool-Ergebnisse), daher impliziert das Aktivieren dies Zustimmung zu allem, was die anderen `OTEL_LOG_*` Content-Flags offenbaren würden. Claudes Extended-Thinking-Inhalte werden unabhängig von anderen Einstellungen immer aus diesen Texten geschwärzt

## Überwachung von Claude Code auf Amazon Bedrock

Für detaillierte Anleitung zur Überwachung der Claude Code-Nutzung für Amazon Bedrock siehe [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
