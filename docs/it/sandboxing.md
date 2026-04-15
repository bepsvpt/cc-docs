> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sandboxing

> Scopri come lo strumento bash in sandbox di Claude Code fornisce isolamento del filesystem e della rete per un'esecuzione dell'agente più sicura e autonoma.

## Panoramica

Claude Code include il sandboxing nativo per fornire un ambiente più sicuro per l'esecuzione dell'agente, riducendo la necessità di prompt di autorizzazione costanti. Invece di chiedere autorizzazione per ogni comando bash, il sandboxing crea confini definiti in anticipo dove Claude Code può lavorare più liberamente con rischio ridotto.

Lo strumento bash in sandbox utilizza primitive a livello del sistema operativo per applicare sia l'isolamento del filesystem che della rete.

## Perché il sandboxing è importante

La sicurezza tradizionale basata su autorizzazioni richiede l'approvazione costante dell'utente per i comandi bash. Sebbene questo fornisca controllo, può portare a:

* **Affaticamento da approvazione**: Fare clic ripetutamente su "approva" può causare agli utenti di prestare meno attenzione a ciò che stanno approvando
* **Produttività ridotta**: Le interruzioni costanti rallentano i flussi di lavoro di sviluppo
* **Autonomia limitata**: Claude Code non può lavorare in modo efficiente quando è in attesa di approvazioni

Il sandboxing affronta queste sfide:

1. **Definendo confini chiari**: Specifica esattamente quali directory e host di rete Claude Code può accedere
2. **Riducendo i prompt di autorizzazione**: I comandi sicuri all'interno della sandbox non richiedono approvazione
3. **Mantenendo la sicurezza**: I tentativi di accedere a risorse al di fuori della sandbox attivano notifiche immediate
4. **Abilitando l'autonomia**: Claude Code può funzionare più indipendentemente entro limiti definiti

<Warning>
  Il sandboxing efficace richiede **sia** l'isolamento del filesystem che della rete. Senza isolamento della rete, un agente compromesso potrebbe esfiltare file sensibili come chiavi SSH. Senza isolamento del filesystem, un agente compromesso potrebbe backdoor le risorse di sistema per ottenere accesso alla rete. Quando si configura il sandboxing è importante assicurarsi che le impostazioni configurate non creino bypass in questi sistemi.
</Warning>

## Come funziona

### Isolamento del filesystem

Lo strumento bash in sandbox limita l'accesso al file system a directory specifiche:

* **Comportamento di scrittura predefinito**: Accesso in lettura e scrittura alla directory di lavoro corrente e alle sue sottodirectory
* **Comportamento di lettura predefinito**: Accesso in lettura all'intero computer, ad eccezione di determinate directory negate
* **Accesso bloccato**: Non è possibile modificare file al di fuori della directory di lavoro corrente senza autorizzazione esplicita
* **Configurabile**: Definisci percorsi consentiti e negati personalizzati tramite le impostazioni

È possibile concedere l'accesso in scrittura a percorsi aggiuntivi utilizzando `sandbox.filesystem.allowWrite` nelle impostazioni. Queste restrizioni sono applicate a livello del sistema operativo (Seatbelt su macOS, bubblewrap su Linux), quindi si applicano a tutti i comandi dei sottoprocessi, inclusi strumenti come `kubectl`, `terraform` e `npm`, non solo agli strumenti di file di Claude.

### Isolamento della rete

L'accesso alla rete è controllato tramite un server proxy in esecuzione al di fuori della sandbox:

* **Restrizioni di dominio**: Solo i domini approvati possono essere accessibili
* **Conferma dell'utente**: Le nuove richieste di dominio attivano prompt di autorizzazione (a meno che [`allowManagedDomainsOnly`](/it/settings#sandbox-settings) non sia abilitato, che blocca automaticamente i domini non consentiti)
* **Supporto proxy personalizzato**: Gli utenti avanzati possono implementare regole personalizzate sul traffico in uscita
* **Copertura completa**: Le restrizioni si applicano a tutti gli script, programmi e sottoprocessi generati dai comandi

### Applicazione a livello del sistema operativo

Lo strumento bash in sandbox sfrutta le primitive di sicurezza del sistema operativo:

* **macOS**: Utilizza Seatbelt per l'applicazione della sandbox
* **Linux**: Utilizza [bubblewrap](https://github.com/containers/bubblewrap) per l'isolamento
* **WSL2**: Utilizza bubblewrap, come Linux

WSL1 non è supportato perché bubblewrap richiede funzionalità del kernel disponibili solo in WSL2.

Queste restrizioni a livello del sistema operativo assicurano che tutti i processi figlio generati dai comandi di Claude Code ereditino gli stessi confini di sicurezza.

## Iniziare

### Prerequisiti

Su **macOS**, il sandboxing funziona subito utilizzando il framework Seatbelt integrato.

Su **Linux e WSL2**, installa prima i pacchetti richiesti:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

### Abilita il sandboxing

È possibile abilitare il sandboxing eseguendo il comando `/sandbox`:

```text theme={null}
/sandbox
```

Questo apre un menu in cui è possibile scegliere tra le modalità sandbox. Se le dipendenze richieste sono mancanti (come `bubblewrap` o `socat` su Linux), il menu visualizza le istruzioni di installazione per la piattaforma.

Per impostazione predefinita, se la sandbox non può avviarsi (dipendenze mancanti, piattaforma non supportata o restrizioni della piattaforma), Claude Code mostra un avviso ed esegue i comandi senza sandboxing. Per rendere questo un errore grave, imposta [`sandbox.failIfUnavailable`](/it/settings#sandbox-settings) su `true`. Questo è destinato a distribuzioni gestite che richiedono il sandboxing come gate di sicurezza.

### Modalità sandbox

Claude Code offre due modalità sandbox:

**Modalità auto-allow**: I comandi Bash tenteranno di eseguire all'interno della sandbox e sono automaticamente consentiti senza richiedere autorizzazione. I comandi che non possono essere sandboxati (come quelli che necessitano di accesso alla rete a host non consentiti) ricadono nel flusso di autorizzazione regolare. Le regole di chiesta/negazione esplicite che hai configurato sono sempre rispettate.

**Modalità autorizzazioni regolari**: Tutti i comandi bash passano attraverso il flusso di autorizzazione standard, anche quando sandboxati. Questo fornisce più controllo ma richiede più approvazioni.

In entrambe le modalità, la sandbox applica le stesse restrizioni di filesystem e rete. La differenza è solo se i comandi sandboxati sono auto-approvati o richiedono autorizzazione esplicita.

<Info>
  La modalità auto-allow funziona indipendentemente dall'impostazione della modalità di autorizzazione. Anche se non sei in modalità "accetta modifiche", i comandi bash sandboxati verranno eseguiti automaticamente quando auto-allow è abilitato. Ciò significa che i comandi bash che modificano file entro i confini della sandbox verranno eseguiti senza richiedere, anche quando gli strumenti di modifica dei file normalmente richiederebbero approvazione.
</Info>

### Configura il sandboxing

Personalizza il comportamento della sandbox tramite il file `settings.json`. Vedi [Settings](/it/settings#sandbox-settings) per il riferimento di configurazione completo.

#### Concessione dell'accesso in scrittura dei sottoprocessi a percorsi specifici

Per impostazione predefinita, i comandi sandboxati possono scrivere solo nella directory di lavoro corrente. Se i comandi dei sottoprocessi come `kubectl`, `terraform` o `npm` devono scrivere al di fuori della directory del progetto, utilizza `sandbox.filesystem.allowWrite` per concedere l'accesso a percorsi specifici:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

Questi percorsi sono applicati a livello del sistema operativo, quindi tutti i comandi in esecuzione all'interno della sandbox, inclusi i loro processi figlio, li rispettano. Questo è l'approccio consigliato quando uno strumento ha bisogno di accesso in scrittura a una posizione specifica, piuttosto che escludere completamente lo strumento dalla sandbox con `excludedCommands`.

Quando `allowWrite` (o `denyWrite`/`denyRead`/`allowRead`) è definito in più [ambiti di impostazioni](/it/settings#settings-precedence), gli array sono **uniti**, il che significa che i percorsi da ogni ambito sono combinati, non sostituiti. Ad esempio, se le impostazioni gestite consentono scritture in `/opt/company-tools` e un utente aggiunge `~/.kube` nelle sue impostazioni personali, entrambi i percorsi sono inclusi nella configurazione finale della sandbox. Ciò significa che gli utenti e i progetti possono estendere l'elenco senza duplicare o sovrascrivere i percorsi impostati da ambiti con priorità più alta.

I prefissi di percorso controllano come i percorsi vengono risolti:

| Prefisso               | Significato                                                                                                         | Esempio                                                                     |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- |
| `/`                    | Percorso assoluto dalla radice del filesystem                                                                       | `/tmp/build` rimane `/tmp/build`                                            |
| `~/`                   | Relativo alla directory home                                                                                        | `~/.kube` diventa `$HOME/.kube`                                             |
| `./` o nessun prefisso | Relativo alla radice del progetto per le impostazioni del progetto, o a `~/.claude` per le impostazioni dell'utente | `./output` in `.claude/settings.json` si risolve in `<project-root>/output` |

Il prefisso precedente `//path` per i percorsi assoluti funziona ancora. Se in precedenza hai utilizzato `/path` aspettandoti una risoluzione relativa al progetto, passa a `./path`. Questa sintassi differisce dalle [regole di autorizzazione Read e Edit](/it/permissions#read-and-edit), che utilizzano `//path` per assoluto e `/path` per relativo al progetto. I percorsi del filesystem della sandbox utilizzano convenzioni standard: `/tmp/build` è un percorso assoluto.

È inoltre possibile negare l'accesso in scrittura o lettura utilizzando `sandbox.filesystem.denyWrite` e `sandbox.filesystem.denyRead`. Questi vengono uniti con qualsiasi percorso dalle regole di autorizzazione `Edit(...)` e `Read(...)`. Per ri-consentire la lettura di percorsi specifici all'interno di una regione `denyRead`, utilizza `sandbox.filesystem.allowRead`, che ha la precedenza su `denyRead`. Quando `allowManagedReadPathsOnly` è abilitato nelle impostazioni gestite, solo le voci `allowRead` gestite sono rispettate; le voci `allowRead` dell'utente, del progetto e locali vengono ignorate. `denyRead` continua a unirsi da tutte le fonti.

Ad esempio, per bloccare la lettura dall'intera directory home consentendo comunque letture dal progetto corrente, aggiungi questo al `.claude/settings.json` del tuo progetto:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

Il `.` in `allowRead` si risolve nella radice del progetto perché questa configurazione si trova nelle impostazioni del progetto. Se hai posizionato la stessa configurazione in `~/.claude/settings.json`, `.` si risolverebbe in `~/.claude` invece, e i file del progetto rimarrebbero bloccati dalla regola `denyRead`.

<Tip>
  Non tutti i comandi sono compatibili con il sandboxing subito. Alcuni appunti che potrebbero aiutarti a ottenere il massimo dalla sandbox:

  * Molti strumenti CLI richiedono l'accesso a determinati host. Man mano che utilizzi questi strumenti, richiederanno l'autorizzazione per accedere a determinati host. Concedere l'autorizzazione consentirà loro di accedere a questi host ora e in futuro, consentendo loro di eseguire in modo sicuro all'interno della sandbox.
  * `watchman` è incompatibile con l'esecuzione nella sandbox. Se stai eseguendo `jest`, considera di utilizzare `jest --no-watchman`
  * `docker` è incompatibile con l'esecuzione nella sandbox. Considera di specificare `docker` in `excludedCommands` per forzarlo a eseguire al di fuori della sandbox.
</Tip>

<Note>
  Claude Code include un meccanismo di escape hatch intenzionale che consente ai comandi di eseguire al di fuori della sandbox quando necessario. Quando un comando non riesce a causa di restrizioni della sandbox (come problemi di connettività di rete o strumenti incompatibili), Claude viene richiesto di analizzare l'errore e potrebbe riprovare il comando con il parametro `dangerouslyDisableSandbox`. I comandi che utilizzano questo parametro passano attraverso il flusso di autorizzazioni normale di Claude Code richiedendo l'autorizzazione dell'utente per l'esecuzione. Ciò consente a Claude Code di gestire i casi limite in cui determinati strumenti o operazioni di rete non possono funzionare entro i vincoli della sandbox.

  È possibile disabilitare questo escape hatch impostando `"allowUnsandboxedCommands": false` nelle [impostazioni della sandbox](/it/settings#sandbox-settings). Quando disabilitato, il parametro `dangerouslyDisableSandbox` viene completamente ignorato e tutti i comandi devono essere eseguiti sandboxati o essere esplicitamente elencati in `excludedCommands`.
</Note>

## Vantaggi della sicurezza

### Protezione contro l'iniezione di prompt

Anche se un attaccante manipola con successo il comportamento di Claude Code attraverso l'iniezione di prompt, la sandbox assicura che il sistema rimanga sicuro:

**Protezione del filesystem:**

* Non è possibile modificare file di configurazione critici come `~/.bashrc`
* Non è possibile modificare file a livello di sistema in `/bin/`
* Non è possibile leggere file che sono negati nelle [impostazioni di autorizzazione di Claude](/it/permissions#manage-permissions)

**Protezione della rete:**

* Non è possibile esfiltare dati a server controllati dall'attaccante
* Non è possibile scaricare script dannosi da domini non autorizzati
* Non è possibile effettuare chiamate API inaspettate a servizi non approvati
* Non è possibile contattare alcun dominio non esplicitamente consentito

**Monitoraggio e controllo:**

* Tutti i tentativi di accesso al di fuori della sandbox sono bloccati a livello del sistema operativo
* Ricevi notifiche immediate quando i confini vengono testati
* È possibile scegliere di negare, consentire una volta o aggiornare permanentemente la configurazione

### Superficie di attacco ridotta

Il sandboxing limita il danno potenziale da:

* **Dipendenze dannose**: Pacchetti NPM o altre dipendenze con codice dannoso
* **Script compromessi**: Script di compilazione o strumenti con vulnerabilità di sicurezza
* **Ingegneria sociale**: Attacchi che ingannano gli utenti nel far eseguire comandi pericolosi
* **Iniezione di prompt**: Attacchi che ingannano Claude nel far eseguire comandi pericolosi

### Funzionamento trasparente

Quando Claude Code tenta di accedere a risorse di rete al di fuori della sandbox:

1. L'operazione viene bloccata a livello del sistema operativo
2. Ricevi una notifica immediata
3. È possibile scegliere di:
   * Negare la richiesta
   * Consentirla una volta
   * Aggiornare la configurazione della sandbox per consentirla permanentemente

## Limitazioni della sicurezza

* Limitazioni del sandboxing della rete: Il sistema di filtraggio della rete funziona limitando i domini a cui i processi possono connettersi. Non ispeziona altrimenti il traffico che passa attraverso il proxy e gli utenti sono responsabili di assicurarsi che consentano solo domini affidabili nella loro politica.

<Warning>
  Gli utenti dovrebbero essere consapevoli dei potenziali rischi derivanti dal consentire domini ampi come `github.com` che potrebbero consentire l'esfiltrazione di dati. Inoltre, in alcuni casi potrebbe essere possibile aggirare il filtraggio della rete attraverso il [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting).
</Warning>

* Escalation dei privilegi tramite Unix Sockets: La configurazione `allowUnixSockets` può inavvertitamente concedere l'accesso a potenti servizi di sistema che potrebbero portare a bypass della sandbox. Ad esempio, se viene utilizzato per consentire l'accesso a `/var/run/docker.sock` questo concederebbe effettivamente l'accesso al sistema host sfruttando il socket docker. Gli utenti sono incoraggiati a considerare attentamente qualsiasi socket unix che consentono attraverso la sandbox.
* Escalation dei permessi del filesystem: I permessi di scrittura del filesystem eccessivamente ampi possono abilitare attacchi di escalation dei privilegi. Consentire scritture a directory contenenti eseguibili in `$PATH`, directory di configurazione di sistema o file di configurazione della shell dell'utente (`.bashrc`, `.zshrc`) può portare all'esecuzione di codice in diversi contesti di sicurezza quando altri utenti o processi di sistema accedono a questi file.
* Forza della sandbox Linux: L'implementazione Linux fornisce un forte isolamento del filesystem e della rete ma include una modalità `enableWeakerNestedSandbox` che le consente di funzionare all'interno di ambienti Docker senza namespace privilegiati. Questa opzione indebolisce considerevolmente la sicurezza e dovrebbe essere utilizzata solo nei casi in cui l'isolamento aggiuntivo è altrimenti applicato.

## Come il sandboxing si relaziona alle autorizzazioni

Il sandboxing e le [autorizzazioni](/it/permissions) sono livelli di sicurezza complementari che funzionano insieme:

* **Autorizzazioni** controllano quali strumenti Claude Code può utilizzare e vengono valutate prima che qualsiasi strumento venga eseguito. Si applicano a tutti gli strumenti: Bash, Read, Edit, WebFetch, MCP e altri.
* **Sandboxing** fornisce l'applicazione a livello del sistema operativo che limita ciò che i comandi Bash possono accedere a livello di filesystem e rete. Si applica solo ai comandi Bash e ai loro processi figlio.

Le restrizioni di filesystem e rete sono configurate sia tramite le impostazioni della sandbox che le regole di autorizzazione:

* Utilizza `sandbox.filesystem.allowWrite` per concedere l'accesso in scrittura dei sottoprocessi a percorsi al di fuori della directory di lavoro
* Utilizza `sandbox.filesystem.denyWrite` e `sandbox.filesystem.denyRead` per bloccare l'accesso dei sottoprocessi a percorsi specifici
* Utilizza `sandbox.filesystem.allowRead` per ri-consentire la lettura di percorsi specifici all'interno di una regione `denyRead`
* Utilizza le regole di negazione `Read` e `Edit` per bloccare l'accesso a file o directory specifici
* Utilizza le regole di consentimento/negazione `WebFetch` per controllare l'accesso al dominio
* Utilizza la sandbox `allowedDomains` per controllare quali domini i comandi Bash possono raggiungere

I percorsi dalle impostazioni `sandbox.filesystem` e dalle regole di autorizzazione vengono uniti insieme nella configurazione finale della sandbox.

Questo [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) include configurazioni di impostazioni iniziali per scenari di distribuzione comuni, inclusi esempi specifici della sandbox. Utilizzali come punti di partenza e adattali alle tue esigenze.

## Utilizzo avanzato

### Configurazione proxy personalizzata

Per le organizzazioni che richiedono una sicurezza di rete avanzata, è possibile implementare un proxy personalizzato per:

* Decrittare e ispezionare il traffico HTTPS
* Applicare regole di filtraggio personalizzate
* Registrare tutte le richieste di rete
* Integrarsi con l'infrastruttura di sicurezza esistente

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### Integrazione con gli strumenti di sicurezza esistenti

Lo strumento bash in sandbox funziona insieme a:

* **Regole di autorizzazione**: Combina con [impostazioni di autorizzazione](/it/permissions) per la difesa in profondità
* **Contenitori di sviluppo**: Utilizza con [devcontainers](/it/devcontainer) per un isolamento aggiuntivo
* **Politiche aziendali**: Applica le configurazioni della sandbox tramite [impostazioni gestite](/it/settings#settings-precedence)

## Best practice

1. **Inizia restrittivo**: Inizia con autorizzazioni minime e espandi secondo le necessità
2. **Monitora i log**: Rivedi i tentativi di violazione della sandbox per comprendere le esigenze di Claude Code
3. **Utilizza configurazioni specifiche dell'ambiente**: Diverse regole sandbox per contesti di sviluppo rispetto a produzione
4. **Combina con autorizzazioni**: Utilizza il sandboxing insieme alle politiche IAM per una sicurezza completa
5. **Testa le configurazioni**: Verifica che le impostazioni della sandbox non blocchino i flussi di lavoro legittimi

## Open source

Il runtime della sandbox è disponibile come pacchetto npm open source per l'uso nei tuoi progetti di agente. Ciò consente alla comunità più ampia degli agenti AI di costruire sistemi autonomi più sicuri. Questo può anche essere utilizzato per sandboxare altri programmi che potresti desiderare di eseguire. Ad esempio, per sandboxare un server MCP potresti eseguire:

```bash theme={null}
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Per i dettagli di implementazione e il codice sorgente, visita il [repository GitHub](https://github.com/anthropic-experimental/sandbox-runtime).

## Limitazioni

* **Overhead di prestazioni**: Minimo, ma alcune operazioni del filesystem potrebbero essere leggermente più lente
* **Compatibilità**: Alcuni strumenti che richiedono modelli di accesso al sistema specifici potrebbero necessitare di regolazioni di configurazione, o potrebbero anche dover essere eseguiti al di fuori della sandbox
* **Supporto della piattaforma**: Supporta macOS, Linux e WSL2. WSL1 non è supportato. Il supporto nativo di Windows è pianificato.

## Cosa il sandboxing non copre

La sandbox isola i sottoprocessi Bash. Altri strumenti operano sotto confini diversi:

* **Strumenti di file integrati**: Read, Edit e Write utilizzano il sistema di autorizzazione direttamente piuttosto che eseguire attraverso la sandbox. Vedi [autorizzazioni](/it/permissions).
* **Utilizzo del computer**: quando Claude apre app e controlla lo schermo su macOS, viene eseguito sul tuo desktop effettivo piuttosto che in un ambiente isolato. I prompt di autorizzazione per app gating ogni applicazione. Vedi [utilizzo del computer nella CLI](/it/computer-use) o [utilizzo del computer in Desktop](/it/desktop#let-claude-use-your-computer).

## Vedi anche

* [Security](/it/security) - Funzionalità di sicurezza complete e best practice
* [Permissions](/it/permissions) - Configurazione delle autorizzazioni e controllo dell'accesso
* [Settings](/it/settings) - Riferimento di configurazione completo
* [CLI reference](/it/cli-reference) - Opzioni della riga di comando
