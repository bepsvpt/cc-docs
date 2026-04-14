> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code di web

> Jalankan tugas Claude Code secara asinkron pada infrastruktur cloud yang aman

<Note>
  Claude Code di web saat ini dalam pratinjau penelitian.
</Note>

## Apa itu Claude Code di web?

Claude Code di web memungkinkan pengembang untuk memulai Claude Code dari aplikasi Claude. Ini sempurna untuk:

* **Menjawab pertanyaan**: Tanyakan tentang arsitektur kode dan bagaimana fitur diimplementasikan
* **Perbaikan bug dan tugas rutin**: Tugas yang terdefinisi dengan baik yang tidak memerlukan pengarahan sering
* **Pekerjaan paralel**: Tangani beberapa perbaikan bug secara bersamaan
* **Repositori yang tidak ada di mesin lokal Anda**: Bekerja pada kode yang tidak Anda miliki checkout secara lokal
* **Perubahan backend**: Di mana Claude Code dapat menulis tes dan kemudian menulis kode untuk lulus tes tersebut

Claude Code juga tersedia di aplikasi Claude untuk [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) dan [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) untuk memulai tugas saat bepergian dan memantau pekerjaan yang sedang berlangsung.

Anda dapat [memulai tugas baru di web dari terminal Anda](#from-terminal-to-web) dengan `--remote`, atau [teleport sesi web kembali ke terminal Anda](#from-web-to-terminal) untuk melanjutkan secara lokal. Untuk menggunakan antarmuka web sambil menjalankan Claude Code di mesin Anda sendiri alih-alih infrastruktur cloud, lihat [Remote Control](/id/remote-control).

## Siapa yang dapat menggunakan Claude Code di web?

Claude Code di web tersedia dalam pratinjau penelitian untuk:

* **Pengguna Pro**
* **Pengguna Max**
* **Pengguna Team**
* **Pengguna Enterprise** dengan kursi premium atau kursi Chat + Claude Code

## Memulai

Siapkan Claude Code di web dari browser atau dari terminal Anda.

### Dari browser

1. Kunjungi [claude.ai/code](https://claude.ai/code)
2. Hubungkan akun GitHub Anda
3. Instal aplikasi Claude GitHub di repositori Anda
4. Pilih lingkungan default Anda
5. Kirimkan tugas pengkodean Anda
6. Tinjau perubahan dalam tampilan diff, ulangi dengan komentar, kemudian buat pull request

### Dari terminal

Jalankan `/web-setup` di dalam Claude Code untuk menghubungkan GitHub menggunakan kredensial CLI `gh` lokal Anda. Perintah ini menyinkronkan `gh auth token` Anda ke Claude Code di web, membuat lingkungan cloud default, dan membuka claude.ai/code di browser Anda saat selesai.

Jalur ini memerlukan CLI `gh` untuk diinstal dan diautentikasi dengan `gh auth login`. Jika `gh` tidak tersedia, `/web-setup` membuka claude.ai/code sehingga Anda dapat menghubungkan GitHub dari browser sebagai gantinya.

Kredensial `gh` Anda memberikan Claude akses untuk mengkloning dan mendorong, sehingga Anda dapat melewati Aplikasi GitHub untuk sesi dasar. Instal Aplikasi nanti jika Anda menginginkan [Auto-fix](#auto-fix-pull-requests), yang menggunakan Aplikasi untuk menerima webhook PR.

<Note>
  Admin Team dan Enterprise dapat menonaktifkan penyiapan terminal dengan toggle Quick web setup di [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
</Note>

## Cara kerjanya

Ketika Anda memulai tugas di Claude Code di web:

1. **Kloning repositori**: Repositori Anda dikloning ke mesin virtual yang dikelola Anthropic
2. **Penyiapan lingkungan**: Claude menyiapkan lingkungan cloud yang aman dengan kode Anda, kemudian menjalankan [skrip setup](#setup-scripts) Anda jika dikonfigurasi
3. **Konfigurasi jaringan**: Akses internet dikonfigurasi berdasarkan pengaturan Anda
4. **Eksekusi tugas**: Claude menganalisis kode, membuat perubahan, menjalankan tes, dan memeriksa pekerjaannya
5. **Penyelesaian**: Anda diberitahu ketika selesai dan dapat membuat PR dengan perubahan
6. **Hasil**: Perubahan didorong ke cabang, siap untuk pembuatan pull request

## Tinjau perubahan dengan tampilan diff

Tampilan diff memungkinkan Anda melihat dengan tepat apa yang diubah Claude sebelum membuat pull request. Alih-alih mengklik "Create PR" untuk meninjau perubahan di GitHub, lihat diff langsung di aplikasi dan ulangi dengan Claude sampai perubahan siap.

Ketika Claude membuat perubahan pada file, indikator statistik diff muncul menunjukkan jumlah baris yang ditambahkan dan dihapus (misalnya, `+12 -1`). Pilih indikator ini untuk membuka penampil diff, yang menampilkan daftar file di sebelah kiri dan perubahan untuk setiap file di sebelah kanan.

Dari tampilan diff, Anda dapat:

* Meninjau perubahan file demi file
* Berkomentar pada perubahan spesifik untuk meminta modifikasi
* Terus mengulangi dengan Claude berdasarkan apa yang Anda lihat

Ini memungkinkan Anda menyempurnakan perubahan melalui beberapa putaran umpan balik tanpa membuat PR draft atau beralih ke GitHub.

## Auto-fix pull requests

Claude dapat memantau pull request dan secara otomatis merespons kegagalan CI dan komentar ulasan. Claude berlangganan aktivitas GitHub di PR, dan ketika pemeriksaan gagal atau pengulas meninggalkan komentar, Claude menyelidiki dan mendorong perbaikan jika ada yang jelas.

<Note>
  Auto-fix memerlukan Aplikasi Claude GitHub untuk diinstal di repositori Anda. Jika Anda belum melakukannya, instal dari [halaman Aplikasi GitHub](https://github.com/apps/claude) atau saat diminta selama [penyiapan](#getting-started).
</Note>

Ada beberapa cara untuk mengaktifkan auto-fix tergantung di mana PR berasal dan perangkat apa yang Anda gunakan:

* **PR yang dibuat di Claude Code di web**: buka bilah status CI dan pilih **Auto-fix**
* **Dari aplikasi mobile**: beri tahu Claude untuk auto-fix PR, misalnya "watch this PR and fix any CI failures or review comments"
* **PR yang ada**: tempel URL PR ke sesi dan beri tahu Claude untuk auto-fix

### Bagaimana Claude merespons aktivitas PR

Ketika auto-fix aktif, Claude menerima acara GitHub untuk PR termasuk komentar ulasan baru dan kegagalan pemeriksaan CI. Untuk setiap acara, Claude menyelidiki dan memutuskan cara melanjutkan:

* **Perbaikan yang jelas**: jika Claude yakin dengan perbaikan dan tidak bertentangan dengan instruksi sebelumnya, Claude membuat perubahan, mendorongnya, dan menjelaskan apa yang dilakukan dalam sesi
* **Permintaan yang ambigu**: jika komentar pengulas dapat diinterpretasikan dengan beberapa cara atau melibatkan sesuatu yang secara arsitektur signifikan, Claude bertanya kepada Anda sebelum bertindak
* **Acara duplikat atau tanpa tindakan**: jika acara adalah duplikat atau tidak memerlukan perubahan, Claude mencatatnya dalam sesi dan melanjutkan

Claude dapat membalas utas komentar ulasan di GitHub sebagai bagian dari penyelesaiannya. Balasan ini diposting menggunakan akun GitHub Anda, sehingga muncul di bawah nama pengguna Anda, tetapi setiap balasan diberi label sebagai berasal dari Claude Code sehingga pengulas tahu itu ditulis oleh agen dan bukan oleh Anda secara langsung.

<Warning>
  Jika repositori Anda menggunakan otomasi yang dipicu komentar seperti Atlantis, Terraform Cloud, atau GitHub Actions kustom yang berjalan pada acara `issue_comment`, ketahui bahwa balasan Claude dapat memicu alur kerja tersebut. Tinjau otomasi repositori Anda sebelum mengaktifkan auto-fix, dan pertimbangkan untuk menonaktifkan auto-fix untuk repositori di mana komentar PR dapat menerapkan infrastruktur atau menjalankan operasi istimewa.
</Warning>

## Memindahkan tugas antara web dan terminal

Anda dapat memulai tugas baru di web dari terminal Anda, atau menarik sesi web ke terminal Anda untuk melanjutkan secara lokal. Sesi web bertahan bahkan jika Anda menutup laptop Anda, dan Anda dapat memantaunya dari mana saja termasuk aplikasi mobile Claude.

<Note>
  Handoff sesi adalah satu arah: Anda dapat menarik sesi web ke terminal Anda, tetapi Anda tidak dapat mendorong sesi terminal yang ada ke web. Bendera `--remote` membuat sesi web *baru* untuk repositori Anda saat ini.
</Note>

### Dari terminal ke web

Mulai sesi web dari baris perintah dengan bendera `--remote`:

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Ini membuat sesi web baru di claude.ai. Tugas berjalan di cloud sementara Anda terus bekerja secara lokal. Gunakan `/tasks` untuk memeriksa kemajuan, atau buka sesi di claude.ai atau aplikasi mobile Claude untuk berinteraksi langsung. Dari sana Anda dapat mengarahkan Claude, memberikan umpan balik, atau menjawab pertanyaan seperti percakapan lainnya.

#### Tips untuk tugas jarak jauh

**Rencanakan secara lokal, jalankan dari jarak jauh**: Untuk tugas kompleks, mulai Claude dalam plan mode untuk berkolaborasi pada pendekatan, kemudian kirim pekerjaan ke web:

```bash  theme={null}
claude --permission-mode plan
```

Dalam plan mode, Claude hanya dapat membaca file dan menjelajahi basis kode. Setelah Anda puas dengan rencana, mulai sesi jarak jauh untuk eksekusi otonom:

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Pola ini memberi Anda kontrol atas strategi sambil membiarkan Claude mengeksekusi secara otonom di cloud.

**Jalankan tugas secara paralel**: Setiap perintah `--remote` membuat sesi web sendiri yang berjalan secara independen. Anda dapat memulai beberapa tugas dan semuanya akan berjalan secara bersamaan dalam sesi terpisah:

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Pantau semua sesi dengan `/tasks`. Ketika sesi selesai, Anda dapat membuat PR dari antarmuka web atau [teleport](#from-web-to-terminal) sesi ke terminal Anda untuk melanjutkan bekerja.

### Dari web ke terminal

Ada beberapa cara untuk menarik sesi web ke terminal Anda:

* **Menggunakan `/teleport`**: Dari dalam Claude Code, jalankan `/teleport` (atau `/tp`) untuk melihat pemilih interaktif sesi web Anda. Jika Anda memiliki perubahan yang tidak dikomit, Anda akan diminta untuk menyimpannya terlebih dahulu.
* **Menggunakan `--teleport`**: Dari baris perintah, jalankan `claude --teleport` untuk pemilih sesi interaktif, atau `claude --teleport <session-id>` untuk melanjutkan sesi spesifik secara langsung.
* **Dari `/tasks`**: Jalankan `/tasks` untuk melihat sesi latar belakang Anda, kemudian tekan `t` untuk teleport ke salah satunya
* **Dari antarmuka web**: Klik "Open in CLI" untuk menyalin perintah yang dapat Anda tempel ke terminal Anda

Ketika Anda teleport sesi, Claude memverifikasi Anda berada di repositori yang benar, mengambil dan checkout cabang dari sesi jarak jauh, dan memuat riwayat percakapan lengkap ke terminal Anda.

#### Persyaratan untuk teleporting

Teleport memeriksa persyaratan ini sebelum melanjutkan sesi. Jika ada persyaratan yang tidak terpenuhi, Anda akan melihat kesalahan atau diminta untuk menyelesaikan masalah.

| Persyaratan           | Detail                                                                                                                                   |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Status git bersih     | Direktori kerja Anda harus tidak memiliki perubahan yang tidak dikomit. Teleport meminta Anda untuk menyimpan perubahan jika diperlukan. |
| Repositori yang benar | Anda harus menjalankan `--teleport` dari checkout repositori yang sama, bukan fork.                                                      |
| Cabang tersedia       | Cabang dari sesi web harus telah didorong ke remote. Teleport secara otomatis mengambil dan checkout.                                    |
| Akun yang sama        | Anda harus diautentikasi ke akun Claude.ai yang sama yang digunakan dalam sesi web.                                                      |

### Berbagi sesi

Untuk berbagi sesi, alihkan visibilitasnya sesuai dengan jenis akun di bawah ini. Setelah itu, bagikan tautan sesi apa adanya. Penerima yang membuka sesi bersama Anda akan melihat status terbaru sesi saat dimuat, tetapi halaman penerima tidak akan diperbarui secara real-time.

#### Berbagi dari akun Enterprise atau Teams

Untuk akun Enterprise dan Teams, dua opsi visibilitas adalah **Private** dan **Team**. Visibilitas Team membuat sesi terlihat oleh anggota lain dari organisasi Claude.ai Anda. Verifikasi akses repositori diaktifkan secara default, berdasarkan akun GitHub yang terhubung ke akun penerima Anda. Nama tampilan akun Anda terlihat oleh semua penerima dengan akses. Sesi [Claude in Slack](/id/slack) secara otomatis dibagikan dengan visibilitas Team.

#### Berbagi dari akun Max atau Pro

Untuk akun Max dan Pro, dua opsi visibilitas adalah **Private** dan **Public**. Visibilitas Public membuat sesi terlihat oleh pengguna mana pun yang masuk ke claude.ai.

Periksa sesi Anda untuk konten sensitif sebelum berbagi. Sesi dapat berisi kode dan kredensial dari repositori GitHub pribadi. Verifikasi akses repositori tidak diaktifkan secara default.

Aktifkan verifikasi akses repositori dan/atau tahan nama Anda dari sesi bersama Anda dengan membuka Settings > Claude Code > Sharing settings.

## Jadwalkan tugas berulang

Jalankan Claude pada jadwal berulang untuk mengotomatisasi pekerjaan seperti ulasan PR harian, audit dependensi, dan analisis kegagalan CI. Lihat [Schedule tasks on the web](/id/web-scheduled-tasks) untuk panduan lengkap.

## Mengelola sesi

### Mengarsipkan sesi

Anda dapat mengarsipkan sesi untuk menjaga daftar sesi Anda tetap terorganisir. Sesi yang diarsipkan disembunyikan dari daftar sesi default tetapi dapat dilihat dengan memfilter sesi yang diarsipkan.

Untuk mengarsipkan sesi, arahkan ke sesi di sidebar dan klik ikon arsip.

### Menghapus sesi

Menghapus sesi secara permanen menghapus sesi dan datanya. Tindakan ini tidak dapat dibatalkan. Anda dapat menghapus sesi dengan dua cara:

* **Dari sidebar**: Filter untuk sesi yang diarsipkan, kemudian arahkan ke sesi yang ingin Anda hapus dan klik ikon hapus
* **Dari menu sesi**: Buka sesi, klik dropdown di sebelah judul sesi, dan pilih **Delete**

Anda akan diminta untuk mengonfirmasi sebelum sesi dihapus.

## Lingkungan cloud

### Gambar default

Kami membangun dan memelihara gambar universal dengan toolchain umum dan ekosistem bahasa yang sudah diinstal sebelumnya. Gambar ini mencakup:

* Bahasa pemrograman dan runtime populer
* Alat build umum dan pengelola paket
* Framework pengujian dan linter

#### Memeriksa alat yang tersedia

Untuk melihat apa yang sudah diinstal di lingkungan Anda, minta Claude Code untuk menjalankan:

```bash  theme={null}
check-tools
```

Perintah ini menampilkan:

* Bahasa pemrograman dan versinya
* Pengelola paket yang tersedia
* Alat pengembangan yang diinstal

#### Penyiapan khusus bahasa

Gambar universal mencakup lingkungan yang sudah dikonfigurasi untuk:

* **Python**: Python 3.x dengan pip, poetry, dan perpustakaan ilmiah umum
* **Node.js**: Versi LTS terbaru dengan npm, yarn, pnpm, dan bun
* **Ruby**: Versi 3.1.6, 3.2.6, 3.3.6 (default: 3.3.6) dengan gem, bundler, dan rbenv untuk manajemen versi
* **PHP**: Versi 8.4.14
* **Java**: OpenJDK dengan Maven dan Gradle
* **Go**: Versi stabil terbaru dengan dukungan modul
* **Rust**: Rust toolchain dengan cargo
* **C++**: Kompiler GCC dan Clang

#### Database

Gambar universal mencakup database berikut:

* **PostgreSQL**: Versi 16
* **Redis**: Versi 7.0

### Konfigurasi lingkungan

Ketika Anda memulai sesi di Claude Code di web, inilah yang terjadi di balik layar:

1. **Persiapan lingkungan**: Kami mengkloning repositori Anda dan menjalankan [skrip setup](#setup-scripts) yang dikonfigurasi. Repo akan dikloning dengan cabang default di repo GitHub Anda. Jika Anda ingin checkout cabang spesifik, Anda dapat menentukan itu dalam prompt.

2. **Konfigurasi jaringan**: Kami mengonfigurasi akses internet untuk agen. Akses internet dibatasi secara default, tetapi Anda dapat mengonfigurasi lingkungan untuk tidak memiliki internet atau akses internet penuh berdasarkan kebutuhan Anda.

3. **Eksekusi Claude Code**: Claude Code berjalan untuk menyelesaikan tugas Anda, menulis kode, menjalankan tes, dan memeriksa pekerjaannya. Anda dapat memandu dan mengarahkan Claude sepanjang sesi melalui antarmuka web. Claude menghormati konteks yang telah Anda tentukan di `CLAUDE.md` Anda.

4. **Hasil**: Ketika Claude menyelesaikan pekerjaannya, itu akan mendorong cabang ke remote. Anda akan dapat membuat PR untuk cabang tersebut.

<Note>
  Claude beroperasi sepenuhnya melalui terminal dan alat CLI yang tersedia di lingkungan. Ini menggunakan alat yang sudah diinstal sebelumnya di gambar universal dan alat tambahan apa pun yang Anda instal melalui hooks atau manajemen dependensi.
</Note>

**Untuk menambahkan lingkungan baru:** Pilih lingkungan saat ini untuk membuka pemilih lingkungan, kemudian pilih "Add environment". Ini akan membuka dialog di mana Anda dapat menentukan nama lingkungan, tingkat akses jaringan, variabel lingkungan, dan [skrip setup](#setup-scripts).

**Untuk memperbarui lingkungan yang ada:** Pilih lingkungan saat ini, di sebelah kanan nama lingkungan, dan pilih tombol pengaturan. Ini akan membuka dialog di mana Anda dapat memperbarui nama lingkungan, akses jaringan, variabel lingkungan, dan skrip setup.

**Untuk memilih lingkungan default Anda dari terminal:** Jika Anda memiliki beberapa lingkungan yang dikonfigurasi, jalankan `/remote-env` untuk memilih mana yang akan digunakan saat memulai sesi web dari terminal Anda dengan `--remote`. Dengan satu lingkungan, perintah ini menunjukkan konfigurasi Anda saat ini.

<Note>
  Variabel lingkungan harus ditentukan sebagai pasangan kunci-nilai, dalam [format `.env`](https://www.dotenv.org/). Misalnya:

  ```text  theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Setup scripts

Setup script adalah skrip Bash yang berjalan ketika sesi cloud baru dimulai, sebelum Claude Code diluncurkan. Gunakan setup scripts untuk menginstal dependensi, mengonfigurasi alat, atau menyiapkan apa pun yang dibutuhkan lingkungan cloud yang tidak ada di [gambar default](#default-image).

Skrip berjalan sebagai root di Ubuntu 24.04, jadi `apt install` dan sebagian besar pengelola paket bahasa bekerja.

<Tip>
  Untuk memeriksa apa yang sudah diinstal sebelum menambahkannya ke skrip Anda, minta Claude untuk menjalankan `check-tools` dalam sesi cloud.
</Tip>

Untuk menambahkan setup script, buka dialog pengaturan lingkungan dan masukkan skrip Anda di bidang **Setup script**.

Contoh ini menginstal CLI `gh`, yang tidak ada di gambar default:

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Setup scripts berjalan hanya saat membuat sesi baru. Mereka dilewati saat melanjutkan sesi yang ada.

Jika skrip keluar dengan non-zero, sesi gagal dimulai. Tambahkan `|| true` ke perintah non-kritis untuk menghindari pemblokiran sesi pada instalasi yang tidak stabil.

<Note>
  Setup scripts yang menginstal paket memerlukan akses jaringan untuk menjangkau registri. Akses jaringan default memungkinkan koneksi ke [registri paket umum](#default-allowed-domains) termasuk npm, PyPI, RubyGems, dan crates.io. Skrip akan gagal menginstal paket jika lingkungan Anda memiliki akses jaringan yang dinonaktifkan.
</Note>

#### Setup scripts vs. SessionStart hooks

Gunakan setup script untuk menginstal hal-hal yang dibutuhkan cloud tetapi laptop Anda sudah memiliki, seperti runtime bahasa atau alat CLI. Gunakan [SessionStart hook](/id/hooks#sessionstart) untuk penyiapan proyek yang harus berjalan di mana-mana, cloud dan lokal, seperti `npm install`.

Keduanya berjalan di awal sesi, tetapi mereka termasuk di tempat yang berbeda:

|                  | Setup scripts                                         | SessionStart hooks                                                          |
| ---------------- | ----------------------------------------------------- | --------------------------------------------------------------------------- |
| Terlampir pada   | Lingkungan cloud                                      | Repositori Anda                                                             |
| Dikonfigurasi di | UI lingkungan cloud                                   | `.claude/settings.json` di repo Anda                                        |
| Berjalan         | Sebelum Claude Code diluncurkan, hanya pada sesi baru | Setelah Claude Code diluncurkan, pada setiap sesi termasuk yang dilanjutkan |
| Cakupan          | Hanya lingkungan cloud                                | Lokal dan cloud                                                             |

SessionStart hooks juga dapat didefinisikan di `~/.claude/settings.json` tingkat pengguna Anda secara lokal, tetapi pengaturan tingkat pengguna tidak terbawa ke sesi cloud. Di cloud, hanya hooks yang dikomit ke repo yang berjalan.

### Manajemen dependensi

Gambar lingkungan kustom dan snapshot belum didukung. Gunakan [setup scripts](#setup-scripts) untuk menginstal paket saat sesi dimulai, atau [SessionStart hooks](/id/hooks#sessionstart) untuk instalasi dependensi yang juga harus berjalan di lingkungan lokal. SessionStart hooks memiliki [batasan yang diketahui](#dependency-management-limitations).

Untuk mengonfigurasi instalasi dependensi otomatis dengan setup script, buka pengaturan lingkungan Anda dan tambahkan skrip:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

Alternatifnya, Anda dapat menggunakan SessionStart hooks di file `.claude/settings.json` repositori Anda untuk instalasi dependensi yang juga harus berjalan di lingkungan lokal:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Buat skrip yang sesuai di `scripts/install_pkgs.sh`:

```bash  theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Buat dapat dieksekusi: `chmod +x scripts/install_pkgs.sh`

#### Pertahankan variabel lingkungan

SessionStart hooks dapat mempertahankan variabel lingkungan untuk perintah Bash berikutnya dengan menulis ke file yang ditentukan dalam variabel lingkungan `CLAUDE_ENV_FILE`. Untuk detail, lihat [SessionStart hooks](/id/hooks#sessionstart) dalam referensi hooks.

#### Batasan manajemen dependensi

* **Hooks berjalan untuk semua sesi**: SessionStart hooks berjalan di lingkungan lokal dan jarak jauh. Tidak ada konfigurasi hook untuk membatasi hook hanya ke sesi jarak jauh. Untuk melewati eksekusi lokal, periksa variabel lingkungan `CLAUDE_CODE_REMOTE` dalam skrip Anda seperti yang ditunjukkan di atas.
* **Memerlukan akses jaringan**: Perintah install memerlukan akses jaringan untuk menjangkau registri paket. Jika lingkungan Anda dikonfigurasi dengan akses "No internet", hooks ini akan gagal. Gunakan akses jaringan "Limited" (default) atau "Full". [Daftar putih default](#default-allowed-domains) mencakup registri umum seperti npm, PyPI, RubyGems, dan crates.io.
* **Kompatibilitas proxy**: Semua lalu lintas keluar di lingkungan jarak jauh melewati [security proxy](#security-proxy). Beberapa pengelola paket tidak bekerja dengan benar dengan proxy ini. Bun adalah contoh yang diketahui.
* **Berjalan pada setiap awal sesi**: Hooks berjalan setiap kali sesi dimulai atau dilanjutkan, menambah latensi startup. Jaga skrip install tetap cepat dengan memeriksa apakah dependensi sudah ada sebelum menginstal ulang.

## Akses jaringan dan keamanan

### Kebijakan jaringan

#### Proxy GitHub

Untuk keamanan, semua operasi GitHub melewati layanan proxy khusus yang secara transparan menangani semua interaksi git. Di dalam sandbox, klien git mengautentikasi menggunakan kredensial bersistem yang dibuat khusus. Proxy ini:

* Mengelola autentikasi GitHub dengan aman - klien git menggunakan kredensial bersistem di dalam sandbox, yang diverifikasi proxy dan diterjemahkan ke token autentikasi GitHub aktual Anda
* Membatasi operasi git push ke cabang kerja saat ini untuk keamanan
* Memungkinkan kloning, pengambilan, dan operasi PR yang mulus sambil mempertahankan batas keamanan

#### Security proxy

Lingkungan berjalan di belakang proxy jaringan HTTP/HTTPS untuk tujuan keamanan dan pencegahan penyalahgunaan. Semua lalu lintas internet keluar melewati proxy ini, yang menyediakan:

* Perlindungan terhadap permintaan berbahaya
* Pembatasan laju dan pencegahan penyalahgunaan
* Penyaringan konten untuk keamanan yang ditingkatkan

### Tingkat akses

Secara default, akses jaringan dibatasi pada [domain yang diizinkan](#default-allowed-domains).

Anda dapat mengonfigurasi akses jaringan kustom, termasuk menonaktifkan akses jaringan.

### Domain yang diizinkan secara default

Saat menggunakan akses jaringan "Limited", domain berikut diizinkan secara default:

#### Layanan Anthropic

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### Kontrol Versi

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### Registri Kontainer

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* public.ecr.aws

#### Platform Cloud

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### Pengelola Paket - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Pengelola Paket - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Pengelola Paket - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### Pengelola Paket - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Pengelola Paket - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Pengelola Paket - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### Pengelola Paket - Bahasa Lain

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Distribusi Linux

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Alat Pengembangan & Platform

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### Layanan Cloud & Monitoring

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### Pengiriman Konten & Mirror

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Skema & Konfigurasi

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

<Note>
  Domain yang ditandai dengan `*` menunjukkan pencocokan subdomain wildcard. Misalnya, `*.gcr.io` memungkinkan akses ke subdomain apa pun dari `gcr.io`.
</Note>

### Praktik terbaik keamanan untuk akses jaringan yang disesuaikan

1. **Prinsip privilege minimal**: Hanya aktifkan akses jaringan minimum yang diperlukan
2. **Audit secara teratur**: Tinjau domain yang diizinkan secara berkala
3. **Gunakan HTTPS**: Selalu lebih suka endpoint HTTPS daripada HTTP

## Keamanan dan isolasi

Claude Code di web menyediakan jaminan keamanan yang kuat:

* **Mesin virtual terisolasi**: Setiap sesi berjalan di VM yang terisolasi dan dikelola Anthropic
* **Kontrol akses jaringan**: Akses jaringan dibatasi secara default, dan dapat dinonaktifkan

<Note>
  Saat berjalan dengan akses jaringan dinonaktifkan, Claude Code diizinkan untuk berkomunikasi dengan API Anthropic yang mungkin masih memungkinkan data keluar dari VM Claude Code yang terisolasi.
</Note>

* **Perlindungan kredensial**: Kredensial sensitif (seperti kredensial git atau kunci penandatanganan) tidak pernah ada di dalam sandbox dengan Claude Code. Autentikasi ditangani melalui proxy aman menggunakan kredensial bersistem
* **Analisis aman**: Kode dianalisis dan dimodifikasi dalam VM terisolasi sebelum membuat PR

## Harga dan batas laju

Claude Code di web berbagi batas laju dengan semua penggunaan Claude dan Claude Code lainnya dalam akun Anda. Menjalankan beberapa tugas secara paralel akan mengonsumsi lebih banyak batas laju secara proporsional.

## Batasan

* **Autentikasi repositori**: Anda hanya dapat memindahkan sesi dari web ke lokal saat Anda diautentikasi ke akun yang sama
* **Pembatasan platform**: Claude Code di web hanya bekerja dengan kode yang dihosting di GitHub. Instans [GitHub Enterprise Server](/id/github-enterprise-server) yang di-host sendiri didukung untuk rencana Teams dan Enterprise. Repositori GitLab dan non-GitHub lainnya tidak dapat digunakan dengan sesi cloud

## Praktik terbaik

1. **Otomatisasi penyiapan lingkungan**: Gunakan [setup scripts](#setup-scripts) untuk menginstal dependensi dan mengonfigurasi alat sebelum Claude Code diluncurkan. Untuk skenario yang lebih canggih, konfigurasikan [SessionStart hooks](/id/hooks#sessionstart).
2. **Dokumentasikan persyaratan**: Tentukan dengan jelas dependensi dan perintah di file `CLAUDE.md` Anda. Jika Anda memiliki file `AGENTS.md`, Anda dapat bersumber di `CLAUDE.md` Anda menggunakan `@AGENTS.md` untuk mempertahankan sumber kebenaran tunggal.

## Sumber daya terkait

* [Konfigurasi Hooks](/id/hooks)
* [Referensi Pengaturan](/id/settings)
* [Keamanan](/id/security)
* [Penggunaan Data](/id/data-usage)
