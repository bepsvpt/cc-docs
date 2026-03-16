> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Google Vertex AI

> Scopri come configurare Claude Code tramite Google Vertex AI, inclusa la configurazione, la configurazione IAM e la risoluzione dei problemi.

## Prerequisiti

Prima di configurare Claude Code con Vertex AI, assicurati di avere:

* Un account Google Cloud Platform (GCP) con fatturazione abilitata
* Un progetto GCP con Vertex AI API abilitata
* Accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) installato e configurato
* Quota allocata nella regione GCP desiderata

## Configurazione della regione

Claude Code può essere utilizzato sia con endpoint Vertex AI [globali](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) che regionali.

<Note>
  Vertex AI potrebbe non supportare i modelli predefiniti di Claude Code in tutte le regioni. Potrebbe essere necessario passare a una [regione o modello supportato](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  Vertex AI potrebbe non supportare i modelli predefiniti di Claude Code su endpoint globali. Potrebbe essere necessario passare a un endpoint regionale o a un [modello supportato](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
</Note>

## Configurazione

### 1. Abilita Vertex AI API

Abilita Vertex AI API nel tuo progetto GCP:

```bash  theme={null}
# Imposta il tuo ID progetto
gcloud config set project YOUR-PROJECT-ID

# Abilita Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Richiedi accesso al modello

Richiedi accesso ai modelli Claude in Vertex AI:

1. Accedi a [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Cerca i modelli "Claude"
3. Richiedi accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.5)
4. Attendi l'approvazione (potrebbe richiedere 24-48 ore)

### 3. Configura le credenziali GCP

Claude Code utilizza l'autenticazione standard di Google Cloud.

Per ulteriori informazioni, consulta la [documentazione di autenticazione di Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Durante l'autenticazione, Claude Code utilizzerà automaticamente l'ID progetto dalla variabile di ambiente `ANTHROPIC_VERTEX_PROJECT_ID`. Per eseguire l'override, imposta una di queste variabili di ambiente: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` o `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Configura Claude Code

Imposta le seguenti variabili di ambiente:

```bash  theme={null}
# Abilita integrazione Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Facoltativo: Disabilita prompt caching se necessario
export DISABLE_PROMPT_CACHING=1

# Quando CLOUD_ML_REGION=global, esegui l'override della regione per i modelli non supportati
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Facoltativo: Esegui l'override delle regioni per altri modelli specifici
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) è automaticamente supportato quando specifichi il flag effimero `cache_control`. Per disabilitarlo, imposta `DISABLE_PROMPT_CACHING=1`. Per limiti di velocità aumentati, contatta il supporto di Google Cloud.
</Note>

<Note>
  Quando si utilizza Vertex AI, i comandi `/login` e `/logout` sono disabilitati poiché l'autenticazione viene gestita tramite le credenziali di Google Cloud.
</Note>

### 5. Configurazione del modello

Claude Code utilizza questi modelli predefiniti per Vertex AI:

| Tipo di modello        | Valore predefinito           |
| :--------------------- | :--------------------------- |
| Modello primario       | `claude-sonnet-4-5@20250929` |
| Modello piccolo/veloce | `claude-haiku-4-5@20251001`  |

<Note>
  Per gli utenti di Vertex AI, Claude Code non eseguirà automaticamente l'aggiornamento da Haiku 3.5 a Haiku 4.5. Per passare manualmente a un modello Haiku più recente, imposta la variabile di ambiente `ANTHROPIC_DEFAULT_HAIKU_MODEL` sul nome completo del modello (ad esempio, `claude-haiku-4-5@20251001`).
</Note>

Per personalizzare i modelli:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Configurazione IAM

Assegna i permessi IAM richiesti:

Il ruolo `roles/aiplatform.user` include i permessi richiesti:

* `aiplatform.endpoints.predict` - Richiesto per l'invocazione del modello e il conteggio dei token

Per permessi più restrittivi, crea un ruolo personalizzato con solo i permessi di cui sopra.

Per i dettagli, consulta la [documentazione IAM di Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Consigliamo di creare un progetto GCP dedicato per Claude Code per semplificare il tracciamento dei costi e il controllo degli accessi.
</Note>

## Finestra di contesto da 1M token

Claude Sonnet 4 e Sonnet 4.5 supportano la [finestra di contesto da 1M token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) su Vertex AI.

<Note>
  La finestra di contesto da 1M token è attualmente in beta. Per utilizzare la finestra di contesto estesa, includi l'intestazione beta `context-1m-2025-08-07` nelle tue richieste Vertex AI.
</Note>

## Risoluzione dei problemi

Se riscontri problemi di quota:

* Controlla le quote attuali o richiedi un aumento della quota tramite [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Se riscontri errori "model not found" 404:

* Conferma che il modello sia abilitato in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifica di avere accesso alla regione specificata
* Se utilizzi `CLOUD_ML_REGION=global`, verifica che i tuoi modelli supportino endpoint globali in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) sotto "Supported features". Per i modelli che non supportano endpoint globali, puoi:
  * Specificare un modello supportato tramite `ANTHROPIC_MODEL` o `ANTHROPIC_SMALL_FAST_MODEL`, oppure
  * Impostare un endpoint regionale utilizzando le variabili di ambiente `VERTEX_REGION_<MODEL_NAME>`

Se riscontri errori 429:

* Per endpoint regionali, assicurati che il modello primario e il modello piccolo/veloce siano supportati nella tua regione selezionata
* Considera di passare a `CLOUD_ML_REGION=global` per una migliore disponibilità

## Risorse aggiuntive

* [Documentazione di Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Prezzi di Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Quote e limiti di Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
