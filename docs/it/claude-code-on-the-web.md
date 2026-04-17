> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usa Claude Code sul web

> Configura ambienti cloud, script di configurazione, accesso alla rete e Docker nella sandbox di Anthropic. Sposta le sessioni tra web e terminale con `--remote` e `--teleport`.

<Note>
  Claude Code sul web è in anteprima di ricerca per gli utenti Pro, Max e Team, e per gli utenti Enterprise con posti premium o posti Chat + Claude Code.
</Note>

Claude Code sul web esegue attività su infrastruttura cloud gestita da Anthropic su [claude.ai/code](https://claude.ai/code). Le sessioni persistono anche se chiudi il browser e puoi monitorarle dall'app mobile Claude.

<Tip>
  Nuovo a Claude Code sul web? Inizia con [Guida introduttiva](/it/web-quickstart) per connettere il tuo account GitHub e inviare il tuo primo compito.
</Tip>

Questa pagina copre:

* [Opzioni di autenticazione GitHub](#github-authentication-options): due modi per connettere GitHub
* [L'ambiente cloud](#the-cloud-environment): quale configurazione viene trasferita, quali strumenti sono installati e come configurare gli ambienti
* [Script di configurazione](#setup-scripts) e gestione delle dipendenze
* [Accesso alla rete](#network-access): livelli, proxy e l'elenco di consentiti predefinito
* [Sposta attività tra web e terminale](#move-tasks-between-web-and-terminal) con `--remote` e `--teleport`
* [Lavora con le sessioni](#work-with-sessions): revisione, condivisione, archiviazione, eliminazione
* [Correzione automatica delle pull request](#auto-fix-pull-requests): rispondi automaticamente ai fallimenti CI e ai commenti di revisione
* [Sicurezza e isolamento](#security-and-isolation): come le sessioni sono isolate
* [Limitazioni](#limitations): limiti di velocità e restrizioni della piattaforma

## Opzioni di autenticazione GitHub

Le sessioni cloud hanno bisogno di accesso ai tuoi repository GitHub per clonare il codice e inviare i rami. Puoi concedere l'accesso in due modi:

| Metodo           | Come funziona                                                                                                                                                                | Migliore per                                                   |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| **GitHub App**   | Installa l'app Claude GitHub su repository specifici durante l'[onboarding web](/it/web-quickstart). L'accesso è limitato per repository.                                    | Team che desiderano un'autorizzazione esplicita per repository |
| **`/web-setup`** | Esegui `/web-setup` nel tuo terminale per sincronizzare il tuo token CLI `gh` locale al tuo account Claude. L'accesso corrisponde a quello che il tuo token `gh` può vedere. | Sviluppatori individuali che già usano `gh`                    |

Entrambi i metodi funzionano. [`/schedule`](/it/routines) verifica entrambe le forme di accesso e ti chiede di eseguire `/web-setup` se nessuna è configurata. Vedi [Connetti dal tuo terminale](/it/web-quickstart#connect-from-your-terminal) per la procedura dettagliata di `/web-setup`.

L'app GitHub è richiesta per [Auto-fix](#auto-fix-pull-requests), che utilizza l'app per ricevere webhook PR. Se ti connetti con `/web-setup` e successivamente desideri Auto-fix, installa l'app su quei repository.

Gli amministratori di Team e Enterprise possono disabilitare `/web-setup` con l'interruttore Quick web setup su [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

<Note>
  Le organizzazioni con [Zero Data Retention](/it/zero-data-retention) abilitato non possono utilizzare `/web-setup` o altre funzionalità di sessione cloud.
</Note>

## L'ambiente cloud

Ogni sessione viene eseguita in una VM gestita da Anthropic appena creata con il tuo repository clonato. Questa sezione copre cosa è disponibile quando una sessione inizia e come personalizzarlo.

### Cosa è disponibile nelle sessioni cloud

Le sessioni cloud iniziano da un clone appena creato del tuo repository. Qualsiasi cosa sottoposta a commit nel repository è disponibile. Qualsiasi cosa che hai installato o configurato solo sulla tua macchina non lo è.

|                                                                                 | Disponibile nelle sessioni cloud | Perché                                                                                                                                                                  |
| :------------------------------------------------------------------------------ | :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Il tuo `CLAUDE.md` del repository                                               | Sì                               | Parte del clone                                                                                                                                                         |
| I tuoi hook `.claude/settings.json` del repository                              | Sì                               | Parte del clone                                                                                                                                                         |
| I tuoi server MCP `.mcp.json` del repository                                    | Sì                               | Parte del clone                                                                                                                                                         |
| Le tue `.claude/rules/` del repository                                          | Sì                               | Parte del clone                                                                                                                                                         |
| Le tue `.claude/skills/`, `.claude/agents/`, `.claude/commands/` del repository | Sì                               | Parte del clone                                                                                                                                                         |
| Plugin dichiarati in `.claude/settings.json`                                    | Sì                               | Installati all'inizio della sessione dal [marketplace](/it/plugin-marketplaces) che hai dichiarato. Richiede accesso alla rete per raggiungere la fonte del marketplace |
| Il tuo `~/.claude/CLAUDE.md` utente                                             | No                               | Vive sulla tua macchina, non nel repository                                                                                                                             |
| Plugin abilitati solo nelle tue impostazioni utente                             | No                               | L'`enabledPlugins` con ambito utente vive in `~/.claude/settings.json`. Dichiarali invece in `.claude/settings.json` del repository                                     |
| Server MCP che hai aggiunto con `claude mcp add`                                | No                               | Quelli scrivono nella tua configurazione utente locale, non nel repository. Dichiara il server in [`.mcp.json`](/it/mcp#project-scope) invece                           |
| Token API statici e credenziali                                                 | No                               | Non esiste ancora un archivio di segreti dedicato. Vedi sotto                                                                                                           |
| Autenticazione interattiva come AWS SSO                                         | No                               | Non supportato. SSO richiede un login basato su browser che non può essere eseguito in una sessione cloud                                                               |

Per rendere la configurazione disponibile nelle sessioni cloud, eseguine il commit nel repository. Un archivio di segreti dedicato non è ancora disponibile. Sia le variabili di ambiente che gli script di configurazione sono archiviati nella configurazione dell'ambiente, visibili a chiunque possa modificare quell'ambiente. Se hai bisogno di segreti in una sessione cloud, aggiungili come variabili di ambiente con quella visibilità in mente.

### Strumenti installati

Le sessioni cloud vengono fornite con runtime di linguaggio comuni, strumenti di compilazione e database preinstallati. La tabella seguente riassume cosa è incluso per categoria.

| Categoria    | Incluso                                                                            |
| :----------- | :--------------------------------------------------------------------------------- |
| **Python**   | Python 3.x con pip, poetry, uv, black, mypy, pytest, ruff                          |
| **Node.js**  | 20, 21 e 22 tramite nvm, con npm, yarn, pnpm, bun¹, eslint, prettier, chromedriver |
| **Ruby**     | 3.1, 3.2, 3.3 con gem, bundler, rbenv                                              |
| **PHP**      | 8.4 con Composer                                                                   |
| **Java**     | OpenJDK 21 con Maven e Gradle                                                      |
| **Go**       | ultima versione stabile con supporto dei moduli                                    |
| **Rust**     | rustc e cargo                                                                      |
| **C/C++**    | GCC, Clang, cmake, ninja, conan                                                    |
| **Docker**   | docker, dockerd, docker compose                                                    |
| **Database** | PostgreSQL 16, Redis 7.0                                                           |
| **Utilità**  | git, jq, yq, ripgrep, tmux, vim, nano                                              |

¹ Bun è installato ma ha [problemi di compatibilità proxy](#install-dependencies-with-a-sessionstart-hook) noti per il recupero dei pacchetti.

Per le versioni esatte, chiedi a Claude di eseguire `check-tools` in una sessione cloud. Questo comando esiste solo nelle sessioni cloud.

### Lavora con i problemi e le pull request di GitHub

Le sessioni cloud includono strumenti GitHub integrati che consentono a Claude di leggere i problemi, elencare le pull request, recuperare i diff e pubblicare commenti senza alcuna configurazione. Questi strumenti si autenticano tramite il [proxy GitHub](#github-proxy) utilizzando il metodo che hai configurato in [Opzioni di autenticazione GitHub](#github-authentication-options), quindi il tuo token non entra mai nel contenitore.

La CLI `gh` non è preinstallata. Se hai bisogno di un comando `gh` che gli strumenti integrati non coprono, come `gh release` o `gh workflow run`, installalo e autenticalo tu stesso:

<Steps>
  <Step title="Installa gh nel tuo script di configurazione">
    Aggiungi `apt update && apt install -y gh` al tuo [script di configurazione](#setup-scripts).
  </Step>

  <Step title="Fornisci un token">
    Aggiungi una variabile di ambiente `GH_TOKEN` alle tue [impostazioni dell'ambiente](#configure-your-environment) con un token di accesso personale GitHub. `gh` legge `GH_TOKEN` automaticamente, quindi non è necessario alcun passaggio `gh auth login`.
  </Step>
</Steps>

### Collega gli artefatti di nuovo alla sessione

Ogni sessione cloud ha un URL di trascrizione su claude.ai e la sessione può leggere il suo ID dalla variabile di ambiente `CLAUDE_CODE_REMOTE_SESSION_ID`. Usa questo per mettere un link tracciabile nei corpi PR, nei messaggi di commit, nei post Slack o nei report generati in modo che un revisore possa aprire l'esecuzione che li ha prodotti.

Chiedi a Claude di costruire il link dalla variabile di ambiente. Il seguente comando stampa l'URL:

```bash theme={null}
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

### Esegui test, avvia servizi e aggiungi pacchetti

Claude esegue i test come parte del lavoro su un compito. Chiedilo nel tuo prompt, come "correggi i test falliti in `tests/`" o "esegui pytest dopo ogni modifica." I test runner come pytest, jest e cargo test funzionano subito poiché sono preinstallati.

PostgreSQL e Redis sono preinstallati ma non in esecuzione per impostazione predefinita. Avvia ognuno durante la sessione:

```bash theme={null}
service postgresql start
```

```bash theme={null}
service redis-server start
```

Docker è disponibile per l'esecuzione di servizi containerizzati. Chiedi a Claude di eseguire `docker compose up` per avviare i servizi del tuo progetto. L'accesso alla rete per il pull delle immagini segue il [livello di accesso](#access-levels) del tuo ambiente e i [Trusted defaults](#default-allowed-domains) includono Docker Hub e altri registri comuni.

Se le tue immagini sono grandi o lente da estrarre, aggiungi `docker compose pull` o `docker compose build` al tuo [script di configurazione](#setup-scripts). Le immagini estratte vengono salvate nell'[ambiente memorizzato nella cache](#environment-caching), quindi ogni nuova sessione le ha su disco. La cache memorizza solo i file, non i processi in esecuzione, quindi Claude avvia comunque i contenitori ogni sessione.

Per aggiungere pacchetti che non sono preinstallati, usa uno [script di configurazione](#setup-scripts). L'output dello script è [memorizzato nella cache](#environment-caching), quindi i pacchetti che installi lì sono disponibili all'inizio di ogni sessione senza reinstallare ogni volta. Puoi anche chiedere a Claude di installare pacchetti durante la sessione, ma quelle installazioni non persistono tra le sessioni.

### Limiti di risorse

Le sessioni cloud vengono eseguite con limiti di risorse approssimativi che possono cambiare nel tempo:

* 4 vCPU
* 16 GB di RAM
* 30 GB di disco

I compiti che richiedono significativamente più memoria, come grandi lavori di compilazione o test ad alta intensità di memoria, potrebbero fallire o essere terminati. Per carichi di lavoro oltre questi limiti, usa [Remote Control](/it/remote-control) per eseguire Claude Code sul tuo hardware.

### Configura il tuo ambiente

Gli ambienti controllano l'[accesso alla rete](#network-access), le variabili di ambiente e lo [script di configurazione](#setup-scripts) che viene eseguito prima che una sessione inizi. Vedi [Strumenti installati](#installed-tools) per cosa è disponibile senza alcuna configurazione. Puoi gestire gli ambienti dall'interfaccia web o dal terminale:

| Azione                                | Come                                                                                                                                                                                                                                   |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aggiungi un ambiente                  | Seleziona l'ambiente attuale per aprire il selettore, quindi seleziona **Aggiungi ambiente**. La finestra di dialogo include nome, livello di accesso alla rete, variabili di ambiente e script di configurazione.                     |
| Modifica un ambiente                  | Seleziona l'icona delle impostazioni a destra del nome dell'ambiente.                                                                                                                                                                  |
| Archivia un ambiente                  | Apri l'ambiente per la modifica e seleziona **Archivia**. Gli ambienti archiviati sono nascosti dal selettore ma le sessioni esistenti continuano a essere eseguite.                                                                   |
| Imposta il predefinito per `--remote` | Esegui `/remote-env` nel tuo terminale. Se hai un singolo ambiente, questo comando mostra la tua configurazione attuale. `/remote-env` seleziona solo il predefinito; aggiungi, modifica e archivia gli ambienti dall'interfaccia web. |

Le variabili di ambiente usano il formato `.env` con una coppia `KEY=value` per riga. Non racchiudere i valori tra virgolette, poiché le virgolette vengono archiviate come parte del valore.

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

## Script di configurazione

Uno script di configurazione è uno script Bash che viene eseguito quando inizia una nuova sessione cloud, prima che Claude Code si avvii. Usa gli script di configurazione per installare dipendenze, configurare strumenti o recuperare qualsiasi cosa di cui la sessione ha bisogno che non sia preinstallata.

Gli script vengono eseguiti come root su Ubuntu 24.04, quindi `apt install` e la maggior parte dei gestori di pacchetti di linguaggio funzionano.

Per aggiungere uno script di configurazione, apri la finestra di dialogo delle impostazioni dell'ambiente e inserisci il tuo script nel campo **Script di configurazione**.

Questo esempio installa la CLI `gh`, che non è preinstallata:

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Se lo script esce con un codice diverso da zero, la sessione non si avvia. Aggiungi `|| true` ai comandi non critici per evitare di bloccare la sessione su un'installazione intermittente fallita.

<Note>
  Gli script di configurazione che installano pacchetti hanno bisogno di accesso alla rete per raggiungere i registri. L'accesso alla rete predefinito **Trusted** consente connessioni ai [domini di pacchetti comuni](#default-allowed-domains) inclusi npm, PyPI, RubyGems e crates.io. Gli script non riusciranno a installare pacchetti se il tuo ambiente usa l'accesso alla rete **None**.
</Note>

### Memorizzazione nella cache dell'ambiente

Lo script di configurazione viene eseguito la prima volta che avvii una sessione in un ambiente. Dopo il completamento, Anthropic crea uno snapshot del file system e riutilizza quello snapshot come punto di partenza per le sessioni successive. Le nuove sessioni iniziano con le tue dipendenze, strumenti e immagini Docker già su disco e il passaggio dello script di configurazione viene saltato. Questo mantiene l'avvio veloce anche quando lo script installa grandi toolchain o estrae immagini di contenitori.

La cache acquisisce i file, non i processi in esecuzione. Qualsiasi cosa che lo script di configurazione scrive su disco viene trasferita. I servizi o i contenitori che avvia non lo fanno, quindi avvia quelli per sessione chiedendo a Claude o con un [hook SessionStart](#setup-scripts-vs-sessionstart-hooks).

Lo script di configurazione viene eseguito di nuovo per ricostruire la cache quando modifichi lo script di configurazione dell'ambiente o gli host di rete consentiti e quando la cache raggiunge la sua scadenza dopo circa sette giorni. Riprendere una sessione esistente non esegue mai di nuovo lo script di configurazione.

Non è necessario abilitare la memorizzazione nella cache o gestire gli snapshot tu stesso.

### Script di configurazione vs. hook SessionStart

Usa uno script di configurazione per installare cose di cui il cloud ha bisogno ma il tuo laptop ha già, come un runtime di linguaggio o uno strumento CLI. Usa un [hook SessionStart](/it/hooks#sessionstart) per la configurazione del progetto che dovrebbe essere eseguita ovunque, cloud e locale, come `npm install`.

Entrambi vengono eseguiti all'inizio di una sessione, ma appartengono a posti diversi:

|                | Script di configurazione                                                                                                | Hook SessionStart                                                      |
| -------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Allegato a     | L'ambiente cloud                                                                                                        | Il tuo repository                                                      |
| Configurato in | Interfaccia utente dell'ambiente cloud                                                                                  | `.claude/settings.json` nel tuo repository                             |
| Viene eseguito | Prima che Claude Code si avvii, quando non è disponibile alcun [ambiente memorizzato nella cache](#environment-caching) | Dopo che Claude Code si avvia, su ogni sessione incluse quelle riprese |
| Ambito         | Solo ambienti cloud                                                                                                     | Sia locale che cloud                                                   |

Gli hook SessionStart possono anche essere definiti nel tuo `~/.claude/settings.json` a livello di utente localmente, ma le impostazioni a livello di utente non vengono trasferite alle sessioni cloud. Nel cloud, vengono eseguiti solo gli hook sottoposti a commit nel repository.

### Installa le dipendenze con un hook SessionStart

Per installare le dipendenze solo nelle sessioni cloud, aggiungi un hook SessionStart al `.claude/settings.json` del tuo repository:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
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

Crea lo script in `scripts/install_pkgs.sh` e rendilo eseguibile con `chmod +x`. La variabile di ambiente `CLAUDE_CODE_REMOTE` è impostata su `true` nelle sessioni cloud, quindi puoi usarla per saltare l'esecuzione locale:

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Gli hook SessionStart hanno alcune limitazioni nelle sessioni cloud:

* **Nessun ambito solo cloud**: gli hook vengono eseguiti sia nelle sessioni locali che cloud. Per saltare l'esecuzione locale, controlla la variabile di ambiente `CLAUDE_CODE_REMOTE` come mostrato sopra.
* **Richiede accesso alla rete**: i comandi di installazione hanno bisogno di raggiungere i registri di pacchetti. Se il tuo ambiente usa l'accesso alla rete **None**, questi hook falliranno. L'[elenco di consentiti predefinito](#default-allowed-domains) sotto **Trusted** copre npm, PyPI, RubyGems e crates.io.
* **Compatibilità proxy**: tutto il traffico in uscita passa attraverso un [proxy di sicurezza](#security-proxy). Alcuni gestori di pacchetti non funzionano correttamente con questo proxy. Bun è un esempio noto.
* **Aggiunge latenza di avvio**: gli hook vengono eseguiti ogni volta che una sessione si avvia o riprende, a differenza degli script di configurazione che beneficiano della [memorizzazione nella cache dell'ambiente](#environment-caching). Mantieni gli script di installazione veloci controllando se le dipendenze sono già presenti prima di reinstallarle.

Per persistere le variabili di ambiente per i comandi Bash successivi, scrivi nel file in `$CLAUDE_ENV_FILE`. Vedi [Hook SessionStart](/it/hooks#sessionstart) per i dettagli.

La sostituzione dell'immagine di base con la tua immagine Docker non è ancora supportata. Usa uno script di configurazione per installare quello di cui hai bisogno sopra l'[immagine fornita](#installed-tools) o esegui la tua immagine come contenitore insieme a Claude con `docker compose`.

## Accesso alla rete

L'accesso alla rete controlla le connessioni in uscita dall'ambiente cloud. Ogni ambiente specifica un livello di accesso e puoi estenderlo con domini personalizzati consentiti. Il predefinito è **Trusted**, che consente i registri di pacchetti e altri [domini consentiti](#default-allowed-domains).

### Livelli di accesso

Scegli un livello di accesso quando crei o modifichi un ambiente:

| Livello     | Connessioni in uscita                                                                        |
| :---------- | :------------------------------------------------------------------------------------------- |
| **None**    | Nessun accesso alla rete in uscita                                                           |
| **Trusted** | [Domini consentiti](#default-allowed-domains) solo: registri di pacchetti, GitHub, SDK cloud |
| **Full**    | Qualsiasi dominio                                                                            |
| **Custom**  | Il tuo elenco di consentiti, opzionalmente inclusi i predefiniti                             |

Le operazioni GitHub usano un [proxy separato](#github-proxy) che è indipendente da questa impostazione.

### Consenti domini specifici

Per consentire domini che non sono nell'elenco Trusted, seleziona **Custom** nelle impostazioni di accesso alla rete dell'ambiente. Appare un campo **Domini consentiti**. Inserisci un dominio per riga:

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

Usa `*.` per la corrispondenza dei sottodomini con caratteri jolly. Seleziona **Includi anche l'elenco predefinito di gestori di pacchetti comuni** per mantenere i [domini Trusted](#default-allowed-domains) insieme alle tue voci personalizzate, o lascialo deselezionato per consentire solo quello che elenchi.

### Proxy GitHub

Per motivi di sicurezza, tutte le operazioni GitHub passano attraverso un servizio proxy dedicato che gestisce in modo trasparente tutte le interazioni git. All'interno della sandbox, il client git si autentica utilizzando una credenziale con ambito personalizzato. Questo proxy:

* Gestisce l'autenticazione GitHub in modo sicuro: il client git utilizza una credenziale con ambito all'interno della sandbox, che il proxy verifica e traduce nel tuo token di autenticazione GitHub effettivo
* Limita le operazioni git push al ramo di lavoro attuale per motivi di sicurezza
* Abilita il clonaggio, il recupero e le operazioni PR mantenendo i confini di sicurezza

### Proxy di sicurezza

Gli ambienti vengono eseguiti dietro un proxy di rete HTTP/HTTPS per motivi di sicurezza e prevenzione degli abusi. Tutto il traffico Internet in uscita passa attraverso questo proxy, che fornisce:

* Protezione contro richieste dannose
* Limitazione della velocità e prevenzione degli abusi
* Filtro dei contenuti per una sicurezza migliorata

### Domini consentiti predefiniti

Quando si utilizza l'accesso alla rete **Trusted**, i seguenti domini sono consentiti per impostazione predefinita. I domini contrassegnati con `*` indicano la corrispondenza dei sottodomini con caratteri jolly, quindi `*.gcr.io` consente qualsiasi sottodominio di `gcr.io`.

<AccordionGroup>
  <Accordion title="Servizi Anthropic">
    * api.anthropic.com
    * statsig.anthropic.com
    * docs.claude.com
    * platform.claude.com
    * code.claude.com
    * claude.ai
  </Accordion>

  <Accordion title="Controllo versione">
    * github.com
    * [www.github.com](http://www.github.com)
    * api.github.com
    * npm.pkg.github.com
    * raw\.githubusercontent.com
    * pkg-npm.githubusercontent.com
    * objects.githubusercontent.com
    * release-assets.githubusercontent.com
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
  </Accordion>

  <Accordion title="Registri di container">
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
  </Accordion>

  <Accordion title="Piattaforme cloud">
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
  </Accordion>

  <Accordion title="Gestori di pacchetti JavaScript e Node">
    * registry.npmjs.org
    * [www.npmjs.com](http://www.npmjs.com)
    * [www.npmjs.org](http://www.npmjs.org)
    * npmjs.com
    * npmjs.org
    * yarnpkg.com
    * registry.yarnpkg.com
  </Accordion>

  <Accordion title="Gestori di pacchetti Python">
    * pypi.org
    * [www.pypi.org](http://www.pypi.org)
    * files.pythonhosted.org
    * pythonhosted.org
    * test.pypi.org
    * pypi.python.org
    * pypa.io
    * [www.pypa.io](http://www.pypa.io)
  </Accordion>

  <Accordion title="Gestori di pacchetti Ruby">
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
  </Accordion>

  <Accordion title="Gestori di pacchetti Rust">
    * crates.io
    * [www.crates.io](http://www.crates.io)
    * index.crates.io
    * static.crates.io
    * rustup.rs
    * static.rust-lang.org
    * [www.rust-lang.org](http://www.rust-lang.org)
  </Accordion>

  <Accordion title="Gestori di pacchetti Go">
    * proxy.golang.org
    * sum.golang.org
    * index.golang.org
    * golang.org
    * [www.golang.org](http://www.golang.org)
    * goproxy.io
    * pkg.go.dev
  </Accordion>

  <Accordion title="Gestori di pacchetti JVM">
    * maven.org
    * repo.maven.org
    * central.maven.org
    * repo1.maven.org
    * repo.maven.apache.org
    * jcenter.bintray.com
    * gradle.org
    * [www.gradle.org](http://www.gradle.org)
    * services.gradle.org
    * plugins.gradle.org
    * kotlinlang.org
    * [www.kotlinlang.org](http://www.kotlinlang.org)
    * spring.io
    * repo.spring.io
  </Accordion>

  <Accordion title="Altri gestori di pacchetti">
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
  </Accordion>

  <Accordion title="Distribuzioni Linux">
    * archive.ubuntu.com
    * security.ubuntu.com
    * ubuntu.com
    * [www.ubuntu.com](http://www.ubuntu.com)
    * \*.ubuntu.com
    * ppa.launchpad.net
    * launchpad.net
    * [www.launchpad.net](http://www.launchpad.net)
    * \*.nixos.org
  </Accordion>

  <Accordion title="Strumenti di sviluppo e piattaforme">
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
    * developer.apple.com
    * developer.android.com
    * pkg.stainless.com
    * binaries.prisma.sh
  </Accordion>

  <Accordion title="Servizi cloud e monitoraggio">
    * statsig.com
    * [www.statsig.com](http://www.statsig.com)
    * api.statsig.com
    * sentry.io
    * \*.sentry.io
    * downloads.sentry-cdn.com
    * http-intake.logs.datadoghq.com
    * \*.datadoghq.com
    * \*.datadoghq.eu
    * api.honeycomb.io
  </Accordion>

  <Accordion title="Distribuzione di contenuti e mirror">
    * sourceforge.net
    * \*.sourceforge.net
    * packagecloud.io
    * \*.packagecloud.io
    * fonts.googleapis.com
    * fonts.gstatic.com
  </Accordion>

  <Accordion title="Schema e configurazione">
    * json-schema.org
    * [www.json-schema.org](http://www.json-schema.org)
    * json.schemastore.org
    * [www.schemastore.org](http://www.schemastore.org)
  </Accordion>

  <Accordion title="Model Context Protocol">
    * \*.modelcontextprotocol.io
  </Accordion>
</AccordionGroup>

## Sposta attività tra web e terminale

Questi flussi di lavoro richiedono la [CLI Claude Code](/it/quickstart) connessa allo stesso account claude.ai. Puoi avviare nuove sessioni cloud dal tuo terminale o estrarre sessioni cloud nel tuo terminale per continuare localmente. Le sessioni cloud persistono anche se chiudi il tuo laptop e puoi monitorarle da qualsiasi luogo inclusa l'app mobile Claude.

<Note>
  Dalla CLI, l'handoff della sessione è unidirezionale: puoi estrarre sessioni cloud nel tuo terminale con `--teleport`, ma non puoi inviare una sessione terminale esistente al web. Il flag `--remote` crea una nuova sessione cloud per il tuo repository attuale. L'[app Desktop](/it/desktop#continue-in-another-surface) fornisce un menu Continua in che può inviare una sessione locale al web.
</Note>

### Dal terminale al web

Avvia una sessione cloud dalla riga di comando con il flag `--remote`:

```bash theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Questo crea una nuova sessione cloud su claude.ai. La sessione clona il remoto GitHub della tua directory attuale al tuo ramo attuale, quindi esegui il push prima se hai commit locali, poiché la VM clona da GitHub piuttosto che dalla tua macchina. `--remote` funziona con un singolo repository alla volta. L'attività viene eseguita nel cloud mentre continui a lavorare localmente.

<Note>
  `--remote` crea sessioni cloud. `--remote-control` non è correlato: espone una sessione CLI locale per il monitoraggio dal web. Vedi [Remote Control](/it/remote-control).
</Note>

Usa `/tasks` nella CLI Claude Code per controllare l'avanzamento, o apri la sessione su claude.ai o l'app mobile Claude per interagire direttamente. Da lì puoi guidare Claude, fornire feedback o rispondere a domande proprio come in qualsiasi altra conversazione.

#### Suggerimenti per attività cloud

**Pianifica localmente, esegui da remoto**: per attività complesse, avvia Claude in plan mode per collaborare sull'approccio, quindi invia il lavoro al cloud:

```bash theme={null}
claude --permission-mode plan
```

In plan mode, Claude legge i file, esegue comandi per esplorare e propone un piano senza modificare il codice sorgente. Una volta soddisfatto, salva il piano nel repository, esegui il commit e il push in modo che la VM cloud possa clonarlo. Quindi avvia una sessione cloud per l'esecuzione autonoma:

```bash theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Questo modello ti dà il controllo sulla strategia mentre consente a Claude di eseguire autonomamente nel cloud.

**Pianifica nel cloud con ultraplan**: per elaborare e rivedere il piano stesso in una sessione web, usa [ultraplan](/it/ultraplan). Claude genera il piano su Claude Code sul web mentre continui a lavorare, quindi commenti le sezioni nel tuo browser e scegli di eseguire da remoto o inviare il piano di nuovo al tuo terminale.

**Esegui attività in parallelo**: ogni comando `--remote` crea la sua propria sessione cloud che viene eseguita indipendentemente. Puoi avviare più attività e verranno tutte eseguite simultaneamente in sessioni separate:

```bash theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Monitora tutte le sessioni con `/tasks` nella CLI Claude Code. Quando una sessione si completa, puoi creare una PR dall'interfaccia web o [teletrasportare](#from-web-to-terminal) la sessione nel tuo terminale per continuare a lavorare.

#### Invia repository locali senza GitHub

Quando esegui `claude --remote` da un repository che non è connesso a GitHub, Claude Code raggruppa il tuo repository locale e lo carica direttamente nella sessione cloud. Il bundle include la tua cronologia completa del repository su tutti i rami, più eventuali modifiche non sottoposte a commit ai file tracciati.

Questo fallback si attiva automaticamente quando l'accesso a GitHub non è disponibile. Per forzarlo anche quando GitHub è connesso, imposta `CCR_FORCE_BUNDLE=1`:

```bash theme={null}
CCR_FORCE_BUNDLE=1 claude --remote "Run the test suite and fix any failures"
```

I repository raggruppati devono soddisfare questi limiti:

* La directory deve essere un repository git con almeno un commit
* Il repository raggruppato deve essere inferiore a 100 MB. I repository più grandi ricadono nel raggruppamento solo del ramo attuale, quindi in uno snapshot squashed singolo dell'albero di lavoro e falliscono solo se lo snapshot è ancora troppo grande
* I file non tracciati non sono inclusi; esegui `git add` sui file che desideri che la sessione cloud veda
* Le sessioni create da un bundle non possono eseguire il push di nuovo a un remoto a meno che tu non abbia anche [autenticazione GitHub](#github-authentication-options) configurata

### Dal web al terminale

Estrai una sessione cloud nel tuo terminale usando uno di questi:

* **Usando `--teleport`**: dalla riga di comando, esegui `claude --teleport` per un selettore di sessione interattivo, o `claude --teleport <session-id>` per riprendere una sessione specifica direttamente. Se hai modifiche non sottoposte a commit, ti verrà chiesto di archiviarle prima.
* **Usando `/teleport`**: all'interno di una sessione CLI esistente, esegui `/teleport` (o `/tp`) per aprire lo stesso selettore di sessione senza riavviare Claude Code.
* **Da `/tasks`**: esegui `/tasks` per vedere le tue sessioni in background, quindi premi `t` per teletrasportarti in una
* **Dall'interfaccia web**: seleziona **Apri in CLI** per copiare un comando che puoi incollare nel tuo terminale

Quando teletrasporti una sessione, Claude verifica che sei nel repository corretto, recupera e controlla il ramo dalla sessione cloud e carica la cronologia completa della conversazione nel tuo terminale.

`--teleport` è distinto da `--resume`. `--resume` riapre una conversazione dalla cronologia locale di questa macchina e non elenca le sessioni cloud; `--teleport` estrae una sessione cloud e il suo ramo.

#### Requisiti per il teletrasporto

Il teletrasporto verifica questi requisiti prima di riprendere una sessione. Se un requisito non è soddisfatto, vedrai un errore o ti verrà chiesto di risolvere il problema.

| Requisito           | Dettagli                                                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stato git pulito    | La tua directory di lavoro non deve avere modifiche non sottoposte a commit. Il teletrasporto ti chiede di archiviare le modifiche se necessario. |
| Repository corretto | Devi eseguire `--teleport` da un checkout dello stesso repository, non da un fork.                                                                |
| Ramo disponibile    | Il ramo dalla sessione cloud deve essere stato inviato al remoto. Il teletrasporto lo recupera e lo controlla automaticamente.                    |
| Stesso account      | Devi essere autenticato allo stesso account claude.ai utilizzato nella sessione cloud.                                                            |

#### `--teleport` non è disponibile

Il teletrasporto richiede l'autenticazione dell'abbonamento claude.ai. Se sei autenticato tramite chiave API, Bedrock, Vertex AI o Microsoft Foundry, esegui `/login` per accedere con il tuo account claude.ai. Se sei già connesso tramite claude.ai e `--teleport` non è ancora disponibile, la tua organizzazione potrebbe aver disabilitato le sessioni cloud.

## Lavora con le sessioni

Le sessioni appaiono nella barra laterale su claude.ai/code. Da lì puoi rivedere le modifiche, condividere con i compagni di squadra, archiviare il lavoro completato o eliminare le sessioni in modo permanente.

### Gestisci il contesto

Le sessioni cloud supportano [comandi integrati](/it/commands) che producono output di testo. I comandi che aprono un selettore di terminale interattivo, come `/model` o `/config`, non sono disponibili.

Per la gestione del contesto in particolare:

| Comando    | Funziona nelle sessioni cloud | Note                                                                                                                           |
| :--------- | :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `/compact` | Sì                            | Riassume la conversazione per liberare il contesto. Accetta istruzioni di focus opzionali come `/compact keep the test output` |
| `/context` | Sì                            | Mostra cosa è attualmente nella finestra di contesto                                                                           |
| `/clear`   | No                            | Avvia una nuova sessione dalla barra laterale                                                                                  |

L'auto-compattazione viene eseguita automaticamente quando la finestra di contesto si avvicina alla capacità, come nella CLI. Per attivarla prima, imposta [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/it/env-vars) nelle tue [variabili di ambiente](#configure-your-environment). Ad esempio, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` compatta al 70% della capacità invece del \~95% predefinito. Per modificare la dimensione della finestra effettiva per i calcoli di compattazione, usa [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/it/env-vars).

I [subagent](/it/sub-agents) funzionano allo stesso modo che fanno localmente. Claude può generarli con lo strumento Task per scaricare la ricerca o il lavoro parallelo in una finestra di contesto separata, mantenendo la conversazione principale più leggera. I subagent definiti in `.claude/agents/` del tuo repository vengono raccolti automaticamente. I [team di agenti](/it/agent-teams) sono disabilitati per impostazione predefinita ma possono essere abilitati aggiungendo `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` alle tue [variabili di ambiente](#configure-your-environment).

### Rivedi le modifiche

Ogni sessione mostra un indicatore diff con righe aggiunte e rimosse, come `+42 -18`. Selezionalo per aprire la vista diff, lascia commenti in linea su righe specifiche e inviali a Claude con il tuo prossimo messaggio. Vedi [Rivedi e itera](/it/web-quickstart#review-and-iterate) per la procedura dettagliata completa inclusa la creazione di PR. Per fare in modo che Claude monitori la PR per i fallimenti CI e i commenti di revisione automaticamente, vedi [Correzione automatica delle pull request](#auto-fix-pull-requests).

### Condividi sessioni

Per condividere una sessione, attiva/disattiva la sua visibilità in base ai tipi di account di seguito. Dopo di che, condividi il link della sessione così com'è. I destinatari vedono lo stato più recente quando aprono il link, ma la loro vista non si aggiorna in tempo reale.

#### Condividi da un account Enterprise o Team

Per gli account Enterprise e Team, le due opzioni di visibilità sono **Private** e **Team**. La visibilità Team rende la sessione visibile agli altri membri della tua organizzazione claude.ai. La verifica dell'accesso al repository è abilitata per impostazione predefinita, in base all'account GitHub connesso all'account del destinatario. Il nome visualizzato del tuo account è visibile a tutti i destinatari con accesso. Le sessioni [Claude in Slack](/it/slack) vengono condivise automaticamente con visibilità Team.

#### Condividi da un account Max o Pro

Per gli account Max e Pro, le due opzioni di visibilità sono **Private** e **Public**. La visibilità Public rende la sessione visibile a qualsiasi utente connesso a claude.ai.

Controlla la tua sessione per contenuti sensibili prima di condividere. Le sessioni possono contenere codice e credenziali da repository GitHub privati. La verifica dell'accesso al repository non è abilitata per impostazione predefinita.

Per richiedere ai destinatari di avere accesso al repository o per nascondere il tuo nome dalle sessioni condivise, vai a Impostazioni > Claude Code > Impostazioni di condivisione.

### Archivia sessioni

Puoi archiviare le sessioni per mantenere organizzato il tuo elenco di sessioni. Le sessioni archiviate sono nascoste dall'elenco di sessioni predefinito ma possono essere visualizzate filtrando le sessioni archiviate.

Per archiviare una sessione, passa il mouse sulla sessione nella barra laterale e seleziona l'icona di archiviazione.

### Elimina sessioni

L'eliminazione di una sessione rimuove permanentemente la sessione e i suoi dati. Questa azione non può essere annullata. Puoi eliminare una sessione in due modi:

* **Dalla barra laterale**: filtra le sessioni archiviate, quindi passa il mouse sulla sessione che desideri eliminare e seleziona l'icona di eliminazione
* **Dal menu della sessione**: apri una sessione, seleziona il menu a discesa accanto al titolo della sessione e seleziona **Elimina**

Ti verrà chiesto di confermare prima che una sessione venga eliminata.

## Correzione automatica delle pull request

Claude può monitorare una pull request e rispondere automaticamente ai fallimenti CI e ai commenti di revisione. Claude si iscrive all'attività GitHub sulla PR e, quando un controllo fallisce o un revisore lascia un commento, Claude indaga e invia una correzione se una è chiara.

<Note>
  Auto-fix richiede che l'app Claude GitHub sia installata nel tuo repository. Se non l'hai già fatto, installala dalla [pagina dell'app GitHub](https://github.com/apps/claude) o quando richiesto durante la [configurazione](/it/web-quickstart#connect-github-and-create-an-environment).
</Note>

Ci sono alcuni modi per attivare auto-fix a seconda da dove proviene la PR e quale dispositivo stai utilizzando:

* **PR create in Claude Code sul web**: apri la barra di stato CI e seleziona **Auto-fix**
* **Dal tuo terminale**: esegui [`/autofix-pr`](/it/commands) mentre sei sul ramo della PR. Claude Code rileva la PR aperta con `gh`, genera una sessione web e attiva auto-fix in un passaggio
* **Dall'app mobile**: dì a Claude di correggere automaticamente la PR, ad esempio "guarda questa PR e correggi eventuali fallimenti CI o commenti di revisione"
* **Qualsiasi PR esistente**: incolla l'URL della PR in una sessione e dì a Claude di correggerla automaticamente

### Come Claude risponde all'attività PR

Quando auto-fix è attivo, Claude riceve eventi GitHub per la PR inclusi nuovi commenti di revisione e fallimenti di controllo CI. Per ogni evento, Claude indaga e decide come procedere:

* **Correzioni chiare**: se Claude è sicuro di una correzione e non entra in conflitto con le istruzioni precedenti, Claude apporta la modifica, la invia e spiega cosa è stato fatto nella sessione
* **Richieste ambigue**: se il commento di un revisore potrebbe essere interpretato in più modi o coinvolge qualcosa di architettonicamente significativo, Claude ti chiede prima di agire
* **Eventi duplicati o senza azione**: se un evento è un duplicato o non richiede modifiche, Claude lo annota nella sessione e continua

Claude potrebbe rispondere ai thread di commenti di revisione su GitHub come parte della loro risoluzione. Queste risposte vengono pubblicate utilizzando il tuo account GitHub, quindi appaiono sotto il tuo nome utente, ma ogni risposta è etichettata come proveniente da Claude Code in modo che i revisori sappiano che è stata scritta dall'agente e non da te direttamente.

<Warning>
  Se il tuo repository utilizza automazione attivata da commenti come Atlantis, Terraform Cloud o GitHub Actions personalizzate che vengono eseguite su eventi `issue_comment`, tieni presente che le risposte di Claude possono attivare questi flussi di lavoro. Rivedi l'automazione del tuo repository prima di abilitare auto-fix e considera di disabilitare auto-fix per i repository in cui un commento PR può distribuire infrastruttura o eseguire operazioni privilegiate.
</Warning>

## Sicurezza e isolamento

Ogni sessione cloud è separata dalla tua macchina e dalle altre sessioni attraverso diversi livelli:

* **Macchine virtuali isolate**: ogni sessione viene eseguita in una VM isolata gestita da Anthropic
* **Controlli di accesso alla rete**: l'accesso alla rete è limitato per impostazione predefinita e può essere disabilitato. Quando viene eseguito con l'accesso alla rete disabilitato, Claude Code può comunque comunicare con l'API Anthropic, che potrebbe consentire ai dati di uscire dalla VM.
* **Protezione delle credenziali**: le credenziali sensibili come le credenziali git o le chiavi di firma non sono mai all'interno della sandbox con Claude Code. L'autenticazione viene gestita tramite un proxy sicuro utilizzando credenziali con ambito.
* **Analisi sicura**: il codice viene analizzato e modificato all'interno di VM isolate prima di creare PR

## Limitazioni

Prima di fare affidamento sulle sessioni cloud per un flusso di lavoro, tieni conto di questi vincoli:

* **Limiti di velocità**: Claude Code sul web condivide i limiti di velocità con tutti gli altri utilizzi di Claude e Claude Code all'interno del tuo account. L'esecuzione di più attività in parallelo consumerà più limiti di velocità proporzionalmente. Non esiste alcun addebito di calcolo separato per la VM cloud.
* **Autenticazione del repository**: puoi spostare le sessioni da web a locale solo quando sei autenticato allo stesso account
* **Restrizioni della piattaforma**: il clonaggio del repository e la creazione di pull request richiedono GitHub. Le istanze self-hosted di [GitHub Enterprise Server](/it/github-enterprise-server) sono supportate per i piani Team e Enterprise. GitLab, Bitbucket e altri repository non GitHub possono essere inviati alle sessioni cloud come [bundle locale](#send-local-repositories-without-github), ma la sessione non può eseguire il push dei risultati di nuovo al remoto

## Risorse correlate

* [Ultraplan](/it/ultraplan): elabora un piano in una sessione cloud e revisionalo nel tuo browser
* [Ultrareview](/it/ultrareview): esegui una profonda revisione del codice multi-agente in una sandbox cloud
* [Routines](/it/routines): automatizza il lavoro su una pianificazione, tramite chiamata API o in risposta agli eventi GitHub
* [Configurazione degli hook](/it/hooks): esegui script agli eventi del ciclo di vita della sessione
* [Riferimento delle impostazioni](/it/settings): tutte le opzioni di configurazione
* [Sicurezza](/it/security): garanzie di isolamento e gestione dei dati
* [Utilizzo dei dati](/it/data-usage): cosa Anthropic conserva dalle sessioni cloud
