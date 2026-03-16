> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Output styles

> Adattare Claude Code per usi oltre l'ingegneria del software

Output styles consente di utilizzare Claude Code come qualsiasi tipo di agente mantenendo
le sue capacità principali, come l'esecuzione di script locali, la lettura/scrittura di file e
il tracciamento dei TODO.

## Output styles integrati

Lo **Default** output style di Claude Code è il prompt di sistema esistente, progettato
per aiutarvi a completare i compiti di ingegneria del software in modo efficiente.

Ci sono due output styles integrati aggiuntivi focalizzati sull'insegnamento del
codebase e su come Claude opera:

* **Explanatory**: Fornisce "Insights" educativi tra l'aiuto nel completamento dei compiti
  di ingegneria del software. Aiuta a comprendere le scelte di implementazione
  e i pattern del codebase.

* **Learning**: Modalità collaborativa di apprendimento pratico in cui Claude non solo
  condividerà "Insights" durante la codifica, ma vi chiederà anche di contribuire con piccoli,
  strategici pezzi di codice voi stessi. Claude Code aggiungerà marcatori `TODO(human)` nel vostro
  codice per voi da implementare.

## Come funzionano gli output styles

Gli output styles modificano direttamente il prompt di sistema di Claude Code.

* Tutti gli output styles escludono istruzioni per un output efficiente (come
  rispondere in modo conciso).
* Gli output styles personalizzati escludono istruzioni per la codifica (come la verifica del codice
  con i test), a meno che `keep-coding-instructions` non sia true.
* Tutti gli output styles hanno le loro istruzioni personalizzate aggiunte alla fine del
  prompt di sistema.
* Tutti gli output styles attivano promemoria affinché Claude aderisca alle istruzioni
  dell'output style durante la conversazione.

## Cambiare il vostro output style

Eseguite `/config` e selezionate **Output style** per scegliere uno stile da un menu. La vostra
selezione viene salvata in `.claude/settings.local.json` al
[livello del progetto locale](/it/settings).

Per impostare uno stile senza il menu, modificate direttamente il campo `outputStyle` in un
file di impostazioni:

```json  theme={null}
{
  "outputStyle": "Explanatory"
}
```

Poiché l'output style è impostato nel prompt di sistema all'avvio della sessione,
le modifiche hanno effetto la prossima volta che avviate una nuova sessione. Questo mantiene il prompt di sistema
stabile durante una conversazione in modo che il prompt caching possa ridurre la latenza e
il costo.

## Creare un output style personalizzato

Gli output styles personalizzati sono file Markdown con frontmatter e il testo che verrà
aggiunto al prompt di sistema:

```markdown  theme={null}
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

Potete salvare questi file a livello utente (`~/.claude/output-styles`) o
a livello di progetto (`.claude/output-styles`).

### Frontmatter

I file di output style supportano frontmatter per specificare i metadati:

| Frontmatter                | Scopo                                                                              | Predefinito               |
| :------------------------- | :--------------------------------------------------------------------------------- | :------------------------ |
| `name`                     | Nome dell'output style, se non il nome del file                                    | Eredita dal nome del file |
| `description`              | Descrizione dell'output style, mostrata nel picker `/config`                       | Nessuno                   |
| `keep-coding-instructions` | Se mantenere le parti del prompt di sistema di Claude Code relative alla codifica. | false                     |

## Confronti con funzionalità correlate

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Gli output styles "disattivano" completamente le parti del prompt di sistema predefinito di Claude Code
specifiche per l'ingegneria del software. Né CLAUDE.md né
`--append-system-prompt` modificano il prompt di sistema predefinito di Claude Code. CLAUDE.md
aggiunge i contenuti come messaggio utente *seguendo* il prompt di sistema predefinito di Claude Code. `--append-system-prompt` aggiunge il contenuto al prompt di sistema.

### Output Styles vs. [Agents](/it/sub-agents)

Gli output styles influenzano direttamente il loop dell'agente principale e influenzano solo il prompt
di sistema. Gli agenti vengono invocati per gestire compiti specifici e possono includere impostazioni aggiuntive
come il modello da utilizzare, gli strumenti disponibili e un contesto
su quando utilizzare l'agente.

### Output Styles vs. [Skills](/it/skills)

Gli output styles modificano il modo in cui Claude risponde (formattazione, tono, struttura) e sono sempre attivi una volta selezionati. Skills sono prompt specifici per compiti che invocate con `/skill-name` o che Claude carica automaticamente quando rilevante. Utilizzate gli output styles per preferenze di formattazione coerenti; utilizzate skills per flussi di lavoro e compiti riutilizzabili.
