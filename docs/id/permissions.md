> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi izin

> Kontrol apa yang dapat diakses Claude Code dan lakukan dengan aturan izin terperinci, mode, dan kebijakan terkelola.

Claude Code mendukung izin terperinci sehingga Anda dapat menentukan dengan tepat apa yang diizinkan dilakukan oleh agen dan apa yang tidak. Pengaturan izin dapat diperiksa ke dalam kontrol versi dan didistribusikan ke semua pengembang di organisasi Anda, serta disesuaikan oleh pengembang individual.

## Sistem izin

Claude Code menggunakan sistem izin berjenjang untuk menyeimbangkan kekuatan dan keamanan:

| Jenis alat      | Contoh               | Persetujuan diperlukan | Perilaku "Ya, jangan tanya lagi"                  |
| :-------------- | :------------------- | :--------------------- | :------------------------------------------------ |
| Hanya baca      | Pembacaan file, Grep | Tidak                  | T/A                                               |
| Perintah Bash   | Eksekusi shell       | Ya                     | Secara permanen per direktori proyek dan perintah |
| Modifikasi file | Edit/tulis file      | Ya                     | Hingga akhir sesi                                 |

## Kelola izin

Anda dapat melihat dan mengelola izin alat Claude Code dengan `/permissions`. UI ini mencantumkan semua aturan izin dan file settings.json tempat mereka bersumber.

* Aturan **Allow** memungkinkan Claude Code menggunakan alat yang ditentukan tanpa persetujuan manual.
* Aturan **Ask** meminta konfirmasi setiap kali Claude Code mencoba menggunakan alat yang ditentukan.
* Aturan **Deny** mencegah Claude Code menggunakan alat yang ditentukan.

Aturan dievaluasi secara berurutan: **deny -> ask -> allow**. Aturan pertama yang cocok menang, jadi aturan deny selalu memiliki prioritas.

## Mode izin

Claude Code mendukung beberapa mode izin yang mengontrol bagaimana alat disetujui. Atur `defaultMode` dalam [file pengaturan](/id/settings#settings-files) Anda:

| Mode                | Deskripsi                                                                                                 |
| :------------------ | :-------------------------------------------------------------------------------------------------------- |
| `default`           | Perilaku standar: meminta izin pada penggunaan pertama setiap alat                                        |
| `acceptEdits`       | Secara otomatis menerima izin edit file untuk sesi                                                        |
| `plan`              | Plan Mode: Claude dapat menganalisis tetapi tidak memodifikasi file atau menjalankan perintah             |
| `dontAsk`           | Secara otomatis menolak alat kecuali pra-disetujui melalui `/permissions` atau aturan `permissions.allow` |
| `bypassPermissions` | Melewati semua prompt izin (memerlukan lingkungan yang aman, lihat peringatan di bawah)                   |

<Warning>
  Mode `bypassPermissions` menonaktifkan semua pemeriksaan izin. Hanya gunakan ini di lingkungan terisolasi seperti kontainer atau VM tempat Claude Code tidak dapat menyebabkan kerusakan. Administrator dapat mencegah mode ini dengan mengatur `disableBypassPermissionsMode` ke `"disable"` dalam [pengaturan terkelola](#managed-settings).
</Warning>

## Sintaks aturan izin

Aturan izin mengikuti format `Tool` atau `Tool(specifier)`.

### Cocokkan semua penggunaan alat

Untuk mencocokkan semua penggunaan alat, gunakan hanya nama alat tanpa tanda kurung:

| Aturan     | Efek                                         |
| :--------- | :------------------------------------------- |
| `Bash`     | Mencocokkan semua perintah Bash              |
| `WebFetch` | Mencocokkan semua permintaan pengambilan web |
| `Read`     | Mencocokkan semua pembacaan file             |

`Bash(*)` setara dengan `Bash` dan mencocokkan semua perintah Bash.

### Gunakan specifier untuk kontrol terperinci

Tambahkan specifier dalam tanda kurung untuk mencocokkan penggunaan alat tertentu:

| Aturan                         | Efek                                                    |
| :----------------------------- | :------------------------------------------------------ |
| `Bash(npm run build)`          | Mencocokkan perintah yang tepat `npm run build`         |
| `Read(./.env)`                 | Mencocokkan pembacaan file `.env` di direktori saat ini |
| `WebFetch(domain:example.com)` | Mencocokkan permintaan pengambilan ke example.com       |

### Pola wildcard

Aturan Bash mendukung pola glob dengan `*`. Wildcard dapat muncul di posisi mana pun dalam perintah. Konfigurasi ini memungkinkan perintah npm dan git commit sambil memblokir git push:

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

Spasi sebelum `*` penting: `Bash(ls *)` mencocokkan `ls -la` tetapi bukan `lsof`, sementara `Bash(ls*)` mencocokkan keduanya. Sintaks akhiran `:*` warisan setara dengan ` *` tetapi sudah usang.

## Aturan izin khusus alat

### Bash

Aturan izin Bash mendukung pencocokan wildcard dengan `*`. Wildcard dapat muncul di posisi mana pun dalam perintah, termasuk di awal, tengah, atau akhir:

* `Bash(npm run build)` mencocokkan perintah Bash yang tepat `npm run build`
* `Bash(npm run test *)` mencocokkan perintah Bash yang dimulai dengan `npm run test`
* `Bash(npm *)` mencocokkan perintah apa pun yang dimulai dengan `npm `
* `Bash(* install)` mencocokkan perintah apa pun yang berakhir dengan ` install`
* `Bash(git * main)` mencocokkan perintah seperti `git checkout main`, `git merge main`

Ketika `*` muncul di akhir dengan spasi sebelumnya (seperti `Bash(ls *)`), ini memberlakukan batas kata, memerlukan awalan diikuti oleh spasi atau akhir string. Misalnya, `Bash(ls *)` mencocokkan `ls -la` tetapi bukan `lsof`. Sebaliknya, `Bash(ls*)` tanpa spasi mencocokkan `ls -la` dan `lsof` karena tidak ada batasan batas kata.

<Tip>
  Claude Code menyadari operator shell (seperti `&&`) jadi aturan pencocokan awalan seperti `Bash(safe-cmd *)` tidak akan memberinya izin untuk menjalankan perintah `safe-cmd && other-cmd`.
</Tip>

<Warning>
  Pola izin Bash yang mencoba membatasi argumen perintah rapuh. Misalnya, `Bash(curl http://github.com/ *)` dimaksudkan untuk membatasi curl ke URL GitHub, tetapi tidak akan mencocokkan variasi seperti:

  * Opsi sebelum URL: `curl -X GET http://github.com/...`
  * Protokol berbeda: `curl https://github.com/...`
  * Pengalihan: `curl -L http://bit.ly/xyz` (pengalihan ke github)
  * Variabel: `URL=http://github.com && curl $URL`
  * Spasi ekstra: `curl  http://github.com`

  Untuk penyaringan URL yang lebih andal, pertimbangkan:

  * **Batasi alat jaringan Bash**: gunakan aturan deny untuk memblokir `curl`, `wget`, dan perintah serupa, kemudian gunakan alat WebFetch dengan izin `WebFetch(domain:github.com)` untuk domain yang diizinkan
  * **Gunakan hook PreToolUse**: implementasikan hook yang memvalidasi URL dalam perintah Bash dan memblokir domain yang tidak diizinkan
  * Menginstruksikan Claude Code tentang pola curl yang diizinkan Anda melalui CLAUDE.md

  Perhatikan bahwa menggunakan WebFetch saja tidak mencegah akses jaringan. Jika Bash diizinkan, Claude masih dapat menggunakan `curl`, `wget`, atau alat lain untuk menjangkau URL apa pun.
</Warning>

### Read dan Edit

Aturan `Edit` berlaku untuk semua alat bawaan yang mengedit file. Claude membuat upaya terbaik untuk menerapkan aturan `Read` ke semua alat bawaan yang membaca file seperti Grep dan Glob.

Aturan Read dan Edit keduanya mengikuti spesifikasi [gitignore](https://git-scm.com/docs/gitignore) dengan empat jenis pola yang berbeda:

| Pola                 | Arti                                          | Contoh                           | Cocok                          |
| -------------------- | --------------------------------------------- | -------------------------------- | ------------------------------ |
| `//path`             | Jalur **absolut** dari akar sistem file       | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`             | Jalur dari direktori **home**                 | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`              | Jalur **relatif terhadap akar proyek**        | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` atau `./path` | Jalur **relatif terhadap direktori saat ini** | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  Pola seperti `/Users/alice/file` BUKAN jalur absolut. Ini relatif terhadap akar proyek. Gunakan `//Users/alice/file` untuk jalur absolut.
</Warning>

Contoh:

* `Edit(/docs/**)`: edit di `<project>/docs/` (BUKAN `/docs/` dan BUKAN `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: membaca `.zshrc` direktori home Anda
* `Edit(//tmp/scratch.txt)`: edit jalur absolut `/tmp/scratch.txt`
* `Read(src/**)`: membaca dari `<current-directory>/src/`

<Note>
  Dalam pola gitignore, `*` mencocokkan file dalam satu direktori sementara `**` mencocokkan secara rekursif di seluruh direktori. Untuk memungkinkan semua akses file, gunakan hanya nama alat tanpa tanda kurung: `Read`, `Edit`, atau `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` mencocokkan permintaan pengambilan ke example.com

### MCP

* `mcp__puppeteer` mencocokkan alat apa pun yang disediakan oleh server `puppeteer` (nama dikonfigurasi di Claude Code)
* `mcp__puppeteer__*` sintaks wildcard yang juga mencocokkan semua alat dari server `puppeteer`
* `mcp__puppeteer__puppeteer_navigate` mencocokkan alat `puppeteer_navigate` yang disediakan oleh server `puppeteer`

### Agent (subagents)

Gunakan aturan `Agent(AgentName)` untuk mengontrol [subagents](/id/sub-agents) mana yang dapat digunakan Claude:

* `Agent(Explore)` mencocokkan subagent Explore
* `Agent(Plan)` mencocokkan subagent Plan
* `Agent(my-custom-agent)` mencocokkan subagent kustom bernama `my-custom-agent`

Tambahkan aturan ini ke array `deny` dalam pengaturan Anda atau gunakan flag CLI `--disallowedTools` untuk menonaktifkan agen tertentu. Untuk menonaktifkan agen Explore:

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Perluas izin dengan hook

[Hook Claude Code](/id/hooks-guide) menyediakan cara untuk mendaftarkan perintah shell kustom guna melakukan evaluasi izin saat runtime. Ketika Claude Code membuat panggilan alat, hook PreToolUse berjalan sebelum sistem izin, dan output hook dapat menentukan apakah akan menyetujui atau menolak panggilan alat sebagai pengganti sistem izin.

## Direktori kerja

Secara default, Claude memiliki akses ke file di direktori tempat diluncurkan. Anda dapat memperluas akses ini:

* **Saat startup**: gunakan argumen CLI `--add-dir <path>`
* **Selama sesi**: gunakan perintah `/add-dir`
* **Konfigurasi persisten**: tambahkan ke `additionalDirectories` dalam [file pengaturan](/id/settings#settings-files)

File di direktori tambahan mengikuti aturan izin yang sama dengan direktori kerja asli: mereka menjadi dapat dibaca tanpa prompt, dan izin edit file mengikuti mode izin saat ini.

## Bagaimana izin berinteraksi dengan sandboxing

Izin dan [sandboxing](/id/sandboxing) adalah lapisan keamanan pelengkap:

* **Izin** mengontrol alat mana yang dapat digunakan Claude Code dan file atau domain mana yang dapat diaksesnya. Mereka berlaku untuk semua alat (Bash, Read, Edit, WebFetch, MCP, dan lainnya).
* **Sandboxing** menyediakan penegakan tingkat OS yang membatasi akses sistem file dan jaringan alat Bash. Ini hanya berlaku untuk perintah Bash dan proses anak mereka.

Gunakan keduanya untuk pertahanan berlapis:

* Aturan deny izin memblokir Claude dari bahkan mencoba mengakses sumber daya terbatas
* Pembatasan sandbox mencegah perintah Bash menjangkau sumber daya di luar batas yang ditentukan, bahkan jika injeksi prompt melewati pengambilan keputusan Claude
* Pembatasan sistem file di sandbox menggunakan aturan deny Read dan Edit, bukan konfigurasi sandbox terpisah
* Pembatasan jaringan menggabungkan aturan izin WebFetch dengan daftar `allowedDomains` sandbox

## Pengaturan terkelola

Untuk organisasi yang memerlukan kontrol terpusat atas konfigurasi Claude Code, administrator dapat menerapkan pengaturan terkelola yang tidak dapat ditimpa oleh pengaturan pengguna atau proyek. Pengaturan kebijakan ini mengikuti format yang sama dengan file pengaturan reguler dan dapat dikirimkan melalui kebijakan MDM/tingkat OS, file pengaturan terkelola, atau [pengaturan yang dikelola server](/id/server-managed-settings). Lihat [file pengaturan](/id/settings#settings-files) untuk mekanisme pengiriman dan lokasi file.

### Pengaturan khusus terkelola

Beberapa pengaturan hanya efektif dalam pengaturan terkelola:

| Pengaturan                                | Deskripsi                                                                                                                                                                                                                                                 |
| :---------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | Atur ke `"disable"` untuk mencegah mode `bypassPermissions` dan flag `--dangerously-skip-permissions`                                                                                                                                                     |
| `allowManagedPermissionRulesOnly`         | Ketika `true`, mencegah pengaturan pengguna dan proyek dari mendefinisikan aturan izin `allow`, `ask`, atau `deny`. Hanya aturan dalam pengaturan terkelola yang berlaku                                                                                  |
| `allowManagedHooksOnly`                   | Ketika `true`, mencegah pemuatan hook pengguna, proyek, dan plugin. Hanya hook terkelola dan hook SDK yang diizinkan                                                                                                                                      |
| `allowManagedMcpServersOnly`              | Ketika `true`, hanya `allowedMcpServers` dari pengaturan terkelola yang dihormati. `deniedMcpServers` masih digabung dari semua sumber. Lihat [Konfigurasi MCP terkelola](/id/mcp#managed-mcp-configuration)                                              |
| `blockedMarketplaces`                     | Daftar blokir sumber marketplace. Sumber yang diblokir diperiksa sebelum mengunduh, jadi mereka tidak pernah menyentuh sistem file. Lihat [pembatasan marketplace terkelola](/id/plugin-marketplaces#managed-marketplace-restrictions)                    |
| `sandbox.network.allowManagedDomainsOnly` | Ketika `true`, hanya `allowedDomains` dan aturan allow `WebFetch(domain:...)` dari pengaturan terkelola yang dihormati. Domain yang tidak diizinkan diblokir secara otomatis tanpa meminta pengguna. Domain yang ditolak masih digabung dari semua sumber |
| `strictKnownMarketplaces`                 | Mengontrol marketplace plugin mana yang dapat ditambahkan pengguna. Lihat [pembatasan marketplace terkelola](/id/plugin-marketplaces#managed-marketplace-restrictions)                                                                                    |
| `allow_remote_sessions`                   | Ketika `true`, memungkinkan pengguna memulai [Remote Control](/id/remote-control) dan [sesi web](/id/claude-code-on-the-web). Default ke `true`. Atur ke `false` untuk mencegah akses sesi jarak jauh                                                     |

## Prioritas pengaturan

Aturan izin mengikuti [prioritas pengaturan](/id/settings#settings-precedence) yang sama dengan semua pengaturan Claude Code lainnya:

1. **Pengaturan terkelola**: tidak dapat ditimpa oleh tingkat lain apa pun, termasuk argumen baris perintah
2. **Argumen baris perintah**: penggantian sesi sementara
3. **Pengaturan proyek lokal** (`.claude/settings.local.json`)
4. **Pengaturan proyek bersama** (`.claude/settings.json`)
5. **Pengaturan pengguna** (`~/.claude/settings.json`)

Jika alat ditolak di tingkat mana pun, tidak ada tingkat lain yang dapat mengizinkannya. Misalnya, deny pengaturan terkelola tidak dapat ditimpa oleh `--allowedTools`, dan `--disallowedTools` dapat menambahkan pembatasan di luar apa yang ditentukan pengaturan terkelola.

Jika izin diizinkan dalam pengaturan pengguna tetapi ditolak dalam pengaturan proyek, pengaturan proyek memiliki prioritas dan izin diblokir.

## Contoh konfigurasi

[Repositori](https://github.com/anthropics/claude-code/tree/main/examples/settings) ini mencakup konfigurasi pengaturan pemula untuk skenario penerapan umum. Gunakan ini sebagai titik awal dan sesuaikan dengan kebutuhan Anda.

## Lihat juga

* [Pengaturan](/id/settings): referensi konfigurasi lengkap termasuk tabel pengaturan izin
* [Sandboxing](/id/sandboxing): isolasi sistem file dan jaringan tingkat OS untuk perintah Bash
* [Autentikasi](/id/authentication): atur akses pengguna ke Claude Code
* [Keamanan](/id/security): perlindungan keamanan dan praktik terbaik
* [Hook](/id/hooks-guide): otomatisasi alur kerja dan perluas evaluasi izin
