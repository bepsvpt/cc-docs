> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sandboxing

> Pelajari bagaimana alat bash sandboxed Claude Code menyediakan isolasi filesystem dan jaringan untuk eksekusi agen yang lebih aman dan mandiri.

## Ikhtisar

Claude Code menampilkan sandboxing asli untuk menyediakan lingkungan yang lebih aman untuk eksekusi agen sambil mengurangi kebutuhan akan prompt izin yang konstan. Alih-alih meminta izin untuk setiap perintah bash, sandboxing menciptakan batas yang ditentukan di awal di mana Claude Code dapat bekerja lebih bebas dengan risiko yang berkurang.

Alat bash sandboxed menggunakan primitif tingkat OS untuk memberlakukan isolasi filesystem dan jaringan.

## Mengapa sandboxing penting

Keamanan berbasis izin tradisional memerlukan persetujuan pengguna yang konstan untuk perintah bash. Meskipun ini memberikan kontrol, hal ini dapat menyebabkan:

* **Kelelahan persetujuan**: Berulang kali mengklik "setujui" dapat menyebabkan pengguna kurang memperhatikan apa yang mereka setujui
* **Produktivitas berkurang**: Gangguan konstan memperlambat alur kerja pengembangan
* **Otonomi terbatas**: Claude Code tidak dapat bekerja seefisien mungkin saat menunggu persetujuan

Sandboxing mengatasi tantangan ini dengan:

1. **Mendefinisikan batas yang jelas**: Tentukan dengan tepat direktori dan host jaringan mana yang dapat diakses Claude Code
2. **Mengurangi prompt izin**: Perintah aman dalam sandbox tidak memerlukan persetujuan
3. **Mempertahankan keamanan**: Upaya untuk mengakses sumber daya di luar sandbox memicu notifikasi segera
4. **Memungkinkan otonomi**: Claude Code dapat berjalan lebih independen dalam batas yang ditentukan

<Warning>
  Sandboxing yang efektif memerlukan **baik** isolasi filesystem maupun jaringan. Tanpa isolasi jaringan, agen yang dikompromikan dapat mengeksfiltrasikan file sensitif seperti kunci SSH. Tanpa isolasi filesystem, agen yang dikompromikan dapat memasang pintu belakang pada sumber daya sistem untuk mendapatkan akses jaringan. Saat mengonfigurasi sandboxing, penting untuk memastikan bahwa pengaturan yang dikonfigurasi tidak menciptakan bypass dalam sistem ini.
</Warning>

## Cara kerjanya

### Isolasi filesystem

Alat bash sandboxed membatasi akses sistem file ke direktori tertentu:

* **Perilaku penulisan default**: Akses baca dan tulis ke direktori kerja saat ini dan subdirektorinya
* **Perilaku pembacaan default**: Akses baca ke seluruh komputer, kecuali direktori tertentu yang ditolak
* **Akses terblokir**: Tidak dapat memodifikasi file di luar direktori kerja saat ini tanpa izin eksplisit
* **Dapat dikonfigurasi**: Tentukan jalur yang diizinkan dan ditolak khusus melalui pengaturan

Anda dapat memberikan akses tulis ke jalur tambahan menggunakan `sandbox.filesystem.allowWrite` dalam pengaturan Anda. Pembatasan ini diberlakukan pada tingkat OS (Seatbelt di macOS, bubblewrap di Linux), sehingga berlaku untuk semua perintah subprocess, termasuk alat seperti `kubectl`, `terraform`, dan `npm`, bukan hanya alat file Claude.

### Isolasi jaringan

Akses jaringan dikendalikan melalui server proxy yang berjalan di luar sandbox:

* **Pembatasan domain**: Hanya domain yang disetujui yang dapat diakses
* **Konfirmasi pengguna**: Permintaan domain baru memicu prompt izin (kecuali [`allowManagedDomainsOnly`](/id/settings#sandbox-settings) diaktifkan, yang secara otomatis memblokir domain yang tidak diizinkan)
* **Dukungan proxy khusus**: Pengguna tingkat lanjut dapat menerapkan aturan khusus pada lalu lintas keluar
* **Cakupan komprehensif**: Pembatasan berlaku untuk semua skrip, program, dan subprocess yang dihasilkan oleh perintah

### Penegakan tingkat OS

Alat bash sandboxed memanfaatkan primitif keamanan sistem operasi:

* **macOS**: Menggunakan Seatbelt untuk penegakan sandbox
* **Linux**: Menggunakan [bubblewrap](https://github.com/containers/bubblewrap) untuk isolasi
* **WSL2**: Menggunakan bubblewrap, sama seperti Linux

WSL1 tidak didukung karena bubblewrap memerlukan fitur kernel yang hanya tersedia di WSL2.

Pembatasan tingkat OS ini memastikan bahwa semua proses anak yang dihasilkan oleh perintah Claude Code mewarisi batas keamanan yang sama.

## Memulai

### Prasyarat

Di **macOS**, sandboxing bekerja langsung menggunakan kerangka Seatbelt bawaan.

Di **Linux dan WSL2**, instal paket yang diperlukan terlebih dahulu:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

### Aktifkan sandboxing

Anda dapat mengaktifkan sandboxing dengan menjalankan perintah `/sandbox`:

```text  theme={null}
/sandbox
```

Ini membuka menu di mana Anda dapat memilih antara mode sandbox. Jika dependensi yang diperlukan hilang (seperti `bubblewrap` atau `socat` di Linux), menu menampilkan instruksi instalasi untuk platform Anda.

Secara default, jika sandbox tidak dapat dimulai (dependensi yang hilang, platform yang tidak didukung, atau pembatasan platform), Claude Code menampilkan peringatan dan menjalankan perintah tanpa sandboxing. Untuk menjadikan ini kegagalan keras sebagai gantinya, atur [`sandbox.failIfUnavailable`](/id/settings#sandbox-settings) ke `true`. Ini dimaksudkan untuk penyebaran terkelola yang memerlukan sandboxing sebagai gerbang keamanan.

### Mode sandbox

Claude Code menawarkan dua mode sandbox:

**Mode izin otomatis**: Perintah Bash akan mencoba berjalan di dalam sandbox dan secara otomatis diizinkan tanpa memerlukan izin. Perintah yang tidak dapat di-sandbox (seperti yang memerlukan akses jaringan ke host yang tidak diizinkan) kembali ke alur izin reguler. Aturan tanya/tolak eksplisit yang telah Anda konfigurasi selalu dihormati.

**Mode izin reguler**: Semua perintah bash melalui alur izin standar, bahkan saat di-sandbox. Ini memberikan lebih banyak kontrol tetapi memerlukan lebih banyak persetujuan.

Di kedua mode, sandbox memberlakukan pembatasan filesystem dan jaringan yang sama. Perbedaannya hanya dalam apakah perintah sandboxed disetujui secara otomatis atau memerlukan izin eksplisit.

<Info>
  Mode izin otomatis bekerja secara independen dari pengaturan mode izin Anda. Bahkan jika Anda tidak dalam mode "terima edit", perintah bash sandboxed akan berjalan secara otomatis saat izin otomatis diaktifkan. Ini berarti perintah bash yang memodifikasi file dalam batas sandbox akan dieksekusi tanpa meminta, bahkan ketika alat edit file biasanya memerlukan persetujuan.
</Info>

### Konfigurasi sandboxing

Sesuaikan perilaku sandbox melalui file `settings.json` Anda. Lihat [Settings](/id/settings#sandbox-settings) untuk referensi konfigurasi lengkap.

#### Memberikan akses tulis subprocess ke jalur tertentu

Secara default, perintah sandboxed hanya dapat menulis ke direktori kerja saat ini. Jika perintah subprocess seperti `kubectl`, `terraform`, atau `npm` perlu menulis di luar direktori proyek, gunakan `sandbox.filesystem.allowWrite` untuk memberikan akses ke jalur tertentu:

```json  theme={null}
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

Ketika `allowWrite` (atau `denyWrite`/`denyRead`/`allowRead`) didefinisikan dalam beberapa [cakupan pengaturan](/id/settings#settings-precedence), array **digabungkan**, artinya jalur dari setiap cakupan digabungkan, bukan diganti. Misalnya, jika pengaturan terkelola memungkinkan penulisan ke `/opt/company-tools` dan pengguna menambahkan `~/.kube` dalam pengaturan pribadi mereka, kedua jalur disertakan dalam konfigurasi sandbox akhir. Ini berarti pengguna dan proyek dapat memperluas daftar tanpa menduplikasi atau menimpa jalur yang ditetapkan oleh cakupan prioritas lebih tinggi.

Awalan jalur mengontrol bagaimana jalur diselesaikan:

| Awalan                 | Arti                                                                                                | Contoh                                                                           |
| :--------------------- | :-------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `/`                    | Jalur absolut dari akar filesystem                                                                  | `/tmp/build` tetap `/tmp/build`                                                  |
| `~/`                   | Relatif terhadap direktori home                                                                     | `~/.kube` menjadi `$HOME/.kube`                                                  |
| `./` atau tanpa awalan | Relatif terhadap akar proyek untuk pengaturan proyek, atau ke `~/.claude` untuk pengaturan pengguna | `./output` dalam `.claude/settings.json` diselesaikan ke `<project-root>/output` |

Awalan `//path` yang lebih lama untuk jalur absolut masih berfungsi. Jika Anda sebelumnya menggunakan `/path` tunggal mengharapkan resolusi relatif proyek, beralih ke `./path`. Sintaks ini berbeda dari [aturan izin Read dan Edit](/id/permissions#read-and-edit), yang menggunakan `//path` untuk absolut dan `/path` untuk relatif proyek. Jalur filesystem sandbox menggunakan konvensi standar: `/tmp/build` adalah jalur absolut.

Anda juga dapat menolak akses tulis atau baca menggunakan `sandbox.filesystem.denyWrite` dan `sandbox.filesystem.denyRead`. Ini digabungkan dengan jalur apa pun dari aturan izin `Edit(...)` dan `Read(...)`. Untuk mengizinkan kembali pembacaan jalur tertentu dalam wilayah yang ditolak, gunakan `sandbox.filesystem.allowRead`, yang mengambil alih `denyRead`. Ketika `allowManagedReadPathsOnly` diaktifkan dalam pengaturan terkelola, hanya entri `allowRead` terkelola yang dihormati; entri `allowRead` pengguna, proyek, dan lokal diabaikan.

Misalnya, untuk memblokir pembacaan dari seluruh direktori home sambil tetap memungkinkan pembacaan dari proyek saat ini, tambahkan ini ke `.claude/settings.json` proyek Anda:

```json  theme={null}
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

<Tip>
  Tidak semua perintah kompatibel dengan sandboxing langsung. Beberapa catatan yang mungkin membantu Anda memanfaatkan sandbox sebaik-baiknya:

  * Banyak alat CLI memerlukan akses ke host tertentu. Saat Anda menggunakan alat ini, mereka akan meminta izin untuk mengakses host tertentu. Memberikan izin akan memungkinkan mereka mengakses host ini sekarang dan di masa depan, memungkinkan mereka untuk dieksekusi dengan aman di dalam sandbox.
  * `watchman` tidak kompatibel dengan berjalan di sandbox. Jika Anda menjalankan `jest`, pertimbangkan menggunakan `jest --no-watchman`
  * `docker` tidak kompatibel dengan berjalan di sandbox. Pertimbangkan untuk menentukan `docker` dalam `excludedCommands` untuk memaksanya berjalan di luar sandbox.
</Tip>

<Note>
  Claude Code mencakup mekanisme pintu keluar yang disengaja yang memungkinkan perintah berjalan di luar sandbox saat diperlukan. Ketika perintah gagal karena pembatasan sandbox (seperti masalah konektivitas jaringan atau alat yang tidak kompatibel), Claude diminta untuk menganalisis kegagalan dan dapat mencoba kembali perintah dengan parameter `dangerouslyDisableSandbox`. Perintah yang menggunakan parameter ini melalui alur izin Claude Code normal yang memerlukan izin pengguna untuk dieksekusi. Ini memungkinkan Claude Code menangani kasus tepi di mana alat tertentu atau operasi jaringan tidak dapat berfungsi dalam batasan sandbox.

  Anda dapat menonaktifkan pintu keluar ini dengan mengatur `"allowUnsandboxedCommands": false` dalam [pengaturan sandbox](/id/settings#sandbox-settings) Anda. Saat dinonaktifkan, parameter `dangerouslyDisableSandbox` sepenuhnya diabaikan dan semua perintah harus berjalan sandboxed atau secara eksplisit terdaftar dalam `excludedCommands`.
</Note>

## Manfaat keamanan

### Perlindungan terhadap prompt injection

Bahkan jika penyerang berhasil memanipulasi perilaku Claude Code melalui prompt injection, sandbox memastikan sistem Anda tetap aman:

**Perlindungan filesystem:**

* Tidak dapat memodifikasi file konfigurasi kritis seperti `~/.bashrc`
* Tidak dapat memodifikasi file tingkat sistem di `/bin/`
* Tidak dapat membaca file yang ditolak dalam [pengaturan izin Claude](/id/permissions#manage-permissions) Anda

**Perlindungan jaringan:**

* Tidak dapat mengeksfiltrasikan data ke server yang dikendalikan penyerang
* Tidak dapat mengunduh skrip berbahaya dari domain yang tidak sah
* Tidak dapat melakukan panggilan API yang tidak terduga ke layanan yang tidak disetujui
* Tidak dapat menghubungi domain apa pun yang tidak secara eksplisit diizinkan

**Pemantauan dan kontrol:**

* Semua upaya akses di luar sandbox diblokir pada tingkat OS
* Anda menerima notifikasi segera ketika batas diuji
* Anda dapat memilih untuk menolak, mengizinkan sekali, atau secara permanen memperbarui konfigurasi Anda

### Permukaan serangan berkurang

Sandboxing membatasi potensi kerusakan dari:

* **Dependensi berbahaya**: Paket NPM atau dependensi lain dengan kode berbahaya
* **Skrip yang dikompromikan**: Skrip build atau alat dengan kerentanan keamanan
* **Rekayasa sosial**: Serangan yang menipu pengguna untuk menjalankan perintah berbahaya
* **Prompt injection**: Serangan yang menipu Claude untuk menjalankan perintah berbahaya

### Operasi transparan

Ketika Claude Code mencoba mengakses sumber daya jaringan di luar sandbox:

1. Operasi diblokir pada tingkat OS
2. Anda menerima notifikasi segera
3. Anda dapat memilih untuk:
   * Menolak permintaan
   * Mengizinkan sekali
   * Memperbarui konfigurasi sandbox Anda untuk secara permanen mengizinkannya

## Keterbatasan Keamanan

* Keterbatasan Sandboxing Jaringan: Sistem penyaringan jaringan beroperasi dengan membatasi domain yang diizinkan untuk terhubung oleh proses. Ini tidak sebaliknya memeriksa lalu lintas yang melewati proxy dan pengguna bertanggung jawab untuk memastikan mereka hanya mengizinkan domain tepercaya dalam kebijakan mereka.

<Warning>
  Pengguna harus menyadari potensi risiko yang datang dari mengizinkan domain luas seperti `github.com` yang mungkin memungkinkan eksfiltrasi data. Juga, dalam beberapa kasus mungkin dapat membypass penyaringan jaringan melalui [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting).
</Warning>

* Eskalasi Privilege melalui Unix Sockets: Konfigurasi `allowUnixSockets` dapat secara tidak sengaja memberikan akses ke layanan sistem yang kuat yang dapat menyebabkan bypass sandbox. Misalnya, jika digunakan untuk memungkinkan akses ke `/var/run/docker.sock` ini akan secara efektif memberikan akses ke sistem host melalui eksploitasi soket docker. Pengguna didorong untuk mempertimbangkan dengan hati-hati soket unix apa pun yang mereka izinkan melalui sandbox.
* Eskalasi Izin Filesystem: Izin penulisan filesystem yang terlalu luas dapat memungkinkan serangan eskalasi privilege. Mengizinkan penulisan ke direktori yang berisi executable dalam `$PATH`, direktori konfigurasi sistem, atau file konfigurasi shell pengguna (`.bashrc`, `.zshrc`) dapat menyebabkan eksekusi kode dalam konteks keamanan yang berbeda ketika pengguna lain atau proses sistem mengakses file ini.
* Kekuatan Sandbox Linux: Implementasi Linux menyediakan isolasi filesystem dan jaringan yang kuat tetapi mencakup mode `enableWeakerNestedSandbox` yang memungkinkannya bekerja di dalam lingkungan Docker tanpa namespace istimewa. Opsi ini secara konsiderabel melemahkan keamanan dan hanya boleh digunakan dalam kasus di mana isolasi tambahan sebaliknya diberlakukan.

## Bagaimana sandboxing berhubungan dengan izin

Sandboxing dan [izin](/id/permissions) adalah lapisan keamanan komplementer yang bekerja bersama:

* **Izin** mengontrol alat mana yang dapat digunakan Claude Code dan dievaluasi sebelum alat apa pun berjalan. Mereka berlaku untuk semua alat: Bash, Read, Edit, WebFetch, MCP, dan lainnya.
* **Sandboxing** menyediakan penegakan tingkat OS yang membatasi apa yang dapat diakses perintah Bash pada tingkat filesystem dan jaringan. Ini hanya berlaku untuk perintah Bash dan proses anak mereka.

Pembatasan filesystem dan jaringan dikonfigurasi melalui pengaturan sandbox dan aturan izin:

* Gunakan `sandbox.filesystem.allowWrite` untuk memberikan akses tulis subprocess ke jalur di luar direktori kerja
* Gunakan `sandbox.filesystem.denyWrite` dan `sandbox.filesystem.denyRead` untuk memblokir akses subprocess ke jalur tertentu
* Gunakan `sandbox.filesystem.allowRead` untuk mengizinkan kembali pembacaan jalur tertentu dalam wilayah yang ditolak
* Gunakan aturan tolak `Read` dan `Edit` untuk memblokir akses ke file atau direktori tertentu
* Gunakan aturan izin/tolak `WebFetch` untuk mengontrol akses domain
* Gunakan `allowedDomains` sandbox untuk mengontrol domain mana yang dapat dijangkau perintah Bash

Jalur dari pengaturan `sandbox.filesystem` dan aturan izin digabungkan bersama ke dalam konfigurasi sandbox akhir.

[Repositori](https://github.com/anthropics/claude-code/tree/main/examples/settings) ini mencakup konfigurasi pengaturan pemula untuk skenario penyebaran umum, termasuk contoh khusus sandbox. Gunakan ini sebagai titik awal dan sesuaikan dengan kebutuhan Anda.

## Penggunaan lanjutan

### Konfigurasi proxy khusus

Untuk organisasi yang memerlukan keamanan jaringan lanjutan, Anda dapat menerapkan proxy khusus untuk:

* Mendekripsi dan memeriksa lalu lintas HTTPS
* Menerapkan aturan penyaringan khusus
* Mencatat semua permintaan jaringan
* Mengintegrasikan dengan infrastruktur keamanan yang ada

```json  theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### Integrasi dengan alat keamanan yang ada

Alat bash sandboxed bekerja bersama dengan:

* **Aturan izin**: Gabungkan dengan [pengaturan izin](/id/permissions) untuk pertahanan berlapis
* **Kontainer pengembangan**: Gunakan dengan [devcontainers](/id/devcontainer) untuk isolasi tambahan
* **Kebijakan perusahaan**: Terapkan konfigurasi sandbox melalui [pengaturan terkelola](/id/settings#settings-precedence)

## Praktik terbaik

1. **Mulai ketat**: Mulai dengan izin minimal dan perluas sesuai kebutuhan
2. **Pantau log**: Tinjau upaya pelanggaran sandbox untuk memahami kebutuhan Claude Code
3. **Gunakan konfigurasi khusus lingkungan**: Aturan sandbox berbeda untuk konteks pengembangan vs. produksi
4. **Gabungkan dengan izin**: Gunakan sandboxing bersama dengan kebijakan IAM untuk keamanan komprehensif
5. **Konfigurasi uji**: Verifikasi pengaturan sandbox Anda tidak memblokir alur kerja yang sah

## Sumber terbuka

Runtime sandbox tersedia sebagai paket npm sumber terbuka untuk digunakan dalam proyek agen Anda sendiri. Ini memungkinkan komunitas agen AI yang lebih luas untuk membangun sistem otonom yang lebih aman dan lebih aman. Ini juga dapat digunakan untuk sandbox program lain yang mungkin ingin Anda jalankan. Misalnya, untuk sandbox server MCP Anda dapat menjalankan:

```bash  theme={null}
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Untuk detail implementasi dan kode sumber, kunjungi [repositori GitHub](https://github.com/anthropic-experimental/sandbox-runtime).

## Keterbatasan

* **Overhead kinerja**: Minimal, tetapi beberapa operasi filesystem mungkin sedikit lebih lambat
* **Kompatibilitas**: Beberapa alat yang memerlukan pola akses sistem tertentu mungkin memerlukan penyesuaian konfigurasi, atau bahkan mungkin perlu dijalankan di luar sandbox
* **Dukungan platform**: Mendukung macOS, Linux, dan WSL2. WSL1 tidak didukung. Dukungan Windows asli sedang direncanakan.

## Apa yang sandboxing tidak mencakup

Sandbox mengisolasi subprocess Bash. Alat lain beroperasi di bawah batas yang berbeda:

* **Alat file bawaan**: Read, Edit, dan Write menggunakan sistem izin secara langsung daripada berjalan melalui sandbox. Lihat [izin](/id/permissions).
* **Penggunaan komputer di Desktop**: ketika Claude membuka aplikasi dan mengontrol layar Anda di macOS, itu berjalan di desktop aktual Anda daripada di lingkungan terisolasi. Prompt izin per-aplikasi membatasi setiap aplikasi. Lihat [penggunaan komputer](/id/desktop#let-claude-use-your-computer).

## Lihat juga

* [Security](/id/security) - Fitur keamanan komprehensif dan praktik terbaik
* [Permissions](/id/permissions) - Konfigurasi izin dan kontrol akses
* [Settings](/id/settings) - Referensi konfigurasi lengkap
* [CLI reference](/id/cli-reference) - Opsi baris perintah
