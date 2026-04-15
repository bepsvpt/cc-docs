> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Impostazioni di Claude Code

> Configura Claude Code con impostazioni globali e a livello di progetto, e variabili di ambiente.

Claude Code offre una varietà di impostazioni per configurare il suo comportamento in base alle tue esigenze. Puoi configurare Claude Code eseguendo il comando `/config` quando utilizzi il REPL interattivo, che apre un'interfaccia Impostazioni con schede dove puoi visualizzare le informazioni di stato e modificare le opzioni di configurazione.

## Ambiti di configurazione

Claude Code utilizza un **sistema di ambiti** per determinare dove si applicano le configurazioni e con chi vengono condivise. Comprendere gli ambiti ti aiuta a decidere come configurare Claude Code per uso personale, collaborazione di team o distribuzione aziendale.

### Ambiti disponibili

| Ambito      | Posizione                                                                                         | Chi è interessato                          | Condiviso con il team? |
| :---------- | :------------------------------------------------------------------------------------------------ | :----------------------------------------- | :--------------------- |
| **Managed** | Impostazioni gestite dal server, plist / registro, o `managed-settings.json` a livello di sistema | Tutti gli utenti sulla macchina            | Sì (distribuito da IT) |
| **User**    | Directory `~/.claude/`                                                                            | Tu, in tutti i progetti                    | No                     |
| **Project** | `.claude/` nel repository                                                                         | Tutti i collaboratori su questo repository | Sì (committato in git) |
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
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | Nessuno                         |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json` (per-progetto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` o `.claude/CLAUDE.md` | Nessuno                         |

***

## File di impostazioni

Il file `settings.json` è il meccanismo ufficiale per configurare Claude Code attraverso impostazioni gerarchiche:

* **Le impostazioni utente** sono definite in `~/.claude/settings.json` e si applicano a tutti i progetti.
* **Le impostazioni di progetto** vengono salvate nella directory del tuo progetto:
  * `.claude/settings.json` per le impostazioni che vengono controllate nel controllo del codice sorgente e condivise con il tuo team
  * `.claude/settings.local.json` per le impostazioni che non vengono controllate, utili per preferenze personali e sperimentazione. Claude Code configurerà git per ignorare `.claude/settings.local.json` quando viene creato.
* **Impostazioni gestite**: Per le organizzazioni che necessitano di controllo centralizzato, Claude Code supporta più meccanismi di distribuzione per le impostazioni gestite. Tutti utilizzano lo stesso formato JSON e non possono essere ignorati dalle impostazioni utente o di progetto:

  * **Impostazioni gestite dal server**: consegnate dai server di Anthropic tramite la console di amministrazione Claude.ai. Vedi [impostazioni gestite dal server](/it/server-managed-settings).
  * **Politiche MDM/a livello di sistema operativo**: consegnate tramite la gestione nativa dei dispositivi su macOS e Windows:
    * macOS: dominio delle preferenze gestite `com.anthropic.claudecode` (distribuito tramite profili di configurazione in Jamf, Kandji o altri strumenti MDM)
    * Windows: chiave di registro `HKLM\SOFTWARE\Policies\ClaudeCode` con un valore `Settings` (REG\_SZ o REG\_EXPAND\_SZ) contenente JSON (distribuito tramite Criteri di gruppo o Intune)
    * Windows (a livello utente): `HKCU\SOFTWARE\Policies\ClaudeCode` (priorità di politica più bassa, utilizzata solo quando non esiste alcuna fonte a livello di amministratore)
  * **Basate su file**: `managed-settings.json` e `managed-mcp.json` distribuite alle directory di sistema:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux e WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      Il percorso Windows legacy `C:\ProgramData\ClaudeCode\managed-settings.json` non è più supportato a partire da v2.1.75. Gli amministratori che hanno distribuito impostazioni in quella posizione devono migrare i file a `C:\Program Files\ClaudeCode\managed-settings.json`.
    </Warning>

    Le impostazioni gestite basate su file supportano anche una directory drop-in in `managed-settings.d/` nella stessa directory di sistema insieme a `managed-settings.json`. Questo consente ai team separati di distribuire frammenti di politica indipendenti senza coordinare le modifiche a un singolo file.

    Seguendo la convenzione systemd, `managed-settings.json` viene unito per primo come base, quindi tutti i file `*.json` nella directory drop-in vengono ordinati alfabeticamente e uniti in cima. I file successivi ignorano quelli precedenti per i valori scalari; gli array vengono concatenati e deduplicati; gli oggetti vengono uniti in profondità. I file nascosti che iniziano con `.` vengono ignorati.

    Usa prefissi numerici per controllare l'ordine di unione, ad esempio `10-telemetry.json` e `20-security.json`.

  Vedi [impostazioni gestite](/it/permissions#managed-only-settings) e [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration) per i dettagli.

  <Note>
    Le distribuzioni gestite possono anche limitare **le aggiunte del marketplace dei plugin** utilizzando `strictKnownMarketplaces`. Per ulteriori informazioni, vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Altra configurazione** è archiviata in `~/.claude.json`. Questo file contiene le tue preferenze (tema, impostazioni di notifica, modalità editor), sessione OAuth, configurazioni dei [MCP server](/it/mcp) per gli ambiti utente e locale, stato per-progetto (strumenti consentiti, impostazioni di fiducia), e varie cache. I MCP server con ambito di progetto sono archiviati separatamente in `.mcp.json`.

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

| Chiave                            | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Esempio                                                                                                                       |
| :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | Esegui il thread principale come un subagent denominato. Applica il prompt di sistema, le restrizioni degli strumenti e il modello di quel subagent. Vedi [Invoca i subagent esplicitamente](/it/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                                                                                                                                                                                                                                       | `"code-reviewer"`                                                                                                             |
| `allowedChannelPlugins`           | (Solo impostazioni gestite) Elenco di autorizzazione dei plugin di canale che possono inviare messaggi. Sostituisce l'elenco di autorizzazione predefinito di Anthropic quando impostato. Non definito = ricaduta al predefinito, array vuoto = blocca tutti i plugin di canale. Richiede `channelsEnabled: true`. Vedi [Limita quali plugin di canale possono essere eseguiti](/it/channels#restrict-which-channel-plugins-can-run)                                                                                                                                                                                                           | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                        |
| `allowedHttpHookUrls`             | Elenco di autorizzazione dei modelli di URL che gli hook HTTP possono indirizzare. Supporta `*` come carattere jolly. Quando impostato, gli hook con URL non corrispondenti vengono bloccati. Non definito = nessuna restrizione, array vuoto = blocca tutti gli hook HTTP. Gli array si uniscono tra le fonti di impostazioni. Vedi [Configurazione hook](#hook-configuration)                                                                                                                                                                                                                                                                | `["https://hooks.example.com/*"]`                                                                                             |
| `allowedMcpServers`               | Quando impostato in managed-settings.json, elenco di autorizzazione dei MCP server che gli utenti possono configurare. Non definito = nessuna restrizione, array vuoto = blocco. Si applica a tutti gli ambiti. L'elenco di negazione ha la precedenza. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                   | `[{ "serverName": "github" }]`                                                                                                |
| `allowManagedHooksOnly`           | (Solo impostazioni gestite) Previeni il caricamento di hook utente, di progetto e di plugin. Consenti solo hook gestiti e hook SDK. Vedi [Configurazione hook](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `true`                                                                                                                        |
| `allowManagedMcpServersOnly`      | (Solo impostazioni gestite) Solo `allowedMcpServers` dalle impostazioni gestite sono rispettati. `deniedMcpServers` si unisce comunque da tutte le fonti. Gli utenti possono ancora aggiungere MCP server, ma si applica solo l'elenco di autorizzazione definito dall'amministratore. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                    | `true`                                                                                                                        |
| `allowManagedPermissionRulesOnly` | (Solo impostazioni gestite) Previeni che le impostazioni utente e di progetto definiscano regole di permesso `allow`, `ask` o `deny`. Si applicano solo le regole nelle impostazioni gestite. Vedi [Impostazioni solo gestite](/it/permissions#managed-only-settings)                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                        |
| `alwaysThinkingEnabled`           | Abilita il [pensiero esteso](/it/common-workflows#use-extended-thinking-thinking-mode) per impostazione predefinita per tutte le sessioni. Tipicamente configurato tramite il comando `/config` piuttosto che modificato direttamente                                                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                        |
| `apiKeyHelper`                    | Script personalizzato, da eseguire in `/bin/sh`, per generare un valore di autenticazione. Questo valore verrà inviato come intestazioni `X-Api-Key` e `Authorization: Bearer` per le richieste di modello                                                                                                                                                                                                                                                                                                                                                                                                                                     | `/bin/generate_temp_api_key.sh`                                                                                               |
| `attribution`                     | Personalizza l'attribuzione per i commit git e le pull request. Vedi [Impostazioni di attribuzione](#attribution-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                       |
| `autoMemoryDirectory`             | Directory personalizzata per l'archiviazione della [memoria automatica](/it/memory#storage-location). Accetta percorsi espansi con `~/`. Non accettato nelle impostazioni di progetto (`.claude/settings.json`) per prevenire che i repository condivisi reindirizzino le scritture di memoria a posizioni sensibili. Accettato dalle impostazioni di politica, locale e utente                                                                                                                                                                                                                                                                | `"~/my-memory-dir"`                                                                                                           |
| `autoMode`                        | Personalizza cosa il classificatore della [modalità auto](/it/permission-modes#eliminate-prompts-with-auto-mode) blocca e consente. Contiene array `environment`, `allow` e `soft_deny` di regole in prosa. Vedi [Configura il classificatore della modalità auto](/it/permissions#configure-the-auto-mode-classifier). Non letto dalle impostazioni di progetto condivise                                                                                                                                                                                                                                                                     | `{"environment": ["Trusted repo: github.example.com/acme"]}`                                                                  |
| `autoUpdatesChannel`              | Canale di rilascio da seguire per gli aggiornamenti. Usa `"stable"` per una versione che è tipicamente circa una settimana vecchia e salta le versioni con regressioni importanti, o `"latest"` (predefinito) per il rilascio più recente                                                                                                                                                                                                                                                                                                                                                                                                      | `"stable"`                                                                                                                    |
| `availableModels`                 | Limita quali modelli gli utenti possono selezionare tramite `/model`, `--model`, strumento Config, o `ANTHROPIC_MODEL`. Non influisce sull'opzione Predefinito. Vedi [Limita la selezione del modello](/it/model-config#restrict-model-selection)                                                                                                                                                                                                                                                                                                                                                                                              | `["sonnet", "haiku"]`                                                                                                         |
| `awsAuthRefresh`                  | Script personalizzato che modifica la directory `.aws` (vedi [configurazione avanzata delle credenziali](/it/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `aws sso login --profile myprofile`                                                                                           |
| `awsCredentialExport`             | Script personalizzato che restituisce JSON con le credenziali AWS (vedi [configurazione avanzata delle credenziali](/it/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `/bin/generate_aws_grant.sh`                                                                                                  |
| `blockedMarketplaces`             | (Solo impostazioni gestite) Elenco di negazione delle fonti del marketplace. Le fonti bloccate vengono controllate prima del download, quindi non toccano mai il filesystem. Vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                                                                              | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                       |
| `channelsEnabled`                 | (Solo impostazioni gestite) Consenti [channels](/it/channels) per gli utenti Team e Enterprise. Non impostato o `false` blocca la consegna dei messaggi del canale indipendentemente da cosa gli utenti passano a `--channels`                                                                                                                                                                                                                                                                                                                                                                                                                 | `true`                                                                                                                        |
| `cleanupPeriodDays`               | Le sessioni inattive per un periodo più lungo di questo vengono eliminate all'avvio (predefinito: 30 giorni, minimo 1). L'impostazione a `0` viene rifiutata con un errore di convalida. Per disabilitare completamente le scritture di trascritti in modalità non interattiva (`-p`), usa il flag `--no-session-persistence` o l'opzione SDK `persistSession: false`; non esiste un equivalente in modalità interattiva.                                                                                                                                                                                                                      | `20`                                                                                                                          |
| `companyAnnouncements`            | Annuncio da visualizzare agli utenti all'avvio. Se vengono forniti più annunci, verranno alternati casualmente.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                       |
| `defaultShell`                    | Shell predefinita per i comandi `!` della casella di input. Accetta `"bash"` (predefinito) o `"powershell"`. L'impostazione a `"powershell"` instrada i comandi `!` interattivi tramite PowerShell su Windows. Richiede `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Vedi [Strumento PowerShell](/it/tools-reference#powershell-tool)                                                                                                                                                                                                                                                                                                                  | `"powershell"`                                                                                                                |
| `deniedMcpServers`                | Quando impostato in managed-settings.json, elenco di negazione dei MCP server che sono esplicitamente bloccati. Si applica a tutti gli ambiti inclusi i server gestiti. L'elenco di negazione ha la precedenza sull'elenco di autorizzazione. Vedi [Configurazione MCP gestita](/it/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                             | `[{ "serverName": "filesystem" }]`                                                                                            |
| `disableAllHooks`                 | Disabilita tutti gli [hooks](/it/hooks) e qualsiasi [status line](/it/statusline) personalizzato                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `true`                                                                                                                        |
| `disableAutoMode`                 | Imposta a `"disable"` per prevenire l'attivazione della [modalità auto](/it/permission-modes#eliminate-prompts-with-auto-mode). Rimuove `auto` dal ciclo `Shift+Tab` e rifiuta `--permission-mode auto` all'avvio. Molto utile nelle [impostazioni gestite](/it/permissions#managed-settings) dove gli utenti non possono ignorarla                                                                                                                                                                                                                                                                                                            | `"disable"`                                                                                                                   |
| `disableDeepLinkRegistration`     | Imposta a `"disable"` per prevenire che Claude Code registri il gestore del protocollo `claude-cli://` con il sistema operativo all'avvio. I deep link consentono agli strumenti esterni di aprire una sessione di Claude Code con un prompt pre-compilato tramite `claude-cli://open?q=...`. Utile negli ambienti in cui la registrazione del gestore del protocollo è limitata o gestita separatamente                                                                                                                                                                                                                                       | `"disable"`                                                                                                                   |
| `disabledMcpjsonServers`          | Elenco di MCP server specifici dai file `.mcp.json` da rifiutare                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `["filesystem"]`                                                                                                              |
| `effortLevel`                     | Persisti il [livello di sforzo](/it/model-config#adjust-effort-level) tra le sessioni. Accetta `"low"`, `"medium"`, o `"high"`. Scritto automaticamente quando esegui `/effort low`, `/effort medium`, o `/effort high`. Supportato su Opus 4.6 e Sonnet 4.6                                                                                                                                                                                                                                                                                                                                                                                   | `"medium"`                                                                                                                    |
| `enableAllProjectMcpServers`      | Approva automaticamente tutti i MCP server definiti nei file `.mcp.json` del progetto                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                        |
| `enabledMcpjsonServers`           | Elenco di MCP server specifici dai file `.mcp.json` da approvare                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `["memory", "github"]`                                                                                                        |
| `env`                             | Variabili di ambiente che verranno applicate a ogni sessione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `{"FOO": "bar"}`                                                                                                              |
| `fastModePerSessionOptIn`         | Quando `true`, la modalità veloce non persiste tra le sessioni. Ogni sessione inizia con la modalità veloce disattivata, richiedendo agli utenti di abilitarla con `/fast`. La preferenza della modalità veloce dell'utente viene comunque salvata. Vedi [Richiedi opt-in per sessione](/it/fast-mode#require-per-session-opt-in)                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                        |
| `feedbackSurveyRate`              | Probabilità (0–1) che il [sondaggio sulla qualità della sessione](/it/data-usage#session-quality-surveys) appaia quando idoneo. Imposta a `0` per sopprimere completamente. Utile quando si utilizza Bedrock, Vertex, o Foundry dove il tasso di campionamento predefinito non si applica                                                                                                                                                                                                                                                                                                                                                      | `0.05`                                                                                                                        |
| `fileSuggestion`                  | Configura uno script personalizzato per l'autocompletamento dei file `@`. Vedi [Impostazioni di suggerimento file](#file-suggestion-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                              |
| `forceLoginMethod`                | Usa `claudeai` per limitare l'accesso agli account Claude.ai, `console` per limitare l'accesso agli account Claude Console (fatturazione per utilizzo API)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `claudeai`                                                                                                                    |
| `forceLoginOrgUUID`               | Richiedi che l'accesso appartenga a un'organizzazione specifica. Accetta una singola stringa UUID, che pre-seleziona anche quell'organizzazione durante l'accesso, o un array di UUID dove qualsiasi organizzazione elencata è accettata senza pre-selezione. Quando impostato nelle impostazioni gestite, l'accesso fallisce se l'account autenticato non appartiene a un'organizzazione elencata; un array vuoto fallisce in modo chiuso e blocca l'accesso con un messaggio di errore di configurazione                                                                                                                                     | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` o `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `hooks`                           | Configura comandi personalizzati da eseguire agli eventi del ciclo di vita. Vedi [documentazione hooks](/it/hooks) per il formato                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Vedi [hooks](/it/hooks)                                                                                                       |
| `httpHookAllowedEnvVars`          | Elenco di autorizzazione dei nomi delle variabili di ambiente che gli hook HTTP possono interpolare nelle intestazioni. Quando impostato, l'`allowedEnvVars` effettivo di ogni hook è l'intersezione con questo elenco. Non definito = nessuna restrizione. Gli array si uniscono tra le fonti di impostazioni. Vedi [Configurazione hook](#hook-configuration)                                                                                                                                                                                                                                                                                | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                 |
| `includeCoAuthoredBy`             | **Deprecato**: Usa `attribution` invece. Se includere la riga `co-authored-by Claude` nei commit git e nelle pull request (predefinito: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `false`                                                                                                                       |
| `includeGitInstructions`          | Includi le istruzioni integrate del flusso di lavoro di commit e PR e lo snapshot dello stato git nel prompt di sistema di Claude (predefinito: `true`). Imposta a `false` per rimuovere entrambi, ad esempio quando utilizzi le tue skill di flusso di lavoro git. La variabile di ambiente `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` ha la precedenza su questa impostazione quando impostata                                                                                                                                                                                                                                                   | `false`                                                                                                                       |
| `language`                        | Configura la lingua di risposta preferita di Claude (ad es., `"japanese"`, `"spanish"`, `"french"`). Claude risponderà in questa lingua per impostazione predefinita. Imposta anche la lingua della [dettatura vocale](/it/voice-dictation#change-the-dictation-language)                                                                                                                                                                                                                                                                                                                                                                      | `"japanese"`                                                                                                                  |
| `model`                           | Ignora il modello predefinito da utilizzare per Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `"claude-sonnet-4-6"`                                                                                                         |
| `modelOverrides`                  | Mappa gli ID dei modelli Anthropic agli ID dei modelli specifici del provider come gli ARN del profilo di inferenza Bedrock. Ogni voce del selettore di modello utilizza il suo valore mappato quando chiama l'API del provider. Vedi [Ignora gli ID dei modelli per versione](/it/model-config#override-model-ids-per-version)                                                                                                                                                                                                                                                                                                                | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                  |
| `otelHeadersHelper`               | Script per generare intestazioni OpenTelemetry dinamiche. Viene eseguito all'avvio e periodicamente (vedi [Intestazioni dinamiche](/it/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `/bin/generate_otel_headers.sh`                                                                                               |
| `outputStyle`                     | Configura uno stile di output per regolare il prompt di sistema. Vedi [documentazione degli stili di output](/it/output-styles)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `"Explanatory"`                                                                                                               |
| `permissions`                     | Vedi la tabella sottostante per la struttura dei permessi.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                               |
| `plansDirectory`                  | Personalizza dove vengono archiviati i file di piano. Il percorso è relativo alla radice del progetto. Predefinito: `~/.claude/plans`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `"./plans"`                                                                                                                   |
| `pluginTrustMessage`              | (Solo impostazioni gestite) Messaggio personalizzato aggiunto all'avviso di fiducia del plugin mostrato prima dell'installazione. Usa questo per aggiungere contesto specifico dell'organizzazione, ad esempio per confermare che i plugin dal tuo marketplace interno sono controllati.                                                                                                                                                                                                                                                                                                                                                       | `"All plugins from our marketplace are approved by IT"`                                                                       |
| `prefersReducedMotion`            | Riduci o disabilita le animazioni dell'interfaccia utente (spinner, shimmer, effetti flash) per l'accessibilità                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `true`                                                                                                                        |
| `respectGitignore`                | Controlla se il selettore di file `@` rispetta i modelli `.gitignore`. Quando `true` (predefinito), i file che corrispondono ai modelli `.gitignore` sono esclusi dai suggerimenti                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `false`                                                                                                                       |
| `showClearContextOnPlanAccept`    | Mostra l'opzione "cancella contesto" nella schermata di accettazione del piano. Predefinito: `false`. Imposta a `true` per ripristinare l'opzione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                        |
| `showThinkingSummaries`           | Mostra i riassunti del [pensiero esteso](/it/common-workflows#use-extended-thinking-thinking-mode) nelle sessioni interattive. Quando non impostato o `false` (predefinito in modalità interattiva), i blocchi di pensiero vengono redatti dall'API e mostrati come uno stub compresso. La redazione cambia solo quello che vedi, non quello che il modello genera: per ridurre la spesa di pensiero, [abbassa il budget o disabilita il pensiero](/it/common-workflows#use-extended-thinking-thinking-mode) invece. La modalità non interattiva (`-p`) e i chiamanti SDK ricevono sempre i riassunti indipendentemente da questa impostazione | `true`                                                                                                                        |
| `spinnerTipsEnabled`              | Mostra suggerimenti nello spinner mentre Claude sta lavorando. Imposta a `false` per disabilitare i suggerimenti (predefinito: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `false`                                                                                                                       |
| `spinnerTipsOverride`             | Ignora i suggerimenti dello spinner con stringhe personalizzate. `tips`: array di stringhe di suggerimento. `excludeDefault`: se `true`, mostra solo suggerimenti personalizzati; se `false` o assente, i suggerimenti personalizzati vengono uniti ai suggerimenti incorporati                                                                                                                                                                                                                                                                                                                                                                | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                             |
| `spinnerVerbs`                    | Personalizza i verbi di azione mostrati nello spinner e nei messaggi di durata del turno. Imposta `mode` a `"replace"` per utilizzare solo i tuoi verbi, o `"append"` per aggiungerli ai predefiniti                                                                                                                                                                                                                                                                                                                                                                                                                                           | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                      |
| `statusLine`                      | Configura una status line personalizzata per visualizzare il contesto. Vedi [documentazione `statusLine`](/it/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                   |
| `strictKnownMarketplaces`         | (Solo impostazioni gestite) Elenco di autorizzazione dei marketplace dei plugin che gli utenti possono aggiungere. Non definito = nessuna restrizione, array vuoto = blocco. Si applica solo alle aggiunte del marketplace. Vedi [Restrizioni del marketplace gestito](/it/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                               | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                       |
| `useAutoModeDuringPlan`           | Se la modalità piano utilizza la semantica della modalità auto quando la modalità auto è disponibile. Predefinito: `true`. Non letto dalle impostazioni di progetto condivise. Appare in `/config` come "Use auto mode during plan"                                                                                                                                                                                                                                                                                                                                                                                                            | `false`                                                                                                                       |
| `voiceEnabled`                    | Abilita la [dettatura vocale](/it/voice-dictation) push-to-talk. Scritto automaticamente quando esegui `/voice`. Richiede un account Claude.ai                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `true`                                                                                                                        |

### Impostazioni di configurazione globale

Queste impostazioni sono archiviate in `~/.claude.json` piuttosto che in `settings.json`. Aggiungerle a `settings.json` attiverà un errore di convalida dello schema.

| Chiave                       | Descrizione                                                                                                                                                                                                                                                                                                                                       | Esempio        |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `autoConnectIde`             | Connettiti automaticamente a un IDE in esecuzione quando Claude Code si avvia da un terminale esterno. Predefinito: `false`. Appare in `/config` come **Auto-connect to IDE (external terminal)** quando eseguito al di fuori di un terminale VS Code o JetBrains                                                                                 | `true`         |
| `autoInstallIdeExtension`    | Installa automaticamente l'estensione IDE di Claude Code quando eseguito da un terminale VS Code. Predefinito: `true`. Appare in `/config` come **Auto-install IDE extension** quando eseguito all'interno di un terminale VS Code o JetBrains. Puoi anche impostare la variabile di ambiente [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/it/env-vars) | `false`        |
| `editorMode`                 | Modalità di scorciatoie da tastiera per il prompt di input: `"normal"` o `"vim"`. Predefinito: `"normal"`. Scritto automaticamente quando esegui `/vim`. Appare in `/config` come **Key binding mode**                                                                                                                                            | `"vim"`        |
| `showTurnDuration`           | Mostra i messaggi di durata del turno dopo le risposte, ad es. "Cooked for 1m 6s". Predefinito: `true`. Appare in `/config` come **Show turn duration**                                                                                                                                                                                           | `false`        |
| `terminalProgressBarEnabled` | Mostra la barra di avanzamento del terminale nei terminali supportati: ConEmu, Ghostty 1.2.0+, e iTerm2 3.6.6+. Predefinito: `true`. Appare in `/config` come **Terminal progress bar**                                                                                                                                                           | `false`        |
| `teammateMode`               | Come i compagni di squadra del [team di agenti](/it/agent-teams) vengono visualizzati: `auto` (sceglie riquadri divisi in tmux o iTerm2, in-process altrimenti), `in-process`, o `tmux`. Vedi [scegli una modalità di visualizzazione](/it/agent-teams#choose-a-display-mode)                                                                     | `"in-process"` |

### Impostazioni worktree

Configura come `--worktree` crea e gestisce i git worktrees. Usa queste impostazioni per ridurre l'utilizzo del disco e il tempo di avvio nei grandi monorepo.

| Chiave                        | Descrizione                                                                                                                                                                                                        | Esempio                               |
| :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.symlinkDirectories` | Directory da collegare simbolicamente dal repository principale in ogni worktree per evitare di duplicare grandi directory su disco. Nessuna directory viene collegata simbolicamente per impostazione predefinita | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Directory da estrarre in ogni worktree tramite git sparse-checkout (modalità cone). Solo i percorsi elencati vengono scritti su disco, il che è più veloce nei grandi monorepo                                     | `["packages/my-app", "shared/utils"]` |

Per copiare file gitignored come `.env` nei nuovi worktrees, usa un file [`.worktreeinclude`](/it/common-workflows#copy-gitignored-files-to-worktrees) nella radice del tuo progetto invece di un'impostazione.

### Impostazioni di permesso

| Chiavi                              | Descrizione                                                                                                                                                                                                                                                                                                                                  | Esempio                                                                |
| :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                             | Array di regole di permesso per consentire l'uso dello strumento. Vedi [Sintassi della regola di permesso](#permission-rule-syntax) sottostante per i dettagli della corrispondenza dei modelli                                                                                                                                              | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | Array di regole di permesso per chiedere conferma all'uso dello strumento. Vedi [Sintassi della regola di permesso](#permission-rule-syntax) sottostante                                                                                                                                                                                     | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | Array di regole di permesso per negare l'uso dello strumento. Usa questo per escludere file sensibili dall'accesso di Claude Code. Vedi [Sintassi della regola di permesso](#permission-rule-syntax) e [Limitazioni dei permessi Bash](/it/permissions#tool-specific-permission-rules)                                                       | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | [Directory di lavoro](/it/permissions#working-directories) aggiuntive per l'accesso ai file. La maggior parte della configurazione `.claude/` [non viene scoperta](/it/permissions#additional-directories-grant-file-access-not-configuration) da queste directory                                                                           | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | [Modalità di permesso](/it/permission-modes) predefinita quando si apre Claude Code. Valori validi: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. Il flag CLI `--permission-mode` ignora questa impostazione per una singola sessione                                                                            | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | Imposta a `"disable"` per prevenire l'attivazione della modalità `bypassPermissions`. Disabilita il flag della riga di comando `--dangerously-skip-permissions`. Molto utile nelle [impostazioni gestite](/it/permissions#managed-settings) dove gli utenti non possono ignorarla                                                            | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | Salta il prompt di conferma mostrato prima di entrare nella modalità bypass dei permessi tramite `--dangerously-skip-permissions` o `defaultMode: "bypassPermissions"`. Ignorato quando impostato nelle impostazioni di progetto (`.claude/settings.json`) per prevenire che i repository non attendibili ignorino automaticamente il prompt | `true`                                                                 |

### Sintassi della regola di permesso

Le regole di permesso seguono il formato `Tool` o `Tool(specifier)`. Le regole vengono valutate in ordine: prima le regole di negazione, poi di richiesta, poi di autorizzazione. La prima regola corrispondente vince.

Esempi rapidi:

| Regola                         | Effetto                                           |
| :----------------------------- | :------------------------------------------------ |
| `Bash`                         | Corrisponde a tutti i comandi Bash                |
| `Bash(npm run *)`              | Corrisponde ai comandi che iniziano con `npm run` |
| `Read(./.env)`                 | Corrisponde alla lettura del file `.env`          |
| `WebFetch(domain:example.com)` | Corrisponde alle richieste di fetch a example.com |

Per il riferimento completo della sintassi delle regole, incluso il comportamento dei caratteri jolly, i modelli specifici dello strumento per Read, Edit, WebFetch, MCP e Agent, e le limitazioni di sicurezza dei modelli Bash, vedi [Sintassi della regola di permesso](/it/permissions#permission-rule-syntax).

### Impostazioni sandbox

Configura il comportamento avanzato del sandboxing. Il sandboxing isola i comandi bash dal tuo filesystem e dalla rete. Vedi [Sandboxing](/it/sandboxing) per i dettagli.

| Chiavi                                 | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                       | Esempio                         |
| :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                              | Abilita il sandboxing bash (macOS, Linux e WSL2). Predefinito: false                                                                                                                                                                                                                                                                                                                                              | `true`                          |
| `failIfUnavailable`                    | Esci con un errore all'avvio se `sandbox.enabled` è true ma la sandbox non può avviarsi (dipendenze mancanti, piattaforma non supportata, o restrizioni della piattaforma). Quando false (predefinito), viene mostrato un avviso e i comandi vengono eseguiti senza sandbox. Destinato alle distribuzioni di impostazioni gestite che richiedono il sandboxing come gate rigido                                   | `true`                          |
| `autoAllowBashIfSandboxed`             | Approva automaticamente i comandi bash quando sandboxed. Predefinito: true                                                                                                                                                                                                                                                                                                                                        | `true`                          |
| `excludedCommands`                     | Comandi che dovrebbero essere eseguiti al di fuori della sandbox                                                                                                                                                                                                                                                                                                                                                  | `["git", "docker"]`             |
| `allowUnsandboxedCommands`             | Consenti ai comandi di essere eseguiti al di fuori della sandbox tramite il parametro `dangerouslyDisableSandbox`. Quando impostato a `false`, la scappatoia `dangerouslyDisableSandbox` è completamente disabilitata e tutti i comandi devono essere sandboxed (o essere in `excludedCommands`). Utile per le politiche aziendali che richiedono un sandboxing rigoroso. Predefinito: true                       | `false`                         |
| `filesystem.allowWrite`                | Percorsi aggiuntivi dove i comandi sandboxed possono scrivere. Gli array vengono uniti in tutti gli ambiti di impostazioni: i percorsi utente, progetto e gestiti vengono combinati, non sostituiti. Anche uniti con i percorsi dalle regole di permesso `Edit(...)` allow. Vedi [prefissi di percorso sandbox](#sandbox-path-prefixes) sottostante.                                                              | `["/tmp/build", "~/.kube"]`     |
| `filesystem.denyWrite`                 | Percorsi dove i comandi sandboxed non possono scrivere. Gli array vengono uniti in tutti gli ambiti di impostazioni. Anche uniti con i percorsi dalle regole di permesso `Edit(...)` deny.                                                                                                                                                                                                                        | `["/etc", "/usr/local/bin"]`    |
| `filesystem.denyRead`                  | Percorsi dove i comandi sandboxed non possono leggere. Gli array vengono uniti in tutti gli ambiti di impostazioni. Anche uniti con i percorsi dalle regole di permesso `Read(...)` deny.                                                                                                                                                                                                                         | `["~/.aws/credentials"]`        |
| `filesystem.allowRead`                 | Percorsi per consentire nuovamente la lettura all'interno delle regioni `denyRead`. Ha la precedenza su `denyRead`. Gli array vengono uniti in tutti gli ambiti di impostazioni. Usa questo per creare modelli di accesso in lettura solo per l'area di lavoro.                                                                                                                                                   | `["."]`                         |
| `filesystem.allowManagedReadPathsOnly` | (Solo impostazioni gestite) Solo i percorsi `filesystem.allowRead` dalle impostazioni gestite sono rispettati. `denyRead` si unisce comunque da tutte le fonti. Predefinito: false                                                                                                                                                                                                                                | `true`                          |
| `network.allowUnixSockets`             | Percorsi dei socket Unix accessibili nella sandbox (per agenti SSH, ecc.)                                                                                                                                                                                                                                                                                                                                         | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`          | Consenti tutte le connessioni ai socket Unix nella sandbox. Predefinito: false                                                                                                                                                                                                                                                                                                                                    | `true`                          |
| `network.allowLocalBinding`            | Consenti il binding alle porte localhost (solo macOS). Predefinito: false                                                                                                                                                                                                                                                                                                                                         | `true`                          |
| `network.allowedDomains`               | Array di domini da consentire per il traffico di rete in uscita. Supporta i caratteri jolly (ad es., `*.example.com`).                                                                                                                                                                                                                                                                                            | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly`      | (Solo impostazioni gestite) Solo `allowedDomains` e le regole allow `WebFetch(domain:...)` dalle impostazioni gestite sono rispettate. I domini dalle impostazioni utente, progetto e locale vengono ignorati. I domini non consentiti vengono bloccati automaticamente senza richiedere all'utente. I domini negati vengono comunque rispettati da tutte le fonti. Predefinito: false                            | `true`                          |
| `network.httpProxyPort`                | Porta del proxy HTTP utilizzata se desideri portare il tuo proxy. Se non specificato, Claude eseguirà il suo proxy.                                                                                                                                                                                                                                                                                               | `8080`                          |
| `network.socksProxyPort`               | Porta del proxy SOCKS5 utilizzata se desideri portare il tuo proxy. Se non specificato, Claude eseguirà il suo proxy.                                                                                                                                                                                                                                                                                             | `8081`                          |
| `enableWeakerNestedSandbox`            | Abilita una sandbox più debole per gli ambienti Docker senza privilegi (solo Linux e WSL2). **Riduce la sicurezza.** Predefinito: false                                                                                                                                                                                                                                                                           | `true`                          |
| `enableWeakerNetworkIsolation`         | (Solo macOS) Consenti l'accesso al servizio di fiducia TLS del sistema (`com.apple.trustd.agent`) nella sandbox. Richiesto affinché gli strumenti basati su Go come `gh`, `gcloud` e `terraform` verifichino i certificati TLS quando si utilizza `httpProxyPort` con un proxy MITM e una CA personalizzata. **Riduce la sicurezza** aprendo un potenziale percorso di esfiltrazione dei dati. Predefinito: false | `true`                          |

#### Prefissi di percorso sandbox

I percorsi in `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead` e `filesystem.allowRead` supportano questi prefissi:

| Prefisso               | Significato                                                                                                   | Esempio                                                                     |
| :--------------------- | :------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------- |
| `/`                    | Percorso assoluto dalla radice del filesystem                                                                 | `/tmp/build` rimane `/tmp/build`                                            |
| `~/`                   | Relativo alla directory home                                                                                  | `~/.kube` diventa `$HOME/.kube`                                             |
| `./` o nessun prefisso | Relativo alla radice del progetto per le impostazioni di progetto, o a `~/.claude` per le impostazioni utente | `./output` in `.claude/settings.json` si risolve in `<project-root>/output` |

Il prefisso più vecchio `//path` per i percorsi assoluti funziona ancora. Se in precedenza hai utilizzato il singolo slash `/path` aspettandoti una risoluzione relativa al progetto, passa a `./path`. Questa sintassi differisce dalle [regole di permesso Read e Edit](/it/permissions#read-and-edit), che utilizzano `//path` per assoluto e `/path` per relativo al progetto. I percorsi del filesystem sandbox utilizzano convenzioni standard: `/tmp/build` è un percorso assoluto.

**Esempio di configurazione:**

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
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

**Le restrizioni del filesystem e della rete** possono essere configurate in due modi che vengono uniti insieme:

* **Impostazioni `sandbox.filesystem`** (mostrate sopra): Controllano i percorsi al confine della sandbox a livello di sistema operativo. Queste restrizioni si applicano a tutti i comandi dei sottoprocessi (ad es., `kubectl`, `terraform`, `npm`), non solo agli strumenti di file di Claude.
* **Regole di permesso**: Usa le regole allow/deny `Edit` per controllare l'accesso dello strumento di file di Claude, le regole deny `Read` per bloccare le letture, e le regole allow/deny `WebFetch` per controllare i domini di rete. I percorsi da queste regole vengono anche uniti nella configurazione della sandbox.

### Impostazioni di attribuzione

Claude Code aggiunge attribuzione ai commit git e alle pull request. Questi vengono configurati separatamente:

* I commit utilizzano i [git trailers](https://git-scm.com/docs/git-interpret-trailers) (come `Co-Authored-By`) per impostazione predefinita, che possono essere personalizzati o disabilitati
* Le descrizioni delle pull request sono testo semplice

| Chiavi   | Descrizione                                                                                                     |
| :------- | :-------------------------------------------------------------------------------------------------------------- |
| `commit` | Attribuzione per i commit git, inclusi eventuali trailer. La stringa vuota nasconde l'attribuzione del commit   |
| `pr`     | Attribuzione per le descrizioni delle pull request. La stringa vuota nasconde l'attribuzione della pull request |

**Attribuzione predefinita del commit:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Attribuzione predefinita della pull request:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Esempio:**

```json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  L'impostazione `attribution` ha la precedenza sull'impostazione deprecata `includeCoAuthoredBy`. Per nascondere tutta l'attribuzione, imposta `commit` e `pr` a stringhe vuote.
</Note>

### Impostazioni di suggerimento file

Configura un comando personalizzato per l'autocompletamento del percorso del file `@`. Il suggerimento di file incorporato utilizza l'attraversamento veloce del filesystem, ma i grandi monorepo potrebbero beneficiare dell'indicizzazione specifica del progetto come un indice di file pre-costruito o strumenti personalizzati.

```json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Il comando viene eseguito con le stesse variabili di ambiente degli [hooks](/it/hooks), incluso `CLAUDE_PROJECT_DIR`. Riceve JSON tramite stdin con un campo `query`:

```json theme={null}
{"query": "src/comp"}
```

Restituisci i percorsi dei file separati da newline a stdout (attualmente limitati a 15):

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Esempio:**

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configurazione hook

Queste impostazioni controllano quali hook possono essere eseguiti e a cosa possono accedere gli hook HTTP. L'impostazione `allowManagedHooksOnly` può essere configurata solo nelle [impostazioni gestite](#settings-files). Gli elenchi di autorizzazione degli URL e delle variabili di ambiente possono essere impostati a qualsiasi livello di impostazioni e si uniscono tra le fonti.

**Comportamento quando `allowManagedHooksOnly` è `true`:**

* Gli hook gestiti e gli hook SDK vengono caricati
* Gli hook utente, di progetto e di plugin vengono bloccati

**Limita gli URL degli hook HTTP:**

Limita quali URL gli hook HTTP possono indirizzare. Supporta `*` come carattere jolly per la corrispondenza. Quando l'array è definito, gli hook HTTP che indirizzano URL non corrispondenti vengono silenziosamente bloccati.

```json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Limita le variabili di ambiente degli hook HTTP:**

Limita quali nomi di variabili di ambiente gli hook HTTP possono interpolare nei valori delle intestazioni. L'`allowedEnvVars` effettivo di ogni hook è l'intersezione del suo elenco e di questa impostazione.

```json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Precedenza delle impostazioni

Le impostazioni si applicano in ordine di precedenza. Dal più alto al più basso:

1. **Impostazioni gestite** ([gestite dal server](/it/server-managed-settings), [politiche MDM/a livello di sistema operativo](#configuration-scopes), o [impostazioni gestite](/it/settings#settings-files))
   * Politiche distribuite da IT tramite consegna dal server, profili di configurazione MDM, politiche di registro, o file di impostazioni gestite
   * Non possono essere ignorate da nessun altro livello, inclusi gli argomenti della riga di comando
   * All'interno del livello gestito, la precedenza è: gestite dal server > politiche MDM/a livello di sistema operativo > file-based (`managed-settings.d/*.json` + `managed-settings.json`) > registro HKCU (solo Windows). Viene utilizzata una sola fonte gestita; le fonti non si uniscono tra i livelli. All'interno del livello file-based, i file drop-in e il file base vengono uniti insieme.

2. **Argomenti della riga di comando**
   * Override temporanei per una sessione specifica

3. **Impostazioni di progetto locale** (`.claude/settings.local.json`)
   * Impostazioni personali specifiche del progetto

4. **Impostazioni di progetto condivise** (`.claude/settings.json`)
   * Impostazioni di progetto condivise dal team nel controllo del codice sorgente

5. **Impostazioni utente** (`~/.claude/settings.json`)
   * Impostazioni globali personali

Questa gerarchia garantisce che le politiche organizzative siano sempre applicate mentre consente comunque ai team e agli individui di personalizzare la loro esperienza. La stessa precedenza si applica se esegui Claude Code dalla CLI, dall'[estensione VS Code](/it/vs-code), o da un [IDE JetBrains](/it/jetbrains).

Ad esempio, se le tue impostazioni utente consentono `Bash(npm run *)` ma le impostazioni condivise di un progetto lo negano, l'impostazione di progetto ha la precedenza e il comando viene bloccato.

<Note>
  **Le impostazioni di array si uniscono tra gli ambiti.** Quando la stessa impostazione con valore di array (come `sandbox.filesystem.allowWrite` o `permissions.allow`) appare in più ambiti, gli array vengono **concatenati e deduplicati**, non sostituiti. Ciò significa che gli ambiti con priorità inferiore possono aggiungere voci senza ignorare quelle impostate da ambiti con priorità più alta, e viceversa. Ad esempio, se le impostazioni gestite impostano `allowWrite` a `["/opt/company-tools"]` e un utente aggiunge `["~/.kube"]`, entrambi i percorsi sono inclusi nella configurazione finale.
</Note>

### Verifica le impostazioni attive

Esegui `/status` all'interno di Claude Code per vedere quali fonti di impostazioni sono attive e da dove provengono. L'output mostra ogni livello di configurazione (gestito, utente, progetto) insieme alla sua origine, come `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, o `Enterprise managed settings (file)`. Se un file di impostazioni contiene errori, `/status` segnala il problema in modo che tu possa risolverlo.

### Punti chiave sul sistema di configurazione

* **File di memoria (`CLAUDE.md`)**: Contengono istruzioni e contesto che Claude carica all'avvio
* **File di impostazioni (JSON)**: Configurano permessi, variabili di ambiente e comportamento dello strumento
* **Skills**: Prompt personalizzati che possono essere invocati con `/skill-name` o caricati automaticamente da Claude
* **MCP servers**: Estendono Claude Code con strumenti e integrazioni aggiuntivi
* **Precedenza**: Le configurazioni di livello superiore (Managed) ignorano quelle di livello inferiore (User/Project)
* **Ereditarietà**: Le impostazioni vengono unite, con impostazioni più specifiche che aggiungono o ignorano quelle più ampie

### Prompt di sistema

Il prompt di sistema interno di Claude Code non è pubblicato. Per aggiungere istruzioni personalizzate, usa i file `CLAUDE.md` o il flag `--append-system-prompt`.

### Esclusione di file sensibili

Per prevenire che Claude Code acceda a file contenenti informazioni sensibili come chiavi API, segreti e file di ambiente, usa l'impostazione `permissions.deny` nel tuo file `.claude/settings.json`:

```json theme={null}
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

## Configurazione plugin

Claude Code supporta un sistema di plugin che ti consente di estendere la funzionalità con skills, agenti, hooks e MCP servers. I plugin vengono distribuiti tramite marketplace e possono essere configurati sia a livello utente che di repository.

### Impostazioni plugin

Impostazioni relative ai plugin in `settings.json`:

```json theme={null}
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
* **Impostazioni gestite** (`managed-settings.json`): Override della politica a livello organizzativo che blocca l'installazione in tutti gli ambiti e nasconde il plugin dal marketplace

**Esempio**:

```json theme={null}
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

```json theme={null}
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
* `settings`: marketplace inline dichiarato direttamente in settings.json senza un repository ospitato separato (utilizza `name` e `plugins`)

Usa `source: 'settings'` per dichiarare un piccolo set di plugin inline senza configurare un repository marketplace ospitato. I plugin elencati qui devono fare riferimento a fonti esterne come GitHub o npm. Devi comunque abilitare ogni plugin separatamente in `enabledPlugins`.

```json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Solo impostazioni gestite**: Controlla quali marketplace dei plugin gli utenti possono aggiungere. Questa impostazione può essere configurata solo nelle [impostazioni gestite](/it/settings#settings-files) e fornisce agli amministratori un controllo rigoroso sulle fonti del marketplace.

**Posizioni dei file di impostazioni gestite**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux e WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Caratteristiche chiave**:

* Disponibile solo nelle impostazioni gestite (`managed-settings.json`)
* Non può essere ignorato da nessun'altra impostazione (precedenza più alta)
* Applicato PRIMA delle operazioni di rete/filesystem (le fonti bloccate non vengono mai eseguite)
* Utilizza la corrispondenza esatta per le specifiche della fonte (incluso `ref`, `path` per le fonti git), tranne `hostPattern`, che utilizza la corrispondenza regex

**Comportamento dell'elenco di autorizzazione**:

* `undefined` (predefinito): Nessuna restrizione - gli utenti possono aggiungere qualsiasi marketplace
* Array vuoto `[]`: Blocco completo - gli utenti non possono aggiungere nuovi marketplace
* Elenco di fonti: Gli utenti possono aggiungere solo i marketplace che corrispondono esattamente

**Tutti i tipi di fonte supportati**:

L'elenco di autorizzazione supporta più tipi di fonte del marketplace. La maggior parte delle fonti utilizza la corrispondenza esatta, mentre `hostPattern` utilizza la corrispondenza regex rispetto all'host del marketplace.

1. **Repository GitHub**:

```json theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Campi: `repo` (obbligatorio), `ref` (facoltativo: ramo/tag/SHA), `path` (facoltativo: sottodirectory)

2. **Repository Git**:

```json theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Campi: `url` (obbligatorio), `ref` (facoltativo: ramo/tag/SHA), `path` (facoltativo: sottodirectory)

3. **Marketplace basati su URL**:

```json theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Campi: `url` (obbligatorio), `headers` (facoltativo: intestazioni HTTP per l'accesso autenticato)

<Note>
  I marketplace basati su URL scaricano solo il file `marketplace.json`. Non scaricano i file dei plugin dal server. I plugin nei marketplace basati su URL devono utilizzare fonti esterne (URL GitHub, npm o git) piuttosto che percorsi relativi. Per i plugin con percorsi relativi, utilizza un marketplace basato su Git. Vedi [Troubleshooting](/it/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) per i dettagli.
</Note>

4. **Pacchetti NPM**:

```json theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Campi: `package` (obbligatorio, supporta pacchetti con scope)

5. **Percorsi di file**:

```json theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Campi: `path` (obbligatorio: percorso assoluto al file marketplace.json)

6. **Percorsi di directory**:

```json theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Campi: `path` (obbligatorio: percorso assoluto alla directory contenente `.claude-plugin/marketplace.json`)

7. **Corrispondenza del modello host**:

```json theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Campi: `hostPattern` (obbligatorio: modello regex per abbinare l'host del marketplace)

Utilizza la corrispondenza del modello host quando desideri consentire tutti i marketplace da un host specifico senza enumerare ogni repository individualmente. Questo è utile per le organizzazioni con server GitHub Enterprise o GitLab interni dove gli sviluppatori creano i loro marketplace.

Estrazione dell'host per tipo di fonte:

* `github`: corrisponde sempre a `github.com`
* `git`: estrae il nome host dall'URL (supporta sia i formati HTTPS che SSH)
* `url`: estrae il nome host dall'URL
* `npm`, `file`, `directory`: non supportati per la corrispondenza del modello host

**Esempi di configurazione**:

Esempio: consenti solo marketplace specifici:

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
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Esempio - Disabilita tutte le aggiunte del marketplace:

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Esempio: consenti tutti i marketplace da un server git interno:

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

**Requisiti di corrispondenza esatta**:

Le fonti del marketplace devono corrispondere **esattamente** affinché l'aggiunta di un utente sia consentita. Per le fonti basate su git (`github` e `git`), questo include tutti i campi facoltativi:

* Il `repo` o `url` deve corrispondere esattamente
* Il campo `ref` deve corrispondere esattamente (o entrambi non essere definiti)
* Il campo `path` deve corrispondere esattamente (o entrambi non essere definiti)

Esempi di fonti che **NON corrispondono**:

```json theme={null}
// Queste sono DIVERSE fonti:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Anche queste sono DIVERSE:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Confronto con `extraKnownMarketplaces`**:

| Aspetto                  | `strictKnownMarketplaces`                            | `extraKnownMarketplaces`                        |
| ------------------------ | ---------------------------------------------------- | ----------------------------------------------- |
| **Scopo**                | Applicazione della politica organizzativa            | Comodità del team                               |
| **File di impostazioni** | Solo `managed-settings.json`                         | Qualsiasi file di impostazioni                  |
| **Comportamento**        | Blocca le aggiunte non nell'elenco di autorizzazione | Installa automaticamente i marketplace mancanti |
| **Quando applicato**     | Prima delle operazioni di rete/filesystem            | Dopo il prompt di fiducia dell'utente           |
| **Può essere ignorato**  | No (precedenza più alta)                             | Sì (da impostazioni con precedenza più alta)    |
| **Formato della fonte**  | Oggetto fonte diretto                                | Marketplace denominato con fonte nidificata     |
| **Caso d'uso**           | Conformità, restrizioni di sicurezza                 | Onboarding, standardizzazione                   |

**Differenza di formato**:

`strictKnownMarketplaces` utilizza oggetti fonte diretti:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` richiede marketplace denominati:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Utilizzo di entrambi insieme**:

`strictKnownMarketplaces` è un gate di politica: controlla cosa gli utenti possono aggiungere ma non registra alcun marketplace. Per limitare e pre-registrare un marketplace per tutti gli utenti, imposta entrambi in `managed-settings.json`:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Con solo `strictKnownMarketplaces` impostato, gli utenti possono comunque aggiungere il marketplace consentito manualmente tramite `/plugin marketplace add`, ma non è disponibile automaticamente.

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

Le variabili di ambiente ti consentono di controllare il comportamento di Claude Code senza modificare i file di impostazioni. Qualsiasi variabile può anche essere configurata in [`settings.json`](#available-settings) sotto la chiave `env` per applicarla a ogni sessione o distribuirla al tuo team.

Vedi il [riferimento delle variabili di ambiente](/it/env-vars) per l'elenco completo.

## Strumenti disponibili per Claude

Claude Code ha accesso a un set di strumenti per leggere, modificare, cercare, eseguire comandi e orchestrare subagent. I nomi degli strumenti sono le stringhe esatte che utilizzi nelle regole di permesso e nei matcher degli hook.

Vedi il [riferimento degli strumenti](/it/tools-reference) per l'elenco completo e i dettagli del comportamento dello strumento Bash.

## Vedi anche

* [Permissions](/it/permissions): sistema di permessi, sintassi delle regole, modelli specifici dello strumento e politiche gestite
* [Authentication](/it/authentication): configura l'accesso degli utenti a Claude Code
* [Troubleshooting](/it/troubleshooting): soluzioni per i problemi di configurazione comuni
