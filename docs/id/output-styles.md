> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Output styles

> Sesuaikan Claude Code untuk penggunaan di luar rekayasa perangkat lunak

Output styles mengubah cara Claude merespons, bukan apa yang Claude ketahui. Mereka memodifikasi system prompt untuk menetapkan peran, nada, dan format output sambil mempertahankan kemampuan inti seperti menjalankan skrip, membaca dan menulis file, serta melacak TODOs. Gunakan satu ketika Anda terus-menerus meminta kembali untuk suara atau format yang sama setiap giliran, atau ketika Anda ingin Claude bertindak sebagai sesuatu selain seorang insinyur perangkat lunak.

Untuk instruksi tentang proyek, konvensi, atau codebase Anda, gunakan [CLAUDE.md](/id/memory) sebagai gantinya.

## Gaya output bawaan

Gaya output **Default** Claude Code adalah system prompt yang ada, dirancang
untuk membantu Anda menyelesaikan tugas-tugas rekayasa perangkat lunak secara efisien.

Ada tiga gaya output bawaan tambahan:

* **Proactive**: Claude dieksekusi segera, membuat asumsi yang masuk akal
  alih-alih berhenti untuk keputusan rutin, dan lebih memilih tindakan daripada perencanaan.
  Ini menerapkan panduan yang sama seperti
  [mode otomatis](/id/permission-modes#eliminate-prompts-with-auto-mode) tanpa
  mengubah mode izin Anda, jadi Anda masih melihat prompt izin sebelum
  alat dijalankan.

* **Explanatory**: Menyediakan "Insights" edukatif di antara membantu Anda
  menyelesaikan tugas-tugas rekayasa perangkat lunak. Membantu Anda memahami
  pilihan implementasi dan pola codebase.

* **Learning**: Mode kolaboratif belajar-dengan-melakukan di mana Claude tidak hanya
  akan berbagi "Insights" saat coding, tetapi juga meminta Anda untuk berkontribusi dengan
  potongan kode kecil dan strategis sendiri. Claude Code akan menambahkan penanda `TODO(human)` dalam kode Anda
  untuk Anda implementasikan.

## Cara kerja output styles

Output styles secara langsung memodifikasi system prompt Claude Code.

* Custom output styles mengecualikan instruksi untuk coding (seperti memverifikasi kode
  dengan tes), kecuali `keep-coding-instructions` bernilai true.
* Semua output styles memiliki instruksi kustom mereka sendiri yang ditambahkan ke akhir
  system prompt.
* Semua output styles memicu pengingat bagi Claude untuk mematuhi instruksi output style
  selama percakapan.

Penggunaan token tergantung pada style. Menambahkan instruksi ke system prompt
meningkatkan input tokens, meskipun prompt caching mengurangi biaya ini setelah permintaan pertama
dalam sesi. Built-in Explanatory dan Learning styles menghasilkan respons yang lebih panjang
daripada Default secara desain, yang meningkatkan output tokens. Untuk custom styles,
penggunaan output tokens tergantung pada apa yang instruksi Anda katakan kepada Claude untuk diproduksi.

## Ubah output style Anda

Jalankan `/config` dan pilih **Output style** untuk memilih style dari menu. Pilihan Anda
disimpan ke `.claude/settings.local.json` di
[tingkat proyek lokal](/id/settings).

Untuk menetapkan style tanpa menu, edit field `outputStyle` secara langsung dalam
file settings:

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Karena output style ditetapkan dalam system prompt saat awal sesi,
perubahan berlaku saat Anda memulai sesi baru. Ini menjaga system
prompt tetap stabil sepanjang percakapan sehingga prompt caching dapat mengurangi latensi dan
biaya.

## Buat custom output style

Custom output styles adalah file Markdown dengan frontmatter dan teks yang akan
ditambahkan ke system prompt:

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

Anda dapat menyimpan file-file ini di tiga tingkat:

* User: `~/.claude/output-styles`
* Project: `.claude/output-styles`
* Managed policy: `.claude/output-styles` di dalam [direktori pengaturan terkelola](/id/settings#settings-files)

[Plugins](/id/plugins-reference) juga dapat mengirimkan output styles dalam direktori `output-styles/`.

### Frontmatter

File output style mendukung frontmatter untuk menentukan metadata:

| Frontmatter                | Tujuan                                                                                                                                                                                                                                                                      | Default                 |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------- |
| `name`                     | Nama output style, jika bukan nama file                                                                                                                                                                                                                                     | Mewarisi dari nama file |
| `description`              | Deskripsi output style, ditampilkan dalam picker `/config`                                                                                                                                                                                                                  | Tidak ada               |
| `keep-coding-instructions` | Apakah akan mempertahankan bagian-bagian dari system prompt Claude Code yang terkait dengan coding.                                                                                                                                                                         | false                   |
| `force-for-plugin`         | Plugin output styles hanya: terapkan style ini secara otomatis kapan pun plugin diaktifkan, tanpa memerlukan pengguna untuk memilihnya. Mengesampingkan pengaturan `outputStyle` pengguna. Jika beberapa plugin yang diaktifkan menetapkan ini, yang pertama dimuat menang. | false                   |

## Perbandingan dengan fitur terkait

### Output Styles vs. CLAUDE.md vs. --append-system-prompt

Output styles sepenuhnya "mematikan" bagian-bagian dari default system prompt Claude Code
yang spesifik untuk rekayasa perangkat lunak. Baik CLAUDE.md maupun
`--append-system-prompt` tidak mengedit default system prompt Claude Code. CLAUDE.md
menambahkan konten sebagai pesan pengguna *setelah* default system prompt Claude Code. `--append-system-prompt` menambahkan konten ke system prompt.

### Output Styles vs. [Agents](/id/sub-agents)

Output styles secara langsung mempengaruhi loop agen utama dan hanya mempengaruhi system
prompt. Agents dipanggil untuk menangani tugas-tugas spesifik dan dapat mencakup pengaturan tambahan
seperti model yang akan digunakan, tools yang tersedia bagi mereka, dan beberapa konteks
tentang kapan menggunakan agent.

### Output Styles vs. [Skills](/id/skills)

Output styles memodifikasi cara Claude merespons (pemformatan, nada, struktur) dan selalu aktif setelah dipilih. Skills adalah prompts khusus tugas yang Anda panggil dengan `/skill-name` atau yang Claude muat secara otomatis saat relevan. Gunakan output styles untuk preferensi pemformatan yang konsisten; gunakan skills untuk alur kerja dan tugas yang dapat digunakan kembali.
