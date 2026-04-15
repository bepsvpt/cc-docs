> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Come Claude ricorda il tuo progetto

> Fornisci a Claude istruzioni persistenti con file CLAUDE.md e lascia che Claude accumuli apprendimenti automaticamente con la memoria automatica.

Ogni sessione di Claude Code inizia con una finestra di contesto nuova. Due meccanismi trasportano la conoscenza tra le sessioni:

* **File CLAUDE.md**: istruzioni che scrivi per dare a Claude un contesto persistente
* **Memoria automatica**: note che Claude scrive da solo in base alle tue correzioni e preferenze

Questa pagina spiega come:

* [Scrivere e organizzare file CLAUDE.md](#claude-md-files)
* [Limitare le regole a tipi di file specifici](#organize-rules-with-claude/rules/) con `.claude/rules/`
* [Configurare la memoria automatica](#auto-memory) in modo che Claude prenda note automaticamente
* [Risolvere i problemi](#troubleshoot-memory-issues) quando le istruzioni non vengono seguite

## CLAUDE.md vs memoria automatica

Claude Code ha due sistemi di memoria complementari. Entrambi vengono caricati all'inizio di ogni conversazione. Claude li tratta come contesto, non come configurazione forzata. Più specifiche e concise sono le tue istruzioni, più coerentemente Claude le segue.

|                   | File CLAUDE.md                                                    | Memoria automatica                                                               |
| :---------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| **Chi lo scrive** | Tu                                                                | Claude                                                                           |
| **Cosa contiene** | Istruzioni e regole                                               | Apprendimenti e modelli                                                          |
| **Ambito**        | Progetto, utente o organizzazione                                 | Per worktree                                                                     |
| **Caricato in**   | Ogni sessione                                                     | Ogni sessione (prime 200 righe o 25KB)                                           |
| **Usare per**     | Standard di codifica, flussi di lavoro, architettura del progetto | Comandi di compilazione, approfondimenti sul debug, preferenze che Claude scopre |

Usa file CLAUDE.md quando vuoi guidare il comportamento di Claude. La memoria automatica consente a Claude di imparare dalle tue correzioni senza sforzo manuale.

I subagents possono anche mantenere la propria memoria automatica. Vedi [configurazione subagent](/it/sub-agents#enable-persistent-memory) per i dettagli.

## File CLAUDE.md

I file CLAUDE.md sono file markdown che forniscono a Claude istruzioni persistenti per un progetto, il tuo flusso di lavoro personale o l'intera organizzazione. Scrivi questi file in testo semplice; Claude li legge all'inizio di ogni sessione.

### Scegli dove mettere i file CLAUDE.md

I file CLAUDE.md possono trovarsi in diversi percorsi, ognuno con un ambito diverso. I percorsi più specifici hanno la precedenza su quelli più ampi.

| Ambito                     | Posizione                                                                                                                                                             | Scopo                                                   | Esempi di casi d'uso                                                            | Condiviso con                                         |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Politica gestita**       | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux e WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Istruzioni a livello organizzativo gestite da IT/DevOps | Standard di codifica aziendale, politiche di sicurezza, requisiti di conformità | Tutti gli utenti dell'organizzazione                  |
| **Istruzioni di progetto** | `./CLAUDE.md` o `./.claude/CLAUDE.md`                                                                                                                                 | Istruzioni condivise dal team per il progetto           | Architettura del progetto, standard di codifica, flussi di lavoro comuni        | Membri del team tramite controllo del codice sorgente |
| **Istruzioni utente**      | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferenze personali per tutti i progetti               | Preferenze di stile del codice, scorciatoie di strumenti personali              | Solo tu (tutti i progetti)                            |

I file CLAUDE.md nella gerarchia di directory sopra la directory di lavoro vengono caricati completamente all'avvio. I file CLAUDE.md nelle sottodirectory vengono caricati su richiesta quando Claude legge i file in quelle directory. Vedi [Come vengono caricati i file CLAUDE.md](#how-claude-md-files-load) per l'ordine di risoluzione completo.

Per i progetti di grandi dimensioni, puoi suddividere le istruzioni in file specifici per argomento utilizzando [regole di progetto](#organize-rules-with-claude/rules/). Le regole ti consentono di limitare le istruzioni a tipi di file specifici o sottodirectory.

### Configura un CLAUDE.md di progetto

Un CLAUDE.md di progetto può essere archiviato in `./CLAUDE.md` o `./.claude/CLAUDE.md`. Crea questo file e aggiungi istruzioni che si applicano a chiunque lavori sul progetto: comandi di compilazione e test, standard di codifica, decisioni architettoniche, convenzioni di denominazione e flussi di lavoro comuni. Queste istruzioni vengono condivise con il tuo team tramite controllo del codice sorgente, quindi concentrati su standard a livello di progetto piuttosto che su preferenze personali.

<Tip>
  Esegui `/init` per generare automaticamente un CLAUDE.md iniziale. Claude analizza la tua base di codice e crea un file con comandi di compilazione, istruzioni di test e convenzioni di progetto che scopre. Se esiste già un CLAUDE.md, `/init` suggerisce miglioramenti piuttosto che sovrascriverlo. Perfezionalo da lì con istruzioni che Claude non scoprirebbe da solo.

  Imposta `CLAUDE_CODE_NEW_INIT=1` per abilitare un flusso interattivo multi-fase. `/init` chiede quali artefatti configurare: file CLAUDE.md, skills e hooks. Quindi esplora la tua base di codice con un subagent, colma le lacune tramite domande di follow-up e presenta una proposta revisionabile prima di scrivere qualsiasi file.
</Tip>

### Scrivi istruzioni efficaci

I file CLAUDE.md vengono caricati nella finestra di contesto all'inizio di ogni sessione, consumando token insieme alla tua conversazione. La [visualizzazione della finestra di contesto](/it/context-window) mostra dove CLAUDE.md si carica rispetto al resto del contesto di avvio. Poiché sono contesto piuttosto che configurazione forzata, il modo in cui scrivi le istruzioni influisce su quanto affidabilmente Claude le segue. Le istruzioni specifiche, concise e ben strutturate funzionano meglio.

**Dimensione**: punta a meno di 200 righe per file CLAUDE.md. I file più lunghi consumano più contesto e riducono l'aderenza. Se le tue istruzioni stanno crescendo molto, dividile usando [importazioni](#import-additional-files) o file [`.claude/rules/`](#organize-rules-with-claude/rules/).

**Struttura**: usa intestazioni e punti elenco markdown per raggruppare le istruzioni correlate. Claude scansiona la struttura nello stesso modo in cui i lettori lo fanno: le sezioni organizzate sono più facili da seguire rispetto ai paragrafi densi.

**Specificità**: scrivi istruzioni abbastanza concrete da poter verificare. Ad esempio:

* "Usa indentazione a 2 spazi" invece di "Formatta il codice correttamente"
* "Esegui `npm test` prima di eseguire il commit" invece di "Testa le tue modifiche"
* "I gestori API si trovano in `src/api/handlers/`" invece di "Mantieni i file organizzati"

**Coerenza**: se due regole si contraddicono a vicenda, Claude potrebbe sceglierne una arbitrariamente. Rivedi periodicamente i tuoi file CLAUDE.md, i file CLAUDE.md annidati nelle sottodirectory e i file [`.claude/rules/`](#organize-rules-with-claude/rules/) per rimuovere istruzioni obsolete o conflittuali. Nei monorepo, usa [`claudeMdExcludes`](#exclude-specific-claude-md-files) per saltare i file CLAUDE.md di altri team che non sono rilevanti per il tuo lavoro.

### Importa file aggiuntivi

I file CLAUDE.md possono importare file aggiuntivi usando la sintassi `@path/to/import`. I file importati vengono espansi e caricati nel contesto all'avvio insieme al CLAUDE.md che li riferisce.

Sono consentiti sia i percorsi relativi che assoluti. I percorsi relativi si risolvono rispetto al file che contiene l'importazione, non alla directory di lavoro. I file importati possono importare ricorsivamente altri file, con una profondità massima di cinque hop.

Per includere un README, package.json e una guida al flusso di lavoro, fai riferimento ad essi con la sintassi `@` in qualsiasi punto del tuo CLAUDE.md:

```text theme={null}
Vedi @README per la panoramica del progetto e @package.json per i comandi npm disponibili per questo progetto.

# Istruzioni aggiuntive
- flusso di lavoro git @docs/git-instructions.md
```

Per le preferenze personali che non vuoi archiviare, importa un file dalla tua home directory. L'importazione va nel CLAUDE.md condiviso, ma il file a cui punta rimane sulla tua macchina:

```text theme={null}
# Preferenze individuali
- @~/.claude/my-project-instructions.md
```

<Warning>
  La prima volta che Claude Code incontra importazioni esterne in un progetto, mostra una finestra di dialogo di approvazione che elenca i file. Se rifiuti, le importazioni rimangono disabilitate e la finestra di dialogo non appare di nuovo.
</Warning>

Per un approccio più strutturato all'organizzazione delle istruzioni, vedi [`.claude/rules/`](#organize-rules-with-claude/rules/).

### AGENTS.md

Claude Code legge `CLAUDE.md`, non `AGENTS.md`. Se il tuo repository utilizza già `AGENTS.md` per altri agenti di codifica, crea un `CLAUDE.md` che lo importa in modo che entrambi gli strumenti leggano le stesse istruzioni senza duplicarle. Puoi anche aggiungere istruzioni specifiche di Claude Code sotto l'importazione. Claude carica il file importato all'inizio della sessione, quindi aggiunge il resto:

```markdown CLAUDE.md theme={null}
@AGENTS.md

## Claude Code

Usa plan mode per le modifiche in `src/billing/`.
```

### Come vengono caricati i file CLAUDE.md

Claude Code legge i file CLAUDE.md camminando verso l'alto nell'albero delle directory dalla tua directory di lavoro corrente, controllando ogni directory lungo il percorso. Ciò significa che se esegui Claude Code in `foo/bar/`, carica le istruzioni sia da `foo/bar/CLAUDE.md` che da `foo/CLAUDE.md`.

Claude scopre anche i file CLAUDE.md nelle sottodirectory sotto la tua directory di lavoro corrente. Invece di caricarli all'avvio, vengono inclusi quando Claude legge i file in quelle sottodirectory.

Se lavori in un grande monorepo dove i file CLAUDE.md di altri team vengono raccolti, usa [`claudeMdExcludes`](#exclude-specific-claude-md-files) per saltarli.

I commenti HTML a livello di blocco (`<!-- maintainer notes -->`) nei file CLAUDE.md vengono rimossi prima che il contenuto venga iniettato nel contesto di Claude. Usali per lasciare note per i manutentori umani senza spendere token di contesto su di essi. I commenti all'interno dei blocchi di codice vengono preservati. Quando apri un file CLAUDE.md direttamente con lo strumento Read, i commenti rimangono visibili.

#### Carica da directory aggiuntive

Il flag `--add-dir` dà a Claude accesso a directory aggiuntive al di fuori della tua directory di lavoro principale. Per impostazione predefinita, i file CLAUDE.md da queste directory non vengono caricati.

Per caricare anche i file CLAUDE.md da directory aggiuntive, inclusi `CLAUDE.md`, `.claude/CLAUDE.md` e `.claude/rules/*.md`, imposta la variabile di ambiente `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Organizza le regole con `.claude/rules/`

Per i progetti più grandi, puoi organizzare le istruzioni in più file usando la directory `.claude/rules/`. Questo mantiene le istruzioni modulari e più facili da mantenere per i team. Le regole possono anche essere [limitate a percorsi di file specifici](#path-specific-rules), quindi vengono caricate nel contesto solo quando Claude lavora con file corrispondenti, riducendo il rumore e risparmiando spazio di contesto.

<Note>
  Le regole vengono caricate nel contesto ogni sessione o quando vengono aperti file corrispondenti. Per le istruzioni specifiche dell'attività che non devono essere nel contesto tutto il tempo, usa [skills](/it/skills) invece, che vengono caricate solo quando le invochi o quando Claude determina che sono rilevanti per il tuo prompt.
</Note>

#### Configura le regole

Posiziona i file markdown nella directory `.claude/rules/` del tuo progetto. Ogni file dovrebbe coprire un argomento, con un nome file descrittivo come `testing.md` o `api-design.md`. Tutti i file `.md` vengono scoperti ricorsivamente, quindi puoi organizzare le regole in sottodirectory come `frontend/` o `backend/`:

```text theme={null}
your-project/
├── .claude/
│   ├── CLAUDE.md           # Istruzioni principali del progetto
│   └── rules/
│       ├── code-style.md   # Linee guida di stile del codice
│       ├── testing.md      # Convenzioni di test
│       └── security.md     # Requisiti di sicurezza
```

Le regole senza [frontmatter `paths`](#path-specific-rules) vengono caricate all'avvio con la stessa priorità di `.claude/CLAUDE.md`.

#### Regole specifiche del percorso

Le regole possono essere limitate a file specifici usando il frontmatter YAML con il campo `paths`. Queste regole condizionali si applicano solo quando Claude lavora con file che corrispondono ai modelli specificati.

```markdown theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Regole di sviluppo API

- Tutti gli endpoint API devono includere la convalida dell'input
- Usa il formato di risposta di errore standard
- Includi commenti di documentazione OpenAPI
```

Le regole senza un campo `paths` vengono caricate incondizionatamente e si applicano a tutti i file. Le regole con ambito di percorso si attivano quando Claude legge file che corrispondono al modello, non ad ogni utilizzo dello strumento.

Usa modelli glob nel campo `paths` per abbinare i file per estensione, directory o qualsiasi combinazione:

| Modello                | Corrisponde a                                  |
| ---------------------- | ---------------------------------------------- |
| `**/*.ts`              | Tutti i file TypeScript in qualsiasi directory |
| `src/**/*`             | Tutti i file nella directory `src/`            |
| `*.md`                 | File Markdown nella radice del progetto        |
| `src/components/*.tsx` | Componenti React in una directory specifica    |

Puoi specificare più modelli e usare l'espansione tra parentesi graffe per abbinare più estensioni in un modello:

```markdown theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Condividi le regole tra i progetti con symlink

La directory `.claude/rules/` supporta symlink, quindi puoi mantenere un set di regole condivise e collegarle a più progetti. I symlink vengono risolti e caricati normalmente, e i symlink circolari vengono rilevati e gestiti correttamente.

Questo esempio collega sia una directory condivisa che un file individuale:

```bash theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### Regole a livello di utente

Le regole personali in `~/.claude/rules/` si applicano a ogni progetto sulla tua macchina. Usale per le preferenze che non sono specifiche del progetto:

```text theme={null}
~/.claude/rules/
├── preferences.md    # Le tue preferenze di codifica personali
└── workflows.md      # I tuoi flussi di lavoro preferiti
```

Le regole a livello di utente vengono caricate prima delle regole di progetto, dando alle regole di progetto una priorità più alta.

### Gestisci CLAUDE.md per team di grandi dimensioni

Per le organizzazioni che distribuiscono Claude Code tra i team, puoi centralizzare le istruzioni e controllare quali file CLAUDE.md vengono caricati.

#### Distribuisci CLAUDE.md a livello di organizzazione

Le organizzazioni possono distribuire un CLAUDE.md gestito centralmente che si applica a tutti gli utenti su una macchina. Questo file non può essere escluso dalle impostazioni individuali.

<Steps>
  <Step title="Crea il file nella posizione della politica gestita">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux e WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Distribuisci con il tuo sistema di gestione della configurazione">
    Usa MDM, Group Policy, Ansible o strumenti simili per distribuire il file tra le macchine degli sviluppatori. Vedi [impostazioni gestite](/it/permissions#managed-settings) per altre opzioni di configurazione a livello di organizzazione.
  </Step>
</Steps>

Un CLAUDE.md gestito e [impostazioni gestite](/it/settings#settings-files) servono a scopi diversi. Usa le impostazioni per l'applicazione tecnica e CLAUDE.md per la guida comportamentale:

| Preoccupazione                                         | Configura in                                                  |
| :----------------------------------------------------- | :------------------------------------------------------------ |
| Blocca strumenti, comandi o percorsi di file specifici | Impostazioni gestite: `permissions.deny`                      |
| Applica l'isolamento sandbox                           | Impostazioni gestite: `sandbox.enabled`                       |
| Variabili di ambiente e routing del provider API       | Impostazioni gestite: `env`                                   |
| Metodo di autenticazione e blocco dell'organizzazione  | Impostazioni gestite: `forceLoginMethod`, `forceLoginOrgUUID` |
| Linee guida di stile del codice e qualità              | CLAUDE.md gestito                                             |
| Promemoria sulla gestione dei dati e conformità        | CLAUDE.md gestito                                             |
| Istruzioni comportamentali per Claude                  | CLAUDE.md gestito                                             |

Le regole delle impostazioni vengono applicate dal client indipendentemente da ciò che Claude decide di fare. Le istruzioni CLAUDE.md modellano il comportamento di Claude ma non sono un livello di applicazione rigido.

#### Escludi file CLAUDE.md specifici

Nei grandi monorepo, i file CLAUDE.md antenati possono contenere istruzioni che non sono rilevanti per il tuo lavoro. L'impostazione `claudeMdExcludes` ti consente di saltare file specifici per percorso o modello glob.

Questo esempio esclude un CLAUDE.md di primo livello e una directory di regole da una cartella padre. Aggiungilo a `.claude/settings.local.json` in modo che l'esclusione rimanga locale alla tua macchina:

```json theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

I modelli vengono abbinati ai percorsi di file assoluti usando la sintassi glob. Puoi configurare `claudeMdExcludes` in qualsiasi [livello di impostazioni](/it/settings#settings-files): utente, progetto, locale o politica gestita. Gli array si uniscono tra i livelli.

I file CLAUDE.md della politica gestita non possono essere esclusi. Ciò garantisce che le istruzioni a livello di organizzazione si applichino sempre indipendentemente dalle impostazioni individuali.

## Memoria automatica

La memoria automatica consente a Claude di accumulare conoscenze tra le sessioni senza che tu scriva nulla. Claude salva note per se stesso mentre lavora: comandi di compilazione, approfondimenti sul debug, note sull'architettura, preferenze di stile del codice e abitudini di flusso di lavoro. Claude non salva qualcosa ogni sessione. Decide cosa vale la pena ricordare in base al fatto che l'informazione sarebbe utile in una conversazione futura.

<Note>
  La memoria automatica richiede Claude Code v2.1.59 o successivo. Controlla la tua versione con `claude --version`.
</Note>

### Abilita o disabilita la memoria automatica

La memoria automatica è attivata per impostazione predefinita. Per attivarla/disattivarla, apri `/memory` in una sessione e usa l'interruttore di memoria automatica, oppure imposta `autoMemoryEnabled` nelle impostazioni del tuo progetto:

```json theme={null}
{
  "autoMemoryEnabled": false
}
```

Per disabilitare la memoria automatica tramite variabile di ambiente, imposta `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Posizione di archiviazione

Ogni progetto ottiene la propria directory di memoria in `~/.claude/projects/<project>/memory/`. Il percorso `<project>` è derivato dal repository git, quindi tutti i worktrees e le sottodirectory all'interno dello stesso repo condividono una directory di memoria automatica. Al di fuori di un repository git, viene utilizzata la radice del progetto.

Per archiviare la memoria automatica in una posizione diversa, imposta `autoMemoryDirectory` nelle impostazioni dell'utente o locali:

```json theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

Questa impostazione è accettata dalle impostazioni di politica, locali e utente. Non è accettata dalle impostazioni di progetto (`.claude/settings.json`) per evitare che un progetto condiviso reindirizza le scritture di memoria automatica a posizioni sensibili.

La directory contiene un punto di ingresso `MEMORY.md` e file di argomento opzionali:

```text theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Indice conciso, caricato in ogni sessione
├── debugging.md       # Note dettagliate sui modelli di debug
├── api-conventions.md # Decisioni di progettazione API
└── ...                # Qualsiasi altro file di argomento che Claude crea
```

`MEMORY.md` funge da indice della directory di memoria. Claude legge e scrive file in questa directory durante la tua sessione, usando `MEMORY.md` per tenere traccia di ciò che è archiviato dove.

La memoria automatica è locale alla macchina. Tutti i worktrees e le sottodirectory all'interno dello stesso repository git condividono una directory di memoria automatica. I file non vengono condivisi tra macchine o ambienti cloud.

### Come funziona

Le prime 200 righe di `MEMORY.md`, o i primi 25KB, a seconda di quale viene raggiunto per primo, vengono caricate all'inizio di ogni conversazione. Il contenuto oltre quella soglia non viene caricato all'inizio della sessione. Claude mantiene `MEMORY.md` conciso spostando le note dettagliate in file di argomento separati.

Questo limite si applica solo a `MEMORY.md`. I file CLAUDE.md vengono caricati completamente indipendentemente dalla lunghezza, anche se i file più brevi producono una migliore aderenza.

I file di argomento come `debugging.md` o `patterns.md` non vengono caricati all'avvio. Claude li legge su richiesta usando i suoi strumenti di file standard quando ha bisogno delle informazioni.

Claude legge e scrive file di memoria durante la tua sessione. Quando vedi "Writing memory" o "Recalled memory" nell'interfaccia di Claude Code, Claude sta attivamente aggiornando o leggendo da `~/.claude/projects/<project>/memory/`.

### Controlla e modifica la tua memoria

I file di memoria automatica sono markdown semplice che puoi modificare o eliminare in qualsiasi momento. Esegui [`/memory`](#view-and-edit-with-memory) per sfogliare e aprire i file di memoria da una sessione.

## Visualizza e modifica con `/memory`

Il comando `/memory` elenca tutti i file CLAUDE.md e rules caricati nella tua sessione corrente, ti consente di attivare o disattivare la memoria automatica e fornisce un collegamento per aprire la cartella di memoria automatica. Seleziona qualsiasi file per aprirlo nel tuo editor.

Quando chiedi a Claude di ricordare qualcosa, come "usa sempre pnpm, non npm" o "ricorda che i test API richiedono un'istanza Redis locale", Claude lo salva nella memoria automatica. Per aggiungere istruzioni a CLAUDE.md, chiedi direttamente a Claude, come "aggiungi questo a CLAUDE.md", oppure modifica il file tu stesso tramite `/memory`.

## Risolvi i problemi di memoria

Questi sono i problemi più comuni con CLAUDE.md e la memoria automatica, insieme ai passaggi per risolverli.

### Claude non sta seguendo il mio CLAUDE.md

Il contenuto di CLAUDE.md viene consegnato come messaggio utente dopo il prompt di sistema, non come parte del prompt di sistema stesso. Claude lo legge e cerca di seguirlo, ma non c'è garanzia di conformità rigorosa, specialmente per istruzioni vaghe o conflittuali.

Per eseguire il debug:

* Esegui `/memory` per verificare che i tuoi file CLAUDE.md vengono caricati. Se un file non è elencato, Claude non può vederlo.
* Verifica che il CLAUDE.md rilevante si trovi in una posizione che viene caricata per la tua sessione (vedi [Scegli dove mettere i file CLAUDE.md](#choose-where-to-put-claude-md-files)).
* Rendi le istruzioni più specifiche. "Usa indentazione a 2 spazi" funziona meglio di "formatta il codice bene".
* Cerca istruzioni conflittuali tra i file CLAUDE.md. Se due file danno una guida diversa per lo stesso comportamento, Claude potrebbe sceglierne una arbitrariamente.

Per le istruzioni che vuoi a livello di prompt di sistema, usa [`--append-system-prompt`](/it/cli-reference#system-prompt-flags). Questo deve essere passato ad ogni invocazione, quindi è più adatto a script e automazione che all'uso interattivo.

<Tip>
  Usa l'hook [`InstructionsLoaded`](/it/hooks#instructionsloaded) per registrare esattamente quali file di istruzioni vengono caricati, quando vengono caricati e perché. Questo è utile per eseguire il debug di regole specifiche del percorso o file caricati pigriamente nelle sottodirectory.
</Tip>

### Non so cosa ha salvato la memoria automatica

Esegui `/memory` e seleziona la cartella di memoria automatica per sfogliare ciò che Claude ha salvato. Tutto è markdown semplice che puoi leggere, modificare o eliminare.

### Il mio CLAUDE.md è troppo grande

I file con più di 200 righe consumano più contesto e possono ridurre l'aderenza. Sposta il contenuto dettagliato in file separati a cui si fa riferimento con importazioni `@path` (vedi [Importa file aggiuntivi](#import-additional-files)), oppure dividi le tue istruzioni tra file `.claude/rules/`.

### Le istruzioni sembrano perse dopo `/compact`

CLAUDE.md sopravvive completamente alla compattazione. Dopo `/compact`, Claude rilegge il tuo CLAUDE.md dal disco e lo reinetta fresco nella sessione. Se un'istruzione è scomparsa dopo la compattazione, è stata data solo nella conversazione, non scritta su CLAUDE.md. Aggiungila a CLAUDE.md per farla persistere tra le sessioni.

Vedi [Scrivi istruzioni efficaci](#write-effective-instructions) per una guida su dimensione, struttura e specificità.

## Risorse correlate

* [Skills](/it/skills): pacchetto di flussi di lavoro ripetibili che si caricano su richiesta
* [Impostazioni](/it/settings): configura il comportamento di Claude Code con file di impostazioni
* [Gestisci sessioni](/it/sessions): gestisci il contesto, riprendi conversazioni ed esegui sessioni parallele
* [Memoria subagent](/it/sub-agents#enable-persistent-memory): consenti ai subagents di mantenere la propria memoria automatica
