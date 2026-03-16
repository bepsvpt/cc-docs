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

## Konfiguration

### Modellauswahl

Standardmäßig verwendet Claude Code Standard-Modellnamen für das ausgewählte API-Format.

Wenn Sie benutzerdefinierte Modellnamen in Ihrem Gateway konfiguriert haben, verwenden Sie die in [Modellkonfiguration](/de/model-config) dokumentierten Umgebungsvariablen, um Ihre benutzerdefinierten Namen zu entsprechen.

## LiteLLM-Konfiguration

<Note>
  LiteLLM ist ein Drittanbieter-Proxy-Service. Anthropic befürwortet, wartet oder prüft nicht die Sicherheit oder Funktionalität von LiteLLM. Diese Anleitung wird zu Informationszwecken bereitgestellt und kann veraltet werden. Verwenden Sie sie nach eigenem Ermessen.
</Note>

### Voraussetzungen

* Claude Code auf die neueste Version aktualisiert
* LiteLLM Proxy Server bereitgestellt und zugänglich
* Zugriff auf Claude-Modelle über Ihren gewählten Anbieter

### Grundlegende LiteLLM-Einrichtung

**Konfigurieren Sie Claude Code**:

#### Authentifizierungsmethoden

##### Statischer API-Schlüssel

Einfachste Methode mit einem festen API-Schlüssel:

```bash  theme={null}
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

```bash  theme={null}
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

```json  theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Legen Sie das Token-Aktualisierungsintervall fest:

```bash  theme={null}
# Alle Stunde aktualisieren (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Dieser Wert wird als `Authorization`- und `X-Api-Key`-Header gesendet. Der `apiKeyHelper` hat eine niedrigere Priorität als `ANTHROPIC_AUTH_TOKEN` oder `ANTHROPIC_API_KEY`.

#### Einheitlicher Endpoint (empfohlen)

Verwendung von LiteLLMs [Anthropic-Format-Endpoint](https://docs.litellm.ai/docs/anthropic_unified):

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Vorteile des einheitlichen Endpoints gegenüber Pass-Through-Endpoints:**

* Lastverteilung
* Fallbacks
* Konsistente Unterstützung für Kosten-Tracking und End-Benutzer-Tracking

#### Anbieter-spezifische Pass-Through-Endpoints (Alternative)

##### Claude API über LiteLLM

Verwendung von [Pass-Through-Endpoint](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock über LiteLLM

Verwendung von [Pass-Through-Endpoint](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash  theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI über LiteLLM

Verwendung von [Pass-Through-Endpoint](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash  theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Weitere detaillierte Informationen finden Sie in der [LiteLLM-Dokumentation](https://docs.litellm.ai/).

## Zusätzliche Ressourcen

* [LiteLLM-Dokumentation](https://docs.litellm.ai/)
* [Claude Code-Einstellungen](/de/settings)
* [Enterprise-Netzwerkkonfiguration](/de/network-config)
* [Übersicht über Drittanbieter-Integrationen](/de/third-party-integrations)
