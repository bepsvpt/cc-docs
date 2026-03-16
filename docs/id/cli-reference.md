> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referensi CLI

> Referensi lengkap untuk antarmuka baris perintah Claude Code, termasuk perintah dan flag.

## Perintah CLI

Anda dapat memulai sesi, menyalurkan konten, melanjutkan percakapan, dan mengelola pembaruan dengan perintah-perintah ini:

| Perintah                        | Deskripsi                                                                                                                                                                                            | Contoh                                             |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | Mulai sesi interaktif                                                                                                                                                                                | `claude`                                           |
| `claude "query"`                | Mulai sesi interaktif dengan prompt awal                                                                                                                                                             | `claude "explain this project"`                    |
| `claude -p "query"`             | Kueri melalui SDK, kemudian keluar                                                                                                                                                                   | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | Proses konten yang disalurkan                                                                                                                                                                        | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | Lanjutkan percakapan terbaru di direktori saat ini                                                                                                                                                   | `claude -c`                                        |
| `claude -c -p "query"`          | Lanjutkan melalui SDK                                                                                                                                                                                | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | Lanjutkan sesi berdasarkan ID atau nama                                                                                                                                                              | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | Perbarui ke versi terbaru                                                                                                                                                                            | `claude update`                                    |
| `claude auth login`             | Masuk ke akun Anthropic Anda. Gunakan `--email` untuk mengisi email Anda sebelumnya dan `--sso` untuk memaksa autentikasi SSO                                                                        | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Keluar dari akun Anthropic Anda                                                                                                                                                                      | `claude auth logout`                               |
| `claude auth status`            | Tampilkan status autentikasi sebagai JSON. Gunakan `--text` untuk output yang dapat dibaca manusia. Keluar dengan kode 0 jika masuk, 1 jika tidak                                                    | `claude auth status`                               |
| `claude agents`                 | Daftar semua [subagents](/id/sub-agents) yang dikonfigurasi, dikelompokkan berdasarkan sumber                                                                                                        | `claude agents`                                    |
| `claude mcp`                    | Konfigurasi server Model Context Protocol (MCP)                                                                                                                                                      | Lihat [dokumentasi Claude Code MCP](/id/mcp).      |
| `claude remote-control`         | Mulai sesi [Remote Control](/id/remote-control) untuk mengontrol Claude Code dari Claude.ai atau aplikasi Claude sambil berjalan secara lokal. Lihat [Remote Control](/id/remote-control) untuk flag | `claude remote-control`                            |

## Flag CLI

Sesuaikan perilaku Claude Code dengan flag baris perintah ini:

| Flag                                   | Deskripsi                                                                                                                                                                                                                          | Contoh                                                                                             |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Tambahkan direktori kerja tambahan untuk Claude akses (memvalidasi setiap jalur ada sebagai direktori)                                                                                                                             | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Tentukan agen untuk sesi saat ini (menimpa pengaturan `agent`)                                                                                                                                                                     | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Tentukan [subagents](/id/sub-agents) kustom secara dinamis melalui JSON (lihat di bawah untuk format)                                                                                                                              | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Aktifkan bypass izin sebagai opsi tanpa langsung mengaktifkannya. Memungkinkan komposisi dengan `--permission-mode` (gunakan dengan hati-hati)                                                                                     | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Alat yang dijalankan tanpa meminta izin. Lihat [sintaks aturan izin](/id/settings#permission-rule-syntax) untuk pencocokan pola. Untuk membatasi alat mana yang tersedia, gunakan `--tools` sebagai gantinya                       | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Tambahkan teks kustom ke akhir prompt sistem default                                                                                                                                                                               | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Muat teks prompt sistem tambahan dari file dan tambahkan ke prompt default                                                                                                                                                         | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | Header beta untuk disertakan dalam permintaan API (hanya pengguna kunci API)                                                                                                                                                       | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Aktifkan [integrasi browser Chrome](/id/chrome) untuk otomasi web dan pengujian                                                                                                                                                    | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Muat percakapan terbaru di direktori saat ini                                                                                                                                                                                      | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Lewati semua prompt izin (gunakan dengan hati-hati)                                                                                                                                                                                | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Aktifkan mode debug dengan penyaringan kategori opsional (misalnya, `"api,hooks"` atau `"!statsig,!file"`)                                                                                                                         | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Nonaktifkan semua skills dan perintah untuk sesi ini                                                                                                                                                                               | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Alat yang dihapus dari konteks model dan tidak dapat digunakan                                                                                                                                                                     | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Aktifkan fallback otomatis ke model yang ditentukan ketika model default kelebihan beban (mode cetak saja)                                                                                                                         | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | Saat melanjutkan, buat ID sesi baru alih-alih menggunakan kembali yang asli (gunakan dengan `--resume` atau `--continue`)                                                                                                          | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Lanjutkan sesi yang ditautkan ke PR GitHub tertentu. Menerima nomor PR atau URL. Sesi secara otomatis ditautkan saat dibuat melalui `gh pr create`                                                                                 | `claude --from-pr 123`                                                                             |
| `--ide`                                | Terhubung secara otomatis ke IDE saat startup jika tepat satu IDE valid tersedia                                                                                                                                                   | `claude --ide`                                                                                     |
| `--init`                               | Jalankan hook inisialisasi dan mulai mode interaktif                                                                                                                                                                               | `claude --init`                                                                                    |
| `--init-only`                          | Jalankan hook inisialisasi dan keluar (tidak ada sesi interaktif)                                                                                                                                                                  | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Sertakan peristiwa streaming parsial dalam output (memerlukan `--print` dan `--output-format=stream-json`)                                                                                                                         | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Tentukan format input untuk mode cetak (opsi: `text`, `stream-json`)                                                                                                                                                               | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Dapatkan output JSON yang divalidasi sesuai dengan JSON Schema setelah agen menyelesaikan alurnya (mode cetak saja, lihat [structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs))                  | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Jalankan hook pemeliharaan dan keluar                                                                                                                                                                                              | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Jumlah dolar maksimum untuk dihabiskan pada panggilan API sebelum berhenti (mode cetak saja)                                                                                                                                       | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Batasi jumlah putaran agentic (mode cetak saja). Keluar dengan kesalahan saat batas tercapai. Tidak ada batas secara default                                                                                                       | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Muat server MCP dari file JSON atau string (dipisahkan spasi)                                                                                                                                                                      | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Menetapkan model untuk sesi saat ini dengan alias untuk model terbaru (`sonnet` atau `opus`) atau nama lengkap model                                                                                                               | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Nonaktifkan [integrasi browser Chrome](/id/chrome) untuk sesi ini                                                                                                                                                                  | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Nonaktifkan persistensi sesi sehingga sesi tidak disimpan ke disk dan tidak dapat dilanjutkan (mode cetak saja)                                                                                                                    | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Tentukan format output untuk mode cetak (opsi: `text`, `json`, `stream-json`)                                                                                                                                                      | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Mulai dalam [mode izin](/id/permissions#permission-modes) yang ditentukan                                                                                                                                                          | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Tentukan alat MCP untuk menangani prompt izin dalam mode non-interaktif                                                                                                                                                            | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Muat plugin dari direktori untuk sesi ini saja (dapat diulang)                                                                                                                                                                     | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Cetak respons tanpa mode interaktif (lihat [dokumentasi Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) untuk detail penggunaan programatik)                                                                    | `claude -p "query"`                                                                                |
| `--remote`                             | Buat sesi [web](/id/claude-code-on-the-web) baru di claude.ai dengan deskripsi tugas yang disediakan                                                                                                                               | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Lanjutkan sesi tertentu berdasarkan ID atau nama, atau tampilkan pemilih interaktif untuk memilih sesi                                                                                                                             | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Gunakan ID sesi tertentu untuk percakapan (harus UUID yang valid)                                                                                                                                                                  | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Daftar sumber pengaturan yang dipisahkan koma untuk dimuat (`user`, `project`, `local`)                                                                                                                                            | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Jalur ke file JSON pengaturan atau string JSON untuk memuat pengaturan tambahan dari                                                                                                                                               | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Hanya gunakan server MCP dari `--mcp-config`, abaikan semua konfigurasi MCP lainnya                                                                                                                                                | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Ganti seluruh prompt sistem dengan teks kustom                                                                                                                                                                                     | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Muat prompt sistem dari file, mengganti prompt default                                                                                                                                                                             | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Lanjutkan sesi [web](/id/claude-code-on-the-web) di terminal lokal Anda                                                                                                                                                            | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Atur bagaimana [tim agen](/id/agent-teams) rekan kerja ditampilkan: `auto` (default), `in-process`, atau `tmux`. Lihat [atur tim agen](/id/agent-teams#set-up-agent-teams)                                                         | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Batasi alat bawaan mana yang dapat digunakan Claude. Gunakan `""` untuk menonaktifkan semua, `"default"` untuk semua, atau nama alat seperti `"Bash,Edit,Read"`                                                                    | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Aktifkan logging verbose, menampilkan output putaran penuh                                                                                                                                                                         | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Keluarkan nomor versi                                                                                                                                                                                                              | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Mulai Claude dalam [git worktree](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) terisolasi di `<repo>/.claude/worktrees/<name>`. Jika tidak ada nama yang diberikan, satu akan dibuat secara otomatis | `claude -w feature-auth`                                                                           |

<Tip>
  Flag `--output-format json` sangat berguna untuk skrip dan
  otomasi, memungkinkan Anda mengurai respons Claude secara programatik.
</Tip>

### Format flag agents

Flag `--agents` menerima objek JSON yang mendefinisikan satu atau lebih subagents kustom. Setiap subagent memerlukan nama unik (sebagai kunci) dan objek definisi dengan bidang berikut:

| Bidang            | Diperlukan | Deskripsi                                                                                                                                                                                                                      |
| :---------------- | :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | Ya         | Deskripsi bahasa alami tentang kapan subagent harus dipanggil                                                                                                                                                                  |
| `prompt`          | Ya         | Prompt sistem yang memandu perilaku subagent                                                                                                                                                                                   |
| `tools`           | Tidak      | Array alat spesifik yang dapat digunakan subagent, misalnya `["Read", "Edit", "Bash"]`. Jika dihilangkan, mewarisi semua alat. Mendukung sintaks [`Agent(agent_type)`](/id/sub-agents#restrict-which-subagents-can-be-spawned) |
| `disallowedTools` | Tidak      | Array nama alat untuk secara eksplisit menolak untuk subagent ini                                                                                                                                                              |
| `model`           | Tidak      | Alias model untuk digunakan: `sonnet`, `opus`, `haiku`, atau `inherit`. Jika dihilangkan, default ke `inherit`                                                                                                                 |
| `skills`          | Tidak      | Array nama [skill](/id/skills) untuk dimuat sebelumnya ke dalam konteks subagent                                                                                                                                               |
| `mcpServers`      | Tidak      | Array [server MCP](/id/mcp) untuk subagent ini. Setiap entri adalah string nama server atau objek `{name: config}`                                                                                                             |
| `maxTurns`        | Tidak      | Jumlah maksimum putaran agentic sebelum subagent berhenti                                                                                                                                                                      |

Contoh:

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

Untuk detail lebih lanjut tentang membuat dan menggunakan subagents, lihat [dokumentasi subagents](/id/sub-agents).

### Flag prompt sistem

Claude Code menyediakan empat flag untuk menyesuaikan prompt sistem. Keempat flag bekerja dalam mode interaktif dan non-interaktif.

| Flag                          | Perilaku                                      | Kasus penggunaan                                                                |
| :---------------------------- | :-------------------------------------------- | :------------------------------------------------------------------------------ |
| `--system-prompt`             | **Mengganti** seluruh prompt default          | Kontrol lengkap atas perilaku dan instruksi Claude                              |
| `--system-prompt-file`        | **Mengganti** dengan konten file              | Muat prompt dari file untuk reproduksibilitas dan kontrol versi                 |
| `--append-system-prompt`      | **Menambahkan** ke prompt default             | Tambahkan instruksi spesifik sambil mempertahankan perilaku Claude Code default |
| `--append-system-prompt-file` | **Menambahkan** konten file ke prompt default | Muat instruksi tambahan dari file sambil mempertahankan default                 |

**Kapan menggunakan masing-masing:**

* **`--system-prompt`**: gunakan ketika Anda memerlukan kontrol lengkap atas prompt sistem Claude. Ini menghapus semua instruksi Claude Code default, memberikan Anda kanvas kosong.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: gunakan ketika Anda ingin memuat prompt kustom dari file, berguna untuk konsistensi tim atau template prompt yang dikontrol versi.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: gunakan ketika Anda ingin menambahkan instruksi spesifik sambil mempertahankan kemampuan default Claude Code. Ini adalah opsi paling aman untuk sebagian besar kasus penggunaan.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: gunakan ketika Anda ingin menambahkan instruksi dari file sambil mempertahankan default Claude Code. Berguna untuk penambahan yang dikontrol versi.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` dan `--system-prompt-file` saling eksklusif. Flag append dapat digunakan bersama dengan flag penggantian apa pun.

Untuk sebagian besar kasus penggunaan, `--append-system-prompt` atau `--append-system-prompt-file` direkomendasikan karena mereka mempertahankan kemampuan bawaan Claude Code sambil menambahkan persyaratan kustom Anda. Gunakan `--system-prompt` atau `--system-prompt-file` hanya ketika Anda memerlukan kontrol lengkap atas prompt sistem.

## Lihat juga

* [Ekstensi Chrome](/id/chrome) - Otomasi browser dan pengujian web
* [Mode interaktif](/id/interactive-mode) - Pintasan, mode input, dan fitur interaktif
* [Panduan quickstart](/id/quickstart) - Memulai dengan Claude Code
* [Alur kerja umum](/id/common-workflows) - Alur kerja dan pola lanjutan
* [Pengaturan](/id/settings) - Opsi konfigurasi
* [Dokumentasi Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) - Penggunaan programatik dan integrasi
