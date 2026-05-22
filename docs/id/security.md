> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Keamanan

> Pelajari tentang perlindungan keamanan Claude Code dan praktik terbaik untuk penggunaan yang aman.

## Bagaimana kami mendekati keamanan

### Fondasi keamanan

Keamanan kode Anda adalah prioritas utama. Claude Code dibangun dengan keamanan sebagai inti, dikembangkan sesuai dengan program keamanan komprehensif Anthropic. Pelajari lebih lanjut dan akses sumber daya (laporan SOC 2 Type 2, sertifikat ISO 27001, dll.) di [Anthropic Trust Center](https://trust.anthropic.com).

### Arsitektur berbasis izin

Claude Code menggunakan izin baca-saja yang ketat secara default. Ketika tindakan tambahan diperlukan (mengedit file, menjalankan tes, mengeksekusi perintah), Claude Code meminta izin eksplisit. Pengguna mengontrol apakah akan menyetujui tindakan sekali atau mengizinkannya secara otomatis.

Kami merancang Claude Code agar transparan dan aman. Misalnya, kami memerlukan persetujuan untuk perintah bash sebelum mengeksekusinya, memberikan Anda kontrol langsung. Pendekatan ini memungkinkan pengguna dan organisasi untuk mengonfigurasi izin secara langsung.

Untuk konfigurasi izin terperinci, lihat [Permissions](/id/permissions).

### Perlindungan bawaan

Untuk mengurangi risiko dalam sistem agentic:

* **Alat bash bersandbox**: [Sandbox](/id/sandboxing) perintah bash dengan isolasi filesystem dan jaringan, mengurangi permintaan izin sambil mempertahankan keamanan. Aktifkan dengan `/sandbox` untuk menentukan batas tempat Claude Code dapat bekerja secara otonom
* **Pembatasan akses tulis**: Claude Code hanya dapat menulis ke folder tempat dimulai dan subfolder-nya—tidak dapat memodifikasi file di direktori induk tanpa izin eksplisit. Meskipun Claude Code dapat membaca file di luar direktori kerja (berguna untuk mengakses perpustakaan sistem dan dependensi), operasi tulis dibatasi ketat pada cakupan proyek, menciptakan batas keamanan yang jelas
* **Mitigasi kelelahan permintaan**: Dukungan untuk allowlisting perintah aman yang sering digunakan per-pengguna, per-codebase, atau per-organisasi
* **Mode Accept Edits**: Persetujuan otomatis untuk edit file dan serangkaian perintah Bash filesystem tetap seperti `mkdir`, `touch`, `rm`, `mv`, `cp`, dan `sed` untuk jalur di direktori kerja. Perintah Bash lainnya dan jalur di luar cakupan masih meminta persetujuan

### Tanggung jawab pengguna

Claude Code hanya memiliki izin yang Anda berikan. Anda bertanggung jawab untuk meninjau kode dan perintah yang diusulkan untuk keamanan sebelum persetujuan.

## Lindungi dari prompt injection

Prompt injection adalah teknik di mana penyerang mencoba mengganti atau memanipulasi instruksi asisten AI dengan menyisipkan teks berbahaya. Claude Code mencakup beberapa perlindungan terhadap serangan ini:

### Perlindungan inti

* **Sistem izin**: Operasi sensitif memerlukan persetujuan eksplisit
* **Analisis yang menyadari konteks**: Mendeteksi instruksi yang berpotensi berbahaya dengan menganalisis permintaan lengkap
* **Sanitasi input**: Mencegah command injection dengan memproses input pengguna
* **Daftar blokir perintah**: Memblokir perintah berisiko yang mengambil konten arbitrer dari web seperti `curl` dan `wget` secara default. Ketika secara eksplisit diizinkan, waspadai [batasan pola izin](/id/permissions#tool-specific-permission-rules)

### Perlindungan privasi

Kami telah menerapkan beberapa perlindungan untuk melindungi data Anda, termasuk:

* Periode retensi terbatas untuk informasi sensitif (lihat [Privacy Center](https://privacy.anthropic.com/en/articles/10023548-how-long-do-you-store-my-data) untuk mempelajari lebih lanjut)
* Akses terbatas ke data sesi pengguna
* Kontrol pengguna atas preferensi pelatihan data. Pengguna konsumen dapat mengubah [pengaturan privasi](https://claude.ai/settings/privacy) mereka kapan saja.

Untuk detail lengkap, silakan tinjau [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) kami (untuk pengguna Team, Enterprise, dan API) atau [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (untuk pengguna Free, Pro, dan Max) dan [Privacy Policy](https://www.anthropic.com/legal/privacy).

### Perlindungan tambahan

* **Persetujuan permintaan jaringan**: Alat yang membuat permintaan jaringan memerlukan persetujuan pengguna secara default
* **Jendela konteks terisolasi**: Web fetch menggunakan jendela konteks terpisah untuk menghindari injeksi prompt yang berpotensi berbahaya
* **Verifikasi kepercayaan**: Jalankan codebase pertama kali dan server MCP baru memerlukan verifikasi kepercayaan
  * Catatan: Verifikasi kepercayaan dinonaktifkan saat menjalankan secara non-interaktif dengan flag `-p`. Pengecualiannya adalah [`--worktree`](/id/worktrees), yang masih memerlukan kepercayaan telah diterima untuk direktori
  * Catatan: Ketika Anda memulai Claude Code langsung di direktori home Anda, penerimaan kepercayaan disimpan untuk sesi saat ini saja dan tidak ditulis ke disk, jadi prompt muncul kembali pada setiap peluncuran. Tidak ada pengaturan untuk mempertahankannya. Mulai Claude Code dari subdirektori proyek sebagai gantinya, di mana penerimaan kepercayaan disimpan per direktori
* **Deteksi command injection**: Perintah bash yang mencurigakan memerlukan persetujuan manual bahkan jika sebelumnya allowlisted
* **Pencocokan fail-closed**: Perintah yang tidak cocok secara default memerlukan persetujuan manual
* **Deskripsi bahasa alami**: Perintah bash kompleks menyertakan penjelasan untuk pemahaman pengguna
* **Penyimpanan kredensial aman**: Kunci API dan token dienkripsi. Lihat [Credential Management](/id/authentication#credential-management)

<Warning>
  **Risiko keamanan Windows WebDAV**: Saat menjalankan Claude Code di Windows, kami merekomendasikan untuk tidak mengaktifkan WebDAV atau mengizinkan Claude Code mengakses path seperti `\\*` yang mungkin berisi subdirektori WebDAV. [WebDAV telah dihentikan oleh Microsoft](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features#:~:text=The%20Webclient%20\(WebDAV\)%20service%20is%20deprecated) karena risiko keamanan. Mengaktifkan WebDAV dapat memungkinkan Claude Code memicu permintaan jaringan ke host jarak jauh, melewati sistem izin.
</Warning>

**Praktik terbaik untuk bekerja dengan konten yang tidak dipercaya**:

1. Tinjau perintah yang disarankan sebelum persetujuan
2. Hindari piping konten yang tidak dipercaya langsung ke Claude
3. Verifikasi perubahan yang diusulkan pada file kritis
4. Gunakan mesin virtual (VM) untuk menjalankan skrip dan membuat panggilan alat, terutama saat berinteraksi dengan layanan web eksternal
5. Laporkan perilaku mencurigakan dengan `/feedback`

<Warning>
  Meskipun perlindungan ini secara signifikan mengurangi risiko, tidak ada sistem yang
  sepenuhnya kebal terhadap semua serangan. Selalu pertahankan praktik keamanan yang baik saat bekerja
  dengan alat AI apa pun.
</Warning>

## Keamanan MCP

Claude Code memungkinkan pengguna untuk mengonfigurasi server Model Context Protocol (MCP). Daftar server MCP yang diizinkan dikonfigurasi dalam kode sumber Anda, sebagai bagian dari pengaturan Claude Code yang diperiksa insinyur ke dalam kontrol sumber.

Kami mendorong untuk menulis server MCP Anda sendiri atau menggunakan server MCP dari penyedia yang Anda percayai. Anda dapat mengonfigurasi izin Claude Code untuk server MCP. Anthropic meninjau konektor terhadap [kriteria pendaftarannya](https://claude.com/docs/connectors/building/review-criteria) sebelum menambahkannya ke [Direktori Anthropic](https://claude.ai/directory), tetapi tidak melakukan audit keamanan atau mengelola server MCP apa pun.

## Keamanan IDE

Lihat [VS Code security and privacy](/id/vs-code#security-and-privacy) untuk informasi lebih lanjut tentang menjalankan Claude Code di IDE.

## Keamanan eksekusi cloud

Saat menggunakan [Claude Code di web](/id/claude-code-on-the-web), kontrol keamanan tambahan tersedia:

* **Mesin virtual terisolasi**: Setiap sesi cloud berjalan di VM yang terisolasi dan dikelola Anthropic
* **Kontrol akses jaringan**: Akses jaringan dibatasi secara default dan dapat dikonfigurasi untuk dinonaktifkan atau hanya mengizinkan domain tertentu
* **Perlindungan kredensial**: Autentikasi ditangani melalui proxy aman yang menggunakan kredensial bersisir di dalam sandbox, yang kemudian diterjemahkan ke token autentikasi GitHub aktual Anda
* **Pembatasan cabang**: Operasi git push dibatasi pada cabang kerja saat ini
* **Pencatatan audit**: Semua operasi di lingkungan cloud dicatat untuk kepatuhan dan tujuan audit
* **Pembersihan otomatis**: Lingkungan cloud secara otomatis dihentikan setelah penyelesaian sesi

Untuk detail lebih lanjut tentang eksekusi cloud, lihat [Claude Code di web](/id/claude-code-on-the-web).

Sesi [Remote Control](/id/remote-control) bekerja berbeda: antarmuka web terhubung ke proses Claude Code yang berjalan di mesin lokal Anda. Semua eksekusi kode dan akses file tetap lokal, dan data yang sama yang mengalir selama sesi Claude Code lokal apa pun berjalan melalui Anthropic API melalui TLS. Tidak ada VM cloud atau sandboxing yang terlibat. Koneksi menggunakan beberapa kredensial berumur pendek dengan cakupan sempit, masing-masing dibatasi untuk tujuan tertentu dan kedaluwarsa secara independen, untuk membatasi radius ledakan dari kredensial tunggal yang dikompromikan.

## Praktik terbaik keamanan

### Bekerja dengan kode sensitif

* Tinjau semua perubahan yang disarankan sebelum persetujuan
* Gunakan pengaturan izin khusus proyek untuk repositori sensitif
* Pertimbangkan menggunakan [dev containers](/id/devcontainer) untuk isolasi tambahan
* Audit secara teratur pengaturan izin Anda dengan `/permissions`

### Keamanan tim

* Gunakan [managed settings](/id/settings#settings-files) untuk menegakkan standar organisasi
* Bagikan konfigurasi izin yang disetujui melalui kontrol versi
* Latih anggota tim tentang praktik terbaik keamanan
* Pantau penggunaan Claude Code melalui [OpenTelemetry metrics](/id/monitoring-usage)
* Audit atau blokir perubahan pengaturan selama sesi dengan [`ConfigChange` hooks](/id/hooks#configchange)

### Melaporkan masalah keamanan

Jika Anda menemukan kerentanan keamanan di Claude Code:

1. Jangan ungkapkan secara publik
2. Laporkan melalui [program HackerOne](https://hackerone.com/4f1f16ba-10d3-4d09-9ecc-c721aad90f24/embedded_submissions/new) kami
3. Sertakan langkah reproduksi terperinci
4. Berikan waktu bagi kami untuk mengatasi masalah sebelum pengungkapan publik

## Sumber daya terkait

* [Sandbox environments](/id/sandbox-environments): bandingkan pendekatan isolasi dan pilih satu untuk model ancaman Anda
* [Sandboxing](/id/sandboxing): isolasi filesystem dan jaringan untuk perintah Bash
* [Permissions](/id/permissions): konfigurasi izin dan kontrol akses
* [Monitoring usage](/id/monitoring-usage): lacak dan audit aktivitas Claude Code
* [Development containers](/id/devcontainer): lingkungan yang aman dan terisolasi
* [Anthropic Trust Center](https://trust.anthropic.com): sertifikasi keamanan dan kepatuhan
