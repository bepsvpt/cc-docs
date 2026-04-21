> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Gunakan Claude Code Desktop

> Dapatkan lebih banyak dari Claude Code Desktop: sesi paralel dengan isolasi Git, tata letak pane drag-and-drop, terminal terintegrasi dan editor file, side chats, computer use, Dispatch sessions dari ponsel Anda, tinjauan diff visual, pratinjau aplikasi, pemantauan PR, konektor, dan konfigurasi enterprise.

Tab Code dalam aplikasi Claude Desktop memungkinkan Anda menggunakan Claude Code melalui antarmuka grafis alih-alih terminal.

<CardGroup cols={2}>
  <Card title="Download for macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
    Universal build for Intel and Apple Silicon
  </Card>

  <Card title="Download for Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs">
    For x64 processors
  </Card>
</CardGroup>

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). Linux is not supported.

Setelah menginstal, luncurkan Claude, masuk, dan klik tab **Code**. Lihat [panduan Memulai](/id/desktop-quickstart) untuk panduan lengkap sesi pertama Anda.

Desktop menambahkan kemampuan ini di atas pengalaman Claude Code standar:

* [Sesi paralel](#work-in-parallel-with-sessions) dengan isolasi Git worktree otomatis
* [Tata letak drag-and-drop](#arrange-your-workspace) dengan terminal terintegrasi, editor file, dan pane pratinjau
* [Side chats](#ask-a-side-question-without-derailing-the-session) yang bercabang tanpa mempengaruhi thread utama
* [Tinjauan diff visual](#review-changes-with-diff-view) dengan komentar inline
* [Pratinjau aplikasi langsung](#preview-your-app) dengan dev server, file HTML, dan PDF
* [Computer use](#let-claude-use-your-computer) untuk membuka aplikasi dan mengontrol layar Anda di macOS dan Windows
* [Pemantauan PR GitHub](#monitor-pull-request-status) dengan auto-fix, auto-merge, dan auto-archive
* [Dispatch](#sessions-from-dispatch) integration: kirim tugas dari ponsel Anda, dapatkan sesi di sini
* [Tugas terjadwal](/id/desktop-scheduled-tasks) yang menjalankan Claude sesuai jadwal berulang
* [Konektor](#connect-external-tools) untuk GitHub, Slack, Linear, dan lainnya
* Lingkungan lokal, [SSH](#ssh-sessions), dan [cloud](#run-long-running-tasks-remotely)

<Note>
  Tata letak workspace, terminal, editor file, side chats, dan mode tampilan yang dijelaskan di halaman ini memerlukan Claude Desktop v1.2581.0 atau lebih baru. Buka **Claude → Check for Updates** di macOS atau **Help → Check for Updates** di Windows untuk memperbarui.
</Note>

Halaman ini mencakup [bekerja dengan kode](#work-with-code), [mengatur workspace Anda](#arrange-your-workspace), [computer use](#let-claude-use-your-computer), [mengelola sesi](#manage-sessions), [memperluas Claude Code](#extend-claude-code), dan [konfigurasi](#environment-configuration). Halaman ini juga mencakup [perbandingan CLI](#coming-from-the-cli) dan [pemecahan masalah](#troubleshooting).

## Mulai sesi

Sebelum Anda mengirim pesan pertama, konfigurasikan empat hal di area prompt:

* **Environment**: pilih di mana Claude berjalan. Pilih **Local** untuk mesin Anda, **Remote** untuk sesi cloud yang dihosting Anthropic, atau [**koneksi SSH**](#ssh-sessions) untuk mesin jarak jauh yang Anda kelola. Lihat [konfigurasi lingkungan](#environment-configuration).
* **Project folder**: pilih folder atau repositori tempat Claude bekerja. Untuk sesi jarak jauh, Anda dapat menambahkan [beberapa repositori](#run-long-running-tasks-remotely).
* **Model**: pilih [model](/id/model-config#available-models) dari dropdown di sebelah tombol kirim. Anda dapat mengubah ini selama sesi.
* **Permission mode**: pilih berapa banyak otonomi yang dimiliki Claude dari [pemilih mode](#choose-a-permission-mode). Anda dapat mengubah ini selama sesi.

Ketik tugas Anda dan tekan **Enter** untuk memulai. Setiap sesi melacak konteksnya sendiri dan perubahan secara independen.

## Bekerja dengan kode

Berikan Claude konteks yang tepat, kontrol berapa banyak yang dilakukannya sendiri, dan tinjau apa yang diubahnya.

### Gunakan kotak prompt

Ketik apa yang ingin Anda lakukan Claude dan tekan **Enter** untuk mengirim. Claude membaca file proyek Anda, membuat perubahan, dan menjalankan perintah berdasarkan [permission mode](#choose-a-permission-mode) Anda. Anda dapat menghentikan Claude kapan saja: klik tombol stop atau ketik koreksi Anda dan tekan **Enter**. Claude berhenti melakukan apa yang sedang dilakukannya dan menyesuaikan berdasarkan input Anda.

Tombol **+** di sebelah kotak prompt memberi Anda akses ke lampiran file, [skills](#use-skills), [konektor](#connect-external-tools), dan [plugins](#install-plugins).

### Tambahkan file dan konteks ke prompt

Kotak prompt mendukung dua cara untuk membawa konteks eksternal:

* **@mention files**: ketik `@` diikuti dengan nama file untuk menambahkan file ke konteks percakapan. Claude kemudian dapat membaca dan mereferensikan file tersebut. @mention tidak tersedia di sesi jarak jauh.
* **Attach files**: lampirkan gambar, PDF, dan file lainnya ke prompt Anda menggunakan tombol lampiran, atau seret dan lepas file langsung ke prompt. Ini berguna untuk berbagi tangkapan layar bug, mockup desain, atau dokumen referensi.

### Pilih permission mode

Permission modes mengontrol berapa banyak otonomi yang dimiliki Claude selama sesi: apakah itu meminta izin sebelum mengedit file, menjalankan perintah, atau keduanya. Anda dapat beralih mode kapan saja menggunakan pemilih mode di sebelah tombol kirim. Mulai dengan Ask permissions untuk melihat dengan tepat apa yang dilakukan Claude, kemudian pindah ke Auto accept edits atau Plan mode saat Anda merasa nyaman.

| Mode                   | Settings key        | Behavior                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ask permissions**    | `default`           | Claude meminta izin sebelum mengedit file atau menjalankan perintah. Anda melihat diff dan dapat menerima atau menolak setiap perubahan. Direkomendasikan untuk pengguna baru.                                                                                                                                                                                                                                                                                                                                       |
| **Auto accept edits**  | `acceptEdits`       | Claude secara otomatis menerima edit file dan perintah filesystem umum seperti `mkdir`, `touch`, dan `mv`, tetapi masih meminta izin sebelum menjalankan perintah terminal lainnya. Gunakan ini ketika Anda mempercayai perubahan file dan menginginkan iterasi yang lebih cepat.                                                                                                                                                                                                                                    |
| **Plan mode**          | `plan`              | Claude membaca file dan menjalankan perintah untuk menjelajahi, kemudian mengusulkan rencana tanpa mengedit kode sumber Anda. Bagus untuk tugas kompleks di mana Anda ingin meninjau pendekatan terlebih dahulu.                                                                                                                                                                                                                                                                                                     |
| **Auto**               | `auto`              | Claude mengeksekusi semua tindakan dengan pemeriksaan keamanan latar belakang yang memverifikasi keselarasan dengan permintaan Anda. Mengurangi prompt izin sambil mempertahankan pengawasan. Saat ini pratinjau penelitian. Tersedia di rencana Max, Team, Enterprise, dan API. Memerlukan Claude Sonnet 4.6, Opus 4.6, atau Opus 4.7 di rencana Team, Enterprise, dan API; Claude Opus 4.7 saja di rencana Max. Tidak tersedia di rencana Pro atau penyedia pihak ketiga. Aktifkan di Settings → Claude Code Anda. |
| **Bypass permissions** | `bypassPermissions` | Claude berjalan tanpa prompt izin apa pun, setara dengan `--dangerously-skip-permissions` di CLI. Aktifkan di Settings → Claude Code Anda di bawah "Allow bypass permissions mode". Hanya gunakan ini di kontainer atau VM yang disandbox. Admin enterprise dapat menonaktifkan opsi ini.                                                                                                                                                                                                                            |

Mode izin `dontAsk` hanya tersedia di [CLI](/id/permission-modes#allow-only-pre-approved-tools-with-dontask-mode).

<Tip title="Best practice">
  Mulai tugas kompleks di Plan mode sehingga Claude memetakan pendekatan sebelum membuat perubahan. Setelah Anda menyetujui rencana, beralih ke Auto accept edits atau Ask permissions untuk menjalankannya. Lihat [explore first, then plan, then code](/id/best-practices#explore-first-then-plan-then-code) untuk informasi lebih lanjut tentang alur kerja ini.
</Tip>

Sesi jarak jauh mendukung Auto accept edits dan Plan mode. Ask permissions tidak tersedia karena sesi jarak jauh secara otomatis menerima edit file secara default, dan Bypass permissions tidak tersedia karena lingkungan jarak jauh sudah disandbox.

Admin enterprise dapat membatasi permission modes mana yang tersedia. Lihat [enterprise configuration](#enterprise-configuration) untuk detail.

### Pratinjau aplikasi Anda

Claude dapat memulai dev server dan membuka browser tertanam untuk memverifikasi perubahannya. Ini berfungsi untuk aplikasi web frontend serta server backend: Claude dapat menguji endpoint API, melihat log server, dan mengulangi masalah yang ditemukannya. Dalam kebanyakan kasus, Claude memulai server secara otomatis setelah mengedit file proyek. Anda juga dapat meminta Claude untuk pratinjau kapan saja. Secara default, Claude [auto-verifies](#auto-verify-changes) perubahan setelah setiap edit.

Pane pratinjau juga dapat membuka file HTML statis, PDF, dan gambar dari proyek Anda. Klik path HTML, PDF, atau gambar di chat untuk membukanya di pratinjau.

Dari pane pratinjau, Anda dapat:

* Berinteraksi dengan aplikasi yang sedang berjalan langsung di browser tertanam
* Tonton Claude memverifikasi perubahannya sendiri secara otomatis: mengambil tangkapan layar, memeriksa DOM, mengklik elemen, mengisi formulir, dan memperbaiki masalah yang ditemukannya
* Mulai atau hentikan server dari dropdown **Preview** di toolbar sesi
* Pertahankan cookie dan penyimpanan lokal di seluruh restart server dengan memilih **Persist sessions** di dropdown, sehingga Anda tidak perlu masuk kembali selama pengembangan
* Edit konfigurasi server atau hentikan semua server sekaligus

Claude membuat konfigurasi server awal berdasarkan proyek Anda. Jika aplikasi Anda menggunakan perintah dev kustom, edit `.claude/launch.json` agar sesuai dengan setup Anda. Lihat [Configure preview servers](#configure-preview-servers) untuk referensi lengkap.

Untuk menghapus data sesi yang disimpan, alihkan **Persist preview sessions** di Settings → Claude Code. Untuk menonaktifkan pratinjau sepenuhnya, alihkan **Preview** di Settings → Claude Code.

### Tinjau perubahan dengan diff view

Setelah Claude membuat perubahan pada kode Anda, diff view memungkinkan Anda meninjau modifikasi file demi file sebelum membuat pull request.

Ketika Claude mengubah file, indikator statistik diff muncul menunjukkan jumlah baris yang ditambahkan dan dihapus, seperti `+12 -1`. Klik indikator ini untuk membuka diff viewer, yang menampilkan daftar file di sebelah kiri dan perubahan untuk setiap file di sebelah kanan.

Untuk mengomentari baris tertentu, klik baris apa pun di diff untuk membuka kotak komentar. Ketik umpan balik Anda dan tekan **Enter** untuk menambahkan komentar. Setelah menambahkan komentar ke beberapa baris, kirimkan semua komentar sekaligus:

* **macOS**: tekan **Cmd+Enter**
* **Windows**: tekan **Ctrl+Enter**

Claude membaca komentar Anda dan membuat perubahan yang diminta, yang muncul sebagai diff baru yang dapat Anda tinjau.

### Tinjau kode Anda

Di diff view, klik **Review code** di toolbar kanan atas untuk meminta Claude mengevaluasi perubahan sebelum Anda melakukan commit. Claude memeriksa diff saat ini dan meninggalkan komentar langsung di diff view. Anda dapat merespons komentar apa pun atau meminta Claude untuk merevisi.

Tinjauan berfokus pada masalah sinyal tinggi: kesalahan kompilasi, kesalahan logika pasti, kerentanan keamanan, dan bug yang jelas. Ini tidak menandai gaya, pemformatan, masalah yang sudah ada sebelumnya, atau apa pun yang akan ditangkap linter.

### Pantau status pull request

Setelah Anda membuka pull request, bilah status CI muncul di sesi. Claude Code menggunakan GitHub CLI untuk menanyakan hasil pemeriksaan dan menampilkan kegagalan.

* **Auto-fix**: ketika diaktifkan, Claude secara otomatis mencoba memperbaiki pemeriksaan CI yang gagal dengan membaca output kegagalan dan mengulangi.
* **Auto-merge**: ketika diaktifkan, Claude menggabungkan PR setelah semua pemeriksaan lulus. Metode penggabungan adalah squash. Auto-merge harus [diaktifkan di pengaturan repositori GitHub Anda](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) agar ini berfungsi.

Gunakan toggle **Auto-fix** dan **Auto-merge** di bilah status CI untuk mengaktifkan salah satu opsi. Claude Code juga mengirim notifikasi desktop ketika CI selesai. Untuk mengarsipkan sesi secara otomatis setelah PR digabungkan atau ditutup, aktifkan [auto-archive](#work-in-parallel-with-sessions) di Settings → Claude Code.

<Note>
  Pemantauan PR memerlukan [GitHub CLI (`gh`)](https://cli.github.com/) untuk diinstal dan diautentikasi di mesin Anda. Jika `gh` tidak diinstal, Desktop akan meminta Anda untuk memasangnya saat pertama kali Anda mencoba membuat PR.
</Note>

## Atur workspace Anda

Aplikasi desktop dibangun di sekitar pane yang dapat Anda atur dalam tata letak apa pun: chat, diff, preview, terminal, file, plan, tasks, dan subagent. Seret pane dengan headernya untuk memposisikan ulang, atau seret tepi pane untuk mengubah ukurannya. Tekan **Cmd+\\** di macOS atau **Ctrl+\\** di Windows untuk menutup pane yang fokus. Buka pane tambahan dari menu **Views** di toolbar sesi.

### Jalankan perintah di terminal

Terminal terintegrasi memungkinkan Anda menjalankan perintah bersama sesi Anda tanpa beralih ke aplikasi lain. Buka dari menu **Views** atau tekan **Ctrl+\`** di macOS atau Windows. Terminal terbuka di direktori kerja sesi Anda dan berbagi lingkungan yang sama dengan Claude, jadi perintah seperti `npm test` atau `git status` melihat file yang sama yang sedang diedit Claude. Terminal hanya tersedia di sesi lokal.

### Buka dan edit file

Klik path file di chat atau diff viewer untuk membukanya di pane file. Path HTML, PDF, dan gambar terbuka di [pane pratinjau](#preview-your-app) sebagai gantinya. Buat edit spot dan klik **Save** untuk menulisnya kembali. Jika file berubah di disk sejak Anda membukanya, pane memperingatkan Anda dan memungkinkan Anda menimpa atau membuang. Klik **Discard** untuk mengembalikan edit Anda, atau klik path di header pane untuk menyalin path absolut.

Pane file tersedia di sesi lokal dan SSH. Untuk sesi jarak jauh, minta Claude untuk membuat perubahan.

### Buka file di aplikasi lain

Klik kanan path file apa pun di chat, diff viewer, atau pane file untuk membuka menu konteks:

* **Attach as context**: tambahkan file ke prompt berikutnya Anda
* **Open in**: buka file di editor yang diinstal seperti VS Code, Cursor, atau Zed
* **Show in Finder** di macOS, **Show in Explorer** di Windows: buka folder yang berisi
* **Copy path**: salin path absolut ke clipboard Anda

### Alihkan view modes

View modes mengontrol berapa banyak detail yang muncul di transkrip chat. Alihkan mode dari dropdown **Transcript view** di sebelah tombol kirim, atau tekan **Ctrl+O** di macOS atau Windows untuk bersiklus melaluinya.

| Mode        | Apa yang ditampilkan                                                   |
| ----------- | ---------------------------------------------------------------------- |
| **Normal**  | Tool calls yang diciutkan menjadi ringkasan, dengan respons teks penuh |
| **Verbose** | Setiap tool call, file read, dan langkah perantara yang diambil Claude |
| **Summary** | Hanya respons final Claude dan perubahan yang dibuatnya                |

Gunakan Verbose saat men-debug mengapa Claude mengambil tindakan tertentu. Gunakan Summary ketika Anda menjalankan beberapa sesi dan ingin memindai hasil dengan cepat.

### Keyboard shortcuts

Tekan **Cmd+/** di macOS atau **Ctrl+/** di Windows untuk melihat semua pintasan keyboard yang tersedia di tab Code. Di Windows, gunakan **Ctrl** sebagai pengganti **Cmd** untuk pintasan di bawah. Siklus sesi, toggle terminal, dan toggle view-mode menggunakan **Ctrl** di setiap platform.

| Shortcut                              | Action                          |
| ------------------------------------- | ------------------------------- |
| `Cmd` `/`                             | Tampilkan pintasan keyboard     |
| `Cmd` `N`                             | Sesi baru                       |
| `Cmd` `W`                             | Tutup sesi                      |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab`   | Sesi berikutnya atau sebelumnya |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Sesi berikutnya atau sebelumnya |
| `Esc`                                 | Hentikan respons Claude         |
| `Cmd` `Shift` `D`                     | Alihkan pane diff               |
| `Cmd` `Shift` `P`                     | Alihkan pane pratinjau          |
| `Cmd` `Shift` `S`                     | Pilih elemen di pratinjau       |
| `Ctrl` `` ` ``                        | Alihkan pane terminal           |
| `Cmd` `\`                             | Tutup pane yang fokus           |
| `Cmd` `;`                             | Buka side chat                  |
| `Ctrl` `O`                            | Siklus view modes               |
| `Cmd` `Shift` `M`                     | Buka menu permission mode       |
| `Cmd` `Shift` `I`                     | Buka menu model                 |
| `Cmd` `Shift` `E`                     | Buka menu effort                |
| `1`–`9`                               | Pilih item di menu terbuka      |

Pintasan ini hanya berlaku untuk tab Code. Pintasan [interactive mode](/id/interactive-mode#keyboard-shortcuts) berbasis terminal, seperti `Shift+Tab` untuk siklus mode, tidak berlaku di Desktop.

### Periksa penggunaan

Klik cincin penggunaan di sebelah pemilih model untuk melihat penggunaan jendela konteks saat ini Anda dan penggunaan rencana Anda untuk periode tersebut. Penggunaan konteks per sesi; penggunaan rencana dibagikan di semua permukaan Claude Code Anda.

## Biarkan Claude menggunakan komputer Anda

Computer use memungkinkan Claude membuka aplikasi Anda, mengontrol layar Anda, dan bekerja langsung di mesin Anda seperti yang Anda lakukan. Minta Claude untuk menguji aplikasi native di mobile simulator, berinteraksi dengan alat desktop yang tidak memiliki CLI, atau mengotomatisasi sesuatu yang hanya berfungsi melalui GUI.

<Note>
  Computer use adalah pratinjau penelitian di macOS dan Windows yang memerlukan rencana Pro atau Max. Ini tidak tersedia di rencana Team atau Enterprise. Aplikasi Claude Desktop harus berjalan.
</Note>

Computer use dimatikan secara default. [Aktifkan di Settings](#enable-computer-use) sebelum Claude dapat mengontrol layar Anda. Di macOS, Anda juga perlu memberikan izin Accessibility dan Screen Recording.

<Warning>
  Tidak seperti [alat Bash yang disandbox](/id/sandboxing), computer use berjalan di desktop aktual Anda dengan akses ke apa pun yang Anda setujui. Claude memeriksa setiap tindakan dan menandai potensi prompt injection dari konten di layar, tetapi batas kepercayaan berbeda. Lihat [panduan keamanan computer use](https://support.claude.com/en/articles/14128542) untuk praktik terbaik.
</Warning>

### Kapan computer use berlaku

Claude memiliki beberapa cara untuk berinteraksi dengan aplikasi atau layanan, dan computer use adalah yang paling luas dan paling lambat. Ini mencoba alat yang paling presisi terlebih dahulu:

* Jika Anda memiliki [konektor](#connect-external-tools) untuk layanan, Claude menggunakan konektor.
* Jika tugas adalah perintah shell, Claude menggunakan Bash.
* Jika tugas adalah pekerjaan browser dan Anda memiliki [Claude di Chrome](/id/chrome) yang disiapkan, Claude menggunakan itu.
* Jika tidak ada yang berlaku, Claude menggunakan computer use.

[Per-app access tiers](#app-permissions) memperkuat ini: browser dibatasi hanya tampilan, dan terminal serta IDE dibatasi hanya klik, mengarahkan Claude ke alat khusus bahkan ketika computer use aktif. Kontrol layar dicadangkan untuk hal-hal yang tidak dapat dijangkau oleh yang lain, seperti aplikasi native, panel kontrol perangkat keras, mobile simulator, atau alat proprietary tanpa API.

### Aktifkan computer use

Computer use dimatikan secara default. Jika Anda meminta Claude melakukan sesuatu yang membutuhkannya saat dimatikan, Claude memberi tahu Anda bahwa itu dapat melakukan tugas jika Anda mengaktifkan computer use di Settings.

<Steps>
  <Step title="Perbarui aplikasi desktop">
    Pastikan Anda memiliki versi terbaru Claude Desktop. Unduh atau perbarui di [claude.com/download](https://claude.com/download), kemudian mulai ulang aplikasi.
  </Step>

  <Step title="Aktifkan toggle">
    Di aplikasi desktop, buka **Settings > General** (di bawah **Desktop app**). Temukan toggle **Computer use** dan aktifkan. Di Windows, toggle berlaku segera dan setup selesai. Di macOS, lanjutkan ke langkah berikutnya.

    Jika Anda tidak melihat toggle, konfirmasi Anda menggunakan macOS atau Windows dengan rencana Pro atau Max, kemudian perbarui dan mulai ulang aplikasi.
  </Step>

  <Step title="Berikan izin macOS">
    Di macOS, berikan dua izin sistem sebelum toggle berlaku:

    * **Accessibility**: memungkinkan Claude mengklik, mengetik, dan menggulir
    * **Screen Recording**: memungkinkan Claude melihat apa yang ada di layar Anda

    Halaman Settings menunjukkan status saat ini dari setiap izin. Jika salah satu ditolak, klik badge untuk membuka pane System Settings yang relevan.
  </Step>
</Steps>

### App permissions

Pertama kali Claude perlu menggunakan aplikasi, prompt muncul di sesi Anda. Klik **Allow for this session** atau **Deny**. Persetujuan berlaku untuk sesi saat ini, atau 30 menit di [sesi yang dispawn Dispatch](#sessions-from-dispatch).

Prompt juga menunjukkan tingkat kontrol apa yang diperoleh Claude untuk aplikasi itu. Tingkat ini diperbaiki berdasarkan kategori aplikasi dan tidak dapat diubah:

| Tier         | Apa yang dapat dilakukan Claude                                          | Berlaku untuk                 |
| :----------- | :----------------------------------------------------------------------- | :---------------------------- |
| View only    | Lihat aplikasi di tangkapan layar                                        | Browser, platform perdagangan |
| Click only   | Klik dan gulir, tetapi tidak mengetik atau menggunakan pintasan keyboard | Terminal, IDE                 |
| Full control | Klik, ketik, seret, dan gunakan pintasan keyboard                        | Semuanya yang lain            |

Aplikasi dengan jangkauan luas seperti terminal, Finder atau File Explorer, dan System Settings atau Settings menampilkan peringatan tambahan di prompt sehingga Anda tahu apa yang disetujui.

Anda dapat mengonfigurasi dua pengaturan di **Settings > General** (di bawah **Desktop app**):

* **Denied apps**: tambahkan aplikasi di sini untuk menolaknya tanpa meminta. Claude mungkin masih mempengaruhi aplikasi yang ditolak secara tidak langsung melalui tindakan di aplikasi yang diizinkan, tetapi tidak dapat berinteraksi dengan aplikasi yang ditolak secara langsung.
* **Unhide apps when Claude finishes**: saat Claude bekerja, jendela lain Anda disembunyikan sehingga hanya berinteraksi dengan aplikasi yang disetujui. Ketika Claude selesai, jendela yang disembunyikan dipulihkan kecuali Anda mematikan pengaturan ini.

## Kelola sesi

Setiap sesi adalah percakapan independen dengan konteks dan perubahannya sendiri. Anda dapat menjalankan beberapa sesi secara paralel, mengirim pekerjaan ke cloud, atau membiarkan Dispatch memulai sesi untuk Anda dari ponsel Anda.

### Bekerja secara paralel dengan sesi

Klik **+ New session** di sidebar, atau tekan **Cmd+N** di macOS atau **Ctrl+N** di Windows, untuk bekerja pada beberapa tugas secara paralel. Tekan **Ctrl+Tab** dan **Ctrl+Shift+Tab** untuk bersiklus melalui sesi di sidebar. Untuk repositori Git, setiap sesi mendapatkan salinan proyek Anda yang terisolasi menggunakan [Git worktrees](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), sehingga perubahan dalam satu sesi tidak mempengaruhi sesi lain sampai Anda melakukan commit.

Worktrees disimpan di `<project-root>/.claude/worktrees/` secara default. Anda dapat mengubah ini ke direktori kustom di Settings → Claude Code di bawah "Worktree location". Anda juga dapat mengatur awalan cabang yang ditambahkan ke setiap nama cabang worktree, yang berguna untuk menjaga cabang yang dibuat Claude tetap terorganisir. Untuk menghapus worktree ketika selesai, arahkan ke sesi di sidebar dan klik ikon archive. Untuk memiliki sesi mengarsipkan diri mereka sendiri ketika pull request mereka digabungkan atau ditutup, aktifkan **Auto-archive after PR merge or close** di Settings → Claude Code. Auto-archive hanya berlaku untuk sesi lokal yang telah selesai berjalan.

Untuk menyertakan file yang diabaikan git seperti `.env` di worktree baru, buat file [`.worktreeinclude`](/id/common-workflows#copy-gitignored-files-to-worktrees) di root proyek Anda.

<Note>
  Isolasi sesi memerlukan [Git](https://git-scm.com/downloads). Sebagian besar Mac menyertakan Git secara default. Jalankan `git --version` di Terminal untuk memeriksa. Di Windows, Git diperlukan agar tab Code berfungsi: [unduh Git untuk Windows](https://git-scm.com/downloads/win), pasang, dan mulai ulang aplikasi. Jika Anda mengalami kesalahan Git, coba sesi Cowork untuk membantu memecahkan masalah setup Anda.
</Note>

Gunakan kontrol di bagian atas sidebar untuk memfilter sesi berdasarkan status, proyek, atau lingkungan, dan untuk mengelompokkan sesi berdasarkan proyek. Untuk mengganti nama sesi, klik judul sesi di toolbar di bagian atas sesi aktif. Untuk memeriksa penggunaan konteks, lihat [Check usage](#check-usage). Ketika konteks penuh, Claude secara otomatis merangkum percakapan dan terus bekerja. Anda juga dapat mengetik `/compact` untuk memicu perangkuman lebih awal dan membebaskan ruang konteks. Lihat [jendela konteks](/id/how-claude-code-works#the-context-window) untuk detail tentang cara pemadatan bekerja.

### Tanyakan pertanyaan sampingan tanpa menggoyahkan sesi

Side chat memungkinkan Anda mengajukan pertanyaan kepada Claude yang menggunakan konteks sesi Anda tetapi tidak menambahkan apa pun kembali ke percakapan utama. Gunakan ketika Anda ingin memahami sepotong kode, memeriksa asumsi, atau menjelajahi ide tanpa mengarahkan sesi ke arah yang berbeda.

Tekan **Cmd+;** di macOS atau **Ctrl+;** di Windows untuk membuka side chat, atau ketik `/btw` di kotak prompt. Side chat dapat membaca semuanya di thread utama hingga titik itu. Ketika selesai, tutup side chat dan lanjutkan sesi utama di mana Anda tinggalkan. Side chats tersedia di sesi lokal dan SSH.

### Tonton background tasks

Pane tasks menunjukkan pekerjaan latar belakang yang berjalan di dalam sesi saat ini: subagent, perintah shell latar belakang, dan workflow. Buka dari menu **Views** atau seret ke dalam tata letak Anda.

Klik entri apa pun untuk melihat outputnya di pane subagent atau hentikan. Untuk melihat apa yang dilakukan sesi lain, gunakan [sidebar](#work-in-parallel-with-sessions).

### Jalankan tugas jangka panjang dari jarak jauh

Untuk refaktor besar, suite pengujian, migrasi, atau tugas jangka panjang lainnya, pilih **Remote** alih-alih **Local** saat memulai sesi. Sesi jarak jauh berjalan pada infrastruktur cloud Anthropic dan terus berjalan bahkan jika Anda menutup aplikasi atau mematikan komputer. Periksa kembali kapan saja untuk melihat kemajuan atau mengarahkan Claude ke arah yang berbeda. Anda juga dapat memantau sesi jarak jauh dari [claude.ai/code](https://claude.ai/code) atau aplikasi Claude iOS.

Sesi jarak jauh juga mendukung beberapa repositori. Setelah memilih lingkungan cloud, klik tombol **+** di sebelah pil repo untuk menambahkan repositori tambahan ke sesi. Setiap repo mendapatkan pemilih cabang sendiri. Ini berguna untuk tugas yang mencakup beberapa basis kode, seperti memperbarui perpustakaan bersama dan konsumennya.

Lihat [Claude Code di web](/id/claude-code-on-the-web) untuk informasi lebih lanjut tentang cara kerja sesi jarak jauh.

### Lanjutkan di permukaan lain

Menu **Continue in**, dapat diakses dari ikon VS Code di kanan bawah toolbar sesi, memungkinkan Anda memindahkan sesi ke permukaan lain:

* **Claude Code on the Web**: mengirim sesi lokal Anda untuk terus berjalan dari jarak jauh. Desktop mendorong cabang Anda, menghasilkan ringkasan percakapan, dan membuat sesi jarak jauh baru dengan konteks lengkap. Anda kemudian dapat memilih untuk mengarsipkan sesi lokal atau menyimpannya. Ini memerlukan pohon kerja yang bersih, dan tidak tersedia untuk sesi SSH.
* **Your IDE**: membuka proyek Anda di IDE yang didukung di direktori kerja saat ini.

### Sesi dari Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) adalah percakapan persisten dengan Claude yang tinggal di tab [Cowork](https://claude.com/product/cowork#dispatch-and-computer-use). Anda mengirim pesan Dispatch dengan tugas, dan itu memutuskan cara menanganinya.

Tugas dapat berakhir sebagai sesi Code dengan dua cara: Anda meminta satu secara langsung, seperti "buka sesi Claude Code dan perbaiki bug login", atau Dispatch memutuskan tugas adalah pekerjaan pengembangan dan menspawn satu sendiri. Tugas yang biasanya diarahkan ke Code termasuk memperbaiki bug, memperbarui dependensi, menjalankan tes, atau membuka pull request. Penelitian, pengeditan dokumen, dan pekerjaan spreadsheet tetap di Cowork.

Bagaimanapun, sesi Code muncul di sidebar tab Code dengan badge **Dispatch**. Anda mendapatkan notifikasi push di ponsel Anda ketika selesai atau memerlukan persetujuan Anda.

Jika Anda memiliki [computer use](#let-claude-use-your-computer) diaktifkan, sesi Code yang dispawn Dispatch juga dapat menggunakannya. Persetujuan aplikasi di sesi tersebut kedaluwarsa setelah 30 menit dan meminta kembali, daripada berlangsung untuk sesi penuh seperti sesi Code biasa.

Untuk setup, pairing, dan pengaturan Dispatch, lihat [artikel bantuan Dispatch](https://support.claude.com/en/articles/13947068). Dispatch memerlukan rencana Pro atau Max dan tidak tersedia di rencana Team atau Enterprise.

Dispatch adalah salah satu dari beberapa cara untuk bekerja dengan Claude ketika Anda jauh dari terminal Anda. Lihat [Platforms and integrations](/id/platforms#work-when-you-are-away-from-your-terminal) untuk membandingkannya dengan Remote Control, Channels, Slack, dan tugas terjadwal.

## Perluas Claude Code

Hubungkan layanan eksternal, tambahkan alur kerja yang dapat digunakan kembali, sesuaikan perilaku Claude, dan konfigurasikan server pratinjau.

### Hubungkan alat eksternal

Untuk sesi lokal dan [SSH](#ssh-sessions), klik tombol **+** di sebelah kotak prompt dan pilih **Connectors** untuk menambahkan integrasi seperti Google Calendar, Slack, GitHub, Linear, Notion, dan lainnya. Anda dapat menambahkan konektor sebelum atau selama sesi. Tombol **+** tidak tersedia di sesi jarak jauh, tetapi [routines](/id/routines) mengonfigurasi konektor pada waktu pembuatan routine.

Untuk mengelola atau memutuskan konektor, buka Settings → Connectors di aplikasi desktop, atau pilih **Manage connectors** dari menu Connectors di kotak prompt.

Setelah terhubung, Claude dapat membaca kalender Anda, mengirim pesan, membuat masalah, dan berinteraksi dengan alat Anda secara langsung. Anda dapat meminta Claude konektor apa yang dikonfigurasi di sesi Anda.

Konektor adalah [MCP servers](/id/mcp) dengan alur pengaturan grafis. Gunakan untuk integrasi cepat dengan layanan yang didukung. Untuk integrasi yang tidak tercantum di Connectors, tambahkan MCP servers secara manual melalui [file pengaturan](/id/mcp#installing-mcp-servers). Anda juga dapat [membuat konektor kustom](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Gunakan skills

[Skills](/id/skills) memperluas apa yang dapat dilakukan Claude. Claude memuatnya secara otomatis ketika relevan, atau Anda dapat menginvokan satu secara langsung: ketik `/` di kotak prompt atau klik tombol **+** dan pilih **Slash commands** untuk melihat apa yang tersedia. Ini mencakup [built-in commands](/id/commands), [custom skills](/id/skills#create-your-first-skill) Anda, project skills dari basis kode Anda, dan skills dari [installed plugins](/id/plugins) apa pun. Pilih satu dan itu muncul disorot di bidang input. Ketik tugas Anda setelahnya dan kirim seperti biasa.

### Instal plugins

[Plugins](/id/plugins) adalah paket yang dapat digunakan kembali yang menambahkan skills, agents, hooks, MCP servers, dan konfigurasi LSP ke Claude Code. Anda dapat memasang plugins dari aplikasi desktop tanpa menggunakan terminal.

Untuk sesi lokal dan [SSH](#ssh-sessions), klik tombol **+** di sebelah kotak prompt dan pilih **Plugins** untuk melihat plugins yang diinstal dan skills mereka. Untuk menambahkan plugin, pilih **Add plugin** dari submenu untuk membuka plugin browser, yang menampilkan plugins yang tersedia dari [marketplaces](/id/plugin-marketplaces) yang dikonfigurasi termasuk marketplace Anthropic resmi. Pilih **Manage plugins** untuk mengaktifkan, menonaktifkan, atau mencopot plugins.

Plugins dapat dibatasi pada akun pengguna Anda, proyek tertentu, atau lokal saja. Jika organisasi Anda mengelola plugins secara terpusat, plugins tersebut tersedia di sesi desktop dengan cara yang sama seperti di CLI. Plugins tidak tersedia untuk sesi jarak jauh. Untuk referensi plugin lengkap termasuk membuat plugins Anda sendiri, lihat [plugins](/id/plugins).

### Konfigurasikan server pratinjau

Claude secara otomatis mendeteksi setup dev server Anda dan menyimpan konfigurasi di `.claude/launch.json` di root folder yang Anda pilih saat memulai sesi. Preview menggunakan folder ini sebagai direktori kerjanya, jadi jika Anda memilih folder induk, subfolder dengan server dev mereka sendiri tidak akan terdeteksi secara otomatis. Untuk bekerja dengan server subfolder, mulai sesi di folder itu secara langsung atau tambahkan konfigurasi secara manual.

Untuk menyesuaikan cara server Anda dimulai, misalnya menggunakan `yarn dev` alih-alih `npm run dev` atau mengubah port, edit file secara manual atau klik **Edit configuration** di dropdown Preview untuk membukanya di editor kode Anda. File mendukung JSON dengan komentar.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Anda dapat menentukan beberapa konfigurasi untuk menjalankan server berbeda dari proyek yang sama, seperti frontend dan API. Lihat [examples](#examples) di bawah.

#### Auto-verify changes

Ketika `autoVerify` diaktifkan, Claude secara otomatis memverifikasi perubahan kode setelah mengedit file. Mengambil tangkapan layar, memeriksa kesalahan, dan mengkonfirmasi perubahan berfungsi sebelum menyelesaikan responsnya.

Auto-verify aktif secara default. Nonaktifkan per-proyek dengan menambahkan `"autoVerify": false` ke `.claude/launch.json`, atau alihkan dari menu dropdown **Preview**.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Ketika dinonaktifkan, alat pratinjau masih tersedia dan Anda dapat meminta Claude untuk memverifikasi kapan saja. Auto-verify membuatnya otomatis setelah setiap edit.

#### Configuration fields

Setiap entri dalam array `configurations` menerima bidang berikut:

| Field               | Type      | Description                                                                                                                                                                                                                                                                                              |
| ------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Pengidentifikasi unik untuk server ini                                                                                                                                                                                                                                                                   |
| `runtimeExecutable` | string    | Perintah untuk dijalankan, seperti `npm`, `yarn`, atau `node`                                                                                                                                                                                                                                            |
| `runtimeArgs`       | string\[] | Argumen yang dilewatkan ke `runtimeExecutable`, seperti `["run", "dev"]`                                                                                                                                                                                                                                 |
| `port`              | number    | Port yang didengarkan server Anda. Default ke 3000                                                                                                                                                                                                                                                       |
| `cwd`               | string    | Direktori kerja relatif terhadap root proyek Anda. Default ke root proyek. Gunakan `${workspaceFolder}` untuk mereferensikan root proyek secara eksplisit                                                                                                                                                |
| `env`               | object    | Variabel lingkungan tambahan sebagai pasangan kunci-nilai, seperti `{ "NODE_ENV": "development" }`. Jangan letakkan rahasia di sini karena file ini dilakukan commit ke repo Anda. Untuk meneruskan rahasia ke dev server Anda, aturlah di [local environment editor](#local-sessions) sebagai gantinya. |
| `autoPort`          | boolean   | Cara menangani konflik port. Lihat di bawah                                                                                                                                                                                                                                                              |
| `program`           | string    | Skrip untuk dijalankan dengan `node`. Lihat [when to use `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                                                                    |
| `args`              | string\[] | Argumen yang dilewatkan ke `program`. Hanya digunakan ketika `program` diatur                                                                                                                                                                                                                            |

##### When to use `program` vs `runtimeExecutable`

Gunakan `runtimeExecutable` dengan `runtimeArgs` untuk memulai dev server melalui package manager. Misalnya, `"runtimeExecutable": "npm"` dengan `"runtimeArgs": ["run", "dev"]` menjalankan `npm run dev`.

Gunakan `program` ketika Anda memiliki skrip mandiri yang ingin Anda jalankan dengan `node` secara langsung. Misalnya, `"program": "server.js"` menjalankan `node server.js`. Lewatkan flag tambahan dengan `args`.

#### Port conflicts

Bidang `autoPort` mengontrol apa yang terjadi ketika port pilihan Anda sudah digunakan:

* **`true`**: Claude menemukan dan menggunakan port gratis secara otomatis. Cocok untuk sebagian besar dev server.
* **`false`**: Claude gagal dengan kesalahan. Gunakan ini ketika server Anda harus menggunakan port tertentu, seperti untuk callback OAuth atau allowlist CORS.
* **Not set (default)**: Claude menanyakan apakah server memerlukan port itu, kemudian menyimpan jawaban Anda.

Ketika Claude memilih port yang berbeda, itu melewatkan port yang ditugaskan ke server Anda melalui variabel lingkungan `PORT`.

#### Examples

Konfigurasi ini menunjukkan setup umum untuk tipe proyek berbeda:

<Tabs>
  <Tab title="Next.js">
    Konfigurasi ini menjalankan aplikasi Next.js menggunakan Yarn di port 3000:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Untuk monorepo dengan server frontend dan API, tentukan beberapa konfigurasi. Frontend menggunakan `autoPort: true` sehingga memilih port gratis jika 3000 diambil, sementara server API memerlukan port 8080 dengan tepat:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Untuk menjalankan skrip Node.js secara langsung alih-alih menggunakan perintah package manager, gunakan bidang `program`:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Konfigurasi lingkungan

Lingkungan yang Anda pilih saat [memulai sesi](#start-a-session) menentukan di mana Claude mengeksekusi dan cara Anda terhubung:

* **Local**: berjalan di mesin Anda dengan akses langsung ke file Anda
* **Remote**: berjalan pada infrastruktur cloud Anthropic. Sesi terus berlanjut bahkan jika Anda menutup aplikasi.
* **SSH**: berjalan di mesin jarak jauh yang Anda hubungkan melalui SSH, seperti server Anda sendiri, cloud VM, atau dev container

### Local sessions

Aplikasi desktop tidak selalu mewarisi lingkungan shell lengkap Anda. Di macOS, ketika Anda meluncurkan aplikasi dari Dock atau Finder, itu membaca profil shell Anda, seperti `~/.zshrc` atau `~/.bashrc`, untuk mengekstrak `PATH` dan set tetap variabel Claude Code, tetapi variabel lain yang Anda ekspor di sana tidak diambil. Di Windows, aplikasi mewarisi variabel lingkungan pengguna dan sistem tetapi tidak membaca profil PowerShell.

Untuk mengatur variabel lingkungan untuk sesi lokal dan dev server di platform apa pun, buka dropdown lingkungan di kotak prompt, arahkan ke **Local**, dan klik ikon gear untuk membuka editor lingkungan lokal. Variabel yang Anda simpan di sini disimpan terenkripsi di mesin Anda dan berlaku untuk setiap sesi lokal dan server pratinjau yang Anda mulai. Anda juga dapat menambahkan variabel ke kunci `env` di file `~/.claude/settings.json` Anda, meskipun ini hanya mencapai sesi Claude dan bukan dev server. Lihat [environment variables](/id/env-vars) untuk daftar lengkap variabel yang didukung.

[Extended thinking](/id/common-workflows#use-extended-thinking-thinking-mode) diaktifkan secara default, yang meningkatkan kinerja pada tugas penalaran kompleks tetapi menggunakan token tambahan. Untuk menonaktifkan pemikiran sepenuhnya, atur `MAX_THINKING_TOKENS` ke `0` di editor lingkungan lokal. Pada model dengan [adaptive reasoning](/id/model-config#adjust-effort-level), nilai `MAX_THINKING_TOKENS` apa pun yang lain diabaikan karena adaptive reasoning mengontrol kedalaman pemikiran sebagai gantinya. Pada Opus 4.6 dan Sonnet 4.6, atur `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` ke `1` untuk menggunakan anggaran pemikiran tetap; Opus 4.7 selalu menggunakan adaptive reasoning dan tidak memiliki mode anggaran tetap.

### Remote sessions

Sesi jarak jauh terus berlanjut di latar belakang bahkan jika Anda menutup aplikasi. Penggunaan dihitung terhadap [batas rencana langganan](/id/costs) Anda tanpa biaya komputasi terpisah.

Anda dapat membuat lingkungan cloud kustom dengan tingkat akses jaringan dan variabel lingkungan yang berbeda. Pilih dropdown lingkungan saat memulai sesi jarak jauh dan pilih **Add environment**. Lihat [cloud environment](/id/claude-code-on-the-web#the-cloud-environment) untuk detail tentang mengonfigurasi akses jaringan dan variabel lingkungan.

### SSH sessions

Sesi SSH memungkinkan Anda menjalankan Claude Code di mesin jarak jauh sambil menggunakan aplikasi desktop sebagai antarmuka Anda. Ini berguna untuk bekerja dengan basis kode yang tinggal di cloud VM, dev container, atau server dengan perangkat keras atau dependensi tertentu.

Untuk menambahkan koneksi SSH, klik dropdown lingkungan sebelum memulai sesi dan pilih **+ Add SSH connection**. Dialog menanyakan:

* **Name**: label ramah untuk koneksi ini
* **SSH Host**: `user@hostname` atau host yang ditentukan di `~/.ssh/config`
* **SSH Port**: default ke 22 jika dibiarkan kosong, atau menggunakan port dari konfigurasi SSH Anda
* **Identity File**: path ke kunci pribadi Anda, seperti `~/.ssh/id_rsa`. Biarkan kosong untuk menggunakan kunci default atau konfigurasi SSH Anda.

Setelah ditambahkan, koneksi muncul di dropdown lingkungan. Pilih untuk memulai sesi di mesin itu. Claude berjalan di mesin jarak jauh dengan akses ke file dan alatnya.

Mesin jarak jauh harus menjalankan Linux atau macOS, dan Claude Code harus diinstal di atasnya. Setelah terhubung, sesi SSH mendukung permission modes, konektor, plugins, dan MCP servers.

## Enterprise configuration

Organisasi pada rencana Team atau Enterprise dapat mengelola perilaku aplikasi desktop melalui kontrol konsol admin, file pengaturan yang dikelola, dan kebijakan manajemen perangkat.

### Admin console controls

Pengaturan ini dikonfigurasi melalui [konsol pengaturan admin](https://claude.ai/admin-settings/claude-code):

* **Code in the desktop**: kontrol apakah pengguna di organisasi Anda dapat mengakses Claude Code di aplikasi desktop
* **Code in the web**: aktifkan atau nonaktifkan [web sessions](/id/claude-code-on-the-web) untuk organisasi Anda
* **Remote Control**: aktifkan atau nonaktifkan [Remote Control](/id/remote-control) untuk organisasi Anda
* **Disable Bypass permissions mode**: cegah pengguna di organisasi Anda dari mengaktifkan bypass permissions mode

### Managed settings

Pengaturan yang dikelola menimpa pengaturan proyek dan pengguna dan berlaku ketika Desktop menjalankan sesi CLI. Anda dapat mengatur kunci ini di file [managed settings](/id/settings#settings-precedence) organisasi Anda atau mendorongnya dari jarak jauh melalui konsol admin.

| Key                                        | Description                                                                                                                                                                                               |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissions.disableBypassPermissionsMode` | atur ke `"disable"` untuk mencegah pengguna dari mengaktifkan Bypass permissions mode.                                                                                                                    |
| `disableAutoMode`                          | atur ke `"disable"` untuk mencegah pengguna dari mengaktifkan [Auto](/id/permission-modes#eliminate-prompts-with-auto-mode) mode. Menghapus Auto dari pemilih mode. Juga diterima di bawah `permissions`. |
| `autoMode`                                 | sesuaikan apa yang dipercaya dan diblokir oleh pengklasifikasi auto mode di seluruh organisasi Anda. Lihat [Configure the auto mode classifier](/id/permissions#configure-the-auto-mode-classifier).      |

`permissions.disableBypassPermissionsMode` dan `disableAutoMode` juga bekerja di pengaturan pengguna dan proyek, tetapi menempatkannya di pengaturan yang dikelola mencegah pengguna dari menimpanya. `autoMode` dibaca dari pengaturan pengguna, `.claude/settings.local.json`, dan pengaturan yang dikelola, tetapi bukan dari `.claude/settings.json` yang diperiksa: repositori yang diklon tidak dapat menyuntikkan aturan pengklasifikasinya sendiri. Untuk daftar lengkap pengaturan khusus yang dikelola termasuk `allowManagedPermissionRulesOnly` dan `allowManagedHooksOnly`, lihat [managed-only settings](/id/permissions#managed-only-settings).

Pengaturan yang dikelola jarak jauh yang diunggah melalui konsol admin saat ini berlaku untuk sesi CLI dan IDE saja. Untuk pembatasan khusus Desktop, gunakan kontrol konsol admin di atas.

### Device management policies

Tim IT dapat mengelola aplikasi desktop melalui MDM di macOS atau group policy di Windows. Kebijakan yang tersedia termasuk mengaktifkan atau menonaktifkan fitur Claude Code, mengontrol auto-updates, dan menetapkan URL penyebaran kustom.

* **macOS**: konfigurasikan melalui domain preferensi `com.anthropic.Claude` menggunakan alat seperti Jamf atau Kandji
* **Windows**: konfigurasikan melalui registri di `SOFTWARE\Policies\Claude`

### Authentication and SSO

Organisasi enterprise dapat memerlukan SSO untuk semua pengguna. Lihat [authentication](/id/authentication) untuk detail tingkat rencana dan [Setting up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) untuk konfigurasi SAML dan OIDC.

### Data handling

Claude Code memproses kode Anda secara lokal dalam sesi lokal atau pada infrastruktur cloud Anthropic dalam sesi jarak jauh. Percakapan dan konteks kode dikirim ke API Anthropic untuk diproses. Lihat [data handling](/id/data-usage) untuk detail tentang retensi data, privasi, dan kepatuhan.

### Deployment

Desktop dapat didistribusikan melalui alat penyebaran enterprise:

* **macOS**: distribusikan melalui MDM seperti Jamf atau Kandji menggunakan installer `.dmg`
* **Windows**: sebarkan melalui paket MSIX atau installer `.exe`. Lihat [Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) untuk opsi penyebaran enterprise termasuk instalasi senyap

Untuk konfigurasi jaringan seperti pengaturan proxy, allowlist firewall, dan LLM gateway, lihat [network configuration](/id/network-config).

Untuk referensi konfigurasi enterprise lengkap, lihat [enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Coming from the CLI?

Jika Anda sudah menggunakan CLI Claude Code, Desktop menjalankan mesin yang sama dengan antarmuka grafis. Anda dapat menjalankan keduanya secara bersamaan di mesin yang sama, bahkan di proyek yang sama. Masing-masing mempertahankan riwayat sesi terpisah, tetapi mereka berbagi konfigurasi dan memori proyek melalui file CLAUDE.md.

Untuk memindahkan sesi CLI ke Desktop, jalankan `/desktop` di terminal. Claude menyimpan sesi Anda dan membukanya di aplikasi desktop, kemudian keluar dari CLI. Perintah ini hanya tersedia di macOS dan Windows.

<Tip>
  Kapan menggunakan Desktop vs CLI: gunakan Desktop ketika Anda ingin mengelola sesi paralel di satu jendela, mengatur pane berdampingan, atau meninjau perubahan secara visual. Gunakan CLI ketika Anda memerlukan scripting, otomasi, atau lebih suka alur kerja terminal.
</Tip>

### CLI flag equivalents

Tabel ini menunjukkan setara aplikasi desktop untuk flag CLI umum. Flag yang tidak tercantum tidak memiliki setara desktop karena dirancang untuk scripting atau otomasi.

| CLI                                   | Desktop equivalent                                                                                                                                  |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                      | Model dropdown di sebelah tombol kirim                                                                                                              |
| `--resume`, `--continue`              | Klik sesi di sidebar                                                                                                                                |
| `--permission-mode`                   | Mode selector di sebelah tombol kirim                                                                                                               |
| `--dangerously-skip-permissions`      | Bypass permissions mode. Aktifkan di Settings → Claude Code → "Allow bypass permissions mode". Admin enterprise dapat menonaktifkan pengaturan ini. |
| `--add-dir`                           | Tambahkan beberapa repo dengan tombol **+** di sesi jarak jauh                                                                                      |
| `--allowedTools`, `--disallowedTools` | Tidak tersedia di Desktop                                                                                                                           |
| `--verbose`                           | [Verbose view mode](#switch-view-modes) di dropdown Transcript view                                                                                 |
| `--print`, `--output-format`          | Tidak tersedia. Desktop hanya interaktif.                                                                                                           |
| `ANTHROPIC_MODEL` env var             | Model dropdown di sebelah tombol kirim                                                                                                              |
| `MAX_THINKING_TOKENS` env var         | Atur di editor lingkungan lokal. Lihat [environment configuration](#environment-configuration).                                                     |

### Shared configuration

Desktop dan CLI membaca file konfigurasi yang sama, jadi setup Anda terbawa:

* **[CLAUDE.md](/id/memory)** dan file `CLAUDE.local.md` di proyek Anda digunakan oleh keduanya
* **[MCP servers](/id/mcp)** yang dikonfigurasi di `~/.claude.json` atau `.mcp.json` bekerja di keduanya
* **[Hooks](/id/hooks)** dan **[skills](/id/skills)** yang ditentukan dalam pengaturan berlaku untuk keduanya
* **[Settings](/id/settings)** di `~/.claude.json` dan `~/.claude/settings.json` dibagikan. Aturan izin, alat yang diizinkan, dan pengaturan lainnya di `settings.json` berlaku untuk sesi Desktop.
* **Models**: Sonnet, Opus, dan Haiku tersedia di keduanya. Di Desktop, pilih model dari dropdown di sebelah tombol kirim. Anda dapat mengubah model selama sesi.

<Note>
  **MCP servers: desktop chat app vs Claude Code**: MCP servers yang dikonfigurasi untuk aplikasi chat Claude Desktop di `claude_desktop_config.json` terpisah dari Claude Code dan tidak akan muncul di tab Code. Untuk menggunakan MCP servers di Claude Code, konfigurasikan di `~/.claude.json` atau file `.mcp.json` proyek Anda. Lihat [MCP configuration](/id/mcp#installing-mcp-servers) untuk detail.
</Note>

### Feature comparison

Tabel ini membandingkan kemampuan inti antara CLI dan Desktop. Untuk daftar lengkap flag CLI, lihat [CLI reference](/id/cli-reference).

| Feature                                               | CLI                                                       | Desktop                                                                                                                                                                                                                        |
| ----------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Permission modes                                      | Semua mode termasuk `dontAsk`                             | Ask permissions, Auto accept edits, Plan mode, Auto, dan Bypass permissions via Settings                                                                                                                                       |
| `--dangerously-skip-permissions`                      | CLI flag                                                  | Bypass permissions mode. Aktifkan di Settings → Claude Code → "Allow bypass permissions mode"                                                                                                                                  |
| [Third-party providers](/id/third-party-integrations) | Bedrock, Vertex, Foundry                                  | Anthropic's API secara default. Enterprise deployments dapat mengonfigurasi Vertex AI dan gateway providers. Lihat [enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration). |
| [MCP servers](/id/mcp)                                | Konfigurasikan di file pengaturan                         | Connectors UI untuk sesi lokal dan SSH, atau file pengaturan                                                                                                                                                                   |
| [Plugins](/id/plugins)                                | `/plugin` command                                         | Plugin manager UI                                                                                                                                                                                                              |
| @mention files                                        | Berbasis teks                                             | Dengan autocomplete; sesi lokal dan SSH saja                                                                                                                                                                                   |
| File attachments                                      | Tidak tersedia                                            | Gambar, PDF                                                                                                                                                                                                                    |
| Session isolation                                     | [`--worktree`](/id/cli-reference) flag                    | Automatic worktrees                                                                                                                                                                                                            |
| Multiple sessions                                     | Terminal terpisah                                         | Sidebar tabs                                                                                                                                                                                                                   |
| Recurring tasks                                       | Cron jobs, CI pipelines                                   | [Scheduled tasks](/id/desktop-scheduled-tasks)                                                                                                                                                                                 |
| Computer use                                          | [Enable via `/mcp`](/id/computer-use) di macOS            | [App and screen control](#let-claude-use-your-computer) di macOS dan Windows                                                                                                                                                   |
| Dispatch integration                                  | Tidak tersedia                                            | [Dispatch sessions](#sessions-from-dispatch) di sidebar                                                                                                                                                                        |
| Scripting and automation                              | [`--print`](/id/cli-reference), [Agent SDK](/id/headless) | Tidak tersedia                                                                                                                                                                                                                 |

### What's not available in Desktop

Fitur berikut hanya tersedia di CLI atau VS Code extension:

* **Third-party providers**: Desktop terhubung ke Anthropic's API secara default. Enterprise deployments dapat mengonfigurasi Vertex AI dan gateway providers via [managed settings](https://support.claude.com/en/articles/12622667-enterprise-configuration). Untuk Bedrock atau Foundry, gunakan [CLI](/id/quickstart).
* **Linux**: aplikasi desktop hanya tersedia di macOS dan Windows.
* **Inline code suggestions**: Desktop tidak menyediakan saran gaya autocomplete. Ini bekerja melalui prompt percakapan dan perubahan kode eksplisit.
* **Agent teams**: orkestrasi multi-agent tersedia melalui [CLI](/id/agent-teams) dan [Agent SDK](/id/headless), bukan di Desktop.

## Troubleshooting

Bagian di bawah mencakup masalah khusus untuk aplikasi desktop. Untuk kesalahan API runtime yang muncul di chat seperti `API Error: 500`, `529 Overloaded`, `429`, atau `Prompt is too long`, lihat [Error reference](/id/errors). Kesalahan tersebut dan perbaikannya sama di CLI, desktop, dan web.

### Check your version

Untuk melihat versi aplikasi desktop yang Anda jalankan:

* **macOS**: klik **Claude** di menu bar, kemudian **About Claude**
* **Windows**: klik **Help**, kemudian **About**

Klik nomor versi untuk menyalinnya ke clipboard Anda.

### 403 or authentication errors in the Code tab

Jika Anda melihat `Error 403: Forbidden` atau kegagalan autentikasi lainnya saat menggunakan tab Code:

1. Keluar dan masuk kembali dari menu aplikasi. Ini adalah perbaikan paling umum.
2. Verifikasi Anda memiliki langganan berbayar aktif: Pro, Max, Team, atau Enterprise.
3. Jika CLI berfungsi tetapi Desktop tidak, keluar dari aplikasi desktop sepenuhnya, bukan hanya tutup jendela, kemudian buka kembali dan masuk.
4. Periksa koneksi internet dan pengaturan proxy Anda.

### Blank or stuck screen on launch

Jika aplikasi terbuka tetapi menampilkan layar kosong atau tidak responsif:

1. Mulai ulang aplikasi.
2. Periksa pembaruan yang tertunda. Aplikasi secara otomatis memperbarui saat peluncuran.
3. Di Windows, periksa Event Viewer untuk log crash di bawah **Windows Logs → Application**.

### "Failed to load session"

Jika Anda melihat `Failed to load session`, folder yang dipilih mungkin tidak lagi ada, repositori Git mungkin memerlukan Git LFS yang tidak diinstal, atau izin file mungkin mencegah akses. Coba pilih folder berbeda atau mulai ulang aplikasi.

### Session not finding installed tools

Jika Claude tidak dapat menemukan alat seperti `npm`, `node`, atau perintah CLI lainnya, verifikasi alat bekerja di terminal biasa Anda, periksa bahwa profil shell Anda dengan benar menyiapkan PATH, dan mulai ulang aplikasi desktop untuk memuat ulang variabel lingkungan.

### Git and Git LFS errors

Di Windows, Git diperlukan agar tab Code memulai sesi lokal. Jika Anda melihat "Git is required," instal [Git for Windows](https://git-scm.com/downloads/win) dan mulai ulang aplikasi.

Jika Anda melihat "Git LFS is required by this repository but is not installed," instal Git LFS dari [git-lfs.com](https://git-lfs.com/), jalankan `git lfs install`, dan mulai ulang aplikasi.

### MCP servers not working on Windows

Jika toggle MCP server tidak merespons atau server gagal terhubung di Windows, periksa bahwa server dikonfigurasi dengan benar di pengaturan Anda, mulai ulang aplikasi, verifikasi proses server berjalan di Task Manager, dan tinjau log server untuk kesalahan koneksi.

### App won't quit

* **macOS**: tekan Cmd+Q. Jika aplikasi tidak merespons, gunakan Force Quit dengan Cmd+Option+Esc, pilih Claude, dan klik Force Quit.
* **Windows**: gunakan Task Manager dengan Ctrl+Shift+Esc untuk mengakhiri proses Claude.

### Windows-specific issues

* **PATH not updated after install**: buka jendela terminal baru. Pembaruan PATH hanya berlaku untuk sesi terminal baru.
* **Concurrent installation error**: jika Anda melihat kesalahan tentang instalasi lain sedang berlangsung tetapi tidak ada, coba jalankan installer sebagai Administrator.

### "Branch doesn't exist yet" when opening in CLI

Sesi jarak jauh dapat membuat cabang yang tidak ada di mesin lokal Anda. Klik nama cabang di toolbar sesi untuk menyalinnya, kemudian ambil secara lokal:

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Still stuck?

* Cari atau laporkan bug di [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Kunjungi [Claude support center](https://support.claude.com/)

Saat melaporkan bug, sertakan versi aplikasi desktop Anda, sistem operasi Anda, pesan kesalahan yang tepat, dan log yang relevan. Di macOS, periksa Console.app. Di Windows, periksa Event Viewer → Windows Logs → Application.
