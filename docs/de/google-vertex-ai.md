> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code auf Google Vertex AI

> Erfahren Sie, wie Sie Claude Code über Google Vertex AI konfigurieren, einschließlich Setup, IAM-Konfiguration und Fehlerbehebung.

## Voraussetzungen

Bevor Sie Claude Code mit Vertex AI konfigurieren, stellen Sie sicher, dass Sie über Folgendes verfügen:

* Ein Google Cloud Platform (GCP)-Konto mit aktivierter Abrechnung
* Ein GCP-Projekt mit aktivierter Vertex AI API
* Zugriff auf gewünschte Claude-Modelle (z. B. Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installiert und konfiguriert
* Kontingent im gewünschten GCP-Bereich zugewiesen

<Note>
  Wenn Sie Claude Code für mehrere Benutzer bereitstellen, [fixieren Sie Ihre Modellversionen](#5-pin-model-versions), um Fehler zu vermeiden, wenn Anthropic neue Modelle veröffentlicht.
</Note>

## Regionskonfiguration

Claude Code kann sowohl mit Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) als auch mit regionalen Endpunkten verwendet werden.

<Note>
  Vertex AI unterstützt möglicherweise die Claude Code-Standardmodelle nicht in allen [Regionen](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models) oder auf [globalen Endpunkten](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Möglicherweise müssen Sie zu einer unterstützten Region wechseln, einen regionalen Endpunkt verwenden oder ein unterstütztes Modell angeben.
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
3. Fordern Sie Zugriff auf gewünschte Claude-Modelle an (z. B. Claude Sonnet 4.6)
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

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) wird automatisch unterstützt, wenn Sie das Flag `cache_control` ephemeral angeben. Um es zu deaktivieren, legen Sie `DISABLE_PROMPT_CACHING=1` fest. Für erhöhte Ratenlimits wenden Sie sich an den Google Cloud-Support. Bei Verwendung von Vertex AI sind die Befehle `/login` und `/logout` deaktiviert, da die Authentifizierung über Google Cloud-Anmeldedaten erfolgt.

### 5. Modellversionen fixieren

<Warning>
  Fixieren Sie spezifische Modellversionen für jede Bereitstellung. Wenn Sie Modellaliase (`sonnet`, `opus`, `haiku`) ohne Fixierung verwenden, versucht Claude Code möglicherweise, eine neuere Modellversion zu verwenden, die in Ihrem Vertex AI-Projekt nicht aktiviert ist, was bestehende Benutzer unterbricht, wenn Anthropic Updates veröffentlicht.
</Warning>

Legen Sie diese Umgebungsvariablen auf spezifische Vertex AI-Modell-IDs fest:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Aktuelle und ältere Modell-IDs finden Sie unter [Modellübersicht](https://platform.claude.com/docs/en/about-claude/models/overview). Siehe [Modellkonfiguration](/de/model-config#pin-models-for-third-party-deployments) für die vollständige Liste der Umgebungsvariablen.

Claude Code verwendet diese Standardmodelle, wenn keine Fixierungsvariablen gesetzt sind:

| Modelltyp                | Standardwert                |
| :----------------------- | :-------------------------- |
| Primäres Modell          | `claude-sonnet-4-6`         |
| Kleines/schnelles Modell | `claude-haiku-4-5@20251001` |

Um Modelle weiter anzupassen:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-6'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## IAM-Konfiguration

Weisen Sie die erforderlichen IAM-Berechtigungen zu:

Die Rolle `roles/aiplatform.user` umfasst die erforderlichen Berechtigungen:

* `aiplatform.endpoints.predict` - Erforderlich für Modellaufrufe und Token-Zählung

Für restriktivere Berechtigungen erstellen Sie eine benutzerdefinierte Rolle nur mit den oben genannten Berechtigungen.

Weitere Informationen finden Sie in der [Vertex IAM-Dokumentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Erstellen Sie ein dediziertes GCP-Projekt für Claude Code, um die Kostenverfolgung und Zugriffskontrolle zu vereinfachen.
</Note>

## 1M Token-Kontextfenster

Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5 und Sonnet 4 unterstützen das [1M Token-Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) auf Vertex AI. Claude Code aktiviert automatisch das erweiterte Kontextfenster, wenn Sie eine 1M-Modellvariante auswählen.

Um das 1M-Kontextfenster für Ihr fixiertes Modell zu aktivieren, hängen Sie `[1m]` an die Modell-ID an. Siehe [Modelle für Drittanbieter-Bereitstellungen fixieren](/de/model-config#pin-models-for-third-party-deployments) für Details.

## Fehlerbehebung

Wenn Sie auf Kontingentprobleme stoßen:

* Überprüfen Sie aktuelle Kontingente oder fordern Sie eine Kontingenterhöhung über die [Cloud Console](https://cloud.google.com/docs/quotas/view-manage) an

Wenn Sie auf Fehler „Modell nicht gefunden" 404 stoßen:

* Bestätigen Sie, dass das Modell im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) aktiviert ist
* Überprüfen Sie, dass Sie Zugriff auf die angegebene Region haben
* Wenn Sie `CLOUD_ML_REGION=global` verwenden, überprüfen Sie, dass Ihre Modelle globale Endpunkte im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) unter „Unterstützte Funktionen" unterstützen. Für Modelle, die globale Endpunkte nicht unterstützen, können Sie entweder:
  * Ein unterstütztes Modell über `ANTHROPIC_MODEL` oder `ANTHROPIC_SMALL_FAST_MODEL` angeben, oder
  * Einen regionalen Endpunkt mit `VERTEX_REGION_<MODEL_NAME>`-Umgebungsvariablen festlegen

Wenn Sie auf 429-Fehler stoßen:

* Stellen Sie für regionale Endpunkte sicher, dass das primäre Modell und das kleine/schnelle Modell in Ihrer ausgewählten Region unterstützt werden
* Erwägen Sie, zu `CLOUD_ML_REGION=global` zu wechseln, um bessere Verfügbarkeit zu erreichen

## Zusätzliche Ressourcen

* [Vertex AI-Dokumentation](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI-Preisgestaltung](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI-Kontingente und -Limits](https://cloud.google.com/vertex-ai/docs/quotas)
