> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Siapkan Claude Code

> Instal, autentikasi, dan mulai menggunakan Claude Code di mesin pengembangan Anda.

## Persyaratan sistem

* **Sistem Operasi**:
  * macOS 13.0+
  * Windows 10 1809+ atau Windows Server 2019+ ([lihat catatan setup](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([dependensi tambahan diperlukan](#platform-specific-setup))
* **Hardware**: RAM 4 GB+
* **Jaringan**: Koneksi internet diperlukan (lihat [konfigurasi jaringan](/id/network-config#network-access-requirements))
* **Shell**: Bekerja terbaik di Bash atau Zsh
* **Lokasi**: [Negara yang didukung Anthropic](https://www.anthropic.com/supported-countries)

### Dependensi tambahan

* **ripgrep**: Biasanya disertakan dengan Claude Code. Jika pencarian gagal, lihat [pemecahan masalah pencarian](/id/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)**: Hanya diperlukan untuk [instalasi npm yang sudah usang](#npm-installation-deprecated)

## Instalasi

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

Setelah proses instalasi selesai, navigasikan ke proyek Anda dan mulai Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Jika Anda mengalami masalah apa pun selama instalasi, konsultasikan [panduan pemecahan masalah](/id/troubleshooting).

<Tip>
  Jalankan `claude doctor` setelah instalasi untuk memeriksa jenis dan versi instalasi Anda.
</Tip>

### Setup khusus platform

**Windows**: Jalankan Claude Code secara native (memerlukan [Git Bash](https://git-scm.com/downloads/win)) atau di dalam WSL. Baik WSL 1 maupun WSL 2 didukung, tetapi WSL 1 memiliki dukungan terbatas dan tidak mendukung fitur seperti sandboxing alat Bash.

**Alpine Linux dan distribusi berbasis musl/uClibc lainnya**:

Installer native di Alpine dan distribusi berbasis musl/uClibc lainnya memerlukan `libgcc`, `libstdc++`, dan `ripgrep`. Instal ini menggunakan manajer paket distribusi Anda, kemudian atur `USE_BUILTIN_RIPGREP=0`.

Di Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Autentikasi

#### Untuk individu

1. **Paket Claude Pro atau Max** (direkomendasikan): Berlangganan [paket Pro atau Max](https://claude.ai/pricing) Claude untuk langganan terpadu yang mencakup Claude Code dan Claude di web. Kelola akun Anda di satu tempat dan masuk dengan akun Claude.ai Anda.
2. **Claude Console**: Terhubung melalui [Claude Console](https://console.anthropic.com) dan selesaikan proses OAuth. Memerlukan penagihan aktif di Anthropic Console. Ruang kerja "Claude Code" dibuat secara otomatis untuk pelacakan penggunaan dan manajemen biaya. Anda tidak dapat membuat kunci API untuk ruang kerja Claude Code; itu didedikasikan secara eksklusif untuk penggunaan Claude Code.

#### Untuk tim dan organisasi

1. **Claude untuk Tim atau Enterprise** (direkomendasikan): Berlangganan [Claude untuk Tim](https://claude.com/pricing#team-&-enterprise) atau [Claude untuk Enterprise](https://anthropic.com/contact-sales) untuk penagihan terpusat, manajemen tim, dan akses ke Claude Code dan Claude di web. Anggota tim masuk dengan akun Claude.ai mereka.
2. **Claude Console dengan penagihan tim**: Siapkan organisasi [Claude Console](https://console.anthropic.com) bersama dengan penagihan tim. Undang anggota tim dan tetapkan peran untuk pelacakan penggunaan.
3. **Penyedia cloud**: Konfigurasikan Claude Code untuk menggunakan [Amazon Bedrock, Google Vertex AI, atau Microsoft Foundry](/id/third-party-integrations) untuk penyebaran dengan infrastruktur cloud yang ada.

### Instal versi tertentu

Installer native menerima nomor versi tertentu atau saluran rilis (`latest` atau `stable`). Saluran yang Anda pilih saat instalasi menjadi default untuk pembaruan otomatis. Lihat [Konfigurasikan saluran rilis](#configure-release-channel) untuk informasi lebih lanjut.

Untuk menginstal versi terbaru (default):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Untuk menginstal versi stabil:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Untuk menginstal nomor versi tertentu:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Integritas biner dan penandatanganan kode

* Checksum SHA256 untuk semua platform dipublikasikan dalam manifes rilis, saat ini berlokasi di `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (contoh: ganti `{VERSION}` dengan `2.0.30`)
* Biner yang ditandatangani didistribusikan untuk platform berikut:
  * macOS: Ditandatangani oleh "Anthropic PBC" dan dinotarisi oleh Apple
  * Windows: Ditandatangani oleh "Anthropic, PBC"

## Instalasi NPM (usang)

Instalasi NPM sudah usang. Gunakan metode [instalasi native](#installation) jika memungkinkan. Untuk memigrasikan instalasi npm yang ada ke native, jalankan `claude install`.

**Instalasi npm global**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  JANGAN gunakan `sudo npm install -g` karena ini dapat menyebabkan masalah izin dan risiko keamanan.
  Jika Anda mengalami kesalahan izin, lihat [pemecahan masalah kesalahan izin](/id/troubleshooting#command-not-found-claude-or-permission-errors) untuk solusi yang direkomendasikan.
</Warning>

## Setup Windows

**Opsi 1: Claude Code dalam WSL**

* Baik WSL 1 maupun WSL 2 didukung
* WSL 2 mendukung [sandboxing](/id/sandboxing) untuk keamanan yang ditingkatkan. WSL 1 tidak mendukung sandboxing.

**Opsi 2: Claude Code di Windows native dengan Git Bash**

* Memerlukan [Git untuk Windows](https://git-scm.com/downloads/win)
* Untuk instalasi Git portabel, tentukan jalur ke `bash.exe` Anda:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Perbarui Claude Code

### Pembaruan otomatis

Claude Code secara otomatis tetap terbaru untuk memastikan Anda memiliki fitur terbaru dan perbaikan keamanan.

* **Pemeriksaan pembaruan**: Dilakukan saat startup dan secara berkala saat berjalan
* **Proses pembaruan**: Mengunduh dan menginstal secara otomatis di latar belakang
* **Notifikasi**: Anda akan melihat notifikasi ketika pembaruan diinstal
* **Menerapkan pembaruan**: Pembaruan berlaku saat Anda memulai Claude Code berikutnya

<Note>
  Instalasi Homebrew dan WinGet tidak auto-update. Gunakan `brew upgrade claude-code` atau `winget upgrade Anthropic.ClaudeCode` untuk memperbarui secara manual.

  **Masalah yang diketahui:** Claude Code mungkin memberi tahu Anda tentang pembaruan sebelum versi baru tersedia di manajer paket ini. Jika upgrade gagal, tunggu dan coba lagi nanti.
</Note>

### Konfigurasikan saluran rilis

Konfigurasikan saluran rilis mana yang diikuti Claude Code untuk pembaruan otomatis dan `claude update` dengan pengaturan `autoUpdatesChannel`:

* `"latest"` (default): Terima fitur baru segera setelah dirilis
* `"stable"`: Gunakan versi yang biasanya sekitar satu minggu lama, lewati rilis dengan regresi besar

Konfigurasikan ini melalui `/config` → **Saluran auto-update**, atau tambahkan ke [file settings.json](/id/settings) Anda:

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Untuk penyebaran enterprise, Anda dapat memberlakukan saluran rilis yang konsisten di seluruh organisasi Anda menggunakan [pengaturan terkelola](/id/settings#settings-files).

### Nonaktifkan pembaruan otomatis

Atur variabel lingkungan `DISABLE_AUTOUPDATER` di shell Anda atau [file settings.json](/id/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Perbarui secara manual

```bash  theme={null}
claude update
```

## Copot Claude Code

Jika Anda perlu mencopot Claude Code, ikuti instruksi untuk metode instalasi Anda.

### Instalasi native

Hapus biner Claude Code dan file versi:

**macOS, Linux, WSL:**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell:**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD:**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Instalasi Homebrew

```bash  theme={null}
brew uninstall --cask claude-code
```

### Instalasi WinGet

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Instalasi NPM

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Bersihkan file konfigurasi (opsional)

<Warning>
  Menghapus file konfigurasi akan menghapus semua pengaturan, alat yang diizinkan, konfigurasi server MCP, dan riwayat sesi Anda.
</Warning>

Untuk menghapus pengaturan Claude Code dan data cache:

**macOS, Linux, WSL:**

```bash  theme={null}
# Hapus pengaturan pengguna dan status
rm -rf ~/.claude
rm ~/.claude.json

# Hapus pengaturan khusus proyek (jalankan dari direktori proyek Anda)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# Hapus pengaturan pengguna dan status
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Hapus pengaturan khusus proyek (jalankan dari direktori proyek Anda)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM Hapus pengaturan pengguna dan status
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Hapus pengaturan khusus proyek (jalankan dari direktori proyek Anda)
rmdir /s /q ".claude"
del ".mcp.json"
```
