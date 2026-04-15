> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Usa Claude Code con JetBrains IDEs inclusi IntelliJ, PyCharm, WebStorm e altri

Claude Code si integra con JetBrains IDEs attraverso un plugin dedicato, fornendo funzionalità come la visualizzazione interattiva dei diff, la condivisione del contesto della selezione e altro ancora.

## IDE supportati

Il plugin Claude Code funziona con la maggior parte dei JetBrains IDEs, inclusi:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Funzionalità

* **Avvio rapido**: Usa `Cmd+Esc` (Mac) o `Ctrl+Esc` (Windows/Linux) per aprire Claude Code direttamente dal tuo editor, oppure fai clic sul pulsante Claude Code nell'interfaccia utente
* **Visualizzazione dei diff**: Le modifiche al codice possono essere visualizzate direttamente nel visualizzatore diff dell'IDE invece del terminale
* **Contesto della selezione**: La selezione/scheda corrente nell'IDE viene automaticamente condivisa con Claude Code
* **Scorciatoie di riferimento file**: Usa `Cmd+Option+K` (Mac) o `Alt+Ctrl+K` (Linux/Windows) per inserire riferimenti ai file (ad esempio, @File#L1-99)
* **Condivisione diagnostica**: Gli errori diagnostici (lint, sintassi, ecc.) dall'IDE vengono automaticamente condivisi con Claude mentre lavori

## Installazione

### Installazione da Marketplace

Trova e installa il [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) dal marketplace di JetBrains e riavvia il tuo IDE.

Se non hai ancora installato Claude Code, consulta la [nostra guida di avvio rapido](/it/quickstart) per le istruzioni di installazione.

<Note>
  Dopo aver installato il plugin, potrebbe essere necessario riavviare completamente il tuo IDE affinché abbia effetto.
</Note>

## Utilizzo

### Dal tuo IDE

Esegui `claude` dal terminale integrato del tuo IDE e tutte le funzionalità di integrazione saranno attive.

### Da terminali esterni

Usa il comando `/ide` in qualsiasi terminale esterno per connettere Claude Code al tuo JetBrains IDE e attivare tutte le funzionalità:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Se desideri che Claude abbia accesso agli stessi file del tuo IDE, avvia Claude Code dalla stessa directory della radice del progetto del tuo IDE.

## Configurazione

### Impostazioni di Claude Code

Configura l'integrazione dell'IDE attraverso le impostazioni di Claude Code:

1. Esegui `claude`
2. Inserisci il comando `/config`
3. Imposta lo strumento diff su `auto` per il rilevamento automatico dell'IDE

### Impostazioni del plugin

Configura il plugin Claude Code andando a **Impostazioni → Strumenti → Claude Code \[Beta]**:

#### Impostazioni generali

* **Comando Claude**: Specifica un comando personalizzato per eseguire Claude (ad esempio, `claude`, `/usr/local/bin/claude`, o `npx @anthropic/claude`)
* **Sopprimere la notifica per il comando Claude non trovato**: Salta le notifiche relative al mancato reperimento del comando Claude
* **Abilita l'uso di Option+Invio per prompt multi-riga** (solo macOS): Quando abilitato, Option+Invio inserisce nuove righe nei prompt di Claude Code. Disabilita se riscontri problemi con il tasto Option catturato inaspettatamente (richiede il riavvio del terminale)
* **Abilita aggiornamenti automatici**: Controlla automaticamente e installa gli aggiornamenti del plugin (applicati al riavvio)

<Tip>
  Per gli utenti WSL: Imposta `wsl -d Ubuntu -- bash -lic "claude"` come comando Claude (sostituisci `Ubuntu` con il nome della tua distribuzione WSL)
</Tip>

#### Configurazione del tasto ESC

Se il tasto ESC non interrompe le operazioni di Claude Code nei terminali JetBrains:

1. Vai a **Impostazioni → Strumenti → Terminale**
2. Oppure:
   * Deseleziona "Sposta il focus sull'editor con Escape", oppure
   * Fai clic su "Configura scorciatoie da tastiera del terminale" e elimina la scorciatoia "Sposta il focus sull'editor"
3. Applica le modifiche

Questo consente al tasto ESC di interrompere correttamente le operazioni di Claude Code.

## Configurazioni speciali

### Sviluppo remoto

<Warning>
  Quando usi JetBrains Remote Development, devi installare il plugin nell'host remoto tramite **Impostazioni → Plugin (Host)**.
</Warning>

Il plugin deve essere installato sull'host remoto, non sulla tua macchina client locale.

### Configurazione WSL

<Warning>
  Gli utenti WSL potrebbero aver bisogno di configurazione aggiuntiva affinché il rilevamento dell'IDE funzioni correttamente. Consulta la nostra [guida alla risoluzione dei problemi WSL](/it/troubleshooting#jetbrains-ide-not-detected-on-wsl2) per istruzioni di configurazione dettagliate.
</Warning>

La configurazione WSL potrebbe richiedere:

* Configurazione corretta del terminale
* Regolazioni della modalità di rete
* Aggiornamenti delle impostazioni del firewall

## Risoluzione dei problemi

### Plugin non funzionante

* Assicurati di eseguire Claude Code dalla directory radice del progetto
* Verifica che il plugin JetBrains sia abilitato nelle impostazioni dell'IDE
* Riavvia completamente l'IDE (potrebbe essere necessario farlo più volte)
* Per Remote Development, assicurati che il plugin sia installato nell'host remoto

### IDE non rilevato

* Verifica che il plugin sia installato e abilitato
* Riavvia completamente l'IDE
* Verifica che tu stia eseguendo Claude Code dal terminale integrato
* Per gli utenti WSL, consulta la [guida alla risoluzione dei problemi WSL](/it/troubleshooting#jetbrains-ide-not-detected-on-wsl2)

### Comando non trovato

Se facendo clic sull'icona Claude viene visualizzato "comando non trovato":

1. Verifica che Claude Code sia installato: `npm list -g @anthropic-ai/claude-code`
2. Configura il percorso del comando Claude nelle impostazioni del plugin
3. Per gli utenti WSL, usa il formato del comando WSL menzionato nella sezione di configurazione

## Considerazioni sulla sicurezza

Quando Claude Code viene eseguito in un JetBrains IDE con le autorizzazioni di modifica automatica abilitate, potrebbe essere in grado di modificare i file di configurazione dell'IDE che possono essere eseguiti automaticamente dal tuo IDE. Questo potrebbe aumentare il rischio di eseguire Claude Code in modalità di modifica automatica e consentire di aggirare i prompt di autorizzazione di Claude Code per l'esecuzione bash.

Quando si esegue in JetBrains IDEs, considera:

* Utilizzare la modalità di approvazione manuale per le modifiche
* Prestare particolare attenzione per assicurarsi che Claude sia utilizzato solo con prompt affidabili
* Essere consapevole di quali file Claude Code ha accesso per modificare

Per ulteriore aiuto, consulta la nostra [guida alla risoluzione dei problemi](/it/troubleshooting).
