> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Gunakan Claude Code Desktop

> Dapatkan lebih banyak dari Claude Code Desktop: sesi paralel dengan isolasi Git, tinjauan diff visual, pratinjau aplikasi, pemantauan PR, mode izin, konektor, dan konfigurasi enterprise.

Tab Code dalam aplikasi Claude Desktop memungkinkan Anda menggunakan Claude Code melalui antarmuka grafis alih-alih terminal.

Desktop menambahkan kemampuan ini di atas pengalaman Claude Code standar:

* [Tinjauan diff visual](#review-changes-with-diff-view) dengan komentar inline
* [Pratinjau aplikasi langsung](#preview-your-app) dengan server dev
* [Pemantauan PR GitHub](#monitor-pull-request-status) dengan perbaikan otomatis dan penggabungan otomatis
* [Sesi paralel](#work-in-parallel-with-sessions) dengan isolasi Git worktree otomatis
* [Tugas terjadwal](#schedule-recurring-tasks) yang menjalankan Claude sesuai jadwal berulang
* [Konektor](#connect-external-tools) untuk GitHub, Slack, Linear, dan lainnya
* Lingkungan lokal, [SSH](#ssh-sessions), dan [cloud](#run-long-running-tasks-remotely)

<Tip>
  Baru di Desktop? Mulai dengan [Memulai](/id/desktop-quickstart) untuk memasang aplikasi dan membuat edit pertama Anda.
</Tip>

Halaman ini mencakup [bekerja dengan kode](#work-with-code), [mengelola sesi](#manage-sessions), [memperluas Claude Code](#extend-claude-code), [tugas terjadwal](#schedule-recurring-tasks), dan [konfigurasi](#environment-configuration). Halaman ini juga mencakup [perbandingan CLI](#coming-from-the-cli) dan [pemecahan masalah](#troubleshooting).

## Mulai sesi

Sebelum Anda mengirim pesan pertama, konfigurasikan empat hal di area prompt:

* **Lingkungan**: pilih di mana Claude berjalan. Pilih **Lokal** untuk mesin Anda, **Jarak Jauh** untuk sesi cloud yang dihosting Anthropic, atau [**koneksi SSH**](#ssh-sessions) untuk mesin jarak jauh yang Anda kelola. Lihat [konfigurasi lingkungan](#environment-configuration).
* **Folder proyek**: pilih folder atau repositori tempat Claude bekerja. Untuk sesi jarak jauh, Anda dapat menambahkan [beberapa repositori](#run-long-running-tasks-remotely).
* **Model**: pilih [model](/id/model-config#available-models) dari dropdown di sebelah tombol kirim. Model dikunci setelah sesi dimulai.
* **Mode izin**: pilih berapa banyak otonomi yang dimiliki Claude dari [pemilih mode](#choose-a-permission-mode). Anda dapat mengubah ini selama sesi.

Ketik tugas Anda dan tekan **Enter** untuk memulai. Setiap sesi melacak konteksnya sendiri dan perubahan secara independen.

## Bekerja dengan kode

Berikan Claude konteks yang tepat, kontrol berapa banyak yang dilakukannya sendiri, dan tinjau apa yang diubahnya.

### Gunakan kotak prompt

Ketik apa yang ingin Anda lakukan Claude dan tekan **Enter** untuk mengirim. Claude membaca file proyek Anda, membuat perubahan, dan menjalankan perintah berdasarkan [mode izin](#choose-a-permission-mode) Anda. Anda dapat menghentikan Claude kapan saja: klik tombol berhenti atau ketik koreksi Anda dan tekan **Enter**. Claude berhenti melakukan apa yang sedang dilakukannya dan menyesuaikan berdasarkan input Anda.

Tombol **+** di sebelah kotak prompt memberi Anda akses ke lampiran file, [skills](#use-skills), [konektor](#connect-external-tools), dan [plugins](#install-plugins).

### Tambahkan file dan konteks ke prompt

Kotak prompt mendukung dua cara untuk membawa konteks eksternal:

* **File @mention**: ketik `@` diikuti nama file untuk menambahkan file ke konteks percakapan. Claude kemudian dapat membaca dan mereferensikan file tersebut.
* **Lampirkan file**: lampirkan gambar, PDF, dan file lainnya ke prompt Anda menggunakan tombol lampiran, atau seret dan lepas file langsung ke prompt. Ini berguna untuk berbagi tangkapan layar bug, mockup desain, atau dokumen referensi.

### Pilih mode izin

Mode izin mengontrol berapa banyak otonomi yang dimiliki Claude selama sesi: apakah itu meminta izin sebelum mengedit file, menjalankan perintah, atau keduanya. Anda dapat beralih mode kapan saja menggunakan pemilih mode di sebelah tombol kirim. Mulai dengan Minta izin untuk melihat dengan tepat apa yang dilakukan Claude, kemudian pindah ke Terima edit otomatis atau Mode Rencana saat Anda merasa nyaman.

| Mode                     | Kunci Pengaturan    | Perilaku                                                                                                                                                                                                                                                                               |
| ------------------------ | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Minta izin**           | `default`           | Claude meminta izin sebelum mengedit file atau menjalankan perintah. Anda melihat diff dan dapat menerima atau menolak setiap perubahan. Direkomendasikan untuk pengguna baru.                                                                                                         |
| **Terima edit otomatis** | `acceptEdits`       | Claude secara otomatis menerima edit file tetapi masih meminta izin sebelum menjalankan perintah terminal. Gunakan ini ketika Anda mempercayai perubahan file dan menginginkan iterasi yang lebih cepat.                                                                               |
| **Mode Rencana**         | `plan`              | Claude menganalisis kode Anda dan membuat rencana tanpa memodifikasi file atau menjalankan perintah. Bagus untuk tugas kompleks di mana Anda ingin meninjau pendekatan terlebih dahulu.                                                                                                |
| **Lewati izin**          | `bypassPermissions` | Claude berjalan tanpa prompt izin apa pun, setara dengan `--dangerously-skip-permissions` di CLI. Aktifkan di Pengaturan Anda → Claude Code di bawah "Izinkan mode lewati izin". Hanya gunakan ini di kontainer atau VM yang disandbox. Admin enterprise dapat menonaktifkan opsi ini. |

Mode izin `dontAsk` hanya tersedia di [CLI](/id/permissions#permission-modes).

<Tip title="Praktik terbaik">
  Mulai tugas kompleks di Mode Rencana sehingga Claude memetakan pendekatan sebelum membuat perubahan. Setelah Anda menyetujui rencana, beralih ke Terima edit otomatis atau Minta izin untuk menjalankannya. Lihat [jelajahi terlebih dahulu, kemudian rencanakan, kemudian kode](/id/best-practices#explore-first-then-plan-then-code) untuk informasi lebih lanjut tentang alur kerja ini.
</Tip>

Sesi jarak jauh mendukung Terima edit otomatis dan Mode Rencana. Minta izin tidak tersedia karena sesi jarak jauh secara otomatis menerima edit file secara default, dan Lewati izin tidak tersedia karena lingkungan jarak jauh sudah disandbox.

Admin enterprise dapat membatasi mode izin mana yang tersedia. Lihat [konfigurasi enterprise](#enterprise-configuration) untuk detail.

### Pratinjau aplikasi Anda

Claude dapat memulai server dev dan membuka browser tertanam untuk memverifikasi perubahannya. Ini berfungsi untuk aplikasi web frontend serta server backend: Claude dapat menguji endpoint API, melihat log server, dan mengulangi masalah yang ditemukannya. Dalam kebanyakan kasus, Claude memulai server secara otomatis setelah mengedit file proyek. Anda juga dapat meminta Claude untuk pratinjau kapan saja. Secara default, Claude [memverifikasi otomatis](#auto-verify-changes) perubahan setelah setiap edit.

Dari panel pratinjau, Anda dapat:

* Berinteraksi dengan aplikasi yang sedang berjalan langsung di browser tertanam
* Tonton Claude memverifikasi perubahannya sendiri secara otomatis: mengambil tangkapan layar, memeriksa DOM, mengklik elemen, mengisi formulir, dan memperbaiki masalah yang ditemukannya
* Mulai atau hentikan server dari dropdown **Pratinjau** di toolbar sesi
* Pertahankan cookie dan penyimpanan lokal di seluruh restart server dengan memilih **Pertahankan sesi** di dropdown, sehingga Anda tidak perlu masuk kembali selama pengembangan
* Edit konfigurasi server atau hentikan semua server sekaligus

Claude membuat konfigurasi server awal berdasarkan proyek Anda. Jika aplikasi Anda menggunakan perintah dev khusus, edit `.claude/launch.json` agar sesuai dengan setup Anda. Lihat [Konfigurasi server pratinjau](#configure-preview-servers) untuk referensi lengkap.

Untuk menghapus data sesi yang disimpan, aktifkan **Pertahankan sesi pratinjau** di Pengaturan → Claude Code. Untuk menonaktifkan pratinjau sepenuhnya, aktifkan **Pratinjau** di Pengaturan → Claude Code.

### Tinjau perubahan dengan tampilan diff

Setelah Claude membuat perubahan pada kode Anda, tampilan diff memungkinkan Anda meninjau modifikasi file demi file sebelum membuat pull request.

Ketika Claude mengubah file, indikator statistik diff muncul menunjukkan jumlah baris yang ditambahkan dan dihapus, seperti `+12 -1`. Klik indikator ini untuk membuka penampil diff, yang menampilkan daftar file di sebelah kiri dan perubahan untuk setiap file di sebelah kanan.

Untuk mengomentari baris tertentu, klik baris apa pun di diff untuk membuka kotak komentar. Ketik umpan balik Anda dan tekan **Enter** untuk menambahkan komentar. Setelah menambahkan komentar ke beberapa baris, kirimkan semua komentar sekaligus:

* **macOS**: tekan **Cmd+Enter**
* **Windows**: tekan **Ctrl+Enter**

Claude membaca komentar Anda dan membuat perubahan yang diminta, yang muncul sebagai diff baru yang dapat Anda tinjau.

### Tinjau kode Anda

Di tampilan diff, klik **Tinjau kode** di toolbar kanan atas untuk meminta Claude mengevaluasi perubahan sebelum Anda melakukan commit. Claude memeriksa diff saat ini dan meninggalkan komentar langsung di tampilan diff. Anda dapat merespons komentar apa pun atau meminta Claude untuk merevisi.

Tinjauan berfokus pada masalah sinyal tinggi: kesalahan kompilasi, kesalahan logika pasti, kerentanan keamanan, dan bug yang jelas. Ini tidak menandai gaya, pemformatan, masalah yang sudah ada sebelumnya, atau apa pun yang akan ditangkap linter.

### Pantau status pull request

Setelah Anda membuka pull request, bilah status CI muncul di sesi. Claude Code menggunakan GitHub CLI untuk menanyakan hasil pemeriksaan dan menampilkan kegagalan.

* **Perbaikan otomatis**: ketika diaktifkan, Claude secara otomatis mencoba memperbaiki pemeriksaan CI yang gagal dengan membaca output kegagalan dan mengulangi.
* **Penggabungan otomatis**: ketika diaktifkan, Claude menggabungkan PR setelah semua pemeriksaan lulus. Metode penggabungan adalah squash. Penggabungan otomatis harus [diaktifkan di pengaturan repositori GitHub Anda](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) agar ini berfungsi.

Gunakan toggle **Perbaikan otomatis** dan **Penggabungan otomatis** di bilah status CI untuk mengaktifkan salah satu opsi. Claude Code juga mengirim notifikasi desktop ketika CI selesai.

<Note>
  Pemantauan PR memerlukan [GitHub CLI (`gh`)](https://cli.github.com/) untuk diinstal dan diautentikasi di mesin Anda. Jika `gh` tidak diinstal, Desktop akan meminta Anda untuk memasangnya saat pertama kali Anda mencoba membuat PR.
</Note>

## Kelola sesi

Setiap sesi adalah percakapan independen dengan konteks dan perubahannya sendiri. Anda dapat menjalankan beberapa sesi secara paralel atau mengirim pekerjaan ke cloud.

### Bekerja secara paralel dengan sesi

Klik **+ Sesi Baru** di sidebar untuk bekerja pada beberapa tugas secara paralel. Untuk repositori Git, setiap sesi mendapatkan salinan proyek Anda yang terisolasi menggunakan [Git worktrees](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), sehingga perubahan dalam satu sesi tidak mempengaruhi sesi lain sampai Anda melakukan commit.

Worktrees disimpan di `<project-root>/.claude/worktrees/` secara default. Anda dapat mengubah ini ke direktori khusus di Pengaturan → Claude Code di bawah "Lokasi Worktree". Anda juga dapat mengatur awalan cabang yang ditambahkan ke setiap nama cabang worktree, yang berguna untuk menjaga cabang yang dibuat Claude tetap terorganisir. Untuk menghapus worktree setelah selesai, arahkan ke sesi di sidebar dan klik ikon arsip.

<Note>
  Isolasi sesi memerlukan [Git](https://git-scm.com/downloads). Sebagian besar Mac menyertakan Git secara default. Jalankan `git --version` di Terminal untuk memeriksa. Di Windows, Git diperlukan agar tab Code berfungsi: [unduh Git untuk Windows](https://git-scm.com/downloads/win), pasang, dan mulai ulang aplikasi. Jika Anda mengalami kesalahan Git, coba sesi Cowork untuk membantu memecahkan masalah setup Anda.
</Note>

Gunakan ikon filter di bagian atas sidebar untuk memfilter sesi berdasarkan status (Aktif, Diarsipkan) dan lingkungan (Lokal, Cloud). Untuk mengganti nama sesi atau memeriksa penggunaan konteks, klik judul sesi di toolbar di bagian atas sesi aktif. Ketika konteks penuh, Claude secara otomatis merangkum percakapan dan terus bekerja. Anda juga dapat mengetik `/compact` untuk memicu perangkuman lebih awal dan membebaskan ruang konteks. Lihat [jendela konteks](/id/how-claude-code-works#the-context-window) untuk detail tentang cara pemadatan bekerja.

### Jalankan tugas jangka panjang dari jarak jauh

Untuk refaktor besar, suite pengujian, migrasi, atau tugas jangka panjang lainnya, pilih **Jarak Jauh** alih-alih **Lokal** saat memulai sesi. Sesi jarak jauh berjalan di infrastruktur cloud Anthropic dan terus berjalan bahkan jika Anda menutup aplikasi atau mematikan komputer. Periksa kembali kapan saja untuk melihat kemajuan atau mengarahkan Claude ke arah yang berbeda. Anda juga dapat memantau sesi jarak jauh dari [claude.ai/code](https://claude.ai/code) atau aplikasi Claude iOS.

Sesi jarak jauh juga mendukung beberapa repositori. Setelah memilih lingkungan cloud, klik tombol **+** di sebelah pil repo untuk menambahkan repositori tambahan ke sesi. Setiap repo mendapatkan pemilih cabang sendiri. Ini berguna untuk tugas yang mencakup beberapa basis kode, seperti memperbarui perpustakaan bersama dan konsumennya.

Lihat [Claude Code di web](/id/claude-code-on-the-web) untuk informasi lebih lanjut tentang cara kerja sesi jarak jauh.

### Lanjutkan di permukaan lain

Menu **Lanjutkan di**, dapat diakses dari ikon VS Code di kanan bawah toolbar sesi, memungkinkan Anda memindahkan sesi ke permukaan lain:

* **Claude Code di Web**: mengirim sesi lokal Anda untuk terus berjalan dari jarak jauh. Desktop mendorong cabang Anda, menghasilkan ringkasan percakapan, dan membuat sesi jarak jauh baru dengan konteks lengkap. Anda kemudian dapat memilih untuk mengarsipkan sesi lokal atau menyimpannya. Ini memerlukan pohon kerja yang bersih, dan tidak tersedia untuk sesi SSH.
* **IDE Anda**: membuka proyek Anda di IDE yang didukung di direktori kerja saat ini.

## Perluas Claude Code

Hubungkan layanan eksternal, tambahkan alur kerja yang dapat digunakan kembali, sesuaikan perilaku Claude, dan konfigurasikan server pratinjau.

### Hubungkan alat eksternal

Untuk sesi lokal dan [SSH](#ssh-sessions), klik tombol **+** di sebelah kotak prompt dan pilih **Konektor** untuk menambahkan integrasi seperti Google Calendar, Slack, GitHub, Linear, Notion, dan lainnya. Anda dapat menambahkan konektor sebelum atau selama sesi. Konektor tidak tersedia untuk sesi jarak jauh.

Untuk mengelola atau memutuskan konektor, buka Pengaturan → Konektor di aplikasi desktop, atau pilih **Kelola konektor** dari menu Konektor di kotak prompt.

Setelah terhubung, Claude dapat membaca kalender Anda, mengirim pesan, membuat masalah, dan berinteraksi dengan alat Anda secara langsung. Anda dapat meminta Claude konektor apa yang dikonfigurasi di sesi Anda.

Konektor adalah [MCP servers](/id/mcp) dengan alur pengaturan grafis. Gunakan untuk integrasi cepat dengan layanan yang didukung. Untuk integrasi yang tidak tercantum di Konektor, tambahkan MCP servers secara manual melalui [file pengaturan](/id/mcp#installing-mcp-servers). Anda juga dapat [membuat konektor khusus](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Gunakan skills

[Skills](/id/skills) memperluas apa yang dapat dilakukan Claude. Claude memuatnya secara otomatis ketika relevan, atau Anda dapat menginvokan satu secara langsung: ketik `/` di kotak prompt atau klik tombol **+** dan pilih **Slash commands** untuk melihat apa yang tersedia. Ini mencakup [perintah bawaan](/id/interactive-mode#built-in-commands), [skills khusus](/id/skills#create-custom-skills) Anda, skills proyek dari basis kode Anda, dan skills dari [plugins yang diinstal](/id/plugins) apa pun. Pilih satu dan itu muncul disorot di bidang input. Ketik tugas Anda setelahnya dan kirim seperti biasa.

### Instal plugins

[Plugins](/id/plugins) adalah paket yang dapat digunakan kembali yang menambahkan skills, agents, hooks, MCP servers, dan konfigurasi LSP ke Claude Code. Anda dapat memasang plugins dari aplikasi desktop tanpa menggunakan terminal.

Untuk sesi lokal dan [SSH](#ssh-sessions), klik tombol **+** di sebelah kotak prompt dan pilih **Plugins** untuk melihat plugins yang diinstal dan perintahnya. Untuk menambahkan plugin, pilih **Tambah plugin** dari submenu untuk membuka browser plugin, yang menampilkan plugins yang tersedia dari [marketplaces](/id/plugin-marketplaces) yang dikonfigurasi termasuk marketplace Anthropic resmi. Pilih **Kelola plugins** untuk mengaktifkan, menonaktifkan, atau mencopot plugins.

Plugins dapat dibatasi pada akun pengguna Anda, proyek tertentu, atau lokal saja. Plugins tidak tersedia untuk sesi jarak jauh. Untuk referensi plugin lengkap termasuk membuat plugins Anda sendiri, lihat [plugins](/id/plugins).

### Konfigurasikan server pratinjau

Claude secara otomatis mendeteksi setup server dev Anda dan menyimpan konfigurasi di `.claude/launch.json` di root folder yang Anda pilih saat memulai sesi. Pratinjau menggunakan folder ini sebagai direktori kerjanya, jadi jika Anda memilih folder induk, subfolder dengan server dev mereka sendiri tidak akan terdeteksi secara otomatis. Untuk bekerja dengan server subfolder, mulai sesi di folder itu secara langsung atau tambahkan konfigurasi secara manual.

Untuk menyesuaikan cara server Anda dimulai, misalnya menggunakan `yarn dev` alih-alih `npm run dev` atau mengubah port, edit file secara manual atau klik **Edit konfigurasi** di dropdown Pratinjau untuk membukanya di editor kode Anda. File mendukung JSON dengan komentar.

```json  theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Anda dapat menentukan beberapa konfigurasi untuk menjalankan server berbeda dari proyek yang sama, seperti frontend dan API. Lihat [contoh](#examples) di bawah.

#### Verifikasi otomatis perubahan

Ketika `autoVerify` diaktifkan, Claude secara otomatis memverifikasi perubahan kode setelah mengedit file. Mengambil tangkapan layar, memeriksa kesalahan, dan mengkonfirmasi perubahan berfungsi sebelum menyelesaikan responsnya.

Verifikasi otomatis aktif secara default. Nonaktifkan per-proyek dengan menambahkan `"autoVerify": false` ke `.claude/launch.json`, atau aktifkan dari menu dropdown **Pratinjau**.

```json  theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Ketika dinonaktifkan, alat pratinjau masih tersedia dan Anda dapat meminta Claude untuk memverifikasi kapan saja. Verifikasi otomatis membuatnya otomatis setelah setiap edit.

#### Bidang konfigurasi

Setiap entri dalam array `configurations` menerima bidang berikut:

| Bidang              | Tipe      | Deskripsi                                                                                                                                                                                                                                                   |
| ------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Pengidentifikasi unik untuk server ini                                                                                                                                                                                                                      |
| `runtimeExecutable` | string    | Perintah untuk dijalankan, seperti `npm`, `yarn`, atau `node`                                                                                                                                                                                               |
| `runtimeArgs`       | string\[] | Argumen yang dilewatkan ke `runtimeExecutable`, seperti `["run", "dev"]`                                                                                                                                                                                    |
| `port`              | number    | Port yang didengarkan server Anda. Default ke 3000                                                                                                                                                                                                          |
| `cwd`               | string    | Direktori kerja relatif terhadap root proyek Anda. Default ke root proyek. Gunakan `${workspaceFolder}` untuk mereferensikan root proyek secara eksplisit                                                                                                   |
| `env`               | object    | Variabel lingkungan tambahan sebagai pasangan kunci-nilai, seperti `{ "NODE_ENV": "development" }`. Jangan letakkan rahasia di sini karena file ini dilakukan commit ke repo Anda. Rahasia yang ditetapkan di profil shell Anda diwariskan secara otomatis. |
| `autoPort`          | boolean   | Cara menangani konflik port. Lihat di bawah                                                                                                                                                                                                                 |
| `program`           | string    | Skrip untuk dijalankan dengan `node`. Lihat [kapan menggunakan `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                 |
| `args`              | string\[] | Argumen yang dilewatkan ke `program`. Hanya digunakan ketika `program` diatur                                                                                                                                                                               |

##### Kapan menggunakan `program` vs `runtimeExecutable`

Gunakan `runtimeExecutable` dengan `runtimeArgs` untuk memulai server dev melalui pengelola paket. Misalnya, `"runtimeExecutable": "npm"` dengan `"runtimeArgs": ["run", "dev"]` menjalankan `npm run dev`.

Gunakan `program` ketika Anda memiliki skrip mandiri yang ingin Anda jalankan dengan `node` secara langsung. Misalnya, `"program": "server.js"` menjalankan `node server.js`. Lewatkan flag tambahan dengan `args`.

#### Konflik port

Bidang `autoPort` mengontrol apa yang terjadi ketika port pilihan Anda sudah digunakan:

* **`true`**: Claude menemukan dan menggunakan port gratis secara otomatis. Cocok untuk sebagian besar server dev.
* **`false`**: Claude gagal dengan kesalahan. Gunakan ini ketika server Anda harus menggunakan port tertentu, seperti untuk callback OAuth atau allowlist CORS.
* **Tidak diatur (default)**: Claude menanyakan apakah server memerlukan port itu, kemudian menyimpan jawaban Anda.

Ketika Claude memilih port yang berbeda, itu melewatkan port yang ditugaskan ke server Anda melalui variabel lingkungan `PORT`.

#### Contoh

Konfigurasi ini menunjukkan setup umum untuk tipe proyek berbeda:

<Tabs>
  <Tab title="Next.js">
    Konfigurasi ini menjalankan aplikasi Next.js menggunakan Yarn di port 3000:

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Untuk monorepo dengan server frontend dan API, tentukan beberapa konfigurasi. Frontend menggunakan `autoPort: true` sehingga memilih port gratis jika 3000 diambil, sementara server API memerlukan port 8080 dengan tepat:

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Untuk menjalankan skrip Node.js secara langsung alih-alih menggunakan perintah pengelola paket, gunakan bidang `program`:

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Jadwalkan tugas berulang

Tugas terjadwal memulai sesi lokal baru secara otomatis pada waktu dan frekuensi yang Anda pilih. Gunakan untuk pekerjaan berulang seperti tinjauan kode harian, pemeriksaan pembaruan dependensi, atau briefing pagi yang menarik dari kalender dan inbox Anda.

Tugas berjalan di mesin Anda, jadi aplikasi desktop harus terbuka dan komputer Anda terjaga agar mereka dapat dijalankan. Lihat [Cara tugas terjadwal berjalan](#how-scheduled-tasks-run) untuk detail tentang run yang terlewat dan perilaku catch-up.

<Note>
  Secara default, tugas terjadwal berjalan terhadap status apa pun yang ada di direktori kerja Anda, termasuk perubahan yang tidak dilakukan commit. Aktifkan toggle worktree di input prompt untuk memberikan setiap run worktree Git terisolasi sendiri, dengan cara yang sama [sesi paralel](#work-in-parallel-with-sessions) bekerja.
</Note>

Untuk membuat tugas terjadwal, klik **Jadwal** di sidebar, kemudian **+ Tugas Baru**. Konfigurasikan bidang ini:

| Bidang    | Deskripsi                                                                                                                                                                                                                          |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nama      | Pengidentifikasi untuk tugas. Dikonversi ke kebab-case huruf kecil dan digunakan sebagai nama folder di disk. Harus unik di seluruh tugas Anda.                                                                                    |
| Deskripsi | Ringkasan singkat yang ditampilkan di daftar tugas.                                                                                                                                                                                |
| Prompt    | Instruksi yang dikirim ke Claude ketika tugas berjalan. Tulis ini dengan cara yang sama seperti Anda menulis pesan apa pun di kotak prompt. Input prompt juga mencakup kontrol untuk model, mode izin, folder kerja, dan worktree. |
| Frekuensi | Seberapa sering tugas berjalan. Lihat [opsi frekuensi](#frequency-options) di bawah.                                                                                                                                               |

Anda juga dapat membuat tugas dengan mendeskripsikan apa yang Anda inginkan di sesi apa pun. Misalnya, "atur tinjauan kode harian yang berjalan setiap pagi jam 9 pagi."

### Opsi frekuensi

* **Manual**: tidak ada jadwal, hanya berjalan ketika Anda klik **Jalankan sekarang**. Berguna untuk menyimpan prompt yang Anda picu sesuai permintaan
* **Setiap jam**: berjalan setiap jam. Setiap tugas mendapatkan offset tetap hingga 10 menit dari atas jam untuk menjarangkan lalu lintas API
* **Harian**: menampilkan pemilih waktu, default ke 9:00 AM waktu lokal
* **Hari kerja**: sama dengan Harian tetapi melewati Sabtu dan Minggu
* **Mingguan**: menampilkan pemilih waktu dan pemilih hari

Untuk interval yang tidak ditawarkan pemilih (setiap 15 menit, hari pertama setiap bulan, dll.), minta Claude di sesi Desktop apa pun untuk mengatur jadwal. Gunakan bahasa biasa; misalnya, "jadwalkan tugas untuk menjalankan semua tes setiap 6 jam."

### Cara tugas terjadwal berjalan

Tugas terjadwal berjalan secara lokal di mesin Anda. Desktop memeriksa jadwal setiap menit saat aplikasi terbuka dan memulai sesi segar ketika tugas jatuh tempo, independen dari sesi manual apa pun yang Anda buka. Setiap tugas mendapatkan penundaan tetap hingga 10 menit setelah waktu terjadwal untuk menjarangkan lalu lintas API. Penundaan bersifat deterministik: tugas yang sama selalu dimulai pada offset yang sama.

Ketika tugas dijalankan, Anda mendapatkan notifikasi desktop dan sesi baru muncul di bawah bagian **Terjadwal** di sidebar. Buka untuk melihat apa yang dilakukan Claude, tinjau perubahan, atau respons ke prompt izin. Sesi bekerja seperti yang lain: Claude dapat mengedit file, menjalankan perintah, membuat commit, dan membuka pull request.

Tugas hanya berjalan saat aplikasi desktop berjalan dan komputer Anda terjaga. Jika komputer Anda tidur melalui waktu terjadwal, run dilewati. Untuk mencegah idle-sleep, aktifkan **Jaga komputer tetap terjaga** di Pengaturan di bawah **Aplikasi desktop → Umum**. Menutup tutup laptop masih membuatnya tidur.

### Run yang terlewat

Ketika aplikasi dimulai atau komputer Anda bangun, Desktop memeriksa apakah setiap tugas melewatkan run apa pun dalam tujuh hari terakhir. Jika ya, Desktop memulai tepat satu run catch-up untuk waktu yang paling baru terlewat dan membuang apa pun yang lebih lama. Tugas harian yang melewatkan enam hari berjalan sekali saat bangun. Desktop menampilkan notifikasi ketika run catch-up dimulai.

Ingat ini saat menulis prompt. Tugas yang dijadwalkan untuk 9 pagi mungkin berjalan pada 11 malam jika komputer Anda tidur sepanjang hari. Jika waktu penting, tambahkan penjaga ke prompt itu sendiri, misalnya: "Hanya tinjau commit hari ini. Jika sudah setelah jam 5 sore, lewati tinjauan dan hanya posting ringkasan apa yang terlewat."

### Izin untuk tugas terjadwal

Setiap tugas memiliki mode izin sendiri, yang Anda atur saat membuat atau mengedit tugas. Aturan izin dari `~/.claude/settings.json` juga berlaku untuk sesi tugas terjadwal. Jika tugas berjalan dalam mode Tanya dan perlu menjalankan alat yang tidak memiliki izin, run macet sampai Anda menyetujuinya. Sesi tetap terbuka di sidebar sehingga Anda dapat menjawab nanti.

Untuk menghindari macet, klik **Jalankan sekarang** setelah membuat tugas, tonton prompt izin, dan pilih "selalu izinkan" untuk setiap satu. Run tugas masa depan secara otomatis menyetujui alat yang sama tanpa meminta. Anda dapat meninjau dan mencabut persetujuan ini dari halaman detail tugas.

### Kelola tugas terjadwal

Klik tugas di daftar **Jadwal** untuk membuka halaman detailnya. Dari sini Anda dapat:

* **Jalankan sekarang**: mulai tugas segera tanpa menunggu waktu terjadwal berikutnya
* **Toggle berulang**: jeda atau lanjutkan run terjadwal tanpa menghapus tugas
* **Edit**: ubah prompt, frekuensi, folder, atau pengaturan lainnya
* **Tinjau riwayat**: lihat setiap run masa lalu, termasuk yang dilewati karena komputer Anda tidur
* **Tinjau izin yang diizinkan**: lihat dan cabut persetujuan alat yang disimpan untuk tugas ini dari panel **Selalu diizinkan**
* **Hapus**: hapus tugas dan arsipkan semua sesi yang dibuatnya

Anda juga dapat mengelola tugas dengan meminta Claude di sesi Desktop apa pun. Misalnya, "jeda tugas dependency-audit saya", "hapus tugas standup-prep", atau "tunjukkan tugas terjadwal saya."

Untuk mengedit prompt tugas di disk, buka `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (atau di bawah [`CLAUDE_CONFIG_DIR`](/id/settings#environment-variables) jika diatur). File menggunakan frontmatter YAML untuk `name` dan `description`, dengan prompt sebagai body. Perubahan berlaku pada run berikutnya. Jadwal, folder, model, dan status yang diaktifkan tidak ada di file ini: ubah melalui formulir Edit atau minta Claude.

## Konfigurasi lingkungan

Lingkungan yang Anda pilih saat [memulai sesi](#start-a-session) menentukan di mana Claude mengeksekusi dan cara Anda terhubung:

* **Lokal**: berjalan di mesin Anda dengan akses langsung ke file Anda
* **Jarak Jauh**: berjalan di infrastruktur cloud Anthropic. Sesi terus berlanjut bahkan jika Anda menutup aplikasi.
* **SSH**: berjalan di mesin jarak jauh yang Anda hubungkan melalui SSH, seperti server Anda sendiri, cloud VM, atau dev containers

### Sesi lokal

Sesi lokal mewarisi variabel lingkungan dari shell Anda. Jika Anda memerlukan variabel tambahan, atur di profil shell Anda, seperti `~/.zshrc` atau `~/.bashrc`, dan mulai ulang aplikasi desktop. Lihat [variabel lingkungan](/id/settings#environment-variables) untuk daftar lengkap variabel yang didukung.

[Extended thinking](/id/common-workflows#use-extended-thinking-thinking-mode) diaktifkan secara default, yang meningkatkan kinerja pada tugas penalaran kompleks tetapi menggunakan token tambahan. Untuk menonaktifkan pemikiran sepenuhnya, atur `MAX_THINKING_TOKENS=0` di profil shell Anda. Di Opus, `MAX_THINKING_TOKENS` diabaikan kecuali untuk `0` karena penalaran adaptif mengontrol kedalaman pemikiran sebagai gantinya.

### Sesi jarak jauh

Sesi jarak jauh terus berlanjut di latar belakang bahkan jika Anda menutup aplikasi. Penggunaan dihitung terhadap [batas rencana langganan](/id/costs) Anda tanpa biaya komputasi terpisah.

Anda dapat membuat lingkungan cloud khusus dengan tingkat akses jaringan dan variabel lingkungan yang berbeda. Pilih dropdown lingkungan saat memulai sesi jarak jauh dan pilih **Tambah lingkungan**. Lihat [lingkungan cloud](/id/claude-code-on-the-web#cloud-environment) untuk detail tentang mengonfigurasi akses jaringan dan variabel lingkungan.

### Sesi SSH

Sesi SSH memungkinkan Anda menjalankan Claude Code di mesin jarak jauh sambil menggunakan aplikasi desktop sebagai antarmuka Anda. Ini berguna untuk bekerja dengan basis kode yang tinggal di cloud VM, dev containers, atau server dengan perangkat keras atau dependensi tertentu.

Untuk menambahkan koneksi SSH, klik dropdown lingkungan sebelum memulai sesi dan pilih **+ Tambah koneksi SSH**. Dialog menanyakan:

* **Nama**: label ramah untuk koneksi ini
* **SSH Host**: `user@hostname` atau host yang ditentukan di `~/.ssh/config`
* **SSH Port**: default ke 22 jika dibiarkan kosong, atau menggunakan port dari konfigurasi SSH Anda
* **Identity File**: path ke kunci pribadi Anda, seperti `~/.ssh/id_rsa`. Biarkan kosong untuk menggunakan kunci default atau konfigurasi SSH Anda.

Setelah ditambahkan, koneksi muncul di dropdown lingkungan. Pilih untuk memulai sesi di mesin itu. Claude berjalan di mesin jarak jauh dengan akses ke file dan alatnya.

Claude Code harus diinstal di mesin jarak jauh. Setelah terhubung, sesi SSH mendukung mode izin, konektor, plugins, dan MCP servers.

## Konfigurasi enterprise

Organisasi pada rencana Teams atau Enterprise dapat mengelola perilaku aplikasi desktop melalui kontrol konsol admin, file pengaturan yang dikelola, dan kebijakan manajemen perangkat.

### Kontrol konsol admin

Pengaturan ini dikonfigurasi melalui [konsol pengaturan admin](https://claude.ai/admin-settings/claude-code):

* **Aktifkan atau nonaktifkan tab Code**: kontrol apakah pengguna di organisasi Anda dapat mengakses Claude Code di aplikasi desktop
* **Nonaktifkan mode Lewati izin**: cegah pengguna di organisasi Anda dari mengaktifkan mode lewati izin
* **Nonaktifkan Claude Code di web**: aktifkan atau nonaktifkan sesi jarak jauh untuk organisasi Anda

### Pengaturan yang dikelola

Pengaturan yang dikelola menimpa pengaturan proyek dan pengguna dan berlaku ketika Desktop menjalankan sesi CLI. Anda dapat mengatur kunci ini di file [pengaturan yang dikelola](/id/settings#settings-precedence) organisasi Anda atau mendorongnya dari jarak jauh melalui konsol admin.

| Kunci                          | Deskripsi                                                                                                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode` | atur ke `"disable"` untuk mencegah pengguna dari mengaktifkan mode lewati izin. Lihat [pengaturan yang dikelola](/id/permissions#managed-only-settings). |

Untuk daftar lengkap pengaturan khusus yang dikelola termasuk `allowManagedPermissionRulesOnly` dan `allowManagedHooksOnly`, lihat [pengaturan khusus yang dikelola](/id/permissions#managed-only-settings).

Pengaturan yang dikelola jarak jauh yang diunggah melalui konsol admin saat ini berlaku untuk sesi CLI dan IDE saja. Untuk pembatasan khusus Desktop, gunakan kontrol konsol admin di atas.

### Kebijakan manajemen perangkat

Tim IT dapat mengelola aplikasi desktop melalui MDM di macOS atau kebijakan grup di Windows. Kebijakan yang tersedia termasuk mengaktifkan atau menonaktifkan fitur Claude Code, mengontrol pembaruan otomatis, dan menetapkan URL penyebaran khusus.

* **macOS**: konfigurasikan melalui domain preferensi `com.anthropic.Claude` menggunakan alat seperti Jamf atau Kandji
* **Windows**: konfigurasikan melalui registri di `SOFTWARE\Policies\Claude`

### Autentikasi dan SSO

Organisasi enterprise dapat memerlukan SSO untuk semua pengguna. Lihat [autentikasi](/id/authentication) untuk detail tingkat rencana dan [Menyiapkan SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) untuk konfigurasi SAML dan OIDC.

### Penanganan data

Claude Code memproses kode Anda secara lokal di sesi lokal atau di infrastruktur cloud Anthropic di sesi jarak jauh. Percakapan dan konteks kode dikirim ke API Anthropic untuk diproses. Lihat [penanganan data](/id/data-usage) untuk detail tentang retensi data, privasi, dan kepatuhan.

### Penyebaran

Desktop dapat didistribusikan melalui alat penyebaran enterprise:

* **macOS**: distribusikan melalui MDM seperti Jamf atau Kandji menggunakan installer `.dmg`
* **Windows**: sebarkan melalui paket MSIX atau installer `.exe`. Lihat [Sebarkan Claude Desktop untuk Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) untuk opsi penyebaran enterprise termasuk instalasi senyap

Untuk konfigurasi jaringan seperti pengaturan proxy, allowlisting firewall, dan gateway LLM, lihat [konfigurasi jaringan](/id/network-config).

Untuk referensi konfigurasi enterprise lengkap, lihat [panduan konfigurasi enterprise](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Datang dari CLI?

Jika Anda sudah menggunakan CLI Claude Code, Desktop menjalankan mesin yang sama dengan antarmuka grafis. Anda dapat menjalankan keduanya secara bersamaan di mesin yang sama, bahkan di proyek yang sama. Masing-masing mempertahankan riwayat sesi terpisah, tetapi mereka berbagi konfigurasi dan memori proyek melalui file CLAUDE.md.

Untuk memindahkan sesi CLI ke Desktop, jalankan `/desktop` di terminal. Claude menyimpan sesi Anda dan membukanya di aplikasi desktop, kemudian keluar dari CLI. Perintah ini hanya tersedia di macOS dan Windows.

<Tip>
  Kapan menggunakan Desktop vs CLI: gunakan Desktop ketika Anda menginginkan tinjauan diff visual, lampiran file, atau manajemen sesi di sidebar. Gunakan CLI ketika Anda memerlukan scripting, otomasi, penyedia pihak ketiga, atau lebih suka alur kerja terminal.
</Tip>

### Setara flag CLI

Tabel ini menunjukkan setara aplikasi desktop untuk flag CLI umum. Flag yang tidak tercantum tidak memiliki setara desktop karena dirancang untuk scripting atau otomasi.

| CLI                                   | Setara desktop                                                                                                                            |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                      | dropdown model di sebelah tombol kirim, sebelum memulai sesi                                                                              |
| `--resume`, `--continue`              | klik sesi di sidebar                                                                                                                      |
| `--permission-mode`                   | pemilih mode di sebelah tombol kirim                                                                                                      |
| `--dangerously-skip-permissions`      | Mode Lewati izin. Aktifkan di Pengaturan → Claude Code → "Izinkan mode lewati izin". Admin enterprise dapat menonaktifkan pengaturan ini. |
| `--add-dir`                           | tambahkan beberapa repo dengan tombol **+** di sesi jarak jauh                                                                            |
| `--allowedTools`, `--disallowedTools` | tidak tersedia di Desktop                                                                                                                 |
| `--verbose`                           | tidak tersedia. Periksa log sistem: Console.app di macOS, Event Viewer → Windows Logs → Application di Windows                            |
| `--print`, `--output-format`          | tidak tersedia. Desktop hanya interaktif.                                                                                                 |
| `ANTHROPIC_MODEL` env var             | dropdown model di sebelah tombol kirim                                                                                                    |
| `MAX_THINKING_TOKENS` env var         | atur di profil shell; berlaku untuk sesi lokal. Lihat [konfigurasi lingkungan](#environment-configuration).                               |

### Konfigurasi bersama

Desktop dan CLI membaca file konfigurasi yang sama, jadi setup Anda terbawa:

* File **[CLAUDE.md](/id/memory)** di proyek Anda digunakan oleh keduanya
* **[MCP servers](/id/mcp)** yang dikonfigurasi di `~/.claude.json` atau `.mcp.json` bekerja di keduanya
* **[Hooks](/id/hooks)** dan **[skills](/id/skills)** yang ditentukan dalam pengaturan berlaku untuk keduanya
* **[Pengaturan](/id/settings)** di `~/.claude.json` dan `~/.claude/settings.json` dibagikan. Aturan izin, alat yang diizinkan, dan pengaturan lainnya di `settings.json` berlaku untuk sesi Desktop.
* **Model**: Sonnet, Opus, dan Haiku tersedia di keduanya. Di Desktop, pilih model dari dropdown di sebelah tombol kirim sebelum memulai sesi. Anda tidak dapat mengubah model selama sesi aktif.

<Note>
  **MCP servers: aplikasi chat desktop vs Claude Code**: MCP servers yang dikonfigurasi untuk aplikasi chat Claude Desktop di `claude_desktop_config.json` terpisah dari Claude Code dan tidak akan muncul di tab Code. Untuk menggunakan MCP servers di Claude Code, konfigurasikan di `~/.claude.json` atau file `.mcp.json` proyek Anda. Lihat [konfigurasi MCP](/id/mcp#installing-mcp-servers) untuk detail.
</Note>

### Perbandingan fitur

Tabel ini membandingkan kemampuan inti antara CLI dan Desktop. Untuk daftar lengkap flag CLI, lihat [referensi CLI](/id/cli-reference).

| Fitur                                                 | CLI                                                       | Desktop                                                                             |
| ----------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Mode izin                                             | semua mode termasuk `dontAsk`                             | Minta izin, Terima edit otomatis, Mode Rencana, dan Lewati izin melalui Pengaturan  |
| `--dangerously-skip-permissions`                      | Flag CLI                                                  | Mode Lewati izin. Aktifkan di Pengaturan → Claude Code → "Izinkan mode lewati izin" |
| [Penyedia pihak ketiga](/id/third-party-integrations) | Bedrock, Vertex, Foundry                                  | tidak tersedia. Desktop terhubung langsung ke API Anthropic.                        |
| [MCP servers](/id/mcp)                                | konfigurasikan di file pengaturan                         | UI Konektor untuk sesi lokal dan SSH, atau file pengaturan                          |
| [Plugins](/id/plugins)                                | perintah `/plugin`                                        | UI pengelola plugin                                                                 |
| File @mention                                         | berbasis teks                                             | dengan autocomplete                                                                 |
| Lampiran file                                         | tidak tersedia                                            | gambar, PDF                                                                         |
| Isolasi sesi                                          | flag [`--worktree`](/id/cli-reference)                    | worktrees otomatis                                                                  |
| Beberapa sesi                                         | terminal terpisah                                         | tab sidebar                                                                         |
| Tugas berulang                                        | cron jobs, pipeline CI                                    | [tugas terjadwal](#schedule-recurring-tasks)                                        |
| Scripting dan otomasi                                 | [`--print`](/id/cli-reference), [Agent SDK](/id/headless) | tidak tersedia                                                                      |

### Apa yang tidak tersedia di Desktop

Fitur berikut hanya tersedia di CLI atau ekstensi VS Code:

* **Penyedia pihak ketiga**: Desktop terhubung langsung ke API Anthropic. Gunakan [CLI](/id/quickstart) dengan Bedrock, Vertex, atau Foundry sebagai gantinya.
* **Linux**: aplikasi desktop hanya tersedia di macOS dan Windows.
* **Saran kode inline**: Desktop tidak menyediakan saran gaya autocomplete. Ini bekerja melalui prompt percakapan dan perubahan kode eksplisit.
* **Tim agent**: orkestrasi multi-agent tersedia melalui [CLI](/id/agent-teams) dan [Agent SDK](/id/headless), bukan di Desktop.

## Pemecahan masalah

### Periksa versi Anda

Untuk melihat versi aplikasi desktop yang Anda jalankan:

* **macOS**: klik **Claude** di menu bar, kemudian **Tentang Claude**
* **Windows**: klik **Bantuan**, kemudian **Tentang**

Klik nomor versi untuk menyalinnya ke clipboard Anda.

### Kesalahan 403 atau autentikasi di tab Code

Jika Anda melihat `Error 403: Forbidden` atau kegagalan autentikasi lainnya saat menggunakan tab Code:

1. Keluar dan masuk kembali dari menu aplikasi. Ini adalah perbaikan paling umum.
2. Verifikasi Anda memiliki langganan berbayar aktif: Pro, Max, Teams, atau Enterprise.
3. Jika CLI berfungsi tetapi Desktop tidak, keluar dari aplikasi desktop sepenuhnya, bukan hanya tutup jendela, kemudian buka kembali dan masuk.
4. Periksa koneksi internet dan pengaturan proxy Anda.

### Layar kosong atau macet saat peluncuran

Jika aplikasi terbuka tetapi menampilkan layar kosong atau tidak responsif:

1. Mulai ulang aplikasi.
2. Periksa pembaruan yang tertunda. Aplikasi secara otomatis memperbarui saat peluncuran.
3. Di Windows, periksa Event Viewer untuk log crash di bawah **Windows Logs → Application**.

### "Gagal memuat sesi"

Jika Anda melihat `Failed to load session`, folder yang dipilih mungkin tidak lagi ada, repositori Git mungkin memerlukan Git LFS yang tidak diinstal, atau izin file mungkin mencegah akses. Coba pilih folder berbeda atau mulai ulang aplikasi.

### Sesi tidak menemukan alat yang diinstal

Jika Claude tidak dapat menemukan alat seperti `npm`, `node`, atau perintah CLI lainnya, verifikasi alat bekerja di terminal biasa Anda, periksa bahwa profil shell Anda dengan benar menyiapkan PATH, dan mulai ulang aplikasi desktop untuk memuat ulang variabel lingkungan.

### Kesalahan Git dan Git LFS

Di Windows, Git diperlukan untuk tab Code memulai sesi lokal. Jika Anda melihat "Git diperlukan," instal [Git untuk Windows](https://git-scm.com/downloads/win) dan mulai ulang aplikasi.

Jika Anda melihat "Git LFS diperlukan oleh repositori ini tetapi tidak diinstal," instal Git LFS dari [git-lfs.com](https://git-lfs.com/), jalankan `git lfs install`, dan mulai ulang aplikasi.

### MCP servers tidak bekerja di Windows

Jika toggle MCP server tidak merespons atau server gagal terhubung di Windows, periksa bahwa server dikonfigurasi dengan benar di pengaturan Anda, mulai ulang aplikasi, verifikasi proses server berjalan di Task Manager, dan tinjau log server untuk kesalahan koneksi.

### Aplikasi tidak akan keluar

* **macOS**: tekan Cmd+Q. Jika aplikasi tidak merespons, gunakan Force Quit dengan Cmd+Option+Esc, pilih Claude, dan klik Force Quit.
* **Windows**: gunakan Task Manager dengan Ctrl+Shift+Esc untuk mengakhiri proses Claude.

### Masalah khusus Windows

* **PATH tidak diperbarui setelah instalasi**: buka jendela terminal baru. Pembaruan PATH hanya berlaku untuk sesi terminal baru.
* **Kesalahan instalasi bersamaan**: jika Anda melihat kesalahan tentang instalasi lain sedang berlangsung tetapi tidak ada, coba jalankan installer sebagai Administrator.
* **ARM64**: perangkat Windows ARM64 sepenuhnya didukung.

### Tab Cowork tidak tersedia di Mac Intel

Tab Cowork memerlukan Apple Silicon (M1 atau lebih baru) di macOS. Di Windows, Cowork tersedia di semua perangkat keras yang didukung. Tab Chat dan Code berfungsi normal di Mac Intel.

### "Cabang belum ada" saat membuka di CLI

Sesi jarak jauh dapat membuat cabang yang tidak ada di mesin lokal Anda. Klik nama cabang di toolbar sesi untuk menyalinnya, kemudian ambil secara lokal:

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Masih terjebak?

* Cari atau laporkan bug di [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Kunjungi [pusat dukungan Claude](https://support.claude.com/)

Saat melaporkan bug, sertakan versi aplikasi desktop Anda, sistem operasi Anda, pesan kesalahan yang tepat, dan log yang relevan. Di macOS, periksa Console.app. Di Windows, periksa Event Viewer → Windows Logs → Application.
