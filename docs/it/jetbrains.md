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
* **Contesto della selezione**: La selezione corrente o la scheda nell'IDE viene automaticamente condivisa con Claude Code
* **Scorciatoie di riferimento file**: Usa `Cmd+Option+K` (Mac) o `Alt+Ctrl+K` (Linux/Windows) per inserire riferimenti ai file come `@src/auth.ts#L1-99`
* **Condivisione diagnostica**: Gli errori diagnostici dall'IDE, come errori di lint e sintassi, vengono automaticamente condivisi con Claude mentre lavori

## Installazione

### Installazione da Marketplace

Trova e installa il [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) dal marketplace di JetBrains e riavvia il tuo IDE.

Se non hai ancora installato Claude Code, consulta la [guida di avvio rapido](/it/quickstart) per le istruzioni di installazione.

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
3. Imposta lo strumento diff su `auto` per mostrare i diff nell'IDE, oppure `terminal` per mantenerli nel terminale

### Impostazioni del plugin

Configura il plugin Claude Code andando a **Impostazioni → Strumenti → Claude Code \[Beta]**:

#### Impostazioni generali

* **Comando Claude**: Specifica un comando personalizzato per eseguire Claude, ad esempio `claude`, `/usr/local/bin/claude`, o `npx @anthropic-ai/claude-code`
* **Sopprimere la notifica per il comando Claude non trovato**: Salta le notifiche relative al mancato reperimento del comando Claude
* **Abilita l'uso di Option+Invio per prompt multi-riga**: Solo su macOS. Quando abilitato, Option+Invio inserisce nuove righe nei prompt di Claude Code. Disabilita se il tasto Option viene catturato inaspettatamente. Richiede il riavvio del terminale.
* **Abilita aggiornamenti automatici**: Controlla automaticamente e installa gli aggiornamenti del plugin, applicati al riavvio

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

Se stai usando Claude Code su WSL2 con un JetBrains IDE e vedi "No available IDEs detected", la causa è solitamente la rete NAT di WSL2 o il Windows Firewall che blocca la connessione tra WSL2 e l'IDE in esecuzione sull'host Windows. WSL1 utilizza direttamente la rete dell'host e non è interessato.

#### Consenti il traffico WSL2 attraverso Windows Firewall

Questa è la correzione consigliata perché mantiene la tua modalità di rete WSL2 esistente.

<Steps>
  <Step title="Trova il tuo indirizzo IP WSL2">
    Dalla tua shell WSL, esegui:

    ```bash theme={null}
    hostname -I
    ```

    Annota la subnet, ad esempio `172.21.123.45` è in `172.21.0.0/16`.
  </Step>

  <Step title="Crea una regola firewall">
    Apri PowerShell come Amministratore ed esegui quanto segue, regolando l'intervallo IP per corrispondere alla tua subnet:

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="Riavvia il tuo IDE e Claude Code">
    Chiudi e riapri entrambi affinché la nuova regola abbia effetto.
  </Step>
</Steps>

#### Passa WSL2 alla rete con mirroring

La rete con mirroring richiede Windows 11 22H2 o successivo. Se sei su Windows 10, usa la regola firewall sopra indicata.

Aggiungi questo a `.wslconfig` nella tua directory utente Windows:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Quindi riavvia WSL con `wsl --shutdown` da PowerShell.

## Risoluzione dei problemi

### Plugin non funzionante

Se il plugin è installato ma le funzionalità di Claude Code non appaiono nel tuo IDE:

* Assicurati di eseguire Claude Code dalla directory radice del progetto
* Verifica che il plugin JetBrains sia abilitato nelle impostazioni dell'IDE
* Riavvia completamente l'IDE (potrebbe essere necessario farlo più volte)
* Per Remote Development, assicurati che il plugin sia installato nell'host remoto

### IDE non rilevato

Se l'esecuzione di `claude` mostra "No available IDEs detected":

* Verifica che il plugin sia installato e abilitato
* Riavvia completamente l'IDE
* Verifica che tu stia eseguendo Claude Code dal terminale integrato
* Per gli utenti WSL, consulta la [configurazione WSL](#wsl-configuration) sopra

### Comando non trovato

Se facendo clic sull'icona Claude viene visualizzato "command not found":

1. Verifica che Claude Code sia installato eseguendo `claude --version` in un terminale
2. Configura il percorso del comando Claude nelle impostazioni del plugin
3. Per gli utenti WSL, usa il formato del comando WSL menzionato nella sezione di configurazione

## Considerazioni sulla sicurezza

Quando Claude Code viene eseguito in un JetBrains IDE con le autorizzazioni di modifica automatica abilitate, potrebbe essere in grado di modificare i file di configurazione dell'IDE che possono essere eseguiti automaticamente dal tuo IDE. Questo potrebbe aumentare il rischio di eseguire Claude Code in modalità di modifica automatica e consentire di aggirare i prompt di autorizzazione di Claude Code per l'esecuzione bash.

Quando si esegue in JetBrains IDEs, considera:

* Utilizzare la modalità di approvazione manuale per le modifiche
* Prestare particolare attenzione per assicurarsi che Claude sia utilizzato solo con prompt affidabili
* Essere consapevole di quali file Claude Code ha accesso per modificare

Per problemi di installazione o accesso a Claude Code al di fuori dell'IDE, consulta [Risolvi i problemi di installazione e accesso](/it/troubleshoot-install).
