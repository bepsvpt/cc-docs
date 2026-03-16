> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referensi Plugins

> Referensi teknis lengkap untuk sistem plugin Claude Code, termasuk skema, perintah CLI, dan spesifikasi komponen.

<Tip>
  Mencari cara memasang plugins? Lihat [Temukan dan pasang plugins](/id/discover-plugins). Untuk membuat plugins, lihat [Plugins](/id/plugins). Untuk mendistribusikan plugins, lihat [Plugin marketplaces](/id/plugin-marketplaces).
</Tip>

Referensi ini menyediakan spesifikasi teknis lengkap untuk sistem plugin Claude Code, termasuk skema komponen, perintah CLI, dan alat pengembangan.

Sebuah **plugin** adalah direktori yang mandiri berisi komponen yang memperluas Claude Code dengan fungsionalitas khusus. Komponen plugin mencakup skills, agents, hooks, MCP servers, dan LSP servers.

## Referensi komponen plugin

### Skills

Plugins menambahkan skills ke Claude Code, membuat pintasan `/name` yang dapat Anda atau Claude panggil.

**Lokasi**: Direktori `skills/` atau `commands/` di root plugin

**Format file**: Skills adalah direktori dengan `SKILL.md`; commands adalah file markdown sederhana

**Struktur skill**:

```text  theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (opsional)
│   └── scripts/ (opsional)
└── code-reviewer/
    └── SKILL.md
```

**Perilaku integrasi**:

* Skills dan commands secara otomatis ditemukan saat plugin dipasang
* Claude dapat memanggilnya secara otomatis berdasarkan konteks tugas
* Skills dapat menyertakan file pendukung di samping SKILL.md

Untuk detail lengkap, lihat [Skills](/id/skills).

### Agents

Plugins dapat menyediakan subagents khusus untuk tugas-tugas tertentu yang dapat Claude panggil secara otomatis jika sesuai.

**Lokasi**: Direktori `agents/` di root plugin

**Format file**: File markdown yang menjelaskan kemampuan agent

**Struktur agent**:

```markdown  theme={null}
---
name: agent-name
description: Apa yang agent ini spesialisasikan dan kapan Claude harus memanggilnya
---

Prompt sistem terperinci untuk agent yang menjelaskan peran, keahlian, dan perilakunya.
```

**Titik integrasi**:

* Agents muncul di antarmuka `/agents`
* Claude dapat memanggil agents secara otomatis berdasarkan konteks tugas
* Agents dapat dipanggil secara manual oleh pengguna
* Plugin agents bekerja bersama agents Claude bawaan

Untuk detail lengkap, lihat [Subagents](/id/sub-agents).

### Hooks

Plugins dapat menyediakan event handlers yang merespons peristiwa Claude Code secara otomatis.

**Lokasi**: `hooks/hooks.json` di root plugin, atau inline di plugin.json

**Format**: Konfigurasi JSON dengan event matchers dan actions

**Konfigurasi hook**:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Event yang tersedia**:

* `PreToolUse`: Sebelum Claude menggunakan alat apa pun
* `PostToolUse`: Setelah Claude berhasil menggunakan alat apa pun
* `PostToolUseFailure`: Setelah eksekusi alat Claude gagal
* `PermissionRequest`: Saat dialog izin ditampilkan
* `UserPromptSubmit`: Saat pengguna mengirimkan prompt
* `Notification`: Saat Claude Code mengirim notifikasi
* `Stop`: Saat Claude mencoba berhenti
* `SubagentStart`: Saat subagent dimulai
* `SubagentStop`: Saat subagent mencoba berhenti
* `SessionStart`: Di awal sesi
* `SessionEnd`: Di akhir sesi
* `TeammateIdle`: Saat rekan tim tim agent akan menjadi idle
* `TaskCompleted`: Saat tugas ditandai sebagai selesai
* `PreCompact`: Sebelum riwayat percakapan dikompres

**Tipe hook**:

* `command`: Jalankan perintah shell atau script
* `prompt`: Evaluasi prompt dengan LLM (menggunakan placeholder `$ARGUMENTS` untuk konteks)
* `agent`: Jalankan verifier agentic dengan alat untuk tugas verifikasi kompleks

### MCP servers

Plugins dapat menggabungkan Model Context Protocol (MCP) servers untuk menghubungkan Claude Code dengan alat dan layanan eksternal.

**Lokasi**: `.mcp.json` di root plugin, atau inline di plugin.json

**Format**: Konfigurasi MCP server standar

**Konfigurasi MCP server**:

```json  theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Perilaku integrasi**:

* Plugin MCP servers dimulai secara otomatis saat plugin diaktifkan
* Servers muncul sebagai alat MCP standar di toolkit Claude
* Kemampuan server terintegrasi dengan mulus dengan alat Claude yang ada
* Plugin servers dapat dikonfigurasi secara independen dari MCP servers pengguna

### LSP servers

<Tip>
  Mencari cara menggunakan LSP plugins? Pasang dari marketplace resmi: cari "lsp" di tab Discover `/plugin`. Bagian ini mendokumentasikan cara membuat LSP plugins untuk bahasa yang tidak tercakup oleh marketplace resmi.
</Tip>

Plugins dapat menyediakan server [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) untuk memberikan Claude intelijen kode real-time saat bekerja pada codebase Anda.

Integrasi LSP menyediakan:

* **Diagnostik instan**: Claude melihat kesalahan dan peringatan segera setelah setiap edit
* **Navigasi kode**: buka definisi, temukan referensi, dan informasi hover
* **Kesadaran bahasa**: informasi tipe dan dokumentasi untuk simbol kode

**Lokasi**: `.lsp.json` di root plugin, atau inline di `plugin.json`

**Format**: Konfigurasi JSON yang memetakan nama language server ke konfigurasinya

**Format file `.lsp.json`**:

```json  theme={null}
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

**Inline di `plugin.json`**:

```json  theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Field yang diperlukan:**

| Field                 | Deskripsi                                          |
| :-------------------- | :------------------------------------------------- |
| `command`             | Biner LSP yang akan dijalankan (harus ada di PATH) |
| `extensionToLanguage` | Memetakan ekstensi file ke pengenal bahasa         |

**Field opsional:**

| Field                   | Deskripsi                                                             |
| :---------------------- | :-------------------------------------------------------------------- |
| `args`                  | Argumen baris perintah untuk LSP server                               |
| `transport`             | Transport komunikasi: `stdio` (default) atau `socket`                 |
| `env`                   | Variabel lingkungan yang diatur saat memulai server                   |
| `initializationOptions` | Opsi yang diteruskan ke server selama inisialisasi                    |
| `settings`              | Pengaturan yang diteruskan melalui `workspace/didChangeConfiguration` |
| `workspaceFolder`       | Jalur folder workspace untuk server                                   |
| `startupTimeout`        | Waktu maksimal untuk menunggu startup server (milidetik)              |
| `shutdownTimeout`       | Waktu maksimal untuk menunggu shutdown yang elegan (milidetik)        |
| `restartOnCrash`        | Apakah secara otomatis memulai ulang server jika crash                |
| `maxRestarts`           | Jumlah maksimal upaya restart sebelum menyerah                        |

<Warning>
  **Anda harus memasang biner language server secara terpisah.** LSP plugins mengonfigurasi cara Claude Code terhubung ke language server, tetapi mereka tidak menyertakan server itu sendiri. Jika Anda melihat `Executable not found in $PATH` di tab Errors `/plugin`, pasang biner yang diperlukan untuk bahasa Anda.
</Warning>

**LSP plugins yang tersedia:**

| Plugin           | Language server            | Perintah instalasi                                                                        |
| :--------------- | :------------------------- | :---------------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` atau `npm install -g pyright`                                       |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                    |
| `rust-lsp`       | rust-analyzer              | [Lihat instalasi rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Pasang language server terlebih dahulu, kemudian pasang plugin dari marketplace.

***

## Cakupan instalasi plugin

Saat Anda memasang plugin, Anda memilih **cakupan** yang menentukan di mana plugin tersedia dan siapa lagi yang dapat menggunakannya:

| Cakupan   | File pengaturan                                     | Kasus penggunaan                                  |
| :-------- | :-------------------------------------------------- | :------------------------------------------------ |
| `user`    | `~/.claude/settings.json`                           | Plugin pribadi tersedia di semua proyek (default) |
| `project` | `.claude/settings.json`                             | Plugin tim yang dibagikan melalui version control |
| `local`   | `.claude/settings.local.json`                       | Plugin khusus proyek, gitignored                  |
| `managed` | [Pengaturan terkelola](/id/settings#settings-files) | Plugin terkelola (read-only, hanya update)        |

Plugins menggunakan sistem cakupan yang sama dengan konfigurasi Claude Code lainnya. Untuk instruksi instalasi dan flag cakupan, lihat [Pasang plugins](/id/discover-plugins#install-plugins). Untuk penjelasan lengkap tentang cakupan, lihat [Configuration scopes](/id/settings#configuration-scopes).

***

## Skema manifest plugin

File `.claude-plugin/plugin.json` mendefinisikan metadata dan konfigurasi plugin Anda. Bagian ini mendokumentasikan semua field dan opsi yang didukung.

Manifest bersifat opsional. Jika dihilangkan, Claude Code secara otomatis menemukan komponen di [lokasi default](#file-locations-reference) dan menurunkan nama plugin dari nama direktori. Gunakan manifest saat Anda perlu memberikan metadata atau jalur komponen khusus.

### Skema lengkap

```json  theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Field yang diperlukan

Jika Anda menyertakan manifest, `name` adalah satu-satunya field yang diperlukan.

| Field  | Tipe   | Deskripsi                               | Contoh               |
| :----- | :----- | :-------------------------------------- | :------------------- |
| `name` | string | Pengenal unik (kebab-case, tanpa spasi) | `"deployment-tools"` |

Nama ini digunakan untuk namespacing komponen. Misalnya, di UI, agent `agent-creator` untuk plugin dengan nama `plugin-dev` akan muncul sebagai `plugin-dev:agent-creator`.

### Field metadata

| Field         | Tipe   | Deskripsi                                                                                                                             | Contoh                                             |
| :------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `version`     | string | Versi semantik. Jika juga diatur di entri marketplace, `plugin.json` memiliki prioritas. Anda hanya perlu mengaturnya di satu tempat. | `"2.1.0"`                                          |
| `description` | string | Penjelasan singkat tentang tujuan plugin                                                                                              | `"Deployment automation tools"`                    |
| `author`      | object | Informasi penulis                                                                                                                     | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | URL dokumentasi                                                                                                                       | `"https://docs.example.com"`                       |
| `repository`  | string | URL kode sumber                                                                                                                       | `"https://github.com/user/plugin"`                 |
| `license`     | string | Pengenal lisensi                                                                                                                      | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Tag penemuan                                                                                                                          | `["deployment", "ci-cd"]`                          |

### Field jalur komponen

| Field          | Tipe                  | Deskripsi                                                                                                                                                   | Contoh                                   |
| :------------- | :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------- |
| `commands`     | string\|array         | File/direktori command tambahan                                                                                                                             | `"./custom/cmd.md"` atau `["./cmd1.md"]` |
| `agents`       | string\|array         | File agent tambahan                                                                                                                                         | `"./custom/agents/reviewer.md"`          |
| `skills`       | string\|array         | Direktori skill tambahan                                                                                                                                    | `"./custom/skills/"`                     |
| `hooks`        | string\|array\|object | Jalur konfigurasi hook atau konfigurasi inline                                                                                                              | `"./my-extra-hooks.json"`                |
| `mcpServers`   | string\|array\|object | Jalur konfigurasi MCP atau konfigurasi inline                                                                                                               | `"./my-extra-mcp-config.json"`           |
| `outputStyles` | string\|array         | File/direktori gaya output tambahan                                                                                                                         | `"./styles/"`                            |
| `lspServers`   | string\|array\|object | Konfigurasi [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) untuk intelijen kode (buka definisi, temukan referensi, dll.) | `"./.lsp.json"`                          |

### Aturan perilaku jalur

**Penting**: Jalur khusus melengkapi direktori default - mereka tidak menggantikannya.

* Jika `commands/` ada, itu dimuat selain jalur command khusus
* Semua jalur harus relatif terhadap root plugin dan dimulai dengan `./`
* Commands dari jalur khusus menggunakan aturan penamaan dan namespacing yang sama
* Beberapa jalur dapat ditentukan sebagai array untuk fleksibilitas

**Contoh jalur**:

```json  theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Variabel lingkungan

**`${CLAUDE_PLUGIN_ROOT}`**: Berisi jalur absolut ke direktori plugin Anda. Gunakan ini di hooks, MCP servers, dan scripts untuk memastikan jalur yang benar terlepas dari lokasi instalasi.

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

***

## Caching plugin dan resolusi file

Plugins ditentukan dalam salah satu dari dua cara:

* Melalui `claude --plugin-dir`, untuk durasi sesi.
* Melalui marketplace, dipasang untuk sesi mendatang.

Untuk tujuan keamanan dan verifikasi, Claude Code menyalin plugin *marketplace* ke **plugin cache** lokal pengguna (`~/.claude/plugins/cache`) daripada menggunakannya di tempat. Memahami perilaku ini penting saat mengembangkan plugins yang mereferensikan file eksternal.

### Batasan path traversal

Plugin yang dipasang tidak dapat mereferensikan file di luar direktorinya. Jalur yang melintasi di luar root plugin (seperti `../shared-utils`) tidak akan berfungsi setelah instalasi karena file eksternal tersebut tidak disalin ke cache.

### Bekerja dengan dependensi eksternal

Jika plugin Anda perlu mengakses file di luar direktorinya, Anda dapat membuat symbolic links ke file eksternal dalam direktori plugin Anda. Symlinks dihormati selama proses penyalinan:

```bash  theme={null}
# Di dalam direktori plugin Anda
ln -s /path/to/shared-utils ./shared-utils
```

Konten yang di-symlink akan disalin ke plugin cache. Ini memberikan fleksibilitas sambil mempertahankan manfaat keamanan dari sistem caching.

***

## Struktur direktori plugin

### Tata letak plugin standar

Plugin lengkap mengikuti struktur ini:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # Direktori metadata (opsional)
│   └── plugin.json             # plugin manifest
├── commands/                 # Lokasi command default
│   ├── status.md
│   └── logs.md
├── agents/                   # Lokasi agent default
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Konfigurasi hook
│   ├── hooks.json           # Konfigurasi hook utama
│   └── security-hooks.json  # Hook tambahan
├── settings.json            # Pengaturan default untuk plugin
├── .mcp.json                # Definisi MCP server
├── .lsp.json                # Konfigurasi LSP server
├── scripts/                 # Hook dan utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # File lisensi
└── CHANGELOG.md             # Riwayat versi
```

<Warning>
  Direktori `.claude-plugin/` berisi file `plugin.json`. Semua direktori lainnya (commands/, agents/, skills/, hooks/) harus berada di root plugin, bukan di dalam `.claude-plugin/`.
</Warning>

### Referensi lokasi file

| Komponen        | Lokasi Default               | Tujuan                                                                                                                        |
| :-------------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**    | `.claude-plugin/plugin.json` | Metadata dan konfigurasi plugin (opsional)                                                                                    |
| **Commands**    | `commands/`                  | File Markdown Skill (legacy; gunakan `skills/` untuk skill baru)                                                              |
| **Agents**      | `agents/`                    | File Markdown Subagent                                                                                                        |
| **Skills**      | `skills/`                    | Skills dengan struktur `<name>/SKILL.md`                                                                                      |
| **Hooks**       | `hooks/hooks.json`           | Konfigurasi hook                                                                                                              |
| **MCP servers** | `.mcp.json`                  | Definisi MCP server                                                                                                           |
| **LSP servers** | `.lsp.json`                  | Konfigurasi language server                                                                                                   |
| **Settings**    | `settings.json`              | Konfigurasi default yang diterapkan saat plugin diaktifkan. Saat ini hanya pengaturan [`agent`](/id/sub-agents) yang didukung |

***

## Referensi perintah CLI

Claude Code menyediakan perintah CLI untuk manajemen plugin non-interaktif, berguna untuk scripting dan otomasi.

### plugin install

Pasang plugin dari marketplace yang tersedia.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name` untuk marketplace tertentu

**Opsi:**

| Opsi                  | Deskripsi                                          | Default |
| :-------------------- | :------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Cakupan instalasi: `user`, `project`, atau `local` | `user`  |
| `-h, --help`          | Tampilkan bantuan untuk perintah                   |         |

Cakupan menentukan file pengaturan mana yang ditambahkan plugin yang dipasang. Misalnya, --scope project menulis ke `enabledPlugins` di .claude/settings.json, membuat plugin tersedia untuk semua orang yang mengkloning repositori proyek.

**Contoh:**

```bash  theme={null}
# Pasang ke cakupan user (default)
claude plugin install formatter@my-marketplace

# Pasang ke cakupan project (dibagikan dengan tim)
claude plugin install formatter@my-marketplace --scope project

# Pasang ke cakupan local (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Hapus plugin yang dipasang.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name`

**Opsi:**

| Opsi                  | Deskripsi                                           | Default |
| :-------------------- | :-------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Hapus dari cakupan: `user`, `project`, atau `local` | `user`  |
| `-h, --help`          | Tampilkan bantuan untuk perintah                    |         |

**Alias:** `remove`, `rm`

### plugin enable

Aktifkan plugin yang dinonaktifkan.

```bash  theme={null}
claude plugin enable <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name`

**Opsi:**

| Opsi                  | Deskripsi                                                 | Default |
| :-------------------- | :-------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Cakupan untuk diaktifkan: `user`, `project`, atau `local` | `user`  |
| `-h, --help`          | Tampilkan bantuan untuk perintah                          |         |

### plugin disable

Nonaktifkan plugin tanpa menghapusnya.

```bash  theme={null}
claude plugin disable <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name`

**Opsi:**

| Opsi                  | Deskripsi                                                    | Default |
| :-------------------- | :----------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Cakupan untuk dinonaktifkan: `user`, `project`, atau `local` | `user`  |
| `-h, --help`          | Tampilkan bantuan untuk perintah                             |         |

### plugin update

Perbarui plugin ke versi terbaru.

```bash  theme={null}
claude plugin update <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name`

**Opsi:**

| Opsi                  | Deskripsi                                                            | Default |
| :-------------------- | :------------------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Cakupan untuk diperbarui: `user`, `project`, `local`, atau `managed` | `user`  |
| `-h, --help`          | Tampilkan bantuan untuk perintah                                     |         |

***

## Alat debugging dan pengembangan

### Perintah debugging

Gunakan `claude --debug` (atau `/debug` dalam TUI) untuk melihat detail loading plugin:

Ini menunjukkan:

* Plugin mana yang sedang dimuat
* Kesalahan apa pun dalam manifest plugin
* Registrasi command, agent, dan hook
* Inisialisasi MCP server

### Masalah umum

| Masalah                             | Penyebab                       | Solusi                                                                          |
| :---------------------------------- | :----------------------------- | :------------------------------------------------------------------------------ |
| Plugin tidak dimuat                 | `plugin.json` tidak valid      | Validasi sintaks JSON dengan `claude plugin validate` atau `/plugin validate`   |
| Commands tidak muncul               | Struktur direktori salah       | Pastikan `commands/` di root, bukan di `.claude-plugin/`                        |
| Hooks tidak aktif                   | Script tidak dapat dieksekusi  | Jalankan `chmod +x script.sh`                                                   |
| MCP server gagal                    | `${CLAUDE_PLUGIN_ROOT}` hilang | Gunakan variabel untuk semua jalur plugin                                       |
| Kesalahan jalur                     | Jalur absolut digunakan        | Semua jalur harus relatif dan dimulai dengan `./`                               |
| LSP `Executable not found in $PATH` | Language server tidak dipasang | Pasang biner (misalnya, `npm install -g typescript-language-server typescript`) |

### Contoh pesan kesalahan

**Kesalahan validasi manifest**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: periksa koma yang hilang, koma ekstra, atau string yang tidak dikutip
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: field yang diperlukan hilang
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: kesalahan sintaks JSON

**Kesalahan loading plugin**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: jalur command ada tetapi tidak berisi file command yang valid
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: jalur `source` di marketplace.json menunjuk ke direktori yang tidak ada
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: hapus definisi komponen duplikat atau hapus `strict: false` di entri marketplace

### Troubleshooting hook

**Hook script tidak dieksekusi**:

1. Periksa script dapat dieksekusi: `chmod +x ./scripts/your-script.sh`
2. Verifikasi baris shebang: Baris pertama harus `#!/bin/bash` atau `#!/usr/bin/env bash`
3. Periksa jalur menggunakan `${CLAUDE_PLUGIN_ROOT}`: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Uji script secara manual: `./scripts/your-script.sh`

**Hook tidak dipicu pada event yang diharapkan**:

1. Verifikasi nama event benar (case-sensitive): `PostToolUse`, bukan `postToolUse`
2. Periksa pola matcher cocok dengan alat Anda: `"matcher": "Write|Edit"` untuk operasi file
3. Konfirmkan tipe hook valid: `command`, `prompt`, atau `agent`

### Troubleshooting MCP server

**Server tidak dimulai**:

1. Periksa command ada dan dapat dieksekusi
2. Verifikasi semua jalur menggunakan variabel `${CLAUDE_PLUGIN_ROOT}`
3. Periksa log MCP server: `claude --debug` menunjukkan kesalahan inisialisasi
4. Uji server secara manual di luar Claude Code

**Alat server tidak muncul**:

1. Pastikan server dikonfigurasi dengan benar di `.mcp.json` atau `plugin.json`
2. Verifikasi server mengimplementasikan protokol MCP dengan benar
3. Periksa timeout koneksi di output debug

### Kesalahan struktur direktori

**Gejala**: Plugin dimuat tetapi komponen (commands, agents, hooks) hilang.

**Struktur yang benar**: Komponen harus berada di root plugin, bukan di dalam `.claude-plugin/`. Hanya `plugin.json` yang termasuk di `.claude-plugin/`.

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Hanya manifest di sini
├── commands/            ← Di level root
├── agents/              ← Di level root
└── hooks/               ← Di level root
```

Jika komponen Anda berada di dalam `.claude-plugin/`, pindahkan ke root plugin.

**Daftar periksa debug**:

1. Jalankan `claude --debug` dan cari pesan "loading plugin"
2. Periksa bahwa setiap direktori komponen terdaftar di output debug
3. Verifikasi izin file memungkinkan membaca file plugin

***

## Referensi distribusi dan versioning

### Manajemen versi

Ikuti semantic versioning untuk rilis plugin:

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Format versi**: `MAJOR.MINOR.PATCH`

* **MAJOR**: Perubahan breaking (perubahan API yang tidak kompatibel)
* **MINOR**: Fitur baru (penambahan yang kompatibel ke belakang)
* **PATCH**: Perbaikan bug (perbaikan yang kompatibel ke belakang)

**Best practices**:

* Mulai dari `1.0.0` untuk rilis stabil pertama Anda
* Perbarui versi di `plugin.json` sebelum mendistribusikan perubahan
* Dokumentasikan perubahan dalam file `CHANGELOG.md`
* Gunakan versi pre-release seperti `2.0.0-beta.1` untuk pengujian

<Warning>
  Claude Code menggunakan versi untuk menentukan apakah akan memperbarui plugin Anda. Jika Anda mengubah kode plugin Anda tetapi tidak meningkatkan versi di `plugin.json`, pengguna plugin Anda yang ada tidak akan melihat perubahan Anda karena caching.

  Jika plugin Anda berada dalam direktori [marketplace](/id/plugin-marketplaces), Anda dapat mengelola versi melalui `marketplace.json` sebagai gantinya dan menghilangkan field `version` dari `plugin.json`.
</Warning>

***

## Lihat juga

* [Plugins](/id/plugins) - Tutorial dan penggunaan praktis
* [Plugin marketplaces](/id/plugin-marketplaces) - Membuat dan mengelola marketplace
* [Skills](/id/skills) - Detail pengembangan skill
* [Subagents](/id/sub-agents) - Konfigurasi dan kemampuan agent
* [Hooks](/id/hooks) - Penanganan event dan otomasi
* [MCP](/id/mcp) - Integrasi alat eksternal
* [Settings](/id/settings) - Opsi konfigurasi untuk plugins
