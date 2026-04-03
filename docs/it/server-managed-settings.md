> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurare le impostazioni gestite dal server (beta pubblico)

> Configurare centralmente Claude Code per la vostra organizzazione tramite impostazioni consegnate dal server, senza richiedere infrastrutture di gestione dei dispositivi.

Le impostazioni gestite dal server consentono agli amministratori di configurare centralmente Claude Code tramite un'interfaccia basata sul web su Claude.ai. I client di Claude Code ricevono automaticamente queste impostazioni quando gli utenti si autenticano con le credenziali della loro organizzazione.

Questo approccio è progettato per le organizzazioni che non dispongono di infrastrutture di gestione dei dispositivi, o che hanno la necessità di gestire le impostazioni per gli utenti su dispositivi non gestiti.

<Note>
  Le impostazioni gestite dal server sono in beta pubblico e disponibili per i clienti di [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) e [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise). Le funzionalità potrebbero evolversi prima della disponibilità generale.
</Note>

## Requisiti

Per utilizzare le impostazioni gestite dal server, è necessario:

* Piano Claude for Teams o Claude for Enterprise
* Claude Code versione 2.1.38 o successiva per Claude for Teams, o versione 2.1.30 o successiva per Claude for Enterprise
* Accesso di rete a `api.anthropic.com`

## Scegliere tra impostazioni gestite dal server e gestite dall'endpoint

Claude Code supporta due approcci per la configurazione centralizzata. Le impostazioni gestite dal server forniscono la configurazione dai server di Anthropic. Le [impostazioni gestite dall'endpoint](/it/settings#settings-files) vengono distribuite direttamente ai dispositivi tramite criteri nativi del sistema operativo (preferenze gestite macOS, registro Windows) o file di impostazioni gestiti.

| Approccio                                                             | Ideale per                                                    | Modello di sicurezza                                                                                                                |
| :-------------------------------------------------------------------- | :------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Impostazioni gestite dal server**                                   | Organizzazioni senza MDM, o utenti su dispositivi non gestiti | Impostazioni consegnate dai server di Anthropic al momento dell'autenticazione                                                      |
| **[Impostazioni gestite dall'endpoint](/it/settings#settings-files)** | Organizzazioni con MDM o gestione degli endpoint              | Impostazioni distribuite ai dispositivi tramite profili di configurazione MDM, criteri del registro, o file di impostazioni gestiti |

Se i vostri dispositivi sono registrati in una soluzione MDM o di gestione degli endpoint, le impostazioni gestite dall'endpoint forniscono garanzie di sicurezza più forti perché il file di impostazioni può essere protetto dalla modifica dell'utente a livello del sistema operativo.

## Configurare le impostazioni gestite dal server

<Steps>
  <Step title="Aprire la console di amministrazione">
    In [Claude.ai](https://claude.ai), navigare a **Admin Settings > Claude Code > Managed settings**.
  </Step>

  <Step title="Definire le impostazioni">
    Aggiungere la configurazione come JSON. Tutte le [impostazioni disponibili in `settings.json`](/it/settings#available-settings) sono supportate, inclusi [hooks](/it/hooks), [variabili di ambiente](/it/env-vars), e [impostazioni solo gestite](/it/permissions#managed-only-settings) come `allowManagedPermissionRulesOnly`.

    Questo esempio applica un elenco di negazione delle autorizzazioni, impedisce agli utenti di ignorare le autorizzazioni e limita le regole di autorizzazione a quelle definite nelle impostazioni gestite:

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      },
      "allowManagedPermissionRulesOnly": true
    }
    ```

    Gli hook utilizzano lo stesso formato di `settings.json`.

    Questo esempio esegue uno script di audit dopo ogni modifica di file in tutta l'organizzazione:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    Per configurare il classificatore della [modalità auto](/it/permission-modes#eliminate-prompts-with-auto-mode) in modo che conosca quali repository, bucket e domini la vostra organizzazione ritiene affidabili:

    ```json  theme={null}
    {
      "autoMode": {
        "environment": [
          "Source control: github.example.com/acme-corp and all repos under it",
          "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
          "Trusted internal domains: *.corp.example.com"
        ]
      }
    }
    ```

    Poiché gli hook eseguono comandi shell, gli utenti vedono una [finestra di dialogo di approvazione della sicurezza](#security-approval-dialogs) prima che vengano applicati. Vedere [Configurare il classificatore della modalità auto](/it/permissions#configure-the-auto-mode-classifier) per come le voci `autoMode` influenzano ciò che il classificatore blocca e avvertimenti importanti sui campi `allow` e `soft_deny`.
  </Step>

  <Step title="Salvare e distribuire">
    Salvare le modifiche. I client di Claude Code ricevono le impostazioni aggiornate al prossimo avvio o ciclo di polling orario.
  </Step>
</Steps>

### Verificare la consegna delle impostazioni

Per confermare che le impostazioni vengono applicate, chiedere a un utente di riavviare Claude Code. Se la configurazione include impostazioni che attivano la [finestra di dialogo di approvazione della sicurezza](#security-approval-dialogs), l'utente vede un prompt che descrive le impostazioni gestite all'avvio. È inoltre possibile verificare che le regole di autorizzazione gestite siano attive facendo eseguire a un utente `/permissions` per visualizzare le regole di autorizzazione effettive.

### Controllo di accesso

I seguenti ruoli possono gestire le impostazioni gestite dal server:

* **Primary Owner**
* **Owner**

Limitare l'accesso al personale di fiducia, poiché le modifiche alle impostazioni si applicano a tutti gli utenti dell'organizzazione.

### Impostazioni solo gestite

La maggior parte delle [chiavi di impostazioni](/it/settings#available-settings) funzionano in qualsiasi ambito. Un numero limitato di chiavi viene letto solo dalle impostazioni gestite e non ha alcun effetto quando posizionato nei file di impostazioni dell'utente o del progetto. Vedere [impostazioni solo gestite](/it/permissions#managed-only-settings) per l'elenco completo. Qualsiasi impostazione non in tale elenco può comunque essere posizionata nelle impostazioni gestite e ha la precedenza più alta.

### Limitazioni attuali

Le impostazioni gestite dal server hanno le seguenti limitazioni durante il periodo beta:

* Le impostazioni si applicano uniformemente a tutti gli utenti dell'organizzazione. Le configurazioni per gruppo non sono ancora supportate.
* Le [configurazioni del server MCP](/it/mcp#managed-mcp-configuration) non possono essere distribuite tramite impostazioni gestite dal server.

## Consegna delle impostazioni

### Precedenza delle impostazioni

Le impostazioni gestite dal server e le [impostazioni gestite dall'endpoint](/it/settings#settings-files) occupano entrambe il livello più alto nella [gerarchia delle impostazioni](/it/settings#settings-precedence) di Claude Code. Nessun altro livello di impostazioni può sostituirle, inclusi gli argomenti della riga di comando.

All'interno del livello gestito, la prima fonte che fornisce una configurazione non vuota vince. Le impostazioni gestite dal server vengono controllate per prime, quindi le impostazioni gestite dall'endpoint. Le fonti non si uniscono: se le impostazioni gestite dal server forniscono qualsiasi chiave, le impostazioni gestite dall'endpoint vengono ignorate completamente. Se le impostazioni gestite dal server non forniscono nulla, le impostazioni gestite dall'endpoint si applicano.

Se cancellate la configurazione gestita dal server nella console di amministrazione con l'intenzione di tornare a una plist gestita dall'endpoint o a una politica del registro, tenete presente che le [impostazioni memorizzate nella cache](#fetch-and-caching-behavior) persistono sulle macchine client fino al prossimo recupero riuscito. Eseguite `/status` per vedere quale fonte gestita è attiva.

### Comportamento di recupero e caching

Claude Code recupera le impostazioni dai server di Anthropic all'avvio e esegue il polling per gli aggiornamenti ogni ora durante le sessioni attive.

**Primo avvio senza impostazioni memorizzate nella cache:**

* Claude Code recupera le impostazioni in modo asincrono
* Se il recupero non riesce, Claude Code continua senza impostazioni gestite
* C'è una breve finestra prima che le impostazioni si carichino in cui le restrizioni non sono ancora applicate

**Avvii successivi con impostazioni memorizzate nella cache:**

* Le impostazioni memorizzate nella cache si applicano immediatamente all'avvio
* Claude Code recupera le impostazioni aggiornate in background
* Le impostazioni memorizzate nella cache persistono attraverso i guasti di rete

Claude Code applica gli aggiornamenti delle impostazioni automaticamente senza un riavvio, ad eccezione delle impostazioni avanzate come la configurazione di OpenTelemetry, che richiedono un riavvio completo per avere effetto.

### Finestre di dialogo di approvazione della sicurezza

Determinate impostazioni che potrebbero comportare rischi di sicurezza richiedono l'approvazione esplicita dell'utente prima di essere applicate:

* **Impostazioni dei comandi shell**: impostazioni che eseguono comandi shell
* **Variabili di ambiente personalizzate**: variabili non nell'elenco di sicurezza noto
* **Configurazioni di hook**: qualsiasi definizione di hook

Quando queste impostazioni sono presenti, gli utenti vedono una finestra di dialogo di sicurezza che spiega cosa viene configurato. Gli utenti devono approvare per procedere. Se un utente rifiuta le impostazioni, Claude Code esce.

<Note>
  In modalità non interattiva con il flag `-p`, Claude Code salta le finestre di dialogo di sicurezza e applica le impostazioni senza approvazione dell'utente.
</Note>

## Disponibilità della piattaforma

Le impostazioni gestite dal server richiedono una connessione diretta a `api.anthropic.com` e non sono disponibili quando si utilizzano provider di modelli di terze parti:

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* Endpoint API personalizzati tramite `ANTHROPIC_BASE_URL` o [gateway LLM](/it/llm-gateway)

## Registrazione di audit

Gli eventi del registro di audit per le modifiche alle impostazioni sono disponibili tramite l'API di conformità o l'esportazione del registro di audit. Contattare il vostro team di account Anthropic per l'accesso.

Gli eventi di audit includono il tipo di azione eseguita, l'account e il dispositivo che ha eseguito l'azione, e riferimenti ai valori precedenti e nuovi.

## Considerazioni sulla sicurezza

Le impostazioni gestite dal server forniscono l'applicazione centralizzata dei criteri, ma operano come un controllo lato client. Su dispositivi non gestiti, gli utenti con accesso amministratore o sudo possono modificare il binario di Claude Code, il filesystem, o la configurazione di rete.

| Scenario                                                          | Comportamento                                                                                                                                                    |
| :---------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| L'utente modifica il file di impostazioni memorizzato nella cache | Il file manomesso si applica all'avvio, ma le impostazioni corrette si ripristinano al prossimo recupero dal server                                              |
| L'utente elimina il file di impostazioni memorizzato nella cache  | Si verifica il comportamento del primo avvio: le impostazioni vengono recuperate in modo asincrono con una breve finestra non applicata                          |
| L'API non è disponibile                                           | Le impostazioni memorizzate nella cache si applicano se disponibili, altrimenti le impostazioni gestite non vengono applicate fino al prossimo recupero riuscito |
| L'utente si autentica con un'organizzazione diversa               | Le impostazioni non vengono consegnate per gli account al di fuori dell'organizzazione gestita                                                                   |
| L'utente imposta un `ANTHROPIC_BASE_URL` non predefinito          | Le impostazioni gestite dal server vengono ignorate quando si utilizzano provider API di terze parti                                                             |

Per rilevare le modifiche della configurazione in fase di esecuzione, utilizzare gli [hook `ConfigChange`](/it/hooks#configchange) per registrare le modifiche o bloccare le modifiche non autorizzate prima che abbiano effetto.

Per garanzie di applicazione più forti, utilizzare le [impostazioni gestite dall'endpoint](/it/settings#settings-files) su dispositivi registrati in una soluzione MDM.

## Vedere anche

Pagine correlate per la gestione della configurazione di Claude Code:

* [Settings](/it/settings): riferimento di configurazione completo incluse tutte le impostazioni disponibili
* [Endpoint-managed settings](/it/settings#settings-files): impostazioni gestite distribuite ai dispositivi dal reparto IT
* [Authentication](/it/authentication): configurare l'accesso degli utenti a Claude Code
* [Security](/it/security): salvaguardie di sicurezza e best practice
