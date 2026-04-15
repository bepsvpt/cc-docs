> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Creare e distribuire un marketplace di plugin

> Crea e ospita marketplace di plugin per distribuire estensioni Claude Code tra team e comunità.

Un **plugin marketplace** è un catalogo che ti consente di distribuire plugin ad altri. I marketplace forniscono scoperta centralizzata, tracciamento delle versioni, aggiornamenti automatici e supporto per più tipi di fonte (repository git, percorsi locali e altro). Questa guida ti mostra come creare il tuo marketplace per condividere plugin con il tuo team o comunità.

Stai cercando di installare plugin da un marketplace esistente? Vedi [Scopri e installa plugin precostruiti](/it/discover-plugins).

## Panoramica

La creazione e la distribuzione di un marketplace comporta:

1. **Creazione di plugin**: crea uno o più plugin con comandi, agenti, hooks, MCP servers o LSP servers. Questa guida presuppone che tu abbia già plugin da distribuire; vedi [Crea plugin](/it/plugins) per i dettagli su come crearli.
2. **Creazione di un file marketplace**: definisci un `marketplace.json` che elenca i tuoi plugin e dove trovarli (vedi [Crea il file marketplace](#create-the-marketplace-file)).
3. **Ospita il marketplace**: esegui il push su GitHub, GitLab o un altro host git (vedi [Ospita e distribuisci marketplace](#host-and-distribute-marketplaces)).
4. **Condividi con gli utenti**: gli utenti aggiungono il tuo marketplace con `/plugin marketplace add` e installano singoli plugin (vedi [Scopri e installa plugin](/it/discover-plugins)).

Una volta che il tuo marketplace è attivo, puoi aggiornarlo eseguendo il push delle modifiche al tuo repository. Gli utenti aggiornano la loro copia locale con `/plugin marketplace update`.

## Procedura dettagliata: creare un marketplace locale

Questo esempio crea un marketplace con un plugin: una skill `/quality-review` per le revisioni del codice. Creerai la struttura delle directory, aggiungerai una skill, creerai il manifest del plugin e il catalogo del marketplace, quindi lo installerai e lo testerai.

<Steps>
  <Step title="Crea la struttura delle directory">
    ```bash theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Crea la skill">
    Crea un file `SKILL.md` che definisce cosa fa la skill `/quality-review`.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Rivedi il codice per bug, sicurezza e prestazioni
    disable-model-invocation: true
    ---

    Rivedi il codice che ho selezionato o i cambiamenti recenti per:
    - Potenziali bug o casi limite
    - Problemi di sicurezza
    - Problemi di prestazioni
    - Miglioramenti di leggibilità

    Sii conciso e pratico.
    ```
  </Step>

  <Step title="Crea il manifest del plugin">
    Crea un file `plugin.json` che descrive il plugin. Il manifest va nella directory `.claude-plugin/`.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Aggiunge una skill /quality-review per revisioni rapide del codice",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Crea il file marketplace">
    Crea il catalogo marketplace che elenca il tuo plugin.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Aggiunge una skill /quality-review per revisioni rapide del codice"
        }
      ]
    }
    ```
  </Step>

  <Step title="Aggiungi e installa">
    Aggiungi il marketplace e installa il plugin.

    ```shell theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Provalo">
    Seleziona del codice nel tuo editor ed esegui il tuo nuovo comando.

    ```shell theme={null}
    /quality-review
    ```
  </Step>
</Steps>

Per saperne di più su cosa possono fare i plugin, inclusi hooks, agenti, MCP servers e LSP servers, vedi [Plugin](/it/plugins).

<Note>
  **Come vengono installati i plugin**: Quando gli utenti installano un plugin, Claude Code copia la directory del plugin in una posizione cache. Ciò significa che i plugin non possono fare riferimento a file al di fuori della loro directory utilizzando percorsi come `../shared-utils`, perché quei file non verranno copiati.

  Se hai bisogno di condividere file tra plugin, usa symlink (che vengono seguiti durante la copia). Vedi [Plugin caching and file resolution](/it/plugins-reference#plugin-caching-and-file-resolution) per i dettagli.
</Note>

## Crea il file marketplace

Crea `.claude-plugin/marketplace.json` nella radice del tuo repository. Questo file definisce il nome del tuo marketplace, le informazioni del proprietario e un elenco di plugin con le loro fonti.

Ogni voce di plugin ha bisogno almeno di un `name` e di una `source` (da dove recuperarla). Vedi lo [schema completo](#marketplace-schema) di seguito per tutti i campi disponibili.

```json theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Formattazione automatica del codice al salvataggio",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Strumenti di automazione della distribuzione"
    }
  ]
}
```

## Schema del marketplace

### Campi obbligatori

| Campo     | Tipo   | Descrizione                                                                                                                                                                          | Esempio         |
| :-------- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| `name`    | string | Identificatore del marketplace (kebab-case, senza spazi). Questo è pubblico: gli utenti lo vedono quando installano plugin (ad esempio, `/plugin install my-tool@your-marketplace`). | `"acme-tools"`  |
| `owner`   | object | Informazioni sul manutentore del marketplace ([vedi i campi di seguito](#owner-fields))                                                                                              |                 |
| `plugins` | array  | Elenco dei plugin disponibili                                                                                                                                                        | Vedi di seguito |

<Note>
  **Nomi riservati**: I seguenti nomi di marketplace sono riservati per uso ufficiale di Anthropic e non possono essere utilizzati da marketplace di terze parti: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Anche i nomi che impersonano marketplace ufficiali (come `official-claude-plugins` o `anthropic-tools-v2`) sono bloccati.
</Note>

### Campi del proprietario

| Campo   | Tipo   | Obbligatorio | Descrizione                          |
| :------ | :----- | :----------- | :----------------------------------- |
| `name`  | string | Sì           | Nome del manutentore o del team      |
| `email` | string | No           | Email di contatto per il manutentore |

### Metadati opzionali

| Campo                  | Tipo   | Descrizione                                                                                                                                                                                  |
| :--------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | Breve descrizione del marketplace                                                                                                                                                            |
| `metadata.version`     | string | Versione del marketplace                                                                                                                                                                     |
| `metadata.pluginRoot`  | string | Directory di base anteposta ai percorsi di fonte del plugin relativo (ad esempio, `"./plugins"` ti consente di scrivere `"source": "formatter"` invece di `"source": "./plugins/formatter"`) |

## Voci di plugin

Ogni voce di plugin nell'array `plugins` descrive un plugin e dove trovarlo. Puoi includere qualsiasi campo dallo [schema del manifest del plugin](/it/plugins-reference#plugin-manifest-schema) (come `description`, `version`, `author`, `commands`, `hooks`, ecc.), più questi campi specifici del marketplace: `source`, `category`, `tags` e `strict`.

### Campi obbligatori

| Campo    | Tipo           | Descrizione                                                                                                                                                           |
| :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Identificatore del plugin (kebab-case, senza spazi). Questo è pubblico: gli utenti lo vedono quando installano (ad esempio, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Da dove recuperare il plugin (vedi [Plugin sources](#plugin-sources) di seguito)                                                                                      |

### Campi di plugin opzionali

**Campi di metadati standard:**

| Campo         | Tipo    | Descrizione                                                                                                                                 |
| :------------ | :------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `description` | string  | Breve descrizione del plugin                                                                                                                |
| `version`     | string  | Versione del plugin                                                                                                                         |
| `author`      | object  | Informazioni sull'autore del plugin (`name` obbligatorio, `email` opzionale)                                                                |
| `homepage`    | string  | URL della homepage o della documentazione del plugin                                                                                        |
| `repository`  | string  | URL del repository del codice sorgente                                                                                                      |
| `license`     | string  | Identificatore di licenza SPDX (ad esempio, MIT, Apache-2.0)                                                                                |
| `keywords`    | array   | Tag per la scoperta e la categorizzazione dei plugin                                                                                        |
| `category`    | string  | Categoria del plugin per l'organizzazione                                                                                                   |
| `tags`        | array   | Tag per la ricercabilità                                                                                                                    |
| `strict`      | boolean | Controlla se `plugin.json` è l'autorità per le definizioni dei componenti (predefinito: true). Vedi [Strict mode](#strict-mode) di seguito. |

**Campi di configurazione dei componenti:**

| Campo        | Tipo           | Descrizione                                                            |
| :----------- | :------------- | :--------------------------------------------------------------------- |
| `commands`   | string\|array  | Percorsi personalizzati ai file o alle directory dei comandi           |
| `agents`     | string\|array  | Percorsi personalizzati ai file degli agenti                           |
| `hooks`      | string\|object | Configurazione degli hook personalizzati o percorso al file degli hook |
| `mcpServers` | string\|object | Configurazioni del server MCP o percorso alla configurazione MCP       |
| `lspServers` | string\|object | Configurazioni del server LSP o percorso alla configurazione LSP       |

## Plugin sources

Le plugin sources indicano a Claude Code dove recuperare ogni singolo plugin elencato nel tuo marketplace. Questi sono impostati nel campo `source` di ogni voce di plugin in `marketplace.json`.

Una volta che un plugin viene clonato o copiato nella macchina locale, viene copiato nella cache del plugin locale con versione in `~/.claude/plugins/cache`.

| Source            | Tipo                              | Campi                              | Note                                                                                                                             |
| ----------------- | --------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Percorso relativo | `string` (ad es. `"./my-plugin"`) | nessuno                            | Directory locale all'interno del repository del marketplace. Deve iniziare con `./`                                              |
| `github`          | object                            | `repo`, `ref?`, `sha?`             |                                                                                                                                  |
| `url`             | object                            | `url`, `ref?`, `sha?`              | Fonte URL Git                                                                                                                    |
| `git-subdir`      | object                            | `url`, `path`, `ref?`, `sha?`      | Sottodirectory all'interno di un repository git. Clona in modo sparso per ridurre al minimo la larghezza di banda per i monorepo |
| `npm`             | object                            | `package`, `version?`, `registry?` | Installato tramite `npm install`                                                                                                 |

<Note>
  **Marketplace sources vs plugin sources**: Questi sono concetti diversi che controllano cose diverse.

  * **Marketplace source** — dove recuperare il catalogo `marketplace.json` stesso. Impostato quando gli utenti eseguono `/plugin marketplace add` o nelle impostazioni `extraKnownMarketplaces`. Supporta `ref` (branch/tag) ma non `sha`.
  * **Plugin source** — dove recuperare un singolo plugin elencato nel marketplace. Impostato nel campo `source` di ogni voce di plugin all'interno di `marketplace.json`. Supporta sia `ref` (branch/tag) che `sha` (commit esatto).

  Ad esempio, un marketplace ospitato in `acme-corp/plugin-catalog` (marketplace source) può elencare un plugin recuperato da `acme-corp/code-formatter` (plugin source). La marketplace source e la plugin source puntano a repository diversi e sono fissate indipendentemente.
</Note>

### Percorsi relativi

Per i plugin nello stesso repository, usa un percorso che inizia con `./`:

```json theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

I percorsi si risolvono relativamente alla radice del marketplace, che è la directory contenente `.claude-plugin/`. Nell'esempio sopra, `./plugins/my-plugin` punta a `<repo>/plugins/my-plugin`, anche se `marketplace.json` si trova in `<repo>/.claude-plugin/marketplace.json`. Non usare `../` per uscire da `.claude-plugin/`.

<Note>
  I percorsi relativi funzionano solo quando gli utenti aggiungono il tuo marketplace tramite Git (GitHub, GitLab o URL git). Se gli utenti aggiungono il tuo marketplace tramite un URL diretto al file `marketplace.json`, i percorsi relativi non si risolveranno correttamente. Per la distribuzione basata su URL, usa invece GitHub, npm o fonti URL git. Vedi [Troubleshooting](#plugins-with-relative-paths-fail-in-url-based-marketplaces) per i dettagli.
</Note>

### Repository GitHub

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Puoi fissare a un branch, tag o commit specifico:

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Campo  | Tipo   | Descrizione                                                                             |
| :----- | :----- | :-------------------------------------------------------------------------------------- |
| `repo` | string | Obbligatorio. Repository GitHub nel formato `owner/repo`                                |
| `ref`  | string | Opzionale. Branch o tag Git (predefinito al branch predefinito del repository)          |
| `sha`  | string | Opzionale. SHA del commit git completo a 40 caratteri per fissare a una versione esatta |

### Repository Git

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Puoi fissare a un branch, tag o commit specifico:

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Campo | Tipo   | Descrizione                                                                                                                                                                       |
| :---- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Obbligatorio. URL completo del repository git (`https://` o `git@`). Il suffisso `.git` è opzionale, quindi gli URL di Azure DevOps e AWS CodeCommit senza il suffisso funzionano |
| `ref` | string | Opzionale. Branch o tag Git (predefinito al branch predefinito del repository)                                                                                                    |
| `sha` | string | Opzionale. SHA del commit git completo a 40 caratteri per fissare a una versione esatta                                                                                           |

### Sottodirectory Git

Usa `git-subdir` per puntare a un plugin che si trova all'interno di una sottodirectory di un repository git. Claude Code utilizza un clone parziale e sparso per recuperare solo la sottodirectory, riducendo al minimo la larghezza di banda per i grandi monorepo.

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Puoi fissare a un branch, tag o commit specifico:

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

Il campo `url` accetta anche una scorciatoia GitHub (`owner/repo`) o URL SSH (`git@github.com:owner/repo.git`).

| Campo  | Tipo   | Descrizione                                                                                                                 |
| :----- | :----- | :-------------------------------------------------------------------------------------------------------------------------- |
| `url`  | string | Obbligatorio. URL del repository Git, scorciatoia GitHub `owner/repo` o URL SSH                                             |
| `path` | string | Obbligatorio. Percorso della sottodirectory all'interno del repo contenente il plugin (ad esempio, `"tools/claude-plugin"`) |
| `ref`  | string | Opzionale. Branch o tag Git (predefinito al branch predefinito del repository)                                              |
| `sha`  | string | Opzionale. SHA del commit git completo a 40 caratteri per fissare a una versione esatta                                     |

### Pacchetti npm

I plugin distribuiti come pacchetti npm vengono installati utilizzando `npm install`. Questo funziona con qualsiasi pacchetto nel registro npm pubblico o in un registro privato ospitato dal tuo team.

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Per fissare a una versione specifica, aggiungi il campo `version`:

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Per installare da un registro privato o interno, aggiungi il campo `registry`:

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Campo      | Tipo   | Descrizione                                                                                                     |
| :--------- | :----- | :-------------------------------------------------------------------------------------------------------------- |
| `package`  | string | Obbligatorio. Nome del pacchetto o pacchetto con scope (ad esempio, `@org/plugin`)                              |
| `version`  | string | Opzionale. Versione o intervallo di versione (ad esempio, `2.1.0`, `^2.0.0`, `~1.5.0`)                          |
| `registry` | string | Opzionale. URL del registro npm personalizzato. Predefinito al registro npm del sistema (tipicamente npmjs.org) |

### Voci di plugin avanzate

Questo esempio mostra una voce di plugin che utilizza molti dei campi opzionali, inclusi percorsi personalizzati per comandi, agenti, hooks e server MCP:

```json theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Strumenti di automazione del flusso di lavoro aziendale",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Cose importanti da notare:

* **`commands` e `agents`**: Puoi specificare più directory o singoli file. I percorsi sono relativi alla radice del plugin.
* **`${CLAUDE_PLUGIN_ROOT}`**: Usa questa variabile nelle configurazioni degli hook e del server MCP per fare riferimento ai file all'interno della directory di installazione del plugin. Questo è necessario perché i plugin vengono copiati in una posizione cache quando installati. Per le dipendenze o lo stato che dovrebbe sopravvivere agli aggiornamenti dei plugin, usa [`${CLAUDE_PLUGIN_DATA}`](/it/plugins-reference#persistent-data-directory) invece.
* **`strict: false`**: Poiché è impostato su false, il plugin non ha bisogno del suo `plugin.json`. La voce del marketplace definisce tutto. Vedi [Strict mode](#strict-mode) di seguito.

### Strict mode

Il campo `strict` controlla se `plugin.json` è l'autorità per le definizioni dei componenti (comandi, agenti, hooks, skill, server MCP, stili di output).

| Valore               | Comportamento                                                                                                                                                         |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (predefinito) | `plugin.json` è l'autorità. La voce del marketplace può integrarla con componenti aggiuntivi e entrambe le fonti vengono unite.                                       |
| `false`              | La voce del marketplace è la definizione completa. Se il plugin ha anche un `plugin.json` che dichiara componenti, è un conflitto e il plugin non riesce a caricarsi. |

**Quando usare ogni modalità:**

* **`strict: true`**: il plugin ha il suo `plugin.json` e gestisce i suoi componenti. La voce del marketplace può aggiungere comandi o hook extra in cima. Questo è il predefinito e funziona per la maggior parte dei plugin.
* **`strict: false`**: l'operatore del marketplace vuole il controllo completo. Il repository del plugin fornisce file grezzi e la voce del marketplace definisce quali di questi file sono esposti come comandi, agenti, hook, ecc. Utile quando il marketplace ristruttura o cura i componenti di un plugin diversamente da quanto previsto dall'autore del plugin.

## Ospita e distribuisci marketplace

### Ospita su GitHub (consigliato)

GitHub fornisce il metodo di distribuzione più semplice:

1. **Crea un repository**: Configura un nuovo repository per il tuo marketplace
2. **Aggiungi il file marketplace**: Crea `.claude-plugin/marketplace.json` con le tue definizioni di plugin
3. **Condividi con i team**: Gli utenti aggiungono il tuo marketplace con `/plugin marketplace add owner/repo`

**Vantaggi**: Controllo della versione integrato, tracciamento dei problemi e funzionalità di collaborazione del team.

### Ospita su altri servizi git

Qualsiasi servizio di hosting git funziona, come GitLab, Bitbucket e server self-hosted. Gli utenti aggiungono con l'URL completo del repository:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Repository privati

Claude Code supporta l'installazione di plugin da repository privati. Per l'installazione manuale e gli aggiornamenti, Claude Code utilizza i tuoi helper di credenziali git esistenti. Se `git clone` funziona per un repository privato nel tuo terminale, funziona anche in Claude Code. Gli helper di credenziali comuni includono `gh auth login` per GitHub, Keychain di macOS e `git-credential-store`.

Gli aggiornamenti automatici in background vengono eseguiti all'avvio senza helper di credenziali, poiché i prompt interattivi bloccherebbero l'avvio di Claude Code. Per abilitare gli aggiornamenti automatici per i marketplace privati, imposta il token di autenticazione appropriato nel tuo ambiente:

| Provider  | Variabili di ambiente       | Note                                               |
| :-------- | :-------------------------- | :------------------------------------------------- |
| GitHub    | `GITHUB_TOKEN` o `GH_TOKEN` | Token di accesso personale o token di GitHub App   |
| GitLab    | `GITLAB_TOKEN` o `GL_TOKEN` | Token di accesso personale o token di progetto     |
| Bitbucket | `BITBUCKET_TOKEN`           | Password dell'app o token di accesso al repository |

Imposta il token nella configurazione della tua shell (ad esempio, `.bashrc`, `.zshrc`) o passalo quando esegui Claude Code:

```bash theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Per gli ambienti CI/CD, configura il token come variabile di ambiente segreta. GitHub Actions fornisce automaticamente `GITHUB_TOKEN` per i repository nella stessa organizzazione.
</Note>

### Testa localmente prima della distribuzione

Testa il tuo marketplace localmente prima di condividerlo:

```shell theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Per l'intera gamma di comandi add (GitHub, URL Git, percorsi locali, URL remoti), vedi [Aggiungi marketplace](/it/discover-plugins#add-marketplaces).

### Richiedi marketplace per il tuo team

Puoi configurare il tuo repository in modo che i membri del team vengano automaticamente invitati a installare il tuo marketplace quando fidano della cartella del progetto. Aggiungi il tuo marketplace a `.claude/settings.json`:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Puoi anche specificare quali plugin devono essere abilitati per impostazione predefinita:

```json theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Per le opzioni di configurazione complete, vedi [Plugin settings](/it/settings#plugin-settings).

<Note>
  Se usi una fonte locale `directory` o `file` con un percorso relativo, il percorso si risolve rispetto al checkout principale del tuo repository. Quando esegui Claude Code da un git worktree, il percorso punta ancora al checkout principale, quindi tutti i worktree condividono la stessa posizione del marketplace. Lo stato del marketplace viene archiviato una volta per utente in `~/.claude/plugins/known_marketplaces.json`, non per progetto.
</Note>

### Pre-popola plugin per i container

Per le immagini container e gli ambienti CI, puoi pre-popolare una directory di plugin al momento della compilazione in modo che Claude Code si avvii con marketplace e plugin già disponibili, senza clonare nulla al runtime. Imposta la variabile di ambiente `CLAUDE_CODE_PLUGIN_SEED_DIR` per puntare a questa directory.

Per stratificare più directory seed, separa i percorsi con `:` su Unix o `;` su Windows. Claude Code cerca ogni directory in ordine e il primo seed che contiene un determinato marketplace o cache di plugin vince.

La directory seed rispecchia la struttura di `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

Il modo più semplice per costruire una directory seed è eseguire Claude Code una volta durante la compilazione dell'immagine, installare i plugin di cui hai bisogno, quindi copiare la directory `~/.claude/plugins` risultante nella tua immagine e puntare `CLAUDE_CODE_PLUGIN_SEED_DIR` ad essa.

All'avvio, Claude Code registra i marketplace trovati nel `known_marketplaces.json` del seed nella configurazione primaria e utilizza le cache dei plugin trovate sotto `cache/` al posto senza ri-clonare. Questo funziona sia in modalità interattiva che in modalità non interattiva con il flag `-p`.

Dettagli del comportamento:

* **Sola lettura**: la directory seed non viene mai scritta. Gli aggiornamenti automatici sono disabilitati per i marketplace seed poiché git pull fallirebbe su un filesystem di sola lettura.
* **Le voci seed hanno precedenza**: i marketplace dichiarati nel seed sovrascrivono qualsiasi voce corrispondente nella configurazione dell'utente ad ogni avvio. Per rinunciare a un plugin seed, usa `/plugin disable` piuttosto che rimuovere il marketplace.
* **Risoluzione del percorso**: Claude Code individua il contenuto del marketplace sondando `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` al runtime, non fidandosi dei percorsi archiviati all'interno del JSON del seed. Ciò significa che il seed funziona correttamente anche quando montato in un percorso diverso da dove è stato compilato.
* **Compone con le impostazioni**: se `extraKnownMarketplaces` o `enabledPlugins` dichiarano un marketplace che esiste già nel seed, Claude Code utilizza la copia del seed invece di clonare.

### Restrizioni del marketplace gestito

Per le organizzazioni che richiedono un controllo rigoroso sulle fonti dei plugin, gli amministratori possono limitare quali marketplace di plugin gli utenti possono aggiungere utilizzando l'impostazione [`strictKnownMarketplaces`](/it/settings#strictknownmarketplaces) nelle impostazioni gestite.

Quando `strictKnownMarketplaces` è configurato nelle impostazioni gestite, il comportamento della restrizione dipende dal valore:

| Valore                     | Comportamento                                                                                             |
| -------------------------- | --------------------------------------------------------------------------------------------------------- |
| Non definito (predefinito) | Nessuna restrizione. Gli utenti possono aggiungere qualsiasi marketplace                                  |
| Array vuoto `[]`           | Blocco completo. Gli utenti non possono aggiungere nuovi marketplace                                      |
| Elenco di fonti            | Gli utenti possono aggiungere solo marketplace che corrispondono esattamente all'elenco di autorizzazione |

#### Configurazioni comuni

Disabilita tutti gli aggiunte di marketplace:

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Consenti solo marketplace specifici:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Consenti tutti i marketplace da un server git interno utilizzando la corrispondenza del modello regex sull'host. Questo è l'approccio consigliato per [GitHub Enterprise Server](/it/github-enterprise-server#plugin-marketplaces-on-ghes) o istanze GitLab self-hosted:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Consenti marketplace basati su filesystem da una directory specifica utilizzando la corrispondenza del modello regex sul percorso:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Usa `".*"` come `pathPattern` per consentire qualsiasi percorso del filesystem controllando comunque le fonti di rete con `hostPattern`.

<Note>
  `strictKnownMarketplaces` limita ciò che gli utenti possono aggiungere, ma non registra i marketplace di per sé. Per rendere i marketplace consentiti disponibili automaticamente senza che gli utenti eseguano `/plugin marketplace add`, abbinalo a [`extraKnownMarketplaces`](/it/settings#extraknownmarketplaces) nello stesso `managed-settings.json`. Vedi [Usare entrambi insieme](/it/settings#strictknownmarketplaces).
</Note>

#### Come funzionano le restrizioni

Le restrizioni vengono convalidate all'inizio del processo di installazione del plugin, prima di qualsiasi richiesta di rete o operazione del filesystem. Ciò impedisce i tentativi di accesso non autorizzato al marketplace.

L'elenco di autorizzazione utilizza la corrispondenza esatta per la maggior parte dei tipi di fonte. Affinché un marketplace sia consentito, tutti i campi specificati devono corrispondere esattamente:

* Per le fonti GitHub: `repo` è obbligatorio e `ref` o `path` devono corrispondere anche se specificati nell'elenco di autorizzazione
* Per le fonti URL: l'URL completo deve corrispondere esattamente
* Per le fonti `hostPattern`: l'host del marketplace viene confrontato con il modello regex
* Per le fonti `pathPattern`: il percorso del filesystem del marketplace viene confrontato con il modello regex

Poiché `strictKnownMarketplaces` è impostato nelle [impostazioni gestite](/it/settings#settings-files), le configurazioni individuali degli utenti e dei progetti non possono ignorare queste restrizioni.

Per i dettagli di configurazione completi inclusi tutti i tipi di fonte supportati e il confronto con `extraKnownMarketplaces`, vedi il [riferimento strictKnownMarketplaces](/it/settings#strictknownmarketplaces).

### Risoluzione della versione e canali di rilascio

Le versioni dei plugin determinano i percorsi della cache e il rilevamento degli aggiornamenti. Puoi specificare la versione nel manifest del plugin (`plugin.json`) o nella voce del marketplace (`marketplace.json`).

<Warning>
  Quando possibile, evita di impostare la versione in entrambi i posti. Il manifest del plugin vince sempre silenziosamente, il che può causare l'ignoranza della versione del marketplace. Per i plugin con percorso relativo, imposta la versione nella voce del marketplace. Per tutte le altre fonti di plugin, impostala nel manifest del plugin.
</Warning>

#### Configura i canali di rilascio

Per supportare i canali di rilascio "stable" e "latest" per i tuoi plugin, puoi configurare due marketplace che puntano a diversi ref o SHA dello stesso repo. Puoi quindi assegnare i due marketplace a diversi gruppi di utenti tramite [impostazioni gestite](/it/settings#settings-files).

<Warning>
  Il `plugin.json` del plugin deve dichiarare una `version` diversa in ogni ref o commit fissato. Se due ref o commit hanno la stessa versione del manifest, Claude Code li tratta come identici e salta l'aggiornamento.
</Warning>

##### Esempio

```json theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Assegna i canali ai gruppi di utenti

Assegna ogni marketplace al gruppo di utenti appropriato tramite impostazioni gestite. Ad esempio, il gruppo stabile riceve:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

Il gruppo early-access riceve invece `latest-tools`:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Validazione e test

Testa il tuo marketplace prima di condividerlo.

Valida la sintassi JSON del tuo marketplace:

```bash theme={null}
claude plugin validate .
```

O da Claude Code:

```shell theme={null}
/plugin validate .
```

Aggiungi il marketplace per il test:

```shell theme={null}
/plugin marketplace add ./path/to/marketplace
```

Installa un plugin di test per verificare che tutto funzioni:

```shell theme={null}
/plugin install test-plugin@marketplace-name
```

Per i flussi di lavoro di test completi dei plugin, vedi [Testa i tuoi plugin localmente](/it/plugins#test-your-plugins-locally). Per la risoluzione dei problemi tecnici, vedi [Plugins reference](/it/plugins-reference).

## Troubleshooting

### Marketplace non carica

**Sintomi**: Non riesci ad aggiungere il marketplace o a vedere i plugin da esso

**Soluzioni**:

* Verifica che l'URL del marketplace sia accessibile
* Controlla che `.claude-plugin/marketplace.json` esista nel percorso specificato
* Assicurati che la sintassi JSON sia valida e che il frontmatter sia ben formato utilizzando `claude plugin validate` o `/plugin validate`
* Per i repository privati, conferma di avere i permessi di accesso

### Errori di validazione del marketplace

Esegui `claude plugin validate .` o `/plugin validate .` dalla directory del tuo marketplace per verificare i problemi. Il validatore controlla `plugin.json`, il frontmatter di skill/agente/comando e `hooks/hooks.json` per errori di sintassi e schema. Errori comuni:

| Errore                                            | Causa                                                 | Soluzione                                                                                               |
| :------------------------------------------------ | :---------------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `File not found: .claude-plugin/marketplace.json` | Manifest mancante                                     | Crea `.claude-plugin/marketplace.json` con i campi obbligatori                                          |
| `Invalid JSON syntax: Unexpected token...`        | Errore di sintassi JSON in marketplace.json           | Controlla le virgole mancanti, le virgole extra o le stringhe non quotate                               |
| `Duplicate plugin name "x" found in marketplace`  | Due plugin condividono lo stesso nome                 | Dai a ogni plugin un valore `name` univoco                                                              |
| `plugins[0].source: Path contains ".."`           | Il percorso di fonte contiene `..`                    | Usa percorsi relativi alla radice del marketplace senza `..`. Vedi [Percorsi relativi](#relative-paths) |
| `YAML frontmatter failed to parse: ...`           | YAML non valido in un file di skill, agente o comando | Correggi la sintassi YAML nel blocco frontmatter. Al runtime questo file si carica senza metadati.      |
| `Invalid JSON syntax: ...` (hooks.json)           | `hooks/hooks.json` malformato                         | Correggi la sintassi JSON. Un `hooks/hooks.json` malformato impedisce al plugin intero di caricarsi.    |

**Avvisi** (non bloccanti):

* `Marketplace has no plugins defined`: aggiungi almeno un plugin all'array `plugins`
* `No marketplace description provided`: aggiungi `metadata.description` per aiutare gli utenti a comprendere il tuo marketplace
* `Plugin name "x" is not kebab-case`: il nome del plugin contiene lettere maiuscole, spazi o caratteri speciali. Rinomina in lettere minuscole, cifre e trattini solo (ad esempio, `my-plugin`). Claude Code accetta altre forme, ma la sincronizzazione del marketplace Claude.ai le rifiuta.

### Errori di installazione del plugin

**Sintomi**: Il marketplace appare ma l'installazione del plugin non riesce

**Soluzioni**:

* Verifica che gli URL di fonte del plugin siano accessibili
* Controlla che le directory dei plugin contengano i file richiesti
* Per le fonti GitHub, assicurati che i repository siano pubblici o che tu abbia accesso
* Testa manualmente le fonti dei plugin clonando/scaricando

### L'autenticazione del repository privato non riesce

**Sintomi**: Errori di autenticazione durante l'installazione di plugin da repository privati

**Soluzioni**:

Per l'installazione manuale e gli aggiornamenti:

* Verifica di essere autenticato con il tuo provider git (ad esempio, esegui `gh auth status` per GitHub)
* Controlla che il tuo helper di credenziali sia configurato correttamente: `git config --global credential.helper`
* Prova a clonare il repository manualmente per verificare che le tue credenziali funzionino

Per gli aggiornamenti automatici in background:

* Imposta il token appropriato nel tuo ambiente: `echo $GITHUB_TOKEN`
* Controlla che il token abbia i permessi richiesti (accesso in lettura al repository)
* Per GitHub, assicurati che il token abbia lo scope `repo` per i repository privati
* Per GitLab, assicurati che il token abbia almeno lo scope `read_repository`
* Verifica che il token non sia scaduto

### Le operazioni Git scadono

**Sintomi**: L'installazione del plugin o gli aggiornamenti del marketplace non riescono con un errore di timeout come "Git clone timed out after 120s" o "Git pull timed out after 120s".

**Causa**: Claude Code utilizza un timeout di 120 secondi per tutte le operazioni git, inclusa la clonazione dei repository dei plugin e il pull degli aggiornamenti del marketplace. I repository di grandi dimensioni o le connessioni di rete lente possono superare questo limite.

**Soluzione**: Aumenta il timeout utilizzando la variabile di ambiente `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. Il valore è in millisecondi:

```bash theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minuti
```

### I plugin con percorsi relativi non riescono nei marketplace basati su URL

**Sintomi**: Hai aggiunto un marketplace tramite URL (come `https://example.com/marketplace.json`), ma i plugin con fonti di percorso relativo come `"./plugins/my-plugin"` non riescono a installare con errori "path not found".

**Causa**: I marketplace basati su URL scaricano solo il file `marketplace.json` stesso. Non scaricano i file dei plugin dal server. I percorsi relativi nella voce del marketplace fanno riferimento a file sul server remoto che non sono stati scaricati.

**Soluzioni**:

* **Usa fonti esterne**: Cambia le voci dei plugin per usare GitHub, npm o fonti URL git invece di percorsi relativi:
  ```json theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Usa un marketplace basato su Git**: Ospita il tuo marketplace in un repository Git e aggiungilo con l'URL git. I marketplace basati su Git clonano l'intero repository, rendendo i percorsi relativi funzionanti correttamente.

### File non trovati dopo l'installazione

**Sintomi**: Il plugin si installa ma i riferimenti ai file non riescono, specialmente i file al di fuori della directory del plugin

**Causa**: I plugin vengono copiati in una directory cache piuttosto che utilizzati in-place. I percorsi che fanno riferimento a file al di fuori della directory del plugin (come `../shared-utils`) non funzioneranno perché quei file non vengono copiati.

**Soluzioni**: Vedi [Plugin caching and file resolution](/it/plugins-reference#plugin-caching-and-file-resolution) per le soluzioni alternative inclusi symlink e ristrutturazione delle directory.

Per ulteriori strumenti di debug e problemi comuni, vedi [Debugging and development tools](/it/plugins-reference#debugging-and-development-tools).

## Vedi anche

* [Scopri e installa plugin precostruiti](/it/discover-plugins) - Installazione di plugin da marketplace esistenti
* [Plugin](/it/plugins) - Creazione dei tuoi plugin
* [Plugins reference](/it/plugins-reference) - Specifiche tecniche complete e schemi
* [Plugin settings](/it/settings#plugin-settings) - Opzioni di configurazione dei plugin
* [strictKnownMarketplaces reference](/it/settings#strictknownmarketplaces) - Restrizioni del marketplace gestito
