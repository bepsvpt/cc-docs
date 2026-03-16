> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Perluas Claude dengan skills

> Buat, kelola, dan bagikan skills untuk memperluas kemampuan Claude di Claude Code. Termasuk perintah kustom dan skills bundel.

Skills memperluas apa yang dapat dilakukan Claude. Buat file `SKILL.md` dengan instruksi, dan Claude menambahkannya ke toolkit-nya. Claude menggunakan skills ketika relevan, atau Anda dapat menginvokasinya secara langsung dengan `/skill-name`.

<Note>
  Untuk perintah bawaan seperti `/help` dan `/compact`, lihat [mode interaktif](/id/interactive-mode#built-in-commands).

  **Perintah kustom telah digabungkan ke dalam skills.** File di `.claude/commands/deploy.md` dan skill di `.claude/skills/deploy/SKILL.md` keduanya membuat `/deploy` dan bekerja dengan cara yang sama. File `.claude/commands/` yang ada tetap berfungsi. Skills menambahkan fitur opsional: direktori untuk file pendukung, frontmatter untuk [mengontrol apakah Anda atau Claude menginvokasinya](#control-who-invokes-a-skill), dan kemampuan bagi Claude untuk memuatnya secara otomatis ketika relevan.
</Note>

Skills Claude Code mengikuti standar terbuka [Agent Skills](https://agentskills.io), yang bekerja di berbagai alat AI. Claude Code memperluas standar dengan fitur tambahan seperti [kontrol invokasi](#control-who-invokes-a-skill), [eksekusi subagent](#run-skills-in-a-subagent), dan [injeksi konteks dinamis](#inject-dynamic-context).

## Skills bundel

Skills bundel dikirim dengan Claude Code dan tersedia di setiap sesi. Tidak seperti [perintah bawaan](/id/interactive-mode#built-in-commands), yang menjalankan logika tetap secara langsung, skills bundel berbasis prompt: mereka memberikan Claude playbook terperinci dan membiarkannya mengorkestrasi pekerjaan menggunakan tools-nya. Ini berarti skills bundel dapat menelurkan agen paralel, membaca file, dan beradaptasi dengan codebase Anda.

Anda menginvokasinya skills bundel dengan cara yang sama seperti skill lainnya: ketik `/` diikuti dengan nama skill.

* **`/simplify`**: meninjau file yang baru-baru ini diubah untuk masalah penggunaan kembali kode, kualitas, dan efisiensi, kemudian memperbaikinya. Jalankan setelah mengimplementasikan fitur atau perbaikan bug untuk membersihkan pekerjaan Anda. Ini menelurkan tiga agen review secara paralel (penggunaan kembali kode, kualitas kode, efisiensi), mengagregasi temuan mereka, dan menerapkan perbaikan. Lewatkan teks opsional untuk fokus pada kekhawatiran tertentu: `/simplify focus on memory efficiency`.

* **`/batch <instruction>`**: mengorkestrasi perubahan skala besar di seluruh codebase secara paralel. Berikan deskripsi perubahan dan `/batch` meneliti codebase, menguraikan pekerjaan menjadi 5 hingga 30 unit independen, dan menyajikan rencana untuk persetujuan Anda. Setelah disetujui, ia menelurkan satu agen latar belakang per unit, masing-masing dalam [git worktree](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) yang terisolasi. Setiap agen mengimplementasikan unitnya, menjalankan tes, dan membuka pull request. Memerlukan repositori git. Contoh: `/batch migrate src/ from Solid to React`.

* **`/debug [description]`**: memecahkan masalah sesi Claude Code Anda saat ini dengan membaca log debug sesi. Secara opsional jelaskan masalahnya untuk fokus analisis.

* **`/loop [interval] <prompt>`**: menjalankan prompt berulang kali pada interval sambil sesi tetap terbuka. Claude menguraikan interval, menjadwalkan tugas cron berulang, dan mengonfirmasi ritme. Berguna untuk polling deployment, mengasuh PR, atau menjalankan kembali skill lain secara berkala. Contoh: `/loop 5m check if the deploy finished`. Lihat [Jalankan prompt sesuai jadwal](/id/scheduled-tasks).

* **`/claude-api`**: memuat materi referensi Claude API untuk bahasa proyek Anda (Python, TypeScript, Java, Go, Ruby, C#, PHP, atau cURL) dan referensi Agent SDK untuk Python dan TypeScript. Mencakup tool use, streaming, batches, structured outputs, dan pitfalls umum. Juga diaktifkan secara otomatis ketika kode Anda mengimpor `anthropic`, `@anthropic-ai/sdk`, atau `claude_agent_sdk`.

## Memulai

### Buat skill pertama Anda

Contoh ini membuat skill yang mengajarkan Claude menjelaskan kode menggunakan diagram visual dan analogi. Karena menggunakan frontmatter default, Claude dapat memuatnya secara otomatis ketika Anda bertanya bagaimana sesuatu bekerja, atau Anda dapat menginvokasinya secara langsung dengan `/explain-code`.

<Steps>
  <Step title="Buat direktori skill">
    Buat direktori untuk skill di folder skills pribadi Anda. Skills pribadi tersedia di semua proyek Anda.

    ```bash  theme={null}
    mkdir -p ~/.claude/skills/explain-code
    ```
  </Step>

  <Step title="Tulis SKILL.md">
    Setiap skill memerlukan file `SKILL.md` dengan dua bagian: frontmatter YAML (antara penanda `---`) yang memberi tahu Claude kapan menggunakan skill, dan konten markdown dengan instruksi yang diikuti Claude ketika skill diinvokasinya. Bidang `name` menjadi `/slash-command`, dan `description` membantu Claude memutuskan kapan memuatnya secara otomatis.

    Buat `~/.claude/skills/explain-code/SKILL.md`:

    ```yaml  theme={null}
    ---
    name: explain-code
    description: Menjelaskan kode dengan diagram visual dan analogi. Gunakan saat menjelaskan cara kerja kode, mengajar tentang codebase, atau ketika pengguna bertanya "bagaimana cara kerjanya?"
    ---

    Saat menjelaskan kode, selalu sertakan:

    1. **Mulai dengan analogi**: Bandingkan kode dengan sesuatu dari kehidupan sehari-hari
    2. **Gambar diagram**: Gunakan ASCII art untuk menunjukkan alur, struktur, atau hubungan
    3. **Jelajahi kode**: Jelaskan langkah demi langkah apa yang terjadi
    4. **Sorot gotcha**: Apa kesalahan umum atau kesalahpahaman?

    Jaga penjelasan tetap percakapan. Untuk konsep kompleks, gunakan beberapa analogi.
    ```
  </Step>

  <Step title="Uji skill">
    Anda dapat mengujinya dengan dua cara:

    **Biarkan Claude menginvokasinya secara otomatis** dengan bertanya sesuatu yang cocok dengan deskripsi:

    ```text  theme={null}
    Bagaimana cara kerja kode ini?
    ```

    **Atau invokasinya secara langsung** dengan nama skill:

    ```text  theme={null}
    /explain-code src/auth/login.ts
    ```

    Baik cara mana pun, Claude harus menyertakan analogi dan diagram ASCII dalam penjelasannya.
  </Step>
</Steps>

### Tempat skills berada

Tempat Anda menyimpan skill menentukan siapa yang dapat menggunakannya:

| Lokasi     | Path                                                      | Berlaku untuk                     |
| :--------- | :-------------------------------------------------------- | :-------------------------------- |
| Enterprise | Lihat [pengaturan terkelola](/id/settings#settings-files) | Semua pengguna di organisasi Anda |
| Pribadi    | `~/.claude/skills/<skill-name>/SKILL.md`                  | Semua proyek Anda                 |
| Proyek     | `.claude/skills/<skill-name>/SKILL.md`                    | Proyek ini saja                   |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`                   | Tempat plugin diaktifkan          |

Ketika skills berbagi nama yang sama di berbagai level, lokasi prioritas lebih tinggi menang: enterprise > pribadi > proyek. Skills plugin menggunakan namespace `plugin-name:skill-name`, jadi mereka tidak dapat bertentangan dengan level lain. Jika Anda memiliki file di `.claude/commands/`, file tersebut bekerja dengan cara yang sama, tetapi jika skill dan perintah berbagi nama yang sama, skill mengambil alih.

#### Penemuan otomatis dari direktori bersarang

Ketika Anda bekerja dengan file di subdirektori, Claude Code secara otomatis menemukan skills dari direktori `.claude/skills/` bersarang. Misalnya, jika Anda mengedit file di `packages/frontend/`, Claude Code juga mencari skills di `packages/frontend/.claude/skills/`. Ini mendukung pengaturan monorepo di mana paket memiliki skills mereka sendiri.

Setiap skill adalah direktori dengan `SKILL.md` sebagai titik masuk:

```text  theme={null}
my-skill/
├── SKILL.md           # Instruksi utama (diperlukan)
├── template.md        # Template untuk Claude isi
├── examples/
│   └── sample.md      # Contoh output menunjukkan format yang diharapkan
└── scripts/
    └── validate.sh    # Script Claude dapat jalankan
```

`SKILL.md` berisi instruksi utama dan diperlukan. File lainnya opsional dan memungkinkan Anda membangun skills yang lebih kuat: template untuk Claude isi, contoh output menunjukkan format yang diharapkan, script Claude dapat jalankan, atau dokumentasi referensi terperinci. Referensikan file pendukung ini dari `SKILL.md` Anda sehingga Claude tahu apa yang mereka berisi dan kapan memuatnya. Lihat [Tambahkan file pendukung](#add-supporting-files) untuk detail lebih lanjut.

<Note>
  File di `.claude/commands/` masih bekerja dan mendukung [frontmatter](#frontmatter-reference) yang sama. Skills direkomendasikan karena mendukung fitur tambahan seperti file pendukung.
</Note>

#### Skills dari direktori tambahan

Skills yang didefinisikan di `.claude/skills/` dalam direktori yang ditambahkan melalui `--add-dir` dimuat secara otomatis dan diambil oleh deteksi perubahan langsung, jadi Anda dapat mengeditnya selama sesi tanpa memulai ulang.

<Note>
  File CLAUDE.md dari direktori `--add-dir` tidak dimuat secara default. Untuk memuatnya, atur `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. Lihat [Muat dari direktori tambahan](/id/memory#load-from-additional-directories).
</Note>

## Konfigurasi skills

Skills dikonfigurasi melalui frontmatter YAML di bagian atas `SKILL.md` dan konten markdown yang mengikutinya.

### Jenis konten skill

File skill dapat berisi instruksi apa pun, tetapi memikirkan tentang cara Anda ingin menginvokasinya membantu memandu apa yang harus disertakan:

**Konten referensi** menambahkan pengetahuan yang diterapkan Claude pada pekerjaan Anda saat ini. Konvensi, pola, panduan gaya, pengetahuan domain. Konten ini berjalan inline sehingga Claude dapat menggunakannya bersama konteks percakapan Anda.

```yaml  theme={null}
---
name: api-conventions
description: Pola desain API untuk codebase ini
---

Saat menulis endpoint API:
- Gunakan konvensi penamaan RESTful
- Kembalikan format kesalahan yang konsisten
- Sertakan validasi permintaan
```

**Konten tugas** memberikan Claude instruksi langkah demi langkah untuk tindakan tertentu, seperti deployment, commit, atau pembuatan kode. Ini sering kali tindakan yang ingin Anda invokasinya secara langsung dengan `/skill-name` daripada membiarkan Claude memutuskan kapan menjalankannya. Tambahkan `disable-model-invocation: true` untuk mencegah Claude memicunya secara otomatis.

```yaml  theme={null}
---
name: deploy
description: Deployment aplikasi ke produksi
context: fork
disable-model-invocation: true
---

Deployment aplikasi:
1. Jalankan test suite
2. Build aplikasi
3. Push ke target deployment
```

`SKILL.md` Anda dapat berisi apa pun, tetapi memikirkan tentang cara Anda ingin skill diinvokasinya (oleh Anda, oleh Claude, atau keduanya) dan di mana Anda ingin menjalankannya (inline atau di subagent) membantu memandu apa yang harus disertakan. Untuk skills kompleks, Anda juga dapat [menambahkan file pendukung](#add-supporting-files) untuk menjaga skill utama tetap fokus.

### Referensi frontmatter

Selain konten markdown, Anda dapat mengonfigurasi perilaku skill menggunakan bidang frontmatter YAML antara penanda `---` di bagian atas file `SKILL.md` Anda:

```yaml  theme={null}
---
name: my-skill
description: Apa yang dilakukan skill ini
disable-model-invocation: true
allowed-tools: Read, Grep
---

Instruksi skill Anda di sini...
```

Semua bidang opsional. Hanya `description` yang direkomendasikan sehingga Claude tahu kapan menggunakan skill.

| Bidang                     | Diperlukan       | Deskripsi                                                                                                                                                                          |
| :------------------------- | :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | Tidak            | Nama tampilan untuk skill. Jika dihilangkan, menggunakan nama direktori. Huruf kecil, angka, dan tanda hubung saja (maks 64 karakter).                                             |
| `description`              | Direkomendasikan | Apa yang dilakukan skill dan kapan menggunakannya. Claude menggunakan ini untuk memutuskan kapan menerapkan skill. Jika dihilangkan, menggunakan paragraf pertama konten markdown. |
| `argument-hint`            | Tidak            | Petunjuk ditampilkan selama autocomplete untuk menunjukkan argumen yang diharapkan. Contoh: `[issue-number]` atau `[filename] [format]`.                                           |
| `disable-model-invocation` | Tidak            | Atur ke `true` untuk mencegah Claude memuatnya secara otomatis. Gunakan untuk alur kerja yang ingin Anda picu secara manual dengan `/name`. Default: `false`.                      |
| `user-invocable`           | Tidak            | Atur ke `false` untuk menyembunyikan dari menu `/`. Gunakan untuk pengetahuan latar belakang yang tidak boleh diinvokasinya pengguna secara langsung. Default: `true`.             |
| `allowed-tools`            | Tidak            | Tools yang dapat digunakan Claude tanpa meminta izin ketika skill ini aktif.                                                                                                       |
| `model`                    | Tidak            | Model yang digunakan ketika skill ini aktif.                                                                                                                                       |
| `context`                  | Tidak            | Atur ke `fork` untuk menjalankan dalam konteks subagent yang di-fork.                                                                                                              |
| `agent`                    | Tidak            | Jenis subagent mana yang digunakan ketika `context: fork` diatur.                                                                                                                  |
| `hooks`                    | Tidak            | Hooks yang dibatasi pada siklus hidup skill ini. Lihat [Hooks dalam skills dan agents](/id/hooks#hooks-in-skills-and-agents) untuk format konfigurasi.                             |

#### Substitusi string yang tersedia

Skills mendukung substitusi string untuk nilai dinamis dalam konten skill:

| Variabel               | Deskripsi                                                                                                                                                                                                                                                                            |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | Semua argumen yang dilewatkan saat menginvokasinya skill. Jika `$ARGUMENTS` tidak ada dalam konten, argumen ditambahkan sebagai `ARGUMENTS: <value>`.                                                                                                                                |
| `$ARGUMENTS[N]`        | Akses argumen tertentu berdasarkan indeks berbasis 0, seperti `$ARGUMENTS[0]` untuk argumen pertama.                                                                                                                                                                                 |
| `$N`                   | Singkat untuk `$ARGUMENTS[N]`, seperti `$0` untuk argumen pertama atau `$1` untuk argumen kedua.                                                                                                                                                                                     |
| `${CLAUDE_SESSION_ID}` | ID sesi saat ini. Berguna untuk logging, membuat file khusus sesi, atau menghubungkan output skill dengan sesi.                                                                                                                                                                      |
| `${CLAUDE_SKILL_DIR}`  | Direktori yang berisi file `SKILL.md` skill. Untuk skills plugin, ini adalah subdirektori skill dalam plugin, bukan root plugin. Gunakan ini dalam perintah injeksi bash untuk mereferensikan script atau file yang disertakan dengan skill, terlepas dari direktori kerja saat ini. |

**Contoh menggunakan substitusi:**

```yaml  theme={null}
---
name: session-logger
description: Log aktivitas untuk sesi ini
---

Log berikut ke logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Tambahkan file pendukung

Skills dapat menyertakan beberapa file di direktorinya. Ini menjaga `SKILL.md` fokus pada hal-hal penting sambil membiarkan Claude mengakses materi referensi terperinci hanya saat diperlukan. Dokumen referensi besar, spesifikasi API, atau koleksi contoh tidak perlu dimuat ke dalam konteks setiap kali skill berjalan.

```text  theme={null}
my-skill/
├── SKILL.md (diperlukan - gambaran umum dan navigasi)
├── reference.md (dokumen API terperinci - dimuat saat diperlukan)
├── examples.md (contoh penggunaan - dimuat saat diperlukan)
└── scripts/
    └── helper.py (script utilitas - dijalankan, tidak dimuat)
```

Referensikan file pendukung dari `SKILL.md` Anda sehingga Claude tahu apa yang berisi setiap file dan kapan memuatnya:

```markdown  theme={null}
## Sumber daya tambahan

- Untuk detail API lengkap, lihat [reference.md](reference.md)
- Untuk contoh penggunaan, lihat [examples.md](examples.md)
```

<Tip>Jaga `SKILL.md` di bawah 500 baris. Pindahkan materi referensi terperinci ke file terpisah.</Tip>

### Kontrol siapa yang menginvokasinya skill

Secara default, baik Anda maupun Claude dapat menginvokasinya skill apa pun. Anda dapat mengetik `/skill-name` untuk menginvokasinya secara langsung, dan Claude dapat memuatnya secara otomatis ketika relevan dengan percakapan Anda. Dua bidang frontmatter memungkinkan Anda membatasi ini:

* **`disable-model-invocation: true`**: Hanya Anda yang dapat menginvokasinya skill. Gunakan ini untuk alur kerja dengan efek samping atau yang ingin Anda kontrol waktunya, seperti `/commit`, `/deploy`, atau `/send-slack-message`. Anda tidak ingin Claude memutuskan untuk deploy karena kode Anda terlihat siap.

* **`user-invocable: false`**: Hanya Claude yang dapat menginvokasinya skill. Gunakan ini untuk pengetahuan latar belakang yang tidak dapat ditindaklanjuti sebagai perintah. Skill `legacy-system-context` menjelaskan cara kerja sistem lama. Claude harus tahu ini ketika relevan, tetapi `/legacy-system-context` bukan tindakan bermakna bagi pengguna untuk diambil.

Contoh ini membuat skill deploy yang hanya dapat Anda picu. Bidang `disable-model-invocation: true` mencegah Claude menjalankannya secara otomatis:

```yaml  theme={null}
---
name: deploy
description: Deployment aplikasi ke produksi
disable-model-invocation: true
---

Deployment $ARGUMENTS ke produksi:

1. Jalankan test suite
2. Build aplikasi
3. Push ke target deployment
4. Verifikasi deployment berhasil
```

Berikut adalah cara dua bidang mempengaruhi invokasi dan pemuatan konteks:

| Frontmatter                      | Anda dapat menginvokasinya | Claude dapat menginvokasinya | Kapan dimuat ke dalam konteks                                               |
| :------------------------------- | :------------------------- | :--------------------------- | :-------------------------------------------------------------------------- |
| (default)                        | Ya                         | Ya                           | Deskripsi selalu dalam konteks, skill penuh dimuat saat diinvokasinya       |
| `disable-model-invocation: true` | Ya                         | Tidak                        | Deskripsi tidak dalam konteks, skill penuh dimuat saat Anda menginvokasinya |
| `user-invocable: false`          | Tidak                      | Ya                           | Deskripsi selalu dalam konteks, skill penuh dimuat saat diinvokasinya       |

<Note>
  Dalam sesi reguler, deskripsi skill dimuat ke dalam konteks sehingga Claude tahu apa yang tersedia, tetapi konten skill penuh hanya dimuat saat diinvokasinya. [Subagents dengan skills yang dimuat sebelumnya](/id/sub-agents#preload-skills-into-subagents) bekerja berbeda: konten skill penuh disuntikkan saat startup.
</Note>

### Batasi akses tool

Gunakan bidang `allowed-tools` untuk membatasi tools mana yang dapat digunakan Claude ketika skill aktif. Skill ini membuat mode baca-saja di mana Claude dapat menjelajahi file tetapi tidak memodifikasinya:

```yaml  theme={null}
---
name: safe-reader
description: Baca file tanpa membuat perubahan
allowed-tools: Read, Grep, Glob
---
```

### Lewatkan argumen ke skills

Baik Anda maupun Claude dapat melewatkan argumen saat menginvokasinya skill. Argumen tersedia melalui placeholder `$ARGUMENTS`.

Skill ini memperbaiki masalah GitHub berdasarkan nomor. Placeholder `$ARGUMENTS` diganti dengan apa pun yang mengikuti nama skill:

```yaml  theme={null}
---
name: fix-issue
description: Perbaiki masalah GitHub
disable-model-invocation: true
---

Perbaiki masalah GitHub $ARGUMENTS mengikuti standar coding kami.

1. Baca deskripsi masalah
2. Pahami persyaratan
3. Implementasikan perbaikan
4. Tulis tes
5. Buat commit
```

Ketika Anda menjalankan `/fix-issue 123`, Claude menerima "Perbaiki masalah GitHub 123 mengikuti standar coding kami..."

Jika Anda menginvokasinya skill dengan argumen tetapi skill tidak menyertakan `$ARGUMENTS`, Claude Code menambahkan `ARGUMENTS: <your input>` ke akhir konten skill sehingga Claude masih melihat apa yang Anda ketik.

Untuk mengakses argumen individual berdasarkan posisi, gunakan `$ARGUMENTS[N]` atau yang lebih pendek `$N`:

```yaml  theme={null}
---
name: migrate-component
description: Migrasikan komponen dari satu framework ke framework lain
---

Migrasikan komponen $ARGUMENTS[0] dari $ARGUMENTS[1] ke $ARGUMENTS[2].
Pertahankan semua perilaku dan tes yang ada.
```

Menjalankan `/migrate-component SearchBar React Vue` mengganti `$ARGUMENTS[0]` dengan `SearchBar`, `$ARGUMENTS[1]` dengan `React`, dan `$ARGUMENTS[2]` dengan `Vue`. Skill yang sama menggunakan singkat `$N`:

```yaml  theme={null}
---
name: migrate-component
description: Migrasikan komponen dari satu framework ke framework lain
---

Migrasikan komponen $0 dari $1 ke $2.
Pertahankan semua perilaku dan tes yang ada.
```

## Pola lanjutan

### Injeksi konteks dinamis

Sintaks `!`command\`\` menjalankan perintah shell sebelum konten skill dikirim ke Claude. Output perintah mengganti placeholder, jadi Claude menerima data aktual, bukan perintah itu sendiri.

Skill ini merangkum pull request dengan mengambil data PR langsung dengan GitHub CLI. Perintah `!`gh pr diff\`\` dan lainnya berjalan terlebih dahulu, dan output mereka dimasukkan ke dalam prompt:

```yaml  theme={null}
---
name: pr-summary
description: Rangkum perubahan dalam pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Konteks pull request
- PR diff: !`gh pr diff`
- Komentar PR: !`gh pr view --comments`
- File yang diubah: !`gh pr diff --name-only`

## Tugas Anda
Rangkum pull request ini...
```

Ketika skill ini berjalan:

1. Setiap `!`command\`\` dijalankan segera (sebelum Claude melihat apa pun)
2. Output mengganti placeholder dalam konten skill
3. Claude menerima prompt yang sepenuhnya dirender dengan data PR aktual

Ini adalah preprocessing, bukan sesuatu yang dijalankan Claude. Claude hanya melihat hasil akhir.

<Tip>
  Untuk mengaktifkan [extended thinking](/id/common-workflows#use-extended-thinking-thinking-mode) dalam skill, sertakan kata "ultrathink" di mana pun dalam konten skill Anda.
</Tip>

### Jalankan skills dalam subagent

Tambahkan `context: fork` ke frontmatter Anda ketika Anda ingin skill berjalan dalam isolasi. Konten skill menjadi prompt yang mendorong subagent. Ini tidak akan memiliki akses ke riwayat percakapan Anda.

<Warning>
  `context: fork` hanya masuk akal untuk skills dengan instruksi eksplisit. Jika skill Anda berisi pedoman seperti "gunakan konvensi API ini" tanpa tugas, subagent menerima pedoman tetapi tidak ada prompt yang dapat ditindaklanjuti, dan kembali tanpa output bermakna.
</Warning>

Skills dan [subagents](/id/sub-agents) bekerja bersama dalam dua arah:

| Pendekatan                      | System prompt                             | Tugas                 | Juga memuat                               |
| :------------------------------ | :---------------------------------------- | :-------------------- | :---------------------------------------- |
| Skill dengan `context: fork`    | Dari jenis agent (`Explore`, `Plan`, dll) | Konten SKILL.md       | CLAUDE.md                                 |
| Subagent dengan bidang `skills` | Badan markdown subagent                   | Pesan delegasi Claude | Skills yang dimuat sebelumnya + CLAUDE.md |

Dengan `context: fork`, Anda menulis tugas dalam skill Anda dan memilih jenis agent untuk menjalankannya. Untuk kebalikannya (mendefinisikan subagent kustom yang menggunakan skills sebagai materi referensi), lihat [Subagents](/id/sub-agents#preload-skills-into-subagents).

#### Contoh: Skill penelitian menggunakan agen Explore

Skill ini menjalankan penelitian dalam agen Explore yang di-fork. Konten skill menjadi tugas, dan agen menyediakan tools baca-saja yang dioptimalkan untuk eksplorasi codebase:

```yaml  theme={null}
---
name: deep-research
description: Teliti topik secara menyeluruh
context: fork
agent: Explore
---

Teliti $ARGUMENTS secara menyeluruh:

1. Temukan file relevan menggunakan Glob dan Grep
2. Baca dan analisis kode
3. Rangkum temuan dengan referensi file tertentu
```

Ketika skill ini berjalan:

1. Konteks terisolasi baru dibuat
2. Subagent menerima konten skill sebagai promptnya ("Teliti \$ARGUMENTS secara menyeluruh...")
3. Bidang `agent` menentukan lingkungan eksekusi (model, tools, dan izin)
4. Hasil dirangkum dan dikembalikan ke percakapan utama Anda

Bidang `agent` menentukan konfigurasi subagent mana yang digunakan. Opsi termasuk agen bawaan (`Explore`, `Plan`, `general-purpose`) atau subagent kustom apa pun dari `.claude/agents/`. Jika dihilangkan, menggunakan `general-purpose`.

### Batasi akses skill Claude

Secara default, Claude dapat menginvokasinya skill apa pun yang tidak memiliki `disable-model-invocation: true` diatur. Skills yang mendefinisikan `allowed-tools` memberikan Claude akses ke tools tersebut tanpa persetujuan per-penggunaan ketika skill aktif. Pengaturan [izin](/id/permissions) Anda masih mengatur perilaku persetujuan baseline untuk semua tools lainnya. Perintah bawaan seperti `/compact` dan `/init` tidak tersedia melalui tool Skill.

Tiga cara untuk mengontrol skills mana yang dapat diinvokasinya Claude:

**Nonaktifkan semua skills** dengan menolak tool Skill dalam `/permissions`:

```text  theme={null}
# Tambahkan ke aturan penolakan:
Skill
```

**Izinkan atau tolak skills tertentu** menggunakan [aturan izin](/id/permissions):

```text  theme={null}
# Izinkan hanya skills tertentu
Skill(commit)
Skill(review-pr *)

# Tolak skills tertentu
Skill(deploy *)
```

Sintaks izin: `Skill(name)` untuk kecocokan tepat, `Skill(name *)` untuk kecocokan awalan dengan argumen apa pun.

**Sembunyikan skills individual** dengan menambahkan `disable-model-invocation: true` ke frontmatter mereka. Ini menghapus skill dari konteks Claude sepenuhnya.

<Note>
  Bidang `user-invocable` hanya mengontrol visibilitas menu, bukan akses tool Skill. Gunakan `disable-model-invocation: true` untuk memblokir invokasi pemrograman.
</Note>

## Bagikan skills

Skills dapat didistribusikan pada cakupan berbeda tergantung pada audiens Anda:

* **Skills proyek**: Commit `.claude/skills/` ke kontrol versi
* **Plugins**: Buat direktori `skills/` dalam [plugin](/id/plugins) Anda
* **Terkelola**: Deployment di seluruh organisasi melalui [pengaturan terkelola](/id/settings#settings-files)

### Hasilkan output visual

Skills dapat membundel dan menjalankan script dalam bahasa apa pun, memberikan Claude kemampuan di luar apa yang mungkin dalam prompt tunggal. Satu pola yang kuat adalah menghasilkan output visual: file HTML interaktif yang terbuka di browser Anda untuk menjelajahi data, debugging, atau membuat laporan.

Contoh ini membuat penjelajah codebase: tampilan pohon interaktif di mana Anda dapat memperluas dan menciutkan direktori, melihat ukuran file sekilas, dan mengidentifikasi jenis file berdasarkan warna.

Buat direktori Skill:

```bash  theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Buat `~/.claude/skills/codebase-visualizer/SKILL.md`. Deskripsi memberi tahu Claude kapan mengaktifkan Skill ini, dan instruksi memberi tahu Claude untuk menjalankan script bundel:

````yaml  theme={null}
---
name: codebase-visualizer
description: Hasilkan visualisasi pohon interaktif yang dapat diciutkan dari codebase Anda. Gunakan saat menjelajahi repo baru, memahami struktur proyek, atau mengidentifikasi file besar.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Hasilkan tampilan pohon HTML interaktif yang menunjukkan struktur file proyek Anda dengan direktori yang dapat diciutkan.

## Penggunaan

Jalankan script visualisasi dari root proyek Anda:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```text

Ini membuat `codebase-map.html` di direktori saat ini dan membukanya di browser default Anda.

## Apa yang ditampilkan visualisasi

- **Direktori yang dapat diciutkan**: Klik folder untuk memperluas/menciutkan
- **Ukuran file**: Ditampilkan di sebelah setiap file
- **Warna**: Warna berbeda untuk jenis file berbeda
- **Total direktori**: Menunjukkan ukuran agregat setiap folder
````

Buat `~/.claude/skills/codebase-visualizer/scripts/visualize.py`. Script ini memindai pohon direktori dan menghasilkan file HTML mandiri dengan:

* **Sidebar ringkasan** menampilkan jumlah file, jumlah direktori, ukuran total, dan jumlah jenis file
* **Bagan batang** memecah codebase berdasarkan jenis file (8 teratas berdasarkan ukuran)
* **Pohon yang dapat diciutkan** di mana Anda dapat memperluas dan menciutkan direktori, dengan indikator jenis file berkode warna

Script memerlukan Python tetapi hanya menggunakan library bawaan, jadi tidak ada paket untuk diinstal:

```python expandable theme={null}
#!/usr/bin/env python3
"""Hasilkan visualisasi pohon interaktif yang dapat diciutkan dari codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

Untuk menguji, buka Claude Code di proyek apa pun dan tanya "Visualisasi codebase ini." Claude menjalankan script, menghasilkan `codebase-map.html`, dan membukanya di browser Anda.

Pola ini bekerja untuk output visual apa pun: grafik dependensi, laporan cakupan tes, dokumentasi API, atau visualisasi skema database. Script bundel melakukan pekerjaan berat sementara Claude menangani orkestrasi.

## Troubleshooting

### Skill tidak terpicu

Jika Claude tidak menggunakan skill Anda saat diharapkan:

1. Periksa deskripsi mencakup kata kunci yang akan dikatakan pengguna secara alami
2. Verifikasi skill muncul dalam `What skills are available?`
3. Coba rephrase permintaan Anda agar lebih cocok dengan deskripsi
4. Invokasinya secara langsung dengan `/skill-name` jika skill dapat diinvokasinya pengguna

### Skill terpicu terlalu sering

Jika Claude menggunakan skill Anda saat Anda tidak menginginkannya:

1. Buat deskripsi lebih spesifik
2. Tambahkan `disable-model-invocation: true` jika Anda hanya menginginkan invokasi manual

### Claude tidak melihat semua skills saya

Deskripsi skill dimuat ke dalam konteks sehingga Claude tahu apa yang tersedia. Jika Anda memiliki banyak skills, mereka mungkin melebihi anggaran karakter. Anggaran diskalakan secara dinamis pada 2% dari jendela konteks, dengan fallback 16.000 karakter. Jalankan `/context` untuk memeriksa peringatan tentang skills yang dikecualikan.

Untuk mengganti batas, atur variabel lingkungan `SLASH_COMMAND_TOOL_CHAR_BUDGET`.

## Sumber daya terkait

* **[Subagents](/id/sub-agents)**: delegasikan tugas ke agen khusus
* **[Plugins](/id/plugins)**: paket dan distribusikan skills dengan ekstensi lainnya
* **[Hooks](/id/hooks)**: otomatisasi alur kerja di sekitar peristiwa tool
* **[Memory](/id/memory)**: kelola file CLAUDE.md untuk konteks persisten
* **[Mode interaktif](/id/interactive-mode#built-in-commands)**: perintah bawaan dan pintasan
* **[Permissions](/id/permissions)**: kontrol akses tool dan skill
