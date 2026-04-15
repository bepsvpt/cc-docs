> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Gunakan Claude Code dengan JetBrains IDEs termasuk IntelliJ, PyCharm, WebStorm, dan lainnya

Claude Code terintegrasi dengan JetBrains IDEs melalui plugin khusus, menyediakan fitur seperti tampilan diff interaktif, berbagi konteks seleksi, dan lainnya.

## IDE yang Didukung

Plugin Claude Code bekerja dengan sebagian besar JetBrains IDEs, termasuk:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Fitur

* **Peluncuran cepat**: Gunakan `Cmd+Esc` (Mac) atau `Ctrl+Esc` (Windows/Linux) untuk membuka Claude Code langsung dari editor Anda, atau klik tombol Claude Code di UI
* **Tampilan diff**: Perubahan kode dapat ditampilkan langsung di penampil diff IDE alih-alih terminal
* **Konteks seleksi**: Seleksi/tab saat ini di IDE secara otomatis dibagikan dengan Claude Code
* **Pintasan referensi file**: Gunakan `Cmd+Option+K` (Mac) atau `Alt+Ctrl+K` (Linux/Windows) untuk menyisipkan referensi file (misalnya, @File#L1-99)
* **Berbagi diagnostik**: Kesalahan diagnostik (lint, sintaks, dll.) dari IDE secara otomatis dibagikan dengan Claude saat Anda bekerja

## Instalasi

### Instalasi Marketplace

Temukan dan instal [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) dari marketplace JetBrains dan mulai ulang IDE Anda.

Jika Anda belum menginstal Claude Code, lihat [panduan quickstart kami](/id/quickstart) untuk instruksi instalasi.

<Note>
  Setelah menginstal plugin, Anda mungkin perlu memulai ulang IDE Anda sepenuhnya agar dapat diterapkan.
</Note>

## Penggunaan

### Dari IDE Anda

Jalankan `claude` dari terminal terintegrasi IDE Anda, dan semua fitur integrasi akan aktif.

### Dari Terminal Eksternal

Gunakan perintah `/ide` di terminal eksternal apa pun untuk menghubungkan Claude Code ke JetBrains IDE Anda dan mengaktifkan semua fitur:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Jika Anda ingin Claude memiliki akses ke file yang sama dengan IDE Anda, mulai Claude Code dari direktori yang sama dengan root proyek IDE Anda.

## Konfigurasi

### Pengaturan Claude Code

Konfigurasikan integrasi IDE melalui pengaturan Claude Code:

1. Jalankan `claude`
2. Masukkan perintah `/config`
3. Atur alat diff ke `auto` untuk deteksi IDE otomatis

### Pengaturan Plugin

Konfigurasikan plugin Claude Code dengan membuka **Settings → Tools → Claude Code \[Beta]**:

#### Pengaturan Umum

* **Perintah Claude**: Tentukan perintah khusus untuk menjalankan Claude (misalnya, `claude`, `/usr/local/bin/claude`, atau `npx @anthropic/claude`)
* **Tekan notifikasi untuk perintah Claude tidak ditemukan**: Lewati notifikasi tentang tidak menemukan perintah Claude
* **Aktifkan penggunaan Option+Enter untuk prompt multi-baris** (hanya macOS): Ketika diaktifkan, Option+Enter menyisipkan baris baru dalam prompt Claude Code. Nonaktifkan jika mengalami masalah dengan tombol Option yang ditangkap secara tidak terduga (memerlukan restart terminal)
* **Aktifkan pembaruan otomatis**: Secara otomatis periksa dan instal pembaruan plugin (diterapkan saat restart)

<Tip>
  Untuk pengguna WSL: Atur `wsl -d Ubuntu -- bash -lic "claude"` sebagai perintah Claude Anda (ganti `Ubuntu` dengan nama distribusi WSL Anda)
</Tip>

#### Konfigurasi Tombol ESC

Jika tombol ESC tidak menghentikan operasi Claude Code di terminal JetBrains:

1. Buka **Settings → Tools → Terminal**
2. Salah satu dari:
   * Batalkan centang "Pindahkan fokus ke editor dengan Escape", atau
   * Klik "Konfigurasikan pintasan keyboard terminal" dan hapus pintasan "Alihkan fokus ke Editor"
3. Terapkan perubahan

Ini memungkinkan tombol ESC untuk dengan benar menghentikan operasi Claude Code.

## Konfigurasi Khusus

### Pengembangan Jarak Jauh

<Warning>
  Saat menggunakan JetBrains Remote Development, Anda harus menginstal plugin di host jarak jauh melalui **Settings → Plugin (Host)**.
</Warning>

Plugin harus diinstal di host jarak jauh, bukan di mesin klien lokal Anda.

### Konfigurasi WSL

<Warning>
  Pengguna WSL mungkin memerlukan konfigurasi tambahan agar deteksi IDE berfungsi dengan baik. Lihat [panduan troubleshooting WSL kami](/id/troubleshooting#jetbrains-ide-not-detected-on-wsl2) untuk instruksi setup terperinci.
</Warning>

Konfigurasi WSL mungkin memerlukan:

* Konfigurasi terminal yang tepat
* Penyesuaian mode jaringan
* Pembaruan pengaturan firewall

## Troubleshooting

### Plugin Tidak Berfungsi

* Pastikan Anda menjalankan Claude Code dari direktori root proyek
* Periksa bahwa plugin JetBrains diaktifkan dalam pengaturan IDE
* Mulai ulang IDE sepenuhnya (Anda mungkin perlu melakukan ini beberapa kali)
* Untuk Remote Development, pastikan plugin diinstal di host jarak jauh

### IDE Tidak Terdeteksi

* Verifikasi plugin diinstal dan diaktifkan
* Mulai ulang IDE sepenuhnya
* Periksa bahwa Anda menjalankan Claude Code dari terminal terintegrasi
* Untuk pengguna WSL, lihat [panduan troubleshooting WSL](/id/troubleshooting#jetbrains-ide-not-detected-on-wsl2)

### Perintah Tidak Ditemukan

Jika mengklik ikon Claude menunjukkan "command not found":

1. Verifikasi Claude Code diinstal: `npm list -g @anthropic-ai/claude-code`
2. Konfigurasikan jalur perintah Claude dalam pengaturan plugin
3. Untuk pengguna WSL, gunakan format perintah WSL yang disebutkan di bagian konfigurasi

## Pertimbangan Keamanan

Ketika Claude Code berjalan di JetBrains IDE dengan izin auto-edit diaktifkan, Claude Code mungkin dapat memodifikasi file konfigurasi IDE yang dapat dijalankan secara otomatis oleh IDE Anda. Ini dapat meningkatkan risiko menjalankan Claude Code dalam mode auto-edit dan memungkinkan melewati prompt izin Claude Code untuk eksekusi bash.

Saat berjalan di JetBrains IDEs, pertimbangkan:

* Menggunakan mode persetujuan manual untuk edit
* Berhati-hati ekstra untuk memastikan Claude hanya digunakan dengan prompt terpercaya
* Menyadari file mana yang Claude Code memiliki akses untuk memodifikasi

Untuk bantuan tambahan, lihat [panduan troubleshooting kami](/id/troubleshooting).
