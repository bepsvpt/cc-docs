> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Kontainer pengembangan

> Jalankan Claude Code di dalam kontainer pengembangan untuk lingkungan yang konsisten dan terisolasi di seluruh tim Anda.

Sebuah [kontainer pengembangan](https://containers.dev/), atau dev container, memungkinkan Anda mendefinisikan lingkungan yang identik dan terisolasi yang dapat dijalankan oleh setiap insinyur di tim Anda. Dengan Claude Code yang diinstal di kontainer tersebut, perintah yang dijalankan Claude dieksekusi di dalamnya daripada di mesin host, sementara pengeditan file proyek Anda muncul di repositori lokal Anda saat Anda bekerja.

Halaman ini mencakup [menginstal Claude Code di dev container Anda](#add-claude-code-to-your-dev-container) dan topik konfigurasi yang mengikuti. Setiap topik berdiri sendiri, jadi lompat ke topik yang sesuai dengan apa yang perlu Anda atur:

* [Pertahankan autentikasi dan pengaturan di seluruh rebuild](#persist-authentication-and-settings-across-rebuilds)
* [Terapkan kebijakan organisasi](#enforce-organization-policy)
* [Batasi egress jaringan](#restrict-network-egress)
* [Jalankan tanpa permintaan izin](#run-without-permission-prompts)

<Warning>
  Meskipun dev container menyediakan perlindungan yang substansial, tidak ada sistem yang sepenuhnya kebal terhadap semua serangan.
  Ketika dijalankan dengan `--dangerously-skip-permissions`, dev container tidak mencegah proyek berbahaya dari mengekstraksi apa pun yang dapat diakses di dalam kontainer, termasuk kredensial Claude Code yang disimpan di [`~/.claude`](/id/claude-directory).
  Hanya gunakan dev container saat mengembangkan dengan repositori terpercaya, dan pantau aktivitas Claude.
  Hindari memasang rahasia host seperti `~/.ssh` atau file kredensial cloud ke dalam kontainer; lebih suka token yang dibatasi repositori atau token berumur pendek.
</Warning>

<Accordion title="Bagaimana dev container bekerja dengan editor Anda">
  <img src="https://mintcdn.com/claude-code/YvJyjZfd9yMihr0i/images/devcontainer-architecture.svg?fit=max&auto=format&n=YvJyjZfd9yMihr0i&q=85&s=9017b1d16a446c6cc37ba562f35b9aae" className="dark:hidden" alt="Diagram menunjukkan editor di host yang terhubung ke Docker dev container. Claude Code, terminal, dan alat build berjalan di dalam kontainer. Repositori host di-bind-mount ke dalam kontainer sebagai workspace." width="640" height="300" data-path="images/devcontainer-architecture.svg" />

  <img src="https://mintcdn.com/claude-code/YvJyjZfd9yMihr0i/images/devcontainer-architecture-dark.svg?fit=max&auto=format&n=YvJyjZfd9yMihr0i&q=85&s=ef00c8e25b1ea7a3a152895f1488831b" className="hidden dark:block" alt="Diagram menunjukkan editor di host yang terhubung ke Docker dev container. Claude Code, terminal, dan alat build berjalan di dalam kontainer. Repositori host di-bind-mount ke dalam kontainer sebagai workspace." width="640" height="300" data-path="images/devcontainer-architecture-dark.svg" />

  Dev container berjalan sebagai Docker container, baik di mesin Anda atau di host cloud seperti GitHub Codespaces. Editor yang mendukung spesifikasi Dev Containers, seperti VS Code, GitHub Codespaces, JetBrains IDE, atau Cursor, terhubung ke kontainer tersebut: Anda menjelajahi dan mengedit file di editor seperti biasa, tetapi terminal terintegrasi, language server, dan alat build semuanya berjalan di dalam kontainer daripada di host Anda. Editor tanpa dukungan dev container, seperti Vim biasa, bukan bagian dari alur kerja ini.

  Claude Code berjalan di dalam kontainer, jadi ia melihat file, dependensi, dan alat yang sama seperti sisa toolchain proyek Anda. Di VS Code Anda dapat menggunakan [panel ekstensi Claude Code](/id/vs-code) atau menjalankan `claude` di terminal terintegrasi; keduanya berjalan di dalam kontainer dan berbagi konfigurasi `~/.claude` yang sama.
</Accordion>

## Tambahkan Claude Code ke dev container Anda

Claude Code diinstal ke dalam dev container apa pun melalui [Claude Code Dev Container Feature](https://github.com/anthropics/devcontainer-features/tree/main/src/claude-code).

Pengaturan bekerja dengan alat apa pun yang mendukung spesifikasi Dev Containers, seperti VS Code, GitHub Codespaces, atau JetBrains IDEs. Langkah-langkah di bawah menggunakan VS Code sebagai contoh.

Ketika Anda membuka kontainer di VS Code atau Codespaces, fitur juga menambahkan ekstensi VS Code Claude Code; editor lain mengabaikan bagian itu.

<Tip>
  Baru mengenal dev container? Tutorial [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/tutorial) memandu Anda melalui penginstalan Docker, ekstensi, dan membuka kontainer pertama Anda. Untuk contoh yang lebih lengkap dan diperkuat dengan firewall dan volume persisten, lihat [Coba kontainer referensi](#try-the-reference-container).
</Tip>

<Steps>
  <Step title="Buat atau perbarui devcontainer.json">
    Simpan yang berikut sebagai `.devcontainer/devcontainer.json` di repositori Anda, atau tambahkan blok `features` ke file yang sudah ada.

    Tag versi di akhir, seperti `:1.0`, menentukan skrip instalasi fitur, bukan rilis Claude Code. Fitur menginstal Claude Code terbaru, dan Claude Code secara otomatis memperbarui dirinya sendiri di dalam kontainer secara default.

    Untuk menentukan versi CLI atau menonaktifkan auto-update, lihat [Terapkan kebijakan organisasi](#enforce-organization-policy).

    ```json .devcontainer/devcontainer.json theme={null}
    {
      "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
      "features": {
        "ghcr.io/anthropics/devcontainer-features/claude-code:1.0": {}
      }
    }
    ```

    Ganti baris `image` dengan citra dasar proyek Anda atau hapus jika file yang ada menggunakan Dockerfile.
  </Step>

  <Step title="Rebuild kontainer">
    Buka Command Palette VS Code dengan `Cmd+Shift+P` di Mac atau `Ctrl+Shift+P` di Windows dan Linux, dan jalankan **Dev Containers: Rebuild Container**.

    Untuk alat lain, ikuti tindakan rebuild alat tersebut: lihat [rebuilding di GitHub Codespaces](https://docs.github.com/en/codespaces/developing-in-a-codespace/rebuilding-the-container-in-a-codespace), [Dev Containers CLI](https://github.com/devcontainers/cli), atau dokumentasi dev container IDE Anda.
  </Step>

  <Step title="Masuk ke Claude Code">
    Buka terminal di kontainer yang telah dibangun kembali dan jalankan `claude`, kemudian ikuti permintaan autentikasi.
  </Step>
</Steps>

Apa yang Anda lihat di permintaan autentikasi tergantung pada penyedia Anda:

* **Anthropic**: masuk melalui browser dengan akun Claude atau Anthropic Console Anda
* **[Amazon Bedrock, Google Vertex AI, atau Microsoft Foundry](/id/third-party-integrations)**: Claude Code menggunakan kredensial penyedia cloud Anda, tanpa permintaan browser

Untuk penyedia cloud, teruskan kredensial ke dalam kontainer sebagai variabel lingkungan melalui `containerEnv`, rahasia Codespaces, atau identitas workload cloud Anda daripada memasang file kredensial dari host. Lihat [Amazon Bedrock](/id/amazon-bedrock), [Google Vertex AI](/id/google-vertex-ai), atau [Microsoft Foundry](/id/microsoft-foundry) untuk rantai kredensial yang dibaca Claude Code.

Lihat [Pilih penyedia API Anda](/id/admin-setup#choose-your-api-provider) untuk memutuskan jalur mana yang sesuai dengan organisasi Anda.

<Note>
  Jika masuk browser selesai tetapi callback tidak pernah mencapai kontainer, salin kode yang ditampilkan di browser dan tempel di permintaan `Paste code here if prompted` di terminal. Ini dapat terjadi ketika port forwarding editor tidak merutekan callback localhost.
</Note>

## Pertahankan autentikasi dan pengaturan di seluruh rebuild

Secara default, direktori home kontainer dibuang saat rebuild, jadi insinyur harus masuk lagi setiap kali. Claude Code menyimpan token autentikasi, pengaturan pengguna, dan riwayat sesi di bawah [`~/.claude`](/id/claude-directory). Pasang volume bernama di jalur tersebut untuk menjaga status ini di seluruh rebuild.

Contoh berikut memasang volume di direktori home pengguna `node`:

```json devcontainer.json theme={null}
"mounts": [
  "source=claude-code-config,target=/home/node/.claude,type=volume"
]
```

Ganti `/home/node` dengan direktori home `remoteUser` kontainer Anda. Jika Anda memasang volume di tempat lain selain `~/.claude`, atur [`CLAUDE_CONFIG_DIR`](/id/env-vars) ke jalur mount sehingga Claude Code membaca dan menulis di sana.

Untuk mengisolasi status per proyek daripada berbagi satu volume di semua repositori, sertakan variabel `${devcontainerId}` dalam nama sumber. [Konfigurasi referensi](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json) menggunakan `source=claude-code-config-${devcontainerId}` untuk tujuan ini.

Di GitHub Codespaces, `~/.claude` bertahan di seluruh penghentian dan memulai codespace, tetapi masih dihapus saat Anda membangun kembali kontainer, jadi pemasangan volume di atas juga berlaku di sana. Untuk membawa autentikasi di seluruh codespace, simpan `ANTHROPIC_API_KEY` atau `CLAUDE_CODE_OAUTH_TOKEN` dari [`claude setup-token`](/id/authentication#generate-a-long-lived-token) sebagai [rahasia Codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces); Codespaces membuat rahasia tersedia sebagai variabel lingkungan di dalam kontainer secara otomatis.

## Terapkan kebijakan organisasi

Dev container adalah tempat yang nyaman untuk menerapkan kebijakan organisasi, karena citra dan konfigurasi yang sama berjalan di mesin setiap insinyur.

Claude Code membaca `/etc/claude-code/managed-settings.json` di Linux dan menerapkannya dengan prioritas tertinggi dalam [hierarki pengaturan](/id/settings#how-scopes-interact), jadi nilai di sana menggantikan apa pun yang ditetapkan insinyur di `~/.claude` atau direktori `.claude/` proyek. Salin file ke tempat dari Dockerfile Anda:

```dockerfile Dockerfile theme={null}
RUN mkdir -p /etc/claude-code
COPY managed-settings.json /etc/claude-code/managed-settings.json
```

Karena Dockerfile berada di repositori, siapa pun dengan akses tulis dapat mengubah atau menghapus langkah ini. Untuk kebijakan yang tidak dapat dilewati insinyur dengan mengedit file repositori, berikan pengaturan terkelola melalui [pengaturan yang dikelola server](/id/server-managed-settings) atau MDM Anda. Lihat [file pengaturan terkelola](/id/settings#settings-files) untuk kunci yang tersedia dan jalur pengiriman lainnya.

Untuk mengatur [variabel lingkungan](/id/env-vars) yang berlaku untuk setiap sesi Claude Code di kontainer, tambahkan ke `containerEnv` di `devcontainer.json` Anda. Contoh berikut memilih keluar dari telemetri dan pelaporan kesalahan dan mencegah Claude Code dari auto-update setelah instalasi:

```json devcontainer.json theme={null}
"containerEnv": {
  "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
  "DISABLE_AUTOUPDATER": "1"
}
```

Dev Container Feature selalu menginstal rilis Claude Code terbaru. Untuk menentukan versi Claude Code tertentu untuk build yang dapat direproduksi, instal dari Dockerfile Anda dengan `npm install -g @anthropic-ai/claude-code@X.Y.Z` daripada menggunakan fitur, dan atur `DISABLE_AUTOUPDATER` seperti yang ditunjukkan di atas.

Untuk daftar lengkap kontrol kebijakan termasuk aturan izin, pembatasan alat, dan allowlist server MCP, lihat [Atur Claude Code untuk organisasi Anda](/id/admin-setup).

Untuk membuat [server MCP](/id/mcp) tersedia di dalam kontainer, tentukan di [cakupan proyek](/id/mcp#mcp-installation-scopes) dalam file `.mcp.json` di akar repositori sehingga diperiksa bersama konfigurasi dev container Anda. Instal binari apa pun yang bergantung pada server stdio lokal di Dockerfile Anda, dan tambahkan domain server jarak jauh ke allowlist jaringan Anda.

## Batasi egress jaringan

Anda dapat membatasi lalu lintas keluar kontainer hanya ke domain yang dibutuhkan Claude Code. Lihat [Persyaratan akses jaringan](/id/network-config#network-access-requirements) untuk domain inferensi dan autentikasi, dan [Layanan telemetri](/id/data-usage#telemetry-services) untuk koneksi telemetri dan pelaporan kesalahan opsional dan cara menonaktifkannya.

Kontainer referensi mencakup skrip [`init-firewall.sh`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh) yang memblokir semua lalu lintas keluar kecuali domain yang dibutuhkan Claude Code dan alat pengembangan Anda. Menjalankan firewall di dalam kontainer memerlukan izin ekstra, jadi referensi menambahkan kemampuan `NET_ADMIN` dan `NET_RAW` melalui `runArgs`. Skrip firewall dan kemampuan ini tidak diperlukan untuk Claude Code itu sendiri: Anda dapat meninggalkannya dan mengandalkan kontrol jaringan Anda sendiri.

## Jalankan tanpa permintaan izin

Karena kontainer menjalankan Claude Code sebagai pengguna non-root dan membatasi eksekusi perintah ke kontainer, Anda dapat melewatkan `--dangerously-skip-permissions` untuk operasi tanpa pengawasan. CLI menolak flag ini saat diluncurkan sebagai root, jadi konfirmasi `remoteUser` diatur ke akun non-root.

Melewatkan permintaan izin menghilangkan kesempatan Anda untuk meninjau panggilan alat sebelum dijalankan. Claude masih dapat memodifikasi file apa pun di workspace yang di-bind-mount, yang muncul langsung di host Anda, dan menjangkau apa pun yang diizinkan kebijakan jaringan kontainer. Pasangkan flag ini dengan [pembatasan egress jaringan](#restrict-network-egress) di atas untuk membatasi apa yang dapat dijangkau sesi yang dilewati.

Jika Anda menginginkan lebih sedikit permintaan tanpa menonaktifkan pemeriksaan keamanan, pertimbangkan [mode otomatis](/id/permission-modes#eliminate-prompts-with-auto-mode), yang memiliki pengklasifikasi meninjau tindakan sebelum dijalankan. Untuk mencegah insinyur menggunakan `--dangerously-skip-permissions` sama sekali, atur `permissions.disableBypassPermissionsMode` ke `"disable"` dalam [pengaturan terkelola](/id/settings#permission-settings).

## Coba kontainer referensi

Repositori [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/.devcontainer) mencakup contoh dev container yang menggabungkan CLI, firewall egress, volume persisten, dan shell berbasis Zsh. Ini disediakan sebagai contoh kerja daripada citra dasar yang dipertahankan; gunakan untuk melihat bagaimana potongan-potongan cocok bersama sebelum menerapkannya ke konfigurasi Anda sendiri.

<Steps>
  <Step title="Instal prasyarat">
    Instal VS Code dan [ekstensi Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
  </Step>

  <Step title="Kloning referensi">
    Kloning [repositori Claude Code](https://github.com/anthropics/claude-code) dan buka di VS Code.
  </Step>

  <Step title="Buka kembali di kontainer">
    Ketika diminta, klik **Reopen in Container**, atau jalankan **Dev Containers: Reopen in Container** dari Command Palette.
  </Step>

  <Step title="Mulai Claude Code">
    Setelah kontainer selesai dibangun, buka terminal dengan `` Ctrl+` `` dan jalankan `claude` untuk masuk dan mulai sesi pertama Anda.
  </Step>
</Steps>

Untuk menggunakan konfigurasi ini dengan proyek Anda sendiri, salin direktori `.devcontainer/` ke repositori Anda dan sesuaikan Dockerfile untuk toolchain Anda, atau kembali ke [Tambahkan Claude Code ke dev container Anda](#add-claude-code-to-your-dev-container) untuk menambahkan hanya fitur ke setup yang sudah Anda miliki.

Konfigurasi referensi terdiri dari tiga file. Tidak satupun dari mereka diperlukan saat Anda menambahkan Claude Code ke dev container Anda sendiri melalui fitur, tetapi mereka menunjukkan satu cara untuk menggabungkan potongan-potongan.

| File                                                                                                       | Tujuan                                                                       |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`devcontainer.json`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json) | Pemasangan volume, kemampuan `runArgs`, ekstensi VS Code, dan `containerEnv` |
| [`Dockerfile`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile)               | Citra dasar, alat pengembangan, dan instalasi Claude Code                    |
| [`init-firewall.sh`](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh)   | Memblokir semua lalu lintas jaringan keluar kecuali domain yang diizinkan    |

## Langkah berikutnya

Setelah Claude Code berjalan di dev container Anda, halaman di bawah mencakup sisa peluncuran organisasi: memilih jalur autentikasi, memberikan kebijakan terkelola di luar repositori, memantau penggunaan, dan memahami apa yang disimpan dan dikirim Claude Code.

* [Atur Claude Code untuk organisasi Anda](/id/admin-setup): pilih penyedia autentikasi, putuskan bagaimana kebijakan mencapai perangkat, dan rencanakan peluncuran
* [Pengaturan yang dikelola server](/id/server-managed-settings): berikan kebijakan terkelola dari konsol admin Claude.ai sehingga insinyur tidak dapat melewatinya dengan mengedit file repositori
* [Pantau penggunaan dan aktivitas audit](/id/monitoring-usage): ekspor metrik OpenTelemetry dan tinjau apa yang dijalankan tim Anda
* [Persyaratan akses jaringan](/id/network-config#network-access-requirements): daftar domain lengkap untuk proxy dan firewall
* [Layanan telemetri dan opt-out](/id/data-usage#telemetry-services): apa yang dikirim Claude Code secara default dan variabel lingkungan yang menonaktifkannya
* [Jelajahi direktori `.claude`](/id/claude-directory): apa yang disimpan pemasangan volume, termasuk kredensial, pengaturan, dan riwayat sesi
* [Model keamanan](/id/security): bagaimana sistem izin Claude Code, sandboxing, dan perlindungan injeksi prompt cocok bersama
* [Mode izin](/id/permission-modes): rentang lengkap dari mode rencana ke mode otomatis ke bypass, dan kapan menggunakan masing-masing
