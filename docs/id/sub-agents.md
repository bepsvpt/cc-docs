> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Buat subagent khusus

> Buat dan gunakan subagent AI khusus di Claude Code untuk alur kerja khusus tugas dan manajemen konteks yang lebih baik.

Subagent adalah asisten AI khusus yang menangani jenis tugas tertentu. Setiap subagent berjalan di jendela konteksnya sendiri dengan prompt sistem khusus, akses alat tertentu, dan izin independen. Ketika Claude menemukan tugas yang sesuai dengan deskripsi subagent, Claude mendelegasikan ke subagent tersebut, yang bekerja secara independen dan mengembalikan hasil.

<Note>
  Jika Anda memerlukan beberapa agen yang bekerja secara paralel dan berkomunikasi satu sama lain, lihat [tim agen](/id/agent-teams) sebagai gantinya. Subagent bekerja dalam satu sesi; tim agen mengoordinasikan di seluruh sesi terpisah.
</Note>

Subagent membantu Anda:

* **Mempertahankan konteks** dengan menjaga eksplorasi dan implementasi di luar percakapan utama Anda
* **Menerapkan batasan** dengan membatasi alat mana yang dapat digunakan subagent
* **Menggunakan kembali konfigurasi** di seluruh proyek dengan subagent tingkat pengguna
* **Mengkhususkan perilaku** dengan prompt sistem yang terfokus untuk domain tertentu
* **Mengontrol biaya** dengan merutekan tugas ke model yang lebih cepat dan lebih murah seperti Haiku

Claude menggunakan deskripsi setiap subagent untuk memutuskan kapan mendelegasikan tugas. Ketika Anda membuat subagent, tulis deskripsi yang jelas sehingga Claude tahu kapan menggunakannya.

Claude Code mencakup beberapa subagent bawaan seperti **Explore**, **Plan**, dan **general-purpose**. Anda juga dapat membuat subagent khusus untuk menangani tugas tertentu. Halaman ini mencakup [subagent bawaan](#built-in-subagents), [cara membuat subagent Anda sendiri](#quickstart-create-your-first-subagent), [opsi konfigurasi lengkap](#configure-subagents), [pola untuk bekerja dengan subagent](#work-with-subagents), dan [contoh subagent](#example-subagents).

## Subagent bawaan

Claude Code mencakup subagent bawaan yang Claude gunakan secara otomatis jika sesuai. Masing-masing mewarisi izin percakapan induk dengan pembatasan alat tambahan.

<Tabs>
  <Tab title="Explore">
    Agen cepat yang dioptimalkan hanya-baca untuk mencari dan menganalisis basis kode.

    * **Model**: Haiku (cepat, latensi rendah)
    * **Alat**: Alat hanya-baca (akses ditolak ke alat Write dan Edit)
    * **Tujuan**: Penemuan file, pencarian kode, eksplorasi basis kode

    Claude mendelegasikan ke Explore ketika perlu mencari atau memahami basis kode tanpa membuat perubahan. Ini menjaga hasil eksplorasi di luar konteks percakapan utama Anda.

    Saat memanggil Explore, Claude menentukan tingkat ketelitian: **quick** untuk pencarian yang ditargetkan, **medium** untuk eksplorasi seimbang, atau **very thorough** untuk analisis komprehensif.
  </Tab>

  <Tab title="Plan">
    Agen penelitian yang digunakan selama [plan mode](/id/common-workflows#use-plan-mode-for-safe-code-analysis) untuk mengumpulkan konteks sebelum menyajikan rencana.

    * **Model**: Mewarisi dari percakapan utama
    * **Alat**: Alat hanya-baca (akses ditolak ke alat Write dan Edit)
    * **Tujuan**: Penelitian basis kode untuk perencanaan

    Ketika Anda dalam plan mode dan Claude perlu memahami basis kode Anda, Claude mendelegasikan penelitian ke subagent Plan. Ini mencegah nesting tak terbatas (subagent tidak dapat menelurkan subagent lain) sambil tetap mengumpulkan konteks yang diperlukan.
  </Tab>

  <Tab title="General-purpose">
    Agen yang mampu untuk tugas kompleks multi-langkah yang memerlukan eksplorasi dan tindakan.

    * **Model**: Mewarisi dari percakapan utama
    * **Alat**: Semua alat
    * **Tujuan**: Penelitian kompleks, operasi multi-langkah, modifikasi kode

    Claude mendelegasikan ke general-purpose ketika tugas memerlukan eksplorasi dan modifikasi, penalaran kompleks untuk menafsirkan hasil, atau beberapa langkah yang saling bergantung.
  </Tab>

  <Tab title="Other">
    Claude Code mencakup agen pembantu tambahan untuk tugas tertentu. Ini biasanya dipanggil secara otomatis, jadi Anda tidak perlu menggunakannya secara langsung.

    | Agen              | Model    | Kapan Claude menggunakannya                                                  |
    | :---------------- | :------- | :--------------------------------------------------------------------------- |
    | Bash              | Mewarisi | Menjalankan perintah terminal dalam konteks terpisah                         |
    | statusline-setup  | Sonnet   | Ketika Anda menjalankan `/statusline` untuk mengonfigurasi baris status Anda |
    | Claude Code Guide | Haiku    | Ketika Anda mengajukan pertanyaan tentang fitur Claude Code                  |
  </Tab>
</Tabs>

Selain subagent bawaan ini, Anda dapat membuat subagent Anda sendiri dengan prompt khusus, pembatasan alat, mode izin, hooks, dan skills. Bagian berikut menunjukkan cara memulai dan menyesuaikan subagent.

## Quickstart: buat subagent pertama Anda

Subagent didefinisikan dalam file Markdown dengan frontmatter YAML. Anda dapat [membuatnya secara manual](#write-subagent-files) atau menggunakan perintah `/agents`.

Panduan ini memandu Anda melalui pembuatan subagent tingkat pengguna dengan perintah `/agents`. Subagent meninjau kode dan menyarankan perbaikan untuk basis kode.

<Steps>
  <Step title="Buka antarmuka subagent">
    Di Claude Code, jalankan:

    ```text  theme={null}
    /agents
    ```
  </Step>

  <Step title="Pilih lokasi">
    Pilih **Create new agent**, kemudian pilih **Personal**. Ini menyimpan subagent ke `~/.claude/agents/` sehingga tersedia di semua proyek Anda.
  </Step>

  <Step title="Hasilkan dengan Claude">
    Pilih **Generate with Claude**. Ketika diminta, jelaskan subagent:

    ```text  theme={null}
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

    ```text  theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude mendelegasikan ke subagent baru Anda, yang memindai basis kode dan mengembalikan saran perbaikan.
  </Step>
</Steps>

Anda sekarang memiliki subagent yang dapat Anda gunakan di proyek apa pun di mesin Anda untuk menganalisis basis kode dan menyarankan perbaikan.

Anda juga dapat membuat subagent secara manual sebagai file Markdown, mendefinisikannya melalui flag CLI, atau mendistribusikannya melalui plugins. Bagian berikut mencakup semua opsi konfigurasi.

## Konfigurasi subagent

### Gunakan perintah /agents

Perintah `/agents` menyediakan antarmuka interaktif untuk mengelola subagent. Jalankan `/agents` untuk:

* Melihat semua subagent yang tersedia (bawaan, pengguna, proyek, dan plugin)
* Membuat subagent baru dengan setup terpandu atau generasi Claude
* Mengedit konfigurasi subagent yang ada dan akses alat
* Menghapus subagent khusus
* Melihat subagent mana yang aktif ketika duplikat ada

Ini adalah cara yang direkomendasikan untuk membuat dan mengelola subagent. Untuk pembuatan manual atau otomasi, Anda juga dapat menambahkan file subagent secara langsung.

Untuk membuat daftar semua subagent yang dikonfigurasi dari baris perintah tanpa memulai sesi interaktif, jalankan `claude agents`. Ini menunjukkan agen yang dikelompokkan berdasarkan sumber dan menunjukkan mana yang ditimpa oleh definisi prioritas lebih tinggi.

### Pilih cakupan subagent

Subagent adalah file Markdown dengan frontmatter YAML. Simpan mereka di lokasi berbeda tergantung cakupan. Ketika beberapa subagent berbagi nama yang sama, lokasi prioritas lebih tinggi menang.

| Lokasi                     | Cakupan                  | Prioritas     | Cara membuat                               |
| :------------------------- | :----------------------- | :------------ | :----------------------------------------- |
| Flag CLI `--agents`        | Sesi saat ini            | 1 (tertinggi) | Lewatkan JSON saat meluncurkan Claude Code |
| `.claude/agents/`          | Proyek saat ini          | 2             | Interaktif atau manual                     |
| `~/.claude/agents/`        | Semua proyek Anda        | 3             | Interaktif atau manual                     |
| Direktori `agents/` plugin | Tempat plugin diaktifkan | 4 (terendah)  | Diinstal dengan [plugins](/id/plugins)     |

**Subagent proyek** (`.claude/agents/`) ideal untuk subagent khusus untuk basis kode. Periksa mereka ke kontrol versi sehingga tim Anda dapat menggunakannya dan meningkatkannya secara kolaboratif.

**Subagent pengguna** (`~/.claude/agents/`) adalah subagent pribadi yang tersedia di semua proyek Anda.

**Subagent yang ditentukan CLI** dilewatkan sebagai JSON saat meluncurkan Claude Code. Mereka hanya ada untuk sesi itu dan tidak disimpan ke disk, menjadikannya berguna untuk pengujian cepat atau skrip otomasi. Anda dapat mendefinisikan beberapa subagent dalam satu panggilan `--agents`:

```bash  theme={null}
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

Flag `--agents` menerima JSON dengan [frontmatter](#supported-frontmatter-fields) yang sama bidang file-based subagent: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, dan `isolation`. Gunakan `prompt` untuk prompt sistem, setara dengan badan markdown dalam subagent berbasis file.

**Subagent plugin** berasal dari [plugins](/id/plugins) yang telah Anda instal. Mereka muncul di `/agents` bersama subagent khusus Anda. Lihat [referensi komponen plugin](/id/plugins-reference#agents) untuk detail tentang membuat subagent plugin.

<Note>
  Untuk alasan keamanan, subagent plugin tidak mendukung bidang frontmatter `hooks`, `mcpServers`, atau `permissionMode`. Bidang-bidang ini diabaikan saat memuat agen dari plugin. Jika Anda membutuhkannya, salin file agen ke dalam `.claude/agents/` atau `~/.claude/agents/`. Anda juga dapat menambahkan aturan ke [`permissions.allow`](/id/settings#permission-settings) dalam `settings.json` atau `settings.local.json`, tetapi aturan-aturan ini berlaku untuk seluruh sesi, bukan hanya subagent plugin.
</Note>

### Tulis file subagent

File subagent menggunakan frontmatter YAML untuk konfigurasi, diikuti oleh prompt sistem dalam Markdown:

<Note>
  Subagent dimuat saat awal sesi. Jika Anda membuat subagent dengan menambahkan file secara manual, restart sesi Anda atau gunakan `/agents` untuk memuatnya segera.
</Note>

```markdown  theme={null}
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

#### Bidang frontmatter yang didukung

Bidang berikut dapat digunakan dalam frontmatter YAML. Hanya `name` dan `description` yang diperlukan.

| Bidang            | Diperlukan | Deskripsi                                                                                                                                                                                                                                                                                             |
| :---------------- | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Ya         | Pengenal unik menggunakan huruf kecil dan tanda hubung                                                                                                                                                                                                                                                |
| `description`     | Ya         | Kapan Claude harus mendelegasikan ke subagent ini                                                                                                                                                                                                                                                     |
| `tools`           | Tidak      | [Alat](#available-tools) yang dapat digunakan subagent. Mewarisi semua alat jika dihilangkan                                                                                                                                                                                                          |
| `disallowedTools` | Tidak      | Alat untuk ditolak, dihapus dari daftar yang diwarisi atau ditentukan                                                                                                                                                                                                                                 |
| `model`           | Tidak      | [Model](#choose-a-model) untuk digunakan: `sonnet`, `opus`, `haiku`, ID model lengkap (misalnya, `claude-opus-4-6`), atau `inherit`. Default ke `inherit`                                                                                                                                             |
| `permissionMode`  | Tidak      | [Mode izin](#permission-modes): `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, atau `plan`                                                                                                                                                                                                 |
| `maxTurns`        | Tidak      | Jumlah maksimum putaran agentic sebelum subagent berhenti                                                                                                                                                                                                                                             |
| `skills`          | Tidak      | [Skills](/id/skills) untuk dimuat ke dalam konteks subagent saat startup. Konten skill lengkap disuntikkan, bukan hanya tersedia untuk invokasi. Subagent tidak mewarisi skills dari percakapan induk                                                                                                 |
| `mcpServers`      | Tidak      | [MCP servers](/id/mcp) tersedia untuk subagent ini. Setiap entri adalah nama server yang mereferensikan server yang sudah dikonfigurasi (misalnya, `"slack"`) atau definisi inline dengan nama server sebagai kunci dan [konfigurasi MCP server](/id/mcp#configure-mcp-servers) lengkap sebagai nilai |
| `hooks`           | Tidak      | [Lifecycle hooks](#define-hooks-for-subagents) yang dibatasi pada subagent ini                                                                                                                                                                                                                        |
| `memory`          | Tidak      | [Cakupan memori persisten](#enable-persistent-memory): `user`, `project`, atau `local`. Memungkinkan pembelajaran lintas sesi                                                                                                                                                                         |
| `background`      | Tidak      | Atur ke `true` untuk selalu menjalankan subagent ini sebagai [background task](#run-subagents-in-foreground-or-background). Default: `false`                                                                                                                                                          |
| `effort`          | Tidak      | Tingkat usaha ketika subagent ini aktif. Menimpa tingkat usaha sesi. Default: mewarisi dari sesi. Opsi: `low`, `medium`, `high`, `max` (Opus 4.6 saja)                                                                                                                                                |
| `isolation`       | Tidak      | Atur ke `worktree` untuk menjalankan subagent dalam [git worktree](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) sementara, memberikannya salinan repositori yang terisolasi. Worktree secara otomatis dibersihkan jika subagent tidak membuat perubahan                 |
| `initialPrompt`   | Tidak      | Auto-submitted sebagai putaran pengguna pertama ketika agen ini berjalan sebagai agen sesi utama (melalui `--agent` atau pengaturan `agent`). [Commands](/id/commands) dan [skills](/id/skills) diproses. Ditambahkan di depan prompt yang disediakan pengguna apa pun                                |

### Pilih model

Bidang `model` mengontrol [model AI](/id/model-config) mana yang digunakan subagent:

* **Alias model**: Gunakan salah satu alias yang tersedia: `sonnet`, `opus`, atau `haiku`
* **ID model lengkap**: Gunakan ID model lengkap seperti `claude-opus-4-6` atau `claude-sonnet-4-6`. Menerima nilai yang sama dengan flag `--model`
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

```yaml  theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Contoh ini menggunakan `disallowedTools` untuk mewarisi setiap alat dari percakapan utama kecuali Write dan Edit. Subagent menyimpan Bash, alat MCP, dan semuanya yang lain:

```yaml  theme={null}
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

```yaml  theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Ini adalah allowlist: hanya subagent `worker` dan `researcher` yang dapat dihasilkan. Jika agen mencoba menelurkan jenis lain, permintaan gagal dan agen hanya melihat jenis yang diizinkan dalam promptnya. Untuk memblokir agen tertentu sambil mengizinkan semua yang lain, gunakan [`permissions.deny`](#disable-specific-subagents) sebagai gantinya.

Untuk mengizinkan penelur subagent apa pun tanpa pembatasan, gunakan `Agent` tanpa tanda kurung:

```yaml  theme={null}
tools: Agent, Read, Bash
```

Jika `Agent` dihilangkan dari daftar `tools` sepenuhnya, agen tidak dapat menelurkan subagent apa pun. Pembatasan ini hanya berlaku untuk agen yang berjalan sebagai thread utama dengan `claude --agent`. Subagent tidak dapat menelurkan subagent lain, jadi `Agent(agent_type)` tidak berpengaruh dalam definisi subagent.

#### Cakupan MCP servers ke subagent

Gunakan bidang `mcpServers` untuk memberikan subagent akses ke [MCP](/id/mcp) servers yang tidak tersedia dalam percakapan utama. Server inline yang ditentukan di sini terhubung saat subagent dimulai dan terputus saat selesai. Referensi string berbagi koneksi sesi induk.

Setiap entri dalam daftar adalah definisi server inline atau string yang mereferensikan MCP server yang sudah dikonfigurasi dalam sesi Anda:

```yaml  theme={null}
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

| Mode                | Perilaku                                                                      |
| :------------------ | :---------------------------------------------------------------------------- |
| `default`           | Pemeriksaan izin standar dengan prompt                                        |
| `acceptEdits`       | Auto-terima edit file                                                         |
| `dontAsk`           | Auto-tolak prompt izin (alat yang secara eksplisit diizinkan masih berfungsi) |
| `bypassPermissions` | Lewati prompt izin                                                            |
| `plan`              | Plan mode (eksplorasi hanya-baca)                                             |

<Warning>
  Gunakan `bypassPermissions` dengan hati-hati. Ini melewati prompt izin, memungkinkan subagent untuk menjalankan operasi tanpa persetujuan. Penulisan ke direktori `.git`, `.claude`, `.vscode`, dan `.idea` masih meminta konfirmasi, kecuali untuk `.claude/commands`, `.claude/agents`, dan `.claude/skills`. Lihat [permission modes](/id/permission-modes#skip-all-checks-with-bypasspermissions-mode) untuk detail.
</Warning>

Jika induk menggunakan `bypassPermissions`, ini mengambil alih dan tidak dapat ditimpa. Jika induk menggunakan [auto mode](/id/permission-modes#eliminate-prompts-with-auto-mode), subagent mewarisi auto mode dan `permissionMode` apa pun dalam frontmatternya diabaikan: pengklasifikasi mengevaluasi panggilan alat subagent dengan aturan blok dan izin yang sama dengan sesi induk.

#### Preload skills ke dalam subagent

Gunakan bidang `skills` untuk menyuntikkan konten skill ke dalam konteks subagent saat startup. Ini memberikan subagent pengetahuan domain tanpa memerlukan penemuan dan pemuatan skills selama eksekusi.

```yaml  theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

Konten lengkap setiap skill disuntikkan ke dalam konteks subagent, bukan hanya tersedia untuk invokasi. Subagent tidak mewarisi skills dari percakapan induk; Anda harus mencantumkannya secara eksplisit.

<Note>
  Ini adalah kebalikan dari [menjalankan skill dalam subagent](/id/skills#run-skills-in-a-subagent). Dengan `skills` dalam subagent, subagent mengontrol prompt sistem dan memuat konten skill. Dengan `context: fork` dalam skill, konten skill disuntikkan ke dalam agen yang Anda tentukan. Keduanya menggunakan sistem yang mendasar yang sama.
</Note>

#### Aktifkan memori persisten

Bidang `memory` memberikan subagent direktori persisten yang bertahan di seluruh percakapan. Subagent menggunakan direktori ini untuk membangun pengetahuan seiring waktu, seperti pola basis kode, wawasan debugging, dan keputusan arsitektur.

```yaml  theme={null}
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
* Prompt sistem subagent juga mencakup 200 baris pertama `MEMORY.md` dalam direktori memori, dengan instruksi untuk mengkurasi `MEMORY.md` jika melebihi 200 baris.
* Alat Read, Write, dan Edit secara otomatis diaktifkan sehingga subagent dapat mengelola file memorinya.

##### Tips memori persisten

* `project` adalah cakupan default yang direkomendasikan. Ini membuat pengetahuan subagent dapat dibagikan melalui kontrol versi. Gunakan `user` ketika pengetahuan subagent berlaku secara luas di seluruh proyek, atau `local` ketika pengetahuan tidak boleh diperiksa ke dalam kontrol versi.
* Minta subagent untuk berkonsultasi dengan memorinya sebelum memulai pekerjaan: "Review PR ini, dan periksa memori Anda untuk pola yang telah Anda lihat sebelumnya."
* Minta subagent untuk memperbarui memorinya setelah menyelesaikan tugas: "Sekarang setelah Anda selesai, simpan apa yang Anda pelajari ke memori Anda." Seiring waktu, ini membangun basis pengetahuan yang membuat subagent lebih efektif.
* Sertakan instruksi memori langsung dalam file markdown subagent sehingga secara proaktif mempertahankan basis pengetahuannya sendiri:

  ```markdown  theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Aturan bersyarat dengan hooks

Untuk kontrol yang lebih dinamis atas penggunaan alat, gunakan hooks `PreToolUse` untuk memvalidasi operasi sebelum dijalankan. Ini berguna ketika Anda perlu mengizinkan beberapa operasi alat sambil memblokir yang lain.

Contoh ini membuat subagent yang hanya mengizinkan kueri database hanya-baca. Hook `PreToolUse` menjalankan skrip yang ditentukan dalam `command` sebelum setiap perintah Bash dijalankan:

```yaml  theme={null}
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

```bash  theme={null}
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

Lihat [Hook input](/id/hooks#pretooluse-input) untuk skema input lengkap dan [exit codes](/id/hooks#exit-code-output) untuk bagaimana kode keluar mempengaruhi perilaku.

#### Nonaktifkan subagent tertentu

Anda dapat mencegah Claude menggunakan subagent tertentu dengan menambahkannya ke array `deny` dalam [pengaturan](/id/settings#permission-settings) Anda. Gunakan format `Agent(subagent-name)` di mana `subagent-name` cocok dengan bidang nama subagent.

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Ini berfungsi untuk subagent bawaan dan khusus. Anda juga dapat menggunakan flag CLI `--disallowedTools`:

```bash  theme={null}
claude --disallowedTools "Agent(Explore)"
```

Lihat [dokumentasi Permissions](/id/permissions#tool-specific-permission-rules) untuk detail lebih lanjut tentang aturan izin.

### Tentukan hooks untuk subagent

Subagent dapat mendefinisikan [hooks](/id/hooks) yang berjalan selama siklus hidup subagent. Ada dua cara untuk mengonfigurasi hooks:

1. **Dalam frontmatter subagent**: Tentukan hooks yang hanya berjalan saat subagent tertentu itu aktif
2. **Dalam `settings.json`**: Tentukan hooks yang berjalan dalam sesi utama ketika subagent dimulai atau berhenti

#### Hooks dalam frontmatter subagent

Tentukan hooks langsung dalam file markdown subagent. Hooks ini hanya berjalan saat subagent spesifik itu aktif dan dibersihkan saat selesai.

Semua [hook events](/id/hooks#hook-events) didukung. Peristiwa paling umum untuk subagent adalah:

| Peristiwa     | Input Matcher | Kapan itu terjadi                                                   |
| :------------ | :------------ | :------------------------------------------------------------------ |
| `PreToolUse`  | Nama alat     | Sebelum subagent menggunakan alat                                   |
| `PostToolUse` | Nama alat     | Setelah subagent menggunakan alat                                   |
| `Stop`        | (tidak ada)   | Ketika subagent selesai (dikonversi ke `SubagentStop` saat runtime) |

Contoh ini memvalidasi perintah Bash dengan hook `PreToolUse` dan menjalankan linter setelah edit file dengan `PostToolUse`:

```yaml  theme={null}
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

```json  theme={null}
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

```text  theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention subagent.** Ketik `@` dan pilih subagent dari typeahead, dengan cara yang sama Anda @-mention file. Ini memastikan subagent tertentu berjalan daripada meninggalkan pilihan kepada Claude:

```text  theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Pesan lengkap Anda masih pergi ke Claude, yang menulis prompt tugas subagent berdasarkan apa yang Anda minta. @-mention mengontrol subagent mana yang Claude panggil, bukan prompt apa yang diterima.

Subagent yang disediakan oleh [plugin](/id/plugins) yang diaktifkan muncul di typeahead sebagai `<plugin-name>:<agent-name>`. Anda juga dapat mengetik mention secara manual tanpa menggunakan picker: `@agent-<name>` untuk subagent lokal, atau `@agent-<plugin-name>:<agent-name>` untuk subagent plugin.

**Jalankan seluruh sesi sebagai subagent.** Lewatkan [`--agent <name>`](/id/cli-reference) untuk memulai sesi di mana thread utama itu sendiri mengambil prompt sistem subagent, pembatasan alat, dan model:

```bash  theme={null}
claude --agent code-reviewer
```

Prompt sistem subagent menggantikan prompt sistem Claude Code default sepenuhnya, dengan cara yang sama [`--system-prompt`](/id/cli-reference) melakukannya. File `CLAUDE.md` dan memori proyek masih dimuat melalui aliran pesan normal. Nama agen muncul sebagai `@<name>` di header startup sehingga Anda dapat mengonfirmasi itu aktif.

Ini berfungsi dengan subagent bawaan dan khusus, dan pilihan bertahan ketika Anda melanjutkan sesi.

Untuk subagent yang disediakan plugin, lewatkan nama yang dibatasi: `claude --agent <plugin-name>:<agent-name>`.

Untuk menjadikannya default untuk setiap sesi dalam proyek, atur `agent` dalam `.claude/settings.json`:

```json  theme={null}
{
  "agent": "code-reviewer"
}
```

Flag CLI menimpa pengaturan jika keduanya ada.

### Jalankan subagent di foreground atau background

Subagent dapat berjalan di foreground (blocking) atau background (concurrent):

* **Subagent foreground** memblokir percakapan utama sampai selesai. Prompt izin dan pertanyaan klarifikasi (seperti [`AskUserQuestion`](/id/tools-reference)) dilewatkan kepada Anda.
* **Subagent background** berjalan secara bersamaan sementara Anda terus bekerja. Sebelum diluncurkan, Claude Code meminta izin alat apa pun yang akan dibutuhkan subagent, memastikan ia memiliki persetujuan yang diperlukan di muka. Setelah berjalan, subagent mewarisi izin ini dan auto-menolak apa pun yang tidak pra-disetujui. Jika subagent background perlu mengajukan pertanyaan klarifikasi, panggilan alat itu gagal tetapi subagent terus.

Jika subagent background gagal karena izin yang hilang, Anda dapat memulai subagent foreground baru dengan tugas yang sama untuk mencoba lagi dengan prompt interaktif.

Claude memutuskan apakah akan menjalankan subagent di foreground atau background berdasarkan tugas. Anda juga dapat:

* Minta Claude untuk "run this in the background"
* Tekan **Ctrl+B** untuk menempatkan tugas yang sedang berjalan di background

Untuk menonaktifkan semua fungsionalitas background task, atur variabel lingkungan `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` ke `1`. Lihat [Environment variables](/id/env-vars).

### Pola umum

#### Isolasi operasi volume tinggi

Salah satu penggunaan paling efektif untuk subagent adalah mengisolasi operasi yang menghasilkan jumlah output besar. Menjalankan tes, mengambil dokumentasi, atau memproses file log dapat mengonsumsi konteks yang signifikan. Dengan mendelegasikan ini ke subagent, output verbose tetap dalam konteks subagent sementara hanya ringkasan relevan yang kembali ke percakapan utama Anda.

```text  theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Jalankan penelitian paralel

Untuk investigasi independen, hasilkan beberapa subagent untuk bekerja secara bersamaan:

```text  theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Setiap subagent mengeksplorasi areanya secara independen, kemudian Claude mensintesis temuan. Ini berfungsi terbaik ketika jalur penelitian tidak saling bergantung.

<Warning>
  Ketika subagent selesai, hasil mereka kembali ke percakapan utama Anda. Menjalankan banyak subagent yang masing-masing mengembalikan hasil terperinci dapat mengonsumsi konteks yang signifikan.
</Warning>

Untuk tugas yang memerlukan paralelisme berkelanjutan atau melebihi jendela konteks Anda, [tim agen](/id/agent-teams) memberikan setiap pekerja konteksnya sendiri yang independen.

#### Rantai subagent

Untuk alur kerja multi-langkah, minta Claude untuk menggunakan subagent secara berurutan. Setiap subagent menyelesaikan tugasnya dan mengembalikan hasil ke Claude, yang kemudian melewatkan konteks relevan ke subagent berikutnya.

```text  theme={null}
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

Untuk pertanyaan cepat tentang sesuatu yang sudah ada dalam percakapan Anda, gunakan [`/btw`](/id/interactive-mode#side-questions-with-btw) sebagai gantinya dari subagent. Ini melihat konteks penuh Anda tetapi tidak memiliki akses alat, dan jawabannya dibuang daripada ditambahkan ke riwayat.

<Note>
  Subagent tidak dapat menelurkan subagent lain. Jika alur kerja Anda memerlukan delegasi bersarang, gunakan [Skills](/id/skills) atau [rantai subagent](#chain-subagents) dari percakapan utama.
</Note>

### Kelola konteks subagent

#### Lanjutkan subagent

Setiap invokasi subagent membuat instance baru dengan konteks segar. Untuk melanjutkan pekerjaan subagent yang ada daripada memulai dari awal, minta Claude untuk melanjutkannya.

Subagent yang dilanjutkan mempertahankan riwayat percakapan lengkap mereka, termasuk semua panggilan alat sebelumnya, hasil, dan penalaran. Subagent melanjutkan tepat di mana ia berhenti daripada memulai segar.

Ketika subagent selesai, Claude menerima ID agennya. Claude menggunakan alat `SendMessage` dengan ID agen sebagai bidang `to` untuk melanjutkannya. Untuk melanjutkan subagent, minta Claude untuk melanjutkan pekerjaan sebelumnya:

```text  theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Anda juga dapat meminta Claude untuk ID agen jika Anda ingin mereferensikannya secara eksplisit, atau temukan ID dalam file transkrip di `~/.claude/projects/{project}/{sessionId}/subagents/`. Setiap transkrip disimpan sebagai `agent-{agentId}.jsonl`.

Transkrip subagent bertahan secara independen dari percakapan utama:

* **Pemadatan percakapan utama**: Ketika percakapan utama dipadatkan, transkrip subagent tidak terpengaruh. Mereka disimpan dalam file terpisah.
* **Persistensi sesi**: Transkrip subagent bertahan dalam sesi mereka. Anda dapat [melanjutkan subagent](#resume-subagents) setelah memulai ulang Claude Code dengan melanjutkan sesi yang sama.
* **Pembersihan otomatis**: Transkrip dibersihkan berdasarkan pengaturan `cleanupPeriodDays` (default: 30 hari).

#### Auto-compaction

Subagent mendukung pemadatan otomatis menggunakan logika yang sama dengan percakapan utama. Secara default, auto-compaction dipicu pada kapasitas sekitar 95%. Untuk memicu pemadatan lebih awal, atur `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` ke persentase yang lebih rendah (misalnya, `50`). Lihat [environment variables](/id/env-vars) untuk detail.

Peristiwa pemadatan dicatat dalam file transkrip subagent:

```json  theme={null}
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

```markdown  theme={null}
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

```markdown  theme={null}
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

```markdown  theme={null}
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

```markdown  theme={null}
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

```bash  theme={null}
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

Buat skrip dapat dieksekusi:

```bash  theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

Hook menerima JSON melalui stdin dengan perintah Bash dalam `tool_input.command`. Kode keluar 2 memblokir operasi dan mengirimkan pesan kesalahan kembali ke Claude. Lihat [Hooks](/id/hooks#exit-code-output) untuk detail tentang kode keluar dan [Hook input](/id/hooks#pretooluse-input) untuk skema input lengkap.

## Langkah berikutnya

Sekarang setelah Anda memahami subagent, jelajahi fitur terkait ini:

* [Distribusikan subagent dengan plugins](/id/plugins) untuk berbagi subagent di seluruh tim atau proyek
* [Jalankan Claude Code secara terprogram](/id/headless) dengan Agent SDK untuk CI/CD dan otomasi
* [Gunakan MCP servers](/id/mcp) untuk memberikan subagent akses ke alat dan data eksternal
