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
* Tools dan plugins yang Anda gunakan di semua proyek
* Kunci API dan autentikasi (disimpan dengan aman)

**Cakupan Project** paling baik untuk:

* Pengaturan bersama tim (izin, hooks, MCP servers)
* Plugins yang harus dimiliki seluruh tim
* Standardisasi tooling di seluruh kolaborator

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
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                    | Tidak ada                     |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                          | `~/.claude.json` (per-proyek) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`              | `.claude/settings.local.json` |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` atau `.claude/CLAUDE.md` | Tidak ada                     |

***

## File pengaturan

File `settings.json` adalah mekanisme resmi untuk mengonfigurasi Claude Code melalui pengaturan hierarki:

* **Pengaturan pengguna** didefinisikan dalam `~/.claude/settings.json` dan berlaku untuk semua proyek.
* **Pengaturan proyek** disimpan di direktori proyek Anda:
  * `.claude/settings.json` untuk pengaturan yang diperiksa ke dalam kontrol sumber dan dibagikan dengan tim Anda
  * `.claude/settings.local.json` untuk pengaturan yang tidak diperiksa, berguna untuk preferensi pribadi dan eksperimen. Claude Code akan mengonfigurasi git untuk mengabaikan `.claude/settings.local.json` saat dibuat.
* **Pengaturan Managed**: Untuk organisasi yang memerlukan kontrol terpusat, Claude Code mendukung beberapa mekanisme pengiriman untuk pengaturan yang dikelola. Semua menggunakan format JSON yang sama dan tidak dapat ditimpa oleh pengaturan pengguna atau proyek:

  * **Pengaturan yang dikelola server**: dikirimkan dari server Anthropic melalui konsol admin Claude.ai. Lihat [pengaturan yang dikelola server](/id/server-managed-settings).
  * **Kebijakan tingkat MDM/OS**: dikirimkan melalui manajemen perangkat asli di macOS dan Windows:
    * macOS: domain preferensi terkelola `com.anthropic.claudecode` (digunakan melalui profil konfigurasi di Jamf, Kandji, atau alat MDM lainnya)
    * Windows: kunci registry `HKLM\SOFTWARE\Policies\ClaudeCode` dengan nilai `Settings` (REG\_SZ atau REG\_EXPAND\_SZ) berisi JSON (digunakan melalui Group Policy atau Intune)
    * Windows (tingkat pengguna): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioritas kebijakan terendah, hanya digunakan ketika tidak ada sumber tingkat admin)
  * **Berbasis file**: `managed-settings.json` dan `managed-mcp.json` digunakan ke direktori sistem:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux dan WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      Jalur Windows warisan `C:\ProgramData\ClaudeCode\managed-settings.json` tidak lagi didukung sejak v2.1.75. Administrator yang menggunakan pengaturan ke lokasi tersebut harus memigrasikan file ke `C:\Program Files\ClaudeCode\managed-settings.json`.
    </Warning>

    Pengaturan yang dikelola berbasis file juga mendukung direktori drop-in di `managed-settings.d/` dalam direktori sistem yang sama bersama `managed-settings.json`. Ini memungkinkan tim terpisah untuk menggunakan fragmen kebijakan independen tanpa mengoordinasikan pengeditan ke file tunggal.

    Mengikuti konvensi systemd, `managed-settings.json` digabungkan terlebih dahulu sebagai dasar, kemudian semua file `*.json` dalam direktori drop-in diurutkan secara alfabetis dan digabungkan di atas. File yang lebih baru menimpa yang lebih awal untuk nilai skalar; array digabungkan dan dihilangkan duplikatnya; objek digabungkan secara mendalam. File tersembunyi yang dimulai dengan `.` diabaikan.

    Gunakan prefiks numerik untuk mengontrol urutan penggabungan, misalnya `10-telemetry.json` dan `20-security.json`.

  Lihat [pengaturan yang dikelola](/id/permissions#managed-only-settings) dan [Konfigurasi MCP yang Dikelola](/id/mcp#managed-mcp-configuration) untuk detail.

  <Note>
    Penyebaran yang dikelola juga dapat membatasi **penambahan marketplace plugin** menggunakan `strictKnownMarketplaces`. Untuk informasi lebih lanjut, lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Konfigurasi lainnya** disimpan dalam `~/.claude.json`. File ini berisi preferensi Anda (tema, pengaturan notifikasi, mode editor), sesi OAuth, konfigurasi [MCP server](/id/mcp) untuk cakupan pengguna dan lokal, status per-proyek (tools yang diizinkan, pengaturan kepercayaan), dan berbagai cache. MCP servers dengan cakupan proyek disimpan secara terpisah dalam `.mcp.json`.

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

| Kunci                             | Deskripsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Contoh                                                                                                                           |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | Jalankan thread utama sebagai subagent bernama. Menerapkan prompt sistem subagent, pembatasan tool, dan model. Lihat [Panggil subagents secara eksplisit](/id/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                                                                                                                                                                                                                                                           | `"code-reviewer"`                                                                                                                |
| `allowedChannelPlugins`           | (Pengaturan yang dikelola saja) Daftar putih plugin channel yang dapat mendorong pesan. Menggantikan daftar putih Anthropic default saat diatur. Tidak terdefinisi = kembali ke default, array kosong = blokir semua plugin channel. Memerlukan `channelsEnabled: true`. Lihat [Batasi plugin channel mana yang dapat dijalankan](/id/channels#restrict-which-channel-plugins-can-run)                                                                                                                                                                                                                                          | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                           |
| `allowedHttpHookUrls`             | Daftar putih pola URL yang dapat ditargetkan oleh HTTP hooks. Mendukung `*` sebagai wildcard. Saat diatur, hooks dengan URL yang tidak cocok diblokir. Tidak terdefinisi = tidak ada pembatasan, array kosong = blokir semua HTTP hooks. Array digabungkan di seluruh sumber pengaturan. Lihat [Konfigurasi Hook](#hook-configuration)                                                                                                                                                                                                                                                                                          | `["https://hooks.example.com/*"]`                                                                                                |
| `allowedMcpServers`               | Saat diatur dalam managed-settings.json, daftar putih MCP servers yang dapat dikonfigurasi pengguna. Tidak terdefinisi = tidak ada pembatasan, array kosong = lockdown. Berlaku untuk semua cakupan. Daftar hitam memiliki prioritas. Lihat [Konfigurasi MCP yang Dikelola](/id/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                  | `[{ "serverName": "github" }]`                                                                                                   |
| `allowManagedHooksOnly`           | (Pengaturan yang dikelola saja) Cegah pemuatan hooks pengguna, proyek, dan plugin. Hanya memungkinkan hooks yang dikelola dan hooks SDK. Lihat [Konfigurasi Hook](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                           |
| `allowManagedMcpServersOnly`      | (Pengaturan yang dikelola saja) Hanya `allowedMcpServers` dari pengaturan yang dikelola yang dihormati. `deniedMcpServers` masih digabungkan dari semua sumber. Pengguna masih dapat menambahkan MCP servers, tetapi hanya daftar putih yang ditentukan admin yang berlaku. Lihat [Konfigurasi MCP yang Dikelola](/id/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                            | `true`                                                                                                                           |
| `allowManagedPermissionRulesOnly` | (Pengaturan yang dikelola saja) Cegah pengaturan pengguna dan proyek dari mendefinisikan aturan izin `allow`, `ask`, atau `deny`. Hanya aturan dalam pengaturan yang dikelola yang berlaku. Lihat [Pengaturan khusus yang dikelola](/id/permissions#managed-only-settings)                                                                                                                                                                                                                                                                                                                                                      | `true`                                                                                                                           |
| `alwaysThinkingEnabled`           | Aktifkan [pemikiran yang diperluas](/id/common-workflows#use-extended-thinking-thinking-mode) secara default untuk semua sesi. Biasanya dikonfigurasi melalui perintah `/config` daripada mengedit langsung                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                           |
| `apiKeyHelper`                    | Skrip khusus, yang akan dieksekusi dalam `/bin/sh`, untuk menghasilkan nilai auth. Nilai ini akan dikirim sebagai header `X-Api-Key` dan `Authorization: Bearer` untuk permintaan model                                                                                                                                                                                                                                                                                                                                                                                                                                         | `/bin/generate_temp_api_key.sh`                                                                                                  |
| `attribution`                     | Sesuaikan atribusi untuk komit git dan pull request. Lihat [Pengaturan atribusi](#attribution-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                          |
| `autoMemoryDirectory`             | Direktori khusus untuk penyimpanan [memori otomatis](/id/memory#storage-location). Menerima jalur yang diperluas `~/`. Tidak diterima dalam pengaturan proyek (`.claude/settings.json`) untuk mencegah repo bersama dari pengalihan penulisan memori ke lokasi sensitif. Diterima dari pengaturan kebijakan, lokal, dan pengguna                                                                                                                                                                                                                                                                                                | `"~/my-memory-dir"`                                                                                                              |
| `autoMode`                        | Sesuaikan apa yang diblokir dan diizinkan oleh pengklasifikasi [mode otomatis](/id/permission-modes#eliminate-prompts-with-auto-mode). Berisi array aturan prosa `environment`, `allow`, dan `soft_deny`. Lihat [Konfigurasikan pengklasifikasi mode otomatis](/id/permissions#configure-the-auto-mode-classifier). Tidak dibaca dari pengaturan proyek bersama                                                                                                                                                                                                                                                                 | `{"environment": ["Trusted repo: github.example.com/acme"]}`                                                                     |
| `autoUpdatesChannel`              | Saluran rilis untuk diikuti untuk pembaruan. Gunakan `"stable"` untuk versi yang biasanya sekitar satu minggu lama dan melewati versi dengan regresi besar, atau `"latest"` (default) untuk rilis terbaru                                                                                                                                                                                                                                                                                                                                                                                                                       | `"stable"`                                                                                                                       |
| `availableModels`                 | Batasi model mana yang dapat dipilih pengguna melalui `/model`, `--model`, alat Config, atau `ANTHROPIC_MODEL`. Tidak mempengaruhi opsi Default. Lihat [Batasi pemilihan model](/id/model-config#restrict-model-selection)                                                                                                                                                                                                                                                                                                                                                                                                      | `["sonnet", "haiku"]`                                                                                                            |
| `awsAuthRefresh`                  | Skrip khusus yang memodifikasi direktori `.aws` (lihat [konfigurasi kredensial lanjutan](/id/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `aws sso login --profile myprofile`                                                                                              |
| `awsCredentialExport`             | Skrip khusus yang menampilkan JSON dengan kredensial AWS (lihat [konfigurasi kredensial lanjutan](/id/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `/bin/generate_aws_grant.sh`                                                                                                     |
| `blockedMarketplaces`             | (Pengaturan yang dikelola saja) Daftar hitam sumber marketplace. Sumber yang diblokir diperiksa sebelum mengunduh, jadi mereka tidak pernah menyentuh sistem file. Lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                                                                       | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                          |
| `channelsEnabled`                 | (Pengaturan yang dikelola saja) Izinkan [channels](/id/channels) untuk pengguna Team dan Enterprise. Tidak diatur atau `false` memblokir pengiriman pesan channel terlepas dari apa yang dilewatkan pengguna ke `--channels`                                                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                           |
| `cleanupPeriodDays`               | Sesi yang tidak aktif lebih lama dari periode ini dihapus saat startup (default: 30 hari, minimum 1). Pengaturan ke `0` ditolak dengan kesalahan validasi. Untuk menonaktifkan penulisan transkrip sepenuhnya dalam mode non-interaktif (`-p`), gunakan flag `--no-session-persistence` atau opsi SDK `persistSession: false`; tidak ada yang setara dalam mode interaktif.                                                                                                                                                                                                                                                     | `20`                                                                                                                             |
| `companyAnnouncements`            | Pengumuman untuk ditampilkan kepada pengguna saat startup. Jika beberapa pengumuman disediakan, mereka akan diputar secara acak.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                          |
| `defaultShell`                    | Shell default untuk perintah `!` input-box. Menerima `"bash"` (default) atau `"powershell"`. Pengaturan `"powershell"` merutekan perintah `!` interaktif melalui PowerShell di Windows. Memerlukan `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Lihat [PowerShell tool](/id/tools-reference#powershell-tool)                                                                                                                                                                                                                                                                                                                            | `"powershell"`                                                                                                                   |
| `deniedMcpServers`                | Saat diatur dalam managed-settings.json, daftar hitam MCP servers yang secara eksplisit diblokir. Berlaku untuk semua cakupan termasuk servers yang dikelola. Daftar hitam memiliki prioritas atas daftar putih. Lihat [Konfigurasi MCP yang Dikelola](/id/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                       | `[{ "serverName": "filesystem" }]`                                                                                               |
| `disableAllHooks`                 | Nonaktifkan semua [hooks](/id/hooks) dan [status line](/id/statusline) khusus apa pun                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `true`                                                                                                                           |
| `disableAutoMode`                 | Atur ke `"disable"` untuk mencegah [mode otomatis](/id/permission-modes#eliminate-prompts-with-auto-mode) diaktifkan. Menghapus `auto` dari siklus `Shift+Tab` dan menolak `--permission-mode auto` saat startup. Paling berguna dalam [pengaturan yang dikelola](/id/permissions#managed-settings) di mana pengguna tidak dapat menimpanya                                                                                                                                                                                                                                                                                     | `"disable"`                                                                                                                      |
| `disableDeepLinkRegistration`     | Atur ke `"disable"` untuk mencegah Claude Code mendaftarkan penanganan protokol `claude-cli://` dengan sistem operasi saat startup. Deep links memungkinkan tools eksternal membuka sesi Claude Code dengan prompt yang sudah diisi sebelumnya melalui `claude-cli://open?q=...`. Berguna di lingkungan di mana pendaftaran penanganan protokol dibatasi atau dikelola secara terpisah                                                                                                                                                                                                                                          | `"disable"`                                                                                                                      |
| `disabledMcpjsonServers`          | Daftar MCP servers spesifik dari file `.mcp.json` untuk menolak                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `["filesystem"]`                                                                                                                 |
| `effortLevel`                     | Pertahankan [tingkat usaha](/id/model-config#adjust-effort-level) di seluruh sesi. Menerima `"low"`, `"medium"`, atau `"high"`. Ditulis secara otomatis saat Anda menjalankan `/effort low`, `/effort medium`, atau `/effort high`. Didukung di Opus 4.6 dan Sonnet 4.6                                                                                                                                                                                                                                                                                                                                                         | `"medium"`                                                                                                                       |
| `enableAllProjectMcpServers`      | Secara otomatis menyetujui semua MCP servers yang ditentukan dalam file `.mcp.json` proyek                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `true`                                                                                                                           |
| `enabledMcpjsonServers`           | Daftar MCP servers spesifik dari file `.mcp.json` untuk menyetujui                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `["memory", "github"]`                                                                                                           |
| `env`                             | Variabel lingkungan yang akan diterapkan ke setiap sesi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `{"FOO": "bar"}`                                                                                                                 |
| `fastModePerSessionOptIn`         | Saat `true`, mode cepat tidak bertahan di seluruh sesi. Setiap sesi dimulai dengan mode cepat mati, memerlukan pengguna untuk mengaktifkannya dengan `/fast`. Preferensi mode cepat pengguna masih disimpan. Lihat [Memerlukan opt-in per sesi](/id/fast-mode#require-per-session-opt-in)                                                                                                                                                                                                                                                                                                                                       | `true`                                                                                                                           |
| `feedbackSurveyRate`              | Probabilitas (0–1) bahwa [survei kualitas sesi](/id/data-usage#session-quality-surveys) muncul saat memenuhi syarat. Atur ke `0` untuk menekan sepenuhnya. Berguna saat menggunakan Bedrock, Vertex, atau Foundry di mana tingkat sampel default tidak berlaku                                                                                                                                                                                                                                                                                                                                                                  | `0.05`                                                                                                                           |
| `fileSuggestion`                  | Konfigurasikan skrip khusus untuk pelengkapan otomatis file `@`. Lihat [Pengaturan saran file](#file-suggestion-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                                 |
| `forceLoginMethod`                | Gunakan `claudeai` untuk membatasi login ke akun Claude.ai, `console` untuk membatasi login ke akun Claude Console (penagihan penggunaan API)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `claudeai`                                                                                                                       |
| `forceLoginOrgUUID`               | Tentukan UUID organisasi untuk memilihnya secara otomatis selama login, melewati langkah pemilihan organisasi. Memerlukan `forceLoginMethod` untuk diatur                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` atau `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `hooks`                           | Konfigurasikan perintah khusus untuk dijalankan pada acara siklus hidup. Lihat [dokumentasi hooks](/id/hooks) untuk format                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Lihat [hooks](/id/hooks)                                                                                                         |
| `httpHookAllowedEnvVars`          | Daftar putih nama variabel lingkungan yang dapat diinterpolasi oleh HTTP hooks ke dalam header. Saat diatur, `allowedEnvVars` efektif setiap hook adalah persimpangan dengan daftar ini. Tidak terdefinisi = tidak ada pembatasan. Array digabungkan di seluruh sumber pengaturan. Lihat [Konfigurasi Hook](#hook-configuration)                                                                                                                                                                                                                                                                                                | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                    |
| `includeCoAuthoredBy`             | **Usang**: Gunakan `attribution` sebagai gantinya. Apakah akan menyertakan baris `co-authored-by Claude` dalam komit git dan pull request (default: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `false`                                                                                                                          |
| `includeGitInstructions`          | Sertakan instruksi alur kerja komit dan PR bawaan dan snapshot status git dalam prompt sistem Claude (default: `true`). Atur ke `false` untuk menghapus keduanya, misalnya saat menggunakan skills alur kerja git Anda sendiri. Variabel lingkungan `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` memiliki prioritas atas pengaturan ini saat diatur                                                                                                                                                                                                                                                                                   | `false`                                                                                                                          |
| `language`                        | Konfigurasikan bahasa respons pilihan Claude (misalnya, `"japanese"`, `"spanish"`, `"french"`). Claude akan merespons dalam bahasa ini secara default. Juga menetapkan bahasa [voice dictation](/id/voice-dictation#change-the-dictation-language)                                                                                                                                                                                                                                                                                                                                                                              | `"japanese"`                                                                                                                     |
| `model`                           | Timpa model default untuk digunakan untuk Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `"claude-sonnet-4-6"`                                                                                                            |
| `modelOverrides`                  | Peta ID model Anthropic ke ID model spesifik penyedia seperti ARN profil inferensi Bedrock. Setiap entri pemilih model menggunakan nilai yang dipetakan saat memanggil API penyedia. Lihat [Timpa ID model per versi](/id/model-config#override-model-ids-per-version)                                                                                                                                                                                                                                                                                                                                                          | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                     |
| `otelHeadersHelper`               | Skrip untuk menghasilkan header OpenTelemetry dinamis. Berjalan saat startup dan secara berkala (lihat [Header dinamis](/id/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `/bin/generate_otel_headers.sh`                                                                                                  |
| `outputStyle`                     | Konfigurasikan gaya output untuk menyesuaikan prompt sistem. Lihat [dokumentasi gaya output](/id/output-styles)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `"Explanatory"`                                                                                                                  |
| `permissions`                     | Lihat tabel di bawah untuk struktur izin.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                  |
| `plansDirectory`                  | Sesuaikan di mana file rencana disimpan. Jalur relatif terhadap akar proyek. Default: `~/.claude/plans`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `"./plans"`                                                                                                                      |
| `pluginTrustMessage`              | (Pengaturan yang dikelola saja) Pesan khusus ditambahkan ke peringatan kepercayaan plugin yang ditampilkan sebelum instalasi. Gunakan ini untuk menambahkan konteks spesifik organisasi, misalnya untuk mengonfirmasi bahwa plugin dari marketplace internal Anda telah disaring.                                                                                                                                                                                                                                                                                                                                               | `"All plugins from our marketplace are approved by IT"`                                                                          |
| `prefersReducedMotion`            | Kurangi atau nonaktifkan animasi UI (spinners, shimmer, efek flash) untuk aksesibilitas                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `true`                                                                                                                           |
| `respectGitignore`                | Kontrol apakah pemilih file `@` menghormati pola `.gitignore`. Saat `true` (default), file yang cocok dengan pola `.gitignore` dikecualikan dari saran                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `false`                                                                                                                          |
| `showClearContextOnPlanAccept`    | Tampilkan opsi "clear context" pada layar penerimaan rencana. Default ke `false`. Atur ke `true` untuk mengembalikan opsi                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `true`                                                                                                                           |
| `showThinkingSummaries`           | Tampilkan ringkasan [pemikiran yang diperluas](/id/common-workflows#use-extended-thinking-thinking-mode) dalam sesi interaktif. Saat tidak diatur atau `false` (default dalam mode interaktif), blok pemikiran diredaksi oleh API dan ditampilkan sebagai stub yang runtuh. Redaksi hanya mengubah apa yang Anda lihat, bukan apa yang dihasilkan model: untuk mengurangi pengeluaran pemikiran, [turunkan anggaran atau nonaktifkan pemikiran](/id/common-workflows#use-extended-thinking-thinking-mode) sebagai gantinya. Mode non-interaktif (`-p`) dan pemanggil SDK selalu menerima ringkasan terlepas dari pengaturan ini | `true`                                                                                                                           |
| `spinnerTipsEnabled`              | Tampilkan tips dalam spinner saat Claude bekerja. Atur ke `false` untuk menonaktifkan tips (default: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `false`                                                                                                                          |
| `spinnerTipsOverride`             | Timpa tips spinner dengan string khusus. `tips`: array string tip. `excludeDefault`: jika `true`, hanya tampilkan tips khusus; jika `false` atau tidak ada, tips khusus digabungkan dengan tips bawaan                                                                                                                                                                                                                                                                                                                                                                                                                          | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                                |
| `spinnerVerbs`                    | Sesuaikan kata kerja aksi yang ditampilkan dalam spinner dan pesan durasi giliran. Atur `mode` ke `"replace"` untuk menggunakan hanya kata kerja Anda, atau `"append"` untuk menambahkannya ke default                                                                                                                                                                                                                                                                                                                                                                                                                          | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                         |
| `statusLine`                      | Konfigurasikan status line khusus untuk menampilkan konteks. Lihat [dokumentasi `statusLine`](/id/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                      |
| `strictKnownMarketplaces`         | (Pengaturan yang dikelola saja) Daftar putih marketplace plugin yang dapat ditambahkan pengguna. Tidak terdefinisi = tidak ada pembatasan, array kosong = lockdown. Berlaku untuk penambahan marketplace saja. Lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                           | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                          |
| `useAutoModeDuringPlan`           | Apakah plan mode menggunakan semantik mode otomatis saat mode otomatis tersedia. Default: `true`. Tidak dibaca dari pengaturan proyek bersama. Muncul di `/config` sebagai "Use auto mode during plan"                                                                                                                                                                                                                                                                                                                                                                                                                          | `false`                                                                                                                          |
| `voiceEnabled`                    | Aktifkan push-to-talk [voice dictation](/id/voice-dictation). Ditulis secara otomatis saat Anda menjalankan `/voice`. Memerlukan akun Claude.ai                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `true`                                                                                                                           |

### Pengaturan konfigurasi global

Pengaturan ini disimpan dalam `~/.claude.json` daripada `settings.json`. Menambahkannya ke `settings.json` akan memicu kesalahan validasi skema.

| Kunci                        | Deskripsi                                                                                                                                                                                                                                                                                                                   | Contoh         |
| :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| `autoConnectIde`             | Secara otomatis terhubung ke IDE yang sedang berjalan saat Claude Code dimulai dari terminal eksternal. Default: `false`. Muncul di `/config` sebagai **Auto-connect to IDE (external terminal)** saat berjalan di luar terminal VS Code atau JetBrains                                                                     | `true`         |
| `autoInstallIdeExtension`    | Secara otomatis instal ekstensi IDE Claude Code saat berjalan dari terminal VS Code. Default: `true`. Muncul di `/config` sebagai **Auto-install IDE extension** saat berjalan di dalam terminal VS Code atau JetBrains. Anda juga dapat menetapkan variabel lingkungan [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/id/env-vars) | `false`        |
| `editorMode`                 | Mode binding kunci untuk prompt input: `"normal"` atau `"vim"`. Default: `"normal"`. Ditulis secara otomatis saat Anda menjalankan `/vim`. Muncul di `/config` sebagai **Key binding mode**                                                                                                                                 | `"vim"`        |
| `showTurnDuration`           | Tampilkan pesan durasi giliran setelah respons, misalnya "Cooked for 1m 6s". Default: `true`. Muncul di `/config` sebagai **Show turn duration**                                                                                                                                                                            | `false`        |
| `terminalProgressBarEnabled` | Tampilkan bilah kemajuan terminal di terminal yang didukung: ConEmu, Ghostty 1.2.0+, dan iTerm2 3.6.6+. Default: `true`. Muncul di `/config` sebagai **Terminal progress bar**                                                                                                                                              | `false`        |
| `teammateMode`               | Bagaimana [rekan tim agent](/id/agent-teams) ditampilkan: `auto` (memilih panel terpisah di tmux atau iTerm2, dalam proses sebaliknya), `in-process`, atau `tmux`. Lihat [pilih mode tampilan](/id/agent-teams#choose-a-display-mode)                                                                                       | `"in-process"` |

### Pengaturan worktree

Konfigurasikan bagaimana `--worktree` membuat dan mengelola git worktrees. Gunakan pengaturan ini untuk mengurangi penggunaan disk dan waktu startup di monorepo besar.

| Kunci                         | Deskripsi                                                                                                                                                                 | Contoh                                |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------ |
| `worktree.symlinkDirectories` | Direktori untuk symlink dari repositori utama ke setiap worktree untuk menghindari duplikasi direktori besar di disk. Tidak ada direktori yang disymlink secara default   | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Direktori untuk diperiksa di setiap worktree melalui git sparse-checkout (mode cone). Hanya jalur yang terdaftar yang ditulis ke disk, yang lebih cepat di monorepo besar | `["packages/my-app", "shared/utils"]` |

Untuk menyalin file yang diabaikan git seperti `.env` ke worktrees baru, gunakan file [`.worktreeinclude`](/id/common-workflows#copy-gitignored-files-to-worktrees) di akar proyek Anda daripada pengaturan.

### Pengaturan izin

| Kunci                               | Deskripsi                                                                                                                                                                                                                                                                                                            | Contoh                                                                 |
| :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                             | Array aturan izin untuk memungkinkan penggunaan tool. Lihat [Sintaks aturan izin](#permission-rule-syntax) di bawah untuk detail pencocokan pola                                                                                                                                                                     | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | Array aturan izin untuk meminta konfirmasi saat penggunaan tool. Lihat [Sintaks aturan izin](#permission-rule-syntax) di bawah                                                                                                                                                                                       | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | Array aturan izin untuk menolak penggunaan tool. Gunakan ini untuk mengecualikan file sensitif dari akses Claude Code. Lihat [Sintaks aturan izin](#permission-rule-syntax) dan [Batasan izin Bash](/id/permissions#tool-specific-permission-rules)                                                                  | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | [Direktori kerja](/id/permissions#working-directories) tambahan untuk akses file. Sebagian besar konfigurasi `.claude/` [tidak ditemukan](/id/permissions#additional-directories-grant-file-access-not-configuration) dari direktori ini                                                                             | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | Mode [izin](/id/permission-modes) default saat membuka Claude Code. Nilai yang valid: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. Flag CLI `--permission-mode` menimpa pengaturan ini untuk sesi tunggal                                                                               | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | Atur ke `"disable"` untuk mencegah mode `bypassPermissions` diaktifkan. Ini menonaktifkan flag baris perintah `--dangerously-skip-permissions`. Paling berguna dalam [pengaturan yang dikelola](/id/permissions#managed-settings) di mana pengguna tidak dapat menimpanya                                            | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | Lewati prompt konfirmasi yang ditampilkan sebelum memasuki mode bypass permissions melalui `--dangerously-skip-permissions` atau `defaultMode: "bypassPermissions"`. Diabaikan saat diatur dalam pengaturan proyek (`.claude/settings.json`) untuk mencegah repositori yang tidak terpercaya dari auto-bypass prompt | `true`                                                                 |

### Sintaks aturan izin

Aturan izin mengikuti format `Tool` atau `Tool(specifier)`. Aturan dievaluasi secara berurutan: aturan deny terlebih dahulu, kemudian ask, kemudian allow. Aturan pertama yang cocok menang.

Contoh cepat:

| Aturan                         | Efek                                                |
| :----------------------------- | :-------------------------------------------------- |
| `Bash`                         | Cocok dengan semua perintah Bash                    |
| `Bash(npm run *)`              | Cocok dengan perintah yang dimulai dengan `npm run` |
| `Read(./.env)`                 | Cocok dengan membaca file `.env`                    |
| `WebFetch(domain:example.com)` | Cocok dengan permintaan fetch ke example.com        |

Untuk referensi sintaks aturan lengkap, termasuk perilaku wildcard, pola spesifik tool untuk Read, Edit, WebFetch, MCP, dan aturan Agent, dan batasan keamanan pola Bash, lihat [Sintaks aturan izin](/id/permissions#permission-rule-syntax).

### Pengaturan sandbox

Konfigurasikan perilaku sandboxing lanjutan. Sandboxing mengisolasi perintah bash dari sistem file dan jaringan Anda. Lihat [Sandboxing](/id/sandboxing) untuk detail.

| Kunci                                  | Deskripsi                                                                                                                                                                                                                                                                                                                                                                             | Contoh                          |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------ |
| `enabled`                              | Aktifkan bash sandboxing (macOS, Linux, dan WSL2). Default: false                                                                                                                                                                                                                                                                                                                     | `true`                          |
| `failIfUnavailable`                    | Keluar dengan kesalahan saat startup jika `sandbox.enabled` adalah true tetapi sandbox tidak dapat dimulai (dependensi yang hilang, platform yang tidak didukung, atau pembatasan platform). Saat false (default), peringatan ditampilkan dan perintah berjalan tanpa sandbox. Dimaksudkan untuk penyebaran pengaturan yang dikelola yang memerlukan sandboxing sebagai gerbang keras | `true`                          |
| `autoAllowBashIfSandboxed`             | Secara otomatis menyetujui perintah bash saat sandboxed. Default: true                                                                                                                                                                                                                                                                                                                | `true`                          |
| `excludedCommands`                     | Perintah yang harus dijalankan di luar sandbox                                                                                                                                                                                                                                                                                                                                        | `["git", "docker"]`             |
| `allowUnsandboxedCommands`             | Izinkan perintah dijalankan di luar sandbox melalui parameter `dangerouslyDisableSandbox`. Saat diatur ke `false`, pintu keluar `dangerouslyDisableSandbox` sepenuhnya dinonaktifkan dan semua perintah harus dijalankan sandboxed (atau berada dalam `excludedCommands`). Berguna untuk kebijakan perusahaan yang memerlukan sandboxing ketat. Default: true                         | `false`                         |
| `filesystem.allowWrite`                | Jalur tambahan di mana perintah sandboxed dapat menulis. Array digabungkan di seluruh semua cakupan pengaturan: jalur pengguna, proyek, dan yang dikelola digabungkan, bukan diganti. Juga digabungkan dengan jalur dari aturan izin `Edit(...)` allow. Lihat [prefiks jalur sandbox](#sandbox-path-prefixes) di bawah.                                                               | `["/tmp/build", "~/.kube"]`     |
| `filesystem.denyWrite`                 | Jalur di mana perintah sandboxed tidak dapat menulis. Array digabungkan di seluruh semua cakupan pengaturan. Juga digabungkan dengan jalur dari aturan izin `Edit(...)` deny.                                                                                                                                                                                                         | `["/etc", "/usr/local/bin"]`    |
| `filesystem.denyRead`                  | Jalur di mana perintah sandboxed tidak dapat membaca. Array digabungkan di seluruh semua cakupan pengaturan. Juga digabungkan dengan jalur dari aturan izin `Read(...)` deny.                                                                                                                                                                                                         | `["~/.aws/credentials"]`        |
| `filesystem.allowRead`                 | Jalur untuk mengizinkan kembali pembacaan dalam region `denyRead`. Memiliki prioritas atas `denyRead`. Array digabungkan di seluruh semua cakupan pengaturan. Gunakan ini untuk membuat pola akses baca khusus workspace.                                                                                                                                                             | `["."]`                         |
| `filesystem.allowManagedReadPathsOnly` | (Pengaturan yang dikelola saja) Hanya jalur `filesystem.allowRead` dari pengaturan yang dikelola yang dihormati. `denyRead` masih digabungkan dari semua sumber. Default: false                                                                                                                                                                                                       | `true`                          |
| `network.allowUnixSockets`             | Jalur soket Unix yang dapat diakses dalam sandbox (untuk agen SSH, dll.)                                                                                                                                                                                                                                                                                                              | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`          | Izinkan semua koneksi soket Unix dalam sandbox. Default: false                                                                                                                                                                                                                                                                                                                        | `true`                          |
| `network.allowLocalBinding`            | Izinkan pengikatan ke port localhost (macOS saja). Default: false                                                                                                                                                                                                                                                                                                                     | `true`                          |
| `network.allowedDomains`               | Array domain untuk memungkinkan lalu lintas jaringan keluar. Mendukung wildcard (misalnya, `*.example.com`).                                                                                                                                                                                                                                                                          | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly`      | (Pengaturan yang dikelola saja) Hanya `allowedDomains` dan aturan allow `WebFetch(domain:...)` dari pengaturan yang dikelola yang dihormati. Domain dari pengaturan pengguna, proyek, dan lokal diabaikan. Domain yang tidak diizinkan diblokir secara otomatis tanpa meminta pengguna. Domain yang ditolak masih dihormati dari semua sumber. Default: false                         | `true`                          |
| `network.httpProxyPort`                | Port proxy HTTP yang digunakan jika Anda ingin membawa proxy Anda sendiri. Jika tidak ditentukan, Claude akan menjalankan proxy-nya sendiri.                                                                                                                                                                                                                                          | `8080`                          |
| `network.socksProxyPort`               | Port proxy SOCKS5 yang digunakan jika Anda ingin membawa proxy Anda sendiri. Jika tidak ditentukan, Claude akan menjalankan proxy-nya sendiri.                                                                                                                                                                                                                                        | `8081`                          |
| `enableWeakerNestedSandbox`            | Aktifkan sandbox yang lebih lemah untuk lingkungan Docker tanpa hak istimewa (Linux dan WSL2 saja). **Mengurangi keamanan.** Default: false                                                                                                                                                                                                                                           | `true`                          |
| `enableWeakerNetworkIsolation`         | (macOS saja) Izinkan akses ke layanan kepercayaan TLS sistem (`com.apple.trustd.agent`) dalam sandbox. Diperlukan untuk tools berbasis Go seperti `gh`, `gcloud`, dan `terraform` untuk memverifikasi sertifikat TLS saat menggunakan `httpProxyPort` dengan proxy MITM dan CA khusus. **Mengurangi keamanan** dengan membuka jalur eksfiltrasi data potensial. Default: false        | `true`                          |

#### Prefiks jalur sandbox

Jalur dalam `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead`, dan `filesystem.allowRead` mendukung prefiks ini:

| Prefiks                     | Arti                                                                                                | Contoh                                                                           |
| :-------------------------- | :-------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `/`                         | Jalur absolut dari akar sistem file                                                                 | `/tmp/build` tetap `/tmp/build`                                                  |
| `~/`                        | Relatif terhadap direktori home                                                                     | `~/.kube` menjadi `$HOME/.kube`                                                  |
| `./` atau tidak ada prefiks | Relatif terhadap akar proyek untuk pengaturan proyek, atau ke `~/.claude` untuk pengaturan pengguna | `./output` dalam `.claude/settings.json` diselesaikan ke `<project-root>/output` |

Prefiks `//path` yang lebih lama untuk jalur absolut masih berfungsi. Jika Anda sebelumnya menggunakan `/path` tunggal mengharapkan resolusi relatif proyek, beralih ke `./path`. Sintaks ini berbeda dari [aturan izin Read dan Edit](/id/permissions#read-and-edit), yang menggunakan `//path` untuk absolut dan `/path` untuk relatif proyek. Jalur sistem file sandbox menggunakan konvensi standar: `/tmp/build` adalah jalur absolut.

**Contoh konfigurasi:**

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
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

* **Pengaturan `sandbox.filesystem`** (ditampilkan di atas): Kontrol jalur pada batas sandbox tingkat OS. Pembatasan ini berlaku untuk semua perintah subprocess (misalnya, `kubectl`, `terraform`, `npm`), bukan hanya tools file Claude.
* **Aturan izin**: Gunakan aturan allow/deny `Edit` untuk mengontrol akses tools file Claude, aturan deny `Read` untuk memblokir pembacaan, dan aturan allow/deny `WebFetch` untuk mengontrol domain jaringan. Jalur dari aturan ini juga digabungkan ke dalam konfigurasi sandbox.

### Pengaturan atribusi

Claude Code menambahkan atribusi ke komit git dan pull request. Ini dikonfigurasi secara terpisah:

* Komit menggunakan [git trailers](https://git-scm.com/docs/git-interpret-trailers) (seperti `Co-Authored-By`) secara default, yang dapat disesuaikan atau dinonaktifkan
* Deskripsi pull request adalah teks biasa

| Kunci    | Deskripsi                                                                                       |
| :------- | :---------------------------------------------------------------------------------------------- |
| `commit` | Atribusi untuk komit git, termasuk trailer apa pun. String kosong menyembunyikan atribusi komit |
| `pr`     | Atribusi untuk deskripsi pull request. String kosong menyembunyikan atribusi pull request       |

**Atribusi komit default:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Atribusi pull request default:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Contoh:**

```json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  Pengaturan `attribution` memiliki prioritas atas pengaturan `includeCoAuthoredBy` yang usang. Untuk menyembunyikan semua atribusi, atur `commit` dan `pr` ke string kosong.
</Note>

### Pengaturan saran file

Konfigurasikan perintah khusus untuk pelengkapan otomatis jalur file `@`. Saran file bawaan menggunakan traversal sistem file cepat, tetapi monorepo besar mungkin mendapat manfaat dari pengindeksan spesifik proyek seperti indeks file yang telah dibangun sebelumnya atau tooling khusus.

```json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

Perintah berjalan dengan variabel lingkungan yang sama seperti [hooks](/id/hooks), termasuk `CLAUDE_PROJECT_DIR`. Ini menerima JSON melalui stdin dengan bidang `query`:

```json theme={null}
{"query": "src/comp"}
```

Keluarkan jalur file yang dipisahkan baris baru ke stdout (saat ini dibatasi hingga 15):

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Contoh:**

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Konfigurasi hook

Pengaturan ini mengontrol hook mana yang diizinkan untuk dijalankan dan apa yang dapat diakses oleh HTTP hooks. Pengaturan `allowManagedHooksOnly` hanya dapat dikonfigurasi dalam [pengaturan yang dikelola](#settings-files). Daftar putih URL dan env var dapat diatur di tingkat pengaturan apa pun dan digabungkan di seluruh sumber.

**Perilaku saat `allowManagedHooksOnly` adalah `true`:**

* Hooks yang dikelola dan hooks SDK dimuat
* Hooks pengguna, hooks proyek, dan hooks plugin diblokir

**Batasi URL HTTP hook:**

Batasi URL mana yang dapat ditargetkan oleh HTTP hooks. Mendukung `*` sebagai wildcard untuk pencocokan. Saat array didefinisikan, HTTP hooks yang menargetkan URL yang tidak cocok diblokir secara diam-diam.

```json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Batasi variabel lingkungan HTTP hook:**

Batasi nama variabel lingkungan mana yang dapat diinterpolasi oleh HTTP hooks ke dalam nilai header. `allowedEnvVars` efektif setiap hook adalah persimpangan dari daftar sendiri dan pengaturan ini.

```json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Prioritas pengaturan

Pengaturan berlaku dalam urutan prioritas. Dari tertinggi ke terendah:

1. **Pengaturan yang dikelola** ([yang dikelola server](/id/server-managed-settings), [kebijakan tingkat MDM/OS](#configuration-scopes), atau [pengaturan yang dikelola](/id/settings#settings-files))
   * Kebijakan yang digunakan oleh IT melalui pengiriman server, profil konfigurasi MDM, kebijakan registry, atau file pengaturan yang dikelola
   * Tidak dapat ditimpa oleh tingkat apa pun, termasuk argumen baris perintah
   * Dalam tingkat yang dikelola, prioritas adalah: yang dikelola server > kebijakan tingkat MDM/OS > file-based (`managed-settings.d/*.json` + `managed-settings.json`) > registry HKCU (Windows saja). Hanya satu sumber yang dikelola yang digunakan; sumber tidak digabungkan di seluruh tingkat. Dalam tingkat berbasis file, file drop-in dan file dasar digabungkan bersama.

2. **Argumen baris perintah**
   * Penggantian sementara untuk sesi tertentu

3. **Pengaturan proyek lokal** (`.claude/settings.local.json`)
   * Pengaturan proyek pribadi

4. **Pengaturan proyek bersama** (`.claude/settings.json`)
   * Pengaturan proyek bersama tim dalam kontrol sumber

5. **Pengaturan pengguna** (`~/.claude/settings.json`)
   * Pengaturan global pribadi

Hierarki ini memastikan bahwa kebijakan organisasi selalu diterapkan sambil tetap memungkinkan tim dan individu untuk menyesuaikan pengalaman mereka. Prioritas yang sama berlaku apakah Anda menjalankan Claude Code dari CLI, [ekstensi VS Code](/id/vs-code), atau [IDE JetBrains](/id/jetbrains).

Misalnya, jika pengaturan pengguna Anda memungkinkan `Bash(npm run *)` tetapi pengaturan bersama proyek menolaknya, pengaturan proyek memiliki prioritas dan perintah diblokir.

<Note>
  **Pengaturan array digabungkan di seluruh cakupan.** Ketika pengaturan yang bernilai array yang sama (seperti `sandbox.filesystem.allowWrite` atau `permissions.allow`) muncul dalam beberapa cakupan, array **digabungkan dan dihilangkan duplikatnya**, bukan diganti. Ini berarti cakupan prioritas lebih rendah dapat menambahkan entri tanpa menimpa yang ditetapkan oleh cakupan prioritas lebih tinggi, dan sebaliknya. Misalnya, jika pengaturan yang dikelola menetapkan `allowWrite` ke `["/opt/company-tools"]` dan pengguna menambahkan `["~/.kube"]`, kedua jalur disertakan dalam konfigurasi akhir.
</Note>

### Verifikasi pengaturan aktif

Jalankan `/status` di dalam Claude Code untuk melihat sumber pengaturan mana yang aktif dan dari mana asalnya. Output menunjukkan setiap lapisan konfigurasi (yang dikelola, pengguna, proyek) bersama dengan asalnya, seperti `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, atau `Enterprise managed settings (file)`. Jika file pengaturan berisi kesalahan, `/status` melaporkan masalah sehingga Anda dapat memperbaikinya.

### Poin kunci tentang sistem konfigurasi

* **File memori (`CLAUDE.md`)**: Berisi instruksi dan konteks yang dimuat Claude saat startup
* **File pengaturan (JSON)**: Konfigurasikan izin, variabel lingkungan, dan perilaku tool
* **Skills**: Prompt khusus yang dapat dipanggil dengan `/skill-name` atau dimuat oleh Claude secara otomatis
* **MCP servers**: Perluas Claude Code dengan tools dan integrasi tambahan
* **Prioritas**: Konfigurasi tingkat lebih tinggi (Managed) menimpa yang tingkat lebih rendah (User/Project)
* **Warisan**: Pengaturan digabungkan, dengan pengaturan yang lebih spesifik menambah atau menimpa yang lebih luas

### Prompt sistem

Prompt sistem internal Claude Code tidak dipublikasikan. Untuk menambahkan instruksi khusus, gunakan file `CLAUDE.md` atau flag `--append-system-prompt`.

### Mengecualikan file sensitif

Untuk mencegah Claude Code mengakses file yang berisi informasi sensitif seperti kunci API, rahasia, dan file lingkungan, gunakan pengaturan `permissions.deny` dalam file `.claude/settings.json` Anda:

```json theme={null}
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

Ini menggantikan konfigurasi `ignorePatterns` yang usang. File yang cocok dengan pola ini dikecualikan dari penemuan file dan hasil pencarian, dan operasi baca pada file ini ditolak.

## Konfigurasi subagent

Claude Code mendukung subagents AI khusus yang dapat dikonfigurasi di tingkat pengguna dan proyek. Subagents ini disimpan sebagai file Markdown dengan frontmatter YAML:

* **Subagents pengguna**: `~/.claude/agents/` - Tersedia di semua proyek Anda
* **Subagents proyek**: `.claude/agents/` - Spesifik untuk proyek Anda dan dapat dibagikan dengan tim Anda

File subagent mendefinisikan asisten AI khusus dengan prompt khusus dan izin tool. Pelajari lebih lanjut tentang membuat dan menggunakan subagents dalam [dokumentasi subagents](/id/sub-agents).

## Konfigurasi plugin

Claude Code mendukung sistem plugin yang memungkinkan Anda memperluas fungsionalitas dengan skills, agents, hooks, dan MCP servers. Plugin didistribusikan melalui marketplace dan dapat dikonfigurasi di tingkat pengguna dan repositori.

### Pengaturan plugin

Pengaturan terkait plugin dalam `settings.json`:

```json theme={null}
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
* **Pengaturan yang dikelola** (`managed-settings.json`): Penggantian kebijakan organisasi yang memblokir instalasi di semua cakupan dan menyembunyikan plugin dari marketplace

**Contoh**:

```json theme={null}
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
2. Anggota tim kemudian diminta untuk menginstal plugin dari marketplace tersebut
3. Pengguna dapat melewati marketplace atau plugin yang tidak diinginkan (disimpan dalam pengaturan pengguna)
4. Instalasi menghormati batas kepercayaan dan memerlukan persetujuan eksplisit

**Contoh**:

```json theme={null}
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
* `settings`: marketplace inline yang dideklarasikan langsung dalam settings.json tanpa repositori yang dihosting terpisah (menggunakan `name` dan `plugins`)

Gunakan `source: 'settings'` untuk mendeklarasikan serangkaian plugin kecil inline tanpa menyiapkan repositori marketplace yang dihosting. Plugin yang terdaftar di sini harus mereferensikan sumber eksternal seperti GitHub atau npm. Anda masih perlu mengaktifkan setiap plugin secara terpisah dalam `enabledPlugins`.

```json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Pengaturan yang dikelola saja**: Mengontrol marketplace plugin mana yang diizinkan pengguna untuk ditambahkan. Pengaturan ini hanya dapat dikonfigurasi dalam [pengaturan yang dikelola](/id/settings#settings-files) dan memberikan administrator kontrol ketat atas sumber marketplace.

**Lokasi file pengaturan yang dikelola**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux dan WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Karakteristik kunci**:

* Hanya tersedia dalam pengaturan yang dikelola (`managed-settings.json`)
* Tidak dapat ditimpa oleh pengaturan pengguna atau proyek (prioritas tertinggi)
* Diterapkan SEBELUM operasi jaringan/sistem file (sumber yang diblokir tidak pernah dieksekusi)
* Menggunakan pencocokan tepat untuk spesifikasi sumber (termasuk `ref`, `path` untuk sumber git), kecuali `hostPattern`, yang menggunakan pencocokan regex

**Perilaku daftar putih**:

* `undefined` (default): Tidak ada pembatasan - pengguna dapat menambahkan marketplace apa pun
* Array kosong `[]`: Lockdown lengkap - pengguna tidak dapat menambahkan marketplace baru apa pun
* Daftar sumber: Pengguna hanya dapat menambahkan marketplace yang cocok dengan tepat

**Semua jenis sumber yang didukung**:

Daftar putih mendukung beberapa jenis sumber marketplace. Sebagian besar sumber menggunakan pencocokan tepat, sementara `hostPattern` menggunakan pencocokan regex terhadap host marketplace.

1. **Repositori GitHub**:

```json theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Bidang: `repo` (diperlukan), `ref` (opsional: cabang/tag/SHA), `path` (opsional: subdirektori)

2. **Repositori Git**:

```json theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Bidang: `url` (diperlukan), `ref` (opsional: cabang/tag/SHA), `path` (opsional: subdirektori)

3. **Marketplace berbasis URL**:

```json theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Bidang: `url` (diperlukan), `headers` (opsional: header HTTP untuk akses terautentikasi)

<Note>
  Marketplace berbasis URL hanya mengunduh file `marketplace.json`. Mereka tidak mengunduh file plugin dari server. Plugin dalam marketplace berbasis URL harus menggunakan sumber eksternal (GitHub, npm, atau URL git) daripada jalur relatif. Untuk plugin dengan jalur relatif, gunakan marketplace berbasis Git sebagai gantinya. Lihat [Troubleshooting](/id/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) untuk detail.
</Note>

4. **Paket NPM**:

```json theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Bidang: `package` (diperlukan, mendukung paket berscopus)

5. **Jalur file**:

```json theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Bidang: `path` (diperlukan: jalur absolut ke file marketplace.json)

6. **Jalur direktori**:

```json theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Bidang: `path` (diperlukan: jalur absolut ke direktori yang berisi `.claude-plugin/marketplace.json`)

7. **Pencocokan pola host**:

```json theme={null}
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

Contoh: izinkan marketplace spesifik saja:

```json theme={null}
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

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Contoh: izinkan semua marketplace dari server git internal:

```json theme={null}
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

```json theme={null}
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
| **File pengaturan**  | `managed-settings.json` saja                        | File pengaturan apa pun                     |
| **Perilaku**         | Blokir penambahan yang tidak ada dalam daftar putih | Instal otomatis marketplace yang hilang     |
| **Saat diterapkan**  | Sebelum operasi jaringan/sistem file                | Setelah prompt kepercayaan pengguna         |
| **Dapat ditimpa**    | Tidak (prioritas tertinggi)                         | Ya (oleh pengaturan prioritas lebih tinggi) |
| **Format sumber**    | Objek sumber langsung                               | Marketplace bernama dengan sumber bersarang |
| **Kasus penggunaan** | Pembatasan kepatuhan, keamanan                      | Onboarding, standardisasi                   |

**Perbedaan format**:

`strictKnownMarketplaces` menggunakan objek sumber langsung:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` memerlukan marketplace bernama:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Menggunakan keduanya bersama**:

`strictKnownMarketplaces` adalah gerbang kebijakan: mengontrol apa yang dapat ditambahkan pengguna tetapi tidak mendaftarkan marketplace apa pun. Untuk membatasi dan pra-mendaftarkan marketplace untuk semua pengguna, atur keduanya dalam `managed-settings.json`:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Dengan hanya `strictKnownMarketplaces` yang diatur, pengguna masih dapat menambahkan marketplace yang diizinkan secara manual melalui `/plugin marketplace add`, tetapi tidak tersedia secara otomatis.

**Catatan penting**:

* Pembatasan diperiksa SEBELUM permintaan jaringan atau operasi sistem file apa pun
* Saat diblokir, pengguna melihat pesan kesalahan yang jelas menunjukkan sumber diblokir oleh kebijakan yang dikelola
* Pembatasan hanya berlaku untuk menambahkan marketplace BARU; marketplace yang sebelumnya diinstal tetap dapat diakses
* Pengaturan yang dikelola memiliki prioritas tertinggi dan tidak dapat ditimpa

Lihat [Pembatasan marketplace yang dikelola](/id/plugin-marketplaces#managed-marketplace-restrictions) untuk dokumentasi yang menghadap pengguna.

### Mengelola plugin

Gunakan perintah `/plugin` untuk mengelola plugin secara interaktif:

* Jelajahi plugin yang tersedia dari marketplace
* Instal/copot plugin
* Aktifkan/nonaktifkan plugin
* Lihat detail plugin (perintah, agents, hooks yang disediakan)
* Tambah/hapus marketplace

Pelajari lebih lanjut tentang sistem plugin dalam [dokumentasi plugins](/id/plugins).

## Variabel lingkungan

Variabel lingkungan memungkinkan Anda mengontrol perilaku Claude Code tanpa mengedit file pengaturan. Variabel apa pun juga dapat dikonfigurasi dalam [`settings.json`](#available-settings) di bawah kunci `env` untuk menerapkannya ke setiap sesi atau mengulanginya ke tim Anda.

Lihat [referensi variabel lingkungan](/id/env-vars) untuk daftar lengkap.

## Tools yang tersedia untuk Claude

Claude Code memiliki akses ke serangkaian tools untuk membaca, mengedit, mencari, menjalankan perintah, dan mengorkestrasi subagents. Nama tool adalah string tepat yang Anda gunakan dalam aturan izin dan pencocokan hook.

Lihat [referensi tools](/id/tools-reference) untuk daftar lengkap dan detail perilaku tool Bash.

## Lihat juga

* [Permissions](/id/permissions): sistem izin, sintaks aturan, pola spesifik tool, dan kebijakan yang dikelola
* [Authentication](/id/authentication): atur akses pengguna ke Claude Code
* [Troubleshooting](/id/troubleshooting): solusi untuk masalah konfigurasi umum
