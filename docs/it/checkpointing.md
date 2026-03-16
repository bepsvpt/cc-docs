> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# checkpoint

> Traccia automaticamente e riavvolgi gli edit di Claude per recuperare rapidamente dai cambiamenti indesiderati.

Claude Code traccia automaticamente gli edit dei file di Claude mentre lavori, permettendoti di annullare rapidamente i cambiamenti e riavvolgere a stati precedenti se qualcosa va fuori strada.

## Come funziona il checkpoint

Mentre lavori con Claude, il checkpointing cattura automaticamente lo stato del tuo codice prima di ogni edit. Questa rete di sicurezza ti permette di perseguire compiti ambiziosi e su larga scala sapendo che puoi sempre tornare a uno stato di codice precedente.

### Tracciamento automatico

Claude Code traccia tutti i cambiamenti effettuati dai suoi strumenti di editing dei file:

* Ogni prompt dell'utente crea un nuovo checkpoint
* I checkpoint persistono tra le sessioni, quindi puoi accedervi nelle conversazioni riprese
* Puliti automaticamente insieme alle sessioni dopo 30 giorni (configurabile)

### Riavvolgimento dei cambiamenti

Premi `Esc` due volte (`Esc` + `Esc`) o usa il comando `/rewind` per aprire il menu di riavvolgimento. Puoi scegliere di ripristinare:

* **Solo conversazione**: Riavvolgi a un messaggio dell'utente mantenendo i cambiamenti del codice
* **Solo codice**: Ripristina i cambiamenti dei file mantenendo la conversazione
* **Sia codice che conversazione**: Ripristina entrambi a un punto precedente nella sessione

## Casi d'uso comuni

I checkpoint sono particolarmente utili quando:

* **Esplorare alternative**: Prova diversi approcci di implementazione senza perdere il tuo punto di partenza
* **Recuperare da errori**: Annulla rapidamente i cambiamenti che hanno introdotto bug o rotto la funzionalità
* **Iterare sulle funzionalità**: Sperimenta variazioni sapendo che puoi tornare a stati funzionanti

## Limitazioni

### I cambiamenti dei comandi Bash non vengono tracciati

Il checkpointing non traccia i file modificati dai comandi bash. Ad esempio, se Claude Code esegue:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Queste modifiche ai file non possono essere annullate tramite riavvolgimento. Solo gli edit diretti dei file effettuati attraverso gli strumenti di editing dei file di Claude vengono tracciati.

### I cambiamenti esterni non vengono tracciati

Il checkpointing traccia solo i file che sono stati modificati nella sessione corrente. I cambiamenti manuali che effettui ai file al di fuori di Claude Code e gli edit da altre sessioni concorrenti normalmente non vengono acquisiti, a meno che non modifichino gli stessi file della sessione corrente.

### Non è un sostituto del controllo di versione

I checkpoint sono progettati per il recupero rapido a livello di sessione. Per la cronologia permanente della versione e la collaborazione:

* Continua a utilizzare il controllo di versione (es. Git) per commit, branch e cronologia a lungo termine
* I checkpoint completano ma non sostituiscono il controllo di versione appropriato
* Pensa ai checkpoint come "annulla locale" e Git come "cronologia permanente"

## Vedi anche

* [Modalità interattiva](/it/interactive-mode) - Scorciatoie da tastiera e controlli della sessione
* [Comandi integrati](/it/interactive-mode#built-in-commands) - Accesso ai checkpoint usando `/rewind`
* [Riferimento CLI](/it/cli-reference) - Opzioni della riga di comando
