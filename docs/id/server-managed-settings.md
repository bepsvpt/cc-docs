> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi pengaturan yang dikelola server (beta publik)

> Konfigurasi Claude Code secara terpusat untuk organisasi Anda melalui pengaturan yang dikirimkan server, tanpa memerlukan infrastruktur manajemen perangkat.

Pengaturan yang dikelola server memungkinkan administrator untuk mengonfigurasi Claude Code secara terpusat melalui antarmuka berbasis web di Claude.ai. Klien Claude Code secara otomatis menerima pengaturan ini ketika pengguna melakukan autentikasi dengan kredensial organisasi mereka.

Pendekatan ini dirancang untuk organisasi yang tidak memiliki infrastruktur manajemen perangkat, atau perlu mengelola pengaturan untuk pengguna pada perangkat yang tidak dikelola.

<Note>
  Pengaturan yang dikelola server berada dalam beta publik dan tersedia untuk pelanggan [Claude for Teams](https://claude.com/pricing#team-&-enterprise) dan [Claude for Enterprise](https://anthropic.com/contact-sales). Fitur dapat berkembang sebelum ketersediaan umum.
</Note>

## Persyaratan

Untuk menggunakan pengaturan yang dikelola server, Anda memerlukan:

* Paket Claude for Teams atau Claude for Enterprise
* Claude Code versi 2.1.38 atau lebih baru untuk Claude for Teams, atau versi 2.1.30 atau lebih baru untuk Claude for Enterprise
* Akses jaringan ke `api.anthropic.com`

## Pilih antara pengaturan yang dikelola server dan endpoint

Claude Code mendukung dua pendekatan untuk konfigurasi terpusat. Pengaturan yang dikelola server mengirimkan konfigurasi dari server Anthropic. [Pengaturan yang dikelola endpoint](/id/settings#settings-files) digunakan langsung ke perangkat melalui kebijakan OS asli (preferensi terkelola macOS, registri Windows) atau file pengaturan terkelola.

| Pendekatan                                                           | Terbaik untuk                                                          | Model keamanan                                                                                                       |
| :------------------------------------------------------------------- | :--------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Pengaturan yang dikelola server**                                  | Organisasi tanpa MDM, atau pengguna pada perangkat yang tidak dikelola | Pengaturan dikirimkan dari server Anthropic pada waktu autentikasi                                                   |
| **[Pengaturan yang dikelola endpoint](/id/settings#settings-files)** | Organisasi dengan MDM atau manajemen endpoint                          | Pengaturan digunakan ke perangkat melalui profil konfigurasi MDM, kebijakan registri, atau file pengaturan terkelola |

Jika perangkat Anda terdaftar dalam solusi MDM atau manajemen endpoint, pengaturan yang dikelola endpoint memberikan jaminan keamanan yang lebih kuat karena file pengaturan dapat dilindungi dari modifikasi pengguna di tingkat OS.

## Konfigurasi pengaturan yang dikelola server

<Steps>
  <Step title="Buka konsol admin">
    Di [Claude.ai](https://claude.ai), navigasikan ke **Admin Settings > Claude Code > Managed settings**.
  </Step>

  <Step title="Tentukan pengaturan Anda">
    Tambahkan konfigurasi Anda sebagai JSON. Semua [pengaturan yang tersedia di `settings.json`](/id/settings#available-settings) didukung, termasuk [pengaturan yang hanya dikelola](/id/permissions#managed-only-settings) seperti `disableBypassPermissionsMode`.

    Contoh ini memberlakukan daftar penolakan izin dan mencegah pengguna dari melewati izin:

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ]
      },
      "disableBypassPermissionsMode": "disable"
    }
    ```
  </Step>

  <Step title="Simpan dan terapkan">
    Simpan perubahan Anda. Klien Claude Code menerima pengaturan yang diperbarui pada startup berikutnya atau siklus polling per jam.
  </Step>
</Steps>

### Verifikasi pengiriman pengaturan

Untuk mengonfirmasi bahwa pengaturan sedang diterapkan, minta pengguna untuk memulai ulang Claude Code. Jika konfigurasi mencakup pengaturan yang memicu [dialog persetujuan keamanan](#security-approval-dialogs), pengguna melihat prompt yang menjelaskan pengaturan yang dikelola pada startup. Anda juga dapat memverifikasi bahwa aturan izin terkelola aktif dengan meminta pengguna menjalankan `/permissions` untuk melihat aturan izin efektif mereka.

### Kontrol akses

Peran berikut dapat mengelola pengaturan yang dikelola server:

* **Primary Owner**
* **Owner**

Batasi akses ke personel terpercaya, karena perubahan pengaturan berlaku untuk semua pengguna dalam organisasi.

### Batasan saat ini

Pengaturan yang dikelola server memiliki batasan berikut selama periode beta:

* Pengaturan berlaku secara seragam untuk semua pengguna dalam organisasi. Konfigurasi per-grup belum didukung.
* [Konfigurasi server MCP](/id/mcp#managed-mcp-configuration) tidak dapat didistribusikan melalui pengaturan yang dikelola server.

## Pengiriman pengaturan

### Prioritas pengaturan

Pengaturan yang dikelola server dan [pengaturan yang dikelola endpoint](/id/settings#settings-files) keduanya menempati tingkat tertinggi dalam [hierarki pengaturan](/id/settings#settings-precedence) Claude Code. Tidak ada tingkat pengaturan lain yang dapat menimpanya, termasuk argumen baris perintah. Ketika keduanya ada, pengaturan yang dikelola server memiliki prioritas dan pengaturan yang dikelola endpoint tidak digunakan.

### Perilaku pengambilan dan caching

Claude Code mengambil pengaturan dari server Anthropic pada startup dan melakukan polling untuk pembaruan setiap jam selama sesi aktif.

**Peluncuran pertama tanpa pengaturan yang di-cache:**

* Claude Code mengambil pengaturan secara asinkron
* Jika pengambilan gagal, Claude Code melanjutkan tanpa pengaturan terkelola
* Ada jendela singkat sebelum pengaturan dimuat di mana pembatasan belum diterapkan

**Peluncuran berikutnya dengan pengaturan yang di-cache:**

* Pengaturan yang di-cache berlaku segera pada startup
* Claude Code mengambil pengaturan segar di latar belakang
* Pengaturan yang di-cache bertahan melalui kegagalan jaringan

Claude Code menerapkan pembaruan pengaturan secara otomatis tanpa restart, kecuali untuk pengaturan lanjutan seperti konfigurasi OpenTelemetry, yang memerlukan restart penuh agar efektif.

### Dialog persetujuan keamanan

Pengaturan tertentu yang dapat menimbulkan risiko keamanan memerlukan persetujuan pengguna eksplisit sebelum diterapkan:

* **Pengaturan perintah shell**: pengaturan yang menjalankan perintah shell
* **Variabel lingkungan kustom**: variabel yang tidak ada dalam daftar aman yang diketahui
* **Konfigurasi hook**: definisi hook apa pun

Ketika pengaturan ini ada, pengguna melihat dialog keamanan yang menjelaskan apa yang sedang dikonfigurasi. Pengguna harus menyetujui untuk melanjutkan. Jika pengguna menolak pengaturan, Claude Code keluar.

<Note>
  Dalam mode non-interaktif dengan flag `-p`, Claude Code melewati dialog keamanan dan menerapkan pengaturan tanpa persetujuan pengguna.
</Note>

## Ketersediaan platform

Pengaturan yang dikelola server memerlukan koneksi langsung ke `api.anthropic.com` dan tidak tersedia saat menggunakan penyedia model pihak ketiga:

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* Endpoint API kustom melalui `ANTHROPIC_BASE_URL` atau [gateway LLM](/id/llm-gateway)

## Audit logging

Acara log audit untuk perubahan pengaturan tersedia melalui API kepatuhan atau ekspor log audit. Hubungi tim akun Anthropic Anda untuk akses.

Acara audit mencakup jenis tindakan yang dilakukan, akun dan perangkat yang melakukan tindakan, dan referensi ke nilai sebelumnya dan baru.

## Pertimbangan keamanan

Pengaturan yang dikelola server menyediakan penegakan kebijakan terpusat, tetapi mereka beroperasi sebagai kontrol sisi klien. Pada perangkat yang tidak dikelola, pengguna dengan akses admin atau sudo dapat memodifikasi biner Claude Code, sistem file, atau konfigurasi jaringan.

| Skenario                                                      | Perilaku                                                                                                                                     |
| :------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| Pengguna mengedit file pengaturan yang di-cache               | File yang dirusak berlaku pada startup, tetapi pengaturan yang benar dipulihkan pada pengambilan server berikutnya                           |
| Pengguna menghapus file pengaturan yang di-cache              | Perilaku peluncuran pertama terjadi: pengaturan mengambil secara asinkron dengan jendela unenforced singkat                                  |
| API tidak tersedia                                            | Pengaturan yang di-cache berlaku jika tersedia, jika tidak pengaturan terkelola tidak diterapkan sampai pengambilan yang berhasil berikutnya |
| Pengguna melakukan autentikasi dengan organisasi yang berbeda | Pengaturan tidak dikirimkan untuk akun di luar organisasi yang dikelola                                                                      |
| Pengguna menetapkan `ANTHROPIC_BASE_URL` non-default          | Pengaturan yang dikelola server dilewati saat menggunakan penyedia API pihak ketiga                                                          |

Untuk mendeteksi perubahan konfigurasi runtime, gunakan [hook `ConfigChange`](/id/hooks#configchange) untuk mencatat modifikasi atau memblokir perubahan yang tidak sah sebelum diterapkan.

Untuk jaminan penegakan yang lebih kuat, gunakan [pengaturan yang dikelola endpoint](/id/settings#settings-files) pada perangkat yang terdaftar dalam solusi MDM.

## Lihat juga

Halaman terkait untuk mengelola konfigurasi Claude Code:

* [Settings](/id/settings): referensi konfigurasi lengkap termasuk semua pengaturan yang tersedia
* [Pengaturan yang dikelola endpoint](/id/settings#settings-files): pengaturan terkelola yang digunakan ke perangkat oleh IT
* [Authentication](/id/authentication): atur akses pengguna ke Claude Code
* [Security](/id/security): perlindungan keamanan dan praktik terbaik
