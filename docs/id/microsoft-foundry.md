> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code di Microsoft Foundry

> Pelajari tentang mengonfigurasi Claude Code melalui Microsoft Foundry, termasuk setup, konfigurasi, dan pemecahan masalah.

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

## Prasyarat

Sebelum mengonfigurasi Claude Code dengan Microsoft Foundry, pastikan Anda memiliki:

* Langganan Azure dengan akses ke Microsoft Foundry
* Izin RBAC untuk membuat sumber daya dan deployment Microsoft Foundry
* Azure CLI diinstal dan dikonfigurasi (opsional - hanya diperlukan jika Anda tidak memiliki mekanisme lain untuk mendapatkan kredensial)

<Note>
  Jika Anda menerapkan Claude Code ke beberapa pengguna, [pin versi model Anda](#4-pin-model-versions) untuk mencegah kerusakan ketika Anthropic merilis model baru.
</Note>

## Setup

### 1. Menyediakan sumber daya Microsoft Foundry

Pertama, buat sumber daya Claude di Azure:

1. Navigasikan ke [portal Microsoft Foundry](https://ai.azure.com/)
2. Buat sumber daya baru, catat nama sumber daya Anda
3. Buat deployment untuk model Claude:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Konfigurasi kredensial Azure

Claude Code mendukung dua metode autentikasi untuk Microsoft Foundry. Pilih metode yang paling sesuai dengan persyaratan keamanan Anda.

**Opsi A: Autentikasi kunci API**

1. Navigasikan ke sumber daya Anda di portal Microsoft Foundry
2. Buka bagian **Endpoints and keys**
3. Salin **API Key**
4. Atur variabel lingkungan:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Opsi B: Autentikasi Microsoft Entra ID**

Ketika `ANTHROPIC_FOUNDRY_API_KEY` tidak diatur, Claude Code secara otomatis menggunakan Azure SDK [rantai kredensial default](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
Ini mendukung berbagai metode untuk mengautentikasi beban kerja lokal dan jarak jauh.

Di lingkungan lokal, Anda biasanya dapat menggunakan Azure CLI:

```bash theme={null}
az login
```

<Note>
  Saat menggunakan Microsoft Foundry, perintah `/login` dan `/logout` dinonaktifkan karena autentikasi ditangani melalui kredensial Azure.
</Note>

### 3. Konfigurasi Claude Code

Atur variabel lingkungan berikut untuk mengaktifkan Microsoft Foundry:

```bash theme={null}
# Aktifkan integrasi Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nama sumber daya Azure (ganti {resource} dengan nama sumber daya Anda)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Atau berikan URL dasar lengkap:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. Pin model versions

<Warning>
  Pin versi model spesifik untuk setiap deployment. Jika Anda menggunakan alias model (`sonnet`, `opus`, `haiku`) tanpa pinning, Claude Code mungkin mencoba menggunakan versi model yang lebih baru yang tidak tersedia di akun Foundry Anda, merusak pengguna yang ada ketika Anthropic merilis pembaruan. Ketika Anda membuat deployment Azure, pilih versi model spesifik daripada "auto-update to latest."
</Warning>

Atur variabel model agar sesuai dengan nama deployment yang Anda buat di langkah 1.

Tanpa `ANTHROPIC_DEFAULT_OPUS_MODEL`, alias `opus` di Foundry diselesaikan ke Opus 4.6. Aturnya ke ID Opus 4.7 untuk menggunakan model terbaru:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Untuk ID model saat ini dan legacy, lihat [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Lihat [Model configuration](/id/model-config#pin-models-for-third-party-deployments) untuk daftar lengkap variabel lingkungan.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) diaktifkan secara otomatis. Untuk meminta TTL cache 1 jam alih-alih default 5 menit, atur variabel berikut; cache writes dengan TTL 1 jam ditagih dengan tarif yang lebih tinggi:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Konfigurasi Azure RBAC

Peran default `Azure AI User` dan `Cognitive Services User` mencakup semua izin yang diperlukan untuk memanggil model Claude.

Untuk izin yang lebih ketat, buat peran khusus dengan yang berikut:

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

Untuk detail, lihat [dokumentasi RBAC Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Pemecahan Masalah

Jika Anda menerima kesalahan "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Konfigurasi Entra ID di lingkungan, atau atur `ANTHROPIC_FOUNDRY_API_KEY`.

## Sumber daya tambahan

* [Dokumentasi Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Model Microsoft Foundry](https://ai.azure.com/explore/models)
* [Harga Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
