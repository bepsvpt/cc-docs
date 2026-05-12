> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi LLM gateway

> Pelajari cara mengonfigurasi Claude Code untuk bekerja dengan solusi LLM gateway. Mencakup persyaratan gateway, konfigurasi autentikasi, pemilihan model, dan pengaturan endpoint khusus penyedia.

LLM gateway menyediakan lapisan proxy terpusat antara Claude Code dan penyedia model, sering kali menyediakan:

* **Autentikasi terpusat** - Titik tunggal untuk manajemen kunci API
* **Pelacakan penggunaan** - Pantau penggunaan di seluruh tim dan proyek
* **Kontrol biaya** - Terapkan anggaran dan batas laju
* **Pencatatan audit** - Lacak semua interaksi model untuk kepatuhan
* **Perutean model** - Beralih antar penyedia tanpa perubahan kode

## Persyaratan gateway

Agar LLM gateway dapat bekerja dengan Claude Code, gateway harus memenuhi persyaratan berikut:

**Format API**

Gateway harus mengekspos ke klien setidaknya salah satu format API berikut:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * Harus meneruskan header permintaan: `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * Harus mempertahankan bidang badan permintaan: `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Harus meneruskan header permintaan: `anthropic-beta`, `anthropic-version`

Kegagalan untuk meneruskan header atau mempertahankan bidang badan dapat mengakibatkan fungsionalitas berkurang atau ketidakmampuan menggunakan fitur Claude Code.

<Note>
  Claude Code menentukan fitur mana yang akan diaktifkan berdasarkan format API. Saat menggunakan format Anthropic Messages dengan Bedrock atau Vertex, Anda mungkin perlu mengatur variabel lingkungan `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

**Header permintaan**

Claude Code menyertakan header berikut pada permintaan API:

| Header                          | Deskripsi                                                                                                                                                                                                                                                                                              |
| :------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `X-Claude-Code-Session-Id`      | Pengidentifikasi unik untuk sesi Claude Code saat ini. Proxy dapat menggunakan ini untuk mengagregasi semua permintaan API dari sesi tunggal tanpa mengurai badan permintaan.                                                                                                                          |
| `X-Claude-Code-Agent-Id`        | Pengidentifikasi subagen atau rekan kerja yang mengeluarkan permintaan. Proxy Anda dapat menggunakan ini untuk mengatribusikan biaya API ke subagen paralel individual dalam sesi, tanpa mengurai badan permintaan. Hanya ada untuk permintaan yang dibuat oleh subagen atau rekan kerja dalam proses. |
| `X-Claude-Code-Parent-Agent-Id` | Pengidentifikasi agen yang melahirkan agen yang membuat permintaan. Gunakan ini dengan `X-Claude-Code-Agent-Id` untuk mengatribusikan biaya API di seluruh agen bersarang dalam proxy Anda. Hanya ada ketika agen yang meminta itu sendiri dilahirkan oleh agen lain.                                  |

Kedua header ID agen adalah pengidentifikasi per-spawn yang bersifat sementara, bukan ID pengguna atau perangkat yang persisten.

Claude Code juga menambahkan blok atribusi singkat ke prompt sistem yang berisi versi klien dan sidik jari yang berasal dari percakapan. API Anthropic menghapus blok ini sebelum memproses, sehingga tidak mempengaruhi prompt caching pihak pertama. Jika gateway Anda menerapkan cache prompt sendiri yang dikunci pada badan permintaan lengkap, atur [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/id/env-vars) untuk menghilangkannya.

## Konfigurasi

### Pemilihan model

Secara default, Claude Code menggunakan nama model standar untuk format API yang dipilih.

Ketika `ANTHROPIC_BASE_URL` menunjuk ke gateway yang mengekspos format Anthropic Messages, Claude Code dapat menanyakan endpoint `/v1/models` gateway saat startup dan menambahkan model yang dikembalikan ke pemilih `/model`. Atur `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` untuk mengaktifkan ini. Penemuan dimatikan secara default sehingga gateway yang didukung oleh kunci API bersama tidak menampilkan setiap model yang dapat diakses kunci ke setiap pengguna. Setiap entri yang ditemukan diberi label "From gateway" dan menggunakan field `display_name` dari respons ketika satu disediakan. Ini memerlukan Claude Code v2.1.129 atau lebih baru.

Penemuan hanya berlaku untuk format Anthropic Messages. Ini tidak berjalan untuk endpoint pass-through Bedrock atau Vertex, dan tidak berjalan ketika `ANTHROPIC_BASE_URL` tidak diatur atau menunjuk ke `api.anthropic.com`.

Permintaan penemuan mengautentikasi dengan cara yang sama seperti permintaan inferensi: ia mengirimkan `ANTHROPIC_AUTH_TOKEN` sebagai token bearer, atau `ANTHROPIC_API_KEY` sebagai header `x-api-key` ketika tidak ada token auth yang diatur, bersama dengan header apa pun dari `ANTHROPIC_CUSTOM_HEADERS`. Hanya model yang ID-nya dimulai dengan `claude` atau `anthropic` yang ditambahkan ke pemilih. Hasil disimpan dalam cache ke `~/.claude/cache/gateway-models.json` dan disegarkan pada setiap startup. Jika permintaan gagal atau gateway tidak mengimplementasikan `/v1/models`, pemilih kembali ke daftar cache dari startup sebelumnya atau ke daftar model bawaan.

Jika gateway Anda menggunakan nama model yang tidak cocok dengan filter penemuan, gunakan variabel lingkungan yang didokumentasikan dalam [Konfigurasi Model](/id/model-config) untuk menambahkannya secara manual.

## Konfigurasi LiteLLM

<Warning>
  Versi PyPI LiteLLM 1.82.7 dan 1.82.8 dikompromikan dengan malware pencuri kredensial. Jangan instal versi ini. Jika Anda telah menginstalnya:

  * Hapus paket
  * Putar semua kredensial pada sistem yang terpengaruh
  * Ikuti langkah remediasi dalam [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM adalah layanan proxy pihak ketiga. Anthropic tidak mendukung, memelihara, atau mengaudit keamanan atau fungsionalitas LiteLLM. Panduan ini disediakan untuk tujuan informasi dan mungkin menjadi ketinggalan zaman. Gunakan atas kebijakan Anda sendiri.
</Warning>

### Prasyarat

* Claude Code diperbarui ke versi terbaru
* LiteLLM Proxy Server diterapkan dan dapat diakses
* Akses ke model Claude melalui penyedia pilihan Anda

### Pengaturan LiteLLM dasar

**Konfigurasi Claude Code**:

#### Metode autentikasi

##### Kunci API statis

Metode paling sederhana menggunakan kunci API tetap:

```bash theme={null}
# Atur di lingkungan
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Atau di pengaturan Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Nilai ini akan dikirim sebagai header `Authorization`.

##### Kunci API dinamis dengan pembantu

Untuk kunci yang berputar atau autentikasi per pengguna:

1. Buat skrip pembantu kunci API:

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Contoh: Ambil kunci dari vault
vault kv get -field=api_key secret/litellm/claude-code

# Contoh: Hasilkan token JWT
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Konfigurasi pengaturan Claude Code untuk menggunakan pembantu:

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Atur interval penyegaran token:

```bash theme={null}
# Segarkan setiap jam (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Nilai ini akan dikirim sebagai header `Authorization` dan `X-Api-Key`. `apiKeyHelper` memiliki prioritas lebih rendah daripada `ANTHROPIC_AUTH_TOKEN` atau `ANTHROPIC_API_KEY`.

#### Endpoint terpadu (direkomendasikan)

Menggunakan [endpoint format Anthropic](https://docs.litellm.ai/docs/anthropic_unified) LiteLLM:

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Manfaat endpoint terpadu dibandingkan endpoint pass-through:**

* Penyeimbangan beban
* Fallback
* Dukungan konsisten untuk pelacakan biaya dan pelacakan pengguna akhir

#### Endpoint pass-through khusus penyedia (alternatif)

##### Claude API melalui LiteLLM

Menggunakan [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock melalui LiteLLM

Menggunakan [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI melalui LiteLLM

Menggunakan [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

##### Claude Platform on AWS melalui gateway

Arahkan ke gateway yang meneruskan ke endpoint [Claude Platform on AWS](/id/claude-platform-on-aws):

```bash theme={null}
export ANTHROPIC_AWS_BASE_URL=https://litellm-server:4000/anthropic-aws
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
```

Untuk informasi lebih terperinci, lihat [dokumentasi LiteLLM](https://docs.litellm.ai/).

## Sumber daya tambahan

* [Dokumentasi LiteLLM](https://docs.litellm.ai/)
* [Pengaturan Claude Code](/id/settings)
* [Konfigurasi jaringan enterprise](/id/network-config)
* [Ikhtisar integrasi pihak ketiga](/id/third-party-integrations)
