> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Alur kerja umum

> Panduan langkah demi langkah untuk menjelajahi basis kode, memperbaiki bug, refactoring, pengujian, dan tugas sehari-hari lainnya dengan Claude Code.

Halaman ini mencakup alur kerja praktis untuk pengembangan sehari-hari: menjelajahi kode yang tidak familiar, debugging, refactoring, menulis tes, membuat PR, dan mengelola sesi. Setiap bagian mencakup contoh prompt yang dapat Anda sesuaikan dengan proyek Anda sendiri. Untuk pola dan tips tingkat yang lebih tinggi, lihat [Best practices](/id/best-practices).

## Pahami basis kode baru

### Dapatkan gambaran umum basis kode dengan cepat

Misalkan Anda baru saja bergabung dengan proyek baru dan perlu memahami strukturnya dengan cepat.

<Steps>
  <Step title="Navigasi ke direktori root proyek">
    ```bash  theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Mulai Claude Code">
    ```bash  theme={null}
    claude 
    ```
  </Step>

  <Step title="Minta gambaran umum tingkat tinggi">
    ```text  theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Selami komponen spesifik lebih dalam">
    ```text  theme={null}
    explain the main architecture patterns used here
    ```

    ```text  theme={null}
    what are the key data models?
    ```

    ```text  theme={null}
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

### Temukan kode yang relevan

Misalkan Anda perlu menemukan kode yang terkait dengan fitur atau fungsionalitas tertentu.

<Steps>
  <Step title="Minta Claude untuk menemukan file yang relevan">
    ```text  theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Dapatkan konteks tentang cara komponen berinteraksi">
    ```text  theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Pahami alur eksekusi">
    ```text  theme={null}
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

## Perbaiki bug secara efisien

Misalkan Anda telah mengalami pesan kesalahan dan perlu menemukan dan memperbaiki sumbernya.

<Steps>
  <Step title="Bagikan kesalahan dengan Claude">
    ```text  theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Minta rekomendasi perbaikan">
    ```text  theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Terapkan perbaikan">
    ```text  theme={null}
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

## Refactor kode

Misalkan Anda perlu memperbarui kode lama untuk menggunakan pola dan praktik modern.

<Steps>
  <Step title="Identifikasi kode legacy untuk refactoring">
    ```text  theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Dapatkan rekomendasi refactoring">
    ```text  theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Terapkan perubahan dengan aman">
    ```text  theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Verifikasi refactoring">
    ```text  theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Minta Claude untuk menjelaskan manfaat pendekatan modern
  * Minta agar perubahan mempertahankan kompatibilitas backward ketika diperlukan
  * Lakukan refactoring dalam increment kecil yang dapat diuji
</Tip>

***

## Gunakan subagents khusus

Misalkan Anda ingin menggunakan subagents AI khusus untuk menangani tugas spesifik dengan lebih efektif.

<Steps>
  <Step title="Lihat subagents yang tersedia">
    ```text  theme={null}
    /agents
    ```

    Ini menampilkan semua subagents yang tersedia dan memungkinkan Anda membuat yang baru.
  </Step>

  <Step title="Gunakan subagents secara otomatis">
    Claude Code secara otomatis mendelegasikan tugas yang sesuai ke subagents khusus:

    ```text  theme={null}
    review my recent code changes for security issues
    ```

    ```text  theme={null}
    run all tests and fix any failures
    ```
  </Step>

  <Step title="Minta subagents spesifik secara eksplisit">
    ```text  theme={null}
    use the code-reviewer subagent to check the auth module
    ```

    ```text  theme={null}
    have the debugger subagent investigate why users can't log in
    ```
  </Step>

  <Step title="Buat subagents kustom untuk alur kerja Anda">
    ```text  theme={null}
    /agents
    ```

    Kemudian pilih "Create New subagent" dan ikuti prompt untuk mendefinisikan:

    * Pengenal unik yang menggambarkan tujuan subagent (misalnya, `code-reviewer`, `api-designer`).
    * Kapan Claude harus menggunakan agen ini
    * Alat mana yang dapat diaksesnya
    * Prompt sistem yang menggambarkan peran dan perilaku agen
  </Step>
</Steps>

<Tip>
  Tips:

  * Buat subagents khusus proyek di `.claude/agents/` untuk berbagi tim
  * Gunakan field `description` deskriptif untuk mengaktifkan delegasi otomatis
  * Batasi akses alat ke apa yang benar-benar dibutuhkan setiap subagent
  * Periksa [dokumentasi subagents](/id/sub-agents) untuk contoh terperinci
</Tip>

***

## Gunakan Plan Mode untuk analisis kode yang aman

Plan Mode menginstruksikan Claude untuk membuat rencana dengan menganalisis basis kode dengan operasi read-only, sempurna untuk menjelajahi basis kode, merencanakan perubahan kompleks, atau meninjau kode dengan aman. Dalam Plan Mode, Claude menggunakan [`AskUserQuestion`](/id/settings#tools-available-to-claude) untuk mengumpulkan persyaratan dan memperjelas tujuan Anda sebelum mengusulkan rencana.

### Kapan menggunakan Plan Mode

* **Implementasi multi-langkah**: Ketika fitur Anda memerlukan pengeditan ke banyak file
* **Eksplorasi kode**: Ketika Anda ingin meneliti basis kode secara menyeluruh sebelum mengubah apa pun
* **Pengembangan interaktif**: Ketika Anda ingin mengulangi arah dengan Claude

### Cara menggunakan Plan Mode

**Aktifkan Plan Mode selama sesi**

Anda dapat beralih ke Plan Mode selama sesi menggunakan **Shift+Tab** untuk bersiklus melalui mode izin.

Jika Anda berada dalam Normal Mode, **Shift+Tab** pertama kali beralih ke Auto-Accept Mode, ditunjukkan oleh `⏵⏵ accept edits on` di bagian bawah terminal. **Shift+Tab** berikutnya akan beralih ke Plan Mode, ditunjukkan oleh `⏸ plan mode on`.

**Mulai sesi baru dalam Plan Mode**

Untuk memulai sesi baru dalam Plan Mode, gunakan flag `--permission-mode plan`:

```bash  theme={null}
claude --permission-mode plan
```

**Jalankan query "headless" dalam Plan Mode**

Anda juga dapat menjalankan query dalam Plan Mode secara langsung dengan `-p` (yaitu, dalam ["headless mode"](/id/headless)):

```bash  theme={null}
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Contoh: Merencanakan refactor kompleks

```bash  theme={null}
claude --permission-mode plan
```

```text  theme={null}
I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude menganalisis implementasi saat ini dan membuat rencana komprehensif. Perbaiki dengan tindak lanjut:

```text  theme={null}
What about backward compatibility?
```

```text  theme={null}
How should we handle database migration?
```

<Tip>Tekan `Ctrl+G` untuk membuka rencana di editor teks default Anda, di mana Anda dapat mengeditnya secara langsung sebelum Claude melanjutkan.</Tip>

### Konfigurasikan Plan Mode sebagai default

```json  theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Lihat [dokumentasi settings](/id/settings#available-settings) untuk opsi konfigurasi lainnya.

***

## Bekerja dengan tes

Misalkan Anda perlu menambahkan tes untuk kode yang tidak tercakup.

<Steps>
  <Step title="Identifikasi kode yang tidak diuji">
    ```text  theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Hasilkan scaffolding tes">
    ```text  theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Tambahkan kasus tes yang bermakna">
    ```text  theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Jalankan dan verifikasi tes">
    ```text  theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude dapat menghasilkan tes yang mengikuti pola dan konvensi yang ada dalam proyek Anda. Saat meminta tes, jadilah spesifik tentang perilaku apa yang ingin Anda verifikasi. Claude memeriksa file tes yang ada untuk mencocokkan gaya, framework, dan pola pernyataan yang sudah digunakan.

Untuk cakupan komprehensif, minta Claude untuk mengidentifikasi kasus tepi yang mungkin Anda lewatkan. Claude dapat menganalisis jalur kode Anda dan menyarankan tes untuk kondisi kesalahan, nilai batas, dan input yang tidak terduga yang mudah diabaikan.

***

## Buat pull request

Anda dapat membuat pull request dengan meminta Claude secara langsung ("create a pr for my changes"), atau memandu Claude melaluinya langkah demi langkah:

<Steps>
  <Step title="Ringkas perubahan Anda">
    ```text  theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Hasilkan pull request">
    ```text  theme={null}
    create a pr
    ```
  </Step>

  <Step title="Tinjau dan perbaiki">
    ```text  theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

Ketika Anda membuat PR menggunakan `gh pr create`, sesi secara otomatis ditautkan ke PR tersebut. Anda dapat melanjutkannya nanti dengan `claude --from-pr <number>`.

<Tip>
  Tinjau PR yang dihasilkan Claude sebelum mengirimkan dan minta Claude untuk menyoroti risiko atau pertimbangan potensial.
</Tip>

## Tangani dokumentasi

Misalkan Anda perlu menambah atau memperbarui dokumentasi untuk kode Anda.

<Steps>
  <Step title="Identifikasi kode yang tidak terdokumentasi">
    ```text  theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Hasilkan dokumentasi">
    ```text  theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Tinjau dan tingkatkan">
    ```text  theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Verifikasi dokumentasi">
    ```text  theme={null}
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

## Bekerja dengan gambar

Misalkan Anda perlu bekerja dengan gambar dalam basis kode Anda, dan Anda ingin bantuan Claude dalam menganalisis konten gambar.

<Steps>
  <Step title="Tambahkan gambar ke percakapan">
    Anda dapat menggunakan salah satu metode ini:

    1. Seret dan lepas gambar ke jendela Claude Code
    2. Salin gambar dan tempel ke CLI dengan ctrl+v (Jangan gunakan cmd+v)
    3. Berikan jalur gambar ke Claude. Misalnya, "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Minta Claude untuk menganalisis gambar">
    ```text  theme={null}
    What does this image show?
    ```

    ```text  theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text  theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Gunakan gambar untuk konteks">
    ```text  theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text  theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Dapatkan saran kode dari konten visual">
    ```text  theme={null}
    Generate CSS to match this design mockup
    ```

    ```text  theme={null}
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

## File dan direktori referensi

Gunakan @ untuk dengan cepat menyertakan file atau direktori tanpa menunggu Claude membacanya.

<Steps>
  <Step title="Referensikan file tunggal">
    ```text  theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    Ini menyertakan konten lengkap file dalam percakapan.
  </Step>

  <Step title="Referensikan direktori">
    ```text  theme={null}
    What's the structure of @src/components?
    ```

    Ini menyediakan daftar direktori dengan informasi file.
  </Step>

  <Step title="Referensikan sumber daya MCP">
    ```text  theme={null}
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

## Gunakan extended thinking (thinking mode)

[Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) diaktifkan secara default, memberikan Claude ruang untuk bernalar melalui masalah kompleks langkah demi langkah sebelum merespons. Penalaran ini terlihat dalam verbose mode, yang dapat Anda aktifkan dengan `Ctrl+O`.

Selain itu, Opus 4.6 memperkenalkan adaptive reasoning: alih-alih anggaran token thinking yang tetap, model secara dinamis mengalokasikan thinking berdasarkan pengaturan [effort level](/id/model-config#adjust-effort-level) Anda. Extended thinking dan adaptive reasoning bekerja bersama untuk memberi Anda kontrol atas seberapa dalam Claude bernalar sebelum merespons.

Extended thinking sangat berharga untuk keputusan arsitektur kompleks, bug yang menantang, perencanaan implementasi multi-langkah, dan mengevaluasi trade-off antara pendekatan yang berbeda.

<Note>
  Frasa seperti "think", "think hard", dan "think more" diinterpretasikan sebagai instruksi prompt reguler dan tidak mengalokasikan token thinking.
</Note>

### Konfigurasikan thinking mode

Thinking diaktifkan secara default, tetapi Anda dapat menyesuaikan atau menonaktifkannya.

| Scope                       | Cara mengkonfigurasi                                                                             | Detail                                                                                                                                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effort level**            | Sesuaikan di `/model` atau atur [`CLAUDE_CODE_EFFORT_LEVEL`](/id/settings#environment-variables) | Kontrol kedalaman thinking untuk Opus 4.6 dan Sonnet 4.6: low, medium, high. Lihat [Adjust effort level](/id/model-config#adjust-effort-level)                                                     |
| **Kata kunci `ultrathink`** | Sertakan "ultrathink" di mana saja dalam prompt Anda                                             | Menetapkan effort ke high untuk giliran itu pada Opus 4.6 dan Sonnet 4.6. Berguna untuk tugas sekali jadi yang memerlukan penalaran mendalam tanpa mengubah pengaturan effort Anda secara permanen |
| **Pintasan toggle**         | Tekan `Option+T` (macOS) atau `Alt+T` (Windows/Linux)                                            | Toggle thinking on/off untuk sesi saat ini (semua model). Mungkin memerlukan [konfigurasi terminal](/id/terminal-config) untuk mengaktifkan pintasan tombol Option                                 |
| **Default global**          | Gunakan `/config` untuk toggle thinking mode                                                     | Menetapkan default Anda di semua proyek (semua model).<br />Disimpan sebagai `alwaysThinkingEnabled` di `~/.claude/settings.json`                                                                  |
| **Batasi anggaran token**   | Atur variabel lingkungan [`MAX_THINKING_TOKENS`](/id/settings#environment-variables)             | Batasi anggaran thinking ke jumlah token tertentu (diabaikan pada Opus 4.6 kecuali diatur ke 0). Contoh: `export MAX_THINKING_TOKENS=10000`                                                        |

Untuk melihat proses thinking Claude, tekan `Ctrl+O` untuk toggle verbose mode dan lihat penalaran internal ditampilkan sebagai teks italic abu-abu.

### Cara kerja extended thinking

Extended thinking mengontrol berapa banyak penalaran internal yang dilakukan Claude sebelum merespons. Lebih banyak thinking memberikan lebih banyak ruang untuk menjelajahi solusi, menganalisis kasus tepi, dan memperbaiki kesalahan sendiri.

**Dengan Opus 4.6**, thinking menggunakan adaptive reasoning: model secara dinamis mengalokasikan token thinking berdasarkan [effort level](/id/model-config#adjust-effort-level) yang Anda pilih (low, medium, high). Ini adalah cara yang direkomendasikan untuk menyesuaikan trade-off antara kecepatan dan kedalaman penalaran.

**Dengan model lain**, thinking menggunakan anggaran tetap hingga 31.999 token dari anggaran output Anda. Anda dapat membatasinya dengan variabel lingkungan [`MAX_THINKING_TOKENS`](/id/settings#environment-variables), atau menonaktifkan thinking sepenuhnya melalui `/config` atau toggle `Option+T`/`Alt+T`.

`MAX_THINKING_TOKENS` diabaikan pada Opus 4.6 dan Sonnet 4.6, karena adaptive reasoning mengontrol kedalaman thinking sebagai gantinya. Satu pengecualian: mengatur `MAX_THINKING_TOKENS=0` masih menonaktifkan thinking sepenuhnya pada model apa pun. Untuk menonaktifkan adaptive thinking dan kembali ke anggaran thinking tetap, atur `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Lihat [variabel lingkungan](/id/settings#environment-variables).

<Warning>
  Anda dikenakan biaya untuk semua token thinking yang digunakan, meskipun model Claude 4 menampilkan thinking yang diringkas
</Warning>

***

## Lanjutkan percakapan sebelumnya

Saat memulai Claude Code, Anda dapat melanjutkan sesi sebelumnya:

* `claude --continue` melanjutkan percakapan terbaru di direktori saat ini
* `claude --resume` membuka pemilih percakapan atau melanjutkan berdasarkan nama
* `claude --from-pr 123` melanjutkan sesi yang ditautkan ke pull request tertentu

Dari dalam sesi aktif, gunakan `/resume` untuk beralih ke percakapan berbeda.

Sesi disimpan per direktori proyek. Pemilih `/resume` menampilkan sesi dari repositori git yang sama, termasuk worktrees.

### Beri nama sesi Anda

Berikan sesi nama deskriptif untuk menemukannya nanti. Ini adalah praktik terbaik saat bekerja pada beberapa tugas atau fitur.

<Steps>
  <Step title="Beri nama sesi saat ini">
    Gunakan `/rename` selama sesi untuk memberikannya nama yang mudah diingat:

    ```text  theme={null}
    /rename auth-refactor
    ```

    Anda juga dapat mengganti nama sesi apa pun dari pemilih: jalankan `/resume`, navigasi ke sesi, dan tekan `R`.
  </Step>

  <Step title="Lanjutkan berdasarkan nama nanti">
    Dari baris perintah:

    ```bash  theme={null}
    claude --resume auth-refactor
    ```

    Atau dari dalam sesi aktif:

    ```text  theme={null}
    /resume auth-refactor
    ```
  </Step>
</Steps>

### Gunakan pemilih sesi

Perintah `/resume` (atau `claude --resume` tanpa argumen) membuka pemilih sesi interaktif dengan fitur-fitur ini:

**Pintasan keyboard dalam pemilih:**

| Pintasan  | Tindakan                                          |
| :-------- | :------------------------------------------------ |
| `↑` / `↓` | Navigasi antar sesi                               |
| `→` / `←` | Perluas atau tutup sesi yang dikelompokkan        |
| `Enter`   | Pilih dan lanjutkan sesi yang disorot             |
| `P`       | Pratinjau konten sesi                             |
| `R`       | Ganti nama sesi yang disorot                      |
| `/`       | Cari untuk memfilter sesi                         |
| `A`       | Toggle antara direktori saat ini dan semua proyek |
| `B`       | Filter ke sesi dari cabang git saat ini Anda      |
| `Esc`     | Keluar dari pemilih atau mode pencarian           |

**Organisasi sesi:**

Pemilih menampilkan sesi dengan metadata yang membantu:

* Nama sesi atau prompt awal
* Waktu yang telah berlalu sejak aktivitas terakhir
* Jumlah pesan
* Cabang Git (jika berlaku)

Sesi yang di-fork (dibuat dengan `/rewind` atau `--fork-session`) dikelompokkan bersama di bawah sesi root mereka, memudahkan menemukan percakapan terkait.

<Tip>
  Tips:

  * **Beri nama sesi lebih awal**: Gunakan `/rename` saat memulai pekerjaan pada tugas yang berbeda—jauh lebih mudah menemukan "payment-integration" daripada "explain this function" nanti
  * Gunakan `--continue` untuk akses cepat ke percakapan terbaru Anda di direktori saat ini
  * Gunakan `--resume session-name` ketika Anda tahu sesi mana yang Anda butuhkan
  * Gunakan `--resume` (tanpa nama) ketika Anda perlu menjelajahi dan memilih
  * Untuk skrip, gunakan `claude --continue --print "prompt"` untuk melanjutkan dalam mode non-interaktif
  * Tekan `P` dalam pemilih untuk melihat pratinjau sesi sebelum melanjutkannya
  * Percakapan yang dilanjutkan dimulai dengan model dan konfigurasi yang sama dengan yang asli

  Cara kerjanya:

  1. **Penyimpanan Percakapan**: Semua percakapan secara otomatis disimpan secara lokal dengan riwayat pesan lengkap mereka
  2. **Deserialisasi Pesan**: Saat melanjutkan, seluruh riwayat pesan dipulihkan untuk mempertahankan konteks
  3. **Status Alat**: Penggunaan alat dan hasil dari percakapan sebelumnya dipertahankan
  4. **Pemulihan Konteks**: Percakapan dilanjutkan dengan semua konteks sebelumnya utuh
</Tip>

***

## Jalankan sesi Claude Code paralel dengan Git worktrees

Saat bekerja pada beberapa tugas sekaligus, Anda memerlukan setiap sesi Claude untuk memiliki salinan basis kode sendiri sehingga perubahan tidak bertabrakan. Git worktrees menyelesaikan ini dengan membuat direktori kerja terpisah yang masing-masing memiliki file dan cabang sendiri, sambil berbagi riwayat repositori dan koneksi remote yang sama. Ini berarti Anda dapat memiliki Claude bekerja pada fitur di satu worktree sambil memperbaiki bug di worktree lain, tanpa sesi apa pun mengganggu yang lain.

Gunakan flag `--worktree` (`-w`) untuk membuat worktree terisolasi dan memulai Claude di dalamnya. Nilai yang Anda berikan menjadi nama direktori worktree dan nama cabang:

```bash  theme={null}
# Mulai Claude dalam worktree bernama "feature-auth"
# Membuat .claude/worktrees/feature-auth/ dengan cabang baru
claude --worktree feature-auth

# Mulai sesi lain dalam worktree terpisah
claude --worktree bugfix-123
```

Jika Anda menghilangkan nama, Claude secara otomatis menghasilkan nama acak:

```bash  theme={null}
# Auto-generates a name like "bright-running-fox"
claude --worktree
```

Worktrees dibuat di `<repo>/.claude/worktrees/<name>` dan bercabang dari cabang remote default. Cabang worktree dinamai `worktree-<name>`.

Anda juga dapat meminta Claude untuk "work in a worktree" atau "start a worktree" selama sesi, dan itu akan membuat satu secara otomatis.

### Worktrees subagent

Subagents juga dapat menggunakan isolasi worktree untuk bekerja secara paralel tanpa konflik. Minta Claude untuk "use worktrees for your agents" atau konfigurasikan di [custom subagent](/id/sub-agents#supported-frontmatter-fields) dengan menambahkan `isolation: worktree` ke frontmatter agen. Setiap subagent mendapatkan worktree sendiri yang secara otomatis dibersihkan ketika subagent selesai tanpa perubahan.

### Pembersihan worktree

Saat Anda keluar dari sesi worktree, Claude menangani pembersihan berdasarkan apakah Anda membuat perubahan:

* **Tidak ada perubahan**: worktree dan cabangnya dihapus secara otomatis
* **Perubahan atau commit ada**: Claude meminta Anda untuk menyimpan atau menghapus worktree. Menyimpan mempertahankan direktori dan cabang sehingga Anda dapat kembali nanti. Menghapus menghapus direktori worktree dan cabangnya, membuang semua perubahan yang tidak dilakukan dan commit

Untuk membersihkan worktrees di luar sesi Claude, gunakan [manajemen worktree manual](#manage-worktrees-manually).

<Tip>
  Tambahkan `.claude/worktrees/` ke `.gitignore` Anda untuk mencegah konten worktree muncul sebagai file yang tidak dilacak dalam repositori utama Anda.
</Tip>

### Kelola worktrees secara manual

Untuk kontrol lebih besar atas lokasi worktree dan konfigurasi cabang, buat worktrees dengan Git secara langsung. Ini berguna ketika Anda perlu checkout cabang yang ada tertentu atau menempatkan worktree di luar repositori.

```bash  theme={null}
# Buat worktree dengan cabang baru
git worktree add ../project-feature-a -b feature-a

# Buat worktree dengan cabang yang ada
git worktree add ../project-bugfix bugfix-123

# Mulai Claude dalam worktree
cd ../project-feature-a && claude

# Bersihkan saat selesai
git worktree list
git worktree remove ../project-feature-a
```

Pelajari lebih lanjut di [dokumentasi Git worktree resmi](https://git-scm.com/docs/git-worktree).

<Tip>
  Ingat untuk menginisialisasi lingkungan pengembangan Anda di setiap worktree baru sesuai dengan setup proyek Anda. Tergantung pada stack Anda, ini mungkin termasuk menjalankan instalasi dependensi (`npm install`, `yarn`), menyiapkan lingkungan virtual, atau mengikuti proses setup standar proyek Anda.
</Tip>

### Kontrol versi non-git

Isolasi worktree bekerja dengan git secara default. Untuk sistem kontrol versi lain seperti SVN, Perforce, atau Mercurial, konfigurasikan [hook WorktreeCreate dan WorktreeRemove](/id/hooks#worktreecreate) untuk menyediakan logika pembuatan dan pembersihan worktree kustom. Ketika dikonfigurasi, hook ini menggantikan perilaku git default saat Anda menggunakan `--worktree`.

Untuk koordinasi otomatis sesi paralel dengan tugas bersama dan pesan, lihat [agent teams](/id/agent-teams).

***

## Dapatkan notifikasi ketika Claude membutuhkan perhatian Anda

Ketika Anda memulai tugas yang berjalan lama dan beralih ke jendela lain, Anda dapat menyiapkan notifikasi desktop sehingga Anda tahu ketika Claude selesai atau membutuhkan input Anda. Ini menggunakan event hook `Notification` [](/id/hooks-guide#get-notified-when-claude-needs-input), yang diaktifkan setiap kali Claude menunggu izin, idle dan siap untuk prompt baru, atau menyelesaikan autentikasi.

<Steps>
  <Step title="Buka menu hooks">
    Ketik `/hooks` dan pilih `Notification` dari daftar event.
  </Step>

  <Step title="Konfigurasikan matcher">
    Pilih `+ Match all (no filter)` untuk diaktifkan pada semua jenis notifikasi. Untuk memberi tahu hanya untuk event spesifik, pilih `+ Add new matcher…` dan masukkan salah satu nilai ini:

    | Matcher              | Diaktifkan ketika                                        |
    | :------------------- | :------------------------------------------------------- |
    | `permission_prompt`  | Claude membutuhkan Anda untuk menyetujui penggunaan alat |
    | `idle_prompt`        | Claude selesai dan menunggu prompt berikutnya Anda       |
    | `auth_success`       | Autentikasi selesai                                      |
    | `elicitation_dialog` | Claude mengajukan pertanyaan kepada Anda                 |
  </Step>

  <Step title="Tambahkan perintah notifikasi Anda">
    Pilih `+ Add new hook…` dan masukkan perintah untuk OS Anda:

    <Tabs>
      <Tab title="macOS">
        Menggunakan [`osascript`](https://ss64.com/mac/osascript.html) untuk memicu notifikasi macOS asli melalui AppleScript:

        ```
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Menggunakan `notify-send`, yang sudah diinstal sebelumnya di sebagian besar desktop Linux dengan daemon notifikasi:

        ```
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Menggunakan PowerShell untuk menampilkan kotak pesan asli melalui Windows Forms .NET:

        ```
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Simpan ke pengaturan pengguna">
    Pilih `User settings` untuk menerapkan notifikasi di semua proyek Anda.
  </Step>
</Steps>

Untuk panduan lengkap dengan contoh konfigurasi JSON, lihat [Automate workflows with hooks](/id/hooks-guide#get-notified-when-claude-needs-input). Untuk skema event lengkap dan jenis notifikasi, lihat [referensi Notification](/id/hooks#notification).

***

## Gunakan Claude sebagai utilitas gaya unix

### Tambahkan Claude ke proses verifikasi Anda

Misalkan Anda ingin menggunakan Claude Code sebagai linter atau code reviewer.

**Tambahkan Claude ke skrip build Anda:**

```json  theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  Tips:

  * Gunakan Claude untuk code review otomatis dalam pipeline CI/CD Anda
  * Sesuaikan prompt untuk memeriksa masalah spesifik yang relevan dengan proyek Anda
  * Pertimbangkan membuat beberapa skrip untuk jenis verifikasi yang berbeda
</Tip>

### Pipe in, pipe out

Misalkan Anda ingin pipe data ke Claude, dan dapatkan kembali data dalam format terstruktur.

**Pipe data melalui Claude:**

```bash  theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  Tips:

  * Gunakan pipe untuk mengintegrasikan Claude ke dalam skrip shell yang ada
  * Gabungkan dengan alat Unix lain untuk alur kerja yang kuat
  * Pertimbangkan menggunakan --output-format untuk output terstruktur
</Tip>

### Kontrol format output

Misalkan Anda memerlukan output Claude dalam format tertentu, terutama saat mengintegrasikan Claude Code ke dalam skrip atau alat lain.

<Steps>
  <Step title="Gunakan format teks (default)">
    ```bash  theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    Ini menampilkan hanya respons teks biasa Claude (perilaku default).
  </Step>

  <Step title="Gunakan format JSON">
    ```bash  theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    Ini menampilkan array JSON pesan dengan metadata termasuk biaya dan durasi.
  </Step>

  <Step title="Gunakan format streaming JSON">
    ```bash  theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    Ini menampilkan serangkaian objek JSON secara real-time saat Claude memproses permintaan. Setiap pesan adalah objek JSON yang valid, tetapi seluruh output bukan JSON yang valid jika digabungkan.
  </Step>
</Steps>

<Tip>
  Tips:

  * Gunakan `--output-format text` untuk integrasi sederhana di mana Anda hanya memerlukan respons Claude
  * Gunakan `--output-format json` ketika Anda memerlukan log percakapan lengkap
  * Gunakan `--output-format stream-json` untuk output real-time dari setiap giliran percakapan
</Tip>

***

## Tanyakan Claude tentang kemampuannya

Claude memiliki akses bawaan ke dokumentasinya dan dapat menjawab pertanyaan tentang fitur dan keterbatasannya sendiri.

### Contoh pertanyaan

```text  theme={null}
can Claude Code create pull requests?
```

```text  theme={null}
how does Claude Code handle permissions?
```

```text  theme={null}
what skills are available?
```

```text  theme={null}
how do I use MCP with Claude Code?
```

```text  theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text  theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude memberikan jawaban berbasis dokumentasi untuk pertanyaan-pertanyaan ini. Untuk contoh yang dapat dieksekusi dan demonstrasi langsung, lihat bagian alur kerja spesifik di atas.
</Note>

<Tip>
  Tips:

  * Claude selalu memiliki akses ke dokumentasi Claude Code terbaru, terlepas dari versi yang Anda gunakan
  * Ajukan pertanyaan spesifik untuk mendapatkan jawaban terperinci
  * Claude dapat menjelaskan fitur kompleks seperti integrasi MCP, konfigurasi enterprise, dan alur kerja lanjutan
</Tip>

***

## Langkah berikutnya

<CardGroup cols={2}>
  <Card title="Best practices" icon="lightbulb" href="/id/best-practices">
    Pola untuk mendapatkan hasil maksimal dari Claude Code
  </Card>

  <Card title="Cara kerja Claude Code" icon="gear" href="/id/how-claude-code-works">
    Pahami loop agentic dan manajemen konteks
  </Card>

  <Card title="Perluas Claude Code" icon="puzzle-piece" href="/id/features-overview">
    Tambahkan skills, hooks, MCP, subagents, dan plugins
  </Card>

  <Card title="Implementasi referensi" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clone implementasi referensi container pengembangan kami
  </Card>
</CardGroup>
