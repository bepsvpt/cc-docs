> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Claude Code di Amazon Bedrock

> Pelajari tentang mengonfigurasi Claude Code melalui Amazon Bedrock, termasuk pengaturan, konfigurasi IAM, dan pemecahan masalah.

## Prasyarat

Sebelum mengonfigurasi Claude Code dengan Bedrock, pastikan Anda memiliki:

* Akun AWS dengan akses Bedrock yang diaktifkan
* Akses ke model Claude yang diinginkan (misalnya, Claude Sonnet 4.6) di Bedrock
* AWS CLI terinstal dan dikonfigurasi (opsional - hanya diperlukan jika Anda tidak memiliki mekanisme lain untuk mendapatkan kredensial)
* Izin IAM yang sesuai

<Note>
  Jika Anda menerapkan Claude Code ke beberapa pengguna, [pin versi model Anda](#4-pin-model-versions) untuk mencegah kerusakan ketika Anthropic merilis model baru.
</Note>

## Pengaturan

### 1. Kirimkan detail kasus penggunaan

Pengguna pertama kali dari model Anthropic harus mengirimkan detail kasus penggunaan sebelum memanggil model. Ini dilakukan sekali per akun.

1. Pastikan Anda memiliki izin IAM yang tepat (lihat lebih lanjut di bawah)
2. Navigasikan ke [konsol Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Pilih **Chat/Text playground**
4. Pilih model Anthropic apa pun dan Anda akan diminta untuk mengisi formulir kasus penggunaan

### 2. Konfigurasi kredensial AWS

Claude Code menggunakan rantai kredensial SDK AWS default. Atur kredensial Anda menggunakan salah satu metode berikut:

**Opsi A: Konfigurasi AWS CLI**

```bash  theme={null}
aws configure
```

**Opsi B: Variabel lingkungan (kunci akses)**

```bash  theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Opsi C: Variabel lingkungan (profil SSO)**

```bash  theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Opsi D: Kredensial AWS Management Console**

```bash  theme={null}
aws login
```

[Pelajari lebih lanjut](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) tentang `aws login`.

**Opsi E: Kunci API Bedrock**

```bash  theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Kunci API Bedrock menyediakan metode autentikasi yang lebih sederhana tanpa memerlukan kredensial AWS lengkap. [Pelajari lebih lanjut tentang kunci API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Konfigurasi kredensial lanjutan

Claude Code mendukung penyegaran kredensial otomatis untuk AWS SSO dan penyedia identitas perusahaan. Tambahkan pengaturan ini ke file pengaturan Claude Code Anda (lihat [Settings](/id/settings) untuk lokasi file).

Ketika Claude Code mendeteksi bahwa kredensial AWS Anda telah kedaluwarsa (baik secara lokal berdasarkan stempel waktu mereka atau ketika Bedrock mengembalikan kesalahan kredensial), Claude Code akan secara otomatis menjalankan perintah `awsAuthRefresh` dan/atau `awsCredentialExport` yang dikonfigurasi untuk mendapatkan kredensial baru sebelum mencoba ulang permintaan.

##### Contoh konfigurasi

```json  theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Pengaturan konfigurasi dijelaskan

**`awsAuthRefresh`**: Gunakan ini untuk perintah yang memodifikasi direktori `.aws`, seperti memperbarui kredensial, cache SSO, atau file konfigurasi. Output perintah ditampilkan kepada pengguna, tetapi input interaktif tidak didukung. Ini bekerja dengan baik untuk alur SSO berbasis browser di mana CLI menampilkan URL atau kode dan Anda menyelesaikan autentikasi di browser.

**`awsCredentialExport`**: Hanya gunakan ini jika Anda tidak dapat memodifikasi `.aws` dan harus secara langsung mengembalikan kredensial. Output ditangkap secara diam-diam dan tidak ditampilkan kepada pengguna. Perintah harus menampilkan JSON dalam format ini:

```json  theme={null}
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

```bash  theme={null}
# Aktifkan integrasi Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # atau wilayah pilihan Anda

# Opsional: Ganti wilayah untuk model kecil/cepat (Haiku)
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
  Pin versi model spesifik untuk setiap penerapan. Jika Anda menggunakan alias model (`sonnet`, `opus`, `haiku`) tanpa pinning, Claude Code mungkin mencoba menggunakan versi model yang lebih baru yang tidak tersedia di akun Bedrock Anda, merusak pengguna yang ada ketika Anthropic merilis pembaruan.
</Warning>

Atur variabel lingkungan ini ke ID model Bedrock spesifik:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Variabel ini menggunakan ID profil inferensi lintas wilayah (dengan awalan `us.`). Jika Anda menggunakan awalan wilayah berbeda atau profil inferensi aplikasi, sesuaikan sesuai kebutuhan. Untuk ID model saat ini dan warisan, lihat [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Lihat [Model configuration](/id/model-config#pin-models-for-third-party-deployments) untuk daftar lengkap variabel lingkungan.

Claude Code menggunakan model default ini ketika tidak ada variabel pinning yang diatur:

| Jenis model       | Nilai default                                  |
| :---------------- | :--------------------------------------------- |
| Model utama       | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Model kecil/cepat | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

Untuk menyesuaikan model lebih lanjut, gunakan salah satu metode berikut:

```bash  theme={null}
# Menggunakan ID profil inferensi
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Menggunakan ARN profil inferensi aplikasi
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Opsional: Nonaktifkan prompt caching jika diperlukan
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) mungkin tidak tersedia di semua wilayah.</Note>

#### Petakan setiap versi model ke profil inferensi

Variabel lingkungan `ANTHROPIC_DEFAULT_*_MODEL` mengonfigurasi satu profil inferensi per keluarga model. Jika organisasi Anda perlu mengekspos beberapa versi dari keluarga yang sama di pemilih `/model`, masing-masing dirutekan ke ARN profil inferensi aplikasi sendiri, gunakan pengaturan `modelOverrides` di [file pengaturan](/id/settings#settings-files) Anda sebagai gantinya.

Contoh ini memetakan tiga versi Opus ke ARN yang berbeda sehingga pengguna dapat beralih di antara mereka tanpa melewati profil inferensi organisasi Anda:

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Ketika pengguna memilih salah satu versi ini di `/model`, Claude Code memanggil Bedrock dengan ARN yang dipetakan. Versi tanpa override kembali ke ID model Bedrock bawaan atau profil inferensi yang cocok yang ditemukan saat startup. Lihat [Override model IDs per version](/id/model-config#override-model-ids-per-version) untuk detail tentang bagaimana override berinteraksi dengan `availableModels` dan pengaturan model lainnya.

## Jendela konteks token 1M

Claude Opus 4.6 dan Sonnet 4.6 mendukung [jendela konteks token 1M](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) di Amazon Bedrock. Claude Code secara otomatis mengaktifkan jendela konteks yang diperluas ketika Anda memilih varian model 1M.

Untuk mengaktifkan jendela konteks 1M untuk model yang Anda pin, tambahkan `[1m]` ke ID model. Lihat [Pin models for third-party deployments](/id/model-config#pin-models-for-third-party-deployments) untuk detail.

## Konfigurasi IAM

Buat kebijakan IAM dengan izin yang diperlukan untuk Claude Code:

```json  theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
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

Untuk detail, lihat [dokumentasi IAM Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Buat akun AWS khusus untuk Claude Code untuk menyederhanakan pelacakan biaya dan kontrol akses.
</Note>

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) memungkinkan Anda menerapkan penyaringan konten untuk Claude Code. Buat Guardrail di [konsol Amazon Bedrock](https://console.aws.amazon.com/bedrock/), publikasikan versi, kemudian tambahkan header Guardrail ke [file pengaturan](/id/settings) Anda. Aktifkan inferensi Cross-Region pada Guardrail Anda jika Anda menggunakan profil inferensi lintas wilayah.

Contoh konfigurasi:

```json  theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

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

## Sumber daya tambahan

* [Dokumentasi Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Harga Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Profil inferensi Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code di Amazon Bedrock: Panduan Pengaturan Cepat](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementasi Pemantauan Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
