> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurasi model

> Pelajari tentang konfigurasi model Claude Code, termasuk alias model seperti `opusplan`

## Model yang tersedia

Untuk pengaturan `model` di Claude Code, Anda dapat mengonfigurasi salah satu dari:

* Sebuah **alias model**
* Sebuah **nama model**
  * Anthropic API: Sebuah **[nama model](https://platform.claude.com/docs/id/about-claude/models/overview)** lengkap
  * Bedrock: ARN profil inferensi
  * Foundry: nama deployment
  * Vertex: nama versi

<Note>
  `ANTHROPIC_BASE_URL` mengubah tempat permintaan dikirim, bukan model mana yang menjawabnya. Untuk merutekan Claude melalui gateway LLM, lihat [konfigurasi gateway LLM](/id/llm-gateway).
</Note>

### Alias model

Alias model menyediakan cara yang nyaman untuk memilih pengaturan model tanpa perlu mengingat nomor versi yang tepat:

| Alias model      | Perilaku                                                                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Nilai khusus yang menghapus penggantian model apa pun dan kembali ke model yang direkomendasikan untuk jenis akun Anda. Bukan sendiri alias model                          |
| **`best`**       | Menggunakan model yang paling mampu tersedia, saat ini setara dengan `opus`                                                                                                |
| **`sonnet`**     | Menggunakan model Sonnet terbaru untuk tugas coding sehari-hari                                                                                                            |
| **`opus`**       | Menggunakan model Opus terbaru untuk tugas penalaran kompleks                                                                                                              |
| **`haiku`**      | Menggunakan model Haiku yang cepat dan efisien untuk tugas sederhana                                                                                                       |
| **`sonnet[1m]`** | Menggunakan Sonnet dengan [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows#1m-token-context-window) untuk sesi panjang |
| **`opus[1m]`**   | Menggunakan Opus dengan [jendela konteks 1 juta token](https://platform.claude.com/docs/id/build-with-claude/context-windows#1m-token-context-window) untuk sesi panjang   |
| **`opusplan`**   | Mode khusus yang menggunakan `opus` selama Plan Mode, kemudian beralih ke `sonnet` untuk eksekusi                                                                          |

Di Anthropic API dan [Claude Platform on AWS](/id/claude-platform-on-aws), `opus` diselesaikan ke Opus 4.7 dan `sonnet` diselesaikan ke Sonnet 4.6. Di Bedrock, Vertex, dan Foundry, `opus` diselesaikan ke Opus 4.6 dan `sonnet` diselesaikan ke Sonnet 4.5; model yang lebih baru tersedia di penyedia tersebut dengan memilih nama model lengkap secara eksplisit atau mengatur `ANTHROPIC_DEFAULT_OPUS_MODEL` atau `ANTHROPIC_DEFAULT_SONNET_MODEL`.

Alias menunjuk ke versi yang direkomendasikan untuk penyedia Anda dan diperbarui seiring waktu. Untuk menetapkan versi tertentu, gunakan nama model lengkap (misalnya, `claude-opus-4-7`) atau atur variabel lingkungan yang sesuai seperti `ANTHROPIC_DEFAULT_OPUS_MODEL`.

<Note>
  Opus 4.7 memerlukan Claude Code v2.1.111 atau lebih baru. Jalankan `claude update` untuk meningkatkan.
</Note>

### Mengatur model Anda

Anda dapat mengonfigurasi model Anda dengan beberapa cara, yang tercantum dalam urutan prioritas:

1. **Selama sesi** - Gunakan `/model <alias|name>` untuk beralih segera, atau jalankan `/model` tanpa argumen untuk membuka pemilih. Pemilih meminta konfirmasi ketika percakapan memiliki output sebelumnya, karena respons berikutnya membaca ulang riwayat lengkap tanpa konteks cache
2. **Saat startup** - Luncurkan dengan `claude --model <alias|name>`
3. **Variabel lingkungan** - Atur `ANTHROPIC_MODEL=<alias|name>`
4. **Pengaturan** - Konfigurasi secara permanen di file pengaturan Anda menggunakan bidang `model`.

<Note>
  Pilihan `/model` Anda disimpan ke pengaturan pengguna dan bertahan di seluruh restart. Mulai dari v2.1.117, jika `.claude/settings.json` proyek menetapkan model yang berbeda, Claude Code juga menulis pilihan Anda ke `.claude/settings.local.json` sehingga terus berlaku di proyek tersebut setelah restart. Pengaturan yang dikelola memiliki prioritas dan diterapkan kembali pada peluncuran berikutnya.
</Note>

Bendera `--model` dan variabel lingkungan `ANTHROPIC_MODEL` hanya berlaku untuk sesi yang Anda luncurkan dengan mereka dan tidak disimpan. Untuk menjalankan model yang berbeda di terminal yang berbeda pada waktu yang sama, luncurkan masing-masing dengan bendera `--model` miliknya sendiri daripada beralih dengan `/model`.

Ketika model aktif saat startup berasal dari pengaturan proyek atau yang dikelola daripada pilihan Anda sendiri, header startup menunjukkan file pengaturan mana yang menetapkannya. Jalankan `/model` untuk mengganti untuk sesi saat ini.

Contoh penggunaan:

```bash theme={null}
# Mulai dengan Opus
claude --model opus

# Beralih ke Sonnet selama sesi
/model sonnet
```

Contoh file pengaturan:

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Batasi pemilihan model

Administrator enterprise dapat menggunakan `availableModels` dalam [pengaturan terkelola atau kebijakan](/id/settings#settings-files) untuk membatasi model mana yang dapat dipilih pengguna.

Ketika `availableModels` diatur, pengguna tidak dapat beralih ke model yang tidak ada dalam daftar melalui `/model`, flag `--model`, atau variabel lingkungan `ANTHROPIC_MODEL`.

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Perilaku model default

Opsi Default di pemilih model tidak dipengaruhi oleh `availableModels`. Opsi ini selalu tetap tersedia dan mewakili default runtime sistem [berdasarkan tingkat langganan pengguna](#default-model-setting).

Bahkan dengan `availableModels: []`, pengguna masih dapat menggunakan Claude Code dengan model Default untuk tingkat mereka.

### Kontrol model yang dijalankan pengguna

Pengaturan `model` adalah pilihan awal, bukan penegakan. Ini menetapkan model mana yang aktif ketika sesi dimulai, tetapi pengguna masih dapat membuka `/model` dan memilih Default, yang diselesaikan ke default sistem untuk tingkat mereka terlepas dari apa yang `model` ditetapkan.

Untuk sepenuhnya mengontrol pengalaman model, gabungkan tiga pengaturan:

* **`availableModels`**: membatasi model bernama mana yang dapat dialihkan pengguna
* **`model`**: menetapkan pilihan model awal ketika sesi dimulai
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**: mengontrol apa yang diselesaikan opsi Default dan alias `sonnet`, `opus`, dan `haiku`

Contoh ini memulai pengguna di Sonnet 4.5, membatasi pemilih ke Sonnet dan Haiku, dan menetapkan Default untuk diselesaikan ke Sonnet 4.5 daripada rilis terbaru:

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Tanpa blok `env`, pengguna yang memilih Default di pemilih akan mendapatkan rilis Sonnet terbaru, melewati pin versi dalam `model` dan `availableModels`.

### Perilaku penggabungan

Ketika `availableModels` diatur di beberapa tingkat, seperti pengaturan pengguna dan pengaturan proyek, array digabungkan dan dideduplikasi. Untuk memberlakukan allowlist ketat, atur `availableModels` dalam pengaturan terkelola atau kebijakan yang memiliki prioritas tertinggi.

### ID model Mantle

Ketika [endpoint Bedrock Mantle](/id/amazon-bedrock#use-the-mantle-endpoint) diaktifkan, entri dalam `availableModels` yang dimulai dengan `anthropic.` ditambahkan ke pemilih `/model` sebagai opsi kustom dan dirutekan ke endpoint Mantle. Ini adalah pengecualian terhadap pencocokan alias-saja yang dijelaskan dalam [Tetapkan model untuk deployment pihak ketiga](#pin-models-for-third-party-deployments). Pengaturan masih membatasi pemilih ke entri yang tercantum, jadi sertakan alias standar bersama ID Mantle apa pun.

## Perilaku model khusus

### Pengaturan model `default`

Perilaku `default` tergantung pada jenis akun Anda:

* **Max dan Team Premium**: default ke Opus 4.7
* **Pro, Team Standard, Enterprise, dan Anthropic API**: default ke Sonnet 4.6
* **Bedrock, Vertex, dan Foundry**: default ke Sonnet 4.5

Claude Code dapat secara otomatis kembali ke Sonnet jika Anda mencapai ambang penggunaan dengan Opus.

<Note>
  Pada 23 April 2026, model default untuk pengguna Enterprise pay-as-you-go dan Anthropic API akan berubah ke Opus 4.7. Untuk mempertahankan default yang berbeda, atur `ANTHROPIC_MODEL` atau bidang `model` dalam [pengaturan yang dikelola server](/id/server-managed-settings).
</Note>

### Pengaturan model `opusplan`

Alias model `opusplan` menyediakan pendekatan hibrida otomatis:

* **Dalam plan mode** - Menggunakan `opus` untuk penalaran kompleks dan keputusan arsitektur
* **Dalam execution mode** - Secara otomatis beralih ke `sonnet` untuk pembuatan kode dan implementasi

Ini memberi Anda yang terbaik dari kedua dunia: penalaran superior Opus untuk perencanaan, dan efisiensi Sonnet untuk eksekusi.

Fase Opus dalam plan mode berjalan dengan jendela konteks standar 200K. Peningkatan 1M otomatis yang dijelaskan dalam [Konteks diperluas](#extended-context) berlaku untuk pengaturan model `opus` dan tidak memperluas ke `opusplan`.

### Sesuaikan tingkat usaha

[Tingkat usaha](https://platform.claude.com/docs/en/build-with-claude/effort) mengontrol penalaran adaptif, yang memungkinkan model memutuskan apakah dan berapa banyak untuk berpikir pada setiap langkah berdasarkan kompleksitas tugas. Usaha lebih rendah lebih cepat dan lebih murah untuk tugas-tugas langsung, sementara usaha lebih tinggi memberikan penalaran lebih dalam untuk masalah kompleks.

Usaha didukung pada Opus 4.7, Opus 4.6, dan Sonnet 4.6. Tingkat yang tersedia tergantung pada model:

| Model                   | Tingkat                                 |
| :---------------------- | :-------------------------------------- |
| Opus 4.7                | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 dan Sonnet 4.6 | `low`, `medium`, `high`, `max`          |

Jika Anda menetapkan tingkat yang tidak didukung model aktif, Claude Code kembali ke tingkat tertinggi yang didukung pada atau di bawah tingkat yang Anda tetapkan. Misalnya, `xhigh` berjalan sebagai `high` pada Opus 4.6.

Mulai dari v2.1.117, usaha default adalah `xhigh` pada Opus 4.7 dan `high` pada Opus 4.6 dan Sonnet 4.6.

Ketika Anda pertama kali menjalankan Opus 4.7, Claude Code menerapkan `xhigh` bahkan jika Anda sebelumnya menetapkan tingkat usaha yang berbeda untuk Opus 4.6 atau Sonnet 4.6. Jalankan `/effort` lagi untuk memilih tingkat yang berbeda setelah beralih.

`low`, `medium`, `high`, dan `xhigh` bertahan di seluruh sesi. `max` memberikan penalaran paling dalam tanpa batasan pengeluaran token dan berlaku untuk sesi saat ini saja, kecuali ketika diatur melalui variabel lingkungan `CLAUDE_CODE_EFFORT_LEVEL`.

#### Pilih tingkat usaha

Setiap tingkat menukar pengeluaran token terhadap kemampuan. Default cocok untuk sebagian besar tugas coding; sesuaikan ketika Anda menginginkan keseimbangan yang berbeda.

| Tingkat  | Kapan menggunakannya                                                                                                                                                        |
| :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `low`    | Cadangkan untuk tugas pendek, terbatas, sensitif latensi yang tidak sensitif intelijen                                                                                      |
| `medium` | Mengurangi penggunaan token untuk pekerjaan sensitif biaya yang dapat menukar beberapa intelijen                                                                            |
| `high`   | Menyeimbangkan penggunaan token dan intelijen. Gunakan sebagai minimum untuk pekerjaan sensitif intelijen, atau untuk mengurangi pengeluaran token relatif terhadap `xhigh` |
| `xhigh`  | Hasil terbaik untuk sebagian besar tugas coding dan agentic. Default yang direkomendasikan di Opus 4.7                                                                      |
| `max`    | Dapat meningkatkan kinerja pada tugas yang menuntut tetapi mungkin menunjukkan hasil yang berkurang dan rentan terhadap overthinking. Uji sebelum mengadopsi secara luas    |

Skala usaha dikalibrasi per model, jadi nama tingkat yang sama tidak mewakili nilai yang sama di seluruh model.

#### Gunakan ultrathink untuk penalaran mendalam sekali

Sertakan `ultrathink` di mana saja dalam prompt Anda untuk meminta penalaran lebih dalam pada giliran itu tanpa mengubah pengaturan usaha sesi Anda. Claude Code mengenali kata kunci dan menambahkan instruksi dalam konteks. Tingkat usaha yang dikirim ke API tidak berubah. Frasa lain seperti "think", "think hard", dan "think more" dilewatkan sebagai teks prompt biasa dan tidak dikenali sebagai kata kunci.

#### Atur tingkat usaha

Anda dapat mengubah usaha melalui salah satu dari berikut ini:

* **`/effort`**: jalankan `/effort` tanpa argumen untuk membuka slider interaktif, `/effort` diikuti dengan nama tingkat untuk menetapkannya secara langsung, atau `/effort auto` untuk mengatur ulang ke default model
* **Dalam `/model`**: gunakan tombol panah kiri/kanan untuk menyesuaikan slider usaha saat memilih model
* **Flag `--effort`**: teruskan nama tingkat untuk menetapkannya untuk sesi tunggal saat meluncurkan Claude Code
* **Variabel lingkungan**: atur `CLAUDE_CODE_EFFORT_LEVEL` ke nama tingkat atau `auto`
* **Pengaturan**: atur `effortLevel` ke `low`, `medium`, `high`, atau `xhigh` dalam file pengaturan Anda. `max` adalah [hanya sesi](#adjust-effort-level) dan tidak diterima di sini
* **Skill dan subagent frontmatter**: atur `effort` dalam file markdown [skill](/id/skills#frontmatter-reference) atau [subagent](/id/sub-agents#supported-frontmatter-fields) untuk mengganti tingkat usaha ketika skill atau subagent itu berjalan

Variabel lingkungan mengambil alih semua metode lain, kemudian tingkat yang Anda konfigurasi, kemudian default model. Usaha frontmatter berlaku ketika skill atau subagent itu aktif, mengganti tingkat sesi tetapi bukan variabel lingkungan.

Slider usaha muncul dalam `/model` ketika model yang didukung dipilih. Tingkat usaha saat ini juga ditampilkan di sebelah logo dan spinner, misalnya "with low effort", sehingga Anda dapat mengkonfirmasi pengaturan mana yang aktif tanpa membuka `/model`.

#### Penalaran adaptif dan anggaran pemikiran tetap

Penalaran adaptif membuat pemikiran opsional pada setiap langkah, jadi Claude dapat merespons lebih cepat ke prompt rutin dan menyisihkan pemikiran lebih dalam untuk langkah yang mendapat manfaat darinya. Jika Anda ingin Claude berpikir lebih atau kurang sering daripada tingkat saat ini menghasilkan, Anda dapat mengatakan demikian secara langsung dalam prompt Anda atau dalam `CLAUDE.md`; model merespons panduan itu dalam pengaturan usahanya.

Opus 4.7 selalu menggunakan penalaran adaptif. Mode anggaran pemikiran tetap dan `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` tidak berlaku untuk itu.

Di Opus 4.6 dan Sonnet 4.6, Anda dapat mengatur `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` untuk kembali ke anggaran pemikiran tetap sebelumnya yang dikendalikan oleh `MAX_THINKING_TOKENS`. Lihat [variabel lingkungan](/id/env-vars).

### Pemikiran diperluas

Pemikiran diperluas adalah penalaran yang Claude keluarkan sebelum merespons. Pada model yang mendukung [penalaran adaptif](#adjust-effort-level), tingkat usaha adalah kontrol utama untuk berapa banyak pemikiran yang terjadi; pengaturan di bawah ini menghidupkan atau mematikan pemikiran dan mengontrol cara tampilannya.

| Kontrol                         | Cara menetapkannya                                                                                                                                       |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Toggle untuk sesi saat ini      | Tekan `Option+T` di macOS atau `Alt+T` di Windows dan Linux                                                                                              |
| Atur default global             | Jalankan `/config` dan toggle thinking mode. Disimpan sebagai `alwaysThinkingEnabled` dalam `~/.claude/settings.json`                                    |
| Nonaktifkan terlepas dari usaha | Atur [`MAX_THINKING_TOKENS=0`](/id/env-vars). Nilai lain berlaku hanya dengan [anggaran pemikiran tetap](#adaptive-reasoning-and-fixed-thinking-budgets) |

Output pemikiran dilipat secara default. Tekan `Ctrl+O` untuk toggle verbose mode dan lihat penalaran sebagai teks miring abu-abu. Sesi interaktif di Anthropic API menerima blok pemikiran yang diredaksi secara default, jadi atur `showThinkingSummaries: true` dalam [pengaturan](/id/settings) jika Anda menginginkan ringkasan lengkap yang tersedia saat Anda memperluas. Anda dikenakan biaya untuk semua token pemikiran yang dihasilkan, bahkan ketika dilipat atau diredaksi.

### Konteks diperluas

Opus 4.7, Opus 4.6, dan Sonnet 4.6 mendukung [jendela konteks 1 juta token](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) untuk sesi panjang dengan basis kode besar.

Ketersediaan bervariasi menurut model dan paket. Di paket Max, Team, dan Enterprise, Opus secara otomatis ditingkatkan ke konteks 1M tanpa konfigurasi tambahan. Ini berlaku untuk kedua kursi Team Standard dan Team Premium. Sonnet dengan konteks 1M bukan bagian dari peningkatan otomatis dan memerlukan [penggunaan tambahan](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) di setiap paket langganan, termasuk Max.

| Paket                     | Opus dengan konteks 1M                                                                                              | Sonnet dengan konteks 1M                                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Max, Team, dan Enterprise | Disertakan dengan langganan                                                                                         | Memerlukan [penggunaan tambahan](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                       | Memerlukan [penggunaan tambahan](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) | Memerlukan [penggunaan tambahan](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API dan pay-as-you-go     | Akses penuh                                                                                                         | Akses penuh                                                                                                         |

Untuk menonaktifkan konteks 1M sepenuhnya, atur `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Ini menghapus varian model 1M dari pemilih model. Lihat [variabel lingkungan](/id/env-vars).

Jendela konteks 1M menggunakan harga model standar tanpa premium untuk token di luar 200K. Untuk paket di mana konteks diperluas disertakan dengan langganan Anda, penggunaan tetap tercakup oleh langganan Anda. Untuk paket yang mengakses konteks diperluas melalui penggunaan tambahan, token ditagihkan ke penggunaan tambahan.

Jika akun Anda mendukung konteks 1M, opsi muncul di pemilih model (`/model`) dalam versi terbaru Claude Code. Jika Anda tidak melihatnya, coba mulai ulang sesi Anda.

Anda juga dapat menggunakan akhiran `[1m]` dengan alias model atau nama model lengkap:

```bash theme={null}
# Gunakan alias opus[1m] atau sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# Atau tambahkan [1m] ke nama model lengkap
/model claude-opus-4-7[1m]
```

## Memeriksa model Anda saat ini

Anda dapat melihat model mana yang sedang Anda gunakan dengan beberapa cara:

1. Dalam [status line](/id/statusline) (jika dikonfigurasi)
2. Dalam `/status`, yang juga menampilkan informasi akun Anda.

## Tambahkan opsi model kustom

Gunakan `ANTHROPIC_CUSTOM_MODEL_OPTION` untuk menambahkan satu entri kustom ke pemilih `/model` tanpa mengganti alias bawaan. Ini berguna untuk pengujian ID model yang tidak tercantum Claude Code secara default. Untuk deployment gateway LLM, Claude Code dapat mengisi pemilih dari endpoint `/v1/models` gateway ketika `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` diatur, jadi variabel ini diperlukan hanya ketika penemuan dinonaktifkan atau tidak mengembalikan model yang Anda inginkan. Lihat [pemilihan model gateway LLM](/id/llm-gateway#model-selection).

Contoh ini menetapkan ketiga variabel untuk membuat deployment Opus yang dirutekan gateway dapat dipilih:

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-7"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

Entri kustom muncul di bagian bawah pemilih `/model`. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` dan `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` bersifat opsional. Jika dihilangkan, ID model digunakan sebagai nama dan deskripsi default ke `Custom model (<model-id>)`.

Claude Code melewati validasi untuk ID model yang ditetapkan dalam `ANTHROPIC_CUSTOM_MODEL_OPTION`, sehingga Anda dapat menggunakan string apa pun yang diterima endpoint API Anda.

## Variabel lingkungan

Anda dapat menggunakan variabel lingkungan berikut, yang harus berupa **nama model** lengkap (atau setara untuk penyedia API Anda), untuk mengontrol nama model yang dipetakan alias.

| Variabel lingkungan              | Deskripsi                                                                                                                                                                 |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Model yang digunakan untuk `opus`, atau untuk `opusplan` ketika Plan Mode aktif.                                                                                          |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Model yang digunakan untuk `sonnet`, atau untuk `opusplan` ketika Plan Mode tidak aktif.                                                                                  |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Model yang digunakan untuk `haiku`, atau [fungsionalitas latar belakang](/id/costs#background-token-usage)                                                                |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Model yang digunakan untuk semua [subagents](/id/sub-agents#choose-a-model). Mengganti baik parameter `model` per-invocation maupun frontmatter `model` definisi subagent |

Catatan: `ANTHROPIC_SMALL_FAST_MODEL` sudah usang dan digantikan oleh `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Tetapkan model untuk deployment pihak ketiga

Saat menerapkan Claude Code melalui [Bedrock](/id/amazon-bedrock), [Vertex AI](/id/google-vertex-ai), [Foundry](/id/microsoft-foundry), atau [Claude Platform on AWS](/id/claude-platform-on-aws), tetapkan versi model sebelum meluncurkan ke pengguna.

Tanpa penentapan, Claude Code menggunakan alias model (`sonnet`, `opus`, `haiku`) yang diselesaikan ke versi terbaru. Ketika Anthropic merilis model baru yang belum diaktifkan di akun pengguna, pengguna Bedrock dan Vertex AI melihat pemberitahuan dan kembali ke versi sebelumnya untuk sesi itu, sementara pengguna Foundry melihat kesalahan karena Foundry tidak memiliki pemeriksaan startup yang setara.

<Warning>
  Atur ketiga variabel lingkungan model ke ID versi spesifik sebagai bagian dari pengaturan awal Anda. Penentapan memungkinkan Anda mengontrol kapan pengguna Anda pindah ke model baru.
</Warning>

Gunakan variabel lingkungan berikut dengan ID model spesifik versi untuk penyedia Anda:

| Penyedia  | Contoh                                                               |
| :-------- | :------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |

Terapkan pola yang sama untuk `ANTHROPIC_DEFAULT_SONNET_MODEL` dan `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Untuk ID model saat ini dan warisan di semua penyedia, lihat [Ikhtisar Model](https://platform.claude.com/docs/en/about-claude/models/overview). Untuk meningkatkan pengguna ke versi model baru, perbarui variabel lingkungan ini dan terapkan kembali.

Untuk mengaktifkan [konteks diperluas](#extended-context) untuk model yang ditetapkan, tambahkan `[1m]` ke ID model dalam `ANTHROPIC_DEFAULT_OPUS_MODEL` atau `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7[1m]'
```

Akhiran `[1m]` menerapkan jendela konteks 1M ke semua penggunaan alias tersebut, termasuk `opusplan`. Claude Code menghapus akhiran sebelum mengirim ID model ke penyedia Anda. Hanya tambahkan `[1m]` ketika model yang mendasar mendukung konteks 1M, seperti Opus 4.7 atau Sonnet 4.6.

<Note>
  Allowlist `settings.availableModels` masih berlaku saat menggunakan penyedia pihak ketiga. Penyaringan cocok pada alias model (`opus`, `sonnet`, `haiku`), bukan ID model spesifik penyedia.
</Note>

### Sesuaikan tampilan dan kemampuan model yang ditetapkan

Ketika Anda menetapkan model pada penyedia pihak ketiga, ID spesifik penyedia muncul apa adanya di pemilih `/model` dan Claude Code mungkin tidak mengenali fitur mana yang didukung model. Anda dapat mengganti nama tampilan dan mendeklarasikan kemampuan dengan variabel lingkungan pendamping untuk setiap model yang ditetapkan.

Variabel ini berlaku pada penyedia pihak ketiga seperti Bedrock, Vertex AI, dan Foundry. Variabel `_NAME` dan `_DESCRIPTION` juga berlaku ketika `ANTHROPIC_BASE_URL` menunjuk ke [gateway LLM](/id/llm-gateway). Mereka tidak berpengaruh saat menghubungkan langsung ke `api.anthropic.com`.

| Variabel lingkungan                                   | Deskripsi                                                                                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Nama tampilan untuk model Opus yang ditetapkan di pemilih `/model`. Default ke ID model saat tidak diatur                 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Deskripsi tampilan untuk model Opus yang ditetapkan di pemilih `/model`. Default ke `Custom Opus model` saat tidak diatur |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Daftar kemampuan yang dipisahkan koma yang didukung model Opus yang ditetapkan                                            |

Akhiran `_NAME`, `_DESCRIPTION`, dan `_SUPPORTED_CAPABILITIES` yang sama tersedia untuk `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`, dan `ANTHROPIC_CUSTOM_MODEL_OPTION`.

Claude Code mengaktifkan fitur seperti [tingkat usaha](#adjust-effort-level) dan [extended thinking](#extended-thinking) dengan mencocokkan ID model terhadap pola yang dikenal. ID spesifik penyedia seperti ARN Bedrock atau nama deployment kustom sering kali tidak cocok dengan pola ini, meninggalkan fitur yang didukung dinonaktifkan. Atur `_SUPPORTED_CAPABILITIES` untuk memberi tahu Claude Code fitur mana yang benar-benar didukung model:

| Nilai kemampuan        | Mengaktifkan                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `effort`               | [Tingkat usaha](#adjust-effort-level) dan perintah `/effort`                                  |
| `xhigh_effort`         | {/* min-version: 2.1.111 */}Tingkat usaha `xhigh`                                             |
| `max_effort`           | Tingkat usaha `max`                                                                           |
| `thinking`             | [Extended thinking](#extended-thinking)                                                       |
| `adaptive_thinking`    | Penalaran adaptif yang secara dinamis mengalokasikan pemikiran berdasarkan kompleksitas tugas |
| `interleaved_thinking` | Pemikiran antara panggilan alat                                                               |

Ketika `_SUPPORTED_CAPABILITIES` diatur, kemampuan yang tercantum diaktifkan dan kemampuan yang tidak tercantum dinonaktifkan untuk model yang ditetapkan yang cocok. Ketika variabel tidak diatur, Claude Code kembali ke deteksi bawaan berdasarkan ID model.

Contoh ini menetapkan Opus ke ARN model kustom Bedrock, menetapkan nama yang ramah, dan mendeklarasikan kemampuannya:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Ganti ID model per versi

Variabel lingkungan tingkat keluarga di atas mengonfigurasi satu ID model per alias keluarga. Jika Anda perlu memetakan beberapa versi dalam keluarga yang sama ke ID penyedia yang berbeda, gunakan pengaturan `modelOverrides` sebagai gantinya.

`modelOverrides` memetakan ID model Anthropic individual ke string spesifik penyedia yang dikirim Claude Code ke API penyedia Anda. Ketika pengguna memilih model yang dipetakan di pemilih `/model`, Claude Code menggunakan nilai yang Anda konfigurasi alih-alih default bawaan.

Ini memungkinkan administrator enterprise untuk merutekan setiap versi model ke ARN profil inferensi Bedrock tertentu, nama versi Vertex AI, atau nama deployment Foundry untuk tata kelola, alokasi biaya, atau perutean regional.

Atur `modelOverrides` dalam [file pengaturan](/id/settings#settings-files) Anda:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
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

Variabel lingkungan ini memberi Anda kontrol terperinci atas perilaku prompt caching. Pengaturan global `DISABLE_PROMPT_CACHING` mengambil alih pengaturan spesifik model, memungkinkan Anda dengan cepat menonaktifkan semua caching saat diperlukan. Pengaturan per-model berguna untuk kontrol selektif, seperti saat men-debug model tertentu atau bekerja dengan penyedia cloud yang mungkin memiliki implementasi caching berbeda.
