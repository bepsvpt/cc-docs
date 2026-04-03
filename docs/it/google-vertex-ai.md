> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Google Vertex AI

> Scopri come configurare Claude Code tramite Google Vertex AI, inclusa la configurazione, la configurazione IAM e la risoluzione dei problemi.

## Prerequisiti

Prima di configurare Claude Code con Vertex AI, assicurati di avere:

* Un account Google Cloud Platform (GCP) con fatturazione abilitata
* Un progetto GCP con Vertex AI API abilitata
* Accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installato e configurato
* Quota allocata nella regione GCP desiderata

<Note>
  Se stai distribuendo Claude Code a più utenti, [fissa le versioni del tuo modello](#5-pin-model-versions) per evitare interruzioni quando Anthropic rilascia nuovi modelli.
</Note>

## Configurazione della regione

Claude Code può essere utilizzato sia con endpoint Vertex AI [globali](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) che regionali.

<Note>
  Vertex AI potrebbe non supportare i modelli predefiniti di Claude Code in tutte le [regioni](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models) o su [endpoint globali](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Potrebbe essere necessario passare a una regione supportata, utilizzare un endpoint regionale o specificare un modello supportato.
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
3. Richiedi accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.6)
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

# Facoltativo: Esegui l'override dell'URL dell'endpoint Vertex per endpoint personalizzati o gateway
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Facoltativo: Disabilita prompt caching se necessario
export DISABLE_PROMPT_CACHING=1

# Quando CLOUD_ML_REGION=global, esegui l'override della regione per i modelli che non supportano endpoint globali
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Ogni versione del modello ha la sua propria variabile `VERTEX_REGION_CLAUDE_*`. Consulta il [riferimento delle variabili di ambiente](/it/env-vars) per l'elenco completo. Controlla [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) per determinare quali modelli supportano endpoint globali rispetto a quelli solo regionali.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) è automaticamente supportato quando specifichi il flag effimero `cache_control`. Per disabilitarlo, imposta `DISABLE_PROMPT_CACHING=1`. Per limiti di velocità aumentati, contatta il supporto di Google Cloud. Quando utilizzi Vertex AI, i comandi `/login` e `/logout` sono disabilitati poiché l'autenticazione è gestita tramite le credenziali di Google Cloud.

### 5. Fissa le versioni del modello

<Warning>
  Fissa versioni specifiche del modello per ogni distribuzione. Se utilizzi alias di modello (`sonnet`, `opus`, `haiku`) senza fissare, Claude Code potrebbe tentare di utilizzare una versione di modello più recente che non è abilitata nel tuo progetto Vertex AI, interrompendo gli utenti esistenti quando Anthropic rilascia aggiornamenti.
</Warning>

Imposta queste variabili di ambiente su ID modello Vertex AI specifici:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Per gli ID modello attuali e legacy, consulta [Panoramica dei modelli](https://platform.claude.com/docs/en/about-claude/models/overview). Consulta [Configurazione del modello](/it/model-config#pin-models-for-third-party-deployments) per l'elenco completo delle variabili di ambiente.

Claude Code utilizza questi modelli predefiniti quando nessuna variabile di fissaggio è impostata:

| Tipo di modello        | Valore predefinito           |
| :--------------------- | :--------------------------- |
| Modello primario       | `claude-sonnet-4-5@20250929` |
| Modello piccolo/veloce | `claude-haiku-4-5@20251001`  |

Per personalizzare ulteriormente i modelli:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Configurazione IAM

Assegna le autorizzazioni IAM richieste:

Il ruolo `roles/aiplatform.user` include le autorizzazioni richieste:

* `aiplatform.endpoints.predict` - Richiesto per l'invocazione del modello e il conteggio dei token

Per autorizzazioni più restrittive, crea un ruolo personalizzato con solo le autorizzazioni di cui sopra.

Per i dettagli, consulta la [documentazione IAM di Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Crea un progetto GCP dedicato per Claude Code per semplificare il tracciamento dei costi e il controllo degli accessi.
</Note>

## Finestra di contesto da 1M token

Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5 e Sonnet 4 supportano la [finestra di contesto da 1M token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) su Vertex AI. Claude Code abilita automaticamente la finestra di contesto estesa quando selezioni una variante di modello 1M.

Per abilitare la finestra di contesto 1M per il tuo modello fissato, aggiungi `[1m]` all'ID del modello. Consulta [Fissa i modelli per le distribuzioni di terze parti](/it/model-config#pin-models-for-third-party-deployments) per i dettagli.

## Risoluzione dei problemi

Se riscontri problemi di quota:

* Controlla le quote attuali o richiedi un aumento della quota tramite [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Se riscontri errori "model not found" 404:

* Conferma che il modello è abilitato in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifica di avere accesso alla regione specificata
* Se utilizzi `CLOUD_ML_REGION=global`, controlla che i tuoi modelli supportino endpoint globali in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) in "Supported features". Per i modelli che non supportano endpoint globali, puoi:
  * Specificare un modello supportato tramite `ANTHROPIC_MODEL` o `ANTHROPIC_DEFAULT_HAIKU_MODEL`, oppure
  * Impostare un endpoint regionale utilizzando le variabili di ambiente `VERTEX_REGION_<MODEL_NAME>`

Se riscontri errori 429:

* Per gli endpoint regionali, assicurati che il modello primario e il modello piccolo/veloce siano supportati nella tua regione selezionata
* Considera di passare a `CLOUD_ML_REGION=global` per una migliore disponibilità

## Risorse aggiuntive

* [Documentazione di Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Prezzi di Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Quote e limiti di Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
