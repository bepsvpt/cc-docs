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

# Claude Code di Microsoft Foundry

> Pelajari tentang mengonfigurasi Claude Code melalui Microsoft Foundry, termasuk setup, konfigurasi, dan pemecahan masalah.

## Prasyarat

Sebelum mengonfigurasi Claude Code dengan Microsoft Foundry, pastikan Anda memiliki:

* Langganan Azure dengan akses ke Microsoft Foundry
* Izin RBAC untuk membuat sumber daya dan deployment Microsoft Foundry
* Azure CLI diinstal dan dikonfigurasi (opsional - hanya diperlukan jika Anda tidak memiliki mekanisme lain untuk mendapatkan kredensial)

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

```bash  theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Opsi B: Autentikasi Microsoft Entra ID**

Ketika `ANTHROPIC_FOUNDRY_API_KEY` tidak diatur, Claude Code secara otomatis menggunakan Azure SDK [rantai kredensial default](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
Ini mendukung berbagai metode untuk mengautentikasi beban kerja lokal dan jarak jauh.

Di lingkungan lokal, Anda biasanya dapat menggunakan Azure CLI:

```bash  theme={null}
az login
```

<Note>
  Saat menggunakan Microsoft Foundry, perintah `/login` dan `/logout` dinonaktifkan karena autentikasi ditangani melalui kredensial Azure.
</Note>

### 3. Konfigurasi Claude Code

Atur variabel lingkungan berikut untuk mengaktifkan Microsoft Foundry. Perhatikan bahwa nama deployment Anda diatur sebagai pengenal model di Claude Code (mungkin opsional jika menggunakan nama deployment yang disarankan).

```bash  theme={null}
# Aktifkan integrasi Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nama sumber daya Azure (ganti {resource} dengan nama sumber daya Anda)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Atau berikan URL dasar lengkap:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# Atur model ke nama deployment sumber daya Anda
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'
```

Untuk detail lebih lanjut tentang opsi konfigurasi model, lihat [Konfigurasi model](/id/model-config).

## Konfigurasi Azure RBAC

Peran default `Azure AI User` dan `Cognitive Services User` mencakup semua izin yang diperlukan untuk memanggil model Claude.

Untuk izin yang lebih ketat, buat peran khusus dengan yang berikut:

```json  theme={null}
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
