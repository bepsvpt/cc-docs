> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code pada Google Vertex AI

> Pelajari tentang mengonfigurasi Claude Code melalui Google Vertex AI, termasuk pengaturan, konfigurasi IAM, dan pemecahan masalah.

## Prasyarat

Sebelum mengonfigurasi Claude Code dengan Vertex AI, pastikan Anda memiliki:

* Akun Google Cloud Platform (GCP) dengan penagihan diaktifkan
* Proyek GCP dengan Vertex AI API diaktifkan
* Akses ke model Claude yang diinginkan (misalnya, Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) terinstal dan dikonfigurasi
* Kuota dialokasikan di wilayah GCP yang diinginkan

## Konfigurasi Wilayah

Claude Code dapat digunakan dengan kedua titik akhir Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) dan regional.

<Note>
  Vertex AI mungkin tidak mendukung model default Claude Code di semua wilayah. Anda mungkin perlu beralih ke [wilayah atau model yang didukung](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  Vertex AI mungkin tidak mendukung model default Claude Code pada titik akhir global. Anda mungkin perlu beralih ke titik akhir regional atau [model yang didukung](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
</Note>

## Pengaturan

### 1. Aktifkan Vertex AI API

Aktifkan Vertex AI API di proyek GCP Anda:

```bash  theme={null}
# Atur ID proyek Anda
gcloud config set project YOUR-PROJECT-ID

# Aktifkan Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Minta akses model

Minta akses ke model Claude di Vertex AI:

1. Navigasikan ke [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Cari model "Claude"
3. Minta akses ke model Claude yang diinginkan (misalnya, Claude Sonnet 4.5)
4. Tunggu persetujuan (mungkin memakan waktu 24-48 jam)

### 3. Konfigurasi kredensial GCP

Claude Code menggunakan autentikasi Google Cloud standar.

Untuk informasi lebih lanjut, lihat [dokumentasi autentikasi Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Saat melakukan autentikasi, Claude Code akan secara otomatis menggunakan ID proyek dari variabel lingkungan `ANTHROPIC_VERTEX_PROJECT_ID`. Untuk menimpanya, atur salah satu variabel lingkungan ini: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, atau `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Konfigurasi Claude Code

Atur variabel lingkungan berikut:

```bash  theme={null}
# Aktifkan integrasi Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Opsional: Nonaktifkan prompt caching jika diperlukan
export DISABLE_PROMPT_CACHING=1

# Ketika CLOUD_ML_REGION=global, timpa wilayah untuk model yang tidak didukung
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Opsional: Timpa wilayah untuk model spesifik lainnya
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) didukung secara otomatis ketika Anda menentukan flag ephemeral `cache_control`. Untuk menonaktifkannya, atur `DISABLE_PROMPT_CACHING=1`. Untuk batas laju yang lebih tinggi, hubungi dukungan Google Cloud.
</Note>

<Note>
  Saat menggunakan Vertex AI, perintah `/login` dan `/logout` dinonaktifkan karena autentikasi ditangani melalui kredensial Google Cloud.
</Note>

### 5. Konfigurasi model

Claude Code menggunakan model default ini untuk Vertex AI:

| Jenis model       | Nilai default                |
| :---------------- | :--------------------------- |
| Model utama       | `claude-sonnet-4-5@20250929` |
| Model kecil/cepat | `claude-haiku-4-5@20251001`  |

<Note>
  Untuk pengguna Vertex AI, Claude Code tidak akan secara otomatis meningkatkan dari Haiku 3.5 ke Haiku 4.5. Untuk beralih secara manual ke model Haiku yang lebih baru, atur variabel lingkungan `ANTHROPIC_DEFAULT_HAIKU_MODEL` ke nama model lengkap (misalnya, `claude-haiku-4-5@20251001`).
</Note>

Untuk menyesuaikan model:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Konfigurasi IAM

Tetapkan izin IAM yang diperlukan:

Peran `roles/aiplatform.user` mencakup izin yang diperlukan:

* `aiplatform.endpoints.predict` - Diperlukan untuk invokasi model dan penghitungan token

Untuk izin yang lebih ketat, buat peran kustom dengan hanya izin di atas.

Untuk detail, lihat [dokumentasi Vertex IAM](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Kami merekomendasikan membuat proyek GCP khusus untuk Claude Code untuk menyederhanakan pelacakan biaya dan kontrol akses.
</Note>

## context window 1M token

Claude Sonnet 4 dan Sonnet 4.5 mendukung [context window 1M token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) pada Vertex AI.

<Note>
  context window 1M token saat ini dalam beta. Untuk menggunakan context window yang diperluas, sertakan header beta `context-1m-2025-08-07` dalam permintaan Vertex AI Anda.
</Note>

## Pemecahan Masalah

Jika Anda mengalami masalah kuota:

* Periksa kuota saat ini atau minta peningkatan kuota melalui [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Jika Anda mengalami kesalahan "model not found" 404:

* Konfirmasi model diaktifkan di [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifikasi Anda memiliki akses ke wilayah yang ditentukan
* Jika menggunakan `CLOUD_ML_REGION=global`, periksa bahwa model Anda mendukung titik akhir global di [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) di bawah "Supported features". Untuk model yang tidak mendukung titik akhir global, baik:
  * Tentukan model yang didukung melalui `ANTHROPIC_MODEL` atau `ANTHROPIC_SMALL_FAST_MODEL`, atau
  * Atur titik akhir regional menggunakan variabel lingkungan `VERTEX_REGION_<MODEL_NAME>`

Jika Anda mengalami kesalahan 429:

* Untuk titik akhir regional, pastikan model utama dan model kecil/cepat didukung di wilayah pilihan Anda
* Pertimbangkan untuk beralih ke `CLOUD_ML_REGION=global` untuk ketersediaan yang lebih baik

## Sumber daya tambahan

* [Dokumentasi Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Harga Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Kuota dan batas Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
