> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

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
| **`default`**     | Impostazione del modello consigliata, a seconda del tipo di account                                                                                                                     |
| **`sonnet`**      | Utilizza l'ultimo modello Sonnet (attualmente Sonnet 4.6) per le attività di codifica quotidiane                                                                                        |
| **`opus`**        | Utilizza l'ultimo modello Opus (attualmente Opus 4.6) per attività di ragionamento complesso                                                                                            |
| **`haiku`**       | Utilizza il modello Haiku veloce ed efficiente per attività semplici                                                                                                                    |
| **`sonnet[1m]`**  | Utilizza Sonnet con una [finestra di contesto di 1 milione di token](https://platform.claude.com/docs/it/build-with-claude/context-windows#1m-token-context-window) per sessioni lunghe |
| **`opusplan`**    | Modalità speciale che utilizza `opus` durante la modalità piano, quindi passa a `sonnet` per l'esecuzione                                                                               |

Gli alias puntano sempre alla versione più recente. Per fissare una versione specifica, utilizzare il nome completo del modello (ad esempio, `claude-opus-4-6`) o impostare la variabile di ambiente corrispondente come `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Impostazione del modello

È possibile configurare il modello in diversi modi, elencati in ordine di priorità:

1. **Durante la sessione** - Utilizzare `/model <alias|name>` per cambiare modello durante la sessione
2. **All'avvio** - Avviare con `claude --model <alias|name>`
3. **Variabile di ambiente** - Impostare `ANTHROPIC_MODEL=<alias|name>`
4. **Impostazioni** - Configurare in modo permanente nel file delle impostazioni utilizzando il campo `model`.

Esempio di utilizzo:

```bash  theme={null}
# Avvia con Opus
claude --model opus

# Passa a Sonnet durante la sessione
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

L'opzione Predefinito nel selettore di modelli non è interessata da `availableModels`. Rimane sempre disponibile e rappresenta il valore predefinito di runtime del sistema [basato sul livello di sottoscrizione dell'utente](#default-model-setting).

Anche con `availableModels: []`, gli utenti possono comunque utilizzare Claude Code con il modello Predefinito per il loro livello.

### Controllare il modello su cui gli utenti eseguono

Per controllare completamente l'esperienza del modello, utilizzare `availableModels` insieme all'impostazione `model`:

* **availableModels**: limita a cosa gli utenti possono passare
* **model**: imposta l'override esplicito del modello, che ha la precedenza sul Predefinito

Questo esempio garantisce che tutti gli utenti eseguano Sonnet 4.6 e possono scegliere solo tra Sonnet e Haiku:

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportamento di unione

Quando `availableModels` è impostato a più livelli, come le impostazioni utente e le impostazioni del progetto, gli array vengono uniti e deduplicati. Per applicare un elenco di autorizzazione rigoroso, impostare `availableModels` nelle impostazioni gestite o di policy che hanno la priorità più alta.

## Comportamento speciale del modello

### Impostazione del modello `default`

Il comportamento di `default` dipende dal tipo di account:

* **Max e Team Premium**: per impostazione predefinita Opus 4.6
* **Pro e Team Standard**: per impostazione predefinita Sonnet 4.6
* **Enterprise**: Opus 4.6 è disponibile ma non è il valore predefinito

Claude Code potrebbe eseguire automaticamente il fallback a Sonnet se si raggiunge una soglia di utilizzo con Opus.

### Impostazione del modello `opusplan`

L'alias del modello `opusplan` fornisce un approccio ibrido automatizzato:

* **In modalità piano** - Utilizza `opus` per il ragionamento complesso e le decisioni architettoniche
* **In modalità esecuzione** - Passa automaticamente a `sonnet` per la generazione di codice e l'implementazione

Questo ti dà il meglio di entrambi i mondi: il ragionamento superiore di Opus per la pianificazione e l'efficienza di Sonnet per l'esecuzione.

### Regolare il livello di sforzo

I [livelli di sforzo](https://platform.claude.com/docs/it/build-with-claude/effort) controllano il ragionamento adattivo, che alloca dinamicamente il pensiero in base alla complessità dell'attività. Lo sforzo inferiore è più veloce ed economico per attività semplici, mentre lo sforzo superiore fornisce un ragionamento più profondo per problemi complessi.

Sono disponibili tre livelli: **low**, **medium** e **high**. Opus 4.6 per impostazione predefinita utilizza uno sforzo medio per gli abbonati Max e Team.

**Impostazione dello sforzo:**

* **In `/model`**: utilizzare i tasti freccia sinistra/destra per regolare il cursore dello sforzo quando si seleziona un modello
* **Variabile di ambiente**: impostare `CLAUDE_CODE_EFFORT_LEVEL=low|medium|high`
* **Impostazioni**: impostare `effortLevel` nel file delle impostazioni

Lo sforzo è supportato su Opus 4.6 e Sonnet 4.6. Il cursore dello sforzo appare in `/model` quando è selezionato un modello supportato. Il livello di sforzo corrente viene visualizzato anche accanto al logo e al spinner (ad esempio, "with low effort"), in modo da poter confermare quale impostazione è attiva senza aprire `/model`.

Per disabilitare il ragionamento adattivo su Opus 4.6 e Sonnet 4.6 e ripristinare il budget di pensiero fisso precedente, impostare `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Se disabilitato, questi modelli utilizzano il budget fisso controllato da `MAX_THINKING_TOKENS`. Vedere [variabili di ambiente](/it/settings#environment-variables).

### Contesto esteso

Opus 4.6 e Sonnet 4.6 supportano una [finestra di contesto di 1 milione di token](https://platform.claude.com/docs/it/build-with-claude/context-windows#1m-token-context-window) per sessioni lunghe con basi di codice di grandi dimensioni.

<Note>
  La finestra di contesto 1M è attualmente in beta. Le funzionalità, i prezzi e la disponibilità potrebbero cambiare.
</Note>

Il contesto esteso è disponibile per:

* **Utenti API e pay-as-you-go**: accesso completo al contesto 1M
* **Abbonati Pro, Max, Teams ed Enterprise**: disponibile con [utilizzo extra](https://support.claude.com/it/articles/12429409-extra-usage-for-paid-claude-plans) abilitato

Per disabilitare completamente il contesto 1M, impostare `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Questo rimuove le varianti del modello 1M dal selettore di modelli. Vedere [variabili di ambiente](/it/settings#environment-variables).

La selezione di un modello 1M non cambia immediatamente la fatturazione. La sessione utilizza tariffe standard fino a quando non supera 200K token di contesto. Oltre 200K token, le richieste vengono addebitate ai [prezzi del contesto lungo](https://platform.claude.com/docs/it/about-claude/pricing#long-context-pricing) con [limiti di velocità](https://platform.claude.com/docs/it/api/rate-limits#long-context-rate-limits) dedicati. Per gli abbonati, i token oltre 200K vengono fatturati come utilizzo extra anziché tramite l'abbonamento.

Se il tuo account supporta il contesto 1M, l'opzione appare nel selettore di modelli (`/model`) nelle versioni più recenti di Claude Code. Se non la vedi, prova a riavviare la sessione.

Puoi anche utilizzare il suffisso `[1m]` con alias di modelli o nomi di modelli completi:

```bash  theme={null}
# Utilizza l'alias sonnet[1m]
/model sonnet[1m]

# Oppure aggiungi [1m] a un nome di modello completo
/model claude-sonnet-4-6[1m]
```

## Verifica del modello corrente

Puoi vedere quale modello stai utilizzando attualmente in diversi modi:

1. Nella [riga di stato](/it/statusline) (se configurata)
2. In `/status`, che visualizza anche le informazioni del tuo account.

## Variabili di ambiente

Puoi utilizzare le seguenti variabili di ambiente, che devono essere **nomi di modelli** completi (o equivalenti per il tuo provider API), per controllare i nomi dei modelli a cui gli alias si mappano.

| Variabile di ambiente            | Descrizione                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Il modello da utilizzare per `opus`, o per `opusplan` quando Plan Mode è attivo.                       |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Il modello da utilizzare per `sonnet`, o per `opusplan` quando Plan Mode non è attivo.                 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Il modello da utilizzare per `haiku`, o [funzionalità in background](/it/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Il modello da utilizzare per [subagents](/it/sub-agents)                                               |

Nota: `ANTHROPIC_SMALL_FAST_MODEL` è deprecato a favore di `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Fissare i modelli per distribuzioni di terze parti

Quando si distribuisce Claude Code tramite [Bedrock](/it/amazon-bedrock), [Vertex AI](/it/google-vertex-ai) o [Foundry](/it/microsoft-foundry), fissare le versioni dei modelli prima di distribuire agli utenti.

Senza fissare, Claude Code utilizza alias di modelli (`sonnet`, `opus`, `haiku`) che si risolvono nella versione più recente. Quando Anthropic rilascia un nuovo modello, gli utenti i cui account non hanno la nuova versione abilitata si interromperanno silenziosamente.

<Warning>
  Imposta tutte e tre le variabili di ambiente del modello su ID di versione specifici come parte della configurazione iniziale. Saltare questo passaggio significa che un aggiornamento di Claude Code può interrompere gli utenti senza alcuna azione da parte tua.
</Warning>

Utilizza le seguenti variabili di ambiente con ID di modello specifici della versione per il tuo provider:

| Provider  | Esempio                                                                 |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Applica lo stesso modello per `ANTHROPIC_DEFAULT_SONNET_MODEL` e `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Per gli ID dei modelli attuali e legacy su tutti i provider, vedere [Panoramica dei modelli](https://platform.claude.com/docs/it/about-claude/models/overview). Per aggiornare gli utenti a una nuova versione del modello, aggiorna queste variabili di ambiente e ridistribuisci.

<Note>
  L'elenco di autorizzazione `settings.availableModels` si applica comunque quando si utilizzano provider di terze parti. Il filtro corrisponde all'alias del modello (`opus`, `sonnet`, `haiku`), non all'ID del modello specifico del provider.
</Note>

### Eseguire l'override degli ID dei modelli per versione

Le variabili di ambiente a livello di famiglia sopra configurano un ID di modello per alias di famiglia. Se è necessario mappare più versioni all'interno della stessa famiglia a ID di provider distinti, utilizzare invece l'impostazione `modelOverrides`.

`modelOverrides` mappa i singoli ID di modelli Anthropic alle stringhe specifiche del provider che Claude Code invia all'API del tuo provider. Quando un utente seleziona un modello mappato nel selettore `/model`, Claude Code utilizza il valore configurato invece del valore predefinito incorporato.

Questo consente agli amministratori aziendali di instradare ogni versione del modello a un ARN del profilo di inferenza Bedrock specifico, a un nome di versione Vertex AI o a un nome di distribuzione Foundry per la governance, l'allocazione dei costi o l'instradamento regionale.

Imposta `modelOverrides` nel tuo [file delle impostazioni](/it/settings#settings-files):

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Le chiavi devono essere ID di modelli Anthropic come elencati nella [Panoramica dei modelli](https://platform.claude.com/docs/it/about-claude/models/overview). Per gli ID dei modelli datati, includere il suffisso della data esattamente come appare lì. Le chiavi sconosciute vengono ignorate.

Gli override sostituiscono gli ID dei modelli incorporati che supportano ogni voce nel selettore `/model`. Su Bedrock, gli override hanno la precedenza su qualsiasi profilo di inferenza che Claude Code scopre automaticamente all'avvio. I valori forniti direttamente tramite `ANTHROPIC_MODEL`, `--model` o le variabili di ambiente `ANTHROPIC_DEFAULT_*_MODEL` vengono passati al provider così come sono e non vengono trasformati da `modelOverrides`.

`modelOverrides` funziona insieme a `availableModels`. L'elenco di autorizzazione viene valutato rispetto all'ID del modello Anthropic, non al valore di override, quindi una voce come `"opus"` in `availableModels` continua a corrispondere anche quando le versioni di Opus vengono mappate agli ARN.

### Configurazione del prompt caching

Claude Code utilizza automaticamente il [prompt caching](https://platform.claude.com/docs/it/build-with-claude/prompt-caching) per ottimizzare le prestazioni e ridurre i costi. Puoi disabilitare il prompt caching globalmente o per livelli di modello specifici:

| Variabile di ambiente           | Descrizione                                                                                                               |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Impostare su `1` per disabilitare il prompt caching per tutti i modelli (ha la precedenza sulle impostazioni per modello) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Impostare su `1` per disabilitare il prompt caching solo per i modelli Haiku                                              |
| `DISABLE_PROMPT_CACHING_SONNET` | Impostare su `1` per disabilitare il prompt caching solo per i modelli Sonnet                                             |
| `DISABLE_PROMPT_CACHING_OPUS`   | Impostare su `1` per disabilitare il prompt caching solo per i modelli Opus                                               |

Queste variabili di ambiente ti danno un controllo granulare sul comportamento del prompt caching. L'impostazione globale `DISABLE_PROMPT_CACHING` ha la precedenza sulle impostazioni specifiche del modello, consentendoti di disabilitare rapidamente tutto il caching quando necessario. Le impostazioni per modello sono utili per il controllo selettivo, ad esempio quando si esegue il debug di modelli specifici o si lavora con provider cloud che potrebbero avere implementazioni di caching diverse.
