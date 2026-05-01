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

Claude Code mendukung beberapa mode izin yang mengontrol bagaimana alat disetujui. Lihat [Permission modes](/id/permission-modes) untuk mengetahui kapan menggunakan masing-masing. Atur `defaultMode` dalam [file pengaturan](/id/settings#settings-files) Anda:

| Mode                | Deskripsi                                                                                                                                                                      |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Perilaku standar: meminta izin pada penggunaan pertama setiap alat                                                                                                             |
| `acceptEdits`       | Secara otomatis menerima edit file dan perintah sistem file umum (`mkdir`, `touch`, `mv`, `cp`, dll.) untuk jalur di direktori kerja atau `additionalDirectories`              |
| `plan`              | Plan Mode: Claude dapat menganalisis tetapi tidak memodifikasi file atau menjalankan perintah                                                                                  |
| `auto`              | Secara otomatis menyetujui panggilan alat dengan pemeriksaan keamanan latar belakang yang memverifikasi tindakan selaras dengan permintaan Anda. Saat ini pratinjau penelitian |
| `dontAsk`           | Secara otomatis menolak alat kecuali pra-disetujui melalui `/permissions` atau aturan `permissions.allow`                                                                      |
| `bypassPermissions` | Melewati semua prompt izin. Penghapusan direktori root dan home seperti `rm -rf /` masih meminta sebagai circuit breaker                                                       |

<Warning>
  Mode `bypassPermissions` melewati semua prompt izin, termasuk penulisan ke `.git`, `.claude`, `.vscode`, `.idea`, dan `.husky`. Penghapusan yang menargetkan akar sistem file atau direktori home, seperti `rm -rf /` dan `rm -rf ~`, masih meminta sebagai circuit breaker terhadap kesalahan model. Hanya gunakan mode ini di lingkungan terisolasi seperti kontainer atau VM tempat Claude Code tidak dapat menyebabkan kerusakan. Administrator dapat mencegah mode ini dengan mengatur `permissions.disableBypassPermissionsMode` ke `"disable"` dalam [pengaturan terkelola](#managed-settings).
</Warning>

Untuk mencegah `bypassPermissions` atau mode `auto` digunakan, atur `permissions.disableBypassPermissionsMode` atau `permissions.disableAutoMode` ke `"disable"` dalam [file pengaturan](/id/settings#settings-files) apa pun. Ini paling berguna dalam [pengaturan terkelola](#managed-settings) di mana mereka tidak dapat ditimpa.

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

```json theme={null}
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

Spasi sebelum `*` penting: `Bash(ls *)` mencocokkan `ls -la` tetapi bukan `lsof`, sementara `Bash(ls*)` mencocokkan keduanya. Akhiran `:*` adalah cara setara untuk menulis wildcard trailing, jadi `Bash(ls:*)` mencocokkan perintah yang sama dengan `Bash(ls *)`.

Dialog izin menulis bentuk yang dipisahkan spasi ketika Anda memilih "Ya, jangan tanya lagi" untuk awalan perintah. Bentuk `:*` hanya dikenali di akhir pola. Dalam pola seperti `Bash(git:* push)`, titik dua diperlakukan sebagai karakter literal dan tidak akan mencocokkan perintah git.

## Aturan izin khusus alat

### Bash

Aturan izin Bash mendukung pencocokan wildcard dengan `*`. Wildcard dapat muncul di posisi mana pun dalam perintah, termasuk di awal, tengah, atau akhir:

* `Bash(npm run build)` mencocokkan perintah Bash yang tepat `npm run build`
* `Bash(npm run test *)` mencocokkan perintah Bash yang dimulai dengan `npm run test`
* `Bash(npm *)` mencocokkan perintah apa pun yang dimulai dengan `npm `
* `Bash(* install)` mencocokkan perintah apa pun yang berakhir dengan ` install`
* `Bash(git * main)` mencocokkan perintah seperti `git checkout main` dan `git log --oneline main`

Satu `*` mencocokkan urutan karakter apa pun termasuk spasi, jadi satu wildcard dapat mencakup beberapa argumen. `Bash(git *)` mencocokkan `git log --oneline --all`, dan `Bash(git * main)` mencocokkan `git push origin main` serta `git merge main`.

Ketika `*` muncul di akhir dengan spasi sebelumnya (seperti `Bash(ls *)`), ini memberlakukan batas kata, memerlukan awalan diikuti oleh spasi atau akhir string. Misalnya, `Bash(ls *)` mencocokkan `ls -la` tetapi bukan `lsof`. Sebaliknya, `Bash(ls*)` tanpa spasi mencocokkan `ls -la` dan `lsof` karena tidak ada batasan batas kata.

#### Perintah gabungan

<Tip>
  Claude Code menyadari operator shell, jadi aturan seperti `Bash(safe-cmd *)` tidak akan memberinya izin untuk menjalankan perintah `safe-cmd && other-cmd`. Pemisah perintah yang dikenali adalah `&&`, `||`, `;`, `|`, `|&`, `&`, dan baris baru. Aturan harus mencocokkan setiap subperintah secara independen.
</Tip>

Ketika Anda menyetujui perintah gabungan dengan "Ya, jangan tanya lagi", Claude Code menyimpan aturan terpisah untuk setiap subperintah yang memerlukan persetujuan, bukan satu aturan untuk string gabungan lengkap. Misalnya, menyetujui `git status && npm test` menyimpan aturan untuk `npm test`, jadi invokasi `npm test` di masa depan dikenali terlepas dari apa yang mendahului `&&`. Subperintah seperti `cd` ke subdirektori menghasilkan aturan Read mereka sendiri untuk jalur itu. Hingga 5 aturan dapat disimpan untuk satu perintah gabungan.

#### Pembungkus proses

Sebelum mencocokkan aturan Bash, Claude Code menghilangkan serangkaian pembungkus proses tetap sehingga aturan seperti `Bash(npm test *)` juga mencocokkan `timeout 30 npm test`. Pembungkus yang dikenali adalah `timeout`, `time`, `nice`, `nohup`, dan `stdbuf`.

`xargs` telanjang juga dihilangkan, jadi `Bash(grep *)` mencocokkan `xargs grep pattern`. Penghilangan hanya berlaku ketika `xargs` tidak memiliki flag: invokasi seperti `xargs -n1 grep pattern` dicocokkan sebagai perintah `xargs`, jadi aturan yang ditulis untuk perintah inner tidak mencakupnya.

Daftar pembungkus ini bawaan dan tidak dapat dikonfigurasi. Pelari lingkungan pengembangan seperti `direnv exec`, `devbox run`, `mise exec`, `npx`, dan `docker exec` tidak ada dalam daftar. Karena alat ini menjalankan argumen mereka sebagai perintah, aturan seperti `Bash(devbox run *)` mencocokkan apa pun yang datang setelah `run`, termasuk `devbox run rm -rf .`. Untuk menyetujui pekerjaan di dalam pelari lingkungan, tulis aturan spesifik yang mencakup baik pelari maupun perintah inner, seperti `Bash(devbox run npm test)`. Tambahkan satu aturan per perintah inner yang ingin Anda izinkan.

Pembungkus exec seperti `watch`, `setsid`, `ionice`, dan `flock` selalu meminta dan tidak dapat disetujui otomatis oleh aturan awalan seperti `Bash(watch *)`. Hal yang sama berlaku untuk `find` dengan `-exec` atau `-delete`: aturan `Bash(find *)` tidak mencakup bentuk ini. Untuk menyetujui invokasi spesifik, tulis aturan pencocokan tepat untuk string perintah lengkap.

#### Perintah hanya baca

Claude Code mengenali serangkaian perintah Bash bawaan sebagai hanya baca dan menjalankannya tanpa prompt izin di setiap mode. Ini termasuk `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc`, `diff`, `stat`, `du`, `cd`, dan bentuk hanya baca dari `git`. Serangkaian ini tidak dapat dikonfigurasi; untuk memerlukan prompt untuk salah satu perintah ini, tambahkan aturan `ask` atau `deny` untuk itu.

Pola glob yang tidak dikutip diizinkan untuk perintah yang setiap flagnya hanya baca, jadi `ls *.ts` dan `wc -l src/*.py` berjalan tanpa prompt. Perintah dengan flag yang mampu menulis atau exec, seperti `find`, `sort`, `sed`, dan `git`, masih meminta ketika glob yang tidak dikutip ada karena glob dapat berkembang menjadi flag seperti `-delete`.

`cd` ke jalur di dalam direktori kerja Anda atau [direktori tambahan](#working-directories) juga hanya baca. Perintah gabungan seperti `cd packages/api && ls` berjalan tanpa prompt ketika setiap bagian memenuhi syarat sendiri. Menggabungkan `cd` dengan `git` dalam satu perintah gabungan selalu meminta, terlepas dari direktori target.

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

### PowerShell

Aturan izin PowerShell menggunakan bentuk yang sama dengan aturan Bash. Wildcard dengan `*` cocok di posisi mana pun, akhiran `:*` setara dengan trailing ` *`, dan PowerShell telanjang atau `PowerShell(*)` cocok dengan setiap perintah. Konfigurasi ini memungkinkan perintah `Get-ChildItem` dan `git commit` sambil memblokir `Remove-Item`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Alias umum dikanonikalisasi sebelum pencocokan. Aturan yang ditulis untuk nama cmdlet juga cocok dengan aliasnya, jadi `PowerShell(Get-ChildItem *)` cocok dengan `gci`, `ls`, dan `dir` juga. Pencocokan tidak peka huruf besar-kecil.

Claude Code mengurai AST PowerShell dan memeriksa setiap perintah dalam perintah gabungan secara independen. Operator pipeline `|`, pemisah pernyataan `;`, dan pada PowerShell 7+ operator rantai `&&` dan `||` membagi perintah gabungan menjadi subperintah. Aturan harus cocok dengan setiap subperintah agar perintah gabungan diizinkan.

### Read dan Edit

Aturan `Edit` berlaku untuk semua alat bawaan yang mengedit file. Claude membuat upaya terbaik untuk menerapkan aturan `Read` ke semua alat bawaan yang membaca file seperti Grep dan Glob.

<Warning>
  Aturan deny Read dan Edit berlaku untuk alat file bawaan Claude, bukan untuk subproses Bash. Aturan deny `Read(./.env)` memblokir alat Read tetapi tidak mencegah `cat .env` di Bash. Untuk penegakan tingkat OS yang memblokir semua proses dari mengakses jalur, [aktifkan sandbox](/id/sandboxing).
</Warning>

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

Di Windows, jalur dinormalisasi ke bentuk POSIX sebelum pencocokan. `C:\Users\alice` menjadi `/c/Users/alice`, jadi gunakan `//c/**/.env` untuk mencocokkan file `.env` di mana pun di drive itu. Untuk mencocokkan di semua drive, gunakan `//**/.env`.

Contoh:

* `Edit(/docs/**)`: edit di `<project>/docs/` (BUKAN `/docs/` dan BUKAN `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: membaca `.zshrc` direktori home Anda
* `Edit(//tmp/scratch.txt)`: edit jalur absolut `/tmp/scratch.txt`
* `Read(src/**)`: membaca dari `<current-directory>/src/`

<Note>
  Dalam pola gitignore, `*` mencocokkan file dalam satu direktori sementara `**` mencocokkan secara rekursif di seluruh direktori. Untuk memungkinkan semua akses file, gunakan hanya nama alat tanpa tanda kurung: `Read`, `Edit`, atau `Write`.
</Note>

Ketika Claude mengakses symlink, aturan izin memeriksa dua jalur: symlink itu sendiri dan file yang diselesaikannya. Aturan allow dan deny memperlakukan pasangan itu secara berbeda: aturan allow kembali ke meminta Anda, sementara aturan deny memblokir sepenuhnya.

* **Aturan allow**: berlaku hanya ketika jalur symlink dan targetnya cocok. Symlink di dalam direktori yang diizinkan yang menunjuk ke luar masih meminta Anda.
* **Aturan deny**: berlaku ketika jalur symlink atau targetnya cocok. Symlink yang menunjuk ke file yang ditolak itu sendiri ditolak.

Misalnya, dengan `Read(./project/**)` diizinkan dan `Read(~/.ssh/**)` ditolak, symlink di `./project/key` menunjuk ke `~/.ssh/id_rsa` diblokir: target gagal aturan allow dan cocok dengan aturan deny.

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

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Perluas izin dengan hook

[Hook Claude Code](/id/hooks-guide) menyediakan cara untuk mendaftarkan perintah shell kustom guna melakukan evaluasi izin saat runtime. Ketika Claude Code membuat panggilan alat, hook PreToolUse berjalan sebelum prompt izin. Output hook dapat menolak panggilan alat, memaksa prompt, atau melewati prompt untuk membiarkan panggilan berlanjut.

Keputusan hook tidak melewati aturan izin. Aturan deny dan ask dievaluasi terlepas dari apa yang dikembalikan hook PreToolUse, jadi aturan deny yang cocok memblokir panggilan dan aturan ask masih meminta bahkan ketika hook mengembalikan `"allow"` atau `"ask"`. Ini mempertahankan prioritas deny-first yang dijelaskan dalam [Kelola izin](#manage-permissions), termasuk aturan deny yang ditetapkan dalam pengaturan terkelola.

Hook pemblokiran juga memiliki prioritas atas aturan allow. Hook yang keluar dengan kode 2 menghentikan panggilan alat sebelum aturan izin dievaluasi, jadi blokir berlaku bahkan ketika aturan allow akan membiarkan panggilan berlanjut. Untuk menjalankan semua perintah Bash tanpa prompt kecuali untuk beberapa yang ingin Anda blokir, tambahkan `"Bash"` ke daftar allow Anda dan daftarkan hook PreToolUse yang menolak perintah tertentu itu. Lihat [Block edits to protected files](/id/hooks-guide#block-edits-to-protected-files) untuk skrip hook yang dapat Anda sesuaikan.

## Direktori kerja

Secara default, Claude memiliki akses ke file di direktori tempat diluncurkan. Anda dapat memperluas akses ini:

* **Saat startup**: gunakan argumen CLI `--add-dir <path>`
* **Selama sesi**: gunakan perintah `/add-dir`
* **Konfigurasi persisten**: tambahkan ke `additionalDirectories` dalam [file pengaturan](/id/settings#settings-files)

File di direktori tambahan mengikuti aturan izin yang sama dengan direktori kerja asli: mereka menjadi dapat dibaca tanpa prompt, dan izin edit file mengikuti mode izin saat ini.

### Direktori tambahan memberikan akses file, bukan konfigurasi

Menambahkan direktori memperluas tempat Claude dapat membaca dan mengedit file. Ini tidak membuat direktori itu akar konfigurasi penuh: sebagian besar konfigurasi `.claude/` tidak ditemukan dari direktori tambahan, meskipun beberapa jenis dimuat sebagai pengecualian.

Jenis konfigurasi berikut dimuat dari direktori `--add-dir`:

| Konfigurasi                                                           | Dimuat dari `--add-dir`                                                                                                                                           |
| :-------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Skills](/id/skills) di `.claude/skills/`                             | Ya, dengan live reload                                                                                                                                            |
| Pengaturan plugin di `.claude/settings.json`                          | `enabledPlugins` dan `extraKnownMarketplaces` saja                                                                                                                |
| File [CLAUDE.md](/id/memory), `.claude/rules/`, dan `CLAUDE.local.md` | Hanya ketika `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` diatur. `CLAUDE.local.md` juga memerlukan sumber pengaturan `local`, yang diaktifkan secara default |

Segalanya yang lain, termasuk subagents, commands, output styles, hooks, dan pengaturan lainnya, ditemukan hanya dari direktori kerja saat ini dan induknya, direktori pengguna Anda di `~/.claude/`, dan pengaturan terkelola. Untuk berbagi konfigurasi itu di seluruh proyek, gunakan salah satu pendekatan ini:

* **Konfigurasi tingkat pengguna**: tempatkan file di `~/.claude/agents/`, `~/.claude/output-styles/`, atau `~/.claude/settings.json` untuk membuatnya tersedia di setiap proyek
* **Plugins**: paket dan distribusikan konfigurasi sebagai [plugin](/id/plugins) yang dapat diinstal tim
* **Luncurkan dari direktori konfigurasi**: jalankan Claude Code dari direktori yang berisi konfigurasi `.claude/` yang ingin Anda gunakan

## Bagaimana izin berinteraksi dengan sandboxing

Izin dan [sandboxing](/id/sandboxing) adalah lapisan keamanan pelengkap:

* **Izin** mengontrol alat mana yang dapat digunakan Claude Code dan file atau domain mana yang dapat diaksesnya. Mereka berlaku untuk semua alat (Bash, Read, Edit, WebFetch, MCP, dan lainnya).
* **Sandboxing** menyediakan penegakan tingkat OS yang membatasi akses sistem file dan jaringan alat Bash. Ini hanya berlaku untuk perintah Bash dan proses anak mereka.

Gunakan keduanya untuk pertahanan berlapis:

* Aturan deny izin memblokir Claude dari bahkan mencoba mengakses sumber daya terbatas
* Pembatasan sandbox mencegah perintah Bash menjangkau sumber daya di luar batas yang ditentukan, bahkan jika injeksi prompt melewati pengambilan keputusan Claude
* Pembatasan sistem file di sandbox menggunakan aturan deny Read dan Edit, bukan konfigurasi sandbox terpisah
* Pembatasan jaringan menggabungkan aturan izin WebFetch dengan daftar `allowedDomains` dan `deniedDomains` sandbox

Ketika sandboxing diaktifkan dengan `autoAllowBashIfSandboxed: true`, yang merupakan default, perintah Bash yang di-sandbox berjalan tanpa meminta bahkan jika izin Anda mencakup `ask: Bash(*)`. Batas sandbox menggantikan prompt per-perintah. Aturan deny eksplisit masih berlaku, dan perintah `rm` atau `rmdir` yang menargetkan `/`, direktori home Anda, atau jalur sistem kritis lainnya masih memicu prompt. Lihat [sandbox modes](/id/sandboxing#sandbox-modes) untuk mengubah perilaku ini.

## Pengaturan terkelola

Untuk organisasi yang memerlukan kontrol terpusat atas konfigurasi Claude Code, administrator dapat menerapkan pengaturan terkelola yang tidak dapat ditimpa oleh pengaturan pengguna atau proyek. Pengaturan kebijakan ini mengikuti format yang sama dengan file pengaturan reguler dan dapat dikirimkan melalui kebijakan MDM/tingkat OS, file pengaturan terkelola, atau [pengaturan yang dikelola server](/id/server-managed-settings). Lihat [file pengaturan](/id/settings#settings-files) untuk mekanisme pengiriman dan lokasi file.

### Pengaturan khusus terkelola

Pengaturan berikut hanya dibaca dari pengaturan terkelola. Menempatkan mereka dalam file pengaturan pengguna atau proyek tidak memiliki efek.

| Pengaturan                                     | Deskripsi                                                                                                                                                                                                                                                 |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Daftar izin plugin saluran yang dapat mendorong pesan. Menggantikan daftar izin Anthropic default saat diatur. Memerlukan `channelsEnabled: true`. Lihat [Restrict which channel plugins can run](/id/channels#restrict-which-channel-plugins-can-run)    |
| `allowManagedHooksOnly`                        | Ketika `true`, hanya hook terkelola, hook SDK, dan hook dari plugin yang dipaksa-aktifkan dalam pengaturan terkelola `enabledPlugins` yang dimuat. Hook pengguna, proyek, dan semua plugin lainnya diblokir                                               |
| `allowManagedMcpServersOnly`                   | Ketika `true`, hanya `allowedMcpServers` dari pengaturan terkelola yang dihormati. `deniedMcpServers` masih digabung dari semua sumber. Lihat [Managed MCP configuration](/id/mcp#managed-mcp-configuration)                                              |
| `allowManagedPermissionRulesOnly`              | Ketika `true`, mencegah pengaturan pengguna dan proyek dari mendefinisikan aturan izin `allow`, `ask`, atau `deny`. Hanya aturan dalam pengaturan terkelola yang berlaku                                                                                  |
| `blockedMarketplaces`                          | Daftar blokir sumber marketplace. Sumber yang diblokir diperiksa sebelum mengunduh, jadi mereka tidak pernah menyentuh sistem file. Lihat [managed marketplace restrictions](/id/plugin-marketplaces#managed-marketplace-restrictions)                    |
| `channelsEnabled`                              | Izinkan [channels](/id/channels) untuk pengguna Team dan Enterprise. Tidak diatur atau `false` memblokir pengiriman pesan saluran terlepas dari apa yang dilewatkan pengguna ke `--channels`                                                              |
| `forceRemoteSettingsRefresh`                   | Ketika `true`, memblokir startup CLI hingga pengaturan terkelola jarak jauh segar diambil dan keluar jika pengambilan gagal. Lihat [fail-closed enforcement](/id/server-managed-settings#enforce-fail-closed-startup)                                     |
| `pluginTrustMessage`                           | Pesan kustom ditambahkan ke peringatan kepercayaan plugin yang ditampilkan sebelum instalasi                                                                                                                                                              |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Ketika `true`, hanya jalur `filesystem.allowRead` dari pengaturan terkelola yang dihormati. `denyRead` masih digabung dari semua sumber                                                                                                                   |
| `sandbox.network.allowManagedDomainsOnly`      | Ketika `true`, hanya `allowedDomains` dan aturan allow `WebFetch(domain:...)` dari pengaturan terkelola yang dihormati. Domain yang tidak diizinkan diblokir secara otomatis tanpa meminta pengguna. Domain yang ditolak masih digabung dari semua sumber |
| `strictKnownMarketplaces`                      | Mengontrol sumber marketplace plugin mana yang dapat ditambahkan dan diinstal pengguna. Lihat [managed marketplace restrictions](/id/plugin-marketplaces#managed-marketplace-restrictions)                                                                |
| `wslInheritsWindowsSettings`                   | Ketika `true` dalam kunci registri Windows HKLM atau `C:\Program Files\ClaudeCode\managed-settings.json`, WSL membaca pengaturan terkelola dari rantai kebijakan Windows selain `/etc/claude-code`. Lihat [Settings files](/id/settings#settings-files)   |

`disableBypassPermissionsMode` biasanya ditempatkan dalam pengaturan terkelola untuk memberlakukan kebijakan organisasi, tetapi berfungsi dari cakupan apa pun. Pengguna dapat mengaturnya dalam pengaturan mereka sendiri untuk mengunci diri mereka sendiri dari mode bypass.

<Note>
  Akses ke [Remote Control](/id/remote-control) dan [sesi web](/id/claude-code-on-the-web) tidak dikendalikan oleh kunci pengaturan terkelola. Pada paket Team dan Enterprise, admin mengaktifkan atau menonaktifkan fitur ini dalam [pengaturan admin Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

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

* [Settings](/id/settings): referensi konfigurasi lengkap termasuk tabel pengaturan izin
* [Configure auto mode](/id/auto-mode-config): beri tahu pengklasifikasi mode auto infrastruktur mana yang dipercaya organisasi Anda
* [Sandboxing](/id/sandboxing): isolasi sistem file dan jaringan tingkat OS untuk perintah Bash
* [Authentication](/id/authentication): atur akses pengguna ke Claude Code
* [Security](/id/security): perlindungan keamanan dan praktik terbaik
* [Hooks](/id/hooks-guide): otomatisasi alur kerja dan perluas evaluasi izin
