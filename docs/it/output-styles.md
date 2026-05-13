> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Output styles

> Adattare Claude Code per usi oltre l'ingegneria del software

Output styles cambiano il modo in cui Claude risponde, non quello che Claude sa. Modificano il prompt di sistema per impostare il ruolo, il tono e il formato di output mantenendo le capacità principali come l'esecuzione di script, la lettura e la scrittura di file e il tracciamento dei TODO. Utilizzatene uno quando continuate a ripetere la stessa voce o formato ad ogni turno, oppure quando desiderate che Claude agisca come qualcosa di diverso da un ingegnere del software.

Per le istruzioni relative al vostro progetto, alle convenzioni o al codebase, utilizzate [CLAUDE.md](/it/memory) invece.

## Output styles integrati

Lo **Default** output style di Claude Code è il prompt di sistema esistente, progettato per aiutarvi a completare i compiti di ingegneria del software in modo efficiente.

Ci sono tre output styles integrati aggiuntivi:

* **Proactive**: Claude esegue immediatamente, fa ipotesi ragionevoli invece di fermarsi per decisioni di routine, e preferisce l'azione alla pianificazione. Questo applica la stessa guida della [modalità auto](/it/permission-modes#eliminate-prompts-with-auto-mode) senza cambiare la vostra modalità di permesso, quindi vedete comunque i prompt di permesso prima che gli strumenti vengano eseguiti.

* **Explanatory**: Fornisce "Insights" educativi tra l'aiuto nel completamento dei compiti di ingegneria del software. Aiuta a comprendere le scelte di implementazione e i pattern del codebase.

* **Learning**: Modalità collaborativa di apprendimento pratico in cui Claude non solo condividerà "Insights" durante la codifica, ma vi chiederà anche di contribuire con piccoli, strategici pezzi di codice voi stessi. Claude Code aggiungerà marcatori `TODO(human)` nel vostro codice per voi da implementare.

## Come funzionano gli output styles

Gli output styles modificano direttamente il prompt di sistema di Claude Code.

* Gli output styles personalizzati escludono istruzioni per la codifica (come la verifica del codice con i test), a meno che `keep-coding-instructions` non sia true.
* Tutti gli output styles hanno le loro istruzioni personalizzate aggiunte alla fine del prompt di sistema.
* Tutti gli output styles attivano promemoria affinché Claude aderisca alle istruzioni dell'output style durante la conversazione.

L'utilizzo dei token dipende dallo stile. L'aggiunta di istruzioni al prompt di sistema aumenta i token di input, anche se il prompt caching riduce questo costo dopo la prima richiesta in una sessione. Gli output styles integrati Explanatory e Learning producono risposte più lunghe rispetto a Default per progettazione, il che aumenta i token di output. Per gli stili personalizzati, l'utilizzo dei token di output dipende da ciò che le vostre istruzioni dicono a Claude di produrre.

## Cambiare il vostro output style

Eseguite `/config` e selezionate **Output style** per scegliere uno stile da un menu. La vostra selezione viene salvata in `.claude/settings.local.json` al [livello del progetto locale](/it/settings).

Per impostare uno stile senza il menu, modificate direttamente il campo `outputStyle` in un file di impostazioni:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Poiché l'output style è impostato nel prompt di sistema all'avvio della sessione, le modifiche hanno effetto la prossima volta che avviate una nuova sessione. Questo mantiene il prompt di sistema stabile durante una conversazione in modo che il prompt caching possa ridurre la latenza e il costo.

## Creare un output style personalizzato

Gli output styles personalizzati sono file Markdown con frontmatter e il testo che verrà aggiunto al prompt di sistema:

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

Potete salvare questi file a tre livelli:

* Utente: `~/.claude/output-styles`
* Progetto: `.claude/output-styles`
* Politica gestita: `.claude/output-styles` all'interno della [directory delle impostazioni gestite](/it/settings#settings-files)

I [Plugins](/it/plugins-reference) possono anche fornire output styles in una directory `output-styles/`.

### Frontmatter

I file di output style supportano frontmatter per specificare i metadati:

| Frontmatter                | Scopo                                                                                                                                                                                                                                                                            | Predefinito               |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------ |
| `name`                     | Nome dell'output style, se non il nome del file                                                                                                                                                                                                                                  | Eredita dal nome del file |
| `description`              | Descrizione dell'output style, mostrata nel picker `/config`                                                                                                                                                                                                                     | Nessuno                   |
| `keep-coding-instructions` | Se mantenere le parti del prompt di sistema di Claude Code relative alla codifica.                                                                                                                                                                                               | false                     |
| `force-for-plugin`         | Solo output styles dei plugin: applica questo stile automaticamente ogni volta che il plugin è abilitato, senza richiedere agli utenti di selezionarlo. Sostituisce l'impostazione `outputStyle` dell'utente. Se più plugin abilitati impostano questo, il primo caricato vince. | false                     |

## Confronti con funzionalità correlate

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Scegliete in base al fatto che Claude debba smettere di agire come assistente di codifica o mantenere il suo ruolo predefinito e imparare di più. Gli output styles sostituiscono le parti di ingegneria del software del prompt di sistema di Claude Code con il vostro ruolo e voce personali, quindi utilizzateli quando Claude dovrebbe adottare un'identità diversa, come un editor di testi o un assistente di analisi dei dati. CLAUDE.md e `--append-system-prompt` mantengono entrambi l'identità predefinita di Claude Code e vi aggiungono contenuti, quindi utilizzateli quando Claude dovrebbe rimanere un assistente di codifica che segue anche le convenzioni del vostro progetto o istruzioni aggiuntive.

I meccanismi differiscono inoltre. Gli output styles modificano il prompt di sistema direttamente. CLAUDE.md aggiunge i suoi contenuti come messaggio utente dopo il prompt di sistema. `--append-system-prompt` aggiunge contenuti alla fine del prompt di sistema senza rimuovere nulla.

### Output Styles vs. [Agents](/it/sub-agents)

Utilizzate uno output style per cambiare il modo in cui la conversazione principale risponde in ogni sessione. Utilizzate un [subagent](/it/sub-agents) quando desiderate un helper con ambito separato a cui la conversazione principale delega. Gli output styles influenzano solo il prompt di sistema del loop dell'agente principale. Gli agenti gestiscono compiti specifici e possono avere il loro modello, strumenti e contesto su quando invocarli.

### Output Styles vs. [Skills](/it/skills)

Gli output styles modificano il modo in cui Claude risponde (formattazione, tono, struttura) e sono sempre attivi una volta selezionati. Skills sono prompt specifici per compiti che invocate con `/skill-name` o che Claude carica automaticamente quando rilevante. Utilizzate gli output styles per preferenze di formattazione coerenti; utilizzate skills per flussi di lavoro e compiti riutilizzabili.
