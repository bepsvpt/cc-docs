> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi model

> Pelajari tentang konfigurasi model Claude Code, termasuk alias model seperti `opusplan`

## Model yang tersedia

Untuk pengaturan `model` di Claude Code, Anda dapat mengonfigurasi salah satu dari:

* Sebuah **alias model**
* Sebuah **nama model**
  * Anthropic API: Sebuah **[nama model](https://platform.claude.com/docs/en/about-claude/models/overview)** lengkap
  * Bedrock: ARN profil inferensi
  * Foundry: nama deployment
  * Vertex: nama versi

### Alias model

Alias model menyediakan cara yang nyaman untuk memilih pengaturan model tanpa perlu mengingat nomor versi yang tepat:

| Alias model      | Perilaku                                                                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Pengaturan model yang direkomendasikan, tergantung pada jenis akun Anda                                                                                                    |
| **`sonnet`**     | Menggunakan model Sonnet terbaru (saat ini Sonnet 4.6) untuk tugas coding sehari-hari                                                                                      |
| **`opus`**       | Menggunakan model Opus terbaru (saat ini Opus 4.6) untuk tugas penalaran kompleks                                                                                          |
| **`haiku`**      | Menggunakan model Haiku yang cepat dan efisien untuk tugas sederhana                                                                                                       |
| **`sonnet[1m]`** | Menggunakan Sonnet dengan [jendela konteks 1 juta token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) untuk sesi panjang |
| **`opusplan`**   | Mode khusus yang menggunakan `opus` selama plan mode, kemudian beralih ke `sonnet` untuk eksekusi                                                                          |

Alias selalu menunjuk ke versi terbaru. Untuk menetapkan ke versi tertentu, gunakan nama model lengkap (misalnya, `claude-opus-4-6`) atau atur variabel lingkungan yang sesuai seperti `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Mengatur model Anda

Anda dapat mengonfigurasi model Anda dengan beberapa cara, yang tercantum dalam urutan prioritas:

1. **Selama sesi** - Gunakan `/model <alias|name>` untuk beralih model di tengah sesi
2. **Saat startup** - Luncurkan dengan `claude --model <alias|name>`
3. **Variabel lingkungan** - Atur `ANTHROPIC_MODEL=<alias|name>`
4. **Pengaturan** - Konfigurasi secara permanen di file pengaturan Anda menggunakan bidang `model`.

Contoh penggunaan:

```bash  theme={null}
# Mulai dengan Opus
claude --model opus

# Beralih ke Sonnet selama sesi
/model sonnet
```

Contoh file pengaturan:

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Batasi pemilihan model

Administrator enterprise dapat menggunakan `availableModels` dalam [pengaturan terkelola atau kebijakan](/id/settings#settings-files) untuk membatasi model mana yang dapat dipilih pengguna.

Ketika `availableModels` diatur, pengguna tidak dapat beralih ke model yang tidak ada dalam daftar melalui `/model`, flag `--model`, alat Config, atau variabel lingkungan `ANTHROPIC_MODEL`.

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Perilaku model default

Opsi Default di pemilih model tidak dipengaruhi oleh `availableModels`. Opsi ini selalu tetap tersedia dan mewakili default runtime sistem [berdasarkan tingkat langganan pengguna](#default-model-setting).

Bahkan dengan `availableModels: []`, pengguna masih dapat menggunakan Claude Code dengan model Default untuk tingkat mereka.

### Kontrol model yang dijalankan pengguna

Untuk sepenuhnya mengontrol pengalaman model, gunakan `availableModels` bersama dengan pengaturan `model`:

* **availableModels**: membatasi apa yang dapat dialihkan pengguna
* **model**: menetapkan penggantian model eksplisit, mengambil alih dari Default

Contoh ini memastikan semua pengguna menjalankan Sonnet 4.6 dan hanya dapat memilih antara Sonnet dan Haiku:

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### Perilaku penggabungan

Ketika `availableModels` diatur di beberapa tingkat, seperti pengaturan pengguna dan pengaturan proyek, array digabungkan dan dideduplikasi. Untuk memberlakukan allowlist ketat, atur `availableModels` dalam pengaturan terkelola atau kebijakan yang memiliki prioritas tertinggi.

## Perilaku model khusus

### Pengaturan model `default`

Perilaku `default` tergantung pada jenis akun Anda:

* **Max dan Team Premium**: default ke Opus 4.6
* **Pro dan Team Standard**: default ke Sonnet 4.6
* **Enterprise**: Opus 4.6 tersedia tetapi bukan default

Claude Code dapat secara otomatis kembali ke Sonnet jika Anda mencapai ambang penggunaan dengan Opus.

### Pengaturan model `opusplan`

Alias model `opusplan` menyediakan pendekatan hibrida otomatis:

* **Dalam plan mode** - Menggunakan `opus` untuk penalaran kompleks dan keputusan arsitektur
* **Dalam execution mode** - Secara otomatis beralih ke `sonnet` untuk pembuatan kode dan implementasi

Ini memberi Anda yang terbaik dari kedua dunia: penalaran superior Opus untuk perencanaan, dan efisiensi Sonnet untuk eksekusi.

### Sesuaikan tingkat usaha

[Tingkat usaha](https://platform.claude.com/docs/en/build-with-claude/effort) mengontrol penalaran adaptif, yang secara dinamis mengalokasikan pemikiran berdasarkan kompleksitas tugas. Usaha lebih rendah lebih cepat dan lebih murah untuk tugas-tugas langsung, sementara usaha lebih tinggi memberikan penalaran lebih dalam untuk masalah kompleks.

Tiga tingkat tersedia: **low**, **medium**, dan **high**. Opus 4.6 default ke medium effort untuk pelanggan Max dan Team.

**Mengatur usaha:**

* **Dalam `/model`**: gunakan tombol panah kiri/kanan untuk menyesuaikan slider usaha saat memilih model
* **Variabel lingkungan**: atur `CLAUDE_CODE_EFFORT_LEVEL=low|medium|high`
* **Pengaturan**: atur `effortLevel` di file pengaturan Anda

Usaha didukung pada Opus 4.6 dan Sonnet 4.6. Slider usaha muncul dalam `/model` ketika model yang didukung dipilih. Tingkat usaha saat ini juga ditampilkan di sebelah logo dan spinner (misalnya, "with low effort"), sehingga Anda dapat mengkonfirmasi pengaturan mana yang aktif tanpa membuka `/model`.

Untuk menonaktifkan penalaran adaptif pada Opus 4.6 dan Sonnet 4.6 dan kembali ke anggaran pemikiran tetap sebelumnya, atur `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Ketika dinonaktifkan, model ini menggunakan anggaran tetap yang dikendalikan oleh `MAX_THINKING_TOKENS`. Lihat [variabel lingkungan](/id/settings#environment-variables).

### Konteks diperluas

Opus 4.6 dan Sonnet 4.6 mendukung [jendela konteks 1 juta token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) untuk sesi panjang dengan basis kode besar.

<Note>
  Jendela konteks 1M saat ini dalam beta. Fitur, harga, dan ketersediaan dapat berubah.
</Note>

Konteks diperluas tersedia untuk:

* **Pengguna API dan pay-as-you-go**: akses penuh ke konteks 1M
* **Pelanggan Pro, Max, Teams, dan Enterprise**: tersedia dengan [penggunaan ekstra](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) diaktifkan

Untuk menonaktifkan konteks 1M sepenuhnya, atur `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Ini menghapus varian model 1M dari pemilih model. Lihat [variabel lingkungan](/id/settings#environment-variables).

Memilih model 1M tidak segera mengubah penagihan. Sesi Anda menggunakan tarif standar hingga melebihi 200K token konteks. Melampaui 200K token, permintaan dikenakan biaya pada [harga konteks panjang](https://platform.claude.com/docs/en/about-claude/pricing#long-context-pricing) dengan [batas laju](https://platform.claude.com/docs/en/api/rate-limits#long-context-rate-limits) khusus. Untuk pelanggan, token melampaui 200K ditagih sebagai penggunaan ekstra daripada melalui langganan.

Jika akun Anda mendukung konteks 1M, opsi muncul di pemilih model (`/model`) dalam versi terbaru Claude Code. Jika Anda tidak melihatnya, coba mulai ulang sesi Anda.

Anda juga dapat menggunakan akhiran `[1m]` dengan alias model atau nama model lengkap:

```bash  theme={null}
# Gunakan alias sonnet[1m]
/model sonnet[1m]

# Atau tambahkan [1m] ke nama model lengkap
/model claude-sonnet-4-6[1m]
```

## Memeriksa model Anda saat ini

Anda dapat melihat model mana yang sedang Anda gunakan dengan beberapa cara:

1. Dalam [baris status](/id/statusline) (jika dikonfigurasi)
2. Dalam `/status`, yang juga menampilkan informasi akun Anda.

## Variabel lingkungan

Anda dapat menggunakan variabel lingkungan berikut, yang harus berupa **nama model** lengkap (atau setara untuk penyedia API Anda), untuk mengontrol nama model yang dipetakan alias.

| Variabel lingkungan              | Deskripsi                                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Model yang digunakan untuk `opus`, atau untuk `opusplan` ketika Plan Mode aktif.                           |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Model yang digunakan untuk `sonnet`, atau untuk `opusplan` ketika Plan Mode tidak aktif.                   |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Model yang digunakan untuk `haiku`, atau [fungsionalitas latar belakang](/id/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Model yang digunakan untuk [subagents](/id/sub-agents)                                                     |

Catatan: `ANTHROPIC_SMALL_FAST_MODEL` sudah usang dan digantikan oleh `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Tetapkan model untuk deployment pihak ketiga

Saat menerapkan Claude Code melalui [Bedrock](/id/amazon-bedrock), [Vertex AI](/id/google-vertex-ai), atau [Foundry](/id/microsoft-foundry), tetapkan versi model sebelum meluncurkan ke pengguna.

Tanpa penetapan, Claude Code menggunakan alias model (`sonnet`, `opus`, `haiku`) yang diselesaikan ke versi terbaru. Ketika Anthropic merilis model baru, pengguna yang akunnya tidak memiliki versi baru yang diaktifkan akan rusak secara diam-diam.

<Warning>
  Atur ketiga variabel lingkungan model ke ID versi spesifik sebagai bagian dari pengaturan awal Anda. Melewatkan langkah ini berarti pembaruan Claude Code dapat merusak pengguna Anda tanpa tindakan apa pun dari pihak Anda.
</Warning>

Gunakan variabel lingkungan berikut dengan ID model spesifik versi untuk penyedia Anda:

| Penyedia  | Contoh                                                                  |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Terapkan pola yang sama untuk `ANTHROPIC_DEFAULT_SONNET_MODEL` dan `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Untuk ID model saat ini dan warisan di semua penyedia, lihat [Ikhtisar Model](https://platform.claude.com/docs/en/about-claude/models/overview). Untuk meningkatkan pengguna ke versi model baru, perbarui variabel lingkungan ini dan terapkan kembali.

<Note>
  Allowlist `settings.availableModels` masih berlaku saat menggunakan penyedia pihak ketiga. Penyaringan cocok pada alias model (`opus`, `sonnet`, `haiku`), bukan ID model spesifik penyedia.
</Note>

### Ganti ID model per versi

Variabel lingkungan tingkat keluarga di atas mengonfigurasi satu ID model per alias keluarga. Jika Anda perlu memetakan beberapa versi dalam keluarga yang sama ke ID penyedia yang berbeda, gunakan pengaturan `modelOverrides` sebagai gantinya.

`modelOverrides` memetakan ID model Anthropic individual ke string spesifik penyedia yang dikirim Claude Code ke API penyedia Anda. Ketika pengguna memilih model yang dipetakan di pemilih `/model`, Claude Code menggunakan nilai yang dikonfigurasi Anda alih-alih default bawaan.

Ini memungkinkan administrator enterprise untuk merutekan setiap versi model ke ARN profil inferensi Bedrock spesifik, nama versi Vertex AI, atau nama deployment Foundry untuk tata kelola, alokasi biaya, atau perutean regional.

Atur `modelOverrides` dalam [file pengaturan Anda](/id/settings#settings-files):

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Kunci harus berupa ID model Anthropic seperti yang tercantum dalam [Ikhtisar Model](https://platform.claude.com/docs/en/about-claude/models/overview). Untuk ID model bertanggal, sertakan akhiran tanggal persis seperti yang muncul di sana. Kunci yang tidak dikenal diabaikan.

Penggantian menggantikan ID model bawaan yang mendukung setiap entri di pemilih `/model`. Di Bedrock, penggantian mengambil alih profil inferensi apa pun yang ditemukan Claude Code secara otomatis saat startup. Nilai yang Anda berikan langsung melalui `ANTHROPIC_MODEL`, `--model`, atau variabel lingkungan `ANTHROPIC_DEFAULT_*_MODEL` diteruskan ke penyedia apa adanya dan tidak diubah oleh `modelOverrides`.

`modelOverrides` bekerja bersama `availableModels`. Allowlist dievaluasi terhadap ID model Anthropic, bukan nilai penggantian, jadi entri seperti `"opus"` dalam `availableModels` terus cocok bahkan ketika versi Opus dipetakan ke ARN.

### Konfigurasi prompt caching

Claude Code secara otomatis menggunakan [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) untuk mengoptimalkan kinerja dan mengurangi biaya. Anda dapat menonaktifkan prompt caching secara global atau untuk tingkat model tertentu:

| Variabel lingkungan             | Deskripsi                                                                                              |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `DISABLE_PROMPT_CACHING`        | Atur ke `1` untuk menonaktifkan prompt caching untuk semua model (mengambil alih pengaturan per-model) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Atur ke `1` untuk menonaktifkan prompt caching hanya untuk model Haiku                                 |
| `DISABLE_PROMPT_CACHING_SONNET` | Atur ke `1` untuk menonaktifkan prompt caching hanya untuk model Sonnet                                |
| `DISABLE_PROMPT_CACHING_OPUS`   | Atur ke `1` untuk menonaktifkan prompt caching hanya untuk model Opus                                  |

Variabel lingkungan ini memberi Anda kontrol terperinci atas perilaku prompt caching. Pengaturan global `DISABLE_PROMPT_CACHING` mengambil alih pengaturan spesifik model, memungkinkan Anda dengan cepat menonaktifkan semua caching saat diperlukan. Pengaturan per-model berguna untuk kontrol selektif, seperti saat men-debug model tertentu atau bekerja dengan penyedia cloud yang mungkin memiliki implementasi caching yang berbeda.
