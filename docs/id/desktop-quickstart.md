> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Memulai dengan aplikasi desktop

> Instal Claude Code di desktop dan mulai sesi coding pertama Anda

Aplikasi desktop memberi Anda Claude Code dengan antarmuka grafis: tinjauan diff visual, pratinjau aplikasi langsung, pemantauan GitHub PR dengan penggabungan otomatis, sesi paralel dengan isolasi Git worktree, tugas terjadwal, dan kemampuan untuk menjalankan tugas dari jarak jauh. Tidak perlu terminal.

Halaman ini memandu Anda melalui instalasi aplikasi dan memulai sesi pertama Anda. Jika Anda sudah siap, lihat [Gunakan Claude Code Desktop](/id/desktop) untuk referensi lengkap.

<Frame>
  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce" className="block dark:hidden" alt="Antarmuka Claude Code Desktop menampilkan tab Code yang dipilih, dengan kotak prompt, pemilih mode izin diatur ke Minta izin, pemilih model, pemilih folder, dan opsi Lingkungan Lokal" width="2500" height="1376" data-path="images/desktop-code-tab-light.png" />

  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8" className="hidden dark:block" alt="Antarmuka Claude Code Desktop dalam mode gelap menampilkan tab Code yang dipilih, dengan kotak prompt, pemilih mode izin diatur ke Minta izin, pemilih model, pemilih folder, dan opsi Lingkungan Lokal" width="2504" height="1374" data-path="images/desktop-code-tab-dark.png" />
</Frame>

Aplikasi desktop memiliki tiga tab:

* **Chat**: Percakapan umum tanpa akses file, mirip dengan claude.ai.
* **Cowork**: Agen latar belakang otonom yang bekerja pada tugas di VM cloud dengan lingkungannya sendiri. Dapat berjalan secara independen saat Anda melakukan pekerjaan lain.
* **Code**: Asisten coding interaktif dengan akses langsung ke file lokal Anda. Anda meninjau dan menyetujui setiap perubahan secara real-time.

Chat dan Cowork tercakup dalam [artikel dukungan Claude Desktop](https://support.claude.com/en/collections/16163169-claude-desktop). Halaman ini berfokus pada tab **Code**.

<Note>
  Claude Code memerlukan [langganan Pro, Max, Teams, atau Enterprise](https://claude.com/pricing).
</Note>

## Instal

<Steps>
  <Step title="Unduh aplikasi">
    Unduh Claude untuk platform Anda.

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Build universal untuk Intel dan Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Untuk prosesor x64
      </Card>
    </CardGroup>

    Untuk Windows ARM64, [unduh di sini](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

    Linux saat ini tidak didukung.
  </Step>

  <Step title="Masuk">
    Luncurkan Claude dari folder Aplikasi Anda (macOS) atau menu Start (Windows). Masuk dengan akun Anthropic Anda.
  </Step>

  <Step title="Buka tab Code">
    Klik tab **Code** di bagian atas tengah. Jika mengklik Code meminta Anda untuk upgrade, Anda perlu [berlangganan paket berbayar](https://claude.com/pricing) terlebih dahulu. Jika meminta Anda untuk masuk online, selesaikan masuk dan mulai ulang aplikasi. Jika Anda melihat kesalahan 403, lihat [pemecahan masalah autentikasi](/id/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

Aplikasi desktop menyertakan Claude Code. Anda tidak perlu menginstal Node.js atau CLI secara terpisah. Untuk menggunakan `claude` dari terminal, instal CLI secara terpisah. Lihat [Memulai dengan CLI](/id/quickstart).

## Mulai sesi pertama Anda

Dengan tab Code terbuka, pilih proyek dan beri Claude sesuatu untuk dikerjakan.

<Steps>
  <Step title="Pilih lingkungan dan folder">
    Pilih **Local** untuk menjalankan Claude di mesin Anda menggunakan file Anda secara langsung. Klik **Select folder** dan pilih direktori proyek Anda.

    <Tip>
      Mulai dengan proyek kecil yang Anda kenal dengan baik. Ini adalah cara tercepat untuk melihat apa yang dapat dilakukan Claude Code. Di Windows, [Git](https://git-scm.com/downloads/win) harus diinstal agar sesi lokal berfungsi. Sebagian besar Mac menyertakan Git secara default.
    </Tip>

    Anda juga dapat memilih:

    * **Remote**: Jalankan sesi pada infrastruktur cloud Anthropic yang berlanjut bahkan jika Anda menutup aplikasi. Sesi remote menggunakan infrastruktur yang sama dengan [Claude Code di web](/id/claude-code-on-the-web).
    * **SSH**: Terhubung ke mesin jarak jauh melalui SSH (server Anda sendiri, VM cloud, atau dev containers). Claude Code harus diinstal di mesin jarak jauh.
  </Step>

  <Step title="Pilih model">
    Pilih model dari dropdown di sebelah tombol kirim. Lihat [models](/id/model-config#available-models) untuk perbandingan Opus, Sonnet, dan Haiku. Anda tidak dapat mengubah model setelah sesi dimulai.
  </Step>

  <Step title="Beri tahu Claude apa yang harus dilakukan">
    Ketik apa yang ingin Anda lakukan Claude:

    * `Find a TODO comment and fix it`
    * `Add tests for the main function`
    * `Create a CLAUDE.md with instructions for this codebase`

    [Sesi](/id/desktop#work-in-parallel-with-sessions) adalah percakapan dengan Claude tentang kode Anda. Setiap sesi melacak konteks dan perubahannya sendiri, sehingga Anda dapat bekerja pada beberapa tugas tanpa saling mengganggu.
  </Step>

  <Step title="Tinjau dan terima perubahan">
    Secara default, tab Code dimulai dalam [mode Minta izin](/id/desktop#choose-a-permission-mode), di mana Claude mengusulkan perubahan dan menunggu persetujuan Anda sebelum menerapkannya. Anda akan melihat:

    1. [Tampilan diff](/id/desktop#review-changes-with-diff-view) menunjukkan dengan tepat apa yang akan berubah di setiap file
    2. Tombol Terima/Tolak untuk menyetujui atau menolak setiap perubahan
    3. Pembaruan real-time saat Claude menyelesaikan permintaan Anda

    Jika Anda menolak perubahan, Claude akan bertanya bagaimana Anda ingin melanjutkan dengan cara yang berbeda. File Anda tidak dimodifikasi sampai Anda menerima.
  </Step>
</Steps>

## Sekarang apa?

Anda telah membuat edit pertama Anda. Untuk referensi lengkap tentang semua yang dapat dilakukan Desktop, lihat [Gunakan Claude Code Desktop](/id/desktop). Berikut adalah beberapa hal yang dapat dicoba selanjutnya.

**Interupsi dan arahkan.** Anda dapat menghentikan Claude kapan saja. Jika itu menuju jalan yang salah, klik tombol stop atau ketik koreksi Anda dan tekan **Enter**. Claude berhenti melakukan apa yang sedang dilakukannya dan menyesuaikan berdasarkan input Anda. Anda tidak perlu menunggu sampai selesai atau memulai dari awal.

**Beri Claude lebih banyak konteks.** Ketik `@filename` di kotak prompt untuk menarik file tertentu ke dalam percakapan, lampirkan gambar dan PDF menggunakan tombol lampiran, atau seret dan lepas file langsung ke prompt. Semakin banyak konteks yang dimiliki Claude, semakin baik hasilnya. Lihat [Tambahkan file dan konteks](/id/desktop#add-files-and-context-to-prompts).

**Gunakan skills untuk tugas yang dapat diulang.** Ketik `/` atau klik **+** → **Slash commands** untuk menjelajahi [perintah bawaan](/id/interactive-mode#built-in-commands), [skills kustom](/id/skills), dan skills plugin. Skills adalah prompt yang dapat digunakan kembali yang dapat Anda panggil kapan pun Anda membutuhkannya, seperti daftar periksa tinjauan kode atau langkah penyebaran.

**Tinjau perubahan sebelum melakukan commit.** Setelah Claude mengedit file, indikator `+12 -1` muncul. Klik untuk membuka [tampilan diff](/id/desktop#review-changes-with-diff-view), tinjau modifikasi file demi file, dan beri komentar pada baris tertentu. Claude membaca komentar Anda dan merevisi. Klik **Review code** untuk membuat Claude mengevaluasi diff itu sendiri dan meninggalkan saran inline.

**Sesuaikan berapa banyak kontrol yang Anda miliki.** [Mode izin](/id/desktop#choose-a-permission-mode) Anda mengontrol keseimbangan. Minta izin (default) memerlukan persetujuan sebelum setiap edit. Auto accept edits secara otomatis menerima edit file untuk iterasi yang lebih cepat. Plan mode memungkinkan Claude memetakan pendekatan tanpa menyentuh file apa pun, yang berguna sebelum refactor besar.

**Tambahkan plugins untuk kemampuan lebih.** Klik tombol **+** di sebelah kotak prompt dan pilih **Plugins** untuk menjelajahi dan menginstal [plugins](/id/desktop#install-plugins) yang menambahkan skills, agents, MCP servers, dan lainnya.

**Pratinjau aplikasi Anda.** Klik dropdown **Preview** untuk menjalankan dev server Anda langsung di desktop. Claude dapat melihat aplikasi yang berjalan, menguji endpoint, memeriksa log, dan melakukan iterasi pada apa yang dilihatnya. Lihat [Pratinjau aplikasi Anda](/id/desktop#preview-your-app).

**Lacak pull request Anda.** Setelah membuka PR, Claude Code memantau hasil pemeriksaan CI dan dapat secara otomatis memperbaiki kegagalan atau menggabungkan PR setelah semua pemeriksaan lulus. Lihat [Pantau status pull request](/id/desktop#monitor-pull-request-status).

**Letakkan Claude pada jadwal.** Atur [tugas terjadwal](/id/desktop#schedule-recurring-tasks) untuk menjalankan Claude secara otomatis secara berulang: tinjauan kode harian setiap pagi, audit dependensi mingguan, atau briefing yang menarik dari alat yang terhubung.

**Skalakan ketika Anda siap.** Buka [sesi paralel](/id/desktop#work-in-parallel-with-sessions) dari sidebar untuk bekerja pada beberapa tugas sekaligus, masing-masing di Git worktree-nya sendiri. Kirim [pekerjaan jangka panjang ke cloud](/id/desktop#run-long-running-tasks-remotely) sehingga terus berlanjut bahkan jika Anda menutup aplikasi, atau [lanjutkan sesi di web atau di IDE Anda](/id/desktop#continue-in-another-surface) jika tugas memakan waktu lebih lama dari yang diharapkan. [Hubungkan alat eksternal](/id/desktop#extend-claude-code) seperti GitHub, Slack, dan Linear untuk menyatukan alur kerja Anda.

## Datang dari CLI?

Desktop menjalankan mesin yang sama dengan CLI dengan antarmuka grafis. Anda dapat menjalankan keduanya secara bersamaan pada proyek yang sama, dan mereka berbagi konfigurasi (file CLAUDE.md, MCP servers, hooks, skills, dan settings). Untuk perbandingan lengkap fitur, setara flag, dan apa yang tidak tersedia di Desktop, lihat [perbandingan CLI](/id/desktop#coming-from-the-cli).

## Apa selanjutnya

* [Gunakan Claude Code Desktop](/id/desktop): mode izin, sesi paralel, tampilan diff, konektor, dan konfigurasi enterprise
* [Pemecahan masalah](/id/desktop#troubleshooting): solusi untuk kesalahan umum dan masalah setup
* [Praktik terbaik](/id/best-practices): tips untuk menulis prompt yang efektif dan mendapatkan hasil maksimal dari Claude Code
* [Alur kerja umum](/id/common-workflows): tutorial untuk debugging, refactoring, testing, dan lainnya
