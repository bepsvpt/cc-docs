> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Traccia, riavvolgi e riassumi le modifiche e la conversazione di Claude per gestire lo stato della sessione.

Claude Code traccia automaticamente le modifiche ai file di Claude mentre lavori, permettendoti di annullare rapidamente le modifiche e tornare a stati precedenti se qualcosa non va come previsto.

## Come funziona il checkpointing

Mentre lavori con Claude, il checkpointing cattura automaticamente lo stato del tuo codice prima di ogni modifica. Questa rete di sicurezza ti permette di affrontare compiti ambiziosi e su larga scala sapendo che puoi sempre tornare a uno stato di codice precedente.

### Tracciamento automatico

Claude Code traccia tutti i cambiamenti effettuati dai suoi strumenti di modifica dei file:

* Ogni prompt dell'utente crea un nuovo checkpoint
* I checkpoint persistono tra le sessioni, quindi puoi accedervi nelle conversazioni riprese
* Puliti automaticamente insieme alle sessioni dopo 30 giorni (configurabile)

### Riavvolgi e riassumi

Esegui `/rewind`, oppure premi `Esc` due volte quando il campo di input del prompt è vuoto, per aprire il menu di riavvolgimento.

<Note>
  Se il campo di input del prompt contiene testo, doppio `Esc` lo cancella invece di aprire il menu. Il testo cancellato viene salvato nella cronologia di input, quindi premi `Su` per richiamarlo dopo aver terminato nel menu di riavvolgimento.
</Note>

Il menu di riavvolgimento elenca ogni prompt che hai inviato durante la sessione. Seleziona il punto su cui desideri agire, quindi scegli un'azione:

* **Ripristina codice e conversazione**: ripristina sia il codice che la conversazione a quel punto
* **Ripristina conversazione**: riavvolgi al messaggio mantenendo il codice attuale
* **Ripristina codice**: ripristina le modifiche ai file mantenendo la conversazione
* **Riassumi da qui**: comprimi la conversazione da questo punto in avanti in un riassunto, liberando spazio nella context window
* **Riassumi fino a qui**: comprimi la conversazione prima di questo punto in un riassunto, mantenendo i messaggi successivi intatti
* **Non importa**: torna all'elenco dei messaggi senza apportare modifiche

Dopo aver ripristinato la conversazione o aver scelto Riassumi da qui, il prompt originale dal messaggio selezionato viene ripristinato nel campo di input in modo che tu possa reinviarlo o modificarlo.

Scegliendo Riassumi fino a qui ti lascia alla fine della conversazione con l'input vuoto.

#### Ripristina vs. riassumi

Le opzioni di ripristino ripristinano lo stato: annullano le modifiche al codice, la cronologia della conversazione o entrambi. Le opzioni di riassunto comprimono parte della conversazione in un riassunto generato dall'IA senza modificare i file su disco:

* **Riassumi da qui**: i messaggi prima del messaggio selezionato rimangono intatti. Il messaggio selezionato e tutto ciò che segue vengono sostituiti con un riassunto. Usa questo per scartare una discussione laterale mantenendo il contesto iniziale in dettaglio completo.
* **Riassumi fino a qui**: i messaggi prima del messaggio selezionato vengono sostituiti con un riassunto. Il messaggio selezionato e tutto ciò che segue rimangono intatti, e rimani alla fine della conversazione. Usa questo per comprimere la discussione di configurazione iniziale mantenendo il lavoro recente in dettaglio completo.

In entrambi i casi i messaggi originali vengono conservati nella trascrizione della sessione, quindi Claude può fare riferimento ai dettagli se necessario. Puoi digitare istruzioni facoltative per guidare su cosa si concentra il riassunto. Questo è simile a `/compact`, ma mirato: invece di riassumere l'intera conversazione, scegli quale lato del messaggio selezionato comprimere.

<Note>
  Riassumi ti mantiene nella stessa sessione e comprime il contesto. Se desideri creare un ramo e provare un approccio diverso preservando la sessione originale intatta, usa [fork](/it/sessions#branch-a-session) invece (`claude --continue --fork-session`).
</Note>

## Casi d'uso comuni

I checkpoint sono particolarmente utili quando:

* **Esplorare alternative**: prova diversi approcci di implementazione senza perdere il tuo punto di partenza
* **Recuperare da errori**: annulla rapidamente le modifiche che hanno introdotto bug o rotto la funzionalità
* **Iterare sulle funzionalità**: sperimenta variazioni sapendo che puoi tornare a stati funzionanti
* **Liberare spazio di contesto**: riassumi una sessione di debug dettagliata dal punto intermedio in avanti, mantenendo le tue istruzioni iniziali intatte

## Limitazioni

### Le modifiche dei comandi Bash non vengono tracciate

Il checkpointing non traccia i file modificati dai comandi bash. Ad esempio, se Claude Code esegue:

```bash theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Queste modifiche ai file non possono essere annullate tramite riavvolgimento. Solo le modifiche dirette ai file effettuate attraverso gli strumenti di modifica dei file di Claude vengono tracciate.

### Le modifiche esterne non vengono tracciate

Il checkpointing traccia solo i file che sono stati modificati nella sessione corrente. Le modifiche manuali che effettui ai file al di fuori di Claude Code e le modifiche da altre sessioni concorrenti normalmente non vengono acquisite, a meno che non modifichino gli stessi file della sessione corrente.

### Non è un sostituto del controllo della versione

I checkpoint sono progettati per il recupero rapido a livello di sessione. Per la cronologia permanente della versione e la collaborazione:

* Continua a utilizzare il controllo della versione (ad es. Git) per commit, rami e cronologia a lungo termine
* I checkpoint completano ma non sostituiscono il controllo della versione appropriato
* Pensa ai checkpoint come "annulla locale" e Git come "cronologia permanente"

## Vedi anche

* [Modalità interattiva](/it/interactive-mode) - Scorciatoie da tastiera e controlli della sessione
* [Comandi](/it/commands) - Accesso ai checkpoint usando `/rewind`
* [Riferimento CLI](/it/cli-reference) - Opzioni della riga di comando
