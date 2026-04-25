> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Connetti Claude Code ai tuoi strumenti tramite MCP

> Scopri come connettere Claude Code ai tuoi strumenti con il Model Context Protocol.

export const MCPServersTable = ({platform = "all"}) => {
  const ifYouAreAnAiAgentReadingThisYouShouldInsteadFetch = 'https://api.anthropic.com/mcp-registry/docs';
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    const fetchServers = async () => {
      try {
        setLoading(true);
        const allServers = [];
        let cursor = null;
        do {
          const url = new URL('https://api.anthropic.com/mcp-registry/v0/servers');
          url.searchParams.set('version', 'latest');
          url.searchParams.set('visibility', 'commercial');
          url.searchParams.set('limit', '100');
          if (cursor) {
            url.searchParams.set('cursor', cursor);
          }
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`Failed to fetch MCP registry: ${response.status}`);
          }
          const data = await response.json();
          allServers.push(...data.servers);
          cursor = data.metadata?.nextCursor || null;
        } while (cursor);
        const transformedServers = allServers.map(item => {
          const server = item.server;
          const meta = item._meta?.['com.anthropic.api/mcp-registry'] || ({});
          const worksWith = meta.worksWith || [];
          const availability = {
            claudeCode: worksWith.includes('claude-code'),
            mcpConnector: worksWith.includes('claude-api'),
            claudeDesktop: worksWith.includes('claude-desktop')
          };
          const remotes = server.remotes || [];
          const httpRemote = remotes.find(r => r.type === 'streamable-http');
          const sseRemote = remotes.find(r => r.type === 'sse');
          const preferredRemote = httpRemote || sseRemote;
          const remoteUrl = preferredRemote?.url || meta.url;
          const remoteType = preferredRemote?.type;
          const isTemplatedUrl = remoteUrl?.includes('{');
          let setupUrl;
          if (isTemplatedUrl && meta.requiredFields) {
            const urlField = meta.requiredFields.find(f => f.field === 'url');
            setupUrl = urlField?.sourceUrl || meta.documentation;
          }
          const urls = {};
          if (!isTemplatedUrl) {
            if (remoteType === 'streamable-http') {
              urls.http = remoteUrl;
            } else if (remoteType === 'sse') {
              urls.sse = remoteUrl;
            }
          }
          let envVars = [];
          if (server.packages && server.packages.length > 0) {
            const npmPackage = server.packages.find(p => p.registryType === 'npm');
            if (npmPackage) {
              urls.stdio = `npx -y ${npmPackage.identifier}`;
              if (npmPackage.environmentVariables) {
                envVars = npmPackage.environmentVariables;
              }
            }
          }
          return {
            name: meta.displayName || server.title || server.name,
            description: meta.oneLiner || server.description,
            documentation: meta.documentation,
            urls: urls,
            envVars: envVars,
            availability: availability,
            customCommands: meta.claudeCodeCopyText ? {
              claudeCode: meta.claudeCodeCopyText
            } : undefined,
            setupUrl: setupUrl
          };
        });
        setServers(transformedServers);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching MCP registry:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchServers();
  }, []);
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode.replace('--transport streamable-http', '--transport http');
    }
    const serverSlug = server.name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    if (server.urls.http) {
      return `claude mcp add ${serverSlug} --transport http ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add ${serverSlug} --transport sse ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.envVars && server.envVars.length > 0 ? server.envVars.map(v => `--env ${v.name}=YOUR_${v.name}`).join(' ') : '';
      const baseCommand = `claude mcp add ${serverSlug} --transport stdio`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  if (loading) {
    return <div>Loading MCP servers...</div>;
  }
  if (error) {
    return <div>Error loading MCP servers: {error}</div>;
  }
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>

      <div className="cards-container">
        {filteredServers.map(server => {
    const claudeCodeCommand = generateClaudeCodeCommand(server);
    const mcpUrl = server.urls.http || server.urls.sse;
    const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
    return <div key={server.name} className="server-card">
              <div>
                {server.documentation ? <a href={server.documentation}>
                    <strong>{server.name}</strong>
                  </a> : <strong>{server.name}</strong>}
              </div>

              <p style={{
      margin: '0.5rem 0',
      fontSize: '0.9rem'
    }}>
                {server.description}
              </p>

              {server.setupUrl && <p style={{
      margin: '0.25rem 0',
      fontSize: '0.8rem',
      fontStyle: 'italic',
      opacity: 0.7
    }}>
                  Requires user-specific URL.{' '}
                  <a href={server.setupUrl} style={{
      textDecoration: 'underline'
    }}>
                    Get your URL here
                  </a>.
                </p>}

              {commandToShow && !server.setupUrl && <>
                <p style={{
      display: 'block',
      fontSize: '0.75rem',
      fontWeight: 500,
      minWidth: 'fit-content',
      marginTop: '0.5rem',
      marginBottom: 0
    }}>
                  {platform === "claudeCode" ? "Command" : "URL"}
                </p>
                <div className="command-row">
                  <code>
                    {commandToShow}
                  </code>
                </div>
              </>}
            </div>;
  })}
      </div>
    </>;
};

Claude Code può connettersi a centinaia di strumenti e fonti di dati esterni attraverso il [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), uno standard open source per le integrazioni AI-tool. I server MCP danno a Claude Code accesso ai tuoi strumenti, database e API.

Connetti un server quando ti trovi a copiare dati in chat da un altro strumento, come un issue tracker o un dashboard di monitoraggio. Una volta connesso, Claude può leggere e agire su quel sistema direttamente invece di lavorare da quello che incolla.

## Cosa puoi fare con MCP

Con i server MCP connessi, puoi chiedere a Claude Code di:

* **Implementare funzionalità da issue tracker**: "Aggiungi la funzionalità descritta nel ticket JIRA ENG-4521 e crea una PR su GitHub."
* **Analizzare dati di monitoraggio**: "Controlla Sentry e Statsig per verificare l'utilizzo della funzionalità descritta in ENG-4521."
* **Interrogare database**: "Trova gli indirizzi email di 10 utenti casuali che hanno utilizzato la funzionalità ENG-4521, in base al nostro database PostgreSQL."
* **Integrare design**: "Aggiorna il nostro modello di email standard in base ai nuovi design Figma che sono stati pubblicati su Slack"
* **Automatizzare flussi di lavoro**: "Crea bozze Gmail invitando questi 10 utenti a una sessione di feedback sulla nuova funzionalità."
* **Reagire a eventi esterni**: Un server MCP può anche agire come un [canale](/it/channels) che invia messaggi nella tua sessione, in modo che Claude reagisca ai messaggi Telegram, chat Discord o eventi webhook mentre sei assente.

## Server MCP popolari

Ecco alcuni server MCP comunemente utilizzati che puoi connettere a Claude Code:

<Warning>
  Utilizza server MCP di terze parti a tuo rischio - Anthropic non ha verificato
  la correttezza o la sicurezza di tutti questi server.
  Assicurati di fidarti dei server MCP che stai installando.
  Fai particolare attenzione quando utilizzi server MCP che potrebbero recuperare
  contenuti non attendibili, poiché questi possono esporti al rischio di prompt injection.
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **Hai bisogno di un'integrazione specifica?** [Trova centinaia di altri server MCP su GitHub](https://github.com/modelcontextprotocol/servers), oppure crea il tuo utilizzando l'[MCP SDK](https://modelcontextprotocol.io/quickstart/server).
</Note>

## Installazione dei server MCP

I server MCP possono essere configurati in tre modi diversi a seconda delle tue esigenze:

### Opzione 1: Aggiungi un server HTTP remoto

I server HTTP sono l'opzione consigliata per connettersi ai server MCP remoti. Questo è il trasporto più ampiamente supportato per i servizi basati su cloud.

```bash theme={null}
# Sintassi di base
claude mcp add --transport http <name> <url>

# Esempio reale: Connessione a Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Esempio con token Bearer
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Opzione 2: Aggiungi un server SSE remoto

<Warning>
  Il trasporto SSE (Server-Sent Events) è deprecato. Utilizza server HTTP invece, dove disponibili.
</Warning>

```bash theme={null}
# Sintassi di base
claude mcp add --transport sse <name> <url>

# Esempio reale: Connessione ad Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Esempio con header di autenticazione
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Opzione 3: Aggiungi un server stdio locale

I server stdio vengono eseguiti come processi locali sulla tua macchina. Sono ideali per strumenti che necessitano di accesso diretto al sistema o script personalizzati.

```bash theme={null}
# Sintassi di base
claude mcp add [options] <name> -- <command> [args...]

# Esempio reale: Aggiungi server Airtable
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **Importante: Ordine delle opzioni**

  Tutte le opzioni (`--transport`, `--env`, `--scope`, `--header`) devono venire **prima** del nome del server. Il `--` (doppio trattino) separa quindi il nome del server dal comando e dagli argomenti che vengono passati al server MCP.

  Per esempio:

  * `claude mcp add --transport stdio myserver -- npx server` → esegue `npx server`
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → esegue `python server.py --port 8080` con `KEY=value` nell'ambiente

  Questo previene conflitti tra i flag di Claude e i flag del server.
</Note>

### Gestione dei tuoi server

Una volta configurati, puoi gestire i tuoi server MCP con questi comandi:

```bash theme={null}
# Elenca tutti i server configurati
claude mcp list

# Ottieni dettagli per un server specifico
claude mcp get github

# Rimuovi un server
claude mcp remove github

# (all'interno di Claude Code) Controlla lo stato del server
/mcp
```

### Aggiornamenti dinamici degli strumenti

Claude Code supporta le notifiche `list_changed` di MCP, consentendo ai server MCP di aggiornare dinamicamente i loro strumenti, prompt e risorse disponibili senza richiedere di disconnettersi e riconnettersi. Quando un server MCP invia una notifica `list_changed`, Claude Code aggiorna automaticamente le capacità disponibili da quel server.

### Riconnessione automatica

Se un server HTTP o SSE si disconnette durante una sessione, Claude Code si riconnette automaticamente con backoff esponenziale: fino a cinque tentativi, a partire da un ritardo di un secondo e raddoppiando ogni volta. Il server appare come in sospeso in `/mcp` mentre la riconnessione è in corso. Dopo cinque tentativi falliti il server è contrassegnato come non riuscito e puoi riprovare manualmente da `/mcp`. I server stdio sono processi locali e non vengono riconnessi automaticamente.

### Invia messaggi con canali

Un server MCP può anche inviare messaggi direttamente nella tua sessione in modo che Claude possa reagire a eventi esterni come risultati CI, avvisi di monitoraggio o messaggi di chat. Per abilitare questa funzionalità, il tuo server dichiara la capacità `claude/channel` e tu la abiliti con il flag `--channels` all'avvio. Vedi [Canali](/it/channels) per utilizzare un canale ufficialmente supportato, oppure [Riferimento canali](/it/channels-reference) per costruire il tuo.

<Tip>
  Suggerimenti:

  * Utilizza il flag `--scope` per specificare dove viene archiviata la configurazione:
    * `local` (predefinito): Disponibile solo per te nel progetto corrente (era chiamato `project` nelle versioni precedenti)
    * `project`: Condiviso con tutti nel progetto tramite il file `.mcp.json`
    * `user`: Disponibile per te in tutti i progetti (era chiamato `global` nelle versioni precedenti)
  * Imposta le variabili di ambiente con i flag `--env` (per esempio, `--env KEY=value`)
  * Configura il timeout di avvio del server MCP utilizzando la variabile di ambiente MCP\_TIMEOUT (per esempio, `MCP_TIMEOUT=10000 claude` imposta un timeout di 10 secondi)
  * Claude Code visualizzerà un avviso quando l'output dello strumento MCP supera 10.000 token. Per aumentare questo limite, imposta la variabile di ambiente `MAX_MCP_OUTPUT_TOKENS` (per esempio, `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Utilizza `/mcp` per autenticarti con server remoti che richiedono l'autenticazione OAuth 2.0
</Tip>

### Server MCP forniti da plugin

I [plugin](/it/plugins) possono raggruppare server MCP, fornendo automaticamente strumenti e integrazioni quando il plugin è abilitato. I server MCP dei plugin funzionano in modo identico ai server configurati dall'utente.

**Come funzionano i server MCP dei plugin**:

* I plugin definiscono i server MCP in `.mcp.json` nella radice del plugin o inline in `plugin.json`
* Quando un plugin è abilitato, i suoi server MCP si avviano automaticamente
* Gli strumenti MCP del plugin appaiono insieme agli strumenti MCP configurati manualmente
* I server dei plugin vengono gestiti tramite l'installazione del plugin (non tramite comandi `/mcp`)

**Esempio di configurazione MCP del plugin**:

In `.mcp.json` nella radice del plugin:

```json theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

O inline in `plugin.json`:

```json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Funzionalità MCP del plugin**:

* **Ciclo di vita automatico**: All'avvio della sessione, i server per i plugin abilitati si connettono automaticamente. Se abiliti o disabiliti un plugin durante una sessione, esegui `/reload-plugins` per connettere o disconnettere i suoi server MCP
* **Variabili di ambiente**: Utilizza `${CLAUDE_PLUGIN_ROOT}` per i file del plugin raggruppati e `${CLAUDE_PLUGIN_DATA}` per lo [stato persistente](/it/plugins-reference#persistent-data-directory) che sopravvive agli aggiornamenti del plugin
* **Accesso alle variabili di ambiente dell'utente**: Accesso alle stesse variabili di ambiente dei server configurati manualmente
* **Tipi di trasporto multipli**: Supporto per trasporti stdio, SSE e HTTP (il supporto del trasporto può variare a seconda del server)

**Visualizzazione dei server MCP del plugin**:

```bash theme={null}
# All'interno di Claude Code, vedi tutti i server MCP inclusi quelli dei plugin
/mcp
```

I server dei plugin appaiono nell'elenco con indicatori che mostrano che provengono dai plugin.

**Vantaggi dei server MCP dei plugin**:

* **Distribuzione raggruppata**: Strumenti e server confezionati insieme
* **Configurazione automatica**: Nessuna configurazione MCP manuale necessaria
* **Coerenza del team**: Tutti ottengono gli stessi strumenti quando il plugin è installato

Vedi il [riferimento dei componenti del plugin](/it/plugins-reference#mcp-servers) per i dettagli su come raggruppare i server MCP con i plugin.

## Ambiti di installazione MCP

I server MCP possono essere configurati a tre ambiti diversi. L'ambito che scegli controlla in quali progetti il server viene caricato e se la configurazione è condivisa con il tuo team.

| Ambito                     | Carica in                 | Condiviso con il team                | Archiviato in                         |
| -------------------------- | ------------------------- | ------------------------------------ | ------------------------------------- |
| [Locale](#local-scope)     | Solo il progetto corrente | No                                   | `~/.claude.json`                      |
| [Progetto](#project-scope) | Solo il progetto corrente | Sì, tramite controllo della versione | `.mcp.json` nella radice del progetto |
| [Utente](#user-scope)      | Tutti i tuoi progetti     | No                                   | `~/.claude.json`                      |

### Ambito locale

L'ambito locale è il predefinito. Un server con ambito locale viene caricato solo nel progetto in cui lo hai aggiunto e rimane privato per te. Claude Code lo archivia in `~/.claude.json` nel percorso di quel progetto, quindi lo stesso server non apparirà nei tuoi altri progetti. Utilizza l'ambito locale per server di sviluppo personali, configurazioni sperimentali o server con credenziali che non desideri nel controllo della versione.

<Note>
  Il termine "ambito locale" per i server MCP differisce dalle impostazioni locali generali. I server MCP con ambito locale vengono archiviati in `~/.claude.json` (la tua directory home), mentre le impostazioni locali generali utilizzano `.claude/settings.local.json` (nella directory del progetto). Vedi [Impostazioni](/it/settings#settings-files) per i dettagli sui percorsi dei file di impostazioni.
</Note>

```bash theme={null}
# Aggiungi un server con ambito locale (predefinito)
claude mcp add --transport http stripe https://mcp.stripe.com

# Specifica esplicitamente l'ambito locale
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

Il comando scrive il server nella voce per il tuo progetto corrente all'interno di `~/.claude.json`. L'esempio seguente mostra il risultato quando lo esegui da `/path/to/your/project`:

```json theme={null}
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

### Ambito del progetto

I server con ambito del progetto abilitano la collaborazione del team archiviando le configurazioni in un file `.mcp.json` nella directory radice del tuo progetto. Questo file è progettato per essere archiviato nel controllo della versione, assicurando che tutti i membri del team abbiano accesso agli stessi strumenti e servizi MCP. Quando aggiungi un server con ambito del progetto, Claude Code crea o aggiorna automaticamente questo file con la struttura di configurazione appropriata.

```bash theme={null}
# Aggiungi un server con ambio del progetto
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Il file `.mcp.json` risultante segue un formato standardizzato:

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

Per motivi di sicurezza, Claude Code richiede l'approvazione prima di utilizzare server con ambito del progetto dai file `.mcp.json`. Se devi ripristinare queste scelte di approvazione, utilizza il comando `claude mcp reset-project-choices`.

### Ambito utente

I server con ambito utente vengono archiviati in `~/.claude.json` e forniscono accessibilità tra progetti, rendendoli disponibili in tutti i progetti sulla tua macchina mentre rimangono privati al tuo account utente. Questo ambito funziona bene per server di utilità personali, strumenti di sviluppo o servizi che utilizzi frequentemente in diversi progetti.

```bash theme={null}
# Aggiungi un server utente
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Gerarchia e precedenza dell'ambito

Quando lo stesso server è definito in più di un posto, Claude Code si connette ad esso una volta, utilizzando la definizione dalla fonte con la precedenza più alta:

1. Ambito locale
2. Ambito del progetto
3. Ambito utente
4. [Server forniti da plugin](/it/plugins)
5. [Connettori claude.ai](#use-mcp-servers-from-claude-ai)

I tre ambiti corrispondono ai duplicati per nome. I plugin e i connettori corrispondono per endpoint, quindi uno che punta allo stesso URL o comando di un server sopra è trattato come un duplicato.

### Espansione delle variabili di ambiente in `.mcp.json`

Claude Code supporta l'espansione delle variabili di ambiente nei file `.mcp.json`, consentendo ai team di condividere configurazioni mantenendo flessibilità per i percorsi specifici della macchina e i valori sensibili come le chiavi API.

**Sintassi supportata:**

* `${VAR}` - Si espande al valore della variabile di ambiente `VAR`
* `${VAR:-default}` - Si espande a `VAR` se impostato, altrimenti utilizza `default`

**Posizioni di espansione:**
Le variabili di ambiente possono essere espanse in:

* `command` - Il percorso dell'eseguibile del server
* `args` - Argomenti della riga di comando
* `env` - Variabili di ambiente passate al server
* `url` - Per i tipi di server HTTP
* `headers` - Per l'autenticazione del server HTTP

**Esempio con espansione di variabili:**

```json theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Se una variabile di ambiente richiesta non è impostata e non ha un valore predefinito, Claude Code non riuscirà ad analizzare la configurazione.

## Esempi pratici

{/* ### Example: Automate browser testing with Playwright

```bash
claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
```

Then write and run browser tests:

```text
Test if the login flow works with test@example.com
```
```text
Take a screenshot of the checkout page on mobile
```
```text
Verify that the search feature returns results
``` */}

### Esempio: Monitora gli errori con Sentry

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Autenticati con il tuo account Sentry:

```text theme={null}
/mcp
```

Quindi esegui il debug dei problemi di produzione:

```text theme={null}
Quali sono gli errori più comuni nelle ultime 24 ore?
```

```text theme={null}
Mostrami la stack trace per l'errore ID abc123
```

```text theme={null}
Quale deployment ha introdotto questi nuovi errori?
```

### Esempio: Connettiti a GitHub per le revisioni del codice

Il server MCP remoto di GitHub si autentica con un token di accesso personale GitHub passato come header. Per ottenerne uno, apri le [impostazioni del token GitHub](https://github.com/settings/personal-access-tokens), genera un nuovo token con granularità fine con accesso ai repository con cui desideri che Claude lavori, quindi aggiungi il server:

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Quindi lavora con GitHub:

```text theme={null}
Rivedi la PR #456 e suggerisci miglioramenti
```

```text theme={null}
Crea un nuovo issue per il bug che abbiamo appena trovato
```

```text theme={null}
Mostrami tutte le PR aperte assegnate a me
```

### Esempio: Interroga il tuo database PostgreSQL

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Quindi interroga il tuo database naturalmente:

```text theme={null}
Qual è il nostro ricavo totale questo mese?
```

```text theme={null}
Mostrami lo schema per la tabella orders
```

```text theme={null}
Trova i clienti che non hanno effettuato un acquisto negli ultimi 90 giorni
```

## Autenticazione con server MCP remoti

Molti server MCP basati su cloud richiedono l'autenticazione. Claude Code supporta OAuth 2.0 per connessioni sicure.

<Steps>
  <Step title="Aggiungi il server che richiede l'autenticazione">
    Per esempio:

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Utilizza il comando /mcp all'interno di Claude Code">
    In Claude Code, utilizza il comando:

    ```text theme={null}
    /mcp
    ```

    Quindi segui i passaggi nel tuo browser per accedere.
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * I token di autenticazione vengono archiviati in modo sicuro e aggiornati automaticamente
  * Utilizza "Clear authentication" nel menu `/mcp` per revocare l'accesso
  * Se il tuo browser non si apre automaticamente, copia l'URL fornito e aprilo manualmente
  * Se il reindirizzamento del browser non riesce con un errore di connessione dopo l'autenticazione, incolla l'URL di callback completo dalla barra degli indirizzi del tuo browser nel prompt dell'URL che appare in Claude Code
  * L'autenticazione OAuth funziona con i server HTTP
</Tip>

### Utilizza una porta di callback OAuth fissa

Alcuni server MCP richiedono un URI di reindirizzamento specifico registrato in anticipo. Per impostazione predefinita, Claude Code sceglie una porta disponibile casuale per il callback OAuth. Utilizza `--callback-port` per fissare la porta in modo che corrisponda a un URI di reindirizzamento pre-registrato della forma `http://localhost:PORT/callback`.

Puoi utilizzare `--callback-port` da solo (con registrazione dinamica del client) o insieme a `--client-id` (con credenziali pre-configurate).

```bash theme={null}
# Porta di callback fissa con registrazione dinamica del client
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Utilizza credenziali OAuth pre-configurate

Alcuni server MCP non supportano la configurazione OAuth automatica tramite Dynamic Client Registration. Se vedi un errore come "Incompatible auth server: does not support dynamic client registration," il server richiede credenziali pre-configurate. Claude Code supporta anche server che utilizzano un Client ID Metadata Document (CIMD) invece di Dynamic Client Registration e li scopre automaticamente. Se la scoperta automatica non riesce, registra prima un'app OAuth tramite il portale degli sviluppatori del server, quindi fornisci le credenziali quando aggiungi il server.

<Steps>
  <Step title="Registra un'app OAuth con il server">
    Crea un'app tramite il portale degli sviluppatori del server e annota il tuo ID client e il segreto client.

    Molti server richiedono anche un URI di reindirizzamento. Se è così, scegli una porta e registra un URI di reindirizzamento nel formato `http://localhost:PORT/callback`. Utilizza quella stessa porta con `--callback-port` nel passaggio successivo.
  </Step>

  <Step title="Aggiungi il server con le tue credenziali">
    Scegli uno dei seguenti metodi. La porta utilizzata per `--callback-port` può essere qualsiasi porta disponibile. Deve solo corrispondere all'URI di reindirizzamento che hai registrato nel passaggio precedente.

    <Tabs>
      <Tab title="claude mcp add">
        Utilizza `--client-id` per passare l'ID client della tua app. Il flag `--client-secret` richiede il segreto con input mascherato:

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Includi l'oggetto `oauth` nella configurazione JSON e passa `--client-secret` come flag separato:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (solo porta di callback)">
        Utilizza `--callback-port` senza un ID client per fissare la porta mentre utilizzi la registrazione dinamica del client:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / env var">
        Imposta il segreto tramite variabile di ambiente per saltare il prompt interattivo:

        ```bash theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Autenticati in Claude Code">
    Esegui `/mcp` in Claude Code e segui il flusso di accesso del browser.
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Il segreto client viene archiviato in modo sicuro nel tuo portachiavi di sistema (macOS) o in un file di credenziali, non nella tua configurazione
  * Se il server utilizza un client OAuth pubblico senza segreto, utilizza solo `--client-id` senza `--client-secret`
  * `--callback-port` può essere utilizzato con o senza `--client-id`
  * Questi flag si applicano solo ai trasporti HTTP e SSE. Non hanno effetto sui server stdio
  * Utilizza `claude mcp get <name>` per verificare che le credenziali OAuth siano configurate per un server
</Tip>

### Sovrascrivi la scoperta dei metadati OAuth

Indirizza Claude Code a un URL di metadati OAuth specifico per bypassare la catena di scoperta predefinita. Imposta `authServerMetadataUrl` quando gli endpoint standard del server MCP generano errori, o quando desideri instradare la scoperta attraverso un proxy interno. Per impostazione predefinita, Claude Code controlla prima i metadati della risorsa protetta RFC 9728 su `/.well-known/oauth-protected-resource`, quindi ricade sui metadati del server di autorizzazione RFC 8414 su `/.well-known/oauth-authorization-server`.

Imposta `authServerMetadataUrl` nell'oggetto `oauth` della configurazione del tuo server in `.mcp.json`:

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

L'URL deve utilizzare `https://`. `authServerMetadataUrl` richiede Claude Code v2.1.64 o successiva. L'`scopes_supported` dell'URL dei metadati sovrascrive gli ambiti che il server upstream pubblicizza.

### Limita gli ambiti OAuth

Imposta `oauth.scopes` per fissare gli ambiti che Claude Code richiede durante il flusso di autorizzazione. Questo è il modo supportato per limitare un server MCP a un sottoinsieme approvato dal team di sicurezza quando il server di autorizzazione upstream pubblicizza più ambiti di quelli che desideri concedere. Il valore è una singola stringa separata da spazi, corrispondente al formato del parametro `scope` in RFC 6749 §3.3.

```json theme={null}
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` ha la precedenza sia su `authServerMetadataUrl` che sugli ambiti che il server scopre su `/.well-known`. Lascialo non impostato per consentire al server MCP di determinare l'insieme di ambiti richiesti.

Se il server di autorizzazione pubblicizza `offline_access` in `scopes_supported`, Claude Code lo aggiunge agli ambiti fissati in modo che il token di accesso possa essere aggiornato senza un nuovo accesso al browser.

Se il server successivamente restituisce un 403 `insufficient_scope` per una chiamata di strumento, Claude Code si autentica di nuovo con gli stessi ambiti fissati. Amplia `oauth.scopes` quando uno strumento di cui hai bisogno richiede un ambito al di fuori del pin.

### Utilizza intestazioni dinamiche per l'autenticazione personalizzata

Se il tuo server MCP utilizza uno schema di autenticazione diverso da OAuth (come Kerberos, token di breve durata o un SSO interno), utilizza `headersHelper` per generare intestazioni di richiesta al momento della connessione. Claude Code esegue il comando e unisce il suo output alle intestazioni di connessione.

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

Il comando può anche essere inline:

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Requisiti:**

* Il comando deve scrivere un oggetto JSON di coppie chiave-valore stringa su stdout
* Il comando viene eseguito in una shell con un timeout di 10 secondi
* Le intestazioni dinamiche sovrascrivono qualsiasi `headers` statico con lo stesso nome

L'helper viene eseguito di nuovo ad ogni connessione (all'avvio della sessione e alla riconnessione). Non c'è caching, quindi il tuo script è responsabile di qualsiasi riutilizzo di token.

Claude Code imposta queste variabili di ambiente quando esegue l'helper:

| Variabile                     | Valore                 |
| :---------------------------- | :--------------------- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | il nome del server MCP |
| `CLAUDE_CODE_MCP_SERVER_URL`  | l'URL del server MCP   |

Utilizza questi per scrivere un singolo script helper che serve più server MCP.

<Note>
  `headersHelper` esegue comandi shell arbitrari. Quando definito a livello di progetto o locale, viene eseguito solo dopo che accetti la finestra di dialogo di fiducia dell'area di lavoro.
</Note>

## Aggiungi server MCP dalla configurazione JSON

Se hai una configurazione JSON per un server MCP, puoi aggiungerla direttamente:

<Steps>
  <Step title="Aggiungi un server MCP da JSON">
    ```bash theme={null}
    # Sintassi di base
    claude mcp add-json <name> '<json>'

    # Esempio: Aggiunta di un server HTTP con configurazione JSON
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Esempio: Aggiunta di un server stdio con configurazione JSON
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # Esempio: Aggiunta di un server HTTP con credenziali OAuth pre-configurate
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="Verifica che il server sia stato aggiunto">
    ```bash theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Assicurati che il JSON sia correttamente sfuggito nella tua shell
  * Il JSON deve conformarsi allo schema di configurazione del server MCP
  * Puoi utilizzare `--scope user` per aggiungere il server alla tua configurazione utente invece di quella specifica del progetto
</Tip>

## Importa server MCP da Claude Desktop

Se hai già configurato server MCP in Claude Desktop, puoi importarli:

<Steps>
  <Step title="Importa server da Claude Desktop">
    ```bash theme={null}
    # Sintassi di base 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Seleziona quali server importare">
    Dopo aver eseguito il comando, vedrai una finestra di dialogo interattiva che ti consente di selezionare quali server desideri importare.
  </Step>

  <Step title="Verifica che i server siano stati importati">
    ```bash theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Questa funzionalità funziona solo su macOS e Windows Subsystem for Linux (WSL)
  * Legge il file di configurazione di Claude Desktop dalla sua posizione standard su quelle piattaforme
  * Utilizza il flag `--scope user` per aggiungere server alla tua configurazione utente
  * I server importati avranno gli stessi nomi di Claude Desktop
  * Se server con gli stessi nomi esistono già, riceveranno un suffisso numerico (per esempio, `server_1`)
</Tip>

## Utilizza server MCP da Claude.ai

Se hai effettuato l'accesso a Claude Code con un account [Claude.ai](https://claude.ai), i server MCP che hai aggiunto in Claude.ai sono automaticamente disponibili in Claude Code:

<Steps>
  <Step title="Configura server MCP in Claude.ai">
    Aggiungi server su [claude.ai/customize/connectors](https://claude.ai/customize/connectors). Nei piani Team ed Enterprise, solo gli amministratori possono aggiungere server.
  </Step>

  <Step title="Autentica il server MCP">
    Completa eventuali passaggi di autenticazione richiesti in Claude.ai.
  </Step>

  <Step title="Visualizza e gestisci i server in Claude Code">
    In Claude Code, utilizza il comando:

    ```text theme={null}
    /mcp
    ```

    I server Claude.ai appaiono nell'elenco con indicatori che mostrano che provengono da Claude.ai.
  </Step>
</Steps>

Per disabilitare i server MCP di claude.ai in Claude Code, imposta la variabile di ambiente `ENABLE_CLAUDEAI_MCP_SERVERS` su `false`:

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Utilizza Claude Code come server MCP

Puoi utilizzare Claude Code stesso come server MCP a cui altre applicazioni possono connettersi:

```bash theme={null}
# Avvia Claude come server MCP stdio
claude mcp serve
```

Puoi utilizzarlo in Claude Desktop aggiungendo questa configurazione a claude\_desktop\_config.json:

```json theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **Configurazione del percorso dell'eseguibile**: Il campo `command` deve fare riferimento all'eseguibile di Claude Code. Se il comando `claude` non è nel PATH del tuo sistema, dovrai specificare il percorso completo dell'eseguibile.

  Per trovare il percorso completo:

  ```bash theme={null}
  which claude
  ```

  Quindi utilizza il percorso completo nella tua configurazione:

  ```json theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  Senza il percorso dell'eseguibile corretto, incontrerai errori come `spawn claude ENOENT`.
</Warning>

<Tip>
  Suggerimenti:

  * Il server fornisce accesso agli strumenti di Claude come View, Edit, LS, ecc.
  * In Claude Desktop, prova a chiedere a Claude di leggere file in una directory, fare modifiche e altro ancora.
  * Nota che questo server MCP sta solo esponendo gli strumenti di Claude Code al tuo client MCP, quindi il tuo client è responsabile dell'implementazione della conferma dell'utente per le singole chiamate di strumenti.
</Tip>

## Limiti di output MCP e avvisi

Quando gli strumenti MCP producono output di grandi dimensioni, Claude Code aiuta a gestire l'utilizzo dei token per evitare di sovraccaricare il contesto della tua conversazione:

* **Soglia di avviso di output**: Claude Code visualizza un avviso quando l'output di qualsiasi strumento MCP supera 10.000 token
* **Limite configurabile**: Puoi regolare il massimo di token di output MCP consentiti utilizzando la variabile di ambiente `MAX_MCP_OUTPUT_TOKENS`
* **Limite predefinito**: Il massimo predefinito è 25.000 token
* **Ambito**: La variabile di ambiente si applica agli strumenti che non dichiarano il loro limite. Gli strumenti che impostano [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) utilizzano quel valore invece per il contenuto di testo, indipendentemente da ciò che `MAX_MCP_OUTPUT_TOKENS` è impostato. Gli strumenti che restituiscono dati di immagine sono ancora soggetti a `MAX_MCP_OUTPUT_TOKENS`

Per aumentare il limite per gli strumenti che producono output di grandi dimensioni:

```bash theme={null}
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Questo è particolarmente utile quando si lavora con server MCP che:

* Interrogano grandi set di dati o database
* Generano report o documentazione dettagliati
* Elaborano file di log estesi o informazioni di debug

### Aumenta il limite per uno strumento specifico

Se stai costruendo un server MCP, puoi consentire ai singoli strumenti di restituire risultati più grandi della soglia predefinita impostando `_meta["anthropic/maxResultSizeChars"]` nella voce dello strumento nella risposta `tools/list`. Claude Code aumenta la soglia di quello strumento al valore annotato, fino a un limite massimo di 500.000 caratteri.

Questo è utile per strumenti che restituiscono output intrinsecamente grandi ma necessari, come schemi di database o alberi di file completi. Senza l'annotazione, i risultati che superano la soglia predefinita vengono persistiti su disco e sostituiti con un riferimento a file nella conversazione.

```json theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

L'annotazione si applica indipendentemente da `MAX_MCP_OUTPUT_TOKENS` per il contenuto di testo, quindi gli utenti non hanno bisogno di aumentare la variabile di ambiente per gli strumenti che la dichiarano. Gli strumenti che restituiscono dati di immagine sono ancora soggetti al limite di token.

<Warning>
  Se incontri frequentemente avvisi di output con server MCP specifici che non controlli, considera di aumentare il limite `MAX_MCP_OUTPUT_TOKENS`. Puoi anche chiedere all'autore del server di aggiungere l'annotazione `anthropic/maxResultSizeChars` o di impaginare le loro risposte. L'annotazione non ha effetto sugli strumenti che restituiscono contenuto di immagine; per quelli, aumentare `MAX_MCP_OUTPUT_TOKENS` è l'unica opzione.
</Warning>

## Rispondi alle richieste di elicitazione MCP

I server MCP possono richiedere input strutturato da te durante un'attività utilizzando l'elicitazione. Quando un server ha bisogno di informazioni che non può ottenere da solo, Claude Code visualizza una finestra di dialogo interattiva e passa la tua risposta al server. Non è richiesta alcuna configurazione da parte tua: le finestre di dialogo di elicitazione appaiono automaticamente quando un server le richiede.

I server possono richiedere input in due modi:

* **Modalità modulo**: Claude Code mostra una finestra di dialogo con campi modulo definiti dal server (per esempio, un prompt di nome utente e password). Compila i campi e invia.
* **Modalità URL**: Claude Code apre un URL del browser per l'autenticazione o l'approvazione. Completa il flusso nel browser, quindi conferma nella CLI.

Per rispondere automaticamente alle richieste di elicitazione senza mostrare una finestra di dialogo, utilizza l'[hook `Elicitation`](/it/hooks#elicitation).

Se stai costruendo un server MCP che utilizza l'elicitazione, vedi la [specifica di elicitazione MCP](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) per i dettagli del protocollo e gli esempi di schema.

## Utilizza risorse MCP

I server MCP possono esporre risorse che puoi referenziare utilizzando menzioni @, simile a come referenzi i file.

### Referenzia risorse MCP

<Steps>
  <Step title="Elenca le risorse disponibili">
    Digita `@` nel tuo prompt per vedere le risorse disponibili da tutti i server MCP connessi. Le risorse appaiono insieme ai file nel menu di completamento automatico.
  </Step>

  <Step title="Referenzia una risorsa specifica">
    Utilizza il formato `@server:protocol://resource/path` per referenziare una risorsa:

    ```text theme={null}
    Puoi analizzare @github:issue://123 e suggerire una correzione?
    ```

    ```text theme={null}
    Per favore rivedi la documentazione API su @docs:file://api/authentication
    ```
  </Step>

  <Step title="Referenze di risorse multiple">
    Puoi referenziare più risorse in un singolo prompt:

    ```text theme={null}
    Confronta @postgres:schema://users con @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Le risorse vengono recuperate automaticamente e incluse come allegati quando referenziate
  * I percorsi delle risorse sono ricercabili con fuzzy search nel completamento automatico della menzione @
  * Claude Code fornisce automaticamente strumenti per elencare e leggere risorse MCP quando i server le supportano
  * Le risorse possono contenere qualsiasi tipo di contenuto fornito dal server MCP (testo, JSON, dati strutturati, ecc.)
</Tip>

## Scala con MCP Tool Search

Tool search mantiene l'utilizzo del contesto MCP basso rimandando le definizioni degli strumenti fino a quando Claude ne ha bisogno. Solo i nomi degli strumenti vengono caricati all'avvio della sessione, quindi aggiungere più server MCP ha un impatto minimo sulla tua finestra di contesto.

### Come funziona

Tool search è abilitato per impostazione predefinita. Gli strumenti MCP vengono rimandati piuttosto che caricati nel contesto in anticipo, e Claude utilizza uno strumento di ricerca per scoprire quelli rilevanti quando un'attività ne ha bisogno. Solo gli strumenti che Claude effettivamente utilizza entrano nel contesto. Dal tuo punto di vista, gli strumenti MCP funzionano esattamente come prima.

Se preferisci il caricamento basato su soglia, imposta `ENABLE_TOOL_SEARCH=auto` per caricare gli schemi in anticipo quando si adattano entro il 10% della finestra di contesto e rimanda solo l'overflow. Vedi [Configura tool search](#configure-tool-search) per tutte le opzioni.

### Per gli autori di server MCP

Se stai costruendo un server MCP, il campo delle istruzioni del server diventa più utile con Tool Search abilitato. Le istruzioni del server aiutano Claude a capire quando cercare i tuoi strumenti, simile a come funzionano le [skills](/it/skills).

Aggiungi istruzioni del server chiare e descrittive che spieghino:

* Quale categoria di attività gestiscono i tuoi strumenti
* Quando Claude dovrebbe cercare i tuoi strumenti
* Capacità chiave che il tuo server fornisce

Claude Code tronca le descrizioni degli strumenti e le istruzioni del server a 2KB ciascuna. Mantienile concise per evitare il troncamento e metti i dettagli critici all'inizio.

### Configura tool search

Tool search è abilitato per impostazione predefinita: gli strumenti MCP vengono rimandati e scoperti su richiesta. È disabilitato per impostazione predefinita su Vertex AI, che non accetta l'intestazione beta tool search, e quando `ANTHROPIC_BASE_URL` punta a un host non di prima parte, poiché la maggior parte dei proxy non inoltrano blocchi `tool_reference`. Imposta `ENABLE_TOOL_SEARCH` esplicitamente per opt-in. Questa funzionalità richiede modelli che supportano blocchi `tool_reference`: Sonnet 4 e successivi, oppure Opus 4 e successivi. I modelli Haiku non supportano tool search.

Controlla il comportamento di tool search con la variabile di ambiente `ENABLE_TOOL_SEARCH`:

| Valore          | Comportamento                                                                                                                                                        |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (non impostato) | Tutti gli strumenti MCP rimandati e caricati su richiesta. Ricade al caricamento in anticipo su Vertex AI o quando `ANTHROPIC_BASE_URL` è un host non di prima parte |
| `true`          | Tutti gli strumenti MCP rimandati, incluso su Vertex AI e per `ANTHROPIC_BASE_URL` non di prima parte                                                                |
| `auto`          | Modalità soglia: gli strumenti vengono caricati in anticipo se si adattano entro il 10% della finestra di contesto, rimandati altrimenti                             |
| `auto:<N>`      | Modalità soglia con una percentuale personalizzata, dove `<N>` è 0-100 (ad es. `auto:5` per il 5%)                                                                   |
| `false`         | Tutti gli strumenti MCP caricati in anticipo, nessun rinvio                                                                                                          |

```bash theme={null}
# Utilizza una soglia personalizzata del 5%
ENABLE_TOOL_SEARCH=auto:5 claude

# Disabilita completamente tool search
ENABLE_TOOL_SEARCH=false claude
```

Oppure imposta il valore nel campo `env` del tuo [settings.json](/it/settings#available-settings).

Puoi anche disabilitare lo strumento `ToolSearch` specificamente:

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

## Utilizza i prompt MCP come comandi

I server MCP possono esporre prompt che diventano disponibili come comandi in Claude Code.

### Esegui i prompt MCP

<Steps>
  <Step title="Scopri i prompt disponibili">
    Digita `/` per vedere tutti i comandi disponibili, inclusi quelli dai server MCP. I prompt MCP appaiono con il formato `/mcp__servername__promptname`.
  </Step>

  <Step title="Esegui un prompt senza argomenti">
    ```text theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Esegui un prompt con argomenti">
    Molti prompt accettano argomenti. Passali separati da spazi dopo il comando:

    ```text theme={null}
    /mcp__github__pr_review 456
    ```

    ```text theme={null}
    /mcp__jira__create_issue "Bug nel flusso di accesso" high
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * I prompt MCP vengono scoperti dinamicamente dai server connessi
  * Gli argomenti vengono analizzati in base ai parametri definiti del prompt
  * I risultati del prompt vengono iniettati direttamente nella conversazione
  * I nomi del server e del prompt vengono normalizzati (gli spazi diventano trattini bassi)
</Tip>

## Configurazione MCP gestita

Per le organizzazioni che necessitano di un controllo centralizzato sui server MCP, Claude Code supporta due opzioni di configurazione:

1. **Controllo esclusivo con `managed-mcp.json`**: Distribuisci un set fisso di server MCP che gli utenti non possono modificare o estendere
2. **Controllo basato su policy con allowlist/denylist**: Consenti agli utenti di aggiungere i propri server, ma limita quali sono consentiti

Queste opzioni consentono agli amministratori IT di:

* **Controllare a quali server MCP i dipendenti possono accedere**: Distribuisci un set standardizzato di server MCP approvati in tutta l'organizzazione
* **Prevenire server MCP non autorizzati**: Limita gli utenti dall'aggiungere server MCP non approvati
* **Disabilitare completamente MCP**: Rimuovi completamente la funzionalità MCP se necessario

### Opzione 1: Controllo esclusivo con managed-mcp.json

Quando distribuisci un file `managed-mcp.json`, assume il **controllo esclusivo** su tutti i server MCP. Gli utenti non possono aggiungere, modificare o utilizzare alcun server MCP diverso da quelli definiti in questo file. Questo è l'approccio più semplice per le organizzazioni che desiderano un controllo completo.

Gli amministratori di sistema distribuiscono il file di configurazione a una directory a livello di sistema:

* macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux e WSL: `/etc/claude-code/managed-mcp.json`
* Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

<Note>
  Questi sono percorsi a livello di sistema (non directory home dell'utente come `~/Library/...`) che richiedono privilegi di amministratore. Sono progettati per essere distribuiti dagli amministratori IT.
</Note>

Il file `managed-mcp.json` utilizza lo stesso formato di un file `.mcp.json` standard:

```json theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Opzione 2: Controllo basato su policy con allowlist e denylist

Invece di assumere il controllo esclusivo, gli amministratori possono consentire agli utenti di configurare i propri server MCP mentre applicano restrizioni su quali server sono consentiti. Questo approccio utilizza `allowedMcpServers` e `deniedMcpServers` nel [file di impostazioni gestite](/it/settings#settings-files).

<Note>
  **Scelta tra le opzioni**: Utilizza l'Opzione 1 (`managed-mcp.json`) quando desideri distribuire un set fisso di server senza personalizzazione dell'utente. Utilizza l'Opzione 2 (allowlist/denylist) quando desideri consentire agli utenti di aggiungere i propri server entro i vincoli della policy.
</Note>

#### Opzioni di restrizione

Ogni voce nell'allowlist o denylist può limitare i server in tre modi:

1. **Per nome del server** (`serverName`): Corrisponde al nome configurato del server
2. **Per comando** (`serverCommand`): Corrisponde al comando esatto e agli argomenti utilizzati per avviare i server stdio
3. **Per pattern URL** (`serverUrl`): Corrisponde agli URL dei server remoti con supporto per i caratteri jolly

**Importante**: Ogni voce deve avere esattamente uno tra `serverName`, `serverCommand` o `serverUrl`.

#### Configurazione di esempio

```json theme={null}
{
  "allowedMcpServers": [
    // Consenti per nome del server
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Consenti per comando esatto (per server stdio)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Consenti per pattern URL (per server remoti)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Blocca per nome del server
    { "serverName": "dangerous-server" },

    // Blocca per comando esatto (per server stdio)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Blocca per pattern URL (per server remoti)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### Come funzionano le restrizioni basate su comando

**Corrispondenza esatta**:

* Gli array di comando devono corrispondere **esattamente** - sia il comando che tutti gli argomenti nell'ordine corretto
* Esempio: `["npx", "-y", "server"]` NON corrisponderà a `["npx", "server"]` o `["npx", "-y", "server", "--flag"]`

**Comportamento del server stdio**:

* Quando l'allowlist contiene **qualsiasi** voce `serverCommand`, i server stdio **devono** corrispondere a uno di quei comandi
* I server stdio non possono passare solo per nome quando sono presenti restrizioni di comando
* Questo assicura che gli amministratori possono applicare quali comandi sono consentiti di eseguire

**Comportamento del server non-stdio**:

* I server remoti (HTTP, SSE, WebSocket) utilizzano la corrispondenza basata su URL quando esistono voci `serverUrl` nell'allowlist
* Se non esistono voci URL, i server remoti ricadono sulla corrispondenza basata su nome
* Le restrizioni di comando non si applicano ai server remoti

#### Come funzionano le restrizioni basate su URL

I pattern URL supportano i caratteri jolly utilizzando `*` per corrispondere a qualsiasi sequenza di caratteri. Questo è utile per consentire interi domini o sottodomini.

**Esempi di caratteri jolly**:

* `https://mcp.company.com/*` - Consenti tutti i percorsi su un dominio specifico
* `https://*.example.com/*` - Consenti qualsiasi sottodominio di example.com
* `http://localhost:*/*` - Consenti qualsiasi porta su localhost

**Comportamento del server remoto**:

* Quando l'allowlist contiene **qualsiasi** voce `serverUrl`, i server remoti **devono** corrispondere a uno di quei pattern URL
* I server remoti non possono passare solo per nome quando sono presenti restrizioni URL
* Questo assicura che gli amministratori possono applicare quali endpoint remoti sono consentiti

<Accordion title="Esempio: Allowlist solo URL">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.company.com/*" },
      { "serverUrl": "https://*.internal.corp/*" }
    ]
  }
  ```

  **Risultato**:

  * Server HTTP su `https://mcp.company.com/api`: ✅ Consentito (corrisponde al pattern URL)
  * Server HTTP su `https://api.internal.corp/mcp`: ✅ Consentito (corrisponde al sottodominio jolly)
  * Server HTTP su `https://external.com/mcp`: ❌ Bloccato (non corrisponde a nessun pattern URL)
  * Server stdio con qualsiasi comando: ❌ Bloccato (nessuna voce di nome o comando per corrispondere)
</Accordion>

<Accordion title="Esempio: Allowlist solo comando">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Risultato**:

  * Server stdio con `["npx", "-y", "approved-package"]`: ✅ Consentito (corrisponde al comando)
  * Server stdio con `["node", "server.js"]`: ❌ Bloccato (non corrisponde al comando)
  * Server HTTP denominato "my-api": ❌ Bloccato (nessuna voce di nome per corrispondere)
</Accordion>

<Accordion title="Esempio: Allowlist misto di nome e comando">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Risultato**:

  * Server stdio denominato "local-tool" con `["npx", "-y", "approved-package"]`: ✅ Consentito (corrisponde al comando)
  * Server stdio denominato "local-tool" con `["node", "server.js"]`: ❌ Bloccato (le voci di comando esistono ma non corrisponde)
  * Server stdio denominato "github" con `["node", "server.js"]`: ❌ Bloccato (i server stdio devono corrispondere ai comandi quando le voci di comando esistono)
  * Server HTTP denominato "github": ✅ Consentito (corrisponde al nome)
  * Server HTTP denominato "other-api": ❌ Bloccato (il nome non corrisponde)
</Accordion>

<Accordion title="Esempio: Allowlist solo nome">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  **Risultato**:

  * Server stdio denominato "github" con qualsiasi comando: ✅ Consentito (nessuna restrizione di comando)
  * Server stdio denominato "internal-tool" con qualsiasi comando: ✅ Consentito (nessuna restrizione di comando)
  * Server HTTP denominato "github": ✅ Consentito (corrisponde al nome)
  * Qualsiasi server denominato "other": ❌ Bloccato (il nome non corrisponde)
</Accordion>

#### Comportamento dell'allowlist (`allowedMcpServers`)

* `undefined` (predefinito): Nessuna restrizione - gli utenti possono configurare qualsiasi server MCP
* Array vuoto `[]`: Blocco completo - gli utenti non possono configurare alcun server MCP
* Elenco di voci: Gli utenti possono configurare solo server che corrispondono per nome, comando o pattern URL

#### Comportamento della denylist (`deniedMcpServers`)

* `undefined` (predefinito): Nessun server è bloccato
* Array vuoto `[]`: Nessun server è bloccato
* Elenco di voci: I server specificati sono esplicitamente bloccati in tutti gli ambiti

#### Note importanti

* **L'Opzione 1 e l'Opzione 2 possono essere combinate**: Se `managed-mcp.json` esiste, ha il controllo esclusivo e gli utenti non possono aggiungere server. Gli allowlist/denylist si applicano comunque ai server gestiti stessi.
* **La denylist ha precedenza assoluta**: Se un server corrisponde a una voce della denylist (per nome, comando o URL), sarà bloccato anche se è nell'allowlist
* **Le restrizioni basate su nome, comando e URL funzionano insieme**: un server passa se corrisponde a **una** voce di nome, una voce di comando o un pattern URL (a meno che non sia bloccato dalla denylist)

<Note>
  **Quando utilizzi `managed-mcp.json`**: Gli utenti non possono aggiungere server MCP tramite `claude mcp add` o file di configurazione. Le impostazioni `allowedMcpServers` e `deniedMcpServers` si applicano comunque per filtrare quali server gestiti vengono effettivamente caricati.
</Note>
