> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code GitLab CI/CD

> Scopri come integrare Claude Code nel tuo flusso di lavoro di sviluppo con GitLab CI/CD

<Info>
  Claude Code per GitLab CI/CD è attualmente in beta. Le funzionalità e la funzionalità possono evolversi mentre perfezzioniamo l'esperienza.

  Questa integrazione è mantenuta da GitLab. Per il supporto, consultare il seguente [problema GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/573776).
</Info>

<Note>
  Questa integrazione è costruita sulla base di [Claude Code CLI e Agent SDK](https://platform.claude.com/docs/it/agent-sdk/overview), consentendo l'uso programmatico di Claude nei vostri lavori CI/CD e flussi di lavoro di automazione personalizzati.
</Note>

## Perché utilizzare Claude Code con GitLab?

* **Creazione istantanea di MR**: Descrivete ciò di cui avete bisogno e Claude propone un MR completo con modifiche e spiegazione
* **Implementazione automatizzata**: Trasformate i problemi in codice funzionante con un singolo comando o menzione
* **Consapevole del progetto**: Claude segue le vostre linee guida `CLAUDE.md` e i modelli di codice esistenti
* **Configurazione semplice**: Aggiungete un lavoro a `.gitlab-ci.yml` e una variabile CI/CD mascherata
* **Pronto per l'azienda**: Scegliete Claude API, AWS Bedrock o Google Vertex AI per soddisfare le esigenze di residenza dei dati e approvvigionamento
* **Sicuro per impostazione predefinita**: Viene eseguito nei vostri runner GitLab con la vostra protezione dei rami e approvazioni

## Come funziona

Claude Code utilizza GitLab CI/CD per eseguire attività di intelligenza artificiale in lavori isolati e eseguire il commit dei risultati tramite MR:

1. **Orchestrazione basata su eventi**: GitLab ascolta i trigger scelti (ad esempio, un commento che menziona `@claude` in un problema, MR o thread di revisione). Il lavoro raccoglie il contesto dal thread e dal repository, costruisce prompt da tale input ed esegue Claude Code.

2. **Astrazione del provider**: Utilizzate il provider che si adatta al vostro ambiente:
   * Claude API (SaaS)
   * AWS Bedrock (accesso basato su IAM, opzioni multi-regione)
   * Google Vertex AI (nativo GCP, Workload Identity Federation)

3. **Esecuzione in sandbox**: Ogni interazione viene eseguita in un contenitore con regole rigorose di rete e filesystem. Claude Code applica autorizzazioni con ambito workspace per limitare le scritture. Ogni modifica passa attraverso un MR in modo che i revisori vedano il diff e le approvazioni si applichino ancora.

Scegliete endpoint regionali per ridurre la latenza e soddisfare i requisiti di sovranità dei dati mentre utilizzate gli accordi cloud esistenti.

## Cosa può fare Claude?

Claude Code abilita potenti flussi di lavoro CI/CD che trasformano il modo in cui lavorate con il codice:

* Creare e aggiornare MR da descrizioni di problemi o commenti
* Analizzare regressioni di prestazioni e proporre ottimizzazioni
* Implementare funzionalità direttamente in un ramo, quindi aprire un MR
* Correggere bug e regressioni identificati da test o commenti
* Rispondere ai commenti di follow-up per iterare sulle modifiche richieste

## Configurazione

### Configurazione rapida

Il modo più veloce per iniziare è aggiungere un lavoro minimo al vostro `.gitlab-ci.yml` e impostare la vostra chiave API come variabile mascherata.

1. **Aggiungere una variabile CI/CD mascherata**
   * Andate a **Impostazioni** → **CI/CD** → **Variabili**
   * Aggiungete `ANTHROPIC_API_KEY` (mascherata, protetta secondo necessità)

2. **Aggiungere un lavoro Claude a `.gitlab-ci.yml`**

```yaml  theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  # Regolate le regole per adattarsi a come desiderate attivare il lavoro:
  # - esecuzioni manuali
  # - eventi di merge request
  # - trigger web/API quando un commento contiene '@claude'
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    # Facoltativo: avviare un server GitLab MCP se la vostra configurazione lo fornisce
    - /bin/gitlab-mcp-server || true
    # Utilizzate le variabili AI_FLOW_* quando richiamate tramite trigger web/API con payload di contesto
    - echo "$AI_FLOW_INPUT for $AI_FLOW_CONTEXT on $AI_FLOW_EVENT"
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
```

Dopo aver aggiunto il lavoro e la vostra variabile `ANTHROPIC_API_KEY`, testate eseguendo il lavoro manualmente da **CI/CD** → **Pipeline**, oppure attivate da un MR per consentire a Claude di proporre aggiornamenti in un ramo e aprire un MR se necessario.

<Note>
  Per eseguire su AWS Bedrock o Google Vertex AI invece dell'API Claude, consultate la sezione [Utilizzo con AWS Bedrock e Google Vertex AI](#utilizzo-con-aws-bedrock--google-vertex-ai) di seguito per la configurazione dell'autenticazione e dell'ambiente.
</Note>

### Configurazione manuale (consigliata per la produzione)

Se preferite una configurazione più controllata o avete bisogno di provider aziendali:

1. **Configurare l'accesso al provider**:
   * **Claude API**: Creare e archiviare `ANTHROPIC_API_KEY` come variabile CI/CD mascherata
   * **AWS Bedrock**: **Configurare GitLab** → **AWS OIDC** e creare un ruolo IAM per Bedrock
   * **Google Vertex AI**: **Configurare Workload Identity Federation per GitLab** → **GCP**

2. **Aggiungere credenziali di progetto per le operazioni dell'API GitLab**:
   * Utilizzate `CI_JOB_TOKEN` per impostazione predefinita, oppure create un Project Access Token con ambito `api`
   * Archiviate come `GITLAB_ACCESS_TOKEN` (mascherato) se utilizzate un PAT

3. **Aggiungere il lavoro Claude a `.gitlab-ci.yml`** (vedere gli esempi di seguito)

4. **(Facoltativo) Abilitare trigger basati su menzioni**:
   * Aggiungere un webhook di progetto per "Commenti (note)" al vostro listener di eventi (se ne utilizzate uno)
   * Fare in modo che il listener chiami l'API di attivazione della pipeline con variabili come `AI_FLOW_INPUT` e `AI_FLOW_CONTEXT` quando un commento contiene `@claude`

## Esempi di casi d'uso

### Trasformare i problemi in MR

In un commento di problema:

```text  theme={null}
@claude implement this feature based on the issue description
```

Claude analizza il problema e la base di codice, scrive le modifiche in un ramo e apre un MR per la revisione.

### Ottenere aiuto nell'implementazione

In una discussione MR:

```text  theme={null}
@claude suggest a concrete approach to cache the results of this API call
```

Claude propone modifiche, aggiunge codice con caching appropriato e aggiorna il MR.

### Correggere i bug rapidamente

In un commento di problema o MR:

```text  theme={null}
@claude fix the TypeError in the user dashboard component
```

Claude individua il bug, implementa una correzione e aggiorna il ramo o apre un nuovo MR.

## Utilizzo con AWS Bedrock e Google Vertex AI

Per ambienti aziendali, potete eseguire Claude Code interamente sulla vostra infrastruttura cloud con la stessa esperienza per gli sviluppatori.

<Tabs>
  <Tab title="AWS Bedrock">
    ### Prerequisiti

    Prima di configurare Claude Code con AWS Bedrock, avete bisogno di:

    1. Un account AWS con accesso ad Amazon Bedrock ai modelli Claude desiderati
    2. GitLab configurato come provider di identità OIDC in AWS IAM
    3. Un ruolo IAM con autorizzazioni Bedrock e una politica di trust limitata al vostro progetto/rami GitLab
    4. Variabili CI/CD GitLab per l'assunzione del ruolo:
       * `AWS_ROLE_TO_ASSUME` (ARN del ruolo)
       * `AWS_REGION` (regione Bedrock)

    ### Istruzioni di configurazione

    Configurate AWS per consentire ai lavori CI di GitLab di assumere un ruolo IAM tramite OIDC (nessuna chiave statica).

    **Configurazione richiesta:**

    1. Abilitare Amazon Bedrock e richiedere l'accesso ai vostri modelli Claude target
    2. Creare un provider OIDC IAM per GitLab se non già presente
    3. Creare un ruolo IAM attendibile dal provider OIDC di GitLab, limitato al vostro progetto e rami protetti
    4. Allegare autorizzazioni con privilegi minimi per le API di invocazione Bedrock

    **Valori richiesti da archiviare nelle variabili CI/CD:**

    * `AWS_ROLE_TO_ASSUME`
    * `AWS_REGION`

    Aggiungete le variabili in Impostazioni → CI/CD → Variabili:

    ```yaml  theme={null}
    # Per AWS Bedrock:
    - AWS_ROLE_TO_ASSUME
    - AWS_REGION
    ```

    Utilizzate l'esempio di lavoro AWS Bedrock sopra per scambiare il token di lavoro GitLab con credenziali AWS temporanee in fase di esecuzione.
  </Tab>

  <Tab title="Google Vertex AI">
    ### Prerequisiti

    Prima di configurare Claude Code con Google Vertex AI, avete bisogno di:

    1. Un progetto Google Cloud con:
       * API Vertex AI abilitata
       * Workload Identity Federation configurata per attendere OIDC di GitLab
    2. Un account di servizio dedicato con solo i ruoli Vertex AI richiesti
    3. Variabili CI/CD GitLab per WIF:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER` (nome completo della risorsa)
       * `GCP_SERVICE_ACCOUNT` (email dell'account di servizio)

    ### Istruzioni di configurazione

    Configurate Google Cloud per consentire ai lavori CI di GitLab di rappresentare un account di servizio tramite Workload Identity Federation.

    **Configurazione richiesta:**

    1. Abilitare API IAM Credentials, STS API e Vertex AI API
    2. Creare un Workload Identity Pool e un provider per OIDC di GitLab
    3. Creare un account di servizio dedicato con ruoli Vertex AI
    4. Concedere al principale WIF l'autorizzazione per rappresentare l'account di servizio

    **Valori richiesti da archiviare nelle variabili CI/CD:**

    * `GCP_WORKLOAD_IDENTITY_PROVIDER`
    * `GCP_SERVICE_ACCOUNT`

    Aggiungete le variabili in Impostazioni → CI/CD → Variabili:

    ```yaml  theme={null}
    # Per Google Vertex AI:
    - GCP_WORKLOAD_IDENTITY_PROVIDER
    - GCP_SERVICE_ACCOUNT
    - CLOUD_ML_REGION (ad esempio, us-east5)
    ```

    Utilizzate l'esempio di lavoro Google Vertex AI sopra per autenticarvi senza archiviare le chiavi.
  </Tab>
</Tabs>

## Esempi di configurazione

Di seguito sono riportati frammenti pronti all'uso che potete adattare alla vostra pipeline.

### .gitlab-ci.yml di base (Claude API)

```yaml  theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Summarize recent changes and suggest improvements'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  # Claude Code utilizzerà ANTHROPIC_API_KEY dalle variabili CI/CD
```

### Esempio di lavoro AWS Bedrock (OIDC)

**Prerequisiti:**

* Amazon Bedrock abilitato con accesso ai vostri modelli Claude scelti
* OIDC di GitLab configurato in AWS con un ruolo che attendibile al vostro progetto e rami GitLab
* Ruolo IAM con autorizzazioni Bedrock (privilegi minimi consigliati)

**Variabili CI/CD richieste:**

* `AWS_ROLE_TO_ASSUME`: ARN del ruolo IAM per l'accesso a Bedrock
* `AWS_REGION`: Regione Bedrock (ad esempio, `us-west-2`)

```yaml  theme={null}
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Scambiare il token OIDC di GitLab con credenziali AWS
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implement the requested changes and open an MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

<Note>
  Gli ID modello per Bedrock includono prefissi specifici della regione (ad esempio, `us.anthropic.claude-sonnet-4-6`). Passate il modello desiderato tramite la configurazione del lavoro o il prompt se il vostro flusso di lavoro lo supporta.
</Note>

### Esempio di lavoro Google Vertex AI (Workload Identity Federation)

**Prerequisiti:**

* API Vertex AI abilitata nel vostro progetto GCP
* Workload Identity Federation configurata per attendere OIDC di GitLab
* Un account di servizio con autorizzazioni Vertex AI

**Variabili CI/CD richieste:**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Nome completo della risorsa del provider
* `GCP_SERVICE_ACCOUNT`: Email dell'account di servizio
* `CLOUD_ML_REGION`: Regione Vertex (ad esempio, `us-east5`)

```yaml  theme={null}
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apt-get update && apt-get install -y git && apt-get clean
    - curl -fsSL https://claude.ai/install.sh | bash
    # Autenticarsi a Google Cloud tramite WIF (nessuna chiave scaricata)
    - >
      gcloud auth login --cred-file=<(cat <<EOF
      {
        "type": "external_account",
        "audience": "${GCP_WORKLOAD_IDENTITY_PROVIDER}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken",
        "token_url": "https://sts.googleapis.com/v1/token"
      }
      EOF
      )
    - gcloud config set project "$(gcloud projects list --format='value(projectId)' --filter="name:${CI_PROJECT_NAMESPACE}" | head -n1)" || true
  script:
    - /bin/gitlab-mcp-server || true
    - >
      CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}"
      claude
      -p "${AI_FLOW_INPUT:-'Review and update code as requested'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    CLOUD_ML_REGION: "us-east5"
```

<Note>
  Con Workload Identity Federation, non è necessario archiviare le chiavi dell'account di servizio. Utilizzate condizioni di trust specifiche del repository e account di servizio con privilegi minimi.
</Note>

## Best practice

### Configurazione CLAUDE.md

Create un file `CLAUDE.md` nella radice del repository per definire standard di codifica, criteri di revisione e regole specifiche del progetto. Claude legge questo file durante le esecuzioni e segue le vostre convenzioni quando propone modifiche.

### Considerazioni sulla sicurezza

**Non eseguite mai il commit di chiavi API o credenziali cloud nel vostro repository**. Utilizzate sempre le variabili CI/CD di GitLab:

* Aggiungete `ANTHROPIC_API_KEY` come variabile mascherata (e proteggetela se necessario)
* Utilizzate OIDC specifico del provider dove possibile (nessuna chiave di lunga durata)
* Limitate le autorizzazioni dei lavori e l'uscita di rete
* Revisionate i MR di Claude come qualsiasi altro contributore

### Ottimizzazione delle prestazioni

* Mantenete `CLAUDE.md` focalizzato e conciso
* Fornite descrizioni chiare di problemi/MR per ridurre le iterazioni
* Configurate timeout di lavoro ragionevoli per evitare esecuzioni incontrollate
* Memorizzate nella cache npm e installazioni di pacchetti nei runner dove possibile

### Costi CI

Quando utilizzate Claude Code con GitLab CI/CD, siate consapevoli dei costi associati:

* **Tempo del runner GitLab**:
  * Claude viene eseguito sui vostri runner GitLab e consuma minuti di calcolo
  * Consultate la fatturazione del runner del vostro piano GitLab per i dettagli

* **Costi API**:
  * Ogni interazione Claude consuma token in base alla dimensione del prompt e della risposta
  * L'utilizzo dei token varia in base alla complessità dell'attività e alla dimensione della base di codice
  * Consultate [Prezzi Anthropic](https://platform.claude.com/docs/it/about-claude/pricing) per i dettagli

* **Suggerimenti per l'ottimizzazione dei costi**:
  * Utilizzate comandi `@claude` specifici per ridurre i turni non necessari
  * Impostate valori `max_turns` e timeout di lavoro appropriati
  * Limitate la concorrenza per controllare le esecuzioni parallele

## Sicurezza e governance

* Ogni lavoro viene eseguito in un contenitore isolato con accesso di rete limitato
* Le modifiche di Claude passano attraverso MR in modo che i revisori vedano ogni diff
* Le regole di protezione dei rami e approvazione si applicano al codice generato da IA
* Claude Code utilizza autorizzazioni con ambito workspace per limitare le scritture
* I costi rimangono sotto il vostro controllo perché portate le vostre credenziali del provider

## Risoluzione dei problemi

### Claude non risponde ai comandi @claude

* Verificate che la vostra pipeline sia attivata (manualmente, evento MR o tramite listener di note/webhook)
* Assicuratevi che le variabili CI/CD (`ANTHROPIC_API_KEY` o impostazioni del provider cloud) siano presenti e non mascherate
* Controllate che il commento contenga `@claude` (non `/claude`) e che il vostro trigger di menzione sia configurato

### Il lavoro non può scrivere commenti o aprire MR

* Assicuratevi che `CI_JOB_TOKEN` abbia autorizzazioni sufficienti per il progetto, oppure utilizzate un Project Access Token con ambito `api`
* Controllate che lo strumento `mcp__gitlab` sia abilitato in `--allowedTools`
* Confermate che il lavoro viene eseguito nel contesto del MR o abbia contesto sufficiente tramite variabili `AI_FLOW_*`

### Errori di autenticazione

* **Per Claude API**: Confermate che `ANTHROPIC_API_KEY` sia valida e non scaduta
* **Per Bedrock/Vertex**: Verificate la configurazione OIDC/WIF, l'impersonificazione del ruolo e i nomi segreti; confermate la disponibilità della regione e del modello

## Configurazione avanzata

### Parametri e variabili comuni

Claude Code supporta questi input comunemente utilizzati:

* `prompt` / `prompt_file`: Fornite istruzioni inline (`-p`) o tramite un file
* `max_turns`: Limitate il numero di iterazioni avanti e indietro
* `timeout_minutes`: Limitate il tempo di esecuzione totale
* `ANTHROPIC_API_KEY`: Richiesto per l'API Claude (non utilizzato per Bedrock/Vertex)
* Ambiente specifico del provider: `AWS_REGION`, variabili di progetto/regione per Vertex

<Note>
  I flag e i parametri esatti possono variare in base alla versione di `@anthropic-ai/claude-code`. Eseguite `claude --help` nel vostro lavoro per vedere le opzioni supportate.
</Note>

### Personalizzazione del comportamento di Claude

Potete guidare Claude in due modi principali:

1. **CLAUDE.md**: Definite standard di codifica, requisiti di sicurezza e convenzioni di progetto. Claude legge questo durante le esecuzioni e segue le vostre regole.
2. **Prompt personalizzati**: Passate istruzioni specifiche dell'attività tramite `prompt`/`prompt_file` nel lavoro. Utilizzate prompt diversi per lavori diversi (ad esempio, revisione, implementazione, refactoring).
