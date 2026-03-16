> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurare le autorizzazioni

> Controlla cosa Claude Code può accedere e fare con regole di autorizzazione granulari, modalità e criteri gestiti.

Claude Code supporta autorizzazioni granulari in modo che tu possa specificare esattamente cosa l'agente è autorizzato a fare e cosa non può fare. Le impostazioni di autorizzazione possono essere archiviate nel controllo della versione e distribuite a tutti gli sviluppatori della tua organizzazione, nonché personalizzate dai singoli sviluppatori.

## Sistema di autorizzazione

Claude Code utilizza un sistema di autorizzazione a livelli per bilanciare potenza e sicurezza:

| Tipo di strumento | Esempio                    | Approvazione richiesta | Comportamento "Sì, non chiedere più"                |
| :---------------- | :------------------------- | :--------------------- | :-------------------------------------------------- |
| Sola lettura      | Letture di file, Grep      | No                     | N/A                                                 |
| Comandi Bash      | Esecuzione shell           | Sì                     | Permanentemente per directory di progetto e comando |
| Modifica di file  | Modifica/scrittura di file | Sì                     | Fino alla fine della sessione                       |

## Gestire le autorizzazioni

Puoi visualizzare e gestire le autorizzazioni degli strumenti di Claude Code con `/permissions`. Questa interfaccia utente elenca tutte le regole di autorizzazione e il file settings.json da cui provengono.

* Le regole **Allow** consentono a Claude Code di utilizzare lo strumento specificato senza approvazione manuale.
* Le regole **Ask** richiedono una conferma ogni volta che Claude Code tenta di utilizzare lo strumento specificato.
* Le regole **Deny** impediscono a Claude Code di utilizzare lo strumento specificato.

Le regole vengono valutate in ordine: **deny -> ask -> allow**. La prima regola corrispondente vince, quindi le regole deny hanno sempre la precedenza.

## Modalità di autorizzazione

Claude Code supporta diverse modalità di autorizzazione che controllano come gli strumenti vengono approvati. Imposta `defaultMode` nei tuoi [file di impostazioni](/it/settings#settings-files):

| Modalità            | Descrizione                                                                                                               |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| `default`           | Comportamento standard: richiede l'autorizzazione al primo utilizzo di ogni strumento                                     |
| `acceptEdits`       | Accetta automaticamente le autorizzazioni di modifica dei file per la sessione                                            |
| `plan`              | Plan Mode: Claude può analizzare ma non modificare file o eseguire comandi                                                |
| `dontAsk`           | Nega automaticamente gli strumenti a meno che non siano pre-approvati tramite `/permissions` o regole `permissions.allow` |
| `bypassPermissions` | Salta tutti i prompt di autorizzazione (richiede un ambiente sicuro, vedi avviso di seguito)                              |

<Warning>
  La modalità `bypassPermissions` disabilita tutti i controlli di autorizzazione. Utilizzala solo in ambienti isolati come contenitori o macchine virtuali dove Claude Code non può causare danni. Gli amministratori possono impedire questa modalità impostando `disableBypassPermissionsMode` su `"disable"` nelle [impostazioni gestite](#managed-settings).
</Warning>

## Sintassi delle regole di autorizzazione

Le regole di autorizzazione seguono il formato `Tool` o `Tool(specifier)`.

### Corrispondere a tutti gli utilizzi di uno strumento

Per corrispondere a tutti gli utilizzi di uno strumento, utilizza solo il nome dello strumento senza parentesi:

| Regola     | Effetto                                       |
| :--------- | :-------------------------------------------- |
| `Bash`     | Corrisponde a tutti i comandi Bash            |
| `WebFetch` | Corrisponde a tutte le richieste di web fetch |
| `Read`     | Corrisponde a tutte le letture di file        |

`Bash(*)` è equivalente a `Bash` e corrisponde a tutti i comandi Bash.

### Utilizzare gli specificatori per il controllo granulare

Aggiungi uno specificatore tra parentesi per corrispondere a utilizzi specifici dello strumento:

| Regola                         | Effetto                                                           |
| :----------------------------- | :---------------------------------------------------------------- |
| `Bash(npm run build)`          | Corrisponde al comando esatto `npm run build`                     |
| `Read(./.env)`                 | Corrisponde alla lettura del file `.env` nella directory corrente |
| `WebFetch(domain:example.com)` | Corrisponde alle richieste di fetch a example.com                 |

### Modelli con caratteri jolly

Le regole Bash supportano modelli glob con `*`. I caratteri jolly possono apparire in qualsiasi posizione nel comando. Questa configurazione consente comandi npm e git commit mentre blocca git push:

```json  theme={null}
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

Lo spazio prima di `*` è importante: `Bash(ls *)` corrisponde a `ls -la` ma non a `lsof`, mentre `Bash(ls*)` corrisponde a entrambi. La sintassi legacy con suffisso `:*` è equivalente a ` *` ma è deprecata.

## Regole di autorizzazione specifiche dello strumento

### Bash

Le regole di autorizzazione Bash supportano la corrispondenza con caratteri jolly con `*`. I caratteri jolly possono apparire in qualsiasi posizione nel comando, incluso all'inizio, nel mezzo o alla fine:

* `Bash(npm run build)` corrisponde al comando Bash esatto `npm run build`
* `Bash(npm run test *)` corrisponde ai comandi Bash che iniziano con `npm run test`
* `Bash(npm *)` corrisponde a qualsiasi comando che inizia con `npm `
* `Bash(* install)` corrisponde a qualsiasi comando che termina con ` install`
* `Bash(git * main)` corrisponde a comandi come `git checkout main`, `git merge main`

Quando `*` appare alla fine con uno spazio prima (come `Bash(ls *)`), applica un confine di parola, richiedendo che il prefisso sia seguito da uno spazio o dalla fine della stringa. Ad esempio, `Bash(ls *)` corrisponde a `ls -la` ma non a `lsof`. Al contrario, `Bash(ls*)` senza spazio corrisponde sia a `ls -la` che a `lsof` perché non c'è un vincolo di confine di parola.

<Tip>
  Claude Code è consapevole degli operatori shell (come `&&`) quindi una regola di corrispondenza del prefisso come `Bash(safe-cmd *)` non gli darà il permesso di eseguire il comando `safe-cmd && other-cmd`.
</Tip>

<Warning>
  I modelli di autorizzazione Bash che tentano di vincolare gli argomenti del comando sono fragili. Ad esempio, `Bash(curl http://github.com/ *)` intende limitare curl agli URL di GitHub, ma non corrisponderà a variazioni come:

  * Opzioni prima dell'URL: `curl -X GET http://github.com/...`
  * Protocollo diverso: `curl https://github.com/...`
  * Reindirizzamenti: `curl -L http://bit.ly/xyz` (reindirizza a github)
  * Variabili: `URL=http://github.com && curl $URL`
  * Spazi extra: `curl  http://github.com`

  Per un filtraggio URL più affidabile, considera:

  * **Limitare gli strumenti di rete Bash**: utilizza regole deny per bloccare `curl`, `wget` e comandi simili, quindi utilizza lo strumento WebFetch con l'autorizzazione `WebFetch(domain:github.com)` per i domini consentiti
  * **Utilizzare hook PreToolUse**: implementa un hook che convalida gli URL nei comandi Bash e blocca i domini non consentiti
  * Istruire Claude Code sui tuoi modelli curl consentiti tramite CLAUDE.md

  Nota che l'utilizzo di WebFetch da solo non impedisce l'accesso alla rete. Se Bash è consentito, Claude può comunque utilizzare `curl`, `wget` o altri strumenti per raggiungere qualsiasi URL.
</Warning>

### Read e Edit

Le regole `Edit` si applicano a tutti gli strumenti integrati che modificano i file. Claude fa un tentativo migliore per applicare le regole `Read` a tutti gli strumenti integrati che leggono file come Grep e Glob.

Le regole Read e Edit seguono entrambe la specifica [gitignore](https://git-scm.com/docs/gitignore) con quattro tipi di modello distinti:

| Modello           | Significato                                       | Esempio                          | Corrisponde                    |
| ----------------- | ------------------------------------------------- | -------------------------------- | ------------------------------ |
| `//path`          | Percorso **assoluto** dalla radice del filesystem | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`          | Percorso dalla directory **home**                 | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`           | Percorso **relativo alla radice del progetto**    | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` o `./path` | Percorso **relativo alla directory corrente**     | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  Un modello come `/Users/alice/file` NON è un percorso assoluto. È relativo alla radice del progetto. Utilizza `//Users/alice/file` per i percorsi assoluti.
</Warning>

Esempi:

* `Edit(/docs/**)`: modifica in `<project>/docs/` (NON `/docs/` e NON `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: legge il `.zshrc` della tua directory home
* `Edit(//tmp/scratch.txt)`: modifica il percorso assoluto `/tmp/scratch.txt`
* `Read(src/**)`: legge da `<current-directory>/src/`

<Note>
  Nei modelli gitignore, `*` corrisponde ai file in una singola directory mentre `**` corrisponde ricorsivamente tra le directory. Per consentire l'accesso a tutti i file, utilizza solo il nome dello strumento senza parentesi: `Read`, `Edit` o `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` corrisponde alle richieste di fetch a example.com

### MCP

* `mcp__puppeteer` corrisponde a qualsiasi strumento fornito dal server `puppeteer` (nome configurato in Claude Code)
* `mcp__puppeteer__*` sintassi con caratteri jolly che corrisponde anche a tutti gli strumenti dal server `puppeteer`
* `mcp__puppeteer__puppeteer_navigate` corrisponde allo strumento `puppeteer_navigate` fornito dal server `puppeteer`

### Agent (subagents)

Utilizza le regole `Agent(AgentName)` per controllare quali [subagents](/it/sub-agents) Claude può utilizzare:

* `Agent(Explore)` corrisponde al subagent Explore
* `Agent(Plan)` corrisponde al subagent Plan
* `Agent(my-custom-agent)` corrisponde a un subagent personalizzato denominato `my-custom-agent`

Aggiungi queste regole all'array `deny` nelle tue impostazioni o utilizza il flag CLI `--disallowedTools` per disabilitare agenti specifici. Per disabilitare l'agente Explore:

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Estendere le autorizzazioni con hook

Gli [hook di Claude Code](/it/hooks-guide) forniscono un modo per registrare comandi shell personalizzati per eseguire la valutazione delle autorizzazioni in fase di esecuzione. Quando Claude Code effettua una chiamata di strumento, gli hook PreToolUse vengono eseguiti prima del sistema di autorizzazione e l'output dell'hook può determinare se approvare o negare la chiamata dello strumento al posto del sistema di autorizzazione.

## Directory di lavoro

Per impostazione predefinita, Claude ha accesso ai file nella directory in cui è stato avviato. Puoi estendere questo accesso:

* **Durante l'avvio**: utilizza l'argomento CLI `--add-dir <path>`
* **Durante la sessione**: utilizza il comando `/add-dir`
* **Configurazione persistente**: aggiungi a `additionalDirectories` nei [file di impostazioni](/it/settings#settings-files)

I file nelle directory aggiuntive seguono le stesse regole di autorizzazione della directory di lavoro originale: diventano leggibili senza prompt e le autorizzazioni di modifica dei file seguono la modalità di autorizzazione corrente.

## Come le autorizzazioni interagiscono con il sandboxing

Le autorizzazioni e il [sandboxing](/it/sandboxing) sono livelli di sicurezza complementari:

* **Autorizzazioni** controllano quali strumenti Claude Code può utilizzare e quali file o domini può accedere. Si applicano a tutti gli strumenti (Bash, Read, Edit, WebFetch, MCP e altri).
* **Sandboxing** fornisce l'applicazione a livello del sistema operativo che limita l'accesso al filesystem e alla rete dello strumento Bash. Si applica solo ai comandi Bash e ai loro processi figlio.

Utilizza entrambi per la difesa in profondità:

* Le regole deny di autorizzazione impediscono a Claude di tentare anche di accedere alle risorse limitate
* Le restrizioni sandbox impediscono ai comandi Bash di raggiungere risorse al di fuori dei confini definiti, anche se un'iniezione di prompt bypassa il processo decisionale di Claude
* Le restrizioni del filesystem nella sandbox utilizzano le regole deny di Read e Edit, non una configurazione sandbox separata
* Le restrizioni di rete combinano le regole di autorizzazione WebFetch con l'elenco `allowedDomains` della sandbox

## Impostazioni gestite

Per le organizzazioni che necessitano di un controllo centralizzato sulla configurazione di Claude Code, gli amministratori possono distribuire impostazioni gestite che non possono essere ignorate dalle impostazioni utente o di progetto. Queste impostazioni di criteri seguono lo stesso formato dei file di impostazioni regolari e possono essere fornite tramite criteri MDM/a livello del sistema operativo, file di impostazioni gestite o [impostazioni gestite dal server](/it/server-managed-settings). Vedi [file di impostazioni](/it/settings#settings-files) per i meccanismi di consegna e i percorsi dei file.

### Impostazioni solo gestite

Alcune impostazioni sono efficaci solo nelle impostazioni gestite:

| Impostazione                              | Descrizione                                                                                                                                                                                                                                                            |
| :---------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | Imposta su `"disable"` per impedire la modalità `bypassPermissions` e il flag `--dangerously-skip-permissions`                                                                                                                                                         |
| `allowManagedPermissionRulesOnly`         | Quando `true`, impedisce alle impostazioni utente e di progetto di definire regole di autorizzazione `allow`, `ask` o `deny`. Si applicano solo le regole nelle impostazioni gestite                                                                                   |
| `allowManagedHooksOnly`                   | Quando `true`, impedisce il caricamento di hook utente, progetto e plugin. Sono consentiti solo hook gestiti e hook SDK                                                                                                                                                |
| `allowManagedMcpServersOnly`              | Quando `true`, solo `allowedMcpServers` dalle impostazioni gestite sono rispettati. `deniedMcpServers` si unisce comunque da tutte le fonti. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                      |
| `blockedMarketplaces`                     | Elenco di blocco delle fonti del marketplace. Le fonti bloccate vengono controllate prima del download, quindi non toccano mai il filesystem. Vedi [restrizioni marketplace gestite](/it/plugin-marketplaces#managed-marketplace-restrictions)                         |
| `sandbox.network.allowManagedDomainsOnly` | Quando `true`, solo `allowedDomains` e le regole allow `WebFetch(domain:...)` dalle impostazioni gestite sono rispettate. I domini non consentiti vengono bloccati automaticamente senza richiedere all'utente. I domini negati si uniscono comunque da tutte le fonti |
| `strictKnownMarketplaces`                 | Controlla quali marketplace di plugin gli utenti possono aggiungere. Vedi [restrizioni marketplace gestite](/it/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                  |
| `allow_remote_sessions`                   | Quando `true`, consente agli utenti di avviare [Remote Control](/it/remote-control) e [sessioni web](/it/claude-code-on-the-web). Predefinito su `true`. Imposta su `false` per impedire l'accesso alle sessioni remote                                                |

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

Questo [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) include configurazioni di impostazioni iniziali per scenari di distribuzione comuni. Utilizzale come punti di partenza e adattale alle tue esigenze.

## Vedi anche

* [Settings](/it/settings): riferimento di configurazione completo inclusa la tabella delle impostazioni di autorizzazione
* [Sandboxing](/it/sandboxing): isolamento del filesystem e della rete a livello del sistema operativo per i comandi Bash
* [Authentication](/it/authentication): configura l'accesso utente a Claude Code
* [Security](/it/security): salvaguardie di sicurezza e best practice
* [Hooks](/it/hooks-guide): automatizza i flussi di lavoro ed estendi la valutazione delle autorizzazioni
