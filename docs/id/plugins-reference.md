> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referensi Plugins

> Referensi teknis lengkap untuk sistem plugin Claude Code, termasuk skema, perintah CLI, dan spesifikasi komponen.

<Tip>
  Mencari cara memasang plugins? Lihat [Temukan dan pasang plugins](/id/discover-plugins). Untuk membuat plugins, lihat [Plugins](/id/plugins). Untuk mendistribusikan plugins, lihat [Plugin marketplaces](/id/plugin-marketplaces).
</Tip>

Referensi ini menyediakan spesifikasi teknis lengkap untuk sistem plugin Claude Code, termasuk skema komponen, perintah CLI, dan alat pengembangan.

Sebuah **plugin** adalah direktori yang mandiri berisi komponen yang memperluas Claude Code dengan fungsionalitas khusus. Komponen plugin mencakup skills, agents, hooks, MCP servers, LSP servers, dan monitors.

## Referensi komponen plugin

### Skills

Plugins menambahkan skills ke Claude Code, membuat pintasan `/name` yang dapat Anda atau Claude panggil.

**Lokasi**: Direktori `skills/` atau `commands/` di root plugin

**Format file**: Skills adalah direktori dengan `SKILL.md`; commands adalah file markdown sederhana

**Struktur skill**:

```text theme={null}
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

```markdown theme={null}
---
name: agent-name
description: Apa yang agent ini spesialisasikan dan kapan Claude harus memanggilnya
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Prompt sistem terperinci untuk agent yang menjelaskan peran, keahlian, dan perilakunya.
```

Plugin agents mendukung field frontmatter `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, dan `isolation`. Satu-satunya nilai `isolation` yang valid adalah `"worktree"`. Untuk alasan keamanan, `hooks`, `mcpServers`, dan `permissionMode` tidak didukung untuk agents yang dikirim plugin.

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

```json theme={null}
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

Plugin hooks merespons peristiwa lifecycle yang sama seperti [hooks yang ditentukan pengguna](/id/hooks):

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

**Tipe hook**:

* `command`: jalankan perintah shell atau scripts
* `http`: kirim JSON event sebagai POST request ke URL
* `mcp_tool`: panggil tool pada [MCP server](/id/mcp) yang dikonfigurasi
* `prompt`: evaluasi prompt dengan LLM (menggunakan placeholder `$ARGUMENTS` untuk konteks)
* `agent`: jalankan verifier agentic dengan tools untuk tugas verifikasi kompleks

### MCP servers

Plugins dapat menggabungkan Model Context Protocol (MCP) servers untuk menghubungkan Claude Code dengan alat dan layanan eksternal.

**Lokasi**: `.mcp.json` di root plugin, atau inline di plugin.json

**Format**: Konfigurasi MCP server standar

**Konfigurasi MCP server**:

```json theme={null}
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

```json theme={null}
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

```json theme={null}
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

| Plugin              | Language server            | Perintah instalasi                                                                        |
| :------------------ | :------------------------- | :---------------------------------------------------------------------------------------- |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` atau `npm install -g pyright`                                       |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                    |
| `rust-analyzer-lsp` | rust-analyzer              | [Lihat instalasi rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Pasang language server terlebih dahulu, kemudian pasang plugin dari marketplace.

### Monitors

Plugins dapat mendeklarasikan monitors latar belakang yang Claude Code mulai secara otomatis saat plugin aktif. Setiap monitor menjalankan perintah shell untuk seumur hidup sesi dan mengirimkan setiap baris stdout ke Claude sebagai notifikasi, sehingga Claude dapat bereaksi terhadap entri log, perubahan status, atau peristiwa yang dipolling tanpa diminta untuk memulai watch itu sendiri.

Plugin monitors menggunakan mekanisme yang sama seperti [Monitor tool](/id/tools-reference#monitor-tool) dan berbagi batasan ketersediaannya. Mereka hanya berjalan dalam sesi CLI interaktif, berjalan tanpa sandbox pada tingkat kepercayaan yang sama seperti [hooks](#hooks), dan dilewati pada host di mana Monitor tool tidak tersedia.

<Note>
  Plugin monitors memerlukan Claude Code v2.1.105 atau lebih baru.
</Note>

**Lokasi**: `monitors/monitors.json` di root plugin, atau inline di `plugin.json`

**Format**: Array JSON dari entri monitor

`monitors/monitors.json` berikut memantau endpoint status deployment dan log error lokal:

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

Untuk mendeklarasikan monitors inline, atur `experimental.monitors` di `plugin.json` ke array yang sama. Untuk memuat dari jalur non-default, atur `experimental.monitors` ke string jalur relatif seperti `"./config/monitors.json"`. Monitors adalah [komponen eksperimental](#experimental-components).

**Field yang diperlukan:**

| Field         | Deskripsi                                                                                                     |
| :------------ | :------------------------------------------------------------------------------------------------------------ |
| `name`        | Pengenal unik dalam plugin. Mencegah proses duplikat saat plugin dimuat ulang atau skill dipanggil lagi       |
| `command`     | Perintah shell yang dijalankan sebagai proses latar belakang persisten dalam direktori kerja sesi             |
| `description` | Ringkasan singkat tentang apa yang sedang dipantau. Ditampilkan di panel tugas dan dalam ringkasan notifikasi |

**Field opsional:**

| Field  | Deskripsi                                                                                                                                                                                                                |
| :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `when` | Mengontrol kapan monitor dimulai. `"always"` memulainya saat startup sesi dan pada reload plugin, dan merupakan default. `"on-skill-invoke:<skill-name>"` memulainya pertama kali skill bernama dalam plugin ini dikirim |

Nilai `command` mendukung [substitusi variabel](#environment-variables) yang sama seperti konfigurasi MCP dan LSP server: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.*}`, dan `${ENV_VAR}` apa pun dari lingkungan. Awali perintah dengan `cd "${CLAUDE_PLUGIN_ROOT}" && ` jika script perlu berjalan dari direktori plugin itu sendiri.

Menonaktifkan plugin di tengah sesi tidak menghentikan monitors yang sudah berjalan. Mereka berhenti saat sesi berakhir.

### Themes

Plugins dapat mengirimkan color themes yang muncul di `/theme` bersama preset bawaan dan themes lokal pengguna. Sebuah theme adalah file JSON di `themes/` dengan preset `base` dan peta `overrides` yang sparse dari color tokens. Themes adalah [komponen eksperimental](#experimental-components).

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Memilih plugin theme menyimpan `custom:<plugin-name>:<slug>` di config pengguna. Plugin themes bersifat read-only; menekan `Ctrl+E` pada salah satu di `/theme` menyalinnya ke `~/.claude/themes/` sehingga pengguna dapat mengedit salinannya.

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

```json theme={null}
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
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Field yang diperlukan

Jika Anda menyertakan manifest, `name` adalah satu-satunya field yang diperlukan.

| Field  | Tipe   | Deskripsi                               | Contoh               |
| :----- | :----- | :-------------------------------------- | :------------------- |
| `name` | string | Pengenal unik (kebab-case, tanpa spasi) | `"deployment-tools"` |

Nama ini digunakan untuk namespacing komponen. Misalnya, di UI, agent `agent-creator` untuk plugin dengan nama `plugin-dev` akan muncul sebagai `plugin-dev:agent-creator`.

### Field metadata

| Field         | Tipe   | Deskripsi                                                                                                                                                                                                                                                                                                                                                                       | Contoh                                                            |
| :------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------- |
| `$schema`     | string | URL JSON Schema untuk autocomplete dan validasi editor. Claude Code mengabaikan field ini saat waktu load.                                                                                                                                                                                                                                                                      | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `version`     | string | Opsional. Versi semantik. Mengatur ini mengikat plugin ke string versi tersebut, sehingga pengguna hanya menerima update saat Anda menaikkannya. Jika dihilangkan, Claude Code kembali ke SHA commit git, sehingga setiap commit diperlakukan sebagai versi baru. Jika juga diatur di entri marketplace, `plugin.json` menang. Lihat [Version management](#version-management). | `"2.1.0"`                                                         |
| `description` | string | Penjelasan singkat tentang tujuan plugin                                                                                                                                                                                                                                                                                                                                        | `"Deployment automation tools"`                                   |
| `author`      | object | Informasi penulis                                                                                                                                                                                                                                                                                                                                                               | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | URL dokumentasi                                                                                                                                                                                                                                                                                                                                                                 | `"https://docs.example.com"`                                      |
| `repository`  | string | URL kode sumber                                                                                                                                                                                                                                                                                                                                                                 | `"https://github.com/user/plugin"`                                |
| `license`     | string | Pengenal lisensi                                                                                                                                                                                                                                                                                                                                                                | `"MIT"`, `"Apache-2.0"`                                           |
| `keywords`    | array  | Tag penemuan                                                                                                                                                                                                                                                                                                                                                                    | `["deployment", "ci-cd"]`                                         |

### Field jalur komponen

| Field                   | Tipe                  | Deskripsi                                                                                                                                                   | Contoh                                               |
| :---------------------- | :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`                | string\|array         | Direktori skill khusus yang berisi `<name>/SKILL.md` (selain default `skills/`)                                                                             | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | File skill `.md` datar atau direktori khusus (menggantikan default `commands/`)                                                                             | `"./custom/cmd.md"` atau `["./cmd1.md"]`             |
| `agents`                | string\|array         | File agent khusus (menggantikan default `agents/`)                                                                                                          | `"./custom/agents/reviewer.md"`                      |
| `hooks`                 | string\|array\|object | Jalur konfigurasi hook atau konfigurasi inline                                                                                                              | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | Jalur konfigurasi MCP atau konfigurasi inline                                                                                                               | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | File/direktori gaya output khusus (menggantikan default `output-styles/`)                                                                                   | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | Konfigurasi [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) untuk intelijen kode (buka definisi, temukan referensi, dll.) | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | File/direktori tema warna (menggantikan default `themes/`). Lihat [Themes](#themes)                                                                         | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | Konfigurasi [Monitor](/id/tools-reference#monitor-tool) latar belakang yang dimulai secara otomatis saat plugin aktif. Lihat [Monitors](#monitors)          | `"./monitors.json"`                                  |
| `userConfig`            | object                | Nilai yang dapat dikonfigurasi pengguna yang diminta saat enable. Lihat [User configuration](#user-configuration)                                           | Lihat di bawah                                       |
| `channels`              | array                 | Deklarasi channel untuk message injection (Telegram, Slack, Discord style). Lihat [Channels](#channels)                                                     | Lihat di bawah                                       |
| `dependencies`          | array                 | Plugin lain yang diperlukan plugin ini, secara opsional dengan batasan versi semver. Lihat [Constrain plugin dependency versions](/id/plugin-dependencies)  | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Komponen eksperimental

Komponen di bawah kunci `experimental`, `themes` dan `monitors`, memiliki skema manifest yang mungkin berubah antar rilis saat mereka stabil. Di mana Anda mendeklarasikannya adalah migrasi terpisah: tingkat atas masih berfungsi, `claude plugin validate` memperingatkan, dan rilis mendatang akan memerlukan `experimental.*`.

### User configuration

Field `userConfig` mendeklarasikan nilai yang Claude Code minta dari pengguna saat plugin diaktifkan. Gunakan ini daripada memerlukan pengguna untuk mengedit `settings.json` secara manual.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Endpoint API tim Anda"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token autentikasi API",
      "sensitive": true
    }
  }
}
```

Kunci harus berupa pengenal yang valid. Setiap opsi mendukung field berikut:

| Field         | Diperlukan | Deskripsi                                                                                             |
| :------------ | :--------- | :---------------------------------------------------------------------------------------------------- |
| `type`        | Ya         | Salah satu dari `string`, `number`, `boolean`, `directory`, atau `file`                               |
| `title`       | Ya         | Label yang ditampilkan dalam dialog konfigurasi                                                       |
| `description` | Ya         | Teks bantuan yang ditampilkan di bawah field                                                          |
| `sensitive`   | Tidak      | Jika `true`, menyembunyikan input dan menyimpan nilai dalam penyimpanan aman daripada `settings.json` |
| `required`    | Tidak      | Jika `true`, validasi gagal saat field kosong                                                         |
| `default`     | Tidak      | Nilai yang digunakan saat pengguna tidak memberikan apa pun                                           |
| `multiple`    | Tidak      | Untuk tipe `string`, izinkan array string                                                             |
| `min` / `max` | Tidak      | Batas untuk tipe `number`                                                                             |

Setiap nilai tersedia untuk substitusi sebagai `${user_config.KEY}` di konfigurasi MCP dan LSP server, perintah hook, dan perintah monitor. Nilai non-sensitif juga dapat disubstitusi dalam konten skill dan agent. Semua nilai diekspor ke subprocess plugin sebagai variabel lingkungan `CLAUDE_PLUGIN_OPTION_<KEY>`.

Nilai non-sensitif disimpan di `settings.json` di bawah `pluginConfigs[<plugin-id>].options`. Nilai sensitif masuk ke keychain sistem (atau `~/.claude/.credentials.json` di mana keychain tidak tersedia). Penyimpanan keychain dibagikan dengan token OAuth dan memiliki batas total sekitar 2 KB, jadi jaga nilai sensitif tetap kecil.

### Channels

Field `channels` memungkinkan plugin mendeklarasikan satu atau lebih message channels yang menyuntikkan konten ke dalam percakapan. Setiap channel mengikat ke MCP server yang disediakan plugin.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Token bot Telegram",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "ID pengguna Telegram Anda"
        }
      }
    }
  ]
}
```

Field `server` diperlukan dan harus cocok dengan kunci di `mcpServers` plugin. Field `userConfig` per-channel opsional menggunakan skema yang sama dengan field tingkat atas, memungkinkan plugin meminta token bot atau ID pemilik saat plugin diaktifkan.

### Aturan perilaku jalur

Apakah jalur khusus menggantikan atau memperluas direktori default plugin tergantung pada field:

* **Menggantikan default**: `commands`, `agents`, `outputStyles`, `experimental.themes`, `experimental.monitors`. Misalnya, saat manifest menentukan `commands`, direktori default `commands/` tidak dipindai. Untuk menyimpan default dan menambahkan lebih banyak, sertakan secara eksplisit: `"commands": ["./commands/", "./extras/"]`
* **Menambah default**: `skills`. Direktori default `skills/` selalu dipindai, dan direktori yang tercantum di `skills` dimuat bersama dengannya
* **Aturan penggabungan sendiri**: [hooks](#hooks), [MCP servers](#mcp-servers), dan [LSP servers](#lsp-servers). Lihat setiap bagian untuk cara beberapa sumber digabungkan

Untuk semua field jalur:

* Semua jalur harus relatif terhadap root plugin dan dimulai dengan `./`
* Komponen dari jalur khusus menggunakan aturan penamaan dan namespacing yang sama
* Beberapa jalur dapat ditentukan sebagai array
* Saat jalur skill menunjuk ke direktori yang berisi `SKILL.md` secara langsung, misalnya `"skills": ["./"]` menunjuk ke root plugin, field frontmatter `name` di `SKILL.md` menentukan nama invokasi skill. Ini memberikan nama stabil terlepas dari direktori instalasi. Jika `name` tidak diatur di frontmatter, basename direktori digunakan sebagai fallback.

**Contoh jalur**:

```json theme={null}
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

Claude Code menyediakan dua variabel untuk mereferensikan jalur plugin. Keduanya disubstitusi inline di mana pun mereka muncul dalam konten skill, konten agent, perintah hook, perintah monitor, dan konfigurasi MCP atau LSP server. Keduanya juga diekspor sebagai variabel lingkungan ke proses hook dan subprocess MCP atau LSP server.

**`${CLAUDE_PLUGIN_ROOT}`**: jalur absolut ke direktori instalasi plugin Anda. Gunakan ini untuk mereferensikan scripts, binaries, dan file konfigurasi yang disertakan dengan plugin. Jalur ini berubah saat plugin diperbarui. Direktori versi sebelumnya tetap berada di disk selama sekitar tujuh hari setelah update sebelum pembersihan, tetapi perlakukan sebagai ephemeral dan jangan tulis state di sini.

Saat plugin diperbarui di tengah sesi, perintah hook, monitor, MCP server, dan LSP server terus menggunakan jalur versi sebelumnya. Jalankan `/reload-plugins` untuk mengalihkan hooks, MCP server, dan LSP server ke jalur baru; monitor memerlukan restart sesi.

**`${CLAUDE_PLUGIN_DATA}`**: direktori persisten untuk state plugin yang bertahan setelah updates. Gunakan ini untuk dependensi yang dipasang seperti `node_modules` atau Python virtual environments, kode yang dihasilkan, caches, dan file lainnya yang harus bertahan di seluruh versi plugin. Direktori dibuat secara otomatis pertama kali variabel ini direferensikan.

```json theme={null}
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

#### Direktori data persisten

Direktori `${CLAUDE_PLUGIN_DATA}` diselesaikan ke `~/.claude/plugins/data/{id}/`, di mana `{id}` adalah pengenal plugin dengan karakter di luar `a-z`, `A-Z`, `0-9`, `_`, dan `-` diganti dengan `-`. Untuk plugin yang dipasang sebagai `formatter@my-marketplace`, direktorinya adalah `~/.claude/plugins/data/formatter-my-marketplace/`.

Penggunaan umum adalah memasang dependensi bahasa sekali dan menggunakannya kembali di seluruh sesi dan update plugin. Karena direktori data bertahan lebih lama dari versi plugin tunggal, pemeriksaan keberadaan direktori saja tidak dapat mendeteksi saat update mengubah manifest dependensi plugin. Pola yang direkomendasikan membandingkan manifest yang disertakan terhadap salinan di direktori data dan memasang ulang saat mereka berbeda.

Hook `SessionStart` ini memasang `node_modules` pada run pertama dan lagi kapan pun update plugin menyertakan `package.json` yang berubah:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

`diff` keluar nonzero saat salinan yang disimpan hilang atau berbeda dari yang disertakan, mencakup run pertama dan updates yang mengubah dependensi. Jika `npm install` gagal, trailing `rm` menghapus manifest yang disalin sehingga sesi berikutnya mencoba lagi.

Scripts yang disertakan di `${CLAUDE_PLUGIN_ROOT}` kemudian dapat berjalan terhadap `node_modules` yang persisten:

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

Direktori data dihapus secara otomatis saat Anda menghapus plugin dari cakupan terakhir di mana itu dipasang. Antarmuka `/plugin` menunjukkan ukuran direktori dan meminta sebelum menghapus. CLI menghapus secara default; teruskan [`--keep-data`](#plugin-uninstall) untuk mempertahankannya.

***

## Plugin caching dan resolusi file

Plugins ditentukan dalam salah satu dari dua cara:

* Melalui `claude --plugin-dir` atau `claude --plugin-url`, untuk durasi sesi.
* Melalui marketplace, dipasang untuk sesi mendatang.

Untuk tujuan keamanan dan verifikasi, Claude Code menyalin plugin *marketplace* ke **plugin cache** lokal pengguna (`~/.claude/plugins/cache`) daripada menggunakannya di tempat. Memahami perilaku ini penting saat mengembangkan plugins yang mereferensikan file eksternal.

Setiap versi yang dipasang adalah direktori terpisah dalam cache. Saat Anda memperbarui atau menghapus plugin, direktori versi sebelumnya ditandai sebagai orphaned dan dihapus secara otomatis 7 hari kemudian. Periode grace memungkinkan sesi Claude Code bersamaan yang sudah memuat versi lama untuk terus berjalan tanpa kesalahan.

Tools Glob dan Grep Claude melewati direktori versi orphaned selama pencarian, jadi hasil file tidak menyertakan kode plugin yang ketinggalan zaman.

### Batasan path traversal

Plugin yang dipasang tidak dapat mereferensikan file di luar direktorinya. Jalur yang melintasi di luar root plugin (seperti `../shared-utils`) tidak akan berfungsi setelah instalasi karena file eksternal tersebut tidak disalin ke cache.

### Bekerja dengan dependensi eksternal

Jika plugin Anda perlu mengakses file di luar direktorinya, Anda dapat membuat symbolic links ke file eksternal dalam direktori plugin Anda. Symlinks dipertahankan dalam cache daripada didereferensikan, dan mereka diselesaikan ke target mereka saat runtime. Perintah berikut membuat link dari dalam direktori plugin Anda ke lokasi utilitas bersama:

```bash theme={null}
ln -s /path/to/shared-utils ./shared-utils
```

Ini memberikan fleksibilitas sambil mempertahankan manfaat keamanan dari sistem caching.

***

## Struktur direktori plugin

### Tata letak plugin standar

Plugin lengkap mengikuti struktur ini:

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Direktori metadata (opsional)
│   └── plugin.json             # plugin manifest
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills sebagai file .md datar
│   ├── status.md
│   └── logs.md
├── agents/                   # Definisi subagent
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # Definisi gaya output
│   └── terse.md
├── themes/                   # Definisi tema warna
│   └── dracula.json
├── monitors/                 # Konfigurasi monitor latar belakang
│   └── monitors.json
├── hooks/                    # Konfigurasi hooks
│   ├── hooks.json           # Konfigurasi hook utama
│   └── security-hooks.json  # Hook tambahan
├── bin/                      # Plugin executables ditambahkan ke PATH
│   └── my-tool               # Dapat dipanggil sebagai perintah bare di Bash tool
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
  Direktori `.claude-plugin/` berisi file `plugin.json`. Semua direktori lainnya (commands/, agents/, skills/, output-styles/, themes/, monitors/, hooks/) harus berada di root plugin, bukan di dalam `.claude-plugin/`.
</Warning>

File `CLAUDE.md` di root plugin tidak dimuat sebagai konteks proyek. Plugin berkontribusi konteks melalui skills, agents, dan hooks daripada CLAUDE.md. Untuk mengirimkan instruksi yang dimuat ke dalam konteks Claude, letakkan mereka dalam sebuah [skill](#skills).

### Referensi lokasi file

| Komponen          | Lokasi Default               | Tujuan                                                                                                                                                                                    |
| :---------------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**      | `.claude-plugin/plugin.json` | Metadata dan konfigurasi plugin (opsional)                                                                                                                                                |
| **Skills**        | `skills/`                    | Skills dengan struktur `<name>/SKILL.md`                                                                                                                                                  |
| **Commands**      | `commands/`                  | Skills sebagai file Markdown datar. Gunakan `skills/` untuk plugin baru                                                                                                                   |
| **Agents**        | `agents/`                    | File Markdown Subagent                                                                                                                                                                    |
| **Output styles** | `output-styles/`             | Definisi gaya output                                                                                                                                                                      |
| **Themes**        | `themes/`                    | Definisi tema warna                                                                                                                                                                       |
| **Hooks**         | `hooks/hooks.json`           | Konfigurasi hook                                                                                                                                                                          |
| **MCP servers**   | `.mcp.json`                  | Definisi MCP server                                                                                                                                                                       |
| **LSP servers**   | `.lsp.json`                  | Konfigurasi language server                                                                                                                                                               |
| **Monitors**      | `monitors/monitors.json`     | Konfigurasi monitor latar belakang                                                                                                                                                        |
| **Executables**   | `bin/`                       | Executables ditambahkan ke `PATH` Bash tool. File di sini dapat dipanggil sebagai perintah bare di panggilan Bash tool apa pun saat plugin diaktifkan                                     |
| **Settings**      | `settings.json`              | Konfigurasi default yang diterapkan saat plugin diaktifkan. Saat ini hanya kunci [`agent`](/id/sub-agents) dan [`subagentStatusLine`](/id/statusline#subagent-status-lines) yang didukung |

***

## Referensi perintah CLI

Claude Code menyediakan perintah CLI untuk manajemen plugin non-interaktif, berguna untuk scripting dan otomasi.

### plugin install

Pasang plugin dari marketplace yang tersedia.

```bash theme={null}
claude plugin install <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name` untuk marketplace tertentu

**Opsi:**

| Opsi                  | Deskripsi                                          | Default |
| :-------------------- | :------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Cakupan instalasi: `user`, `project`, atau `local` | `user`  |
| `-h, --help`          | Tampilkan bantuan untuk perintah                   |         |

Cakupan menentukan file pengaturan mana yang ditambahkan plugin yang dipasang. Misalnya, `--scope project` menulis ke `enabledPlugins` di .claude/settings.json, membuat plugin tersedia untuk semua orang yang mengkloning repositori proyek.

**Contoh:**

```bash theme={null}
# Pasang ke cakupan user (default)
claude plugin install formatter@my-marketplace

# Pasang ke cakupan project (dibagikan dengan tim)
claude plugin install formatter@my-marketplace --scope project

# Pasang ke cakupan local (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Hapus plugin yang dipasang.

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumen:**

* `<plugin>`: Nama plugin atau `plugin-name@marketplace-name`

**Opsi:**

| Opsi                  | Deskripsi                                                                                                           | Default |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------ | :------ |
| `-s, --scope <scope>` | Hapus dari cakupan: `user`, `project`, atau `local`                                                                 | `user`  |
| `--keep-data`         | Pertahankan [direktori data persisten](#persistent-data-directory) plugin                                           |         |
| `--prune`             | Juga hapus dependensi yang dipasang otomatis yang tidak diperlukan plugin lain. Lihat [plugin prune](#plugin-prune) |         |
| `-y, --yes`           | Lewati prompt konfirmasi `--prune`. Diperlukan ketika stdin bukan TTY                                               |         |
| `-h, --help`          | Tampilkan bantuan untuk perintah                                                                                    |         |

**Alias:** `remove`, `rm`

Secara default, menghapus dari cakupan terakhir yang tersisa juga menghapus direktori `${CLAUDE_PLUGIN_DATA}` plugin. Gunakan `--keep-data` untuk mempertahankannya, misalnya saat memasang ulang setelah menguji versi baru.

### plugin prune

Hapus dependensi plugin yang dipasang otomatis yang tidak lagi diperlukan oleh plugin yang dipasang. Dependensi yang Claude Code tarik untuk memenuhi bidang [`dependencies`](/id/plugin-dependencies) plugin lain dihapus; plugin yang Anda pasang secara langsung tidak pernah disentuh.

```bash theme={null}
claude plugin prune [options]
```

**Opsi:**

| Opsi                  | Deskripsi                                                   | Default |
| :-------------------- | :---------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Prune pada cakupan: `user`, `project`, atau `local`         | `user`  |
| `--dry-run`           | Daftar apa yang akan dihapus tanpa menghapus apa pun        |         |
| `-y, --yes`           | Lewati prompt konfirmasi. Diperlukan ketika stdin bukan TTY |         |
| `-h, --help`          | Tampilkan bantuan untuk perintah                            |         |

**Alias:** `autoremove`

Perintah ini mencantumkan dependensi yatim piatu dan meminta konfirmasi sebelum menghapusnya. Untuk menghapus plugin dan membersihkan dependensinya dalam satu langkah, jalankan `claude plugin uninstall <plugin> --prune`.

<Note>
  `claude plugin prune` memerlukan Claude Code v2.1.121 atau lebih baru.
</Note>

### plugin enable

Aktifkan plugin yang dinonaktifkan.

```bash theme={null}
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

```bash theme={null}
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

```bash theme={null}
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

### plugin list

Daftar plugin yang dipasang dengan versi, marketplace sumber, dan status enable mereka.

```bash theme={null}
claude plugin list [options]
```

**Opsi:**

| Opsi          | Deskripsi                                                           | Default |
| :------------ | :------------------------------------------------------------------ | :------ |
| `--json`      | Output sebagai JSON                                                 |         |
| `--available` | Sertakan plugin yang tersedia dari marketplace. Memerlukan `--json` |         |
| `-h, --help`  | Tampilkan bantuan untuk perintah                                    |         |

### plugin tag

Buat tag rilis git untuk plugin di direktori saat ini. Jalankan dari dalam folder plugin. Lihat [Tag plugin releases](/id/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```bash theme={null}
claude plugin tag [options]
```

**Opsi:**

| Opsi          | Deskripsi                                                 | Default |
| :------------ | :-------------------------------------------------------- | :------ |
| `--push`      | Dorong tag ke remote setelah membuatnya                   |         |
| `--dry-run`   | Cetak apa yang akan diberi tag tanpa membuat tag          |         |
| `-f, --force` | Buat tag bahkan jika pohon kerja kotor atau tag sudah ada |         |
| `-h, --help`  | Tampilkan bantuan untuk perintah                          |         |

***

## Alat debugging dan pengembangan

### Perintah debugging

Gunakan `claude --debug` untuk melihat detail loading plugin:

Ini menunjukkan:

* Plugin mana yang sedang dimuat
* Kesalahan apa pun dalam manifest plugin
* Registrasi skill, agent, dan hook
* Inisialisasi MCP server

### Masalah umum

| Masalah                             | Penyebab                       | Solusi                                                                                                                                                                             |
| :---------------------------------- | :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plugin tidak dimuat                 | `plugin.json` tidak valid      | Jalankan `claude plugin validate` atau `/plugin validate` untuk memeriksa `plugin.json`, frontmatter skill/agent/command, dan `hooks/hooks.json` untuk kesalahan sintaks dan skema |
| Skills tidak muncul                 | Struktur direktori salah       | Pastikan `skills/` atau `commands/` di root plugin, bukan di `.claude-plugin/`                                                                                                     |
| Hooks tidak aktif                   | Script tidak dapat dieksekusi  | Jalankan `chmod +x script.sh`                                                                                                                                                      |
| MCP server gagal                    | `${CLAUDE_PLUGIN_ROOT}` hilang | Gunakan variabel untuk semua jalur plugin                                                                                                                                          |
| Kesalahan jalur                     | Jalur absolut digunakan        | Semua jalur harus relatif dan dimulai dengan `./`                                                                                                                                  |
| LSP `Executable not found in $PATH` | Language server tidak dipasang | Pasang biner (misalnya, `npm install -g typescript-language-server typescript`)                                                                                                    |

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
3. Konfirmkan tipe hook valid: `command`, `http`, `mcp_tool`, `prompt`, atau `agent`

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

**Gejala**: Plugin dimuat tetapi komponen (skills, agents, hooks) hilang.

**Struktur yang benar**: Komponen harus berada di root plugin, bukan di dalam `.claude-plugin/`. Hanya `plugin.json` yang termasuk di `.claude-plugin/`.

```text theme={null}
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

Claude Code menggunakan versi plugin sebagai cache key yang menentukan apakah pembaruan tersedia. Ketika Anda menjalankan `/plugin update` atau auto-update dipicu, Claude Code menghitung versi saat ini dan melewati pembaruan jika cocok dengan apa yang sudah terpasang.

Versi diselesaikan dari yang pertama dari ini yang diatur:

1. Field `version` dalam `plugin.json` plugin
2. Field `version` dalam entri marketplace plugin dalam `marketplace.json`
3. Git commit SHA dari sumber plugin, untuk sumber `github`, `url`, `git-subdir`, dan relative-path dalam marketplace yang dihosting git
4. `unknown`, untuk sumber `npm` atau direktori lokal yang tidak berada dalam repositori git

Ini memberi Anda dua cara untuk memberi versi pada plugin:

| Pendekatan           | Cara                                                         | Perilaku pembaruan                                                                                                                                                                                 | Terbaik untuk                                         |
| :------------------- | :----------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------- |
| **Versi eksplisit**  | Atur `"version": "2.1.0"` dalam `plugin.json`                | Pengguna mendapatkan pembaruan hanya ketika Anda menaikkan field ini. Mendorong commit baru tanpa menaikkannya tidak berpengaruh, dan `/plugin update` melaporkan "already at the latest version". | Plugin yang dipublikasikan dengan siklus rilis stabil |
| **Versi commit-SHA** | Hilangkan `version` dari `plugin.json` dan entri marketplace | Pengguna mendapatkan pembaruan pada setiap commit baru ke sumber git plugin                                                                                                                        | Plugin internal atau tim di bawah pengembangan aktif  |

<Warning>
  Jika Anda mengatur `version` dalam `plugin.json`, Anda harus menaikkannya setiap kali Anda ingin pengguna menerima perubahan. Mendorong commit baru saja tidak cukup, karena Claude Code melihat string versi yang sama dan menyimpan salinan yang di-cache. Jika Anda melakukan iterasi dengan cepat, biarkan `version` tidak diatur sehingga git commit SHA digunakan sebagai gantinya.
</Warning>

Jika Anda menggunakan versi eksplisit, ikuti [semantic versioning](https://semver.org) (`MAJOR.MINOR.PATCH`): naikkan MAJOR untuk perubahan breaking, MINOR untuk fitur baru, PATCH untuk perbaikan bug. Dokumentasikan perubahan dalam `CHANGELOG.md`.

***

## Lihat juga

* [Plugins](/id/plugins) - Tutorial dan penggunaan praktis
* [Plugin marketplaces](/id/plugin-marketplaces) - Membuat dan mengelola marketplace
* [Skills](/id/skills) - Detail pengembangan skill
* [Subagents](/id/sub-agents) - Konfigurasi dan kemampuan agent
* [Hooks](/id/hooks) - Penanganan event dan otomasi
* [MCP](/id/mcp) - Integrasi alat eksternal
* [Settings](/id/settings) - Opsi konfigurasi untuk plugins
