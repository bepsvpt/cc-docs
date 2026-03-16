> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Jalankan prompt sesuai jadwal

> Gunakan /loop dan alat penjadwalan cron untuk menjalankan prompt berulang kali, polling status, atau mengatur pengingat sekali jalan dalam sesi Claude Code.

<Note>
  Tugas terjadwal memerlukan Claude Code v2.1.72 atau lebih baru. Periksa versi Anda dengan `claude --version`.
</Note>

Tugas terjadwal memungkinkan Claude menjalankan kembali prompt secara otomatis pada interval tertentu. Gunakan untuk polling deployment, mengawasi PR, memeriksa build yang berjalan lama, atau mengingatkan diri sendiri untuk melakukan sesuatu nanti dalam sesi.

Tugas bersifat session-scoped: mereka hidup dalam proses Claude Code saat ini dan hilang saat Anda keluar. Untuk penjadwalan yang tahan lama yang bertahan setelah restart dan berjalan tanpa sesi terminal aktif, lihat [Desktop scheduled tasks](/id/desktop#schedule-recurring-tasks) atau [GitHub Actions](/id/github-actions).

## Jadwalkan prompt berulang dengan /loop

Skill `/loop` [bundled skill](/id/skills#bundled-skills) adalah cara tercepat untuk menjadwalkan prompt berulang. Berikan interval opsional dan prompt, dan Claude menyiapkan pekerjaan cron yang berjalan di latar belakang sementara sesi tetap terbuka.

```text  theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude mengurai interval, mengonversinya ke ekspresi cron, menjadwalkan pekerjaan, dan mengonfirmasi cadence dan ID pekerjaan.

### Sintaks interval

Interval bersifat opsional. Anda dapat memimpinnya, mengikutinya, atau meninggalkannya sepenuhnya.

| Form                       | Contoh                                | Interval yang diurai    |
| :------------------------- | :------------------------------------ | :---------------------- |
| Token terdepan             | `/loop 30m check the build`           | setiap 30 menit         |
| Klausa `every` di belakang | `/loop check the build every 2 hours` | setiap 2 jam            |
| Tidak ada interval         | `/loop check the build`               | default setiap 10 menit |

Unit yang didukung adalah `s` untuk detik, `m` untuk menit, `h` untuk jam, dan `d` untuk hari. Detik dibulatkan ke menit terdekat karena cron memiliki granularitas satu menit. Interval yang tidak terbagi rata ke dalam unit mereka, seperti `7m` atau `90m`, dibulatkan ke interval yang bersih terdekat dan Claude memberi tahu Anda apa yang dipilihnya.

### Loop di atas perintah lain

Prompt terjadwal itu sendiri dapat berupa invokasi perintah atau skill. Ini berguna untuk menjalankan kembali alur kerja yang telah Anda paket.

```text  theme={null}
/loop 20m /review-pr 1234
```

Setiap kali pekerjaan berjalan, Claude menjalankan `/review-pr 1234` seolah-olah Anda telah mengetiknya.

## Atur pengingat sekali jalan

Untuk pengingat sekali jalan, jelaskan apa yang Anda inginkan dalam bahasa alami daripada menggunakan `/loop`. Claude menjadwalkan tugas single-fire yang menghapus dirinya sendiri setelah berjalan.

```text  theme={null}
remind me at 3pm to push the release branch
```

```text  theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude menyematkan waktu api ke menit dan jam tertentu menggunakan ekspresi cron dan mengonfirmasi kapan akan berjalan.

## Kelola tugas terjadwal

Minta Claude dalam bahasa alami untuk membuat daftar atau membatalkan tugas, atau referensikan alat yang mendasarinya secara langsung.

```text  theme={null}
what scheduled tasks do I have?
```

```text  theme={null}
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

Untuk menghindari setiap sesi mengenai API pada momen dinding jam yang sama, penjadwal menambahkan offset deterministik kecil untuk waktu api:

* Tugas berulang berjalan hingga 10% dari periode mereka terlambat, dibatasi pada 15 menit. Pekerjaan per jam mungkin berjalan di mana saja dari `:00` hingga `:06`.
* Tugas sekali jalan yang dijadwalkan untuk bagian atas atau bawah jam berjalan hingga 90 detik lebih awal.

Offset berasal dari ID tugas, jadi tugas yang sama selalu mendapatkan offset yang sama. Jika waktu yang tepat penting, pilih menit yang bukan `:00` atau `:30`, misalnya `3 9 * * *` daripada `0 9 * * *`, dan jitter sekali jalan tidak akan berlaku.

### Kedaluwarsa tiga hari

Tugas berulang secara otomatis kedaluwarsa 3 hari setelah pembuatan. Tugas berjalan satu kali terakhir, kemudian menghapus dirinya sendiri. Ini membatasi berapa lama loop yang terlupakan dapat berjalan. Jika Anda memerlukan tugas berulang untuk bertahan lebih lama, batalkan dan buat ulang sebelum kedaluwarsa, atau gunakan [Desktop scheduled tasks](/id/desktop#schedule-recurring-tasks) untuk penjadwalan yang tahan lama.

## Referensi ekspresi cron

`CronCreate` menerima ekspresi cron 5-field standar: `minute hour day-of-month month day-of-week`. Semua field mendukung wildcard (`*`), nilai tunggal (`5`), langkah (`*/15`), rentang (`1-5`), dan daftar yang dipisahkan koma (`1,15,30`).

| Contoh         | Arti                              |
| :------------- | :-------------------------------- |
| `*/5 * * * *`  | Setiap 5 menit                    |
| `0 * * * *`    | Setiap jam pada jam               |
| `7 * * * *`    | Setiap jam pada 7 menit lewat     |
| `0 9 * * *`    | Setiap hari pada jam 9 pagi lokal |
| `0 9 * * 1-5`  | Hari kerja pada jam 9 pagi lokal  |
| `30 14 15 3 *` | 15 Maret pada jam 2:30 sore lokal |

Day-of-week menggunakan `0` atau `7` untuk Minggu hingga `6` untuk Sabtu. Sintaks yang diperluas seperti `L`, `W`, `?`, dan alias nama seperti `MON` atau `JAN` tidak didukung.

Ketika hari-bulan dan hari-minggu keduanya dibatasi, tanggal cocok jika salah satu field cocok. Ini mengikuti semantik vixie-cron standar.

## Nonaktifkan tugas terjadwal

Atur `CLAUDE_CODE_DISABLE_CRON=1` di lingkungan Anda untuk menonaktifkan penjadwal sepenuhnya. Alat cron dan `/loop` menjadi tidak tersedia, dan tugas yang sudah terjadwal berhenti berjalan. Lihat [Environment variables](/id/settings#environment-variables) untuk daftar lengkap flag disable.

## Keterbatasan

Penjadwalan session-scoped memiliki batasan yang melekat:

* Tugas hanya berjalan saat Claude Code berjalan dan idle. Menutup terminal atau membiarkan sesi keluar membatalkan semuanya.
* Tidak ada catch-up untuk api yang terlewat. Jika waktu terjadwal tugas berlalu saat Claude sibuk dengan permintaan yang berjalan lama, itu berjalan sekali saat Claude menjadi idle, bukan sekali per interval yang terlewat.
* Tidak ada persistensi di seluruh restart. Memulai ulang Claude Code menghapus semua tugas session-scoped.

Untuk otomasi yang didorong cron yang perlu berjalan tanpa pengawasan, gunakan [GitHub Actions workflow](/id/github-actions) dengan pemicu `schedule`, atau [Desktop scheduled tasks](/id/desktop#schedule-recurring-tasks) jika Anda menginginkan alur pengaturan grafis.
