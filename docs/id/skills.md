> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Perluas Claude dengan skills

> Buat, kelola, dan bagikan skills untuk memperluas kemampuan Claude di Claude Code. Termasuk perintah kustom dan skills bundel.

Skills memperluas apa yang dapat dilakukan Claude. Buat file `SKILL.md` dengan instruksi, dan Claude menambahkannya ke toolkit-nya. Claude menggunakan skills saat relevan, atau Anda dapat menginvokasinya secara langsung dengan `/skill-name`.

Buat skill ketika Anda terus menempel instruksi yang sama, checklist, atau prosedur multi-langkah ke dalam chat, atau ketika bagian dari CLAUDE.md telah berkembang menjadi prosedur daripada fakta. Tidak seperti konten CLAUDE.md, badan skill hanya dimuat saat digunakan, jadi materi referensi yang panjang hampir tidak ada biayanya sampai Anda membutuhkannya.

<Note>
  Untuk perintah bawaan seperti `/help` dan `/compact`, dan skills bundel seperti `/debug` dan `/simplify`, lihat [referensi perintah](/id/commands).

  **Perintah kustom telah digabungkan ke dalam skills.** File di `.claude/commands/deploy.md` dan skill di `.claude/skills/deploy/SKILL.md` keduanya membuat `/deploy` dan bekerja dengan cara yang sama. File `.claude/commands/` yang ada tetap berfungsi. Skills menambahkan fitur opsional: direktori untuk file pendukung, frontmatter untuk [mengontrol apakah Anda atau Claude menginvokasinya](#control-who-invokes-a-skill), dan kemampuan bagi Claude untuk memuatnya secara otomatis saat relevan.
</Note>

Skills Claude Code mengikuti standar terbuka [Agent Skills](https://agentskills.io), yang bekerja di berbagai alat AI. Claude Code memperluas standar dengan fitur tambahan seperti [kontrol invokasi](#control-who-invokes-a-skill), [eksekusi subagent](#run-skills-in-a-subagent), dan [injeksi konteks dinamis](#inject-dynamic-context).

## Skills bundel

Claude Code menyertakan serangkaian skills bundel yang tersedia di setiap sesi, termasuk `/simplify`, `/batch`, `/debug`, `/loop`, dan `/claude-api`. Tidak seperti sebagian besar perintah bawaan, yang menjalankan logika tetap secara langsung, skills bundel berbasis prompt: mereka memberikan Claude instruksi terperinci dan membiarkannya mengorkestrasi pekerjaan menggunakan tools-nya. Anda menginvokasinya dengan cara yang sama seperti skill lainnya, dengan mengetik `/` diikuti dengan nama skill.

Skills bundel terdaftar bersama perintah bawaan dalam [referensi perintah](/id/commands), ditandai **Skill** di kolom Tujuan.

## Memulai

### Buat skill pertama Anda

Contoh ini membuat skill yang merangkum perubahan yang belum di-commit dalam repositori git Anda dan menandai apa pun yang berisiko. Ini menarik diff langsung ke dalam prompt sebelum Claude membacanya, sehingga respons didasarkan pada pohon kerja aktual Anda daripada apa yang dapat Claude tebak dari file terbuka. Claude memuat skill secara otomatis saat Anda bertanya tentang perubahan Anda, atau Anda dapat menginvokasinya secara langsung dengan `/summarize-changes`.

<Steps>
  <Step title="Buat direktori skill">
    Buat direktori untuk skill di folder skills pribadi Anda. Skills pribadi tersedia di semua proyek Anda.

    ```bash theme={null}
    mkdir -p ~/.claude/skills/summarize-changes
    ```
  </Step>

  <Step title="Tulis SKILL.md">
    Setiap skill memerlukan file `SKILL.md` dengan dua bagian: frontmatter YAML antara penanda `---` yang memberi tahu Claude kapan menggunakan skill, dan konten markdown dengan instruksi yang diikuti Claude saat skill dijalankan. Nama direktori menjadi perintah yang Anda ketik, dan `description` membantu Claude memutuskan kapan memuatnya secara otomatis.

    Simpan ini ke `~/.claude/skills/summarize-changes/SKILL.md`:

    ```yaml theme={null}
    ---
    description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
    ---

    ## Current changes

    !`git diff HEAD`

    ## Instructions

    Summarize the changes above in two or three bullet points, then list any risks you notice such as missing error handling, hardcoded values, or tests that need updating. If the diff is empty, say there are no uncommitted changes.
    ```

    Baris `` !`git diff HEAD` `` menggunakan [injeksi konteks dinamis](#inject-dynamic-context): Claude Code menjalankan perintah dan mengganti baris dengan outputnya sebelum Claude melihat konten skill, sehingga instruksi tiba dengan diff saat ini sudah inline.
  </Step>

  <Step title="Uji skill">
    Buka proyek git, buat edit kecil ke file apa pun, dan mulai Claude Code dengan menjalankan `claude`. Anda dapat menguji skill dengan dua cara.

    **Biarkan Claude menginvokasinya secara otomatis** dengan menanyakan sesuatu yang cocok dengan deskripsi:

    ```text theme={null}
    What did I change?
    ```

    **Atau invokasinya secara langsung** dengan nama skill:

    ```text theme={null}
    /summarize-changes
    ```

    Baik cara apa pun, Claude harus merespons dengan ringkasan singkat edit Anda dan daftar risiko.
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

Ketika skills berbagi nama yang sama di berbagai level, enterprise menggantikan pribadi, dan pribadi menggantikan proyek. Skills plugin menggunakan namespace `plugin-name:skill-name`, jadi mereka tidak dapat bertentangan dengan level lain. Jika Anda memiliki file di `.claude/commands/`, file tersebut bekerja dengan cara yang sama, tetapi jika skill dan perintah berbagi nama yang sama, skill mengambil alih.

#### Deteksi perubahan langsung

Claude Code memantau direktori skill untuk perubahan file. Menambahkan, mengedit, atau menghapus skill di bawah `~/.claude/skills/`, proyek `.claude/skills/`, atau `.claude/skills/` di dalam direktori `--add-dir` berlaku dalam sesi saat ini tanpa memulai ulang. Membuat direktori skills tingkat atas yang tidak ada saat sesi dimulai memerlukan memulai ulang Claude Code sehingga direktori baru dapat dipantau.

#### Penemuan otomatis dari direktori induk dan bersarang

Project skills memuat dari `.claude/skills/` di direktori awal Anda dan di setiap direktori induk hingga akar repositori, jadi memulai Claude di subdirektori masih mengambil skills yang ditentukan di akar. Saat Anda bekerja dengan file di subdirektori di bawah direktori awal Anda, Claude Code juga menemukan skills dari direktori `.claude/skills/` bersarang sesuai permintaan. Misalnya, jika Anda mengedit file di `packages/frontend/`, Claude Code juga mencari skills di `packages/frontend/.claude/skills/`. Ini mendukung pengaturan monorepo di mana paket memiliki skills mereka sendiri.

Setiap skill adalah direktori dengan `SKILL.md` sebagai titik masuk:

```text theme={null}
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

`SKILL.md` berisi instruksi utama dan diperlukan. File lainnya opsional dan memungkinkan Anda membangun skills yang lebih kuat: template untuk diisi Claude, contoh output yang menunjukkan format yang diharapkan, script yang dapat dijalankan Claude, atau dokumentasi referensi terperinci. Referensikan file pendukung dari `SKILL.md` Anda sehingga Claude tahu apa yang mereka berisi dan kapan memuatnya. Lihat [Tambahkan file pendukung](#add-supporting-files) untuk detail lebih lanjut.

<Note>
  File di `.claude/commands/` masih berfungsi dan mendukung [frontmatter](#frontmatter-reference) yang sama. Skills direkomendasikan karena mendukung fitur tambahan seperti file pendukung.
</Note>

#### Skills dari direktori tambahan

Bendera `--add-dir` [memberikan akses file](/id/permissions#additional-directories-grant-file-access-not-configuration) daripada penemuan konfigurasi, tetapi skills adalah pengecualian: `.claude/skills/` dalam direktori yang ditambahkan dimuat secara otomatis. Lihat [Deteksi perubahan langsung](#live-change-detection) untuk bagaimana edit diambil selama sesi.

Konfigurasi `.claude/` lainnya seperti subagents, perintah, dan gaya output tidak dimuat dari direktori tambahan. Lihat [tabel pengecualian](/id/permissions#additional-directories-grant-file-access-not-configuration) untuk daftar lengkap apa yang dimuat dan tidak dimuat, serta cara yang direkomendasikan untuk berbagi konfigurasi di seluruh proyek.

<Note>
  File CLAUDE.md dari direktori `--add-dir` tidak dimuat secara default. Untuk memuatnya, atur `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. Lihat [Muat dari direktori tambahan](/id/memory#load-from-additional-directories).
</Note>

## Konfigurasi skills

Skills dikonfigurasi melalui frontmatter YAML di bagian atas `SKILL.md` dan konten markdown yang mengikutinya.

### Jenis konten skill

File skill dapat berisi instruksi apa pun, tetapi memikirkan bagaimana Anda ingin menginvokasinya membantu memandu apa yang harus disertakan:

**Konten referensi** menambahkan pengetahuan yang diterapkan Claude pada pekerjaan Anda saat ini. Konvensi, pola, panduan gaya, pengetahuan domain. Konten ini berjalan inline sehingga Claude dapat menggunakannya bersama konteks percakapan Anda.

```yaml theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Konten tugas** memberikan Claude instruksi langkah demi langkah untuk tindakan spesifik, seperti deployment, commit, atau pembuatan kode. Ini sering kali tindakan yang ingin Anda invokasinya secara langsung dengan `/skill-name` daripada membiarkan Claude memutuskan kapan menjalankannya. Tambahkan `disable-model-invocation: true` untuk mencegah Claude memicunya secara otomatis.

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

`SKILL.md` Anda dapat berisi apa pun, tetapi memikirkan bagaimana Anda ingin skill diinvokasinya (oleh Anda, oleh Claude, atau keduanya) dan di mana Anda ingin menjalankannya (inline atau di subagent) membantu memandu apa yang harus disertakan. Untuk skills kompleks, Anda juga dapat [menambahkan file pendukung](#add-supporting-files) untuk menjaga skill utama tetap fokus.

Jaga isi itu sendiri tetap ringkas. Setelah skill dimuat, kontennya [tetap dalam konteks di seluruh giliran](#skill-content-lifecycle), jadi setiap baris adalah biaya token berulang. Nyatakan apa yang harus dilakukan daripada menceritakan bagaimana atau mengapa, dan terapkan tes keringkasan yang sama yang akan Anda lakukan untuk [konten CLAUDE.md](/id/best-practices#write-an-effective-claude-md).

### Referensi frontmatter

Selain konten markdown, Anda dapat mengonfigurasi perilaku skill menggunakan bidang frontmatter YAML antara penanda `---` di bagian atas file `SKILL.md` Anda:

```yaml theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

Semua bidang opsional. Hanya `description` yang direkomendasikan sehingga Claude tahu kapan menggunakan skill.

| Bidang                     | Diperlukan       | Deskripsi                                                                                                                                                                                                                                                                                                                                              |
| :------------------------- | :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | Tidak            | Nama tampilan untuk skill. Jika dihilangkan, menggunakan nama direktori. Huruf kecil, angka, dan tanda hubung saja (maks 64 karakter).                                                                                                                                                                                                                 |
| `description`              | Direkomendasikan | Apa yang dilakukan skill dan kapan menggunakannya. Claude menggunakan ini untuk memutuskan kapan menerapkan skill. Jika dihilangkan, menggunakan paragraf pertama konten markdown. Depankan kasus penggunaan utama: teks gabungan `description` dan `when_to_use` dipotong pada 1.536 karakter dalam daftar skill untuk mengurangi penggunaan konteks. |
| `when_to_use`              | Tidak            | Konteks tambahan untuk kapan Claude harus menginvokasinya skill, seperti frasa pemicu atau permintaan contoh. Ditambahkan ke `description` dalam daftar skill dan dihitung terhadap batas 1.536 karakter.                                                                                                                                              |
| `argument-hint`            | Tidak            | Petunjuk yang ditampilkan selama autocomplete untuk menunjukkan argumen yang diharapkan. Contoh: `[issue-number]` atau `[filename] [format]`.                                                                                                                                                                                                          |
| `arguments`                | Tidak            | Argumen posisional bernama untuk [substitusi `$name`](#available-string-substitutions) dalam konten skill. Menerima string yang dipisahkan spasi atau daftar YAML. Nama memetakan ke posisi argumen secara berurutan.                                                                                                                                  |
| `disable-model-invocation` | Tidak            | Atur ke `true` untuk mencegah Claude memuat skill ini secara otomatis. Gunakan untuk workflow yang ingin Anda picu secara manual dengan `/name`. Juga mencegah skill dari [dimuat sebelumnya ke dalam subagents](/id/sub-agents#preload-skills-into-subagents). Default: `false`.                                                                      |
| `user-invocable`           | Tidak            | Atur ke `false` untuk menyembunyikan dari menu `/`. Gunakan untuk pengetahuan latar belakang yang tidak boleh diinvokasinya pengguna secara langsung. Default: `true`.                                                                                                                                                                                 |
| `allowed-tools`            | Tidak            | Tools yang dapat digunakan Claude tanpa meminta izin saat skill ini aktif. Menerima string yang dipisahkan spasi atau daftar YAML.                                                                                                                                                                                                                     |
| `model`                    | Tidak            | Model yang digunakan saat skill ini aktif. Penggantian berlaku untuk sisa giliran saat ini dan tidak disimpan ke pengaturan; model sesi dilanjutkan pada prompt Anda berikutnya. Menerima nilai yang sama seperti [`/model`](/id/model-config), atau `inherit` untuk menjaga model aktif.                                                              |
| `effort`                   | Tidak            | [Effort level](/id/model-config#adjust-effort-level) saat skill ini aktif. Mengganti effort level sesi. Default: mewarisi dari sesi. Opsi: `low`, `medium`, `high`, `xhigh`, `max`; level yang tersedia tergantung pada model.                                                                                                                         |
| `context`                  | Tidak            | Atur ke `fork` untuk menjalankan dalam konteks subagent yang di-fork.                                                                                                                                                                                                                                                                                  |
| `agent`                    | Tidak            | Jenis subagent mana yang digunakan saat `context: fork` diatur.                                                                                                                                                                                                                                                                                        |
| `hooks`                    | Tidak            | Hooks yang dibatasi pada lifecycle skill ini. Lihat [Hooks dalam skills dan agents](/id/hooks#hooks-in-skills-and-agents) untuk format konfigurasi.                                                                                                                                                                                                    |
| `paths`                    | Tidak            | Pola glob yang membatasi kapan skill ini diaktifkan. Menerima string yang dipisahkan koma atau daftar YAML. Ketika diatur, Claude memuat skill secara otomatis hanya saat bekerja dengan file yang cocok dengan pola. Menggunakan format yang sama seperti [aturan khusus path](/id/memory#path-specific-rules).                                       |
| `shell`                    | Tidak            | Shell yang digunakan untuk `` !`command` `` dan ` ```! ` blocks dalam skill ini. Menerima `bash` (default) atau `powershell`. Mengatur `powershell` menjalankan perintah shell inline melalui PowerShell di Windows. Memerlukan `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.                                                                                   |

#### Substitusi string yang tersedia

Skills mendukung substitusi string untuk nilai dinamis dalam konten skill:

| Variabel               | Deskripsi                                                                                                                                                                                                                                                                            |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | Semua argumen yang dilewatkan saat menginvokasinya skill. Jika `$ARGUMENTS` tidak ada dalam konten, argumen ditambahkan sebagai `ARGUMENTS: <value>`.                                                                                                                                |
| `$ARGUMENTS[N]`        | Akses argumen spesifik berdasarkan indeks berbasis 0, seperti `$ARGUMENTS[0]` untuk argumen pertama.                                                                                                                                                                                 |
| `$N`                   | Singkat untuk `$ARGUMENTS[N]`, seperti `$0` untuk argumen pertama atau `$1` untuk argumen kedua.                                                                                                                                                                                     |
| `$name`                | Argumen bernama yang dideklarasikan dalam daftar frontmatter [`arguments`](#frontmatter-reference). Nama memetakan ke posisi secara berurutan, jadi dengan `arguments: [issue, branch]` placeholder `$issue` berkembang menjadi argumen pertama dan `$branch` menjadi argumen kedua. |
| `${CLAUDE_SESSION_ID}` | ID sesi saat ini. Berguna untuk logging, membuat file khusus sesi, atau mengkorelasikan output skill dengan sesi.                                                                                                                                                                    |
| `${CLAUDE_EFFORT}`     | Effort level saat ini: `low`, `medium`, `high`, `xhigh`, atau `max`. Gunakan ini untuk menyesuaikan instruksi skill dengan pengaturan effort aktif.                                                                                                                                  |
| `${CLAUDE_SKILL_DIR}`  | Direktori yang berisi file `SKILL.md` skill. Untuk skills plugin, ini adalah subdirektori skill dalam plugin, bukan root plugin. Gunakan ini dalam perintah injeksi bash untuk mereferensikan script atau file yang dikemas dengan skill, terlepas dari direktori kerja saat ini.    |

Argumen yang diindeks menggunakan quoting gaya shell, jadi bungkus nilai multi-kata dalam tanda kutip untuk meneruskannya sebagai argumen tunggal. Misalnya, `/my-skill "hello world" second` membuat `$0` berkembang menjadi `hello world` dan `$1` menjadi `second`. Placeholder `$ARGUMENTS` selalu berkembang menjadi string argumen lengkap seperti yang diketik.

**Contoh menggunakan substitusi:**

```yaml theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Tambahkan file pendukung

Skills dapat menyertakan beberapa file di direktorinya. Ini menjaga `SKILL.md` tetap fokus pada hal-hal penting sambil membiarkan Claude mengakses materi referensi terperinci hanya saat diperlukan. Dokumen referensi besar, spesifikasi API, atau koleksi contoh tidak perlu dimuat ke dalam konteks setiap kali skill berjalan.

```text theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

Referensikan file pendukung dari `SKILL.md` Anda sehingga Claude tahu apa yang berisi setiap file dan kapan memuatnya:

```markdown theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>Jaga `SKILL.md` di bawah 500 baris. Pindahkan materi referensi terperinci ke file terpisah.</Tip>

### Kontrol siapa yang menginvokasinya skill

Secara default, baik Anda maupun Claude dapat menginvokasinya skill apa pun. Anda dapat mengetik `/skill-name` untuk menginvokasinya secara langsung, dan Claude dapat memuatnya secara otomatis saat relevan dengan percakapan Anda. Dua bidang frontmatter memungkinkan Anda membatasi ini:

* **`disable-model-invocation: true`**: Hanya Anda yang dapat menginvokasinya skill. Gunakan ini untuk workflow dengan efek samping atau yang ingin Anda kontrol waktu, seperti `/commit`, `/deploy`, atau `/send-slack-message`. Anda tidak ingin Claude memutuskan untuk deploy karena kode Anda terlihat siap.

* **`user-invocable: false`**: Hanya Claude yang dapat menginvokasinya skill. Gunakan ini untuk pengetahuan latar belakang yang tidak dapat ditindaklanjuti sebagai perintah. Skill `legacy-system-context` menjelaskan bagaimana sistem lama bekerja. Claude harus tahu ini saat relevan, tetapi `/legacy-system-context` bukan tindakan yang bermakna bagi pengguna untuk diambil.

Contoh ini membuat skill deploy yang hanya dapat Anda picu. Bidang `disable-model-invocation: true` mencegah Claude menjalankannya secara otomatis:

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

Berikut adalah bagaimana dua bidang mempengaruhi invokasi dan pemuatan konteks:

| Frontmatter                      | Anda dapat menginvokasinya | Claude dapat menginvokasinya | Saat dimuat ke dalam konteks                                                |
| :------------------------------- | :------------------------- | :--------------------------- | :-------------------------------------------------------------------------- |
| (default)                        | Ya                         | Ya                           | Deskripsi selalu dalam konteks, skill penuh dimuat saat diinvokasinya       |
| `disable-model-invocation: true` | Ya                         | Tidak                        | Deskripsi tidak dalam konteks, skill penuh dimuat saat Anda menginvokasinya |
| `user-invocable: false`          | Tidak                      | Ya                           | Deskripsi selalu dalam konteks, skill penuh dimuat saat diinvokasinya       |

<Note>
  Dalam sesi reguler, deskripsi skill dimuat ke dalam konteks sehingga Claude tahu apa yang tersedia, tetapi konten skill penuh hanya dimuat saat diinvokasinya. [Subagents dengan skills yang dimuat sebelumnya](/id/sub-agents#preload-skills-into-subagents) bekerja berbeda: konten skill penuh disuntikkan saat startup.
</Note>

### Lifecycle konten skill

Saat Anda atau Claude menginvokasinya skill, konten `SKILL.md` yang dirender memasuki percakapan sebagai pesan tunggal dan tetap di sana untuk sisa sesi. Claude Code tidak membaca ulang file skill pada giliran berikutnya, jadi tulis panduan yang harus berlaku sepanjang tugas sebagai instruksi berdiri daripada langkah satu kali.

[Auto-compaction](/id/how-claude-code-works#when-context-fills-up) membawa skills yang diinvokasinya maju dalam anggaran token. Ketika percakapan dirangkum untuk membebaskan konteks, Claude Code melampirkan kembali invokasi skill terbaru setelah ringkasan, menjaga 5.000 token pertama dari masing-masing. Skills yang dilampirkan kembali berbagi anggaran gabungan 25.000 token. Claude Code mengisi anggaran ini mulai dari skill yang paling baru diinvokasinya, jadi skills yang lebih lama dapat dijatuhkan sepenuhnya setelah compaction jika Anda telah menginvokasinya banyak dalam satu sesi.

Jika skill tampaknya berhenti mempengaruhi perilaku setelah respons pertama, konten biasanya masih ada dan model memilih tools atau pendekatan lain. Perkuat deskripsi skill dan instruksi sehingga model terus menyukainya, atau gunakan [hooks](/id/hooks) untuk menerapkan perilaku secara deterministik. Jika skill besar atau Anda menginvokasinya beberapa yang lain setelahnya, invokasinya kembali setelah compaction untuk mengembalikan konten penuh.

### Pra-setujui tools untuk skill

Bidang `allowed-tools` memberikan izin untuk tools yang terdaftar saat skill aktif, sehingga Claude dapat menggunakannya tanpa meminta persetujuan Anda. Ini tidak membatasi tools mana yang tersedia: setiap tool tetap dapat dipanggil, dan [pengaturan izin](/id/permissions) Anda masih mengatur tools yang tidak terdaftar.

Untuk skills yang diperiksa ke dalam direktori `.claude/skills/` proyek, `allowed-tools` berlaku setelah Anda menerima dialog kepercayaan workspace untuk folder itu, sama seperti aturan izin dalam `.claude/settings.json`. Tinjau skills proyek sebelum mempercayai repositori, karena skill dapat memberikan dirinya sendiri akses tools yang luas.

Skill ini memungkinkan Claude menjalankan perintah git tanpa persetujuan per-penggunaan kapan pun Anda menginvokasinya:

```yaml theme={null}
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

Untuk memblokir skill dari menggunakan tools tertentu, tambahkan aturan deny dalam [pengaturan izin](/id/permissions) Anda sebagai gantinya.

### Lewatkan argumen ke skills

Baik Anda maupun Claude dapat melewatkan argumen saat menginvokasinya skill. Argumen tersedia melalui placeholder `$ARGUMENTS`.

Skill ini memperbaiki masalah GitHub berdasarkan nomor. Placeholder `$ARGUMENTS` diganti dengan apa pun yang mengikuti nama skill:

```yaml theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

Saat Anda menjalankan `/fix-issue 123`, Claude menerima "Fix GitHub issue 123 following our coding standards..."

Jika Anda menginvokasinya skill dengan argumen tetapi skill tidak menyertakan `$ARGUMENTS`, Claude Code menambahkan `ARGUMENTS: <your input>` ke akhir konten skill sehingga Claude masih melihat apa yang Anda ketik.

Untuk mengakses argumen individual berdasarkan posisi, gunakan `$ARGUMENTS[N]` atau yang lebih pendek `$N`:

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

Menjalankan `/migrate-component SearchBar React Vue` mengganti `$ARGUMENTS[0]` dengan `SearchBar`, `$ARGUMENTS[1]` dengan `React`, dan `$ARGUMENTS[2]` dengan `Vue`. Skill yang sama menggunakan shorthand `$N`:

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## Pola lanjutan

### Injeksi konteks dinamis

Sintaks `` !`<command>` `` menjalankan perintah shell sebelum konten skill dikirim ke Claude. Output perintah mengganti placeholder, sehingga Claude menerima data aktual, bukan perintah itu sendiri.

Skill ini merangkum pull request dengan mengambil data PR langsung dengan GitHub CLI. Perintah `` !`gh pr diff` `` dan lainnya berjalan terlebih dahulu, dan output mereka dimasukkan ke dalam prompt:

```yaml theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

Saat skill ini berjalan:

1. Setiap `` !`<command>` `` dijalankan segera (sebelum Claude melihat apa pun)
2. Output mengganti placeholder dalam konten skill
3. Claude menerima prompt yang sepenuhnya dirender dengan data PR aktual

Ini adalah preprocessing, bukan sesuatu yang dijalankan Claude. Claude hanya melihat hasil akhir.

Substitusi berjalan sekali di atas file asli. Output perintah dimasukkan sebagai teks biasa dan tidak dipindai ulang untuk placeholder `` !`<command>` `` lebih lanjut, jadi perintah tidak dapat mengeluarkan placeholder untuk pass yang lebih lambat untuk diperluas.

Untuk perintah multi-baris, gunakan blok kode yang dibuka dengan ` ```! ` sebagai gantinya dari bentuk inline:

````markdown theme={null}
## Environment
```!
node --version
npm --version
git status --short
```
````

Untuk menonaktifkan perilaku ini untuk skills dan perintah kustom dari sumber pengguna, proyek, plugin, atau [direktori tambahan](#skills-from-additional-directories), atur `"disableSkillShellExecution": true` dalam [pengaturan](/id/settings). Setiap perintah diganti dengan `[shell command execution disabled by policy]` sebagai gantinya dijalankan. Skills bundel dan terkelola tidak terpengaruh. Pengaturan ini paling berguna dalam [pengaturan terkelola](/id/permissions#managed-settings), di mana pengguna tidak dapat menimpanya.

<Tip>
  Untuk meminta penalaran yang lebih dalam saat skill berjalan, sertakan `ultrathink` di mana pun dalam konten skill. Lihat [Gunakan ultrathink untuk penalaran mendalam sekali jalan](/id/model-config#use-ultrathink-for-one-off-deep-reasoning).
</Tip>

### Jalankan skills dalam subagent

Tambahkan `context: fork` ke frontmatter Anda saat Anda ingin skill berjalan dalam isolasi. Konten skill menjadi prompt yang mendorong subagent. Ini tidak akan memiliki akses ke riwayat percakapan Anda.

<Warning>
  `context: fork` hanya masuk akal untuk skills dengan instruksi eksplisit. Jika skill Anda berisi panduan seperti "gunakan konvensi API ini" tanpa tugas, subagent menerima panduan tetapi tidak ada prompt yang dapat ditindaklanjuti, dan kembali tanpa output yang bermakna.
</Warning>

Skills dan [subagents](/id/sub-agents) bekerja bersama dalam dua arah:

| Pendekatan                      | System prompt                            | Tugas                 | Juga memuat                               |
| :------------------------------ | :--------------------------------------- | :-------------------- | :---------------------------------------- |
| Skill dengan `context: fork`    | Dari jenis agen (`Explore`, `Plan`, dll) | Konten SKILL.md       | CLAUDE.md                                 |
| Subagent dengan bidang `skills` | Badan markdown subagent                  | Pesan delegasi Claude | Skills yang dimuat sebelumnya + CLAUDE.md |

Dengan `context: fork`, Anda menulis tugas dalam skill Anda dan memilih jenis agen untuk menjalankannya. Untuk kebalikannya (mendefinisikan subagent kustom yang menggunakan skills sebagai materi referensi), lihat [Subagents](/id/sub-agents#preload-skills-into-subagents).

#### Contoh: Skill penelitian menggunakan agen Explore

Skill ini menjalankan penelitian dalam agen Explore yang di-fork. Konten skill menjadi tugas, dan agen menyediakan tools baca-saja yang dioptimalkan untuk eksplorasi codebase:

```yaml theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

Saat skill ini berjalan:

1. Konteks terisolasi baru dibuat
2. Subagent menerima konten skill sebagai promptnya ("Research \$ARGUMENTS thoroughly...")
3. Bidang `agent` menentukan lingkungan eksekusi (model, tools, dan izin)
4. Hasil dirangkum dan dikembalikan ke percakapan utama Anda

Bidang `agent` menentukan konfigurasi subagent mana yang digunakan. Opsi termasuk agen bawaan (`Explore`, `Plan`, `general-purpose`) atau subagent kustom apa pun dari `.claude/agents/`. Jika dihilangkan, menggunakan `general-purpose`.

### Batasi akses skill Claude

Secara default, Claude dapat menginvokasinya skill apa pun yang tidak memiliki `disable-model-invocation: true` diatur. Skills yang mendefinisikan `allowed-tools` memberikan Claude akses ke tools tersebut tanpa persetujuan per-penggunaan saat skill aktif. Pengaturan [izin](/id/permissions) Anda masih mengatur perilaku persetujuan baseline untuk semua tools lainnya. Beberapa perintah bawaan juga tersedia melalui tool Skill, termasuk `/init`, `/review`, dan `/security-review`. Perintah bawaan lainnya seperti `/compact` tidak.

Tiga cara untuk mengontrol skills mana yang dapat diinvokasinya Claude:

**Nonaktifkan semua skills** dengan menolak tool Skill di `/permissions`:

```text theme={null}
# Add to deny rules:
Skill
```

**Izinkan atau tolak skills spesifik** menggunakan [aturan izin](/id/permissions):

```text theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Sintaks izin: `Skill(name)` untuk kecocokan tepat, `Skill(name *)` untuk kecocokan awalan dengan argumen apa pun.

**Sembunyikan skills individual** dengan menambahkan `disable-model-invocation: true` ke frontmatter mereka. Ini menghapus skill dari konteks Claude sepenuhnya.

<Note>
  Bidang `user-invocable` hanya mengontrol visibilitas menu, bukan akses tool Skill. Gunakan `disable-model-invocation: true` untuk memblokir invokasi programatik.
</Note>

### Ganti visibilitas skill dari pengaturan

Pengaturan `skillOverrides` mengontrol visibilitas skill dari [pengaturan](/id/settings) Anda sebagai gantinya dari frontmatter skill itu sendiri. Gunakan untuk skills yang SKILL.md-nya Anda tidak ingin edit, seperti yang diperiksa ke dalam repo proyek bersama atau disediakan oleh server MCP. Menu `/skills` menulisnya untuk Anda: sorot skill dan tekan `Space` untuk mengubah status, kemudian `Enter` untuk menyimpan ke `.claude/settings.local.json`.

Setiap kunci adalah nama skill dan setiap nilai adalah salah satu dari empat status:

| Nilai                   | Terdaftar ke Claude | Dalam menu `/` |
| :---------------------- | :------------------ | :------------- |
| `"on"`                  | Nama dan deskripsi  | Ya             |
| `"name-only"`           | Nama saja           | Ya             |
| `"user-invocable-only"` | Tersembunyi         | Ya             |
| `"off"`                 | Tersembunyi         | Tersembunyi    |

Skill yang tidak ada dalam `skillOverrides` diperlakukan sebagai `"on"`. Contoh di bawah ini menciutkan satu skill menjadi namanya dan mematikan yang lain sepenuhnya:

```json theme={null}
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

Plugin skills tidak terpengaruh oleh `skillOverrides`. Kelola yang melalui `/plugin` sebagai gantinya.

## Bagikan skills

Skills dapat didistribusikan pada cakupan berbeda tergantung pada audiens Anda:

* **Skills proyek**: Commit `.claude/skills/` ke version control
* **Plugins**: Buat direktori `skills/` dalam [plugin](/id/plugins) Anda
* **Terkelola**: Terapkan di seluruh organisasi melalui [pengaturan terkelola](/id/settings#settings-files)

### Hasilkan output visual

Skills dapat membundel dan menjalankan script dalam bahasa apa pun, memberikan Claude kemampuan di luar apa yang mungkin dalam prompt tunggal. Satu pola yang kuat adalah menghasilkan output visual: file HTML interaktif yang terbuka di browser Anda untuk menjelajahi data, debugging, atau membuat laporan.

Contoh ini membuat penjelajah codebase: tampilan pohon interaktif di mana Anda dapat memperluas dan menciutkan direktori, melihat ukuran file sekilas, dan mengidentifikasi jenis file berdasarkan warna.

Buat direktori Skill:

```bash theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Simpan ini ke `~/.claude/skills/codebase-visualizer/SKILL.md`. Deskripsi memberi tahu Claude kapan mengaktifkan Skill ini, dan instruksi memberi tahu Claude untuk menjalankan script yang dikemas. Jalur script menggunakan [`${CLAUDE_SKILL_DIR}`](#available-string-substitutions) sehingga dapat diselesaikan dengan benar apakah skill diinstal pada tingkat personal, proyek, atau plugin:

````yaml theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python3 *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

Simpan ini ke `~/.claude/skills/codebase-visualizer/scripts/visualize.py`. Script ini memindai pohon direktori dan menghasilkan file HTML yang mandiri dengan:

* **Sidebar ringkasan** yang menunjukkan jumlah file, jumlah direktori, ukuran total, dan jumlah jenis file
* **Bagan batang** yang memecah codebase berdasarkan jenis file (8 teratas berdasarkan ukuran)
* **Pohon yang dapat diciutkan** di mana Anda dapat memperluas dan menciutkan direktori, dengan indikator jenis file berkode warna

Script memerlukan Python 3 tetapi hanya menggunakan library bawaan, jadi tidak ada paket yang perlu diinstal:

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from html import escape
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
      <h1>📁 {escape(data["name"])}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function esc(s) {{ return s.replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c])); }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{esc(node.name)}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{esc(node.name)}}<span class="size">${{fmt(node.size)}}</span>`;
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

Untuk menguji, buka Claude Code di proyek apa pun dan tanyakan "Visualize this codebase." Claude menjalankan script, menghasilkan `codebase-map.html`, dan membukanya di browser Anda.

Pola ini bekerja untuk output visual apa pun: grafik ketergantungan, laporan cakupan tes, dokumentasi API, atau visualisasi skema database. Script yang dikemas melakukan pekerjaan berat sementara Claude menangani orkestrasi.

## Troubleshooting

### Skill tidak terpicu

Jika Claude tidak menggunakan skill Anda saat diharapkan:

1. Periksa deskripsi mencakup kata kunci yang akan dikatakan pengguna secara alami
2. Verifikasi skill muncul di `What skills are available?`
3. Coba rephrase permintaan Anda agar lebih cocok dengan deskripsi
4. Invokasinya secara langsung dengan `/skill-name` jika skill dapat diinvokasinya pengguna

### Skill terpicu terlalu sering

Jika Claude menggunakan skill Anda saat Anda tidak menginginkannya:

1. Buat deskripsi lebih spesifik
2. Tambahkan `disable-model-invocation: true` jika Anda hanya menginginkan invokasi manual

### Deskripsi skill dipotong pendek

Deskripsi skill dimuat ke dalam konteks sehingga Claude tahu apa yang tersedia. Semua nama skill selalu disertakan, tetapi jika Anda memiliki banyak skills, deskripsi diperpendek agar sesuai dengan anggaran karakter, yang dapat menghilangkan kata kunci yang dibutuhkan Claude untuk mencocokkan permintaan Anda. Anggaran diskalakan pada 1% dari jendela konteks model. Ketika meluap, deskripsi untuk skills yang Anda invokasinya paling sedikit dijatuhkan terlebih dahulu, sehingga skills yang benar-benar Anda gunakan tetap mempertahankan teks lengkapnya. Jalankan `/doctor` untuk melihat apakah anggaran meluap dan skills mana yang terpengaruh.

Untuk menaikkan anggaran, atur pengaturan [`skillListingBudgetFraction`](/id/settings#available-settings) (misalnya `0.02` = 2%) atau variabel lingkungan `SLASH_COMMAND_TOOL_CHAR_BUDGET` ke jumlah karakter tetap. Untuk membebaskan anggaran bagi skills lainnya, atur entri prioritas rendah ke `"name-only"` di [`skillOverrides`](#override-skill-visibility-from-settings) sehingga mereka terdaftar tanpa deskripsi. Anda juga dapat memangkas teks `description` dan `when_to_use` di sumbernya: depankan kasus penggunaan utama, karena teks gabungan setiap entri dibatasi pada 1.536 karakter terlepas dari anggaran. Batas dapat dikonfigurasi dengan [`maxSkillDescriptionChars`](/id/settings#available-settings).

## Sumber daya terkait

* **[Debug konfigurasi Anda](/id/debug-your-config)**: diagnosis mengapa skill tidak muncul atau tidak terpicu
* **[Subagents](/id/sub-agents)**: delegasikan tugas ke agen khusus
* **[Plugins](/id/plugins)**: paket dan distribusikan skills dengan ekstensi lainnya
* **[Hooks](/id/hooks)**: otomatisasi workflow di sekitar peristiwa tool
* **[Memory](/id/memory)**: kelola file CLAUDE.md untuk konteks persisten
* **[Commands](/id/commands)**: referensi untuk perintah bawaan dan skills bundel
* **[Permissions](/id/permissions)**: kontrol akses tool dan skill
