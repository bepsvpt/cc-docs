> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code di Google Vertex AI

> Pelajari tentang mengonfigurasi Claude Code melalui Google Vertex AI, termasuk pengaturan, konfigurasi IAM, dan pemecahan masalah.

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

## Prasyarat

Sebelum mengonfigurasi Claude Code dengan Vertex AI, pastikan Anda memiliki:

* Akun Google Cloud Platform (GCP) dengan penagihan diaktifkan
* Proyek GCP dengan Vertex AI API diaktifkan
* Akses ke model Claude yang diinginkan (misalnya, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) terinstal dan dikonfigurasi
* Kuota dialokasikan di wilayah GCP yang diinginkan

Untuk masuk dengan kredensial Vertex AI Anda sendiri, ikuti [Masuk dengan Vertex AI](#sign-in-with-vertex-ai) di bawah. Untuk menerapkan Claude Code di seluruh tim, gunakan langkah [pengaturan manual](#set-up-manually) dan [pin versi model Anda](#5-pin-model-versions) sebelum melakukan peluncuran.

## Masuk dengan Vertex AI

Jika Anda memiliki kredensial Google Cloud dan ingin mulai menggunakan Claude Code melalui Vertex AI, wizard login akan memandu Anda. Anda menyelesaikan prasyarat sisi GCP sekali per proyek; wizard menangani sisi Claude Code.

<Note>
  Wizard pengaturan Vertex AI memerlukan Claude Code v2.1.98 atau lebih baru. Jalankan `claude --version` untuk memeriksa.
</Note>

<Steps>
  <Step title="Aktifkan model Claude di proyek GCP Anda">
    [Aktifkan Vertex AI API](#1-enable-vertex-ai-api) untuk proyek Anda, kemudian minta akses ke model Claude yang Anda inginkan di [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). Lihat [konfigurasi IAM](#iam-configuration) untuk izin yang akun Anda butuhkan.
  </Step>

  <Step title="Mulai Claude Code dan pilih Vertex AI">
    Jalankan `claude`. Pada prompt login, pilih **3rd-party platform**, kemudian **Google Vertex AI**.
  </Step>

  <Step title="Ikuti prompt wizard">
    Pilih cara Anda melakukan autentikasi ke Google Cloud: Application Default Credentials dari `gcloud`, file kunci akun layanan, atau kredensial yang sudah ada di lingkungan Anda. Wizard mendeteksi proyek dan wilayah Anda, memverifikasi model Claude mana yang dapat dijalankan proyek Anda, dan memungkinkan Anda untuk mempinnya. Ini menyimpan hasilnya ke blok `env` dari [file pengaturan pengguna Anda](/id/settings), jadi Anda tidak perlu mengekspor variabel lingkungan sendiri.
  </Step>
</Steps>

Setelah Anda masuk, jalankan `/setup-vertex` kapan saja untuk membuka kembali wizard dan mengubah kredensial, proyek, wilayah, atau pin model Anda.

## Konfigurasi wilayah

Claude Code mendukung Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multi-region, dan titik akhir regional. Atur `CLOUD_ML_REGION` ke `global`, lokasi multi-region seperti `eu` atau `us`, atau wilayah spesifik seperti `us-east5`. Claude Code memilih nama host Vertex AI yang benar untuk setiap bentuk, termasuk host `aiplatform.eu.rep.googleapis.com` dan `aiplatform.us.rep.googleapis.com` untuk lokasi multi-region.

<Note>
  Vertex AI mungkin tidak mendukung model default Claude Code di setiap jenis titik akhir. Ketersediaan model bervariasi di [wilayah spesifik](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), lokasi multi-region, dan [titik akhir global](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Anda mungkin perlu beralih ke lokasi yang didukung atau menentukan model yang didukung.
</Note>

## Pengaturan manual

Untuk mengonfigurasi Vertex AI melalui variabel lingkungan alih-alih wizard, misalnya di CI atau peluncuran perusahaan yang ditulis skrip, ikuti langkah-langkah di bawah.

### 1. Aktifkan Vertex AI API

Aktifkan Vertex AI API di proyek GCP Anda:

```bash theme={null}
# Atur ID proyek Anda
gcloud config set project YOUR-PROJECT-ID

# Aktifkan Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Minta akses model

Minta akses ke model Claude di Vertex AI:

1. Navigasikan ke [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Cari model "Claude"
3. Minta akses ke model Claude yang diinginkan (misalnya, Claude Sonnet 4.6)
4. Tunggu persetujuan (mungkin memakan waktu 24-48 jam)

### 3. Konfigurasi kredensial GCP

Claude Code menggunakan autentikasi Google Cloud standar.

Untuk informasi lebih lanjut, lihat [dokumentasi autentikasi Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Saat melakukan autentikasi, Claude Code akan secara otomatis menggunakan ID proyek dari variabel lingkungan `ANTHROPIC_VERTEX_PROJECT_ID`. Untuk menimpanya, atur salah satu variabel lingkungan ini: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, atau `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Konfigurasi Claude Code

Atur variabel lingkungan berikut:

```bash theme={null}
# Aktifkan integrasi Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Opsional: Timpa URL titik akhir Vertex untuk titik akhir kustom atau gateway
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Opsional: Nonaktifkan prompt caching jika diperlukan
export DISABLE_PROMPT_CACHING=1

# Ketika CLOUD_ML_REGION=global, timpa wilayah untuk model yang tidak mendukung titik akhir global
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Sebagian besar versi model memiliki variabel `VERTEX_REGION_CLAUDE_*` yang sesuai. Lihat [referensi variabel lingkungan](/id/env-vars) untuk daftar lengkap. Periksa [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) untuk menentukan model mana yang mendukung titik akhir global versus regional saja.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) didukung secara otomatis ketika Anda menentukan flag ephemeral `cache_control`. Untuk menonaktifkannya, atur `DISABLE_PROMPT_CACHING=1`. Untuk batas laju yang lebih tinggi, hubungi dukungan Google Cloud. Saat menggunakan Vertex AI, perintah `/login` dan `/logout` dinonaktifkan karena autentikasi ditangani melalui kredensial Google Cloud.

### 5. Pin versi model

<Warning>
  Pin versi model spesifik saat menerapkan ke beberapa pengguna. Tanpa pinning, alias model seperti `sonnet` dan `opus` diselesaikan ke versi terbaru, yang mungkin belum diaktifkan di proyek Vertex AI Anda ketika Anthropic merilis pembaruan. Claude Code [kembali](#startup-model-checks) ke versi sebelumnya saat startup ketika versi terbaru tidak tersedia, tetapi pinning memungkinkan Anda mengontrol kapan pengguna Anda pindah ke model baru.
</Warning>

Atur variabel lingkungan ini ke ID model Vertex AI spesifik.

Tanpa `ANTHROPIC_DEFAULT_OPUS_MODEL`, alias `opus` di Vertex diselesaikan ke Opus 4.6. Aturnya ke ID Opus 4.7 untuk menggunakan model terbaru:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Untuk ID model saat ini dan warisan, lihat [Ikhtisar Model](https://platform.claude.com/docs/en/about-claude/models/overview). Lihat [Konfigurasi Model](/id/model-config#pin-models-for-third-party-deployments) untuk daftar lengkap variabel lingkungan.

Claude Code menggunakan model default ini ketika tidak ada variabel pinning yang diatur:

| Jenis model       | Nilai default                |
| :---------------- | :--------------------------- |
| Model utama       | `claude-sonnet-4-5@20250929` |
| Model kecil/cepat | `claude-haiku-4-5@20251001`  |

Untuk menyesuaikan model lebih lanjut:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Pemeriksaan model startup

Ketika Claude Code dimulai dengan Vertex AI dikonfigurasi, ia memverifikasi bahwa model yang dimaksudkan untuk digunakan dapat diakses di proyek Anda. Pemeriksaan ini memerlukan Claude Code v2.1.98 atau lebih baru.

Jika Anda telah mempinkan versi model yang lebih lama dari default Claude Code saat ini, dan proyek Anda dapat memanggil versi yang lebih baru, Claude Code akan meminta Anda untuk memperbarui pin. Menerima menulis ID model baru ke [file pengaturan pengguna Anda](/id/settings) dan memulai ulang Claude Code. Menolak diingat sampai perubahan versi default berikutnya.

Jika Anda belum mempinkan model dan default saat ini tidak tersedia di proyek Anda, Claude Code kembali ke versi sebelumnya untuk sesi saat ini dan menampilkan pemberitahuan. Fallback tidak disimpan. Aktifkan model yang lebih baru di [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) atau [pin versi](#5-pin-model-versions) untuk membuat pilihan permanen.

## Konfigurasi IAM

Tetapkan izin IAM yang diperlukan:

Peran `roles/aiplatform.user` mencakup izin yang diperlukan:

* `aiplatform.endpoints.predict` - Diperlukan untuk invokasi model dan penghitungan token

Untuk izin yang lebih ketat, buat peran kustom dengan hanya izin di atas.

Untuk detail, lihat [dokumentasi Vertex IAM](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Buat proyek GCP khusus untuk Claude Code untuk menyederhanakan pelacakan biaya dan kontrol akses.
</Note>

## Jendela konteks token 1M

Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6 mendukung [jendela konteks token 1M](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) di Vertex AI. Claude Code secara otomatis mengaktifkan jendela konteks yang diperluas ketika Anda memilih varian model 1M.

[Wizard pengaturan](#sign-in-with-vertex-ai) menawarkan opsi konteks 1M ketika mempinkan model. Untuk mengaktifkannya untuk model yang dipinkan secara manual, tambahkan `[1m]` ke ID model. Lihat [Pin models for third-party deployments](/id/model-config#pin-models-for-third-party-deployments) untuk detail.

## Pemecahan masalah

Jika Anda mengalami masalah kuota:

* Periksa kuota saat ini atau minta peningkatan kuota melalui [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Jika Anda mengalami kesalahan "model not found" 404:

* Konfirmasi model diaktifkan di [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifikasi model tersedia di lokasi yang Anda tentukan. Beberapa model hanya ditawarkan di lokasi `global` atau multi-region seperti `eu` dan `us`, bukan di wilayah spesifik
* Jika menggunakan `CLOUD_ML_REGION=global`, periksa bahwa model Anda mendukung titik akhir global di [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) di bawah "Supported features". Untuk model yang tidak mendukung titik akhir global, baik:
  * Tentukan model yang didukung melalui `ANTHROPIC_MODEL` atau `ANTHROPIC_DEFAULT_HAIKU_MODEL`, atau
  * Atur wilayah atau lokasi multi-region menggunakan variabel lingkungan `VERTEX_REGION_<MODEL_NAME>`

Jika Anda mengalami kesalahan 429:

* Untuk titik akhir regional, pastikan model utama dan model kecil/cepat didukung di wilayah yang Anda pilih
* Pertimbangkan untuk beralih ke `CLOUD_ML_REGION=global` untuk ketersediaan yang lebih baik

## Sumber daya tambahan

* [Dokumentasi Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Harga Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Kuota dan batas Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
