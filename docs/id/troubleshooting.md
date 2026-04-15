> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting

> Temukan solusi untuk masalah umum dengan instalasi dan penggunaan Claude Code.

## Troubleshoot installation issues

<Tip>
  Jika Anda lebih suka melewati terminal sepenuhnya, [aplikasi Claude Code Desktop](/id/desktop-quickstart) memungkinkan Anda menginstal dan menggunakan Claude Code melalui antarmuka grafis. Unduh untuk [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) atau [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) dan mulai coding tanpa setup command-line apa pun.
</Tip>

Temukan pesan kesalahan atau gejala yang Anda lihat:

| Apa yang Anda lihat                                                   | Solusi                                                                                                                  |
| :-------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| `command not found: claude` atau `'claude' is not recognized`         | [Perbaiki PATH Anda](#command-not-found-claude-after-installation)                                                      |
| `syntax error near unexpected token '<'`                              | [Install script returns HTML](#install-script-returns-html-instead-of-a-shell-script)                                   |
| `curl: (56) Failure writing output to destination`                    | [Download script first, then run it](#curl-56-failure-writing-output-to-destination)                                    |
| `Killed` selama install di Linux                                      | [Add swap space for low-memory servers](#install-killed-on-low-memory-linux-servers)                                    |
| `TLS connect error` atau `SSL/TLS secure channel`                     | [Update CA certificates](#tls-or-ssl-connection-errors)                                                                 |
| `Failed to fetch version` atau tidak dapat menjangkau server download | [Check network and proxy settings](#check-network-connectivity)                                                         |
| `irm is not recognized` atau `&& is not valid`                        | [Use the right command for your shell](#windows-irm-or--not-recognized)                                                 |
| `Claude Code on Windows requires git-bash`                            | [Install or configure Git Bash](#windows-claude-code-on-windows-requires-git-bash)                                      |
| `Error loading shared library`                                        | [Wrong binary variant for your system](#linux-wrong-binary-variant-installed-muslglibc-mismatch)                        |
| `Illegal instruction` di Linux                                        | [Architecture mismatch](#illegal-instruction-on-linux)                                                                  |
| `dyld: cannot load` atau `Abort trap` di macOS                        | [Binary incompatibility](#dyld-cannot-load-on-macos)                                                                    |
| `Invoke-Expression: Missing argument in parameter list`               | [Install script returns HTML](#install-script-returns-html-instead-of-a-shell-script)                                   |
| `App unavailable in region`                                           | Claude Code tidak tersedia di negara Anda. Lihat [negara yang didukung](https://www.anthropic.com/supported-countries). |
| `unable to get local issuer certificate`                              | [Configure corporate CA certificates](#tls-or-ssl-connection-errors)                                                    |
| `OAuth error` atau `403 Forbidden`                                    | [Fix authentication](#authentication-issues)                                                                            |

Jika masalah Anda tidak terdaftar, kerjakan langkah-langkah diagnostik ini.

## Debug installation problems

### Check network connectivity

Installer mengunduh dari `storage.googleapis.com`. Verifikasi Anda dapat menjangkaunya:

```bash theme={null}
curl -sI https://storage.googleapis.com
```

Jika ini gagal, jaringan Anda mungkin memblokir koneksi. Penyebab umum:

* Firewall perusahaan atau proxy memblokir Google Cloud Storage
* Pembatasan jaringan regional: coba VPN atau jaringan alternatif
* Masalah TLS/SSL: perbarui sertifikat CA sistem Anda, atau periksa apakah `HTTPS_PROXY` dikonfigurasi

Jika Anda berada di belakang proxy perusahaan, atur `HTTPS_PROXY` dan `HTTP_PROXY` ke alamat proxy Anda sebelum menginstal. Tanyakan kepada tim IT Anda untuk URL proxy jika Anda tidak mengetahuinya, atau periksa pengaturan proxy browser Anda.

Contoh ini menetapkan kedua variabel proxy, kemudian menjalankan installer melalui proxy Anda:

```bash theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### Verify your PATH

Jika instalasi berhasil tetapi Anda mendapatkan kesalahan `command not found` atau `not recognized` saat menjalankan `claude`, direktori instalasi tidak ada di PATH Anda. Shell Anda mencari program di direktori yang terdaftar di PATH, dan installer menempatkan `claude` di `~/.local/bin/claude` di macOS/Linux atau `%USERPROFILE%\.local\bin\claude.exe` di Windows.

Periksa apakah direktori instalasi ada di PATH Anda dengan membuat daftar entri PATH dan memfilter untuk `local/bin`:

<Tabs>
  <Tab title="macOS/Linux">
    ```bash theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    Jika tidak ada output, direktori hilang. Tambahkan ke konfigurasi shell Anda:

    ```bash theme={null}
    # Zsh (macOS default)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux default)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    Atau, tutup dan buka kembali terminal Anda.

    Verifikasi perbaikan berhasil:

    ```bash theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    Jika tidak ada output, tambahkan direktori instalasi ke User PATH Anda:

    ```powershell theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    Mulai ulang terminal Anda agar perubahan berlaku.

    Verifikasi perbaikan berhasil:

    ```powershell theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    Jika tidak ada output, buka System Settings, buka Environment Variables, dan tambahkan `%USERPROFILE%\.local\bin` ke variabel User PATH Anda. Mulai ulang terminal Anda.

    Verifikasi perbaikan berhasil:

    ```batch theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### Check for conflicting installations

Beberapa instalasi Claude Code dapat menyebabkan ketidakcocokan versi atau perilaku yang tidak terduga. Periksa apa yang diinstal:

<Tabs>
  <Tab title="macOS/Linux">
    Buat daftar semua binary `claude` yang ditemukan di PATH Anda:

    ```bash theme={null}
    which -a claude
    ```

    Periksa apakah installer native dan versi npm ada:

    ```bash theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

Jika Anda menemukan beberapa instalasi, pertahankan hanya satu. Instalasi native di `~/.local/bin/claude` direkomendasikan. Hapus instalasi tambahan apa pun:

Uninstall instalasi npm global:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

Hapus instalasi Homebrew di macOS:

```bash theme={null}
brew uninstall --cask claude-code
```

### Check directory permissions

Installer memerlukan akses tulis ke `~/.local/bin/` dan `~/.claude/`. Jika instalasi gagal dengan kesalahan izin, periksa apakah direktori ini dapat ditulis:

```bash theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

Jika salah satu direktori tidak dapat ditulis, buat direktori instalasi dan atur pengguna Anda sebagai pemilik:

```bash theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### Verify the binary works

Jika `claude` diinstal tetapi crash atau hang saat startup, jalankan pemeriksaan ini untuk mempersempit penyebabnya.

Konfirmasi binary ada dan dapat dieksekusi:

```bash theme={null}
ls -la $(which claude)
```

Di Linux, periksa perpustakaan bersama yang hilang. Jika `ldd` menunjukkan perpustakaan yang hilang, Anda mungkin perlu menginstal paket sistem. Di Alpine Linux dan distribusi berbasis musl lainnya, lihat [Alpine Linux setup](/id/setup#alpine-linux-and-musl-based-distributions).

```bash theme={null}
ldd $(which claude) | grep "not found"
```

Jalankan pemeriksaan kewarasan cepat bahwa binary dapat dieksekusi:

```bash theme={null}
claude --version
```

## Common installation issues

Ini adalah masalah instalasi yang paling sering dihadapi dan solusinya.

### Install script returns HTML instead of a shell script

Saat menjalankan perintah install, Anda mungkin melihat salah satu kesalahan ini:

```text theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

Di PowerShell, masalah yang sama muncul sebagai:

```text theme={null}
Invoke-Expression: Missing argument in parameter list.
```

Ini berarti URL instalasi mengembalikan halaman HTML alih-alih skrip instalasi. Jika halaman HTML mengatakan "App unavailable in region," Claude Code tidak tersedia di negara Anda. Lihat [negara yang didukung](https://www.anthropic.com/supported-countries).

Jika tidak, ini dapat terjadi karena masalah jaringan, perutean regional, atau gangguan layanan sementara.

**Solusi:**

1. **Gunakan metode instalasi alternatif**:

   Di macOS atau Linux, instal melalui Homebrew:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   Di Windows, instal melalui WinGet:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **Coba lagi setelah beberapa menit**: masalahnya sering bersifat sementara. Tunggu dan coba perintah asli lagi.

### `command not found: claude` after installation

Instalasi selesai tetapi `claude` tidak berfungsi. Pesan kesalahan yang tepat bervariasi menurut platform:

| Platform    | Pesan kesalahan                                                        |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

Ini berarti direktori instalasi tidak ada di jalur pencarian shell Anda. Lihat [Verify your PATH](#verify-your-path) untuk perbaikan di setiap platform.

### `curl: (56) Failure writing output to destination`

Perintah `curl ... | bash` mengunduh skrip dan meneruskannya langsung ke Bash untuk dieksekusi menggunakan pipe (`|`). Kesalahan ini berarti koneksi putus sebelum skrip selesai diunduh. Penyebab umum termasuk gangguan jaringan, unduhan diblokir di tengah aliran, atau batas sumber daya sistem.

**Solusi:**

1. **Periksa stabilitas jaringan**: Binary Claude Code dihosting di Google Cloud Storage. Uji bahwa Anda dapat menjangkaunya:
   ```bash theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   Jika perintah selesai diam-diam, koneksi Anda baik-baik saja dan masalahnya mungkin intermiten. Coba ulang perintah install. Jika Anda melihat kesalahan, jaringan Anda mungkin memblokir unduhan.

2. **Coba metode instalasi alternatif**:

   Di macOS atau Linux:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   Di Windows:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

### TLS or SSL connection errors

Kesalahan seperti `curl: (35) TLS connect error`, `schannel: next InitializeSecurityContext failed`, atau PowerShell's `Could not establish trust relationship for the SSL/TLS secure channel` menunjukkan kegagalan handshake TLS.

**Solusi:**

1. **Perbarui sertifikat CA sistem Anda**:

   Di Ubuntu/Debian:

   ```bash theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   Di macOS melalui Homebrew:

   ```bash theme={null}
   brew install ca-certificates
   ```

2. **Di Windows, aktifkan TLS 1.2** di PowerShell sebelum menjalankan installer:
   ```powershell theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **Periksa gangguan proxy atau firewall**: proxy perusahaan yang melakukan inspeksi TLS dapat menyebabkan kesalahan ini, termasuk `unable to get local issuer certificate`. Atur `NODE_EXTRA_CA_CERTS` ke bundel sertifikat CA perusahaan Anda:
   ```bash theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   Tanyakan kepada tim IT Anda untuk file sertifikat jika Anda tidak memilikinya. Anda juga dapat mencoba pada koneksi langsung untuk mengkonfirmasi proxy adalah penyebabnya.

### `Failed to fetch version from storage.googleapis.com`

Installer tidak dapat menjangkau server download. Ini biasanya berarti `storage.googleapis.com` diblokir di jaringan Anda.

**Solusi:**

1. **Uji konektivitas secara langsung**:
   ```bash theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **Jika di belakang proxy**, atur `HTTPS_PROXY` sehingga installer dapat merutekan melaluinya. Lihat [proxy configuration](/id/network-config#proxy-configuration) untuk detail.
   ```bash theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **Jika di jaringan terbatas**, coba jaringan berbeda atau VPN, atau gunakan metode instalasi alternatif:

   Di macOS atau Linux:

   ```bash theme={null}
   brew install --cask claude-code
   ```

   Di Windows:

   ```powershell theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows: `irm` or `&&` not recognized

Jika Anda melihat `'irm' is not recognized` atau `The token '&&' is not valid`, Anda menjalankan perintah yang salah untuk shell Anda.

* **`irm` not recognized**: Anda berada di CMD, bukan PowerShell. Anda memiliki dua opsi:

  Buka PowerShell dengan mencari "PowerShell" di menu Start, kemudian jalankan perintah install asli:

  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  Atau tetap di CMD dan gunakan installer CMD sebagai gantinya:

  ```batch theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` not valid**: Anda berada di PowerShell tetapi menjalankan perintah installer CMD. Gunakan installer PowerShell:
  ```powershell theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### Install killed on low-memory Linux servers

Jika Anda melihat `Killed` selama instalasi di VPS atau instance cloud:

```text theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Pembunuh OOM Linux menghentikan proses karena sistem kehabisan memori. Claude Code memerlukan setidaknya 4 GB RAM yang tersedia.

**Solusi:**

1. **Tambahkan ruang swap** jika server Anda memiliki RAM terbatas. Swap menggunakan ruang disk sebagai memori overflow, memungkinkan instalasi selesai bahkan dengan RAM fisik rendah.

   Buat file swap 2 GB dan aktifkan:

   ```bash theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   Kemudian coba ulang instalasi:

   ```bash theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Tutup proses lain** untuk membebaskan memori sebelum menginstal.

3. **Gunakan instance yang lebih besar** jika memungkinkan. Claude Code memerlukan setidaknya 4 GB RAM.

### Install hangs in Docker

Saat menginstal Claude Code di container Docker, menginstal sebagai root ke `/` dapat menyebabkan hang.

**Solusi:**

1. **Atur direktori kerja** sebelum menjalankan installer. Saat dijalankan dari `/`, installer memindai seluruh filesystem, yang menyebabkan penggunaan memori berlebihan. Menetapkan `WORKDIR` membatasi pemindaian ke direktori kecil:
   ```dockerfile theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Tingkatkan batas memori Docker** jika menggunakan Docker Desktop:
   ```bash theme={null}
   docker build --memory=4g .
   ```

### Windows: Claude Desktop overrides `claude` CLI command

Jika Anda menginstal versi lama Claude Desktop, itu mungkin mendaftarkan `Claude.exe` di direktori `WindowsApps` yang mengambil prioritas PATH atas Claude Code CLI. Menjalankan `claude` membuka aplikasi Desktop alih-alih CLI.

Perbarui Claude Desktop ke versi terbaru untuk memperbaiki masalah ini.

### Windows: "Claude Code on Windows requires git-bash"

Claude Code di Windows native memerlukan [Git for Windows](https://git-scm.com/downloads/win), yang mencakup Git Bash.

**Jika Git tidak diinstal**, unduh dan instal dari [git-scm.com/downloads/win](https://git-scm.com/downloads/win). Selama setup, pilih "Add to PATH." Mulai ulang terminal Anda setelah menginstal.

**Jika Git sudah diinstal** tetapi Claude Code masih tidak dapat menemukannya, atur jalur di [file settings.json](/id/settings) Anda:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Jika Git Anda diinstal di tempat lain, temukan jalur dengan menjalankan `where.exe git` di PowerShell dan gunakan jalur `bin\bash.exe` dari direktori itu.

### Linux: wrong binary variant installed (musl/glibc mismatch)

Jika Anda melihat kesalahan tentang perpustakaan bersama yang hilang seperti `libstdc++.so.6` atau `libgcc_s.so.1` setelah instalasi, installer mungkin telah mengunduh varian binary yang salah untuk sistem Anda.

```text theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

Ini dapat terjadi pada sistem berbasis glibc yang memiliki paket cross-compilation musl terinstal, menyebabkan installer salah mendeteksi sistem sebagai musl.

**Solusi:**

1. **Periksa libc mana yang digunakan sistem Anda**:
   ```bash theme={null}
   ldd /bin/ls | head -1
   ```
   Jika menunjukkan `linux-vdso.so` atau referensi ke `/lib/x86_64-linux-gnu/`, Anda berada di glibc. Jika menunjukkan `musl`, Anda berada di musl.

2. **Jika Anda berada di glibc tetapi mendapat binary musl**, hapus instalasi dan instal ulang. Anda juga dapat mengunduh binary yang benar secara manual dari bucket GCS di `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Ajukan [GitHub issue](https://github.com/anthropics/claude-code/issues) dengan output dari `ldd /bin/ls` dan `ls /lib/libc.musl*`.

3. **Jika Anda benar-benar di musl** (Alpine Linux), instal paket yang diperlukan:
   ```bash theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### `Illegal instruction` on Linux

Jika installer mencetak `Illegal instruction` alih-alih pesan OOM `Killed`, binary yang diunduh tidak cocok dengan arsitektur CPU Anda. Ini biasanya terjadi pada server ARM yang menerima binary x86, atau pada CPU lama yang kekurangan set instruksi yang diperlukan.

```text theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**Solusi:**

1. **Verifikasi arsitektur Anda**:
   ```bash theme={null}
   uname -m
   ```
   `x86_64` berarti 64-bit Intel/AMD, `aarch64` berarti ARM64. Jika binary tidak cocok, [ajukan GitHub issue](https://github.com/anthropics/claude-code/issues) dengan output.

2. **Coba metode instalasi alternatif** sementara masalah arsitektur diselesaikan:
   ```bash theme={null}
   brew install --cask claude-code
   ```

### `dyld: cannot load` on macOS

Jika Anda melihat `dyld: cannot load` atau `Abort trap: 6` selama instalasi, binary tidak kompatibel dengan versi macOS atau hardware Anda.

```text theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**Solusi:**

1. **Periksa versi macOS Anda**: Claude Code memerlukan macOS 13.0 atau lebih baru. Buka menu Apple dan pilih About This Mac untuk memeriksa versi Anda.

2. **Perbarui macOS** jika Anda berada di versi lama. Binary menggunakan perintah load yang versi macOS lama tidak mendukung.

3. **Coba Homebrew** sebagai metode instalasi alternatif:
   ```bash theme={null}
   brew install --cask claude-code
   ```

### Windows installation issues: errors in WSL

Anda mungkin mengalami masalah berikut di WSL:

**OS/platform detection issues**: jika Anda menerima kesalahan selama instalasi, WSL mungkin menggunakan Windows `npm`. Coba:

* Jalankan `npm config set os linux` sebelum instalasi
* Instal dengan `npm install -g @anthropic-ai/claude-code --force --no-os-check`. Jangan gunakan `sudo`.

**Node not found errors**: jika Anda melihat `exec: node: not found` saat menjalankan `claude`, lingkungan WSL Anda mungkin menggunakan instalasi Windows Node.js. Anda dapat mengkonfirmasi ini dengan `which npm` dan `which node`, yang harus menunjuk ke jalur Linux yang dimulai dengan `/usr/` daripada `/mnt/c/`. Untuk memperbaiki ini, coba menginstal Node melalui package manager distribusi Linux Anda atau melalui [`nvm`](https://github.com/nvm-sh/nvm).

**nvm version conflicts**: jika Anda memiliki nvm terinstal di WSL dan Windows, Anda mungkin mengalami konflik versi saat beralih versi Node di WSL. Ini terjadi karena WSL mengimpor Windows PATH secara default, menyebabkan Windows nvm/npm mengambil prioritas atas instalasi WSL.

Anda dapat mengidentifikasi masalah ini dengan:

* Menjalankan `which npm` dan `which node` - jika mereka menunjuk ke jalur Windows (dimulai dengan `/mnt/c/`), versi Windows sedang digunakan
* Mengalami fungsionalitas yang rusak setelah beralih versi Node dengan nvm di WSL

Untuk mengatasi masalah ini, perbaiki Linux PATH Anda untuk memastikan versi Linux node/npm mengambil prioritas:

**Solusi utama: Pastikan nvm dimuat dengan benar di shell Anda**

Penyebab paling umum adalah nvm tidak dimuat di shell non-interaktif. Tambahkan berikut ini ke file konfigurasi shell Anda (`~/.bashrc`, `~/.zshrc`, dll.):

```bash theme={null}
# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

Atau jalankan langsung di sesi saat ini:

```bash theme={null}
source ~/.nvm/nvm.sh
```

**Alternatif: Sesuaikan urutan PATH**

Jika nvm dimuat dengan benar tetapi jalur Windows masih mengambil prioritas, Anda dapat secara eksplisit menambahkan jalur Linux Anda ke PATH di konfigurasi shell Anda:

```bash theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  Hindari menonaktifkan impor Windows PATH melalui `appendWindowsPath = false` karena ini merusak kemampuan untuk memanggil executable Windows dari WSL. Demikian pula, hindari menghapus Node.js dari Windows jika Anda menggunakannya untuk pengembangan Windows.
</Warning>

### WSL2 sandbox setup

[Sandboxing](/id/sandboxing) didukung di WSL2 tetapi memerlukan penginstalan paket tambahan. Jika Anda melihat kesalahan seperti "Sandbox requires socat and bubblewrap" saat menjalankan `/sandbox`, instal dependensi:

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

WSL1 tidak mendukung sandboxing. Jika Anda melihat "Sandboxing requires WSL2", Anda perlu upgrade ke WSL2 atau menjalankan Claude Code tanpa sandboxing.

### Permission errors during installation

Jika installer native gagal dengan kesalahan izin, direktori target mungkin tidak dapat ditulis. Lihat [Check directory permissions](#check-directory-permissions).

Jika Anda sebelumnya menginstal dengan npm dan mengalami kesalahan spesifik npm, beralih ke installer native:

```bash theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## Permissions and authentication

Bagian-bagian ini mengatasi kegagalan login, masalah token, dan perilaku prompt izin.

### Repeated permission prompts

Jika Anda menemukan diri Anda berulang kali menyetujui perintah yang sama, Anda dapat mengizinkan alat tertentu berjalan tanpa persetujuan menggunakan perintah `/permissions`. Lihat [Permissions docs](/id/permissions#manage-permissions).

### Authentication issues

Jika Anda mengalami masalah autentikasi:

1. Jalankan `/logout` untuk keluar sepenuhnya
2. Tutup Claude Code
3. Mulai ulang dengan `claude` dan selesaikan proses autentikasi lagi

Jika browser tidak terbuka secara otomatis selama login, tekan `c` untuk menyalin URL OAuth ke clipboard Anda, kemudian tempel ke browser Anda secara manual.

### OAuth error: Invalid code

Jika Anda melihat `OAuth error: Invalid code. Please make sure the full code was copied`, kode login kedaluwarsa atau terpotong selama copy-paste.

**Solusi:**

* Tekan Enter untuk mencoba ulang dan selesaikan login dengan cepat setelah browser terbuka
* Ketik `c` untuk menyalin URL lengkap jika browser tidak terbuka secara otomatis
* Jika menggunakan sesi remote/SSH, browser mungkin terbuka di mesin yang salah. Salin URL yang ditampilkan di terminal dan buka di browser lokal Anda sebagai gantinya.

### 403 Forbidden after login

Jika Anda melihat `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}` setelah login:

* **Pengguna Claude Pro/Max**: verifikasi langganan Anda aktif di [claude.ai/settings](https://claude.ai/settings)
* **Pengguna Console**: konfirmasi akun Anda memiliki peran "Claude Code" atau "Developer" yang ditetapkan oleh admin Anda
* **Di belakang proxy**: proxy perusahaan dapat mengganggu permintaan API. Lihat [network configuration](/id/network-config) untuk setup proxy.

### OAuth login fails in WSL2

Login berbasis browser di WSL2 mungkin gagal jika WSL tidak dapat membuka browser Windows Anda. Atur variabel lingkungan `BROWSER`:

```bash theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

Atau salin URL secara manual: saat prompt login muncul, tekan `c` untuk menyalin URL OAuth, kemudian tempel ke browser Windows Anda.

### "Not logged in" or token expired

Jika Claude Code meminta Anda untuk login lagi setelah sesi, token OAuth Anda mungkin telah kedaluwarsa.

Jalankan `/login` untuk re-authenticate. Jika ini terjadi sering, periksa bahwa jam sistem Anda akurat, karena validasi token bergantung pada timestamp yang benar.

## Configuration file locations

Claude Code menyimpan konfigurasi di beberapa lokasi:

| File                          | Tujuan                                                                                                   |
| :---------------------------- | :------------------------------------------------------------------------------------------------------- |
| `~/.claude/settings.json`     | Pengaturan pengguna (izin, hooks, override model)                                                        |
| `.claude/settings.json`       | Pengaturan proyek (diperiksa ke kontrol sumber)                                                          |
| `.claude/settings.local.json` | Pengaturan proyek lokal (tidak dikomit)                                                                  |
| `~/.claude.json`              | Status global (tema, OAuth, MCP servers)                                                                 |
| `.mcp.json`                   | MCP servers proyek (diperiksa ke kontrol sumber)                                                         |
| `managed-mcp.json`            | [Managed MCP servers](/id/mcp#managed-mcp-configuration)                                                 |
| Managed settings              | [Managed settings](/id/settings#settings-files) (server-managed, MDM/OS-level policies, atau file-based) |

Di Windows, `~` mengacu pada direktori home pengguna Anda, seperti `C:\Users\YourName`.

Untuk detail tentang mengonfigurasi file ini, lihat [Settings](/id/settings) dan [MCP](/id/mcp).

### Resetting configuration

Untuk mengatur ulang Claude Code ke pengaturan default, Anda dapat menghapus file konfigurasi:

```bash theme={null}
# Reset all user settings and state
rm ~/.claude.json
rm -rf ~/.claude/

# Reset project-specific settings
rm -rf .claude/
rm .mcp.json
```

<Warning>
  Ini akan menghapus semua pengaturan, konfigurasi MCP server, dan riwayat sesi Anda.
</Warning>

## Performance and stability

Bagian-bagian ini mencakup masalah yang terkait dengan penggunaan sumber daya, responsivitas, dan perilaku pencarian.

### High CPU or memory usage

Claude Code dirancang untuk bekerja dengan sebagian besar lingkungan pengembangan, tetapi dapat mengonsumsi sumber daya signifikan saat memproses codebase besar. Jika Anda mengalami masalah kinerja:

1. Gunakan `/compact` secara teratur untuk mengurangi ukuran konteks
2. Tutup dan mulai ulang Claude Code di antara tugas-tugas besar
3. Pertimbangkan menambahkan direktori build besar ke file `.gitignore` Anda

### Command hangs or freezes

Jika Claude Code tampak tidak responsif:

1. Tekan Ctrl+C untuk mencoba membatalkan operasi saat ini
2. Jika tidak responsif, Anda mungkin perlu menutup terminal dan memulai ulang

### Search and discovery issues

Jika Search tool, `@file` mentions, custom agents, dan custom skills tidak berfungsi, instal sistem `ripgrep`:

```bash theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Kemudian atur `USE_BUILTIN_RIPGREP=0` di [environment](/id/env-vars) Anda.

### Slow or incomplete search results on WSL

Penalti kinerja pembacaan disk saat [bekerja lintas filesystem di WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) dapat menghasilkan kecocokan yang lebih sedikit dari yang diharapkan saat menggunakan Claude Code di WSL. Pencarian masih berfungsi, tetapi mengembalikan hasil lebih sedikit daripada di filesystem native.

<Note>
  `/doctor` akan menunjukkan Search sebagai OK dalam kasus ini.
</Note>

**Solusi:**

1. **Kirimkan pencarian yang lebih spesifik**: kurangi jumlah file yang dicari dengan menentukan direktori atau jenis file: "Search for JWT validation logic in the auth-service package" atau "Find use of md5 hash in JS files".

2. **Pindahkan proyek ke filesystem Linux**: jika memungkinkan, pastikan proyek Anda berada di filesystem Linux (`/home/`) daripada filesystem Windows (`/mnt/c/`).

3. **Gunakan Windows native sebagai gantinya**: pertimbangkan menjalankan Claude Code secara native di Windows alih-alih melalui WSL, untuk kinerja filesystem yang lebih baik.

## IDE integration issues

Jika Claude Code tidak terhubung ke IDE Anda atau berperilaku tidak terduga dalam terminal IDE, coba solusi di bawah ini.

### JetBrains IDE not detected on WSL2

Jika Anda menggunakan Claude Code di WSL2 dengan IDE JetBrains dan mendapatkan kesalahan "No available IDEs detected", ini mungkin karena konfigurasi jaringan WSL2 atau Windows Firewall memblokir koneksi.

#### WSL2 networking modes

WSL2 menggunakan jaringan NAT secara default, yang dapat mencegah deteksi IDE. Anda memiliki dua opsi:

**Opsi 1: Konfigurasi Windows Firewall** (direkomendasikan)

1. Temukan alamat IP WSL2 Anda:
   ```bash theme={null}
   wsl hostname -I
   # Example output: 172.21.123.45
   ```

2. Buka PowerShell sebagai Administrator dan buat aturan firewall:
   ```powershell theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   Sesuaikan rentang IP berdasarkan subnet WSL2 Anda dari langkah 1.

3. Mulai ulang IDE dan Claude Code Anda

**Opsi 2: Beralih ke mirrored networking**

Tambahkan ke `.wslconfig` di direktori pengguna Windows Anda:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Kemudian mulai ulang WSL dengan `wsl --shutdown` dari PowerShell.

<Note>
  Masalah jaringan ini hanya mempengaruhi WSL2. WSL1 menggunakan jaringan host secara langsung dan tidak memerlukan konfigurasi ini.
</Note>

Untuk tips konfigurasi JetBrains tambahan, lihat [JetBrains IDE guide](/id/jetbrains#plugin-settings).

### Report Windows IDE integration issues

Jika Anda mengalami masalah integrasi IDE di Windows, [buat issue](https://github.com/anthropics/claude-code/issues) dengan informasi berikut:

* Tipe lingkungan: Windows native (Git Bash) atau WSL1/WSL2
* Mode jaringan WSL, jika berlaku: NAT atau mirrored
* Nama dan versi IDE
* Versi ekstensi/plugin Claude Code
* Tipe shell: Bash, Zsh, PowerShell, dll.

### Escape key not working in JetBrains IDE terminals

Jika Anda menggunakan Claude Code di terminal JetBrains dan tombol `Esc` tidak mengganggu agen seperti yang diharapkan, ini mungkin karena benturan pintasan keyboard dengan pintasan default JetBrains.

Untuk memperbaiki masalah ini:

1. Buka Settings → Tools → Terminal
2. Baik:
   * Hapus centang "Move focus to the editor with Escape", atau
   * Klik "Configure terminal keybindings" dan hapus pintasan "Switch focus to Editor"
3. Terapkan perubahan

Ini memungkinkan tombol `Esc` untuk benar-benar mengganggu operasi Claude Code.

## Markdown formatting issues

Claude Code kadang-kadang menghasilkan file markdown dengan tag bahasa yang hilang pada fence kode, yang dapat mempengaruhi syntax highlighting dan readability di GitHub, editor, dan alat dokumentasi.

### Missing language tags in code blocks

Jika Anda memperhatikan blok kode seperti ini dalam markdown yang dihasilkan:

````markdown theme={null}
```
function example() {
  return "hello";
}
```text
````

Alih-alih blok yang diberi tag dengan benar seperti:

````markdown theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**Solusi:**

1. **Minta Claude untuk menambahkan tag bahasa**: minta "Add appropriate language tags to all code blocks in this markdown file."

2. **Gunakan post-processing hooks**: atur hooks pemformatan otomatis untuk mendeteksi dan menambahkan tag bahasa yang hilang. Lihat [Auto-format code after edits](/id/hooks-guide#auto-format-code-after-edits) untuk contoh hook PostToolUse pemformatan.

3. **Verifikasi manual**: setelah menghasilkan file markdown, tinjau untuk pemformatan blok kode yang tepat dan minta koreksi jika diperlukan.

### Inconsistent spacing and formatting

Jika markdown yang dihasilkan memiliki baris kosong berlebihan atau spasi yang tidak konsisten:

**Solusi:**

1. **Minta koreksi pemformatan**: minta Claude untuk "Fix spacing and formatting issues in this markdown file."

2. **Gunakan alat pemformatan**: atur hooks untuk menjalankan formatter markdown seperti `prettier` atau skrip pemformatan kustom pada file markdown yang dihasilkan.

3. **Tentukan preferensi pemformatan**: sertakan persyaratan pemformatan dalam prompt Anda atau file [memory](/id/memory) proyek.

### Reduce markdown formatting issues

Untuk meminimalkan masalah pemformatan:

* **Jadilah eksplisit dalam permintaan**: minta "properly formatted markdown with language-tagged code blocks"
* **Gunakan konvensi proyek**: dokumentasikan gaya markdown pilihan Anda di [`CLAUDE.md`](/id/memory)
* **Atur validation hooks**: gunakan post-processing hooks untuk secara otomatis memverifikasi dan memperbaiki masalah pemformatan umum

## Get more help

Jika Anda mengalami masalah yang tidak tercakup di sini:

1. Gunakan perintah `/bug` dalam Claude Code untuk melaporkan masalah langsung ke Anthropic
2. Periksa [GitHub repository](https://github.com/anthropics/claude-code) untuk masalah yang diketahui
3. Jalankan `/doctor` untuk mendiagnosis masalah. Ini memeriksa:
   * Tipe instalasi, versi, dan fungsionalitas pencarian
   * Status auto-update dan versi yang tersedia
   * File pengaturan yang tidak valid (JSON yang salah bentuk, tipe yang tidak benar)
   * Kesalahan konfigurasi MCP server
   * Masalah konfigurasi pintasan keyboard
   * Peringatan penggunaan konteks (file CLAUDE.md besar, penggunaan token MCP tinggi, aturan izin yang tidak dapat dijangkau)
   * Plugin dan kesalahan pemuatan agen
4. Tanyakan Claude secara langsung tentang kemampuan dan fiturnya - Claude memiliki akses bawaan ke dokumentasinya
