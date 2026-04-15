> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurazione di rete aziendale

> Configurare Claude Code per ambienti aziendali con server proxy, Autorità di Certificazione (CA) personalizzate e autenticazione Transport Layer Security (mTLS) reciproca.

Claude Code supporta varie configurazioni di rete e sicurezza aziendali attraverso variabili di ambiente. Ciò include l'instradamento del traffico attraverso server proxy aziendali, la fiducia in Autorità di Certificazione (CA) personalizzate e l'autenticazione con certificati Transport Layer Security (mTLS) reciproco per una sicurezza migliorata.

<Note>
  Tutte le variabili di ambiente mostrate in questa pagina possono essere configurate anche in [`settings.json`](/it/settings).
</Note>

## Configurazione del proxy

### Variabili di ambiente

Claude Code rispetta le variabili di ambiente proxy standard:

```bash theme={null}
# Proxy HTTPS (consigliato)
export HTTPS_PROXY=https://proxy.example.com:8080

# Proxy HTTP (se HTTPS non disponibile)
export HTTP_PROXY=http://proxy.example.com:8080

# Ignora il proxy per richieste specifiche - formato separato da spazi
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Ignora il proxy per richieste specifiche - formato separato da virgole
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Ignora il proxy per tutte le richieste
export NO_PROXY="*"
```

<Note>
  Claude Code non supporta proxy SOCKS.
</Note>

### Autenticazione di base

Se il proxy richiede l'autenticazione di base, includere le credenziali nell'URL del proxy:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Evitare di codificare le password negli script. Utilizzare variabili di ambiente o archiviazione sicura delle credenziali.
</Warning>

<Tip>
  Per proxy che richiedono autenticazione avanzata (NTLM, Kerberos, ecc.), considerare l'utilizzo di un servizio LLM Gateway che supporti il metodo di autenticazione.
</Tip>

## Certificati CA personalizzati

Se l'ambiente aziendale utilizza CA personalizzate per le connessioni HTTPS (sia tramite proxy che accesso diretto all'API), configurare Claude Code per fidarsi di esse:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autenticazione mTLS

Per ambienti aziendali che richiedono l'autenticazione del certificato client:

```bash theme={null}
# Certificato client per l'autenticazione
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Chiave privata del client
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Facoltativo: Passphrase per la chiave privata crittografata
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Requisiti di accesso alla rete

Claude Code richiede accesso ai seguenti URL:

* `api.anthropic.com`: endpoint dell'API Claude
* `claude.ai`: autenticazione per account claude.ai
* `platform.claude.com`: autenticazione per account Anthropic Console

Assicurarsi che questi URL siano inseriti nella whitelist nella configurazione del proxy e nelle regole del firewall. Ciò è particolarmente importante quando si utilizza Claude Code in ambienti di rete containerizzati o limitati.

L'installer nativo e i controlli degli aggiornamenti richiedono inoltre i seguenti URL. Inserire nella whitelist entrambi, poiché l'installer e l'auto-updater scaricano da `storage.googleapis.com` mentre i download dei plugin utilizzano `downloads.claude.ai`. Se si installa Claude Code tramite npm o si gestisce la propria distribuzione binaria, gli utenti finali potrebbero non avere bisogno di accesso:

* `storage.googleapis.com`: bucket di download per il binario Claude Code e l'auto-updater
* `downloads.claude.ai`: CDN che ospita lo script di installazione, i puntatori di versione, i manifesti, le chiavi di firma e gli eseguibili dei plugin

[Claude Code sul web](/it/claude-code-on-the-web) e [Code Review](/it/code-review) si connettono ai repository dall'infrastruttura gestita da Anthropic. Se l'organizzazione GitHub Enterprise Cloud limita l'accesso per indirizzo IP, abilitare [l'ereditarietà della lista di indirizzi IP consentiti per le app GitHub installate](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). L'app GitHub di Claude registra i suoi intervalli di indirizzi IP, quindi l'abilitazione di questa impostazione consente l'accesso senza configurazione manuale. Per [aggiungere gli intervalli alla lista di indirizzi consentiti manualmente](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) invece, o per configurare altri firewall, consultare gli [indirizzi IP dell'API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Per istanze [GitHub Enterprise Server](/it/github-enterprise-server) auto-ospitate dietro un firewall, inserire nella whitelist gli stessi [indirizzi IP dell'API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) in modo che l'infrastruttura Anthropic possa raggiungere l'host GHES per clonare i repository e pubblicare i commenti di revisione.

## Risorse aggiuntive

* [Impostazioni di Claude Code](/it/settings)
* [Riferimento delle variabili di ambiente](/it/env-vars)
* [Guida alla risoluzione dei problemi](/it/troubleshooting)
