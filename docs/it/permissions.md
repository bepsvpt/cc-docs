> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurare le autorizzazioni

> Controlla cosa Claude Code può accedere e fare con regole di autorizzazione granulari, modalità e criteri gestiti.

Claude Code supporta autorizzazioni granulari in modo che Lei possa specificare esattamente cosa l'agente è autorizzato a fare e cosa non può fare. Le impostazioni di autorizzazione possono essere archiviate nel controllo della versione e distribuite a tutti gli sviluppatori della Sua organizzazione, nonché personalizzate dai singoli sviluppatori.

## Sistema di autorizzazione

Claude Code utilizza un sistema di autorizzazione a livelli per bilanciare potenza e sicurezza:

| Tipo di strumento | Esempio               | Approvazione richiesta | Comportamento "Sì, non chiedere più"                |
| :---------------- | :-------------------- | :--------------------- | :-------------------------------------------------- |
| Sola lettura      | Letture di file, Grep | No                     | N/A                                                 |
| Comandi Bash      | Esecuzione shell      | Sì                     | Permanentemente per directory di progetto e comando |
| Modifica di file  | Edit/Write di file    | Sì                     | Fino alla fine della sessione                       |

## Gestire le autorizzazioni

Potete visualizzare e gestire le autorizzazioni degli strumenti di Claude Code con `/permissions`. Questa interfaccia utente elenca tutte le regole di autorizzazione e il file settings.json da cui provengono.

* Le regole **Allow** consentono a Claude Code di utilizzare lo strumento specificato senza approvazione manuale.
* Le regole **Ask** richiedono una conferma ogni volta che Claude Code tenta di utilizzare lo strumento specificato.
* Le regole **Deny** impediscono a Claude Code di utilizzare lo strumento specificato.

Le regole vengono valutate in ordine: **deny -> ask -> allow**. La prima regola corrispondente vince, quindi le regole deny hanno sempre la precedenza.

<Note>
  Le regole di autorizzazione sono applicate da Claude Code, non dal modello. Le istruzioni nel vostro prompt o in `CLAUDE.md` determinano ciò che Claude tenta di fare, ma non cambiano ciò che Claude Code consente. Per concedere o revocare l'accesso, utilizzate `/permissions`, le regole descritte qui, una [modalità di autorizzazione](/it/permission-modes), o un [hook PreToolUse](#extend-permissions-with-hooks).
</Note>

## Modalità di autorizzazione

Claude Code supporta diverse modalità di autorizzazione che controllano come gli strumenti vengono approvati. Vedi [Permission modes](/it/permission-modes) per quando utilizzare ciascuna. Impostate `defaultMode` nei vostri [file di impostazioni](/it/settings#settings-files):

| Modalità            | Descrizione                                                                                                                                                                                                                                        |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportamento standard: richiede l'autorizzazione al primo utilizzo di ogni strumento                                                                                                                                                              |
| `acceptEdits`       | Accetta automaticamente le modifiche ai file e i comandi comuni del filesystem (`mkdir`, `touch`, `mv`, `cp`, ecc.) per i percorsi nella directory di lavoro o `additionalDirectories`                                                             |
| `plan`              | Plan Mode: Claude legge i file ed esegue comandi shell di sola lettura per esplorare ma non modifica i vostri file sorgente                                                                                                                        |
| `auto`              | Auto-approva le chiamate di strumento con controlli di sicurezza in background che verificano che le azioni si allineino con la Sua richiesta. Attualmente un'anteprima di ricerca                                                                 |
| `dontAsk`           | Nega automaticamente gli strumenti a meno che non siano pre-approvati tramite `/permissions` o regole `permissions.allow`                                                                                                                          |
| `bypassPermissions` | Salta i prompt di autorizzazione. Le rimozioni che hanno come destinazione la radice del filesystem o la directory home, come `rm -rf /` e `rm -rf ~`, richiedono comunque un prompt come interruttore di protezione contro gli errori del modello |

<Warning>
  La modalità `bypassPermissions` salta i prompt di autorizzazione, incluse le scritture in `.git`, `.claude`, `.vscode`, `.idea` e `.husky`. Le rimozioni che hanno come destinazione la radice del filesystem o la directory home, come `rm -rf /` e `rm -rf ~`, richiedono comunque un prompt come interruttore di protezione contro gli errori del modello. Utilizzate questa modalità solo in ambienti isolati come contenitori o macchine virtuali dove Claude Code non può causare danni. Gli amministratori possono impedire questa modalità impostando `permissions.disableBypassPermissionsMode` su `"disable"` nelle [impostazioni gestite](#managed-settings).
</Warning>

Per prevenire che la modalità `bypassPermissions` o `auto` venga utilizzata, impostate `permissions.disableBypassPermissionsMode` o `permissions.disableAutoMode` su `"disable"` in qualsiasi [file di impostazioni](/it/settings#settings-files). Questi sono più utili nelle [impostazioni gestite](#managed-settings) dove non possono essere ignorati.

## Sintassi delle regole di autorizzazione

Le regole di autorizzazione seguono il formato `Tool` o `Tool(specifier)`.

### Corrispondere a tutti gli utilizzi di uno strumento

Per corrispondere a tutti gli utilizzi di uno strumento, utilizzate solo il nome dello strumento senza parentesi:

| Regola     | Effetto                                       |
| :--------- | :-------------------------------------------- |
| `Bash`     | Corrisponde a tutti i comandi Bash            |
| `WebFetch` | Corrisponde a tutte le richieste di web fetch |
| `Read`     | Corrisponde a tutte le letture di file        |

`Bash(*)` è equivalente a `Bash` e corrisponde a tutti i comandi Bash.

### Utilizzare gli specificatori per il controllo granulare

Aggiungete uno specificatore tra parentesi per corrispondere a utilizzi specifici dello strumento:

| Regola                         | Effetto                                                           |
| :----------------------------- | :---------------------------------------------------------------- |
| `Bash(npm run build)`          | Corrisponde al comando esatto `npm run build`                     |
| `Read(./.env)`                 | Corrisponde alla lettura del file `.env` nella directory corrente |
| `WebFetch(domain:example.com)` | Corrisponde alle richieste di fetch a example.com                 |

### Modelli con caratteri jolly

Le regole Bash supportano modelli glob con `*`. I caratteri jolly possono apparire in qualsiasi posizione nel comando. Questa configurazione consente comandi npm e git commit mentre blocca git push:

```json theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

Lo spazio prima di `*` è importante: `Bash(ls *)` corrisponde a `ls -la` ma non a `lsof`, mentre `Bash(ls*)` corrisponde a entrambi. Il suffisso `:*` è un modo equivalente per scrivere un carattere jolly finale, quindi `Bash(ls:*)` corrisponde agli stessi comandi di `Bash(ls *)`.

La finestra di dialogo di autorizzazione scrive la forma separata da spazi quando selezionate "Sì, non chiedere più" per un prefisso di comando. La forma `:*` è riconosciuta solo alla fine di un modello. In un modello come `Bash(git:* push)`, il due punti viene trattato come un carattere letterale e non corrisponderà ai comandi git.

## Regole di autorizzazione specifiche dello strumento

### Bash

Le regole di autorizzazione Bash supportano la corrispondenza con caratteri jolly con `*`. I caratteri jolly possono apparire in qualsiasi posizione nel comando, incluso all'inizio, nel mezzo o alla fine:

* `Bash(npm run build)` corrisponde al comando Bash esatto `npm run build`
* `Bash(npm run test *)` corrisponde ai comandi Bash che iniziano con `npm run test`
* `Bash(npm *)` corrisponde a qualsiasi comando che inizia con `npm `
* `Bash(* install)` corrisponde a qualsiasi comando che termina con ` install`
* `Bash(git * main)` corrisponde a comandi come `git checkout main` e `git log --oneline main`

Un singolo `*` corrisponde a qualsiasi sequenza di caratteri inclusi gli spazi, quindi un singolo carattere jolly può estendersi su più argomenti. `Bash(git *)` corrisponde a `git log --oneline --all` e `Bash(git * main)` corrisponde sia a `git push origin main` che a `git merge main`.

Quando `*` appare alla fine con uno spazio prima (come `Bash(ls *)`), applica un confine di parola, richiedendo che il prefisso sia seguito da uno spazio o dalla fine della stringa. Ad esempio, `Bash(ls *)` corrisponde a `ls -la` ma non a `lsof`. Al contrario, `Bash(ls*)` senza spazio corrisponde sia a `ls -la` che a `lsof` perché non c'è un vincolo di confine di parola.

#### Comandi composti

<Tip>
  Claude Code è consapevole degli operatori shell, quindi una regola come `Bash(safe-cmd *)` non gli darà il permesso di eseguire il comando `safe-cmd && other-cmd`. I separatori di comando riconosciuti sono `&&`, `||`, `;`, `|`, `|&`, `&` e newline. Una regola deve corrispondere a ogni sottocomando indipendentemente.
</Tip>

Quando approvate un comando composto con "Sì, non chiedere più", Claude Code salva una regola separata per ogni sottocomando che richiede approvazione, piuttosto che una singola regola per la stringa completa. Ad esempio, approvando `git status && npm test` salva una regola per `npm test`, quindi le future invocazioni di `npm test` vengono riconosciute indipendentemente da cosa precede `&&`. I sottocomandi come `cd` in una sottodirectory generano la loro propria regola Read per quel percorso. Fino a 5 regole possono essere salvate per un singolo comando composto.

#### Wrapper di processo

Prima di corrispondere alle regole Bash, Claude Code rimuove un insieme fisso di wrapper di processo in modo che una regola come `Bash(npm test *)` corrisponda anche a `timeout 30 npm test`. I wrapper riconosciuti sono `timeout`, `time`, `nice`, `nohup` e `stdbuf`.

Anche `xargs` nudo viene rimosso, quindi `Bash(grep *)` corrisponde a `xargs grep pattern`. La rimozione si applica solo quando `xargs` non ha flag: un'invocazione come `xargs -n1 grep pattern` viene abbinata come comando `xargs`, quindi le regole scritte per il comando interno non la coprono.

Questo elenco di wrapper è integrato e non è configurabile. I runner dell'ambiente di sviluppo come `direnv exec`, `devbox run`, `mise exec`, `npx` e `docker exec` non sono nell'elenco. Poiché questi strumenti eseguono i loro argomenti come comando, una regola come `Bash(devbox run *)` corrisponde a qualsiasi cosa venga dopo `run`, incluso `devbox run rm -rf .`. Per approvare il lavoro all'interno di un runner dell'ambiente, scrivete una regola specifica che includa sia il runner che il comando interno, come `Bash(devbox run npm test)`. Aggiungete una regola per ogni comando interno che desiderate consentire.

I wrapper exec come `watch`, `setsid`, `ionice` e `flock` richiedono sempre un prompt e non possono essere auto-approvati da una regola di prefisso come `Bash(watch *)`. Lo stesso vale per `find` con `-exec` o `-delete`: una regola `Bash(find *)` non copre queste forme. Per approvare un'invocazione specifica, scrivete una regola di corrispondenza esatta per la stringa di comando completa.

#### Comandi di sola lettura

Claude Code riconosce un insieme integrato di comandi Bash come di sola lettura e li esegue senza un prompt di autorizzazione in ogni modalità. Questi includono `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc`, `diff`, `stat`, `du`, `cd` e forme di sola lettura di `git`. L'insieme non è configurabile; per richiedere un prompt per uno di questi comandi, aggiungete una regola `ask` o `deny` per esso.

I modelli glob non quotati sono consentiti per i comandi il cui ogni flag è di sola lettura, quindi `ls *.ts` e `wc -l src/*.py` vengono eseguiti senza un prompt. I comandi con flag in grado di scrivere o eseguire, come `find`, `sort`, `sed` e `git`, richiedono comunque un prompt quando è presente un glob non quotato perché il glob potrebbe espandersi a un flag come `-delete`.

Un `cd` in un percorso all'interno della vostra directory di lavoro o di una [directory aggiuntiva](#working-directories) è anche di sola lettura. Un comando composto come `cd packages/api && ls` viene eseguito senza un prompt quando ogni parte si qualifica da sola. La combinazione di `cd` con `git` in un comando composto richiede sempre un prompt, indipendentemente dalla directory di destinazione.

<Warning>
  I modelli di autorizzazione Bash che tentano di vincolare gli argomenti del comando sono fragili. Ad esempio, `Bash(curl http://github.com/ *)` intende limitare curl agli URL di GitHub, ma non corrisponderà a variazioni come:

  * Opzioni prima dell'URL: `curl -X GET http://github.com/...`
  * Protocollo diverso: `curl https://github.com/...`
  * Reindirizzamenti: `curl -L http://bit.ly/xyz` (reindirizza a github)
  * Variabili: `URL=http://github.com && curl $URL`
  * Spazi extra: `curl  http://github.com`

  Per un filtraggio URL più affidabile, considerate:

  * **Limitare gli strumenti di rete Bash**: utilizzate regole deny per bloccare `curl`, `wget` e comandi simili, quindi utilizzate lo strumento WebFetch con l'autorizzazione `WebFetch(domain:github.com)` per i domini consentiti
  * **Utilizzare hook PreToolUse**: implementate un hook che convalida gli URL nei comandi Bash e blocca i domini non consentiti
  * **Aggiungere guida CLAUDE.md**: descrivete i vostri modelli curl consentiti in `CLAUDE.md`. Questo modella quello che Claude prova ma non applica un confine, quindi abbinate con una delle opzioni sopra

  Nota che l'utilizzo di WebFetch da solo non impedisce l'accesso alla rete. Se Bash è consentito, Claude può comunque utilizzare `curl`, `wget` o altri strumenti per raggiungere qualsiasi URL.
</Warning>

### PowerShell

Le regole di autorizzazione PowerShell utilizzano la stessa forma delle regole Bash. I caratteri jolly con `*` corrispondono in qualsiasi posizione, il suffisso `:*` è equivalente a un ` *` finale, e un PowerShell nudo o `PowerShell(*)` corrisponde a ogni comando. Questa configurazione consente comandi `Get-ChildItem` e `git commit` mentre blocca `Remove-Item`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Gli alias comuni vengono canonicalizati prima della corrispondenza. Una regola scritta per il nome del cmdlet corrisponde anche ai suoi alias, quindi `PowerShell(Get-ChildItem *)` corrisponde a `gci`, `ls` e `dir` nonché. La corrispondenza non è sensibile alle maiuscole.

Claude Code analizza l'AST di PowerShell e controlla ogni comando in un comando composto indipendentemente. Gli operatori pipeline `|`, i separatori di istruzione `;` e su PowerShell 7+ gli operatori di catena `&&` e `||` dividono un comando composto in sottocomandi. Una regola deve corrispondere a ogni sottocomando affinché il comando composto sia consentito.

### Read e Edit

Le regole `Edit` si applicano a tutti gli strumenti integrati che modificano i file. Claude fa un tentativo migliore per applicare le regole `Read` a tutti gli strumenti integrati che leggono file come Grep e Glob.

<Warning>
  Le regole deny di Read e Edit si applicano agli strumenti di file integrati di Claude e ai comandi di file che Claude Code riconosce in Bash, come `cat`, `head`, `tail` e `sed`. Non si applicano a sottoprocessi arbitrari che leggono o scrivono file indirettamente, come uno script Python o Node che apre i file da solo. Per l'applicazione a livello del sistema operativo che blocca tutti i processi dall'accesso a un percorso, [abilitate la sandbox](/it/sandboxing).
</Warning>

Le regole Read e Edit seguono entrambe la specifica [gitignore](https://git-scm.com/docs/gitignore) con quattro tipi di modello distinti:

| Modello           | Significato                                       | Esempio                          | Corrisponde                    |
| ----------------- | ------------------------------------------------- | -------------------------------- | ------------------------------ |
| `//path`          | Percorso **assoluto** dalla radice del filesystem | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`          | Percorso dalla directory **home**                 | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`           | Percorso **relativo alla radice del progetto**    | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` o `./path` | Percorso **relativo alla directory corrente**     | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  Un modello come `/Users/alice/file` NON è un percorso assoluto. È relativo alla radice del progetto. Utilizzate `//Users/alice/file` per i percorsi assoluti.
</Warning>

Su Windows, i percorsi vengono normalizzati in forma POSIX prima della corrispondenza. `C:\Users\alice` diventa `/c/Users/alice`, quindi utilizzate `//c/**/.env` per corrispondere ai file `.env` in qualsiasi punto su quel drive. Per corrispondere su tutti i drive, utilizzate `//**/.env`.

Esempi:

* `Edit(/docs/**)`: modifica in `<project>/docs/` (NON `/docs/` e NON `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: legge il `.zshrc` della vostra directory home
* `Edit(//tmp/scratch.txt)`: modifica il percorso assoluto `/tmp/scratch.txt`
* `Read(src/**)`: legge da `<current-directory>/src/`

Una regola corrisponde solo ai file sotto il suo ancoraggio, quindi l'ancoraggio determina quanto lontano una regola deny raggiunge. I nomi di file nudi seguono la semantica gitignore e corrispondono a qualsiasi profondità, quindi `Read(.env)` e `Read(**/.env)` sono equivalenti:

| Regola deny                    | Blocca                                              | Non blocca                                             |
| ------------------------------ | --------------------------------------------------- | ------------------------------------------------------ |
| `Read(.env)` o `Read(**/.env)` | qualsiasi `.env` alla o sotto la directory corrente | `.env` in una directory padre o in un altro progetto   |
| `Read(//**/.env)`              | qualsiasi `.env` in qualsiasi punto del filesystem  | nulla; la regola è ancorata alla radice del filesystem |

<Note>
  Nei modelli gitignore, `*` corrisponde ai file in una singola directory mentre `**` corrisponde ricorsivamente tra le directory. Per consentire l'accesso a tutti i file, utilizzate solo il nome dello strumento senza parentesi: `Read`, `Edit` o `Write`.
</Note>

Quando Claude accede a un symlink, le regole di autorizzazione controllano due percorsi: il symlink stesso e il file a cui si risolve. Le regole allow e deny trattano quella coppia diversamente: le regole allow ricadono nel richiedere un prompt, mentre le regole deny bloccano completamente.

* **Regole allow**: si applicano solo quando sia il percorso del symlink che il suo target corrispondono. Un symlink all'interno di una directory consentita che punta al di fuori di essa richiede comunque un prompt.
* **Regole deny**: si applicano quando il percorso del symlink o il suo target corrisponde. Un symlink che punta a un file negato è esso stesso negato.

Ad esempio, con `Read(./project/**)` consentito e `Read(~/.ssh/**)` negato, un symlink in `./project/key` che punta a `~/.ssh/id_rsa` viene bloccato: il target non supera la regola allow e corrisponde alla regola deny.

### WebFetch

* `WebFetch(domain:example.com)` corrisponde alle richieste di fetch a example.com

### MCP

* `mcp__puppeteer` corrisponde a qualsiasi strumento fornito dal server `puppeteer` (nome configurato in Claude Code)
* `mcp__puppeteer__*` sintassi con caratteri jolly che corrisponde anche a tutti gli strumenti dal server `puppeteer`
* `mcp__puppeteer__puppeteer_navigate` corrisponde allo strumento `puppeteer_navigate` fornito dal server `puppeteer`

### Agent (subagents)

Utilizzate le regole `Agent(AgentName)` per controllare quali [subagents](/it/sub-agents) Claude può utilizzare:

* `Agent(Explore)` corrisponde al subagent Explore
* `Agent(Plan)` corrisponde al subagent Plan
* `Agent(my-custom-agent)` corrisponde a un subagent personalizzato denominato `my-custom-agent`

Aggiungete queste regole all'array `deny` nelle vostre impostazioni o utilizzate il flag CLI `--disallowedTools` per disabilitare agenti specifici. Per disabilitare l'agente Explore:

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Estendere le autorizzazioni con hook

Gli [hook di Claude Code](/it/hooks-guide) forniscono un modo per registrare comandi shell personalizzati per eseguire la valutazione delle autorizzazioni in fase di esecuzione. Quando Claude Code effettua una chiamata di strumento, gli hook PreToolUse vengono eseguiti prima del prompt di autorizzazione. L'output dell'hook può negare la chiamata dello strumento, forzare un prompt o saltare il prompt per consentire alla chiamata di procedere.

Le decisioni dell'hook non bypassano le regole di autorizzazione. Le regole deny e ask vengono valutate indipendentemente da ciò che un hook PreToolUse restituisce, quindi una regola deny corrispondente blocca la chiamata e una regola ask corrispondente richiede comunque un prompt anche quando l'hook ha restituito `"allow"` o `"ask"`. Questo preserva la precedenza deny-first descritta in [Gestire le autorizzazioni](#manage-permissions), incluse le regole deny impostate nelle impostazioni gestite.

Un hook di blocco ha anche la precedenza sulle regole allow. Un hook che esce con codice 2 interrompe la chiamata dello strumento prima che le regole di autorizzazione vengono valutate, quindi il blocco si applica anche quando una regola allow consentirebbe altrimenti la chiamata. Per eseguire tutti i comandi Bash senza prompt tranne alcuni che desiderate bloccare, aggiungete `"Bash"` al vostro elenco allow e registrate un hook PreToolUse che rifiuta quei comandi specifici. Vedi [Bloccare le modifiche ai file protetti](/it/hooks-guide#block-edits-to-protected-files) per uno script di hook che potete adattare.

## Directory di lavoro

Per impostazione predefinita, Claude ha accesso ai file nella directory in cui è stato avviato. Potete estendere questo accesso:

* **Durante l'avvio**: utilizzate l'argomento CLI `--add-dir <path>`
* **Durante la sessione**: utilizzate il comando `/add-dir`
* **Configurazione persistente**: aggiungete a `additionalDirectories` nei [file di impostazioni](/it/settings#settings-files)

I file nelle directory aggiuntive seguono le stesse regole di autorizzazione della directory di lavoro originale: diventano leggibili senza prompt e le autorizzazioni di modifica dei file seguono la modalità di autorizzazione corrente.

### Le directory aggiuntive concedono l'accesso ai file, non la configurazione

L'aggiunta di una directory estende dove Claude può leggere e modificare i file. Non rende quella directory una radice di configurazione completa: la maggior parte della configurazione `.claude/` non viene scoperta dalle directory aggiuntive, anche se alcuni tipi vengono caricati come eccezioni.

I seguenti tipi di configurazione vengono caricati dalle directory `--add-dir`:

| Configurazione                                                     | Caricato da `--add-dir`                                                                                                                                                                  |
| :----------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Skills](/it/skills) in `.claude/skills/`                          | Sì, con ricaricamento live                                                                                                                                                               |
| Impostazioni plugin in `.claude/settings.json`                     | Solo `enabledPlugins` e `extraKnownMarketplaces`                                                                                                                                         |
| File [CLAUDE.md](/it/memory), `.claude/rules/` e `CLAUDE.local.md` | Solo quando `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` è impostato. `CLAUDE.local.md` richiede inoltre l'impostazione `local` source, che è abilitata per impostazione predefinita |

Tutto il resto, inclusi subagents, commands, output styles, hooks e altre impostazioni, viene scoperto solo dalla directory di lavoro corrente e dai suoi genitori, dalla vostra directory utente in `~/.claude/` e dalle impostazioni gestite. Per condividere quella configurazione tra progetti, utilizzate uno di questi approcci:

* **Configurazione a livello utente**: posizionate i file in `~/.claude/agents/`, `~/.claude/output-styles/` o `~/.claude/settings.json` per renderli disponibili in ogni progetto
* **Plugin**: pacchetto e distribuite la configurazione come [plugin](/it/plugins) che i team possono installare
* **Avviate dalla directory di configurazione**: eseguite Claude Code dalla directory contenente la configurazione `.claude/` che desiderate

## Come le autorizzazioni interagiscono con il sandboxing

Le autorizzazioni e il [sandboxing](/it/sandboxing) sono livelli di sicurezza complementari:

* **Autorizzazioni** controllano quali strumenti Claude Code può utilizzare e quali file o domini può accedere. Si applicano a tutti gli strumenti (Bash, Read, Edit, WebFetch, MCP e altri).
* **Sandboxing** fornisce l'applicazione a livello del sistema operativo che limita l'accesso al filesystem e alla rete dello strumento Bash. Si applica solo ai comandi Bash e ai loro processi figlio.

Utilizzate entrambi per la difesa in profondità:

* Le regole deny di autorizzazione impediscono a Claude di tentare anche di accedere alle risorse limitate
* Le restrizioni sandbox impediscono ai comandi Bash di raggiungere risorse al di fuori dei confini definiti, anche se un'iniezione di prompt bypassa il processo decisionale di Claude
* Le restrizioni del filesystem nella sandbox combinano le impostazioni [`sandbox.filesystem`](/it/sandboxing) con le regole deny di Read e Edit; entrambe vengono unite nel confine sandbox finale
* Le restrizioni di rete combinano le regole di autorizzazione WebFetch con gli elenchi `allowedDomains` e `deniedDomains` della sandbox

Quando il sandboxing è abilitato con `autoAllowBashIfSandboxed: true`, che è l'impostazione predefinita, i comandi Bash in sandbox vengono eseguiti senza richiedere un prompt anche se le vostre autorizzazioni includono `ask: Bash(*)`. Il confine della sandbox sostituisce il prompt per comando. Le regole deny esplicite si applicano ancora, e i comandi `rm` o `rmdir` che hanno come destinazione `/`, la vostra directory home o altri percorsi critici del sistema attivano comunque un prompt. Consultate [modalità sandbox](/it/sandboxing#sandbox-modes) per modificare questo comportamento.

## Impostazioni gestite

Per le organizzazioni che necessitano di un controllo centralizzato sulla configurazione di Claude Code, gli amministratori possono distribuire impostazioni gestite che non possono essere ignorate dalle impostazioni utente o di progetto. Queste impostazioni di criteri seguono lo stesso formato dei file di impostazioni regolari e possono essere fornite tramite criteri MDM/a livello del sistema operativo, file di impostazioni gestite o [impostazioni gestite dal server](/it/server-managed-settings). Vedi [file di impostazioni](/it/settings#settings-files) per i meccanismi di consegna e i percorsi dei file.

### Impostazioni solo gestite

Le seguenti impostazioni sono efficaci solo nelle impostazioni gestite. Posizionarle nei file di impostazioni utente o di progetto non ha alcun effetto.

| Impostazione                                   | Descrizione                                                                                                                                                                                                                                                                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Elenco di autorizzazione dei plugin di canale che possono inviare messaggi. Sostituisce l'elenco di autorizzazione Anthropic predefinito quando impostato. Richiede `channelsEnabled: true`. Vedi [Limitare quali plugin di canale possono essere eseguiti](/it/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Quando `true`, solo gli hook gestiti, gli hook SDK e gli hook dai plugin force-enabled nelle impostazioni gestite `enabledPlugins` vengono caricati. Gli hook utente, progetto e tutti gli altri plugin vengono bloccati                                                                                         |
| `allowManagedMcpServersOnly`                   | Quando `true`, solo `allowedMcpServers` dalle impostazioni gestite sono rispettati. `deniedMcpServers` si unisce comunque da tutte le fonti. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                                                                |
| `allowManagedPermissionRulesOnly`              | Quando `true`, impedisce alle impostazioni utente e di progetto di definire regole di autorizzazione `allow`, `ask` o `deny`. Si applicano solo le regole nelle impostazioni gestite                                                                                                                             |
| `blockedMarketplaces`                          | Elenco di blocco delle fonti del marketplace. Le fonti bloccate vengono controllate prima del download, quindi non toccano mai il filesystem. Vedi [restrizioni marketplace gestite](/it/plugin-marketplaces#managed-marketplace-restrictions)                                                                   |
| `channelsEnabled`                              | Consenti [channels](/it/channels) per l'organizzazione. Vedi [controlli aziendali](/it/channels#enterprise-controls) per l'impostazione predefinita su ogni piano                                                                                                                                                |
| `forceRemoteSettingsRefresh`                   | Quando `true`, blocca l'avvio della CLI fino a quando le impostazioni gestite remote non vengono recuperate di recente ed esce se il recupero non riesce. Vedi [applicazione fail-closed](/it/server-managed-settings#enforce-fail-closed-startup)                                                               |
| `pluginTrustMessage`                           | Messaggio personalizzato aggiunto all'avviso di fiducia del plugin mostrato prima dell'installazione                                                                                                                                                                                                             |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Quando `true`, solo i percorsi `filesystem.allowRead` dalle impostazioni gestite sono rispettati. `denyRead` si unisce comunque da tutte le fonti                                                                                                                                                                |
| `sandbox.network.allowManagedDomainsOnly`      | Quando `true`, solo `allowedDomains` e le regole allow `WebFetch(domain:...)` dalle impostazioni gestite sono rispettate. I domini non consentiti vengono bloccati automaticamente senza richiedere all'utente. I domini negati si uniscono comunque da tutte le fonti                                           |
| `strictKnownMarketplaces`                      | Controlla quali marketplace di plugin gli utenti possono aggiungere e installare plugin da. Vedi [restrizioni marketplace gestite](/it/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                     |
| `wslInheritsWindowsSettings`                   | Quando `true` nella chiave del registro HKLM di Windows o in `C:\Program Files\ClaudeCode\managed-settings.json`, WSL legge le impostazioni gestite dalla catena di criteri di Windows oltre a `/etc/claude-code`. Vedi [File di impostazioni](/it/settings#settings-files)                                      |

`disableBypassPermissionsMode` è tipicamente posizionato nelle impostazioni gestite per applicare la politica organizzativa, ma funziona da qualsiasi ambito. Un utente può impostarlo nelle proprie impostazioni per bloccarsi dalla modalità bypass.

<Note>
  Su piani Team e Enterprise, un amministratore abilita o disabilita [Remote Control](/it/remote-control) e [sessioni web](/it/claude-code-on-the-web) a livello organizzativo nelle [impostazioni di amministrazione di Claude Code](https://claude.ai/admin-settings/claude-code). Remote Control può inoltre essere disabilitato per dispositivo con l'impostazione gestita [`disableRemoteControl`](/it/settings#available-settings). Le sessioni web non hanno chiavi di impostazioni gestite per dispositivo.
</Note>

## Precedenza delle impostazioni

Le regole di autorizzazione seguono la stessa [precedenza delle impostazioni](/it/settings#settings-precedence) di tutte le altre impostazioni di Claude Code:

1. **Impostazioni gestite**: non possono essere ignorate da nessun altro livello, inclusi gli argomenti della riga di comando
2. **Argomenti della riga di comando**: override temporanei della sessione
3. **Impostazioni di progetto locale** (`.claude/settings.local.json`)
4. **Impostazioni di progetto condivise** (`.claude/settings.json`)
5. **Impostazioni utente** (`~/.claude/settings.json`)

Se uno strumento viene negato a qualsiasi livello, nessun altro livello può consentirlo. Ad esempio, un deny delle impostazioni gestite non può essere ignorato da `--allowedTools` e `--disallowedTools` può aggiungere restrizioni oltre a quelle definite dalle impostazioni gestite.

Se un'autorizzazione è consentita nelle impostazioni utente ma negata nelle impostazioni di progetto, l'impostazione di progetto ha la precedenza e l'autorizzazione viene bloccata.

## Configurazioni di esempio

Questo [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) include configurazioni di impostazioni iniziali per scenari di distribuzione comuni. Utilizzatele come punti di partenza e adattatele alle vostre esigenze.

## Vedi anche

* [Settings](/it/settings): riferimento di configurazione completo inclusa la tabella delle impostazioni di autorizzazione
* [Configure auto mode](/it/auto-mode-config): comunicate al classificatore della modalità auto quale infrastruttura la vostra organizzazione ritiene affidabile
* [Sandboxing](/it/sandboxing): isolamento del filesystem e della rete a livello del sistema operativo per i comandi Bash
* [Authentication](/it/authentication): configurate l'accesso utente a Claude Code
* [Security](/it/security): salvaguardie di sicurezza e best practice
* [Hooks](/it/hooks-guide): automatizzate i flussi di lavoro ed estendete la valutazione delle autorizzazioni
