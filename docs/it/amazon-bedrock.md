> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Amazon Bedrock

> Scopri come configurare Claude Code tramite Amazon Bedrock, inclusa la configurazione, la configurazione IAM e la risoluzione dei problemi.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

<ContactSalesCard surface="bedrock" />

## Prerequisiti

Prima di configurare Claude Code con Bedrock, assicurati di avere:

* Un account AWS con accesso a Bedrock abilitato
* Accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.6) in Bedrock
* AWS CLI installato e configurato (facoltativo - necessario solo se non hai un altro meccanismo per ottenere le credenziali)
* Autorizzazioni IAM appropriate

Per accedere con le tue credenziali Bedrock, segui [Accedi con Bedrock](#sign-in-with-bedrock) di seguito. Per distribuire Claude Code in un team, utilizza i passaggi di [configurazione manuale](#set-up-manually) e [fissa le versioni del tuo modello](#4-pin-model-versions) prima del rollout.

## Accedi con Bedrock

Se hai credenziali AWS e desideri iniziare a utilizzare Claude Code tramite Bedrock, la procedura guidata di accesso ti guida attraverso i passaggi. Completi i prerequisiti lato AWS una volta per account; la procedura guidata gestisce il lato Claude Code.

<Steps>
  <Step title="Abilita i modelli Anthropic nel tuo account AWS">
    Nella [console di Amazon Bedrock](https://console.aws.amazon.com/bedrock/), apri il catalogo dei modelli, seleziona un modello Anthropic e invia il modulo del caso d'uso. L'accesso viene concesso immediatamente dopo l'invio. Vedi [Invia i dettagli del caso d'uso](#1-submit-use-case-details) per AWS Organizations e [Configurazione IAM](#iam-configuration) per le autorizzazioni di cui il tuo ruolo ha bisogno.
  </Step>

  <Step title="Avvia Claude Code e scegli Bedrock">
    Esegui `claude`. Al prompt di accesso, seleziona **3rd-party platform**, quindi **Amazon Bedrock**.
  </Step>

  <Step title="Segui i prompt della procedura guidata">
    Scegli come autenticarti ad AWS: un profilo AWS rilevato dalla tua directory `~/.aws`, una chiave API Bedrock, una chiave di accesso e un segreto, o credenziali già nel tuo ambiente. La procedura guidata rileva la tua regione, verifica quali modelli Claude il tuo account può invocare, e ti consente di fissarli. Salva il risultato nel blocco `env` del tuo [file di impostazioni utente](/it/settings), quindi non è necessario esportare variabili di ambiente da solo.
  </Step>
</Steps>

Dopo aver effettuato l'accesso, esegui `/setup-bedrock` in qualsiasi momento per riaprire la procedura guidata e modificare le tue credenziali, regione o fissaggi di modello.

## Configurazione manuale

Per configurare Bedrock tramite variabili di ambiente invece della procedura guidata, ad esempio in CI o in un rollout aziendale con script, segui i passaggi di seguito.

### 1. Invia i dettagli del caso d'uso

I nuovi utenti dei modelli Anthropic devono inviare i dettagli del caso d'uso prima di invocare un modello. Questa operazione viene eseguita una sola volta per account AWS.

1. Assicurati di avere le giuste autorizzazioni IAM descritte di seguito
2. Accedi alla [console di Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Seleziona un modello Anthropic dal **catalogo dei modelli**
4. Completa il modulo del caso d'uso. L'accesso viene concesso immediatamente dopo l'invio.

Se utilizzi AWS Organizations, puoi inviare il modulo una sola volta dall'account di gestione utilizzando l'API [`PutUseCaseForModelAccess`](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). Questa chiamata richiede l'autorizzazione IAM `bedrock:PutUseCaseForModelAccess`. L'approvazione si estende agli account figlio automaticamente.

### 2. Configura le credenziali AWS

Claude Code utilizza la catena di credenziali predefinita di AWS SDK. Configura le tue credenziali utilizzando uno di questi metodi:

**Opzione A: Configurazione AWS CLI**

```bash theme={null}
aws configure
```

**Opzione B: Variabili di ambiente (chiave di accesso)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Opzione C: Variabili di ambiente (profilo SSO)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Opzione D: Credenziali della console di gestione AWS**

```bash theme={null}
aws login
```

[Scopri di più](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) su `aws login`.

**Opzione E: Chiavi API Bedrock**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Le chiavi API Bedrock forniscono un metodo di autenticazione più semplice senza la necessità di credenziali AWS complete. [Scopri di più sulle chiavi API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Configurazione avanzata delle credenziali

Claude Code supporta l'aggiornamento automatico delle credenziali per AWS SSO e provider di identità aziendali. Aggiungi queste impostazioni al file di impostazioni di Claude Code (vedi [Impostazioni](/it/settings) per i percorsi dei file).

Queste due impostazioni hanno diverse condizioni di attivazione:

* **`awsAuthRefresh`**: viene eseguito solo quando Claude Code rileva che le tue credenziali AWS sono scadute, sia localmente in base al loro timestamp che quando Bedrock restituisce un errore di credenziale, quindi ritenta la richiesta con credenziali aggiornate.
* **`awsCredentialExport`**: viene eseguito all'avvio della sessione e ad ogni ricaricamento delle credenziali, anche quando le credenziali nel tuo provider di credenziali predefinito di AWS sono ancora valide. Usa questo quando il tuo account Bedrock richiede credenziali tra account che differiscono da quelle che il provider predefinito risolverebbe.

##### Configurazione di esempio

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Impostazioni di configurazione spiegate

**`awsAuthRefresh`**: Usa questo per i comandi che modificano la directory `.aws`, come l'aggiornamento delle credenziali, della cache SSO o dei file di configurazione. L'output del comando viene visualizzato all'utente, ma l'input interattivo non è supportato. Funziona bene per i flussi SSO basati su browser in cui la CLI visualizza un URL o un codice e completi l'autenticazione nel browser.

**`awsCredentialExport`**: Usa questo solo se non puoi modificare `.aws` e devi restituire direttamente le credenziali. Questo comando viene eseguito ogni volta che le credenziali devono essere aggiornate, non solo quando le credenziali sono scadute. L'output viene acquisito silenziosamente e non mostrato all'utente. Il comando deve restituire JSON in questo formato:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configura Claude Code

Imposta le seguenti variabili di ambiente per abilitare Bedrock:

```bash theme={null}
# Abilita integrazione Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # o la tua regione preferita

# Facoltativo: Sovrascrivi la regione per il modello piccolo/veloce (Haiku).
# Si applica anche a Bedrock Mantle.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Facoltativo: Sovrascrivi l'URL dell'endpoint Bedrock per endpoint personalizzati o gateway
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Quando abiliti Bedrock per Claude Code, tieni presente quanto segue:

* `AWS_REGION` è una variabile di ambiente obbligatoria. Claude Code non legge dal file di configurazione `.aws` per questa impostazione.
* Quando si utilizza Bedrock, i comandi `/login` e `/logout` sono disabilitati poiché l'autenticazione viene gestita tramite credenziali AWS.
* Puoi utilizzare file di impostazioni per variabili di ambiente come `AWS_PROFILE` che non desideri perdere in altri processi. Vedi [Impostazioni](/it/settings) per ulteriori informazioni.

### 4. Fissa le versioni del modello

<Warning>
  Fissa versioni specifiche del modello quando distribuisci a più utenti. Senza fissaggio, alias di modello come `sonnet` e `opus` si risolvono nella versione più recente, che potrebbe non essere ancora disponibile nel tuo account Bedrock quando Anthropic rilascia un aggiornamento. Claude Code [ritorna](#startup-model-checks) alla versione precedente all'avvio quando la versione più recente non è disponibile, ma il fissaggio ti consente di controllare quando i tuoi utenti passano a un nuovo modello.
</Warning>

Imposta queste variabili di ambiente su ID di modello Bedrock specifici.

Senza `ANTHROPIC_DEFAULT_OPUS_MODEL`, l'alias `opus` su Bedrock si risolve in Opus 4.6. Impostalo sull'ID di Opus 4.7 per utilizzare il modello più recente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Queste variabili utilizzano ID di profili di inferenza tra regioni (con il prefisso `us.`). Se utilizzi un prefisso di regione diverso o profili di inferenza dell'applicazione, regola di conseguenza. Per gli ID di modello attuali e legacy, vedi [Panoramica dei modelli](https://platform.claude.com/docs/en/about-claude/models/overview). Vedi [Configurazione del modello](/it/model-config#pin-models-for-third-party-deployments) per l'elenco completo delle variabili di ambiente.

Claude Code utilizza questi modelli predefiniti quando non sono impostate variabili di fissaggio:

| Tipo di modello        | Valore predefinito                             |
| :--------------------- | :--------------------------------------------- |
| Modello primario       | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Modello piccolo/veloce | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

Per personalizzare ulteriormente i modelli, utilizza uno di questi metodi:

```bash theme={null}
# Utilizzo dell'ID del profilo di inferenza
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Utilizzo dell'ARN del profilo di inferenza dell'applicazione
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Facoltativo: Disabilita il caching dei prompt se necessario
export DISABLE_PROMPT_CACHING=1

# Facoltativo: Richiedi una TTL della cache dei prompt di 1 ora invece del valore predefinito di 5 minuti
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) potrebbe non essere disponibile in tutte le regioni. Le scritture della cache con una TTL di 1 ora vengono fatturate a una tariffa più alta rispetto alle scritture di 5 minuti.</Note>

#### Mappa ogni versione del modello a un profilo di inferenza

Le variabili di ambiente `ANTHROPIC_DEFAULT_*_MODEL` configurano un profilo di inferenza per famiglia di modelli. Se la tua organizzazione ha bisogno di esporre diverse versioni della stessa famiglia nel selettore `/model`, ciascuna instradato al suo ARN del profilo di inferenza dell'applicazione, utilizza invece l'impostazione `modelOverrides` nel tuo [file di impostazioni](/it/settings#settings-files).

Questo esempio mappa quattro versioni di Opus a ARN distinti in modo che gli utenti possano passare da uno all'altro senza aggirare i profili di inferenza della tua organizzazione:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Quando un utente seleziona una di queste versioni in `/model`, Claude Code chiama Bedrock con l'ARN mappato. Le versioni senza un override tornano all'ID del modello Bedrock integrato o a qualsiasi profilo di inferenza corrispondente scoperto all'avvio. Vedi [Sovrascrivi ID di modello per versione](/it/model-config#override-model-ids-per-version) per i dettagli su come gli override interagiscono con `availableModels` e altre impostazioni del modello.

## Controlli del modello all'avvio

Quando Claude Code si avvia con Bedrock configurato, verifica che i modelli che intende utilizzare siano accessibili nel tuo account. Questo controllo richiede Claude Code v2.1.94 o successivo.

Se hai fissato una versione del modello più vecchia rispetto al valore predefinito corrente di Claude Code, e il tuo account può invocare la versione più recente, Claude Code ti chiede di aggiornare il fissaggio. Accettare scrive il nuovo ID del modello nel tuo [file di impostazioni utente](/it/settings) e riavvia Claude Code. Rifiutare viene ricordato fino al prossimo cambio di versione predefinita. I fissaggi che puntano a un [ARN del profilo di inferenza dell'applicazione](#map-each-model-version-to-an-inference-profile) vengono saltati, poiché sono gestiti dal tuo amministratore.

Se non hai fissato un modello e il valore predefinito corrente non è disponibile nel tuo account, Claude Code ritorna alla versione precedente per la sessione corrente e mostra un avviso. Il fallback non è persistente. Abilita il modello più recente nel tuo account Bedrock o [fissa una versione](#4-pin-model-versions) per rendere la scelta permanente.

## Configurazione IAM

Crea una policy IAM con le autorizzazioni richieste per Claude Code:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

Per autorizzazioni più restrittive, puoi limitare la Resource a ARN di profili di inferenza specifici.

`bedrock:GetInferenceProfile` consente a Claude Code di risolvere un [ARN del profilo di inferenza dell'applicazione](#map-each-model-version-to-an-inference-profile) al suo modello di fondazione di supporto, che viene utilizzato per selezionare la forma di richiesta corretta per quel modello.

Se il token non dispone di questa autorizzazione, Claude Code si recupera automaticamente ritentando una volta con la forma alternativa, quindi le richieste hanno comunque successo ma ogni nuovo modello aggiunge un round-trip aggiuntivo. Concedere l'autorizzazione evita il retry. Questo si applica più spesso alle distribuzioni `AWS_BEARER_TOKEN_BEDROCK`, dove la policy del token è tipicamente più ristretta di un ruolo IAM completo.

Per i dettagli, vedi [Documentazione IAM di Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Crea un account AWS dedicato per Claude Code per semplificare il tracciamento dei costi e il controllo degli accessi.
</Note>

## Finestra di contesto da 1M token

Claude Opus 4.7, Opus 4.6 e Sonnet 4.6 supportano la [finestra di contesto da 1M token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) su Amazon Bedrock. Claude Code abilita automaticamente la finestra di contesto estesa quando selezioni una variante di modello da 1M.

La [procedura guidata di configurazione](#sign-in-with-bedrock) offre un'opzione di contesto da 1M quando fissa i modelli. Per abilitarla per un modello fissato manualmente, aggiungi `[1m]` all'ID del modello. Vedi [Fissa i modelli per distribuzioni di terze parti](/it/model-config#pin-models-for-third-party-deployments) per i dettagli.

## Livelli di servizio

[I livelli di servizio di Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html) ti consentono di scambiare il costo rispetto alla latenza. Imposta `ANTHROPIC_BEDROCK_SERVICE_TIER` su `default`, `flex` o `priority`:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code invia questo come intestazione `X-Amzn-Bedrock-Service-Tier` su ogni richiesta. La disponibilità del livello varia in base al modello e alla regione. La capacità riservata utilizza un [ARN di throughput fornito](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) come ID del modello invece di questa impostazione.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) ti consente di implementare il filtro dei contenuti per Claude Code. Crea un Guardrail nella [console di Amazon Bedrock](https://console.aws.amazon.com/bedrock/), pubblica una versione, quindi aggiungi le intestazioni Guardrail al tuo [file di impostazioni](/it/settings). Abilita l'inferenza tra regioni sul tuo Guardrail se stai utilizzando profili di inferenza tra regioni.

Configurazione di esempio:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Utilizza l'endpoint Mantle

Mantle è un endpoint di Amazon Bedrock che serve i modelli Claude attraverso la forma API nativa di Anthropic piuttosto che l'API Invoke di Bedrock. Utilizza le stesse credenziali AWS, autorizzazioni IAM e configurazione `awsAuthRefresh` descritte in precedenza in questa pagina.

<Note>
  Mantle richiede Claude Code v2.1.94 o successivo. Esegui `claude --version` per verificare.
</Note>

### Abilita Mantle

Con le credenziali AWS già configurate, imposta `CLAUDE_CODE_USE_MANTLE` per instradare le richieste all'endpoint Mantle:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code costruisce l'URL dell'endpoint da `AWS_REGION`. Per sovrascriverlo per un endpoint personalizzato o gateway, imposta `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Esegui `/status` all'interno di Claude Code per confermare. La riga del provider mostra `Amazon Bedrock (Mantle)` quando Mantle è attivo.

### Seleziona un modello Mantle

Mantle utilizza ID di modello con prefisso `anthropic.` e senza suffisso di versione, ad esempio `anthropic.claude-haiku-4-5`. I modelli disponibili per il tuo account dipendono da ciò che la tua organizzazione ha ricevuto; gli ID di modello aggiuntivi sono elencati nei tuoi materiali di onboarding da AWS. Contatta il tuo team di account AWS per richiedere l'accesso ai modelli consentiti.

Imposta il modello con il flag `--model` o con `/model` all'interno di Claude Code:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Esegui Mantle insieme all'API Invoke

I modelli disponibili per te su Mantle potrebbero non includere ogni modello che utilizzi oggi. Impostare sia `CLAUDE_CODE_USE_BEDROCK` che `CLAUDE_CODE_USE_MANTLE` consente a Claude Code di chiamare entrambi gli endpoint dalla stessa sessione. Gli ID di modello che corrispondono al formato Mantle vengono instradati a Mantle, e tutti gli altri ID di modello vanno all'API Invoke di Bedrock.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Per visualizzare un modello Mantle nel selettore `/model`, elenca il suo ID in `availableModels` nel tuo [file di impostazioni](/it/settings). Questa impostazione limita anche il selettore alle voci elencate, quindi includi ogni alias che desideri mantenere disponibile:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Le voci con il prefisso `anthropic.` vengono aggiunte come opzioni del selettore personalizzato e instradate a Mantle. Sostituisci `anthropic.claude-haiku-4-5` con l'ID del modello che il tuo account ha ricevuto. Vedi [Limita la selezione del modello](/it/model-config#restrict-model-selection) per come `availableModels` interagisce con altre impostazioni del modello.

Quando entrambi i provider sono attivi, `/status` mostra `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Instrada Mantle attraverso un gateway

Se la tua organizzazione instrada il traffico del modello attraverso un [gateway LLM](/it/llm-gateway) centralizzato che inietta le credenziali AWS lato server, disabilita l'autenticazione lato client in modo che Claude Code invii richieste senza firme SigV4 o intestazioni `x-api-key`:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Variabili di ambiente Mantle

Queste variabili sono specifiche dell'endpoint Mantle. Vedi [Variabili di ambiente](/it/env-vars) per l'elenco completo.

| Variabile                               | Scopo                                                                                |
| :-------------------------------------- | :----------------------------------------------------------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | Abilita l'endpoint Mantle. Imposta su `1` o `true`.                                  |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Sovrascrivi l'URL dell'endpoint Mantle predefinito                                   |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Salta l'autenticazione lato client per configurazioni proxy                          |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Sovrascrivi la regione AWS per il modello della classe Haiku (condiviso con Bedrock) |

## Risoluzione dei problemi

### Loop di autenticazione con SSO e proxy aziendali

Se le schede del browser si aprono ripetutamente quando si utilizza AWS SSO, rimuovi l'impostazione `awsAuthRefresh` dal tuo [file di impostazioni](/it/settings). Questo può accadere quando le VPN aziendali o i proxy di ispezione TLS interrompono il flusso del browser SSO. Claude Code tratta la connessione interrotta come un errore di autenticazione, riesegue `awsAuthRefresh` e si ripete indefinitamente.

Se il tuo ambiente di rete interferisce con i flussi SSO automatici basati su browser, utilizza `aws sso login` manualmente prima di avviare Claude Code invece di affidarti a `awsAuthRefresh`.

### Problemi di regione

Se riscontri problemi di regione:

* Controlla la disponibilità del modello: `aws bedrock list-inference-profiles --region your-region`
* Passa a una regione supportata: `export AWS_REGION=us-east-1`
* Considera l'utilizzo di profili di inferenza per l'accesso tra regioni

Se ricevi un errore "on-demand throughput isn't supported":

* Specifica il modello come ID di [profilo di inferenza](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code utilizza l'API Bedrock [Invoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) e non supporta l'API Converse.

### Errori dell'endpoint Mantle

Se `/status` non mostra `Amazon Bedrock (Mantle)` dopo aver impostato `CLAUDE_CODE_USE_MANTLE`, la variabile non sta raggiungendo il processo. Conferma che sia esportata nella shell in cui hai lanciato `claude`, o impostala nel blocco `env` del tuo [file di impostazioni](/it/settings).

Un `403` dall'endpoint Mantle con credenziali valide significa che il tuo account AWS non ha ricevuto l'accesso al modello che hai richiesto. Contatta il tuo team di account AWS per richiedere l'accesso.

Un `400` che nomina l'ID del modello significa che quel modello non è servito su Mantle. Mantle ha il suo proprio lineup di modelli separato dal catalogo Bedrock standard, quindi gli ID del profilo di inferenza come `us.anthropic.claude-sonnet-4-6` non funzioneranno. Utilizza un ID nel formato Mantle, o abilita [entrambi gli endpoint](#run-mantle-alongside-the-invoke-api) in modo che Claude Code instrada ogni richiesta all'endpoint in cui il modello è disponibile.

## Risorse aggiuntive

* [Documentazione di Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Prezzi di Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Profili di inferenza di Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Burndown dei token di Bedrock e quote](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code su Amazon Bedrock: Guida di configurazione rapida](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementazione del monitoraggio di Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
