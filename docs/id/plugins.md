> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Buat plugins

> Buat plugins kustom untuk memperluas Claude Code dengan skills, agents, hooks, dan MCP servers.

Plugins memungkinkan Anda memperluas Claude Code dengan fungsionalitas kustom yang dapat dibagikan di seluruh proyek dan tim. Panduan ini mencakup pembuatan plugins Anda sendiri dengan skills, agents, hooks, dan MCP servers.

Mencari untuk memasang plugins yang sudah ada? Lihat [Temukan dan pasang plugins](/id/discover-plugins). Untuk spesifikasi teknis lengkap, lihat [Referensi plugins](/id/plugins-reference).

## Kapan menggunakan plugins vs konfigurasi standalone

Claude Code mendukung dua cara untuk menambahkan skills, agents, dan hooks kustom:

| Pendekatan                                                  | Nama skill           | Terbaik untuk                                                                                                      |
| :---------------------------------------------------------- | :------------------- | :----------------------------------------------------------------------------------------------------------------- |
| **Standalone** (direktori `.claude/`)                       | `/hello`             | Alur kerja pribadi, kustomisasi khusus proyek, eksperimen cepat                                                    |
| **Plugins** (direktori dengan `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Berbagi dengan rekan kerja, distribusi ke komunitas, rilis dengan versi, dapat digunakan kembali di seluruh proyek |

**Gunakan konfigurasi standalone ketika**:

* Anda menyesuaikan Claude Code untuk satu proyek
* Konfigurasi bersifat pribadi dan tidak perlu dibagikan
* Anda bereksperimen dengan skills atau hooks sebelum mengemas mereka
* Anda menginginkan nama skill pendek seperti `/hello` atau `/deploy`

**Gunakan plugins ketika**:

* Anda ingin berbagi fungsionalitas dengan tim atau komunitas Anda
* Anda memerlukan skills/agents yang sama di seluruh beberapa proyek
* Anda menginginkan kontrol versi dan pembaruan mudah untuk ekstensi Anda
* Anda mendistribusikan melalui marketplace
* Anda tidak keberatan dengan skills yang diberi namespace seperti `/my-plugin:hello` (namespace mencegah konflik antara plugins)

<Tip>
  Mulai dengan konfigurasi standalone di `.claude/` untuk iterasi cepat, kemudian [konversi ke plugin](#convert-existing-configurations-to-plugins) ketika Anda siap untuk berbagi.
</Tip>

## Quickstart

Quickstart ini memandu Anda melalui pembuatan plugin dengan skill kustom. Anda akan membuat manifest (file konfigurasi yang mendefinisikan plugin Anda), menambahkan skill, dan mengujinya secara lokal menggunakan flag `--plugin-dir`.

### Prasyarat

* Claude Code [diinstal dan diautentikasi](/id/quickstart#step-1-install-claude-code)
* Claude Code versi 1.0.33 atau lebih baru (jalankan `claude --version` untuk memeriksa)

<Note>
  Jika Anda tidak melihat perintah `/plugin`, perbarui Claude Code ke versi terbaru. Lihat [Troubleshooting](/id/troubleshooting) untuk instruksi upgrade.
</Note>

### Buat plugin pertama Anda

<Steps>
  <Step title="Buat direktori plugin">
    Setiap plugin berada di direktorinya sendiri yang berisi manifest dan skills, agents, atau hooks Anda. Buat satu sekarang:

    ```bash  theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Buat manifest plugin">
    File manifest di `.claude-plugin/plugin.json` mendefinisikan identitas plugin Anda: nama, deskripsi, dan versinya. Claude Code menggunakan metadata ini untuk menampilkan plugin Anda di plugin manager.

    Buat direktori `.claude-plugin` di dalam folder plugin Anda:

    ```bash  theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Kemudian buat `my-first-plugin/.claude-plugin/plugin.json` dengan konten ini:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
    "name": "my-first-plugin",
    "description": "A greeting plugin to learn the basics",
    "version": "1.0.0",
    "author": {
    "name": "Your Name"
    }
    }
    ```

    | Field         | Tujuan                                                                                                     |
    | :------------ | :--------------------------------------------------------------------------------------------------------- |
    | `name`        | Pengidentifikasi unik dan namespace skill. Skills diawali dengan ini (misalnya, `/my-first-plugin:hello`). |
    | `description` | Ditampilkan di plugin manager saat menjelajahi atau memasang plugins.                                      |
    | `version`     | Lacak rilis menggunakan [semantic versioning](/id/plugins-reference#version-management).                   |
    | `author`      | Opsional. Membantu untuk atribusi.                                                                         |

    Untuk field tambahan seperti `homepage`, `repository`, dan `license`, lihat [skema manifest lengkap](/id/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Tambahkan skill">
    Skills berada di direktori `skills/`. Setiap skill adalah folder yang berisi file `SKILL.md`. Nama folder menjadi nama skill, diawali dengan namespace plugin (`hello/` dalam plugin bernama `my-first-plugin` membuat `/my-first-plugin:hello`).

    Buat direktori skill di folder plugin Anda:

    ```bash  theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Kemudian buat `my-first-plugin/skills/hello/SKILL.md` dengan konten ini:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Uji plugin Anda">
    Jalankan Claude Code dengan flag `--plugin-dir` untuk memuat plugin Anda:

    ```bash  theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Setelah Claude Code dimulai, coba skill baru Anda:

    ```shell  theme={null}
    /my-first-plugin:hello
    ```

    Anda akan melihat Claude merespons dengan salam. Jalankan `/help` untuk melihat skill Anda terdaftar di bawah namespace plugin.

    <Note>
      **Mengapa namespace?** Plugin skills selalu diberi namespace (seperti `/greet:hello`) untuk mencegah konflik ketika beberapa plugins memiliki skills dengan nama yang sama.

      Untuk mengubah awalan namespace, perbarui field `name` di `plugin.json`.
    </Note>
  </Step>

  <Step title="Tambahkan argumen skill">
    Buat skill Anda dinamis dengan menerima input pengguna. Placeholder `$ARGUMENTS` menangkap teks apa pun yang disediakan pengguna setelah nama skill.

    Perbarui file `SKILL.md` Anda:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Jalankan `/reload-plugins` untuk mengambil perubahan, kemudian coba skill dengan nama Anda:

    ```shell  theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude akan menyapa Anda dengan nama. Untuk lebih lanjut tentang meneruskan argumen ke skills, lihat [Skills](/id/skills#pass-arguments-to-skills).
  </Step>
</Steps>

Anda telah berhasil membuat dan menguji plugin dengan komponen kunci ini:

* **Plugin manifest** (`.claude-plugin/plugin.json`): menjelaskan metadata plugin Anda
* **Direktori skills** (`skills/`): berisi skills kustom Anda
* **Argumen skill** (`$ARGUMENTS`): menangkap input pengguna untuk perilaku dinamis

<Tip>
  Flag `--plugin-dir` berguna untuk pengembangan dan pengujian. Ketika Anda siap untuk berbagi plugin Anda dengan orang lain, lihat [Buat dan distribusikan marketplace plugin](/id/plugin-marketplaces).
</Tip>

## Ikhtisar struktur plugin

Anda telah membuat plugin dengan skill, tetapi plugins dapat mencakup banyak hal lagi: agents kustom, hooks, MCP servers, dan LSP servers.

<Warning>
  **Kesalahan umum**: Jangan letakkan `commands/`, `agents/`, `skills/`, atau `hooks/` di dalam direktori `.claude-plugin/`. Hanya `plugin.json` yang masuk ke dalam `.claude-plugin/`. Semua direktori lainnya harus berada di tingkat root plugin.
</Warning>

| Direktori         | Lokasi      | Tujuan                                                                            |
| :---------------- | :---------- | :-------------------------------------------------------------------------------- |
| `.claude-plugin/` | Root plugin | Berisi manifest `plugin.json` (opsional jika komponen menggunakan lokasi default) |
| `commands/`       | Root plugin | Skills sebagai file Markdown                                                      |
| `agents/`         | Root plugin | Definisi agent kustom                                                             |
| `skills/`         | Root plugin | Agent Skills dengan file `SKILL.md`                                               |
| `hooks/`          | Root plugin | Event handlers di `hooks.json`                                                    |
| `.mcp.json`       | Root plugin | Konfigurasi MCP server                                                            |
| `.lsp.json`       | Root plugin | Konfigurasi LSP server untuk code intelligence                                    |
| `settings.json`   | Root plugin | [Settings](/id/settings) default yang diterapkan ketika plugin diaktifkan         |

<Note>
  **Langkah berikutnya**: Siap menambahkan lebih banyak fitur? Lompat ke [Kembangkan plugins yang lebih kompleks](#develop-more-complex-plugins) untuk menambahkan agents, hooks, MCP servers, dan LSP servers. Untuk spesifikasi teknis lengkap dari semua komponen plugin, lihat [Referensi plugins](/id/plugins-reference).
</Note>

## Kembangkan plugins yang lebih kompleks

Setelah Anda nyaman dengan plugins dasar, Anda dapat membuat ekstensi yang lebih canggih.

### Tambahkan Skills ke plugin Anda

Plugins dapat mencakup [Agent Skills](/id/skills) untuk memperluas kemampuan Claude. Skills diinvokasi oleh model: Claude secara otomatis menggunakannya berdasarkan konteks tugas.

Tambahkan direktori `skills/` di root plugin Anda dengan folder Skill yang berisi file `SKILL.md`:

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Setiap `SKILL.md` memerlukan frontmatter dengan field `name` dan `description`, diikuti dengan instruksi:

```yaml  theme={null}
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Setelah memasang plugin, jalankan `/reload-plugins` untuk memuat Skills. Untuk panduan authoring Skill lengkap termasuk progressive disclosure dan pembatasan tool, lihat [Agent Skills](/id/skills).

### Tambahkan LSP servers ke plugin Anda

<Tip>
  Untuk bahasa umum seperti TypeScript, Python, dan Rust, pasang plugin LSP yang sudah dibangun sebelumnya dari marketplace resmi. Buat plugin LSP kustom hanya ketika Anda memerlukan dukungan untuk bahasa yang belum tercakup.
</Tip>

Plugin LSP (Language Server Protocol) memberikan Claude code intelligence real-time. Jika Anda perlu mendukung bahasa yang tidak memiliki plugin LSP resmi, Anda dapat membuat plugin Anda sendiri dengan menambahkan file `.lsp.json` ke plugin Anda:

```json .lsp.json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Pengguna yang memasang plugin Anda harus memiliki binary language server yang diinstal di mesin mereka.

Untuk opsi konfigurasi LSP lengkap, lihat [LSP servers](/id/plugins-reference#lsp-servers).

### Kirim settings default dengan plugin Anda

Plugins dapat menyertakan file `settings.json` di root plugin untuk menerapkan konfigurasi default ketika plugin diaktifkan. Saat ini, hanya key `agent` yang didukung.

Mengatur `agent` mengaktifkan salah satu [custom agents](/id/sub-agents) plugin sebagai thread utama, menerapkan system prompt, pembatasan tool, dan modelnya. Ini memungkinkan plugin untuk mengubah perilaku Claude Code secara default ketika diaktifkan.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Contoh ini mengaktifkan agent `security-reviewer` yang didefinisikan di direktori `agents/` plugin. Settings dari `settings.json` mengambil prioritas atas `settings` yang dideklarasikan di `plugin.json`. Key yang tidak dikenal diabaikan secara diam-diam.

### Organisir plugins kompleks

Untuk plugins dengan banyak komponen, organisir struktur direktori Anda berdasarkan fungsionalitas. Untuk layout direktori lengkap dan pola organisasi, lihat [Struktur direktori plugin](/id/plugins-reference#plugin-directory-structure).

### Uji plugins Anda secara lokal

Gunakan flag `--plugin-dir` untuk menguji plugins selama pengembangan. Ini memuat plugin Anda secara langsung tanpa memerlukan instalasi.

```bash  theme={null}
claude --plugin-dir ./my-plugin
```

Saat Anda membuat perubahan pada plugin Anda, jalankan `/reload-plugins` untuk mengambil pembaruan tanpa memulai ulang. Perubahan pada konfigurasi LSP server masih memerlukan restart penuh. Uji komponen plugin Anda:

* Coba skills Anda dengan `/plugin-name:skill-name`
* Periksa bahwa agents muncul di `/agents`
* Verifikasi hooks bekerja seperti yang diharapkan

<Tip>
  Anda dapat memuat beberapa plugins sekaligus dengan menentukan flag berkali-kali:

  ```bash  theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Debug masalah plugin

Jika plugin Anda tidak bekerja seperti yang diharapkan:

1. **Periksa struktur**: Pastikan direktori Anda berada di root plugin, bukan di dalam `.claude-plugin/`
2. **Uji komponen secara individual**: Periksa setiap command, agent, dan hook secara terpisah
3. **Gunakan alat validasi dan debugging**: Lihat [Alat debugging dan pengembangan](/id/plugins-reference#debugging-and-development-tools) untuk perintah CLI dan teknik troubleshooting

### Bagikan plugins Anda

Ketika plugin Anda siap untuk dibagikan:

1. **Tambahkan dokumentasi**: Sertakan `README.md` dengan instruksi instalasi dan penggunaan
2. **Versi plugin Anda**: Gunakan [semantic versioning](/id/plugins-reference#version-management) di `plugin.json` Anda
3. **Buat atau gunakan marketplace**: Distribusikan melalui [plugin marketplaces](/id/plugin-marketplaces) untuk instalasi
4. **Uji dengan orang lain**: Minta anggota tim menguji plugin sebelum distribusi yang lebih luas

Setelah plugin Anda berada di marketplace, orang lain dapat memasangnya menggunakan instruksi di [Temukan dan pasang plugins](/id/discover-plugins).

### Kirimkan plugin Anda ke marketplace resmi

Untuk mengirimkan plugin ke marketplace Anthropic resmi, gunakan salah satu formulir pengajuan in-app:

* **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

<Note>
  Untuk spesifikasi teknis lengkap, teknik debugging, dan strategi distribusi, lihat [Referensi plugins](/id/plugins-reference).
</Note>

## Konversi konfigurasi yang ada ke plugins

Jika Anda sudah memiliki skills atau hooks di direktori `.claude/` Anda, Anda dapat mengonversinya menjadi plugin untuk berbagi dan distribusi yang lebih mudah.

### Langkah migrasi

<Steps>
  <Step title="Buat struktur plugin">
    Buat direktori plugin baru:

    ```bash  theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Buat file manifest di `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Salin file yang ada">
    Salin konfigurasi yang ada ke direktori plugin:

    ```bash  theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Migrasi hooks">
    Jika Anda memiliki hooks di settings Anda, buat direktori hooks:

    ```bash  theme={null}
    mkdir my-plugin/hooks
    ```

    Buat `my-plugin/hooks/hooks.json` dengan konfigurasi hooks Anda. Salin objek `hooks` dari `.claude/settings.json` atau `settings.local.json` Anda, karena formatnya sama. Perintah menerima input hook sebagai JSON di stdin, jadi gunakan `jq` untuk mengekstrak path file:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Uji plugin yang dimigrasikan">
    Muat plugin Anda untuk memverifikasi semuanya berfungsi:

    ```bash  theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Uji setiap komponen: jalankan commands Anda, periksa agents muncul di `/agents`, dan verifikasi hooks dipicu dengan benar.
  </Step>
</Steps>

### Apa yang berubah saat migrasi

| Standalone (`.claude/`)                    | Plugin                               |
| :----------------------------------------- | :----------------------------------- |
| Hanya tersedia di satu proyek              | Dapat dibagikan melalui marketplaces |
| File di `.claude/commands/`                | File di `plugin-name/commands/`      |
| Hooks di `settings.json`                   | Hooks di `hooks/hooks.json`          |
| Harus menyalin secara manual untuk berbagi | Pasang dengan `/plugin install`      |

<Note>
  Setelah migrasi, Anda dapat menghapus file asli dari `.claude/` untuk menghindari duplikat. Versi plugin akan mengambil prioritas saat dimuat.
</Note>

## Langkah berikutnya

Sekarang bahwa Anda memahami sistem plugin Claude Code, berikut adalah jalur yang disarankan untuk tujuan yang berbeda:

### Untuk pengguna plugin

* [Temukan dan pasang plugins](/id/discover-plugins): jelajahi marketplaces dan pasang plugins
* [Konfigurasi marketplaces tim](/id/discover-plugins#configure-team-marketplaces): atur plugins tingkat repository untuk tim Anda

### Untuk pengembang plugin

* [Buat dan distribusikan marketplace](/id/plugin-marketplaces): paket dan bagikan plugins Anda
* [Referensi plugins](/id/plugins-reference): spesifikasi teknis lengkap
* Selami lebih dalam komponen plugin spesifik:
  * [Skills](/id/skills): detail pengembangan skill
  * [Subagents](/id/sub-agents): konfigurasi dan kemampuan agent
  * [Hooks](/id/hooks): penanganan event dan otomasi
  * [MCP](/id/mcp): integrasi tool eksternal
