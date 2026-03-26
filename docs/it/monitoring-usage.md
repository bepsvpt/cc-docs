> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoraggio

> Scopri come abilitare e configurare OpenTelemetry per Claude Code.

Traccia l'utilizzo di Claude Code, i costi e l'attività degli strumenti in tutta l'organizzazione esportando i dati di telemetria tramite OpenTelemetry (OTel). Claude Code esporta le metriche come dati di serie temporali tramite il protocollo di metriche standard, e gli eventi tramite il protocollo di log/eventi. Configura i tuoi backend di metriche e log per corrispondere ai tuoi requisiti di monitoraggio.

## Avvio rapido

Configura OpenTelemetry utilizzando variabili di ambiente:

```bash  theme={null}
# 1. Abilita la telemetria
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Scegli gli esportatori (entrambi sono facoltativi - configura solo ciò di cui hai bisogno)
export OTEL_METRICS_EXPORTER=otlp       # Opzioni: otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # Opzioni: otlp, console

# 3. Configura l'endpoint OTLP (per l'esportatore OTLP)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Imposta l'autenticazione (se richiesta)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Per il debug: riduci gli intervalli di esportazione
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 secondi (predefinito: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 secondi (predefinito: 5000ms)

# 6. Esegui Claude Code
claude
```

<Note>
  Gli intervalli di esportazione predefiniti sono 60 secondi per le metriche e 5 secondi per i log. Durante la configurazione, potresti voler utilizzare intervalli più brevi per scopi di debug. Ricordati di ripristinare questi valori per l'uso in produzione.
</Note>

Per le opzioni di configurazione complete, consulta la [specifica OpenTelemetry](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Configurazione dell'amministratore

Gli amministratori possono configurare le impostazioni di OpenTelemetry per tutti gli utenti tramite il [file di impostazioni gestite](/it/settings#settings-files). Ciò consente il controllo centralizzato delle impostazioni di telemetria in tutta l'organizzazione. Consulta la [precedenza delle impostazioni](/it/settings#settings-precedence) per ulteriori informazioni su come vengono applicate le impostazioni.

Esempio di configurazione delle impostazioni gestite:

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  Le impostazioni gestite possono essere distribuite tramite MDM (Mobile Device Management) o altre soluzioni di gestione dei dispositivi. Le variabili di ambiente definite nel file di impostazioni gestite hanno una precedenza elevata e non possono essere sovrascritte dagli utenti.
</Note>

## Dettagli della configurazione

### Variabili di configurazione comuni

| Variabile di ambiente                               | Descrizione                                                                                                                                                                          | Valori di esempio                        |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Abilita la raccolta della telemetria (obbligatorio)                                                                                                                                  | `1`                                      |
| `OTEL_METRICS_EXPORTER`                             | Tipi di esportatore di metriche, separati da virgola                                                                                                                                 | `console`, `otlp`, `prometheus`          |
| `OTEL_LOGS_EXPORTER`                                | Tipi di esportatore di log/eventi, separati da virgola                                                                                                                               | `console`, `otlp`                        |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protocollo per l'esportatore OTLP, si applica a tutti i segnali                                                                                                                      | `grpc`, `http/json`, `http/protobuf`     |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | Endpoint del collettore OTLP per tutti i segnali                                                                                                                                     | `http://localhost:4317`                  |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protocollo per le metriche, sostituisce l'impostazione generale                                                                                                                      | `grpc`, `http/json`, `http/protobuf`     |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | Endpoint OTLP per le metriche, sostituisce l'impostazione generale                                                                                                                   | `http://localhost:4318/v1/metrics`       |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protocollo per i log, sostituisce l'impostazione generale                                                                                                                            | `grpc`, `http/json`, `http/protobuf`     |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | Endpoint OTLP per i log, sostituisce l'impostazione generale                                                                                                                         | `http://localhost:4318/v1/logs`          |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Intestazioni di autenticazione per OTLP                                                                                                                                              | `Authorization=Bearer token`             |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Chiave client per l'autenticazione mTLS                                                                                                                                              | Percorso del file della chiave client    |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Certificato client per l'autenticazione mTLS                                                                                                                                         | Percorso del file del certificato client |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Intervallo di esportazione in millisecondi (predefinito: 60000)                                                                                                                      | `5000`, `60000`                          |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Intervallo di esportazione dei log in millisecondi (predefinito: 5000)                                                                                                               | `1000`, `10000`                          |
| `OTEL_LOG_USER_PROMPTS`                             | Abilita la registrazione del contenuto del prompt dell'utente (predefinito: disabilitato)                                                                                            | `1` per abilitare                        |
| `OTEL_LOG_TOOL_DETAILS`                             | Abilita la registrazione degli argomenti di input dello strumento, dei nomi dei server MCP/strumenti e dei nomi delle skill negli eventi degli strumenti (predefinito: disabilitato) | `1` per abilitare                        |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Preferenza di temporalità delle metriche (predefinito: `delta`). Imposta su `cumulative` se il tuo backend prevede temporalità cumulativa                                            | `delta`, `cumulative`                    |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Intervallo per l'aggiornamento delle intestazioni dinamiche (predefinito: 1740000ms / 29 minuti)                                                                                     | `900000`                                 |

### Controllo della cardinalità delle metriche

Le seguenti variabili di ambiente controllano quali attributi sono inclusi nelle metriche per gestire la cardinalità:

| Variabile di ambiente               | Descrizione                                                                | Valore predefinito | Esempio per disabilitare |
| ----------------------------------- | -------------------------------------------------------------------------- | ------------------ | ------------------------ |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Includi l'attributo session.id nelle metriche                              | `true`             | `false`                  |
| `OTEL_METRICS_INCLUDE_VERSION`      | Includi l'attributo app.version nelle metriche                             | `false`            | `true`                   |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Includi gli attributi user.account\_uuid e user.account\_id nelle metriche | `true`             | `false`                  |

Queste variabili aiutano a controllare la cardinalità delle metriche, che influisce sui requisiti di archiviazione e sulle prestazioni delle query nel backend delle metriche. Una cardinalità inferiore generalmente significa prestazioni migliori e costi di archiviazione inferiori, ma dati meno granulari per l'analisi.

### Intestazioni dinamiche

Per gli ambienti aziendali che richiedono autenticazione dinamica, puoi configurare uno script per generare intestazioni dinamicamente:

#### Configurazione delle impostazioni

Aggiungi al tuo `.claude/settings.json`:

```json  theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Requisiti dello script

Lo script deve generare JSON valido con coppie chiave-valore di stringhe che rappresentano intestazioni HTTP:

```bash  theme={null}
#!/bin/bash
# Esempio: Intestazioni multiple
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Comportamento di aggiornamento

Lo script dell'helper di intestazioni viene eseguito all'avvio e periodicamente in seguito per supportare l'aggiornamento dei token. Per impostazione predefinita, lo script viene eseguito ogni 29 minuti. Personalizza l'intervallo con la variabile di ambiente `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Supporto per organizzazioni multi-team

Le organizzazioni con più team o dipartimenti possono aggiungere attributi personalizzati per distinguere tra diversi gruppi utilizzando la variabile di ambiente `OTEL_RESOURCE_ATTRIBUTES`:

```bash  theme={null}
# Aggiungi attributi personalizzati per l'identificazione del team
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Questi attributi personalizzati verranno inclusi in tutte le metriche e gli eventi, permettendoti di:

* Filtrare le metriche per team o dipartimento
* Tracciare i costi per centro di costo
* Creare dashboard specifici per team
* Configurare avvisi per team specifici

<Warning>
  **Requisiti di formattazione importanti per OTEL\_RESOURCE\_ATTRIBUTES:**

  La variabile di ambiente `OTEL_RESOURCE_ATTRIBUTES` utilizza coppie chiave=valore separate da virgola con requisiti di formattazione rigorosi:

  * **Nessuno spazio consentito**: I valori non possono contenere spazi. Ad esempio, `user.organizationName=My Company` non è valido
  * **Formato**: Deve essere coppie chiave=valore separate da virgola: `key1=value1,key2=value2`
  * **Caratteri consentiti**: Solo caratteri US-ASCII escludendo caratteri di controllo, spazi bianchi, virgolette doppie, virgole, punti e virgola e barre rovesciate
  * **Caratteri speciali**: I caratteri al di fuori dell'intervallo consentito devono essere codificati in percentuale

  **Esempi:**

  ```bash  theme={null}
  # ❌ Non valido - contiene spazi
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Valido - usa sottolineature o camelCase invece
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Valido - codifica in percentuale i caratteri speciali se necessario
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Nota: racchiudere i valori tra virgolette non sfugge agli spazi. Ad esempio, `org.name="My Company"` risulta nel valore letterale `"My Company"` (con virgolette incluse), non `My Company`.
</Warning>

### Configurazioni di esempio

Imposta queste variabili di ambiente prima di eseguire `claude`. Ogni blocco mostra una configurazione completa per un diverso esportatore o scenario di distribuzione:

```bash  theme={null}
# Debug della console (intervalli di 1 secondo)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Esportatori multipli
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Endpoint/backend diversi per metriche e log
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Solo metriche (nessun evento/log)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Solo eventi/log (nessuna metrica)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Metriche e eventi disponibili

### Attributi standard

Tutte le metriche e gli eventi condividono questi attributi standard:

| Attributo           | Descrizione                                                                                                                            | Controllato da                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `session.id`        | Identificatore di sessione univoco                                                                                                     | `OTEL_METRICS_INCLUDE_SESSION_ID` (predefinito: true)   |
| `app.version`       | Versione corrente di Claude Code                                                                                                       | `OTEL_METRICS_INCLUDE_VERSION` (predefinito: false)     |
| `organization.id`   | UUID dell'organizzazione (quando autenticato)                                                                                          | Sempre incluso quando disponibile                       |
| `user.account_uuid` | UUID dell'account (quando autenticato)                                                                                                 | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (predefinito: true) |
| `user.account_id`   | ID dell'account in formato taggato corrispondente alle API di amministrazione Anthropic (quando autenticato), come `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (predefinito: true) |
| `user.id`           | Identificatore anonimo del dispositivo/installazione, generato per ogni installazione di Claude Code                                   | Sempre incluso                                          |
| `user.email`        | Indirizzo email dell'utente (quando autenticato tramite OAuth)                                                                         | Sempre incluso quando disponibile                       |
| `terminal.type`     | Tipo di terminale, come `iTerm.app`, `vscode`, `cursor`, o `tmux`                                                                      | Sempre incluso quando rilevato                          |

Gli eventi includono inoltre i seguenti attributi. Questi non vengono mai allegati alle metriche perché causerebbero cardinalità illimitata:

* `prompt.id`: UUID che correla un prompt dell'utente con tutti gli eventi successivi fino al prompt successivo. Vedi [Attributi di correlazione degli eventi](#event-correlation-attributes).
* `workspace.host_paths`: directory dell'area di lavoro host selezionate nell'app desktop, come array di stringhe

### Metriche

Claude Code esporta le seguenti metriche:

| Nome della metrica                    | Descrizione                                                                        | Unità  |
| ------------------------------------- | ---------------------------------------------------------------------------------- | ------ |
| `claude_code.session.count`           | Conteggio delle sessioni CLI avviate                                               | count  |
| `claude_code.lines_of_code.count`     | Conteggio delle righe di codice modificate                                         | count  |
| `claude_code.pull_request.count`      | Numero di pull request create                                                      | count  |
| `claude_code.commit.count`            | Numero di commit git creati                                                        | count  |
| `claude_code.cost.usage`              | Costo della sessione Claude Code                                                   | USD    |
| `claude_code.token.usage`             | Numero di token utilizzati                                                         | tokens |
| `claude_code.code_edit_tool.decision` | Conteggio delle decisioni di autorizzazione dello strumento di modifica del codice | count  |
| `claude_code.active_time.total`       | Tempo attivo totale in secondi                                                     | s      |

### Dettagli delle metriche

Ogni metrica include gli attributi standard elencati sopra. Le metriche con attributi aggiuntivi specifici del contesto sono indicate di seguito.

#### Contatore di sessione

Incrementato all'inizio di ogni sessione.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)

#### Contatore di righe di codice

Incrementato quando il codice viene aggiunto o rimosso.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `type`: (`"added"`, `"removed"`)

#### Contatore di pull request

Incrementato quando si creano pull request tramite Claude Code.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)

#### Contatore di commit

Incrementato quando si creano commit git tramite Claude Code.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)

#### Contatore di costo

Incrementato dopo ogni richiesta API.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `model`: Identificatore del modello (ad esempio, "claude-sonnet-4-6")

#### Contatore di token

Incrementato dopo ogni richiesta API.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Identificatore del modello (ad esempio, "claude-sonnet-4-6")

#### Contatore di decisione dello strumento di modifica del codice

Incrementato quando l'utente accetta o rifiuta l'utilizzo dello strumento Edit, Write o NotebookEdit.

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `tool_name`: Nome dello strumento (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Decisione dell'utente (`"accept"`, `"reject"`)
* `source`: Fonte della decisione - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`
* `language`: Linguaggio di programmazione del file modificato, come `"TypeScript"`, `"Python"`, `"JavaScript"`, o `"Markdown"`. Restituisce `"unknown"` per estensioni di file non riconosciute.

#### Contatore di tempo attivo

Traccia il tempo effettivo trascorso utilizzando attivamente Claude Code, escludendo il tempo di inattività. Questa metrica viene incrementata durante le interazioni dell'utente (digitazione, lettura delle risposte) e durante l'elaborazione CLI (esecuzione degli strumenti, generazione della risposta AI).

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `type`: `"user"` per le interazioni da tastiera, `"cli"` per l'esecuzione degli strumenti e le risposte AI

### Eventi

Claude Code esporta i seguenti eventi tramite log/eventi OpenTelemetry (quando `OTEL_LOGS_EXPORTER` è configurato):

#### Attributi di correlazione degli eventi

Quando un utente invia un prompt, Claude Code potrebbe effettuare più chiamate API ed eseguire diversi strumenti. L'attributo `prompt.id` ti consente di collegare tutti questi eventi al singolo prompt che li ha attivati.

| Attributo   | Descrizione                                                                                                          |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| `prompt.id` | Identificatore UUID v4 che collega tutti gli eventi prodotti durante l'elaborazione di un singolo prompt dell'utente |

Per tracciare tutta l'attività attivata da un singolo prompt, filtra i tuoi eventi per un valore specifico di `prompt.id`. Questo restituisce l'evento user\_prompt, eventuali eventi api\_request, e eventuali eventi tool\_result che si sono verificati durante l'elaborazione di quel prompt.

<Note>
  `prompt.id` è intenzionalmente escluso dalle metriche perché ogni prompt genera un ID univoco, il che creerebbe un numero sempre crescente di serie temporali. Usalo solo per l'analisi a livello di evento e i trail di audit.
</Note>

#### Evento di prompt dell'utente

Registrato quando un utente invia un prompt.

**Nome evento**: `claude_code.user_prompt`

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contatore monotonicamente crescente per ordinare gli eventi all'interno di una sessione
* `prompt_length`: Lunghezza del prompt
* `prompt`: Contenuto del prompt (redatto per impostazione predefinita, abilita con `OTEL_LOG_USER_PROMPTS=1`)

#### Evento di risultato dello strumento

Registrato quando uno strumento completa l'esecuzione.

**Nome evento**: `claude_code.tool_result`

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contatore monotonicamente crescente per ordinare gli eventi all'interno di una sessione
* `tool_name`: Nome dello strumento
* `success`: `"true"` o `"false"`
* `duration_ms`: Tempo di esecuzione in millisecondi
* `error`: Messaggio di errore (se non riuscito)
* `decision_type`: `"accept"` o `"reject"`
* `decision_source`: Fonte della decisione - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`
* `tool_result_size_bytes`: Dimensione del risultato dello strumento in byte
* `mcp_server_scope`: Identificatore dell'ambito del server MCP (per gli strumenti MCP)
* `tool_parameters`: Stringa JSON contenente parametri specifici dello strumento (quando disponibili)
  * Per lo strumento Bash: include `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox`, e `git_commit_id` (lo SHA del commit, quando un comando `git commit` ha successo)
  * Per gli strumenti MCP (quando `OTEL_LOG_TOOL_DETAILS=1`): include `mcp_server_name`, `mcp_tool_name`
  * Per lo strumento Skill (quando `OTEL_LOG_TOOL_DETAILS=1`): include `skill_name`
* `tool_input` (quando `OTEL_LOG_TOOL_DETAILS=1`): Argomenti dello strumento serializzati in JSON. I singoli valori superiori a 512 caratteri vengono troncati, e il payload completo è limitato a circa 4 K caratteri. Si applica a tutti gli strumenti inclusi gli strumenti MCP.

#### Evento di richiesta API

Registrato per ogni richiesta API a Claude.

**Nome evento**: `claude_code.api_request`

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contatore monotonicamente crescente per ordinare gli eventi all'interno di una sessione
* `model`: Modello utilizzato (ad esempio, "claude-sonnet-4-6")
* `cost_usd`: Costo stimato in USD
* `duration_ms`: Durata della richiesta in millisecondi
* `input_tokens`: Numero di token di input
* `output_tokens`: Numero di token di output
* `cache_read_tokens`: Numero di token letti dalla cache
* `cache_creation_tokens`: Numero di token utilizzati per la creazione della cache
* `speed`: `"fast"` o `"normal"`, indicando se la modalità veloce era attiva

#### Evento di errore API

Registrato quando una richiesta API a Claude non riesce.

**Nome evento**: `claude_code.api_error`

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contatore monotonicamente crescente per ordinare gli eventi all'interno di una sessione
* `model`: Modello utilizzato (ad esempio, "claude-sonnet-4-6")
* `error`: Messaggio di errore
* `status_code`: Codice di stato HTTP come stringa, o `"undefined"` per errori non-HTTP
* `duration_ms`: Durata della richiesta in millisecondi
* `attempt`: Numero di tentativo (per le richieste riprovate)
* `speed`: `"fast"` o `"normal"`, indicando se la modalità veloce era attiva

#### Evento di decisione dello strumento

Registrato quando viene presa una decisione di autorizzazione dello strumento (accetta/rifiuta).

**Nome evento**: `claude_code.tool_decision`

**Attributi**:

* Tutti gli [attributi standard](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contatore monotonicamente crescente per ordinare gli eventi all'interno di una sessione
* `tool_name`: Nome dello strumento (ad esempio, "Read", "Edit", "Write", "NotebookEdit")
* `decision`: `"accept"` o `"reject"`
* `source`: Fonte della decisione - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, o `"user_reject"`

## Interpretazione dei dati di metriche e eventi

Le metriche e gli eventi esportati supportano una gamma di analisi:

### Monitoraggio dell'utilizzo

| Metrica                                                       | Opportunità di analisi                                            |
| ------------------------------------------------------------- | ----------------------------------------------------------------- |
| `claude_code.token.usage`                                     | Suddividi per `type` (input/output), utente, team o modello       |
| `claude_code.session.count`                                   | Traccia l'adozione e l'engagement nel tempo                       |
| `claude_code.lines_of_code.count`                             | Misura la produttività tracciando le aggiunte/rimozioni di codice |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Comprendi l'impatto sui flussi di lavoro di sviluppo              |

### Monitoraggio dei costi

La metrica `claude_code.cost.usage` aiuta con:

* Tracciare i trend di utilizzo tra team o individui
* Identificare sessioni ad alto utilizzo per l'ottimizzazione

<Note>
  Le metriche di costo sono approssimazioni. Per i dati di fatturazione ufficiali, consulta il tuo provider API (Claude Console, AWS Bedrock, o Google Cloud Vertex).
</Note>

### Avvisi e segmentazione

Avvisi comuni da considerare:

* Picchi di costo
* Consumo di token inusuale
* Alto volume di sessioni da utenti specifici

Tutte le metriche possono essere segmentate per `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model`, e `app.version`.

### Analisi degli eventi

I dati degli eventi forniscono informazioni dettagliate sulle interazioni di Claude Code:

**Modelli di utilizzo dello strumento**: analizza gli eventi di risultato dello strumento per identificare:

* Strumenti più frequentemente utilizzati
* Tassi di successo dello strumento
* Tempi di esecuzione medi dello strumento
* Modelli di errore per tipo di strumento

**Monitoraggio delle prestazioni**: traccia le durate delle richieste API e i tempi di esecuzione dello strumento per identificare i colli di bottiglia delle prestazioni.

## Considerazioni sul backend

La scelta dei backend di metriche e log determina i tipi di analisi che puoi eseguire:

### Per le metriche

* **Database di serie temporali (ad esempio, Prometheus)**: Calcoli di velocità, metriche aggregate
* **Archivi colonnari (ad esempio, ClickHouse)**: Query complesse, analisi di utenti univoci
* **Piattaforme di osservabilità complete (ad esempio, Honeycomb, Datadog)**: Query avanzate, visualizzazione, avvisi

### Per eventi/log

* **Sistemi di aggregazione dei log (ad esempio, Elasticsearch, Loki)**: Ricerca full-text, analisi dei log
* **Archivi colonnari (ad esempio, ClickHouse)**: Analisi degli eventi strutturati
* **Piattaforme di osservabilità complete (ad esempio, Honeycomb, Datadog)**: Correlazione tra metriche e eventi

Per le organizzazioni che richiedono metriche Daily/Weekly/Monthly Active User (DAU/WAU/MAU), considera backend che supportano query di valori univoci efficienti.

## Informazioni sul servizio

Tutte le metriche e gli eventi vengono esportati con i seguenti attributi di risorsa:

* `service.name`: `claude-code`
* `service.version`: Versione corrente di Claude Code
* `os.type`: Tipo di sistema operativo (ad esempio, `linux`, `darwin`, `windows`)
* `os.version`: Stringa della versione del sistema operativo
* `host.arch`: Architettura dell'host (ad esempio, `amd64`, `arm64`)
* `wsl.version`: Numero di versione WSL (presente solo quando si esegue su Windows Subsystem for Linux)
* Nome del contatore: `com.anthropic.claude_code`

## Risorse di misurazione del ROI

Per una guida completa sulla misurazione del ritorno sull'investimento per Claude Code, inclusa la configurazione della telemetria, l'analisi dei costi, le metriche di produttività e i report automatizzati, consulta la [Guida alla misurazione del ROI di Claude Code](https://github.com/anthropics/claude-code-monitoring-guide). Questo repository fornisce configurazioni Docker Compose pronte all'uso, configurazioni Prometheus e OpenTelemetry, e modelli per generare report di produttività integrati con strumenti come Linear.

## Sicurezza e privacy

* La telemetria è opt-in e richiede una configurazione esplicita
* I contenuti dei file grezzi e i frammenti di codice non sono inclusi nelle metriche o negli eventi. Gli eventi di esecuzione dello strumento includono comandi bash e percorsi di file nel campo `tool_parameters`, che possono contenere valori sensibili. Se i tuoi comandi possono includere segreti, configura il tuo backend di telemetria per filtrare o redarre `tool_parameters`
* Quando autenticato tramite OAuth, `user.email` è incluso negli attributi di telemetria. Se questo è una preoccupazione per la tua organizzazione, lavora con il tuo backend di telemetria per filtrare o redarre questo campo
* Il contenuto del prompt dell'utente non viene raccolto per impostazione predefinita. Viene registrata solo la lunghezza del prompt. Per includere il contenuto del prompt, imposta `OTEL_LOG_USER_PROMPTS=1`
* Gli argomenti di input dello strumento non vengono registrati per impostazione predefinita. Per includerli, imposta `OTEL_LOG_TOOL_DETAILS=1`. Quando abilitato, gli eventi `tool_result` includono i nomi dei server MCP/strumenti e i nomi delle skill più un attributo `tool_input` con percorsi di file, URL, modelli di ricerca e altri argomenti. I singoli valori superiori a 512 caratteri vengono troncati e il totale è limitato a circa 4 K caratteri, ma gli argomenti potrebbero comunque contenere valori sensibili. Configura il tuo backend di telemetria per filtrare o redarre `tool_input` secondo necessità

## Monitoraggio di Claude Code su Amazon Bedrock

Per una guida dettagliata al monitoraggio dell'utilizzo di Claude Code per Amazon Bedrock, consulta [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
