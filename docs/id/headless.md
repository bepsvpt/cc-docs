> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Jalankan Claude Code secara programatis

> Gunakan Agent SDK untuk menjalankan Claude Code secara programatis dari CLI, Python, atau TypeScript.

<Note>
  Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from your interactive usage limits. See [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) for details.
</Note>

[Agent SDK](/id/agent-sdk/overview) memberikan Anda alat yang sama, loop agen, dan manajemen konteks yang mendukung Claude Code. Tersedia sebagai CLI untuk skrip dan CI/CD, atau sebagai paket [Python](/id/agent-sdk/python) dan [TypeScript](/id/agent-sdk/typescript) untuk kontrol programatis penuh.

Untuk menjalankan Claude Code dalam mode non-interaktif, berikan `-p` dengan prompt Anda dan [opsi CLI](/id/cli-reference) apa pun:

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Halaman ini mencakup penggunaan Agent SDK melalui CLI (`claude -p`). Untuk paket SDK Python dan TypeScript dengan output terstruktur, callback persetujuan alat, dan objek pesan asli, lihat [dokumentasi Agent SDK lengkap](/id/agent-sdk/overview).

## Penggunaan dasar

Tambahkan bendera `-p` (atau `--print`) ke perintah `claude` apa pun untuk menjalankannya secara non-interaktif. Semua [opsi CLI](/id/cli-reference) bekerja dengan `-p`, termasuk:

* `--continue` untuk [melanjutkan percakapan](#continue-conversations)
* `--allowedTools` untuk [persetujuan otomatis alat](#auto-approve-tools)
* `--output-format` untuk [output terstruktur](#get-structured-output)

Contoh ini menanyakan Claude tentang basis kode Anda dan mencetak respons:

```bash theme={null}
claude -p "What does the auth module do?"
```

### Mulai lebih cepat dengan bare mode

Tambahkan `--bare` untuk mengurangi waktu startup dengan melewati penemuan otomatis hooks, skills, plugins, server MCP, auto memory, dan CLAUDE.md. Tanpanya, `claude -p` memuat [konteks](/id/how-claude-code-works#the-context-window) yang sama dengan sesi interaktif, termasuk apa pun yang dikonfigurasi di direktori kerja atau `~/.claude`.

Bare mode berguna untuk CI dan skrip di mana Anda memerlukan hasil yang sama di setiap mesin. Hook di `~/.claude` rekan kerja atau server MCP di `.mcp.json` proyek tidak akan berjalan, karena bare mode tidak pernah membacanya. Hanya bendera yang Anda berikan secara eksplisit yang berlaku.

Contoh ini menjalankan tugas ringkasan sekali pakai dalam bare mode dan pra-menyetujui alat Read sehingga panggilan selesai tanpa prompt izin:

```bash theme={null}
claude --bare -p "Summarize this file" --allowedTools "Read"
```

Dalam bare mode Claude memiliki akses ke alat Bash, pembacaan file, dan pengeditan file. Berikan konteks apa pun yang Anda butuhkan dengan bendera:

| Untuk memuat             | Gunakan                                                 |
| ------------------------ | ------------------------------------------------------- |
| Penambahan prompt sistem | `--append-system-prompt`, `--append-system-prompt-file` |
| Pengaturan               | `--settings <file-or-json>`                             |
| Server MCP               | `--mcp-config <file-or-json>`                           |
| Agen kustom              | `--agents <json>`                                       |
| Plugin                   | `--plugin-dir <path>`, `--plugin-url <url>`             |

Bare mode melewati pembacaan OAuth dan keychain. Autentikasi Anthropic harus berasal dari `ANTHROPIC_API_KEY` atau `apiKeyHelper` dalam JSON yang diteruskan ke `--settings`. Bedrock, Vertex, dan Foundry menggunakan kredensial penyedia biasa mereka.

<Note>
  `--bare` adalah mode yang direkomendasikan untuk panggilan skrip dan SDK, dan akan menjadi default untuk `-p` di rilis mendatang.
</Note>

## Contoh

Contoh-contoh ini menyoroti pola CLI umum. Untuk CI dan panggilan skrip lainnya, tambahkan [`--bare`](#start-faster-with-bare-mode) sehingga mereka tidak mengambil apa pun yang kebetulan dikonfigurasi secara lokal.

### Saluran data melalui Claude

Mode non-interaktif membaca stdin, sehingga Anda dapat menyalurkan data dan mengarahkan respons keluar seperti alat baris perintah lainnya.

Contoh ini menyalurkan log build ke Claude dan menulis penjelasan ke file:

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

Dengan `--output-format json`, payload respons mencakup `total_cost_usd` dan rincian biaya per-model, sehingga pemanggil skrip dapat melacak pengeluaran per invokasi tanpa berkonsultasi dengan [dashboard penggunaan](/id/costs).

<Note>
  Sejak Claude Code v2.1.128, stdin yang disalurkan dibatasi pada 10MB. Jika Anda melampaui batas, Claude Code keluar dengan kesalahan yang jelas dan status bukan nol. Untuk bekerja dengan input yang lebih besar, tulis konten ke file dan referensikan jalur file dalam prompt Anda alih-alih menyalurkannya.
</Note>

### Tambahkan Claude ke skrip build

Anda dapat membungkus panggilan non-interaktif dalam skrip untuk menggunakan Claude sebagai linter atau reviewer khusus proyek.

Skrip `package.json` ini menyalurkan diff terhadap `main` ke Claude dan memintanya untuk melaporkan typo. Menyalurkan diff berarti Claude tidak memerlukan izin Bash untuk membacanya, dan tanda kutip ganda yang di-escape menjaga skrip portabel ke Windows:

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### Dapatkan output terstruktur

Gunakan `--output-format` untuk mengontrol bagaimana respons dikembalikan:

* `text` (default): output teks biasa
* `json`: JSON terstruktur dengan hasil, ID sesi, dan metadata
* `stream-json`: JSON yang dibatasi baris baru untuk streaming real-time

Contoh ini mengembalikan ringkasan proyek sebagai JSON dengan metadata sesi, dengan hasil teks di bidang `result`:

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

Untuk mendapatkan output yang sesuai dengan skema tertentu, gunakan `--output-format json` dengan `--json-schema` dan definisi [JSON Schema](https://json-schema.org/). Respons mencakup metadata tentang permintaan (ID sesi, penggunaan, dll.) dengan output terstruktur di bidang `structured_output`.

Contoh ini mengekstrak nama fungsi dan mengembalikannya sebagai array string:

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  Gunakan alat seperti [jq](https://jqlang.github.io/jq/) untuk mengurai respons dan mengekstrak bidang tertentu:

  ```bash theme={null}
  # Extract the text result
  claude -p "Summarize this project" --output-format json | jq -r '.result'

  # Extract structured output
  claude -p "Extract function names from auth.py" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
    | jq '.structured_output'
  ```
</Tip>

### Streaming respons

Gunakan `--output-format stream-json` dengan `--verbose` dan `--include-partial-messages` untuk menerima token saat dihasilkan. Setiap baris adalah objek JSON yang mewakili acara:

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

Contoh berikut menggunakan [jq](https://jqlang.github.io/jq/) untuk memfilter delta teks dan menampilkan hanya teks streaming. Bendera `-r` menampilkan string mentah (tanpa tanda kutip) dan `-j` bergabung tanpa baris baru sehingga token streaming terus menerus:

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Ketika permintaan API gagal dengan kesalahan yang dapat dicoba ulang, Claude Code memancarkan acara `system/api_retry` sebelum mencoba ulang. Anda dapat menggunakan ini untuk menampilkan kemajuan percobaan ulang atau menerapkan logika backoff kustom.

| Bidang           | Tipe              | Deskripsi                                                                                                                                                                                      |
| ---------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`           | `"system"`        | tipe pesan                                                                                                                                                                                     |
| `subtype`        | `"api_retry"`     | mengidentifikasi ini sebagai acara percobaan ulang                                                                                                                                             |
| `attempt`        | integer           | nomor percobaan saat ini, dimulai dari 1                                                                                                                                                       |
| `max_retries`    | integer           | total percobaan ulang yang diizinkan                                                                                                                                                           |
| `retry_delay_ms` | integer           | milidetik hingga percobaan berikutnya                                                                                                                                                          |
| `error_status`   | integer atau null | kode status HTTP, atau `null` untuk kesalahan koneksi tanpa respons HTTP                                                                                                                       |
| `error`          | string            | kategori kesalahan: `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `rate_limit`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, atau `unknown` |
| `uuid`           | string            | pengidentifikasi acara unik                                                                                                                                                                    |
| `session_id`     | string            | sesi yang dimiliki acara                                                                                                                                                                       |

Acara `system/init` melaporkan metadata sesi termasuk model, alat, server MCP, dan plugin yang dimuat. Ini adalah acara pertama dalam aliran kecuali [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/id/env-vars) diatur, dalam hal ini acara `plugin_install` mendahuluinya. Gunakan bidang plugin untuk gagal CI ketika plugin tidak dimuat:

| Bidang          | Tipe  | Deskripsi                                                                                                                                                                                                                                                                                                                              |
| --------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugins`       | array | plugin yang berhasil dimuat, masing-masing dengan `name` dan `path`                                                                                                                                                                                                                                                                    |
| `plugin_errors` | array | kesalahan waktu muat plugin, masing-masing dengan `plugin`, `type`, dan `message`. Mencakup versi dependensi yang tidak terpenuhi dan kegagalan muat `--plugin-dir` seperti jalur yang hilang atau arsip yang tidak valid. Plugin yang terpengaruh diturunkan dan tidak ada di `plugins`. Kunci dihilangkan ketika tidak ada kesalahan |

Ketika [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/id/env-vars) diatur, Claude Code memancarkan acara `system/plugin_install` saat plugin marketplace dipasang sebelum giliran pertama. Gunakan ini untuk menampilkan kemajuan pemasangan di UI Anda sendiri.

| Bidang       | Tipe                                                       | Deskripsi                                                                                                              |
| ------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `type`       | `"system"`                                                 | tipe pesan                                                                                                             |
| `subtype`    | `"plugin_install"`                                         | mengidentifikasi ini sebagai acara pemasangan plugin                                                                   |
| `status`     | `"started"`, `"installed"`, `"failed"`, atau `"completed"` | `started` dan `completed` membatasi pemasangan keseluruhan; `installed` dan `failed` melaporkan marketplace individual |
| `name`       | string, opsional                                           | nama marketplace, hadir pada `installed` dan `failed`                                                                  |
| `error`      | string, opsional                                           | pesan kegagalan, hadir pada `failed`                                                                                   |
| `uuid`       | string                                                     | pengidentifikasi acara unik                                                                                            |
| `session_id` | string                                                     | sesi yang dimiliki acara                                                                                               |

Untuk streaming programatis dengan callback dan objek pesan, lihat [Stream responses in real-time](/id/agent-sdk/streaming-output) dalam dokumentasi Agent SDK.

### Persetujuan otomatis alat

Gunakan `--allowedTools` untuk membiarkan Claude menggunakan alat tertentu tanpa meminta. Contoh ini menjalankan suite pengujian dan memperbaiki kegagalan, memungkinkan Claude untuk menjalankan perintah Bash dan membaca/mengedit file tanpa meminta izin:

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

Untuk menetapkan baseline untuk seluruh sesi alih-alih mencantumkan alat individual, berikan [mode izin](/id/permission-modes). `dontAsk` menolak apa pun yang tidak ada dalam aturan `permissions.allow` Anda atau [set perintah read-only](/id/permissions#read-only-commands), yang berguna untuk CI runs yang terkunci. `acceptEdits` memungkinkan Claude menulis file tanpa meminta dan juga persetujuan otomatis perintah filesystem umum seperti `mkdir`, `touch`, `mv`, dan `cp`. Perintah shell lainnya dan permintaan jaringan masih memerlukan entri `--allowedTools` atau aturan `permissions.allow`, jika tidak run akan berhenti ketika salah satu dicoba:

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### Buat komit

Contoh ini meninjau perubahan yang dipentaskan dan membuat komit dengan pesan yang sesuai:

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Bendera `--allowedTools` menggunakan [sintaks aturan izin](/id/settings#permission-rule-syntax). Spasi di akhir ` *` memungkinkan pencocokan awalan, jadi `Bash(git diff *)` memungkinkan perintah apa pun yang dimulai dengan `git diff`. Spasi sebelum `*` penting: tanpanya, `Bash(git diff*)` juga akan cocok dengan `git diff-index`.

<Note>
  [skills](/id/skills) yang dipanggil pengguna seperti `/commit` dan [perintah bawaan](/id/commands) hanya tersedia dalam mode interaktif. Dalam mode `-p`, jelaskan tugas yang ingin Anda capai.
</Note>

### Sesuaikan prompt sistem

Gunakan `--append-system-prompt` untuk menambahkan instruksi sambil mempertahankan perilaku default Claude Code. Contoh ini menyalurkan diff PR ke Claude dan menginstruksikannya untuk meninjau kerentanan keamanan:

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Lihat [system prompt flags](/id/cli-reference#system-prompt-flags) untuk opsi lebih lanjut termasuk `--system-prompt` untuk sepenuhnya mengganti prompt default.

### Lanjutkan percakapan

Gunakan `--continue` untuk melanjutkan percakapan terbaru, atau `--resume` dengan ID sesi untuk melanjutkan percakapan tertentu. Contoh ini menjalankan tinjauan, kemudian mengirim prompt tindak lanjut:

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Jika Anda menjalankan beberapa percakapan, tangkap ID sesi untuk melanjutkan percakapan tertentu:

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Langkah berikutnya

* [Agent SDK quickstart](/id/agent-sdk/quickstart): bangun agen pertama Anda dengan Python atau TypeScript
* [CLI reference](/id/cli-reference): semua bendera dan opsi CLI
* [GitHub Actions](/id/github-actions): gunakan Agent SDK dalam alur kerja GitHub
* [GitLab CI/CD](/id/gitlab-ci-cd): gunakan Agent SDK dalam pipeline GitLab
