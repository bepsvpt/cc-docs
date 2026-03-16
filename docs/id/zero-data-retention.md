> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Retensi data nol

> Pelajari tentang Zero Data Retention (ZDR) untuk Claude Code di Claude for Enterprise, termasuk cakupan, fitur yang dinonaktifkan, dan cara meminta pengaktifan.

Zero Data Retention (ZDR) tersedia untuk Claude Code ketika digunakan melalui Claude for Enterprise. Ketika ZDR diaktifkan, prompt dan respons model yang dihasilkan selama sesi Claude Code diproses secara real-time dan tidak disimpan oleh Anthropic setelah respons dikembalikan, kecuali jika diperlukan untuk mematuhi hukum atau memerangi penyalahgunaan.

ZDR di Claude for Enterprise memberikan pelanggan enterprise kemampuan untuk menggunakan Claude Code dengan retensi data nol dan mengakses kemampuan administratif:

* Kontrol biaya per pengguna
* Dashboard [Analytics](/id/analytics)
* [Server-managed settings](/id/server-managed-settings)
* Audit logs

ZDR untuk Claude Code di Claude for Enterprise hanya berlaku untuk platform langsung Anthropic. Untuk penerapan Claude di AWS Bedrock, Google Vertex AI, atau Microsoft Foundry, lihat kebijakan retensi data platform tersebut.

## Cakupan ZDR

ZDR mencakup inferensi Claude Code di Claude for Enterprise.

<Warning>
  ZDR diaktifkan berdasarkan per-organisasi. Setiap organisasi baru memerlukan ZDR untuk diaktifkan secara terpisah oleh tim akun Anthropic Anda. ZDR tidak secara otomatis berlaku untuk organisasi baru yang dibuat di bawah akun yang sama. Hubungi tim akun Anda untuk mengaktifkan ZDR untuk organisasi baru apa pun.
</Warning>

### Apa yang dicakup ZDR

ZDR mencakup panggilan inferensi model yang dilakukan melalui Claude Code di Claude for Enterprise. Ketika Anda menggunakan Claude Code di terminal Anda, prompt yang Anda kirim dan respons yang dihasilkan Claude tidak disimpan oleh Anthropic. Ini berlaku terlepas dari model Claude mana yang digunakan.

### Apa yang tidak dicakup ZDR

ZDR tidak berlaku untuk hal-hal berikut, bahkan untuk organisasi dengan ZDR diaktifkan. Fitur-fitur ini mengikuti [kebijakan retensi data standar](/id/data-usage#data-retention):

| Fitur                        | Detail                                                                                                                                                                                                                                                             |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Chat di claude.ai            | Percakapan chat melalui antarmuka web Claude for Enterprise tidak dicakup oleh ZDR.                                                                                                                                                                                |
| Cowork                       | Sesi Cowork tidak dicakup oleh ZDR.                                                                                                                                                                                                                                |
| Claude Code Analytics        | Tidak menyimpan prompt atau respons model, tetapi mengumpulkan metadata produktivitas seperti email akun dan statistik penggunaan. Metrik kontribusi tidak tersedia untuk organisasi ZDR; [dashboard analytics](/id/analytics) menampilkan metrik penggunaan saja. |
| Manajemen pengguna dan kursi | Data administratif seperti email akun dan penugasan kursi disimpan di bawah kebijakan standar.                                                                                                                                                                     |
| Integrasi pihak ketiga       | Data yang diproses oleh alat pihak ketiga, MCP servers, atau integrasi eksternal lainnya tidak dicakup oleh ZDR. Tinjau praktik penanganan data layanan tersebut secara independen.                                                                                |

## Fitur yang dinonaktifkan di bawah ZDR

Ketika ZDR diaktifkan untuk organisasi Claude Code di Claude for Enterprise, fitur-fitur tertentu yang memerlukan penyimpanan prompt atau completion secara otomatis dinonaktifkan di tingkat backend:

| Fitur                                                                | Alasan                                                              |
| -------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [Claude Code di Web](/id/claude-code-on-the-web)                     | Memerlukan penyimpanan percakapan di sisi server.                   |
| [Remote sessions](/id/desktop#remote-sessions) dari aplikasi Desktop | Memerlukan data sesi persisten yang mencakup prompt dan completion. |
| Pengiriman umpan balik (`/feedback`)                                 | Mengirimkan umpan balik mengirimkan data percakapan ke Anthropic.   |

Fitur-fitur ini diblokir di backend terlepas dari tampilan sisi klien. Jika Anda melihat fitur yang dinonaktifkan di terminal Claude Code selama startup, mencoba menggunakannya mengembalikan kesalahan yang menunjukkan kebijakan organisasi tidak memungkinkan tindakan tersebut.

Fitur-fitur di masa depan juga dapat dinonaktifkan jika memerlukan penyimpanan prompt atau completion.

## Retensi data untuk pelanggaran kebijakan

Bahkan dengan ZDR diaktifkan, Anthropic dapat menyimpan data jika diperlukan oleh hukum atau untuk mengatasi pelanggaran Usage Policy. Jika sesi ditandai untuk pelanggaran kebijakan, Anthropic dapat menyimpan input dan output terkait selama hingga 2 tahun, konsisten dengan kebijakan ZDR standar Anthropic.

## Minta ZDR

Untuk meminta ZDR untuk Claude Code di Claude for Enterprise, hubungi tim akun Anthropic Anda. Tim akun Anda akan mengirimkan permintaan secara internal, dan Anthropic akan meninjau dan mengaktifkan ZDR di organisasi Anda setelah mengkonfirmasi kelayakan. Semua tindakan pengaktifan dicatat dalam audit log.

Jika Anda saat ini menggunakan ZDR untuk Claude Code melalui kunci API pay-as-you-go, Anda dapat beralih ke Claude for Enterprise untuk mendapatkan akses ke fitur administratif sambil mempertahankan ZDR untuk Claude Code. Hubungi tim akun Anda untuk mengoordinasikan migrasi.
