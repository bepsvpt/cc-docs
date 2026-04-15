> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Amazon Bedrock

> Scopri come configurare Claude Code tramite Amazon Bedrock, inclusa la configurazione, la configurazione IAM e la risoluzione dei problemi.

## Prerequisiti

Prima di configurare Claude Code con Bedrock, assicurati di avere:

* Un account AWS con accesso a Bedrock abilitato
* Accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.6) in Bedrock
* AWS CLI installato e configurato (facoltativo - necessario solo se non hai un altro meccanismo per ottenere le credenziali)
* Autorizzazioni IAM appropriate

<Note>
  Se stai distribuendo Claude Code a più utenti, [fissa le versioni del tuo modello](#4-pin-model-versions) per evitare interruzioni quando Anthropic rilascia nuovi modelli.
</Note>

## Configurazione

### 1. Invia i dettagli del caso d'uso

I nuovi utenti dei modelli Anthropic devono inviare i dettagli del caso d'uso prima di invocare un modello. Questa operazione viene eseguita una sola volta per account.

1. Assicurati di avere le giuste autorizzazioni IAM (vedi ulteriori informazioni di seguito)
2. Accedi alla [console di Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Seleziona **Chat/Text playground**
4. Scegli un modello Anthropic qualsiasi e ti verrà chiesto di compilare il modulo del caso d'uso

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

Quando Claude Code rileva che le tue credenziali AWS sono scadute (sia localmente in base al loro timestamp che quando Bedrock restituisce un errore di credenziale), eseguirà automaticamente i tuoi comandi `awsAuthRefresh` e/o `awsCredentialExport` configurati per ottenere nuove credenziali prima di riprovare la richiesta.

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

**`awsCredentialExport`**: Usa questo solo se non puoi modificare `.aws` e devi restituire direttamente le credenziali. L'output viene acquisito silenziosamente e non mostrato all'utente. Il comando deve restituire JSON in questo formato:

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

# Facoltativo: Sovrascrivi la regione per il modello piccolo/veloce (Haiku)
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
  Fissa versioni specifiche del modello per ogni distribuzione. Se utilizzi alias di modello (`sonnet`, `opus`, `haiku`) senza fissare, Claude Code potrebbe tentare di utilizzare una versione di modello più recente che non è disponibile nel tuo account Bedrock, interrompendo gli utenti esistenti quando Anthropic rilascia aggiornamenti.
</Warning>

Imposta queste variabili di ambiente su ID di modello Bedrock specifici:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
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
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Utilizzo dell'ARN del profilo di inferenza dell'applicazione
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Facoltativo: Disabilita il caching dei prompt se necessario
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) potrebbe non essere disponibile in tutte le regioni.</Note>

#### Mappa ogni versione del modello a un profilo di inferenza

Le variabili di ambiente `ANTHROPIC_DEFAULT_*_MODEL` configurano un profilo di inferenza per famiglia di modelli. Se la tua organizzazione ha bisogno di esporre diverse versioni della stessa famiglia nel selettore `/model`, ciascuna instradato al suo ARN del profilo di inferenza dell'applicazione, utilizza invece l'impostazione `modelOverrides` nel tuo [file di impostazioni](/it/settings#settings-files).

Questo esempio mappa tre versioni di Opus a ARN distinti in modo che gli utenti possano passare da uno all'altro senza aggirare i profili di inferenza della tua organizzazione:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Quando un utente seleziona una di queste versioni in `/model`, Claude Code chiama Bedrock con l'ARN mappato. Le versioni senza un override tornano all'ID del modello Bedrock integrato o a qualsiasi profilo di inferenza corrispondente scoperto all'avvio. Vedi [Sovrascrivi ID di modello per versione](/it/model-config#override-model-ids-per-version) per i dettagli su come gli override interagiscono con `availableModels` e altre impostazioni del modello.

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
        "bedrock:ListInferenceProfiles"
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

Per i dettagli, vedi [Documentazione IAM di Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Crea un account AWS dedicato per Claude Code per semplificare il tracciamento dei costi e il controllo degli accessi.
</Note>

## Finestra di contesto da 1M token

Claude Opus 4.6 e Sonnet 4.6 supportano la [finestra di contesto da 1M token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) su Amazon Bedrock. Claude Code abilita automaticamente la finestra di contesto estesa quando selezioni una variante di modello da 1M.

Per abilitare la finestra di contesto da 1M per il tuo modello fissato, aggiungi `[1m]` all'ID del modello. Vedi [Fissa i modelli per distribuzioni di terze parti](/it/model-config#pin-models-for-third-party-deployments) per i dettagli.

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

## Risorse aggiuntive

* [Documentazione di Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Prezzi di Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Profili di inferenza di Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code su Amazon Bedrock: Guida di configurazione rapida](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementazione del monitoraggio di Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
