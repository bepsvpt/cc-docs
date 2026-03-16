> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Panduan Cepat

> Selamat datang di Claude Code!

Panduan cepat ini akan membuat Anda menggunakan bantuan coding bertenaga AI dalam beberapa menit. Di akhir panduan, Anda akan memahami cara menggunakan Claude Code untuk tugas-tugas pengembangan umum.

## Sebelum Anda memulai

Pastikan Anda memiliki:

* Terminal atau command prompt yang terbuka
  * Jika Anda belum pernah menggunakan terminal sebelumnya, lihat [panduan terminal](/id/terminal-guide)
* Proyek kode untuk dikerjakan
* [Langganan Claude](https://claude.com/pricing) (Pro, Max, Teams, atau Enterprise), akun [Claude Console](https://console.anthropic.com/), atau akses melalui [penyedia cloud yang didukung](/id/third-party-integrations)

<Note>
  Panduan ini mencakup CLI terminal. Claude Code juga tersedia di [web](https://claude.ai/code), sebagai [aplikasi desktop](/id/desktop), di [VS Code](/id/vs-code) dan [IDE JetBrains](/id/jetbrains), di [Slack](/id/slack), dan di CI/CD dengan [GitHub Actions](/id/github-actions) dan [GitLab](/id/gitlab-ci-cd). Lihat [semua antarmuka](/id/overview#use-claude-code-everywhere).
</Note>

## Langkah 1: Instal Claude Code

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

## Langkah 2: Masuk ke akun Anda

Claude Code memerlukan akun untuk digunakan. Ketika Anda memulai sesi interaktif dengan perintah `claude`, Anda perlu masuk:

```bash  theme={null}
claude
# Anda akan diminta untuk masuk pada penggunaan pertama
```

```bash  theme={null}
/login
# Ikuti petunjuk untuk masuk dengan akun Anda
```

Anda dapat masuk menggunakan salah satu jenis akun ini:

* [Claude Pro, Max, Teams, atau Enterprise](https://claude.com/pricing) (direkomendasikan)
* [Claude Console](https://console.anthropic.com/) (akses API dengan kredit prabayar). Pada login pertama, workspace "Claude Code" secara otomatis dibuat di Console untuk pelacakan biaya terpusat.
* [Amazon Bedrock, Google Vertex AI, atau Microsoft Foundry](/id/third-party-integrations) (penyedia cloud enterprise)

Setelah masuk, kredensial Anda disimpan dan Anda tidak perlu masuk lagi. Untuk beralih akun nanti, gunakan perintah `/login`.

## Langkah 3: Mulai sesi pertama Anda

Buka terminal Anda di direktori proyek mana pun dan mulai Claude Code:

```bash  theme={null}
cd /path/to/your/project
claude
```

Anda akan melihat layar sambutan Claude Code dengan informasi sesi, percakapan terbaru, dan pembaruan terbaru. Ketik `/help` untuk perintah yang tersedia atau `/resume` untuk melanjutkan percakapan sebelumnya.

<Tip>
  Setelah masuk (Langkah 2), kredensial Anda disimpan di sistem Anda. Pelajari lebih lanjut di [Manajemen Kredensial](/id/authentication#credential-management).
</Tip>

## Langkah 4: Ajukan pertanyaan pertama Anda

Mari kita mulai dengan memahami basis kode Anda. Coba salah satu perintah ini:

```text  theme={null}
apa yang dilakukan proyek ini?
```

Claude akan menganalisis file Anda dan memberikan ringkasan. Anda juga dapat mengajukan pertanyaan yang lebih spesifik:

```text  theme={null}
teknologi apa yang digunakan proyek ini?
```

```text  theme={null}
di mana titik masuk utama?
```

```text  theme={null}
jelaskan struktur folder
```

Anda juga dapat bertanya kepada Claude tentang kemampuannya sendiri:

```text  theme={null}
apa yang dapat dilakukan Claude Code?
```

```text  theme={null}
bagaimana cara membuat skills kustom di Claude Code?
```

```text  theme={null}
bisakah Claude Code bekerja dengan Docker?
```

<Note>
  Claude Code membaca file proyek Anda sesuai kebutuhan. Anda tidak perlu menambahkan konteks secara manual.
</Note>

## Langkah 5: Buat perubahan kode pertama Anda

Sekarang mari buat Claude Code melakukan beberapa coding sebenarnya. Coba tugas sederhana:

```text  theme={null}
tambahkan fungsi hello world ke file utama
```

Claude Code akan:

1. Menemukan file yang sesuai
2. Menampilkan perubahan yang diusulkan
3. Meminta persetujuan Anda
4. Membuat edit

<Note>
  Claude Code selalu meminta izin sebelum memodifikasi file. Anda dapat menyetujui perubahan individual atau mengaktifkan mode "Terima semua" untuk sesi.
</Note>

## Langkah 6: Gunakan Git dengan Claude Code

Claude Code membuat operasi Git menjadi percakapan:

```text  theme={null}
file apa yang telah saya ubah?
```

```text  theme={null}
commit perubahan saya dengan pesan deskriptif
```

Anda juga dapat meminta operasi Git yang lebih kompleks:

```text  theme={null}
buat cabang baru bernama feature/quickstart
```

```text  theme={null}
tunjukkan 5 commit terakhir saya
```

```text  theme={null}
bantu saya menyelesaikan konflik merge
```

## Langkah 7: Perbaiki bug atau tambahkan fitur

Claude mahir dalam debugging dan implementasi fitur.

Jelaskan apa yang Anda inginkan dalam bahasa alami:

```text  theme={null}
tambahkan validasi input ke formulir pendaftaran pengguna
```

Atau perbaiki masalah yang ada:

```text  theme={null}
ada bug di mana pengguna dapat mengirimkan formulir kosong - perbaiki
```

Claude Code akan:

* Menemukan kode yang relevan
* Memahami konteksnya
* Menerapkan solusi
* Menjalankan tes jika tersedia

## Langkah 8: Coba alur kerja umum lainnya

Ada beberapa cara untuk bekerja dengan Claude:

**Refactor kode**

```text  theme={null}
refactor modul autentikasi untuk menggunakan async/await alih-alih callbacks
```

**Tulis tes**

```text  theme={null}
tulis unit test untuk fungsi kalkulator
```

**Perbarui dokumentasi**

```text  theme={null}
perbarui README dengan instruksi instalasi
```

**Tinjauan kode**

```text  theme={null}
tinjau perubahan saya dan sarankan perbaikan
```

<Tip>
  Berbicara dengan Claude seperti Anda berbicara dengan rekan kerja yang membantu. Jelaskan apa yang ingin Anda capai, dan itu akan membantu Anda sampai ke sana.
</Tip>

## Perintah penting

Berikut adalah perintah paling penting untuk penggunaan sehari-hari:

| Perintah            | Apa yang dilakukannya                              | Contoh                              |
| ------------------- | -------------------------------------------------- | ----------------------------------- |
| `claude`            | Mulai mode interaktif                              | `claude`                            |
| `claude "task"`     | Jalankan tugas satu kali                           | `claude "perbaiki kesalahan build"` |
| `claude -p "query"` | Jalankan kueri sekali jalan, lalu keluar           | `claude -p "jelaskan fungsi ini"`   |
| `claude -c`         | Lanjutkan percakapan terbaru di direktori saat ini | `claude -c`                         |
| `claude -r`         | Lanjutkan percakapan sebelumnya                    | `claude -r`                         |
| `claude commit`     | Buat commit Git                                    | `claude commit`                     |
| `/clear`            | Hapus riwayat percakapan                           | `/clear`                            |
| `/help`             | Tampilkan perintah yang tersedia                   | `/help`                             |
| `exit` atau Ctrl+C  | Keluar dari Claude Code                            | `exit`                              |

Lihat [referensi CLI](/id/cli-reference) untuk daftar lengkap perintah.

## Tips pro untuk pemula

Untuk informasi lebih lanjut, lihat [praktik terbaik](/id/best-practices) dan [alur kerja umum](/id/common-workflows).

<AccordionGroup>
  <Accordion title="Jadilah spesifik dengan permintaan Anda">
    Alih-alih: "perbaiki bug"

    Coba: "perbaiki bug login di mana pengguna melihat layar kosong setelah memasukkan kredensial yang salah"
  </Accordion>

  <Accordion title="Gunakan instruksi langkah demi langkah">
    Pecah tugas kompleks menjadi langkah-langkah:

    ```text  theme={null}
    1. buat tabel database baru untuk profil pengguna
    2. buat endpoint API untuk mendapatkan dan memperbarui profil pengguna
    3. bangun halaman web yang memungkinkan pengguna melihat dan mengedit informasi mereka
    ```
  </Accordion>

  <Accordion title="Biarkan Claude menjelajahi terlebih dahulu">
    Sebelum membuat perubahan, biarkan Claude memahami kode Anda:

    ```text  theme={null}
    analisis skema database
    ```

    ```text  theme={null}
    bangun dasbor yang menampilkan produk yang paling sering dikembalikan oleh pelanggan Inggris kami
    ```
  </Accordion>

  <Accordion title="Hemat waktu dengan pintasan">
    * Tekan `?` untuk melihat semua pintasan keyboard yang tersedia
    * Gunakan Tab untuk penyelesaian perintah
    * Tekan ↑ untuk riwayat perintah
    * Ketik `/` untuk melihat semua perintah dan skills
  </Accordion>
</AccordionGroup>

## Apa selanjutnya?

Sekarang yang Anda telah mempelajari dasar-dasarnya, jelajahi fitur-fitur yang lebih canggih:

<CardGroup cols={2}>
  <Card title="Cara kerja Claude Code" icon="microchip" href="/id/how-claude-code-works">
    Pahami loop agentic, alat bawaan, dan cara Claude Code berinteraksi dengan proyek Anda
  </Card>

  <Card title="Praktik terbaik" icon="star" href="/id/best-practices">
    Dapatkan hasil yang lebih baik dengan prompting yang efektif dan pengaturan proyek
  </Card>

  <Card title="Alur kerja umum" icon="graduation-cap" href="/id/common-workflows">
    Panduan langkah demi langkah untuk tugas-tugas umum
  </Card>

  <Card title="Perluas Claude Code" icon="puzzle-piece" href="/id/features-overview">
    Sesuaikan dengan CLAUDE.md, skills, hooks, MCP, dan lainnya
  </Card>
</CardGroup>

## Mendapatkan bantuan

* **Di Claude Code**: Ketik `/help` atau tanya "bagaimana cara saya..."
* **Dokumentasi**: Anda di sini! Jelajahi panduan lainnya
* **Komunitas**: Bergabunglah dengan [Discord](https://www.anthropic.com/discord) kami untuk tips dan dukungan
