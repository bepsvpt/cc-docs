> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Secara otomatis melacak dan membatalkan pengeditan Claude untuk pemulihan cepat dari perubahan yang tidak diinginkan.

Claude Code secara otomatis melacak pengeditan file Claude saat Anda bekerja, memungkinkan Anda dengan cepat membatalkan perubahan dan kembali ke status sebelumnya jika ada yang tidak sesuai rencana.

## Cara kerja checkpoint

Saat Anda bekerja dengan Claude, checkpointing secara otomatis menangkap status kode Anda sebelum setiap pengeditan. Jaring pengaman ini memungkinkan Anda mengejar tugas-tugas yang ambisius dan berskala besar dengan mengetahui Anda selalu dapat kembali ke status kode sebelumnya.

### Pelacakan otomatis

Claude Code melacak semua perubahan yang dibuat oleh alat pengeditan filenya:

* Setiap prompt pengguna membuat checkpoint baru
* Checkpoint bertahan di seluruh sesi, sehingga Anda dapat mengaksesnya dalam percakapan yang dilanjutkan
* Secara otomatis dibersihkan bersama dengan sesi setelah 30 hari (dapat dikonfigurasi)

### Membatalkan perubahan

Tekan `Esc` dua kali (`Esc` + `Esc`) atau gunakan perintah `/rewind` untuk membuka menu rewind. Anda dapat memilih untuk mengembalikan:

* **Percakapan saja**: Kembali ke pesan pengguna sambil mempertahankan perubahan kode
* **Kode saja**: Kembalikan perubahan file sambil mempertahankan percakapan
* **Kode dan percakapan**: Kembalikan keduanya ke titik sebelumnya dalam sesi

## Kasus penggunaan umum

Checkpoint sangat berguna ketika:

* **Menjelajahi alternatif**: Coba pendekatan implementasi yang berbeda tanpa kehilangan titik awal Anda
* **Memulihkan dari kesalahan**: Dengan cepat batalkan perubahan yang memperkenalkan bug atau merusak fungsionalitas
* **Iterasi pada fitur**: Bereksperimen dengan variasi dengan mengetahui Anda dapat kembali ke status yang berfungsi

## Keterbatasan

### Perubahan perintah Bash tidak dilacak

Checkpointing tidak melacak file yang dimodifikasi oleh perintah bash. Misalnya, jika Claude Code menjalankan:

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Modifikasi file ini tidak dapat dibatalkan melalui rewind. Hanya pengeditan file langsung yang dibuat melalui alat pengeditan file Claude yang dilacak.

### Perubahan eksternal tidak dilacak

Checkpointing hanya melacak file yang telah diedit dalam sesi saat ini. Perubahan manual yang Anda buat pada file di luar Claude Code dan pengeditan dari sesi bersamaan lainnya biasanya tidak ditangkap, kecuali jika kebetulan mereka memodifikasi file yang sama dengan sesi saat ini.

### Bukan pengganti kontrol versi

Checkpoint dirancang untuk pemulihan cepat tingkat sesi. Untuk riwayat versi permanen dan kolaborasi:

* Terus gunakan kontrol versi (mis. Git) untuk commit, branch, dan riwayat jangka panjang
* Checkpoint melengkapi tetapi tidak menggantikan kontrol versi yang tepat
* Pikirkan checkpoint sebagai "undo lokal" dan Git sebagai "riwayat permanen"

## Lihat juga

* [Mode interaktif](/id/interactive-mode) - Pintasan keyboard dan kontrol sesi
* [Perintah bawaan](/id/interactive-mode#built-in-commands) - Mengakses checkpoint menggunakan `/rewind`
* [Referensi CLI](/id/cli-reference) - Opsi baris perintah
