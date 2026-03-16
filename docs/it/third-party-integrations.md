> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Panoramica della distribuzione aziendale

> Scopri come Claude Code può integrarsi con vari servizi di terze parti e infrastrutture per soddisfare i requisiti di distribuzione aziendale.

Questa pagina fornisce una panoramica delle opzioni di distribuzione disponibili e ti aiuta a scegliere la configurazione giusta per la tua organizzazione.

## Confronto dei provider

<table>
  <thead>
    <tr>
      <th>Funzionalità</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Regioni</td>
      <td>Paesi supportati [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Più [regioni](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) AWS</td>
      <td>Più [regioni](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) GCP</td>
      <td>Più [regioni](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) Azure</td>
    </tr>

    <tr>
      <td>Caching dei prompt</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
    </tr>

    <tr>
      <td>Autenticazione</td>
      <td>Chiave API</td>
      <td>Chiave API o credenziali AWS</td>
      <td>Credenziali GCP</td>
      <td>Chiave API o Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Tracciamento dei costi</td>
      <td>Dashboard</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Funzionalità aziendali</td>
      <td>Team, monitoraggio dell'utilizzo</td>
      <td>Criteri IAM, CloudTrail</td>
      <td>Ruoli IAM, Cloud Audit Logs</td>
      <td>Criteri RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Provider cloud

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/it/amazon-bedrock">
    Utilizza i modelli Claude tramite l'infrastruttura AWS con autenticazione basata su chiave API o IAM e monitoraggio nativo di AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/it/google-vertex-ai">
    Accedi ai modelli Claude tramite Google Cloud Platform con sicurezza e conformità di livello aziendale
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/it/microsoft-foundry">
    Accedi a Claude tramite Azure con autenticazione tramite chiave API o Microsoft Entra ID e fatturazione Azure
  </Card>
</CardGroup>

## Infrastruttura aziendale

<CardGroup cols={2}>
  <Card title="Enterprise Network" icon="shield" href="/it/network-config">
    Configura Claude Code per funzionare con i server proxy e i requisiti SSL/TLS della tua organizzazione
  </Card>

  <Card title="LLM Gateway" icon="server" href="/it/llm-gateway">
    Distribuisci l'accesso centralizzato ai modelli con tracciamento dell'utilizzo, budgeting e registrazione di audit
  </Card>
</CardGroup>

## Panoramica della configurazione

Claude Code supporta opzioni di configurazione flessibili che ti permettono di combinare diversi provider e infrastrutture:

<Note>
  Comprendi la differenza tra:

  * **Proxy aziendale**: Un proxy HTTP/HTTPS per l'instradamento del traffico (impostato tramite `HTTPS_PROXY` o `HTTP_PROXY`)
  * **LLM Gateway**: Un servizio che gestisce l'autenticazione e fornisce endpoint compatibili con il provider (impostato tramite `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` o `ANTHROPIC_VERTEX_BASE_URL`)

  Entrambe le configurazioni possono essere utilizzate insieme.
</Note>

### Utilizzo di Bedrock con proxy aziendale

Instrada il traffico Bedrock attraverso un proxy HTTP/HTTPS aziendale:

```bash  theme={null}
# Abilita Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Configura proxy aziendale
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Utilizzo di Bedrock con LLM Gateway

Utilizza un servizio gateway che fornisce endpoint compatibili con Bedrock:

```bash  theme={null}
# Abilita Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configura gateway LLM
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Se il gateway gestisce l'autenticazione AWS
```

### Utilizzo di Foundry con proxy aziendale

Instrada il traffico Azure attraverso un proxy HTTP/HTTPS aziendale:

```bash  theme={null}
# Abilita Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # O ometti per l'autenticazione Entra ID

# Configura proxy aziendale
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Utilizzo di Foundry con LLM Gateway

Utilizza un servizio gateway che fornisce endpoint compatibili con Azure:

```bash  theme={null}
# Abilita Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Configura gateway LLM
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Se il gateway gestisce l'autenticazione Azure
```

### Utilizzo di Vertex AI con proxy aziendale

Instrada il traffico Vertex AI attraverso un proxy HTTP/HTTPS aziendale:

```bash  theme={null}
# Abilita Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Configura proxy aziendale
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Utilizzo di Vertex AI con LLM Gateway

Combina i modelli Google Vertex AI con un gateway LLM per la gestione centralizzata:

```bash  theme={null}
# Abilita Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configura gateway LLM
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Se il gateway gestisce l'autenticazione GCP
```

### Configurazione dell'autenticazione

Claude Code utilizza `ANTHROPIC_AUTH_TOKEN` per l'intestazione `Authorization` quando necessario. I flag `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) vengono utilizzati negli scenari di gateway LLM in cui il gateway gestisce l'autenticazione del provider.

## Scelta della giusta configurazione di distribuzione

Considera questi fattori quando selezioni il tuo approccio di distribuzione:

### Accesso diretto al provider

Ideale per le organizzazioni che:

* Desiderano la configurazione più semplice
* Hanno infrastruttura AWS o GCP esistente
* Hanno bisogno di monitoraggio e conformità nativi del provider

### Proxy aziendale

Ideale per le organizzazioni che:

* Hanno requisiti di proxy aziendale esistenti
* Hanno bisogno di monitoraggio del traffico e conformità
* Devono instradare tutto il traffico attraverso percorsi di rete specifici

### LLM Gateway

Ideale per le organizzazioni che:

* Hanno bisogno di tracciamento dell'utilizzo tra i team
* Desiderano passare dinamicamente tra modelli
* Richiedono limitazione della velocità personalizzata o budget
* Hanno bisogno di gestione dell'autenticazione centralizzata

## Debug

Quando esegui il debug della tua distribuzione:

* Utilizza il [comando slash](/it/slash-commands) `claude /status`. Questo comando fornisce visibilità su qualsiasi autenticazione, proxy e impostazioni URL applicate.
* Imposta la variabile di ambiente `export ANTHROPIC_LOG=debug` per registrare le richieste.

## Best practice per le organizzazioni

### 1. Investire in documentazione e memoria

Ti consigliamo vivamente di investire nella documentazione in modo che Claude Code comprenda il tuo codebase. Le organizzazioni possono distribuire file CLAUDE.md a più livelli:

* **A livello di organizzazione**: Distribuisci in directory di sistema come `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) per gli standard aziendali
* **A livello di repository**: Crea file `CLAUDE.md` nelle radici dei repository contenenti l'architettura del progetto, i comandi di build e le linee guida di contribuzione. Archivialo nel controllo del codice sorgente in modo che tutti gli utenti ne traggano beneficio

  [Scopri di più](/it/memory).

### 2. Semplificare la distribuzione

Se hai un ambiente di sviluppo personalizzato, riteniamo che creare un modo "con un clic" per installare Claude Code sia fondamentale per aumentare l'adozione in tutta l'organizzazione.

### 3. Inizia con un utilizzo guidato

Incoraggia i nuovi utenti a provare Claude Code per domande e risposte sul codebase, o su correzioni di bug più piccole o richieste di funzionalità. Chiedi a Claude Code di fare un piano. Controlla i suggerimenti di Claude e fornisci feedback se non è sulla strada giusta. Nel tempo, man mano che gli utenti comprendono meglio questo nuovo paradigma, saranno più efficaci nel permettere a Claude Code di funzionare in modo più autonomo.

### 4. Configurare i criteri di sicurezza

I team di sicurezza possono configurare autorizzazioni gestite per ciò che Claude Code è e non è autorizzato a fare, che non può essere sovrascritto dalla configurazione locale. [Scopri di più](/it/security).

### 5. Sfruttare MCP per le integrazioni

MCP è un ottimo modo per fornire a Claude Code più informazioni, come la connessione a sistemi di gestione dei ticket o registri di errori. Ti consigliamo che un team centrale configuri i server MCP e archivi una configurazione `.mcp.json` nel codebase in modo che tutti gli utenti ne traggano beneficio. [Scopri di più](/it/mcp).

In Anthropic, confidiamo in Claude Code per alimentare lo sviluppo in ogni codebase di Anthropic. Speriamo che tu apprezzi l'utilizzo di Claude Code quanto lo apprezziamo noi.

## Passaggi successivi

* [Configura Amazon Bedrock](/it/amazon-bedrock) per la distribuzione nativa di AWS
* [Configura Google Vertex AI](/it/google-vertex-ai) per la distribuzione GCP
* [Configura Microsoft Foundry](/it/microsoft-foundry) per la distribuzione Azure
* [Configura Enterprise Network](/it/network-config) per i requisiti di rete
* [Distribuisci LLM Gateway](/it/llm-gateway) per la gestione aziendale
* [Impostazioni](/it/settings) per le opzioni di configurazione e le variabili di ambiente
