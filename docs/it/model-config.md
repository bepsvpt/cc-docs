> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Configurazione del modello

> Scopri la configurazione del modello Claude Code, inclusi gli alias dei modelli come `opusplan`

## Modelli disponibili

Per l'impostazione `model` in Claude Code, è possibile configurare:

* Un **alias del modello**
* Un **nome del modello**
  * API Anthropic: un **[nome del modello](https://platform.claude.com/docs/it/about-claude/models/overview)** completo
  * Bedrock: un ARN del profilo di inferenza
  * Foundry: un nome di distribuzione
  * Vertex: un nome di versione

### Alias dei modelli

Gli alias dei modelli forniscono un modo conveniente per selezionare le impostazioni del modello senza dover ricordare i numeri di versione esatti:

| Alias del modello | Comportamento                                                                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**     | Valore speciale che cancella qualsiasi override del modello e ripristina il modello consigliato per il tipo di account. Non è di per sé un alias del modello                            |
| **`best`**        | Utilizza il modello più capace disponibile, attualmente equivalente a `opus`                                                                                                            |
| **`sonnet`**      | Utilizza il modello Sonnet più recente (attualmente Sonnet 4.6) per le attività di codifica quotidiane                                                                                  |
| **`opus`**        | Utilizza il modello Opus più recente (attualmente Opus 4.6) per attività di ragionamento complesso                                                                                      |
| **`haiku`**       | Utilizza il modello Haiku veloce ed efficiente per attività semplici                                                                                                                    |
| **`sonnet[1m]`**  | Utilizza Sonnet con una [finestra di contesto di 1 milione di token](https://platform.claude.com/docs/it/build-with-claude/context-windows#1m-token-context-window) per sessioni lunghe |
| **`opus[1m]`**    | Utilizza Opus con una [finestra di contesto di 1 milione di token](https://platform.claude.com/docs/it/build-with-claude/context-windows#1m-token-context-window) per sessioni lunghe   |
| **`opusplan`**    | Modalità speciale che utilizza `opus` durante la Plan Mode, quindi passa a `sonnet` per l'esecuzione                                                                                    |

Gli alias puntano sempre alla versione più recente. Per fissare una versione specifica, utilizzare il nome del modello completo (ad esempio, `claude-opus-4-6`) o impostare la variabile di ambiente corrispondente come `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Impostazione del modello

È possibile configurare il modello in diversi modi, elencati in ordine di priorità:

1. **Durante la sessione** - Utilizzare `/model <alias|name>` per cambiare modello durante la sessione
2. **All'avvio** - Avviare con `claude --model <alias|name>`
3. **Variabile di ambiente** - Impostare `ANTHROPIC_MODEL=<alias|name>`
4. **Impostazioni** - Configurare in modo permanente nel file delle impostazioni utilizzando il campo `model`.

Esempio di utilizzo:

```bash  theme={null}
# Avviare con Opus
claude --model opus

# Passare a Sonnet durante la sessione
/model sonnet
```

File delle impostazioni di esempio:

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Limitare la selezione del modello

Gli amministratori aziendali possono utilizzare `availableModels` nelle [impostazioni gestite o di policy](/it/settings#settings-files) per limitare quali modelli gli utenti possono selezionare.

Quando `availableModels` è impostato, gli utenti non possono passare a modelli non presenti nell'elenco tramite `/model`, il flag `--model`, lo strumento Config o la variabile di ambiente `ANTHROPIC_MODEL`.

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportamento del modello predefinito

L'opzione Predefinito nel selettore di modelli non è interessata da `availableModels`. Rimane sempre disponibile e rappresenta il valore predefinito di runtime del sistema [in base al livello di sottoscrizione dell'utente](#default-model-setting).

Anche con `availableModels: []`, gli utenti possono comunque utilizzare Claude Code con il modello Predefinito per il loro livello.

### Controllare il modello su cui gli utenti eseguono

L'impostazione `model` è una selezione iniziale, non un'applicazione. Imposta quale modello è attivo quando una sessione inizia, ma gli utenti possono comunque aprire `/model` e scegliere Predefinito, che si risolve nel valore predefinito del sistema per il loro livello indipendentemente da ciò che `model` è impostato.

Per controllare completamente l'esperienza del modello, combinare tre impostazioni:

* **`availableModels`**: limita a quali modelli denominati gli utenti possono passare
* **`model`**: imposta la selezione del modello iniziale quando una sessione inizia
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**: controllano a cosa si risolvono l'opzione Predefinito e gli alias `sonnet`, `opus` e `haiku`

Questo esempio avvia gli utenti su Sonnet 4.5, limita il selettore a Sonnet e Haiku, e fissa Predefinito per risolversi a Sonnet 4.5 piuttosto che alla versione più recente:

```json  theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Senza il blocco `env`, un utente che seleziona Predefinito nel selettore otterrebbe la versione Sonnet più recente, bypassando il pin di versione in `model` e `availableModels`.

### Comportamento di unione

Quando `availableModels` è impostato a più livelli, come nelle impostazioni utente e nelle impostazioni del progetto, gli array vengono uniti e deduplicati. Per applicare un elenco di autorizzazione rigoroso, impostare `availableModels` nelle impostazioni gestite o di policy che hanno la priorità più alta.

## Comportamento speciale del modello

### Impostazione del modello `default`

Il comportamento di `default` dipende dal tipo di account:

* **Max e Team Premium**: per impostazione predefinita Opus 4.6
* **Pro e Team Standard**: per impostazione predefinita Sonnet 4.6
* **Enterprise**: Opus 4.6 è disponibile ma non è il valore predefinito

Claude Code potrebbe eseguire automaticamente il fallback a Sonnet se si raggiunge una soglia di utilizzo con Opus.

### Impostazione del modello `opusplan`

L'alias del modello `opusplan` fornisce un approccio ibrido automatizzato:

* **In Plan Mode** - Utilizza `opus` per il ragionamento complesso e le decisioni architettoniche
* **In modalità esecuzione** - Passa automaticamente a `sonnet` per la generazione di codice e l'implementazione

Questo ti dà il meglio di entrambi i mondi: il ragionamento superiore di Opus per la pianificazione e l'efficienza di Sonnet per l'esecuzione.

### Regolare il livello di sforzo

I [livelli di sforzo](https://platform.claude.com/docs/it/build-with-claude/effort) controllano il ragionamento adattivo, che alloca dinamicamente il pensiero in base alla complessità dell'attività. Lo sforzo inferiore è più veloce ed economico per attività semplici, mentre lo sforzo superiore fornisce un ragionamento più profondo per problemi complessi.

Tre livelli persistono tra le sessioni: **low**, **medium** e **high**. Un quarto livello, **max**, fornisce il ragionamento più profondo senza vincoli sulla spesa di token, quindi le risposte sono più lente e costano più di `high`. `max` è disponibile solo su Opus 4.6 e non persiste tra le sessioni tranne tramite la variabile di ambiente `CLAUDE_CODE_EFFORT_LEVEL`.

Opus 4.6 e Sonnet 4.6 per impostazione predefinita utilizzano uno sforzo medio. Questo si applica a tutti i provider, inclusi Bedrock, Vertex AI e l'accesso diretto all'API.

Il livello medio è consigliato per la maggior parte delle attività di codifica: bilancia velocità e profondità di ragionamento, e i livelli superiori possono causare al modello di pensare troppo al lavoro di routine. Riservare `high` o `max` per attività che traggono genuinamente vantaggio da un ragionamento più profondo, come problemi di debug difficili o decisioni architettoniche complesse.

Per un ragionamento profondo una tantum senza modificare l'impostazione della sessione, includere "ultrathink" nel prompt per attivare uno sforzo elevato per quel turno.

**Impostazione dello sforzo:**

* **`/effort`**: eseguire `/effort low`, `/effort medium`, `/effort high` o `/effort max` per cambiare il livello, oppure `/effort auto` per ripristinare il valore predefinito del modello
* **In `/model`**: utilizzare i tasti freccia sinistra/destra per regolare il cursore dello sforzo quando si seleziona un modello
* **Flag `--effort`**: passare `low`, `medium`, `high` o `max` per impostare il livello per una singola sessione quando si avvia Claude Code
* **Variabile di ambiente**: impostare `CLAUDE_CODE_EFFORT_LEVEL` su `low`, `medium`, `high`, `max` o `auto`
* **Impostazioni**: impostare `effortLevel` nel file delle impostazioni su `"low"`, `"medium"` o `"high"`
* **Frontmatter di skill e subagent**: impostare `effort` in un file markdown di [skill](/it/skills#frontmatter-reference) o [subagent](/it/sub-agents#supported-frontmatter-fields) per sovrascrivere il livello di sforzo quando quella skill o subagent viene eseguita

La variabile di ambiente ha la precedenza su tutti gli altri metodi, quindi il livello configurato, quindi il valore predefinito del modello. Lo sforzo del frontmatter si applica quando quella skill o subagent è attiva, sovrascrivendo il livello della sessione ma non la variabile di ambiente.

Lo sforzo è supportato su Opus 4.6 e Sonnet 4.6. Il cursore dello sforzo appare in `/model` quando è selezionato un modello supportato. Il livello di sforzo corrente viene visualizzato anche accanto al logo e al spinner, ad esempio "with low effort", in modo da poter confermare quale impostazione è attiva senza aprire `/model`.

Per disabilitare il ragionamento adattivo su Opus 4.6 e Sonnet 4.6 e ripristinare il budget di pensiero fisso precedente, impostare `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Quando disabilitato, questi modelli utilizzano il budget fisso controllato da `MAX_THINKING_TOKENS`. Vedere [variabili di ambiente](/it/env-vars).

### Contesto esteso

Opus 4.6 e Sonnet 4.6 supportano una [finestra di contesto di 1 milione di token](https://platform.claude.com/docs/it/build-with-claude/context-windows#1m-token-context-window) per sessioni lunghe con basi di codice di grandi dimensioni.

La disponibilità varia in base al modello e al piano. Nei piani Max, Team ed Enterprise, Opus viene automaticamente aggiornato al contesto 1M senza configurazione aggiuntiva. Questo si applica sia ai posti Team Standard che Team Premium.

| Piano                              | Opus 4.6 con contesto 1M                                                                                     | Sonnet 4.6 con contesto 1M                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Max, Team ed Enterprise            | Incluso nell'abbonamento                                                                                     | Richiede [utilizzo extra](https://support.claude.com/it/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                                | Richiede [utilizzo extra](https://support.claude.com/it/articles/12429409-extra-usage-for-paid-claude-plans) | Richiede [utilizzo extra](https://support.claude.com/it/articles/12429409-extra-usage-for-paid-claude-plans) |
| API e pagamento in base al consumo | Accesso completo                                                                                             | Accesso completo                                                                                             |

Per disabilitare completamente il contesto 1M, impostare `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Questo rimuove le varianti di modello 1M dal selettore di modelli. Vedere [variabili di ambiente](/it/env-vars).

La finestra di contesto 1M utilizza i prezzi standard del modello senza premio per i token oltre 200K. Per i piani in cui il contesto esteso è incluso nell'abbonamento, l'utilizzo rimane coperto dall'abbonamento. Per i piani che accedono al contesto esteso tramite utilizzo extra, i token vengono fatturati all'utilizzo extra.

Se l'account supporta il contesto 1M, l'opzione appare nel selettore di modelli (`/model`) nelle versioni più recenti di Claude Code. Se non la vedi, prova a riavviare la sessione.

È anche possibile utilizzare il suffisso `[1m]` con alias di modelli o nomi di modelli completi:

```bash  theme={null}
# Utilizzare l'alias opus[1m] o sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# O aggiungere [1m] a un nome di modello completo
/model claude-opus-4-6[1m]
```

## Verifica del modello corrente

È possibile vedere quale modello stai utilizzando attualmente in diversi modi:

1. Nella [riga di stato](/it/statusline) (se configurata)
2. In `/status`, che visualizza anche le informazioni dell'account.

## Aggiungere un'opzione di modello personalizzato

Utilizzare `ANTHROPIC_CUSTOM_MODEL_OPTION` per aggiungere una singola voce personalizzata al selettore `/model` senza sostituire gli alias incorporati. Questo è utile per distribuzioni di gateway LLM o per testare ID di modello che Claude Code non elenca per impostazione predefinita.

Questo esempio imposta tutte e tre le variabili per rendere selezionabile una distribuzione Opus instradata tramite gateway:

```bash  theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-6"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

La voce personalizzata appare in fondo al selettore `/model`. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` e `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` sono facoltativi. Se omessi, l'ID del modello viene utilizzato come nome e la descrizione per impostazione predefinita è `Custom model (<model-id>)`.

Claude Code salta la convalida per l'ID del modello impostato in `ANTHROPIC_CUSTOM_MODEL_OPTION`, quindi è possibile utilizzare qualsiasi stringa che l'endpoint API accetta.

## Variabili di ambiente

È possibile utilizzare le seguenti variabili di ambiente, che devono essere **nomi di modelli** completi (o equivalenti per il provider API), per controllare i nomi dei modelli a cui gli alias si mappano.

| Variabile di ambiente            | Descrizione                                                                                                |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Il modello da utilizzare per `opus`, o per `opusplan` quando Plan Mode è attivo.                           |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Il modello da utilizzare per `sonnet`, o per `opusplan` quando Plan Mode non è attivo.                     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Il modello da utilizzare per `haiku`, o per [funzionalità in background](/it/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Il modello da utilizzare per [subagents](/it/sub-agents)                                                   |

Nota: `ANTHROPIC_SMALL_FAST_MODEL` è deprecato a favore di `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Fissare i modelli per distribuzioni di terze parti

Quando si distribuisce Claude Code tramite [Bedrock](/it/amazon-bedrock), [Vertex AI](/it/google-vertex-ai) o [Foundry](/it/microsoft-foundry), fissare le versioni dei modelli prima di distribuire agli utenti.

Senza fissaggio, Claude Code utilizza alias di modelli (`sonnet`, `opus`, `haiku`) che si risolvono nella versione più recente. Quando Anthropic rilascia un nuovo modello, gli utenti i cui account non hanno la nuova versione abilitata si interromperanno silenziosamente.

<Warning>
  Impostare tutte e tre le variabili di ambiente del modello su ID di versione specifici come parte della configurazione iniziale. Saltare questo passaggio significa che un aggiornamento di Claude Code può interrompere gli utenti senza alcuna azione da parte tua.
</Warning>

Utilizzare le seguenti variabili di ambiente con ID di modello specifici della versione per il provider:

| Provider  | Esempio                                                                 |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Applicare lo stesso modello per `ANTHROPIC_DEFAULT_SONNET_MODEL` e `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Per gli ID di modello attuali e legacy su tutti i provider, vedere [Panoramica dei modelli](https://platform.claude.com/docs/it/about-claude/models/overview). Per aggiornare gli utenti a una nuova versione del modello, aggiornare queste variabili di ambiente e ridistribuire.

Per abilitare il [contesto esteso](#extended-context) per un modello fissato, aggiungere `[1m]` all'ID del modello in `ANTHROPIC_DEFAULT_OPUS_MODEL` o `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

Il suffisso `[1m]` applica la finestra di contesto 1M a tutto l'utilizzo di quell'alias, incluso `opusplan`. Claude Code rimuove il suffisso prima di inviare l'ID del modello al provider. Aggiungere `[1m]` solo quando il modello sottostante supporta il contesto 1M, come Opus 4.6 o Sonnet 4.6.

<Note>
  L'elenco di autorizzazione `settings.availableModels` si applica comunque quando si utilizzano provider di terze parti. Il filtraggio corrisponde all'alias del modello (`opus`, `sonnet`, `haiku`), non all'ID del modello specifico del provider.
</Note>

### Personalizzare la visualizzazione e le capacità del modello fissato

Quando si fissa un modello su un provider di terze parti, l'ID specifico del provider appare così com'è nel selettore `/model` e Claude Code potrebbe non riconoscere quali funzionalità il modello supporta. È possibile sovrascrivere il nome di visualizzazione e dichiarare le capacità con variabili di ambiente complementari per ogni modello fissato.

Queste variabili hanno effetto solo su provider di terze parti come Bedrock, Vertex AI e Foundry. Non hanno effetto quando si utilizza l'API Anthropic direttamente.

| Variabile di ambiente                                 | Descrizione                                                                                                                                              |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Nome di visualizzazione per il modello Opus fissato nel selettore `/model`. Per impostazione predefinita l'ID del modello quando non impostato           |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Descrizione di visualizzazione per il modello Opus fissato nel selettore `/model`. Per impostazione predefinita `Custom Opus model` quando non impostato |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Elenco separato da virgole delle capacità che il modello Opus fissato supporta                                                                           |

Gli stessi suffissi `_NAME`, `_DESCRIPTION` e `_SUPPORTED_CAPABILITIES` sono disponibili per `ANTHROPIC_DEFAULT_SONNET_MODEL` e `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

Claude Code abilita funzionalità come [livelli di sforzo](#adjust-effort-level) e [extended thinking](/it/common-workflows#use-extended-thinking-thinking-mode) abbinando l'ID del modello rispetto a modelli noti. Gli ID specifici del provider come ARN Bedrock o nomi di distribuzione personalizzati spesso non corrispondono a questi modelli, lasciando le funzionalità supportate disabilitate. Impostare `_SUPPORTED_CAPABILITIES` per dire a Claude Code quali funzionalità il modello effettivamente supporta:

| Valore di capacità     | Abilita                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| `effort`               | [Livelli di sforzo](#adjust-effort-level) e il comando `/effort`                                  |
| `max_effort`           | Il livello di sforzo `max`                                                                        |
| `thinking`             | [Extended thinking](/it/common-workflows#use-extended-thinking-thinking-mode)                     |
| `adaptive_thinking`    | Ragionamento adattivo che alloca dinamicamente il pensiero in base alla complessità dell'attività |
| `interleaved_thinking` | Pensiero tra le chiamate di strumento                                                             |

Quando `_SUPPORTED_CAPABILITIES` è impostato, le capacità elencate sono abilitate e le capacità non elencate sono disabilitate per il modello fissato corrispondente. Quando la variabile non è impostata, Claude Code ricade sulla rilevazione incorporata basata sull'ID del modello.

Questo esempio fissa Opus a un ARN di modello personalizzato Bedrock, imposta un nome amichevole e dichiara le sue capacità:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.6 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Eseguire l'override degli ID di modello per versione

Le variabili di ambiente a livello di famiglia sopra configurano un ID di modello per alias di famiglia. Se è necessario mappare diverse versioni all'interno della stessa famiglia a ID di provider distinti, utilizzare invece l'impostazione `modelOverrides`.

`modelOverrides` mappa i singoli ID di modello Anthropic alle stringhe specifiche del provider che Claude Code invia all'API del provider. Quando un utente seleziona un modello mappato nel selettore `/model`, Claude Code utilizza il valore configurato invece del valore predefinito incorporato.

Questo consente agli amministratori aziendali di instradare ogni versione del modello a un ARN di profilo di inferenza Bedrock specifico, a un nome di versione Vertex AI o a un nome di distribuzione Foundry per governance, allocazione dei costi o instradamento regionale.

Impostare `modelOverrides` nel [file delle impostazioni](/it/settings#settings-files):

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Le chiavi devono essere ID di modello Anthropic come elencati nella [Panoramica dei modelli](https://platform.claude.com/docs/it/about-claude/models/overview). Per gli ID di modello datati, includere il suffisso della data esattamente come appare lì. Le chiavi sconosciute vengono ignorate.

Gli override sostituiscono gli ID di modello incorporati che supportano ogni voce nel selettore `/model`. Su Bedrock, gli override hanno la precedenza su qualsiasi profilo di inferenza che Claude Code scopre automaticamente all'avvio. I valori forniti direttamente tramite `ANTHROPIC_MODEL`, `--model` o le variabili di ambiente `ANTHROPIC_DEFAULT_*_MODEL` vengono passati al provider così come sono e non vengono trasformati da `modelOverrides`.

`modelOverrides` funziona insieme a `availableModels`. L'elenco di autorizzazione viene valutato rispetto all'ID di modello Anthropic, non al valore di override, quindi una voce come `"opus"` in `availableModels` continua a corrispondere anche quando le versioni di Opus sono mappate a ARN.

### Configurazione della prompt caching

Claude Code utilizza automaticamente la [prompt caching](https://platform.claude.com/docs/it/build-with-claude/prompt-caching) per ottimizzare le prestazioni e ridurre i costi. È possibile disabilitare la prompt caching globalmente o per livelli di modello specifici:

| Variabile di ambiente           | Descrizione                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Impostare su `1` per disabilitare la prompt caching per tutti i modelli (ha la precedenza sulle impostazioni per modello) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Impostare su `1` per disabilitare la prompt caching solo per i modelli Haiku                                              |
| `DISABLE_PROMPT_CACHING_SONNET` | Impostare su `1` per disabilitare la prompt caching solo per i modelli Sonnet                                             |
| `DISABLE_PROMPT_CACHING_OPUS`   | Impostare su `1` per disabilitare la prompt caching solo per i modelli Opus                                               |

Queste variabili di ambiente ti danno un controllo granulare sul comportamento della prompt caching. L'impostazione globale `DISABLE_PROMPT_CACHING` ha la precedenza sulle impostazioni specifiche del modello, consentendoti di disabilitare rapidamente tutta la caching quando necessario. Le impostazioni per modello sono utili per il controllo selettivo, ad esempio quando si esegue il debug di modelli specifici o si lavora con provider cloud che potrebbero avere implementazioni di caching diverse.
