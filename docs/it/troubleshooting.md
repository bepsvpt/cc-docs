> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting

> Risolvi i problemi di utilizzo elevato di CPU o memoria, blocchi, thrashing auto-compact e problemi di ricerca in Claude Code, e trova la pagina giusta per altri problemi.

Questa pagina copre i problemi di prestazioni, stabilità e ricerca una volta che Claude Code è in esecuzione. Per altri problemi, inizia con la pagina che corrisponde a dove sei bloccato:

| Sintomo                                                                                                     | Vai a                                                                                    |
| :---------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `command not found`, l'installazione fallisce, problemi di PATH, `EACCES`, errori TLS                       | [Troubleshoot installation and login](/it/troubleshoot-install)                          |
| Loop di accesso, errori OAuth, `403 Forbidden`, "organization disabled", credenziali Bedrock/Vertex/Foundry | [Troubleshoot installation and login](/it/troubleshoot-install#login-and-authentication) |
| Le impostazioni non si applicano, gli hooks non si attivano, i server MCP non si caricano                   | [Debug your configuration](/it/debug-your-config)                                        |
| `API Error: 5xx`, `529 Overloaded`, `429`, errori di convalida delle richieste                              | [Error reference](/it/errors)                                                            |
| `model not found` o `you may not have access to it`                                                         | [Error reference](/it/errors#theres-an-issue-with-the-selected-model)                    |
| L'estensione VS Code non si connette o non rileva Claude                                                    | [VS Code integration](/it/vs-code#fix-common-issues)                                     |
| Il plugin JetBrains o l'IDE non viene rilevato                                                              | [JetBrains integration](/it/jetbrains#troubleshooting)                                   |
| Utilizzo elevato di CPU o memoria, risposte lente, blocchi, la ricerca non trova file                       | [Performance and stability](#performance-and-stability) di seguito                       |

Se non sei sicuro di quale si applica, esegui `/doctor` all'interno di Claude Code per un controllo automatico della tua installazione, impostazioni, server MCP e utilizzo del contesto. Se `claude` non si avvia affatto, esegui `claude doctor` dalla tua shell.

## Performance and stability

Queste sezioni coprono i problemi relativi all'utilizzo delle risorse, alla reattività e al comportamento della ricerca.

### High CPU or memory usage

Claude Code è progettato per funzionare con la maggior parte degli ambienti di sviluppo, ma potrebbe consumare risorse significative durante l'elaborazione di grandi basi di codice. Se stai riscontrando problemi di prestazioni:

1. Usa `/compact` regolarmente per ridurre la dimensione del contesto
2. Chiudi e riavvia Claude Code tra i compiti principali
3. Considera di aggiungere grandi directory di build al tuo file `.gitignore`

Se l'utilizzo della memoria rimane elevato dopo questi passaggi, esegui `/heapdump` per scrivere uno snapshot dell'heap JavaScript e una suddivisione della memoria su `~/Desktop`. Su Linux senza una cartella Desktop, i file vengono scritti nella tua directory home.

La suddivisione mostra la dimensione del set residente, l'heap JS, i buffer di array e la memoria nativa non contabilizzata, il che aiuta a identificare se la crescita è negli oggetti JavaScript o nel codice nativo. Per ispezionare i detentori, apri il file `.heapsnapshot` in Chrome DevTools sotto Memory → Load. Allega entrambi i file quando segnali un problema di memoria su [GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compaction stops with a thrashing error

Se vedi `Autocompact is thrashing: the context refilled to the limit...`, la compattazione automatica è riuscita ma un file o un output dello strumento ha immediatamente riempito la finestra di contesto più volte di seguito. Claude Code smette di riprovare per evitare di sprecare chiamate API su un ciclo che non sta facendo progressi.

Per recuperare:

1. Chiedi a Claude di leggere il file di grandi dimensioni in blocchi più piccoli, come un intervallo di righe specifico o una funzione, invece dell'intero file
2. Esegui `/compact` con un focus che elimina l'output di grandi dimensioni, ad esempio `/compact keep only the plan and the diff`
3. Sposta il lavoro su file di grandi dimensioni a un [subagent](/it/sub-agents) in modo che venga eseguito in una finestra di contesto separata
4. Esegui `/clear` se la conversazione precedente non è più necessaria

### Command hangs or freezes

Se Claude Code sembra non reattivo:

1. Premi Ctrl+C per tentare di annullare l'operazione corrente
2. Se non reattivo, potrebbe essere necessario chiudere il terminale e riavviare

Il riavvio non perde la tua conversazione. Esegui `claude --resume` nella stessa directory per riprendere la sessione.

### Search and discovery issues

Se lo strumento Search, le menzioni `@file`, gli agenti personalizzati o le skill personalizzate non trovano file, il binario `ripgrep` in bundle potrebbe non funzionare sul tuo sistema. Installa il pacchetto `ripgrep` della tua piattaforma e dì a Claude Code di usarlo:

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

Quindi imposta `USE_BUILTIN_RIPGREP=0` nel tuo [environment](/it/env-vars).

### Slow or incomplete search results on WSL

Le penalità di prestazioni di lettura del disco quando [lavori tra file system su WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) possono risultare in meno corrispondenze del previsto quando usi Claude Code su WSL. La ricerca funziona ancora, ma restituisce meno risultati rispetto a un file system nativo.

<Note>
  `/doctor` mostrerà Search come OK in questo caso.
</Note>

**Soluzioni:**

1. **Invia ricerche più specifiche**: riduci il numero di file cercati specificando directory o tipi di file: "Search for JWT validation logic in the auth-service package" o "Find use of md5 hash in JS files".

2. **Sposta il progetto al file system Linux**: se possibile, assicurati che il tuo progetto si trovi sul file system Linux (`/home/`) piuttosto che sul file system di Windows (`/mnt/c/`).

3. **Usa Windows nativo**: considera di eseguire Claude Code nativamente su Windows invece che tramite WSL, per migliori prestazioni del file system.

## Get more help

Se stai riscontrando problemi non affrontati qui:

1. Esegui `/doctor` per controllare la salute dell'installazione, la validità delle impostazioni, la configurazione MCP e l'utilizzo del contesto in un unico passaggio
2. Usa il comando `/feedback` all'interno di Claude Code per segnalare i problemi direttamente ad Anthropic
3. Controlla il [repository GitHub](https://github.com/anthropics/claude-code) per i problemi noti
4. Chiedi a Claude direttamente sulle sue capacità e funzionalità. Claude ha accesso integrato alla sua documentazione.
