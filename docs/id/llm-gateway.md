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

## Konfigurasi

### Pemilihan model

Secara default, Claude Code akan menggunakan nama model standar untuk format API yang dipilih.

Jika Anda telah mengonfigurasi nama model khusus di gateway Anda, gunakan variabel lingkungan yang didokumentasikan dalam [Konfigurasi Model](/id/model-config) untuk mencocokkan nama khusus Anda.

## Konfigurasi LiteLLM

<Note>
  LiteLLM adalah layanan proxy pihak ketiga. Anthropic tidak mendukung, memelihara, atau mengaudit keamanan atau fungsionalitas LiteLLM. Panduan ini disediakan untuk tujuan informasi dan mungkin menjadi ketinggalan zaman. Gunakan atas kebijakan Anda sendiri.
</Note>

### Prasyarat

* Claude Code diperbarui ke versi terbaru
* LiteLLM Proxy Server diterapkan dan dapat diakses
* Akses ke model Claude melalui penyedia pilihan Anda

### Pengaturan LiteLLM dasar

**Konfigurasi Claude Code**:

#### Metode autentikasi

##### Kunci API statis

Metode paling sederhana menggunakan kunci API tetap:

```bash  theme={null}
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

```bash  theme={null}
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

```json  theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Atur interval penyegaran token:

```bash  theme={null}
# Segarkan setiap jam (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Nilai ini akan dikirim sebagai header `Authorization` dan `X-Api-Key`. `apiKeyHelper` memiliki prioritas lebih rendah daripada `ANTHROPIC_AUTH_TOKEN` atau `ANTHROPIC_API_KEY`.

#### Endpoint terpadu (direkomendasikan)

Menggunakan [endpoint format Anthropic](https://docs.litellm.ai/docs/anthropic_unified) LiteLLM:

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Manfaat endpoint terpadu dibandingkan endpoint pass-through:**

* Penyeimbangan beban
* Fallback
* Dukungan konsisten untuk pelacakan biaya dan pelacakan pengguna akhir

#### Endpoint pass-through khusus penyedia (alternatif)

##### Claude API melalui LiteLLM

Menggunakan [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock melalui LiteLLM

Menggunakan [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash  theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI melalui LiteLLM

Menggunakan [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash  theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Untuk informasi lebih terperinci, lihat [dokumentasi LiteLLM](https://docs.litellm.ai/).

## Sumber daya tambahan

* [Dokumentasi LiteLLM](https://docs.litellm.ai/)
* [Pengaturan Claude Code](/id/settings)
* [Konfigurasi jaringan enterprise](/id/network-config)
* [Ikhtisar integrasi pihak ketiga](/id/third-party-integrations)
