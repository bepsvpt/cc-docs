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

**Untuk iTerm2:**

1. Buka Settings → Profiles → Keys
2. Di bawah General, atur Left/Right Option key ke "Esc+"

**Untuk terminal VS Code:**

Atur `"terminal.integrated.macOptionIsMeta": true` dalam pengaturan VS Code.

### Pengaturan notifikasi

Ketika Claude selesai bekerja dan menunggu input Anda, Claude mengirimkan acara notifikasi. Anda dapat menampilkan acara ini sebagai notifikasi desktop melalui terminal Anda atau menjalankan logika khusus dengan [hook notifikasi](/id/hooks#notification).

#### Notifikasi terminal

Kitty dan Ghostty mendukung notifikasi desktop tanpa konfigurasi tambahan. iTerm 2 memerlukan pengaturan:

1. Buka iTerm 2 Settings → Profiles → Terminal
2. Aktifkan "Notification Center Alerts"
3. Klik "Filter Alerts" dan centang "Send escape sequence-generated alerts"

Jika notifikasi tidak muncul, verifikasi bahwa aplikasi terminal Anda memiliki izin notifikasi di pengaturan OS Anda.

Ketika menjalankan Claude Code di dalam tmux, notifikasi dan [bilah kemajuan terminal](/id/settings#global-config-settings) hanya mencapai terminal luar, seperti iTerm2, Kitty, atau Ghostty, jika Anda mengaktifkan passthrough dalam konfigurasi tmux Anda:

```
set -g allow-passthrough on
```

Tanpa pengaturan ini, tmux mengintersepsi urutan escape dan mereka tidak mencapai aplikasi terminal.

Terminal lain, termasuk Terminal macOS default, tidak mendukung notifikasi native. Gunakan [hook notifikasi](/id/hooks#notification) sebagai gantinya.

#### Hook notifikasi

Untuk menambahkan perilaku khusus ketika notifikasi dipicu, seperti memutar suara atau mengirim pesan, konfigurasikan [hook notifikasi](/id/hooks#notification). Hook berjalan bersama notifikasi terminal, bukan sebagai pengganti.

### Kurangi flicker dan penggunaan memori

Jika Anda melihat flicker selama sesi panjang, atau posisi scroll terminal Anda melompat ke atas saat Claude sedang bekerja, coba [rendering fullscreen](/id/fullscreen). Ini menggunakan jalur rendering alternatif yang menjaga memori tetap datar dan menambahkan dukungan mouse. Aktifkan dengan `CLAUDE_CODE_NO_FLICKER=1`.

### Menangani input besar

Saat bekerja dengan kode ekstensif atau instruksi panjang:

* **Hindari penempelan langsung**: Claude Code mungkin kesulitan dengan konten yang ditempel sangat panjang
* **Gunakan alur kerja berbasis file**: Tulis konten ke file dan minta Claude untuk membacanya
* **Waspadai keterbatasan VS Code**: Terminal VS Code sangat rentan terhadap pemotongan penempelan panjang

### Mode Vim

Claude Code mendukung subset keybinding Vim yang dapat diaktifkan dengan `/vim` atau dikonfigurasi melalui `/config`. Untuk mengatur mode langsung dalam file konfigurasi Anda, atur kunci konfigurasi global [`editorMode`](/id/settings#global-config-settings) ke `"vim"` dalam `~/.claude.json`.

Subset yang didukung mencakup:

* Pengalihan mode: `Esc` (ke NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (ke INSERT)
* Navigasi: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` dengan pengulangan `;`/`,`
* Pengeditan: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (ulangi)
* Yank/paste: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Objek teks: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentasi: `>>`/`<<`
* Operasi baris: `J` (gabung baris)

Lihat [Mode interaktif](/id/interactive-mode#vim-editor-mode) untuk referensi lengkap.
