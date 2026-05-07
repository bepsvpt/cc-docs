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

**Intestazioni della richiesta**

Claude Code include le seguenti intestazioni su ogni richiesta API:

| Intestazione               | Descrizione                                                                                                                                                                                         |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `X-Claude-Code-Session-Id` | Un identificatore univoco per la sessione Claude Code corrente. I proxy possono utilizzarlo per aggregare tutte le richieste API da una singola sessione senza analizzare il corpo della richiesta. |

Claude Code inoltre antepone un breve blocco di attribuzione al prompt di sistema contenente la versione del client e un'impronta digitale derivata dalla conversazione. L'API Anthropic rimuove questo blocco prima dell'elaborazione, quindi non influisce sulla memorizzazione nella cache del prompt di prima parte. Se il tuo gateway implementa la propria cache del prompt con chiave sul corpo della richiesta completo, imposta [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/it/env-vars) per ometterlo.

## Configurazione

### Selezione del modello

Per impostazione predefinita, Claude Code utilizza nomi di modelli standard per il formato API selezionato.

Quando `ANTHROPIC_BASE_URL` punta a un gateway che espone il formato Anthropic Messages, Claude Code interroga l'endpoint `/v1/models` del gateway all'avvio e aggiunge i modelli restituiti al selettore `/model`. Impostare `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` per abilitare questa funzionalità. La scoperta è disabilitata per impostazione predefinita in modo che i gateway supportati da una chiave API condivisa non espongano ogni modello a cui la chiave può accedere a ogni utente. Ogni voce scoperta è etichettata "From gateway" e utilizza il campo `display_name` dalla risposta quando fornito. Ciò richiede Claude Code v2.1.129 o successivo.

La scoperta si applica solo al formato Anthropic Messages. Non viene eseguita per gli endpoint pass-through Bedrock o Vertex e non viene eseguita quando `ANTHROPIC_BASE_URL` non è impostato o punta a `api.anthropic.com`.

La richiesta di scoperta si autentica nello stesso modo delle richieste di inferenza: invia `ANTHROPIC_AUTH_TOKEN` come token bearer, o `ANTHROPIC_API_KEY` come intestazione `x-api-key` quando nessun token di autenticazione è impostato, insieme a qualsiasi intestazione da `ANTHROPIC_CUSTOM_HEADERS`. Solo i modelli il cui ID inizia con `claude` o `anthropic` vengono aggiunti al selettore. I risultati vengono memorizzati nella cache in `~/.claude/cache/gateway-models.json` e aggiornati a ogni avvio. Se la richiesta non riesce o il gateway non implementa `/v1/models`, il selettore ritorna all'elenco memorizzato nella cache dall'avvio precedente o all'elenco di modelli integrato.

Se il tuo gateway utilizza nomi di modelli che non corrispondono al filtro di scoperta, utilizza le variabili di ambiente documentate in [Configurazione del modello](/it/model-config) per aggiungerli manualmente.

## Configurazione di LiteLLM

<Warning>
  Le versioni PyPI di LiteLLM 1.82.7 e 1.82.8 sono state compromesse con malware che ruba credenziali. Non installare queste versioni. Se le hai già installate:

  * Rimuovi il pacchetto
  * Ruota tutte le credenziali sui sistemi interessati
  * Segui i passaggi di correzione in [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM è un servizio proxy di terze parti. Anthropic non approva, mantiene o controlla la sicurezza o la funzionalità di LiteLLM. Questa guida è fornita a scopo informativo e potrebbe diventare obsoleta. Utilizzala a tua discrezione.
</Warning>

### Prerequisiti

* Claude Code aggiornato all'ultima versione
* LiteLLM Proxy Server distribuito e accessibile
* Accesso ai modelli Claude attraverso il provider scelto

### Configurazione di base di LiteLLM

**Configura Claude Code**:

#### Metodi di autenticazione

##### Chiave API statica

Metodo più semplice utilizzando una chiave API fissa:

```bash theme={null}
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

```bash theme={null}
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

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Imposta l'intervallo di aggiornamento del token:

```bash theme={null}
# Aggiorna ogni ora (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Questo valore verrà inviato come intestazioni `Authorization` e `X-Api-Key`. L'`apiKeyHelper` ha una precedenza inferiore rispetto a `ANTHROPIC_AUTH_TOKEN` o `ANTHROPIC_API_KEY`.

#### Endpoint unificato (consigliato)

Utilizzando l'[endpoint in formato Anthropic](https://docs.litellm.ai/docs/anthropic_unified) di LiteLLM:

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Vantaggi dell'endpoint unificato rispetto agli endpoint pass-through:**

* Bilanciamento del carico
* Fallback
* Supporto coerente per il tracciamento dei costi e il tracciamento dell'utente finale

#### Endpoint pass-through specifici del provider (alternativa)

##### Claude API attraverso LiteLLM

Utilizzando l'[endpoint pass-through](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock attraverso LiteLLM

Utilizzando l'[endpoint pass-through](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI attraverso LiteLLM

Utilizzando l'[endpoint pass-through](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash theme={null}
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
