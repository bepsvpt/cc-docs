> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Panoramica della distribuzione aziendale

> Scopri come Claude Code può integrarsi con vari servizi di terze parti e infrastrutture per soddisfare i requisiti di distribuzione aziendale.

Le organizzazioni possono distribuire Claude Code direttamente tramite Anthropic o tramite un provider cloud. Questa pagina ti aiuta a scegliere la configurazione giusta.

## Confronta le opzioni di distribuzione

Per la maggior parte delle organizzazioni, Claude for Teams o Claude for Enterprise offre la migliore esperienza. I membri del team ottengono accesso sia a Claude Code che a Claude sul web con un'unica sottoscrizione, fatturazione centralizzata e nessuna configurazione dell'infrastruttura richiesta.

**Claude for Teams** è self-service e include funzionalità di collaborazione, strumenti di amministrazione e gestione della fatturazione. Ideale per team più piccoli che hanno bisogno di iniziare rapidamente.

**Claude for Enterprise** aggiunge SSO e domain capture, autorizzazioni basate sui ruoli, accesso all'API di conformità e impostazioni di policy gestite per la distribuzione di configurazioni Claude Code a livello organizzativo. Ideale per organizzazioni più grandi con requisiti di sicurezza e conformità.

Scopri di più su [Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) e [Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

Se la tua organizzazione ha requisiti infrastrutturali specifici, confronta le opzioni di seguito:

<table>
  <thead>
    <tr>
      <th>Funzionalità</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Ideale per</td>
      <td>La maggior parte delle organizzazioni (consigliato)</td>
      <td>Sviluppatori individuali</td>
      <td>Distribuzioni native AWS</td>
      <td>Distribuzioni native GCP</td>
      <td>Distribuzioni native Azure</td>
    </tr>

    <tr>
      <td>Fatturazione</td>
      <td><strong>Teams:</strong> \$150/seat (Premium) con PAYG disponibile<br /><strong>Enterprise:</strong> <a href="https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise">Contatta il team di vendita</a></td>
      <td>PAYG</td>
      <td>PAYG tramite AWS</td>
      <td>PAYG tramite GCP</td>
      <td>PAYG tramite Azure</td>
    </tr>

    <tr>
      <td>Regioni</td>
      <td>Paesi supportati [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Paesi supportati [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Più [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) AWS</td>
      <td>Più [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) GCP</td>
      <td>Più [regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) Azure</td>
    </tr>

    <tr>
      <td>prompt caching</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
      <td>Abilitato per impostazione predefinita</td>
    </tr>

    <tr>
      <td>Autenticazione</td>
      <td>Claude.ai SSO o email</td>
      <td>API key</td>
      <td>API key o credenziali AWS</td>
      <td>Credenziali GCP</td>
      <td>API key o Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Tracciamento dei costi</td>
      <td>Dashboard di utilizzo</td>
      <td>Dashboard di utilizzo</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Include Claude sul web</td>
      <td>Sì</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
    </tr>

    <tr>
      <td>Funzionalità Enterprise</td>
      <td>Gestione del team, SSO, monitoraggio dell'utilizzo</td>
      <td>Nessuna</td>
      <td>Policy IAM, CloudTrail</td>
      <td>Ruoli IAM, Cloud Audit Logs</td>
      <td>Policy RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

Seleziona un'opzione di distribuzione per visualizzare le istruzioni di configurazione:

* [Claude for Teams o Enterprise](/it/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/it/authentication#claude-console-authentication)
* [Amazon Bedrock](/it/amazon-bedrock)
* [Google Vertex AI](/it/google-vertex-ai)
* [Microsoft Foundry](/it/microsoft-foundry)

## Configura proxy e gateway

La maggior parte delle organizzazioni può utilizzare un provider cloud direttamente senza configurazione aggiuntiva. Tuttavia, potrebbe essere necessario configurare un proxy aziendale o un gateway LLM se la tua organizzazione ha requisiti di rete o gestione specifici. Queste sono configurazioni diverse che possono essere utilizzate insieme:

* **Corporate proxy**: Instrada il traffico attraverso un proxy HTTP/HTTPS. Utilizzalo se la tua organizzazione richiede che tutto il traffico in uscita passi attraverso un server proxy per il monitoraggio della sicurezza, la conformità o l'applicazione della policy di rete. Configura con le variabili di ambiente `HTTPS_PROXY` o `HTTP_PROXY`. Scopri di più in [Enterprise network configuration](/it/network-config).
* **LLM Gateway**: Un servizio che si trova tra Claude Code e il provider cloud per gestire l'autenticazione e il routing. Utilizzalo se hai bisogno di tracciamento centralizzato dell'utilizzo tra i team, rate limiting personalizzato o budget, o gestione centralizzata dell'autenticazione. Configura con le variabili di ambiente `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, o `ANTHROPIC_VERTEX_BASE_URL`. Scopri di più in [LLM gateway configuration](/it/llm-gateway).

I seguenti esempi mostrano le variabili di ambiente da impostare nella tua shell o nel profilo shell (`.bashrc`, `.zshrc`). Vedi [Settings](/it/settings) per altri metodi di configurazione.

### Amazon Bedrock

<Tabs>
  <Tab title="Corporate proxy">
    Instrada il traffico Bedrock attraverso il tuo proxy aziendale impostando le seguenti [variabili di ambiente](/it/env-vars):

    ```bash theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=us-east-1

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM Gateway">
    Instrada il traffico Bedrock attraverso il tuo gateway LLM impostando le seguenti [variabili di ambiente](/it/env-vars):

    ```bash theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1

    # Configure LLM gateway
    export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
    export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
    ```
  </Tab>
</Tabs>

### Microsoft Foundry

<Tabs>
  <Tab title="Corporate proxy">
    Instrada il traffico Foundry attraverso il tuo proxy aziendale impostando le seguenti [variabili di ambiente](/it/env-vars):

    ```bash theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1
    export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
    export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Or omit for Entra ID auth

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM Gateway">
    Instrada il traffico Foundry attraverso il tuo gateway LLM impostando le seguenti [variabili di ambiente](/it/env-vars):

    ```bash theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1

    # Configure LLM gateway
    export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
    export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # If gateway handles Azure auth
    ```
  </Tab>
</Tabs>

### Google Vertex AI

<Tabs>
  <Tab title="Corporate proxy">
    Instrada il traffico Vertex AI attraverso il tuo proxy aziendale impostando le seguenti [variabili di ambiente](/it/env-vars):

    ```bash theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM Gateway">
    Instrada il traffico Vertex AI attraverso il tuo gateway LLM impostando le seguenti [variabili di ambiente](/it/env-vars):

    ```bash theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1

    # Configure LLM gateway
    export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
    export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
    ```
  </Tab>
</Tabs>

<Tip>
  Usa `/status` in Claude Code per verificare che la configurazione del proxy e del gateway sia applicata correttamente.
</Tip>

## Best practice per le organizzazioni

### Investi nella documentazione e nella memoria

Ti consigliamo vivamente di investire nella documentazione in modo che Claude Code comprenda il tuo codebase. Le organizzazioni possono distribuire file CLAUDE.md a più livelli:

* **A livello organizzativo**: Distribuisci a directory di sistema come `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) per gli standard a livello aziendale
* **A livello di repository**: Crea file `CLAUDE.md` nelle radici dei repository contenenti l'architettura del progetto, i comandi di build e le linee guida per i contributi. Archivialo nel controllo del codice sorgente in modo che tutti gli utenti ne traggano beneficio

Scopri di più in [Memory and CLAUDE.md files](/it/memory).

### Semplifica la distribuzione

Se hai un ambiente di sviluppo personalizzato, riteniamo che creare un modo "one click" per installare Claude Code sia fondamentale per aumentare l'adozione in tutta l'organizzazione.

### Inizia con un utilizzo guidato

Incoraggia i nuovi utenti a provare Claude Code per domande e risposte sul codebase, o su correzioni di bug più piccole o richieste di funzionalità. Chiedi a Claude Code di fare un piano. Controlla i suggerimenti di Claude e fornisci feedback se è fuori strada. Nel tempo, man mano che gli utenti comprendono meglio questo nuovo paradigma, saranno più efficaci nel permettere a Claude Code di funzionare in modo più agentico.

### Fissa le versioni dei modelli per i provider cloud

Se distribuisci tramite [Bedrock](/it/amazon-bedrock), [Vertex AI](/it/google-vertex-ai), o [Foundry](/it/microsoft-foundry), fissa versioni specifiche dei modelli utilizzando `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, e `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Senza fissare, gli alias dei modelli Claude Code si risolvono nella versione più recente, che può interrompere gli utenti quando Anthropic rilascia un nuovo modello che non è ancora abilitato nel tuo account. Vedi [Model configuration](/it/model-config#pin-models-for-third-party-deployments) per i dettagli.

### Configura le policy di sicurezza

I team di sicurezza possono configurare autorizzazioni gestite per ciò che Claude Code è e non è autorizzato a fare, che non può essere sovrascritto dalla configurazione locale. [Scopri di più](/it/security).

### Sfrutta MCP per le integrazioni

MCP è un ottimo modo per fornire a Claude Code più informazioni, come la connessione a sistemi di gestione dei ticket o log degli errori. Ti consigliamo che un team centrale configuri i server MCP e archivi una configurazione `.mcp.json` nel codebase in modo che tutti gli utenti ne traggano beneficio. [Scopri di più](/it/mcp).

In Anthropic, confidiamo in Claude Code per alimentare lo sviluppo in ogni codebase Anthropic. Speriamo che tu apprezzi l'utilizzo di Claude Code tanto quanto lo facciamo noi.

## Passaggi successivi

Una volta scelto un'opzione di distribuzione e configurato l'accesso per il tuo team:

1. **Distribuisci al tuo team**: Condividi le istruzioni di installazione e fai in modo che i membri del team [installino Claude Code](/it/setup) e si autentichino con le loro credenziali.
2. **Configura la configurazione condivisa**: Crea un [file CLAUDE.md](/it/memory) nei tuoi repository per aiutare Claude Code a comprendere il tuo codebase e gli standard di codifica.
3. **Configura le autorizzazioni**: Rivedi le [impostazioni di sicurezza](/it/security) per definire cosa Claude Code può e non può fare nel tuo ambiente.
