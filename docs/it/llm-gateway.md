> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurazione del gateway LLM

> Scopri come configurare Claude Code per funzionare con soluzioni di gateway LLM. Copre i requisiti del gateway, la configurazione dell'autenticazione, la selezione del modello e la configurazione degli endpoint specifici del provider.

I gateway LLM forniscono un livello proxy centralizzato tra Claude Code e i provider di modelli, spesso fornendo:

* **Autenticazione centralizzata** - Punto singolo per la gestione delle chiavi API
* **Tracciamento dell'utilizzo** - Monitora l'utilizzo tra team e progetti
* **Controlli dei costi** - Implementa budget e limiti di velocità
* **Registrazione di audit** - Traccia tutte le interazioni del modello per la conformità
* **Instradamento dei modelli** - Passa da un provider all'altro senza modifiche al codice

## Requisiti del gateway

Affinché un gateway LLM funzioni con Claude Code, deve soddisfare i seguenti requisiti:

**Formato API**

Il gateway deve esporre ai client almeno uno dei seguenti formati API:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * Deve inoltrare le intestazioni della richiesta: `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * Deve preservare i campi del corpo della richiesta: `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Deve inoltrare le intestazioni della richiesta: `anthropic-beta`, `anthropic-version`

Il mancato inoltro delle intestazioni o la mancata preservazione dei campi del corpo potrebbe causare una riduzione della funzionalità o l'impossibilità di utilizzare le funzionalità di Claude Code.

<Note>
  Claude Code determina quali funzionalità abilitare in base al formato API. Quando si utilizza il formato Anthropic Messages con Bedrock o Vertex, potrebbe essere necessario impostare la variabile di ambiente `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

## Configurazione

### Selezione del modello

Per impostazione predefinita, Claude Code utilizzerà nomi di modelli standard per il formato API selezionato.

Se hai configurato nomi di modelli personalizzati nel tuo gateway, utilizza le variabili di ambiente documentate in [Configurazione del modello](/it/model-config) per abbinare i tuoi nomi personalizzati.

## Configurazione di LiteLLM

<Note>
  LiteLLM è un servizio proxy di terze parti. Anthropic non approva, mantiene o controlla la sicurezza o la funzionalità di LiteLLM. Questa guida è fornita a scopo informativo e potrebbe diventare obsoleta. Utilizzala a tua discrezione.
</Note>

### Prerequisiti

* Claude Code aggiornato all'ultima versione
* LiteLLM Proxy Server distribuito e accessibile
* Accesso ai modelli Claude attraverso il provider scelto

### Configurazione di base di LiteLLM

**Configura Claude Code**:

#### Metodi di autenticazione

##### Chiave API statica

Metodo più semplice utilizzando una chiave API fissa:

```bash  theme={null}
# Imposta nell'ambiente
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# O nelle impostazioni di Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Questo valore verrà inviato come intestazione `Authorization`.

##### Chiave API dinamica con helper

Per chiavi rotanti o autenticazione per utente:

1. Crea uno script helper per la chiave API:

```bash  theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Esempio: Recupera la chiave dal vault
vault kv get -field=api_key secret/litellm/claude-code

# Esempio: Genera token JWT
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Configura le impostazioni di Claude Code per utilizzare l'helper:

```json  theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Imposta l'intervallo di aggiornamento del token:

```bash  theme={null}
# Aggiorna ogni ora (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Questo valore verrà inviato come intestazioni `Authorization` e `X-Api-Key`. L'`apiKeyHelper` ha una precedenza inferiore rispetto a `ANTHROPIC_AUTH_TOKEN` o `ANTHROPIC_API_KEY`.

#### Endpoint unificato (consigliato)

Utilizzando l'[endpoint in formato Anthropic](https://docs.litellm.ai/docs/anthropic_unified) di LiteLLM:

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Vantaggi dell'endpoint unificato rispetto agli endpoint pass-through:**

* Bilanciamento del carico
* Fallback
* Supporto coerente per il tracciamento dei costi e il tracciamento dell'utente finale

#### Endpoint pass-through specifici del provider (alternativa)

##### Claude API attraverso LiteLLM

Utilizzando l'[endpoint pass-through](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock attraverso LiteLLM

Utilizzando l'[endpoint pass-through](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash  theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI attraverso LiteLLM

Utilizzando l'[endpoint pass-through](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash  theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Per informazioni più dettagliate, consulta la [documentazione di LiteLLM](https://docs.litellm.ai/).

## Risorse aggiuntive

* [Documentazione di LiteLLM](https://docs.litellm.ai/)
* [Impostazioni di Claude Code](/it/settings)
* [Configurazione della rete aziendale](/it/network-config)
* [Panoramica delle integrazioni di terze parti](/it/third-party-integrations)
