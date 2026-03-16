> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Impostazioni di Claude Code

> Configura Claude Code con impostazioni globali e a livello di progetto, e variabili di ambiente.

Claude Code offre una varietà di impostazioni per configurare il suo comportamento in base alle tue esigenze. Puoi configurare Claude Code eseguendo il comando `/config` quando utilizzi il REPL interattivo, che apre un'interfaccia Impostazioni con schede dove puoi visualizzare informazioni di stato e modificare le opzioni di configurazione.

## Ambiti di configurazione

Claude Code utilizza un **sistema di ambiti** per determinare dove si applicano le configurazioni e con chi vengono condivise. Comprendere gli ambiti ti aiuta a decidere come configurare Claude Code per uso personale, collaborazione di team o distribuzione aziendale.

### Ambiti disponibili

| Ambito      | Posizione                                                                                         | Chi interessa                              | Condiviso con il team? |
| :---------- | :------------------------------------------------------------------------------------------------ | :----------------------------------------- | :--------------------- |
| **Managed** | Impostazioni gestite dal server, plist / registro, o `managed-settings.json` a livello di sistema | Tutti gli utenti sulla macchina            | Sì (distribuito da IT) |
| **User**    | Directory `~/.claude/`                                                                            | Tu, in tutti i progetti                    | No                     |
| **Project** | `.claude/` nel repository                                                                         | Tutti i collaboratori su questo repository | Sì (committato su git) |
| **Local**   | `.claude/settings.local.json`                                                                     | Tu, solo in questo repository              | No (gitignored)        |

### Quando utilizzare ogni ambito

L'ambito **Managed** è per:

* Politiche di sicurezza che devono essere applicate a livello organizzativo
* Requisiti di conformità che non possono essere ignorati
* Configurazioni standardizzate distribuite da IT/DevOps

L'ambito **User** è migliore per:

* Preferenze personali che desideri ovunque (temi, impostazioni dell'editor)
* Strumenti e plugin che utilizzi in tutti i progetti
* Chiavi API e autenticazione (archiviate in modo sicuro)

L'ambito **Project** è migliore per:

* Impostazioni condivise dal team (permessi, hooks, MCP servers)
* Plugin che l'intero team dovrebbe avere
* Standardizzazione degli strumenti tra i collaboratori

L'ambito **Local** è migliore per:

* Override personali per un progetto specifico
* Test delle configurazioni prima di condividerle con il team
* Impostazioni specifiche della macchina che non funzioneranno per altri

### Come interagiscono gli ambiti

Quando la stessa impostazione è configurata in più ambiti, gli ambiti più specifici hanno la precedenza:

1. **Managed** (più alta) - non può essere ignorata da nulla
2. **Argomenti della riga di comando** - override temporanei della sessione
3. **Local** - ignora le impostazioni di progetto e utente
4. **Project** - ignora le impostazioni utente
5. **User** (più bassa) - si applica quando nient'altro specifica l'impostazione

Ad esempio, se un permesso è consentito nelle impostazioni utente ma negato nelle impostazioni di progetto, l'impostazione di progetto ha la precedenza e il permesso è bloccato.

### Cosa utilizza gli ambiti

Gli ambiti si applicano a molte funzionalità di Claude Code:

| Funzionalità    | Posizione utente          | Posizione progetto                | Posizione locale                |
| :-------------- | :------------------------ | :-------------------------------- | :------------------------------ |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | —                               |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json` (per-progetto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` o `.claude/CLAUDE.md` | —                               |

***

## File di impostazioni

Il file `settings.json` è il nostro meccanismo ufficiale per configurare Claude Code attraverso impostazioni gerarchiche:

* **Le impostazioni utente** sono definite in `~/.claude/settings.json` e si applicano a tutti i progetti.
* **Le impostazioni di progetto** vengono salvate nella directory del tuo progetto:
  * `.claude/settings.json` per le impostazioni che vengono controllate nel controllo del codice sorgente e condivise con il tuo team
  * `.claude/settings.local.json` per le impostazioni che non vengono controllate, utili per preferenze personali e sperimentazione. Claude Code configurerà git per ignorare `.claude/settings.local.json` quando viene creato.
* **Impostazioni gestite**: Per le organizzazioni che necessitano di controllo centralizzato, Claude Code supporta più meccanismi di distribuzione per le impostazioni gestite. Tutti utilizzano lo stesso formato JSON e non possono essere ignorati dalle impostazioni utente o di progetto:

  * **Impostazioni gestite dal server**: consegnate dai server di Anthropic tramite la console di amministrazione di Claude.ai. Vedi [impostazioni gestite dal server](/it/server-managed-settings).
  * **Politiche MDM/a livello di sistema operativo**: consegnate tramite la gestione nativa dei dispositivi su macOS e Windows:
    * macOS: dominio delle preferenze gestite `com.anthropic.claudecode` (distribuito tramite profili di configurazione in Jamf, Kandji o altri strumenti MDM)
    * Windows: chiave di registro `HKLM\SOFTWARE\Policies\ClaudeCode` con un valore `Settings` (REG\_SZ o REG\_EXPAND\_SZ) contenente JSON (distribuito tramite Criteri di gruppo o Intune)
    * Windows (a livello utente): `HKCU\SOFTWARE\Policies\ClaudeCode` (priorità di politica più bassa, utilizzata solo quando non esiste alcuna fonte a livello di amministratore)
  * **Basate su file**: `managed-settings.json` e `managed-mcp.json` distribuite alle directory di sistema:
    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux e WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

  Vedi [impostazioni gestite](/it/permissions#managed-only-settings) e [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration) per i dettagli.

  <Note>
    Le distribuzioni gestite possono anche limitare le **aggiunte del marketplace dei plugin** utilizzando `strictKnownMarketplaces`. Per ulteriori informazioni, vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Altre configurazioni** vengono archiviate in `~/.claude.json`. Questo file contiene le tue preferenze (tema, impostazioni di notifica, modalità editor), sessione OAuth, configurazioni dei [server MCP](/it/mcp) per gli ambiti utente e locale, stato per-progetto (strumenti consentiti, impostazioni di fiducia) e varie cache. I server MCP con ambito di progetto vengono archiviati separatamente in `.mcp.json`.

<Note>
  Claude Code crea automaticamente backup con timestamp dei file di configurazione e conserva i cinque backup più recenti per prevenire la perdita di dati.
</Note>

```JSON Esempio settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

La riga `$schema` nell'esempio sopra punta allo [schema JSON ufficiale](https://json.schemastore.org/claude-code-settings.json) per le impostazioni di Claude Code. Aggiungerlo al tuo `settings.json` abilita l'autocompletamento e la convalida inline in VS Code, Cursor e qualsiasi altro editor che supporta la convalida dello schema JSON.

### Impostazioni disponibili

`settings.json` supporta un numero di opzioni:

| Chiave                            | Descrizione                                                                                                                                                                                                                                                                                                                                                                         | Esempio                                                                 |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Script personalizzato, da eseguire in `/bin/sh`, per generare un valore di autenticazione. Questo valore verrà inviato come intestazioni `X-Api-Key` e `Authorization: Bearer` per le richieste del modello                                                                                                                                                                         | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | Le sessioni inattive per più tempo di questo periodo vengono eliminate all'avvio. L'impostazione a `0` elimina immediatamente tutte le sessioni. (predefinito: 30 giorni)                                                                                                                                                                                                           | `20`                                                                    |
| `companyAnnouncements`            | Annuncio da visualizzare agli utenti all'avvio. Se vengono forniti più annunci, verranno alternati casualmente.                                                                                                                                                                                                                                                                     | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Variabili di ambiente che verranno applicate a ogni sessione                                                                                                                                                                                                                                                                                                                        | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Personalizza l'attribuzione per i commit git e le pull request. Vedi [Impostazioni di attribuzione](#attribution-settings)                                                                                                                                                                                                                                                          | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Deprecato**: Usa `attribution` invece. Se includere la riga `co-authored-by Claude` nei commit git e nelle pull request (predefinito: `true`)                                                                                                                                                                                                                                     | `false`                                                                 |
| `includeGitInstructions`          | Includi le istruzioni integrate del flusso di lavoro di commit e PR nel prompt di sistema di Claude (predefinito: `true`). Impostare su `false` per rimuovere queste istruzioni, ad esempio quando si utilizzano le proprie skill di flusso di lavoro git. La variabile di ambiente `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` ha la precedenza su questa impostazione quando impostata | `false`                                                                 |
| `permissions`                     | Vedi la tabella sottostante per la struttura dei permessi.                                                                                                                                                                                                                                                                                                                          |                                                                         |
| `hooks`                           | Configura comandi personalizzati da eseguire agli eventi del ciclo di vita. Vedi [documentazione hooks](/it/hooks) per il formato                                                                                                                                                                                                                                                   | Vedi [hooks](/it/hooks)                                                 |
| `disableAllHooks`                 | Disabilita tutti gli [hooks](/it/hooks) e qualsiasi [riga di stato](/it/statusline) personalizzata                                                                                                                                                                                                                                                                                  | `true`                                                                  |
| `allowManagedHooksOnly`           | (Solo impostazioni gestite) Impedisci il caricamento degli hook utente, progetto e plugin. Consenti solo gli hook gestiti e gli hook SDK. Vedi [Configurazione hook](#hook-configuration)                                                                                                                                                                                           | `true`                                                                  |
| `allowedHttpHookUrls`             | Elenco di autorizzazione dei modelli di URL che gli hook HTTP possono indirizzare. Supporta `*` come carattere jolly. Quando impostato, gli hook con URL non corrispondenti vengono bloccati. Non definito = nessuna restrizione, array vuoto = blocca tutti gli hook HTTP. Gli array si uniscono tra le fonti di impostazioni. Vedi [Configurazione hook](#hook-configuration)     | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Elenco di autorizzazione dei nomi delle variabili di ambiente che gli hook HTTP possono interpolare nelle intestazioni. Quando impostato, l'`allowedEnvVars` effettivo di ogni hook è l'intersezione con questo elenco. Non definito = nessuna restrizione. Gli array si uniscono tra le fonti di impostazioni. Vedi [Configurazione hook](#hook-configuration)                     | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Solo impostazioni gestite) Impedisci alle impostazioni utente e progetto di definire regole di permesso `allow`, `ask` o `deny`. Si applicano solo le regole nelle impostazioni gestite. Vedi [Impostazioni solo gestite](/it/permissions#managed-only-settings)                                                                                                                   | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Solo impostazioni gestite) Solo `allowedMcpServers` dalle impostazioni gestite vengono rispettati. `deniedMcpServers` si unisce comunque da tutte le fonti. Gli utenti possono comunque aggiungere server MCP, ma si applica solo l'elenco di autorizzazione definito dall'amministratore. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                    | `true`                                                                  |
| `model`                           | Ignora il modello predefinito da utilizzare per Claude Code                                                                                                                                                                                                                                                                                                                         | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Limita quali modelli gli utenti possono selezionare tramite `/model`, `--model`, strumento Config o `ANTHROPIC_MODEL`. Non influisce sull'opzione Predefinito. Vedi [Limita la selezione del modello](/it/model-config#restrict-model-selection)                                                                                                                                    | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Mappa gli ID dei modelli Anthropic agli ID dei modelli specifici del provider come gli ARN del profilo di inferenza Bedrock. Ogni voce del selettore di modelli utilizza il suo valore mappato quando chiama l'API del provider. Vedi [Ignora gli ID dei modelli per versione](/it/model-config#override-model-ids-per-version)                                                     | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | Script per generare intestazioni OpenTelemetry dinamiche. Viene eseguito all'avvio e periodicamente (vedi [Intestazioni dinamiche](/it/monitoring-usage#dynamic-headers))                                                                                                                                                                                                           | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Configura una riga di stato personalizzata per visualizzare il contesto. Vedi [documentazione `statusLine`](/it/statusline)                                                                                                                                                                                                                                                         | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Configura uno script personalizzato per l'autocompletamento dei file `@`. Vedi [Impostazioni di suggerimento file](#file-suggestion-settings)                                                                                                                                                                                                                                       | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Controlla se il selettore di file `@` rispetta i modelli `.gitignore`. Quando `true` (predefinito), i file che corrispondono ai modelli `.gitignore` vengono esclusi dai suggerimenti                                                                                                                                                                                               | `false`                                                                 |
| `outputStyle`                     | Configura uno stile di output per regolare il prompt di sistema. Vedi [documentazione degli stili di output](/it/output-styles)                                                                                                                                                                                                                                                     | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Usa `claudeai` per limitare l'accesso agli account Claude.ai, `console` per limitare l'accesso agli account Claude Console (fatturazione dell'utilizzo dell'API)                                                                                                                                                                                                                    | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Specifica l'UUID di un'organizzazione per selezionarla automaticamente durante l'accesso, ignorando il passaggio di selezione dell'organizzazione. Richiede che `forceLoginMethod` sia impostato                                                                                                                                                                                    | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Approva automaticamente tutti i server MCP definiti nei file `.mcp.json` del progetto                                                                                                                                                                                                                                                                                               | `true`                                                                  |
| `enabledMcpjsonServers`           | Elenco di server MCP specifici dai file `.mcp.json` da approvare                                                                                                                                                                                                                                                                                                                    | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Elenco di server MCP specifici dai file `.mcp.json` da rifiutare                                                                                                                                                                                                                                                                                                                    | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Quando impostato in managed-settings.json, elenco di autorizzazione dei server MCP che gli utenti possono configurare. Non definito = nessuna restrizione, array vuoto = blocco. Si applica a tutti gli ambiti. L'elenco di negazione ha la precedenza. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                        | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Quando impostato in managed-settings.json, elenco di negazione dei server MCP che sono esplicitamente bloccati. Si applica a tutti gli ambiti inclusi i server gestiti. L'elenco di negazione ha la precedenza sull'elenco di autorizzazione. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                                  | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Quando impostato in managed-settings.json, elenco di autorizzazione dei marketplace dei plugin che gli utenti possono aggiungere. Non definito = nessuna restrizione, array vuoto = blocco. Si applica solo alle aggiunte del marketplace. Vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions)                                     | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Solo impostazioni gestite) Elenco di negazione delle fonti del marketplace. Le fonti bloccate vengono controllate prima del download, quindi non toccano mai il filesystem. Vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                   | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Solo impostazioni gestite) Messaggio personalizzato aggiunto all'avviso di fiducia del plugin mostrato prima dell'installazione. Usa questo per aggiungere contesto specifico dell'organizzazione, ad esempio per confermare che i plugin dal tuo marketplace interno sono controllati.                                                                                            | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Script personalizzato che modifica la directory `.aws` (vedi [configurazione avanzata delle credenziali](/it/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                     | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Script personalizzato che restituisce JSON con le credenziali AWS (vedi [configurazione avanzata delle credenziali](/it/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                          | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Abilita il [pensiero esteso](/it/common-workflows#use-extended-thinking-thinking-mode) per impostazione predefinita per tutte le sessioni. Tipicamente configurato tramite il comando `/config` piuttosto che modificato direttamente                                                                                                                                               | `true`                                                                  |
| `plansDirectory`                  | Personalizza dove vengono archiviati i file di piano. Il percorso è relativo alla radice del progetto. Predefinito: `~/.claude/plans`                                                                                                                                                                                                                                               | `"./plans"`                                                             |
| `showTurnDuration`                | Mostra i messaggi di durata del turno dopo le risposte (ad es. "Cooked for 1m 6s"). Impostare su `false` per nascondere questi messaggi                                                                                                                                                                                                                                             | `true`                                                                  |
| `spinnerVerbs`                    | Personalizza i verbi di azione mostrati nello spinner e nei messaggi di durata del turno. Impostare `mode` su `"replace"` per utilizzare solo i tuoi verbi, o `"append"` per aggiungerli ai predefiniti                                                                                                                                                                             | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Configura la lingua di risposta preferita di Claude (ad es. `"japanese"`, `"spanish"`, `"french"`). Claude risponderà in questa lingua per impostazione predefinita                                                                                                                                                                                                                 | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Canale di rilascio da seguire per gli aggiornamenti. Usa `"stable"` per una versione che è tipicamente circa una settimana vecchia e salta le versioni con regressioni importanti, o `"latest"` (predefinito) per il rilascio più recente                                                                                                                                           | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Mostra suggerimenti nello spinner mentre Claude sta lavorando. Impostare su `false` per disabilitare i suggerimenti (predefinito: `true`)                                                                                                                                                                                                                                           | `false`                                                                 |
| `spinnerTipsOverride`             | Ignora i suggerimenti dello spinner con stringhe personalizzate. `tips`: array di stringhe di suggerimento. `excludeDefault`: se `true`, mostra solo suggerimenti personalizzati; se `false` o assente, i suggerimenti personalizzati vengono uniti ai suggerimenti incorporati                                                                                                     | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Abilita la barra di avanzamento del terminale che mostra l'avanzamento nei terminali supportati come Windows Terminal e iTerm2 (predefinito: `true`)                                                                                                                                                                                                                                | `false`                                                                 |
| `prefersReducedMotion`            | Riduci o disabilita le animazioni dell'interfaccia utente (spinner, shimmer, effetti flash) per l'accessibilità                                                                                                                                                                                                                                                                     | `true`                                                                  |
| `fastModePerSessionOptIn`         | Quando `true`, la modalità veloce non persiste tra le sessioni. Ogni sessione inizia con la modalità veloce disattivata, richiedendo agli utenti di abilitarla con `/fast`. La preferenza della modalità veloce dell'utente viene comunque salvata. Vedi [Richiedi opt-in per sessione](/it/fast-mode#require-per-session-opt-in)                                                   | `true`                                                                  |
| `teammateMode`                    | Come i compagni di squadra del [team di agenti](/it/agent-teams) vengono visualizzati: `auto` (sceglie riquadri divisi in tmux o iTerm2, in-process altrimenti), `in-process` o `tmux`. Vedi [configura i team di agenti](/it/agent-teams#set-up-agent-teams)                                                                                                                       | `"in-process"`                                                          |

### Impostazioni di permesso

| Chiavi                         | Descrizione                                                                                                                                                                                                                                                                            | Esempio                                                                |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Array di regole di permesso per consentire l'uso dello strumento. Vedi [Sintassi della regola di permesso](#permission-rule-syntax) sottostante per i dettagli della corrispondenza dei modelli                                                                                        | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Array di regole di permesso per chiedere conferma all'uso dello strumento. Vedi [Sintassi della regola di permesso](#permission-rule-syntax) sottostante                                                                                                                               | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Array di regole di permesso per negare l'uso dello strumento. Usa questo per escludere file sensibili dall'accesso di Claude Code. Vedi [Sintassi della regola di permesso](#permission-rule-syntax) e [Limitazioni dei permessi Bash](/it/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Directory di lavoro](/it/permissions#working-directories) aggiuntive a cui Claude ha accesso                                                                                                                                                                                          | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | [Modalità di permesso](/it/permissions#permission-modes) predefinita all'apertura di Claude Code                                                                                                                                                                                       | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Impostare su `"disable"` per impedire l'attivazione della modalità `bypassPermissions`. Questo disabilita il flag della riga di comando `--dangerously-skip-permissions`. Vedi [impostazioni gestite](/it/permissions#managed-only-settings)                                           | `"disable"`                                                            |

### Sintassi della regola di permesso

Le regole di permesso seguono il formato `Tool` o `Tool(specifier)`. Le regole vengono valutate in ordine: prima le regole di negazione, poi di richiesta, poi di autorizzazione. La prima regola corrispondente vince.

Esempi rapidi:

| Regola                         | Effetto                                              |
| :----------------------------- | :--------------------------------------------------- |
| `Bash`                         | Corrisponde a tutti i comandi Bash                   |
| `Bash(npm run *)`              | Corrisponde ai comandi che iniziano con `npm run`    |
| `Read(./.env)`                 | Corrisponde alla lettura del file `.env`             |
| `WebFetch(domain:example.com)` | Corrisponde alle richieste di recupero a example.com |

Per il riferimento completo della sintassi delle regole, incluso il comportamento dei caratteri jolly, i modelli specifici dello strumento per Read, Edit, WebFetch, MCP e Agent, e le limitazioni di sicurezza dei modelli Bash, vedi [Sintassi della regola di permesso](/it/permissions#permission-rule-syntax).

### Impostazioni sandbox

Configura il comportamento avanzato del sandboxing. Il sandboxing isola i comandi bash dal tuo filesystem e dalla rete. Vedi [Sandboxing](/it/sandboxing) per i dettagli.

| Chiavi                            | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                       | Esempio                         |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | Abilita il sandboxing bash (macOS, Linux e WSL2). Predefinito: false                                                                                                                                                                                                                                                                                                                                              | `true`                          |
| `autoAllowBashIfSandboxed`        | Approva automaticamente i comandi bash quando sandboxed. Predefinito: true                                                                                                                                                                                                                                                                                                                                        | `true`                          |
| `excludedCommands`                | Comandi che dovrebbero essere eseguiti al di fuori della sandbox                                                                                                                                                                                                                                                                                                                                                  | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Consenti ai comandi di essere eseguiti al di fuori della sandbox tramite il parametro `dangerouslyDisableSandbox`. Quando impostato su `false`, la scappatoia `dangerouslyDisableSandbox` è completamente disabilitata e tutti i comandi devono essere sandboxed (o essere in `excludedCommands`). Utile per le politiche aziendali che richiedono un sandboxing rigoroso. Predefinito: true                      | `false`                         |
| `filesystem.allowWrite`           | Percorsi aggiuntivi dove i comandi sandboxed possono scrivere. Gli array vengono uniti in tutti gli ambiti di impostazioni: i percorsi utente, progetto e gestiti vengono combinati, non sostituiti. Anche uniti con i percorsi dalle regole di permesso `Edit(...)` allow. Vedi [prefissi di percorso](#sandbox-path-prefixes) sottostante.                                                                      | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Percorsi dove i comandi sandboxed non possono scrivere. Gli array vengono uniti in tutti gli ambiti di impostazioni. Anche uniti con i percorsi dalle regole di permesso `Edit(...)` deny.                                                                                                                                                                                                                        | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Percorsi dove i comandi sandboxed non possono leggere. Gli array vengono uniti in tutti gli ambiti di impostazioni. Anche uniti con i percorsi dalle regole di permesso `Read(...)` deny.                                                                                                                                                                                                                         | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Percorsi dei socket Unix accessibili nella sandbox (per agenti SSH, ecc.)                                                                                                                                                                                                                                                                                                                                         | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Consenti tutte le connessioni ai socket Unix nella sandbox. Predefinito: false                                                                                                                                                                                                                                                                                                                                    | `true`                          |
| `network.allowLocalBinding`       | Consenti il binding alle porte localhost (solo macOS). Predefinito: false                                                                                                                                                                                                                                                                                                                                         | `true`                          |
| `network.allowedDomains`          | Array di domini da consentire per il traffico di rete in uscita. Supporta i caratteri jolly (ad es. `*.example.com`).                                                                                                                                                                                                                                                                                             | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Solo impostazioni gestite) Solo `allowedDomains` e le regole di autorizzazione `WebFetch(domain:...)` dalle impostazioni gestite vengono rispettate. I domini dalle impostazioni utente, progetto e locale vengono ignorati. I domini non consentiti vengono bloccati automaticamente senza richiedere all'utente. I domini negati vengono comunque rispettati da tutte le fonti. Predefinito: false             | `true`                          |
| `network.httpProxyPort`           | Porta del proxy HTTP utilizzata se desideri portare il tuo proxy. Se non specificato, Claude eseguirà il suo proxy.                                                                                                                                                                                                                                                                                               | `8080`                          |
| `network.socksProxyPort`          | Porta del proxy SOCKS5 utilizzata se desideri portare il tuo proxy. Se non specificato, Claude eseguirà il suo proxy.                                                                                                                                                                                                                                                                                             | `8081`                          |
| `enableWeakerNestedSandbox`       | Abilita una sandbox più debole per ambienti Docker senza privilegi (solo Linux e WSL2). **Riduce la sicurezza.** Predefinito: false                                                                                                                                                                                                                                                                               | `true`                          |
| `enableWeakerNetworkIsolation`    | (Solo macOS) Consenti l'accesso al servizio di fiducia TLS del sistema (`com.apple.trustd.agent`) nella sandbox. Richiesto affinché gli strumenti basati su Go come `gh`, `gcloud` e `terraform` verifichino i certificati TLS quando si utilizza `httpProxyPort` con un proxy MITM e una CA personalizzata. **Riduce la sicurezza** aprendo un potenziale percorso di esfiltrazione dei dati. Predefinito: false | `true`                          |

#### Prefissi di percorso sandbox

I percorsi in `filesystem.allowWrite`, `filesystem.denyWrite` e `filesystem.denyRead` supportano questi prefissi:

| Prefisso               | Significato                                           | Esempio                                |
| :--------------------- | :---------------------------------------------------- | :------------------------------------- |
| `//`                   | Percorso assoluto dalla radice del filesystem         | `//tmp/build` diventa `/tmp/build`     |
| `~/`                   | Relativo alla directory home                          | `~/.kube` diventa `$HOME/.kube`        |
| `/`                    | Relativo alla directory del file di impostazioni      | `/build` diventa `$SETTINGS_DIR/build` |
| `./` o nessun prefisso | Percorso relativo (risolto dal runtime della sandbox) | `./output`                             |

**Esempio di configurazione:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

Le **restrizioni del filesystem e della rete** possono essere configurate in due modi che vengono uniti insieme:

* **Impostazioni `sandbox.filesystem`** (mostrate sopra): Controllano i percorsi al confine della sandbox a livello di sistema operativo. Queste restrizioni si applicano a tutti i comandi dei sottoprocessi (ad es. `kubectl`, `terraform`, `npm`), non solo agli strumenti di file di Claude.
* **Regole di permesso**: Usa le regole di autorizzazione/negazione `Edit` per controllare l'accesso allo strumento di file di Claude, le regole di negazione `Read` per bloccare le letture e le regole di autorizzazione/negazione `WebFetch` per controllare i domini di rete. I percorsi da queste regole vengono anche uniti nella configurazione della sandbox.

### Impostazioni di attribuzione

Claude Code aggiunge attribuzione ai commit git e alle pull request. Questi vengono configurati separatamente:

* I commit utilizzano i [trailer git](https://git-scm.com/docs/git-interpret-trailers) (come `Co-Authored-By`) per impostazione predefinita, che possono essere personalizzati o disabilitati
* Le descrizioni delle pull request sono testo semplice

| Chiavi   | Descrizione                                                                                                     |
| :------- | :-------------------------------------------------------------------------------------------------------------- |
| `commit` | Attribuzione per i commit git, inclusi eventuali trailer. La stringa vuota nasconde l'attribuzione del commit   |
| `pr`     | Attribuzione per le descrizioni delle pull request. La stringa vuota nasconde l'attribuzione della pull request |

**Attribuzione predefinita del commit:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Attribuzione predefinita della pull request:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Esempio:**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  L'impostazione `attribution` ha la precedenza sull'impostazione deprecata `includeCoAuthoredBy`. Per nascondere tutta l'attribuzione, impostare `commit` e `pr` su stringhe vuote.
</Note>

### Impostazioni di suggerimento file

Configura un comando personalizzato per l'autocompletamento del percorso del file `@`. Il suggerimento di file incorporato utilizza l'attraversamento veloce del filesystem, ma i monorepo di grandi dimensioni potrebbero beneficiare dell'indicizzazione specifica del progetto come un indice di file pre-costruito o strumenti personalizzati.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Il comando viene eseguito con le stesse variabili di ambiente degli [hooks](/it/hooks), incluso `CLAUDE_PROJECT_DIR`. Riceve JSON tramite stdin con un campo `query`:

```json  theme={null}
{"query": "src/comp"}
```

Restituisci i percorsi dei file separati da newline a stdout (attualmente limitati a 15):

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Esempio:**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configurazione hook

Queste impostazioni controllano quali hook possono essere eseguiti e a cosa possono accedere gli hook HTTP. L'impostazione `allowManagedHooksOnly` può essere configurata solo nelle [impostazioni gestite](#settings-files). Gli elenchi di autorizzazione degli URL e delle variabili di ambiente possono essere impostati a qualsiasi livello di impostazioni e si uniscono tra le fonti.

**Comportamento quando `allowManagedHooksOnly` è `true`:**

* Gli hook gestiti e gli hook SDK vengono caricati
* Gli hook utente, progetto e plugin vengono bloccati

**Limita gli URL degli hook HTTP:**

Limita quali URL gli hook HTTP possono indirizzare. Supporta `*` come carattere jolly per la corrispondenza. Quando l'array è definito, gli hook HTTP che indirizzano URL non corrispondenti vengono silenziosamente bloccati.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Limita le variabili di ambiente degli hook HTTP:**

Limita quali nomi di variabili di ambiente gli hook HTTP possono interpolare nei valori delle intestazioni. L'`allowedEnvVars` effettivo di ogni hook è l'intersezione del suo elenco e di questa impostazione.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Precedenza delle impostazioni

Le impostazioni si applicano in ordine di precedenza. Dal più alto al più basso:

1. **Impostazioni gestite** ([gestite dal server](/it/server-managed-settings), [politiche MDM/a livello di sistema operativo](#configuration-scopes) o [impostazioni gestite](/it/settings#settings-files))
   * Politiche distribuite da IT tramite consegna dal server, profili di configurazione MDM, politiche di registro o file di impostazioni gestite
   * Non possono essere ignorate da nessun altro livello, inclusi gli argomenti della riga di comando
   * All'interno del livello gestito, la precedenza è: gestite dal server > politiche MDM/a livello di sistema operativo > `managed-settings.json` > registro HKCU (solo Windows). Viene utilizzata una sola fonte gestita; le fonti non si uniscono.

2. **Argomenti della riga di comando**
   * Override temporanei per una sessione specifica

3. **Impostazioni di progetto locale** (`.claude/settings.local.json`)
   * Impostazioni personali specifiche del progetto

4. **Impostazioni di progetto condivise** (`.claude/settings.json`)
   * Impostazioni di progetto condivise dal team nel controllo del codice sorgente

5. **Impostazioni utente** (`~/.claude/settings.json`)
   * Impostazioni globali personali

Questa gerarchia garantisce che le politiche organizzative siano sempre applicate mentre consente comunque ai team e agli individui di personalizzare la loro esperienza.

Ad esempio, se le tue impostazioni utente consentono `Bash(npm run *)` ma le impostazioni condivise di un progetto lo negano, l'impostazione di progetto ha la precedenza e il comando viene bloccato.

<Note>
  **Gli array di impostazioni si uniscono tra gli ambiti.** Quando la stessa impostazione con valore array (come `sandbox.filesystem.allowWrite` o `permissions.allow`) appare in più ambiti, gli array vengono **concatenati e deduplicati**, non sostituiti. Ciò significa che gli ambiti con priorità inferiore possono aggiungere voci senza ignorare quelle impostate da ambiti con priorità più alta, e viceversa. Ad esempio, se le impostazioni gestite impostano `allowWrite` su `["//opt/company-tools"]` e un utente aggiunge `["~/.kube"]`, entrambi i percorsi sono inclusi nella configurazione finale.
</Note>

### Verifica le impostazioni attive

Esegui `/status` all'interno di Claude Code per vedere quali fonti di impostazioni sono attive e da dove provengono. L'output mostra ogni livello di configurazione (gestito, utente, progetto) insieme alla sua origine, come `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)` o `Enterprise managed settings (file)`. Se un file di impostazioni contiene errori, `/status` segnala il problema in modo che tu possa risolverlo.

### Punti chiave sul sistema di configurazione

* **File di memoria (`CLAUDE.md`)**: Contengono istruzioni e contesto che Claude carica all'avvio
* **File di impostazioni (JSON)**: Configurano permessi, variabili di ambiente e comportamento dello strumento
* **Skills**: Prompt personalizzati che possono essere invocati con `/skill-name` o caricati automaticamente da Claude
* **Server MCP**: Estendono Claude Code con strumenti e integrazioni aggiuntivi
* **Precedenza**: Le configurazioni di livello superiore (Managed) ignorano quelle di livello inferiore (User/Project)
* **Ereditarietà**: Le impostazioni vengono unite, con impostazioni più specifiche che si aggiungono o ignorano quelle più ampie

### Prompt di sistema

Il prompt di sistema interno di Claude Code non è pubblicato. Per aggiungere istruzioni personalizzate, usa i file `CLAUDE.md` o il flag `--append-system-prompt`.

### Esclusione di file sensibili

Per impedire a Claude Code di accedere a file contenenti informazioni sensibili come chiavi API, segreti e file di ambiente, usa l'impostazione `permissions.deny` nel tuo file `.claude/settings.json`:

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Questo sostituisce la configurazione deprecata `ignorePatterns`. I file che corrispondono a questi modelli vengono esclusi dalla scoperta dei file e dai risultati della ricerca, e le operazioni di lettura su questi file vengono negate.

## Configurazione subagent

Claude Code supporta subagent AI personalizzati che possono essere configurati sia a livello utente che di progetto. Questi subagent vengono archiviati come file Markdown con frontmatter YAML:

* **Subagent utente**: `~/.claude/agents/` - Disponibili in tutti i tuoi progetti
* **Subagent di progetto**: `.claude/agents/` - Specifici del tuo progetto e possono essere condivisi con il tuo team

I file subagent definiscono assistenti AI specializzati con prompt personalizzati e permessi degli strumenti. Scopri di più sulla creazione e l'utilizzo dei subagent nella [documentazione dei subagent](/it/sub-agents).

## Configurazione dei plugin

Claude Code supporta un sistema di plugin che ti consente di estendere la funzionalità con skill, agenti, hook e server MCP. I plugin vengono distribuiti tramite marketplace e possono essere configurati sia a livello utente che di repository.

### Impostazioni dei plugin

Impostazioni relative ai plugin in `settings.json`:

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

Controlla quali plugin sono abilitati. Formato: `"plugin-name@marketplace-name": true/false`

**Ambiti**:

* **Impostazioni utente** (`~/.claude/settings.json`): Preferenze personali dei plugin
* **Impostazioni di progetto** (`.claude/settings.json`): Plugin specifici del progetto condivisi con il team
* **Impostazioni locali** (`.claude/settings.local.json`): Override per macchina (non committati)

**Esempio**:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Definisce marketplace aggiuntivi che dovrebbero essere resi disponibili per il repository. Tipicamente utilizzato nelle impostazioni a livello di repository per garantire che i membri del team abbiano accesso alle fonti di plugin richieste.

**Quando un repository include `extraKnownMarketplaces`**:

1. I membri del team vengono invitati a installare il marketplace quando fidano della cartella
2. I membri del team vengono quindi invitati a installare i plugin da quel marketplace
3. Gli utenti possono saltare i marketplace o i plugin indesiderati (archiviati nelle impostazioni utente)
4. L'installazione rispetta i confini di fiducia e richiede il consenso esplicito

**Esempio**:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Tipi di fonte del marketplace**:

* `github`: Repository GitHub (utilizza `repo`)
* `git`: Qualsiasi URL git (utilizza `url`)
* `directory`: Percorso del filesystem locale (utilizza `path`, solo per lo sviluppo)
* `hostPattern`: Modello regex per abbinare gli host del marketplace (utilizza `hostPattern`)

#### `strictKnownMarketplaces`

**Solo impostazioni gestite**: Controlla quali marketplace dei plugin gli utenti possono aggiungere. Questa impostazione può essere configurata solo nelle [impostazioni gestite](/it/settings#settings-files) e fornisce agli amministratori un controllo rigoroso sulle fonti del marketplace.

**Posizioni dei file di impostazioni gestite**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux e WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Caratteristiche chiave**:

* Disponibile solo nelle impostazioni gestite (`managed-settings.json`)
* Non può essere ignorato dalle impostazioni utente o progetto (precedenza più alta)
* Applicato PRIMA delle operazioni di rete/filesystem (le fonti bloccate non vengono mai eseguite)
* Utilizza la corrispondenza esatta per le specifiche di origine (incluso `ref`, `path` per le fonti git), tranne `hostPattern`, che utilizza la corrispondenza regex

**Comportamento dell'elenco di autorizzazione**:

* `undefined` (predefinito): Nessuna restrizione - gli utenti possono aggiungere qualsiasi marketplace
* Array vuoto `[]`: Blocco completo - gli utenti non possono aggiungere nuovi marketplace
* Elenco di fonti: Gli utenti possono aggiungere solo i marketplace che corrispondono esattamente

**Tutti i tipi di fonte supportati**:

L'elenco di autorizzazione supporta sette tipi di fonte del marketplace. La maggior parte delle fonti utilizza la corrispondenza esatta, mentre `hostPattern` utilizza la corrispondenza regex rispetto all'host del marketplace.

1. **Repository GitHub**:

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Campi: `repo` (obbligatorio), `ref` (facoltativo: ramo/tag/SHA), `path` (facoltativo: sottodirectory)

2. **Repository Git**:

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Campi: `url` (obbligatorio), `ref` (facoltativo: ramo/tag/SHA), `path` (facoltativo: sottodirectory)

3. **Marketplace basati su URL**:

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Campi: `url` (obbligatorio), `headers` (facoltativo: intestazioni HTTP per l'accesso autenticato)

<Note>
  I marketplace basati su URL scaricano solo il file `marketplace.json`. Non scaricano i file dei plugin dal server. I plugin nei marketplace basati su URL devono utilizzare fonti esterne (URL GitHub, npm o git) piuttosto che percorsi relativi. Per i plugin con percorsi relativi, utilizza un marketplace basato su Git. Vedi [Troubleshooting](/it/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) per i dettagli.
</Note>

4. **Pacchetti NPM**:

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Campi: `package` (obbligatorio, supporta pacchetti con scope)

5. **Percorsi di file**:

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Campi: `path` (obbligatorio: percorso assoluto al file marketplace.json)

6. **Percorsi di directory**:

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Campi: `path` (obbligatorio: percorso assoluto alla directory contenente `.claude-plugin/marketplace.json`)

7. **Corrispondenza del modello di host**:

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Campi: `hostPattern` (obbligatorio: modello regex per abbinare l'host del marketplace)

Utilizza la corrispondenza del modello di host quando desideri consentire tutti i marketplace da un host specifico senza enumerare ogni repository individualmente. Questo è utile per le organizzazioni con server GitHub Enterprise o GitLab interni dove gli sviluppatori creano i propri marketplace.

Estrazione dell'host per tipo di fonte:

* `github`: corrisponde sempre a `github.com`
* `git`: estrae il nome host dall'URL (supporta sia i formati HTTPS che SSH)
* `url`: estrae il nome host dall'URL
* `npm`, `file`, `directory`: non supportati per la corrispondenza del modello di host

**Esempi di configurazione**:

Esempio: consenti solo marketplace specifici:

```json  theme={null}
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
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Esempio - Disabilita tutte le aggiunte del marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Esempio: consenti tutti i marketplace da un server git interno:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Requisiti di corrispondenza esatta**:

Le fonti del marketplace devono corrispondere **esattamente** affinché l'aggiunta di un utente sia consentita. Per le fonti basate su git (`github` e `git`), questo include tutti i campi facoltativi:

* Il `repo` o `url` deve corrispondere esattamente
* Il campo `ref` deve corrispondere esattamente (o entrambi non essere definiti)
* Il campo `path` deve corrispondere esattamente (o entrambi non essere definiti)

Esempi di fonti che **NON corrispondono**:

```json  theme={null}
// Queste sono DIVERSE fonti:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Anche queste sono DIVERSE:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Confronto con `extraKnownMarketplaces`**:

| Aspetto                  | `strictKnownMarketplaces`                 | `extraKnownMarketplaces`                        |
| ------------------------ | ----------------------------------------- | ----------------------------------------------- |
| **Scopo**                | Applicazione della politica organizzativa | Comodità del team                               |
| **File di impostazioni** | Solo `managed-settings.json`              | Qualsiasi file di impostazioni                  |
| **Comportamento**        | Blocca le aggiunte non autorizzate        | Installa automaticamente i marketplace mancanti |
| **Quando applicato**     | Prima delle operazioni di rete/filesystem | Dopo il prompt di fiducia dell'utente           |
| **Può essere ignorato**  | No (precedenza più alta)                  | Sì (dalle impostazioni di precedenza più alta)  |
| **Formato della fonte**  | Oggetto di fonte diretto                  | Marketplace denominato con fonte nidificata     |
| **Caso d'uso**           | Conformità, restrizioni di sicurezza      | Onboarding, standardizzazione                   |

**Differenza di formato**:

`strictKnownMarketplaces` utilizza oggetti di fonte diretti:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` richiede marketplace denominati:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Note importanti**:

* Le restrizioni vengono controllate PRIMA di qualsiasi richiesta di rete o operazione del filesystem
* Quando bloccato, gli utenti vedono messaggi di errore chiari che indicano che la fonte è bloccata dalla politica gestita
* La restrizione si applica solo all'aggiunta di NUOVI marketplace; i marketplace precedentemente installati rimangono accessibili
* Le impostazioni gestite hanno la precedenza più alta e non possono essere ignorate

Vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions) per la documentazione rivolta agli utenti.

### Gestione dei plugin

Usa il comando `/plugin` per gestire i plugin in modo interattivo:

* Sfoglia i plugin disponibili dai marketplace
* Installa/disinstalla plugin
* Abilita/disabilita plugin
* Visualizza i dettagli del plugin (comandi, agenti, hook forniti)
* Aggiungi/rimuovi marketplace

Scopri di più sul sistema di plugin nella [documentazione dei plugin](/it/plugins).

## Variabili di ambiente

Claude Code supporta le seguenti variabili di ambiente per controllare il suo comportamento:

<Note>
  Tutte le variabili di ambiente possono anche essere configurate in [`settings.json`](#available-settings). Questo è utile come modo per impostare automaticamente le variabili di ambiente per ogni sessione, o per distribuire un insieme di variabili di ambiente per l'intero team o organizzazione.
</Note>

| Variabile                                      | Scopo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | Chiave API inviata come intestazione `X-Api-Key`, tipicamente per l'SDK Claude (per l'utilizzo interattivo, esegui `/login`)                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `ANTHROPIC_AUTH_TOKEN`                         | Valore personalizzato per l'intestazione `Authorization` (il valore che imposti qui sarà preceduto da `Bearer `)                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | Intestazioni personalizzate da aggiungere alle richieste (formato `Name: Value`, separato da newline per più intestazioni)                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | Vedi [Configurazione del modello](/it/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | Vedi [Configurazione del modello](/it/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | Vedi [Configurazione del modello](/it/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Chiave API per l'autenticazione Microsoft Foundry (vedi [Microsoft Foundry](/it/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | URL di base completo per la risorsa Foundry (ad esempio, `https://my-resource.services.ai.azure.com/anthropic`). Alternativa a `ANTHROPIC_FOUNDRY_RESOURCE` (vedi [Microsoft Foundry](/it/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                            |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Nome della risorsa Foundry (ad esempio, `my-resource`). Obbligatorio se `ANTHROPIC_FOUNDRY_BASE_URL` non è impostato (vedi [Microsoft Foundry](/it/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_MODEL`                              | Nome dell'impostazione del modello da utilizzare (vedi [Configurazione del modello](/it/model-config#environment-variables))                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[DEPRECATO] Nome del [modello di classe Haiku per attività in background](/it/costs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Ignora la regione AWS per il modello di classe Haiku quando si utilizza Bedrock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Chiave API Bedrock per l'autenticazione (vedi [Chiavi API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | Timeout predefinito per i comandi bash a lunga esecuzione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | Numero massimo di caratteri negli output bash prima che vengano troncati al centro                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `BASH_MAX_TIMEOUT_MS`                          | Timeout massimo che il modello può impostare per i comandi bash a lunga esecuzione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | Imposta la percentuale della capacità del contesto (1-100) a cui viene attivata la compattazione automatica. Per impostazione predefinita, la compattazione automatica viene attivata a circa il 95% della capacità. Usa valori inferiori come `50` per compattare prima. I valori superiori alla soglia predefinita non hanno effetto. Si applica sia alle conversazioni principali che ai subagent. Questa percentuale si allinea con il campo `context_window.used_percentage` disponibile nella [riga di stato](/it/statusline)                                                      |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | Ritorna alla directory di lavoro originale dopo ogni comando Bash                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | UUID dell'account per l'utente autenticato. Utilizzato dai chiamanti dell'SDK per fornire informazioni sull'account in modo sincrono, evitando una condizione di gara in cui gli eventi di telemetria iniziali mancano di metadati dell'account. Richiede che `CLAUDE_CODE_USER_EMAIL` e `CLAUDE_CODE_ORGANIZATION_UUID` siano anche impostati                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Impostare su `1` per caricare i file CLAUDE.md dalle directory specificate con `--add-dir`. Per impostazione predefinita, le directory aggiuntive non caricano file di memoria                                                                                                                                                                                                                                                                                                                                                                                                           | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | Intervallo in millisecondi a cui le credenziali dovrebbero essere aggiornate (quando si utilizza `apiKeyHelper`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | Percorso al file del certificato client per l'autenticazione mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | Percorso al file della chiave privata del client per l'autenticazione mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | Passphrase per `CLAUDE_CODE_CLIENT_KEY` crittografato (facoltativo)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | Impostare su `1` per disabilitare il supporto della [finestra di contesto 1M](/it/model-config#extended-context). Quando impostato, le varianti del modello 1M non sono disponibili nel selettore di modelli. Utile per gli ambienti aziendali con requisiti di conformità                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Impostare su `1` per disabilitare il [ragionamento adattivo](/it/model-config#adjust-effort-level) per Opus 4.6 e Sonnet 4.6. Quando disabilitato, questi modelli tornano al budget di pensiero fisso controllato da `MAX_THINKING_TOKENS`                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | Impostare su `1` per disabilitare la [memoria automatica](/it/memory#auto-memory). Impostare su `0` per forzare la memoria automatica durante il rollout graduale. Quando disabilitato, Claude non crea o carica file di memoria automatica                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Impostare su `1` per rimuovere le istruzioni integrate del flusso di lavoro di commit e PR dal prompt di sistema di Claude. Utile quando si utilizzano le proprie skill di flusso di lavoro git. Ha la precedenza sull'impostazione [`includeGitInstructions`](#available-settings) quando impostato                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | Impostare su `1` per disabilitare tutta la funzionalità di attività in background, incluso il parametro `run_in_background` su strumenti Bash e subagent, auto-backgrounding e la scorciatoia Ctrl+B                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | Impostare su `1` per disabilitare le [attività pianificate](/it/scheduled-tasks). La skill `/loop` e gli strumenti cron diventano non disponibili e qualsiasi attività già pianificata smette di attivarsi, incluse le attività che sono già in esecuzione a metà sessione                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Impostare su `1` per disabilitare le intestazioni `anthropic-beta` specifiche dell'API Anthropic. Usa questo se riscontri problemi come "Unexpected value(s) for the `anthropic-beta` header" quando utilizzi un gateway LLM con provider di terze parti                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | Impostare su `1` per disabilitare la [modalità veloce](/it/fast-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | Impostare su `1` per disabilitare i sondaggi sulla qualità della sessione "How is Claude doing?". Anche disabilitato quando si utilizzano provider di terze parti o quando la telemetria è disabilitata. Vedi [Sondaggi sulla qualità della sessione](/it/data-usage#session-quality-surveys)                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | Equivalente all'impostazione di `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING` e `DISABLE_TELEMETRY`                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | Impostare su `1` per disabilitare gli aggiornamenti automatici del titolo del terminale in base al contesto della conversazione                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | Imposta il livello di sforzo per i modelli supportati. Valori: `low`, `medium`, `high`. Lo sforzo inferiore è più veloce e più economico, lo sforzo superiore fornisce un ragionamento più profondo. Supportato su Opus 4.6 e Sonnet 4.6. Vedi [Regola il livello di sforzo](/it/model-config#adjust-effort-level)                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | Impostare su `false` per disabilitare i suggerimenti di prompt (l'interruttore "Prompt suggestions" in `/config`). Queste sono le previsioni grigie che appaiono nel tuo input di prompt dopo che Claude risponde. Vedi [Suggerimenti di prompt](/it/interactive-mode#prompt-suggestions)                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | Impostare su `false` per tornare temporaneamente all'elenco TODO precedente invece del sistema di tracciamento delle attività. Predefinito: `true`. Vedi [Elenco attività](/it/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | Impostare su `1` per abilitare la raccolta di dati OpenTelemetry per metriche e registrazione. Obbligatorio prima di configurare gli esportatori OTel. Vedi [Monitoraggio](/it/monitoring-usage)                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | Tempo in millisecondi da attendere dopo che il ciclo di query diventa inattivo prima di uscire automaticamente. Utile per flussi di lavoro automatizzati e script che utilizzano la modalità SDK                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | Impostare su `1` per abilitare i [team di agenti](/it/agent-teams). I team di agenti sono sperimentali e disabilitati per impostazione predefinita                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | Ignora il limite di token predefinito per le letture di file. Utile quando è necessario leggere file più grandi per intero                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Impostare su `1` per nascondere il tuo indirizzo email e il nome dell'organizzazione dall'interfaccia utente di Claude Code. Utile quando si trasmette in streaming o si registra                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | Salta l'installazione automatica delle estensioni IDE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | Imposta il numero massimo di token di output per la maggior parte delle richieste. Predefinito: 32.000. Massimo: 64.000. L'aumento di questo valore riduce la finestra di contesto effettiva disponibile prima che venga attivata la [compattazione automatica](/it/costs#reduce-token-usage).                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | UUID dell'organizzazione per l'utente autenticato. Utilizzato dai chiamanti dell'SDK per fornire informazioni sull'account in modo sincrono. Richiede che `CLAUDE_CODE_ACCOUNT_UUID` e `CLAUDE_CODE_USER_EMAIL` siano anche impostati                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | Intervallo per l'aggiornamento delle intestazioni OpenTelemetry dinamiche in millisecondi (predefinito: 1740000 / 29 minuti). Vedi [Intestazioni dinamiche](/it/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | Impostato automaticamente su `true` sui compagni di squadra del [team di agenti](/it/agent-teams) che richiedono l'approvazione del piano. Sola lettura: impostato da Claude Code quando genera i compagni di squadra. Vedi [richiedi approvazione del piano](/it/agent-teams#require-plan-approval-for-teammates)                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | Timeout in millisecondi per le operazioni git durante l'installazione o l'aggiornamento dei plugin (predefinito: 120000). Aumenta questo valore per repository di grandi dimensioni o connessioni di rete lente. Vedi [Le operazioni Git scadono](/it/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | Impostare su `true` per consentire al proxy di eseguire la risoluzione DNS invece del chiamante. Opt-in per gli ambienti in cui il proxy dovrebbe gestire la risoluzione del nome host                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SHELL`                            | Ignora il rilevamento automatico della shell. Utile quando la tua shell di accesso differisce dalla tua shell di lavoro preferita (ad esempio, `bash` vs `zsh`)                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | Prefisso del comando per avvolgere tutti i comandi bash (ad esempio, per la registrazione o il controllo). Esempio: `/path/to/logger.sh` eseguirà `/path/to/logger.sh <command>`                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_SIMPLE`                           | Impostare su `1` per eseguire con un prompt di sistema minimo e solo gli strumenti Bash, lettura di file e modifica di file. Disabilita gli strumenti MCP, gli allegati, gli hook e i file CLAUDE.md                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Salta l'autenticazione AWS per Bedrock (ad esempio, quando si utilizza un gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Salta l'autenticazione Azure per Microsoft Foundry (ad esempio, quando si utilizza un gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Salta l'autenticazione Google per Vertex (ad esempio, quando si utilizza un gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | Vedi [Configurazione del modello](/it/model-config)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | Condividi un elenco di attività tra le sessioni. Imposta lo stesso ID in più istanze di Claude Code per coordinare un elenco di attività condiviso. Vedi [Elenco attività](/it/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_TEAM_NAME`                        | Nome del team di agenti a cui appartiene questo compagno di squadra. Impostato automaticamente sui membri del [team di agenti](/it/agent-teams)                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_TMPDIR`                           | Ignora la directory temporanea utilizzata per i file temporanei interni. Claude Code aggiunge `/claude/` a questo percorso. Predefinito: `/tmp` su Unix/macOS, `os.tmpdir()` su Windows                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_USER_EMAIL`                       | Indirizzo email per l'utente autenticato. Utilizzato dai chiamanti dell'SDK per fornire informazioni sull'account in modo sincrono. Richiede che `CLAUDE_CODE_ACCOUNT_UUID` e `CLAUDE_CODE_ORGANIZATION_UUID` siano anche impostati                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | Usa [Bedrock](/it/amazon-bedrock)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | Usa [Microsoft Foundry](/it/microsoft-foundry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_USE_VERTEX`                       | Usa [Vertex](/it/google-vertex-ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CONFIG_DIR`                            | Personalizza dove Claude Code archivia i suoi file di configurazione e dati                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `DISABLE_AUTOUPDATER`                          | Impostare su `1` per disabilitare gli aggiornamenti automatici.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `DISABLE_BUG_COMMAND`                          | Impostare su `1` per disabilitare il comando `/bug`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `DISABLE_COST_WARNINGS`                        | Impostare su `1` per disabilitare i messaggi di avviso sui costi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_ERROR_REPORTING`                      | Impostare su `1` per rinunciare alla segnalazione degli errori di Sentry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `DISABLE_INSTALLATION_CHECKS`                  | Impostare su `1` per disabilitare gli avvisi di installazione. Usa solo quando gestisci manualmente la posizione di installazione, poiché questo può mascherare i problemi con le installazioni standard                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | Impostare su `1` per disabilitare le chiamate del modello per percorsi non critici come il testo di sapore                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `DISABLE_PROMPT_CACHING`                       | Impostare su `1` per disabilitare il caching dei prompt per tutti i modelli (ha la precedenza sulle impostazioni per modello)                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Impostare su `1` per disabilitare il caching dei prompt per i modelli Haiku                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Impostare su `1` per disabilitare il caching dei prompt per i modelli Opus                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Impostare su `1` per disabilitare il caching dei prompt per i modelli Sonnet                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_TELEMETRY`                            | Impostare su `1` per rinunciare alla telemetria Statsig (nota che gli eventi Statsig non includono dati utente come codice, percorsi di file o comandi bash)                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Impostare su `false` per disabilitare i [server MCP di claude.ai](/it/mcp#use-mcp-servers-from-claudeai) in Claude Code. Abilitato per impostazione predefinita per gli utenti connessi                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `ENABLE_TOOL_SEARCH`                           | Controlla la [ricerca degli strumenti MCP](/it/mcp#scale-with-mcp-tool-search). Valori: `auto` (predefinito, abilita al 10% del contesto), `auto:N` (soglia personalizzata, ad es. `auto:5` per il 5%), `true` (sempre attivo), `false` (disabilitato)                                                                                                                                                                                                                                                                                                                                   |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | Impostare su `true` per forzare gli aggiornamenti automatici dei plugin anche quando l'auto-updater principale è disabilitato tramite `DISABLE_AUTOUPDATER`                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `HTTP_PROXY`                                   | Specifica il server proxy HTTP per le connessioni di rete                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `HTTPS_PROXY`                                  | Specifica il server proxy HTTPS per le connessioni di rete                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `IS_DEMO`                                      | Impostare su `true` per abilitare la modalità demo: nasconde l'email e l'organizzazione dall'interfaccia utente, salta l'onboarding e nasconde i comandi interni. Utile per la trasmissione in streaming o la registrazione di sessioni                                                                                                                                                                                                                                                                                                                                                  |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | Numero massimo di token consentiti nelle risposte dello strumento MCP. Claude Code visualizza un avviso quando l'output supera 10.000 token (predefinito: 25000)                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `MAX_THINKING_TOKENS`                          | Ignora il budget del [pensiero esteso](https://platform.claude.com/docs/en/build-with-claude/extended-thinking). Il pensiero è abilitato al budget massimo (31.999 token) per impostazione predefinita. Usa questo per limitare il budget (ad esempio, `MAX_THINKING_TOKENS=10000`) o disabilitare completamente il pensiero (`MAX_THINKING_TOKENS=0`). Per Opus 4.6, la profondità del pensiero è controllata dal [livello di sforzo](/it/model-config#adjust-effort-level) invece, e questa variabile viene ignorata a meno che non sia impostata su `0` per disabilitare il pensiero. |     |
| `MCP_CLIENT_SECRET`                            | Segreto del client OAuth per i server MCP che richiedono [credenziali pre-configurate](/it/mcp#use-pre-configured-oauth-credentials). Evita il prompt interattivo quando si aggiunge un server con `--client-secret`                                                                                                                                                                                                                                                                                                                                                                     |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | Porta fissa per il callback di reindirizzamento OAuth, come alternativa a `--callback-port` quando si aggiunge un server MCP con [credenziali pre-configurate](/it/mcp#use-pre-configured-oauth-credentials)                                                                                                                                                                                                                                                                                                                                                                             |     |
| `MCP_TIMEOUT`                                  | Timeout in millisecondi per l'avvio del server MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `MCP_TOOL_TIMEOUT`                             | Timeout in millisecondi per l'esecuzione dello strumento MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `NO_PROXY`                                     | Elenco di domini e IP a cui le richieste verranno emesse direttamente, ignorando il proxy                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | Ignora il budget dei caratteri per i metadati della skill mostrati allo [strumento Skill](/it/skills#control-who-invokes-a-skill). Il budget si ridimensiona dinamicamente al 2% della finestra di contesto, con un fallback di 16.000 caratteri. Nome legacy mantenuto per la compatibilità all'indietro                                                                                                                                                                                                                                                                                |     |
| `USE_BUILTIN_RIPGREP`                          | Impostare su `0` per utilizzare il `rg` installato dal sistema invece del `rg` incluso con Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Ignora la regione per Claude 3.5 Haiku quando si utilizza Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Ignora la regione per Claude 3.7 Sonnet quando si utilizza Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Ignora la regione per Claude 4.0 Opus quando si utilizza Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Ignora la regione per Claude 4.0 Sonnet quando si utilizza Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Ignora la regione per Claude 4.1 Opus quando si utilizza Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |

## Strumenti disponibili per Claude

Claude Code ha accesso a un insieme di strumenti potenti che lo aiutano a comprendere e modificare la tua base di codice:

| Strumento                | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Permesso richiesto |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| **Agent**                | Genera un [subagent](/it/sub-agents) con la sua finestra di contesto per gestire un'attività                                                                                                                                                                                                                                                                                                                                                                   | No                 |
| **AskUserQuestion**      | Pone domande a scelta multipla per raccogliere requisiti o chiarire l'ambiguità                                                                                                                                                                                                                                                                                                                                                                                | No                 |
| **Bash**                 | Esegue comandi shell nel tuo ambiente. Vedi [Comportamento dello strumento Bash](#bash-tool-behavior)                                                                                                                                                                                                                                                                                                                                                          | Sì                 |
| **CronCreate**           | Pianifica un prompt ricorrente o una tantum all'interno della sessione corrente (scompare quando Claude esce). Vedi [attività pianificate](/it/scheduled-tasks)                                                                                                                                                                                                                                                                                                | No                 |
| **CronDelete**           | Annulla un'attività pianificata per ID                                                                                                                                                                                                                                                                                                                                                                                                                         | No                 |
| **CronList**             | Elenca tutte le attività pianificate nella sessione                                                                                                                                                                                                                                                                                                                                                                                                            | No                 |
| **Edit**                 | Effettua modifiche mirate a file specifici                                                                                                                                                                                                                                                                                                                                                                                                                     | Sì                 |
| **EnterPlanMode**        | Passa alla modalità piano per progettare un approccio prima di codificare                                                                                                                                                                                                                                                                                                                                                                                      | No                 |
| **EnterWorktree**        | Crea un [git worktree](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolato e vi entra                                                                                                                                                                                                                                                                                                                                           | No                 |
| **ExitPlanMode**         | Presenta un piano per l'approvazione ed esce dalla modalità piano                                                                                                                                                                                                                                                                                                                                                                                              | Sì                 |
| **ExitWorktree**         | Esce da una sessione worktree e ritorna alla directory originale                                                                                                                                                                                                                                                                                                                                                                                               | No                 |
| **Glob**                 | Trova file in base alla corrispondenza dei modelli                                                                                                                                                                                                                                                                                                                                                                                                             | No                 |
| **Grep**                 | Cerca modelli nei contenuti dei file                                                                                                                                                                                                                                                                                                                                                                                                                           | No                 |
| **ListMcpResourcesTool** | Elenca le risorse esposte dai [server MCP](/it/mcp) connessi                                                                                                                                                                                                                                                                                                                                                                                                   | No                 |
| **LSP**                  | Intelligenza del codice tramite server di linguaggio. Segnala automaticamente errori di tipo e avvisi dopo le modifiche ai file. Supporta anche operazioni di navigazione: salta alle definizioni, trova riferimenti, ottieni informazioni sul tipo, elenca i simboli, trova implementazioni, traccia gerarchie di chiamate. Richiede un [plugin di intelligenza del codice](/it/discover-plugins#code-intelligence) e il suo binario del server di linguaggio | No                 |
| **NotebookEdit**         | Modifica le celle del notebook Jupyter                                                                                                                                                                                                                                                                                                                                                                                                                         | Sì                 |
| **Read**                 | Legge il contenuto dei file                                                                                                                                                                                                                                                                                                                                                                                                                                    | No                 |
| **ReadMcpResourceTool**  | Legge una risorsa MCP specifica per URI                                                                                                                                                                                                                                                                                                                                                                                                                        | No                 |
| **Skill**                | Esegue una [skill](/it/skills#control-who-invokes-a-skill) all'interno della conversazione principale                                                                                                                                                                                                                                                                                                                                                          | Sì                 |
| **TaskCreate**           | Crea una nuova attività nell'elenco delle attività                                                                                                                                                                                                                                                                                                                                                                                                             | No                 |
| **TaskGet**              | Recupera i dettagli completi per un'attività specifica                                                                                                                                                                                                                                                                                                                                                                                                         | No                 |
| **TaskList**             | Elenca tutte le attività con il loro stato attuale                                                                                                                                                                                                                                                                                                                                                                                                             | No                 |
| **TaskOutput**           | Recupera l'output da un'attività in background                                                                                                                                                                                                                                                                                                                                                                                                                 | No                 |
| **TaskStop**             | Uccide un'attività in esecuzione per ID                                                                                                                                                                                                                                                                                                                                                                                                                        | No                 |
| **TaskUpdate**           | Aggiorna lo stato dell'attività, le dipendenze, i dettagli o elimina le attività                                                                                                                                                                                                                                                                                                                                                                               | No                 |
| **TodoWrite**            | Gestisce l'elenco di controllo delle attività della sessione. Disponibile in modalità non interattiva e nell'[SDK Agent](/it/headless); le sessioni interattive utilizzano TaskCreate, TaskGet, TaskList e TaskUpdate                                                                                                                                                                                                                                          | No                 |
| **ToolSearch**           | Cerca e carica gli strumenti differiti quando la [ricerca degli strumenti](/it/mcp#scale-with-mcp-tool-search) è abilitata                                                                                                                                                                                                                                                                                                                                     | No                 |
| **WebFetch**             | Recupera il contenuto da un URL specificato                                                                                                                                                                                                                                                                                                                                                                                                                    | Sì                 |
| **WebSearch**            | Esegue ricerche web                                                                                                                                                                                                                                                                                                                                                                                                                                            | Sì                 |
| **Write**                | Crea o sovrascrivi file                                                                                                                                                                                                                                                                                                                                                                                                                                        | Sì                 |

Le regole di permesso possono essere configurate utilizzando `/allowed-tools` o nelle [impostazioni di permesso](/it/settings#available-settings). Vedi anche [Regole di permesso specifiche dello strumento](/it/permissions#tool-specific-permission-rules).

### Comportamento dello strumento Bash

Lo strumento Bash esegue comandi shell con il seguente comportamento di persistenza:

* **La directory di lavoro persiste**: Quando Claude cambia la directory di lavoro (ad esempio, `cd /path/to/dir`), i successivi comandi Bash verranno eseguiti in quella directory. Puoi usare `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` per ripristinare la directory del progetto dopo ogni comando.
* **Le variabili di ambiente NON persistono**: Le variabili di ambiente impostate in un comando Bash (ad esempio, `export MY_VAR=value`) **non** sono disponibili nei successivi comandi Bash. Ogni comando Bash viene eseguito in un ambiente shell fresco.

Per rendere disponibili le variabili di ambiente nei comandi Bash, hai **tre opzioni**:

**Opzione 1: Attiva l'ambiente prima di avviare Claude Code** (approccio più semplice)

Attiva il tuo ambiente virtuale nel tuo terminale prima di avviare Claude Code:

```bash  theme={null}
conda activate myenv
# o: source /path/to/venv/bin/activate
claude
```

Questo funziona per gli ambienti shell ma le variabili di ambiente impostate all'interno dei comandi Bash di Claude non persisteranno tra i comandi.

**Opzione 2: Imposta CLAUDE\_ENV\_FILE prima di avviare Claude Code** (configurazione dell'ambiente persistente)

Esporta il percorso a uno script shell contenente la configurazione del tuo ambiente:

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Dove `/path/to/env-setup.sh` contiene:

```bash  theme={null}
conda activate myenv
# o: source /path/to/venv/bin/activate
# o: export MY_VAR=value
```

Claude Code fornirà questo file prima di ogni comando Bash, rendendo l'ambiente persistente in tutti i comandi.

**Opzione 3: Usa un hook SessionStart** (configurazione specifica del progetto)

Configura in `.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

L'hook scrive in `$CLAUDE_ENV_FILE`, che viene quindi fornito prima di ogni comando Bash. Questo è ideale per le configurazioni di progetto condivise dal team.

Vedi [Hook SessionStart](/it/hooks#persist-environment-variables) per ulteriori dettagli sull'Opzione 3.

### Estensione degli strumenti con hook

Puoi eseguire comandi personalizzati prima o dopo l'esecuzione di qualsiasi strumento utilizzando gli [hook di Claude Code](/it/hooks-guide).

Ad esempio, potresti eseguire automaticamente un formattatore Python dopo che Claude modifica i file Python, o impedire le modifiche ai file di configurazione di produzione bloccando le operazioni Write su determinati percorsi.

## Vedi anche

* [Permessi](/it/permissions): sistema di permessi, sintassi delle regole, modelli specifici dello strumento e politiche gestite
* [Autenticazione](/it/authentication): configura l'accesso degli utenti a Claude Code
* [Troubleshooting](/it/troubleshooting): soluzioni per i problemi di configurazione comuni
