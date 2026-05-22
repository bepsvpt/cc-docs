> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi alat Bash sandboxed

> Pelajari bagaimana alat Bash sandboxed Claude Code menyediakan isolasi filesystem dan jaringan untuk eksekusi agen yang lebih aman dan mandiri.

Sandbox Bash memungkinkan Claude menjalankan sebagian besar perintah shell tanpa berhenti untuk meminta izin. Alih-alih menyetujui setiap perintah, Anda menentukan file dan domain jaringan mana yang dapat diakses perintah, dan sistem operasi memberlakukan batas itu untuk setiap perintah Bash dan proses anak-anaknya.

Halaman ini mencakup cara untuk:

* [Mengaktifkan sandbox](#get-started) dan memilih bagaimana perintah sandboxed disetujui
* [Mengonfigurasi](#configure-sandboxing) jalur dan domain jaringan mana yang dapat dijangkau perintah
* [Menggabungkan sandboxing dengan aturan izin dan mode izin](#how-sandboxing-relates-to-permissions-and-permission-modes)
* [Memberlakukan sandboxing di seluruh organisasi](#configure-the-sandbox-for-your-organization) dengan pengaturan terkelola

<Note>
  Untuk membandingkan pendekatan isolasi lain seperti dev containers, container khusus, dan mesin virtual, lihat [Sandbox environments](/id/sandbox-environments). Untuk mengurangi prompt izin untuk alat selain Bash, lihat [permission modes](/id/permission-modes).
</Note>

## Memulai

Sandbox dibangun ke dalam Claude Code dan berjalan di macOS, Linux, dan WSL2. Windows asli tidak didukung. Di Windows, jalankan Claude Code di dalam distribusi WSL2.

Di macOS, tidak ada yang perlu diinstal: sandboxing menggunakan kerangka Seatbelt bawaan. Di Linux dan WSL2, sandbox bergantung pada dua paket, yang dibahas dalam [Set up Linux and WSL2](#set-up-linux-and-wsl2). Bahkan jika Anda belum menginstalnya, Anda dapat memulai dengan `/sandbox`, karena panelnya menunjukkan apakah ada yang hilang.

<Steps>
  <Step title="Jalankan /sandbox">
    Mulai sesi Claude Code dan jalankan perintah `/sandbox`:

    ```text theme={null}
    /sandbox
    ```

    Ini membuka panel sandbox dengan tiga tab:

    * **Mode**: pilih bagaimana perintah sandboxed disetujui, dibahas dalam langkah berikutnya
    * **Overrides**: pilih apakah perintah yang gagal di bawah sandbox dapat kembali ke menjalankan unsandboxed. Ini adalah pengaturan [`allowUnsandboxedCommands`](/id/settings#sandbox-settings)
    * **Config**: lihat pengaturan sandbox yang diselesaikan

    Jika panel hanya menampilkan tab Dependencies, paket yang diperlukan hilang. Instal seperti yang dijelaskan dalam [Set up Linux and WSL2](#set-up-linux-and-wsl2), restart Claude Code, dan jalankan `/sandbox` lagi.
  </Step>

  <Step title="Pilih mode">
    Di tab Mode, pilih auto-allow atau regular permissions. Auto-allow menjalankan perintah sandboxed tanpa prompt, dan regular permissions menjaga prompt izin reguler bahkan ketika perintah sandboxed. Lihat [Sandbox modes](#sandbox-modes) untuk perintah mana yang masih prompt dalam mode auto-allow.
  </Step>

  <Step title="Jalankan perintah Bash">
    Minta Claude untuk menjalankan perintah, seperti build atau test suite. Secara default, perintah di dalam sandbox hanya dapat menulis ke direktori kerja. Pertama kali perintah memerlukan domain jaringan baru, Claude Code meminta persetujuan.

    Perintah yang tidak dapat berjalan sandboxed kembali ke alur izin reguler. Untuk memperluas atau mempersempit batas ini, lihat [Configure sandboxing](#configure-sandboxing).
  </Step>
</Steps>

Memilih mode dalam panel menulis ke pengaturan lokal proyek Anda di `.claude/settings.local.json`, yang berlaku untuk proyek saat ini dan tidak diperiksa ke git. Untuk mengaktifkan sandbox di semua proyek Anda, atur [`sandbox.enabled`](/id/settings#sandbox-settings) ke `true` dalam pengaturan pengguna Anda di `~/.claude/settings.json`. Untuk memberlakukan sandboxing untuk setiap pengembang dalam organisasi, gunakan [managed settings](#enforce-sandboxing-with-managed-settings).

<Warning>
  Secara default, jika sandbox tidak dapat dimulai karena dependensi hilang atau platform tidak didukung, Claude Code menampilkan peringatan dan menjalankan perintah tanpa sandboxing. Untuk menjadikan ini kegagalan keras sebagai gantinya, atur [`sandbox.failIfUnavailable`](/id/settings#sandbox-settings) ke `true`. Ini dimaksudkan untuk penyebaran terkelola yang memerlukan sandboxing sebagai gerbang keamanan.
</Warning>

### Set up Linux dan WSL2

Di Linux dan WSL2, sandbox bergantung pada dua paket:

* [`bubblewrap`](https://github.com/containers/bubblewrap): alat sandboxing tanpa privilege yang memberlakukan isolasi filesystem
* [`socat`](http://www.dest-unreach.org/socat/): relay yang digunakan untuk merutekan lalu lintas jaringan melalui proxy sandbox

Instal dengan manajer paket distribusi Anda:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

Setelah menginstal, tab Dependencies dalam `/sandbox` menunjukkan apakah `ripgrep`, `bubblewrap`, `socat`, dan filter seccomp tersedia di platform Anda. Ripgrep disertakan dengan binari Claude Code asli. Filter seccomp bersifat opsional dan menambahkan pemblokiran soket domain Unix. Instal dengan `npm install -g @anthropic-ai/sandbox-runtime` jika hilang.

Ketika dependensi yang diperlukan hilang, tab Dependencies adalah satu-satunya tab yang ditampilkan sampai Anda menginstalnya. Pemeriksaan dependensi berjalan saat startup, jadi restart Claude Code setelah menginstal paket untuk `/sandbox` mendeteksinya.

<AccordionGroup>
  <Accordion title="Ubuntu 24.04 dan yang lebih baru: izinkan bubblewrap untuk membuat user namespaces">
    Di Ubuntu 24.04 dan yang lebih baru, kebijakan AppArmor default mencegah bubblewrap dari membuat user namespaces yang dibutuhkannya untuk isolasi.

    Untuk memeriksa apakah lingkungan Anda memberlakukan pembatasan ini, termasuk di dalam WSL2, jalankan `sysctl kernel.apparmor_restrict_unprivileged_userns`. Jika kunci tidak ada atau mengembalikan `0`, lewati langkah ini. Jika mengembalikan `1`, tambahkan profil AppArmor yang memberikan `bwrap` kemampuan ini:

    ```bash theme={null}
    sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
    abi <abi/4.0>,
    include <tunables/global>

    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }
    EOF
    ```

    Profil hanya berlaku untuk `bwrap` itu sendiri, bukan untuk perintah yang berjalan di dalam sandbox. Muat ulang AppArmor untuk menerapkannya:

    ```bash theme={null}
    sudo systemctl reload apparmor
    ```
  </Accordion>

  <Accordion title="Catatan WSL2">
    Periksa versi WSL Anda dengan `wsl -l -v` dari PowerShell. Jika Anda melihat `Sandboxing requires WSL2`, distribusi Anda menjalankan WSL1. Tingkatkan ke WSL2 atau jalankan Claude Code tanpa sandboxing.

    Di WSL2, perintah sandboxed tidak dapat meluncurkan binari Windows seperti `cmd.exe`, `powershell.exe`, atau apa pun di bawah `/mnt/c/`. WSL menyerahkan ini ke host Windows melalui soket Unix, yang sandbox blokir. Jika perintah perlu memanggil binari Windows, tambahkan ke [`excludedCommands`](/id/settings#sandbox-settings) sehingga berjalan di luar sandbox.
  </Accordion>
</AccordionGroup>

### Mode sandbox

Claude Code menawarkan dua mode sandbox:

**Mode auto-allow**: Perintah Bash akan mencoba berjalan di dalam sandbox dan secara otomatis diizinkan tanpa memerlukan izin. Perintah yang tidak dapat di-sandbox, seperti yang memerlukan akses jaringan ke host yang tidak diizinkan, kembali ke alur izin reguler, di mana Claude Code memeriksa [permission rules](/id/permissions) Anda dan meminta Anda untuk perintah apa pun yang tidak diizinkan oleh aturan tersebut.

Bahkan dalam mode auto-allow, hal berikut masih berlaku:

* [Deny rules](/id/permissions) eksplisit selalu dihormati
* Perintah `rm` atau `rmdir` yang menargetkan `/`, direktori home Anda, atau jalur sistem kritis lainnya masih memicu prompt izin
* [Ask rules](/id/permissions) berlaku untuk perintah yang kembali ke alur izin reguler

**Mode regular permissions**: Semua perintah Bash melalui alur izin reguler, bahkan ketika sandboxed. Ini memberikan lebih banyak kontrol tetapi memerlukan lebih banyak persetujuan.

Di kedua mode, sandbox memberlakukan pembatasan filesystem dan jaringan yang sama. Perbedaannya hanya dalam apakah perintah sandboxed disetujui secara otomatis atau memerlukan izin eksplisit.

Beberapa perintah tidak dapat berjalan di dalam sandbox sama sekali, seperti alat yang tidak kompatibel dengannya atau yang memerlukan host yang belum Anda izinkan. Daripada gagal tugas atau memerlukan Anda untuk mematikan sandboxing, Claude Code menyertakan pintu keluar: ketika perintah gagal karena pembatasan sandbox, Claude menganalisis kegagalan dan dapat mencoba kembali perintah dengan parameter `dangerouslyDisableSandbox`. Perintah yang dicoba kembali berjalan di luar sandbox, sehingga melalui alur izin reguler dan memerlukan persetujuan Anda.

Anda dapat menonaktifkan pintu keluar ini dengan mengatur `"allowUnsandboxedCommands": false` dalam [sandbox settings](/id/settings#sandbox-settings) Anda. Ketika dinonaktifkan, yang ditampilkan tab Overrides `/sandbox` sebagai **Strict sandbox mode**, parameter `dangerouslyDisableSandbox` sepenuhnya diabaikan dan semua perintah harus berjalan sandboxed atau secara eksplisit terdaftar dalam `excludedCommands`.

<Info>
  Mode auto-allow bekerja secara independen dari pengaturan mode izin Anda. Bahkan jika Anda tidak dalam mode "accept edits", perintah Bash sandboxed akan berjalan secara otomatis ketika auto-allow diaktifkan. Ini berarti perintah Bash yang memodifikasi file dalam batas sandbox akan dieksekusi tanpa prompt, bahkan ketika alat edit file biasanya memerlukan persetujuan.
</Info>

## Konfigurasi sandboxing

Sesuaikan perilaku sandbox melalui file `settings.json` Anda. Lihat [Settings](/id/settings#sandbox-settings) untuk referensi konfigurasi lengkap.

Secara default, perintah sandboxed hanya dapat menulis ke direktori kerja saat ini. Jika perintah subprocess seperti `kubectl`, `terraform`, atau `npm` perlu menulis di luar direktori proyek, gunakan `sandbox.filesystem.allowWrite` untuk memberikan akses ke jalur tertentu:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

Jalur ini diberlakukan pada tingkat OS, sehingga semua perintah yang berjalan di dalam sandbox, termasuk proses anak mereka, menghormatinya. Ini adalah pendekatan yang direkomendasikan ketika alat memerlukan akses tulis ke lokasi tertentu, daripada mengecualikan alat dari sandbox sepenuhnya dengan `excludedCommands`.

Ketika array filesystem yang sama didefinisikan dalam beberapa [settings scopes](/id/settings#settings-precedence), array digabungkan: jalur dari setiap scope dikombinasikan, bukan diganti.

Awalan jalur mengontrol bagaimana jalur diselesaikan:

| Awalan                 | Arti                                                                                                | Contoh                                                                           |
| :--------------------- | :-------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `/`                    | Jalur absolut dari akar filesystem                                                                  | `/tmp/build` tetap `/tmp/build`                                                  |
| `~/`                   | Relatif terhadap direktori home                                                                     | `~/.kube` menjadi `$HOME/.kube`                                                  |
| `./` atau tanpa awalan | Relatif terhadap akar proyek untuk pengaturan proyek, atau ke `~/.claude` untuk pengaturan pengguna | `./output` dalam `.claude/settings.json` diselesaikan ke `<project-root>/output` |

Sintaks ini berbeda dari [Read and Edit permission rules](/id/permissions#read-and-edit), yang menggunakan `//path` untuk absolut dan `/path` untuk relatif proyek. Jalur filesystem sandbox menggunakan konvensi standar: `/tmp/build` adalah absolut.

Anda juga dapat menolak akses tulis atau baca menggunakan `sandbox.filesystem.denyWrite` dan `sandbox.filesystem.denyRead`, dan mengizinkan kembali jalur tertentu dalam wilayah yang ditolak menggunakan `sandbox.filesystem.allowRead`.

Contoh di bawah memblokir pembacaan dari seluruh direktori home sambil tetap memungkinkan pembacaan dari proyek saat ini. Tempatkan di `.claude/settings.json` proyek Anda, karena jalur relatif `.` diselesaikan ke akar proyek hanya ketika konfigurasi berada dalam pengaturan proyek:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

`.` dalam `allowRead` diselesaikan ke akar proyek karena konfigurasi ini berada dalam pengaturan proyek. Jika Anda menempatkan konfigurasi yang sama dalam `~/.claude/settings.json`, `.` akan diselesaikan ke `~/.claude` sebagai gantinya, dan file proyek akan tetap diblokir oleh aturan `denyRead`.

## Cara sandboxing bekerja

### Isolasi filesystem

Alat Bash sandboxed membatasi akses sistem file ke direktori tertentu:

* **Perilaku penulisan default**: akses baca dan tulis ke direktori kerja saat ini dan subdirektorinya
* **Perilaku pembacaan default**: akses baca ke seluruh komputer, kecuali direktori tertentu yang ditolak. Perhatikan bahwa default ini masih memungkinkan pembacaan file kredensial seperti `~/.aws/credentials` dan `~/.ssh/`. Tambahkan ke `denyRead` untuk memblokirnya.
* **Akses terblokir**: tidak dapat memodifikasi file di luar direktori kerja saat ini tanpa izin eksplisit, termasuk file konfigurasi shell seperti `~/.bashrc` dan binari sistem di `/bin/`
* **Dapat dikonfigurasi**: tentukan jalur yang diizinkan dan ditolak khusus melalui pengaturan

Anda dapat memberikan akses tulis ke jalur tambahan menggunakan `sandbox.filesystem.allowWrite` dalam pengaturan Anda. Pembatasan ini diberlakukan pada tingkat OS, sehingga berlaku untuk semua perintah subprocess, termasuk alat seperti `kubectl`, `terraform`, dan `npm`, bukan hanya alat file Claude.

### Isolasi jaringan

Akses jaringan dikendalikan melalui server proxy yang berjalan di luar sandbox:

* **Pembatasan domain**: tidak ada domain yang diizinkan sebelumnya. Pertama kali perintah memerlukan domain baru, Claude Code meminta persetujuan. Izinkan domain sebelumnya dengan [`allowedDomains`](/id/settings#sandbox-settings) untuk menghindari prompt.
* **Lockdown terkelola**: jika [`allowManagedDomainsOnly`](/id/settings#sandbox-settings) diatur dalam pengaturan terkelola, domain yang tidak diizinkan diblokir secara otomatis alih-alih prompt, dan hanya `allowedDomains` dari pengaturan terkelola yang dihormati.
* **Dukungan proxy khusus**: pengguna tingkat lanjut dapat menerapkan aturan khusus pada lalu lintas keluar
* **Cakupan komprehensif**: pembatasan berlaku untuk semua skrip, program, dan subprocess yang dihasilkan oleh perintah

<Note>
  Proxy bawaan memberlakukan allowlist berdasarkan hostname yang diminta dan tidak menghentikan atau memeriksa lalu lintas TLS. Lihat [Security limitations](#security-limitations) untuk implikasi desain ini, dan [Custom proxy configuration](#custom-proxy-configuration) jika model ancaman Anda memerlukan inspeksi TLS.
</Note>

### Penegakan tingkat OS

Alat Bash sandboxed memanfaatkan primitif keamanan sistem operasi:

* **macOS**: menggunakan Seatbelt untuk penegakan sandbox
* **Linux**: menggunakan [bubblewrap](https://github.com/containers/bubblewrap) untuk isolasi
* **WSL2**: menggunakan bubblewrap, sama seperti Linux

WSL1 tidak didukung karena bubblewrap memerlukan fitur kernel yang hanya tersedia di WSL2. Pembatasan tingkat OS ini memastikan bahwa semua proses anak yang dihasilkan oleh perintah Claude Code mewarisi batas keamanan yang sama.

Primitif yang sama tersedia sebagai paket [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropic-experimental/sandbox-runtime) mandiri, yang halaman [Sandbox environments](/id/sandbox-environments#sandbox-runtime) mencakup sebagai pendekatan terpisah untuk membungkus seluruh proses Claude Code.

## Bagaimana sandboxing berhubungan dengan izin dan mode izin

Sandboxing, [permission rules](/id/permissions), dan [permission modes](/id/permission-modes) adalah lapisan komplementer. Bagian di bawah mencakup bagaimana sandbox berinteraksi dengan masing-masing.

### Aturan izin

Aturan izin dan sandboxing mengontrol hal yang berbeda:

* **Aturan izin** mengontrol alat mana yang dapat digunakan Claude Code dan dievaluasi sebelum alat apa pun berjalan. Mereka berlaku untuk semua alat: Bash, Read, Edit, WebFetch, MCP, dan lainnya.
* **Sandboxing** menyediakan penegakan tingkat OS yang membatasi apa yang dapat diakses perintah Bash pada tingkat filesystem dan jaringan. Ini hanya berlaku untuk perintah Bash dan proses anak mereka.

Kedua lapisan juga berbeda dalam cara penegakan mereka. Claude Code mengevaluasi keputusan izin sebelum perintah berjalan, berdasarkan string perintah dan, dalam mode auto, penilaian classifier terpisah tentang apakah perintah aman. Sistem operasi memberlakukan batas sandbox pada proses yang berjalan, sehingga berlaku terlepas dari apa yang dipilih model untuk dijalankan dan bahkan jika perintah yang diizinkan melakukan lebih dari nama yang disarankan.

Pembatasan filesystem dan jaringan dikonfigurasi melalui pengaturan sandbox dan aturan izin:

| Pengaturan atau aturan                                           | Apa yang dilakukannya                                                                                            |
| :--------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| `sandbox.filesystem.allowWrite`                                  | Memberikan akses tulis subprocess ke jalur di luar direktori kerja                                               |
| `sandbox.filesystem.denyWrite` dan `sandbox.filesystem.denyRead` | Memblokir akses subprocess ke jalur tertentu                                                                     |
| `sandbox.filesystem.allowRead`                                   | Mengizinkan kembali pembacaan jalur tertentu dalam wilayah `denyRead`                                            |
| Aturan izin `Edit`                                               | Memberikan akses tulis ke jalur tertentu, dengan cara yang sama seperti `sandbox.filesystem.allowWrite`          |
| Aturan tolak `Read` dan `Edit`                                   | Memblokir akses ke file atau direktori tertentu                                                                  |
| Aturan izin dan tolak `WebFetch`                                 | Mengontrol akses domain                                                                                          |
| Sandbox `allowedDomains`                                         | Mengontrol domain mana yang dapat dijangkau perintah Bash                                                        |
| Sandbox `deniedDomains`                                          | Memblokir domain tertentu bahkan ketika wildcard `allowedDomains` yang lebih luas akan sebaliknya mengizinkannya |

Jalur dari pengaturan `sandbox.filesystem` dan aturan izin digabungkan bersama ke dalam konfigurasi sandbox akhir.

[Direktori contoh repositori claude-code](https://github.com/anthropics/claude-code/tree/main/examples/settings) mencakup konfigurasi pengaturan pemula untuk skenario penyebaran umum, termasuk contoh khusus sandbox. Gunakan ini sebagai titik awal dan sesuaikan dengan kebutuhan Anda.

### Mode izin

`/sandbox` bukan [permission mode](/id/permission-modes). Mode izin memutuskan apakah panggilan alat berjalan dan apakah Anda diminta terlebih dahulu, sementara sandbox membatasi apa yang dapat diakses perintah Bash setelah berjalan. Mereka berbeda dalam apa yang mereka kontrol dan apa yang menggantikan prompt per-aksi:

|                                                                    | Apa yang dikontrol                                    | Apa yang menggantikan prompt                                                                                                                           |
| :----------------------------------------------------------------- | :---------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/sandbox`                                                         | Apa yang dapat diakses perintah Bash setelah berjalan | Batas sandbox itu sendiri, dalam [mode auto-allow](#sandbox-modes)                                                                                     |
| [Auto mode](/id/permission-modes#eliminate-prompts-with-auto-mode) | Apakah setiap panggilan alat berjalan                 | Classifier yang meninjau tindakan                                                                                                                      |
| `--dangerously-skip-permissions`                                   | Apakah setiap panggilan alat berjalan                 | Tidak ada. Pemeriksaan [Protected path](/id/permission-modes#protected-paths) juga dilewati; hanya menghapus `/` atau direktori home Anda masih prompt |

Mode [auto-allow](#sandbox-modes) sandbox terpisah dari [auto mode](/id/permission-modes#eliminate-prompts-with-auto-mode): auto-allow menyetujui perintah Bash karena batas sandbox memuatnya, sementara auto mode menggunakan classifier untuk meninjau tindakan. Keduanya bekerja secara independen dan dapat dikombinasikan. Untuk memilih batas isolasi untuk run tanpa pengawasan, lihat [Sandbox environments](/id/sandbox-environments#how-isolation-relates-to-permission-modes).

## Konfigurasi sandbox untuk organisasi Anda

Administrator dapat memerlukan sandboxing untuk setiap pengguna, mencegah pengembang memperluas kebijakan, dan merutekan lalu lintas sandbox melalui proxy perusahaan.

### Memberlakukan sandboxing dengan pengaturan terkelola

Untuk memerlukan sandbox untuk setiap pengembang, berikan kunci `sandbox` melalui [managed settings](/id/settings#settings-files), baik sebagai file yang dikelola oleh MDM Anda atau melalui [server-managed settings](/id/server-managed-settings) di Claude.ai.

Konfigurasi pengaturan terkelola berikut mengaktifkan sandbox, menolak untuk memulai Claude Code jika sandbox tidak dapat diinisialisasi, dan mencegah model dari mencoba kembali perintah di luar sandbox:

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

Dua kunci di luar `enabled` mengontrol apa yang terjadi ketika sandbox tidak dapat menjalankan perintah:

* **`failIfUnavailable`**: dependensi yang hilang seperti bubblewrap di Linux memblokir Claude Code dari memulai daripada menampilkan peringatan dan kembali ke eksekusi unsandboxed
* **`allowUnsandboxedCommands: false`**: pintu keluar `dangerouslyDisableSandbox` diabaikan, sehingga perintah yang gagal di bawah sandbox tidak dapat dicoba kembali di luar itu

Dua penambahan layak dipertimbangkan bersama mereka. Tambahkan `excludedCommands` untuk alat yang disetujui organisasi apa pun yang harus berjalan tanpa isolasi. Tambahkan entri [`denyRead`](#filesystem-isolation) untuk direktori kredensial seperti `~/.aws` dan `~/.ssh`, yang kebijakan pembacaan default masih memungkinkan.

Sandbox tidak berjalan di Windows asli, jadi jika armada Anda mencakup host Windows, batasi konfigurasi ini ke macOS dan Linux atau minta pengguna tersebut menjalankan Claude Code di dalam WSL2 atau container.

### Cegah pengembang memperluas kebijakan

Untuk kunci boolean seperti `enabled` dan `failIfUnavailable`, Claude Code menggunakan nilai terkelola dan mengabaikan apa pun yang ditetapkan pengembang secara lokal. Untuk kunci array seperti `excludedCommands` dan `allowRead`, Claude Code menggabungkan entri dari setiap scope, sehingga pengembang dapat menambahkan entri yang memperluas kebijakan.

Atur `allowManagedReadPathsOnly` ke `true` dalam pengaturan terkelola sehingga hanya entri `allowRead` dari pengaturan terkelola yang dihormati. Entri `allowRead` pengguna, proyek, dan lokal diabaikan. Ini mencegah pengembang memperluas akses baca di luar jalur yang disetujui organisasi. Untuk mengunci domain jaringan ke nilai terkelola dengan cara yang sama, atur [`allowManagedDomainsOnly`](/id/settings#sandbox-settings).

`excludedCommands` tidak memiliki lockdown hanya terkelola yang setara, sehingga pengembang selalu dapat menambahkan entri yang menjalankan perintah tambahan di luar sandbox. Jaga daftar terkelola tetap sempit.

### Konfigurasi proxy khusus

Untuk organisasi yang memerlukan keamanan jaringan lanjutan, Anda dapat menerapkan proxy khusus untuk:

* Mendekripsi dan memeriksa lalu lintas HTTPS
* Menerapkan aturan penyaringan khusus
* Mencatat semua permintaan jaringan
* Mengintegrasikan dengan infrastruktur keamanan yang ada

Untuk menunjukkan Claude Code ke proxy Anda, atur port proxy dalam [sandbox settings](/id/settings#sandbox-settings):

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

## Pemecahan masalah

Beberapa perintah gagal di dalam sandbox meskipun bekerja di luar itu. Perbaikan di bawah mencakup kasus paling umum.

* **Perintah gagal dengan kesalahan host-not-allowed**: banyak alat CLI perlu menjangkau host tertentu. Memberikan izin saat diminta menambahkan host ke daftar yang diizinkan sehingga alat berjalan di dalam sandbox di masa depan.
* **`jest` hang atau gagal**: `watchman` tidak kompatibel dengan sandbox. Jalankan `jest --no-watchman` sebagai gantinya.
* **Go-based CLIs gagal verifikasi TLS di macOS**: alat seperti `gh`, `gcloud`, dan `terraform` mungkin gagal verifikasi TLS di bawah Seatbelt. Daftar alat ini dalam `excludedCommands` untuk menjalankannya di luar sandbox. Jika Anda menggunakan `httpProxyPort` dengan proxy MITM dan CA khusus, atur [`enableWeakerNetworkIsolation`](/id/settings#sandbox-settings) ke `true` sebagai gantinya.
* **Perintah `docker` gagal**: `docker` tidak kompatibel dengan sandbox. Tambahkan `docker *` ke `excludedCommands` untuk menjalankannya di luar sandbox.
* **Bubblewrap gagal memulai di dalam container**: dalam container tanpa privilege, bubblewrap tidak dapat memasang filesystem `/proc` segar. Atur [`enableWeakerNestedSandbox`](/id/settings#sandbox-settings) ke `true` sehingga sandbox dalam bind-mount `/proc` yang ada dari container sebagai gantinya. Hanya gunakan pengaturan ini ketika container luar sudah menyediakan batas isolasi yang Anda butuhkan, karena mengekspos informasi proses ke perintah sandboxed yang mount `/proc` segar akan menyembunyikan.
* **Filter seccomp di Linux**: filter seccomp diperlukan untuk memblokir soket domain Unix. Tab Dependencies dalam `/sandbox` menunjukkan apakah tersedia. Jika hilang, jalankan `npm install -g @anthropic-ai/sandbox-runtime` untuk menginstal helper.
* **`--dangerously-skip-permissions` gagal sebagai root**: flag ini diblokir saat menjalankan sebagai root atau melalui sudo di Linux dan macOS, karena akses root dikombinasikan dengan tidak ada prompt izin dapat memodifikasi file atau layanan apa pun di sistem. Pemeriksaan dilewati secara otomatis di dalam sandbox yang dikenali. Untuk menjalankan secara otonom dalam container, gunakan konfigurasi [dev container](/id/devcontainer), yang menjalankan Claude Code sebagai pengguna non-root.

## Keterbatasan

Sandboxing mengurangi risiko tetapi bukan batas isolasi lengkap. Tinjau keterbatasan di bawah sebelum mengandalkannya sebagai kontrol keamanan keras.

### Keterbatasan keamanan

* **Penyaringan jaringan**: sistem penyaringan jaringan beroperasi dengan membatasi domain yang diizinkan untuk terhubung oleh proses. Proxy bawaan tidak menghentikan atau melakukan inspeksi TLS pada lalu lintas keluar, sehingga isi koneksi terenkripsi tidak diperiksa. Anda bertanggung jawab untuk memastikan bahwa hanya domain tepercaya yang diizinkan dalam kebijakan Anda.

<Warning>
  Mengizinkan domain luas seperti `github.com` dapat membuat jalur untuk eksfiltrasi data. Karena proxy membuat keputusan izin dari hostname yang disediakan klien tanpa memeriksa TLS, kode yang berjalan di dalam sandbox berpotensi dapat menggunakan [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) atau teknik serupa untuk menjangkau host di luar allowlist. Jika model ancaman Anda memerlukan jaminan yang lebih kuat, konfigurasikan [custom proxy](#custom-proxy-configuration) yang menghentikan TLS dan memeriksa lalu lintas, dan instal sertifikat CA-nya di dalam sandbox. Isolasi jaringan yang lebih kuat dan sadar TLS adalah area pengembangan aktif.
</Warning>

* **Eskalasi privilege melalui soket Unix**: konfigurasi `allowUnixSockets` dapat secara tidak sengaja memberikan akses ke layanan sistem yang kuat yang dapat menyebabkan bypass sandbox. Misalnya, mengizinkan akses ke `/var/run/docker.sock` secara efektif memberikan akses ke sistem host melalui soket Docker. Pertimbangkan dengan hati-hati soket Unix apa pun yang Anda izinkan melalui sandbox.
* **Eskalasi izin filesystem**: izin penulisan filesystem yang terlalu luas dapat memungkinkan serangan eskalasi privilege. Mengizinkan penulisan ke direktori yang berisi executable dalam `$PATH`, direktori konfigurasi sistem, atau file konfigurasi shell pengguna seperti `.bashrc` atau `.zshrc` dapat menyebabkan eksekusi kode dalam konteks keamanan yang berbeda ketika pengguna lain atau proses sistem mengakses file ini.
* **Kekuatan sandbox Linux**: implementasi Linux menyediakan isolasi filesystem dan jaringan yang kuat tetapi mencakup mode `enableWeakerNestedSandbox` yang memungkinkannya bekerja di dalam lingkungan Docker tanpa namespace istimewa, atau pada host Linux di mana user namespaces tanpa privilege dinonaktifkan oleh sysctl. Opsi ini secara konsiderabel melemahkan keamanan dan hanya boleh digunakan ketika isolasi tambahan sebaliknya diberlakukan.
* **File pengaturan dilindungi**: sandbox secara otomatis menolak akses tulis ke file `settings.json` Claude Code di setiap scope dan ke direktori pengaturan terkelola, sehingga perintah sandboxed tidak dapat memodifikasi kebijakan sendiri.

### Kompatibilitas platform dan alat

* **Dukungan platform**: mendukung macOS, Linux, dan WSL2. WSL1 dan Windows asli tidak didukung.
* **Overhead kinerja**: minimal, tetapi beberapa operasi filesystem mungkin sedikit lebih lambat.
* **Kompatibilitas alat**: beberapa alat yang memerlukan pola akses sistem tertentu mungkin memerlukan penyesuaian konfigurasi, atau mungkin perlu dijalankan di luar sandbox.

### Cakupan

Sandbox mengisolasi subprocess Bash. Alat lain beroperasi di bawah batas yang berbeda:

* **Alat file bawaan**: Read, Edit, dan Write menggunakan sistem izin secara langsung daripada berjalan melalui sandbox. Lihat [permissions](/id/permissions).
* **Penggunaan komputer**: ketika Claude membuka aplikasi dan mengontrol layar Anda, itu berjalan di desktop aktual Anda daripada di lingkungan terisolasi. Prompt izin per-aplikasi membatasi setiap aplikasi. Lihat [computer use in the CLI](/id/computer-use) atau [computer use in Desktop](/id/desktop#let-claude-use-your-computer).
* **Variabel lingkungan**: perintah Bash sandboxed mewarisi lingkungan proses induk secara default, termasuk kredensial apa pun yang ditetapkan di sana. Untuk menghapus kredensial Anthropic dan penyedia cloud dari subprocess, atur [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/id/env-vars).
* **Subagents**: [subagents](/id/sub-agents) berjalan dalam proses yang sama dengan sesi induk dan menggunakan konfigurasi sandbox yang sama. Perintah Bash di dalam subagent di-sandbox ketika sandboxing diaktifkan dalam sesi induk.

<Warning>
  Sandboxing yang efektif memerlukan **baik** isolasi filesystem maupun jaringan. Tanpa isolasi jaringan, agen yang dikompromikan dapat mengeksfiltrasikan file sensitif seperti kunci SSH. Tanpa isolasi filesystem, agen yang dikompromikan dapat memasang pintu belakang pada sumber daya sistem untuk mendapatkan akses jaringan. Ketika Anda memperluas default, periksa bahwa jalur `allowWrite`, entri `allowedDomains` yang luas, atau pengecualian `excludedCommands` tidak membatalkan pembatasan di sisi lain.
</Warning>

## Lihat juga

* [Sandbox environments](/id/sandbox-environments): bandingkan sandbox bawaan dengan dev containers, containers, dan VM
* [Security](/id/security): fitur keamanan komprehensif dan praktik terbaik
* [Permissions](/id/permissions): konfigurasi izin dan kontrol akses
* [Settings](/id/settings): referensi konfigurasi lengkap
* [CLI reference](/id/cli-reference): opsi baris perintah
