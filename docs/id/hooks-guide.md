> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Otomatisasi alur kerja dengan hooks

> Jalankan perintah shell secara otomatis ketika Claude Code mengedit file, menyelesaikan tugas, atau memerlukan input. Format kode, kirim notifikasi, validasi perintah, dan terapkan aturan proyek.

Hooks adalah perintah shell yang ditentukan pengguna yang dijalankan pada titik-titik spesifik dalam siklus hidup Claude Code. Mereka memberikan kontrol deterministik atas perilaku Claude Code, memastikan tindakan tertentu selalu terjadi daripada mengandalkan LLM untuk memilih menjalankannya. Gunakan hooks untuk menegakkan aturan proyek, mengotomatisasi tugas berulang, dan mengintegrasikan Claude Code dengan alat yang sudah ada.

Untuk keputusan yang memerlukan penilaian daripada aturan deterministik, Anda juga dapat menggunakan [prompt-based hooks](#prompt-based-hooks) atau [agent-based hooks](#agent-based-hooks) yang menggunakan model Claude untuk mengevaluasi kondisi.

Untuk cara lain memperluas Claude Code, lihat [skills](/id/skills) untuk memberikan Claude instruksi tambahan dan perintah yang dapat dieksekusi, [subagents](/id/sub-agents) untuk menjalankan tugas dalam konteks terisolasi, dan [plugins](/id/plugins) untuk mengemas ekstensi untuk dibagikan di seluruh proyek.

<Tip>
  Panduan ini mencakup kasus penggunaan umum dan cara memulai. Untuk skema acara lengkap, format input/output JSON, dan fitur lanjutan seperti async hooks dan MCP tool hooks, lihat [Hooks reference](/id/hooks).
</Tip>

## Siapkan hook pertama Anda

Untuk membuat hook, tambahkan blok `hooks` ke [file pengaturan](#configure-hook-location). Panduan ini membuat hook notifikasi desktop, sehingga Anda mendapat peringatan kapan pun Claude menunggu input Anda daripada menonton terminal.

<Steps>
  <Step title="Tambahkan hook ke pengaturan Anda">
    Buka `~/.claude/settings.json` dan tambahkan hook `Notification`. Contoh di bawah menggunakan `osascript` untuk macOS; lihat [Dapatkan notifikasi ketika Claude memerlukan input](#get-notified-when-claude-needs-input) untuk perintah Linux dan Windows.

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

    Jika file pengaturan Anda sudah memiliki kunci `hooks`, gabungkan entri `Notification` ke dalamnya daripada mengganti seluruh objek. Anda juga dapat meminta Claude untuk menulis hook untuk Anda dengan mendeskripsikan apa yang Anda inginkan di CLI.
  </Step>

  <Step title="Verifikasi konfigurasi">
    Ketik `/hooks` untuk membuka browser hooks. Anda akan melihat daftar semua acara hook yang tersedia, dengan hitungan di sebelah setiap acara yang memiliki hooks yang dikonfigurasi. Pilih `Notification` untuk mengonfirmasi hook baru Anda muncul dalam daftar. Memilih hook menampilkan detailnya: acara, matcher, jenis, file sumber, dan perintah.
  </Step>

  <Step title="Uji hook">
    Tekan `Esc` untuk kembali ke CLI. Minta Claude untuk melakukan sesuatu yang memerlukan izin, kemudian beralih dari terminal. Anda harus menerima notifikasi desktop.
  </Step>
</Steps>

<Tip>
  Menu `/hooks` bersifat read-only. Untuk menambah, memodifikasi, atau menghapus hooks, edit JSON pengaturan Anda secara langsung atau minta Claude untuk membuat perubahan.
</Tip>

## Apa yang dapat Anda otomatisasi

Hooks memungkinkan Anda menjalankan kode pada titik-titik kunci dalam siklus hidup Claude Code: format file setelah edit, blokir perintah sebelum dijalankan, kirim notifikasi ketika Claude memerlukan input, injeksi konteks saat awal sesi, dan banyak lagi. Untuk daftar lengkap acara hook, lihat [Hooks reference](/id/hooks#hook-lifecycle).

Setiap contoh mencakup blok konfigurasi siap pakai yang Anda tambahkan ke [file pengaturan](#configure-hook-location). Pola paling umum:

* [Dapatkan notifikasi ketika Claude memerlukan input](#get-notified-when-claude-needs-input)
* [Auto-format kode setelah edit](#auto-format-code-after-edits)
* [Blokir edit ke file yang dilindungi](#block-edits-to-protected-files)
* [Re-inject konteks setelah compaction](#re-inject-context-after-compaction)
* [Audit perubahan konfigurasi](#audit-configuration-changes)
* [Auto-approve prompt izin tertentu](#auto-approve-specific-permission-prompts)

### Dapatkan notifikasi ketika Claude memerlukan input

Dapatkan notifikasi desktop kapan pun Claude selesai bekerja dan memerlukan input Anda, sehingga Anda dapat beralih ke tugas lain tanpa memeriksa terminal.

Hook ini menggunakan acara `Notification`, yang aktif ketika Claude menunggu input atau izin. Setiap tab di bawah menggunakan perintah notifikasi asli platform. Tambahkan ini ke `~/.claude/settings.json`:

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

### Auto-format kode setelah edit

Jalankan [Prettier](https://prettier.io/) secara otomatis pada setiap file yang Claude edit, sehingga pemformatan tetap konsisten tanpa intervensi manual.

Hook ini menggunakan acara `PostToolUse` dengan matcher `Edit|Write`, sehingga hanya berjalan setelah alat pengeditan file. Perintah mengekstrak jalur file yang diedit dengan [`jq`](https://jqlang.github.io/jq/) dan meneruskannya ke Prettier. Tambahkan ini ke `.claude/settings.json` di root proyek Anda:

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
  Contoh Bash di halaman ini menggunakan `jq` untuk parsing JSON. Instal dengan `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), atau lihat [`jq` downloads](https://jqlang.github.io/jq/download/).
</Note>

### Blokir edit ke file yang dilindungi

Cegah Claude dari memodifikasi file sensitif seperti `.env`, `package-lock.json`, atau apa pun di `.git/`. Claude menerima umpan balik yang menjelaskan mengapa edit diblokir, sehingga dapat menyesuaikan pendekatannya.

Contoh ini menggunakan file skrip terpisah yang dipanggil hook. Skrip memeriksa jalur file target terhadap daftar pola yang dilindungi dan keluar dengan kode 2 untuk memblokir edit.

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
    Tambahkan hook `PreToolUse` ke `.claude/settings.json` yang menjalankan skrip sebelum panggilan alat `Edit` atau `Write`:

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

### Re-inject konteks setelah compaction

Ketika jendela konteks Claude penuh, compaction merangkum percakapan untuk membebaskan ruang. Ini dapat kehilangan detail penting. Gunakan hook `SessionStart` dengan matcher `compact` untuk re-inject konteks kritis setelah setiap compaction.

Teks apa pun yang ditulis perintah Anda ke stdout ditambahkan ke konteks Claude. Contoh ini mengingatkan Claude tentang konvensi proyek dan pekerjaan terbaru. Tambahkan ini ke `.claude/settings.json` di root proyek Anda:

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

Matcher memfilter berdasarkan jenis konfigurasi: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, atau `skills`. Untuk memblokir perubahan agar tidak berlaku, keluar dengan kode 2 atau kembalikan `{"decision": "block"}`. Lihat [ConfigChange reference](/id/hooks#configchange) untuk skema input lengkap.

### Auto-approve prompt izin tertentu

Lewati dialog persetujuan untuk panggilan alat yang selalu Anda izinkan. Contoh ini auto-approve `ExitPlanMode`, alat yang Claude panggil ketika selesai menyajikan rencana dan meminta untuk melanjutkan, sehingga Anda tidak diminta setiap kali rencana siap.

Tidak seperti contoh kode keluar di atas, auto-approval memerlukan hook Anda untuk menulis keputusan JSON ke stdout. Hook `PermissionRequest` aktif ketika Claude Code akan menampilkan dialog izin, dan mengembalikan `"behavior": "allow"` menjawabnya atas nama Anda.

Matcher membatasi hook ke `ExitPlanMode` saja, sehingga tidak ada prompt lain yang terpengaruh. Tambahkan ini ke `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

Ketika hook menyetujui, Claude Code keluar dari plan mode dan mengembalikan mode izin apa pun yang aktif sebelum Anda memasuki plan mode. Transkrip menunjukkan "Allowed by PermissionRequest hook" di mana dialog akan muncul. Jalur hook selalu menjaga percakapan saat ini: tidak dapat menghapus konteks dan memulai sesi implementasi segar seperti yang dapat dilakukan dialog.

Untuk menetapkan mode izin tertentu sebagai gantinya, output hook Anda dapat menyertakan array `updatedPermissions` dengan entri `setMode`. Nilai `mode` adalah mode izin apa pun seperti `default`, `acceptEdits`, atau `bypassPermissions`, dan `destination: "session"` menerapkannya hanya untuk sesi saat ini.

Untuk beralih sesi ke `acceptEdits`, hook Anda menulis JSON ini ke stdout:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

Jaga matcher sesempit mungkin. Mencocokkan pada `.*` atau membiarkan matcher kosong akan auto-approve setiap prompt izin, termasuk penulisan file dan perintah shell. Lihat [PermissionRequest reference](/id/hooks#permissionrequest-decision-control) untuk set lengkap bidang keputusan.

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

Setiap hook memiliki `type` yang menentukan cara menjalankannya. Sebagian besar hooks menggunakan `"type": "command"`, yang menjalankan perintah shell. Tiga jenis lain tersedia:

* `"type": "http"`: POST data acara ke URL. Lihat [HTTP hooks](#http-hooks).
* `"type": "prompt"`: evaluasi LLM single-turn. Lihat [Prompt-based hooks](#prompt-based-hooks).
* `"type": "agent"`: verifikasi multi-turn dengan akses alat. Lihat [Agent-based hooks](#agent-based-hooks).

### Baca input dan kembalikan output

Hooks berkomunikasi dengan Claude Code melalui stdin, stdout, stderr, dan kode keluar. Ketika acara aktif, Claude Code meneruskan data spesifik acara sebagai JSON ke stdin skrip Anda. Skrip Anda membaca data itu, melakukan pekerjaan, dan memberi tahu Claude Code apa yang harus dilakukan selanjutnya melalui kode keluar.

#### Hook input

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

Skrip Anda dapat mengurai JSON itu dan bertindak atas bidang apa pun. Hook `UserPromptSubmit` mendapatkan teks `prompt` sebagai gantinya, hook `SessionStart` mendapatkan `source` (startup, resume, clear, compact), dan seterusnya. Lihat [Common input fields](/id/hooks#common-input-fields) dalam referensi untuk bidang bersama, dan bagian setiap acara untuk skema spesifik acara.

#### Hook output

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

#### Structured JSON output

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

Claude Code membaca `permissionDecision` dan membatalkan panggilan alat, kemudian memberi makan `permissionDecisionReason` kembali ke Claude sebagai umpan balik. Tiga opsi ini spesifik untuk `PreToolUse`:

* `"allow"`: lanjutkan tanpa menampilkan prompt izin
* `"deny"`: batalkan panggilan alat dan kirim alasan ke Claude
* `"ask"`: tampilkan prompt izin kepada pengguna seperti biasa

Acara lain menggunakan pola keputusan berbeda. Misalnya, hook `PostToolUse` dan `Stop` menggunakan bidang `decision: "block"` tingkat atas, sementara `PermissionRequest` menggunakan `hookSpecificOutput.decision.behavior`. Lihat [summary table](/id/hooks#decision-control) dalam referensi untuk rincian lengkap berdasarkan acara.

Untuk hook `UserPromptSubmit`, gunakan `additionalContext` sebagai gantinya untuk menyuntikkan teks ke dalam konteks Claude. Hook berbasis prompt (`type: "prompt"`) menangani output secara berbeda: lihat [Prompt-based hooks](#prompt-based-hooks).

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
| `SubagentStart`                                                                                 | jenis agen                 | `Bash`, `Explore`, `Plan`, atau nama agen khusus                                   |
| `PreCompact`                                                                                    | apa yang memicu compaction | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | jenis agen                 | nilai yang sama seperti `SubagentStart`                                            |
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
    Alat MCP menggunakan konvensi penamaan berbeda dari alat bawaan: `mcp__<server>__<tool>`, di mana `<server>` adalah nama server MCP dan `<tool>` adalah alat yang disediakannya. Misalnya, `mcp__github__search_repositories` atau `mcp__filesystem__read_file`. Gunakan matcher regex untuk menargetkan semua alat dari server spesifik, atau cocokkan di seluruh server dengan pola seperti `mcp__.*__write.*`. Lihat [Match MCP tools](/id/hooks#match-mcp-tools) dalam referensi untuk daftar lengkap contoh.

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

Untuk sintaks matcher lengkap, lihat [Hooks reference](/id/hooks#configuration).

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

Jalankan [`/hooks`](/id/hooks#the-hooks-menu) di Claude Code untuk menjelajahi semua hooks yang dikonfigurasi dikelompokkan berdasarkan acara. Untuk menonaktifkan semua hooks sekaligus, atur `"disableAllHooks": true` dalam file pengaturan Anda.

Jika Anda mengedit file pengaturan secara langsung saat Claude Code berjalan, file watcher biasanya mengambil perubahan hook secara otomatis.

## Prompt-based hooks

Untuk keputusan yang memerlukan penilaian daripada aturan deterministik, gunakan hook `type: "prompt"`. Daripada menjalankan perintah shell, Claude Code mengirim prompt Anda dan data input hook ke model Claude (Haiku secara default) untuk membuat keputusan. Anda dapat menentukan model berbeda dengan bidang `model` jika Anda memerlukan kemampuan lebih.

Satu-satunya pekerjaan model adalah mengembalikan keputusan ya/tidak sebagai JSON:

* `"ok": true`: tindakan berlanjut
* `"ok": false`: tindakan diblokir. `"reason"` model diberi makan kembali ke Claude sehingga dapat menyesuaikan.

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

Untuk opsi konfigurasi lengkap, lihat [Prompt-based hooks](/id/hooks#prompt-based-hooks) dalam referensi.

## Agent-based hooks

Ketika verifikasi memerlukan inspeksi file atau menjalankan perintah, gunakan hook `type: "agent"`. Tidak seperti hook prompt yang membuat panggilan LLM tunggal, hook agent menelurkan subagent yang dapat membaca file, mencari kode, dan menggunakan alat lain untuk memverifikasi kondisi sebelum mengembalikan keputusan.

Hook agent menggunakan format respons `"ok"` / `"reason"` yang sama seperti hook prompt, tetapi dengan timeout default lebih lama 60 detik dan hingga 50 putaran penggunaan alat.

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

Gunakan hook prompt ketika data input hook saja cukup untuk membuat keputusan. Gunakan hook agent ketika Anda perlu memverifikasi sesuatu terhadap keadaan aktual codebase.

Untuk opsi konfigurasi lengkap, lihat [Agent-based hooks](/id/hooks#agent-based-hooks) dalam referensi.

## HTTP hooks

Gunakan hook `type: "http"` untuk POST data acara ke endpoint HTTP daripada menjalankan perintah shell. Endpoint menerima JSON yang sama yang diterima hook perintah di stdin, dan mengembalikan hasil melalui badan respons HTTP menggunakan format JSON yang sama.

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

Endpoint harus mengembalikan badan respons JSON menggunakan [output format](/id/hooks#json-output) yang sama seperti hook perintah. Untuk memblokir panggilan alat, kembalikan respons 2xx dengan bidang `hookSpecificOutput` yang sesuai. Kode status HTTP saja tidak dapat memblokir tindakan.

Nilai header mendukung interpolasi variabel lingkungan menggunakan sintaks `$VAR_NAME` atau `${VAR_NAME}`. Hanya variabel yang tercantum dalam array `allowedEnvVars` yang diselesaikan; semua referensi `$VAR` lainnya tetap kosong.

Untuk opsi konfigurasi lengkap dan penanganan respons, lihat [HTTP hooks](/id/hooks#http-hook-fields) dalam referensi.

## Keterbatasan dan troubleshooting

### Keterbatasan

* Hook perintah berkomunikasi melalui stdout, stderr, dan kode keluar saja. Mereka tidak dapat memicu perintah atau panggilan alat secara langsung. HTTP hooks berkomunikasi melalui badan respons sebagai gantinya.
* Timeout hook adalah 10 menit secara default, dapat dikonfigurasi per hook dengan bidang `timeout` (dalam detik).
* Hook `PostToolUse` tidak dapat membatalkan tindakan karena alat sudah dieksekusi.
* Hook `PermissionRequest` tidak aktif dalam [non-interactive mode](/id/headless) (`-p`). Gunakan hook `PreToolUse` untuk keputusan izin otomatis.
* Hook `Stop` aktif kapan pun Claude selesai merespons, bukan hanya pada penyelesaian tugas. Mereka tidak aktif pada interupsi pengguna.

### Hook tidak aktif

Hook dikonfigurasi tetapi tidak pernah dieksekusi.

* Jalankan `/hooks` dan konfirmasi hook muncul di bawah acara yang benar
* Periksa bahwa pola matcher cocok dengan nama alat dengan tepat (matcher peka huruf besar-kecil)
* Verifikasi Anda memicu jenis acara yang benar (misalnya, `PreToolUse` aktif sebelum eksekusi alat, `PostToolUse` aktif setelah)
* Jika menggunakan hook `PermissionRequest` dalam mode non-interaktif (`-p`), beralih ke `PreToolUse` sebagai gantinya

### Hook error dalam output

Anda melihat pesan seperti "PreToolUse hook error: ..." dalam transkrip.

* Skrip Anda keluar dengan kode non-nol secara tidak terduga. Uji secara manual dengan menyalurkan JSON sampel:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* Jika Anda melihat "command not found", gunakan jalur absolut atau `$CLAUDE_PROJECT_DIR` untuk mereferensikan skrip
* Jika Anda melihat "jq: command not found", instal `jq` atau gunakan Python/Node.js untuk parsing JSON
* Jika skrip tidak berjalan sama sekali, buat dapat dieksekusi: `chmod +x ./my-hook.sh`

### `/hooks` menunjukkan tidak ada hooks yang dikonfigurasi

Anda mengedit file pengaturan tetapi hooks tidak muncul dalam menu.

* Edit file biasanya diambil secara otomatis. Jika belum muncul setelah beberapa detik, file watcher mungkin melewatkan perubahan: mulai ulang sesi Anda untuk memaksa reload.
* Verifikasi JSON Anda valid (trailing commas dan comments tidak diizinkan)
* Konfirmkan file pengaturan berada di lokasi yang benar: `.claude/settings.json` untuk hook proyek, `~/.claude/settings.json` untuk hook global

### Stop hook berjalan selamanya

Claude terus bekerja dalam loop tak terbatas daripada berhenti.

Skrip Stop hook Anda perlu memeriksa apakah sudah memicu kelanjutan. Parsing bidang `stop_hook_active` dari input JSON dan keluar lebih awal jika `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### JSON validation failed

Claude Code menampilkan kesalahan parsing JSON meskipun skrip hook Anda mengeluarkan JSON yang valid.

Ketika Claude Code menjalankan hook, ia menelurkan shell yang bersumber dari profil Anda (`~/.zshrc` atau `~/.bashrc`). Jika profil Anda berisi pernyataan `echo` tanpa syarat, output itu ditambahkan ke JSON hook Anda:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code mencoba mengurai ini sebagai JSON dan gagal. Untuk memperbaiki ini, bungkus pernyataan echo dalam profil shell Anda sehingga hanya berjalan di shell interaktif:

```bash  theme={null}
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

Variabel `$-` berisi flag shell, dan `i` berarti interaktif. Hooks berjalan di shell non-interaktif, jadi echo dilewati.

### Teknik debug

Alihkan mode verbose dengan `Ctrl+O` untuk melihat output hook dalam transkrip, atau jalankan `claude --debug` untuk detail eksekusi lengkap termasuk hook mana yang cocok dan kode keluar mereka.

## Pelajari lebih lanjut

* [Hooks reference](/id/hooks): skema acara lengkap, format output JSON, async hooks, dan MCP tool hooks
* [Security considerations](/id/hooks#security-considerations): tinjau sebelum menerapkan hooks dalam lingkungan bersama atau produksi
* [Bash command validator example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): implementasi referensi lengkap
