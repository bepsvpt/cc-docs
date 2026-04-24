> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Microsoft Foundry

> Scopri come configurare Claude Code tramite Microsoft Foundry, inclusi setup, configurazione e risoluzione dei problemi.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

export const Experiment = ({flag, treatment, children}) => {
  const VID_KEY = 'exp_vid';
  const CONSENT_COUNTRIES = new Set(['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'RE', 'GP', 'MQ', 'GF', 'YT', 'BL', 'MF', 'PM', 'WF', 'PF', 'NC', 'AW', 'CW', 'SX', 'FO', 'GL', 'AX', 'GB', 'UK', 'AI', 'BM', 'IO', 'VG', 'KY', 'FK', 'GI', 'MS', 'PN', 'SH', 'TC', 'GG', 'JE', 'IM', 'CA', 'BR', 'IN']);
  const fnv1a = s => {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return h >>> 0;
  };
  const bucket = (seed, vid) => fnv1a(fnv1a(seed + vid) + '') % 10000 < 5000 ? 'control' : 'treatment';
  const [decision] = useState(() => {
    const params = new URLSearchParams(location.search);
    const preBucketed = document.documentElement.dataset['gb_' + flag.replace(/-/g, '_')];
    const force = params.get('gb-force');
    if (force) {
      for (const p of force.split(',')) {
        const [k, v] = p.split(':');
        if (k === flag) return {
          variant: v || 'treatment',
          track: false
        };
      }
    }
    if (navigator.globalPrivacyControl) {
      return {
        variant: 'control',
        track: false
      };
    }
    const prefsMatch = document.cookie.match(/(?:^|; )anthropic-consent-preferences=([^;]+)/);
    if (prefsMatch) {
      try {
        if (JSON.parse(decodeURIComponent(prefsMatch[1])).analytics !== true) {
          return {
            variant: 'control',
            track: false
          };
        }
      } catch {
        return {
          variant: 'control',
          track: false
        };
      }
    } else {
      const country = params.get('country')?.toUpperCase() || (document.cookie.match(/(?:^|; )cf_geo=([A-Z]{2})/) || [])[1];
      if (!country || CONSENT_COUNTRIES.has(country)) {
        return {
          variant: 'control',
          track: false
        };
      }
    }
    let vid;
    try {
      const ajsMatch = document.cookie.match(/(?:^|; )ajs_anonymous_id=([^;]+)/);
      if (ajsMatch) {
        vid = decodeURIComponent(ajsMatch[1]).replace(/^"|"$/g, '');
      } else {
        vid = localStorage.getItem(VID_KEY);
        if (!vid) {
          vid = crypto.randomUUID();
        }
        document.cookie = `ajs_anonymous_id=${vid}; domain=.claude.com; path=/; Secure; SameSite=Lax; max-age=31536000`;
      }
      try {
        localStorage.setItem(VID_KEY, vid);
      } catch {}
    } catch {
      return {
        variant: 'control',
        track: false
      };
    }
    const variant = preBucketed === '1' ? 'treatment' : preBucketed === '0' ? 'control' : bucket(flag, vid);
    return {
      variant,
      track: true,
      vid
    };
  });
  useEffect(() => {
    if (!decision.track) return;
    fetch('https://api.anthropic.com/api/event_logging/v2/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-service-name': 'claude_code_docs'
      },
      body: JSON.stringify({
        events: [{
          event_type: 'GrowthbookExperimentEvent',
          event_data: {
            device_id: decision.vid,
            anonymous_id: decision.vid,
            timestamp: new Date().toISOString(),
            experiment_id: flag,
            variation_id: decision.variant === 'treatment' ? 1 : 0,
            environment: 'production'
          }
        }]
      }),
      keepalive: true
    }).catch(() => {});
  }, []);
  return decision.variant === 'treatment' ? treatment : children;
};

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="foundry" />} />

## Prerequisiti

Prima di configurare Claude Code con Microsoft Foundry, assicurati di avere:

* Un abbonamento Azure con accesso a Microsoft Foundry
* Autorizzazioni RBAC per creare risorse e distribuzioni di Microsoft Foundry
* Azure CLI installato e configurato (facoltativo - necessario solo se non hai un altro meccanismo per ottenere le credenziali)

<Note>
  Se stai distribuendo Claude Code a più utenti, [fissa le versioni del tuo modello](#4-pin-model-versions) per evitare problemi quando Anthropic rilascia nuovi modelli.
</Note>

## Setup

### 1. Provisioning della risorsa Microsoft Foundry

Per prima cosa, crea una risorsa Claude in Azure:

1. Accedi al [portale Microsoft Foundry](https://ai.azure.com/)
2. Crea una nuova risorsa, annotando il nome della risorsa
3. Crea distribuzioni per i modelli Claude:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Configurare le credenziali Azure

Claude Code supporta due metodi di autenticazione per Microsoft Foundry. Scegli il metodo che meglio si adatta ai tuoi requisiti di sicurezza.

**Opzione A: Autenticazione tramite chiave API**

1. Accedi alla tua risorsa nel portale Microsoft Foundry
2. Vai alla sezione **Endpoint e chiavi**
3. Copia **Chiave API**
4. Imposta la variabile di ambiente:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Opzione B: Autenticazione Microsoft Entra ID**

Quando `ANTHROPIC_FOUNDRY_API_KEY` non è impostato, Claude Code utilizza automaticamente la [catena di credenziali predefinita](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview) di Azure SDK.
Questo supporta una varietà di metodi per autenticare carichi di lavoro locali e remoti.

Negli ambienti locali, puoi comunemente utilizzare Azure CLI:

```bash theme={null}
az login
```

<Note>
  Quando si utilizza Microsoft Foundry, i comandi `/login` e `/logout` sono disabilitati poiché l'autenticazione viene gestita tramite le credenziali Azure.
</Note>

### 3. Configurare Claude Code

Imposta le seguenti variabili di ambiente per abilitare Microsoft Foundry:

```bash theme={null}
# Abilita l'integrazione Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nome della risorsa Azure (sostituisci {resource} con il nome della tua risorsa)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Oppure fornisci l'URL di base completo:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. Fissa le versioni del modello

<Warning>
  Fissa versioni specifiche del modello per ogni distribuzione. Se utilizzi alias di modello (`sonnet`, `opus`, `haiku`) senza fissare, Claude Code potrebbe tentare di utilizzare una versione di modello più recente che non è disponibile nel tuo account Foundry, interrompendo gli utenti esistenti quando Anthropic rilascia aggiornamenti. Quando crei distribuzioni Azure, seleziona una versione di modello specifica piuttosto che "aggiornamento automatico alla versione più recente".
</Warning>

Imposta le variabili del modello in modo che corrispondano ai nomi di distribuzione che hai creato nel passaggio 1.

Senza `ANTHROPIC_DEFAULT_OPUS_MODEL`, l'alias `opus` su Foundry si risolve in Opus 4.6. Impostalo sull'ID di Opus 4.7 per utilizzare il modello più recente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Per gli ID dei modelli attuali e legacy, vedi [Panoramica dei modelli](https://platform.claude.com/docs/en/about-claude/models/overview). Vedi [Configurazione del modello](/it/model-config#pin-models-for-third-party-deployments) per l'elenco completo delle variabili di ambiente.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) è abilitato automaticamente. Per richiedere un TTL della cache di 1 ora invece del valore predefinito di 5 minuti, imposta la seguente variabile; le scritture della cache con un TTL di 1 ora vengono fatturate a una tariffa più elevata:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Configurazione RBAC di Azure

I ruoli predefiniti `Azure AI User` e `Cognitive Services User` includono tutte le autorizzazioni necessarie per invocare i modelli Claude.

Per autorizzazioni più restrittive, crea un ruolo personalizzato con quanto segue:

```json theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

Per i dettagli, vedi [Documentazione RBAC di Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Risoluzione dei problemi

Se ricevi un errore "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Configura Entra ID nell'ambiente, oppure imposta `ANTHROPIC_FOUNDRY_API_KEY`.

## Risorse aggiuntive

* [Documentazione di Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Modelli di Microsoft Foundry](https://ai.azure.com/explore/models)
* [Prezzi di Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
