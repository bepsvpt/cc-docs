> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Lanjutkan sesi lokal dari perangkat apa pun dengan Remote Control

> Lanjutkan sesi Claude Code lokal dari ponsel, tablet, atau browser apa pun menggunakan Remote Control. Bekerja dengan claude.ai/code dan aplikasi Claude mobile.

<Note>
  Remote Control tersedia di semua paket. Admin Tim dan Enterprise harus terlebih dahulu mengaktifkan Claude Code di [pengaturan admin](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control menghubungkan [claude.ai/code](https://claude.ai/code) atau aplikasi Claude untuk [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) dan [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) ke sesi Claude Code yang berjalan di mesin Anda. Mulai tugas di meja Anda, kemudian lanjutkan dari ponsel Anda di sofa atau browser di komputer lain.

Ketika Anda memulai sesi Remote Control di mesin Anda, Claude terus berjalan secara lokal sepanjang waktu, jadi tidak ada yang pindah ke cloud. Dengan Remote Control Anda dapat:

* **Gunakan lingkungan lokal penuh Anda dari jarak jauh**: sistem file, [MCP servers](/id/mcp), alat, dan konfigurasi proyek Anda tetap tersedia
* **Bekerja dari kedua permukaan sekaligus**: percakapan tetap tersinkronisasi di semua perangkat yang terhubung, sehingga Anda dapat mengirim pesan dari terminal, browser, dan ponsel Anda secara bergantian
* **Bertahan dari gangguan**: jika laptop Anda tidur atau jaringan Anda terputus, sesi akan terhubung kembali secara otomatis ketika mesin Anda kembali online

Tidak seperti [Claude Code di web](/id/claude-code-on-the-web), yang berjalan di infrastruktur cloud, sesi Remote Control berjalan langsung di mesin Anda dan berinteraksi dengan sistem file lokal Anda. Antarmuka web dan mobile hanyalah jendela ke sesi lokal tersebut.

<Note>
  Remote Control memerlukan Claude Code v2.1.51 atau lebih baru. Periksa versi Anda dengan `claude --version`.
</Note>

Halaman ini mencakup pengaturan, cara memulai dan terhubung ke sesi, dan bagaimana Remote Control dibandingkan dengan Claude Code di web.

## Persyaratan

Sebelum menggunakan Remote Control, konfirmasi bahwa lingkungan Anda memenuhi kondisi berikut:

* **Langganan**: tersedia di paket Pro, Max, Tim, dan Enterprise. Admin Tim dan Enterprise harus terlebih dahulu mengaktifkan Claude Code di [pengaturan admin](https://claude.ai/admin-settings/claude-code). Kunci API tidak didukung.
* **Autentikasi**: jalankan `claude` dan gunakan `/login` untuk masuk melalui claude.ai jika Anda belum melakukannya.
* **Kepercayaan ruang kerja**: jalankan `claude` di direktori proyek Anda setidaknya sekali untuk menerima dialog kepercayaan ruang kerja.

## Mulai sesi Remote Control

Anda dapat memulai sesi baru langsung di Remote Control, atau menghubungkan sesi yang sudah berjalan.

<Tabs>
  <Tab title="Sesi baru">
    Navigasikan ke direktori proyek Anda dan jalankan:

    ```bash  theme={null}
    claude remote-control
    ```

    Proses tetap berjalan di terminal Anda, menunggu koneksi jarak jauh. Ini menampilkan URL sesi yang dapat Anda gunakan untuk [terhubung dari perangkat lain](#connect-from-another-device), dan Anda dapat menekan spacebar untuk menampilkan kode QR untuk akses cepat dari ponsel Anda. Saat sesi jarak jauh aktif, terminal menampilkan status koneksi dan aktivitas alat.

    Perintah ini mendukung flag berikut:

    * **`--name "My Project"`**: atur judul sesi khusus yang terlihat dalam daftar sesi di claude.ai/code. Anda juga dapat meneruskan nama sebagai argumen posisional: `claude remote-control "My Project"`
    * **`--verbose`**: tampilkan log koneksi dan sesi terperinci
    * **`--sandbox`** / **`--no-sandbox`**: aktifkan atau nonaktifkan [sandboxing](/id/sandboxing) untuk isolasi sistem file dan jaringan selama sesi. Sandboxing dimatikan secara default.
  </Tab>

  <Tab title="Dari sesi yang ada">
    Jika Anda sudah dalam sesi Claude Code dan ingin melanjutkannya dari jarak jauh, gunakan perintah `/remote-control` (atau `/rc`):

    ```text  theme={null}
    /remote-control
    ```

    Teruskan nama sebagai argumen untuk menetapkan judul sesi khusus:

    ```text  theme={null}
    /remote-control My Project
    ```

    Ini memulai sesi Remote Control yang membawa riwayat percakapan Anda saat ini dan menampilkan URL sesi dan kode QR yang dapat Anda gunakan untuk [terhubung dari perangkat lain](#connect-from-another-device). Flag `--verbose`, `--sandbox`, dan `--no-sandbox` tidak tersedia dengan perintah ini.
  </Tab>
</Tabs>

### Terhubung dari perangkat lain

Setelah sesi Remote Control aktif, Anda memiliki beberapa cara untuk terhubung dari perangkat lain:

* **Buka URL sesi** di browser apa pun untuk langsung ke sesi di [claude.ai/code](https://claude.ai/code). Baik `claude remote-control` maupun `/remote-control` menampilkan URL ini di terminal.
* **Pindai kode QR** yang ditampilkan di samping URL sesi untuk membukanya langsung di aplikasi Claude. Dengan `claude remote-control`, tekan spacebar untuk mengalihkan tampilan kode QR.
* **Buka [claude.ai/code](https://claude.ai/code) atau aplikasi Claude** dan temukan sesi berdasarkan nama dalam daftar sesi. Sesi Remote Control menampilkan ikon komputer dengan titik status hijau saat online.

Sesi jarak jauh mengambil namanya dari argumen `--name` (atau nama yang diteruskan ke `/remote-control`), pesan terakhir Anda, nilai `/rename` Anda, atau "Remote Control session" jika tidak ada riwayat percakapan. Jika lingkungan sudah memiliki sesi aktif, Anda akan ditanya apakah akan melanjutkannya atau memulai yang baru.

Jika Anda belum memiliki aplikasi Claude, gunakan perintah `/mobile` di dalam Claude Code untuk menampilkan kode QR unduhan untuk [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) atau [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Aktifkan Remote Control untuk semua sesi

Secara default, Remote Control hanya diaktifkan ketika Anda secara eksplisit menjalankan `claude remote-control` atau `/remote-control`. Untuk mengaktifkannya secara otomatis untuk setiap sesi, jalankan `/config` di dalam Claude Code dan atur **Enable Remote Control for all sessions** ke `true`. Atur kembali ke `false` untuk menonaktifkan.

Setiap instans Claude Code mendukung satu sesi jarak jauh pada satu waktu. Jika Anda menjalankan beberapa instans, masing-masing mendapatkan lingkungan dan sesinya sendiri.

## Koneksi dan keamanan

Sesi Claude Code lokal Anda hanya membuat permintaan HTTPS keluar dan tidak pernah membuka port masuk di mesin Anda. Ketika Anda memulai Remote Control, sesi tersebut mendaftar dengan API Anthropic dan melakukan polling untuk pekerjaan. Ketika Anda terhubung dari perangkat lain, server merutekan pesan antara klien web atau mobile dan sesi lokal Anda melalui koneksi streaming.

Semua lalu lintas berjalan melalui API Anthropic melalui TLS, keamanan transportasi yang sama seperti sesi Claude Code apa pun. Koneksi menggunakan beberapa kredensial berumur pendek, masing-masing dibatasi untuk satu tujuan dan kedaluwarsa secara independen.

## Remote Control vs Claude Code di web

Remote Control dan [Claude Code di web](/id/claude-code-on-the-web) keduanya menggunakan antarmuka claude.ai/code. Perbedaan utamanya adalah di mana sesi berjalan: Remote Control dieksekusi di mesin Anda, jadi MCP servers lokal, alat, dan konfigurasi proyek Anda tetap tersedia. Claude Code di web dieksekusi di infrastruktur cloud yang dikelola Anthropic.

Gunakan Remote Control ketika Anda sedang dalam pekerjaan lokal dan ingin terus melanjutkan dari perangkat lain. Gunakan Claude Code di web ketika Anda ingin memulai tugas tanpa pengaturan lokal apa pun, bekerja pada repo yang tidak Anda miliki, atau menjalankan beberapa tugas secara paralel.

## Batasan

* **Satu sesi jarak jauh pada satu waktu**: setiap sesi Claude Code mendukung satu koneksi jarak jauh.
* **Terminal harus tetap terbuka**: Remote Control berjalan sebagai proses lokal. Jika Anda menutup terminal atau menghentikan proses `claude`, sesi berakhir. Jalankan `claude remote-control` lagi untuk memulai yang baru.
* **Pemadaman jaringan yang diperpanjang**: jika mesin Anda aktif tetapi tidak dapat menjangkau jaringan selama lebih dari kira-kira 10 menit, sesi habis waktu dan proses keluar. Jalankan `claude remote-control` lagi untuk memulai sesi baru.

## Sumber daya terkait

* [Claude Code di web](/id/claude-code-on-the-web): jalankan sesi di lingkungan cloud yang dikelola Anthropic alih-alih di mesin Anda
* [Autentikasi](/id/authentication): atur `/login` dan kelola kredensial untuk claude.ai
* [Referensi CLI](/id/cli-reference): daftar lengkap flag dan perintah termasuk `claude remote-control`
* [Keamanan](/id/security): bagaimana sesi Remote Control sesuai dengan model keamanan Claude Code
* [Penggunaan data](/id/data-usage): data apa yang mengalir melalui API Anthropic selama sesi lokal dan jarak jauh
