> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Pengaturan lanjutan

> Persyaratan sistem, instalasi khusus platform, manajemen versi, dan penghapusan instalasi untuk Claude Code.

Halaman ini mencakup persyaratan sistem, detail instalasi khusus platform, pembaruan, dan penghapusan instalasi. Untuk panduan langkah demi langkah sesi pertama Anda, lihat [quickstart](/id/quickstart). Jika Anda belum pernah menggunakan terminal sebelumnya, lihat [panduan terminal](/id/terminal-guide).

## Persyaratan sistem

Claude Code berjalan pada platform dan konfigurasi berikut:

* **Sistem operasi**:
  * macOS 13.0+
  * Windows 10 1809+ atau Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Perangkat keras**: RAM 4 GB+
* **Jaringan**: koneksi internet diperlukan. Lihat [konfigurasi jaringan](/id/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell, atau CMD. Di Windows, [Git for Windows](https://git-scm.com/downloads/win) diperlukan.
* **Lokasi**: [negara yang didukung Anthropic](https://www.anthropic.com/supported-countries)

### Dependensi tambahan

* **ripgrep**: biasanya disertakan dengan Claude Code. Jika pencarian gagal, lihat [troubleshooting pencarian](/id/troubleshooting#search-and-discovery-issues).

## Instal Claude Code

<Tip>
  Lebih suka antarmuka grafis? [Aplikasi Desktop](/id/desktop-quickstart) memungkinkan Anda menggunakan Claude Code tanpa terminal. Unduh untuk [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) atau [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs).

  Baru mengenal terminal? Lihat [panduan terminal](/id/terminal-guide) untuk instruksi langkah demi langkah.
</Tip>

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

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
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

Setelah instalasi selesai, buka terminal di proyek yang ingin Anda kerjakan dan mulai Claude Code:

```bash  theme={null}
claude
```

Jika Anda mengalami masalah apa pun selama instalasi, lihat [panduan troubleshooting](/id/troubleshooting).

### Pengaturan di Windows

Claude Code di Windows memerlukan [Git for Windows](https://git-scm.com/downloads/win) atau WSL. Anda dapat meluncurkan `claude` dari PowerShell, CMD, atau Git Bash. Claude Code menggunakan Git Bash secara internal untuk menjalankan perintah. Anda tidak perlu menjalankan PowerShell sebagai Administrator.

**Opsi 1: Windows Asli dengan Git Bash**

Instal [Git for Windows](https://git-scm.com/downloads/win), kemudian jalankan perintah instalasi dari PowerShell atau CMD.

Jika Claude Code tidak dapat menemukan instalasi Git Bash Anda, atur jalur di [file settings.json](/id/settings) Anda:

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code juga dapat menjalankan PowerShell secara native di Windows sebagai pratinjau opt-in. Lihat [PowerShell tool](/id/tools-reference#powershell-tool) untuk pengaturan dan batasan.

**Opsi 2: WSL**

Baik WSL 1 maupun WSL 2 didukung. WSL 2 mendukung [sandboxing](/id/sandboxing) untuk keamanan yang ditingkatkan. WSL 1 tidak mendukung sandboxing.

### Alpine Linux dan distribusi berbasis musl

Penginstal asli di Alpine dan distribusi berbasis musl/uClibc lainnya memerlukan `libgcc`, `libstdc++`, dan `ripgrep`. Instal ini menggunakan manajer paket distribusi Anda, kemudian atur `USE_BUILTIN_RIPGREP=0`.

Contoh ini menginstal paket yang diperlukan di Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

Kemudian atur `USE_BUILTIN_RIPGREP` ke `0` di file [`settings.json`](/id/settings#available-settings) Anda:

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Verifikasi instalasi Anda

Setelah menginstal, konfirmkan Claude Code berfungsi:

```bash  theme={null}
claude --version
```

Untuk pemeriksaan yang lebih terperinci tentang instalasi dan konfigurasi Anda, jalankan [`claude doctor`](/id/troubleshooting#get-more-help):

```bash  theme={null}
claude doctor
```

## Autentikasi

Claude Code memerlukan akun Pro, Max, Team, Enterprise, atau Console. Paket Claude.ai gratis tidak termasuk akses Claude Code. Anda juga dapat menggunakan Claude Code dengan penyedia API pihak ketiga seperti [Amazon Bedrock](/id/amazon-bedrock), [Google Vertex AI](/id/google-vertex-ai), atau [Microsoft Foundry](/id/microsoft-foundry).

Setelah menginstal, masuk dengan menjalankan `claude` dan mengikuti petunjuk browser. Lihat [Autentikasi](/id/authentication) untuk semua jenis akun dan opsi pengaturan tim.

## Perbarui Claude Code

Instalasi asli secara otomatis diperbarui di latar belakang. Anda dapat [mengonfigurasi saluran rilis](#configure-release-channel) untuk mengontrol apakah Anda menerima pembaruan segera atau sesuai jadwal stabil yang tertunda, atau [menonaktifkan pembaruan otomatis](#disable-auto-updates) sepenuhnya. Instalasi Homebrew dan WinGet memerlukan pembaruan manual.

### Pembaruan otomatis

Claude Code memeriksa pembaruan saat startup dan secara berkala saat berjalan. Pembaruan diunduh dan diinstal di latar belakang, kemudian berlaku saat Anda memulai Claude Code berikutnya.

<Note>
  Instalasi Homebrew dan WinGet tidak auto-update. Gunakan `brew upgrade claude-code` atau `winget upgrade Anthropic.ClaudeCode` untuk memperbarui secara manual.

  **Masalah yang diketahui:** Claude Code dapat memberi tahu Anda tentang pembaruan sebelum versi baru tersedia di manajer paket ini. Jika upgrade gagal, tunggu dan coba lagi nanti.

  Homebrew menyimpan versi lama di disk setelah upgrade. Jalankan `brew cleanup claude-code` secara berkala untuk membebaskan ruang disk.
</Note>

### Konfigurasi saluran rilis

Kontrol saluran rilis mana yang diikuti Claude Code untuk pembaruan otomatis dan `claude update` dengan pengaturan `autoUpdatesChannel`:

* `"latest"`, default: terima fitur baru segera setelah dirilis
* `"stable"`: gunakan versi yang biasanya sekitar satu minggu lama, lewati rilis dengan regresi besar

Konfigurasi ini melalui `/config` → **Auto-update channel**, atau tambahkan ke [file settings.json](/id/settings) Anda:

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Untuk penerapan enterprise, Anda dapat memberlakukan saluran rilis yang konsisten di seluruh organisasi Anda menggunakan [managed settings](/id/permissions#managed-settings).

### Nonaktifkan pembaruan otomatis

Atur `DISABLE_AUTOUPDATER` ke `"1"` di kunci `env` dari file [`settings.json`](/id/settings#available-settings) Anda:

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Perbarui secara manual

Untuk menerapkan pembaruan segera tanpa menunggu pemeriksaan latar belakang berikutnya, jalankan:

```bash  theme={null}
claude update
```

## Opsi instalasi lanjutan

Opsi ini untuk version pinning, migrasi dari npm, dan verifikasi integritas biner.

### Instal versi tertentu

Penginstal asli menerima nomor versi tertentu atau saluran rilis (`latest` atau `stable`). Saluran yang Anda pilih saat instalasi menjadi default Anda untuk pembaruan otomatis. Lihat [konfigurasi saluran rilis](#configure-release-channel) untuk informasi lebih lanjut.

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
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Instalasi npm yang sudah usang

Instalasi npm sudah usang. Penginstal asli lebih cepat, tidak memerlukan dependensi, dan auto-update di latar belakang. Gunakan metode [instalasi asli](#install-claude-code) jika memungkinkan.

#### Migrasi dari npm ke asli

Jika Anda sebelumnya menginstal Claude Code dengan npm, beralih ke penginstal asli:

```bash  theme={null}
# Instal biner asli
curl -fsSL https://claude.ai/install.sh | bash

# Hapus instalasi npm lama
npm uninstall -g @anthropic-ai/claude-code
```

Anda juga dapat menjalankan `claude install` dari instalasi npm yang ada untuk menginstal biner asli bersama dengannya, kemudian hapus versi npm.

#### Instal dengan npm

Jika Anda memerlukan instalasi npm untuk alasan kompatibilitas, Anda harus memiliki [Node.js 18+](https://nodejs.org/en/download) terinstal. Instal paket secara global:

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  JANGAN gunakan `sudo npm install -g` karena ini dapat menyebabkan masalah izin dan risiko keamanan. Jika Anda mengalami kesalahan izin, lihat [troubleshooting kesalahan izin](/id/troubleshooting#permission-errors-during-installation).
</Warning>

### Integritas biner dan penandatanganan kode

Setiap rilis menerbitkan `manifest.json` yang berisi checksum SHA256 untuk setiap biner platform. Manifes ditandatangani dengan kunci GPG Anthropic, jadi memverifikasi tanda tangan pada manifes secara transitif memverifikasi setiap biner yang tercantum.

#### Verifikasi tanda tangan manifes

Langkah-langkah 1-3 memerlukan shell POSIX dengan `gpg` dan `curl`. Di Windows, jalankan di Git Bash atau WSL. Langkah 4 mencakup opsi PowerShell.

<Steps>
  <Step title="Unduh dan impor kunci publik">
    Kunci penandatanganan rilis dipublikasikan di URL tetap.

    ```bash  theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Tampilkan sidik jari kunci yang diimpor.

    ```bash  theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Konfirmasi output mencakup sidik jari ini:

    ```text  theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Unduh manifes dan tanda tangan">
    Atur `VERSION` ke rilis yang ingin Anda verifikasi.

    ```bash  theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Verifikasi tanda tangan">
    Verifikasi tanda tangan terpisah terhadap manifes.

    ```bash  theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    Hasil yang valid melaporkan `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` juga mencetak `WARNING: This key is not certified with a trusted signature!` untuk kunci yang baru diimpor. Ini diharapkan. Baris `Good signature` mengkonfirmasi pemeriksaan kriptografi lulus. Perbandingan sidik jari di Langkah 1 mengkonfirmasi kunci itu sendiri asli.
  </Step>

  <Step title="Periksa biner terhadap manifes">
    Bandingkan checksum SHA256 biner yang diunduh dengan nilai yang tercantum di bawah `platforms.<platform>.checksum` di `manifest.json`.

    <Tabs>
      <Tab title="Linux">
        ```bash  theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash  theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell  theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  Tanda tangan manifes tersedia untuk rilis dari `2.1.89` ke depan. Rilis sebelumnya menerbitkan checksum di `manifest.json` tanpa tanda tangan terpisah.
</Note>

#### Tanda tangan kode platform

Selain manifes yang ditandatangani, biner individual membawa tanda tangan kode native platform di mana didukung.

* **macOS**: ditandatangani oleh "Anthropic PBC" dan dinotarisi oleh Apple. Verifikasi dengan `codesign --verify --verbose ./claude`.
* **Windows**: ditandatangani oleh "Anthropic, PBC". Verifikasi dengan `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: gunakan tanda tangan manifes di atas untuk memverifikasi integritas. Biner Linux tidak ditandatangani kode secara individual.

## Hapus instalasi Claude Code

Untuk menghapus Claude Code, ikuti instruksi untuk metode instalasi Anda.

### Instalasi asli

Hapus biner Claude Code dan file versi:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Instalasi Homebrew

Hapus cask Homebrew:

```bash  theme={null}
brew uninstall --cask claude-code
```

### Instalasi WinGet

Hapus paket WinGet:

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Hapus paket npm global:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Hapus file konfigurasi

<Warning>
  Menghapus file konfigurasi akan menghapus semua pengaturan, alat yang diizinkan, konfigurasi server MCP, dan riwayat sesi Anda.
</Warning>

Untuk menghapus pengaturan Claude Code dan data cache:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # Hapus pengaturan pengguna dan status
    rm -rf ~/.claude
    rm ~/.claude.json

    # Hapus pengaturan khusus proyek (jalankan dari direktori proyek Anda)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # Hapus pengaturan pengguna dan status
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Hapus pengaturan khusus proyek (jalankan dari direktori proyek Anda)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
