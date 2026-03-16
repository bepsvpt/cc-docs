> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Accelera le risposte con la modalità veloce

> Ottieni risposte più veloci di Opus 4.6 in Claude Code attivando la modalità veloce.

<Note>
  La modalità veloce è in [anteprima di ricerca](#research-preview). La funzione, i prezzi e la disponibilità potrebbero cambiare in base al feedback.
</Note>

La modalità veloce è una configurazione ad alta velocità per Claude Opus 4.6, che rende il modello 2,5 volte più veloce a un costo per token più elevato. Attivala con `/fast` quando hai bisogno di velocità per il lavoro interattivo come l'iterazione rapida o il debug in tempo reale, e disattivala quando il costo è più importante della latenza.

La modalità veloce non è un modello diverso. Utilizza lo stesso Opus 4.6 con una configurazione API diversa che dà priorità alla velocità rispetto all'efficienza dei costi. Ottieni la stessa qualità e capacità, solo risposte più veloci.

<Note>
  La modalità veloce richiede Claude Code v2.1.36 o successivo. Controlla la tua versione con `claude --version`.
</Note>

Cosa sapere:

* Usa `/fast` per attivare/disattivare la modalità veloce in Claude Code CLI. Disponibile anche tramite `/fast` nell'estensione Claude Code VS Code.
* I prezzi della modalità veloce per Opus 4.6 iniziano da \$30/150 MTok. La modalità veloce è disponibile con uno sconto del 50% per tutti i piani fino alle 23:59 PT del 16 febbraio.
* Disponibile per tutti gli utenti di Claude Code sui piani di abbonamento (Pro/Max/Team/Enterprise) e Claude Console.
* Per gli utenti di Claude Code sui piani di abbonamento (Pro/Max/Team/Enterprise), la modalità veloce è disponibile solo tramite utilizzo aggiuntivo e non è inclusa nei limiti di velocità dell'abbonamento.

Questa pagina copre come [attivare/disattivare la modalità veloce](#toggle-fast-mode), il suo [compromesso di costo](#understand-the-cost-tradeoff), [quando usarla](#decide-when-to-use-fast-mode), [requisiti](#requirements), [opt-in per sessione](#require-per-session-opt-in), e [comportamento dei limiti di velocità](#handle-rate-limits).

## Attiva/disattiva la modalità veloce

Attiva/disattiva la modalità veloce in uno di questi modi:

* Digita `/fast` e premi Tab per attivare o disattivare
* Imposta `"fastMode": true` nel tuo [file di impostazioni utente](/it/settings)

Per impostazione predefinita, la modalità veloce persiste tra le sessioni. Gli amministratori possono configurare la modalità veloce per ripristinarsi ogni sessione. Vedi [richiedi opt-in per sessione](#require-per-session-opt-in) per i dettagli.

Per la migliore efficienza dei costi, abilita la modalità veloce all'inizio di una sessione piuttosto che passare a metà conversazione. Vedi [comprendi il compromesso di costo](#understand-the-cost-tradeoff) per i dettagli.

Quando abiliti la modalità veloce:

* Se sei su un modello diverso, Claude Code passa automaticamente a Opus 4.6
* Vedrai un messaggio di conferma: "Fast mode ON"
* Un piccolo icona `↯` appare accanto al prompt mentre la modalità veloce è attiva
* Esegui `/fast` di nuovo in qualsiasi momento per verificare se la modalità veloce è attiva o disattiva

Quando disabiliti la modalità veloce con `/fast` di nuovo, rimani su Opus 4.6. Il modello non torna al tuo modello precedente. Per passare a un modello diverso, usa `/model`.

## Comprendi il compromesso di costo

La modalità veloce ha un prezzo per token più elevato rispetto a Opus 4.6 standard:

| Modalità                             | Input (MTok) | Output (MTok) |
| ------------------------------------ | ------------ | ------------- |
| Modalità veloce su Opus 4.6 (\<200K) | \$30         | \$150         |
| Modalità veloce su Opus 4.6 (>200K)  | \$60         | \$225         |

La modalità veloce è compatibile con la finestra di contesto estesa di 1M token.

Quando passi alla modalità veloce a metà conversazione, paghi il prezzo completo del token di input non memorizzato nella cache della modalità veloce per l'intero contesto della conversazione. Questo costa più di quanto avresti pagato se avessi abilitato la modalità veloce dall'inizio.

## Decidi quando usare la modalità veloce

La modalità veloce è migliore per il lavoro interattivo dove la latenza della risposta è più importante del costo:

* Iterazione rapida su modifiche del codice
* Sessioni di debug in tempo reale
* Lavoro sensibile al tempo con scadenze strette

La modalità standard è migliore per:

* Attività autonome lunghe dove la velocità è meno importante
* Elaborazione batch o pipeline CI/CD
* Carichi di lavoro sensibili ai costi

### Modalità veloce rispetto al livello di sforzo

La modalità veloce e il livello di sforzo influenzano entrambi la velocità di risposta, ma in modo diverso:

| Impostazione                    | Effetto                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Modalità veloce**             | Stessa qualità del modello, latenza inferiore, costo più elevato                                       |
| **Livello di sforzo inferiore** | Meno tempo di riflessione, risposte più veloci, potenzialmente qualità inferiore su attività complesse |

Puoi combinare entrambi: usa la modalità veloce con un [livello di sforzo](/it/model-config#adjust-effort-level) inferiore per la massima velocità su attività semplici.

## Requisiti

La modalità veloce richiede tutti i seguenti elementi:

* **Non disponibile su provider cloud di terze parti**: la modalità veloce non è disponibile su Amazon Bedrock, Google Vertex AI o Microsoft Azure Foundry. La modalità veloce è disponibile tramite l'API Anthropic Console e per i piani di abbonamento Claude utilizzando l'utilizzo aggiuntivo.
* **Utilizzo aggiuntivo abilitato**: il tuo account deve avere l'utilizzo aggiuntivo abilitato, che consente la fatturazione oltre l'utilizzo incluso nel tuo piano. Per gli account individuali, abilita questo nelle tue [impostazioni di fatturazione della Console](https://platform.claude.com/settings/organization/billing). Per Teams e Enterprise, un amministratore deve abilitare l'utilizzo aggiuntivo per l'organizzazione.

<Note>
  L'utilizzo della modalità veloce viene fatturato direttamente all'utilizzo aggiuntivo, anche se hai un utilizzo rimanente nel tuo piano. Ciò significa che i token della modalità veloce non contano rispetto all'utilizzo incluso nel tuo piano e vengono addebitati alla tariffa della modalità veloce dal primo token.
</Note>

* **Abilitazione dell'amministratore per Teams e Enterprise**: la modalità veloce è disabilitata per impostazione predefinita per le organizzazioni Teams e Enterprise. Un amministratore deve esplicitamente [abilitare la modalità veloce](#enable-fast-mode-for-your-organization) prima che gli utenti possano accedervi.

<Note>
  Se il tuo amministratore non ha abilitato la modalità veloce per la tua organizzazione, il comando `/fast` mostrerà "Fast mode has been disabled by your organization."
</Note>

### Abilita la modalità veloce per la tua organizzazione

Gli amministratori possono abilitare la modalità veloce in:

* **Console** (clienti API): [Preferenze Claude Code](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Teams e Enterprise): [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

Un'altra opzione per disabilitare completamente la modalità veloce è impostare `CLAUDE_CODE_DISABLE_FAST_MODE=1`. Vedi [Variabili di ambiente](/it/settings#environment-variables).

### Richiedi opt-in per sessione

Per impostazione predefinita, la modalità veloce persiste tra le sessioni: se un utente abilita la modalità veloce, rimane attiva nelle sessioni future. Gli amministratori sui piani [Teams](https://claude.com/pricing#team-&-enterprise) o [Enterprise](https://anthropic.com/contact-sales) possono impedire questo impostando `fastModePerSessionOptIn` a `true` nelle [impostazioni gestite](/it/settings#settings-files) o [impostazioni gestite dal server](/it/server-managed-settings). Ciò fa sì che ogni sessione inizi con la modalità veloce disattivata, richiedendo agli utenti di abilitarla esplicitamente con `/fast`.

```json  theme={null}
{
  "fastModePerSessionOptIn": true
}
```

Questo è utile per controllare i costi nelle organizzazioni in cui gli utenti eseguono più sessioni simultanee. Gli utenti possono comunque abilitare la modalità veloce con `/fast` quando hanno bisogno di velocità, ma si ripristina all'inizio di ogni nuova sessione. La preferenza della modalità veloce dell'utente è ancora salvata, quindi rimuovere questa impostazione ripristina il comportamento persistente predefinito.

## Gestisci i limiti di velocità

La modalità veloce ha limiti di velocità separati da Opus 4.6 standard. Quando raggiungi il limite di velocità della modalità veloce o esaurisci i crediti di utilizzo aggiuntivo:

1. La modalità veloce torna automaticamente a Opus 4.6 standard
2. L'icona `↯` diventa grigia per indicare il raffreddamento
3. Continui a lavorare a velocità e prezzi standard
4. Quando il raffreddamento scade, la modalità veloce si riabilita automaticamente

Per disabilitare manualmente la modalità veloce invece di aspettare il raffreddamento, esegui `/fast` di nuovo.

## Anteprima di ricerca

La modalità veloce è una funzione di anteprima di ricerca. Ciò significa:

* La funzione potrebbe cambiare in base al feedback
* La disponibilità e i prezzi sono soggetti a modifiche
* La configurazione API sottostante potrebbe evolversi

Segnala problemi o feedback tramite i tuoi soliti canali di supporto Anthropic.

## Vedi anche

* [Configurazione del modello](/it/model-config): cambia modelli e regola i livelli di sforzo
* [Gestisci i costi in modo efficace](/it/costs): traccia l'utilizzo dei token e riduci i costi
* [Configurazione della riga di stato](/it/statusline): visualizza le informazioni del modello e del contesto
