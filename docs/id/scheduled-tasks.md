> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Jalankan prompt sesuai jadwal

> Gunakan /loop dan alat penjadwalan cron untuk menjalankan prompt berulang kali, polling status, atau mengatur pengingat sekali jalan dalam sesi Claude Code.

<Note>
  Tugas terjadwal memerlukan Claude Code v2.1.72 atau lebih baru. Periksa versi Anda dengan `claude --version`.
</Note>

Tugas terjadwal memungkinkan Claude menjalankan kembali prompt secara otomatis pada interval tertentu. Gunakan untuk polling deployment, mengawasi PR, memeriksa build yang berjalan lama, atau mengingatkan diri sendiri untuk melakukan sesuatu nanti dalam sesi. Untuk bereaksi terhadap peristiwa saat terjadi daripada polling, lihat [Channels](/id/channels): CI Anda dapat mendorong kegagalan ke dalam sesi secara langsung.

Tugas bersifat session-scoped: mereka hidup dalam proses Claude Code saat ini dan hilang saat Anda keluar. Untuk penjadwalan yang tahan lama yang bertahan setelah restart, gunakan [Routines](/id/routines), [Desktop scheduled tasks](/id/desktop-scheduled-tasks), atau [GitHub Actions](/id/github-actions).

## Bandingkan opsi penjadwalan

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Jalankan prompt berulang dengan /loop

Skill `/loop` [bundled skill](/id/commands) adalah cara tercepat untuk menjalankan prompt berulang sementara sesi tetap terbuka. Baik interval maupun prompt bersifat opsional, dan apa yang Anda berikan menentukan bagaimana loop berperilaku.

| Apa yang Anda berikan                  | Contoh                      | Apa yang terjadi                                                                                          |
| :------------------------------------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------- |
| Interval dan prompt                    | `/loop 5m check the deploy` | Prompt Anda berjalan pada [jadwal tetap](#run-on-a-fixed-interval)                                        |
| Hanya prompt                           | `/loop check the deploy`    | Prompt Anda berjalan pada [interval yang dipilih Claude](#let-claude-choose-the-interval) setiap iterasi  |
| Hanya interval, atau tidak ada apa-apa | `/loop`                     | [Prompt pemeliharaan bawaan](#run-the-built-in-maintenance-prompt) berjalan, atau `loop.md` Anda jika ada |

Anda juga dapat melewatkan perintah lain sebagai prompt, misalnya `/loop 20m /review-pr 1234`, untuk menjalankan kembali workflow yang sudah dikemas setiap iterasi.

### Jalankan pada interval tetap

Ketika Anda memberikan interval, Claude mengonversinya ke ekspresi cron, menjadwalkan job, dan mengonfirmasi cadence dan ID job.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Interval dapat memimpin prompt sebagai token bare seperti `30m`, atau mengikutinya sebagai klausa seperti `every 2 hours`. Unit yang didukung adalah `s` untuk detik, `m` untuk menit, `h` untuk jam, dan `d` untuk hari.

Detik dibulatkan ke menit terdekat karena cron memiliki granularitas satu menit. Interval yang tidak memetakan ke langkah cron yang bersih, seperti `7m` atau `90m`, dibulatkan ke interval terdekat yang bersih dan Claude memberi tahu Anda apa yang dipilihnya.

### Biarkan Claude memilih interval

Ketika Anda menghilangkan interval, Claude memilih satu secara dinamis daripada berjalan pada jadwal cron tetap. Setelah setiap iterasi, Claude memilih penundaan antara satu menit dan satu jam berdasarkan apa yang diamatinya: menunggu pendek saat build selesai atau PR aktif, menunggu lebih lama ketika tidak ada yang tertunda. Penundaan yang dipilih dan alasan untuk itu dicetak di akhir setiap iterasi.

Contoh di bawah memeriksa CI dan komentar review, dengan Claude menunggu lebih lama di antara iterasi setelah PR menjadi tenang:

```text theme={null}
/loop check whether CI passed and address any review comments
```

Ketika Anda meminta jadwal `/loop` dinamis, Claude dapat menggunakan [Monitor tool](/id/tools-reference#monitor-tool) secara langsung. Monitor menjalankan skrip latar belakang dan mengalirkan setiap baris output kembali, yang menghindari polling sama sekali dan sering lebih efisien token dan responsif daripada menjalankan kembali prompt pada interval.

Loop yang dijadwalkan secara dinamis muncul dalam [daftar tugas terjadwal](#manage-scheduled-tasks) Anda seperti tugas lainnya, jadi Anda dapat membuat daftar atau membatalkannya dengan cara yang sama. Aturan [jitter](#jitter) tidak berlaku untuk itu, tetapi [kedaluwarsa tujuh hari](#seven-day-expiry) berlaku: loop berakhir secara otomatis tujuh hari setelah Anda memulainya.

<Note>
  Di Bedrock, Vertex AI, dan Microsoft Foundry, prompt tanpa interval berjalan pada jadwal tetap 10 menit sebagai gantinya.
</Note>

### Jalankan prompt pemeliharaan bawaan

Ketika Anda menghilangkan prompt, Claude menggunakan prompt pemeliharaan bawaan daripada yang Anda berikan. Pada setiap iterasi, Claude bekerja melalui hal-hal berikut, secara berurutan:

* lanjutkan pekerjaan yang belum selesai dari percakapan
* urus pull request cabang saat ini: komentar review, CI runs yang gagal, merge conflicts
* jalankan pass pembersihan seperti bug hunts atau simplification ketika tidak ada yang tertunda

Claude tidak memulai inisiatif baru di luar cakupan itu, dan tindakan yang tidak dapat diubah seperti pushing atau deleting hanya dilanjutkan ketika mereka melanjutkan sesuatu yang sudah diotorisasi transkrip.

```text theme={null}
/loop
```

Bare `/loop` menjalankan prompt ini pada [interval yang dipilih secara dinamis](#let-claude-choose-the-interval). Tambahkan interval, misalnya `/loop 15m`, untuk menjalankannya pada jadwal tetap sebagai gantinya. Untuk mengganti prompt bawaan dengan prompt default Anda sendiri, lihat [Customize the default prompt with loop.md](#customize-the-default-prompt-with-loop-md).

<Note>
  Di Bedrock, Vertex AI, dan Microsoft Foundry, `/loop` tanpa prompt mencetak pesan penggunaan daripada memulai loop pemeliharaan.
</Note>

### Sesuaikan prompt default dengan loop.md

File `loop.md` mengganti prompt pemeliharaan bawaan dengan instruksi Anda sendiri. File ini mendefinisikan satu prompt default tunggal untuk bare `/loop`, bukan daftar tugas terjadwal terpisah, dan diabaikan setiap kali Anda memberikan prompt pada baris perintah. Untuk menjadwalkan prompt tambahan bersama dengannya, gunakan `/loop <prompt>` atau [minta Claude secara langsung](#manage-scheduled-tasks).

Claude mencari file di dua lokasi dan menggunakan yang pertama ditemukannya.

| Path                | Scope                                                                             |
| :------------------ | :-------------------------------------------------------------------------------- |
| `.claude/loop.md`   | Project-level. Mengambil prioritas ketika kedua file ada.                         |
| `~/.claude/loop.md` | User-level. Berlaku di proyek apa pun yang tidak mendefinisikan miliknya sendiri. |

File adalah Markdown biasa tanpa struktur yang diperlukan. Tulislah seolah-olah Anda mengetik prompt `/loop` secara langsung. Contoh berikut menjaga cabang rilis tetap sehat:

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

Edit ke `loop.md` berlaku pada iterasi berikutnya, jadi Anda dapat menyempurnakan instruksi saat loop berjalan. Ketika tidak ada `loop.md` yang ada di lokasi mana pun, loop kembali ke prompt pemeliharaan bawaan. Jaga file tetap ringkas: konten di luar 25.000 byte dipotong.

## Atur pengingat sekali jalan

Untuk pengingat sekali jalan, jelaskan apa yang Anda inginkan dalam bahasa alami daripada menggunakan `/loop`. Claude menjadwalkan tugas single-fire yang menghapus dirinya sendiri setelah berjalan.

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude menyematkan waktu berjalan ke menit dan jam tertentu menggunakan ekspresi cron dan mengonfirmasi kapan akan berjalan.

## Kelola tugas terjadwal

Minta Claude dalam bahasa alami untuk membuat daftar atau membatalkan tugas, atau referensikan alat yang mendasarinya secara langsung.

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

Di balik layar, Claude menggunakan alat-alat ini:

| Alat         | Tujuan                                                                                                                       |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `CronCreate` | Jadwalkan tugas baru. Menerima ekspresi cron 5-field, prompt untuk dijalankan, dan apakah itu berulang atau berjalan sekali. |
| `CronList`   | Buat daftar semua tugas terjadwal dengan ID, jadwal, dan prompt mereka.                                                      |
| `CronDelete` | Batalkan tugas berdasarkan ID.                                                                                               |

Setiap tugas terjadwal memiliki ID 8-karakter yang dapat Anda berikan ke `CronDelete`. Sesi dapat menampung hingga 50 tugas terjadwal sekaligus.

## Bagaimana tugas terjadwal berjalan

Penjadwal memeriksa setiap detik untuk tugas yang jatuh tempo dan memasukkannya ke antrian dengan prioritas rendah. Prompt terjadwal berjalan di antara giliran Anda, bukan saat Claude sedang merespons. Jika Claude sibuk saat tugas jatuh tempo, prompt menunggu sampai giliran saat ini berakhir.

Semua waktu ditafsirkan dalam zona waktu lokal Anda. Ekspresi cron seperti `0 9 * * *` berarti 9am di mana pun Anda menjalankan Claude Code, bukan UTC.

### Jitter

Untuk menghindari setiap sesi mengenai API pada momen dinding jam yang sama, penjadwal menambahkan offset deterministik kecil untuk waktu berjalan:

* Tugas berulang berjalan hingga 10% dari periode mereka terlambat, dibatasi pada 15 menit. Job per jam mungkin berjalan di mana saja dari `:00` hingga `:06`.
* Tugas sekali jalan yang dijadwalkan untuk bagian atas atau bawah jam berjalan hingga 90 detik lebih awal.

Offset berasal dari ID tugas, jadi tugas yang sama selalu mendapatkan offset yang sama. Jika waktu yang tepat penting, pilih menit yang bukan `:00` atau `:30`, misalnya `3 9 * * *` daripada `0 9 * * *`, dan jitter sekali jalan tidak akan berlaku.

### Kedaluwarsa tujuh hari

Tugas berulang secara otomatis kedaluwarsa 7 hari setelah pembuatan. Tugas berjalan satu kali terakhir, kemudian menghapus dirinya sendiri. Ini membatasi berapa lama loop yang terlupakan dapat berjalan. Jika Anda memerlukan tugas berulang untuk bertahan lebih lama, batalkan dan buat ulang sebelum kedaluwarsa, atau gunakan [Routines](/id/routines) atau [Desktop scheduled tasks](/id/desktop-scheduled-tasks) untuk penjadwalan yang tahan lama.

## Referensi ekspresi cron

`CronCreate` menerima ekspresi cron standar 5-field: `minute hour day-of-month month day-of-week`. Semua field mendukung wildcard (`*`), nilai tunggal (`5`), langkah (`*/15`), rentang (`1-5`), dan daftar yang dipisahkan koma (`1,15,30`).

| Contoh         | Arti                              |
| :------------- | :-------------------------------- |
| `*/5 * * * *`  | Setiap 5 menit                    |
| `0 * * * *`    | Setiap jam pada jam               |
| `7 * * * *`    | Setiap jam pada 7 menit lewat     |
| `0 9 * * *`    | Setiap hari pada jam 9 pagi lokal |
| `0 9 * * 1-5`  | Hari kerja pada jam 9 pagi lokal  |
| `30 14 15 3 *` | 15 Maret pada jam 2:30 sore lokal |

Day-of-week menggunakan `0` atau `7` untuk Minggu hingga `6` untuk Sabtu. Sintaks yang diperluas seperti `L`, `W`, `?`, dan alias nama seperti `MON` atau `JAN` tidak didukung.

Ketika day-of-month dan day-of-week keduanya dibatasi, tanggal cocok jika salah satu field cocok. Ini mengikuti semantik vixie-cron standar.

## Nonaktifkan tugas terjadwal

Atur `CLAUDE_CODE_DISABLE_CRON=1` di lingkungan Anda untuk menonaktifkan penjadwal sepenuhnya. Alat cron dan `/loop` menjadi tidak tersedia, dan tugas yang sudah terjadwal berhenti berjalan. Lihat [Environment variables](/id/env-vars) untuk daftar lengkap flag disable.

## Keterbatasan

Penjadwalan session-scoped memiliki batasan yang melekat:

* Tugas hanya berjalan saat Claude Code berjalan dan idle. Menutup terminal atau membiarkan sesi keluar membatalkan semuanya.
* Tidak ada catch-up untuk fire yang terlewat. Jika waktu terjadwal tugas berlalu saat Claude sibuk dengan permintaan yang berjalan lama, itu berjalan sekali saat Claude menjadi idle, bukan sekali per interval yang terlewat.
* Tidak ada persistensi di seluruh restart. Memulai ulang Claude Code menghapus semua tugas session-scoped.

Untuk otomasi yang didorong cron yang perlu berjalan tanpa pengawasan:

* [Routines](/id/routines): berjalan pada infrastruktur yang dikelola Anthropic pada jadwal, melalui panggilan API, atau pada peristiwa GitHub
* [GitHub Actions](/id/github-actions): gunakan trigger `schedule` dalam CI
* [Desktop scheduled tasks](/id/desktop-scheduled-tasks): berjalan secara lokal di mesin Anda
