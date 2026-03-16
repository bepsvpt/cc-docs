> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Pengaturan Claude Code

> Konfigurasikan Claude Code dengan pengaturan global dan tingkat proyek, serta variabel lingkungan.

Claude Code menawarkan berbagai pengaturan untuk mengonfigurasi perilakunya sesuai kebutuhan Anda. Anda dapat mengonfigurasi Claude Code dengan menjalankan perintah `/config` saat menggunakan REPL interaktif, yang membuka antarmuka Pengaturan bertab di mana Anda dapat melihat informasi status dan memodifikasi opsi konfigurasi.

## Cakupan konfigurasi

Claude Code menggunakan **sistem cakupan** untuk menentukan di mana konfigurasi berlaku dan siapa yang membagikannya. Memahami cakupan membantu Anda memutuskan cara mengonfigurasi Claude Code untuk penggunaan pribadi, kolaborasi tim, atau penyebaran perusahaan.

### Cakupan yang tersedia

| Cakupan     | Lokasi                                                                                         | Siapa yang terpengaruh              | Dibagikan dengan tim?  |
| :---------- | :--------------------------------------------------------------------------------------------- | :---------------------------------- | :--------------------- |
| **Managed** | Pengaturan yang dikelola server, plist / registry, atau `managed-settings.json` tingkat sistem | Semua pengguna di mesin             | Ya (digunakan oleh IT) |
| **User**    | Direktori `~/.claude/`                                                                         | Anda, di semua proyek               | Tidak                  |
| **Project** | `.claude/` di repositori                                                                       | Semua kolaborator di repositori ini | Ya (dikomit ke git)    |
| **Local**   | `.claude/settings.local.json`                                                                  | Anda, hanya di repositori ini       | Tidak (diabaikan git)  |

### Kapan menggunakan setiap cakupan

**Cakupan Managed** adalah untuk:

* Kebijakan keamanan yang harus diterapkan di seluruh organisasi
* Persyaratan kepatuhan yang tidak dapat ditimpa
* Konfigurasi standar yang digunakan oleh IT/DevOps

**Cakupan User** paling baik untuk:

* Preferensi pribadi yang Anda inginkan di mana-mana (tema, pengaturan editor)
* Alat dan plugin yang Anda gunakan di semua proyek
* Kunci API dan autentikasi (disimpan dengan aman)

**Cakupan Project** paling baik untuk:

* Pengaturan bersama tim (izin, hooks, MCP servers)
* Plugin yang harus dimiliki seluruh tim
* Standardisasi alat di seluruh kolaborator

**Cakupan Local** paling baik untuk:

* Penggantian pribadi untuk proyek tertentu
* Pengaturan pengujian sebelum dibagikan dengan tim
* Pengaturan spesifik mesin yang tidak akan berfungsi untuk orang lain

### Bagaimana cakupan berinteraksi

Ketika pengaturan yang sama dikonfigurasi dalam beberapa cakupan, cakupan yang lebih spesifik memiliki prioritas:

1. **Managed** (tertinggi) - tidak dapat ditimpa oleh apa pun
2. **Argumen baris perintah** - penggantian sesi sementara
3. **Local** - menimpa pengaturan proyek dan pengguna
4. **Project** - menimpa pengaturan pengguna
5. **User** (terendah) - berlaku ketika tidak ada yang menentukan pengaturan

Misalnya, jika izin diizinkan dalam pengaturan pengguna tetapi ditolak dalam pengaturan proyek, pengaturan proyek memiliki prioritas dan izin diblokir.

### Apa yang menggunakan cakupan

Cakupan berlaku untuk banyak fitur Claude Code:

| Fitur           | Lokasi pengguna           | Lokasi proyek                        | Lokasi lokal                  |
| :-------------- | :------------------------ | :----------------------------------- | :---------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json` |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                    | —                             |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                          | `~/.claude.json` (per-proyek) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json` |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` atau `.claude/CLAUDE.md` | —                             |

***

## File pengaturan

File `settings.json` adalah mekanisme resmi kami untuk mengonfigurasi Claude Code melalui pengaturan hierarki:

* **Pengaturan pengguna** didefinisikan dalam `~/.claude/settings.json` dan berlaku untuk semua proyek.
* **Pengaturan proyek** disimpan di direktori proyek Anda:
  * `.claude/settings.json` untuk pengaturan yang diperiksa ke dalam kontrol sumber dan dibagikan dengan tim Anda
  * `.claude/settings.local.json` untuk pengaturan yang tidak diperiksa, berguna untuk preferensi pribadi dan eksperimen. Claude Code akan mengonfigurasi git untuk mengabaikan `.claude/settings.local.json` saat dibuat.
* **Pengaturan Managed**: Untuk organisasi yang memerlukan kontrol terpusat, Claude Code mendukung beberapa mekanisme pengiriman untuk pengaturan yang dikelola. Semua menggunakan format JSON yang sama dan tidak dapat ditimpa oleh pengaturan pengguna atau proyek:

  * **Pengaturan yang dikelola server**: dikirimkan dari server Anthropic melalui konsol admin Claude.ai. Lihat [pengaturan yang dikelola server](/id/server-managed-settings).
  * **Kebijakan tingkat MDM/OS**: dikirimkan melalui manajemen perangkat asli di macOS dan Windows:
    * macOS: domain preferensi terkelola `com.anthropic.claudecode` (digunakan melalui profil konfigurasi di Jamf, Kandji, atau alat MDM lainnya)
    * Windows: kunci registry `HKLM\SOFTWARE\Policies\ClaudeCode` dengan nilai `Settings` (REG\_SZ atau REG\_EXPAND\_SZ) yang berisi JSON (digunakan melalui Group Policy atau Intune)
    * Windows (tingkat pengguna): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioritas kebijakan terendah, hanya digunakan ketika tidak ada sumber tingkat admin)
  * **Berbasis file**: `managed-settings.json` dan `managed-mcp.json` digunakan ke direktori sistem:
    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux dan WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

  Lihat [pengaturan yang dikelola](/id/permissions#managed-only-settings) dan [Konfigurasi MCP Managed](/id/mcp#managed-mcp-configuration) untuk detail.

  <Note>
    Penyebaran yang dikelola juga dapat membatasi **penambahan marketplace plugin** menggunakan `strictKnownMarketplaces`. Untuk informasi lebih lanjut, lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Konfigurasi lainnya** disimpan dalam `~/.claude.json`. File ini berisi preferensi Anda (tema, pengaturan notifikasi, mode editor), sesi OAuth, konfigurasi [MCP server](/id/mcp) untuk cakupan pengguna dan lokal, status per-proyek (alat yang diizinkan, pengaturan kepercayaan), dan berbagai cache. MCP server dengan cakupan proyek disimpan secara terpisah dalam `.mcp.json`.

<Note>
  Claude Code secara otomatis membuat cadangan file konfigurasi dengan stempel waktu dan menyimpan lima cadangan terbaru untuk mencegah kehilangan data.
</Note>

```JSON Contoh settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

Baris `$schema` dalam contoh di atas menunjuk ke [skema JSON resmi](https://json.schemastore.org/claude-code-settings.json) untuk pengaturan Claude Code. Menambahkannya ke `settings.json` Anda memungkinkan pelengkapan otomatis dan validasi inline di VS Code, Cursor, dan editor lain yang mendukung validasi skema JSON.

### Pengaturan yang tersedia

`settings.json` mendukung sejumlah opsi:

| Kunci                             | Deskripsi                                                                                                                                                                                                                                                                                                                                       | Contoh                                                                  |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Skrip khusus, yang akan dieksekusi dalam `/bin/sh`, untuk menghasilkan nilai auth. Nilai ini akan dikirim sebagai header `X-Api-Key` dan `Authorization: Bearer` untuk permintaan model                                                                                                                                                         | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | Sesi yang tidak aktif lebih lama dari periode ini dihapus saat startup. Mengatur ke `0` segera menghapus semua sesi. (default: 30 hari)                                                                                                                                                                                                         | `20`                                                                    |
| `companyAnnouncements`            | Pengumuman untuk ditampilkan kepada pengguna saat startup. Jika beberapa pengumuman disediakan, mereka akan diputar secara acak.                                                                                                                                                                                                                | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Variabel lingkungan yang akan diterapkan ke setiap sesi                                                                                                                                                                                                                                                                                         | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Sesuaikan atribusi untuk komit git dan permintaan tarik. Lihat [Pengaturan atribusi](#attribution-settings)                                                                                                                                                                                                                                     | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Tidak direkomendasikan**: Gunakan `attribution` sebagai gantinya. Apakah akan menyertakan baris `co-authored-by Claude` dalam komit git dan permintaan tarik (default: `true`)                                                                                                                                                                | `false`                                                                 |
| `includeGitInstructions`          | Sertakan instruksi alur kerja komit dan PR bawaan dalam prompt sistem Claude (default: `true`). Atur ke `false` untuk menghapus instruksi ini, misalnya saat menggunakan skill alur kerja git Anda sendiri. Variabel lingkungan `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` memiliki prioritas atas pengaturan ini saat diatur                       | `false`                                                                 |
| `permissions`                     | Lihat tabel di bawah untuk struktur izin.                                                                                                                                                                                                                                                                                                       |                                                                         |
| `hooks`                           | Konfigurasikan perintah khusus untuk dijalankan pada acara siklus hidup. Lihat [dokumentasi hooks](/id/hooks) untuk format                                                                                                                                                                                                                      | Lihat [hooks](/id/hooks)                                                |
| `disableAllHooks`                 | Nonaktifkan semua [hooks](/id/hooks) dan [status line](/id/statusline) khusus apa pun                                                                                                                                                                                                                                                           | `true`                                                                  |
| `allowManagedHooksOnly`           | (Hanya pengaturan yang dikelola) Cegah pemuatan hook pengguna, proyek, dan plugin. Hanya memungkinkan hook yang dikelola dan hook SDK. Lihat [Konfigurasi Hook](#hook-configuration)                                                                                                                                                            | `true`                                                                  |
| `allowedHttpHookUrls`             | Daftar putih pola URL yang dapat ditargetkan hook HTTP. Mendukung `*` sebagai wildcard. Saat diatur, hook dengan URL yang tidak cocok diblokir. Tidak terdefinisi = tidak ada pembatasan, array kosong = blokir semua hook HTTP. Array digabungkan di seluruh sumber pengaturan. Lihat [Konfigurasi Hook](#hook-configuration)                  | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Daftar putih nama variabel lingkungan yang dapat diinterpolasi hook HTTP ke dalam header. Saat diatur, `allowedEnvVars` efektif setiap hook adalah persimpangan dengan daftar ini. Tidak terdefinisi = tidak ada pembatasan. Array digabungkan di seluruh sumber pengaturan. Lihat [Konfigurasi Hook](#hook-configuration)                      | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Hanya pengaturan yang dikelola) Cegah pengaturan pengguna dan proyek dari mendefinisikan aturan izin `allow`, `ask`, atau `deny`. Hanya aturan dalam pengaturan yang dikelola yang berlaku. Lihat [Pengaturan khusus yang dikelola](/id/permissions#managed-only-settings)                                                                     | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Hanya pengaturan yang dikelola) Hanya `allowedMcpServers` dari pengaturan yang dikelola yang dihormati. `deniedMcpServers` masih digabungkan dari semua sumber. Pengguna masih dapat menambahkan MCP servers, tetapi hanya daftar putih yang ditentukan admin yang berlaku. Lihat [Konfigurasi MCP Managed](/id/mcp#managed-mcp-configuration) | `true`                                                                  |
| `model`                           | Timpa model default untuk digunakan untuk Claude Code                                                                                                                                                                                                                                                                                           | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Batasi model mana yang dapat dipilih pengguna melalui `/model`, `--model`, alat Config, atau `ANTHROPIC_MODEL`. Tidak mempengaruhi opsi Default. Lihat [Batasi pemilihan model](/id/model-config#restrict-model-selection)                                                                                                                      | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Petakan ID model Anthropic ke ID model spesifik penyedia seperti ARN profil inferensi Bedrock. Setiap entri pemilih model menggunakan nilai yang dipetakan saat memanggil API penyedia. Lihat [Timpa ID model per versi](/id/model-config#override-model-ids-per-version)                                                                       | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | Skrip untuk menghasilkan header OpenTelemetry dinamis. Berjalan saat startup dan secara berkala (lihat [Header dinamis](/id/monitoring-usage#dynamic-headers))                                                                                                                                                                                  | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Konfigurasikan status line khusus untuk menampilkan konteks. Lihat [dokumentasi `statusLine`](/id/statusline)                                                                                                                                                                                                                                   | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Konfigurasikan skrip khusus untuk pelengkapan otomatis file `@`. Lihat [Pengaturan saran file](#file-suggestion-settings)                                                                                                                                                                                                                       | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Kontrol apakah pemilih file `@` menghormati pola `.gitignore`. Saat `true` (default), file yang cocok dengan pola `.gitignore` dikecualikan dari saran                                                                                                                                                                                          | `false`                                                                 |
| `outputStyle`                     | Konfigurasikan gaya output untuk menyesuaikan prompt sistem. Lihat [dokumentasi gaya output](/id/output-styles)                                                                                                                                                                                                                                 | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Gunakan `claudeai` untuk membatasi login ke akun Claude.ai, `console` untuk membatasi login ke akun Claude Console (penagihan penggunaan API)                                                                                                                                                                                                   | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Tentukan UUID organisasi untuk secara otomatis memilihnya selama login, melewati langkah pemilihan organisasi. Memerlukan `forceLoginMethod` untuk diatur                                                                                                                                                                                       | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Secara otomatis menyetujui semua MCP servers yang ditentukan dalam file `.mcp.json` proyek                                                                                                                                                                                                                                                      | `true`                                                                  |
| `enabledMcpjsonServers`           | Daftar MCP servers tertentu dari file `.mcp.json` untuk disetujui                                                                                                                                                                                                                                                                               | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Daftar MCP servers tertentu dari file `.mcp.json` untuk ditolak                                                                                                                                                                                                                                                                                 | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Saat diatur dalam managed-settings.json, daftar putih MCP servers yang dapat dikonfigurasi pengguna. Tidak terdefinisi = tidak ada pembatasan, array kosong = lockdown. Berlaku untuk semua cakupan. Daftar hitam memiliki prioritas. Lihat [Konfigurasi MCP Managed](/id/mcp#managed-mcp-configuration)                                        | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Saat diatur dalam managed-settings.json, daftar hitam MCP servers yang secara eksplisit diblokir. Berlaku untuk semua cakupan termasuk server yang dikelola. Daftar hitam memiliki prioritas atas daftar putih. Lihat [Konfigurasi MCP Managed](/id/mcp#managed-mcp-configuration)                                                              | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Saat diatur dalam managed-settings.json, daftar putih marketplace plugin yang dapat ditambahkan pengguna. Tidak terdefinisi = tidak ada pembatasan, array kosong = lockdown. Berlaku hanya untuk penambahan marketplace. Lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions)                 | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Hanya pengaturan yang dikelola) Daftar hitam sumber marketplace. Sumber yang diblokir diperiksa sebelum mengunduh, jadi mereka tidak pernah menyentuh sistem file. Lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions)                                                                      | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Hanya pengaturan yang dikelola) Pesan khusus ditambahkan ke peringatan kepercayaan plugin yang ditampilkan sebelum instalasi. Gunakan ini untuk menambahkan konteks spesifik organisasi, misalnya untuk mengonfirmasi bahwa plugin dari marketplace internal Anda telah disaring.                                                              | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Skrip khusus yang memodifikasi direktori `.aws` (lihat [konfigurasi kredensial lanjutan](/id/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                 | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Skrip khusus yang menampilkan JSON dengan kredensial AWS (lihat [konfigurasi kredensial lanjutan](/id/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                        | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Aktifkan [extended thinking](/id/common-workflows#use-extended-thinking-thinking-mode) secara default untuk semua sesi. Biasanya dikonfigurasi melalui perintah `/config` daripada mengedit langsung                                                                                                                                            | `true`                                                                  |
| `plansDirectory`                  | Sesuaikan di mana file rencana disimpan. Jalur relatif terhadap akar proyek. Default: `~/.claude/plans`                                                                                                                                                                                                                                         | `"./plans"`                                                             |
| `showTurnDuration`                | Tampilkan pesan durasi giliran setelah respons (misalnya, "Cooked for 1m 6s"). Atur ke `false` untuk menyembunyikan pesan ini                                                                                                                                                                                                                   | `true`                                                                  |
| `spinnerVerbs`                    | Sesuaikan kata kerja aksi yang ditampilkan dalam spinner dan pesan durasi giliran. Atur `mode` ke `"replace"` untuk menggunakan hanya kata kerja Anda, atau `"append"` untuk menambahkannya ke default                                                                                                                                          | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Konfigurasikan bahasa respons pilihan Claude (misalnya, `"japanese"`, `"spanish"`, `"french"`). Claude akan merespons dalam bahasa ini secara default                                                                                                                                                                                           | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Saluran rilis untuk diikuti untuk pembaruan. Gunakan `"stable"` untuk versi yang biasanya sekitar satu minggu lama dan melewati versi dengan regresi besar, atau `"latest"` (default) untuk rilis terbaru                                                                                                                                       | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Tampilkan tips dalam spinner saat Claude bekerja. Atur ke `false` untuk menonaktifkan tips (default: `true`)                                                                                                                                                                                                                                    | `false`                                                                 |
| `spinnerTipsOverride`             | Timpa tips spinner dengan string khusus. `tips`: array string tip. `excludeDefault`: jika `true`, hanya tampilkan tip khusus; jika `false` atau tidak ada, tip khusus digabungkan dengan tip bawaan                                                                                                                                             | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Aktifkan bilah kemajuan terminal yang menampilkan kemajuan di terminal yang didukung seperti Windows Terminal dan iTerm2 (default: `true`)                                                                                                                                                                                                      | `false`                                                                 |
| `prefersReducedMotion`            | Kurangi atau nonaktifkan animasi UI (spinner, shimmer, efek flash) untuk aksesibilitas                                                                                                                                                                                                                                                          | `true`                                                                  |
| `fastModePerSessionOptIn`         | Saat `true`, mode cepat tidak bertahan di seluruh sesi. Setiap sesi dimulai dengan mode cepat mati, memerlukan pengguna untuk mengaktifkannya dengan `/fast`. Preferensi mode cepat pengguna masih disimpan. Lihat [Memerlukan opt-in per sesi](/id/fast-mode#require-per-session-opt-in)                                                       | `true`                                                                  |
| `teammateMode`                    | Bagaimana [rekan tim agent](/id/agent-teams) ditampilkan: `auto` (memilih panel terpisah di tmux atau iTerm2, in-process sebaliknya), `in-process`, atau `tmux`. Lihat [atur agent teams](/id/agent-teams#set-up-agent-teams)                                                                                                                   | `"in-process"`                                                          |

### Pengaturan izin

| Kunci                          | Deskripsi                                                                                                                                                                                                                                           | Contoh                                                                 |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Array aturan izin untuk memungkinkan penggunaan alat. Lihat [Sintaks aturan izin](#permission-rule-syntax) di bawah untuk detail pencocokan pola                                                                                                    | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Array aturan izin untuk meminta konfirmasi saat penggunaan alat. Lihat [Sintaks aturan izin](#permission-rule-syntax) di bawah                                                                                                                      | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Array aturan izin untuk menolak penggunaan alat. Gunakan ini untuk mengecualikan file sensitif dari akses Claude Code. Lihat [Sintaks aturan izin](#permission-rule-syntax) dan [Batasan izin Bash](/id/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Direktori kerja](/id/permissions#working-directories) tambahan yang dapat diakses Claude                                                                                                                                                           | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | Mode [izin](/id/permissions#permission-modes) default saat membuka Claude Code                                                                                                                                                                      | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Atur ke `"disable"` untuk mencegah mode `bypassPermissions` diaktifkan. Ini menonaktifkan bendera baris perintah `--dangerously-skip-permissions`. Lihat [pengaturan yang dikelola](/id/permissions#managed-only-settings)                          | `"disable"`                                                            |

### Sintaks aturan izin

Aturan izin mengikuti format `Tool` atau `Tool(specifier)`. Aturan dievaluasi secara berurutan: aturan deny terlebih dahulu, kemudian ask, kemudian allow. Aturan pertama yang cocok menang.

Contoh cepat:

| Aturan                         | Efek                                                |
| :----------------------------- | :-------------------------------------------------- |
| `Bash`                         | Cocok dengan semua perintah Bash                    |
| `Bash(npm run *)`              | Cocok dengan perintah yang dimulai dengan `npm run` |
| `Read(./.env)`                 | Cocok dengan membaca file `.env`                    |
| `WebFetch(domain:example.com)` | Cocok dengan permintaan fetch ke example.com        |

Untuk referensi sintaks aturan lengkap, termasuk perilaku wildcard, pola spesifik alat untuk Read, Edit, WebFetch, MCP, dan aturan Agent, dan batasan keamanan pola Bash, lihat [Sintaks aturan izin](/id/permissions#permission-rule-syntax).

### Pengaturan sandbox

Konfigurasikan perilaku sandboxing lanjutan. Sandboxing mengisolasi perintah bash dari sistem file dan jaringan Anda. Lihat [Sandboxing](/id/sandboxing) untuk detail.

| Kunci                             | Deskripsi                                                                                                                                                                                                                                                                                                                                                                      | Contoh                          |
| :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | Aktifkan bash sandboxing (macOS, Linux, dan WSL2). Default: false                                                                                                                                                                                                                                                                                                              | `true`                          |
| `autoAllowBashIfSandboxed`        | Persetujuan otomatis perintah bash saat sandboxed. Default: true                                                                                                                                                                                                                                                                                                               | `true`                          |
| `excludedCommands`                | Perintah yang harus dijalankan di luar sandbox                                                                                                                                                                                                                                                                                                                                 | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Izinkan perintah untuk dijalankan di luar sandbox melalui parameter `dangerouslyDisableSandbox`. Saat diatur ke `false`, pintu keluar `dangerouslyDisableSandbox` sepenuhnya dinonaktifkan dan semua perintah harus dijalankan sandboxed (atau berada dalam `excludedCommands`). Berguna untuk kebijakan perusahaan yang memerlukan sandboxing ketat. Default: true            | `false`                         |
| `filesystem.allowWrite`           | Jalur tambahan di mana perintah sandboxed dapat menulis. Array digabungkan di semua cakupan pengaturan: jalur pengguna, proyek, dan yang dikelola digabungkan, bukan diganti. Juga digabungkan dengan jalur dari aturan izin `Edit(...)` allow. Lihat [prefiks jalur sandbox](#sandbox-path-prefixes) di bawah.                                                                | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Jalur di mana perintah sandboxed tidak dapat menulis. Array digabungkan di semua cakupan pengaturan. Juga digabungkan dengan jalur dari aturan izin `Edit(...)` deny.                                                                                                                                                                                                          | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Jalur di mana perintah sandboxed tidak dapat membaca. Array digabungkan di semua cakupan pengaturan. Juga digabungkan dengan jalur dari aturan izin `Read(...)` deny.                                                                                                                                                                                                          | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Jalur soket Unix yang dapat diakses dalam sandbox (untuk agen SSH, dll.)                                                                                                                                                                                                                                                                                                       | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Izinkan semua koneksi soket Unix dalam sandbox. Default: false                                                                                                                                                                                                                                                                                                                 | `true`                          |
| `network.allowLocalBinding`       | Izinkan pengikatan ke port localhost (hanya macOS). Default: false                                                                                                                                                                                                                                                                                                             | `true`                          |
| `network.allowedDomains`          | Array domain untuk memungkinkan lalu lintas jaringan keluar. Mendukung wildcard (misalnya, `*.example.com`).                                                                                                                                                                                                                                                                   | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Hanya pengaturan yang dikelola) Hanya `allowedDomains` dan aturan allow `WebFetch(domain:...)` dari pengaturan yang dikelola yang dihormati. Domain dari pengaturan pengguna, proyek, dan lokal diabaikan. Domain yang tidak diizinkan diblokir secara otomatis tanpa meminta pengguna. Domain yang ditolak masih dihormati dari semua sumber. Default: false                 | `true`                          |
| `network.httpProxyPort`           | Port proxy HTTP yang digunakan jika Anda ingin membawa proxy Anda sendiri. Jika tidak ditentukan, Claude akan menjalankan proxy-nya sendiri.                                                                                                                                                                                                                                   | `8080`                          |
| `network.socksProxyPort`          | Port proxy SOCKS5 yang digunakan jika Anda ingin membawa proxy Anda sendiri. Jika tidak ditentukan, Claude akan menjalankan proxy-nya sendiri.                                                                                                                                                                                                                                 | `8081`                          |
| `enableWeakerNestedSandbox`       | Aktifkan sandbox yang lebih lemah untuk lingkungan Docker yang tidak istimewa (hanya Linux dan WSL2). **Mengurangi keamanan.** Default: false                                                                                                                                                                                                                                  | `true`                          |
| `enableWeakerNetworkIsolation`    | (Hanya macOS) Izinkan akses ke layanan kepercayaan TLS sistem (`com.apple.trustd.agent`) dalam sandbox. Diperlukan untuk alat berbasis Go seperti `gh`, `gcloud`, dan `terraform` untuk memverifikasi sertifikat TLS saat menggunakan `httpProxyPort` dengan proxy MITM dan CA khusus. **Mengurangi keamanan** dengan membuka jalur eksfiltrasi data potensial. Default: false | `true`                          |

#### Prefiks jalur sandbox

Jalur dalam `filesystem.allowWrite`, `filesystem.denyWrite`, dan `filesystem.denyRead` mendukung prefiks ini:

| Prefiks                     | Arti                                              | Contoh                                 |
| :-------------------------- | :------------------------------------------------ | :------------------------------------- |
| `//`                        | Jalur absolut dari akar sistem file               | `//tmp/build` menjadi `/tmp/build`     |
| `~/`                        | Relatif terhadap direktori home                   | `~/.kube` menjadi `$HOME/.kube`        |
| `/`                         | Relatif terhadap direktori file pengaturan        | `/build` menjadi `$SETTINGS_DIR/build` |
| `./` atau tidak ada prefiks | Jalur relatif (diselesaikan oleh runtime sandbox) | `./output`                             |

**Contoh konfigurasi:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**Pembatasan sistem file dan jaringan** dapat dikonfigurasi dalam dua cara yang digabungkan bersama:

* **Pengaturan `sandbox.filesystem`** (ditampilkan di atas): Kontrol jalur pada batas sandbox tingkat OS. Pembatasan ini berlaku untuk semua perintah subprocess (misalnya, `kubectl`, `terraform`, `npm`), bukan hanya alat file Claude.
* **Aturan izin**: Gunakan aturan allow/deny `Edit` untuk mengontrol akses alat file Claude, aturan deny `Read` untuk memblokir pembacaan, dan aturan allow/deny `WebFetch` untuk mengontrol domain jaringan. Jalur dari aturan ini juga digabungkan ke dalam konfigurasi sandbox.

### Pengaturan atribusi

Claude Code menambahkan atribusi ke komit git dan permintaan tarik. Ini dikonfigurasi secara terpisah:

* Komit menggunakan [git trailers](https://git-scm.com/docs/git-interpret-trailers) (seperti `Co-Authored-By`) secara default, yang dapat disesuaikan atau dinonaktifkan
* Deskripsi permintaan tarik adalah teks biasa

| Kunci    | Deskripsi                                                                                         |
| :------- | :------------------------------------------------------------------------------------------------ |
| `commit` | Atribusi untuk komit git, termasuk trailer apa pun. String kosong menyembunyikan atribusi komit   |
| `pr`     | Atribusi untuk deskripsi permintaan tarik. String kosong menyembunyikan atribusi permintaan tarik |

**Atribusi komit default:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Atribusi permintaan tarik default:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Contoh:**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  Pengaturan `attribution` memiliki prioritas atas pengaturan `includeCoAuthoredBy` yang tidak direkomendasikan. Untuk menyembunyikan semua atribusi, atur `commit` dan `pr` ke string kosong.
</Note>

### Pengaturan saran file

Konfigurasikan perintah khusus untuk pelengkapan otomatis jalur file `@`. Saran file bawaan menggunakan traversal sistem file cepat, tetapi monorepo besar mungkin mendapat manfaat dari pengindeksan spesifik proyek seperti indeks file yang telah dibangun sebelumnya atau alat khusus.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Perintah berjalan dengan variabel lingkungan yang sama dengan [hooks](/id/hooks), termasuk `CLAUDE_PROJECT_DIR`. Ini menerima JSON melalui stdin dengan bidang `query`:

```json  theme={null}
{"query": "src/comp"}
```

Keluarkan jalur file yang dipisahkan baris baru ke stdout (saat ini dibatasi hingga 15):

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Contoh:**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Konfigurasi hook

Pengaturan ini mengontrol hook mana yang diizinkan untuk dijalankan dan apa yang dapat diakses hook HTTP. Pengaturan `allowManagedHooksOnly` hanya dapat dikonfigurasi dalam [pengaturan yang dikelola](#settings-files). Daftar putih URL dan env var dapat diatur di tingkat pengaturan apa pun dan digabungkan di seluruh sumber.

**Perilaku saat `allowManagedHooksOnly` adalah `true`:**

* Hook yang dikelola dan hook SDK dimuat
* Hook pengguna, hook proyek, dan hook plugin diblokir

**Batasi URL hook HTTP:**

Batasi URL mana yang dapat ditargetkan hook HTTP. Mendukung `*` sebagai wildcard untuk pencocokan. Saat array didefinisikan, hook HTTP yang menargetkan URL yang tidak cocok diblokir secara diam-diam.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Batasi variabel lingkungan hook HTTP:**

Batasi nama variabel lingkungan mana yang dapat diinterpolasi hook HTTP ke dalam nilai header. `allowedEnvVars` efektif setiap hook adalah persimpangan dari daftar sendiri dan pengaturan ini.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Preseden pengaturan

Pengaturan berlaku dalam urutan preseden. Dari tertinggi ke terendah:

1. **Pengaturan yang dikelola** ([yang dikelola server](/id/server-managed-settings), [kebijakan tingkat MDM/OS](#configuration-scopes), atau [pengaturan yang dikelola](/id/settings#settings-files))
   * Kebijakan yang digunakan oleh IT melalui pengiriman server, profil konfigurasi MDM, kebijakan registry, atau file pengaturan yang dikelola
   * Tidak dapat ditimpa oleh tingkat lain apa pun, termasuk argumen baris perintah
   * Dalam tingkat yang dikelola, preseden adalah: yang dikelola server > kebijakan tingkat MDM/OS > `managed-settings.json` > registry HKCU (hanya Windows). Hanya satu sumber yang dikelola yang digunakan; sumber tidak digabungkan.

2. **Argumen baris perintah**
   * Penggantian sementara untuk sesi tertentu

3. **Pengaturan proyek lokal** (`.claude/settings.local.json`)
   * Pengaturan proyek pribadi

4. **Pengaturan proyek bersama** (`.claude/settings.json`)
   * Pengaturan proyek bersama tim dalam kontrol sumber

5. **Pengaturan pengguna** (`~/.claude/settings.json`)
   * Pengaturan global pribadi

Hierarki ini memastikan bahwa kebijakan organisasi selalu diterapkan sambil tetap memungkinkan tim dan individu untuk menyesuaikan pengalaman mereka.

Misalnya, jika pengaturan pengguna Anda memungkinkan `Bash(npm run *)` tetapi pengaturan bersama proyek menolaknya, pengaturan proyek memiliki prioritas dan perintah diblokir.

<Note>
  **Pengaturan array digabungkan di seluruh cakupan.** Ketika pengaturan bernilai array yang sama (seperti `sandbox.filesystem.allowWrite` atau `permissions.allow`) muncul dalam beberapa cakupan, array **digabungkan dan dideduplikasi**, bukan diganti. Ini berarti cakupan prioritas lebih rendah dapat menambahkan entri tanpa menimpa yang ditetapkan oleh cakupan prioritas lebih tinggi, dan sebaliknya. Misalnya, jika pengaturan yang dikelola menetapkan `allowWrite` ke `["//opt/company-tools"]` dan pengguna menambahkan `["~/.kube"]`, kedua jalur disertakan dalam konfigurasi akhir.
</Note>

### Verifikasi pengaturan aktif

Jalankan `/status` di dalam Claude Code untuk melihat sumber pengaturan mana yang aktif dan dari mana asalnya. Output menampilkan setiap lapisan konfigurasi (managed, user, project) bersama dengan asalnya, seperti `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, atau `Enterprise managed settings (file)`. Jika file pengaturan berisi kesalahan, `/status` melaporkan masalah sehingga Anda dapat memperbaikinya.

### Poin kunci tentang sistem konfigurasi

* **File memori (`CLAUDE.md`)**: Berisi instruksi dan konteks yang dimuat Claude saat startup
* **File pengaturan (JSON)**: Konfigurasikan izin, variabel lingkungan, dan perilaku alat
* **Skills**: Prompt khusus yang dapat dipanggil dengan `/skill-name` atau dimuat oleh Claude secara otomatis
* **MCP servers**: Perluas Claude Code dengan alat dan integrasi tambahan
* **Preseden**: Konfigurasi tingkat lebih tinggi (Managed) menimpa yang tingkat lebih rendah (User/Project)
* **Warisan**: Pengaturan digabungkan, dengan pengaturan yang lebih spesifik menambah atau menimpa yang lebih luas

### Prompt sistem

Prompt sistem internal Claude Code tidak dipublikasikan. Untuk menambahkan instruksi khusus, gunakan file `CLAUDE.md` atau bendera `--append-system-prompt`.

### Mengecualikan file sensitif

Untuk mencegah Claude Code mengakses file yang berisi informasi sensitif seperti kunci API, rahasia, dan file lingkungan, gunakan pengaturan `permissions.deny` dalam file `.claude/settings.json` Anda:

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Ini menggantikan konfigurasi `ignorePatterns` yang tidak direkomendasikan. File yang cocok dengan pola ini dikecualikan dari penemuan file dan hasil pencarian, dan operasi baca pada file ini ditolak.

## Konfigurasi subagent

Claude Code mendukung subagent AI khusus yang dapat dikonfigurasi di tingkat pengguna dan proyek. Subagent ini disimpan sebagai file Markdown dengan frontmatter YAML:

* **Subagent pengguna**: `~/.claude/agents/` - Tersedia di semua proyek Anda
* **Subagent proyek**: `.claude/agents/` - Spesifik untuk proyek Anda dan dapat dibagikan dengan tim Anda

File subagent mendefinisikan asisten AI khusus dengan prompt khusus dan izin alat. Pelajari lebih lanjut tentang membuat dan menggunakan subagent dalam [dokumentasi subagent](/id/sub-agents).

## Konfigurasi plugin

Claude Code mendukung sistem plugin yang memungkinkan Anda memperluas fungsionalitas dengan skills, agents, hooks, dan MCP servers. Plugin didistribusikan melalui marketplace dan dapat dikonfigurasi di tingkat pengguna dan repositori.

### Pengaturan plugin

Pengaturan terkait plugin dalam `settings.json`:

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

Mengontrol plugin mana yang diaktifkan. Format: `"plugin-name@marketplace-name": true/false`

**Cakupan**:

* **Pengaturan pengguna** (`~/.claude/settings.json`): Preferensi plugin pribadi
* **Pengaturan proyek** (`.claude/settings.json`): Plugin spesifik proyek yang dibagikan dengan tim
* **Pengaturan lokal** (`.claude/settings.local.json`): Penggantian per-mesin (tidak dikomit)

**Contoh**:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Mendefinisikan marketplace tambahan yang harus tersedia untuk repositori. Biasanya digunakan dalam pengaturan tingkat repositori untuk memastikan anggota tim memiliki akses ke sumber plugin yang diperlukan.

**Ketika repositori menyertakan `extraKnownMarketplaces`**:

1. Anggota tim diminta untuk menginstal marketplace saat mereka mempercayai folder
2. Anggota tim kemudian diminta untuk menginstal plugin dari marketplace itu
3. Pengguna dapat melewati marketplace atau plugin yang tidak diinginkan (disimpan dalam pengaturan pengguna)
4. Instalasi menghormati batas kepercayaan dan memerlukan persetujuan eksplisit

**Contoh**:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Jenis sumber marketplace**:

* `github`: Repositori GitHub (menggunakan `repo`)
* `git`: URL git apa pun (menggunakan `url`)
* `directory`: Jalur sistem file lokal (menggunakan `path`, hanya untuk pengembangan)
* `hostPattern`: Pola regex untuk mencocokkan host marketplace (menggunakan `hostPattern`)

#### `strictKnownMarketplaces`

**Hanya pengaturan yang dikelola**: Mengontrol marketplace plugin mana yang diizinkan pengguna untuk ditambahkan. Pengaturan ini hanya dapat dikonfigurasi dalam [pengaturan yang dikelola](/id/settings#settings-files) dan memberikan administrator kontrol ketat atas sumber marketplace.

**Lokasi file pengaturan yang dikelola**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux dan WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Karakteristik kunci**:

* Hanya tersedia dalam pengaturan yang dikelola (`managed-settings.json`)
* Tidak dapat ditimpa oleh pengaturan pengguna atau proyek (preseden tertinggi)
* Diterapkan SEBELUM operasi jaringan/sistem file (sumber yang diblokir tidak pernah dieksekusi)
* Menggunakan pencocokan tepat untuk spesifikasi sumber (termasuk `ref`, `path` untuk sumber git), kecuali `hostPattern`, yang menggunakan pencocokan regex

**Perilaku daftar putih**:

* `undefined` (default): Tidak ada pembatasan - pengguna dapat menambahkan marketplace apa pun
* Array kosong `[]`: Lockdown lengkap - pengguna tidak dapat menambahkan marketplace baru apa pun
* Daftar sumber: Pengguna hanya dapat menambahkan marketplace yang cocok dengan tepat

**Semua jenis sumber yang didukung**:

Daftar putih mendukung tujuh jenis sumber marketplace. Sebagian besar sumber menggunakan pencocokan tepat, sementara `hostPattern` menggunakan pencocokan regex terhadap host marketplace.

1. **Repositori GitHub**:

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Bidang: `repo` (diperlukan), `ref` (opsional: cabang/tag/SHA), `path` (opsional: subdirektori)

2. **Repositori Git**:

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Bidang: `url` (diperlukan), `ref` (opsional: cabang/tag/SHA), `path` (opsional: subdirektori)

3. **Marketplace berbasis URL**:

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Bidang: `url` (diperlukan), `headers` (opsional: header HTTP untuk akses terautentikasi)

<Note>
  Marketplace berbasis URL hanya mengunduh file `marketplace.json`. Mereka tidak mengunduh file plugin dari server. Plugin dalam marketplace berbasis URL harus menggunakan sumber eksternal (GitHub, npm, atau URL git) daripada jalur relatif. Untuk plugin dengan jalur relatif, gunakan marketplace berbasis Git sebagai gantinya. Lihat [Troubleshooting](/id/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) untuk detail.
</Note>

4. **Paket NPM**:

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Bidang: `package` (diperlukan, mendukung paket yang diberi cakupan)

5. **Jalur file**:

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Bidang: `path` (diperlukan: jalur absolut ke file marketplace.json)

6. **Jalur direktori**:

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Bidang: `path` (diperlukan: jalur absolut ke direktori yang berisi `.claude-plugin/marketplace.json`)

7. **Pencocokan pola host**:

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Bidang: `hostPattern` (diperlukan: pola regex untuk mencocokkan terhadap host marketplace)

Gunakan pencocokan pola host saat Anda ingin memungkinkan semua marketplace dari host tertentu tanpa menghitung setiap repositori secara individual. Ini berguna untuk organisasi dengan server GitHub Enterprise atau GitLab internal di mana pengembang membuat marketplace mereka sendiri.

Ekstraksi host berdasarkan jenis sumber:

* `github`: selalu cocok dengan `github.com`
* `git`: mengekstrak nama host dari URL (mendukung format HTTPS dan SSH)
* `url`: mengekstrak nama host dari URL
* `npm`, `file`, `directory`: tidak didukung untuk pencocokan pola host

**Contoh konfigurasi**:

Contoh: izinkan marketplace tertentu saja:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Contoh - Nonaktifkan semua penambahan marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Contoh: izinkan semua marketplace dari server git internal:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Persyaratan pencocokan tepat**:

Sumber marketplace harus cocok **dengan tepat** agar penambahan pengguna diizinkan. Untuk sumber berbasis git (`github` dan `git`), ini termasuk semua bidang opsional:

* `repo` atau `url` harus cocok dengan tepat
* Bidang `ref` harus cocok dengan tepat (atau keduanya tidak terdefinisi)
* Bidang `path` harus cocok dengan tepat (atau keduanya tidak terdefinisi)

Contoh sumber yang **TIDAK cocok**:

```json  theme={null}
// Ini adalah sumber BERBEDA:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Ini juga BERBEDA:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Perbandingan dengan `extraKnownMarketplaces`**:

| Aspek                | `strictKnownMarketplaces`                           | `extraKnownMarketplaces`                    |
| -------------------- | --------------------------------------------------- | ------------------------------------------- |
| **Tujuan**           | Penegakan kebijakan organisasi                      | Kenyamanan tim                              |
| **File pengaturan**  | Hanya `managed-settings.json`                       | File pengaturan apa pun                     |
| **Perilaku**         | Blokir penambahan yang tidak ada dalam daftar putih | Instal otomatis marketplace yang hilang     |
| **Saat diterapkan**  | Sebelum operasi jaringan/sistem file                | Setelah prompt kepercayaan pengguna         |
| **Dapat ditimpa**    | Tidak (preseden tertinggi)                          | Ya (oleh pengaturan prioritas lebih tinggi) |
| **Format sumber**    | Objek sumber langsung                               | Marketplace bernama dengan sumber bersarang |
| **Kasus penggunaan** | Kepatuhan, pembatasan keamanan                      | Onboarding, standardisasi                   |

**Perbedaan format**:

`strictKnownMarketplaces` menggunakan objek sumber langsung:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` memerlukan marketplace bernama:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Catatan penting**:

* Pembatasan diperiksa SEBELUM permintaan jaringan atau operasi sistem file apa pun
* Saat diblokir, pengguna melihat pesan kesalahan yang jelas yang menunjukkan sumber diblokir oleh kebijakan yang dikelola
* Pembatasan hanya berlaku untuk menambahkan marketplace BARU; marketplace yang sebelumnya diinstal tetap dapat diakses
* Pengaturan yang dikelola memiliki preseden tertinggi dan tidak dapat ditimpa

Lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions) untuk dokumentasi yang menghadap pengguna.

### Mengelola plugin

Gunakan perintah `/plugin` untuk mengelola plugin secara interaktif:

* Jelajahi plugin yang tersedia dari marketplace
* Instal/copot plugin
* Aktifkan/nonaktifkan plugin
* Lihat detail plugin (perintah, agent, hook yang disediakan)
* Tambah/hapus marketplace

Pelajari lebih lanjut tentang sistem plugin dalam [dokumentasi plugin](/id/plugins).

## Variabel lingkungan

Claude Code mendukung variabel lingkungan berikut untuk mengontrol perilakunya:

<Note>
  Semua variabel lingkungan juga dapat dikonfigurasi dalam [`settings.json`](#available-settings). Ini berguna sebagai cara untuk secara otomatis menetapkan variabel lingkungan untuk setiap sesi, atau untuk meluncurkan serangkaian variabel lingkungan untuk seluruh tim atau organisasi Anda.
</Note>

| Variabel                                       | Tujuan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | Kunci API dikirim sebagai header `X-Api-Key`, biasanya untuk SDK Claude (untuk penggunaan interaktif, jalankan `/login`)                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `ANTHROPIC_AUTH_TOKEN`                         | Nilai khusus untuk header `Authorization` (nilai yang Anda atur di sini akan diawali dengan `Bearer `)                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | Header khusus untuk ditambahkan ke permintaan (format `Name: Value`, dipisahkan baris baru untuk beberapa header)                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | Lihat [Konfigurasi Model](/id/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | Lihat [Konfigurasi Model](/id/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | Lihat [Konfigurasi Model](/id/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Kunci API untuk autentikasi Microsoft Foundry (lihat [Microsoft Foundry](/id/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | URL dasar lengkap untuk sumber daya Foundry (misalnya, `https://my-resource.services.ai.azure.com/anthropic`). Alternatif untuk `ANTHROPIC_FOUNDRY_RESOURCE` (lihat [Microsoft Foundry](/id/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                             |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Nama sumber daya Foundry (misalnya, `my-resource`). Diperlukan jika `ANTHROPIC_FOUNDRY_BASE_URL` tidak diatur (lihat [Microsoft Foundry](/id/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `ANTHROPIC_MODEL`                              | Nama pengaturan model untuk digunakan (lihat [Konfigurasi Model](/id/model-config#environment-variables))                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[TIDAK DIREKOMENDASIKAN] Nama [model kelas Haiku untuk tugas latar belakang](/id/costs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Timpa wilayah AWS untuk model kelas Haiku saat menggunakan Bedrock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Kunci API Bedrock untuk autentikasi (lihat [Kunci API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | Timeout default untuk perintah bash yang berjalan lama                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | Jumlah maksimum karakter dalam output bash sebelum dipotong di tengah                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `BASH_MAX_TIMEOUT_MS`                          | Timeout maksimum yang dapat ditetapkan model untuk perintah bash yang berjalan lama                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | Atur persentase kapasitas konteks (1-100) di mana auto-compaction dipicu. Secara default, auto-compaction dipicu pada kapasitas sekitar 95%. Gunakan nilai lebih rendah seperti `50` untuk compact lebih awal. Nilai di atas ambang default tidak berpengaruh. Berlaku untuk percakapan utama dan subagent. Persentase ini selaras dengan bidang `context_window.used_percentage` yang tersedia dalam [status line](/id/statusline)                                                                                                                         |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | Kembali ke direktori kerja asli setelah setiap perintah Bash                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | UUID akun untuk pengguna yang terautentikasi. Digunakan oleh pemanggil SDK untuk memberikan informasi akun secara sinkron, menghindari kondisi balapan di mana acara telemetri awal kekurangan metadata akun. Memerlukan `CLAUDE_CODE_USER_EMAIL` dan `CLAUDE_CODE_ORGANIZATION_UUID` juga diatur                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Atur ke `1` untuk memuat file CLAUDE.md dari direktori yang ditentukan dengan `--add-dir`. Secara default, direktori tambahan tidak memuat file memori                                                                                                                                                                                                                                                                                                                                                                                                      | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | Interval dalam milidetik di mana kredensial harus disegarkan (saat menggunakan `apiKeyHelper`)                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | Jalur ke file sertifikat klien untuk autentikasi mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | Jalur ke file kunci pribadi klien untuk autentikasi mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | Frasa sandi untuk `CLAUDE_CODE_CLIENT_KEY` terenkripsi (opsional)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | Atur ke `1` untuk menonaktifkan dukungan [jendela konteks 1M](/id/model-config#extended-context). Saat diatur, varian model 1M tidak tersedia dalam pemilih model. Berguna untuk lingkungan perusahaan dengan persyaratan kepatuhan                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Atur ke `1` untuk menonaktifkan [penalaran adaptif](/id/model-config#adjust-effort-level) untuk Opus 4.6 dan Sonnet 4.6. Saat dinonaktifkan, model ini kembali ke anggaran pemikiran tetap yang dikendalikan oleh `MAX_THINKING_TOKENS`                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | Atur ke `1` untuk menonaktifkan [auto memory](/id/memory#auto-memory). Atur ke `0` untuk memaksa auto memory selama peluncuran bertahap. Saat dinonaktifkan, Claude tidak membuat atau memuat file auto memory                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Atur ke `1` untuk menghapus instruksi alur kerja komit dan PR bawaan dari prompt sistem Claude. Berguna saat menggunakan skill alur kerja git Anda sendiri. Memiliki prioritas atas pengaturan [`includeGitInstructions`](#available-settings) saat diatur                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | Atur ke `1` untuk menonaktifkan semua fungsionalitas tugas latar belakang, termasuk parameter `run_in_background` pada alat Bash dan subagent, auto-backgrounding, dan pintasan Ctrl+B                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | Atur ke `1` untuk menonaktifkan [tugas terjadwal](/id/scheduled-tasks). Skill `/loop` dan alat cron menjadi tidak tersedia dan tugas yang sudah dijadwalkan berhenti berfungsi, termasuk tugas yang sudah berjalan di tengah sesi                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Atur ke `1` untuk menonaktifkan header `anthropic-beta` spesifik API Anthropic. Gunakan ini jika mengalami masalah seperti "Unexpected value(s) for the `anthropic-beta` header" saat menggunakan gateway LLM dengan penyedia pihak ketiga                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | Atur ke `1` untuk menonaktifkan [mode cepat](/id/fast-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | Atur ke `1` untuk menonaktifkan survei kualitas sesi "How is Claude doing?". Juga dinonaktifkan saat menggunakan penyedia pihak ketiga atau saat telemetri dinonaktifkan. Lihat [Survei kualitas sesi](/id/data-usage#session-quality-surveys)                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | Setara dengan pengaturan `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING`, dan `DISABLE_TELEMETRY`                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | Atur ke `1` untuk menonaktifkan pembaruan judul terminal otomatis berdasarkan konteks percakapan                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | Atur tingkat upaya untuk model yang didukung. Nilai: `low`, `medium`, `high`. Upaya lebih rendah lebih cepat dan lebih murah, upaya lebih tinggi memberikan penalaran lebih dalam. Didukung pada Opus 4.6 dan Sonnet 4.6. Lihat [Sesuaikan tingkat upaya](/id/model-config#adjust-effort-level)                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | Atur ke `false` untuk menonaktifkan saran prompt (toggle "Prompt suggestions" dalam `/config`). Ini adalah prediksi yang diarsir yang muncul dalam input prompt Anda setelah Claude merespons. Lihat [Saran prompt](/id/interactive-mode#prompt-suggestions)                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | Atur ke `false` untuk sementara kembali ke daftar TODO sebelumnya daripada sistem pelacakan tugas. Default: `true`. Lihat [Daftar tugas](/id/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | Atur ke `1` untuk mengaktifkan pengumpulan data OpenTelemetry untuk metrik dan logging. Diperlukan sebelum mengonfigurasi pengekspor OTel. Lihat [Monitoring](/id/monitoring-usage)                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | Waktu dalam milidetik untuk menunggu setelah loop kueri menjadi idle sebelum keluar secara otomatis. Berguna untuk alur kerja otomatis dan skrip menggunakan mode SDK                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | Atur ke `1` untuk mengaktifkan [agent teams](/id/agent-teams). Agent teams bersifat eksperimental dan dinonaktifkan secara default                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | Timpa batas token default untuk pembacaan file. Berguna saat Anda perlu membaca file yang lebih besar secara penuh                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Atur ke `1` untuk menyembunyikan alamat email dan nama organisasi Anda dari UI Claude Code. Berguna saat streaming atau merekam                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | Lewati instalasi otomatis ekstensi IDE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | Atur jumlah maksimum token output untuk sebagian besar permintaan. Default: 32,000. Maksimum: 64,000. Meningkatkan nilai ini mengurangi jendela konteks efektif yang tersedia sebelum [auto-compaction](/id/costs#reduce-token-usage) dipicu.                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | UUID organisasi untuk pengguna yang terautentikasi. Digunakan oleh pemanggil SDK untuk memberikan informasi akun secara sinkron. Memerlukan `CLAUDE_CODE_ACCOUNT_UUID` dan `CLAUDE_CODE_USER_EMAIL` juga diatur                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | Interval untuk menyegarkan header OpenTelemetry dinamis dalam milidetik (default: 1740000 / 29 menit). Lihat [Header dinamis](/id/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | Secara otomatis diatur ke `true` pada [agent team](/id/agent-teams) rekan kerja yang memerlukan persetujuan rencana. Baca-saja: diatur oleh Claude Code saat menghasilkan rekan kerja. Lihat [memerlukan persetujuan rencana](/id/agent-teams#require-plan-approval-for-teammates)                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | Timeout dalam milidetik untuk operasi git saat menginstal atau memperbarui plugin (default: 120000). Tingkatkan nilai ini untuk repositori besar atau koneksi jaringan lambat. Lihat [Operasi Git habis waktu](/id/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | Atur ke `true` untuk memungkinkan proxy melakukan resolusi DNS daripada pemanggil. Opt-in untuk lingkungan di mana proxy harus menangani resolusi nama host                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SHELL`                            | Timpa deteksi shell otomatis. Berguna saat shell login Anda berbeda dari shell kerja pilihan Anda (misalnya, `bash` vs `zsh`)                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | Prefiks perintah untuk membungkus semua perintah bash (misalnya, untuk logging atau auditing). Contoh: `/path/to/logger.sh` akan mengeksekusi `/path/to/logger.sh <command>`                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_SIMPLE`                           | Atur ke `1` untuk menjalankan dengan prompt sistem minimal dan hanya alat Bash, pembacaan file, dan pengeditan file. Menonaktifkan alat MCP, lampiran, hook, dan file CLAUDE.md                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Lewati autentikasi AWS untuk Bedrock (misalnya, saat menggunakan gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Lewati autentikasi Azure untuk Microsoft Foundry (misalnya, saat menggunakan gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Lewati autentikasi Google untuk Vertex (misalnya, saat menggunakan gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | Lihat [Konfigurasi Model](/id/model-config)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | Bagikan daftar tugas di seluruh sesi. Atur ID yang sama dalam beberapa instans Claude Code untuk berkoordinasi pada daftar tugas bersama. Lihat [Daftar tugas](/id/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_TEAM_NAME`                        | Nama agent team yang dimiliki rekan kerja ini. Diatur secara otomatis pada anggota [agent team](/id/agent-teams)                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_TMPDIR`                           | Timpa direktori temp yang digunakan untuk file temp internal. Claude Code menambahkan `/claude/` ke jalur ini. Default: `/tmp` pada Unix/macOS, `os.tmpdir()` pada Windows                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_USER_EMAIL`                       | Alamat email untuk pengguna yang terautentikasi. Digunakan oleh pemanggil SDK untuk memberikan informasi akun secara sinkron. Memerlukan `CLAUDE_CODE_ACCOUNT_UUID` dan `CLAUDE_CODE_ORGANIZATION_UUID` juga diatur                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | Gunakan [Bedrock](/id/amazon-bedrock)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | Gunakan [Microsoft Foundry](/id/microsoft-foundry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_USE_VERTEX`                       | Gunakan [Vertex](/id/google-vertex-ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CONFIG_DIR`                            | Sesuaikan di mana Claude Code menyimpan file konfigurasi dan datanya                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `DISABLE_AUTOUPDATER`                          | Atur ke `1` untuk menonaktifkan pembaruan otomatis.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_BUG_COMMAND`                          | Atur ke `1` untuk menonaktifkan perintah `/bug`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_COST_WARNINGS`                        | Atur ke `1` untuk menonaktifkan pesan peringatan biaya                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `DISABLE_ERROR_REPORTING`                      | Atur ke `1` untuk keluar dari pelaporan kesalahan Sentry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_INSTALLATION_CHECKS`                  | Atur ke `1` untuk menonaktifkan peringatan instalasi. Gunakan hanya saat mengelola lokasi instalasi secara manual, karena ini dapat menyembunyikan masalah dengan instalasi standar                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | Atur ke `1` untuk menonaktifkan panggilan model untuk jalur non-kritis seperti teks flavor                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `DISABLE_PROMPT_CACHING`                       | Atur ke `1` untuk menonaktifkan prompt caching untuk semua model (memiliki prioritas atas pengaturan per-model)                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Atur ke `1` untuk menonaktifkan prompt caching untuk model Haiku                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Atur ke `1` untuk menonaktifkan prompt caching untuk model Opus                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Atur ke `1` untuk menonaktifkan prompt caching untuk model Sonnet                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `DISABLE_TELEMETRY`                            | Atur ke `1` untuk keluar dari telemetri Statsig (perhatikan bahwa acara Statsig tidak menyertakan data pengguna seperti kode, jalur file, atau perintah bash)                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Atur ke `false` untuk menonaktifkan [MCP servers claude.ai](/id/mcp#use-mcp-servers-from-claudeai) dalam Claude Code. Diaktifkan secara default untuk pengguna yang masuk                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ENABLE_TOOL_SEARCH`                           | Mengontrol [pencarian alat MCP](/id/mcp#scale-with-mcp-tool-search). Nilai: `auto` (default, mengaktifkan pada 10% konteks), `auto:N` (ambang batas khusus, misalnya `auto:5` untuk 5%), `true` (selalu aktif), `false` (dinonaktifkan)                                                                                                                                                                                                                                                                                                                     |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | Atur ke `true` untuk memaksa pembaruan otomatis plugin bahkan saat auto-updater utama dinonaktifkan melalui `DISABLE_AUTOUPDATER`                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `HTTP_PROXY`                                   | Tentukan server proxy HTTP untuk koneksi jaringan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `HTTPS_PROXY`                                  | Tentukan server proxy HTTPS untuk koneksi jaringan                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `IS_DEMO`                                      | Atur ke `true` untuk mengaktifkan mode demo: menyembunyikan email dan organisasi dari UI, melewati onboarding, dan menyembunyikan perintah internal. Berguna untuk streaming atau merekam sesi                                                                                                                                                                                                                                                                                                                                                              |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | Jumlah maksimum token yang diizinkan dalam respons alat MCP. Claude Code menampilkan peringatan saat output melebihi 10,000 token (default: 25000)                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `MAX_THINKING_TOKENS`                          | Timpa anggaran token [extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking). Pemikiran diaktifkan pada anggaran maksimum (31,999 token) secara default. Gunakan ini untuk membatasi anggaran (misalnya, `MAX_THINKING_TOKENS=10000`) atau menonaktifkan pemikiran sepenuhnya (`MAX_THINKING_TOKENS=0`). Untuk Opus 4.6, kedalaman pemikiran dikendalikan oleh [tingkat upaya](/id/model-config#adjust-effort-level) sebagai gantinya, dan variabel ini diabaikan kecuali diatur ke `0` untuk menonaktifkan pemikiran. |     |
| `MCP_CLIENT_SECRET`                            | Rahasia klien OAuth untuk MCP servers yang memerlukan [kredensial yang dikonfigurasi sebelumnya](/id/mcp#use-pre-configured-oauth-credentials). Menghindari prompt interaktif saat menambahkan server dengan `--client-secret`                                                                                                                                                                                                                                                                                                                              |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | Port tetap untuk callback pengalihan OAuth, sebagai alternatif untuk `--callback-port` saat menambahkan MCP server dengan [kredensial yang dikonfigurasi sebelumnya](/id/mcp#use-pre-configured-oauth-credentials)                                                                                                                                                                                                                                                                                                                                          |     |
| `MCP_TIMEOUT`                                  | Timeout dalam milidetik untuk startup server MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `MCP_TOOL_TIMEOUT`                             | Timeout dalam milidetik untuk eksekusi alat MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `NO_PROXY`                                     | Daftar domain dan IP ke mana permintaan akan dikeluarkan secara langsung, melewati proxy                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | Timpa anggaran karakter untuk metadata skill yang ditampilkan ke [alat Skill](/id/skills#control-who-invokes-a-skill). Anggaran diskalakan secara dinamis pada 2% dari jendela konteks, dengan fallback 16,000 karakter. Nama warisan disimpan untuk kompatibilitas mundur                                                                                                                                                                                                                                                                                  |     |
| `USE_BUILTIN_RIPGREP`                          | Atur ke `0` untuk menggunakan `rg` yang diinstal sistem daripada `rg` yang disertakan dengan Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Timpa wilayah untuk Claude 3.5 Haiku saat menggunakan Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Timpa wilayah untuk Claude 3.7 Sonnet saat menggunakan Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Timpa wilayah untuk Claude 4.0 Opus saat menggunakan Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Timpa wilayah untuk Claude 4.0 Sonnet saat menggunakan Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Timpa wilayah untuk Claude 4.1 Opus saat menggunakan Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |

## Alat yang tersedia untuk Claude

Claude Code memiliki akses ke serangkaian alat canggih yang membantu memahami dan memodifikasi basis kode Anda:

| Alat                     | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                | Izin Diperlukan |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| **Agent**                | Menghasilkan [subagent](/id/sub-agents) dengan jendela konteks sendiri untuk menangani tugas                                                                                                                                                                                                                                                                                             | Tidak           |
| **AskUserQuestion**      | Mengajukan pertanyaan pilihan ganda untuk mengumpulkan persyaratan atau mengklarifikasi ambiguitas                                                                                                                                                                                                                                                                                       | Tidak           |
| **Bash**                 | Mengeksekusi perintah shell di lingkungan Anda. Lihat [Perilaku alat Bash](#bash-tool-behavior)                                                                                                                                                                                                                                                                                          | Ya              |
| **CronCreate**           | Menjadwalkan prompt berulang atau satu kali dalam sesi saat ini (hilang saat Claude keluar). Lihat [tugas terjadwal](/id/scheduled-tasks)                                                                                                                                                                                                                                                | Tidak           |
| **CronDelete**           | Membatalkan tugas terjadwal berdasarkan ID                                                                                                                                                                                                                                                                                                                                               | Tidak           |
| **CronList**             | Mencantumkan semua tugas terjadwal dalam sesi                                                                                                                                                                                                                                                                                                                                            | Tidak           |
| **Edit**                 | Membuat pengeditan bertarget ke file tertentu                                                                                                                                                                                                                                                                                                                                            | Ya              |
| **EnterPlanMode**        | Beralih ke mode rencana untuk merancang pendekatan sebelum coding                                                                                                                                                                                                                                                                                                                        | Tidak           |
| **EnterWorktree**        | Membuat [git worktree](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) terisolasi dan beralih ke dalamnya                                                                                                                                                                                                                                                     | Tidak           |
| **ExitPlanMode**         | Menyajikan rencana untuk persetujuan dan keluar dari mode rencana                                                                                                                                                                                                                                                                                                                        | Ya              |
| **ExitWorktree**         | Keluar dari sesi worktree dan kembali ke direktori asli                                                                                                                                                                                                                                                                                                                                  | Tidak           |
| **Glob**                 | Menemukan file berdasarkan pencocokan pola                                                                                                                                                                                                                                                                                                                                               | Tidak           |
| **Grep**                 | Mencari pola dalam konten file                                                                                                                                                                                                                                                                                                                                                           | Tidak           |
| **ListMcpResourcesTool** | Mencantumkan sumber daya yang diekspos oleh [MCP servers](/id/mcp) yang terhubung                                                                                                                                                                                                                                                                                                        | Tidak           |
| **LSP**                  | Intelijen kode melalui server bahasa. Melaporkan kesalahan tipe dan peringatan secara otomatis setelah pengeditan file. Juga mendukung operasi navigasi: lompat ke definisi, temukan referensi, dapatkan info tipe, daftar simbol, temukan implementasi, lacak hierarki panggilan. Memerlukan [plugin intelijen kode](/id/discover-plugins#code-intelligence) dan biner server bahasanya | Tidak           |
| **NotebookEdit**         | Memodifikasi sel notebook Jupyter                                                                                                                                                                                                                                                                                                                                                        | Ya              |
| **Read**                 | Membaca konten file                                                                                                                                                                                                                                                                                                                                                                      | Tidak           |
| **ReadMcpResourceTool**  | Membaca sumber daya MCP tertentu berdasarkan URI                                                                                                                                                                                                                                                                                                                                         | Tidak           |
| **Skill**                | Mengeksekusi [skill](/id/skills#control-who-invokes-a-skill) dalam percakapan utama                                                                                                                                                                                                                                                                                                      | Ya              |
| **TaskCreate**           | Membuat tugas baru dalam daftar tugas                                                                                                                                                                                                                                                                                                                                                    | Tidak           |
| **TaskGet**              | Mengambil detail lengkap untuk tugas tertentu                                                                                                                                                                                                                                                                                                                                            | Tidak           |
| **TaskList**             | Mencantumkan semua tugas dengan status saat ini mereka                                                                                                                                                                                                                                                                                                                                   | Tidak           |
| **TaskOutput**           | Mengambil output dari tugas latar belakang                                                                                                                                                                                                                                                                                                                                               | Tidak           |
| **TaskStop**             | Membunuh tugas latar belakang yang sedang berjalan berdasarkan ID                                                                                                                                                                                                                                                                                                                        | Tidak           |
| **TaskUpdate**           | Memperbarui status tugas, dependensi, detail, atau menghapus tugas                                                                                                                                                                                                                                                                                                                       | Tidak           |
| **TodoWrite**            | Mengelola daftar tugas sesi. Tersedia dalam mode non-interaktif dan [Agent SDK](/id/headless); sesi interaktif menggunakan TaskCreate, TaskGet, TaskList, dan TaskUpdate sebagai gantinya                                                                                                                                                                                                | Tidak           |
| **ToolSearch**           | Mencari dan memuat alat yang ditangguhkan saat [pencarian alat](/id/mcp#scale-with-mcp-tool-search) diaktifkan                                                                                                                                                                                                                                                                           | Tidak           |
| **WebFetch**             | Mengambil konten dari URL yang ditentukan                                                                                                                                                                                                                                                                                                                                                | Ya              |
| **WebSearch**            | Melakukan pencarian web                                                                                                                                                                                                                                                                                                                                                                  | Ya              |
| **Write**                | Membuat atau menimpa file                                                                                                                                                                                                                                                                                                                                                                | Ya              |

Aturan izin dapat dikonfigurasi menggunakan `/allowed-tools` atau dalam [pengaturan izin](/id/settings#available-settings). Lihat juga [Aturan izin spesifik alat](/id/permissions#tool-specific-permission-rules).

### Perilaku alat Bash

Alat Bash mengeksekusi perintah shell dengan perilaku persistensi berikut:

* **Direktori kerja bertahan**: Ketika Claude mengubah direktori kerja (misalnya, `cd /path/to/dir`), perintah Bash berikutnya akan dieksekusi di direktori itu. Anda dapat menggunakan `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` untuk kembali ke direktori proyek setelah setiap perintah.
* **Variabel lingkungan TIDAK bertahan**: Variabel lingkungan yang ditetapkan dalam satu perintah Bash (misalnya, `export MY_VAR=value`) **tidak** tersedia dalam perintah Bash berikutnya. Setiap perintah Bash berjalan di lingkungan shell yang segar.

Untuk membuat variabel lingkungan tersedia dalam perintah Bash, Anda memiliki **tiga opsi**:

**Opsi 1: Aktifkan lingkungan sebelum memulai Claude Code** (pendekatan paling sederhana)

Aktifkan lingkungan virtual Anda di terminal sebelum meluncurkan Claude Code:

```bash  theme={null}
conda activate myenv
# atau: source /path/to/venv/bin/activate
claude
```

Ini berfungsi untuk lingkungan shell tetapi variabel lingkungan yang ditetapkan dalam perintah Bash Claude tidak akan bertahan di antara perintah.

**Opsi 2: Atur CLAUDE\_ENV\_FILE sebelum memulai Claude Code** (pengaturan lingkungan yang persisten)

Ekspor jalur ke skrip shell yang berisi pengaturan lingkungan Anda:

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Di mana `/path/to/env-setup.sh` berisi:

```bash  theme={null}
conda activate myenv
# atau: source /path/to/venv/bin/activate
# atau: export MY_VAR=value
```

Claude Code akan membuat sumber file ini sebelum setiap perintah Bash, membuat lingkungan persisten di semua perintah.

**Opsi 3: Gunakan hook SessionStart** (konfigurasi spesifik proyek)

Konfigurasikan dalam `.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

Hook menulis ke `$CLAUDE_ENV_FILE`, yang kemudian dibuat sumber sebelum setiap perintah Bash. Ini ideal untuk konfigurasi proyek bersama tim.

Lihat [hook SessionStart](/id/hooks#persist-environment-variables) untuk detail lebih lanjut tentang Opsi 3.

### Memperluas alat dengan hooks

Anda dapat menjalankan perintah khusus sebelum atau sesudah alat apa pun dieksekusi menggunakan [hook Claude Code](/id/hooks-guide).

Misalnya, Anda dapat secara otomatis menjalankan formatter Python setelah Claude memodifikasi file Python, atau mencegah modifikasi file konfigurasi produksi dengan memblokir operasi Write ke jalur tertentu.

## Lihat juga

* [Permissions](/id/permissions): sistem izin, sintaks aturan, pola spesifik alat, dan kebijakan yang dikelola
* [Authentication](/id/authentication): atur akses pengguna ke Claude Code
* [Troubleshooting](/id/troubleshooting): solusi untuk masalah konfigurasi umum
