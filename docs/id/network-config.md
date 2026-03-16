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

```bash  theme={null}
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

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Hindari hardcoding kata sandi dalam skrip. Gunakan variabel lingkungan atau penyimpanan kredensial aman sebagai gantinya.
</Warning>

<Tip>
  Untuk proxy yang memerlukan autentikasi lanjutan (NTLM, Kerberos, dll.), pertimbangkan menggunakan layanan LLM Gateway yang mendukung metode autentikasi Anda.
</Tip>

## Sertifikat CA kustom

Jika lingkungan enterprise Anda menggunakan CA kustom untuk koneksi HTTPS (baik melalui proxy atau akses API langsung), konfigurasikan Claude Code untuk mempercayainya:

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autentikasi mTLS

Untuk lingkungan enterprise yang memerlukan autentikasi sertifikat klien:

```bash  theme={null}
# Sertifikat klien untuk autentikasi
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Kunci pribadi klien
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Opsional: Frasa sandi untuk kunci pribadi terenkripsi
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Persyaratan akses jaringan

Claude Code memerlukan akses ke URL berikut:

* `api.anthropic.com`: Titik akhir Claude API
* `claude.ai`: autentikasi untuk akun claude.ai
* `platform.claude.com`: autentikasi untuk akun Anthropic Console

Pastikan URL ini diizinkan dalam konfigurasi proxy dan aturan firewall Anda. Ini sangat penting ketika menggunakan Claude Code di lingkungan jaringan terkontainer atau terbatas.

## Sumber daya tambahan

* [Pengaturan Claude Code](/id/settings)
* [Referensi variabel lingkungan](/id/settings#environment-variables)
* [Panduan pemecahan masalah](/id/troubleshooting)
