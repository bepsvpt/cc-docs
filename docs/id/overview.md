> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ikhtisar Claude Code

> Claude Code adalah alat pengkodean agentic yang membaca basis kode Anda, mengedit file, menjalankan perintah, dan terintegrasi dengan alat pengembangan Anda. Tersedia di terminal, IDE, aplikasi desktop, dan browser Anda.

Claude Code adalah asisten pengkodean bertenaga AI yang membantu Anda membangun fitur, memperbaiki bug, dan mengotomatisasi tugas pengembangan. Ini memahami seluruh basis kode Anda dan dapat bekerja di berbagai file dan alat untuk menyelesaikan pekerjaan.

## Memulai

Pilih lingkungan Anda untuk memulai. Sebagian besar permukaan memerlukan [langganan Claude](https://claude.com/pricing) atau akun [Konsol Anthropic](https://console.anthropic.com/). Terminal CLI dan VS Code juga mendukung [penyedia pihak ketiga](/id/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    CLI lengkap untuk bekerja dengan Claude Code langsung di terminal Anda. Edit file, jalankan perintah, dan kelola seluruh proyek Anda dari baris perintah.

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

    Kemudian mulai Claude Code di proyek apa pun:

    ```bash  theme={null}
    cd your-project
    claude
    ```

    Anda akan diminta untuk masuk pada penggunaan pertama. Itu saja! [Lanjutkan dengan Quickstart →](/id/quickstart)

    <Tip>
      Lihat [pengaturan lanjutan](/id/setup) untuk opsi instalasi, pembaruan manual, atau instruksi penghapusan. Kunjungi [pemecahan masalah](/id/troubleshooting) jika Anda mengalami masalah.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    Ekstensi VS Code menyediakan diff inline, @-mentions, tinjauan rencana, dan riwayat percakapan langsung di editor Anda.

    * [Instal untuk VS Code](vscode:extension/anthropic.claude-code)
    * [Instal untuk Cursor](cursor:extension/anthropic.claude-code)

    Atau cari "Claude Code" di tampilan Ekstensi (`Cmd+Shift+X` di Mac, `Ctrl+Shift+X` di Windows/Linux). Setelah menginstal, buka Palet Perintah (`Cmd+Shift+P` / `Ctrl+Shift+P`), ketik "Claude Code", dan pilih **Buka di Tab Baru**.

    [Mulai dengan VS Code →](/id/vs-code#get-started)
  </Tab>

  <Tab title="Aplikasi desktop">
    Aplikasi mandiri untuk menjalankan Claude Code di luar IDE atau terminal Anda. Tinjau diff secara visual, jalankan beberapa sesi berdampingan, jadwalkan tugas berulang, dan mulai sesi cloud.

    Unduh dan instal:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel dan Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (hanya sesi jarak jauh)

    Setelah menginstal, luncurkan Claude, masuk, dan klik tab **Code** untuk mulai pengkodean. [Langganan berbayar](https://claude.com/pricing) diperlukan.

    [Pelajari lebih lanjut tentang aplikasi desktop →](/id/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Jalankan Claude Code di browser Anda tanpa pengaturan lokal. Mulai tugas yang berjalan lama dan periksa kembali saat selesai, bekerja pada repo yang tidak Anda miliki secara lokal, atau jalankan beberapa tugas secara paralel. Tersedia di browser desktop dan aplikasi Claude iOS.

    Mulai pengkodean di [claude.ai/code](https://claude.ai/code).

    [Mulai di web →](/id/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    Plugin untuk IntelliJ IDEA, PyCharm, WebStorm, dan IDE JetBrains lainnya dengan tampilan diff interaktif dan berbagi konteks seleksi.

    Instal [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) dari Marketplace JetBrains dan mulai ulang IDE Anda.

    [Mulai dengan JetBrains →](/id/jetbrains)
  </Tab>
</Tabs>

## Apa yang dapat Anda lakukan

Berikut adalah beberapa cara Anda dapat menggunakan Claude Code:

<AccordionGroup>
  <Accordion title="Otomatisasi pekerjaan yang terus Anda tunda" icon="wand-magic-sparkles">
    Claude Code menangani tugas-tugas membosankan yang menghabiskan hari Anda: menulis tes untuk kode yang tidak diuji, memperbaiki kesalahan lint di seluruh proyek, menyelesaikan konflik penggabungan, memperbarui dependensi, dan menulis catatan rilis.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Bangun fitur dan perbaiki bug" icon="hammer">
    Jelaskan apa yang Anda inginkan dalam bahasa biasa. Claude Code merencanakan pendekatan, menulis kode di berbagai file, dan memverifikasi bahwa itu berfungsi.

    Untuk bug, tempel pesan kesalahan atau jelaskan gejalanya. Claude Code melacak masalah melalui basis kode Anda, mengidentifikasi akar penyebabnya, dan menerapkan perbaikan. Lihat [alur kerja umum](/id/common-workflows) untuk contoh lebih lanjut.
  </Accordion>

  <Accordion title="Buat commit dan pull request" icon="code-branch">
    Claude Code bekerja langsung dengan git. Ini menampilkan perubahan, menulis pesan commit, membuat cabang, dan membuka pull request.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    Di CI, Anda dapat mengotomatisasi tinjauan kode dan triase masalah dengan [GitHub Actions](/id/github-actions) atau [GitLab CI/CD](/id/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Hubungkan alat Anda dengan MCP" icon="plug">
    [Model Context Protocol (MCP)](/id/mcp) adalah standar terbuka untuk menghubungkan alat AI ke sumber data eksternal. Dengan MCP, Claude Code dapat membaca dokumen desain Anda di Google Drive, memperbarui tiket di Jira, menarik data dari Slack, atau menggunakan alat kustom Anda sendiri.
  </Accordion>

  <Accordion title="Sesuaikan dengan instruksi, skills, dan hooks" icon="sliders">
    [`CLAUDE.md`](/id/memory) adalah file markdown yang Anda tambahkan ke root proyek Anda yang dibaca Claude Code di awal setiap sesi. Gunakan untuk menetapkan standar pengkodean, keputusan arsitektur, perpustakaan pilihan, dan daftar periksa tinjauan. Claude juga membangun [memori otomatis](/id/memory#auto-memory) saat bekerja, menyimpan pembelajaran seperti perintah build dan wawasan debugging di seluruh sesi tanpa Anda menulis apa pun.

    Buat [perintah kustom](/id/skills) untuk mengemas alur kerja yang dapat diulang yang dapat dibagikan tim Anda, seperti `/review-pr` atau `/deploy-staging`.

    [Hooks](/id/hooks) memungkinkan Anda menjalankan perintah shell sebelum atau sesudah tindakan Claude Code, seperti pemformatan otomatis setelah setiap pengeditan file atau menjalankan lint sebelum commit.
  </Accordion>

  <Accordion title="Jalankan tim agen dan bangun agen kustom" icon="users">
    Spawn [beberapa agen Claude Code](/id/sub-agents) yang bekerja pada bagian berbeda dari tugas secara bersamaan. Agen utama mengoordinasikan pekerjaan, menetapkan subtask, dan menggabungkan hasil.

    Untuk alur kerja yang sepenuhnya kustom, [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) memungkinkan Anda membangun agen Anda sendiri yang didukung oleh alat dan kemampuan Claude Code, dengan kontrol penuh atas orkestrasi, akses alat, dan izin.
  </Accordion>

  <Accordion title="Pipa, skrip, dan otomatisasi dengan CLI" icon="terminal">
    Claude Code dapat dikomposisi dan mengikuti filosofi Unix. Pipa log ke dalamnya, jalankan di CI, atau rantai dengan alat lain:

    ```bash  theme={null}
    # Monitor logs and get alerted
    tail -f app.log | claude -p "Slack me if you see any anomalies"

    # Automate translations in CI
    claude -p "translate new strings into French and raise a PR for review"

    # Bulk operations across files
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    Lihat [referensi CLI](/id/cli-reference) untuk set lengkap perintah dan flag.
  </Accordion>

  <Accordion title="Bekerja dari mana saja" icon="globe">
    Sesi tidak terikat pada satu permukaan. Pindahkan pekerjaan antar lingkungan saat konteks Anda berubah:

    * Tinggalkan meja Anda dan terus bekerja dari ponsel Anda atau browser apa pun dengan [Remote Control](/id/remote-control)
    * Mulai tugas yang berjalan lama di [web](/id/claude-code-on-the-web) atau [aplikasi iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684), kemudian tariknya ke terminal Anda dengan `/teleport`
    * Serahkan sesi terminal ke [aplikasi Desktop](/id/desktop) dengan `/desktop` untuk tinjauan diff visual
    * Rute tugas dari obrolan tim: sebutkan `@Claude` di [Slack](/id/slack) dengan laporan bug dan dapatkan pull request kembali
  </Accordion>
</AccordionGroup>

## Gunakan Claude Code di mana saja

Setiap permukaan terhubung ke mesin Claude Code yang mendasar yang sama, jadi file CLAUDE.md, pengaturan, dan server MCP Anda bekerja di semua permukaan.

Selain lingkungan [Terminal](/id/quickstart), [VS Code](/id/vs-code), [JetBrains](/id/jetbrains), [Desktop](/id/desktop), dan [Web](/id/claude-code-on-the-web) di atas, Claude Code terintegrasi dengan alur kerja CI/CD, obrolan, dan browser:

| Saya ingin...                                             | Opsi terbaik                                                                                                              |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Lanjutkan sesi lokal dari ponsel atau perangkat lain saya | [Remote Control](/id/remote-control)                                                                                      |
| Mulai tugas secara lokal, lanjutkan di mobile             | [Web](/id/claude-code-on-the-web) atau [aplikasi Claude iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Otomatisasi tinjauan PR dan triase masalah                | [GitHub Actions](/id/github-actions) atau [GitLab CI/CD](/id/gitlab-ci-cd)                                                |
| Dapatkan tinjauan kode otomatis di setiap PR              | [GitHub Code Review](/id/code-review)                                                                                     |
| Rute laporan bug dari Slack ke pull request               | [Slack](/id/slack)                                                                                                        |
| Debug aplikasi web langsung                               | [Chrome](/id/chrome)                                                                                                      |
| Bangun agen kustom untuk alur kerja Anda sendiri          | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                       |

## Langkah berikutnya

Setelah Anda menginstal Claude Code, panduan ini membantu Anda menggali lebih dalam.

* [Quickstart](/id/quickstart): berjalan melalui tugas nyata pertama Anda, dari menjelajahi basis kode hingga melakukan perbaikan
* [Simpan instruksi dan memori](/id/memory): berikan Claude instruksi persisten dengan file CLAUDE.md dan memori otomatis
* [Alur kerja umum](/id/common-workflows) dan [praktik terbaik](/id/best-practices): pola untuk mendapatkan hasil maksimal dari Claude Code
* [Pengaturan](/id/settings): sesuaikan Claude Code untuk alur kerja Anda
* [Pemecahan masalah](/id/troubleshooting): solusi untuk masalah umum
* [code.claude.com](https://code.claude.com/): demo, harga, dan detail produk
