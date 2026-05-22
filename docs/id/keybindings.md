> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sesuaikan pintasan keyboard

> Sesuaikan pintasan keyboard di Claude Code dengan file konfigurasi keybindings.

<Note>
  Pintasan keyboard yang dapat disesuaikan memerlukan Claude Code v2.1.18 atau lebih baru. Periksa versi Anda dengan `claude --version`.
</Note>

Claude Code mendukung pintasan keyboard yang dapat disesuaikan. Jalankan `/keybindings` untuk membuat atau membuka file konfigurasi Anda di `~/.claude/keybindings.json`.

## File konfigurasi

File konfigurasi keybindings adalah objek dengan array `bindings`. Setiap blok menentukan konteks dan peta dari keystroke ke tindakan.

<Note>Perubahan pada file keybindings secara otomatis terdeteksi dan diterapkan tanpa perlu memulai ulang Claude Code.</Note>

| Field      | Deskripsi                                                   |
| :--------- | :---------------------------------------------------------- |
| `$schema`  | URL JSON Schema opsional untuk penyelesaian otomatis editor |
| `$docs`    | URL dokumentasi opsional                                    |
| `bindings` | Array blok binding berdasarkan konteks                      |

Contoh ini mengikat `Ctrl+E` untuk membuka editor eksternal dalam konteks chat, dan membatalkan ikatan `Ctrl+U`:

```json theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/id/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## Konteks

Setiap blok binding menentukan **konteks** di mana binding berlaku:

| Konteks           | Deskripsi                                                       |
| :---------------- | :-------------------------------------------------------------- |
| `Global`          | Berlaku di mana saja dalam aplikasi                             |
| `Chat`            | Area input chat utama                                           |
| `Autocomplete`    | Menu penyelesaian otomatis terbuka                              |
| `Settings`        | Menu pengaturan                                                 |
| `Confirmation`    | Dialog izin dan konfirmasi                                      |
| `Tabs`            | Komponen navigasi tab                                           |
| `Help`            | Menu bantuan terlihat                                           |
| `Transcript`      | Penampil transkrip                                              |
| `HistorySearch`   | Mode pencarian riwayat (Ctrl+R)                                 |
| `Task`            | Tugas latar belakang sedang berjalan                            |
| `ThemePicker`     | Dialog pemilih tema                                             |
| `Attachments`     | Navigasi lampiran gambar dalam dialog pilih                     |
| `Footer`          | Navigasi indikator footer (tugas, tim, diff)                    |
| `MessageSelector` | Pemilihan pesan dialog rewind dan ringkasan                     |
| `DiffDialog`      | Navigasi penampil diff                                          |
| `ModelPicker`     | Tingkat upaya pemilih model                                     |
| `Select`          | Komponen select/list generik                                    |
| `Plugin`          | Dialog plugin (jelajahi, temukan, kelola)                       |
| `Scroll`          | Pengguliran percakapan dan pemilihan teks dalam mode fullscreen |
| `Doctor`          | Layar diagnostik `/doctor`                                      |

## Tindakan yang tersedia

Tindakan mengikuti format `namespace:action`, seperti `chat:submit` untuk mengirim pesan atau `app:toggleTodos` untuk menampilkan daftar tugas. Setiap konteks memiliki tindakan spesifik yang tersedia.

### Tindakan aplikasi

Tindakan yang tersedia dalam konteks `Global`:

| Tindakan               | Default   | Deskripsi                           |
| :--------------------- | :-------- | :---------------------------------- |
| `app:interrupt`        | Ctrl+C    | Batalkan operasi saat ini           |
| `app:exit`             | Ctrl+D    | Keluar dari Claude Code             |
| `app:redraw`           | (unbound) | Paksa terminal untuk digambar ulang |
| `app:toggleTodos`      | Ctrl+T    | Alihkan visibilitas daftar tugas    |
| `app:toggleTranscript` | Ctrl+O    | Alihkan transkrip verbose           |

### Tindakan riwayat

Tindakan untuk menavigasi riwayat perintah:

| Tindakan           | Default | Deskripsi               |
| :----------------- | :------ | :---------------------- |
| `history:search`   | Ctrl+R  | Buka pencarian riwayat  |
| `history:previous` | Up      | Item riwayat sebelumnya |
| `history:next`     | Down    | Item riwayat berikutnya |

### Tindakan chat

Tindakan yang tersedia dalam konteks `Chat`:

| Tindakan              | Default                   | Deskripsi                                                                                                                                                                            |
| :-------------------- | :------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chat:cancel`         | Escape                    | Batalkan input saat ini                                                                                                                                                              |
| `chat:clearInput`     | Ctrl+L                    | Paksa gambar ulang layar penuh, mempertahankan input. Dalam [rendering fullscreen](/id/fullscreen#clear-the-conversation), tekan dua kali dalam dua detik untuk menjalankan `/clear` |
| `chat:clearScreen`    | Cmd+K                     | Dalam [rendering fullscreen](/id/fullscreen#clear-the-conversation), tekan dua kali dalam dua detik untuk menjalankan `/clear`                                                       |
| `chat:killAgents`     | Ctrl+X Ctrl+K             | Matikan semua [subagen latar belakang](/id/sub-agents#run-subagents-in-foreground-or-background) dalam sesi ini                                                                      |
| `chat:cycleMode`      | Shift+Tab\*               | Mode izin siklus                                                                                                                                                                     |
| `chat:modelPicker`    | Meta+P                    | Buka pemilih model                                                                                                                                                                   |
| `chat:fastMode`       | Meta+O                    | Alihkan mode cepat                                                                                                                                                                   |
| `chat:thinkingToggle` | Meta+T                    | Alihkan pemikiran yang diperluas                                                                                                                                                     |
| `chat:submit`         | Enter                     | Kirim pesan                                                                                                                                                                          |
| `chat:newline`        | Ctrl+J                    | Sisipkan baris baru tanpa mengirim                                                                                                                                                   |
| `chat:undo`           | Ctrl+\_, Ctrl+Shift+-     | Batalkan tindakan terakhir                                                                                                                                                           |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E     | Buka di editor eksternal                                                                                                                                                             |
| `chat:stash`          | Ctrl+S                    | Simpan prompt saat ini                                                                                                                                                               |
| `chat:imagePaste`     | Ctrl+V (Alt+V di Windows) | Tempel gambar                                                                                                                                                                        |

\*Di Windows tanpa mode VT (Node \<24.2.0/\<22.17.0, Bun \<1.2.23), default ke Meta+M.

### Tindakan penyelesaian otomatis

Tindakan yang tersedia dalam konteks `Autocomplete`:

| Tindakan                | Default | Deskripsi        |
| :---------------------- | :------ | :--------------- |
| `autocomplete:accept`   | Tab     | Terima saran     |
| `autocomplete:dismiss`  | Escape  | Tutup menu       |
| `autocomplete:previous` | Up      | Saran sebelumnya |
| `autocomplete:next`     | Down    | Saran berikutnya |

### Tindakan konfirmasi

Tindakan yang tersedia dalam konteks `Confirmation`:

| Tindakan                    | Default   | Deskripsi               |
| :-------------------------- | :-------- | :---------------------- |
| `confirm:yes`               | Y, Enter  | Konfirmasi tindakan     |
| `confirm:no`                | N, Escape | Tolak tindakan          |
| `confirm:previous`          | Up        | Opsi sebelumnya         |
| `confirm:next`              | Down      | Opsi berikutnya         |
| `confirm:nextField`         | Tab       | Bidang berikutnya       |
| `confirm:previousField`     | (unbound) | Bidang sebelumnya       |
| `confirm:toggle`            | Space     | Alihkan pilihan         |
| `confirm:cycleMode`         | Shift+Tab | Mode izin siklus        |
| `confirm:toggleExplanation` | Ctrl+E    | Alihkan penjelasan izin |

### Tindakan izin

Tindakan yang tersedia dalam konteks `Confirmation` untuk dialog izin:

| Tindakan                 | Default   | Deskripsi                                                                                                    |
| :----------------------- | :-------- | :----------------------------------------------------------------------------------------------------------- |
| `permission:toggleDebug` | (unbound) | Alihkan info debug izin. Default sebelumnya dari Ctrl+D dihapus dalam v2.1.146 karena mengaburkan `app:exit` |

### Tindakan transkrip

Tindakan yang tersedia dalam konteks `Transcript`:

| Tindakan                   | Default           | Deskripsi                      |
| :------------------------- | :---------------- | :----------------------------- |
| `transcript:toggleShowAll` | Ctrl+E            | Alihkan tampilkan semua konten |
| `transcript:exit`          | q, Ctrl+C, Escape | Keluar dari tampilan transkrip |

### Tindakan pencarian riwayat

Tindakan yang tersedia dalam konteks `HistorySearch`:

| Tindakan                   | Default     | Deskripsi                                  |
| :------------------------- | :---------- | :----------------------------------------- |
| `historySearch:next`       | Ctrl+R      | Kecocokan berikutnya                       |
| `historySearch:accept`     | Escape, Tab | Terima pilihan                             |
| `historySearch:cancel`     | Ctrl+C      | Batalkan pencarian                         |
| `historySearch:execute`    | Enter       | Jalankan perintah yang dipilih             |
| `historySearch:cycleScope` | Ctrl+S      | Siklus cakupan: sesi, proyek, di mana saja |

### Tindakan tugas

Tindakan yang tersedia dalam konteks `Task`:

| Tindakan          | Default | Deskripsi                     |
| :---------------- | :------ | :---------------------------- |
| `task:background` | Ctrl+B  | Tugas latar belakang saat ini |

### Tindakan tema

Tindakan yang tersedia dalam konteks `ThemePicker`:

| Tindakan                         | Default | Deskripsi                  |
| :------------------------------- | :------ | :------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T  | Alihkan penyorotan sintaks |

### Tindakan bantuan

Tindakan yang tersedia dalam konteks `Help`:

| Tindakan       | Default | Deskripsi          |
| :------------- | :------ | :----------------- |
| `help:dismiss` | Escape  | Tutup menu bantuan |

### Tindakan tab

Tindakan yang tersedia dalam konteks `Tabs`:

| Tindakan        | Default         | Deskripsi      |
| :-------------- | :-------------- | :------------- |
| `tabs:next`     | Tab, Right      | Tab berikutnya |
| `tabs:previous` | Shift+Tab, Left | Tab sebelumnya |

### Tindakan lampiran

Tindakan yang tersedia dalam konteks `Attachments`:

| Tindakan               | Default           | Deskripsi                     |
| :--------------------- | :---------------- | :---------------------------- |
| `attachments:next`     | Right             | Lampiran berikutnya           |
| `attachments:previous` | Left              | Lampiran sebelumnya           |
| `attachments:remove`   | Backspace, Delete | Hapus lampiran yang dipilih   |
| `attachments:exit`     | Down, Escape      | Keluar dari navigasi lampiran |

### Tindakan footer

Tindakan yang tersedia dalam konteks `Footer`:

| Tindakan                | Default | Deskripsi                                                |
| :---------------------- | :------ | :------------------------------------------------------- |
| `footer:next`           | Right   | Item footer berikutnya                                   |
| `footer:previous`       | Left    | Item footer sebelumnya                                   |
| `footer:up`             | Up      | Navigasi ke atas dalam footer (batalkan pilihan di atas) |
| `footer:down`           | Down    | Navigasi ke bawah dalam footer                           |
| `footer:openSelected`   | Enter   | Buka item footer yang dipilih                            |
| `footer:clearSelection` | Escape  | Hapus pilihan footer                                     |

### Tindakan pemilih pesan

Tindakan yang tersedia dalam konteks `MessageSelector`:

| Tindakan                 | Default                                   | Deskripsi          |
| :----------------------- | :---------------------------------------- | :----------------- |
| `messageSelector:up`     | Up, K, Ctrl+P                             | Naik dalam daftar  |
| `messageSelector:down`   | Down, J, Ctrl+N                           | Turun dalam daftar |
| `messageSelector:top`    | Ctrl+Up, Shift+Up, Meta+Up, Shift+K       | Lompat ke atas     |
| `messageSelector:bottom` | Ctrl+Down, Shift+Down, Meta+Down, Shift+J | Lompat ke bawah    |
| `messageSelector:select` | Enter                                     | Pilih pesan        |

### Tindakan diff

Tindakan yang tersedia dalam konteks `DiffDialog`:

| Tindakan              | Default            | Deskripsi                   |
| :-------------------- | :----------------- | :-------------------------- |
| `diff:dismiss`        | Escape             | Tutup penampil diff         |
| `diff:previousSource` | Left               | Sumber diff sebelumnya      |
| `diff:nextSource`     | Right              | Sumber diff berikutnya      |
| `diff:previousFile`   | Up                 | File sebelumnya dalam diff  |
| `diff:nextFile`       | Down               | File berikutnya dalam diff  |
| `diff:viewDetails`    | Enter              | Lihat detail diff           |
| `diff:back`           | (context-specific) | Kembali dalam penampil diff |

### Tindakan pemilih model

Tindakan yang tersedia dalam konteks `ModelPicker`:

| Tindakan                     | Default | Deskripsi                                                   |
| :--------------------------- | :------ | :---------------------------------------------------------- |
| `modelPicker:decreaseEffort` | Left    | Kurangi tingkat upaya                                       |
| `modelPicker:increaseEffort` | Right   | Tingkatkan tingkat upaya                                    |
| `modelPicker:setAsDefault`   | d       | Tetapkan model yang disorot sebagai default untuk sesi baru |

### Tindakan pilih

Tindakan yang tersedia dalam konteks `Select`:

| Tindakan          | Default         | Deskripsi        |
| :---------------- | :-------------- | :--------------- |
| `select:next`     | Down, J, Ctrl+N | Opsi berikutnya  |
| `select:previous` | Up, K, Ctrl+P   | Opsi sebelumnya  |
| `select:accept`   | Enter           | Terima pilihan   |
| `select:cancel`   | Escape          | Batalkan pilihan |

### Tindakan plugin

Tindakan yang tersedia dalam konteks `Plugin`:

| Tindakan          | Default | Deskripsi                                                                                        |
| :---------------- | :------ | :----------------------------------------------------------------------------------------------- |
| `plugin:toggle`   | Space   | Alihkan pemilihan plugin                                                                         |
| `plugin:install`  | I       | Instal plugin yang dipilih                                                                       |
| `plugin:favorite` | F       | Tandai plugin yang dipilih sebagai favorit sehingga diurutkan di dekat bagian atas tab Installed |

### Tindakan pengaturan

Tindakan yang tersedia dalam konteks `Settings`:

| Tindakan          | Default | Deskripsi                                                                              |
| :---------------- | :------ | :------------------------------------------------------------------------------------- |
| `settings:search` | /       | Masuk mode pencarian                                                                   |
| `settings:retry`  | R       | Coba muat ulang data penggunaan (saat terjadi kesalahan)                               |
| `settings:close`  | Enter   | Simpan perubahan dan tutup panel konfigurasi. Escape membatalkan perubahan dan menutup |

### Tindakan dokter

Tindakan yang tersedia dalam konteks `Doctor`:

| Tindakan     | Default | Deskripsi                                                                                                          |
| :----------- | :------ | :----------------------------------------------------------------------------------------------------------------- |
| `doctor:fix` | F       | Kirim laporan diagnostik ke Claude untuk memperbaiki masalah yang dilaporkan. Hanya aktif ketika masalah ditemukan |

### Tindakan suara

Tindakan yang tersedia dalam konteks `Chat` ketika [dikte suara](/id/voice-dictation) diaktifkan:

| Tindakan           | Default | Deskripsi                                      |
| :----------------- | :------ | :--------------------------------------------- |
| `voice:pushToTalk` | Space   | Tahan atau ketuk tergantung pada mode `/voice` |

### Tindakan scroll

Tindakan yang tersedia dalam konteks `Scroll` ketika [rendering fullscreen](/id/fullscreen) diaktifkan:

| Tindakan                    | Default              | Deskripsi                                                                                                             |
| :-------------------------- | :------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| `scroll:lineUp`             | (unbound)            | Gulir ke atas satu baris. Pengguliran roda mouse memicu tindakan ini                                                  |
| `scroll:lineDown`           | (unbound)            | Gulir ke bawah satu baris. Pengguliran roda mouse memicu tindakan ini                                                 |
| `scroll:pageUp`             | PageUp               | Gulir ke atas setengah tinggi viewport                                                                                |
| `scroll:pageDown`           | PageDown             | Gulir ke bawah setengah tinggi viewport                                                                               |
| `scroll:top`                | Ctrl+Home            | Lompat ke awal percakapan                                                                                             |
| `scroll:bottom`             | Ctrl+End             | Lompat ke pesan terbaru dan aktifkan kembali auto-follow                                                              |
| `scroll:halfPageUp`         | (unbound)            | Gulir ke atas setengah tinggi viewport. Perilaku yang sama dengan `scroll:pageUp`, disediakan untuk rebind gaya vi    |
| `scroll:halfPageDown`       | (unbound)            | Gulir ke bawah setengah tinggi viewport. Perilaku yang sama dengan `scroll:pageDown`, disediakan untuk rebind gaya vi |
| `scroll:fullPageUp`         | (unbound)            | Gulir ke atas tinggi viewport penuh                                                                                   |
| `scroll:fullPageDown`       | (unbound)            | Gulir ke bawah tinggi viewport penuh                                                                                  |
| `selection:copy`            | Ctrl+Shift+C / Cmd+C | Salin teks yang dipilih ke clipboard                                                                                  |
| `selection:clear`           | (unbound)            | Hapus pemilihan teks aktif                                                                                            |
| `selection:extendLeft`      | Shift+Left           | Perluas pemilihan aktif satu kolom ke kiri                                                                            |
| `selection:extendRight`     | Shift+Right          | Perluas pemilihan aktif satu kolom ke kanan                                                                           |
| `selection:extendUp`        | Shift+Up             | Perluas pemilihan aktif satu baris ke atas. Menggulir viewport ketika pemilihan mencapai tepi atas                    |
| `selection:extendDown`      | Shift+Down           | Perluas pemilihan aktif satu baris ke bawah. Menggulir viewport ketika pemilihan mencapai tepi bawah                  |
| `selection:extendLineStart` | Shift+Home           | Perluas pemilihan aktif ke awal baris                                                                                 |
| `selection:extendLineEnd`   | Shift+End            | Perluas pemilihan aktif ke akhir baris                                                                                |

## Sintaks keystroke

### Pengubah

Gunakan tombol pengubah dengan pemisah `+`:

* `ctrl` atau `control` - Tombol Control
* `shift` - Tombol Shift
* `alt`, `opt`, `option`, atau `meta` - Tombol Alt pada Windows dan Linux, tombol Option pada macOS
* `cmd`, `command`, `super`, atau `win` - Tombol Command pada macOS, tombol Windows pada Windows, tombol Super pada Linux

Grup `cmd` hanya terdeteksi di terminal yang melaporkan pengubah Super, seperti yang mendukung protokol keyboard Kitty atau mode `modifyOtherKeys` xterm. Sebagian besar terminal tidak mengirimnya, jadi gunakan `ctrl` atau `meta` untuk binding yang ingin Anda gunakan di mana saja.

Sebagai contoh:

```text theme={null}
ctrl+k          Ctrl + K
shift+tab       Shift + Tab
meta+p          Option + P pada macOS, Alt + P di tempat lain
ctrl+shift+c    Pengubah ganda
```

### Huruf besar

Huruf besar yang berdiri sendiri menyiratkan Shift. Sebagai contoh, `K` setara dengan `shift+k`. Ini berguna untuk binding gaya vim di mana kunci huruf besar dan kecil memiliki arti berbeda.

Huruf besar dengan pengubah (misalnya, `ctrl+K`) diperlakukan sebagai gaya dan **tidak** menyiratkan Shift: `ctrl+K` sama dengan `ctrl+k`.

### Chord

Chord adalah urutan keystroke yang dipisahkan oleh spasi:

```text theme={null}
ctrl+k ctrl+s   Tekan Ctrl+K, lepaskan, lalu Ctrl+S
```

### Tombol khusus

* `escape` atau `esc` - Tombol Escape
* `enter` atau `return` - Tombol Enter
* `tab` - Tombol Tab
* `space` - Bilah spasi
* `up`, `down`, `left`, `right` - Tombol panah
* `backspace`, `delete` - Tombol hapus

## Batalkan pintasan default

Atur tindakan ke `null` untuk membatalkan ikatan pintasan default:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

Ini juga berfungsi untuk binding chord. Membatalkan setiap chord yang berbagi awalan membebaskan awalan itu untuk digunakan sebagai binding tombol tunggal:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

Jika Anda membatalkan beberapa tetapi tidak semua chord pada awalan, menekan awalan masih memasuki mode chord-wait untuk binding yang tersisa.

## Pintasan yang dicadangkan

Pintasan ini tidak dapat diikat ulang:

| Pintasan  | Alasan                                                  |
| :-------- | :------------------------------------------------------ |
| Ctrl+C    | Interrupt/cancel yang dikodekan keras                   |
| Ctrl+D    | Exit yang dikodekan keras                               |
| Ctrl+M    | Identik dengan Enter di terminal (keduanya mengirim CR) |
| Caps Lock | Tidak dikirimkan ke aplikasi terminal                   |

## Konflik terminal

Beberapa pintasan mungkin bertentangan dengan multiplexer terminal:

| Pintasan | Konflik                                     |
| :------- | :------------------------------------------ |
| Ctrl+B   | Awalan tmux (tekan dua kali untuk mengirim) |
| Ctrl+A   | Awalan GNU screen                           |
| Ctrl+Z   | Suspend proses Unix (SIGTSTP)               |

## Interaksi mode vim

Ketika mode vim diaktifkan melalui `/config` → Editor mode, keybindings dan mode vim beroperasi secara independen:

* **Mode vim** menangani input pada tingkat input teks (gerakan kursor, mode, motions)
* **Keybindings** menangani tindakan pada tingkat komponen (alihkan todos, kirim, dll.)
* Tombol Escape dalam mode vim beralih dari INSERT ke mode NORMAL; itu tidak memicu `chat:cancel`
* Sebagian besar pintasan Ctrl+key melewati mode vim ke sistem keybinding
* Dalam mode NORMAL vim, `?` menampilkan menu bantuan (perilaku vim)

## Validasi

Claude Code memvalidasi keybindings Anda dan menampilkan peringatan untuk:

* Parse errors (JSON atau struktur tidak valid)
* Nama konteks tidak valid
* Konflik pintasan yang dicadangkan
* Konflik multiplexer terminal
* Binding duplikat dalam konteks yang sama

Jalankan `/doctor` untuk melihat peringatan keybinding apa pun.
