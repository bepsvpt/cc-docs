> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Optimalkan pengaturan terminal Anda

> Claude Code bekerja paling baik ketika terminal Anda dikonfigurasi dengan benar. Ikuti panduan ini untuk mengoptimalkan pengalaman Anda.

### Tema dan tampilan

Claude tidak dapat mengontrol tema terminal Anda. Itu ditangani oleh aplikasi terminal Anda. Anda dapat mencocokkan tema Claude Code dengan terminal Anda kapan saja melalui perintah `/config`.

Untuk penyesuaian tambahan dari antarmuka Claude Code itu sendiri, Anda dapat mengonfigurasi [baris status khusus](/id/statusline) untuk menampilkan informasi kontekstual seperti model saat ini, direktori kerja, atau cabang git di bagian bawah terminal Anda.

### Jeda baris

Anda memiliki beberapa opsi untuk memasukkan jeda baris ke dalam Claude Code:

* **Escape cepat**: Ketik `\` diikuti Enter untuk membuat baris baru
* **Shift+Enter**: Bekerja langsung di iTerm2, WezTerm, Ghostty, dan Kitty
* **Pintasan keyboard**: Atur keybinding untuk menyisipkan baris baru di terminal lain

**Atur Shift+Enter untuk terminal lain**

Jalankan `/terminal-setup` dalam Claude Code untuk secara otomatis mengonfigurasi Shift+Enter untuk VS Code, Alacritty, Zed, dan Warp.

<Note>
  Perintah `/terminal-setup` hanya terlihat di terminal yang memerlukan konfigurasi manual. Jika Anda menggunakan iTerm2, WezTerm, Ghostty, atau Kitty, Anda tidak akan melihat perintah ini karena Shift+Enter sudah bekerja secara native.
</Note>

**Atur Option+Enter (VS Code, iTerm2 atau macOS Terminal.app)**

**Untuk Mac Terminal.app:**

1. Buka Settings → Profiles → Keyboard
2. Centang "Use Option as Meta Key"

**Untuk iTerm2 dan terminal VS Code:**

1. Buka Settings → Profiles → Keys
2. Di bawah General, atur Left/Right Option key ke "Esc+"

### Pengaturan notifikasi

Jangan lewatkan saat Claude menyelesaikan tugas dengan konfigurasi notifikasi yang tepat:

#### Notifikasi sistem iTerm 2

Untuk peringatan iTerm 2 saat tugas selesai:

1. Buka iTerm 2 Preferences
2. Navigasi ke Profiles → Terminal
3. Aktifkan "Silence bell" dan Filter Alerts → "Send escape sequence-generated alerts"
4. Atur penundaan notifikasi pilihan Anda

Perhatikan bahwa notifikasi ini khusus untuk iTerm 2 dan tidak tersedia di Terminal macOS default.

#### Hook notifikasi khusus

Untuk penanganan notifikasi tingkat lanjut, Anda dapat membuat [hook notifikasi](/id/hooks#notification) untuk menjalankan logika Anda sendiri.

### Menangani input besar

Saat bekerja dengan kode ekstensif atau instruksi panjang:

* **Hindari penempelan langsung**: Claude Code mungkin kesulitan dengan konten yang ditempel sangat panjang
* **Gunakan alur kerja berbasis file**: Tulis konten ke file dan minta Claude untuk membacanya
* **Waspadai keterbatasan VS Code**: Terminal VS Code sangat rentan terhadap pemotongan penempelan panjang

### Mode Vim

Claude Code mendukung subset keybinding Vim yang dapat diaktifkan dengan `/vim` atau dikonfigurasi melalui `/config`.

Subset yang didukung mencakup:

* Pengalihan mode: `Esc` (ke NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (ke INSERT)
* Navigasi: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` dengan pengulangan `;`/`,`
* Pengeditan: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (ulangi)
* Yank/paste: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Objek teks: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentasi: `>>`/`<<`
* Operasi baris: `J` (gabung baris)

Lihat [Mode interaktif](/id/interactive-mode#vim-editor-mode) untuk referensi lengkap.
