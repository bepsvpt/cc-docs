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

```json  theme={null}
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

| Konteks           | Deskripsi                                     |
| :---------------- | :-------------------------------------------- |
| `Global`          | Berlaku di mana saja dalam aplikasi           |
| `Chat`            | Area input chat utama                         |
| `Autocomplete`    | Menu penyelesaian otomatis terbuka            |
| `Settings`        | Menu pengaturan (dismiss hanya dengan escape) |
| `Confirmation`    | Dialog izin dan konfirmasi                    |
| `Tabs`            | Komponen navigasi tab                         |
| `Help`            | Menu bantuan terlihat                         |
| `Transcript`      | Penampil transkrip                            |
| `HistorySearch`   | Mode pencarian riwayat (Ctrl+R)               |
| `Task`            | Tugas latar belakang sedang berjalan          |
| `ThemePicker`     | Dialog pemilih tema                           |
| `Attachments`     | Navigasi bilah gambar/lampiran                |
| `Footer`          | Navigasi indikator footer (tugas, tim, diff)  |
| `MessageSelector` | Pemilihan pesan dialog rewind dan ringkasan   |
| `DiffDialog`      | Navigasi penampil diff                        |
| `ModelPicker`     | Tingkat upaya pemilih model                   |
| `Select`          | Komponen select/list generik                  |
| `Plugin`          | Dialog plugin (jelajahi, temukan, kelola)     |

## Tindakan yang tersedia

Tindakan mengikuti format `namespace:action`, seperti `chat:submit` untuk mengirim pesan atau `app:toggleTodos` untuk menampilkan daftar tugas. Setiap konteks memiliki tindakan spesifik yang tersedia.

### Tindakan aplikasi

Tindakan yang tersedia dalam konteks `Global`:

| Tindakan               | Default | Deskripsi                        |
| :--------------------- | :------ | :------------------------------- |
| `app:interrupt`        | Ctrl+C  | Batalkan operasi saat ini        |
| `app:exit`             | Ctrl+D  | Keluar dari Claude Code          |
| `app:toggleTodos`      | Ctrl+T  | Alihkan visibilitas daftar tugas |
| `app:toggleTranscript` | Ctrl+O  | Alihkan transkrip verbose        |

### Tindakan riwayat

Tindakan untuk menavigasi riwayat perintah:

| Tindakan           | Default | Deskripsi               |
| :----------------- | :------ | :---------------------- |
| `history:search`   | Ctrl+R  | Buka pencarian riwayat  |
| `history:previous` | Up      | Item riwayat sebelumnya |
| `history:next`     | Down    | Item riwayat berikutnya |

### Tindakan chat

Tindakan yang tersedia dalam konteks `Chat`:

| Tindakan              | Default                   | Deskripsi                         |
| :-------------------- | :------------------------ | :-------------------------------- |
| `chat:cancel`         | Escape                    | Batalkan input saat ini           |
| `chat:killAgents`     | Ctrl+X Ctrl+K             | Matikan semua agen latar belakang |
| `chat:cycleMode`      | Shift+Tab\*               | Mode izin siklus                  |
| `chat:modelPicker`    | Cmd+P / Meta+P            | Buka pemilih model                |
| `chat:fastMode`       | Meta+O                    | Alihkan mode cepat                |
| `chat:thinkingToggle` | Cmd+T / Meta+T            | Alihkan pemikiran yang diperluas  |
| `chat:submit`         | Enter                     | Kirim pesan                       |
| `chat:undo`           | Ctrl+\_                   | Batalkan tindakan terakhir        |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E     | Buka di editor eksternal          |
| `chat:stash`          | Ctrl+S                    | Simpan prompt saat ini            |
| `chat:imagePaste`     | Ctrl+V (Alt+V di Windows) | Tempel gambar                     |

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
| `confirm:cycleMode`         | Shift+Tab | Mode izin siklus        |
| `confirm:toggleExplanation` | Ctrl+E    | Alihkan penjelasan izin |

### Tindakan izin

Tindakan yang tersedia dalam konteks `Confirmation` untuk dialog izin:

| Tindakan                 | Default | Deskripsi               |
| :----------------------- | :------ | :---------------------- |
| `permission:toggleDebug` | Ctrl+D  | Alihkan info debug izin |

### Tindakan transkrip

Tindakan yang tersedia dalam konteks `Transcript`:

| Tindakan                   | Default        | Deskripsi                      |
| :------------------------- | :------------- | :----------------------------- |
| `transcript:toggleShowAll` | Ctrl+E         | Alihkan tampilkan semua konten |
| `transcript:exit`          | Ctrl+C, Escape | Keluar dari tampilan transkrip |

### Tindakan pencarian riwayat

Tindakan yang tersedia dalam konteks `HistorySearch`:

| Tindakan                | Default     | Deskripsi                      |
| :---------------------- | :---------- | :----------------------------- |
| `historySearch:next`    | Ctrl+R      | Kecocokan berikutnya           |
| `historySearch:accept`  | Escape, Tab | Terima pilihan                 |
| `historySearch:cancel`  | Ctrl+C      | Batalkan pencarian             |
| `historySearch:execute` | Enter       | Jalankan perintah yang dipilih |

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

| Tindakan               | Default           | Deskripsi                   |
| :--------------------- | :---------------- | :-------------------------- |
| `attachments:next`     | Right             | Lampiran berikutnya         |
| `attachments:previous` | Left              | Lampiran sebelumnya         |
| `attachments:remove`   | Backspace, Delete | Hapus lampiran yang dipilih |
| `attachments:exit`     | Down, Escape      | Keluar dari bilah lampiran  |

### Tindakan footer

Tindakan yang tersedia dalam konteks `Footer`:

| Tindakan                | Default | Deskripsi                     |
| :---------------------- | :------ | :---------------------------- |
| `footer:next`           | Right   | Item footer berikutnya        |
| `footer:previous`       | Left    | Item footer sebelumnya        |
| `footer:openSelected`   | Enter   | Buka item footer yang dipilih |
| `footer:clearSelection` | Escape  | Hapus pilihan footer          |

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

| Tindakan                     | Default | Deskripsi                |
| :--------------------------- | :------ | :----------------------- |
| `modelPicker:decreaseEffort` | Left    | Kurangi tingkat upaya    |
| `modelPicker:increaseEffort` | Right   | Tingkatkan tingkat upaya |

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

| Tindakan         | Default | Deskripsi                  |
| :--------------- | :------ | :------------------------- |
| `plugin:toggle`  | Space   | Alihkan pemilihan plugin   |
| `plugin:install` | I       | Instal plugin yang dipilih |

### Tindakan pengaturan

Tindakan yang tersedia dalam konteks `Settings`:

| Tindakan          | Default | Deskripsi                                                |
| :---------------- | :------ | :------------------------------------------------------- |
| `settings:search` | /       | Masuk mode pencarian                                     |
| `settings:retry`  | R       | Coba muat ulang data penggunaan (saat terjadi kesalahan) |

### Tindakan suara

Tindakan yang tersedia dalam konteks `Chat` ketika [dikte suara](/id/voice-dictation) diaktifkan:

| Tindakan           | Default | Deskripsi                   |
| :----------------- | :------ | :-------------------------- |
| `voice:pushToTalk` | Space   | Tahan untuk mendikte prompt |

## Sintaks keystroke

### Pengubah

Gunakan tombol pengubah dengan pemisah `+`:

* `ctrl` atau `control` - Tombol Control
* `alt`, `opt`, atau `option` - Tombol Alt/Option
* `shift` - Tombol Shift
* `meta`, `cmd`, atau `command` - Tombol Meta/Command

Sebagai contoh:

```text  theme={null}
ctrl+k          Tombol tunggal dengan pengubah
shift+tab       Shift + Tab
meta+p          Command/Meta + P
ctrl+shift+c    Pengubah ganda
```

### Huruf besar

Huruf besar yang berdiri sendiri menyiratkan Shift. Sebagai contoh, `K` setara dengan `shift+k`. Ini berguna untuk binding gaya vim di mana kunci huruf besar dan kecil memiliki arti berbeda.

Huruf besar dengan pengubah (misalnya, `ctrl+K`) diperlakukan sebagai gaya dan **tidak** menyiratkan Shift — `ctrl+K` sama dengan `ctrl+k`.

### Chord

Chord adalah urutan keystroke yang dipisahkan oleh spasi:

```text  theme={null}
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

```json  theme={null}
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

## Pintasan yang dicadangkan

Pintasan ini tidak dapat diikat ulang:

| Pintasan | Alasan                                                  |
| :------- | :------------------------------------------------------ |
| Ctrl+C   | Interrupt/cancel yang dikodekan keras                   |
| Ctrl+D   | Exit yang dikodekan keras                               |
| Ctrl+M   | Identik dengan Enter di terminal (keduanya mengirim CR) |

## Konflik terminal

Beberapa pintasan mungkin bertentangan dengan multiplexer terminal:

| Pintasan | Konflik                                     |
| :------- | :------------------------------------------ |
| Ctrl+B   | Awalan tmux (tekan dua kali untuk mengirim) |
| Ctrl+A   | Awalan GNU screen                           |
| Ctrl+Z   | Suspend proses Unix (SIGTSTP)               |

## Interaksi mode vim

Ketika mode vim diaktifkan (`/vim`), keybindings dan mode vim beroperasi secara independen:

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
