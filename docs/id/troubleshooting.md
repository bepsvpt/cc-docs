> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting

> Perbaiki penggunaan CPU atau memori yang tinggi, hang, thrashing auto-compact, dan masalah pencarian di Claude Code, dan temukan halaman yang tepat untuk masalah lainnya.

Halaman ini mencakup masalah kinerja, stabilitas, dan pencarian setelah Claude Code berjalan. Untuk masalah lainnya, mulai dengan halaman yang sesuai dengan tempat Anda terjebak:

| Gejala                                                                                                   | Buka                                                                                     |
| :------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `command not found`, instalasi gagal, masalah PATH, `EACCES`, kesalahan TLS                              | [Troubleshoot installation and login](/id/troubleshoot-install)                          |
| Loop login, kesalahan OAuth, `403 Forbidden`, "organization disabled", kredensial Bedrock/Vertex/Foundry | [Troubleshoot installation and login](/id/troubleshoot-install#login-and-authentication) |
| Pengaturan tidak diterapkan, hooks tidak berfungsi, server MCP tidak dimuat                              | [Debug your configuration](/id/debug-your-config)                                        |
| `API Error: 5xx`, `529 Overloaded`, `429`, kesalahan validasi permintaan                                 | [Error reference](/id/errors)                                                            |
| `model not found` atau `you may not have access to it`                                                   | [Error reference](/id/errors#theres-an-issue-with-the-selected-model)                    |
| Ekstensi VS Code tidak terhubung atau tidak mendeteksi Claude                                            | [VS Code integration](/id/vs-code#fix-common-issues)                                     |
| Plugin JetBrains atau IDE tidak terdeteksi                                                               | [JetBrains integration](/id/jetbrains#troubleshooting)                                   |
| CPU atau memori tinggi, respons lambat, hang, pencarian tidak menemukan file                             | [Performance and stability](#performance-and-stability) di bawah                         |

Jika Anda tidak yakin mana yang berlaku, jalankan `/doctor` di dalam Claude Code untuk pemeriksaan otomatis instalasi, pengaturan, server MCP, dan penggunaan konteks Anda. Jika `claude` tidak akan memulai sama sekali, jalankan `claude doctor` dari shell Anda sebagai gantinya.

## Performance and stability

Bagian-bagian ini mencakup masalah yang terkait dengan penggunaan sumber daya, responsivitas, dan perilaku pencarian.

### High CPU or memory usage

Claude Code dirancang untuk bekerja dengan sebagian besar lingkungan pengembangan, tetapi dapat mengonsumsi sumber daya signifikan saat memproses codebase besar. Jika Anda mengalami masalah kinerja:

1. Gunakan `/compact` secara teratur untuk mengurangi ukuran konteks
2. Tutup dan mulai ulang Claude Code di antara tugas-tugas besar
3. Pertimbangkan menambahkan direktori build besar ke file `.gitignore` Anda

Jika penggunaan memori tetap tinggi setelah langkah-langkah ini, jalankan `/heapdump` untuk menulis snapshot heap JavaScript dan rincian memori ke `~/Desktop`. Di Linux tanpa folder Desktop, file ditulis ke direktori home Anda.

Rincian menunjukkan resident set size, JS heap, array buffers, dan memori native yang tidak terhitung, yang membantu mengidentifikasi apakah pertumbuhan ada di objek JavaScript atau di kode native. Untuk memeriksa retainers, buka file `.heapsnapshot` di Chrome DevTools di bawah Memory → Load. Lampirkan kedua file saat melaporkan masalah memori di [GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compaction stops with a thrashing error

Jika Anda melihat `Autocompact is thrashing: the context refilled to the limit...`, automatic compaction berhasil tetapi file atau output alat segera mengisi ulang jendela konteks beberapa kali berturut-turut. Claude Code berhenti mencoba ulang untuk menghindari pemborosan panggilan API pada loop yang tidak membuat kemajuan.

Untuk pulih:

1. Minta Claude membaca file yang terlalu besar dalam potongan yang lebih kecil, seperti rentang baris tertentu atau fungsi, alih-alih seluruh file
2. Jalankan `/compact` dengan fokus yang menjatuhkan output besar, misalnya `/compact keep only the plan and the diff`
3. Pindahkan pekerjaan file besar ke [subagent](/id/sub-agents) sehingga berjalan di jendela konteks terpisah
4. Jalankan `/clear` jika percakapan sebelumnya tidak lagi diperlukan

### Command hangs or freezes

Jika Claude Code tampak tidak responsif:

1. Tekan Ctrl+C untuk mencoba membatalkan operasi saat ini
2. Jika tidak responsif, Anda mungkin perlu menutup terminal dan memulai ulang

Memulai ulang tidak kehilangan percakapan Anda. Jalankan `claude --resume` di direktori yang sama untuk melanjutkan sesi.

### Search and discovery issues

Jika Search tool, `@file` mentions, custom agents, atau custom skills tidak menemukan file, binary `ripgrep` bundel mungkin tidak berjalan di sistem Anda. Instal paket `ripgrep` platform Anda dan beri tahu Claude Code untuk menggunakannya sebagai gantinya:

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

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

## Get more help

Jika Anda mengalami masalah yang tidak tercakup di sini:

1. Jalankan `/doctor` untuk memeriksa kesehatan instalasi, validitas pengaturan, konfigurasi MCP, dan penggunaan konteks dalam satu kali jalan
2. Gunakan perintah `/feedback` dalam Claude Code untuk melaporkan masalah langsung ke Anthropic
3. Periksa [GitHub repository](https://github.com/anthropics/claude-code) untuk masalah yang diketahui
4. Tanyakan Claude secara langsung tentang kemampuan dan fiturnya. Claude memiliki akses bawaan ke dokumentasinya.
