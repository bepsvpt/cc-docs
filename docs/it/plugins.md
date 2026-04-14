> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Creare plugin

> Crea plugin personalizzati per estendere Claude Code con skills, agents, hooks e MCP servers.

I plugin ti permettono di estendere Claude Code con funzionalità personalizzate che possono essere condivise tra progetti e team. Questa guida copre la creazione dei tuoi plugin con skills, agents, hooks e MCP servers.

Stai cercando di installare plugin esistenti? Vedi [Scopri e installa plugin](/it/discover-plugins). Per le specifiche tecniche complete, vedi [Riferimento plugin](/it/plugins-reference).

## Quando usare plugin rispetto alla configurazione standalone

Claude Code supporta due modi per aggiungere skills, agents e hooks personalizzati:

| Approccio                                               | Nomi skill           | Migliore per                                                                                              |
| :------------------------------------------------------ | :------------------- | :-------------------------------------------------------------------------------------------------------- |
| **Standalone** (directory `.claude/`)                   | `/hello`             | Flussi di lavoro personali, personalizzazioni specifiche del progetto, esperimenti rapidi                 |
| **Plugin** (directory con `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Condivisione con i colleghi, distribuzione alla comunità, rilasci versionati, riutilizzabili tra progetti |

**Usa la configurazione standalone quando**:

* Stai personalizzando Claude Code per un singolo progetto
* La configurazione è personale e non ha bisogno di essere condivisa
* Stai sperimentando con skills o hooks prima di pacchettizzarli
* Vuoi nomi skill brevi come `/hello` o `/deploy`

**Usa i plugin quando**:

* Vuoi condividere funzionalità con il tuo team o comunità
* Hai bisogno degli stessi skills/agents in più progetti
* Vuoi il controllo della versione e aggiornamenti facili per le tue estensioni
* Stai distribuendo tramite un marketplace
* Sei d'accordo con skills con namespace come `/my-plugin:hello` (il namespace previene conflitti tra plugin)

<Tip>
  Inizia con la configurazione standalone in `.claude/` per un'iterazione rapida, poi [converti in un plugin](#convert-existing-configurations-to-plugins) quando sei pronto a condividere.
</Tip>

## Quickstart

Questo quickstart ti guida attraverso la creazione di un plugin con uno skill personalizzato. Creerai un manifest (il file di configurazione che definisce il tuo plugin), aggiungerai uno skill e lo testerai localmente usando il flag `--plugin-dir`.

### Prerequisiti

* Claude Code [installato e autenticato](/it/quickstart#step-1-install-claude-code)

<Note>
  Se non vedi il comando `/plugin`, aggiorna Claude Code all'ultima versione. Vedi [Troubleshooting](/it/troubleshooting) per le istruzioni di aggiornamento.
</Note>

### Crea il tuo primo plugin

<Steps>
  <Step title="Crea la directory del plugin">
    Ogni plugin vive nella sua directory contenente un manifest e i tuoi skills, agents o hooks. Creane uno ora:

    ```bash  theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Crea il manifest del plugin">
    Il file manifest in `.claude-plugin/plugin.json` definisce l'identità del tuo plugin: il suo nome, descrizione e versione. Claude Code usa questi metadati per visualizzare il tuo plugin nel plugin manager.

    Crea la directory `.claude-plugin` dentro la cartella del tuo plugin:

    ```bash  theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Poi crea `my-first-plugin/.claude-plugin/plugin.json` con questo contenuto:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
    "name": "my-first-plugin",
    "description": "A greeting plugin to learn the basics",
    "version": "1.0.0",
    "author": {
    "name": "Your Name"
    }
    }
    ```

    | Campo         | Scopo                                                                                                                    |
    | :------------ | :----------------------------------------------------------------------------------------------------------------------- |
    | `name`        | Identificatore univoco e namespace dello skill. Gli skill sono prefissati con questo (ad es., `/my-first-plugin:hello`). |
    | `description` | Mostrato nel plugin manager quando si sfogliano o si installano plugin.                                                  |
    | `version`     | Traccia i rilasci usando il [versionamento semantico](/it/plugins-reference#version-management).                         |
    | `author`      | Opzionale. Utile per l'attribuzione.                                                                                     |

    Per campi aggiuntivi come `homepage`, `repository` e `license`, vedi lo [schema manifest completo](/it/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Aggiungi uno skill">
    Gli skill vivono nella directory `skills/`. Ogni skill è una cartella contenente un file `SKILL.md`. Il nome della cartella diventa il nome dello skill, prefissato con il namespace del plugin (`hello/` in un plugin denominato `my-first-plugin` crea `/my-first-plugin:hello`).

    Crea una directory skill nella cartella del tuo plugin:

    ```bash  theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Poi crea `my-first-plugin/skills/hello/SKILL.md` con questo contenuto:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Testa il tuo plugin">
    Esegui Claude Code con il flag `--plugin-dir` per caricare il tuo plugin:

    ```bash  theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Una volta che Claude Code si avvia, prova il tuo nuovo skill:

    ```shell  theme={null}
    /my-first-plugin:hello
    ```

    Vedrai Claude rispondere con un saluto. Esegui `/help` per vedere il tuo skill elencato sotto il namespace del plugin.

    <Note>
      **Perché il namespace?** Gli skill del plugin hanno sempre il namespace (come `/my-first-plugin:hello`) per prevenire conflitti quando più plugin hanno skill con lo stesso nome.

      Per cambiare il prefisso del namespace, aggiorna il campo `name` in `plugin.json`.
    </Note>
  </Step>

  <Step title="Aggiungi argomenti dello skill">
    Rendi il tuo skill dinamico accettando input dell'utente. Il placeholder `$ARGUMENTS` cattura qualsiasi testo che l'utente fornisce dopo il nome dello skill.

    Aggiorna il tuo file `SKILL.md`:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Esegui `/reload-plugins` per raccogliere i cambiamenti, poi prova lo skill con il tuo nome:

    ```shell  theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude ti saluterà per nome. Per ulteriori informazioni sul passaggio di argomenti agli skill, vedi [Skills](/it/skills#pass-arguments-to-skills).
  </Step>
</Steps>

Hai creato e testato con successo un plugin con questi componenti chiave:

* **Plugin manifest** (`.claude-plugin/plugin.json`): descrive i metadati del tuo plugin
* **Directory skills** (`skills/`): contiene i tuoi skill personalizzati
* **Argomenti dello skill** (`$ARGUMENTS`): cattura l'input dell'utente per il comportamento dinamico

<Tip>
  Il flag `--plugin-dir` è utile per lo sviluppo e il test. Quando sei pronto a condividere il tuo plugin con altri, vedi [Crea e distribuisci un marketplace di plugin](/it/plugin-marketplaces).
</Tip>

## Panoramica della struttura del plugin

Hai creato un plugin con uno skill, ma i plugin possono includere molto di più: agents personalizzati, hooks, MCP servers e LSP servers.

<Warning>
  **Errore comune**: Non mettere `commands/`, `agents/`, `skills/` o `hooks/` dentro la directory `.claude-plugin/`. Solo `plugin.json` va dentro `.claude-plugin/`. Tutte le altre directory devono essere al livello radice del plugin.
</Warning>

| Directory         | Posizione         | Scopo                                                                                      |
| :---------------- | :---------------- | :----------------------------------------------------------------------------------------- |
| `.claude-plugin/` | Radice del plugin | Contiene il manifest `plugin.json` (opzionale se i componenti usano posizioni predefinite) |
| `commands/`       | Radice del plugin | Skills come file Markdown                                                                  |
| `agents/`         | Radice del plugin | Definizioni di agent personalizzati                                                        |
| `skills/`         | Radice del plugin | Agent Skills con file `SKILL.md`                                                           |
| `hooks/`          | Radice del plugin | Gestori di eventi in `hooks.json`                                                          |
| `.mcp.json`       | Radice del plugin | Configurazioni del server MCP                                                              |
| `.lsp.json`       | Radice del plugin | Configurazioni del server LSP per l'intelligenza del codice                                |
| `settings.json`   | Radice del plugin | [Impostazioni](/it/settings) predefinite applicate quando il plugin è abilitato            |

<Note>
  **Prossimi passi**: Pronto ad aggiungere più funzionalità? Vai a [Sviluppa plugin più complessi](#develop-more-complex-plugins) per aggiungere agents, hooks, MCP servers e LSP servers. Per le specifiche tecniche complete di tutti i componenti del plugin, vedi [Riferimento plugin](/it/plugins-reference).
</Note>

## Sviluppa plugin più complessi

Una volta che hai familiarità con i plugin di base, puoi creare estensioni più sofisticate.

### Aggiungi Skills al tuo plugin

I plugin possono includere [Agent Skills](/it/skills) per estendere le capacità di Claude. Gli skill sono invocati dal modello: Claude li usa automaticamente in base al contesto dell'attività.

Aggiungi una directory `skills/` alla radice del tuo plugin con cartelle Skill contenenti file `SKILL.md`:

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Ogni `SKILL.md` ha bisogno di frontmatter con campi `name` e `description`, seguiti da istruzioni:

```yaml  theme={null}
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Dopo aver installato il plugin, esegui `/reload-plugins` per caricare gli Skills. Per una guida completa sulla creazione di Skill inclusa la divulgazione progressiva e le restrizioni degli strumenti, vedi [Agent Skills](/it/skills).

### Aggiungi server LSP al tuo plugin

<Tip>
  Per linguaggi comuni come TypeScript, Python e Rust, installa i plugin LSP pre-costruiti dal marketplace ufficiale. Crea plugin LSP personalizzati solo quando hai bisogno di supporto per linguaggi non ancora coperti.
</Tip>

I plugin LSP (Language Server Protocol) danno a Claude l'intelligenza del codice in tempo reale. Se hai bisogno di supportare un linguaggio che non ha un plugin LSP ufficiale, puoi crearne uno tuo aggiungendo un file `.lsp.json` al tuo plugin:

```json .lsp.json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Gli utenti che installano il tuo plugin devono avere il binario del language server installato sulla loro macchina.

Per le opzioni di configurazione LSP complete, vedi [LSP servers](/it/plugins-reference#lsp-servers).

### Spedisci impostazioni predefinite con il tuo plugin

I plugin possono includere un file `settings.json` alla radice del plugin per applicare la configurazione predefinita quando il plugin è abilitato. Attualmente, è supportata solo la chiave `agent`.

Impostare `agent` attiva uno dei [custom agents](/it/sub-agents) del plugin come thread principale, applicando il suo system prompt, le restrizioni degli strumenti e il modello. Questo consente a un plugin di cambiare il comportamento predefinito di Claude Code quando abilitato.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Questo esempio attiva l'agent `security-reviewer` definito nella directory `agents/` del plugin. Le impostazioni da `settings.json` hanno priorità rispetto alle `settings` dichiarate in `plugin.json`. Le chiavi sconosciute vengono silenziosamente ignorate.

### Organizza plugin complessi

Per i plugin con molti componenti, organizza la tua struttura di directory per funzionalità. Per i layout di directory completi e i modelli di organizzazione, vedi [Struttura della directory del plugin](/it/plugins-reference#plugin-directory-structure).

### Testa i tuoi plugin localmente

Usa il flag `--plugin-dir` per testare i plugin durante lo sviluppo. Questo carica il tuo plugin direttamente senza richiedere l'installazione.

```bash  theme={null}
claude --plugin-dir ./my-plugin
```

Quando un plugin `--plugin-dir` ha lo stesso nome di un plugin marketplace installato, la copia locale ha la precedenza per quella sessione. Questo ti consente di testare le modifiche a un plugin che hai già installato senza disinstallarlo prima. I plugin marketplace forzatamente abilitati dalle impostazioni gestite sono l'unica eccezione e non possono essere sovrascritti.

Man mano che apporti modifiche al tuo plugin, esegui `/reload-plugins` per raccogliere gli aggiornamenti senza riavviare. Questo ricarica plugin, skills, agents, hooks, MCP servers del plugin e LSP servers del plugin. Testa i componenti del tuo plugin:

* Prova i tuoi skill con `/plugin-name:skill-name`
* Verifica che gli agents appaiano in `/agents`
* Verifica che gli hooks funzionino come previsto

<Tip>
  Puoi caricare più plugin contemporaneamente specificando il flag più volte:

  ```bash  theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Esegui il debug dei problemi del plugin

Se il tuo plugin non funziona come previsto:

1. **Controlla la struttura**: Assicurati che le tue directory siano alla radice del plugin, non dentro `.claude-plugin/`
2. **Testa i componenti individualmente**: Controlla ogni comando, agent e hook separatamente
3. **Usa strumenti di validazione e debug**: Vedi [Strumenti di debug e sviluppo](/it/plugins-reference#debugging-and-development-tools) per i comandi CLI e le tecniche di troubleshooting

### Condividi i tuoi plugin

Quando il tuo plugin è pronto per essere condiviso:

1. **Aggiungi documentazione**: Includi un `README.md` con istruzioni di installazione e utilizzo
2. **Versiona il tuo plugin**: Usa il [versionamento semantico](/it/plugins-reference#version-management) nel tuo `plugin.json`
3. **Crea o usa un marketplace**: Distribuisci tramite [marketplace di plugin](/it/plugin-marketplaces) per l'installazione
4. **Testa con altri**: Fai testare il plugin ai colleghi del team prima di una distribuzione più ampia

Una volta che il tuo plugin è in un marketplace, altri possono installarlo usando le istruzioni in [Scopri e installa plugin](/it/discover-plugins).

### Invia il tuo plugin al marketplace ufficiale

Per inviare un plugin al marketplace ufficiale di Anthropic, usa uno dei moduli di invio in-app:

* **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

<Note>
  Per le specifiche tecniche complete, le tecniche di debug e le strategie di distribuzione, vedi [Riferimento plugin](/it/plugins-reference).
</Note>

## Converti configurazioni esistenti in plugin

Se hai già skill o hooks nella tua directory `.claude/`, puoi convertirli in un plugin per una condivisione e distribuzione più facile.

### Passaggi di migrazione

<Steps>
  <Step title="Crea la struttura del plugin">
    Crea una nuova directory plugin:

    ```bash  theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Crea il file manifest in `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Copia i tuoi file esistenti">
    Copia le tue configurazioni esistenti nella directory del plugin:

    ```bash  theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Migra gli hook">
    Se hai hook nelle tue impostazioni, crea una directory hooks:

    ```bash  theme={null}
    mkdir my-plugin/hooks
    ```

    Crea `my-plugin/hooks/hooks.json` con la tua configurazione degli hook. Copia l'oggetto `hooks` dal tuo `.claude/settings.json` o `settings.local.json`, poiché il formato è lo stesso. Il comando riceve l'input dell'hook come JSON su stdin, quindi usa `jq` per estrarre il percorso del file:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Testa il tuo plugin migrato">
    Carica il tuo plugin per verificare che tutto funzioni:

    ```bash  theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Testa ogni componente: esegui i tuoi comandi, verifica che gli agents appaiano in `/agents` e verifica che gli hook si attivino correttamente.
  </Step>
</Steps>

### Cosa cambia durante la migrazione

| Standalone (`.claude/`)                         | Plugin                                   |
| :---------------------------------------------- | :--------------------------------------- |
| Disponibile solo in un progetto                 | Può essere condiviso tramite marketplace |
| File in `.claude/commands/`                     | File in `plugin-name/commands/`          |
| Hook in `settings.json`                         | Hook in `hooks/hooks.json`               |
| Deve essere copiato manualmente per condividere | Installa con `/plugin install`           |

<Note>
  Dopo la migrazione, puoi rimuovere i file originali da `.claude/` per evitare duplicati. La versione del plugin avrà la precedenza quando caricata.
</Note>

## Prossimi passi

Ora che comprendi il sistema di plugin di Claude Code, ecco i percorsi suggeriti per diversi obiettivi:

### Per gli utenti di plugin

* [Scopri e installa plugin](/it/discover-plugins): sfoglia i marketplace e installa i plugin
* [Configura marketplace del team](/it/discover-plugins#configure-team-marketplaces): configura plugin a livello di repository per il tuo team

### Per gli sviluppatori di plugin

* [Crea e distribuisci un marketplace](/it/plugin-marketplaces): pacchetto e condividi i tuoi plugin
* [Riferimento plugin](/it/plugins-reference): specifiche tecniche complete
* Approfondisci componenti specifici del plugin:
  * [Skills](/it/skills): dettagli dello sviluppo dello skill
  * [Subagents](/it/sub-agents): configurazione e capacità dell'agent
  * [Hooks](/it/hooks): gestione degli eventi e automazione
  * [MCP](/it/mcp): integrazione di strumenti esterni
