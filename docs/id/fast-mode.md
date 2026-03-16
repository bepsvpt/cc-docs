> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Percepat respons dengan mode cepat

> Dapatkan respons Opus 4.6 yang lebih cepat di Claude Code dengan mengaktifkan mode cepat.

<Note>
  Mode cepat berada dalam [pratinjau penelitian](#research-preview). Fitur, harga, dan ketersediaan dapat berubah berdasarkan umpan balik.
</Note>

Mode cepat adalah konfigurasi kecepatan tinggi untuk Claude Opus 4.6, membuat model 2,5x lebih cepat dengan biaya per token yang lebih tinggi. Aktifkan dengan `/fast` ketika Anda membutuhkan kecepatan untuk pekerjaan interaktif seperti iterasi cepat atau debugging langsung, dan nonaktifkan ketika biaya lebih penting daripada latensi.

Mode cepat bukan model yang berbeda. Mode ini menggunakan Opus 4.6 yang sama dengan konfigurasi API berbeda yang memprioritaskan kecepatan daripada efisiensi biaya. Anda mendapatkan kualitas dan kemampuan yang identik, hanya respons yang lebih cepat.

<Note>
  Mode cepat memerlukan Claude Code v2.1.36 atau lebih baru. Periksa versi Anda dengan `claude --version`.
</Note>

Yang perlu diketahui:

* Gunakan `/fast` untuk mengaktifkan mode cepat di Claude Code CLI. Juga tersedia melalui `/fast` di Ekstensi Claude Code VS Code.
* Harga mode cepat untuk Opus 4.6 dimulai dari \$30/150 MTok. Mode cepat tersedia dengan diskon 50% untuk semua paket hingga 23:59 PT pada 16 Februari.
* Tersedia untuk semua pengguna Claude Code pada paket berlangganan (Pro/Max/Team/Enterprise) dan Claude Console.
* Untuk pengguna Claude Code pada paket berlangganan (Pro/Max/Team/Enterprise), mode cepat tersedia hanya melalui penggunaan tambahan dan tidak termasuk dalam batas laju penggunaan berlangganan.

Halaman ini mencakup cara [mengaktifkan mode cepat](#toggle-fast-mode), [pertukaran biayanya](#understand-the-cost-tradeoff), [kapan menggunakannya](#decide-when-to-use-fast-mode), [persyaratan](#requirements), [opt-in per sesi](#require-per-session-opt-in), dan [perilaku batas laju](#handle-rate-limits).

## Aktifkan mode cepat

Aktifkan mode cepat dengan salah satu cara berikut:

* Ketik `/fast` dan tekan Tab untuk mengaktifkan atau menonaktifkan
* Atur `"fastMode": true` di [file pengaturan pengguna Anda](/id/settings)

Secara default, mode cepat bertahan di seluruh sesi. Administrator dapat mengonfigurasi mode cepat untuk disetel ulang setiap sesi. Lihat [require per-session opt-in](#require-per-session-opt-in) untuk detail.

Untuk efisiensi biaya terbaik, aktifkan mode cepat di awal sesi daripada beralih di tengah percakapan. Lihat [understand the cost tradeoff](#understand-the-cost-tradeoff) untuk detail.

Ketika Anda mengaktifkan mode cepat:

* Jika Anda berada di model yang berbeda, Claude Code secara otomatis beralih ke Opus 4.6
* Anda akan melihat pesan konfirmasi: "Fast mode ON"
* Ikon kecil `↯` muncul di sebelah prompt saat mode cepat aktif
* Jalankan `/fast` lagi kapan saja untuk memeriksa apakah mode cepat aktif atau tidak

Ketika Anda menonaktifkan mode cepat dengan `/fast` lagi, Anda tetap berada di Opus 4.6. Model tidak kembali ke model sebelumnya. Untuk beralih ke model yang berbeda, gunakan `/model`.

## Pahami pertukaran biaya

Mode cepat memiliki harga per-token yang lebih tinggi daripada Opus 4.6 standar:

| Mode                            | Input (MTok) | Output (MTok) |
| ------------------------------- | ------------ | ------------- |
| Mode cepat di Opus 4.6 (\<200K) | \$30         | \$150         |
| Mode cepat di Opus 4.6 (>200K)  | \$60         | \$225         |

Mode cepat kompatibel dengan jendela konteks yang diperluas 1M token.

Ketika Anda beralih ke mode cepat di tengah percakapan, Anda membayar harga token input mode cepat tanpa cache penuh untuk seluruh konteks percakapan. Ini lebih mahal daripada jika Anda telah mengaktifkan mode cepat dari awal.

## Tentukan kapan menggunakan mode cepat

Mode cepat terbaik untuk pekerjaan interaktif di mana latensi respons lebih penting daripada biaya:

* Iterasi cepat pada perubahan kode
* Sesi debugging langsung
* Pekerjaan sensitif waktu dengan tenggat waktu ketat

Mode standar lebih baik untuk:

* Tugas otonom jangka panjang di mana kecepatan kurang penting
* Pemrosesan batch atau pipeline CI/CD
* Beban kerja sensitif biaya

### Mode cepat vs tingkat usaha

Mode cepat dan tingkat usaha keduanya mempengaruhi kecepatan respons, tetapi dengan cara yang berbeda:

| Pengaturan                     | Efek                                                                                                  |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **Mode cepat**                 | Kualitas model yang sama, latensi lebih rendah, biaya lebih tinggi                                    |
| **Tingkat usaha lebih rendah** | Waktu pemikiran lebih sedikit, respons lebih cepat, potensi kualitas lebih rendah pada tugas kompleks |

Anda dapat menggabungkan keduanya: gunakan mode cepat dengan [tingkat usaha](/id/model-config#adjust-effort-level) yang lebih rendah untuk kecepatan maksimal pada tugas yang mudah.

## Persyaratan

Mode cepat memerlukan semua hal berikut:

* **Tidak tersedia di penyedia cloud pihak ketiga**: mode cepat tidak tersedia di Amazon Bedrock, Google Vertex AI, atau Microsoft Azure Foundry. Mode cepat tersedia melalui API Konsol Anthropic dan untuk paket berlangganan Claude menggunakan penggunaan tambahan.
* **Penggunaan tambahan diaktifkan**: akun Anda harus memiliki penggunaan tambahan diaktifkan, yang memungkinkan penagihan di luar penggunaan yang disertakan dalam paket Anda. Untuk akun individual, aktifkan ini di [pengaturan penagihan Konsol Anda](https://platform.claude.com/settings/organization/billing). Untuk Teams dan Enterprise, admin harus mengaktifkan penggunaan tambahan untuk organisasi.

<Note>
  Penggunaan mode cepat ditagih langsung ke penggunaan tambahan, bahkan jika Anda memiliki penggunaan yang tersisa di paket Anda. Ini berarti token mode cepat tidak dihitung terhadap penggunaan yang disertakan dalam paket Anda dan dikenakan biaya dengan tarif mode cepat dari token pertama.
</Note>

* **Aktivasi admin untuk Teams dan Enterprise**: mode cepat dinonaktifkan secara default untuk organisasi Teams dan Enterprise. Admin harus secara eksplisit [mengaktifkan mode cepat](#enable-fast-mode-for-your-organization) sebelum pengguna dapat mengaksesnya.

<Note>
  Jika admin Anda belum mengaktifkan mode cepat untuk organisasi Anda, perintah `/fast` akan menampilkan "Fast mode has been disabled by your organization."
</Note>

### Aktifkan mode cepat untuk organisasi Anda

Admin dapat mengaktifkan mode cepat di:

* **Console** (pelanggan API): [preferensi Claude Code](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Teams dan Enterprise): [Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

Opsi lain untuk menonaktifkan mode cepat sepenuhnya adalah mengatur `CLAUDE_CODE_DISABLE_FAST_MODE=1`. Lihat [Variabel lingkungan](/id/settings#environment-variables).

### Require per-session opt-in

Secara default, mode cepat bertahan di seluruh sesi: jika pengguna mengaktifkan mode cepat, mode ini tetap aktif di sesi mendatang. Administrator pada paket [Teams](https://claude.com/pricing#team-&-enterprise) atau [Enterprise](https://anthropic.com/contact-sales) dapat mencegah ini dengan mengatur `fastModePerSessionOptIn` ke `true` di [pengaturan terkelola](/id/settings#settings-files) atau [pengaturan yang dikelola server](/id/server-managed-settings). Ini menyebabkan setiap sesi dimulai dengan mode cepat mati, memerlukan pengguna untuk secara eksplisit mengaktifkannya dengan `/fast`.

```json  theme={null}
{
  "fastModePerSessionOptIn": true
}
```

Ini berguna untuk mengontrol biaya di organisasi di mana pengguna menjalankan beberapa sesi bersamaan. Pengguna masih dapat mengaktifkan mode cepat dengan `/fast` ketika mereka membutuhkan kecepatan, tetapi mode ini disetel ulang di awal setiap sesi baru. Preferensi mode cepat pengguna masih disimpan, jadi menghapus pengaturan ini mengembalikan perilaku persisten default.

## Tangani batas laju

Mode cepat memiliki batas laju terpisah dari Opus 4.6 standar. Ketika Anda mencapai batas laju mode cepat atau kehabisan kredit penggunaan tambahan:

1. Mode cepat secara otomatis kembali ke Opus 4.6 standar
2. Ikon `↯` berubah menjadi abu-abu untuk menunjukkan cooldown
3. Anda terus bekerja dengan kecepatan dan harga standar
4. Ketika cooldown berakhir, mode cepat secara otomatis diaktifkan kembali

Untuk menonaktifkan mode cepat secara manual daripada menunggu cooldown, jalankan `/fast` lagi.

## Pratinjau penelitian

Mode cepat adalah fitur pratinjau penelitian. Ini berarti:

* Fitur dapat berubah berdasarkan umpan balik
* Ketersediaan dan harga dapat berubah
* Konfigurasi API yang mendasar dapat berkembang

Laporkan masalah atau umpan balik melalui saluran dukungan Anthropic biasa Anda.

## Lihat juga

* [Konfigurasi model](/id/model-config): beralih model dan sesuaikan tingkat usaha
* [Kelola biaya secara efektif](/id/costs): lacak penggunaan token dan kurangi biaya
* [Konfigurasi baris status](/id/statusline): tampilkan informasi model dan konteks
