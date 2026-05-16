> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code di Amazon Bedrock

> Pelajari tentang mengonfigurasi Claude Code melalui Amazon Bedrock, termasuk pengaturan, konfigurasi IAM, dan pemecahan masalah.

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

<ContactSalesCard surface="bedrock" />

## Prasyarat

Sebelum mengonfigurasi Claude Code dengan Bedrock, pastikan Anda memiliki:

* Akun AWS dengan akses Bedrock yang diaktifkan
* Akses ke model Claude yang diinginkan (misalnya, Claude Sonnet 4.6) di Bedrock
* AWS CLI terinstal dan dikonfigurasi (opsional - hanya diperlukan jika Anda tidak memiliki mekanisme lain untuk mendapatkan kredensial)
* Izin IAM yang sesuai

Untuk masuk dengan kredensial Bedrock Anda sendiri, ikuti [Masuk dengan Bedrock](#sign-in-with-bedrock) di bawah ini. Untuk menerapkan Claude Code di seluruh tim, gunakan langkah [pengaturan manual](#set-up-manually) dan [pin versi model Anda](#4-pin-model-versions) sebelum melakukan peluncuran.

## Masuk dengan Bedrock

Jika Anda memiliki kredensial AWS dan ingin mulai menggunakan Claude Code melalui Bedrock, wizard login akan memandu Anda. Anda menyelesaikan prasyarat sisi AWS sekali per akun; wizard menangani sisi Claude Code.

<Steps>
  <Step title="Aktifkan model Anthropic di akun AWS Anda">
    Di [konsol Amazon Bedrock](https://console.aws.amazon.com/bedrock/), buka katalog Model, pilih model Anthropic, dan kirimkan formulir kasus penggunaan. Akses diberikan segera setelah pengiriman. Lihat [Kirimkan detail kasus penggunaan](#1-submit-use-case-details) untuk AWS Organizations dan [konfigurasi IAM](#iam-configuration) untuk izin yang dibutuhkan peran Anda.
  </Step>

  <Step title="Mulai Claude Code dan pilih Bedrock">
    Jalankan `claude`. Pada prompt login, pilih **3rd-party platform**, kemudian **Amazon Bedrock**.
  </Step>

  <Step title="Ikuti prompt wizard">
    Pilih cara Anda melakukan autentikasi ke AWS: profil AWS yang terdeteksi dari direktori `~/.aws` Anda, kunci API Bedrock, kunci akses dan rahasia, atau kredensial yang sudah ada di lingkungan Anda. Wizard mengambil wilayah Anda, memverifikasi model Claude mana yang dapat dijalankan akun Anda, dan memungkinkan Anda untuk meminnya. Ini menyimpan hasilnya ke blok `env` dari [file pengaturan pengguna Anda](/id/settings), jadi Anda tidak perlu mengekspor variabel lingkungan sendiri.
  </Step>
</Steps>

Setelah Anda masuk, jalankan `/setup-bedrock` kapan saja untuk membuka kembali wizard dan mengubah kredensial, wilayah, atau pin model Anda.

## Pengaturan manual

Untuk mengonfigurasi Bedrock melalui variabel lingkungan alih-alih wizard, misalnya di CI atau peluncuran perusahaan yang ditulis skrip, ikuti langkah-langkah di bawah ini.

### 1. Kirimkan detail kasus penggunaan

Pengguna pertama kali dari model Anthropic harus mengirimkan detail kasus penggunaan sebelum memanggil model. Ini dilakukan sekali per akun AWS.

1. Pastikan Anda memiliki izin IAM yang tepat seperti yang dijelaskan di bawah
2. Navigasikan ke [konsol Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Pilih model Anthropic dari **Model catalog**
4. Lengkapi formulir kasus penggunaan. Akses diberikan segera setelah pengiriman.

Jika Anda menggunakan AWS Organizations, Anda dapat mengirimkan formulir sekali dari akun manajemen menggunakan [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). Panggilan ini memerlukan izin IAM `bedrock:PutUseCaseForModelAccess`. Persetujuan meluas ke akun anak secara otomatis.

### 2. Konfigurasi kredensial AWS

Claude Code menggunakan rantai kredensial SDK AWS default. Atur kredensial Anda menggunakan salah satu metode berikut:

**Opsi A: Konfigurasi AWS CLI**

```bash theme={null}
aws configure
```

**Opsi B: Variabel lingkungan (kunci akses)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Opsi C: Variabel lingkungan (profil SSO)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Opsi D: Kredensial AWS Management Console**

```bash theme={null}
aws login
```

[Pelajari lebih lanjut](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) tentang `aws login`.

**Opsi E: Kunci API Bedrock**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Kunci API Bedrock menyediakan metode autentikasi yang lebih sederhana tanpa memerlukan kredensial AWS lengkap. [Pelajari lebih lanjut tentang kunci API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Konfigurasi kredensial lanjutan

Claude Code mendukung penyegaran kredensial otomatis untuk AWS SSO dan penyedia identitas perusahaan. Tambahkan pengaturan ini ke file pengaturan Claude Code Anda (lihat [Settings](/id/settings) untuk lokasi file).

Kedua pengaturan ini memiliki kondisi pemicu yang berbeda:

* **`awsAuthRefresh`**: berjalan hanya ketika Claude Code mendeteksi bahwa kredensial AWS Anda telah kedaluwarsa, baik secara lokal berdasarkan stempel waktu mereka atau ketika Bedrock mengembalikan kesalahan kredensial, kemudian mencoba ulang permintaan dengan kredensial yang disegarkan.
* **`awsCredentialExport`**: berjalan saat awal sesi dan pada setiap pemuatan ulang kredensial, bahkan ketika kredensial di rantai penyedia kredensial default AWS Anda masih valid. Gunakan ini ketika akun Bedrock Anda memerlukan kredensial lintas akun yang berbeda dari yang akan diselesaikan oleh rantai penyedia default.

##### Contoh konfigurasi

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Pengaturan konfigurasi dijelaskan

**`awsAuthRefresh`**: Gunakan ini untuk perintah yang memodifikasi direktori `.aws`, seperti memperbarui kredensial, cache SSO, atau file konfigurasi. Output perintah ditampilkan kepada pengguna, tetapi input interaktif tidak didukung. Ini bekerja dengan baik untuk alur SSO berbasis browser di mana CLI menampilkan URL atau kode dan Anda menyelesaikan autentikasi di browser.

**`awsCredentialExport`**: Hanya gunakan ini jika Anda tidak dapat memodifikasi `.aws` dan harus secara langsung mengembalikan kredensial. Perintah ini berjalan setiap kali kredensial perlu disegarkan, bukan hanya ketika kredensial telah kedaluwarsa. Output ditangkap secara diam-diam dan tidak ditampilkan kepada pengguna. Perintah harus menampilkan JSON dalam format ini:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Konfigurasi Claude Code

Atur variabel lingkungan berikut untuk mengaktifkan Bedrock:

```bash theme={null}
# Aktifkan integrasi Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # atau wilayah pilihan Anda

# Opsional: Ganti wilayah AWS untuk model kecil/cepat (Bedrock dan Mantle).
# Di Bedrock, tidak berpengaruh tanpa ANTHROPIC_DEFAULT_HAIKU_MODEL
# atau ANTHROPIC_SMALL_FAST_MODEL yang sudah usang diatur.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Opsional: Ganti URL endpoint Bedrock untuk endpoint khusus atau gateway
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Saat mengaktifkan Bedrock untuk Claude Code, perhatikan hal berikut:

* `AWS_REGION` adalah variabel lingkungan yang diperlukan. Claude Code tidak membaca dari file konfigurasi `.aws` untuk pengaturan ini.
* Saat menggunakan Bedrock, perintah `/login` dan `/logout` dinonaktifkan karena autentikasi ditangani melalui kredensial AWS.
* Anda dapat menggunakan file pengaturan untuk variabel lingkungan seperti `AWS_PROFILE` yang tidak ingin Anda bocorkan ke proses lain. Lihat [Settings](/id/settings) untuk informasi lebih lanjut.

### 4. Pin versi model

<Warning>
  Pin versi model spesifik saat menerapkan ke beberapa pengguna. Tanpa pinning, alias model seperti `sonnet` dan `opus` diselesaikan ke versi terbaru, yang mungkin belum tersedia di akun Bedrock Anda ketika Anthropic merilis pembaruan. Claude Code [kembali](#startup-model-checks) ke versi sebelumnya saat startup ketika versi terbaru tidak tersedia, tetapi pinning memungkinkan Anda mengontrol kapan pengguna Anda beralih ke model baru.
</Warning>

Atur variabel lingkungan ini ke ID model Bedrock spesifik.

Tanpa `ANTHROPIC_DEFAULT_OPUS_MODEL`, alias `opus` di Bedrock diselesaikan ke Opus 4.6. Atur ke ID Opus 4.7 untuk menggunakan model terbaru:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Variabel ini menggunakan ID profil inferensi lintas wilayah (dengan awalan `us.`). Jika Anda menggunakan awalan wilayah berbeda atau profil inferensi aplikasi, sesuaikan sesuai kebutuhan. Untuk ID model saat ini dan warisan, lihat [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Lihat [Model configuration](/id/model-config#pin-models-for-third-party-deployments) untuk daftar lengkap variabel lingkungan.

Claude Code menggunakan model default ini ketika tidak ada variabel pinning yang diatur:

| Jenis model       | Nilai default                                  |
| :---------------- | :--------------------------------------------- |
| Model utama       | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Model kecil/cepat | Sama dengan model utama                        |

Tugas latar belakang seperti pembuatan judul sesi menggunakan model kecil/cepat, biasanya model kelas Haiku. Di Bedrock, Claude Code secara default mengatur ini ke model utama karena Haiku mungkin tidak diaktifkan di setiap akun atau wilayah. Untuk menggunakan Haiku untuk tugas latar belakang, atur `ANTHROPIC_DEFAULT_HAIKU_MODEL` ke ID model yang tersedia di akun Anda.

Untuk menyesuaikan model lebih lanjut, gunakan salah satu metode berikut:

```bash theme={null}
# Menggunakan ID profil inferensi
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Menggunakan ARN profil inferensi aplikasi
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Opsional: Nonaktifkan prompt caching jika diperlukan
export DISABLE_PROMPT_CACHING=1

# Opsional: Minta TTL cache prompt 1 jam alih-alih default 5 menit
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) mungkin tidak tersedia di semua wilayah. Cache writes dengan TTL 1 jam ditagih dengan tarif lebih tinggi daripada writes 5 menit.</Note>

#### Petakan setiap versi model ke profil inferensi

Variabel lingkungan `ANTHROPIC_DEFAULT_*_MODEL` mengonfigurasi satu profil inferensi per keluarga model. Jika organisasi Anda perlu mengekspos beberapa versi dari keluarga yang sama di pemilih `/model`, masing-masing dirutekan ke ARN profil inferensi aplikasi sendiri, gunakan pengaturan `modelOverrides` di [file pengaturan](/id/settings#settings-files) Anda sebagai gantinya.

Contoh ini memetakan empat versi Opus ke ARN yang berbeda sehingga pengguna dapat beralih di antara mereka tanpa melewati profil inferensi organisasi Anda:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Ketika pengguna memilih salah satu versi ini di `/model`, Claude Code memanggil Bedrock dengan ARN yang dipetakan. Versi tanpa override kembali ke ID model Bedrock bawaan atau profil inferensi yang cocok yang ditemukan saat startup. Lihat [Override model IDs per version](/id/model-config#override-model-ids-per-version) untuk detail tentang bagaimana override berinteraksi dengan `availableModels` dan pengaturan model lainnya.

## Pemeriksaan model startup

Ketika Claude Code dimulai dengan Bedrock dikonfigurasi, Claude Code memverifikasi bahwa model yang dimaksudkan untuk digunakan dapat diakses di akun Anda. Pemeriksaan ini memerlukan Claude Code v2.1.94 atau lebih baru.

Jika Anda telah mempin versi model yang lebih lama dari default Claude Code saat ini, dan akun Anda dapat memanggil versi yang lebih baru, Claude Code meminta Anda untuk memperbarui pin. Menerima menulis ID model baru ke [file pengaturan pengguna Anda](/id/settings) dan memulai ulang Claude Code. Menolak diingat sampai perubahan versi default berikutnya. Pin yang menunjuk ke [ARN profil inferensi aplikasi](#map-each-model-version-to-an-inference-profile) dilewati, karena dikelola oleh administrator Anda.

Jika Anda belum mempin model dan default saat ini tidak tersedia di akun Anda, Claude Code kembali ke versi sebelumnya untuk sesi saat ini dan menampilkan pemberitahuan. Fallback tidak disimpan. Aktifkan model yang lebih baru di akun Bedrock Anda atau [pin versi](#4-pin-model-versions) untuk membuat pilihan permanen.

## Konfigurasi IAM

Buat kebijakan IAM dengan izin yang diperlukan untuk Claude Code:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

Untuk izin yang lebih ketat, Anda dapat membatasi Resource ke ARN profil inferensi spesifik.

`bedrock:GetInferenceProfile` memungkinkan Claude Code menyelesaikan [ARN profil inferensi aplikasi](#map-each-model-version-to-an-inference-profile) ke model fondasi pendukungnya, yang digunakan untuk memilih bentuk permintaan yang benar untuk model tersebut.

Jika token tidak memiliki izin ini, Claude Code pulih secara otomatis dengan mencoba ulang sekali dengan bentuk alternatif, sehingga permintaan tetap berhasil tetapi setiap model baru menambahkan perjalanan bolak-balik ekstra. Memberikan izin menghindari percobaan ulang. Ini paling sering berlaku untuk penyebaran `AWS_BEARER_TOKEN_BEDROCK`, di mana kebijakan token biasanya lebih sempit daripada peran IAM penuh.

Untuk detail, lihat [dokumentasi IAM Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Buat akun AWS khusus untuk Claude Code untuk menyederhanakan pelacakan biaya dan kontrol akses.
</Note>

## Jendela konteks token 1M

Claude Opus 4.7, Opus 4.6, dan Sonnet 4.6 mendukung [jendela konteks token 1M](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) di Amazon Bedrock. Claude Code secara otomatis mengaktifkan jendela konteks yang diperluas ketika Anda memilih varian model 1M.

[Wizard pengaturan](#sign-in-with-bedrock) menawarkan opsi konteks 1M ketika mempin model. Untuk mengaktifkannya untuk model yang dipinnya secara manual, tambahkan `[1m]` ke ID model. Lihat [Pin models for third-party deployments](/id/model-config#pin-models-for-third-party-deployments) untuk detail.

## Tingkat layanan

[Tingkat layanan Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html) memungkinkan Anda menukar biaya terhadap latensi. Atur `ANTHROPIC_BEDROCK_SERVICE_TIER` ke `default`, `flex`, atau `priority`:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code mengirimkan ini sebagai header `X-Amzn-Bedrock-Service-Tier` pada setiap permintaan. Ketersediaan tingkat bervariasi menurut model dan wilayah. Kapasitas yang dicadangkan menggunakan [throughput yang disediakan](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) ARN sebagai ID model alih-alih pengaturan ini.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) memungkinkan Anda menerapkan penyaringan konten untuk Claude Code. Buat Guardrail di [konsol Amazon Bedrock](https://console.aws.amazon.com/bedrock/), publikasikan versi, kemudian tambahkan header Guardrail ke [file pengaturan](/id/settings) Anda. Aktifkan inferensi Cross-Region pada Guardrail Anda jika Anda menggunakan profil inferensi lintas wilayah.

Contoh konfigurasi:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Gunakan endpoint Mantle

Mantle adalah endpoint Amazon Bedrock yang melayani model Claude melalui bentuk API Anthropic asli daripada Bedrock Invoke API. Ini menggunakan kredensial AWS yang sama, izin IAM, dan konfigurasi `awsAuthRefresh` yang dijelaskan sebelumnya di halaman ini.

<Note>
  Mantle memerlukan Claude Code v2.1.94 atau lebih baru. Jalankan `claude --version` untuk memeriksa.
</Note>

### Aktifkan Mantle

Dengan kredensial AWS sudah dikonfigurasi, atur `CLAUDE_CODE_USE_MANTLE` untuk merutekan permintaan ke endpoint Mantle:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code membuat URL endpoint dari `AWS_REGION`. Untuk menggantinya untuk endpoint khusus atau gateway, atur `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Jalankan `/status` di dalam Claude Code untuk mengonfirmasi. Baris penyedia menunjukkan `Amazon Bedrock (Mantle)` ketika Mantle aktif.

### Pilih model Mantle

Mantle menggunakan ID model dengan awalan `anthropic.` dan tanpa akhiran versi, misalnya `anthropic.claude-haiku-4-5`. Model yang tersedia untuk akun Anda tergantung pada apa yang telah diberikan organisasi Anda; ID model tambahan tercantum dalam materi onboarding Anda dari AWS. Hubungi tim akun AWS Anda untuk meminta akses ke model yang diizinkan.

Atur model dengan flag `--model` atau dengan `/model` di dalam Claude Code:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Jalankan Mantle bersama Invoke API

Model yang tersedia untuk Anda di Mantle mungkin tidak mencakup setiap model yang Anda gunakan hari ini. Menetapkan `CLAUDE_CODE_USE_BEDROCK` dan `CLAUDE_CODE_USE_MANTLE` memungkinkan Claude Code memanggil kedua endpoint dari sesi yang sama. ID model yang cocok dengan format Mantle dirutekan ke Mantle, dan semua ID model lainnya pergi ke Bedrock Invoke API.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Untuk menampilkan model Mantle di pemilih `/model`, daftarkan ID-nya di `availableModels` di [file pengaturan](/id/settings) Anda. Pengaturan ini juga membatasi pemilih ke entri yang terdaftar, jadi sertakan setiap alias yang ingin Anda tetap tersedia:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Entri dengan awalan `anthropic.` ditambahkan sebagai opsi pemilih khusus dan dirutekan ke Mantle. Ganti `anthropic.claude-haiku-4-5` dengan ID model yang telah diberikan akun Anda. Lihat [Restrict model selection](/id/model-config#restrict-model-selection) untuk cara `availableModels` berinteraksi dengan pengaturan model lainnya.

Ketika kedua penyedia aktif, `/status` menunjukkan `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Rutekan Mantle melalui gateway

Jika organisasi Anda merutekan lalu lintas model melalui [LLM gateway](/id/llm-gateway) terpusat yang menyuntikkan kredensial AWS sisi server, nonaktifkan autentikasi sisi klien sehingga Claude Code mengirim permintaan tanpa tanda tangan SigV4 atau header `x-api-key`:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Variabel lingkungan Mantle

Variabel ini khusus untuk endpoint Mantle. Lihat [Environment variables](/id/env-vars) untuk daftar lengkap.

| Variabel                                | Tujuan                                                               |
| :-------------------------------------- | :------------------------------------------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | Aktifkan endpoint Mantle. Atur ke `1` atau `true`.                   |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Ganti URL endpoint Mantle default                                    |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Lewati autentikasi sisi klien untuk pengaturan proxy                 |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Ganti wilayah AWS untuk model kelas Haiku (dibagikan dengan Bedrock) |

## Pemecahan Masalah

### Loop autentikasi dengan SSO dan proxy perusahaan

Jika tab browser muncul berulang kali saat menggunakan AWS SSO, hapus pengaturan `awsAuthRefresh` dari [file pengaturan](/id/settings) Anda. Ini dapat terjadi ketika VPN perusahaan atau proxy inspeksi TLS mengganggu alur browser SSO. Claude Code memperlakukan koneksi yang terputus sebagai kegagalan autentikasi, menjalankan kembali `awsAuthRefresh`, dan loop tanpa batas.

Jika lingkungan jaringan Anda mengganggu alur SSO berbasis browser otomatis, gunakan `aws sso login` secara manual sebelum memulai Claude Code alih-alih mengandalkan `awsAuthRefresh`.

### Masalah wilayah

Jika Anda mengalami masalah wilayah:

* Periksa ketersediaan model: `aws bedrock list-inference-profiles --region your-region`
* Beralih ke wilayah yang didukung: `export AWS_REGION=us-east-1`
* Pertimbangkan menggunakan profil inferensi untuk akses lintas wilayah

Jika Anda menerima kesalahan "on-demand throughput isn't supported":

* Tentukan model sebagai ID [profil inferensi](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code menggunakan [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) Bedrock dan tidak mendukung Converse API.

### Kesalahan endpoint Mantle

Jika `/status` tidak menunjukkan `Amazon Bedrock (Mantle)` setelah Anda menetapkan `CLAUDE_CODE_USE_MANTLE`, variabel tidak mencapai proses. Konfirmasi bahwa variabel diekspor di shell tempat Anda meluncurkan `claude`, atau atur di blok `env` dari [file pengaturan](/id/settings) Anda.

A `403` dari endpoint Mantle dengan kredensial yang valid berarti akun AWS Anda belum diberikan akses ke model yang Anda minta. Hubungi tim akun AWS Anda untuk meminta akses.

A `400` yang menyebutkan ID model berarti model itu tidak dilayani di Mantle. Mantle memiliki lineup model sendiri yang terpisah dari katalog Bedrock standar, jadi ID profil inferensi seperti `us.anthropic.claude-sonnet-4-6` tidak akan berfungsi. Gunakan ID format Mantle, atau aktifkan [kedua endpoint](#run-mantle-alongside-the-invoke-api) sehingga Claude Code merutekan setiap permintaan ke endpoint tempat model tersedia.

## Sumber daya tambahan

* [Dokumentasi Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Harga Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Profil inferensi Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Burndown token Bedrock dan kuota](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code di Amazon Bedrock: Panduan Pengaturan Cepat](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementasi Pemantauan Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
