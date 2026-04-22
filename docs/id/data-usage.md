> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Penggunaan data

> Pelajari kebijakan penggunaan data Anthropic untuk Claude

## Kebijakan data

### Kebijakan pelatihan data

**Pengguna konsumen (paket Free, Pro, dan Max)**:
Kami memberi Anda pilihan untuk mengizinkan data Anda digunakan untuk meningkatkan model Claude di masa depan. Kami akan melatih model baru menggunakan data dari akun Free, Pro, dan Max ketika pengaturan ini aktif (termasuk ketika Anda menggunakan Claude Code dari akun-akun ini).

**Pengguna komersial**: (paket Team dan Enterprise, API, platform pihak ketiga, dan Claude Gov) mempertahankan kebijakan yang ada: Anthropic tidak melatih model generatif menggunakan kode atau prompt yang dikirim ke Claude Code berdasarkan syarat komersial, kecuali pelanggan telah memilih untuk memberikan data mereka kepada kami untuk peningkatan model (misalnya, [Program Mitra Pengembang](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)).

### Program Mitra Pengembang

Jika Anda secara eksplisit memilih untuk memberikan materi kepada kami untuk dilatih, seperti melalui [Program Mitra Pengembang](https://support.claude.com/en/articles/11174108-about-the-development-partner-program), kami dapat menggunakan materi tersebut untuk melatih model kami. Admin organisasi dapat secara tegas memilih untuk bergabung dengan Program Mitra Pengembang untuk organisasi mereka. Perhatikan bahwa program ini hanya tersedia untuk API pihak pertama Anthropic, dan bukan untuk pengguna Bedrock atau Vertex.

### Umpan balik menggunakan perintah `/feedback`

Jika Anda memilih untuk mengirimkan umpan balik kepada kami tentang Claude Code menggunakan perintah `/feedback`, kami dapat menggunakan umpan balik Anda untuk meningkatkan produk dan layanan kami. Transkrip yang dibagikan melalui `/feedback` disimpan selama 5 tahun.

### Survei kualitas sesi

Ketika Anda melihat prompt "Bagaimana Claude melakukan ini di sesi ini?" di Claude Code, merespons survei ini (termasuk memilih "Abaikan"), hanya peringkat numerik Anda (1, 2, 3, atau abaikan) yang dicatat. Kami tidak mengumpulkan atau menyimpan transkrip percakapan, input, output, atau data sesi lainnya sebagai bagian dari survei ini. Tidak seperti umpan balik jempol ke atas/ke bawah atau laporan `/feedback`, survei kualitas sesi ini adalah metrik kepuasan produk sederhana. Respons Anda terhadap survei ini tidak mempengaruhi preferensi pelatihan data Anda dan tidak dapat digunakan untuk melatih model AI kami.

Untuk menonaktifkan survei ini, atur `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. Survei juga dinonaktifkan ketika `DISABLE_TELEMETRY` atau `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` diatur. Untuk mengontrol frekuensi alih-alih menonaktifkan, atur [`feedbackSurveyRate`](/id/settings#available-settings) dalam file pengaturan Anda ke probabilitas antara `0` dan `1`.

### Retensi data

Anthropic menyimpan data Claude Code berdasarkan jenis akun dan preferensi Anda.

**Pengguna konsumen (paket Free, Pro, dan Max)**:

* Pengguna yang mengizinkan penggunaan data untuk peningkatan model: periode retensi 5 tahun untuk mendukung pengembangan model dan peningkatan keamanan
* Pengguna yang tidak mengizinkan penggunaan data untuk peningkatan model: periode retensi 30 hari
* Pengaturan privasi dapat diubah kapan saja di [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Pengguna komersial (Team, Enterprise, dan API)**:

* Standar: periode retensi 30 hari
* [Retensi data nol](/id/zero-data-retention): tersedia untuk Claude Code di Claude untuk Enterprise. ZDR diaktifkan berdasarkan per-organisasi; setiap organisasi baru harus memiliki ZDR diaktifkan secara terpisah oleh tim akun Anda
* Penyimpanan lokal: klien Claude Code menyimpan transkrip sesi secara lokal dalam plaintext di bawah `~/.claude/projects/` selama 30 hari secara default untuk memungkinkan pemulihan sesi. Sesuaikan periode dengan `cleanupPeriodDays`. Lihat [data aplikasi](/id/claude-directory#application-data) untuk apa yang disimpan dan cara menghapusnya.

Anda dapat menghapus sesi Claude Code individual di web kapan saja. Menghapus sesi secara permanen menghapus data peristiwa sesi. Untuk instruksi tentang cara menghapus sesi, lihat [Menghapus sesi](/id/claude-code-on-the-web#delete-sessions).

Pelajari lebih lanjut tentang praktik retensi data di [Pusat Privasi](https://privacy.anthropic.com/) kami.

Untuk detail lengkap, silakan tinjau [Syarat Layanan Komersial](https://www.anthropic.com/legal/commercial-terms) kami (untuk pengguna Team, Enterprise, dan API) atau [Syarat Konsumen](https://www.anthropic.com/legal/consumer-terms) (untuk pengguna Free, Pro, dan Max) dan [Kebijakan Privasi](https://www.anthropic.com/legal/privacy).

## Akses data

Untuk semua pengguna pihak pertama, Anda dapat mempelajari lebih lanjut tentang data apa yang dicatat untuk [Claude Code lokal](#local-claude-code-data-flow-and-dependencies) dan [Claude Code cloud](#cloud-execution-data-flow-and-dependencies). Sesi [Remote Control](/id/remote-control) mengikuti alur data lokal karena semua eksekusi terjadi di mesin Anda. Perhatikan untuk Claude Code jarak jauh, Claude mengakses repositori tempat Anda memulai sesi Claude Code Anda. Claude tidak mengakses repositori yang telah Anda hubungkan tetapi belum memulai sesi di dalamnya.

## Claude Code Lokal: Alur data dan dependensi

Diagram di bawah menunjukkan bagaimana Claude Code terhubung ke layanan eksternal selama instalasi dan operasi normal. Garis solid menunjukkan koneksi yang diperlukan, sementara garis putus-putus mewakili alur data opsional atau yang dimulai pengguna.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/claude-code-data-flow.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=b3f71c69d743bff63343207dfb7ad6ce" alt="Diagram menunjukkan koneksi eksternal Claude Code: install/update terhubung ke NPM, dan permintaan pengguna terhubung ke layanan Anthropic termasuk auth Console, public-api, dan secara opsional Statsig, Sentry, dan pelaporan bug" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code diinstal dari [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code berjalan secara lokal. Untuk berinteraksi dengan LLM, Claude Code mengirimkan data melalui jaringan. Data ini mencakup semua prompt pengguna dan output model. Data dienkripsi dalam transit melalui TLS dan tidak dienkripsi saat istirahat. Claude Code kompatibel dengan sebagian besar VPN dan proxy LLM populer.

Claude Code dibangun di atas API Anthropic. Untuk detail mengenai kontrol keamanan API kami, termasuk prosedur logging API kami, silakan lihat artefak kepatuhan yang ditawarkan di [Pusat Kepercayaan Anthropic](https://trust.anthropic.com).

### Eksekusi cloud: Alur data dan dependensi

Saat menggunakan [Claude Code di web](/id/claude-code-on-the-web), sesi berjalan di mesin virtual yang dikelola Anthropic alih-alih secara lokal. Di lingkungan cloud:

* **Penyimpanan kode dan data:** Repositori Anda diklon ke VM terisolasi. Kode dan data sesi tunduk pada kebijakan retensi dan penggunaan untuk jenis akun Anda (lihat bagian Retensi data di atas)
* **Kredensial:** Autentikasi GitHub ditangani melalui proxy aman; kredensial GitHub Anda tidak pernah memasuki sandbox
* **Lalu lintas jaringan:** Semua lalu lintas keluar melewati proxy keamanan untuk logging audit dan pencegahan penyalahgunaan
* **Data sesi:** Prompt, perubahan kode, dan output mengikuti kebijakan data yang sama dengan penggunaan Claude Code lokal

Untuk detail keamanan tentang eksekusi cloud, lihat [Keamanan](/id/security#cloud-execution-security).

## Layanan telemetri

Claude Code terhubung dari mesin pengguna ke layanan Statsig untuk mencatat metrik operasional seperti latensi, keandalan, dan pola penggunaan. Logging ini tidak mencakup kode atau jalur file apa pun. Data dienkripsi dalam transit menggunakan TLS dan saat istirahat menggunakan enkripsi AES 256-bit. Baca lebih lanjut di [dokumentasi keamanan Statsig](https://www.statsig.com/trust/security). Untuk menolak telemetri Statsig, atur variabel lingkungan `DISABLE_TELEMETRY`.

Claude Code terhubung dari mesin pengguna ke Sentry untuk logging kesalahan operasional. Data dienkripsi dalam transit menggunakan TLS dan saat istirahat menggunakan enkripsi AES 256-bit. Baca lebih lanjut di [dokumentasi keamanan Sentry](https://sentry.io/security/). Untuk menolak logging kesalahan, atur variabel lingkungan `DISABLE_ERROR_REPORTING`.

Ketika pengguna menjalankan perintah `/feedback`, salinan riwayat percakapan lengkap mereka termasuk kode dikirim ke Anthropic. Data dienkripsi dalam transit dan saat istirahat. Secara opsional, masalah Github dibuat di repositori publik kami. Untuk menolak, atur variabel lingkungan `DISABLE_FEEDBACK_COMMAND` ke `1`.

## Perilaku default menurut penyedia API

Secara default, pelaporan kesalahan, telemetri, dan pelaporan bug dinonaktifkan saat menggunakan Bedrock, Vertex, atau Foundry. Survei kualitas sesi dan pemeriksaan keamanan domain WebFetch adalah pengecualian dan berjalan terlepas dari penyedia. Anda dapat menolak semua lalu lintas non-esensial, termasuk survei, sekaligus dengan mengatur `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Variabel ini tidak mempengaruhi pemeriksaan WebFetch, yang memiliki opt-out tersendiri. Berikut adalah perilaku default lengkapnya:

| Layanan                                  | Claude API                                                                                         | Vertex API                                                                                         | Bedrock API                                                                                        | Foundry API                                                                                        |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Statsig (Metrik)**                     | Default aktif.<br />`DISABLE_TELEMETRY=1` untuk menonaktifkan.                                     | Default nonaktif.<br />`CLAUDE_CODE_USE_VERTEX` harus 1.                                           | Default nonaktif.<br />`CLAUDE_CODE_USE_BEDROCK` harus 1.                                          | Default nonaktif.<br />`CLAUDE_CODE_USE_FOUNDRY` harus 1.                                          |
| **Sentry (Kesalahan)**                   | Default aktif.<br />`DISABLE_ERROR_REPORTING=1` untuk menonaktifkan.                               | Default nonaktif.<br />`CLAUDE_CODE_USE_VERTEX` harus 1.                                           | Default nonaktif.<br />`CLAUDE_CODE_USE_BEDROCK` harus 1.                                          | Default nonaktif.<br />`CLAUDE_CODE_USE_FOUNDRY` harus 1.                                          |
| **Claude API (laporan `/feedback`)**     | Default aktif.<br />`DISABLE_FEEDBACK_COMMAND=1` untuk menonaktifkan.                              | Default nonaktif.<br />`CLAUDE_CODE_USE_VERTEX` harus 1.                                           | Default nonaktif.<br />`CLAUDE_CODE_USE_BEDROCK` harus 1.                                          | Default nonaktif.<br />`CLAUDE_CODE_USE_FOUNDRY` harus 1.                                          |
| **Survei kualitas sesi**                 | Default aktif.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` untuk menonaktifkan.                   | Default aktif.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` untuk menonaktifkan.                   | Default aktif.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` untuk menonaktifkan.                   | Default aktif.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` untuk menonaktifkan.                   |
| **Pemeriksaan keamanan domain WebFetch** | Default aktif.<br />`skipWebFetchPreflight: true` di [settings](/id/settings) untuk menonaktifkan. | Default aktif.<br />`skipWebFetchPreflight: true` di [settings](/id/settings) untuk menonaktifkan. | Default aktif.<br />`skipWebFetchPreflight: true` di [settings](/id/settings) untuk menonaktifkan. | Default aktif.<br />`skipWebFetchPreflight: true` di [settings](/id/settings) untuk menonaktifkan. |

Semua variabel lingkungan dapat diperiksa ke dalam `settings.json` (lihat [referensi settings](/id/settings)).

### Pemeriksaan keamanan domain WebFetch

Sebelum mengambil URL, alat WebFetch mengirimkan nama host yang diminta ke `api.anthropic.com` untuk memeriksanya terhadap daftar blocklist keamanan yang dikelola oleh Anthropic. Hanya nama host yang dikirim, bukan URL lengkap, jalur, atau konten halaman. Hasil disimpan dalam cache per nama host selama lima menit.

Pemeriksaan ini berjalan terlepas dari penyedia model mana yang Anda gunakan dan tidak dipengaruhi oleh `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Jika jaringan Anda memblokir `api.anthropic.com`, permintaan WebFetch gagal sampai Anda memungkinkan daftar domain atau mengatur `skipWebFetchPreflight: true` di [settings](/id/settings). Menonaktifkan pemeriksaan berarti WebFetch mencoba mengambil URL apa pun tanpa berkonsultasi dengan daftar blocklist, jadi gabungkan dengan [aturan izin `WebFetch`](/id/permissions#webfetch) jika Anda perlu membatasi domain mana yang dapat diakses Claude.
