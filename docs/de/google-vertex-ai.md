> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code auf Google Vertex AI

> Erfahren Sie, wie Sie Claude Code über Google Vertex AI konfigurieren, einschließlich Setup, IAM-Konfiguration und Fehlerbehebung.

## Voraussetzungen

Bevor Sie Claude Code mit Vertex AI konfigurieren, stellen Sie sicher, dass Sie über Folgendes verfügen:

* Ein Google Cloud Platform (GCP)-Konto mit aktivierter Abrechnung
* Ein GCP-Projekt mit aktivierter Vertex AI API
* Zugriff auf gewünschte Claude-Modelle (z. B. Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) installiert und konfiguriert
* Kontingent in der gewünschten GCP-Region zugewiesen

## Regionskonfiguration

Claude Code kann sowohl mit Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) als auch mit regionalen Endpunkten verwendet werden.

<Note>
  Vertex AI unterstützt möglicherweise die Claude Code-Standardmodelle nicht in allen Regionen. Möglicherweise müssen Sie zu einer [unterstützten Region oder einem unterstützten Modell](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models) wechseln.
</Note>

<Note>
  Vertex AI unterstützt möglicherweise die Claude Code-Standardmodelle nicht auf globalen Endpunkten. Möglicherweise müssen Sie zu einem regionalen Endpunkt oder einem [unterstützten Modell](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models) wechseln.
</Note>

## Setup

### 1. Vertex AI API aktivieren

Aktivieren Sie die Vertex AI API in Ihrem GCP-Projekt:

```bash  theme={null}
# Legen Sie Ihre Projekt-ID fest
gcloud config set project YOUR-PROJECT-ID

# Aktivieren Sie die Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Modellzugriff anfordern

Fordern Sie Zugriff auf Claude-Modelle in Vertex AI an:

1. Navigieren Sie zum [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Suchen Sie nach „Claude"-Modellen
3. Fordern Sie Zugriff auf gewünschte Claude-Modelle an (z. B. Claude Sonnet 4.5)
4. Warten Sie auf Genehmigung (kann 24–48 Stunden dauern)

### 3. GCP-Anmeldedaten konfigurieren

Claude Code verwendet die standardmäßige Google Cloud-Authentifizierung.

Weitere Informationen finden Sie in der [Google Cloud-Authentifizierungsdokumentation](https://cloud.google.com/docs/authentication).

<Note>
  Bei der Authentifizierung verwendet Claude Code automatisch die Projekt-ID aus der Umgebungsvariablen `ANTHROPIC_VERTEX_PROJECT_ID`. Um dies zu überschreiben, legen Sie eine dieser Umgebungsvariablen fest: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` oder `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Claude Code konfigurieren

Legen Sie die folgenden Umgebungsvariablen fest:

```bash  theme={null}
# Aktivieren Sie die Vertex AI-Integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Deaktivieren Sie Prompt Caching bei Bedarf
export DISABLE_PROMPT_CACHING=1

# Wenn CLOUD_ML_REGION=global, überschreiben Sie die Region für nicht unterstützte Modelle
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Optional: Überschreiben Sie Regionen für andere spezifische Modelle
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) wird automatisch unterstützt, wenn Sie das `cache_control` Ephemeral-Flag angeben. Um es zu deaktivieren, legen Sie `DISABLE_PROMPT_CACHING=1` fest. Für erhöhte Ratenlimits wenden Sie sich an den Google Cloud-Support.
</Note>

<Note>
  Bei Verwendung von Vertex AI sind die Befehle `/login` und `/logout` deaktiviert, da die Authentifizierung über Google Cloud-Anmeldedaten erfolgt.
</Note>

### 5. Modellkonfiguration

Claude Code verwendet diese Standardmodelle für Vertex AI:

| Modelltyp                | Standardwert                 |
| :----------------------- | :--------------------------- |
| Primäres Modell          | `claude-sonnet-4-5@20250929` |
| Kleines/schnelles Modell | `claude-haiku-4-5@20251001`  |

<Note>
  Für Vertex AI-Benutzer wird Claude Code nicht automatisch von Haiku 3.5 auf Haiku 4.5 aktualisiert. Um manuell zu einem neueren Haiku-Modell zu wechseln, legen Sie die Umgebungsvariable `ANTHROPIC_DEFAULT_HAIKU_MODEL` auf den vollständigen Modellnamen fest (z. B. `claude-haiku-4-5@20251001`).
</Note>

Um Modelle anzupassen:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## IAM-Konfiguration

Weisen Sie die erforderlichen IAM-Berechtigungen zu:

Die Rolle `roles/aiplatform.user` umfasst die erforderlichen Berechtigungen:

* `aiplatform.endpoints.predict` - Erforderlich für Modellaufrufe und Token-Zählung

Für restriktivere Berechtigungen erstellen Sie eine benutzerdefinierte Rolle nur mit den oben genannten Berechtigungen.

Weitere Informationen finden Sie in der [Vertex IAM-Dokumentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Wir empfehlen, ein dediziertes GCP-Projekt für Claude Code zu erstellen, um die Kostenverfolgung und Zugriffskontrolle zu vereinfachen.
</Note>

## 1M Token-Kontextfenster

Claude Sonnet 4 und Sonnet 4.5 unterstützen das [1M Token-Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) auf Vertex AI.

<Note>
  Das 1M Token-Kontextfenster befindet sich derzeit in der Beta-Phase. Um das erweiterte Kontextfenster zu verwenden, fügen Sie den `context-1m-2025-08-07` Beta-Header in Ihre Vertex AI-Anfragen ein.
</Note>

## Fehlerbehebung

Wenn Sie auf Kontingentprobleme stoßen:

* Überprüfen Sie aktuelle Kontingente oder fordern Sie eine Kontingenterhöhung über die [Cloud Console](https://cloud.google.com/docs/quotas/view-manage) an

Wenn Sie auf „Modell nicht gefunden" 404-Fehler stoßen:

* Bestätigen Sie, dass das Modell im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) aktiviert ist
* Überprüfen Sie, dass Sie Zugriff auf die angegebene Region haben
* Wenn Sie `CLOUD_ML_REGION=global` verwenden, überprüfen Sie, dass Ihre Modelle globale Endpunkte im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) unter „Unterstützte Funktionen" unterstützen. Für Modelle, die globale Endpunkte nicht unterstützen, können Sie entweder:
  * Ein unterstütztes Modell über `ANTHROPIC_MODEL` oder `ANTHROPIC_SMALL_FAST_MODEL` angeben, oder
  * Einen regionalen Endpunkt mit `VERTEX_REGION_<MODEL_NAME>` Umgebungsvariablen festlegen

Wenn Sie auf 429-Fehler stoßen:

* Stellen Sie für regionale Endpunkte sicher, dass das primäre Modell und das kleine/schnelle Modell in Ihrer ausgewählten Region unterstützt werden
* Erwägen Sie, zu `CLOUD_ML_REGION=global` zu wechseln, um bessere Verfügbarkeit zu erreichen

## Zusätzliche Ressourcen

* [Vertex AI-Dokumentation](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI-Preisgestaltung](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI-Kontingente und -Limits](https://cloud.google.com/vertex-ai/docs/quotas)
