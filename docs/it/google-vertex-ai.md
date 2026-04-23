> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Google Vertex AI

> Scopri come configurare Claude Code tramite Google Vertex AI, inclusa la configurazione, la configurazione IAM e la risoluzione dei problemi.

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
          <a href={`https://www.anthropic.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
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

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="vertex" />} />

## Prerequisiti

Prima di configurare Claude Code con Vertex AI, assicurati di avere:

* Un account Google Cloud Platform (GCP) con fatturazione abilitata
* Un progetto GCP con Vertex AI API abilitata
* Accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installato e configurato
* Quota allocata nella regione GCP desiderata

Per accedere con le tue credenziali Vertex AI, segui [Accedi con Vertex AI](#sign-in-with-vertex-ai) di seguito. Per distribuire Claude Code in un team, utilizza i passaggi di [configurazione manuale](#set-up-manually) e [fissa le versioni del tuo modello](#5-pin-model-versions) prima del rollout.

## Accedi con Vertex AI

Se hai credenziali Google Cloud e desideri iniziare a utilizzare Claude Code tramite Vertex AI, la procedura guidata di accesso ti guida attraverso i passaggi. Completi i prerequisiti lato GCP una volta per progetto; la procedura guidata gestisce il lato Claude Code.

<Note>
  La procedura guidata di configurazione di Vertex AI richiede Claude Code v2.1.98 o versione successiva. Esegui `claude --version` per verificare.
</Note>

<Steps>
  <Step title="Abilita i modelli Claude nel tuo progetto GCP">
    [Abilita Vertex AI API](#1-enable-vertex-ai-api) per il tuo progetto, quindi richiedi accesso ai modelli Claude che desideri in [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). Consulta [Configurazione IAM](#iam-configuration) per le autorizzazioni di cui il tuo account ha bisogno.
  </Step>

  <Step title="Avvia Claude Code e scegli Vertex AI">
    Esegui `claude`. Al prompt di accesso, seleziona **3rd-party platform**, quindi **Google Vertex AI**.
  </Step>

  <Step title="Segui i prompt della procedura guidata">
    Scegli come autenticarti a Google Cloud: Application Default Credentials da `gcloud`, un file di chiave dell'account di servizio, o credenziali già presenti nel tuo ambiente. La procedura guidata rileva il tuo progetto e la tua regione, verifica quali modelli Claude il tuo progetto può invocare, e ti consente di fissarli. Salva il risultato nel blocco `env` del tuo [file di impostazioni utente](/it/settings), quindi non è necessario esportare variabili di ambiente da solo.
  </Step>
</Steps>

Dopo aver effettuato l'accesso, esegui `/setup-vertex` in qualsiasi momento per riaprire la procedura guidata e modificare le tue credenziali, progetto, regione o fissaggi di modello.

## Configurazione della regione

Claude Code supporta endpoint Vertex AI [globali](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multi-regione e regionali. Imposta `CLOUD_ML_REGION` su `global`, una posizione multi-regione come `eu` o `us`, o una regione specifica come `us-east5`. Claude Code seleziona il nome host Vertex AI corretto per ogni modulo, inclusi gli host `aiplatform.eu.rep.googleapis.com` e `aiplatform.us.rep.googleapis.com` per le posizioni multi-regione.

<Note>
  Vertex AI potrebbe non supportare i modelli predefiniti di Claude Code su ogni tipo di endpoint. La disponibilità del modello varia tra [regioni specifiche](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), posizioni multi-regione e [endpoint globali](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Potrebbe essere necessario passare a una posizione supportata o specificare un modello supportato.
</Note>

## Configurazione manuale

Per configurare Vertex AI tramite variabili di ambiente invece della procedura guidata, ad esempio in CI o in un rollout aziendale con script, segui i passaggi di seguito.

### 1. Abilita Vertex AI API

Abilita Vertex AI API nel tuo progetto GCP:

```bash theme={null}
# Imposta il tuo ID progetto
gcloud config set project YOUR-PROJECT-ID

# Abilita Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Richiedi accesso al modello

Richiedi accesso ai modelli Claude in Vertex AI:

1. Accedi a [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Cerca i modelli "Claude"
3. Richiedi accesso ai modelli Claude desiderati (ad esempio, Claude Sonnet 4.6)
4. Attendi l'approvazione (potrebbe richiedere 24-48 ore)

### 3. Configura le credenziali GCP

Claude Code utilizza l'autenticazione standard di Google Cloud.

Per ulteriori informazioni, consulta la [documentazione di autenticazione di Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Durante l'autenticazione, Claude Code utilizzerà automaticamente l'ID progetto dalla variabile di ambiente `ANTHROPIC_VERTEX_PROJECT_ID`. Per eseguire l'override, imposta una di queste variabili di ambiente: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` o `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Configura Claude Code

Imposta le seguenti variabili di ambiente:

```bash theme={null}
# Abilita integrazione Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Facoltativo: Esegui l'override dell'URL dell'endpoint Vertex per endpoint personalizzati o gateway
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Facoltativo: Disabilita prompt caching se necessario
export DISABLE_PROMPT_CACHING=1

# Quando CLOUD_ML_REGION=global, esegui l'override della regione per i modelli che non supportano endpoint globali
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

La maggior parte delle versioni del modello ha una variabile `VERTEX_REGION_CLAUDE_*` corrispondente. Consulta il [riferimento delle variabili di ambiente](/it/env-vars) per l'elenco completo. Controlla [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) per determinare quali modelli supportano endpoint globali rispetto a quelli solo regionali.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) è automaticamente supportato quando specifichi il flag effimero `cache_control`. Per disabilitarlo, imposta `DISABLE_PROMPT_CACHING=1`. Per limiti di velocità aumentati, contatta il supporto di Google Cloud. Quando utilizzi Vertex AI, i comandi `/login` e `/logout` sono disabilitati poiché l'autenticazione è gestita tramite le credenziali di Google Cloud.

### 5. Fissa le versioni del modello

<Warning>
  Fissa versioni specifiche del modello quando distribuisci a più utenti. Senza fissaggio, gli alias di modello come `sonnet` e `opus` si risolvono nella versione più recente, che potrebbe non essere ancora abilitata nel tuo progetto Vertex AI quando Anthropic rilascia un aggiornamento. Claude Code [ritorna](#startup-model-checks) alla versione precedente all'avvio quando la versione più recente non è disponibile, ma il fissaggio ti consente di controllare quando i tuoi utenti passano a un nuovo modello.
</Warning>

Imposta queste variabili di ambiente su ID modello Vertex AI specifici.

Senza `ANTHROPIC_DEFAULT_OPUS_MODEL`, l'alias `opus` su Vertex si risolve in Opus 4.6. Impostalo sull'ID di Opus 4.7 per utilizzare il modello più recente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Per gli ID modello attuali e legacy, consulta [Panoramica dei modelli](https://platform.claude.com/docs/en/about-claude/models/overview). Consulta [Configurazione del modello](/it/model-config#pin-models-for-third-party-deployments) per l'elenco completo delle variabili di ambiente.

Claude Code utilizza questi modelli predefiniti quando nessuna variabile di fissaggio è impostata:

| Tipo di modello        | Valore predefinito           |
| :--------------------- | :--------------------------- |
| Modello primario       | `claude-sonnet-4-5@20250929` |
| Modello piccolo/veloce | `claude-haiku-4-5@20251001`  |

Per personalizzare ulteriormente i modelli:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Controlli del modello all'avvio

Quando Claude Code si avvia con Vertex AI configurato, verifica che i modelli che intende utilizzare siano accessibili nel tuo progetto. Questo controllo richiede Claude Code v2.1.98 o versione successiva.

Se hai fissato una versione del modello più vecchia del valore predefinito corrente di Claude Code, e il tuo progetto può invocare la versione più recente, Claude Code ti chiede di aggiornare il fissaggio. Accettare scrive il nuovo ID modello nel tuo [file di impostazioni utente](/it/settings) e riavvia Claude Code. Rifiutare viene ricordato fino al prossimo cambio di versione predefinita.

Se non hai fissato un modello e il valore predefinito corrente non è disponibile nel tuo progetto, Claude Code ritorna alla versione precedente per la sessione corrente e mostra un avviso. Il ritorno non è persistente. Abilita il modello più recente in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) o [fissa una versione](#5-pin-model-versions) per rendere la scelta permanente.

## Configurazione IAM

Assegna le autorizzazioni IAM richieste:

Il ruolo `roles/aiplatform.user` include le autorizzazioni richieste:

* `aiplatform.endpoints.predict` - Richiesto per l'invocazione del modello e il conteggio dei token

Per autorizzazioni più restrittive, crea un ruolo personalizzato con solo le autorizzazioni di cui sopra.

Per i dettagli, consulta la [documentazione IAM di Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Crea un progetto GCP dedicato per Claude Code per semplificare il tracciamento dei costi e il controllo degli accessi.
</Note>

## Finestra di contesto da 1M token

Claude Opus 4.7, Opus 4.6 e Sonnet 4.6 supportano la [finestra di contesto da 1M token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) su Vertex AI. Claude Code abilita automaticamente la finestra di contesto estesa quando selezioni una variante di modello 1M.

La [procedura guidata di configurazione](#sign-in-with-vertex-ai) offre un'opzione di contesto 1M quando fissa i modelli. Per abilitarla per un modello fissato manualmente, aggiungi `[1m]` all'ID del modello. Consulta [Fissa i modelli per le distribuzioni di terze parti](/it/model-config#pin-models-for-third-party-deployments) per i dettagli.

## Risoluzione dei problemi

Se riscontri problemi di quota:

* Controlla le quote attuali o richiedi un aumento della quota tramite [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Se riscontri errori "model not found" 404:

* Conferma che il modello è abilitato in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifica che il modello sia disponibile nella posizione che hai specificato. Alcuni modelli sono offerti solo su posizioni `global` o multi-regione come `eu` e `us`, non in regioni specifiche
* Se utilizzi `CLOUD_ML_REGION=global`, controlla che i tuoi modelli supportino endpoint globali in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) in "Supported features". Per i modelli che non supportano endpoint globali, puoi:
  * Specificare un modello supportato tramite `ANTHROPIC_MODEL` o `ANTHROPIC_DEFAULT_HAIKU_MODEL`, oppure
  * Impostare una regione o una posizione multi-regione utilizzando le variabili di ambiente `VERTEX_REGION_<MODEL_NAME>`

Se riscontri errori 429:

* Per gli endpoint regionali, assicurati che il modello primario e il modello piccolo/veloce siano supportati nella tua regione selezionata
* Considera di passare a `CLOUD_ML_REGION=global` per una migliore disponibilità

## Risorse aggiuntive

* [Documentazione di Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Prezzi di Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Quote e limiti di Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
