> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Come Claude ricorda il vostro progetto

> Fornite a Claude istruzioni persistenti con file CLAUDE.md e lasciate che Claude accumuli apprendimenti automaticamente con la memoria automatica.

Ogni sessione di Claude Code inizia con una finestra di contesto nuova. Due meccanismi trasportano la conoscenza tra le sessioni:

* **File CLAUDE.md**: istruzioni che scrivete per dare a Claude un contesto persistente
* **Memoria automatica**: note che Claude scrive da solo in base alle vostre correzioni e preferenze

Questa pagina spiega come:

* [Scrivere e organizzare file CLAUDE.md](#claudemd-files)
* [Limitare le regole a tipi di file specifici](#organize-rules-with-clauderules) con `.claude/rules/`
* [Configurare la memoria automatica](#auto-memory) in modo che Claude prenda note automaticamente
* [Risolvere i problemi](#troubleshoot-memory-issues) quando le istruzioni non vengono seguite

## CLAUDE.md vs memoria automatica

Claude Code ha due sistemi di memoria complementari. Entrambi vengono caricati all'inizio di ogni conversazione. Claude li tratta come contesto, non come configurazione forzata. Più specifiche e concise sono le vostre istruzioni, più coerentemente Claude le segue.

|                   | File CLAUDE.md                                                    | Memoria automatica                                                               |
| :---------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| **Chi lo scrive** | Voi                                                               | Claude                                                                           |
| **Cosa contiene** | Istruzioni e regole                                               | Apprendimenti e modelli                                                          |
| **Ambito**        | Progetto, utente o organizzazione                                 | Per worktree                                                                     |
| **Caricato in**   | Ogni sessione                                                     | Ogni sessione (prime 200 righe)                                                  |
| **Usare per**     | Standard di codifica, flussi di lavoro, architettura del progetto | Comandi di compilazione, approfondimenti sul debug, preferenze che Claude scopre |

Usate i file CLAUDE.md quando volete guidare il comportamento di Claude. La memoria automatica permette a Claude di imparare dalle vostre correzioni senza sforzo manuale.

I subagents possono anche mantenere la loro propria memoria automatica. Consultate la [configurazione dei subagent](/it/sub-agents#enable-persistent-memory) per i dettagli.

## File CLAUDE.md

I file CLAUDE.md sono file markdown che forniscono a Claude istruzioni persistenti per un progetto, il vostro flusso di lavoro personale o l'intera organizzazione. Scrivete questi file in testo semplice; Claude li legge all'inizio di ogni sessione.

### Scegliere dove mettere i file CLAUDE.md

I file CLAUDE.md possono trovarsi in diversi percorsi, ognuno con un ambito diverso. I percorsi più specifici hanno la precedenza su quelli più ampi.

| Ambito                      | Percorso                                                                                                                                                              | Scopo                                                   | Esempi di casi d'uso                                                            | Condiviso con                                         |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Politica gestita**        | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux e WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Istruzioni a livello organizzativo gestite da IT/DevOps | Standard di codifica aziendale, politiche di sicurezza, requisiti di conformità | Tutti gli utenti dell'organizzazione                  |
| **Istruzioni del progetto** | `./CLAUDE.md` o `./.claude/CLAUDE.md`                                                                                                                                 | Istruzioni condivise dal team per il progetto           | Architettura del progetto, standard di codifica, flussi di lavoro comuni        | Membri del team tramite controllo del codice sorgente |
| **Istruzioni dell'utente**  | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferenze personali per tutti i progetti               | Preferenze di stile del codice, scorciatoie di strumenti personali              | Solo voi (tutti i progetti)                           |

I file CLAUDE.md nella gerarchia di directory sopra la directory di lavoro vengono caricati completamente all'avvio. I file CLAUDE.md nelle sottodirectory vengono caricati su richiesta quando Claude legge i file in quelle directory. Consultate [Come vengono caricati i file CLAUDE.md](#how-claudemd-files-load) per l'ordine di risoluzione completo.

Per i progetti di grandi dimensioni, potete suddividere le istruzioni in file specifici per argomento utilizzando [regole di progetto](#organize-rules-with-clauderules). Le regole vi permettono di limitare le istruzioni a tipi di file specifici o sottodirectory.

### Configurare un CLAUDE.md di progetto

Un CLAUDE.md di progetto può essere archiviato in `./CLAUDE.md` o `./.claude/CLAUDE.md`. Create questo file e aggiungete istruzioni che si applicano a chiunque lavori sul progetto: comandi di compilazione e test, standard di codifica, decisioni architettoniche, convenzioni di denominazione e flussi di lavoro comuni. Queste istruzioni vengono condivise con il vostro team tramite controllo del codice sorgente, quindi concentratevi su standard a livello di progetto piuttosto che su preferenze personali.

<Tip>
  Eseguite `/init` per generare automaticamente un CLAUDE.md iniziale. Claude analizza la vostra base di codice e crea un file con comandi di compilazione, istruzioni di test e convenzioni di progetto che scopre. Se un CLAUDE.md esiste già, `/init` suggerisce miglioramenti piuttosto che sovrascriverlo. Perfezionate da lì con istruzioni che Claude non scoprirebbe da solo.
</Tip>

### Scrivere istruzioni efficaci

I file CLAUDE.md vengono caricati nella finestra di contesto all'inizio di ogni sessione, consumando token insieme alla vostra conversazione. Poiché sono contesto e non configurazione forzata, il modo in cui scrivete le istruzioni influisce su quanto affidabilmente Claude le segue. Le istruzioni specifiche, concise e ben strutturate funzionano meglio.

**Dimensione**: mirate a meno di 200 righe per file CLAUDE.md. I file più lunghi consumano più contesto e riducono l'aderenza. Se le vostre istruzioni stanno crescendo molto, dividetele utilizzando [importazioni](#import-additional-files) o file [`.claude/rules/`](#organize-rules-with-clauderules).

**Struttura**: usate intestazioni markdown e punti elenco per raggruppare le istruzioni correlate. Claude scansiona la struttura nello stesso modo in cui i lettori lo fanno: le sezioni organizzate sono più facili da seguire rispetto ai paragrafi densi.

**Specificità**: scrivete istruzioni abbastanza concrete da poter verificare. Ad esempio:

* "Usate l'indentazione a 2 spazi" invece di "Formattate il codice correttamente"
* "Eseguite `npm test` prima di eseguire il commit" invece di "Testate le vostre modifiche"
* "I gestori API si trovano in `src/api/handlers/`" invece di "Mantenete i file organizzati"

**Coerenza**: se due regole si contraddicono a vicenda, Claude potrebbe sceglierne una arbitrariamente. Esaminate periodicamente i vostri file CLAUDE.md, i file CLAUDE.md annidati nelle sottodirectory e i file [`.claude/rules/`](#organize-rules-with-clauderules) per rimuovere istruzioni obsolete o conflittuali. Nei monorepo, usate [`claudeMdExcludes`](#exclude-specific-claudemd-files) per saltare i file CLAUDE.md di altri team che non sono rilevanti per il vostro lavoro.

### Importare file aggiuntivi

I file CLAUDE.md possono importare file aggiuntivi utilizzando la sintassi `@path/to/import`. I file importati vengono espansi e caricati nel contesto all'avvio insieme al CLAUDE.md che li riferisce.

Sono consentiti sia i percorsi relativi che assoluti. I percorsi relativi si risolvono rispetto al file che contiene l'importazione, non alla directory di lavoro. I file importati possono importare ricorsivamente altri file, con una profondità massima di cinque hop.

Per includere un README, package.json e una guida al flusso di lavoro, fate riferimento ad essi con la sintassi `@` in qualsiasi punto del vostro CLAUDE.md:

```text  theme={null}
Consultate @README per una panoramica del progetto e @package.json per i comandi npm disponibili per questo progetto.

# Istruzioni aggiuntive
- flusso di lavoro git @docs/git-instructions.md
```

Per le preferenze personali che non volete archiviare, importate un file dalla vostra home directory. L'importazione va nel CLAUDE.md condiviso, ma il file a cui punta rimane sulla vostra macchina:

```text  theme={null}
# Preferenze individuali
- @~/.claude/my-project-instructions.md
```

<Warning>
  La prima volta che Claude Code incontra importazioni esterne in un progetto, mostra una finestra di dialogo di approvazione che elenca i file. Se rifiutate, le importazioni rimangono disabilitate e la finestra di dialogo non appare di nuovo.
</Warning>

Per un approccio più strutturato all'organizzazione delle istruzioni, consultate [`.claude/rules/`](#organize-rules-with-clauderules).

### Come vengono caricati i file CLAUDE.md

Claude Code legge i file CLAUDE.md camminando verso l'alto nell'albero delle directory dalla vostra directory di lavoro corrente, controllando ogni directory lungo il percorso. Ciò significa che se eseguite Claude Code in `foo/bar/`, carica le istruzioni sia da `foo/bar/CLAUDE.md` che da `foo/CLAUDE.md`.

Claude scopre anche i file CLAUDE.md nelle sottodirectory sotto la vostra directory di lavoro corrente. Invece di caricarli all'avvio, vengono inclusi quando Claude legge i file in quelle sottodirectory.

Se lavorate in un grande monorepo dove i file CLAUDE.md di altri team vengono raccolti, usate [`claudeMdExcludes`](#exclude-specific-claudemd-files) per saltarli.

#### Caricare da directory aggiuntive

Il flag `--add-dir` dà a Claude accesso a directory aggiuntive al di fuori della vostra directory di lavoro principale. Per impostazione predefinita, i file CLAUDE.md da queste directory non vengono caricati.

Per caricare anche i file CLAUDE.md da directory aggiuntive, inclusi `CLAUDE.md`, `.claude/CLAUDE.md` e `.claude/rules/*.md`, impostate la variabile di ambiente `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash  theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Organizzare le regole con `.claude/rules/`

Per i progetti più grandi, potete organizzare le istruzioni in più file utilizzando la directory `.claude/rules/`. Ciò mantiene le istruzioni modulari e più facili da mantenere per i team. Le regole possono anche essere [limitate a percorsi di file specifici](#path-specific-rules), quindi vengono caricate nel contesto solo quando Claude lavora con file corrispondenti, riducendo il rumore e risparmiando spazio di contesto.

<Note>
  Le regole vengono caricate nel contesto ogni sessione o quando vengono aperti file corrispondenti. Per le istruzioni specifiche di un'attività che non devono essere nel contesto tutto il tempo, usate [skills](/it/skills) invece, che vengono caricate solo quando le richiamate o quando Claude determina che sono rilevanti per il vostro prompt.
</Note>

#### Configurare le regole

Posizionate i file markdown nella directory `.claude/rules/` del vostro progetto. Ogni file dovrebbe coprire un argomento, con un nome file descrittivo come `testing.md` o `api-design.md`. Tutti i file `.md` vengono scoperti ricorsivamente, quindi potete organizzare le regole in sottodirectory come `frontend/` o `backend/`:

```text  theme={null}
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

Le regole possono essere limitate a file specifici utilizzando il frontmatter YAML con il campo `paths`. Queste regole condizionali si applicano solo quando Claude lavora con file che corrispondono ai modelli specificati.

```markdown  theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Regole di sviluppo API

- Tutti gli endpoint API devono includere la convalida dell'input
- Usate il formato di risposta di errore standard
- Includete commenti di documentazione OpenAPI
```

Le regole senza un campo `paths` vengono caricate incondizionatamente e si applicano a tutti i file. Le regole con ambito di percorso si attivano quando Claude legge file che corrispondono al modello, non ad ogni utilizzo dello strumento.

Usate i modelli glob nel campo `paths` per abbinare i file per estensione, directory o qualsiasi combinazione:

| Modello                | Corrisponde a                                  |
| ---------------------- | ---------------------------------------------- |
| `**/*.ts`              | Tutti i file TypeScript in qualsiasi directory |
| `src/**/*`             | Tutti i file sotto la directory `src/`         |
| `*.md`                 | File Markdown nella radice del progetto        |
| `src/components/*.tsx` | Componenti React in una directory specifica    |

Potete specificare più modelli e usare l'espansione tra parentesi graffe per abbinare più estensioni in un modello:

```markdown  theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Condividere le regole tra i progetti con symlink

La directory `.claude/rules/` supporta i symlink, quindi potete mantenere un set di regole condivise e collegarle a più progetti. I symlink vengono risolti e caricati normalmente, e i symlink circolari vengono rilevati e gestiti correttamente.

Questo esempio collega sia una directory condivisa che un file individuale:

```bash  theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### Regole a livello di utente

Le regole personali in `~/.claude/rules/` si applicano a ogni progetto sulla vostra macchina. Usatele per le preferenze che non sono specifiche del progetto:

```text  theme={null}
~/.claude/rules/
├── preferences.md    # Le vostre preferenze di codifica personali
└── workflows.md      # I vostri flussi di lavoro preferiti
```

Le regole a livello di utente vengono caricate prima delle regole di progetto, dando alle regole di progetto una priorità più alta.

### Gestire CLAUDE.md per team di grandi dimensioni

Per le organizzazioni che distribuiscono Claude Code tra i team, potete centralizzare le istruzioni e controllare quali file CLAUDE.md vengono caricati.

#### Distribuire CLAUDE.md a livello organizzativo

Le organizzazioni possono distribuire un CLAUDE.md gestito centralmente che si applica a tutti gli utenti su una macchina. Questo file non può essere escluso dalle impostazioni individuali.

<Steps>
  <Step title="Creare il file nel percorso della politica gestita">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux e WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Distribuire con il vostro sistema di gestione della configurazione">
    Usate MDM, Group Policy, Ansible o strumenti simili per distribuire il file tra le macchine degli sviluppatori. Consultate [impostazioni gestite](/it/permissions#managed-settings) per altre opzioni di configurazione a livello organizzativo.
  </Step>
</Steps>

#### Escludere file CLAUDE.md specifici

Nei grandi monorepo, i file CLAUDE.md antenati possono contenere istruzioni che non sono rilevanti per il vostro lavoro. L'impostazione `claudeMdExcludes` vi permette di saltare file specifici per percorso o modello glob.

Questo esempio esclude un CLAUDE.md di primo livello e una directory di regole da una cartella padre. Aggiungetelo a `.claude/settings.local.json` in modo che l'esclusione rimanga locale alla vostra macchina:

```json  theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

I modelli vengono abbinati ai percorsi di file assoluti utilizzando la sintassi glob. Potete configurare `claudeMdExcludes` in qualsiasi [livello di impostazioni](/it/settings#settings-files): utente, progetto, locale o politica gestita. Gli array si uniscono tra i livelli.

I file CLAUDE.md della politica gestita non possono essere esclusi. Ciò garantisce che le istruzioni a livello organizzativo si applichino sempre indipendentemente dalle impostazioni individuali.

## Memoria automatica

La memoria automatica permette a Claude di accumulare conoscenze tra le sessioni senza che scriviate nulla. Claude salva note per se stesso mentre lavora: comandi di compilazione, approfondimenti sul debug, note sull'architettura, preferenze di stile del codice e abitudini di flusso di lavoro. Claude non salva qualcosa ad ogni sessione. Decide cosa vale la pena ricordare in base al fatto che l'informazione sarebbe utile in una conversazione futura.

<Note>
  La memoria automatica richiede Claude Code v2.1.59 o successivo. Controllate la vostra versione con `claude --version`.
</Note>

### Abilitare o disabilitare la memoria automatica

La memoria automatica è attivata per impostazione predefinita. Per attivarla/disattivarla, aprite `/memory` in una sessione e usate l'interruttore di memoria automatica, oppure impostate `autoMemoryEnabled` nelle impostazioni del vostro progetto:

```json  theme={null}
{
  "autoMemoryEnabled": false
}
```

Per disabilitare la memoria automatica tramite variabile di ambiente, impostate `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Percorso di archiviazione

Ogni progetto ottiene la sua propria directory di memoria in `~/.claude/projects/<project>/memory/`. Il percorso `<project>` è derivato dal repository git, quindi tutti i worktree e le sottodirectory all'interno dello stesso repo condividono una directory di memoria automatica. Al di fuori di un repository git, viene utilizzata la radice del progetto.

Per archiviare la memoria automatica in una posizione diversa, impostate `autoMemoryDirectory` nelle vostre impostazioni utente o locali:

```json  theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

Questa impostazione è accettata dalle impostazioni di politica, locali e utente. Non è accettata dalle impostazioni di progetto (`.claude/settings.json`) per evitare che un progetto condiviso reindirizza le scritture di memoria automatica a posizioni sensibili.

La directory contiene un punto di ingresso `MEMORY.md` e file di argomento opzionali:

```text  theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Indice conciso, caricato in ogni sessione
├── debugging.md       # Note dettagliate sui modelli di debug
├── api-conventions.md # Decisioni di progettazione API
└── ...                # Qualsiasi altro file di argomento che Claude crea
```

`MEMORY.md` funge da indice della directory di memoria. Claude legge e scrive file in questa directory durante la vostra sessione, utilizzando `MEMORY.md` per tenere traccia di ciò che è archiviato dove.

La memoria automatica è locale alla macchina. Tutti i worktree e le sottodirectory all'interno dello stesso repository git condividono una directory di memoria automatica. I file non vengono condivisi tra macchine o ambienti cloud.

### Come funziona

Le prime 200 righe di `MEMORY.md` vengono caricate all'inizio di ogni conversazione. Il contenuto oltre la riga 200 non viene caricato all'inizio della sessione. Claude mantiene `MEMORY.md` conciso spostando le note dettagliate in file di argomento separati.

Questo limite di 200 righe si applica solo a `MEMORY.md`. I file CLAUDE.md vengono caricati completamente indipendentemente dalla lunghezza, anche se i file più brevi producono una migliore aderenza.

I file di argomento come `debugging.md` o `patterns.md` non vengono caricati all'avvio. Claude li legge su richiesta utilizzando i suoi strumenti di file standard quando ha bisogno delle informazioni.

Claude legge e scrive file di memoria durante la vostra sessione. Quando vedete "Writing memory" o "Recalled memory" nell'interfaccia di Claude Code, Claude sta attivamente aggiornando o leggendo da `~/.claude/projects/<project>/memory/`.

### Controllare e modificare la vostra memoria

I file di memoria automatica sono markdown semplice che potete modificare o eliminare in qualsiasi momento. Eseguite [`/memory`](#view-and-edit-with-memory) per sfogliare e aprire i file di memoria da una sessione.

## Visualizzare e modificare con `/memory`

Il comando `/memory` elenca tutti i file CLAUDE.md e rules caricati nella vostra sessione corrente, vi permette di attivare o disattivare la memoria automatica e fornisce un collegamento per aprire la cartella di memoria automatica. Selezionate qualsiasi file per aprirlo nel vostro editor.

Quando chiedete a Claude di ricordare qualcosa, come "usa sempre pnpm, non npm" o "ricorda che i test API richiedono un'istanza Redis locale", Claude lo salva nella memoria automatica. Per aggiungere istruzioni a CLAUDE.md, chiedete direttamente a Claude, come "aggiungi questo a CLAUDE.md", oppure modificate il file voi stessi tramite `/memory`.

## Risolvere i problemi di memoria

Questi sono i problemi più comuni con CLAUDE.md e la memoria automatica, insieme ai passaggi per risolverli.

### Claude non sta seguendo il mio CLAUDE.md

CLAUDE.md è contesto, non applicazione. Claude lo legge e cerca di seguirlo, ma non c'è garanzia di conformità rigorosa, specialmente per istruzioni vaghe o conflittuali.

Per risolvere i problemi:

* Eseguite `/memory` per verificare che i vostri file CLAUDE.md vengono caricati. Se un file non è elencato, Claude non può vederlo.
* Controllate che il CLAUDE.md rilevante si trovi in una posizione che viene caricata per la vostra sessione (consultate [Scegliere dove mettere i file CLAUDE.md](#choose-where-to-put-claudemd-files)).
* Rendete le istruzioni più specifiche. "Usate l'indentazione a 2 spazi" funziona meglio di "formattate il codice bene".
* Cercate istruzioni conflittuali tra i file CLAUDE.md. Se due file danno una guida diversa per lo stesso comportamento, Claude potrebbe sceglierne una arbitrariamente.

<Tip>
  Usate l'hook [`InstructionsLoaded`](/it/hooks#instructionsloaded) per registrare esattamente quali file di istruzioni vengono caricati, quando vengono caricati e perché. Questo è utile per il debug delle regole specifiche del percorso o dei file caricati pigriamente nelle sottodirectory.
</Tip>

### Non so cosa ha salvato la memoria automatica

Eseguite `/memory` e selezionate la cartella di memoria automatica per sfogliare ciò che Claude ha salvato. Tutto è markdown semplice che potete leggere, modificare o eliminare.

### Il mio CLAUDE.md è troppo grande

I file con più di 200 righe consumano più contesto e possono ridurre l'aderenza. Spostate il contenuto dettagliato in file separati a cui si fa riferimento con importazioni `@path` (consultate [Importare file aggiuntivi](#import-additional-files)), oppure dividete le vostre istruzioni tra file `.claude/rules/`.

### Le istruzioni sembrano perse dopo `/compact`

CLAUDE.md sopravvive completamente alla compattazione. Dopo `/compact`, Claude rilegge il vostro CLAUDE.md dal disco e lo reinietta fresco nella sessione. Se un'istruzione è scomparsa dopo la compattazione, è stata data solo nella conversazione, non scritta in CLAUDE.md. Aggiungetela a CLAUDE.md per farla persistere tra le sessioni.

Consultate [Scrivere istruzioni efficaci](#write-effective-instructions) per una guida su dimensione, struttura e specificità.

## Risorse correlate

* [Skills](/it/skills): pacchetto di flussi di lavoro ripetibili che vengono caricati su richiesta
* [Impostazioni](/it/settings): configurare il comportamento di Claude Code con file di impostazioni
* [Gestire le sessioni](/it/sessions): gestire il contesto, riprendere le conversazioni ed eseguire sessioni parallele
* [Memoria dei subagent](/it/sub-agents#enable-persistent-memory): permettere ai subagent di mantenere la loro propria memoria automatica
