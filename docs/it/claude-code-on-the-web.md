> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sul web

> Esegui attività Claude Code in modo asincrono su infrastruttura cloud sicura

<Note>
  Claude Code sul web è attualmente in anteprima di ricerca.
</Note>

## Cos'è Claude Code sul web?

Claude Code sul web consente agli sviluppatori di avviare Claude Code dall'app Claude. Questo è perfetto per:

* **Rispondere a domande**: Poni domande sull'architettura del codice e su come vengono implementate le funzionalità
* **Correzioni di bug e attività di routine**: Attività ben definite che non richiedono una guida frequente
* **Lavoro parallelo**: Affronta più correzioni di bug in parallelo
* **Repository non sulla tua macchina locale**: Lavora su codice che non hai controllato localmente
* **Modifiche backend**: Dove Claude Code può scrivere test e poi scrivere codice per superare quei test

Claude Code è disponibile anche nell'app Claude per [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) e [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) per avviare attività in movimento e monitorare il lavoro in corso.

Puoi [avviare nuove attività sul web dal tuo terminale](#from-terminal-to-web) con `--remote`, oppure [teletrasportare sessioni web nel tuo terminale](#from-web-to-terminal) per continuare localmente. Per utilizzare l'interfaccia web mentre esegui Claude Code sulla tua macchina invece dell'infrastruttura cloud, vedi [Remote Control](/it/remote-control).

## Chi può utilizzare Claude Code sul web?

Claude Code sul web è disponibile in anteprima di ricerca per:

* **Utenti Pro**
* **Utenti Max**
* **Utenti Team**
* **Utenti Enterprise** con posti premium o posti Chat + Claude Code

## Iniziare

Configura Claude Code sul web dal browser o dal tuo terminale.

### Dal browser

1. Visita [claude.ai/code](https://claude.ai/code)
2. Connetti il tuo account GitHub
3. Installa l'app Claude GitHub nei tuoi repository
4. Seleziona il tuo ambiente predefinito
5. Invia la tua attività di codifica
6. Rivedi le modifiche nella vista diff, itera con commenti, quindi crea una pull request

### Dal terminale

Esegui `/web-setup` all'interno di Claude Code per connettere GitHub utilizzando le credenziali locali della tua CLI `gh`. Il comando sincronizza il tuo `gh auth token` a Claude Code sul web, crea un ambiente cloud predefinito e apre claude.ai/code nel tuo browser al termine.

Questo percorso richiede che la CLI `gh` sia installata e autenticata con `gh auth login`. Se `gh` non è disponibile, `/web-setup` apre claude.ai/code in modo che tu possa connettere GitHub dal browser.

Le tue credenziali `gh` danno a Claude accesso al clone e al push, quindi puoi saltare l'app GitHub per le sessioni di base. Installa l'app in seguito se desideri [Auto-fix](#auto-fix-pull-requests), che utilizza l'app per ricevere webhook PR.

<Note>
  Gli amministratori di Team e Enterprise possono disabilitare la configurazione del terminale con l'interruttore Quick web setup su [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
</Note>

## Come funziona

Quando avvii un'attività su Claude Code sul web:

1. **Clonazione del repository**: Il tuo repository viene clonato su una macchina virtuale gestita da Anthropic
2. **Configurazione dell'ambiente**: Claude prepara un ambiente cloud sicuro con il tuo codice, quindi esegue il tuo [script di configurazione](#setup-scripts) se configurato
3. **Configurazione della rete**: L'accesso a Internet viene configurato in base alle tue impostazioni
4. **Esecuzione dell'attività**: Claude analizza il codice, apporta modifiche, esegue test e verifica il suo lavoro
5. **Completamento**: Ricevi una notifica al termine e puoi creare una PR con le modifiche
6. **Risultati**: Le modifiche vengono inviate a un ramo, pronto per la creazione della pull request

## Rivedi le modifiche con la vista diff

La vista diff ti consente di vedere esattamente cosa ha cambiato Claude prima di creare una pull request. Invece di fare clic su "Crea PR" per rivedere le modifiche in GitHub, visualizza il diff direttamente nell'app e itera con Claude fino a quando le modifiche non sono pronte.

Quando Claude apporta modifiche ai file, appare un indicatore di statistiche diff che mostra il numero di righe aggiunte e rimosse (ad esempio, `+12 -1`). Seleziona questo indicatore per aprire il visualizzatore diff, che visualizza un elenco di file a sinistra e le modifiche per ogni file a destra.

Dalla vista diff, puoi:

* Rivedere le modifiche file per file
* Commentare modifiche specifiche per richiedere modifiche
* Continuare a iterare con Claude in base a quello che vedi

Questo ti consente di perfezionare le modifiche attraverso più round di feedback senza creare PR bozza o passare a GitHub.

## Correzione automatica delle pull request

Claude può monitorare una pull request e rispondere automaticamente ai fallimenti CI e ai commenti di revisione. Claude si iscrive all'attività GitHub sulla PR e, quando un controllo fallisce o un revisore lascia un commento, Claude indaga e invia una correzione se una è chiara.

<Note>
  Auto-fix richiede che l'app Claude GitHub sia installata nel tuo repository. Se non l'hai già fatto, installala dalla [pagina dell'app GitHub](https://github.com/apps/claude) o quando richiesto durante la [configurazione](#getting-started).
</Note>

Ci sono alcuni modi per attivare auto-fix a seconda da dove proviene la PR e quale dispositivo stai utilizzando:

* **PR create in Claude Code sul web**: apri la barra di stato CI e seleziona **Auto-fix**
* **Dall'app mobile**: dì a Claude di correggere automaticamente la PR, ad esempio "guarda questa PR e correggi eventuali fallimenti CI o commenti di revisione"
* **Qualsiasi PR esistente**: incolla l'URL della PR in una sessione e dì a Claude di correggerla automaticamente

### Come Claude risponde all'attività PR

Quando auto-fix è attivo, Claude riceve eventi GitHub per la PR inclusi nuovi commenti di revisione e fallimenti di controllo CI. Per ogni evento, Claude indaga e decide come procedere:

* **Correzioni chiare**: se Claude è sicuro di una correzione e non entra in conflitto con le istruzioni precedenti, Claude apporta la modifica, la invia e spiega cosa è stato fatto nella sessione
* **Richieste ambigue**: se il commento di un revisore potrebbe essere interpretato in più modi o coinvolge qualcosa di architettonicamente significativo, Claude ti chiede prima di agire
* **Eventi duplicati o senza azione**: se un evento è un duplicato o non richiede modifiche, Claude lo annota nella sessione e continua

Claude potrebbe rispondere ai thread di commenti di revisione su GitHub come parte della loro risoluzione. Queste risposte vengono pubblicate utilizzando il tuo account GitHub, quindi appaiono sotto il tuo nome utente, ma ogni risposta è etichettata come proveniente da Claude Code in modo che i revisori sappiano che è stata scritta dall'agente e non da te direttamente.

## Spostamento di attività tra web e terminale

Puoi avviare nuove attività sul web dal tuo terminale, oppure estrarre sessioni web nel tuo terminale per continuare localmente. Le sessioni web persistono anche se chiudi il tuo laptop e puoi monitorarle da qualsiasi luogo, inclusa l'app mobile Claude.

<Note>
  L'handoff della sessione è unidirezionale: puoi estrarre sessioni web nel tuo terminale, ma non puoi inviare una sessione terminale esistente al web. Il flag `--remote` crea una *nuova* sessione web per il tuo repository attuale.
</Note>

### Dal terminale al web

Avvia una sessione web dalla riga di comando con il flag `--remote`:

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Questo crea una nuova sessione web su claude.ai. L'attività viene eseguita nel cloud mentre continui a lavorare localmente. Usa `/tasks` per controllare l'avanzamento, oppure apri la sessione su claude.ai o l'app mobile Claude per interagire direttamente. Da lì puoi guidare Claude, fornire feedback o rispondere a domande proprio come in qualsiasi altra conversazione.

#### Suggerimenti per attività remote

**Pianifica localmente, esegui da remoto**: Per attività complesse, avvia Claude in Plan Mode per collaborare sull'approccio, quindi invia il lavoro al web:

```bash  theme={null}
claude --permission-mode plan
```

In Plan Mode, Claude può solo leggere file ed esplorare la base di codice. Una volta soddisfatto del piano, avvia una sessione remota per l'esecuzione autonoma:

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Questo modello ti dà il controllo sulla strategia mentre consente a Claude di eseguire autonomamente nel cloud.

**Esegui attività in parallelo**: Ogni comando `--remote` crea la sua propria sessione web che viene eseguita indipendentemente. Puoi avviare più attività e verranno tutte eseguite simultaneamente in sessioni separate:

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Monitora tutte le sessioni con `/tasks`. Quando una sessione si completa, puoi creare una PR dall'interfaccia web o [teletrasportare](#from-web-to-terminal) la sessione nel tuo terminale per continuare a lavorare.

### Dal web al terminale

Ci sono diversi modi per estrarre una sessione web nel tuo terminale:

* **Usando `/teleport`**: Da Claude Code, esegui `/teleport` (o `/tp`) per vedere un selettore interattivo delle tue sessioni web. Se hai modifiche non sottoposte a commit, ti verrà chiesto di archiviarle prima.
* **Usando `--teleport`**: Dalla riga di comando, esegui `claude --teleport` per un selettore di sessione interattivo, oppure `claude --teleport <session-id>` per riprendere una sessione specifica direttamente.
* **Da `/tasks`**: Esegui `/tasks` per vedere le tue sessioni in background, quindi premi `t` per teletrasportarti in una
* **Dall'interfaccia web**: Fai clic su "Apri in CLI" per copiare un comando che puoi incollare nel tuo terminale

Quando teletrasporti una sessione, Claude verifica che sei nel repository corretto, recupera e controlla il ramo dalla sessione remota e carica la cronologia completa della conversazione nel tuo terminale.

#### Requisiti per il teletrasporto

Il teletrasporto verifica questi requisiti prima di riprendere una sessione. Se un requisito non è soddisfatto, vedrai un errore o ti verrà chiesto di risolvere il problema.

| Requisito           | Dettagli                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stato git pulito    | La tua directory di lavoro non deve avere modifiche non sottoposte a commit. Il teletrasporto ti chiede di archiviare le modifiche se necessario. |
| Repository corretto | Devi eseguire `--teleport` da un checkout dello stesso repository, non da un fork.                                                                |
| Ramo disponibile    | Il ramo dalla sessione web deve essere stato inviato al remoto. Il teletrasporto lo recupera e lo controlla automaticamente.                      |
| Stesso account      | Devi essere autenticato allo stesso account Claude.ai utilizzato nella sessione web.                                                              |

### Condivisione di sessioni

Per condividere una sessione, attiva/disattiva la sua visibilità in base ai tipi di account di seguito. Dopo di che, condividi il link della sessione così com'è. I destinatari che aprono la tua sessione condivisa vedranno lo stato più recente della sessione al caricamento, ma la pagina del destinatario non si aggiornerà in tempo reale.

#### Condivisione da un account Enterprise o Teams

Per gli account Enterprise e Teams, le due opzioni di visibilità sono **Private** e **Team**. La visibilità Team rende la sessione visibile agli altri membri della tua organizzazione Claude.ai. La verifica dell'accesso al repository è abilitata per impostazione predefinita, in base all'account GitHub connesso all'account del destinatario. Il nome visualizzato del tuo account è visibile a tutti i destinatari con accesso. Le sessioni [Claude in Slack](/it/slack) vengono condivise automaticamente con visibilità Team.

#### Condivisione da un account Max o Pro

Per gli account Max e Pro, le due opzioni di visibilità sono **Private** e **Public**. La visibilità Public rende la sessione visibile a qualsiasi utente connesso a claude.ai.

Controlla la tua sessione per contenuti sensibili prima di condividere. Le sessioni possono contenere codice e credenziali da repository GitHub privati. La verifica dell'accesso al repository non è abilitata per impostazione predefinita.

Abilita la verifica dell'accesso al repository e/o nascondi il tuo nome dalle tue sessioni condivise andando su Impostazioni > Claude Code > Impostazioni di condivisione.

## Pianifica attività ricorrenti

Esegui Claude su una pianificazione ricorrente per automatizzare il lavoro come revisioni PR giornaliere, audit delle dipendenze e analisi dei fallimenti CI. Vedi [Pianifica attività sul web](/it/web-scheduled-tasks) per la guida completa.

## Gestione delle sessioni

### Archiviazione di sessioni

Puoi archiviare sessioni per mantenere organizzato il tuo elenco di sessioni. Le sessioni archiviate sono nascoste dall'elenco di sessioni predefinito ma possono essere visualizzate filtrando le sessioni archiviate.

Per archiviare una sessione, passa il mouse sulla sessione nella barra laterale e fai clic sull'icona di archiviazione.

### Eliminazione di sessioni

L'eliminazione di una sessione rimuove permanentemente la sessione e i suoi dati. Questa azione non può essere annullata. Puoi eliminare una sessione in due modi:

* **Dalla barra laterale**: Filtra le sessioni archiviate, quindi passa il mouse sulla sessione che desideri eliminare e fai clic sull'icona di eliminazione
* **Dal menu della sessione**: Apri una sessione, fai clic sul menu a discesa accanto al titolo della sessione e seleziona **Elimina**

Ti verrà chiesto di confermare prima che una sessione venga eliminata.

## Ambiente cloud

### Immagine predefinita

Costruiamo e manteniamo un'immagine universale con toolchain comuni e ecosistemi di linguaggio preinstallati. Questa immagine include:

* Linguaggi di programmazione e runtime popolari
* Strumenti di compilazione comuni e gestori di pacchetti
* Framework di test e linter

#### Verifica degli strumenti disponibili

Per vedere cosa è preinstallato nel tuo ambiente, chiedi a Claude Code di eseguire:

```bash  theme={null}
check-tools
```

Questo comando visualizza:

* Linguaggi di programmazione e loro versioni
* Gestori di pacchetti disponibili
* Strumenti di sviluppo installati

#### Configurazioni specifiche del linguaggio

L'immagine universale include ambienti preconfigurati per:

* **Python**: Python 3.x con pip, poetry e librerie scientifiche comuni
* **Node.js**: Ultime versioni LTS con npm, yarn, pnpm e bun
* **Ruby**: Versioni 3.1.6, 3.2.6, 3.3.6 (predefinita: 3.3.6) con gem, bundler e rbenv per la gestione delle versioni
* **PHP**: Versione 8.4.14
* **Java**: OpenJDK con Maven e Gradle
* **Go**: Ultima versione stabile con supporto dei moduli
* **Rust**: Toolchain Rust con cargo
* **C++**: Compilatori GCC e Clang

#### Database

L'immagine universale include i seguenti database:

* **PostgreSQL**: Versione 16
* **Redis**: Versione 7.0

### Configurazione dell'ambiente

Quando avvii una sessione in Claude Code sul web, ecco cosa accade dietro le quinte:

1. **Preparazione dell'ambiente**: Cloniamo il tuo repository ed eseguiamo qualsiasi [script di configurazione](#setup-scripts) configurato. Il repository verrà clonato con il ramo predefinito nel tuo repository GitHub. Se desideri controllare un ramo specifico, puoi specificarlo nel prompt.

2. **Configurazione della rete**: Configuriamo l'accesso a Internet per l'agente. L'accesso a Internet è limitato per impostazione predefinita, ma puoi configurare l'ambiente per non avere accesso a Internet o accesso completo a Internet in base alle tue esigenze.

3. **Esecuzione di Claude Code**: Claude Code viene eseguito per completare la tua attività, scrivendo codice, eseguendo test e verificando il suo lavoro. Puoi guidare e dirigere Claude durante la sessione tramite l'interfaccia web. Claude rispetta il contesto che hai definito nel tuo `CLAUDE.md`.

4. **Risultato**: Quando Claude completa il suo lavoro, invierà il ramo al remoto. Potrai creare una PR per il ramo.

<Note>
  Claude opera interamente attraverso il terminale e gli strumenti CLI disponibili nell'ambiente. Utilizza gli strumenti preinstallati nell'immagine universale e qualsiasi strumento aggiuntivo che installi tramite hooks o gestione delle dipendenze.
</Note>

**Per aggiungere un nuovo ambiente:** Seleziona l'ambiente attuale per aprire il selettore di ambiente, quindi seleziona "Aggiungi ambiente". Questo aprirà una finestra di dialogo in cui puoi specificare il nome dell'ambiente, il livello di accesso alla rete, le variabili di ambiente e uno [script di configurazione](#setup-scripts).

**Per aggiornare un ambiente esistente:** Seleziona l'ambiente attuale, a destra del nome dell'ambiente, e seleziona il pulsante delle impostazioni. Questo aprirà una finestra di dialogo in cui puoi aggiornare il nome dell'ambiente, l'accesso alla rete, le variabili di ambiente e lo script di configurazione.

**Per selezionare il tuo ambiente predefinito dal terminale:** Se hai più ambienti configurati, esegui `/remote-env` per scegliere quale utilizzare quando avvii sessioni web dal tuo terminale con `--remote`. Con un singolo ambiente, questo comando mostra la tua configurazione attuale.

<Note>
  Le variabili di ambiente devono essere specificate come coppie chiave-valore, in [formato `.env`](https://www.dotenv.org/). Ad esempio:

  ```text  theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Script di configurazione

Uno script di configurazione è uno script Bash che viene eseguito quando inizia una nuova sessione cloud, prima che Claude Code si avvii. Utilizza gli script di configurazione per installare dipendenze, configurare strumenti o preparare qualsiasi cosa di cui l'ambiente cloud ha bisogno che non sia nell'[immagine predefinita](#default-image).

Gli script vengono eseguiti come root su Ubuntu 24.04, quindi `apt install` e la maggior parte dei gestori di pacchetti di linguaggio funzionano.

<Tip>
  Per verificare cosa è già installato prima di aggiungerlo al tuo script, chiedi a Claude di eseguire `check-tools` in una sessione cloud.
</Tip>

Per aggiungere uno script di configurazione, apri la finestra di dialogo delle impostazioni dell'ambiente e inserisci il tuo script nel campo **Setup script**.

Questo esempio installa la CLI `gh`, che non è nell'immagine predefinita:

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Gli script di configurazione vengono eseguiti solo quando si crea una nuova sessione. Vengono saltati quando si riprende una sessione esistente.

Se lo script esce con un codice diverso da zero, la sessione non si avvia. Aggiungi `|| true` ai comandi non critici per evitare di bloccare la sessione su un'installazione instabile.

<Note>
  Gli script di configurazione che installano pacchetti hanno bisogno di accesso alla rete per raggiungere i registri. L'accesso alla rete predefinito consente connessioni a [registri di pacchetti comuni](#default-allowed-domains) inclusi npm, PyPI, RubyGems e crates.io. Gli script non riusciranno a installare pacchetti se il tuo ambiente ha l'accesso alla rete disabilitato.
</Note>

#### Script di configurazione vs. hook SessionStart

Utilizza uno script di configurazione per installare cose di cui il cloud ha bisogno ma il tuo laptop ha già, come un runtime di linguaggio o uno strumento CLI. Utilizza un [hook SessionStart](/it/hooks#sessionstart) per la configurazione del progetto che dovrebbe essere eseguita ovunque, cloud e locale, come `npm install`.

Entrambi vengono eseguiti all'inizio di una sessione, ma appartengono a posti diversi:

|                | Script di configurazione                               | Hook SessionStart                                                      |
| -------------- | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| Allegato a     | L'ambiente cloud                                       | Il tuo repository                                                      |
| Configurato in | Interfaccia utente dell'ambiente cloud                 | `.claude/settings.json` nel tuo repository                             |
| Viene eseguito | Prima che Claude Code si avvii, solo su nuove sessioni | Dopo che Claude Code si avvia, su ogni sessione incluse quelle riprese |
| Ambito         | Solo ambienti cloud                                    | Sia locale che cloud                                                   |

Gli hook SessionStart possono anche essere definiti nel tuo `~/.claude/settings.json` a livello di utente localmente, ma le impostazioni a livello di utente non vengono trasferite alle sessioni cloud. Nel cloud, vengono eseguiti solo gli hook sottoposti a commit nel repository.

### Gestione delle dipendenze

Le immagini di ambiente personalizzate e gli snapshot non sono ancora supportati. Utilizza [script di configurazione](#setup-scripts) per installare pacchetti quando inizia una sessione, oppure [hook SessionStart](/it/hooks#sessionstart) per l'installazione di dipendenze che dovrebbe essere eseguita anche negli ambienti locali. Gli hook SessionStart hanno [limitazioni note](#dependency-management-limitations).

Per configurare l'installazione automatica delle dipendenze con uno script di configurazione, apri le impostazioni dell'ambiente e aggiungi uno script:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

In alternativa, puoi utilizzare gli hook SessionStart nel file `.claude/settings.json` del tuo repository per l'installazione di dipendenze che dovrebbe essere eseguita anche negli ambienti locali:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Crea lo script corrispondente in `scripts/install_pkgs.sh`:

```bash  theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Rendilo eseguibile: `chmod +x scripts/install_pkgs.sh`

#### Persistenza delle variabili di ambiente

Gli hook SessionStart possono persistere le variabili di ambiente per i comandi Bash successivi scrivendo nel file specificato nella variabile di ambiente `CLAUDE_ENV_FILE`. Per i dettagli, vedi [Hook SessionStart](/it/hooks#sessionstart) nel riferimento degli hook.

#### Limitazioni della gestione delle dipendenze

* **Gli hook si attivano per tutte le sessioni**: Gli hook SessionStart vengono eseguiti sia negli ambienti locali che remoti. Non esiste una configurazione di hook per limitare un hook solo alle sessioni remote. Per saltare l'esecuzione locale, controlla la variabile di ambiente `CLAUDE_CODE_REMOTE` nel tuo script come mostrato sopra.
* **Richiede accesso alla rete**: I comandi di installazione hanno bisogno di accesso alla rete per raggiungere i registri di pacchetti. Se il tuo ambiente è configurato con accesso "No internet", questi hook falliranno. Utilizza accesso alla rete "Limited" (predefinito) o "Full". L'[elenco di consentiti predefinito](#default-allowed-domains) include registri comuni come npm, PyPI, RubyGems e crates.io.
* **Compatibilità proxy**: Tutto il traffico in uscita negli ambienti remoti passa attraverso un [proxy di sicurezza](#security-proxy). Alcuni gestori di pacchetti non funzionano correttamente con questo proxy. Bun è un esempio noto.
* **Viene eseguito ad ogni avvio della sessione**: Gli hook vengono eseguiti ogni volta che una sessione si avvia o riprende, aggiungendo latenza di avvio. Mantieni gli script di installazione veloci controllando se le dipendenze sono già presenti prima di reinstallarle.

## Accesso alla rete e sicurezza

### Politica di rete

#### Proxy GitHub

Per motivi di sicurezza, tutte le operazioni GitHub passano attraverso un servizio proxy dedicato che gestisce in modo trasparente tutte le interazioni git. All'interno della sandbox, il client git si autentica utilizzando una credenziale con ambito personalizzato. Questo proxy:

* Gestisce l'autenticazione GitHub in modo sicuro - il client git utilizza una credenziale con ambito all'interno della sandbox, che il proxy verifica e traduce nel tuo token di autenticazione GitHub effettivo
* Limita le operazioni git push al ramo di lavoro attuale per motivi di sicurezza
* Abilita il clonaggio, il recupero e le operazioni PR senza interruzioni mantenendo i confini di sicurezza

#### Proxy di sicurezza

Gli ambienti vengono eseguiti dietro un proxy di rete HTTP/HTTPS per motivi di sicurezza e prevenzione degli abusi. Tutto il traffico Internet in uscita passa attraverso questo proxy, che fornisce:

* Protezione contro richieste dannose
* Limitazione della velocità e prevenzione degli abusi
* Filtro dei contenuti per una sicurezza migliorata

### Livelli di accesso

Per impostazione predefinita, l'accesso alla rete è limitato ai [domini consentiti](#default-allowed-domains).

Puoi configurare l'accesso alla rete personalizzato, inclusa la disabilitazione dell'accesso alla rete.

### Domini consentiti predefiniti

Quando si utilizza l'accesso alla rete "Limited", i seguenti domini sono consentiti per impostazione predefinita:

#### Servizi Anthropic

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### Controllo versione

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### Registri di container

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* public.ecr.aws

#### Piattaforme cloud

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### Gestori di pacchetti - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Gestori di pacchetti - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Gestori di pacchetti - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### Gestori di pacchetti - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Gestori di pacchetti - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Gestori di pacchetti - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### Gestori di pacchetti - Altri linguaggi

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Distribuzioni Linux

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Strumenti di sviluppo e piattaforme

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### Servizi cloud e monitoraggio

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### Distribuzione di contenuti e mirror

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Schema e configurazione

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

<Note>
  I domini contrassegnati con `*` indicano la corrispondenza dei sottodomini con caratteri jolly. Ad esempio, `*.gcr.io` consente l'accesso a qualsiasi sottodominio di `gcr.io`.
</Note>

### Migliori pratiche di sicurezza per l'accesso alla rete personalizzato

1. **Principio del minimo privilegio**: Abilita solo l'accesso alla rete minimo richiesto
2. **Audit regolari**: Rivedi periodicamente i domini consentiti
3. **Usa HTTPS**: Preferisci sempre gli endpoint HTTPS rispetto a HTTP

## Sicurezza e isolamento

Claude Code sul web fornisce forti garanzie di sicurezza:

* **Macchine virtuali isolate**: Ogni sessione viene eseguita in una VM isolata gestita da Anthropic
* **Controlli di accesso alla rete**: L'accesso alla rete è limitato per impostazione predefinita e può essere disabilitato

<Note>
  Quando viene eseguito con l'accesso alla rete disabilitato, Claude Code è autorizzato a comunicare con l'API Anthropic che potrebbe comunque consentire ai dati di uscire dalla VM Claude Code isolata.
</Note>

* **Protezione delle credenziali**: Le credenziali sensibili (come le credenziali git o le chiavi di firma) non sono mai all'interno della sandbox con Claude Code. L'autenticazione viene gestita tramite un proxy sicuro utilizzando credenziali con ambito
* **Analisi sicura**: Il codice viene analizzato e modificato all'interno di VM isolate prima di creare PR

## Prezzi e limiti di velocità

Claude Code sul web condivide i limiti di velocità con tutti gli altri utilizzi di Claude e Claude Code all'interno del tuo account. L'esecuzione di più attività in parallelo consumerà più limiti di velocità proporzionalmente.

## Limitazioni

* **Autenticazione del repository**: Puoi spostare sessioni da web a locale solo quando sei autenticato allo stesso account
* **Restrizioni della piattaforma**: Claude Code sul web funziona solo con codice ospitato in GitHub. Le istanze self-hosted di [GitHub Enterprise Server](/it/github-enterprise-server) sono supportate per i piani Teams e Enterprise. GitLab e altri repository non GitHub non possono essere utilizzati con sessioni cloud

## Migliori pratiche

1. **Automatizza la configurazione dell'ambiente**: Utilizza [script di configurazione](#setup-scripts) per installare dipendenze e configurare strumenti prima che Claude Code si avvii. Per scenari più avanzati, configura [hook SessionStart](/it/hooks#sessionstart).
2. **Documenta i requisiti**: Specifica chiaramente le dipendenze e i comandi nel tuo file `CLAUDE.md`. Se hai un file `AGENTS.md`, puoi fornirlo nel tuo `CLAUDE.md` usando `@AGENTS.md` per mantenere un'unica fonte di verità.

## Risorse correlate

* [Configurazione degli hook](/it/hooks)
* [Riferimento delle impostazioni](/it/settings)
* [Sicurezza](/it/security)
* [Utilizzo dei dati](/it/data-usage)
