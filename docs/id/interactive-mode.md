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

# Mode interaktif

> Referensi lengkap untuk pintasan keyboard, mode input, dan fitur interaktif dalam sesi Claude Code.

## Pintasan keyboard

<Note>
  Pintasan keyboard mungkin berbeda menurut platform dan terminal. Tekan `?` untuk melihat pintasan yang tersedia untuk lingkungan Anda.

  **Pengguna macOS**: Pintasan tombol Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`, `Alt+T`) memerlukan konfigurasi Option sebagai Meta di terminal Anda:

  * **iTerm2**: settings → Profiles → Keys → atur Left/Right Option key ke "Esc+"
  * **Terminal.app**: settings → Profiles → Keyboard → centang "Use Option as Meta Key"
  * **VS Code**: atur `"terminal.integrated.macOptionIsMeta": true` dalam pengaturan VS Code

  Lihat [Konfigurasi terminal](/id/terminal-config) untuk detail.
</Note>

### Kontrol umum

| Pintasan                                              | Deskripsi                                                                           | Konteks                                                                                                                                                                           |
| :---------------------------------------------------- | :---------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                              | Batalkan input atau generasi saat ini                                               | Interupsi standar                                                                                                                                                                 |
| `Ctrl+X Ctrl+K`                                       | Matikan semua agen latar belakang. Tekan dua kali dalam 3 detik untuk mengonfirmasi | Kontrol agen latar belakang                                                                                                                                                       |
| `Ctrl+D`                                              | Keluar dari sesi Claude Code                                                        | Sinyal EOF                                                                                                                                                                        |
| `Ctrl+G` atau `Ctrl+X Ctrl+E`                         | Buka di editor teks default                                                         | Edit prompt atau respons kustom Anda di editor teks default. `Ctrl+X Ctrl+E` adalah binding readline-native                                                                       |
| `Ctrl+L`                                              | Gambar ulang layar                                                                  | Melukis ulang UI saat ini tanpa menghapus riwayat percakapan                                                                                                                      |
| `Ctrl+O`                                              | Alihkan output verbose                                                              | Menampilkan penggunaan dan eksekusi alat yang terperinci. Juga memperluas panggilan baca dan pencarian MCP, yang runtuh menjadi satu baris seperti "Queried slack" secara default |
| `Ctrl+R`                                              | Pencarian riwayat perintah terbalik                                                 | Cari melalui perintah sebelumnya secara interaktif                                                                                                                                |
| `Ctrl+V` atau `Cmd+V` (iTerm2) atau `Alt+V` (Windows) | Tempel gambar dari clipboard                                                        | Menyisipkan chip `[Image #N]` di kursor sehingga Anda dapat mereferensikannya secara posisional dalam prompt Anda                                                                 |
| `Ctrl+B`                                              | Tugas yang berjalan di latar belakang                                               | Menjalankan perintah bash dan agen di latar belakang. Pengguna Tmux tekan dua kali                                                                                                |
| `Ctrl+T`                                              | Alihkan daftar tugas                                                                | Tampilkan atau sembunyikan [daftar tugas](#task-list) di area status terminal                                                                                                     |
| `Left/Right arrows`                                   | Siklus melalui tab dialog                                                           | Navigasi antar tab dalam dialog izin dan menu                                                                                                                                     |
| `Up/Down arrows`                                      | Navigasi riwayat perintah                                                           | Ingat kembali input sebelumnya                                                                                                                                                    |
| `Esc` + `Esc`                                         | Putar ulang atau ringkas                                                            | Kembalikan kode dan/atau percakapan ke titik sebelumnya, atau ringkas dari pesan yang dipilih                                                                                     |
| `Shift+Tab` atau `Alt+M` (beberapa konfigurasi)       | Alihkan mode izin                                                                   | Beralih antara `default`, `acceptEdits`, `plan`, dan mode apa pun yang telah Anda aktifkan, seperti `auto` atau `bypassPermissions`. Lihat [mode izin](/id/permission-modes).     |
| `Option+P` (macOS) atau `Alt+P` (Windows/Linux)       | Alihkan model                                                                       | Alihkan model tanpa menghapus prompt Anda                                                                                                                                         |
| `Option+T` (macOS) atau `Alt+T` (Windows/Linux)       | Alihkan pemikiran yang diperluas                                                    | Aktifkan atau nonaktifkan mode pemikiran yang diperluas. Di macOS, konfigurasi terminal Anda untuk mengirim Option sebagai Meta agar pintasan ini berfungsi                       |
| `Option+O` (macOS) atau `Alt+O` (Windows/Linux)       | Alihkan mode cepat                                                                  | Aktifkan atau nonaktifkan [mode cepat](/id/fast-mode)                                                                                                                             |

### Pengeditan teks

| Pintasan                   | Deskripsi                          | Konteks                                                                                                                       |
| :------------------------- | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                   | Hapus hingga akhir baris           | Menyimpan teks yang dihapus untuk ditempel                                                                                    |
| `Ctrl+U`                   | Hapus dari kursor ke awal baris    | Menyimpan teks yang dihapus untuk ditempel. Ulangi untuk menghapus di seluruh baris dalam input multiline                     |
| `Ctrl+Y`                   | Tempel teks yang dihapus           | Tempel teks yang dihapus dengan `Ctrl+K` atau `Ctrl+U`                                                                        |
| `Alt+Y` (setelah `Ctrl+Y`) | Siklus riwayat tempel              | Setelah menempel, siklus melalui teks yang dihapus sebelumnya. Memerlukan [Option sebagai Meta](#keyboard-shortcuts) di macOS |
| `Alt+B`                    | Pindahkan kursor kembali satu kata | Navigasi kata. Memerlukan [Option sebagai Meta](#keyboard-shortcuts) di macOS                                                 |
| `Alt+F`                    | Pindahkan kursor maju satu kata    | Navigasi kata. Memerlukan [Option sebagai Meta](#keyboard-shortcuts) di macOS                                                 |

### Tema dan tampilan

| Pintasan | Deskripsi                                  | Konteks                                                                                                                   |
| :------- | :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `Ctrl+T` | Alihkan penyorotan sintaks untuk blok kode | Hanya berfungsi di dalam menu pemilih `/theme`. Mengontrol apakah kode dalam respons Claude menggunakan pewarnaan sintaks |

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

| Pintasan    | Deskripsi             | Catatan                                                                 |
| :---------- | :-------------------- | :---------------------------------------------------------------------- |
| `/` di awal | Perintah atau skill   | Lihat [perintah bawaan](#built-in-commands) dan [skills](/id/skills)    |
| `!` di awal | Mode Bash             | Jalankan perintah secara langsung dan tambahkan output eksekusi ke sesi |
| `@`         | Penyebutan jalur file | Picu pelengkapan otomatis jalur file                                    |

### Penampil transkrip

Ketika penampil transkrip terbuka (dialihkan dengan `Ctrl+O`), pintasan ini tersedia. `Ctrl+E` dapat diubah melalui [`transcript:toggleShowAll`](/id/keybindings).

| Pintasan             | Deskripsi                                                                                           |
| :------------------- | :-------------------------------------------------------------------------------------------------- |
| `Ctrl+E`             | Alihkan tampilkan semua konten                                                                      |
| `q`, `Ctrl+C`, `Esc` | Keluar dari tampilan transkrip. Ketiganya dapat diubah melalui [`transcript:exit`](/id/keybindings) |

### Input suara

| Pintasan      | Deskripsi              | Catatan                                                                                                                                                             |
| :------------ | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tahan `Space` | Dictation push-to-talk | Memerlukan [voice dictation](/id/voice-dictation) untuk diaktifkan. Transkrip disisipkan di kursor. [Dapat diubah](/id/voice-dictation#rebind-the-push-to-talk-key) |

## Perintah bawaan

Ketik `/` di Claude Code untuk melihat semua perintah yang tersedia, atau ketik `/` diikuti huruf apa pun untuk memfilter. Menu `/` menampilkan perintah bawaan dan [skills bundel](/id/skills#bundled-skills) seperti `/simplify`. Tidak semua perintah terlihat oleh setiap pengguna karena beberapa bergantung pada platform atau paket Anda.

Lihat [referensi perintah](/id/commands) untuk daftar lengkap perintah bawaan. Untuk membuat perintah Anda sendiri, lihat [skills](/id/skills).

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
| `<<`           | Kurangi indentasi baris         |
| `J`            | Gabungkan baris                 |
| `.`            | Ulangi perubahan terakhir       |

### Objek teks (mode NORMAL)

Objek teks bekerja dengan operator seperti `d`, `c`, dan `y`:

| Perintah  | Tindakan                                 |
| :-------- | :--------------------------------------- |
| `iw`/`aw` | Kata dalam/sekitar                       |
| `iW`/`aW` | KATA dalam/sekitar (dibatasi whitespace) |
| `i"`/`a"` | Dalam/sekitar tanda kutip ganda          |
| `i'`/`a'` | Dalam/sekitar tanda kutip tunggal        |
| `i(`/`a(` | Dalam/sekitar tanda kurung               |
| `i[`/`a[` | Dalam/sekitar kurung siku                |
| `i{`/`a{` | Dalam/sekitar kurung kurawal             |

## Riwayat perintah

Claude Code mempertahankan riwayat perintah untuk sesi saat ini:

* Riwayat input disimpan per direktori kerja
* Riwayat input direset ketika Anda menjalankan `/clear` untuk memulai sesi baru. Percakapan sesi sebelumnya disimpan dan dapat dilanjutkan.
* Gunakan panah Atas/Bawah untuk menavigasi (lihat pintasan keyboard di atas)
* **Catatan**: ekspansi riwayat (`!`) dinonaktifkan secara default

### Pencarian terbalik dengan Ctrl+R

Tekan `Ctrl+R` untuk mencari secara interaktif melalui riwayat perintah Anda:

1. **Mulai pencarian**: tekan `Ctrl+R` untuk mengaktifkan pencarian riwayat terbalik
2. **Ketik kueri**: masukkan teks untuk dicari dalam perintah sebelumnya. Istilah pencarian disorot dalam hasil yang cocok
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

* Output ditulis ke file dan Claude dapat mengambilnya menggunakan alat Read
* Tugas latar belakang memiliki ID unik untuk pelacakan dan pengambilan output
* Tugas latar belakang dibersihkan secara otomatis ketika Claude Code keluar
* Tugas latar belakang secara otomatis dihentikan jika output melebihi 5GB, dengan catatan di stderr yang menjelaskan alasannya

Untuk menonaktifkan semua fungsionalitas tugas latar belakang, atur variabel lingkungan `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` ke `1`. Lihat [Variabel lingkungan](/id/env-vars) untuk detail.

**Perintah yang sering di-background:**

* Alat build (webpack, vite, make)
* Manajer paket (npm, yarn, pnpm)
* Pelari tes (jest, pytest)
* Server pengembangan
* Proses yang berjalan lama (docker, terraform)

### Mode Bash dengan awalan `!`

Jalankan perintah bash secara langsung tanpa melalui Claude dengan menambahkan awalan input Anda dengan `!`:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Mode Bash:

* Menambahkan perintah dan outputnya ke konteks percakapan
* Menampilkan kemajuan dan output secara real-time
* Mendukung backgrounding `Ctrl+B` yang sama untuk perintah yang berjalan lama
* Tidak memerlukan Claude untuk menginterpretasi atau menyetujui perintah
* Mendukung pelengkapan otomatis berbasis riwayat: ketik perintah parsial dan tekan **Tab** untuk melengkapi dari perintah `!` sebelumnya dalam proyek saat ini
* Keluar dengan `Escape`, `Backspace`, atau `Ctrl+U` pada prompt kosong
* Menempel teks yang dimulai dengan `!` ke prompt kosong memasuki mode bash secara otomatis, sesuai dengan perilaku `!` yang diketik

Ini berguna untuk operasi shell cepat sambil mempertahankan konteks percakapan.

## Saran prompt

Ketika Anda pertama kali membuka sesi, perintah contoh yang digelapkan muncul di input prompt untuk membantu Anda memulai. Claude Code memilih ini dari riwayat git proyek Anda, sehingga mencerminkan file yang telah Anda kerjakan baru-baru ini.

Setelah Claude merespons, saran terus muncul berdasarkan riwayat percakapan Anda, seperti langkah lanjutan dari permintaan multi-bagian atau kelanjutan alami dari alur kerja Anda.

* Tekan **Tab** atau **Right arrow** untuk menerima saran, atau tekan **Enter** untuk menerima dan mengirimkan
* Mulai mengetik untuk menolaknya

Saran berjalan sebagai permintaan latar belakang yang menggunakan kembali cache prompt percakapan induk, sehingga biaya tambahan minimal. Claude Code melewati pembuatan saran ketika cache dingin untuk menghindari biaya yang tidak perlu.

Saran secara otomatis dilewati setelah giliran pertama percakapan, dalam mode non-interaktif, dan dalam mode plan.

Untuk menonaktifkan saran prompt sepenuhnya, atur variabel lingkungan atau alihkan pengaturan di `/config`:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Pertanyaan sampingan dengan /btw

Gunakan `/btw` untuk mengajukan pertanyaan cepat tentang pekerjaan saat ini Anda tanpa menambahkan ke riwayat percakapan. Ini berguna ketika Anda menginginkan jawaban cepat tetapi tidak ingin mengacaukan konteks utama atau mengalihkan Claude dari tugas yang berjalan lama.

```
/btw what was the name of that config file again?
```

Pertanyaan sampingan memiliki visibilitas penuh ke percakapan saat ini, sehingga Anda dapat bertanya tentang kode yang telah dibaca Claude, keputusan yang dibuatnya sebelumnya, atau apa pun dari sesi. Pertanyaan dan jawaban bersifat sementara: mereka muncul dalam overlay yang dapat ditutup dan tidak pernah memasuki riwayat percakapan.

* **Tersedia saat Claude sedang bekerja**: Anda dapat menjalankan `/btw` bahkan saat Claude memproses respons. Pertanyaan sampingan berjalan secara independen dan tidak mengganggu giliran utama.
* **Tidak ada akses alat**: pertanyaan sampingan hanya menjawab dari apa yang sudah ada dalam konteks. Claude tidak dapat membaca file, menjalankan perintah, atau mencari saat menjawab pertanyaan sampingan.
* **Respons tunggal**: tidak ada giliran lanjutan. Jika Anda memerlukan bolak-balik, gunakan prompt normal sebagai gantinya.
* **Biaya rendah**: pertanyaan sampingan menggunakan kembali cache prompt percakapan induk, sehingga biaya tambahan minimal.

Tekan **Space**, **Enter**, atau **Escape** untuk menolak jawaban dan kembali ke prompt.

`/btw` adalah kebalikan dari [subagent](/id/sub-agents): ia melihat percakapan lengkap Anda tetapi tidak memiliki alat, sementara subagent memiliki alat lengkap tetapi dimulai dengan konteks kosong. Gunakan `/btw` untuk bertanya tentang apa yang sudah diketahui Claude dari sesi ini; gunakan subagent untuk menemukan sesuatu yang baru.

## Daftar tugas

Ketika mengerjakan pekerjaan yang kompleks dan multi-langkah, Claude membuat daftar tugas untuk melacak kemajuan. Tugas muncul di area status terminal Anda dengan indikator yang menunjukkan apa yang tertunda, sedang berlangsung, atau selesai.

* Tekan `Ctrl+T` untuk mengalihkan tampilan daftar tugas. Tampilan menampilkan hingga 10 tugas sekaligus
* Untuk melihat semua tugas atau menghapusnya, minta Claude secara langsung: "show me all tasks" atau "clear all tasks"
* Tugas bertahan di seluruh pemadatan konteks, membantu Claude tetap terorganisir pada proyek yang lebih besar
* Untuk berbagi daftar tugas di seluruh sesi, atur `CLAUDE_CODE_TASK_LIST_ID` untuk menggunakan direktori bernama di `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`

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
* [Checkpointing](/id/checkpointing) - Putar ulang pengeditan Claude dan kembalikan status sebelumnya
* [Referensi CLI](/id/cli-reference) - Bendera dan opsi baris perintah
* [Pengaturan](/id/settings) - Opsi konfigurasi
* [Manajemen memori](/id/memory) - Mengelola file CLAUDE.md
