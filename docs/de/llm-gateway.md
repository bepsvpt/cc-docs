> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LLM-Gateway-Konfiguration

> Erfahren Sie, wie Sie Claude Code für die Zusammenarbeit mit LLM-Gateway-Lösungen konfigurieren. Behandelt Gateway-Anforderungen, Authentifizierungskonfiguration, Modellauswahl und anbieter-spezifisches Endpoint-Setup.

LLM-Gateways bieten eine zentralisierte Proxy-Schicht zwischen Claude Code und Modellanbietern und bieten häufig:

* **Zentralisierte Authentifizierung** - Einzelner Punkt für die API-Schlüsselverwaltung
* **Nutzungsverfolgung** - Überwachen Sie die Nutzung über Teams und Projekte hinweg
* **Kostenkontrollen** - Implementieren Sie Budgets und Ratenlimits
* **Audit-Protokollierung** - Verfolgen Sie alle Modellinteraktionen zur Compliance
* **Modell-Routing** - Wechseln Sie zwischen Anbietern ohne Code-Änderungen

## Gateway-Anforderungen

Damit ein LLM-Gateway mit Claude Code funktioniert, muss es die folgenden Anforderungen erfüllen:

**API-Format**

Das Gateway muss Clients mindestens eines der folgenden API-Formate bereitstellen:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * Muss Request-Header weiterleiten: `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * Muss Request-Body-Felder beibehalten: `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Muss Request-Header weiterleiten: `anthropic-beta`, `anthropic-version`

Das Nichtweiterleiten von Headern oder das Nichtbeibehalten von Body-Feldern kann zu eingeschränkter Funktionalität oder der Unmöglichkeit führen, Claude Code-Funktionen zu nutzen.

<Note>
  Claude Code bestimmt, welche Funktionen aktiviert werden sollen, basierend auf dem API-Format. Bei Verwendung des Anthropic Messages-Formats mit Bedrock oder Vertex müssen Sie möglicherweise die Umgebungsvariable `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` setzen.
</Note>

**Request-Header**

Claude Code enthält die folgenden Header bei API-Anfragen:

| Header                          | Beschreibung                                                                                                                                                                                                                                                                                                                         |
| :------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `X-Claude-Code-Session-Id`      | Ein eindeutiger Bezeichner für die aktuelle Claude Code-Sitzung. Proxies können dies verwenden, um alle API-Anfragen aus einer einzelnen Sitzung zu aggregieren, ohne den Request-Body zu analysieren.                                                                                                                               |
| `X-Claude-Code-Agent-Id`        | Bezeichner des Subagenten oder Teamkollegen, der die Anfrage gestellt hat. Ihr Proxy kann dies verwenden, um API-Kosten einzelnen parallelen Subagenten innerhalb einer Sitzung zuzuordnen, ohne den Request-Body zu analysieren. Nur für Anfragen vorhanden, die von einem In-Process-Subagenten oder Teamkollegen gestellt werden. |
| `X-Claude-Code-Parent-Agent-Id` | Bezeichner des Agenten, der den Agent spawnte, der die Anfrage stellt. Verwenden Sie dies zusammen mit `X-Claude-Code-Agent-Id`, um API-Kosten über verschachtelte Agenten in Ihrem Proxy zuzuordnen. Nur vorhanden, wenn der anfragende Agent selbst von einem anderen Agenten gespawnt wurde.                                      |

Beide Agent-ID-Header sind ephemere Pro-Spawn-Bezeichner, keine persistenten Benutzer- oder Geräte-IDs.

Claude Code stellt auch einen kurzen Attributionsblock dem System-Prompt voran, der die Client-Version und einen Fingerabdruck aus dem Gespräch enthält. Die Anthropic API entfernt diesen Block vor der Verarbeitung, sodass er sich nicht auf First-Party-Prompt-Caching auswirkt. Wenn Ihr Gateway seinen eigenen Prompt-Cache mit dem vollständigen Request-Body als Schlüssel implementiert, setzen Sie [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/de/env-vars), um ihn auszulassen.

## Konfiguration

### Modellauswahl

Standardmäßig verwendet Claude Code Standard-Modellnamen für das ausgewählte API-Format.

Wenn `ANTHROPIC_BASE_URL` auf ein Gateway verweist, das das Anthropic Messages-Format bereitstellt, fragt Claude Code beim Start den `/v1/models`-Endpunkt des Gateways ab und fügt die zurückgegebenen Modelle zur `/model`-Auswahl hinzu. Setzen Sie `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1`, um dies zu aktivieren. Die Erkennung ist standardmäßig deaktiviert, damit Gateways, die durch einen gemeinsamen API-Schlüssel unterstützt werden, nicht jedes Modell, auf das der Schlüssel zugreifen kann, jedem Benutzer anzeigen. Jeder erkannte Eintrag ist mit „Aus Gateway" gekennzeichnet und verwendet das Feld `display_name` aus der Antwort, wenn eines bereitgestellt wird. Dies erfordert Claude Code v2.1.129 oder später.

Die Erkennung gilt nur für das Anthropic Messages-Format. Sie wird nicht für Bedrock- oder Vertex-Pass-Through-Endpunkte ausgeführt und wird nicht ausgeführt, wenn `ANTHROPIC_BASE_URL` nicht gesetzt ist oder auf `api.anthropic.com` verweist.

Die Erkennungsanfrage authentifiziert sich auf die gleiche Weise wie Inferenzanfragen: Sie sendet `ANTHROPIC_AUTH_TOKEN` als Bearer-Token oder `ANTHROPIC_API_KEY` als `x-api-key`-Header, wenn kein Auth-Token gesetzt ist, zusammen mit allen Headern aus `ANTHROPIC_CUSTOM_HEADERS`. Nur Modelle, deren ID mit `claude` oder `anthropic` beginnt, werden zur Auswahl hinzugefügt. Die Ergebnisse werden in `~/.claude/cache/gateway-models.json` zwischengespeichert und bei jedem Start aktualisiert. Wenn die Anfrage fehlschlägt oder das Gateway `/v1/models` nicht implementiert, wird die Auswahl auf die zwischengespeicherte Liste vom vorherigen Start oder auf die integrierte Modellliste zurückgesetzt.

Wenn Ihr Gateway Modellnamen verwendet, die nicht dem Erkennungsfilter entsprechen, verwenden Sie die in [Modellkonfiguration](/de/model-config) dokumentierten Umgebungsvariablen, um sie manuell hinzuzufügen.

## LiteLLM-Konfiguration

<Warning>
  LiteLLM PyPI-Versionen 1.82.7 und 1.82.8 wurden mit Malware zum Diebstahl von Anmeldedaten kompromittiert. Installieren Sie diese Versionen nicht. Wenn Sie diese bereits installiert haben:

  * Entfernen Sie das Paket
  * Rotieren Sie alle Anmeldedaten auf betroffenen Systemen
  * Folgen Sie den Abhilfeschritten in [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM ist ein Drittanbieter-Proxy-Service. Anthropic befürwortet, wartet oder prüft nicht die Sicherheit oder Funktionalität von LiteLLM. Diese Anleitung wird zu Informationszwecken bereitgestellt und kann veraltet werden. Verwenden Sie sie nach eigenem Ermessen.
</Warning>

### Voraussetzungen

* Claude Code auf die neueste Version aktualisiert
* LiteLLM Proxy Server bereitgestellt und zugänglich
* Zugriff auf Claude-Modelle über Ihren gewählten Anbieter

### Grundlegende LiteLLM-Einrichtung

**Konfigurieren Sie Claude Code**:

#### Authentifizierungsmethoden

##### Statischer API-Schlüssel

Einfachste Methode mit einem festen API-Schlüssel:

```bash theme={null}
# In Umgebung setzen
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Oder in Claude Code-Einstellungen
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Dieser Wert wird als `Authorization`-Header gesendet.

##### Dynamischer API-Schlüssel mit Helper

Für rotierende Schlüssel oder Pro-Benutzer-Authentifizierung:

1. Erstellen Sie ein API-Schlüssel-Helper-Skript:

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Beispiel: Schlüssel aus Vault abrufen
vault kv get -field=api_key secret/litellm/claude-code

# Beispiel: JWT-Token generieren
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Konfigurieren Sie Claude Code-Einstellungen zur Verwendung des Helpers:

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Legen Sie das Token-Aktualisierungsintervall fest:

```bash theme={null}
# Alle Stunde aktualisieren (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Dieser Wert wird als `Authorization`- und `X-Api-Key`-Header gesendet. Der `apiKeyHelper` hat eine niedrigere Priorität als `ANTHROPIC_AUTH_TOKEN` oder `ANTHROPIC_API_KEY`.

#### Einheitlicher Endpoint (empfohlen)

Verwendung von LiteLLMs [Anthropic-Format-Endpoint](https://docs.litellm.ai/docs/anthropic_unified):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Vorteile des einheitlichen Endpoints gegenüber Pass-Through-Endpoints:**

* Lastverteilung
* Fallbacks
* Konsistente Unterstützung für Kosten-Tracking und End-Benutzer-Tracking

#### Anbieter-spezifische Pass-Through-Endpoints (Alternative)

##### Claude API über LiteLLM

Verwendung von [Pass-Through-Endpoint](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock über LiteLLM

Verwendung von [Pass-Through-Endpoint](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI über LiteLLM

Verwendung von [Pass-Through-Endpoint](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

##### Claude Platform auf AWS über ein Gateway

Weiterleitung an ein Gateway, das zum [Claude Platform auf AWS](/de/claude-platform-on-aws) Endpoint weiterleitet:

```bash theme={null}
export ANTHROPIC_AWS_BASE_URL=https://litellm-server:4000/anthropic-aws
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
```

Weitere detaillierte Informationen finden Sie in der [LiteLLM-Dokumentation](https://docs.litellm.ai/).

## Zusätzliche Ressourcen

* [LiteLLM-Dokumentation](https://docs.litellm.ai/)
* [Claude Code-Einstellungen](/de/settings)
* [Enterprise-Netzwerkkonfiguration](/de/network-config)
* [Übersicht über Drittanbieter-Integrationen](/de/third-party-integrations)
