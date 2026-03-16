> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mode interaktif

> Referensi lengkap untuk pintasan keyboard, mode input, dan fitur interaktif dalam sesi Claude Code.

## Pintasan keyboard

<Note>
  Pintasan keyboard mungkin berbeda menurut platform dan terminal. Tekan `?` untuk melihat pintasan yang tersedia untuk lingkungan Anda.

  **Pengguna macOS**: Pintasan tombol Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) memerlukan konfigurasi Option sebagai Meta di terminal Anda:

  * **iTerm2**: settings → Profiles → Keys → atur Left/Right Option key ke "Esc+"
  * **Terminal.app**: settings → Profiles → Keyboard → centang "Use Option as Meta Key"
  * **VS Code**: settings → Profiles → Keys → atur Left/Right Option key ke "Esc+"

  Lihat [Konfigurasi terminal](/id/terminal-config) untuk detail.
</Note>

### Kontrol umum

| Pintasan                                              | Deskripsi                                                                           | Konteks                                                                                                                             |
| :---------------------------------------------------- | :---------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                              | Batalkan input atau generasi saat ini                                               | Interupsi standar                                                                                                                   |
| `Ctrl+F`                                              | Matikan semua agen latar belakang. Tekan dua kali dalam 3 detik untuk mengonfirmasi | Kontrol agen latar belakang                                                                                                         |
| `Ctrl+D`                                              | Keluar dari sesi Claude Code                                                        | Sinyal EOF                                                                                                                          |
| `Ctrl+G`                                              | Buka di editor teks default                                                         | Edit prompt atau respons kustom Anda di editor teks default                                                                         |
| `Ctrl+L`                                              | Bersihkan layar terminal                                                            | Menjaga riwayat percakapan                                                                                                          |
| `Ctrl+O`                                              | Alihkan output verbose                                                              | Menampilkan penggunaan alat dan eksekusi terperinci                                                                                 |
| `Ctrl+R`                                              | Pencarian riwayat perintah terbalik                                                 | Cari melalui perintah sebelumnya secara interaktif                                                                                  |
| `Ctrl+V` atau `Cmd+V` (iTerm2) atau `Alt+V` (Windows) | Tempel gambar dari clipboard                                                        | Menempel gambar atau jalur ke file gambar                                                                                           |
| `Ctrl+B`                                              | Tugas yang berjalan di latar belakang                                               | Menjalankan perintah bash dan agen di latar belakang. Pengguna Tmux tekan dua kali                                                  |
| `Ctrl+T`                                              | Alihkan daftar tugas                                                                | Tampilkan atau sembunyikan [daftar tugas](#task-list) di area status terminal                                                       |
| `Left/Right arrows`                                   | Siklus melalui tab dialog                                                           | Navigasi antar tab dalam dialog izin dan menu                                                                                       |
| `Up/Down arrows`                                      | Navigasi riwayat perintah                                                           | Ingat kembali input sebelumnya                                                                                                      |
| `Esc` + `Esc`                                         | Putar ulang atau ringkas                                                            | Pulihkan kode dan/atau percakapan ke titik sebelumnya, atau ringkas dari pesan yang dipilih                                         |
| `Shift+Tab` atau `Alt+M` (beberapa konfigurasi)       | Alihkan mode izin                                                                   | Beralih antara Mode Auto-Accept, Plan Mode, dan mode normal.                                                                        |
| `Option+P` (macOS) atau `Alt+P` (Windows/Linux)       | Alihkan model                                                                       | Alihkan model tanpa menghapus prompt Anda                                                                                           |
| `Option+T` (macOS) atau `Alt+T` (Windows/Linux)       | Alihkan pemikiran yang diperluas                                                    | Aktifkan atau nonaktifkan mode pemikiran yang diperluas. Jalankan `/terminal-setup` terlebih dahulu untuk mengaktifkan pintasan ini |

### Pengeditan teks

| Pintasan                   | Deskripsi                          | Konteks                                                                                                                       |
| :------------------------- | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                   | Hapus hingga akhir baris           | Menyimpan teks yang dihapus untuk ditempel                                                                                    |
| `Ctrl+U`                   | Hapus seluruh baris                | Menyimpan teks yang dihapus untuk ditempel                                                                                    |
| `Ctrl+Y`                   | Tempel teks yang dihapus           | Tempel teks yang dihapus dengan `Ctrl+K` atau `Ctrl+U`                                                                        |
| `Alt+Y` (setelah `Ctrl+Y`) | Siklus riwayat tempel              | Setelah menempel, siklus melalui teks yang dihapus sebelumnya. Memerlukan [Option sebagai Meta](#keyboard-shortcuts) di macOS |
| `Alt+B`                    | Pindahkan kursor kembali satu kata | Navigasi kata. Memerlukan [Option sebagai Meta](#keyboard-shortcuts) di macOS                                                 |
| `Alt+F`                    | Pindahkan kursor maju satu kata    | Navigasi kata. Memerlukan [Option sebagai Meta](#keyboard-shortcuts) di macOS                                                 |

### Tema dan tampilan

| Pintasan | Deskripsi                                  | Konteks                                                                                                                   |
| :------- | :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `Ctrl+T` | Alihkan penyorotan sintaks untuk blok kode | Hanya berfungsi di dalam menu pemilih `/theme`. Mengontrol apakah kode dalam respons Claude menggunakan pewarnaan sintaks |

<Note>
  Penyorotan sintaks hanya tersedia dalam build asli Claude Code.
</Note>

### Input multiline

| Metode         | Pintasan        | Konteks                                               |
| :------------- | :-------------- | :---------------------------------------------------- |
| Escape cepat   | `\` + `Enter`   | Berfungsi di semua terminal                           |
| Default macOS  | `Option+Enter`  | Default di macOS                                      |
| Shift+Enter    | `Shift+Enter`   | Berfungsi langsung di iTerm2, WezTerm, Ghostty, Kitty |
| Urutan kontrol | `Ctrl+J`        | Karakter line feed untuk multiline                    |
| Mode tempel    | Tempel langsung | Untuk blok kode, log                                  |

<Tip>
  Shift+Enter berfungsi tanpa konfigurasi di iTerm2, WezTerm, Ghostty, dan Kitty. Untuk terminal lain (VS Code, Alacritty, Zed, Warp), jalankan `/terminal-setup` untuk memasang binding.
</Tip>

### Perintah cepat

| Pintasan    | Deskripsi             | Catatan                                                              |
| :---------- | :-------------------- | :------------------------------------------------------------------- |
| `/` di awal | Perintah atau skill   | Lihat [perintah bawaan](#built-in-commands) dan [skills](/id/skills) |
| `!` di awal | Mode Bash             | Jalankan perintah langsung dan tambahkan output eksekusi ke sesi     |
| `@`         | Penyebutan jalur file | Picu pelengkapan otomatis jalur file                                 |

## Perintah bawaan

Ketik `/` di Claude Code untuk melihat semua perintah yang tersedia, atau ketik `/` diikuti huruf apa pun untuk memfilter. Tidak semua perintah terlihat oleh setiap pengguna. Beberapa tergantung pada platform, paket, atau lingkungan Anda. Misalnya, `/desktop` hanya muncul di macOS dan Windows, `/upgrade` dan `/privacy-settings` hanya tersedia di paket Pro dan Max, dan `/terminal-setup` disembunyikan ketika terminal Anda secara asli mendukung pintasan kuncinya.

Claude Code juga dilengkapi dengan [skills bundel](/id/skills#bundled-skills) seperti `/simplify`, `/batch`, dan `/debug` yang muncul bersama perintah bawaan saat Anda mengetik `/`. Untuk membuat perintah Anda sendiri, lihat [skills](/id/skills).

Dalam tabel di bawah, `<arg>` menunjukkan argumen yang diperlukan dan `[arg]` menunjukkan argumen opsional.

| Perintah                  | Tujuan                                                                                                                                                                                                                            |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | Tambahkan direktori kerja baru ke sesi saat ini                                                                                                                                                                                   |
| `/agents`                 | Kelola konfigurasi [agent](/id/sub-agents)                                                                                                                                                                                        |
| `/btw <question>`         | Ajukan [pertanyaan sampingan](#side-questions-with-%2Fbtw) cepat tanpa menambah percakapan                                                                                                                                        |
| `/chrome`                 | Konfigurasi pengaturan [Claude di Chrome](/id/chrome)                                                                                                                                                                             |
| `/clear`                  | Bersihkan riwayat percakapan dan bebaskan konteks. Alias: `/reset`, `/new`                                                                                                                                                        |
| `/compact [instructions]` | Kompak percakapan dengan instruksi fokus opsional                                                                                                                                                                                 |
| `/config`                 | Buka antarmuka [Pengaturan](/id/settings) untuk menyesuaikan tema, model, [gaya output](/id/output-styles), dan preferensi lainnya. Alias: `/settings`                                                                            |
| `/context`                | Visualisasikan penggunaan konteks saat ini sebagai grid berwarna                                                                                                                                                                  |
| `/copy`                   | Salin respons asisten terakhir ke clipboard. Ketika blok kode ada, menampilkan pemilih interaktif untuk memilih blok individual atau respons lengkap                                                                              |
| `/cost`                   | Tampilkan statistik penggunaan token. Lihat [panduan pelacakan biaya](/id/costs#using-the-cost-command) untuk detail khusus langganan                                                                                             |
| `/desktop`                | Lanjutkan sesi saat ini di aplikasi Claude Code Desktop. Hanya macOS dan Windows. Alias: `/app`                                                                                                                                   |
| `/diff`                   | Buka penampil diff interaktif yang menampilkan perubahan yang belum dilakukan dan diff per-turn. Gunakan panah kiri/kanan untuk beralih antara diff git saat ini dan turn Claude individual, dan atas/bawah untuk menelusuri file |
| `/doctor`                 | Diagnosa dan verifikasi instalasi dan pengaturan Claude Code Anda                                                                                                                                                                 |
| `/exit`                   | Keluar dari CLI. Alias: `/quit`                                                                                                                                                                                                   |
| `/export [filename]`      | Ekspor percakapan saat ini sebagai teks biasa. Dengan nama file, menulis langsung ke file itu. Tanpa, membuka dialog untuk menyalin ke clipboard atau menyimpan ke file                                                           |
| `/extra-usage`            | Konfigurasi penggunaan ekstra untuk terus bekerja ketika batas laju tercapai                                                                                                                                                      |
| `/fast [on\|off]`         | Alihkan [mode cepat](/id/fast-mode) aktif atau nonaktif                                                                                                                                                                           |
| `/feedback [report]`      | Kirimkan umpan balik tentang Claude Code. Alias: `/bug`                                                                                                                                                                           |
| `/fork [name]`            | Buat fork percakapan saat ini pada titik ini                                                                                                                                                                                      |
| `/help`                   | Tampilkan bantuan dan perintah yang tersedia                                                                                                                                                                                      |
| `/hooks`                  | Kelola konfigurasi [hook](/id/hooks) untuk peristiwa alat                                                                                                                                                                         |
| `/ide`                    | Kelola integrasi IDE dan tampilkan status                                                                                                                                                                                         |
| `/init`                   | Inisialisasi proyek dengan panduan `CLAUDE.md`                                                                                                                                                                                    |
| `/insights`               | Hasilkan laporan yang menganalisis sesi Claude Code Anda, termasuk area proyek, pola interaksi, dan titik gesekan                                                                                                                 |
| `/install-github-app`     | Atur aplikasi [Claude GitHub Actions](/id/github-actions) untuk repositori. Memandu Anda memilih repo dan mengonfigurasi integrasi                                                                                                |
| `/install-slack-app`      | Instal aplikasi Claude Slack. Membuka browser untuk menyelesaikan alur OAuth                                                                                                                                                      |
| `/keybindings`            | Buka atau buat file konfigurasi pintasan keyboard Anda                                                                                                                                                                            |
| `/login`                  | Masuk ke akun Anthropic Anda                                                                                                                                                                                                      |
| `/logout`                 | Keluar dari akun Anthropic Anda                                                                                                                                                                                                   |
| `/mcp`                    | Kelola koneksi server MCP dan autentikasi OAuth                                                                                                                                                                                   |
| `/memory`                 | Edit file memori `CLAUDE.md`, aktifkan atau nonaktifkan [auto-memory](/id/memory#auto-memory), dan lihat entri auto-memory                                                                                                        |
| `/mobile`                 | Tampilkan kode QR untuk mengunduh aplikasi mobile Claude. Alias: `/ios`, `/android`                                                                                                                                               |
| `/model [model]`          | Pilih atau ubah model AI. Untuk model yang mendukungnya, gunakan panah kiri/kanan untuk [menyesuaikan tingkat upaya](/id/model-config#adjust-effort-level). Perubahan berlaku segera tanpa menunggu respons saat ini selesai      |
| `/passes`                 | Bagikan minggu gratis Claude Code dengan teman. Hanya terlihat jika akun Anda memenuhi syarat                                                                                                                                     |
| `/permissions`            | Lihat atau perbarui [izin](/id/permissions#manage-permissions). Alias: `/allowed-tools`                                                                                                                                           |
| `/plan`                   | Masuk mode rencana langsung dari prompt                                                                                                                                                                                           |
| `/plugin`                 | Kelola [plugin](/id/plugins) Claude Code                                                                                                                                                                                          |
| `/pr-comments [PR]`       | Ambil dan tampilkan komentar dari permintaan tarik GitHub. Secara otomatis mendeteksi PR untuk cabang saat ini, atau lewatkan URL atau nomor PR. Memerlukan CLI `gh`                                                              |
| `/privacy-settings`       | Lihat dan perbarui pengaturan privasi Anda. Hanya tersedia untuk pelanggan paket Pro dan Max                                                                                                                                      |
| `/release-notes`          | Lihat changelog lengkap, dengan versi terbaru paling dekat dengan prompt Anda                                                                                                                                                     |
| `/reload-plugins`         | Muat ulang semua [plugin](/id/plugins) aktif untuk menerapkan perubahan yang tertunda tanpa memulai ulang. Melaporkan apa yang dimuat dan mencatat perubahan apa pun yang memerlukan restart                                      |
| `/remote-control`         | Buat sesi ini tersedia untuk [kontrol jarak jauh](/id/remote-control) dari claude.ai. Alias: `/rc`                                                                                                                                |
| `/remote-env`             | Konfigurasi lingkungan jarak jauh default untuk [sesi teleport](/id/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)                                                                                               |
| `/rename [name]`          | Ubah nama sesi saat ini. Tanpa nama, secara otomatis menghasilkan satu dari riwayat percakapan                                                                                                                                    |
| `/resume [session]`       | Lanjutkan percakapan berdasarkan ID atau nama, atau buka pemilih sesi. Alias: `/continue`                                                                                                                                         |
| `/review`                 | Tidak digunakan lagi. Instal [plugin `code-review`](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md) sebagai gantinya: `claude plugin install code-review@claude-code-marketplace`          |
| `/rewind`                 | Putar ulang percakapan dan/atau kode ke titik sebelumnya, atau ringkas dari pesan yang dipilih. Lihat [checkpointing](/id/checkpointing). Alias: `/checkpoint`                                                                    |
| `/sandbox`                | Alihkan [mode sandbox](/id/sandboxing). Tersedia hanya di platform yang didukung                                                                                                                                                  |
| `/security-review`        | Analisis perubahan yang tertunda di cabang saat ini untuk kerentanan keamanan. Meninjau diff git dan mengidentifikasi risiko seperti injeksi, masalah auth, dan paparan data                                                      |
| `/skills`                 | Daftar [skills](/id/skills) yang tersedia                                                                                                                                                                                         |
| `/stats`                  | Visualisasikan penggunaan harian, riwayat sesi, streak, dan preferensi model                                                                                                                                                      |
| `/status`                 | Buka antarmuka Pengaturan (tab Status) yang menampilkan versi, model, akun, dan konektivitas                                                                                                                                      |
| `/statusline`             | Konfigurasi [status line](/id/statusline) Claude Code. Jelaskan apa yang Anda inginkan, atau jalankan tanpa argumen untuk auto-configure dari prompt shell Anda                                                                   |
| `/stickers`               | Pesan stiker Claude Code                                                                                                                                                                                                          |
| `/tasks`                  | Daftar dan kelola tugas latar belakang                                                                                                                                                                                            |
| `/terminal-setup`         | Konfigurasi pintasan keyboard terminal untuk Shift+Enter dan pintasan lainnya. Hanya terlihat di terminal yang membutuhkannya, seperti VS Code, Alacritty, atau Warp                                                              |
| `/theme`                  | Ubah tema warna. Mencakup varian terang dan gelap, tema yang dapat diakses buta warna (daltonized), dan tema ANSI yang menggunakan palet warna terminal Anda                                                                      |
| `/upgrade`                | Buka halaman upgrade untuk beralih ke tingkat paket yang lebih tinggi                                                                                                                                                             |
| `/usage`                  | Tampilkan batas penggunaan paket dan status batas laju                                                                                                                                                                            |
| `/vim`                    | Alihkan antara mode pengeditan Vim dan Normal                                                                                                                                                                                     |

### Prompt MCP

Server MCP dapat mengekspos prompt yang muncul sebagai perintah. Ini menggunakan format `/mcp__<server>__<prompt>` dan secara dinamis ditemukan dari server yang terhubung. Lihat [prompt MCP](/id/mcp#use-mcp-prompts-as-commands) untuk detail.

## Mode editor Vim

Aktifkan pengeditan gaya vim dengan perintah `/vim` atau konfigurasi secara permanen melalui `/config`.

### Pengalihan mode

| Perintah | Tindakan                | Dari mode |
| :------- | :---------------------- | :-------- |
| `Esc`    | Masuk mode NORMAL       | INSERT    |
| `i`      | Sisipkan sebelum kursor | NORMAL    |
| `I`      | Sisipkan di awal baris  | NORMAL    |
| `a`      | Sisipkan setelah kursor | NORMAL    |
| `A`      | Sisipkan di akhir baris | NORMAL    |
| `o`      | Buka baris di bawah     | NORMAL    |
| `O`      | Buka baris di atas      | NORMAL    |

### Navigasi (mode NORMAL)

| Perintah        | Tindakan                                                    |
| :-------------- | :---------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Pindah kiri/bawah/atas/kanan                                |
| `w`             | Kata berikutnya                                             |
| `e`             | Akhir kata                                                  |
| `b`             | Kata sebelumnya                                             |
| `0`             | Awal baris                                                  |
| `$`             | Akhir baris                                                 |
| `^`             | Karakter non-blank pertama                                  |
| `gg`            | Awal input                                                  |
| `G`             | Akhir input                                                 |
| `f{char}`       | Lompat ke kemunculan berikutnya dari karakter               |
| `F{char}`       | Lompat ke kemunculan sebelumnya dari karakter               |
| `t{char}`       | Lompat ke tepat sebelum kemunculan berikutnya dari karakter |
| `T{char}`       | Lompat ke tepat setelah kemunculan sebelumnya dari karakter |
| `;`             | Ulangi gerakan f/F/t/T terakhir                             |
| `,`             | Ulangi gerakan f/F/t/T terakhir dalam urutan terbalik       |

<Note>
  Dalam mode normal vim, jika kursor berada di awal atau akhir input dan tidak dapat bergerak lebih jauh, tombol panah menavigasi riwayat perintah sebagai gantinya.
</Note>

### Pengeditan (mode NORMAL)

| Perintah       | Tindakan                        |
| :------------- | :------------------------------ |
| `x`            | Hapus karakter                  |
| `dd`           | Hapus baris                     |
| `D`            | Hapus hingga akhir baris        |
| `dw`/`de`/`db` | Hapus kata/hingga akhir/kembali |
| `cc`           | Ubah baris                      |
| `C`            | Ubah hingga akhir baris         |
| `cw`/`ce`/`cb` | Ubah kata/hingga akhir/kembali  |
| `yy`/`Y`       | Yank (salin) baris              |
| `yw`/`ye`/`yb` | Yank kata/hingga akhir/kembali  |
| `p`            | Tempel setelah kursor           |
| `P`            | Tempel sebelum kursor           |
| `>>`           | Indentasi baris                 |
| `<<`           | Dedentasi baris                 |
| `J`            | Gabungkan baris                 |
| `.`            | Ulangi perubahan terakhir       |

### Objek teks (mode NORMAL)

Objek teks bekerja dengan operator seperti `d`, `c`, dan `y`:

| Perintah  | Tindakan                                 |
| :-------- | :--------------------------------------- |
| `iw`/`aw` | Kata dalam/sekitar                       |
| `iW`/`aW` | WORD dalam/sekitar (dibatasi whitespace) |
| `i"`/`a"` | Dalam/sekitar tanda kutip ganda          |
| `i'`/`a'` | Dalam/sekitar tanda kutip tunggal        |
| `i(`/`a(` | Dalam/sekitar tanda kurung               |
| `i[`/`a[` | Dalam/sekitar tanda kurung siku          |
| `i{`/`a{` | Dalam/sekitar tanda kurung kurawal       |

## Riwayat perintah

Claude Code mempertahankan riwayat perintah untuk sesi saat ini:

* Riwayat input disimpan per direktori kerja
* Riwayat input direset ketika Anda menjalankan `/clear` untuk memulai sesi baru. Percakapan sesi sebelumnya dipertahankan dan dapat dilanjutkan.
* Gunakan panah Atas/Bawah untuk menavigasi (lihat pintasan keyboard di atas)
* **Catatan**: ekspansi riwayat (`!`) dinonaktifkan secara default

### Pencarian terbalik dengan Ctrl+R

Tekan `Ctrl+R` untuk secara interaktif mencari melalui riwayat perintah Anda:

1. **Mulai pencarian**: tekan `Ctrl+R` untuk mengaktifkan pencarian riwayat terbalik
2. **Ketik kueri**: masukkan teks untuk dicari di perintah sebelumnya. Istilah pencarian disorot dalam hasil yang cocok
3. **Navigasi kecocokan**: tekan `Ctrl+R` lagi untuk siklus melalui kecocokan yang lebih lama
4. **Terima kecocokan**:
   * Tekan `Tab` atau `Esc` untuk menerima kecocokan saat ini dan lanjutkan pengeditan
   * Tekan `Enter` untuk menerima dan menjalankan perintah segera
5. **Batalkan pencarian**:
   * Tekan `Ctrl+C` untuk membatalkan dan mengembalikan input asli Anda
   * Tekan `Backspace` pada pencarian kosong untuk membatalkan

Pencarian menampilkan perintah yang cocok dengan istilah pencarian disorot, sehingga Anda dapat menemukan dan menggunakan kembali input sebelumnya.

## Perintah bash latar belakang

Claude Code mendukung menjalankan perintah bash di latar belakang, memungkinkan Anda untuk terus bekerja sementara proses yang berjalan lama dieksekusi.

### Cara backgrounding bekerja

Ketika Claude Code menjalankan perintah di latar belakang, ia menjalankan perintah secara asinkron dan segera mengembalikan ID tugas latar belakang. Claude Code dapat merespons prompt baru sementara perintah terus dieksekusi di latar belakang.

Untuk menjalankan perintah di latar belakang, Anda dapat:

* Minta Claude Code untuk menjalankan perintah di latar belakang
* Tekan Ctrl+B untuk memindahkan invokasi alat Bash biasa ke latar belakang. (Pengguna Tmux harus menekan Ctrl+B dua kali karena kunci awalan tmux.)

**Fitur utama:**

* Output di-buffer dan Claude dapat mengambilnya menggunakan alat TaskOutput
* Tugas latar belakang memiliki ID unik untuk pelacakan dan pengambilan output
* Tugas latar belakang secara otomatis dibersihkan ketika Claude Code keluar

Untuk menonaktifkan semua fungsionalitas tugas latar belakang, atur variabel lingkungan `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` ke `1`. Lihat [Variabel lingkungan](/id/settings#environment-variables) untuk detail.

**Perintah yang sering di-background:**

* Alat build (webpack, vite, make)
* Manajer paket (npm, yarn, pnpm)
* Pelari tes (jest, pytest)
* Server pengembangan
* Proses yang berjalan lama (docker, terraform)

### Mode Bash dengan awalan `!`

Jalankan perintah bash langsung tanpa melalui Claude dengan menambahkan awalan input Anda dengan `!`:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Mode Bash:

* Menambahkan perintah dan outputnya ke konteks percakapan
* Menampilkan kemajuan dan output real-time
* Mendukung backgrounding `Ctrl+B` yang sama untuk perintah yang berjalan lama
* Tidak memerlukan Claude untuk menginterpretasi atau menyetujui perintah
* Mendukung pelengkapan otomatis berbasis riwayat: ketik perintah parsial dan tekan **Tab** untuk melengkapi dari perintah `!` sebelumnya di proyek saat ini
* Keluar dengan `Escape`, `Backspace`, atau `Ctrl+U` pada prompt kosong

Ini berguna untuk operasi shell cepat sambil mempertahankan konteks percakapan.

## Saran prompt

Ketika Anda pertama kali membuka sesi, perintah contoh yang digelapkan muncul di input prompt untuk membantu Anda memulai. Claude Code memilih ini dari riwayat git proyek Anda, jadi ini mencerminkan file yang telah Anda kerjakan baru-baru ini.

Setelah Claude merespons, saran terus muncul berdasarkan riwayat percakapan Anda, seperti langkah lanjutan dari permintaan multi-bagian atau kelanjutan alami dari alur kerja Anda.

* Tekan **Tab** untuk menerima saran, atau tekan **Enter** untuk menerima dan mengirimkan
* Mulai mengetik untuk menolaknya

Saran berjalan sebagai permintaan latar belakang yang menggunakan kembali cache prompt percakapan induk, jadi biaya tambahan minimal. Claude Code melewati pembuatan saran ketika cache dingin untuk menghindari biaya yang tidak perlu.

Saran secara otomatis dilewati setelah turn pertama percakapan, dalam mode non-interaktif, dan dalam mode rencana.

Untuk menonaktifkan saran prompt sepenuhnya, atur variabel lingkungan atau alihkan pengaturan di `/config`:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Pertanyaan sampingan dengan /btw

Gunakan `/btw` untuk mengajukan pertanyaan cepat tentang pekerjaan saat ini tanpa menambah riwayat percakapan. Ini berguna ketika Anda menginginkan jawaban cepat tetapi tidak ingin mengacaukan konteks utama atau mengalihkan Claude dari tugas yang berjalan lama.

```
/btw what was the name of that config file again?
```

Pertanyaan sampingan memiliki visibilitas penuh ke percakapan saat ini, jadi Anda dapat bertanya tentang kode yang telah dibaca Claude, keputusan yang dibuatnya sebelumnya, atau apa pun dari sesi. Pertanyaan dan jawaban bersifat sementara: mereka muncul dalam overlay yang dapat ditutup dan tidak pernah memasuki riwayat percakapan.

* **Tersedia saat Claude sedang bekerja**: Anda dapat menjalankan `/btw` bahkan saat Claude memproses respons. Pertanyaan sampingan berjalan secara independen dan tidak mengganggu turn utama.
* **Tidak ada akses alat**: pertanyaan sampingan hanya menjawab dari apa yang sudah ada dalam konteks. Claude tidak dapat membaca file, menjalankan perintah, atau mencari saat menjawab pertanyaan sampingan.
* **Respons tunggal**: tidak ada turn lanjutan. Jika Anda memerlukan bolak-balik, gunakan prompt normal sebagai gantinya.
* **Biaya rendah**: pertanyaan sampingan menggunakan kembali cache prompt percakapan induk, jadi biaya tambahan minimal.

Tekan **Space**, **Enter**, atau **Escape** untuk menolak jawaban dan kembali ke prompt.

`/btw` adalah kebalikan dari [subagent](/id/sub-agents): ia melihat percakapan lengkap Anda tetapi tidak memiliki alat, sementara subagent memiliki alat lengkap tetapi dimulai dengan konteks kosong. Gunakan `/btw` untuk bertanya tentang apa yang sudah diketahui Claude dari sesi ini; gunakan subagent untuk menemukan sesuatu yang baru.

## Daftar tugas

Ketika mengerjakan pekerjaan yang kompleks dan multi-langkah, Claude membuat daftar tugas untuk melacak kemajuan. Tugas muncul di area status terminal Anda dengan indikator yang menunjukkan apa yang tertunda, sedang berlangsung, atau selesai.

* Tekan `Ctrl+T` untuk mengalihkan tampilan daftar tugas. Tampilan menampilkan hingga 10 tugas sekaligus
* Untuk melihat semua tugas atau menghapusnya, minta Claude secara langsung: "show me all tasks" atau "clear all tasks"
* Tugas bertahan di seluruh pemadatan konteks, membantu Claude tetap terorganisir pada proyek yang lebih besar
* Untuk berbagi daftar tugas di seluruh sesi, atur `CLAUDE_CODE_TASK_LIST_ID` untuk menggunakan direktori bernama di `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* Untuk kembali ke daftar TODO sebelumnya, atur `CLAUDE_CODE_ENABLE_TASKS=false`.

## Status tinjauan PR

Ketika bekerja pada cabang dengan permintaan tarik terbuka, Claude Code menampilkan tautan PR yang dapat diklik di footer (misalnya, "PR #446"). Tautan memiliki garis bawah berwarna yang menunjukkan status tinjauan:

* Hijau: disetujui
* Kuning: menunggu tinjauan
* Merah: perubahan diminta
* Abu-abu: draft
* Ungu: digabungkan

`Cmd+click` (Mac) atau `Ctrl+click` (Windows/Linux) tautan untuk membuka permintaan tarik di browser Anda. Status diperbarui secara otomatis setiap 60 detik.

<Note>
  Status PR memerlukan CLI `gh` untuk diinstal dan diautentikasi (`gh auth login`).
</Note>

## Lihat juga

* [Skills](/id/skills) - Prompt dan alur kerja kustom
* [Checkpointing](/id/checkpointing) - Putar ulang pengeditan Claude dan pulihkan status sebelumnya
* [Referensi CLI](/id/cli-reference) - Bendera dan opsi baris perintah
* [Pengaturan](/id/settings) - Opsi konfigurasi
* [Manajemen memori](/id/memory) - Mengelola file CLAUDE.md
