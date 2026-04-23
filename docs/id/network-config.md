> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi jaringan enterprise

> Konfigurasikan Claude Code untuk lingkungan enterprise dengan server proxy, Certificate Authorities (CA) kustom, dan autentikasi mutual Transport Layer Security (mTLS).

Claude Code mendukung berbagai konfigurasi jaringan dan keamanan enterprise melalui variabel lingkungan. Ini termasuk merutekan lalu lintas melalui server proxy perusahaan, mempercayai Certificate Authorities (CA) kustom, dan mengautentikasi dengan sertifikat mutual Transport Layer Security (mTLS) untuk keamanan yang ditingkatkan.

<Note>
  Semua variabel lingkungan yang ditampilkan di halaman ini juga dapat dikonfigurasi di [`settings.json`](/id/settings).
</Note>

## Konfigurasi proxy

### Variabel lingkungan

Claude Code menghormati variabel lingkungan proxy standar:

```bash theme={null}
# HTTPS proxy (direkomendasikan)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (jika HTTPS tidak tersedia)
export HTTP_PROXY=http://proxy.example.com:8080

# Lewati proxy untuk permintaan tertentu - format terpisah spasi
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Lewati proxy untuk permintaan tertentu - format terpisah koma
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Lewati proxy untuk semua permintaan
export NO_PROXY="*"
```

<Note>
  Claude Code tidak mendukung proxy SOCKS.
</Note>

### Autentikasi dasar

Jika proxy Anda memerlukan autentikasi dasar, sertakan kredensial dalam URL proxy:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Hindari hardcoding kata sandi dalam skrip. Gunakan variabel lingkungan atau penyimpanan kredensial aman sebagai gantinya.
</Warning>

<Tip>
  Untuk proxy yang memerlukan autentikasi lanjutan (NTLM, Kerberos, dll.), pertimbangkan menggunakan layanan LLM Gateway yang mendukung metode autentikasi Anda.
</Tip>

## Penyimpanan sertifikat CA

Secara default, Claude Code mempercayai baik sertifikat CA Mozilla yang disertakan maupun penyimpanan sertifikat sistem operasi Anda. Proxy inspeksi TLS enterprise seperti CrowdStrike Falcon dan Zscaler bekerja tanpa konfigurasi tambahan ketika sertifikat akar mereka diinstal di penyimpanan kepercayaan OS.

<Note>
  Integrasi penyimpanan CA sistem memerlukan distribusi biner Claude Code asli. Saat berjalan di runtime Node.js, penyimpanan CA sistem tidak digabungkan secara otomatis. Dalam hal itu, atur `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` untuk mempercayai CA akar enterprise.
</Note>

`CLAUDE_CODE_CERT_STORE` menerima daftar sumber yang dipisahkan koma. Nilai yang dikenali adalah `bundled` untuk set CA Mozilla yang dikirimkan dengan Claude Code dan `system` untuk penyimpanan kepercayaan sistem operasi. Default adalah `bundled,system`.

Untuk mempercayai hanya set CA Mozilla yang disertakan:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

Untuk mempercayai hanya penyimpanan sertifikat OS:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` tidak memiliki kunci skema `settings.json` khusus. Aturnya melalui blok `env` di `~/.claude/settings.json` atau langsung di lingkungan proses.
</Note>

## Sertifikat CA kustom

Jika lingkungan enterprise Anda menggunakan CA kustom, konfigurasikan Claude Code untuk mempercayainya secara langsung:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autentikasi mTLS

Untuk lingkungan enterprise yang memerlukan autentikasi sertifikat klien:

```bash theme={null}
# Sertifikat klien untuk autentikasi
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Kunci pribadi klien
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Opsional: Frasa sandi untuk kunci pribadi terenkripsi
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Persyaratan akses jaringan

Claude Code memerlukan akses ke URL berikut. Izinkan URL ini dalam konfigurasi proxy dan aturan firewall Anda, terutama di lingkungan jaringan terkontainer atau terbatas.

| URL                            | Diperlukan untuk                                                                                   |
| ------------------------------ | -------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`            | Permintaan Claude API                                                                              |
| `claude.ai`                    | Autentikasi akun claude.ai                                                                         |
| `platform.claude.com`          | Autentikasi akun Anthropic Console                                                                 |
| `downloads.claude.ai`          | Unduhan plugin yang dapat dieksekusi; penginstal asli dan pembaruan otomatis asli                  |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}Penginstal asli dan pembaruan otomatis asli pada versi sebelum 2.1.116 |
| `bridge.claudeusercontent.com` | Jembatan WebSocket ekstensi [Claude di Chrome](/id/chrome)                                         |

Jika Anda menginstal Claude Code melalui npm atau mengelola distribusi biner Anda sendiri, pengguna akhir mungkin tidak memerlukan akses ke `downloads.claude.ai` atau `storage.googleapis.com`.

Saat menggunakan [Amazon Bedrock](/id/amazon-bedrock), [Google Vertex AI](/id/google-vertex-ai), atau [Microsoft Foundry](/id/microsoft-foundry), lalu lintas model dan autentikasi menuju penyedia Anda alih-alih `api.anthropic.com`, `claude.ai`, atau `platform.claude.com`. Alat WebFetch masih memanggil `api.anthropic.com` untuk [pemeriksaan keamanan domainnya](/id/data-usage#webfetch-domain-safety-check) kecuali Anda menetapkan `skipWebFetchPreflight: true` di [pengaturan](/id/settings).

[Claude Code di web](/id/claude-code-on-the-web) dan [Code Review](/id/code-review) terhubung ke repositori Anda dari infrastruktur yang dikelola Anthropic. Jika organisasi GitHub Enterprise Cloud Anda membatasi akses berdasarkan alamat IP, aktifkan [pewarisan daftar izin IP untuk GitHub Apps yang diinstal](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). Claude GitHub App mendaftarkan rentang IP-nya, jadi mengaktifkan pengaturan ini memungkinkan akses tanpa konfigurasi manual. Untuk [menambahkan rentang ke daftar izin Anda secara manual](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) sebagai gantinya, atau untuk mengonfigurasi firewall lainnya, lihat [Alamat IP API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Untuk instans [GitHub Enterprise Server](/id/github-enterprise-server) yang dihosting sendiri di belakang firewall, izinkan daftar [Alamat IP API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) yang sama sehingga infrastruktur Anthropic dapat menjangkau host GHES Anda untuk mengkloning repositori dan memposting komentar tinjauan.

## Sumber daya tambahan

* [Pengaturan Claude Code](/id/settings)
* [Referensi variabel lingkungan](/id/env-vars)
* [Panduan pemecahan masalah](/id/troubleshooting)
