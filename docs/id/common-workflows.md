> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Alur kerja umum

> Panduan langkah demi langkah untuk menjelajahi basis kode, memperbaiki bug, refactoring, pengujian, dan tugas sehari-hari lainnya dengan Claude Code.

Halaman ini mengumpulkan resep singkat untuk pengembangan sehari-hari. Untuk panduan tingkat yang lebih tinggi tentang prompting dan manajemen konteks, lihat [Best practices](/id/best-practices).

Halaman ini mencakup:

* [Resep prompt](#prompt-recipes) untuk menjelajahi kode, memperbaiki bug, refactoring, pengujian, PR, dan dokumentasi
* [Lanjutkan percakapan sebelumnya](#resume-previous-conversations) sehingga tugas dapat berlangsung selama beberapa sesi
* [Jalankan sesi paralel dengan worktrees](#run-parallel-sessions-with-worktrees) sehingga edit bersamaan tidak bertabrakan
* [Rencanakan sebelum mengedit](#plan-before-editing) untuk meninjau perubahan sebelum menyentuh disk
* [Delegasikan penelitian ke subagents](#delegate-research-to-subagents) untuk menjaga konteks utama Anda tetap bersih
* [Pipe Claude ke dalam skrip](#pipe-claude-into-scripts) untuk CI dan pemrosesan batch

## Resep prompt

Ini adalah pola prompt untuk tugas sehari-hari seperti menjelajahi kode yang tidak familiar, debugging, refactoring, menulis tes, dan membuat PR. Masing-masing bekerja di permukaan Claude Code apa pun; sesuaikan wording dengan proyek Anda.

### Pahami basis kode baru

#### Dapatkan gambaran umum basis kode dengan cepat

Misalkan Anda baru saja bergabung dengan proyek baru dan perlu memahami strukturnya dengan cepat.

<Steps>
  <Step title="Navigasi ke direktori root proyek">
    ```bash theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Mulai Claude Code">
    ```bash theme={null}
    claude 
    ```
  </Step>

  <Step title="Minta gambaran umum tingkat tinggi">
    ```text theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Selami komponen spesifik lebih dalam">
    ```text theme={null}
    explain the main architecture patterns used here
    ```

    ```text theme={null}
    what are the key data models?
    ```

    ```text theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Mulai dengan pertanyaan luas, kemudian fokus ke area spesifik
  * Tanyakan tentang konvensi koding dan pola yang digunakan dalam proyek
  * Minta glosarium istilah khusus proyek
</Tip>

#### Temukan kode yang relevan

Misalkan Anda perlu menemukan kode yang terkait dengan fitur atau fungsionalitas tertentu.

<Steps>
  <Step title="Minta Claude untuk menemukan file yang relevan">
    ```text theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Dapatkan konteks tentang cara komponen berinteraksi">
    ```text theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Pahami alur eksekusi">
    ```text theme={null}
    trace the login process from front-end to database
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Jadilah spesifik tentang apa yang Anda cari
  * Gunakan bahasa domain dari proyek
  * Instal [code intelligence plugin](/id/discover-plugins#code-intelligence) untuk bahasa Anda untuk memberikan Claude navigasi "go to definition" dan "find references" yang presisi
</Tip>

***

### Perbaiki bug secara efisien

Misalkan Anda telah mengalami pesan kesalahan dan perlu menemukan dan memperbaiki sumbernya.

<Steps>
  <Step title="Bagikan kesalahan dengan Claude">
    ```text theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Minta rekomendasi perbaikan">
    ```text theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Terapkan perbaikan">
    ```text theme={null}
    update user.ts to add the null check you suggested
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Beri tahu Claude perintah untuk mereproduksi masalah dan dapatkan stack trace
  * Sebutkan langkah apa pun untuk mereproduksi kesalahan
  * Beri tahu Claude jika kesalahan bersifat intermiten atau konsisten
</Tip>

***

### Refactor kode

Misalkan Anda perlu memperbarui kode lama untuk menggunakan pola dan praktik modern.

<Steps>
  <Step title="Identifikasi kode legacy untuk refactoring">
    ```text theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Dapatkan rekomendasi refactoring">
    ```text theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Terapkan perubahan dengan aman">
    ```text theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Verifikasi refactoring">
    ```text theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Minta Claude untuk menjelaskan manfaat pendekatan modern
  * Minta agar perubahan mempertahankan kompatibilitas backward ketika diperlukan
  * Lakukan refactoring dalam kenaikan kecil yang dapat diuji
</Tip>

***

### Bekerja dengan tes

Misalkan Anda perlu menambahkan tes untuk kode yang tidak tercakup.

<Steps>
  <Step title="Identifikasi kode yang tidak diuji">
    ```text theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Hasilkan scaffolding tes">
    ```text theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Tambahkan kasus tes yang bermakna">
    ```text theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Jalankan dan verifikasi tes">
    ```text theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude dapat menghasilkan tes yang mengikuti pola dan konvensi proyek Anda yang ada. Saat meminta tes, jadilah spesifik tentang perilaku apa yang ingin Anda verifikasi. Claude memeriksa file tes yang ada untuk mencocokkan gaya, framework, dan pola pernyataan yang sudah digunakan.

Untuk cakupan komprehensif, minta Claude untuk mengidentifikasi kasus tepi yang mungkin Anda lewatkan. Claude dapat menganalisis jalur kode Anda dan menyarankan tes untuk kondisi kesalahan, nilai batas, dan input yang tidak terduga yang mudah diabaikan.

***

### Buat pull request

Anda dapat membuat pull request dengan meminta Claude secara langsung ("create a pr for my changes"), atau memandu Claude melaluinya langkah demi langkah:

<Steps>
  <Step title="Ringkas perubahan Anda">
    ```text theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Hasilkan pull request">
    ```text theme={null}
    create a pr
    ```
  </Step>

  <Step title="Tinjau dan perbaiki">
    ```text theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

Ketika Anda membuat PR menggunakan `gh pr create`, sesi secara otomatis ditautkan ke PR tersebut. Untuk kembali ke sana nanti, jalankan `claude --from-pr <number>` atau tempel URL PR ke dalam [pemilih `/resume`](/id/sessions#use-the-session-picker).

<Tip>
  Tinjau PR yang dihasilkan Claude sebelum mengirimkan dan minta Claude untuk menyoroti risiko atau pertimbangan potensial.
</Tip>

### Tangani dokumentasi

Misalkan Anda perlu menambah atau memperbarui dokumentasi untuk kode Anda.

<Steps>
  <Step title="Identifikasi kode yang tidak terdokumentasi">
    ```text theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Hasilkan dokumentasi">
    ```text theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Tinjau dan tingkatkan">
    ```text theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Verifikasi dokumentasi">
    ```text theme={null}
    check if the documentation follows our project standards
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Tentukan gaya dokumentasi yang Anda inginkan (JSDoc, docstrings, dll.)
  * Minta contoh dalam dokumentasi
  * Minta dokumentasi untuk API publik, antarmuka, dan logika kompleks
</Tip>

***

### Bekerja dalam catatan dan folder non-kode

Claude Code bekerja di direktori apa pun. Jalankan di dalam vault catatan, folder dokumentasi, atau koleksi file markdown apa pun untuk mencari, mengedit, dan mengatur ulang konten dengan cara yang sama seperti Anda melakukan kode.

Direktori `.claude/` dan `CLAUDE.md` duduk bersama direktori konfigurasi alat lain tanpa konflik. Claude membaca file segar pada setiap panggilan alat, jadi ia melihat edit yang Anda buat di aplikasi lain saat berikutnya membaca file tersebut.

***

### Bekerja dengan gambar

Misalkan Anda perlu bekerja dengan gambar dalam basis kode Anda, dan Anda ingin bantuan Claude menganalisis konten gambar.

<Steps>
  <Step title="Tambahkan gambar ke percakapan">
    Anda dapat menggunakan salah satu metode ini:

    1. Seret dan lepas gambar ke jendela Claude Code
    2. Salin gambar dan tempel ke CLI dengan ctrl+v (Jangan gunakan cmd+v)
    3. Berikan jalur gambar ke Claude. Misalnya, "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Minta Claude untuk menganalisis gambar">
    ```text theme={null}
    What does this image show?
    ```

    ```text theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Gunakan gambar untuk konteks">
    ```text theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Dapatkan saran kode dari konten visual">
    ```text theme={null}
    Generate CSS to match this design mockup
    ```

    ```text theme={null}
    What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Gunakan gambar ketika deskripsi teks akan tidak jelas atau merepotkan
  * Sertakan tangkapan layar kesalahan, desain UI, atau diagram untuk konteks yang lebih baik
  * Anda dapat bekerja dengan beberapa gambar dalam percakapan
  * Analisis gambar bekerja dengan diagram, tangkapan layar, mockup, dan lainnya
  * Ketika Claude mereferensikan gambar (misalnya, `[Image #1]`), `Cmd+Click` (Mac) atau `Ctrl+Click` (Windows/Linux) tautan untuk membuka gambar di penampil default Anda
</Tip>

***

### File dan direktori referensi

Gunakan @ untuk dengan cepat menyertakan file atau direktori tanpa menunggu Claude membacanya.

<Steps>
  <Step title="Referensikan file tunggal">
    ```text theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    Ini menyertakan konten lengkap file dalam percakapan.
  </Step>

  <Step title="Referensikan direktori">
    ```text theme={null}
    What's the structure of @src/components?
    ```

    Ini menyediakan daftar direktori dengan informasi file.
  </Step>

  <Step title="Referensikan sumber daya MCP">
    ```text theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    Ini mengambil data dari server MCP yang terhubung menggunakan format @server:resource. Lihat [sumber daya MCP](/id/mcp#use-mcp-resources) untuk detail.
  </Step>
</Steps>

<Tip>
  Tips:

  * Jalur file dapat relatif atau absolut
  * Referensi file @ menambahkan `CLAUDE.md` di direktori file dan direktori induk ke konteks
  * Referensi direktori menampilkan daftar file, bukan konten
  * Anda dapat mereferensikan beberapa file dalam satu pesan (misalnya, "@file1.js and @file2.js")
</Tip>

***

### Jalankan Claude pada jadwal

Misalkan Anda ingin Claude menangani tugas secara otomatis secara berulang, seperti meninjau PR terbuka setiap pagi, mengaudit dependensi mingguan, atau memeriksa kegagalan CI semalam.

Pilih opsi penjadwalan berdasarkan tempat Anda ingin tugas berjalan:

| Opsi                                                   | Tempat berjalan                       | Terbaik untuk                                                                                                                                                                                                   |
| :----------------------------------------------------- | :------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Routines](/id/routines)                               | Infrastruktur yang dikelola Anthropic | Tugas yang harus berjalan bahkan ketika komputer Anda mati. Dapat juga dipicu oleh panggilan API atau event GitHub selain jadwal. Konfigurasikan di [claude.ai/code/routines](https://claude.ai/code/routines). |
| [Desktop scheduled tasks](/id/desktop-scheduled-tasks) | Mesin Anda, melalui aplikasi desktop  | Tugas yang memerlukan akses langsung ke file lokal, alat, atau perubahan yang tidak dilakukan.                                                                                                                  |
| [GitHub Actions](/id/github-actions)                   | Pipeline CI Anda                      | Tugas yang terikat pada event repo seperti PR yang dibuka, atau jadwal cron yang harus hidup bersama konfigurasi alur kerja Anda.                                                                               |
| [`/loop`](/id/scheduled-tasks)                         | Sesi CLI saat ini                     | Polling cepat saat sesi terbuka. Tugas berhenti ketika Anda memulai percakapan baru; `--resume` dan `--continue` mengembalikan yang belum kadaluarsa.                                                           |

<Tip>
  Saat menulis prompt untuk tugas terjadwal, jelaskan apa yang terlihat seperti kesuksesan dan apa yang harus dilakukan dengan hasil. Tugas berjalan secara otonom, jadi tidak dapat mengajukan pertanyaan klarifikasi. Misalnya: "Review open PRs labeled `needs-review`, leave inline comments on any issues, and post a summary in the `#eng-reviews` Slack channel."
</Tip>

***

### Tanyakan Claude tentang kemampuannya

Claude memiliki akses bawaan ke dokumentasinya dan dapat menjawab pertanyaan tentang fitur dan keterbatasannya sendiri.

#### Contoh pertanyaan

```text theme={null}
can Claude Code create pull requests?
```

```text theme={null}
how does Claude Code handle permissions?
```

```text theme={null}
what skills are available?
```

```text theme={null}
how do I use MCP with Claude Code?
```

```text theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude memberikan jawaban berbasis dokumentasi untuk pertanyaan-pertanyaan ini. Untuk demonstrasi langsung, jalankan `/powerup` untuk pelajaran interaktif dengan demo animasi, atau lihat bagian alur kerja spesifik di atas.
</Note>

<Tip>
  Tips:

  * Claude selalu memiliki akses ke dokumentasi Claude Code terbaru, terlepas dari versi yang Anda gunakan
  * Ajukan pertanyaan spesifik untuk mendapatkan jawaban terperinci
  * Claude dapat menjelaskan fitur kompleks seperti integrasi MCP, konfigurasi enterprise, dan alur kerja lanjutan
</Tip>

***

## Lanjutkan percakapan sebelumnya

Ketika tugas berlangsung selama beberapa sesi, ambil alih dari tempat Anda berhenti daripada menjelaskan ulang konteks. Claude Code menyimpan setiap percakapan secara lokal.

```bash theme={null}
claude --continue
```

Ini melanjutkan sesi terbaru di direktori saat ini; jika belum ada, itu mencetak `No conversation found to continue` dan keluar. Gunakan `claude --resume` untuk memilih dari daftar, atau `/resume` dari dalam sesi yang berjalan. Lihat [Kelola sesi](/id/sessions) untuk penamaan, branching, dan referensi pemilih lengkap.

## Jalankan sesi paralel dengan worktrees

Bekerja pada fitur di satu terminal sementara Claude memperbaiki bug di terminal lain, tanpa edit bertabrakan. Setiap worktree adalah checkout terpisah di cabangnya sendiri.

```bash theme={null}
claude --worktree feature-auth
```

Jalankan perintah yang sama dengan nama berbeda di terminal kedua untuk memulai sesi paralel terisolasi. Lihat [Worktrees](/id/worktrees) untuk pembersihan, `.worktreeinclude`, dan dukungan VCS non-git. Untuk memantau sesi paralel dari satu layar daripada terminal terpisah, lihat [background agents](/id/agent-view).

## Rencanakan sebelum mengedit

Untuk perubahan yang ingin Anda tinjau sebelum menyentuh disk, beralih ke plan mode. Claude membaca file dan mengusulkan rencana tetapi tidak membuat edit sampai Anda menyetujui.

```bash theme={null}
claude --permission-mode plan
```

Anda juga dapat menekan `Shift+Tab` di tengah sesi untuk beralih ke plan mode. Lihat [Plan mode](/id/permission-modes#analyze-before-you-edit-with-plan-mode) untuk alur persetujuan dan mengedit rencana di editor teks Anda.

## Delegasikan penelitian ke subagents

Menjelajahi basis kode besar mengisi konteks Anda dengan pembacaan file. Delegasikan eksplorasi sehingga hanya temuan yang kembali.

```text theme={null}
use a subagent to investigate how our auth system handles token refresh
```

Subagent membaca file dalam jendela konteksnya sendiri dan melaporkan ringkasan. Lihat [Subagents](/id/sub-agents) untuk mendefinisikan agen kustom dengan alat dan prompt mereka sendiri.

## Pipe Claude ke dalam skrip

Jalankan Claude secara non-interaktif untuk CI, pre-commit hooks, atau pemrosesan batch. Stdin dan stdout bekerja seperti alat Unix apa pun.

```bash theme={null}
git log --oneline -20 | claude -p "summarize these recent commits"
```

Lihat [Non-interactive mode](/id/headless) untuk format output, flag izin, dan pola fan-out.

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Best practices" icon="lightbulb" href="/id/best-practices">
    Pola untuk mendapatkan hasil maksimal dari Claude Code
  </Card>

  <Card title="Kelola sesi" icon="rotate-left" href="/id/sessions">
    Lanjutkan, beri nama, dan cabang percakapan
  </Card>

  <Card title="Worktrees" icon="code-branch" href="/id/worktrees">
    Jalankan sesi paralel terisolasi
  </Card>

  <Card title="Perluas Claude Code" icon="puzzle-piece" href="/id/features-overview">
    Tambahkan skills, hooks, MCP, subagents, dan plugins
  </Card>
</CardGroup>
