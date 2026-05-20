> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Buat subagent khusus

> Buat dan gunakan subagent AI khusus di Claude Code untuk alur kerja khusus tugas dan manajemen konteks yang lebih baik.

Subagent adalah asisten AI khusus yang menangani jenis tugas tertentu. Gunakan satu ketika tugas sampingan akan membanjiri percakapan utama Anda dengan hasil pencarian, log, atau konten file yang tidak akan Anda referensikan lagi: subagent melakukan pekerjaan itu dalam konteksnya sendiri dan hanya mengembalikan ringkasan. Tentukan subagent khusus ketika Anda terus menelurkan jenis pekerja yang sama dengan instruksi yang sama.

Setiap subagent berjalan di jendela konteksnya sendiri dengan prompt sistem khusus, akses alat tertentu, dan izin independen. Ketika Claude menemukan tugas yang sesuai dengan deskripsi subagent, Claude mendelegasikan ke subagent tersebut, yang bekerja secara independen dan mengembalikan hasil. Untuk melihat penghematan konteks dalam praktik, [visualisasi jendela konteks](/id/context-window) menjelaskan sesi di mana subagent menangani penelitian di jendela terpisahnya sendiri.

<Note>
  Subagent bekerja dalam satu sesi. Untuk menjalankan banyak sesi independen secara paralel dan memantaunya dari satu tempat, lihat [agen latar belakang](/id/agent-view). Untuk sesi yang berkomunikasi satu sama lain, lihat [tim agen](/id/agent-teams).
</Note>

Subagent membantu Anda:

* **Mempertahankan konteks** dengan menjaga eksplorasi dan implementasi di luar percakapan utama Anda
* **Menerapkan batasan** dengan membatasi alat mana yang dapat digunakan subagent
* **Menggunakan kembali konfigurasi** di seluruh proyek dengan subagent tingkat pengguna
* **Mengkhususkan perilaku** dengan prompt sistem yang terfokus untuk domain tertentu
* **Mengontrol biaya** dengan merutekan tugas ke model yang lebih cepat dan lebih murah seperti Haiku

Claude menggunakan deskripsi setiap subagent untuk memutuskan kapan mendelegasikan tugas. Ketika Anda membuat subagent, tulis deskripsi yang jelas sehingga Claude tahu kapan menggunakannya.

Claude Code mencakup beberapa subagent bawaan seperti **Explore**, **Plan**, dan **general-purpose**. Anda juga dapat membuat subagent khusus untuk menangani tugas tertentu. Halaman ini mencakup:

* [Subagent bawaan](#built-in-subagents)
* [Cara membuat subagent Anda sendiri](#quickstart-create-your-first-subagent)
* [Opsi konfigurasi lengkap](#configure-subagents)
* [Pola untuk bekerja dengan subagent](#work-with-subagents)
* [Subagent yang di-fork](#fork-the-current-conversation)
* [Contoh subagent](#example-subagents)

## Subagent bawaan

Claude Code mencakup subagent bawaan yang Claude gunakan secara otomatis jika sesuai. Masing-masing mewarisi izin percakapan induk dengan pembatasan alat tambahan.

Explore dan Plan melewati file CLAUDE.md Anda dan status git sesi induk untuk menjaga penelitian tetap cepat dan hemat biaya. Setiap subagent bawaan lainnya dan [subagent khusus](#configure-subagents) memuat keduanya. Untuk rincian lengkap tentang apa yang mencapai subagent, lihat [apa yang dimuat saat startup](#what-loads-at-startup).

<Tabs>
  <Tab title="Explore">
    Agen cepat yang dioptimalkan hanya-baca untuk mencari dan menganalisis basis kode.

    * **Model**: Haiku (cepat, latensi rendah)
    * **Tools**: Alat hanya-baca (akses ditolak ke alat Write dan Edit)
    * **Purpose**: Penemuan file, pencarian kode, eksplorasi basis kode

    Claude mendelegasikan ke Explore ketika perlu mencari atau memahami basis kode tanpa membuat perubahan. Ini menjaga hasil eksplorasi di luar konteks percakapan utama Anda.

    Saat memanggil Explore, Claude menentukan tingkat ketelitian: **quick** untuk pencarian yang ditargetkan, **medium** untuk eksplorasi seimbang, atau **very thorough** untuk analisis komprehensif.
  </Tab>

  <Tab title="Plan">
    Agen penelitian yang digunakan selama [plan mode](/id/permission-modes#analyze-before-you-edit-with-plan-mode) untuk mengumpulkan konteks sebelum menyajikan rencana.

    * **Model**: Mewarisi dari percakapan utama
    * **Tools**: Alat hanya-baca (akses ditolak ke alat Write dan Edit)
    * **Purpose**: Penelitian basis kode untuk perencanaan

    Ketika Anda dalam plan mode dan Claude perlu memahami basis kode Anda, Claude mendelegasikan penelitian ke subagent Plan. Ini mencegah nesting tak terbatas (subagent tidak dapat menelurkan subagent lain) sambil tetap mengumpulkan konteks yang diperlukan.
  </Tab>

  <Tab title="General-purpose">
    Agen yang mampu untuk tugas kompleks multi-langkah yang memerlukan eksplorasi dan tindakan.

    * **Model**: Mewarisi dari percakapan utama
    * **Tools**: Semua alat
    * **Purpose**: Penelitian kompleks, operasi multi-langkah, modifikasi kode

    Claude mendelegasikan ke general-purpose ketika tugas memerlukan eksplorasi dan modifikasi, penalaran kompleks untuk menafsirkan hasil, atau beberapa langkah yang saling bergantung.
  </Tab>

  <Tab title="Other">
    Claude Code mencakup agen pembantu tambahan untuk tugas tertentu. Ini biasanya dipanggil secara otomatis, jadi Anda tidak perlu menggunakannya secara langsung.

    | Agen              | Model  | Kapan Claude menggunakannya                                                  |
    | :---------------- | :----- | :--------------------------------------------------------------------------- |
    | statusline-setup  | Sonnet | Ketika Anda menjalankan `/statusline` untuk mengonfigurasi baris status Anda |
    | claude-code-guide | Haiku  | Ketika Anda mengajukan pertanyaan tentang fitur Claude Code                  |
  </Tab>
</Tabs>

Selain subagent bawaan ini, Anda dapat membuat subagent Anda sendiri dengan prompt khusus, pembatasan alat, mode izin, hooks, dan skills. Bagian berikut menunjukkan cara memulai dan menyesuaikan subagent.

## Quickstart: buat subagent pertama Anda

Subagent didefinisikan dalam file Markdown dengan frontmatter YAML. Anda dapat [membuatnya secara manual](#write-subagent-files) atau menggunakan perintah `/agents`.

Panduan ini memandu Anda melalui pembuatan subagent tingkat pengguna dengan perintah `/agents`. Subagent meninjau kode dan menyarankan perbaikan untuk basis kode.

<Steps>
  <Step title="Buka antarmuka subagent">
    Di Claude Code, jalankan:

    ```text theme={null}
    /agents
    ```
  </Step>

  <Step title="Pilih lokasi">
    Beralih ke tab **Library**, pilih **Create new agent**, kemudian pilih **Personal**. Ini menyimpan subagent ke `~/.claude/agents/` sehingga tersedia di semua proyek Anda.
  </Step>

  <Step title="Hasilkan dengan Claude">
    Pilih **Generate with Claude**. Ketika diminta, jelaskan subagent:

    ```text theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude menghasilkan pengenal, deskripsi, dan prompt sistem untuk Anda.
  </Step>

  <Step title="Pilih alat">
    Untuk reviewer hanya-baca, batalkan pilihan semuanya kecuali **Read-only tools**. Jika Anda membiarkan semua alat dipilih, subagent mewarisi semua alat yang tersedia untuk percakapan utama.
  </Step>

  <Step title="Pilih model">
    Pilih model mana yang digunakan subagent. Untuk agen contoh ini, pilih **Sonnet**, yang menyeimbangkan kemampuan dan kecepatan untuk menganalisis pola kode.
  </Step>

  <Step title="Pilih warna">
    Pilih warna latar belakang untuk subagent. Ini membantu Anda mengidentifikasi subagent mana yang berjalan di UI.
  </Step>

  <Step title="Konfigurasi memori">
    Pilih **User scope** untuk memberikan subagent [direktori memori persisten](#enable-persistent-memory) di `~/.claude/agent-memory/`. Subagent menggunakan ini untuk mengumpulkan wawasan di seluruh percakapan, seperti pola basis kode dan masalah berulang. Pilih **None** jika Anda tidak ingin subagent mempertahankan pembelajaran.
  </Step>

  <Step title="Simpan dan coba">
    Tinjau ringkasan konfigurasi. Tekan `s` atau `Enter` untuk menyimpan, atau tekan `e` untuk menyimpan dan mengedit file di editor Anda. Subagent tersedia segera. Coba:

    ```text theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude mendelegasikan ke subagent baru Anda, yang memindai basis kode dan mengembalikan saran perbaikan.
  </Step>
</Steps>

Anda sekarang memiliki subagent yang dapat Anda gunakan di proyek apa pun di mesin Anda untuk menganalisis basis kode dan menyarankan perbaikan.

Anda juga dapat membuat subagent secara manual sebagai file Markdown, mendefinisikannya melalui flag CLI, atau mendistribusikannya melalui plugins. Bagian berikut mencakup semua opsi konfigurasi.

## Konfigurasi subagent

### Gunakan perintah /agents

Perintah `/agents` membuka antarmuka bertab untuk mengelola subagent. Tab **Running** menunjukkan subagent langsung dan memungkinkan Anda membuka atau menghentikannya. Tab **Library** memungkinkan Anda:

* Melihat semua subagent yang tersedia (bawaan, pengguna, proyek, dan plugin)
* Membuat subagent baru dengan setup terpandu atau generasi Claude
* Mengedit konfigurasi subagent yang ada dan akses alat
* Menghapus subagent khusus
* Melihat subagent mana yang aktif ketika duplikat ada

Ini adalah cara yang direkomendasikan untuk membuat dan mengelola subagent. Untuk pembuatan manual atau otomasi, Anda juga dapat menambahkan file subagent secara langsung.

### Pilih cakupan subagent

Subagent adalah file Markdown dengan frontmatter YAML. Simpan mereka di lokasi berbeda tergantung cakupan. Ketika beberapa subagent berbagi nama yang sama, lokasi prioritas lebih tinggi menang.

| Lokasi                     | Cakupan                  | Prioritas     | Cara membuat                                           |
| :------------------------- | :----------------------- | :------------ | :----------------------------------------------------- |
| Pengaturan terkelola       | Seluruh organisasi       | 1 (tertinggi) | Digunakan melalui [pengaturan terkelola](/id/settings) |
| Flag CLI `--agents`        | Sesi saat ini            | 2             | Lewatkan JSON saat meluncurkan Claude Code             |
| `.claude/agents/`          | Proyek saat ini          | 3             | Interaktif atau manual                                 |
| `~/.claude/agents/`        | Semua proyek Anda        | 4             | Interaktif atau manual                                 |
| Direktori `agents/` plugin | Tempat plugin diaktifkan | 5 (terendah)  | Diinstal dengan [plugins](/id/plugins)                 |

**Subagent proyek** (`.claude/agents/`) ideal untuk subagent khusus untuk basis kode. Periksa mereka ke kontrol versi sehingga tim Anda dapat menggunakannya dan meningkatkannya secara kolaboratif.

Subagent proyek ditemukan dengan berjalan naik dari direktori kerja saat ini. Direktori yang ditambahkan dengan `--add-dir` [memberikan akses file saja](/id/permissions#additional-directories-grant-file-access-not-configuration) dan tidak dipindai untuk subagent. Untuk berbagi subagent di seluruh proyek, gunakan `~/.claude/agents/` atau [plugin](/id/plugins).

**Subagent pengguna** (`~/.claude/agents/`) adalah subagent pribadi yang tersedia di semua proyek Anda.

Claude Code memindai `.claude/agents/` dan `~/.claude/agents/` secara rekursif, sehingga Anda dapat mengorganisir definisi ke dalam subfolder seperti `agents/review/` atau `agents/research/`. Jalur subdirektori tidak mempengaruhi cara subagent diidentifikasi atau dipanggil, karena identitas hanya berasal dari bidang frontmatter `name`. Jaga nilai `name` tetap unik di seluruh pohon: jika dua file dalam satu cakupan mendeklarasikan nama yang sama, Claude Code menyimpan satu dan membuang yang lain tanpa peringatan.

Direktori `agents/` plugin juga dipindai secara rekursif. Tidak seperti cakupan proyek dan pengguna, subfolder di dalam direktori `agents/` plugin menjadi bagian dari [pengenal yang dibatasi cakupan](#invoke-subagents-explicitly): file di `agents/review/security.md` dalam plugin `my-plugin` terdaftar sebagai `my-plugin:review:security`.

**Subagent yang ditentukan CLI** dilewatkan sebagai JSON saat meluncurkan Claude Code. Mereka hanya ada untuk sesi itu dan tidak disimpan ke disk, menjadikannya berguna untuk pengujian cepat atau skrip otomasi. Anda dapat mendefinisikan beberapa subagent dalam satu panggilan `--agents`:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    claude --agents '{
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }'
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    claude --agents @'
    {
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }
    '@
    ```
  </Tab>
</Tabs>

Flag `--agents` menerima JSON dengan [frontmatter](#supported-frontmatter-fields) yang sama bidang subagent berbasis file: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, dan `color`. Gunakan `prompt` untuk prompt sistem, setara dengan badan markdown dalam subagent berbasis file.

**Subagent terkelola** digunakan oleh administrator organisasi. Tempatkan file markdown dalam `.claude/agents/` di dalam [direktori pengaturan terkelola](/id/settings#settings-files), menggunakan format frontmatter yang sama dengan subagent proyek dan pengguna. Definisi terkelola mengambil alih subagent proyek dan pengguna dengan nama yang sama.

**Subagent plugin** berasal dari [plugins](/id/plugins) yang telah Anda instal. Mereka muncul di `/agents` bersama subagent khusus Anda. Lihat [referensi komponen plugin](/id/plugins-reference#agents) untuk detail tentang membuat subagent plugin.

<Note>
  Untuk alasan keamanan, subagent plugin tidak mendukung bidang frontmatter `hooks`, `mcpServers`, atau `permissionMode`. Bidang-bidang ini diabaikan saat memuat agen dari plugin. Jika Anda membutuhkannya, salin file agen ke dalam `.claude/agents/` atau `~/.claude/agents/`. Anda juga dapat menambahkan aturan ke [`permissions.allow`](/id/settings#permission-settings) dalam `settings.json` atau `settings.local.json`, tetapi aturan-aturan ini berlaku untuk seluruh sesi, bukan hanya subagent plugin.
</Note>

Definisi subagent dari salah satu cakupan ini juga tersedia untuk [tim agen](/id/agent-teams#use-subagent-definitions-for-teammates): saat menelurkan rekan kerja, Anda dapat mereferensikan jenis subagent dan rekan kerja menggunakan `tools` dan `model`-nya, dengan badan definisi ditambahkan ke prompt sistem rekan kerja sebagai instruksi tambahan. Lihat [tim agen](/id/agent-teams#use-subagent-definitions-for-teammates) untuk bidang frontmatter mana yang berlaku pada jalur itu.

### Tulis file subagent

File subagent menggunakan frontmatter YAML untuk konfigurasi, diikuti oleh prompt sistem dalam Markdown:

<Note>
  Subagent dimuat saat awal sesi. Jika Anda menambah atau mengedit file subagent secara langsung di disk, restart sesi Anda untuk memuatnya. Subagent yang dibuat melalui antarmuka `/agents` berlaku segera tanpa restart.
</Note>

```markdown theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Frontmatter mendefinisikan metadata dan konfigurasi subagent. Badan menjadi prompt sistem yang memandu perilaku subagent. Subagent menerima hanya prompt sistem ini (ditambah detail lingkungan dasar seperti direktori kerja), bukan prompt sistem Claude Code lengkap.

Subagent dimulai di direktori kerja saat ini percakapan utama. Dalam subagent, perintah `cd` tidak bertahan antara panggilan alat Bash atau PowerShell dan tidak mempengaruhi direktori kerja percakapan utama. Untuk memberikan subagent salinan repositori yang terisolasi sebagai gantinya, atur [`isolation: worktree`](#supported-frontmatter-fields).

#### Bidang frontmatter yang didukung

Bidang berikut dapat digunakan dalam frontmatter YAML. Hanya `name` dan `description` yang diperlukan.

| Bidang            | Diperlukan | Deskripsi                                                                                                                                                                                                                                                                                                                                                             |
| :---------------- | :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Ya         | Pengenal unik menggunakan huruf kecil dan tanda hubung. [Hooks](/id/hooks#subagentstart) menerima nilai ini sebagai `agent_type`. Nama file tidak harus cocok                                                                                                                                                                                                         |
| `description`     | Ya         | Kapan Claude harus mendelegasikan ke subagent ini                                                                                                                                                                                                                                                                                                                     |
| `tools`           | Tidak      | [Alat](#available-tools) yang dapat digunakan subagent. Mewarisi semua alat jika dihilangkan. Untuk memuat Skills ke dalam konteks, gunakan bidang `skills` daripada mencantumkan `Skill` di sini                                                                                                                                                                     |
| `disallowedTools` | Tidak      | Alat untuk ditolak, dihapus dari daftar yang diwarisi atau ditentukan                                                                                                                                                                                                                                                                                                 |
| `model`           | Tidak      | [Model](#choose-a-model) untuk digunakan: `sonnet`, `opus`, `haiku`, ID model lengkap (misalnya, `claude-opus-4-7`), atau `inherit`. Default ke `inherit`                                                                                                                                                                                                             |
| `permissionMode`  | Tidak      | [Mode izin](#permission-modes): `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, atau `plan`. Diabaikan untuk [subagent plugin](#choose-the-subagent-scope)                                                                                                                                                                                          |
| `maxTurns`        | Tidak      | Jumlah maksimum putaran agentic sebelum subagent berhenti                                                                                                                                                                                                                                                                                                             |
| `skills`          | Tidak      | [Skills](/id/skills) untuk dimuat ke dalam konteks subagent saat startup. Konten skill lengkap disuntikkan, bukan hanya deskripsi. Subagent masih dapat memanggil project, user, dan plugin skills yang tidak tercantum melalui alat Skill                                                                                                                            |
| `mcpServers`      | Tidak      | [MCP servers](/id/mcp) tersedia untuk subagent ini. Setiap entri adalah nama server yang mereferensikan server yang sudah dikonfigurasi (misalnya, `"slack"`) atau definisi inline dengan nama server sebagai kunci dan [konfigurasi MCP server](/id/mcp#installing-mcp-servers) lengkap sebagai nilai. Diabaikan untuk [subagent plugin](#choose-the-subagent-scope) |
| `hooks`           | Tidak      | [Lifecycle hooks](#define-hooks-for-subagents) yang dibatasi pada subagent ini. Diabaikan untuk [subagent plugin](#choose-the-subagent-scope)                                                                                                                                                                                                                         |
| `memory`          | Tidak      | [Cakupan memori persisten](#enable-persistent-memory): `user`, `project`, atau `local`. Memungkinkan pembelajaran lintas sesi                                                                                                                                                                                                                                         |
| `background`      | Tidak      | Atur ke `true` untuk selalu menjalankan subagent ini sebagai [background task](#run-subagents-in-foreground-or-background). Default: `false`                                                                                                                                                                                                                          |
| `effort`          | Tidak      | Tingkat usaha ketika subagent ini aktif. Menimpa tingkat usaha sesi. Default: mewarisi dari sesi. Opsi: `low`, `medium`, `high`, `xhigh`, `max`; tingkat yang tersedia tergantung pada model                                                                                                                                                                          |
| `isolation`       | Tidak      | Atur ke `worktree` untuk menjalankan subagent dalam [git worktree](/id/worktrees) sementara, memberikannya salinan repositori yang terisolasi. Worktree secara otomatis dibersihkan jika subagent tidak membuat perubahan                                                                                                                                             |
| `color`           | Tidak      | Warna tampilan untuk subagent dalam daftar tugas dan transkrip. Menerima `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, atau `cyan`                                                                                                                                                                                                                    |
| `initialPrompt`   | Tidak      | Auto-submitted sebagai putaran pengguna pertama ketika agen ini berjalan sebagai agen sesi utama (melalui `--agent` atau pengaturan `agent`). [Commands](/id/commands) dan [skills](/id/skills) diproses. Ditambahkan di depan prompt yang disediakan pengguna apa pun                                                                                                |

### Pilih model

Bidang `model` mengontrol [model AI](/id/model-config) mana yang digunakan subagent:

* **Alias model**: Gunakan salah satu alias yang tersedia: `sonnet`, `opus`, atau `haiku`
* **ID model lengkap**: Gunakan ID model lengkap seperti `claude-opus-4-7` atau `claude-sonnet-4-6`. Menerima nilai yang sama dengan flag `--model`
* **inherit**: Gunakan model yang sama dengan percakapan utama
* **Dihilangkan**: Jika tidak ditentukan, default ke `inherit` (menggunakan model yang sama dengan percakapan utama)

Ketika Claude memanggil subagent, Claude juga dapat melewatkan parameter `model` untuk invokasi spesifik itu. Claude Code menyelesaikan model subagent dalam urutan ini:

1. Variabel lingkungan [`CLAUDE_CODE_SUBAGENT_MODEL`](/id/model-config#environment-variables), jika diatur
2. Parameter `model` per-invokasi
3. Frontmatter `model` definisi subagent
4. Model percakapan utama

### Kontrol kemampuan subagent

Anda dapat mengontrol apa yang dapat dilakukan subagent melalui akses alat, mode izin, dan aturan bersyarat.

#### Alat yang tersedia

Subagent dapat menggunakan salah satu [alat internal](/id/tools-reference) Claude Code. Secara default, subagent mewarisi semua alat dari percakapan utama, termasuk alat MCP.

Untuk membatasi alat, gunakan bidang `tools` (allowlist) atau bidang `disallowedTools` (denylist). Contoh ini menggunakan `tools` untuk secara eksklusif mengizinkan Read, Grep, Glob, dan Bash. Subagent tidak dapat mengedit file, menulis file, atau menggunakan alat MCP apa pun:

```yaml theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Contoh ini menggunakan `disallowedTools` untuk mewarisi setiap alat dari percakapan utama kecuali Write dan Edit. Subagent menyimpan Bash, alat MCP, dan semuanya yang lain:

```yaml theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

Jika keduanya diatur, `disallowedTools` diterapkan terlebih dahulu, kemudian `tools` diselesaikan terhadap kumpulan yang tersisa. Alat yang tercantum di keduanya dihapus.

#### Batasi subagent mana yang dapat dihasilkan

Ketika agen berjalan sebagai thread utama dengan `claude --agent`, agen dapat menelurkan subagent menggunakan alat Agent. Untuk membatasi jenis subagent mana yang dapat dihasilkan, gunakan sintaks `Agent(agent_type)` dalam bidang `tools`.

<Note>Dalam versi 2.1.63, alat Task diganti nama menjadi Agent. Referensi `Task(...)` yang ada dalam pengaturan dan definisi agen masih berfungsi sebagai alias.</Note>

```yaml theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Ini adalah allowlist: hanya subagent `worker` dan `researcher` yang dapat dihasilkan. Jika agen mencoba menelurkan jenis lain, permintaan gagal dan agen hanya melihat jenis yang diizinkan dalam promptnya. Untuk memblokir agen tertentu sambil mengizinkan semua yang lain, gunakan [`permissions.deny`](#disable-specific-subagents) sebagai gantinya.

Untuk mengizinkan penelur subagent apa pun tanpa pembatasan, gunakan `Agent` tanpa tanda kurung:

```yaml theme={null}
tools: Agent, Read, Bash
```

Jika `Agent` dihilangkan dari daftar `tools` sepenuhnya, agen tidak dapat menelurkan subagent apa pun. Pembatasan ini hanya berlaku untuk agen yang berjalan sebagai thread utama dengan `claude --agent`. Subagent tidak dapat menelurkan subagent lain, jadi `Agent(agent_type)` tidak berpengaruh dalam definisi subagent.

#### Cakupan MCP servers ke subagent

Gunakan bidang `mcpServers` untuk memberikan subagent akses ke [MCP](/id/mcp) servers yang tidak tersedia dalam percakapan utama. Server inline yang ditentukan di sini terhubung saat subagent dimulai dan terputus saat selesai. Referensi string berbagi koneksi sesi induk.

<Note>
  Bidang `mcpServers` berlaku dalam kedua konteks di mana file agen dapat berjalan:

  * Sebagai subagent, dihasilkan melalui alat Agent atau @-mention
  * Sebagai sesi utama, diluncurkan dengan [`--agent`](#invoke-subagents-explicitly) atau pengaturan `agent`

  Ketika agen adalah sesi utama, definisi server inline terhubung saat startup bersama server dari [`.mcp.json`](/id/mcp) dan file pengaturan.
</Note>

Setiap entri dalam daftar adalah definisi server inline atau string yang mereferensikan MCP server yang sudah dikonfigurasi dalam sesi Anda:

```yaml theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Definisi inline menggunakan skema yang sama dengan entri server `.mcp.json` (`stdio`, `http`, `sse`, `ws`), dikunci dengan nama server.

Untuk menjaga MCP server di luar percakapan utama sepenuhnya dan menghindari deskripsi alatnya mengonsumsi konteks di sana, tentukan secara inline di sini daripada di `.mcp.json`. Subagent mendapatkan alat; percakapan induk tidak.

#### Mode izin

Bidang `permissionMode` mengontrol bagaimana subagent menangani prompt izin. Subagent mewarisi konteks izin dari percakapan utama dan dapat menimpa mode, kecuali ketika mode induk mengambil alih seperti yang dijelaskan di bawah.

| Mode                | Perilaku                                                                                                                                                     |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Pemeriksaan izin standar dengan prompt                                                                                                                       |
| `acceptEdits`       | Auto-terima edit file dan perintah sistem file umum untuk jalur di direktori kerja atau `additionalDirectories`                                              |
| `auto`              | [Auto mode](/id/permission-modes#eliminate-prompts-with-auto-mode): pengklasifikasi latar belakang meninjau perintah dan penulisan direktori yang dilindungi |
| `dontAsk`           | Auto-tolak prompt izin (alat yang secara eksplisit diizinkan masih berfungsi)                                                                                |
| `bypassPermissions` | Lewati prompt izin                                                                                                                                           |
| `plan`              | Plan mode (eksplorasi hanya-baca)                                                                                                                            |

<Warning>
  Gunakan `bypassPermissions` dengan hati-hati. Ini melewati prompt izin, memungkinkan subagent untuk menjalankan operasi tanpa persetujuan, termasuk penulisan ke `.git`, `.claude`, `.vscode`, `.idea`, dan `.husky`. Penghapusan direktori root dan home seperti `rm -rf /` masih meminta sebagai circuit breaker. Lihat [permission modes](/id/permission-modes#skip-all-checks-with-bypasspermissions-mode) untuk detail.
</Warning>

Jika induk menggunakan `bypassPermissions` atau `acceptEdits`, ini mengambil alih dan tidak dapat ditimpa. Jika induk menggunakan [auto mode](/id/permission-modes#eliminate-prompts-with-auto-mode), subagent mewarisi auto mode dan `permissionMode` apa pun dalam frontmatternya diabaikan: pengklasifikasi mengevaluasi panggilan alat subagent dengan aturan blok dan izin yang sama dengan sesi induk.

#### Preload skills ke dalam subagent

Gunakan bidang `skills` untuk menyuntikkan konten skill ke dalam konteks subagent saat startup. Ini memberikan subagent pengetahuan domain tanpa memerlukan penemuan dan pemuatan skills selama eksekusi.

```yaml theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

Konten lengkap setiap skill yang tercantum disuntikkan ke dalam konteks subagent saat startup. Bidang ini mengontrol skill mana yang dimuat sebelumnya, bukan skill mana yang dapat diakses subagent: tanpanya, subagent masih dapat menemukan dan memanggil project, user, dan plugin skills melalui alat Skill selama eksekusi. Untuk mencegah subagent memanggil skills sama sekali, hilangkan `Skill` dari daftar [`tools`](#available-tools) atau tambahkan ke `disallowedTools`.

Anda tidak dapat preload skills yang menetapkan [`disable-model-invocation: true`](/id/skills#control-who-invokes-a-skill), karena preloading menarik dari set skills yang sama yang dapat diinvokasi Claude. Jika skill yang tercantum hilang atau dinonaktifkan, Claude Code melewatinya dan mencatat peringatan ke debug log.

<Note>
  Ini adalah kebalikan dari [menjalankan skill dalam subagent](/id/skills#run-skills-in-a-subagent). Dengan `skills` dalam subagent, subagent mengontrol prompt sistem dan memuat konten skill. Dengan `context: fork` dalam skill, konten skill disuntikkan ke dalam agen yang Anda tentukan. Keduanya menggunakan sistem yang mendasar yang sama.
</Note>

#### Aktifkan memori persisten

Bidang `memory` memberikan subagent direktori persisten yang bertahan di seluruh percakapan. Subagent menggunakan direktori ini untuk membangun pengetahuan seiring waktu, seperti pola basis kode, wawasan debugging, dan keputusan arsitektur.

```yaml theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Pilih cakupan berdasarkan seberapa luas memori harus diterapkan:

| Cakupan   | Lokasi                                        | Gunakan ketika                                                                           |
| :-------- | :-------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | subagent harus mengingat pembelajaran di seluruh semua proyek                            |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | pengetahuan subagent spesifik proyek dan dapat dibagikan melalui kontrol versi           |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | pengetahuan subagent spesifik proyek tetapi tidak boleh diperiksa ke dalam kontrol versi |

Ketika memori diaktifkan:

* Prompt sistem subagent mencakup instruksi untuk membaca dan menulis ke direktori memori.
* Prompt sistem subagent juga mencakup 200 baris pertama atau 25KB dari `MEMORY.md` dalam direktori memori, mana pun yang lebih kecil, dengan instruksi untuk mengkurasi `MEMORY.md` jika melebihi batas itu.
* Alat Read, Write, dan Edit secara otomatis diaktifkan sehingga subagent dapat mengelola file memorinya.

##### Tips memori persisten

* `project` adalah cakupan default yang direkomendasikan. Ini membuat pengetahuan subagent dapat dibagikan melalui kontrol versi. Gunakan `user` ketika pengetahuan subagent berlaku secara luas di seluruh proyek, atau `local` ketika pengetahuan tidak boleh diperiksa ke dalam kontrol versi.
* Minta subagent untuk berkonsultasi dengan memorinya sebelum memulai pekerjaan: "Review PR ini, dan periksa memori Anda untuk pola yang telah Anda lihat sebelumnya."
* Minta subagent untuk memperbarui memorinya setelah menyelesaikan tugas: "Sekarang setelah Anda selesai, simpan apa yang Anda pelajari ke memori Anda." Seiring waktu, ini membangun basis pengetahuan yang membuat subagent lebih efektif.
* Sertakan instruksi memori langsung dalam file markdown subagent sehingga secara proaktif mempertahankan basis pengetahuannya sendiri:

  ```markdown theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Aturan bersyarat dengan hooks

Untuk kontrol yang lebih dinamis atas penggunaan alat, gunakan hooks `PreToolUse` untuk memvalidasi operasi sebelum dijalankan. Ini berguna ketika Anda perlu mengizinkan beberapa operasi alat sambil memblokir yang lain.

Contoh ini membuat subagent yang hanya mengizinkan kueri database hanya-baca. Hook `PreToolUse` menjalankan skrip yang ditentukan dalam `command` sebelum setiap perintah Bash dijalankan:

```yaml theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [melewatkan input hook sebagai JSON](/id/hooks#pretooluse-input) melalui stdin ke perintah hook. Skrip validasi membaca JSON ini, mengekstrak perintah Bash, dan [keluar dengan kode 2](/id/hooks#exit-code-2-behavior-per-event) untuk memblokir operasi penulisan:

```bash theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

Lihat [Hook input](/id/hooks#pretooluse-input) untuk skema input lengkap dan [exit codes](/id/hooks#exit-code-output) untuk bagaimana kode keluar mempengaruhi perilaku. Di Windows, tulis skrip hook dalam PowerShell dan tambahkan `shell: powershell` ke entri hook seperti yang ditunjukkan dalam [menjalankan hooks dalam PowerShell](/id/hooks#windows-powershell-tool).

#### Nonaktifkan subagent tertentu

Anda dapat mencegah Claude menggunakan subagent tertentu dengan menambahkannya ke array `deny` dalam [pengaturan](/id/settings#permission-settings) Anda. Gunakan format `Agent(subagent-name)` di mana `subagent-name` cocok dengan bidang nama subagent.

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Ini berfungsi untuk subagent bawaan dan khusus. Anda juga dapat menggunakan flag CLI `--disallowedTools`:

```bash theme={null}
claude --disallowedTools "Agent(Explore)"
```

Lihat [dokumentasi Permissions](/id/permissions#tool-specific-permission-rules) untuk detail lebih lanjut tentang aturan izin.

### Tentukan hooks untuk subagent

Subagent dapat mendefinisikan [hooks](/id/hooks) yang berjalan selama siklus hidup subagent. Ada dua cara untuk mengonfigurasi hooks:

1. **Dalam frontmatter subagent**: Tentukan hooks yang hanya berjalan saat subagent tertentu itu aktif
2. **Dalam `settings.json`**: Tentukan hooks yang berjalan dalam sesi utama ketika subagent dimulai atau berhenti

#### Hooks dalam frontmatter subagent

Tentukan hooks langsung dalam file markdown subagent. Hooks ini hanya berjalan saat subagent spesifik itu aktif dan dibersihkan saat selesai.

<Note>
  Frontmatter hooks terjadi ketika agen dihasilkan sebagai subagent melalui alat Agent atau @-mention, dan ketika agen berjalan sebagai sesi utama melalui [`--agent`](#invoke-subagents-explicitly) atau pengaturan `agent`. Dalam kasus sesi-utama mereka berjalan bersama hook apa pun yang ditentukan dalam [`settings.json`](/id/hooks).
</Note>

Semua [hook events](/id/hooks#hook-events) didukung. Peristiwa paling umum untuk subagent adalah:

| Peristiwa     | Input Matcher | Kapan itu terjadi                                                   |
| :------------ | :------------ | :------------------------------------------------------------------ |
| `PreToolUse`  | Nama alat     | Sebelum subagent menggunakan alat                                   |
| `PostToolUse` | Nama alat     | Setelah subagent menggunakan alat                                   |
| `Stop`        | (tidak ada)   | Ketika subagent selesai (dikonversi ke `SubagentStop` saat runtime) |

Contoh ini memvalidasi perintah Bash dengan hook `PreToolUse` dan menjalankan linter setelah edit file dengan `PostToolUse`:

```yaml theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Hooks `Stop` dalam frontmatter secara otomatis dikonversi ke peristiwa `SubagentStop`.

#### Hooks tingkat proyek untuk peristiwa subagent

Konfigurasi hooks dalam `settings.json` yang merespons peristiwa siklus hidup subagent dalam sesi utama.

| Peristiwa       | Input Matcher   | Kapan itu terjadi                |
| :-------------- | :-------------- | :------------------------------- |
| `SubagentStart` | Nama jenis agen | Ketika subagent mulai dijalankan |
| `SubagentStop`  | Nama jenis agen | Ketika subagent selesai          |

Kedua peristiwa mendukung matcher untuk menargetkan jenis agen tertentu berdasarkan nama. Contoh ini menjalankan skrip setup hanya ketika subagent `db-agent` dimulai, dan skrip cleanup ketika subagent apa pun berhenti:

```json theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

Lihat [Hooks](/id/hooks) untuk format konfigurasi hook lengkap.

## Bekerja dengan subagent

### Pahami delegasi otomatis

Claude secara otomatis mendelegasikan tugas berdasarkan deskripsi tugas dalam permintaan Anda, bidang `description` dalam konfigurasi subagent, dan konteks saat ini. Untuk mendorong delegasi proaktif, sertakan frasa seperti "use proactively" dalam bidang deskripsi subagent Anda.

### Panggil subagent secara eksplisit

Ketika delegasi otomatis tidak cukup, Anda dapat meminta subagent sendiri. Tiga pola meningkat dari saran satu kali ke default sesi-lebar:

* **Bahasa alami**: sebutkan subagent dalam prompt Anda; Claude memutuskan apakah akan mendelegasikan
* **@-mention**: menjamin subagent berjalan untuk satu tugas
* **Sesi-lebar**: seluruh sesi menggunakan prompt sistem subagent, pembatasan alat, dan model melalui flag `--agent` atau pengaturan `agent`

Untuk bahasa alami, tidak ada sintaks khusus. Sebutkan subagent dan Claude biasanya mendelegasikan:

```text theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention subagent.** Ketik `@` dan pilih subagent dari typeahead, dengan cara yang sama Anda @-mention file. Ini memastikan subagent tertentu berjalan daripada meninggalkan pilihan kepada Claude:

```text theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Pesan lengkap Anda masih pergi ke Claude, yang menulis prompt tugas subagent berdasarkan apa yang Anda minta. @-mention mengontrol subagent mana yang Claude panggil, bukan prompt apa yang diterima.

Subagent yang disediakan oleh [plugin](/id/plugins) yang diaktifkan muncul di typeahead dengan nama yang dibatasi, seperti `my-plugin:code-reviewer` atau `my-plugin:review:security` ketika plugin [mengorganisir agen ke dalam subfolder](#choose-the-subagent-scope). Subagent background bernama yang saat ini berjalan dalam sesi juga muncul di typeahead, menunjukkan status mereka di samping nama. Anda juga dapat mengetik mention secara manual tanpa menggunakan picker: `@agent-<name>` untuk subagent lokal, atau `@agent-` diikuti dengan nama yang dibatasi untuk subagent plugin, misalnya `@agent-my-plugin:code-reviewer`.

**Jalankan seluruh sesi sebagai subagent.** Lewatkan [`--agent <name>`](/id/cli-reference) untuk memulai sesi di mana thread utama itu sendiri mengambil prompt sistem subagent, pembatasan alat, dan model:

```bash theme={null}
claude --agent code-reviewer
```

Prompt sistem subagent menggantikan prompt sistem Claude Code default sepenuhnya, dengan cara yang sama [`--system-prompt`](/id/cli-reference) melakukannya. File `CLAUDE.md` dan memori proyek masih dimuat melalui aliran pesan normal. Nama agen muncul sebagai `@<name>` di header startup sehingga Anda dapat mengonfirmasi itu aktif.

Ini berfungsi dengan subagent bawaan dan khusus, dan pilihan bertahan ketika Anda melanjutkan sesi.

Untuk subagent yang disediakan plugin, Anda dapat melewatkan hanya nama agen dan Claude Code akan menemukannya:

```bash theme={null}
claude --agent security-reviewer
```

Jika beberapa plugin menyediakan agen dengan nama yang sama, lewatkan nama yang dibatasi untuk membedakan:

```bash theme={null}
claude --agent my-plugin:security-reviewer
```

Jika plugin menempatkan agen dalam subfolder dari direktori `agents/` nya, sertakan subfolder dalam nama yang dibatasi, misalnya `claude --agent my-plugin:review:security`.

Untuk menjadikannya default untuk setiap sesi dalam proyek, atur `agent` dalam `.claude/settings.json`:

```json theme={null}
{
  "agent": "code-reviewer"
}
```

Flag CLI menimpa pengaturan jika keduanya ada.

### Jalankan subagent di foreground atau background

Subagent dapat berjalan di foreground (blocking) atau background (concurrent):

* **Subagent foreground** memblokir percakapan utama sampai selesai. Prompt izin dilewatkan kepada Anda saat muncul.
* **Subagent background** berjalan secara bersamaan sementara Anda terus bekerja. Mereka berjalan dengan izin yang sudah diberikan dalam sesi dan auto-deny setiap panggilan alat yang sebaliknya akan meminta. Jika subagent background perlu mengajukan pertanyaan klarifikasi, panggilan alat itu gagal tetapi subagent terus.

Jika subagent background gagal karena izin yang hilang, Anda dapat memulai subagent foreground baru dengan tugas yang sama untuk mencoba lagi dengan prompt interaktif.

Claude memutuskan apakah akan menjalankan subagent di foreground atau background berdasarkan tugas. Anda juga dapat:

* Minta Claude untuk "run this in the background"
* Tekan **Ctrl+B** untuk menempatkan tugas yang sedang berjalan di background

Untuk menonaktifkan semua fungsionalitas background task, atur variabel lingkungan `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` ke `1`. Lihat [Environment variables](/id/env-vars).

Ketika [fork mode](#fork-the-current-conversation) diaktifkan, setiap spawn subagent berjalan di background terlepas dari bidang `background`. Fork masih menampilkan prompt izin di terminal Anda saat terjadi; subagent bernama auto-deny apa pun yang sebaliknya akan meminta, seperti dijelaskan di atas.

### Pola umum

#### Isolasi operasi volume tinggi

Salah satu penggunaan paling efektif untuk subagent adalah mengisolasi operasi yang menghasilkan jumlah output besar. Menjalankan tes, mengambil dokumentasi, atau memproses file log dapat mengonsumsi konteks yang signifikan. Dengan mendelegasikan ini ke subagent, output verbose tetap dalam konteks subagent sementara hanya ringkasan relevan yang kembali ke percakapan utama Anda.

```text theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Jalankan penelitian paralel

Untuk investigasi independen, hasilkan beberapa subagent untuk bekerja secara bersamaan:

```text theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Setiap subagent mengeksplorasi areanya secara independen, kemudian Claude mensintesis temuan. Ini berfungsi terbaik ketika jalur penelitian tidak saling bergantung.

<Warning>
  Ketika subagent selesai, hasil mereka kembali ke percakapan utama Anda. Menjalankan banyak subagent yang masing-masing mengembalikan hasil terperinci dapat mengonsumsi konteks yang signifikan.
</Warning>

Untuk tugas yang memerlukan paralelisme berkelanjutan atau melebihi jendela konteks Anda, [tim agen](/id/agent-teams) memberikan setiap pekerja konteksnya sendiri yang independen.

#### Rantai subagent

Untuk alur kerja multi-langkah, minta Claude untuk menggunakan subagent secara berurutan. Setiap subagent menyelesaikan tugasnya dan mengembalikan hasil ke Claude, yang kemudian melewatkan konteks relevan ke subagent berikutnya.

```text theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Pilih antara subagent dan percakapan utama

Gunakan **percakapan utama** ketika:

* Tugas memerlukan bolak-balik yang sering atau penyempurnaan iteratif
* Beberapa fase berbagi konteks yang signifikan (perencanaan → implementasi → pengujian)
* Anda membuat perubahan cepat dan tertarget
* Latensi penting. Subagent dimulai segar dan mungkin memerlukan waktu untuk mengumpulkan konteks

Gunakan **subagent** ketika:

* Tugas menghasilkan output verbose yang Anda tidak butuhkan dalam konteks utama Anda
* Anda ingin menerapkan pembatasan alat atau izin tertentu
* Pekerjaan mandiri dan dapat mengembalikan ringkasan

Pertimbangkan [Skills](/id/skills) sebagai gantinya ketika Anda menginginkan prompt atau alur kerja yang dapat digunakan kembali yang berjalan dalam konteks percakapan utama daripada konteks subagent yang terisolasi.

Untuk pertanyaan cepat tentang sesuatu yang sudah ada dalam percakapan Anda, gunakan [`/btw`](/id/interactive-mode#side-questions-with-%2Fbtw) sebagai gantinya dari subagent. Ini melihat konteks penuh Anda tetapi tidak memiliki akses alat, dan jawabannya dibuang daripada ditambahkan ke riwayat.

<Note>
  Subagent tidak dapat menelurkan subagent lain. Jika alur kerja Anda memerlukan delegasi bersarang, gunakan [Skills](/id/skills) atau [rantai subagent](#chain-subagents) dari percakapan utama.
</Note>

### Kelola konteks subagent

#### Apa yang dimuat saat startup

Setiap subagent dimulai dengan jendela konteks yang segar dan terisolasi. Ini tidak melihat riwayat percakapan Anda, skills yang sudah Anda panggil, atau file yang sudah Claude baca. Claude menyusun pesan delegasi yang merangkum tugas, dan subagent bekerja dari sana. Pengecualiannya adalah [fork](#fork-the-current-conversation), yang mewarisi percakapan induk daripada memulai segar.

Konteks awal subagent non-fork berisi:

* **Prompt sistem**: prompt agen itu sendiri ditambah detail lingkungan yang Claude Code tambahkan, bukan prompt sistem Claude Code lengkap. Subagent khusus mendefinisikan milik mereka dalam [badan markdown](#write-subagent-files) atau bidang `prompt`. Agen bawaan memiliki prompt yang telah ditentukan sebelumnya.
* **Pesan tugas**: prompt delegasi yang Claude tulis ketika menyerahkan pekerjaan.
* **CLAUDE.md dan memori**: setiap level dari [hierarki memori](/id/memory#how-claude-md-files-load) yang dimuat percakapan utama, termasuk `~/.claude/CLAUDE.md`, aturan proyek, `CLAUDE.local.md`, dan file kebijakan yang dikelola. Agen Explore dan Plan bawaan melewati ini.
* **Status Git**: snapshot yang diambil di awal sesi induk. Tidak ada ketika direktori kerja bukan repositori Git atau ketika [`includeGitInstructions`](/id/settings#available-settings) adalah `false`. Explore dan Plan melewatinya terlepas.
* **Skills yang dimuat sebelumnya**: konten lengkap dari skill apa pun yang dinamai dalam bidang [`skills`](#preload-skills-into-subagents) agen. Agen bawaan tidak memuat skills sebelumnya.

Explore dan Plan adalah satu-satunya subagent yang menghilangkan CLAUDE.md dan status git. Tidak ada bidang frontmatter atau pengaturan per-agen untuk mengubah agen mana yang melewatinya.

Percakapan utama membaca hasil Explore dan Plan dengan konteks CLAUDE.md penuh, jadi sebagian besar aturan tidak perlu mencapai subagent itu sendiri. Jika aturan harus, seperti "abaikan direktori `vendor/`," nyatakan kembali dalam prompt yang Anda berikan Claude saat mendelegasikan.

#### Lanjutkan subagent

Setiap invokasi subagent membuat instance baru dengan konteks segar. Untuk melanjutkan pekerjaan subagent yang ada daripada memulai dari awal, minta Claude untuk melanjutkannya.

Subagent yang dilanjutkan mempertahankan riwayat percakapan lengkap mereka, termasuk semua panggilan alat sebelumnya, hasil, dan penalaran. Subagent melanjutkan tepat di mana ia berhenti daripada memulai segar.

Ketika subagent selesai, Claude menerima ID agennya. Claude menggunakan alat `SendMessage` dengan ID agen sebagai bidang `to` untuk melanjutkannya. Alat `SendMessage` hanya tersedia ketika [tim agen](/id/agent-teams) diaktifkan melalui `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Untuk melanjutkan subagent, minta Claude untuk melanjutkan pekerjaan sebelumnya:

```text theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Jika subagent yang dihentikan menerima `SendMessage`, ia auto-resume di background tanpa memerlukan invokasi `Agent` baru.

Anda juga dapat meminta Claude untuk ID agen jika Anda ingin mereferensikannya secara eksplisit, atau temukan ID dalam file transkrip di `~/.claude/projects/{project}/{sessionId}/subagents/`. Setiap transkrip disimpan sebagai `agent-{agentId}.jsonl`.

Transkrip subagent bertahan secara independen dari percakapan utama:

* **Pemadatan percakapan utama**: Ketika percakapan utama dipadatkan, transkrip subagent tidak terpengaruh. Mereka disimpan dalam file terpisah.
* **Persistensi sesi**: Transkrip subagent bertahan dalam sesi mereka. Anda dapat [melanjutkan subagent](#resume-subagents) setelah memulai ulang Claude Code dengan melanjutkan sesi yang sama.
* **Pembersihan otomatis**: Transkrip dibersihkan berdasarkan pengaturan `cleanupPeriodDays` (default: 30 hari).

#### Auto-compaction

Subagent mendukung pemadatan otomatis menggunakan logika yang sama dengan percakapan utama. Secara default, auto-compaction dipicu pada kapasitas sekitar 95%. Untuk memicu pemadatan lebih awal, atur `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` ke persentase yang lebih rendah (misalnya, `50`). Lihat [environment variables](/id/env-vars) untuk detail.

Peristiwa pemadatan dicatat dalam file transkrip subagent:

```json theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

Nilai `preTokens` menunjukkan berapa banyak token yang digunakan sebelum pemadatan terjadi.

## Fork percakapan saat ini

<Note>
  Subagent yang di-fork bersifat eksperimental dan memerlukan Claude Code v2.1.117 atau lebih baru. Perilaku dan konfigurasi mungkin berubah di rilis mendatang. Aktifkan mereka dengan menetapkan variabel lingkungan [`CLAUDE_CODE_FORK_SUBAGENT`](/id/env-vars) ke `1`. Variabel ini dihormati dalam mode interaktif dan melalui SDK atau `claude -p`.
</Note>

Fork adalah subagent yang mewarisi seluruh percakapan sejauh ini daripada memulai segar. Ini menghilangkan isolasi input yang sebaliknya disediakan subagent: fork melihat prompt sistem yang sama, alat, model, dan riwayat pesan sebagai sesi utama, sehingga Anda dapat menyerahkan tugas sampingan tanpa menjelaskan situasinya lagi. Panggilan alat fork sendiri masih tetap keluar dari percakapan Anda dan hanya hasil akhirnya yang kembali, sehingga jendela konteks utama Anda tetap bersih. Gunakan fork ketika subagent bernama memerlukan terlalu banyak latar belakang untuk berguna, atau ketika Anda ingin mencoba beberapa pendekatan secara paralel dari titik awal yang sama.

Mengaktifkan fork mode mengubah Claude Code dalam tiga cara:

* Claude menelurkan fork setiap kali Claude akan menggunakan subagent [general-purpose](#built-in-subagents). Subagent bernama seperti Explore masih menelurkan seperti sebelumnya.
* Setiap spawn subagent berjalan di [background](#run-subagents-in-foreground-or-background), apakah itu fork atau subagent bernama. Atur `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` ke `1` untuk menjaga spawn tetap sinkron.
* Perintah `/fork` menelurkan fork daripada bertindak sebagai alias untuk [`/branch`](/id/commands).

Anda dapat memulai fork sendiri dengan `/fork` diikuti oleh direktif. Claude Code memberi nama fork dari kata-kata pertama direktif. Contoh berikut mem-fork percakapan untuk draft kasus uji sementara Anda melanjutkan dengan implementasi dalam sesi utama:

```text theme={null}
/fork draft unit tests for the parser changes so far
```

Fork muncul di panel di bawah prompt Anda dan berjalan di background sementara Anda terus bekerja. Ketika selesai, hasilnya tiba sebagai pesan dalam percakapan utama Anda. Bagian berikutnya mencakup kontrol panel untuk menonton dan mengarahkan fork saat berjalan.

### Amati dan arahkan fork yang sedang berjalan

Fork yang sedang berjalan muncul di panel di bawah input prompt, dengan satu baris untuk sesi utama dan satu untuk setiap fork. Gunakan kunci ini untuk berinteraksi dengan panel:

| Kunci     | Tindakan                                                          |
| :-------- | :---------------------------------------------------------------- |
| `↑` / `↓` | Pindah antar baris                                                |
| `Enter`   | Buka transkrip fork yang dipilih dan kirimkan pesan tindak lanjut |
| `x`       | Tutup fork yang selesai atau hentikan yang sedang berjalan        |
| `Esc`     | Kembalikan fokus ke input prompt                                  |

### Bagaimana fork berbeda dari subagent bernama

Fork mewarisi segalanya yang dimiliki sesi utama pada saat spawn. Subagent bernama dimulai dari definisinya sendiri.

|                        | Fork                           | Subagent bernama                                                                        |
| :--------------------- | :----------------------------- | :-------------------------------------------------------------------------------------- |
| Konteks                | Riwayat percakapan lengkap     | Konteks segar dengan prompt yang Anda lewatkan                                          |
| Prompt sistem dan alat | Sama dengan sesi utama         | Dari [file definisi](#write-subagent-files) subagent                                    |
| Model                  | Sama dengan sesi utama         | Dari bidang `model` subagent                                                            |
| Izin                   | Prompt muncul di terminal Anda | [Pra-disetujui](#run-subagents-in-foreground-or-background) saat berjalan di background |
| Prompt cache           | Dibagikan dengan sesi utama    | Cache terpisah                                                                          |

Karena prompt sistem fork dan definisi alat identik dengan induk, permintaan pertamanya menggunakan kembali cache prompt induk. Ini membuat forking lebih murah daripada menelurkan subagent segar untuk tugas yang memerlukan konteks yang sama.

Ketika Claude menelurkan fork melalui alat Agent, Claude dapat melewatkan `isolation: "worktree"` sehingga edit file fork ditulis ke git worktree terpisah daripada checkout Anda.

### Keterbatasan

Menetapkan `CLAUDE_CODE_FORK_SUBAGENT=1` mengaktifkan fork mode dalam sesi interaktif, [non-interactive mode](/id/headless), dan Agent SDK. Fork tidak dapat menelurkan fork lebih lanjut.

## Contoh subagent

Contoh-contoh ini mendemonstrasikan pola efektif untuk membangun subagent. Gunakan mereka sebagai titik awal, atau hasilkan versi yang disesuaikan dengan Claude.

<Tip>
  **Best practices:**

  * **Desain subagent yang terfokus:** setiap subagent harus unggul dalam satu tugas spesifik
  * **Tulis deskripsi terperinci:** Claude menggunakan deskripsi untuk memutuskan kapan mendelegasikan
  * **Batasi akses alat:** berikan hanya izin yang diperlukan untuk keamanan dan fokus
  * **Periksa ke dalam kontrol versi:** bagikan subagent proyek dengan tim Anda
</Tip>

### Peninjau kode

Subagent hanya-baca yang meninjau kode tanpa memodifikasinya. Contoh ini menunjukkan cara merancang subagent yang terfokus dengan akses alat terbatas (tidak ada Edit atau Write) dan prompt terperinci yang menentukan dengan tepat apa yang harus dicari dan cara memformat output.

```markdown theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

Subagent yang dapat menganalisis dan memperbaiki masalah. Tidak seperti peninjau kode, yang ini mencakup Edit karena memperbaiki bug memerlukan memodifikasi kode. Prompt menyediakan alur kerja yang jelas dari diagnosis ke verifikasi.

```markdown theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data scientist

Subagent khusus domain untuk pekerjaan analisis data. Contoh ini menunjukkan cara membuat subagent untuk alur kerja khusus di luar tugas pengkodean khas. Ini secara eksplisit menetapkan `model: sonnet` untuk analisis yang lebih mampu.

```markdown theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Validator kueri database

Subagent yang memungkinkan akses Bash tetapi memvalidasi perintah untuk mengizinkan hanya kueri SQL hanya-baca. Contoh ini menunjukkan cara menggunakan hooks `PreToolUse` untuk validasi bersyarat ketika Anda memerlukan kontrol lebih halus daripada bidang `tools`.

```markdown theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [melewatkan input hook sebagai JSON](/id/hooks#pretooluse-input) melalui stdin ke perintah hook. Skrip validasi membaca JSON ini, mengekstrak perintah yang sedang dijalankan, dan memeriksanya terhadap daftar operasi penulisan SQL. Jika operasi penulisan terdeteksi, skrip [keluar dengan kode 2](/id/hooks#exit-code-2-behavior-per-event) untuk memblokir eksekusi dan mengembalikan pesan kesalahan ke Claude melalui stderr.

Buat skrip validasi di mana saja dalam proyek Anda. Jalur harus cocok dengan bidang `command` dalam konfigurasi hook Anda:

```bash theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

Di macOS dan Linux, buat skrip dapat dieksekusi:

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

Di Windows, tulis skrip validasi dalam PowerShell dan tambahkan `shell: powershell` ke entri hook. Lihat [menjalankan hooks dalam PowerShell](/id/hooks#windows-powershell-tool).

Hook menerima JSON melalui stdin dengan perintah Bash dalam `tool_input.command`. Kode keluar 2 memblokir operasi dan mengirimkan pesan kesalahan kembali ke Claude. Lihat [Hooks](/id/hooks#exit-code-output) untuk detail tentang kode keluar dan [Hook input](/id/hooks#pretooluse-input) untuk skema input lengkap.

## Langkah berikutnya

Sekarang setelah Anda memahami subagent, jelajahi fitur terkait ini:

* [Distribusikan subagent dengan plugins](/id/plugins) untuk berbagi subagent di seluruh tim atau proyek
* [Jalankan Claude Code secara terprogram](/id/headless) dengan Agent SDK untuk CI/CD dan otomasi
* [Gunakan MCP servers](/id/mcp) untuk memberikan subagent akses ke alat dan data eksternal
