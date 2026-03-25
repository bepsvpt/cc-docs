> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Panoramica di Claude Code

> Claude Code è uno strumento di codifica agentivo che legge la tua base di codice, modifica i file, esegue comandi e si integra con i tuoi strumenti di sviluppo. Disponibile nel tuo terminale, IDE, app desktop e browser.

Claude Code è un assistente di codifica alimentato da IA che ti aiuta a creare funzionalità, correggere bug e automatizzare attività di sviluppo. Comprende l'intera tua base di codice e può lavorare su più file e strumenti per portare a termine le cose.

## Inizia

Scegli il tuo ambiente per iniziare. La maggior parte delle superfici richiede un [abbonamento a Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) o un account [Anthropic Console](https://console.anthropic.com/). Il Terminal CLI e VS Code supportano anche [provider di terze parti](/it/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    Il CLI completo per lavorare con Claude Code direttamente nel tuo terminale. Modifica file, esegui comandi e gestisci l'intero progetto dalla riga di comando.

    To install Claude Code, use one of the following methods:

    <Tabs>
      <Tab title="Native Install (Recommended)">
        **macOS, Linux, WSL:**

        ```bash  theme={null}
        curl -fsSL https://claude.ai/install.sh | bash
        ```

        **Windows PowerShell:**

        ```powershell  theme={null}
        irm https://claude.ai/install.ps1 | iex
        ```

        **Windows CMD:**

        ```batch  theme={null}
        curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
        ```

        **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

        <Info>
          Native installations automatically update in the background to keep you on the latest version.
        </Info>
      </Tab>

      <Tab title="Homebrew">
        ```bash  theme={null}
        brew install --cask claude-code
        ```

        <Info>
          Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
        </Info>
      </Tab>

      <Tab title="WinGet">
        ```powershell  theme={null}
        winget install Anthropic.ClaudeCode
        ```

        <Info>
          WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
        </Info>
      </Tab>
    </Tabs>

    Quindi avvia Claude Code in qualsiasi progetto:

    ```bash  theme={null}
    cd your-project
    claude
    ```

    Ti verrà chiesto di accedere al primo utilizzo. È tutto! [Continua con la Guida rapida →](/it/quickstart)

    <Tip>
      Vedi [configurazione avanzata](/it/setup) per le opzioni di installazione, gli aggiornamenti manuali o le istruzioni di disinstallazione. Visita [risoluzione dei problemi](/it/troubleshooting) se riscontri problemi.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    L'estensione VS Code fornisce diff inline, @-mentions, revisione del piano e cronologia delle conversazioni direttamente nel tuo editor.

    * [Installa per VS Code](vscode:extension/anthropic.claude-code)
    * [Installa per Cursor](cursor:extension/anthropic.claude-code)

    Oppure cerca "Claude Code" nella visualizzazione Estensioni (`Cmd+Shift+X` su Mac, `Ctrl+Shift+X` su Windows/Linux). Dopo l'installazione, apri il Palette dei comandi (`Cmd+Shift+P` / `Ctrl+Shift+P`), digita "Claude Code" e seleziona **Apri in Nuova Scheda**.

    [Inizia con VS Code →](/it/vs-code#get-started)
  </Tab>

  <Tab title="App desktop">
    Un'app standalone per eseguire Claude Code al di fuori del tuo IDE o terminale. Rivedi i diff visivamente, esegui più sessioni affiancate, pianifica attività ricorrenti e avvia sessioni cloud.

    Scarica e installa:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel e Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (solo sessioni remote)

    Dopo l'installazione, avvia Claude, accedi e fai clic sulla scheda **Code** per iniziare a codificare. È richiesto un [abbonamento a pagamento](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing).

    [Scopri di più sull'app desktop →](/it/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Esegui Claude Code nel tuo browser senza configurazione locale. Avvia attività a lunga esecuzione e controlla quando sono completate, lavora su repository che non hai localmente o esegui più attività in parallelo. Disponibile su browser desktop e sull'app Claude iOS.

    Inizia a codificare su [claude.ai/code](https://claude.ai/code).

    [Inizia sul web →](/it/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    Un plugin per IntelliJ IDEA, PyCharm, WebStorm e altri IDE JetBrains con visualizzazione diff interattiva e condivisione del contesto di selezione.

    Installa il [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) dal JetBrains Marketplace e riavvia il tuo IDE.

    [Inizia con JetBrains →](/it/jetbrains)
  </Tab>
</Tabs>

## Cosa puoi fare

Ecco alcuni dei modi in cui puoi utilizzare Claude Code:

<AccordionGroup>
  <Accordion title="Automatizza il lavoro che continui a rimandare" icon="wand-magic-sparkles">
    Claude Code gestisce i compiti noiosi che consumano la tua giornata: scrivere test per il codice non testato, correggere errori di lint in un progetto, risolvere conflitti di merge, aggiornare dipendenze e scrivere note di rilascio.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Crea funzionalità e correggi bug" icon="hammer">
    Descrivi quello che vuoi in linguaggio naturale. Claude Code pianifica l'approccio, scrive il codice su più file e verifica che funzioni.

    Per i bug, incolla un messaggio di errore o descrivi il sintomo. Claude Code traccia il problema attraverso la tua base di codice, identifica la causa principale e implementa una correzione. Vedi [flussi di lavoro comuni](/it/common-workflows) per altri esempi.
  </Accordion>

  <Accordion title="Crea commit e pull request" icon="code-branch">
    Claude Code funziona direttamente con git. Mette in stage le modifiche, scrive messaggi di commit, crea branch e apre pull request.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    In CI, puoi automatizzare la revisione del codice e il triage dei problemi con [GitHub Actions](/it/github-actions) o [GitLab CI/CD](/it/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Connetti i tuoi strumenti con MCP" icon="plug">
    Il [Model Context Protocol (MCP)](/it/mcp) è uno standard aperto per connettere gli strumenti di IA alle fonti di dati esterne. Con MCP, Claude Code può leggere i tuoi documenti di progettazione in Google Drive, aggiornare i ticket in Jira, estrarre dati da Slack o utilizzare i tuoi strumenti personalizzati.
  </Accordion>

  <Accordion title="Personalizza con istruzioni, skills e hooks" icon="sliders">
    [`CLAUDE.md`](/it/memory) è un file markdown che aggiungi alla radice del tuo progetto che Claude Code legge all'inizio di ogni sessione. Usalo per impostare standard di codifica, decisioni architettoniche, librerie preferite e checklist di revisione. Claude costruisce anche [memoria automatica](/it/memory#auto-memory) mentre lavora, salvando insegnamenti come comandi di build e intuizioni di debug tra le sessioni senza che tu debba scrivere nulla.

    Crea [comandi personalizzati](/it/skills) per pacchettizzare flussi di lavoro ripetibili che il tuo team può condividere, come `/review-pr` o `/deploy-staging`.

    [Hooks](/it/hooks) ti permettono di eseguire comandi shell prima o dopo le azioni di Claude Code, come la formattazione automatica dopo ogni modifica di file o l'esecuzione di lint prima di un commit.
  </Accordion>

  <Accordion title="Esegui team di agenti e crea agenti personalizzati" icon="users">
    Genera [più agenti Claude Code](/it/sub-agents) che lavorano su diverse parti di un'attività contemporaneamente. Un agente principale coordina il lavoro, assegna sottoattività e unisce i risultati.

    Per flussi di lavoro completamente personalizzati, l'[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) ti permette di creare i tuoi agenti alimentati dagli strumenti e dalle capacità di Claude Code, con controllo completo sull'orchestrazione, l'accesso agli strumenti e i permessi.
  </Accordion>

  <Accordion title="Pipe, script e automatizza con il CLI" icon="terminal">
    Claude Code è componibile e segue la filosofia Unix. Pipe i log in esso, eseguilo in CI o concatenalo con altri strumenti:

    ```bash  theme={null}
    # Analizza l'output dei log recenti
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # Automatizza le traduzioni in CI
    claude -p "translate new strings into French and raise a PR for review"

    # Operazioni in blocco su file
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    Vedi il [riferimento CLI](/it/cli-reference) per l'insieme completo di comandi e flag.
  </Accordion>

  <Accordion title="Pianifica attività ricorrenti" icon="clock">
    Esegui Claude su una pianificazione per automatizzare il lavoro che si ripete: revisioni PR mattutine, analisi dei fallimenti CI durante la notte, audit delle dipendenze settimanali o sincronizzazione dei documenti dopo l'unione dei PR.

    * [Attività pianificate cloud](/it/web-scheduled-tasks) vengono eseguite su infrastruttura gestita da Anthropic, quindi continuano a funzionare anche quando il tuo computer è spento. Creale dal web, dall'app Desktop o eseguendo `/schedule` nel CLI.
    * [Attività pianificate desktop](/it/desktop#schedule-recurring-tasks) vengono eseguite sulla tua macchina, con accesso diretto ai tuoi file e strumenti locali
    * [`/loop`](/it/scheduled-tasks) ripete un prompt all'interno di una sessione CLI per il polling rapido
  </Accordion>

  <Accordion title="Lavora da qualsiasi luogo" icon="globe">
    Le sessioni non sono legate a una singola superficie. Sposta il lavoro tra gli ambienti mentre il tuo contesto cambia:

    * Allontanati dalla tua scrivania e continua a lavorare dal tuo telefono o da qualsiasi browser con [Remote Control](/it/remote-control)
    * Invia un messaggio a [Dispatch](/it/desktop#sessions-from-dispatch) con un'attività dal tuo telefono e apri la sessione Desktop che crea
    * Avvia un'attività a lunga esecuzione sul [web](/it/claude-code-on-the-web) o [app iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684), quindi trascinala nel tuo terminale con `/teleport`
    * Trasferisci una sessione di terminale all'[app Desktop](/it/desktop) con `/desktop` per la revisione visiva dei diff
    * Instrada le attività dalla chat del team: menziona `@Claude` in [Slack](/it/slack) con un rapporto di bug e ottieni una pull request in cambio
  </Accordion>
</AccordionGroup>

## Usa Claude Code ovunque

Ogni superficie si connette allo stesso motore Claude Code sottostante, quindi i tuoi file CLAUDE.md, le impostazioni e i MCP servers funzionano su tutti loro.

Oltre agli ambienti [Terminal](/it/quickstart), [VS Code](/it/vs-code), [JetBrains](/it/jetbrains), [Desktop](/it/desktop) e [Web](/it/claude-code-on-the-web) sopra, Claude Code si integra con flussi di lavoro CI/CD, chat e browser:

| Voglio...                                                                 | Opzione migliore                                                                                                             |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Continuare una sessione locale dal mio telefono o da un altro dispositivo | [Remote Control](/it/remote-control)                                                                                         |
| Inviare eventi da Telegram, Discord o i miei webhook in una sessione      | [Channels](/it/channels)                                                                                                     |
| Avviare un'attività localmente, continuare su mobile                      | [Web](/it/claude-code-on-the-web) o [app Claude iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684)            |
| Eseguire Claude su una pianificazione ricorrente                          | [Attività pianificate cloud](/it/web-scheduled-tasks) o [Attività pianificate desktop](/it/desktop#schedule-recurring-tasks) |
| Automatizzare le revisioni PR e il triage dei problemi                    | [GitHub Actions](/it/github-actions) o [GitLab CI/CD](/it/gitlab-ci-cd)                                                      |
| Ottenere revisione automatica del codice su ogni PR                       | [GitHub Code Review](/it/code-review)                                                                                        |
| Instradare i rapporti di bug da Slack alle pull request                   | [Slack](/it/slack)                                                                                                           |
| Eseguire il debug di applicazioni web live                                | [Chrome](/it/chrome)                                                                                                         |
| Creare agenti personalizzati per i tuoi flussi di lavoro                  | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                          |

## Passaggi successivi

Una volta installato Claude Code, queste guide ti aiutano ad approfondire.

* [Guida rapida](/it/quickstart): esamina il tuo primo compito reale, dall'esplorazione di una base di codice al commit di una correzione
* [Archivia istruzioni e memorie](/it/memory): dai a Claude istruzioni persistenti con file CLAUDE.md e memoria automatica
* [Flussi di lavoro comuni](/it/common-workflows) e [best practice](/it/best-practices): modelli per ottenere il massimo da Claude Code
* [Impostazioni](/it/settings): personalizza Claude Code per il tuo flusso di lavoro
* [Risoluzione dei problemi](/it/troubleshooting): soluzioni per i problemi comuni
* [code.claude.com](https://code.claude.com/): demo, prezzi e dettagli del prodotto
