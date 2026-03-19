> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Otomatisasi alur kerja dengan hooks

> Jalankan perintah shell secara otomatis ketika Claude Code mengedit file, menyelesaikan tugas, atau memerlukan input. Format kode, kirim notifikasi, validasi perintah, dan terapkan aturan proyek.

Hooks adalah perintah shell yang ditentukan pengguna yang dijalankan pada titik-titik spesifik dalam siklus hidup Claude Code. Mereka memberikan kontrol deterministik atas perilaku Claude Code, memastikan tindakan tertentu selalu terjadi daripada mengandalkan LLM untuk memilih menjalankannya. Gunakan hooks untuk menegakkan aturan proyek, mengotomatisasi tugas berulang, dan mengintegrasikan Claude Code dengan alat yang sudah ada.

Untuk keputusan yang memerlukan penilaian daripada aturan deterministik, Anda juga dapat menggunakan [hooks berbasis prompt](#prompt-based-hooks) atau [hooks berbasis agent](#agent-based-hooks) yang menggunakan model Claude untuk mengevaluasi kondisi.

Untuk cara lain memperluas Claude Code, lihat [skills](/id/skills) untuk memberikan Claude instruksi tambahan dan perintah yang dapat dieksekusi, [subagents](/id/sub-agents) untuk menjalankan tugas dalam konteks terisolasi, dan [plugins](/id/plugins) untuk mengemas ekstensi untuk dibagikan di seluruh proyek.

<Tip>
  Panduan ini mencakup kasus penggunaan umum dan cara memulai. Untuk skema acara lengkap, format input/output JSON, dan fitur lanjutan seperti hooks asinkron dan hooks alat MCP, lihat [referensi Hooks](/id/hooks).
</Tip>

## Siapkan hook pertama Anda

Cara tercepat untuk membuat hook adalah melalui menu interaktif `/hooks` di Claude Code. Panduan ini membuat hook notifikasi desktop, sehingga Anda mendapat peringatan kapan pun Claude menunggu input Anda daripada menonton terminal.

<Steps>
  <Step title="Buka menu hooks">
    Ketik `/hooks` di CLI Claude Code. Anda akan melihat daftar semua acara hook yang tersedia, ditambah opsi untuk menonaktifkan semua hooks. Setiap acara sesuai dengan titik dalam siklus hidup Claude di mana Anda dapat menjalankan kode khusus. Pilih `Notification` untuk membuat hook yang aktif ketika Claude memerlukan perhatian Anda.
  </Step>

  <Step title="Konfigurasi matcher">
    Menu menampilkan daftar matcher, yang memfilter kapan hook aktif. Atur matcher ke `*` untuk aktif pada semua jenis notifikasi. Anda dapat mempersempit nanti dengan mengubah matcher ke nilai spesifik seperti `permission_prompt` atau `idle_prompt`.
  </Step>

  <Step title="Tambahkan perintah Anda">
    Pilih `+ Add new hook…`. Menu meminta Anda untuk perintah shell yang akan dijalankan ketika acara aktif. Hooks menjalankan perintah shell apa pun yang Anda berikan, jadi Anda dapat menggunakan alat notifikasi bawaan platform Anda. Salin perintah untuk OS Anda:

    <Tabs>
      <Tab title="macOS">
        Menggunakan [`osascript`](https://ss64.com/mac/osascript.html) untuk memicu notifikasi macOS asli melalui AppleScript:

        ```bash  theme={null}
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Menggunakan `notify-send`, yang sudah diinstal sebelumnya di sebagian besar desktop Linux dengan daemon notifikasi:

        ```bash  theme={null}
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Menggunakan PowerShell untuk menampilkan kotak pesan asli melalui Windows Forms .NET:

        ```powershell  theme={null}
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Pilih lokasi penyimpanan">
    Menu menanyakan di mana menyimpan konfigurasi hook. Pilih `User settings` untuk menyimpannya di `~/.claude/settings.json`, yang menerapkan hook ke semua proyek Anda. Anda juga dapat memilih `Project settings` untuk membatasi ke proyek saat ini. Lihat [Konfigurasi lokasi hook](#configure-hook-location) untuk semua cakupan yang tersedia.
  </Step>

  <Step title="Uji hook">
    Tekan `Esc` untuk kembali ke CLI. Minta Claude untuk melakukan sesuatu yang memerlukan izin, kemudian beralih dari terminal. Anda harus menerima notifikasi desktop.
  </Step>
</Steps>

## Apa yang dapat Anda otomatisasi

Hooks memungkinkan Anda menjalankan kode pada titik-titik kunci dalam siklus hidup Claude Code: format file setelah edit, blokir perintah sebelum dijalankan, kirim notifikasi ketika Claude memerlukan input, injeksi konteks saat awal sesi, dan banyak lagi. Untuk daftar lengkap acara hook, lihat [referensi Hooks](/id/hooks#hook-lifecycle).

Setiap contoh mencakup blok konfigurasi siap pakai yang Anda tambahkan ke [file pengaturan](#configure-hook-location). Pola paling umum:

* [Dapatkan notifikasi ketika Claude memerlukan input](#get-notified-when-claude-needs-input)
* [Format kode otomatis setelah edit](#auto-format-code-after-edits)
* [Blokir edit ke file yang dilindungi](#block-edits-to-protected-files)
* [Injeksi ulang konteks setelah pemadatan](#re-inject-context-after-compaction)
* [Audit perubahan konfigurasi](#audit-configuration-changes)

### Dapatkan notifikasi ketika Claude memerlukan input

Dapatkan notifikasi desktop kapan pun Claude selesai bekerja dan memerlukan input Anda, sehingga Anda dapat beralih ke tugas lain tanpa memeriksa terminal.

Hook ini menggunakan acara `Notification`, yang aktif ketika Claude menunggu input atau izin. Setiap tab di bawah menggunakan perintah notifikasi asli platform. Tambahkan ini ke `~/.claude/settings.json`, atau gunakan [panduan interaktif](#set-up-your-first-hook) di atas untuk mengonfigurasinya dengan `/hooks`:

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### Format kode otomatis setelah edit

Jalankan [Prettier](https://prettier.io/) secara otomatis pada setiap file yang Claude edit, sehingga pemformatan tetap konsisten tanpa intervensi manual.

Hook ini menggunakan acara `PostToolUse` dengan matcher `Edit|Write`, sehingga hanya berjalan setelah alat pengeditan file. Perintah mengekstrak jalur file yang diedit dengan [`jq`](https://jqlang.github.io/jq/) dan meneruskannya ke Prettier. Tambahkan ini ke `.claude/settings.json` di akar proyek Anda:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  Contoh Bash di halaman ini menggunakan `jq` untuk penguraian JSON. Instal dengan `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), atau lihat [unduhan `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Blokir edit ke file yang dilindungi

Cegah Claude dari memodifikasi file sensitif seperti `.env`, `package-lock.json`, atau apa pun di `.git/`. Claude menerima umpan balik yang menjelaskan mengapa edit diblokir, sehingga dapat menyesuaikan pendekatannya.

Contoh ini menggunakan file skrip terpisah yang dipanggil oleh hook. Skrip memeriksa jalur file target terhadap daftar pola yang dilindungi dan keluar dengan kode 2 untuk memblokir edit.

<Steps>
  <Step title="Buat skrip hook">
    Simpan ini ke `.claude/hooks/protect-files.sh`:

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="Buat skrip dapat dieksekusi (macOS/Linux)">
    Skrip hook harus dapat dieksekusi agar Claude Code dapat menjalankannya:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Daftarkan hook">
    Tambahkan hook `PreToolUse` ke `.claude/settings.json` yang menjalankan skrip sebelum panggilan alat `Edit` atau `Write` apa pun:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### Injeksi ulang konteks setelah pemadatan

Ketika jendela konteks Claude penuh, pemadatan merangkum percakapan untuk membebaskan ruang. Ini dapat kehilangan detail penting. Gunakan hook `SessionStart` dengan matcher `compact` untuk injeksi ulang konteks kritis setelah setiap pemadatan.

Teks apa pun yang ditulis perintah Anda ke stdout ditambahkan ke konteks Claude. Contoh ini mengingatkan Claude tentang konvensi proyek dan pekerjaan terbaru. Tambahkan ini ke `.claude/settings.json` di akar proyek Anda:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

Anda dapat mengganti `echo` dengan perintah apa pun yang menghasilkan output dinamis, seperti `git log --oneline -5` untuk menampilkan commit terbaru. Untuk injeksi konteks pada setiap awal sesi, pertimbangkan menggunakan [CLAUDE.md](/id/memory) sebagai gantinya. Untuk variabel lingkungan, lihat [`CLAUDE_ENV_FILE`](/id/hooks#persist-environment-variables) dalam referensi.

### Audit perubahan konfigurasi

Lacak ketika file pengaturan atau skills berubah selama sesi. Acara `ConfigChange` aktif ketika proses eksternal atau editor memodifikasi file konfigurasi, sehingga Anda dapat mencatat perubahan untuk kepatuhan atau memblokir modifikasi yang tidak sah.

Contoh ini menambahkan setiap perubahan ke log audit. Tambahkan ini ke `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

Matcher memfilter berdasarkan jenis konfigurasi: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, atau `skills`. Untuk memblokir perubahan agar tidak berlaku, keluar dengan kode 2 atau kembalikan `{"decision": "block"}`. Lihat [referensi ConfigChange](/id/hooks#configchange) untuk skema input lengkap.

## Cara kerja hooks

Acara hook aktif pada titik-titik siklus hidup spesifik di Claude Code. Ketika acara aktif, semua hook yang cocok berjalan secara paralel, dan perintah hook yang identik secara otomatis dideduplikasi. Tabel di bawah menunjukkan setiap acara dan kapan dipicu:

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

Setiap hook memiliki `type` yang menentukan cara menjalankannya. Sebagian besar hooks menggunakan `"type": "command"`, yang menjalankan perintah shell. Tiga jenis lainnya tersedia:

* `"type": "http"`: POST data acara ke URL. Lihat [HTTP hooks](#http-hooks).
* `"type": "prompt"`: evaluasi LLM satu putaran. Lihat [Hooks berbasis prompt](#prompt-based-hooks).
* `"type": "agent"`: verifikasi multi-putaran dengan akses alat. Lihat [Hooks berbasis agent](#agent-based-hooks).

### Baca input dan kembalikan output

Hooks berkomunikasi dengan Claude Code melalui stdin, stdout, stderr, dan kode keluar. Ketika acara aktif, Claude Code meneruskan data khusus acara sebagai JSON ke stdin skrip Anda. Skrip Anda membaca data itu, melakukan pekerjaan, dan memberi tahu Claude Code apa yang harus dilakukan selanjutnya melalui kode keluar.

#### Input hook

Setiap acara mencakup bidang umum seperti `session_id` dan `cwd`, tetapi setiap jenis acara menambahkan data berbeda. Misalnya, ketika Claude menjalankan perintah Bash, hook `PreToolUse` menerima sesuatu seperti ini di stdin:

```json  theme={null}
{
  "session_id": "abc123",          // unique ID for this session
  "cwd": "/Users/sarah/myproject", // working directory when the event fired
  "hook_event_name": "PreToolUse", // which event triggered this hook
  "tool_name": "Bash",             // the tool Claude is about to use
  "tool_input": {                  // the arguments Claude passed to the tool
    "command": "npm test"          // for Bash, this is the shell command
  }
}
```

Skrip Anda dapat menguraikan JSON itu dan bertindak atas bidang apa pun. Hook `UserPromptSubmit` mendapatkan teks `prompt` sebagai gantinya, hook `SessionStart` mendapatkan `source` (startup, resume, clear, compact), dan seterusnya. Lihat [Bidang input umum](/id/hooks#common-input-fields) dalam referensi untuk bidang bersama, dan bagian setiap acara untuk skema khusus acara.

#### Output hook

Skrip Anda memberi tahu Claude Code apa yang harus dilakukan selanjutnya dengan menulis ke stdout atau stderr dan keluar dengan kode spesifik. Misalnya, hook `PreToolUse` yang ingin memblokir perintah:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr becomes Claude's feedback
  exit 2 # exit 2 = block the action
fi

exit 0  # exit 0 = let it proceed
```

Kode keluar menentukan apa yang terjadi selanjutnya:

* **Exit 0**: tindakan berlanjut. Untuk hook `UserPromptSubmit` dan `SessionStart`, apa pun yang Anda tulis ke stdout ditambahkan ke konteks Claude.
* **Exit 2**: tindakan diblokir. Tulis alasan ke stderr, dan Claude menerimanya sebagai umpan balik sehingga dapat menyesuaikan.
* **Kode keluar lainnya**: tindakan berlanjut. Stderr dicatat tetapi tidak ditampilkan ke Claude. Alihkan mode verbose dengan `Ctrl+O` untuk melihat pesan ini dalam transkrip.

#### Output JSON terstruktur

Kode keluar memberi Anda dua opsi: izinkan atau blokir. Untuk kontrol lebih, keluar 0 dan cetak objek JSON ke stdout sebagai gantinya.

<Note>
  Gunakan exit 2 untuk memblokir dengan pesan stderr, atau exit 0 dengan JSON untuk kontrol terstruktur. Jangan campur: Claude Code mengabaikan JSON ketika Anda exit 2.
</Note>

Misalnya, hook `PreToolUse` dapat menolak panggilan alat dan memberi tahu Claude mengapa, atau meningkatkannya ke pengguna untuk persetujuan:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code membaca `permissionDecision` dan membatalkan panggilan alat, kemudian memberi umpan balik `permissionDecisionReason` kembali ke Claude. Tiga opsi ini khusus untuk `PreToolUse`:

* `"allow"`: lanjutkan tanpa menampilkan prompt izin
* `"deny"`: batalkan panggilan alat dan kirim alasan ke Claude
* `"ask"`: tampilkan prompt izin kepada pengguna seperti biasa

Acara lain menggunakan pola keputusan berbeda. Misalnya, hook `PostToolUse` dan `Stop` menggunakan bidang `decision: "block"` tingkat atas, sementara `PermissionRequest` menggunakan `hookSpecificOutput.decision.behavior`. Lihat [tabel ringkasan](/id/hooks#decision-control) dalam referensi untuk rincian lengkap menurut acara.

Untuk hook `UserPromptSubmit`, gunakan `additionalContext` sebagai gantinya untuk injeksi teks ke dalam konteks Claude. Hooks berbasis prompt (`type: "prompt"`) menangani output secara berbeda: lihat [Hooks berbasis prompt](#prompt-based-hooks).

### Filter hooks dengan matchers

Tanpa matcher, hook aktif pada setiap kemunculan acaranya. Matchers memungkinkan Anda mempersempit itu. Misalnya, jika Anda ingin menjalankan formatter hanya setelah edit file (bukan setelah setiap panggilan alat), tambahkan matcher ke hook `PostToolUse` Anda:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

Matcher `"Edit|Write"` adalah pola regex yang cocok dengan nama alat. Hook hanya aktif ketika Claude menggunakan alat `Edit` atau `Write`, bukan ketika menggunakan `Bash`, `Read`, atau alat lainnya.

Setiap jenis acara cocok pada bidang spesifik. Matchers mendukung string tepat dan pola regex:

| Acara                                                                                           | Apa yang difilter matcher  | Contoh nilai matcher                                                               |
| :---------------------------------------------------------------------------------------------- | :------------------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | nama alat                  | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                  | cara sesi dimulai          | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                    | mengapa sesi berakhir      | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                  | jenis notifikasi           | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                 | jenis agent                | `Bash`, `Explore`, `Plan`, atau nama agent khusus                                  |
| `PreCompact`                                                                                    | apa yang memicu pemadatan  | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | jenis agent                | nilai yang sama seperti `SubagentStart`                                            |
| `ConfigChange`                                                                                  | sumber konfigurasi         | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | tidak ada dukungan matcher | selalu aktif pada setiap kemunculan                                                |

Beberapa contoh lagi menunjukkan matchers pada jenis acara berbeda:

<Tabs>
  <Tab title="Catat setiap perintah Bash">
    Cocokkan hanya panggilan alat `Bash` dan catat setiap perintah ke file. Acara `PostToolUse` aktif setelah perintah selesai, jadi `tool_input.command` berisi apa yang berjalan. Hook menerima data acara sebagai JSON di stdin, dan `jq -r '.tool_input.command'` mengekstrak hanya string perintah, yang `>>` tambahkan ke file log:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Cocokkan alat MCP">
    Alat MCP menggunakan konvensi penamaan berbeda dari alat bawaan: `mcp__<server>__<tool>`, di mana `<server>` adalah nama server MCP dan `<tool>` adalah alat yang disediakannya. Misalnya, `mcp__github__search_repositories` atau `mcp__filesystem__read_file`. Gunakan matcher regex untuk menargetkan semua alat dari server spesifik, atau cocokkan di seluruh server dengan pola seperti `mcp__.*__write.*`. Lihat [Cocokkan alat MCP](/id/hooks#match-mcp-tools) dalam referensi untuk daftar lengkap contoh.

    Perintah di bawah mengekstrak nama alat dari input JSON hook dengan `jq` dan menulisnya ke stderr, di mana muncul dalam mode verbose (`Ctrl+O`):

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Bersihkan saat akhir sesi">
    Acara `SessionEnd` mendukung matchers pada alasan sesi berakhir. Hook ini hanya aktif pada `clear` (ketika Anda menjalankan `/clear`), bukan pada keluar normal:

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

Untuk sintaks matcher lengkap, lihat [referensi Hooks](/id/hooks#configuration).

### Konfigurasi lokasi hook

Di mana Anda menambahkan hook menentukan cakupannya:

| Lokasi                                                       | Cakupan                     | Dapat Dibagikan                       |
| :----------------------------------------------------------- | :-------------------------- | :------------------------------------ |
| `~/.claude/settings.json`                                    | Semua proyek Anda           | Tidak, lokal ke mesin Anda            |
| `.claude/settings.json`                                      | Proyek tunggal              | Ya, dapat dikomit ke repo             |
| `.claude/settings.local.json`                                | Proyek tunggal              | Tidak, gitignored                     |
| Pengaturan kebijakan terkelola                               | Seluruh organisasi          | Ya, dikendalikan admin                |
| [Plugin](/id/plugins) `hooks/hooks.json`                     | Ketika plugin diaktifkan    | Ya, dikemas dengan plugin             |
| [Skill](/id/skills) atau [agent](/id/sub-agents) frontmatter | Saat skill atau agent aktif | Ya, didefinisikan dalam file komponen |

Anda juga dapat menggunakan menu [`/hooks`](/id/hooks#the-hooks-menu) di Claude Code untuk menambah, menghapus, dan melihat hooks secara interaktif. Untuk menonaktifkan semua hooks sekaligus, gunakan toggle di bagian bawah menu `/hooks` atau atur `"disableAllHooks": true` dalam file pengaturan Anda.

Hooks yang ditambahkan melalui menu `/hooks` berlaku segera. Jika Anda mengedit file pengaturan secara langsung saat Claude Code berjalan, perubahan tidak akan berlaku sampai Anda meninjau dalam menu `/hooks` atau memulai ulang sesi Anda.

## Hooks berbasis prompt

Untuk keputusan yang memerlukan penilaian daripada aturan deterministik, gunakan hooks `type: "prompt"`. Daripada menjalankan perintah shell, Claude Code mengirim prompt Anda dan data input hook ke model Claude (Haiku secara default) untuk membuat keputusan. Anda dapat menentukan model berbeda dengan bidang `model` jika Anda memerlukan kemampuan lebih.

Satu-satunya pekerjaan model adalah mengembalikan keputusan ya/tidak sebagai JSON:

* `"ok": true`: tindakan berlanjut
* `"ok": false`: tindakan diblokir. `"reason"` model diberi umpan balik ke Claude sehingga dapat menyesuaikan.

Contoh ini menggunakan hook `Stop` untuk menanyakan kepada model apakah semua tugas yang diminta selesai. Jika model mengembalikan `"ok": false`, Claude terus bekerja dan menggunakan `reason` sebagai instruksi berikutnya:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

Untuk opsi konfigurasi lengkap, lihat [Hooks berbasis prompt](/id/hooks#prompt-based-hooks) dalam referensi.

## Hooks berbasis agent

Ketika verifikasi memerlukan inspeksi file atau menjalankan perintah, gunakan hooks `type: "agent"`. Tidak seperti hooks prompt yang membuat panggilan LLM tunggal, hooks agent menelurkan subagent yang dapat membaca file, mencari kode, dan menggunakan alat lain untuk memverifikasi kondisi sebelum mengembalikan keputusan.

Hooks agent menggunakan format respons `"ok"` / `"reason"` yang sama seperti hooks prompt, tetapi dengan timeout default lebih lama 60 detik dan hingga 50 putaran penggunaan alat.

Contoh ini memverifikasi bahwa tes lulus sebelum memungkinkan Claude berhenti:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Gunakan hooks prompt ketika data input hook saja cukup untuk membuat keputusan. Gunakan hooks agent ketika Anda perlu memverifikasi sesuatu terhadap keadaan aktual codebase.

Untuk opsi konfigurasi lengkap, lihat [Hooks berbasis agent](/id/hooks#agent-based-hooks) dalam referensi.

## HTTP hooks

Gunakan hooks `type: "http"` untuk POST data acara ke endpoint HTTP daripada menjalankan perintah shell. Endpoint menerima JSON yang sama yang diterima hook perintah di stdin, dan mengembalikan hasil melalui badan respons HTTP menggunakan format JSON yang sama.

HTTP hooks berguna ketika Anda ingin server web, fungsi cloud, atau layanan eksternal menangani logika hook: misalnya, layanan audit bersama yang mencatat acara penggunaan alat di seluruh tim.

Contoh ini memposting setiap penggunaan alat ke layanan logging lokal:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

Endpoint harus mengembalikan badan respons JSON menggunakan [format output](/id/hooks#json-output) yang sama seperti hooks perintah. Untuk memblokir panggilan alat, kembalikan respons 2xx dengan bidang `hookSpecificOutput` yang sesuai. Kode status HTTP saja tidak dapat memblokir tindakan.

Nilai header mendukung interpolasi variabel lingkungan menggunakan sintaks `$VAR_NAME` atau `${VAR_NAME}`. Hanya variabel yang tercantum dalam array `allowedEnvVars` yang diselesaikan; semua referensi `$VAR` lainnya tetap kosong.

<Note>
  HTTP hooks harus dikonfigurasi dengan mengedit JSON pengaturan Anda secara langsung. Menu interaktif `/hooks` hanya mendukung penambahan hooks perintah.
</Note>

Untuk opsi konfigurasi lengkap dan penanganan respons, lihat [HTTP hooks](/id/hooks#http-hook-fields) dalam referensi.

## Batasan dan pemecahan masalah

### Batasan

* Hooks perintah berkomunikasi melalui stdout, stderr, dan kode keluar saja. Mereka tidak dapat memicu perintah atau panggilan alat secara langsung. HTTP hooks berkomunikasi melalui badan respons sebagai gantinya.
* Timeout hook adalah 10 menit secara default, dapat dikonfigurasi per hook dengan bidang `timeout` (dalam detik).
* Hook `PostToolUse` tidak dapat membatalkan tindakan karena alat sudah dieksekusi.
* Hook `PermissionRequest` tidak aktif dalam [mode non-interaktif](/id/headless) (`-p`). Gunakan hooks `PreToolUse` untuk keputusan izin otomatis.
* Hook `Stop` aktif kapan pun Claude selesai merespons, bukan hanya saat penyelesaian tugas. Mereka tidak aktif pada interupsi pengguna.

### Hook tidak aktif

Hook dikonfigurasi tetapi tidak pernah dieksekusi.

* Jalankan `/hooks` dan konfirmasi hook muncul di bawah acara yang benar
* Periksa bahwa pola matcher cocok dengan nama alat dengan tepat (matchers peka huruf besar-kecil)
* Verifikasi Anda memicu jenis acara yang benar (misalnya, `PreToolUse` aktif sebelum eksekusi alat, `PostToolUse` aktif setelah)
* Jika menggunakan hooks `PermissionRequest` dalam mode non-interaktif (`-p`), beralih ke `PreToolUse` sebagai gantinya

### Kesalahan hook dalam output

Anda melihat pesan seperti "PreToolUse hook error: ..." dalam transkrip.

* Skrip Anda keluar dengan kode non-nol secara tidak terduga. Uji secara manual dengan menyalurkan JSON sampel:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* Jika Anda melihat "command not found", gunakan jalur absolut atau `$CLAUDE_PROJECT_DIR` untuk mereferensikan skrip
* Jika Anda melihat "jq: command not found", instal `jq` atau gunakan Python/Node.js untuk penguraian JSON
* Jika skrip tidak berjalan sama sekali, buatnya dapat dieksekusi: `chmod +x ./my-hook.sh`

### `/hooks` menunjukkan tidak ada hooks yang dikonfigurasi

Anda mengedit file pengaturan tetapi hooks tidak muncul dalam menu.

* Mulai ulang sesi Anda atau buka `/hooks` untuk memuat ulang. Hooks yang ditambahkan melalui menu `/hooks` berlaku segera, tetapi edit file manual memerlukan reload.
* Verifikasi JSON Anda valid (koma trailing dan komentar tidak diizinkan)
* Konfirmasi file pengaturan berada di lokasi yang benar: `.claude/settings.json` untuk hooks proyek, `~/.claude/settings.json` untuk hooks global

### Hook Stop berjalan selamanya

Claude terus bekerja dalam loop tak terbatas daripada berhenti.

Skrip hook Stop Anda perlu memeriksa apakah sudah memicu kelanjutan. Uraikan bidang `stop_hook_active` dari input JSON dan keluar lebih awal jika `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### Validasi JSON gagal

Claude Code menampilkan kesalahan penguraian JSON meskipun skrip hook Anda menampilkan JSON yang valid.

Ketika Claude Code menjalankan hook, ia menelurkan shell yang bersumber dari profil Anda (`~/.zshrc` atau `~/.bashrc`). Jika profil Anda berisi pernyataan `echo` tanpa syarat, output itu ditambahkan ke JSON hook Anda:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code mencoba menguraikan ini sebagai JSON dan gagal. Untuk memperbaiki ini, bungkus pernyataan echo dalam profil shell Anda sehingga hanya berjalan di shell interaktif:

```bash  theme={null}
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

Variabel `$-` berisi flag shell, dan `i` berarti interaktif. Hooks berjalan di shell non-interaktif, jadi echo dilewati.

### Teknik debug

Alihkan mode verbose dengan `Ctrl+O` untuk melihat output hook dalam transkrip, atau jalankan `claude --debug` untuk detail eksekusi lengkap termasuk hooks mana yang cocok dan kode keluar mereka.

## Pelajari lebih lanjut

* [Referensi Hooks](/id/hooks): skema acara lengkap, format output JSON, hooks asinkron, dan hooks alat MCP
* [Pertimbangan keamanan](/id/hooks#security-considerations): tinjau sebelum menerapkan hooks di lingkungan bersama atau produksi
* [Contoh validator perintah Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): implementasi referensi lengkap
