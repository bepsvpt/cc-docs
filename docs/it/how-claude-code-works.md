> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Come funziona Claude Code

> Comprendi il ciclo agentico, gli strumenti integrati e come Claude Code interagisce con il tuo progetto.

Claude Code è un assistente agentico che funziona nel tuo terminale. Sebbene eccella nella programmazione, può aiutarti con qualsiasi cosa tu possa fare dalla riga di comando: scrivere documentazione, eseguire build, cercare file, ricercare argomenti e molto altro.

Questa guida copre l'architettura principale, le capacità integrate e [suggerimenti per lavorare efficacemente](#work-effectively-with-claude-code). Per procedure dettagliate, consulta [Flussi di lavoro comuni](/it/common-workflows). Per funzionalità di estensibilità come skills, MCP e hooks, consulta [Estendi Claude Code](/it/features-overview).

## Il ciclo agentico

Quando dai a Claude un compito, lavora attraverso tre fasi: **raccogliere contesto**, **intraprendere azioni** e **verificare i risultati**. Queste fasi si mescolano insieme. Claude utilizza strumenti durante tutto il processo, sia cercando file per comprendere il tuo codice, modificando per apportare cambiamenti, o eseguendo test per verificare il suo lavoro.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38" alt="Il ciclo agentico: il tuo prompt porta Claude a raccogliere contesto, intraprendere azioni, verificare i risultati e ripetere fino al completamento dell'attività. Puoi interrompere in qualsiasi momento." width="720" height="280" data-path="images/agentic-loop.svg" />

Il ciclo si adatta a quello che chiedi. Una domanda sulla tua base di codice potrebbe richiedere solo la raccolta di contesto. Una correzione di bug cicla attraverso tutte e tre le fasi ripetutamente. Un refactoring potrebbe comportare una verifica estesa. Claude decide cosa richiede ogni passaggio in base a quello che ha imparato dal passaggio precedente, concatenando dozzine di azioni insieme e correggendo il corso lungo il percorso.

Anche tu fai parte di questo ciclo. Puoi interrompere in qualsiasi momento per indirizzare Claude in una direzione diversa, fornire contesto aggiuntivo o chiedergli di provare un approccio diverso. Claude lavora autonomamente ma rimane reattivo al tuo input.

Il ciclo agentico è alimentato da due componenti: [modelli](#models) che ragionano e [strumenti](#tools) che agiscono. Claude Code funge da **harness agentico** intorno a Claude: fornisce gli strumenti, la gestione del contesto e l'ambiente di esecuzione che trasformano un modello di linguaggio in un agente di codifica capace.

### Modelli

Claude Code utilizza i modelli Claude per comprendere il tuo codice e ragionare sui compiti. Claude può leggere codice in qualsiasi linguaggio, comprendere come i componenti si collegano e capire cosa deve cambiare per raggiungere il tuo obiettivo. Per compiti complessi, suddivide il lavoro in passaggi, li esegue e si adatta in base a quello che impara.

[Sono disponibili più modelli](/it/model-config) con diversi compromessi. Sonnet gestisce bene la maggior parte dei compiti di codifica. Opus fornisce un ragionamento più forte per decisioni architettoniche complesse. Cambia con `/model` durante una sessione o inizia con `claude --model <name>`.

Quando questa guida dice "Claude sceglie" o "Claude decide", è il modello che sta facendo il ragionamento.

### Strumenti

Gli strumenti sono ciò che rende Claude Code agentico. Senza strumenti, Claude può solo rispondere con testo. Con gli strumenti, Claude può agire: leggere il tuo codice, modificare file, eseguire comandi, cercare il web e interagire con servizi esterni. Ogni utilizzo di uno strumento restituisce informazioni che si alimentano nel ciclo, informando la decisione successiva di Claude.

Gli strumenti integrati generalmente rientrano in cinque categorie, ognuna rappresentante un diverso tipo di agenzia.

| Categoria                   | Cosa Claude può fare                                                                                                                                                                   |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Operazioni su file**      | Leggere file, modificare codice, creare nuovi file, rinominare e riorganizzare                                                                                                         |
| **Ricerca**                 | Trovare file per pattern, cercare contenuto con regex, esplorare basi di codice                                                                                                        |
| **Esecuzione**              | Eseguire comandi shell, avviare server, eseguire test, usare git                                                                                                                       |
| **Web**                     | Cercare il web, recuperare documentazione, cercare messaggi di errore                                                                                                                  |
| **Intelligenza del codice** | Vedere errori di tipo e avvisi dopo le modifiche, saltare alle definizioni, trovare riferimenti (richiede [plugin di intelligenza del codice](/it/discover-plugins#code-intelligence)) |

Queste sono le capacità principali. Claude ha anche strumenti per generare subagents, farti domande e altri compiti di orchestrazione. Consulta [Strumenti disponibili per Claude](/it/tools-reference) per l'elenco completo.

Claude sceglie quali strumenti utilizzare in base al tuo prompt e a quello che impara lungo il percorso. Quando dici "correggi i test falliti", Claude potrebbe:

1. Eseguire la suite di test per vedere cosa sta fallendo
2. Leggere l'output dell'errore
3. Cercare i file sorgente rilevanti
4. Leggere quei file per comprendere il codice
5. Modificare i file per correggere il problema
6. Eseguire di nuovo i test per verificare

Ogni utilizzo di uno strumento fornisce a Claude nuove informazioni che informano il passaggio successivo. Questo è il ciclo agentico in azione.

**Estensione delle capacità di base:** Gli strumenti integrati sono la fondazione. Puoi estendere quello che Claude sa con [skills](/it/skills), connetterti a servizi esterni con [MCP](/it/mcp), automatizzare flussi di lavoro con [hooks](/it/hooks) e delegare compiti a [subagents](/it/sub-agents). Queste estensioni formano un livello sopra il ciclo agentico principale. Consulta [Estendi Claude Code](/it/features-overview) per una guida sulla scelta dell'estensione giusta per le tue esigenze.

## A cosa Claude può accedere

Questa guida si concentra sul terminale. Claude Code funziona anche in [VS Code](/it/vs-code), [IDE JetBrains](/it/jetbrains) e altri ambienti.

Quando esegui `claude` in una directory, Claude Code ottiene accesso a:

* **Il tuo progetto.** File nella tua directory e sottodirectory, più file altrove con la tua autorizzazione.
* **Il tuo terminale.** Qualsiasi comando che potresti eseguire: strumenti di build, git, gestori di pacchetti, utilità di sistema, script. Se puoi farlo dalla riga di comando, Claude può farlo anche lui.
* **Il tuo stato git.** Ramo corrente, modifiche non committate e cronologia dei commit recenti.
* **Il tuo [CLAUDE.md](/it/memory).** Un file markdown dove memorizzi istruzioni specifiche del progetto, convenzioni e contesto che Claude dovrebbe conoscere ogni sessione.
* **[Auto memory](/it/memory#auto-memory).** Apprendimenti che Claude salva automaticamente mentre lavori, come pattern di progetto e le tue preferenze. Le prime 200 righe o 25KB di MEMORY.md, a seconda di quale viene raggiunto per primo, si caricano all'inizio di ogni sessione.
* **Estensioni che configuri.** [Server MCP](/it/mcp) per servizi esterni, [skills](/it/skills) per flussi di lavoro, [subagents](/it/sub-agents) per lavoro delegato e [Claude in Chrome](/it/chrome) per l'interazione del browser.

Poiché Claude vede l'intero tuo progetto, può lavorare su di esso. Quando chiedi a Claude di "correggere il bug di autenticazione", cerca file rilevanti, legge più file per comprendere il contesto, apporta modifiche coordinate su di essi, esegue test per verificare la correzione e committa le modifiche se lo chiedi. Questo è diverso dagli assistenti di codice inline che vedono solo il file corrente.

## Ambienti e interfacce

Il ciclo agentico, gli strumenti e le capacità descritti sopra sono gli stessi ovunque tu usi Claude Code. Quello che cambia è dove il codice viene eseguito e come interagisci con esso.

### Ambienti di esecuzione

Claude Code funziona in tre ambienti, ognuno con diversi compromessi per dove il tuo codice viene eseguito.

| Ambiente           | Dove viene eseguito il codice              | Caso d'uso                                                       |
| ------------------ | ------------------------------------------ | ---------------------------------------------------------------- |
| **Locale**         | La tua macchina                            | Predefinito. Accesso completo ai tuoi file, strumenti e ambiente |
| **Cloud**          | VM gestite da Anthropic                    | Delegare compiti, lavorare su repo che non hai localmente        |
| **Remote Control** | La tua macchina, controllata da un browser | Usa l'interfaccia web mantenendo tutto locale                    |

### Interfacce

Puoi accedere a Claude Code tramite il terminale, l'[app desktop](/it/desktop), [estensioni IDE](/it/vs-code), [claude.ai/code](https://claude.ai/code), [Remote Control](/it/remote-control), [Slack](/it/slack) e [pipeline CI/CD](/it/github-actions). L'interfaccia determina come vedi e interagisci con Claude, ma il ciclo agentico sottostante è identico. Consulta [Usa Claude Code ovunque](/it/overview#use-claude-code-everywhere) per l'elenco completo.

## Lavora con le sessioni

Claude Code salva la tua conversazione localmente mentre lavori. Ogni messaggio, utilizzo di strumento e risultato viene archiviato, il che consente [il rewind](#undo-changes-with-checkpoints), [la ripresa e il fork](#resume-or-fork-sessions) delle sessioni. Prima che Claude apporta modifiche al codice, crea anche uno snapshot dei file interessati in modo da poter ripristinare se necessario.

**Le sessioni sono indipendenti.** Ogni nuova sessione inizia con una finestra di contesto fresca, senza la cronologia della conversazione dalle sessioni precedenti. Claude può persistere gli apprendimenti tra le sessioni utilizzando [auto memory](/it/memory#auto-memory) e puoi aggiungere le tue istruzioni persistenti in [CLAUDE.md](/it/memory).

### Lavora tra i rami

Ogni conversazione di Claude Code è una sessione legata alla tua directory corrente. Quando riprendi, vedi solo le sessioni da quella directory.

Claude vede i file del tuo ramo corrente. Quando cambi ramo, Claude vede i file del nuovo ramo, ma la cronologia della tua conversazione rimane la stessa. Claude ricorda quello che hai discusso anche dopo il cambio di ramo.

Poiché le sessioni sono legate alle directory, puoi eseguire sessioni Claude parallele utilizzando [git worktrees](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), che creano directory separate per singoli rami.

### Riprendi o fai il fork delle sessioni

Quando riprendi una sessione con `claude --continue` o `claude --resume`, riprendi da dove hai lasciato utilizzando lo stesso ID di sessione. I nuovi messaggi si aggiungono alla conversazione esistente. La tua cronologia completa della conversazione viene ripristinata, ma i permessi con ambito di sessione non lo sono. Dovrai approvarli di nuovo.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30" alt="Continuità della sessione: resume continua la stessa sessione, fork crea un nuovo ramo con un nuovo ID." width="560" height="280" data-path="images/session-continuity.svg" />

Per creare un ramo e provare un approccio diverso senza influenzare la sessione originale, utilizza il flag `--fork-session`:

```bash theme={null}
claude --continue --fork-session
```

Questo crea un nuovo ID di sessione preservando la cronologia della conversazione fino a quel punto. La sessione originale rimane invariata. Come resume, le sessioni forkate non ereditano i permessi con ambito di sessione.

**Stessa sessione in più terminali**: Se riprendi la stessa sessione in più terminali, entrambi i terminali scrivono nello stesso file di sessione. I messaggi da entrambi vengono intercalati, come due persone che scrivono nello stesso quaderno. Nulla si corrompe, ma la conversazione diventa confusa. Ogni terminale vede solo i suoi messaggi durante la sessione, ma se riprendi quella sessione in seguito, vedrai tutto intercalato. Per il lavoro parallelo dallo stesso punto di partenza, utilizza `--fork-session` per dare a ogni terminale la sua sessione pulita.

### La finestra di contesto

La finestra di contesto di Claude contiene la cronologia della tua conversazione, i contenuti dei file, gli output dei comandi, [CLAUDE.md](/it/memory), [auto memory](/it/memory#auto-memory), le skills caricate e le istruzioni di sistema. Man mano che lavori, il contesto si riempie. Claude compatta automaticamente, ma le istruzioni dall'inizio della conversazione possono andare perse. Metti le regole persistenti in CLAUDE.md ed esegui `/context` per vedere cosa sta usando lo spazio.

Per una procedura interattiva di quello che si carica e quando, consulta [Esplora la finestra di contesto](/it/context-window).

#### Quando il contesto si riempie

Claude Code gestisce il contesto automaticamente mentre ti avvicini al limite. Cancella prima gli output degli strumenti più vecchi, quindi riassume la conversazione se necessario. Le tue richieste e i frammenti di codice chiave vengono preservati; le istruzioni dettagliate dall'inizio della conversazione possono andare perse. Metti le regole persistenti in CLAUDE.md piuttosto che fare affidamento sulla cronologia della conversazione.

Per controllare cosa viene preservato durante la compattazione, aggiungi una sezione "Compact Instructions" a CLAUDE.md o esegui `/compact` con un focus (come `/compact focus on the API changes`).

Esegui `/context` per vedere cosa sta usando lo spazio. Le definizioni degli strumenti MCP vengono differite per impostazione predefinita e caricate su richiesta tramite [ricerca degli strumenti](/it/mcp#scale-with-mcp-tool-search), quindi solo i nomi degli strumenti consumano contesto fino a quando Claude utilizza uno strumento specifico. Esegui `/mcp` per controllare i costi per server.

#### Gestisci il contesto con skills e subagents

Oltre alla compattazione, puoi utilizzare altre funzionalità per controllare cosa viene caricato nel contesto.

[Skills](/it/skills) si caricano su richiesta. Claude vede le descrizioni delle skills all'inizio della sessione, ma il contenuto completo si carica solo quando una skill viene utilizzata. Per le skills che invochi manualmente, imposta `disable-model-invocation: true` per mantenere le descrizioni fuori dal contesto fino a quando non ne hai bisogno.

[Subagents](/it/sub-agents) ottengono il loro contesto fresco, completamente separato dalla tua conversazione principale. Il loro lavoro non gonfia il tuo contesto. Quando finito, restituiscono un riassunto. Questo isolamento è il motivo per cui i subagents aiutano con le sessioni lunghe.

Consulta [costi del contesto](/it/features-overview#understand-context-costs) per quello che ogni funzionalità costa e [riduci l'utilizzo dei token](/it/costs#reduce-token-usage) per suggerimenti sulla gestione del contesto.

## Rimani al sicuro con checkpoint e permessi

Claude ha due meccanismi di sicurezza: i checkpoint ti permettono di annullare le modifiche ai file e i permessi controllano cosa Claude può fare senza chiedere.

### Annulla le modifiche con i checkpoint

**Ogni modifica ai file è reversibile.** Prima che Claude modifichi qualsiasi file, crea uno snapshot dei contenuti attuali. Se qualcosa va storto, premi `Esc` due volte per tornare a uno stato precedente, o chiedi a Claude di annullare.

I checkpoint sono locali alla tua sessione, separati da git. Coprono solo le modifiche ai file. Le azioni che influenzano i sistemi remoti (database, API, distribuzioni) non possono essere checkpointed, motivo per cui Claude chiede prima di eseguire comandi con effetti collaterali esterni.

### Controlla cosa Claude può fare

Premi `Shift+Tab` per scorrere le modalità di permesso:

* **Predefinito**: Claude chiede prima delle modifiche ai file e dei comandi shell
* **Auto-accept edits**: Claude modifica i file senza chiedere, chiede ancora per i comandi
* **Plan Mode**: Claude utilizza solo strumenti di sola lettura, creando un piano che puoi approvare prima dell'esecuzione
* **Auto mode**: Claude valuta tutte le azioni con controlli di sicurezza in background. Attualmente un'anteprima di ricerca

Puoi anche consentire comandi specifici in `.claude/settings.json` in modo che Claude non chieda ogni volta. Questo è utile per comandi affidabili come `npm test` o `git status`. Le impostazioni possono essere scoped da politiche a livello di organizzazione fino alle preferenze personali. Consulta [Permessi](/it/permissions) per i dettagli.

***

## Lavora efficacemente con Claude Code

Questi suggerimenti ti aiutano a ottenere risultati migliori da Claude Code.

### Chiedi aiuto a Claude Code

Claude Code può insegnarti come usarlo. Fai domande come "come configuro gli hooks?" o "qual è il modo migliore per strutturare il mio CLAUDE.md?" e Claude spiegherà.

I comandi integrati ti guidano anche attraverso la configurazione:

* `/init` ti guida attraverso la creazione di un CLAUDE.md per il tuo progetto
* `/agents` ti aiuta a configurare subagents personalizzati
* `/doctor` diagnostica i problemi comuni con la tua installazione

### È una conversazione

Claude Code è conversazionale. Non hai bisogno di prompt perfetti. Inizia con quello che vuoi, quindi affina:

```text theme={null}
Correggi il bug di login
```

\[Claude indaga, prova qualcosa]

```text theme={null}
Non è del tutto giusto. Il problema è nella gestione della sessione.
```

\[Claude adatta l'approccio]

Quando il primo tentativo non è giusto, non ricominciare da capo. Itera.

#### Interrompi e indirizza

Puoi interrompere Claude in qualsiasi momento. Se sta andando nella direzione sbagliata, digita semplicemente la tua correzione e premi Invio. Claude smetterà quello che sta facendo e adatterà il suo approccio in base al tuo input. Non devi aspettare che finisca o ricominciare da capo.

### Sii specifico all'inizio

Più preciso è il tuo prompt iniziale, meno correzioni avrai bisogno. Fai riferimento a file specifici, menziona vincoli e indica pattern di esempio.

```text theme={null}
Il flusso di checkout è rotto per gli utenti con carte scadute.
Controlla src/payments/ per il problema, specialmente l'aggiornamento del token.
Scrivi prima un test fallito, poi correggilo.
```

I prompt vaghi funzionano, ma passerai più tempo a indirizzare. I prompt specifici come quello sopra spesso hanno successo al primo tentativo.

### Dai a Claude qualcosa da verificare

Claude funziona meglio quando può verificare il suo lavoro. Includi casi di test, incolla screenshot dell'interfaccia utente prevista o definisci l'output che desideri.

```text theme={null}
Implementa validateEmail. Casi di test: 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Esegui i test dopo.
```

Per il lavoro visivo, incolla uno screenshot del design e chiedi a Claude di confrontare la sua implementazione con esso.

### Esplora prima di implementare

Per problemi complessi, separa la ricerca dalla codifica. Utilizza la modalità piano (`Shift+Tab` due volte) per analizzare prima la base di codice:

```text theme={null}
Leggi src/auth/ e comprendi come gestiamo le sessioni.
Quindi crea un piano per aggiungere il supporto OAuth.
```

Rivedi il piano, affinalo attraverso la conversazione, quindi lascia che Claude implementi. Questo approccio a due fasi produce risultati migliori rispetto al passare direttamente al codice.

### Delega, non dettare

Pensa di delegare a un collega capace. Fornisci contesto e direzione, quindi affida a Claude di capire i dettagli:

```text theme={null}
Il flusso di checkout è rotto per gli utenti con carte scadute.
Il codice rilevante è in src/payments/. Puoi indagare e correggerlo?
```

Non hai bisogno di specificare quali file leggere o quali comandi eseguire. Claude lo capisce.

## Cosa c'è dopo

<CardGroup cols={2}>
  <Card title="Estendi con funzionalità" icon="puzzle-piece" href="/it/features-overview">
    Aggiungi Skills, connessioni MCP e comandi personalizzati
  </Card>

  <Card title="Flussi di lavoro comuni" icon="graduation-cap" href="/it/common-workflows">
    Guide passo dopo passo per compiti tipici
  </Card>
</CardGroup>
