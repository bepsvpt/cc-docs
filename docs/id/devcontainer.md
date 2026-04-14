> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Kontainer pengembangan

> Pelajari tentang kontainer pengembangan Claude Code untuk tim yang membutuhkan lingkungan yang konsisten dan aman.

Referensi [pengaturan devcontainer](https://github.com/anthropics/claude-code/tree/main/.devcontainer) dan [Dockerfile](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile) terkait menawarkan kontainer pengembangan yang telah dikonfigurasi sebelumnya yang dapat Anda gunakan apa adanya, atau sesuaikan dengan kebutuhan Anda. Devcontainer ini bekerja dengan ekstensi [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) Visual Studio Code dan alat serupa.

Langkah-langkah keamanan yang ditingkatkan dari kontainer (isolasi dan aturan firewall) memungkinkan Anda menjalankan `claude --dangerously-skip-permissions` untuk melewati permintaan izin untuk operasi tanpa pengawasan.

<Warning>
  Meskipun devcontainer menyediakan perlindungan yang substansial, tidak ada sistem yang sepenuhnya kebal terhadap semua serangan.
  Ketika dijalankan dengan `--dangerously-skip-permissions`, devcontainer tidak mencegah proyek berbahaya dari mengekstraksi apa pun yang dapat diakses di devcontainer termasuk kredensial Claude Code.
  Kami merekomendasikan hanya menggunakan devcontainer saat mengembangkan dengan repositori terpercaya.
  Selalu pertahankan praktik keamanan yang baik dan pantau aktivitas Claude.
</Warning>

## Fitur utama

* **Node.js siap produksi**: Dibangun di atas Node.js 20 dengan dependensi pengembangan penting
* **Keamanan dengan desain**: Firewall khusus yang membatasi akses jaringan hanya ke layanan yang diperlukan
* **Alat ramah pengembang**: Mencakup git, ZSH dengan peningkatan produktivitas, fzf, dan lainnya
* **Integrasi VS Code yang mulus**: Ekstensi yang telah dikonfigurasi sebelumnya dan pengaturan yang dioptimalkan
* **Persistensi sesi**: Mempertahankan riwayat perintah dan konfigurasi antara restart kontainer
* **Bekerja di mana saja**: Kompatibel dengan lingkungan pengembangan macOS, Windows, dan Linux

## Memulai dalam 4 langkah

1. Instal VS Code dan ekstensi Remote - Containers
2. Kloning repositori [implementasi referensi Claude Code](https://github.com/anthropics/claude-code/tree/main/.devcontainer)
3. Buka repositori di VS Code
4. Ketika diminta, klik "Reopen in Container" (atau gunakan Command Palette: Cmd+Shift+P → "Remote-Containers: Reopen in Container")

## Rincian konfigurasi

Pengaturan devcontainer terdiri dari tiga komponen utama:

* [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Mengontrol pengaturan kontainer, ekstensi, dan pemasangan volume
* [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Mendefinisikan citra kontainer dan alat yang diinstal
* [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Menetapkan aturan keamanan jaringan

## Fitur keamanan

Kontainer mengimplementasikan pendekatan keamanan berlapis dengan konfigurasi firewallnya:

* **Kontrol akses yang tepat**: Membatasi koneksi keluar hanya ke domain yang diizinkan (registri npm, GitHub, Claude API, dll.)
* **Koneksi keluar yang diizinkan**: Firewall memungkinkan koneksi DNS dan SSH keluar
* **Kebijakan default-deny**: Memblokir semua akses jaringan eksternal lainnya
* **Verifikasi startup**: Memvalidasi aturan firewall ketika kontainer diinisialisasi
* **Isolasi**: Membuat lingkungan pengembangan yang aman terpisah dari sistem utama Anda

## Opsi kustomisasi

Konfigurasi devcontainer dirancang untuk dapat disesuaikan dengan kebutuhan Anda:

* Tambahkan atau hapus ekstensi VS Code berdasarkan alur kerja Anda
* Modifikasi alokasi sumber daya untuk lingkungan perangkat keras yang berbeda
* Sesuaikan izin akses jaringan
* Sesuaikan konfigurasi shell dan alat pengembang

## Contoh kasus penggunaan

### Pekerjaan klien yang aman

Gunakan devcontainer untuk mengisolasi proyek klien yang berbeda, memastikan kode dan kredensial tidak pernah bercampur antar lingkungan.

### Onboarding tim

Anggota tim baru dapat mendapatkan lingkungan pengembangan yang sepenuhnya dikonfigurasi dalam hitungan menit, dengan semua alat dan pengaturan yang diperlukan telah diinstal sebelumnya.

### Lingkungan CI/CD yang konsisten

Cerminkan konfigurasi devcontainer Anda dalam pipeline CI/CD untuk memastikan lingkungan pengembangan dan produksi cocok.

## Sumber daya terkait

* [Dokumentasi devcontainer VS Code](https://code.visualstudio.com/docs/devcontainers/containers)
* [Praktik terbaik keamanan Claude Code](/id/security)
* [Konfigurasi jaringan perusahaan](/id/network-config)
