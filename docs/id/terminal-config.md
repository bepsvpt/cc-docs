> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi terminal Anda untuk Claude Code

> Perbaiki Shift+Enter untuk baris baru, dapatkan bel terminal ketika Claude selesai, konfigurasi tmux, cocokkan tema warna, dan aktifkan mode Vim di CLI Claude Code.

Claude Code bekerja di terminal apa pun tanpa konfigurasi. Halaman ini untuk ketika sesuatu yang spesifik tidak berperilaku seperti yang Anda harapkan. Temukan gejala Anda di bawah. Jika semuanya sudah terasa benar, Anda tidak memerlukan halaman ini.

* [Shift+Enter mengirim alih-alih menyisipkan baris baru](#enter-multiline-prompts)
* [Pintasan tombol Option tidak melakukan apa pun di macOS](#enable-option-key-shortcuts-on-macos)
* [Tidak ada suara atau peringatan ketika Claude selesai](#get-a-terminal-bell-or-notification)
* [Anda menjalankan Claude Code di dalam tmux](#configure-tmux)
* [Tampilan berkedip atau scrollback melompat](#switch-to-fullscreen-rendering)
* [Anda ingin kunci Vim di prompt](#edit-prompts-with-vim-keybindings)

Halaman ini tentang membuat terminal Anda mengirimkan sinyal yang tepat ke Claude Code. Untuk mengubah kunci mana yang Claude Code sendiri merespons, lihat [keybindings](/id/keybindings) sebagai gantinya.

## Masukkan prompt multiline

Menekan Enter mengirimkan pesan Anda. Untuk menambahkan jeda baris tanpa mengirimkan, tekan Ctrl+J, atau ketik `\` dan kemudian tekan Enter. Keduanya bekerja di setiap terminal tanpa setup.

Di sebagian besar terminal Anda juga dapat menekan Shift+Enter, tetapi dukungan bervariasi menurut emulator terminal:

| Terminal                                                                            | Shift+Enter untuk baris baru                           |
| :---------------------------------------------------------------------------------- | :----------------------------------------------------- |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                               | Bekerja tanpa setup                                    |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                           | Jalankan `/terminal-setup` sekali                      |
| Windows Terminal, gnome-terminal, JetBrains IDEs seperti PyCharm dan Android Studio | Tidak tersedia; gunakan Ctrl+J atau `\` kemudian Enter |

Untuk VS Code, Cursor, Windsurf, Alacritty, dan Zed, `/terminal-setup` menulis Shift+Enter dan pintasan keyboard lainnya ke dalam file konfigurasi terminal. Di VS Code, Cursor, dan Windsurf, ini juga menetapkan `terminal.integrated.mouseWheelScrollSensitivity` dalam pengaturan editor untuk scrolling yang lebih halus dalam [mode fullscreen](/id/fullscreen). Binding dan pengaturan yang ada dibiarkan tetap ada; jika Anda melihat pesan seperti `VSCode terminal Shift+Enter key binding already configured`, tidak ada perubahan yang dilakukan. Jalankan `/terminal-setup` langsung di terminal host daripada di dalam tmux atau screen, karena perlu menulis ke konfigurasi terminal host.

Jika Anda menjalankan di dalam tmux, Shift+Enter juga memerlukan [konfigurasi tmux di bawah](#configure-tmux) bahkan ketika terminal luar mendukungnya.

Untuk mengikat baris baru ke kunci yang berbeda, atau untuk menukar perilaku sehingga Enter menyisipkan baris baru dan Shift+Enter mengirim, petakan tindakan `chat:newline` dan `chat:submit` di [file pintasan keyboard](/id/keybindings) Anda.

## Aktifkan pintasan tombol Option di macOS

Beberapa pintasan Claude Code menggunakan tombol Option, seperti Option+Enter untuk baris baru atau Option+P untuk beralih model. Di macOS, sebagian besar terminal tidak mengirimkan Option sebagai pengubah secara default, jadi pintasan ini tidak melakukan apa pun sampai Anda mengaktifkannya. Pengaturan terminal untuk ini biasanya berlabel "Use Option as Meta Key"; Meta adalah nama Unix historis untuk kunci yang sekarang berlabel Option atau Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Buka Settings → Profiles → Keyboard dan centang "Use Option as Meta Key".

    Jika Anda menerima prompt first-run Claude Code yang menawarkan "Option+Enter untuk baris baru dan visual bell", ini sudah dilakukan. Prompt itu menjalankan `/terminal-setup` untuk Anda, yang mengaktifkan Option sebagai Meta dan mengalihkan audio bell ke flash layar visual di profil Apple Terminal Anda.
  </Tab>

  <Tab title="iTerm2">
    Buka Settings → Profiles → Keys → General dan atur Left Option key dan Right Option key ke "Esc+".
  </Tab>

  <Tab title="VS Code">
    Tambahkan `"terminal.integrated.macOptionIsMeta": true` ke pengaturan VS Code Anda.
  </Tab>
</Tabs>

Untuk Ghostty, Kitty, dan terminal lainnya, cari pengaturan Option-as-Alt atau Option-as-Meta di file konfigurasi terminal.

## Dapatkan bel terminal atau notifikasi

Ketika Claude menyelesaikan tugas atau berhenti untuk prompt izin, ia mengirimkan acara notifikasi. Menampilkan ini sebagai bel terminal atau notifikasi desktop memungkinkan Anda beralih ke pekerjaan lain saat tugas panjang berjalan.

Claude Code mengirimkan notifikasi desktop hanya di Ghostty, Kitty, dan iTerm2; setiap terminal lain memerlukan [hook Notification](#play-a-sound-with-a-notification-hook) sebagai gantinya. Notifikasi juga mencapai mesin lokal Anda melalui SSH, jadi sesi jarak jauh masih dapat memperingatkan Anda. Ghostty dan Kitty meneruskannya ke pusat notifikasi OS Anda tanpa setup lebih lanjut. iTerm2 memerlukan Anda untuk mengaktifkan penerusan:

<Steps>
  <Step title="Buka pengaturan notifikasi iTerm2">
    Buka Settings → Profiles → Terminal.
  </Step>

  <Step title="Aktifkan peringatan">
    Centang "Notification Center Alerts", kemudian klik "Filter Alerts" dan aktifkan "Send escape sequence-generated alerts".
  </Step>
</Steps>

Jika notifikasi masih tidak muncul, konfirmasi bahwa aplikasi terminal Anda memiliki izin notifikasi di pengaturan OS Anda, dan jika Anda menjalankan di dalam tmux, [aktifkan passthrough](#configure-tmux).

### Putar suara dengan hook Notification

Di terminal apa pun Anda dapat mengonfigurasi [hook Notification](/id/hooks-guide#get-notified-when-claude-needs-input) untuk memutar suara atau menjalankan perintah khusus ketika Claude memerlukan perhatian Anda. Hook berjalan bersama notifikasi desktop daripada menggantinya. Terminal seperti Warp atau Apple Terminal mengandalkan hook saja karena Claude Code tidak mengirimkan mereka notifikasi desktop.

Contoh di bawah memutar suara sistem di macOS. Panduan tertaut memiliki perintah notifikasi desktop untuk macOS, Linux, dan Windows.

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Konfigurasi tmux

Ketika Claude Code berjalan di dalam tmux, dua hal rusak secara default: Shift+Enter mengirim alih-alih menyisipkan baris baru, dan notifikasi desktop dan [progress bar](/id/settings#available-settings) tidak pernah mencapai terminal luar. Tambahkan baris-baris ini ke `~/.tmux.conf`, kemudian jalankan `tmux source-file ~/.tmux.conf` untuk menerapkannya ke server yang berjalan:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

Baris `allow-passthrough` memungkinkan notifikasi dan pembaruan kemajuan mencapai iTerm2, Ghostty, atau Kitty alih-alih ditelan oleh tmux. Baris `extended-keys` memungkinkan tmux membedakan Shift+Enter dari Enter biasa sehingga pintasan baris baru bekerja.

## Cocokkan tema warna

Gunakan perintah `/theme`, atau pemilih tema di `/config`, untuk memilih tema Claude Code yang cocok dengan terminal Anda. Memilih opsi auto mendeteksi latar belakang terminal Anda yang terang atau gelap, jadi tema mengikuti perubahan penampilan OS kapan pun terminal Anda melakukannya. Claude Code tidak mengontrol skema warna terminal itu sendiri, yang diatur oleh aplikasi terminal.

Untuk menyesuaikan apa yang muncul di bagian bawah antarmuka, konfigurasikan [baris status khusus](/id/statusline) yang menampilkan model saat ini, direktori kerja, cabang git, atau konteks lainnya.

### Buat tema khusus

<Note>
  Tema khusus memerlukan Claude Code v2.1.118 atau lebih baru.
</Note>

Selain preset bawaan, `/theme` mencantumkan tema khusus apa pun yang telah Anda tentukan dan tema apa pun yang disumbangkan oleh [plugins](/id/plugins-reference#themes) yang terinstal. Pilih **Tema khusus baru…** di akhir daftar untuk membuat satu secara interaktif: Anda memberi nama tema, kemudian memilih token warna individual untuk ditimpa. Tekan `Ctrl+E` saat tema khusus disorot untuk mengeditnya.

Setiap tema khusus adalah file JSON di `~/.claude/themes/`. Nama file tanpa ekstensi `.json` adalah slug tema, dan memilih tema menyimpan `custom:<slug>` sebagai preferensi tema Anda. File memiliki tiga bidang opsional:

| Bidang      | Tipe   | Deskripsi                                                                                                                                              |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | string | Label tampilan yang ditampilkan di `/theme`. Defaultnya adalah slug nama file                                                                          |
| `base`      | string | Preset bawaan yang dimulai dari tema: `dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi`, atau `light-ansi`. Defaultnya adalah `dark` |
| `overrides` | object | Peta nama token warna ke nilai warna. Token yang tidak tercantum di sini jatuh kembali ke preset dasar                                                 |

Nilai warna menerima `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, atau `ansi:<name>` di mana `<name>` adalah salah satu dari 16 nama warna ANSI standar seperti `red` atau `cyanBright`. Token yang tidak dikenal dan nilai warna yang tidak valid diabaikan, jadi kesalahan ketik tidak dapat merusak rendering.

Contoh berikut mendefinisikan tema yang mempertahankan preset gelap tetapi mengubah warna aksen prompt, teks kesalahan, dan teks kesuksesan:

```json ~/.claude/themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Claude Code memantau `~/.claude/themes/` dan memuat ulang saat file berubah, jadi edit yang dibuat di editor Anda berlaku untuk sesi yang sedang berjalan tanpa restart.

## Beralih ke rendering fullscreen

Jika tampilan berkedip atau posisi scroll melompat saat Claude sedang bekerja, beralih ke [mode rendering fullscreen](/id/fullscreen). Ini menggambar ke layar terpisah yang terminal cadangkan untuk aplikasi full-screen alih-alih menambahkan ke scrollback normal Anda, yang menjaga penggunaan memori tetap datar dan menambahkan dukungan mouse untuk scrolling dan seleksi. Dalam mode ini Anda scroll dengan mouse atau PageUp di dalam Claude Code daripada dengan scrollback native terminal Anda; lihat [halaman fullscreen](/id/fullscreen#search-and-review-the-conversation) untuk cara mencari dan menyalin.

Jalankan `/tui fullscreen` untuk beralih dalam sesi saat ini dengan percakapan Anda tetap utuh. Untuk menjadikannya default, atur variabel lingkungan `CLAUDE_CODE_NO_FLICKER` sebelum memulai Claude Code:

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## Tempel konten besar

Ketika Anda menempel lebih dari 10.000 karakter ke dalam prompt, Claude Code menciutkan input ke placeholder `[Pasted text]` sehingga kotak input tetap dapat digunakan. Konten lengkap masih dikirim ke Claude ketika Anda mengirimkan.

Terminal terintegrasi VS Code dapat menjatuhkan karakter dari penempelan sangat besar sebelum mereka mencapai Claude Code, jadi lebih suka alur kerja berbasis file di sana. Untuk input sangat besar seperti seluruh file atau log panjang, tulis konten ke file dan minta Claude untuk membacanya alih-alih menempel. Ini menjaga transkrip percakapan tetap dapat dibaca dan memungkinkan Claude mereferensikan file berdasarkan path di giliran kemudian.

## Edit prompt dengan pintasan keyboard Vim

Claude Code mencakup mode pengeditan gaya Vim untuk input prompt. Aktifkan melalui `/config` → Editor mode, atau dengan mengatur [`editorMode`](/id/settings#available-settings) ke `"vim"` di `~/.claude/settings.json`. Atur Editor mode kembali ke `normal` untuk mematikannya.

Mode Vim mendukung subset gerakan dan operator mode NORMAL dan VISUAL, seperti navigasi `hjkl`, seleksi `v`/`V`, dan `d`/`c`/`y` dengan objek teks. Lihat [referensi mode editor Vim](/id/interactive-mode#vim-editor-mode) untuk tabel kunci lengkap. Gerakan Vim tidak dapat dipetakan ulang melalui file pintasan keyboard.

Menekan Enter masih mengirimkan prompt Anda dalam mode INSERT, tidak seperti Vim standar. Gunakan `o` atau `O` dalam mode NORMAL, atau Ctrl+J, untuk menyisipkan baris baru sebagai gantinya.

## Sumber daya terkait

* [Mode interaktif](/id/interactive-mode): referensi pintasan keyboard lengkap dan tabel kunci Vim
* [Keybindings](/id/keybindings): petakan ulang pintasan Claude Code apa pun, termasuk Enter dan Shift+Enter
* [Rendering fullscreen](/id/fullscreen): detail tentang scrolling, pencarian, dan copy dalam mode fullscreen
* [Panduan hooks](/id/hooks-guide): lebih banyak contoh hook Notification untuk Linux dan Windows
* [Troubleshooting](/id/troubleshooting): perbaikan untuk masalah di luar konfigurasi terminal
