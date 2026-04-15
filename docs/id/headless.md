> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Jalankan Claude Code secara programatis

> Gunakan Agent SDK untuk menjalankan Claude Code secara programatis dari CLI, Python, atau TypeScript.

[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) memberikan Anda alat yang sama, loop agen, dan manajemen konteks yang mendukung Claude Code. Tersedia sebagai CLI untuk skrip dan CI/CD, atau sebagai paket [Python](https://platform.claude.com/docs/en/agent-sdk/python) dan [TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript) untuk kontrol programatis penuh.

<Note>
  CLI sebelumnya disebut "headless mode." Bendera `-p` dan semua opsi CLI bekerja dengan cara yang sama.
</Note>

Untuk menjalankan Claude Code secara programatis dari CLI, berikan `-p` dengan prompt Anda dan [opsi CLI](/id/cli-reference) apa pun:

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Halaman ini mencakup penggunaan Agent SDK melalui CLI (`claude -p`). Untuk paket SDK Python dan TypeScript dengan output terstruktur, callback persetujuan alat, dan objek pesan asli, lihat [dokumentasi Agent SDK lengkap](https://platform.claude.com/docs/en/agent-sdk/overview).

## Penggunaan dasar

Tambahkan bendera `-p` (atau `--print`) ke perintah `claude` apa pun untuk menjalankannya secara non-interaktif. Semua [opsi CLI](/id/cli-reference) bekerja dengan `-p`, termasuk:

* `--continue` untuk [melanjutkan percakapan](#continue-conversations)
* `--allowedTools` untuk [persetujuan otomatis alat](#auto-approve-tools)
* `--output-format` untuk [output terstruktur](#get-structured-output)

Contoh ini menanyakan Claude tentang basis kode Anda dan mencetak respons:

```bash theme={null}
claude -p "What does the auth module do?"
```

## Contoh

Contoh-contoh ini menyoroti pola CLI umum.

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

Untuk streaming programatis dengan callback dan objek pesan, lihat [Stream responses in real-time](https://platform.claude.com/docs/en/agent-sdk/streaming-output) dalam dokumentasi Agent SDK.

### Persetujuan otomatis alat

Gunakan `--allowedTools` untuk membiarkan Claude menggunakan alat tertentu tanpa meminta. Contoh ini menjalankan suite pengujian dan memperbaiki kegagalan, memungkinkan Claude untuk menjalankan perintah Bash dan membaca/mengedit file tanpa meminta izin:

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
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

* [Agent SDK quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart): bangun agen pertama Anda dengan Python atau TypeScript
* [CLI reference](/id/cli-reference): semua bendera dan opsi CLI
* [GitHub Actions](/id/github-actions): gunakan Agent SDK dalam alur kerja GitHub
* [GitLab CI/CD](/id/gitlab-ci-cd): gunakan Agent SDK dalam pipeline GitLab
