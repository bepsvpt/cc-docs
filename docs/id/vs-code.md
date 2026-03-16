> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Gunakan Claude Code di VS Code

> Instal dan konfigurasi ekstensi Claude Code untuk VS Code. Dapatkan bantuan pengkodean AI dengan diff inline, @-mentions, review rencana, dan pintasan keyboard.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Editor VS Code dengan panel ekstensi Claude Code terbuka di sisi kanan, menampilkan percakapan dengan Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

Ekstensi VS Code menyediakan antarmuka grafis asli untuk Claude Code, terintegrasi langsung ke dalam IDE Anda. Ini adalah cara yang direkomendasikan untuk menggunakan Claude Code di VS Code.

Dengan ekstensi, Anda dapat meninjau dan mengedit rencana Claude sebelum menerimanya, auto-accept edits saat dibuat, @-mention file dengan rentang baris tertentu dari pilihan Anda, akses riwayat percakapan, dan buka beberapa percakapan di tab atau jendela terpisah.

## Prasyarat

Sebelum menginstal, pastikan Anda memiliki:

* VS Code 1.98.0 atau lebih tinggi
* Akun Anthropic (Anda akan masuk saat pertama kali membuka ekstensi). Jika Anda menggunakan penyedia pihak ketiga seperti Amazon Bedrock atau Google Vertex AI, lihat [Gunakan penyedia pihak ketiga](#use-third-party-providers) sebagai gantinya.

<Tip>
  Ekstensi mencakup CLI (command-line interface), yang dapat Anda akses dari terminal terintegrasi VS Code untuk fitur lanjutan. Lihat [Ekstensi VS Code vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) untuk detail.
</Tip>

## Instal ekstensi

Klik tautan untuk IDE Anda untuk menginstal secara langsung:

* [Instal untuk VS Code](vscode:extension/anthropic.claude-code)
* [Instal untuk Cursor](cursor:extension/anthropic.claude-code)

Atau di VS Code, tekan `Cmd+Shift+X` (Mac) atau `Ctrl+Shift+X` (Windows/Linux) untuk membuka tampilan Ekstensi, cari "Claude Code", dan klik **Instal**.

<Note>Jika ekstensi tidak muncul setelah instalasi, restart VS Code atau jalankan "Developer: Reload Window" dari Command Palette.</Note>

## Memulai

Setelah diinstal, Anda dapat mulai menggunakan Claude Code melalui antarmuka VS Code:

<Steps>
  <Step title="Buka panel Claude Code">
    Di seluruh VS Code, ikon Spark menunjukkan Claude Code: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Spark icon" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    Cara tercepat untuk membuka Claude adalah dengan mengklik ikon Spark di **Editor Toolbar** (sudut kanan atas editor). Ikon hanya muncul saat Anda memiliki file terbuka.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Editor VS Code menampilkan ikon Spark di Editor Toolbar" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Cara lain untuk membuka Claude Code:

    * **Activity Bar**: klik ikon Spark di sidebar kiri untuk membuka daftar sesi. Klik sesi apa pun untuk membukanya sebagai tab editor penuh, atau mulai yang baru. Ikon ini selalu terlihat di Activity Bar.
    * **Command Palette**: `Cmd+Shift+P` (Mac) atau `Ctrl+Shift+P` (Windows/Linux), ketik "Claude Code", dan pilih opsi seperti "Open in New Tab"
    * **Status Bar**: klik **✱ Claude Code** di sudut kanan bawah jendela. Ini berfungsi bahkan saat tidak ada file yang terbuka.

    Saat Anda pertama kali membuka panel, daftar periksa **Learn Claude Code** muncul. Kerjakan setiap item dengan mengklik **Show me**, atau tutup dengan X. Untuk membukanya kembali nanti, hapus centang **Hide Onboarding** di pengaturan VS Code di bawah Extensions → Claude Code.

    Anda dapat menyeret panel Claude untuk memposisikan ulang di mana saja di VS Code. Lihat [Sesuaikan alur kerja Anda](#customize-your-workflow) untuk detail.
  </Step>

  <Step title="Kirim prompt">
    Minta Claude untuk membantu dengan kode atau file Anda, baik itu menjelaskan cara kerja sesuatu, men-debug masalah, atau membuat perubahan.

    <Tip>Claude secara otomatis melihat teks pilihan Anda. Tekan `Option+K` (Mac) / `Alt+K` (Windows/Linux) untuk juga menyisipkan referensi @-mention (seperti `@file.ts#5-10`) ke dalam prompt Anda.</Tip>

    Berikut adalah contoh menanyakan tentang baris tertentu dalam file:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Editor VS Code dengan baris 2-3 dipilih dalam file Python, dan panel Claude Code menampilkan pertanyaan tentang baris tersebut dengan referensi @-mention" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Tinjau perubahan">
    Saat Claude ingin mengedit file, ia menampilkan perbandingan berdampingan dari perubahan asli dan yang diusulkan, kemudian meminta izin. Anda dapat menerima, menolak, atau memberi tahu Claude apa yang harus dilakukan sebagai gantinya.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code menampilkan diff dari perubahan yang diusulkan Claude dengan prompt izin menanyakan apakah akan membuat edit" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Untuk lebih banyak ide tentang apa yang dapat Anda lakukan dengan Claude Code, lihat [Alur kerja umum](/id/common-workflows).

<Tip>
  Jalankan "Claude Code: Open Walkthrough" dari Command Palette untuk tur terpandu tentang dasar-dasarnya.
</Tip>

## Gunakan kotak prompt

Kotak prompt mendukung beberapa fitur:

* **Mode izin**: klik indikator mode di bagian bawah kotak prompt untuk beralih mode. Dalam mode normal, Claude meminta izin sebelum setiap tindakan. Dalam Plan mode, Claude menjelaskan apa yang akan dilakukan dan menunggu persetujuan sebelum membuat perubahan. VS Code secara otomatis membuka rencana sebagai dokumen markdown penuh di mana Anda dapat menambahkan komentar inline untuk memberikan umpan balik sebelum Claude mulai. Dalam mode auto-accept, Claude membuat edit tanpa bertanya. Atur default di pengaturan VS Code di bawah `claudeCode.initialPermissionMode`.
* **Menu perintah**: klik `/` atau ketik `/` untuk membuka menu perintah. Opsi termasuk melampirkan file, beralih model, mengalihkan extended thinking, dan melihat penggunaan rencana (`/usage`). Bagian Customize menyediakan akses ke MCP servers, hooks, memory, permissions, dan plugins. Item dengan ikon terminal terbuka di terminal terintegrasi.
* **Indikator konteks**: kotak prompt menunjukkan berapa banyak context window Claude yang Anda gunakan. Claude secara otomatis melakukan compact saat diperlukan, atau Anda dapat menjalankan `/compact` secara manual.
* **Extended thinking**: memungkinkan Claude menghabiskan lebih banyak waktu untuk bernalar melalui masalah kompleks. Alihkan melalui menu perintah (`/`). Lihat [Extended thinking](/id/common-workflows#use-extended-thinking-thinking-mode) untuk detail.
* **Input multi-baris**: tekan `Shift+Enter` untuk menambahkan baris baru tanpa mengirim. Ini juga berfungsi di input teks bebas "Other" dari dialog pertanyaan.

### Referensikan file dan folder

Gunakan @-mentions untuk memberikan Claude konteks tentang file atau folder tertentu. Saat Anda mengetik `@` diikuti dengan nama file atau folder, Claude membaca konten tersebut dan dapat menjawab pertanyaan tentangnya atau membuat perubahan padanya. Claude Code mendukung fuzzy matching, jadi Anda dapat mengetik nama parsial untuk menemukan apa yang Anda butuhkan:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Untuk PDF besar, Anda dapat meminta Claude membaca halaman tertentu alih-alih seluruh file: satu halaman, rentang seperti halaman 1-10, atau rentang terbuka seperti halaman 3 ke depan.

Saat Anda memilih teks di editor, Claude dapat melihat kode yang disorot secara otomatis. Footer kotak prompt menunjukkan berapa banyak baris yang dipilih. Tekan `Option+K` (Mac) / `Alt+K` (Windows/Linux) untuk menyisipkan @-mention dengan jalur file dan nomor baris (misalnya, `@app.ts#5-10`). Klik indikator pilihan untuk mengalihkan apakah Claude dapat melihat teks yang disorot Anda - ikon eye-slash berarti pilihan tersembunyi dari Claude.

Anda juga dapat menahan `Shift` sambil menyeret file ke kotak prompt untuk menambahkannya sebagai lampiran. Klik X pada lampiran apa pun untuk menghapusnya dari konteks.

### Lanjutkan percakapan masa lalu

Klik dropdown di bagian atas panel Claude Code untuk mengakses riwayat percakapan Anda. Anda dapat mencari berdasarkan kata kunci atau menelusuri berdasarkan waktu (Today, Yesterday, Last 7 days, dll.). Klik percakapan apa pun untuk melanjutkannya dengan riwayat pesan lengkap. Arahkan kursor ke sesi untuk mengungkapkan tindakan rename dan remove: rename untuk memberikan judul deskriptif, atau remove untuk menghapusnya dari daftar. Untuk lebih lanjut tentang melanjutkan sesi, lihat [Alur kerja umum](/id/common-workflows#resume-previous-conversations).

### Lanjutkan sesi jarak jauh dari Claude.ai

Jika Anda menggunakan [Claude Code di web](/id/claude-code-on-the-web), Anda dapat melanjutkan sesi jarak jauh tersebut langsung di VS Code. Ini memerlukan masuk dengan **Claude.ai Subscription**, bukan Anthropic Console.

<Steps>
  <Step title="Buka Percakapan Masa Lalu">
    Klik dropdown **Past Conversations** di bagian atas panel Claude Code.
  </Step>

  <Step title="Pilih tab Remote">
    Dialog menampilkan dua tab: Local dan Remote. Klik **Remote** untuk melihat sesi dari claude.ai.
  </Step>

  <Step title="Pilih sesi untuk dilanjutkan">
    Telusuri atau cari sesi jarak jauh Anda. Klik sesi apa pun untuk mengunduhnya dan melanjutkan percakapan secara lokal.
  </Step>
</Steps>

<Note>
  Hanya sesi web yang dimulai dengan repositori GitHub yang muncul di tab Remote. Melanjutkan memuat riwayat percakapan secara lokal; perubahan tidak disinkronkan kembali ke claude.ai.
</Note>

## Sesuaikan alur kerja Anda

Setelah Anda siap dan berjalan, Anda dapat memposisikan ulang panel Claude, menjalankan beberapa sesi, atau beralih ke mode terminal.

### Pilih di mana Claude berada

Anda dapat menyeret panel Claude untuk memposisikan ulang di mana saja di VS Code. Ambil tab atau title bar panel dan seret ke:

* **Secondary sidebar**: sisi kanan jendela. Membuat Claude tetap terlihat saat Anda coding.
* **Primary sidebar**: sidebar kiri dengan ikon untuk Explorer, Search, dll.
* **Editor area**: membuka Claude sebagai tab bersama file Anda. Berguna untuk tugas sampingan.

<Tip>
  Gunakan sidebar untuk sesi Claude utama Anda dan buka tab tambahan untuk tugas sampingan. Claude mengingat lokasi pilihan Anda. Ikon daftar sesi Activity Bar terpisah dari panel Claude: daftar sesi selalu terlihat di Activity Bar, sementara ikon panel Claude hanya muncul di sana saat panel ditambatkan ke sidebar kiri.
</Tip>

### Jalankan beberapa percakapan

Gunakan **Open in New Tab** atau **Open in New Window** dari Command Palette untuk memulai percakapan tambahan. Setiap percakapan mempertahankan riwayat dan konteksnya sendiri, memungkinkan Anda bekerja pada tugas berbeda secara paralel.

Saat menggunakan tab, titik berwarna kecil pada ikon spark menunjukkan status: biru berarti permintaan izin tertunda, oranye berarti Claude selesai saat tab tersembunyi.

### Beralih ke mode terminal

Secara default, ekstensi membuka panel chat grafis. Jika Anda lebih suka antarmuka gaya CLI, buka [pengaturan Use Terminal](vscode://settings/claudeCode.useTerminal) dan centang kotak.

Anda juga dapat membuka pengaturan VS Code (`Cmd+,` di Mac atau `Ctrl+,` di Windows/Linux), buka Extensions → Claude Code, dan centang **Use Terminal**.

## Kelola plugins

Ekstensi VS Code mencakup antarmuka grafis untuk menginstal dan mengelola [plugins](/id/plugins). Ketik `/plugins` di kotak prompt untuk membuka antarmuka **Manage plugins**.

### Instal plugins

Dialog plugin menampilkan dua tab: **Plugins** dan **Marketplaces**.

Di tab Plugins:

* **Installed plugins** muncul di bagian atas dengan tombol toggle untuk mengaktifkan atau menonaktifkannya
* **Available plugins** dari marketplace yang dikonfigurasi muncul di bawah
* Cari untuk memfilter plugins berdasarkan nama atau deskripsi
* Klik **Install** pada plugin yang tersedia apa pun

Saat Anda menginstal plugin, pilih cakupan instalasi:

* **Install for you**: tersedia di semua proyek Anda (user scope)
* **Install for this project**: dibagikan dengan kolaborator proyek (project scope)
* **Install locally**: hanya untuk Anda, hanya di repositori ini (local scope)

### Kelola marketplaces

Beralih ke tab **Marketplaces** untuk menambah atau menghapus sumber plugin:

* Masukkan repo GitHub, URL, atau jalur lokal untuk menambahkan marketplace baru
* Klik ikon refresh untuk memperbarui daftar plugin marketplace
* Klik ikon trash untuk menghapus marketplace

Setelah membuat perubahan, banner meminta Anda untuk restart Claude Code untuk menerapkan pembaruan.

<Note>
  Manajemen plugin di VS Code menggunakan perintah CLI yang sama di balik layar. Plugins dan marketplaces yang Anda konfigurasi di ekstensi juga tersedia di CLI, dan sebaliknya.
</Note>

Untuk lebih lanjut tentang sistem plugin, lihat [Plugins](/id/plugins) dan [Plugin marketplaces](/id/plugin-marketplaces).

## Otomatisasi tugas browser dengan Chrome

Hubungkan Claude ke browser Chrome Anda untuk menguji aplikasi web, debug dengan console logs, dan otomatisasi alur kerja browser tanpa meninggalkan VS Code. Ini memerlukan ekstensi [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versi 1.0.36 atau lebih tinggi.

Ketik `@browser` di kotak prompt diikuti dengan apa yang ingin Anda lakukan Claude:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

Anda juga dapat membuka menu lampiran untuk memilih alat browser tertentu seperti membuka tab baru atau membaca konten halaman.

Claude membuka tab baru untuk tugas browser dan berbagi status login browser Anda, sehingga dapat mengakses situs apa pun yang sudah Anda masuki.

Untuk instruksi setup, daftar lengkap kemampuan, dan troubleshooting, lihat [Gunakan Claude Code dengan Chrome](/id/chrome).

## Perintah dan pintasan VS Code

Buka Command Palette (`Cmd+Shift+P` di Mac atau `Ctrl+Shift+P` di Windows/Linux) dan ketik "Claude Code" untuk melihat semua perintah VS Code yang tersedia untuk ekstensi Claude Code.

Beberapa pintasan tergantung pada panel mana yang "focused" (menerima input keyboard). Saat kursor Anda berada di file kode, editor difokuskan. Saat kursor Anda berada di kotak prompt Claude, Claude difokuskan. Gunakan `Cmd+Esc` / `Ctrl+Esc` untuk beralih di antara keduanya.

<Note>
  Ini adalah perintah VS Code untuk mengontrol ekstensi. Tidak semua perintah Claude Code bawaan tersedia di ekstensi. Lihat [Ekstensi VS Code vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) untuk detail.
</Note>

| Perintah                   | Pintasan                                                 | Deskripsi                                                                      |
| -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Alihkan fokus antara editor dan Claude                                         |
| Open in Side Bar           | -                                                        | Buka Claude di sidebar kiri                                                    |
| Open in Terminal           | -                                                        | Buka Claude dalam mode terminal                                                |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Buka percakapan baru sebagai tab editor                                        |
| Open in New Window         | -                                                        | Buka percakapan baru di jendela terpisah                                       |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Mulai percakapan baru (memerlukan Claude difokuskan)                           |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Sisipkan referensi ke file saat ini dan pilihan (memerlukan editor difokuskan) |
| Show Logs                  | -                                                        | Lihat log debug ekstensi                                                       |
| Logout                     | -                                                        | Keluar dari akun Anthropic Anda                                                |

## Konfigurasi pengaturan

Ekstensi memiliki dua jenis pengaturan:

* **Pengaturan ekstensi** di VS Code: mengontrol perilaku ekstensi dalam VS Code. Buka dengan `Cmd+,` (Mac) atau `Ctrl+,` (Windows/Linux), kemudian buka Extensions → Claude Code. Anda juga dapat mengetik `/` dan memilih **General Config** untuk membuka pengaturan.
* **Pengaturan Claude Code** di `~/.claude/settings.json`: dibagikan antara ekstensi dan CLI. Gunakan untuk perintah yang diizinkan, variabel lingkungan, hooks, dan MCP servers. Lihat [Settings](/id/settings) untuk detail.

<Tip>
  Tambahkan `"$schema": "https://json.schemastore.org/claude-code-settings.json"` ke `settings.json` Anda untuk mendapatkan autocomplete dan validasi inline untuk semua pengaturan yang tersedia langsung di VS Code.
</Tip>

### Pengaturan ekstensi

| Pengaturan                        | Default   | Deskripsi                                                                                                                |
| --------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------ |
| `selectedModel`                   | `default` | Model untuk percakapan baru. Ubah per-sesi dengan `/model`.                                                              |
| `useTerminal`                     | `false`   | Luncurkan Claude dalam mode terminal alih-alih panel grafis                                                              |
| `initialPermissionMode`           | `default` | Mengontrol prompt persetujuan: `default` (tanya setiap kali), `plan`, `acceptEdits`, atau `bypassPermissions`            |
| `preferredLocation`               | `panel`   | Di mana Claude terbuka: `sidebar` (kanan) atau `panel` (tab baru)                                                        |
| `autosave`                        | `true`    | Auto-save file sebelum Claude membaca atau menulisnya                                                                    |
| `useCtrlEnterToSend`              | `false`   | Gunakan Ctrl/Cmd+Enter alih-alih Enter untuk mengirim prompt                                                             |
| `enableNewConversationShortcut`   | `true`    | Aktifkan Cmd/Ctrl+N untuk memulai percakapan baru                                                                        |
| `hideOnboarding`                  | `false`   | Sembunyikan daftar periksa onboarding (ikon topi kelulusan)                                                              |
| `respectGitIgnore`                | `true`    | Kecualikan pola .gitignore dari pencarian file                                                                           |
| `environmentVariables`            | `[]`      | Atur variabel lingkungan untuk proses Claude. Gunakan pengaturan Claude Code sebagai gantinya untuk konfigurasi bersama. |
| `disableLoginPrompt`              | `false`   | Lewati prompt autentikasi (untuk setup penyedia pihak ketiga)                                                            |
| `allowDangerouslySkipPermissions` | `false`   | Lewati semua prompt izin. **Gunakan dengan sangat hati-hati.**                                                           |
| `claudeProcessWrapper`            | -         | Jalur executable yang digunakan untuk meluncurkan proses Claude                                                          |

## Ekstensi VS Code vs. Claude Code CLI

Claude Code tersedia sebagai ekstensi VS Code (panel grafis) dan CLI (command-line interface di terminal). Beberapa fitur hanya tersedia di CLI. Jika Anda memerlukan fitur khusus CLI, jalankan `claude` di terminal terintegrasi VS Code.

| Fitur                  | CLI                                             | Ekstensi VS Code                                                                           |
| ---------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Perintah dan skills    | [Semua](/id/interactive-mode#built-in-commands) | Subset (ketik `/` untuk melihat yang tersedia)                                             |
| Konfigurasi MCP server | Ya                                              | Parsial (tambahkan server melalui CLI; kelola server yang ada dengan `/mcp` di panel chat) |
| Checkpoints            | Ya                                              | Ya                                                                                         |
| Pintasan bash `!`      | Ya                                              | Tidak                                                                                      |
| Tab completion         | Ya                                              | Tidak                                                                                      |

### Rewind dengan checkpoints

Ekstensi VS Code mendukung checkpoints, yang melacak edit file Claude dan memungkinkan Anda untuk rewind ke status sebelumnya. Arahkan kursor ke pesan apa pun untuk mengungkapkan tombol rewind, kemudian pilih dari tiga opsi:

* **Fork conversation from here**: mulai cabang percakapan baru dari pesan ini sambil menjaga semua perubahan kode tetap utuh
* **Rewind code to here**: kembalikan perubahan file ke titik ini dalam percakapan sambil menjaga riwayat percakapan lengkap
* **Fork conversation and rewind code**: mulai cabang percakapan baru dan kembalikan perubahan file ke titik ini

Untuk detail lengkap tentang cara kerja checkpoints dan keterbatasannya, lihat [Checkpointing](/id/checkpointing).

### Jalankan CLI di VS Code

Untuk menggunakan CLI sambil tetap berada di VS Code, buka terminal terintegrasi (`` Ctrl+` `` di Windows/Linux atau `` Cmd+` `` di Mac) dan jalankan `claude`. CLI secara otomatis terintegrasi dengan IDE Anda untuk fitur seperti tampilan diff dan berbagi diagnostik.

Jika menggunakan terminal eksternal, jalankan `/ide` di dalam Claude Code untuk menghubungkannya ke VS Code.

### Beralih antara ekstensi dan CLI

Ekstensi dan CLI berbagi riwayat percakapan yang sama. Untuk melanjutkan percakapan ekstensi di CLI, jalankan `claude --resume` di terminal. Ini membuka picker interaktif di mana Anda dapat mencari dan memilih percakapan Anda.

### Sertakan output terminal dalam prompt

Referensikan output terminal dalam prompt Anda menggunakan `@terminal:name` di mana `name` adalah judul terminal. Ini memungkinkan Claude melihat output perintah, pesan kesalahan, atau log tanpa copy-paste.

### Pantau proses latar belakang

Saat Claude menjalankan perintah yang berjalan lama, ekstensi menampilkan kemajuan di status bar. Namun, visibilitas untuk tugas latar belakang terbatas dibandingkan dengan CLI. Untuk visibilitas yang lebih baik, minta Claude menampilkan perintah sehingga Anda dapat menjalankannya di terminal terintegrasi VS Code.

### Hubungkan ke alat eksternal dengan MCP

MCP (Model Context Protocol) servers memberikan Claude akses ke alat eksternal, database, dan API.

Untuk menambahkan MCP server, buka terminal terintegrasi (`` Ctrl+` `` atau `` Cmd+` ``) dan jalankan:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Setelah dikonfigurasi, minta Claude untuk menggunakan alat (misalnya, "Review PR #456").

Untuk mengelola MCP servers tanpa meninggalkan VS Code, ketik `/mcp` di panel chat. Dialog manajemen MCP memungkinkan Anda mengaktifkan atau menonaktifkan server, reconnect ke server, dan mengelola autentikasi OAuth. Lihat [dokumentasi MCP](/id/mcp) untuk server yang tersedia.

## Bekerja dengan git

Claude Code terintegrasi dengan git untuk membantu dengan alur kerja kontrol versi langsung di VS Code. Minta Claude untuk commit perubahan, membuat pull request, atau bekerja di seluruh branch.

### Buat commits dan pull requests

Claude dapat stage perubahan, menulis pesan commit, dan membuat pull request berdasarkan pekerjaan Anda:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Saat membuat pull request, Claude menghasilkan deskripsi berdasarkan perubahan kode aktual dan dapat menambahkan konteks tentang pengujian atau keputusan implementasi.

### Gunakan git worktrees untuk tugas paralel

Gunakan flag `--worktree` (`-w`) untuk memulai Claude di worktree terisolasi dengan file dan branch-nya sendiri:

```bash  theme={null}
claude --worktree feature-auth
```

Setiap worktree mempertahankan status file independen sambil berbagi riwayat git. Ini mencegah instance Claude saling mengganggu saat bekerja pada tugas berbeda. Untuk detail lebih lanjut, lihat [Jalankan sesi Claude Code paralel dengan Git worktrees](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

## Gunakan penyedia pihak ketiga

Secara default, Claude Code terhubung langsung ke API Anthropic. Jika organisasi Anda menggunakan Amazon Bedrock, Google Vertex AI, atau Microsoft Foundry untuk mengakses Claude, konfigurasi ekstensi untuk menggunakan penyedia Anda sebagai gantinya:

<Steps>
  <Step title="Nonaktifkan prompt login">
    Buka pengaturan [Disable Login Prompt](vscode://settings/claudeCode.disableLoginPrompt) dan centang kotak.

    Anda juga dapat membuka pengaturan VS Code (`Cmd+,` di Mac atau `Ctrl+,` di Windows/Linux), cari "Claude Code login", dan centang **Disable Login Prompt**.
  </Step>

  <Step title="Konfigurasi penyedia Anda">
    Ikuti panduan setup untuk penyedia Anda:

    * [Claude Code di Amazon Bedrock](/id/amazon-bedrock)
    * [Claude Code di Google Vertex AI](/id/google-vertex-ai)
    * [Claude Code di Microsoft Foundry](/id/microsoft-foundry)

    Panduan ini mencakup konfigurasi penyedia Anda di `~/.claude/settings.json`, yang memastikan pengaturan Anda dibagikan antara ekstensi VS Code dan CLI.
  </Step>
</Steps>

## Keamanan dan privasi

Kode Anda tetap pribadi. Claude Code memproses kode Anda untuk memberikan bantuan tetapi tidak menggunakannya untuk melatih model. Untuk detail tentang penanganan data dan cara opt out dari logging, lihat [Data and privacy](/id/data-usage).

Dengan izin auto-edit diaktifkan, Claude Code dapat memodifikasi file konfigurasi VS Code (seperti `settings.json` atau `tasks.json`) yang mungkin dijalankan VS Code secara otomatis. Untuk mengurangi risiko saat bekerja dengan kode yang tidak dipercaya:

* Aktifkan [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) untuk workspace yang tidak dipercaya
* Gunakan mode persetujuan manual alih-alih auto-accept untuk edit
* Tinjau perubahan dengan hati-hati sebelum menerimanya

## Perbaiki masalah umum

### Ekstensi tidak akan diinstal

* Pastikan Anda memiliki versi VS Code yang kompatibel (1.98.0 atau lebih baru)
* Periksa bahwa VS Code memiliki izin untuk menginstal ekstensi
* Coba instal langsung dari [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### Ikon Spark tidak terlihat

Ikon Spark muncul di **Editor Toolbar** (kanan atas editor) saat Anda memiliki file terbuka. Jika Anda tidak melihatnya:

1. **Buka file**: Ikon memerlukan file untuk dibuka. Hanya membuka folder tidak cukup.
2. **Periksa versi VS Code**: Memerlukan 1.98.0 atau lebih tinggi (Help → About)
3. **Restart VS Code**: Jalankan "Developer: Reload Window" dari Command Palette
4. **Nonaktifkan ekstensi yang bertentangan**: Sementara nonaktifkan ekstensi AI lainnya (Cline, Continue, dll.)
5. **Periksa kepercayaan workspace**: Ekstensi tidak berfungsi dalam Restricted Mode

Alternatifnya, klik "✱ Claude Code" di **Status Bar** (sudut kanan bawah). Ini berfungsi bahkan tanpa file terbuka. Anda juga dapat menggunakan **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) dan ketik "Claude Code".

### Claude Code tidak pernah merespons

Jika Claude Code tidak merespons prompt Anda:

1. **Periksa koneksi internet Anda**: Pastikan Anda memiliki koneksi internet yang stabil
2. **Mulai percakapan baru**: Coba mulai percakapan segar untuk melihat apakah masalah berlanjut
3. **Coba CLI**: Jalankan `claude` dari terminal untuk melihat apakah Anda mendapatkan pesan kesalahan yang lebih detail

Jika masalah berlanjut, [file an issue on GitHub](https://github.com/anthropics/claude-code/issues) dengan detail tentang kesalahan.

## Uninstal ekstensi

Untuk menguninstal ekstensi Claude Code:

1. Buka tampilan Extensions (`Cmd+Shift+X` di Mac atau `Ctrl+Shift+X` di Windows/Linux)
2. Cari "Claude Code"
3. Klik **Uninstall**

Untuk juga menghapus data ekstensi dan reset semua pengaturan:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Untuk bantuan tambahan, lihat [panduan troubleshooting](/id/troubleshooting).

## Langkah berikutnya

Sekarang Anda telah menyiapkan Claude Code di VS Code:

* [Jelajahi alur kerja umum](/id/common-workflows) untuk mendapatkan hasil maksimal dari Claude Code
* [Siapkan MCP servers](/id/mcp) untuk memperluas kemampuan Claude dengan alat eksternal. Tambahkan server menggunakan CLI, kemudian kelola dengan `/mcp` di panel chat.
* [Konfigurasi pengaturan Claude Code](/id/settings) untuk menyesuaikan perintah yang diizinkan, hooks, dan lainnya. Pengaturan ini dibagikan antara ekstensi dan CLI.
