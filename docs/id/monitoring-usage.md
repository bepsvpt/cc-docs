> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Pemantauan

> Pelajari cara mengaktifkan dan mengonfigurasi OpenTelemetry untuk Claude Code.

Lacak penggunaan Claude Code, biaya, dan aktivitas alat di seluruh organisasi Anda dengan mengekspor data telemetri melalui OpenTelemetry (OTel). Claude Code mengekspor metrik sebagai data deret waktu melalui protokol metrik standar, acara melalui protokol log/acara, dan secara opsional distributed traces melalui [protokol traces](#traces-beta). Konfigurasikan backend metrik, log, dan traces Anda agar sesuai dengan persyaratan pemantauan Anda.

## Mulai cepat

Konfigurasikan OpenTelemetry menggunakan variabel lingkungan:

```bash theme={null}
# 1. Aktifkan telemetri
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Pilih pengekspor (keduanya bersifat opsional - konfigurasikan hanya yang Anda butuhkan)
export OTEL_METRICS_EXPORTER=otlp       # Opsi: otlp, prometheus, console, none
export OTEL_LOGS_EXPORTER=otlp          # Opsi: otlp, console, none

# 3. Konfigurasikan titik akhir OTLP (untuk pengekspor OTLP)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Atur autentikasi (jika diperlukan)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Untuk debugging: kurangi interval ekspor
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 detik (default: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 detik (default: 5000ms)

# 6. Jalankan Claude Code
claude
```

<Note>
  Interval ekspor default adalah 60 detik untuk metrik dan 5 detik untuk log. Selama pengaturan, Anda mungkin ingin menggunakan interval yang lebih pendek untuk tujuan debugging. Ingat untuk mengatur ulang ini untuk penggunaan produksi.
</Note>

Untuk opsi konfigurasi lengkap, lihat [spesifikasi OpenTelemetry](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Konfigurasi administrator

Administrator dapat mengonfigurasi pengaturan OpenTelemetry untuk semua pengguna melalui [file pengaturan terkelola](/id/settings#settings-files). Ini memungkinkan kontrol terpusat pengaturan telemetri di seluruh organisasi. Lihat [prioritas pengaturan](/id/settings#settings-precedence) untuk informasi lebih lanjut tentang bagaimana pengaturan diterapkan.

Contoh konfigurasi pengaturan terkelola:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  Pengaturan terkelola dapat didistribusikan melalui MDM (Mobile Device Management) atau solusi manajemen perangkat lainnya. Variabel lingkungan yang ditentukan dalam file pengaturan terkelola memiliki prioritas tinggi dan tidak dapat ditimpa oleh pengguna.
</Note>

## Detail konfigurasi

### Variabel konfigurasi umum

| Variabel Lingkungan                                 | Deskripsi                                                                                                                                                                                                                                                                                                                                                           | Nilai Contoh                                                                                                                           |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Mengaktifkan pengumpulan telemetri (diperlukan)                                                                                                                                                                                                                                                                                                                     | `1`                                                                                                                                    |
| `OTEL_METRICS_EXPORTER`                             | Jenis pengekspor metrik, dipisahkan koma. Gunakan `none` untuk menonaktifkan                                                                                                                                                                                                                                                                                        | `console`, `otlp`, `prometheus`, `none`                                                                                                |
| `OTEL_LOGS_EXPORTER`                                | Jenis pengekspor log/acara, dipisahkan koma. Gunakan `none` untuk menonaktifkan                                                                                                                                                                                                                                                                                     | `console`, `otlp`, `none`                                                                                                              |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protokol untuk pengekspor OTLP, berlaku untuk semua sinyal                                                                                                                                                                                                                                                                                                          | `grpc`, `http/json`, `http/protobuf`                                                                                                   |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | Titik akhir pengumpul OTLP untuk semua sinyal                                                                                                                                                                                                                                                                                                                       | `http://localhost:4317`                                                                                                                |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protokol untuk metrik, menimpa pengaturan umum                                                                                                                                                                                                                                                                                                                      | `grpc`, `http/json`, `http/protobuf`                                                                                                   |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | Titik akhir metrik OTLP, menimpa pengaturan umum                                                                                                                                                                                                                                                                                                                    | `http://localhost:4318/v1/metrics`                                                                                                     |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protokol untuk log, menimpa pengaturan umum                                                                                                                                                                                                                                                                                                                         | `grpc`, `http/json`, `http/protobuf`                                                                                                   |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | Titik akhir log OTLP, menimpa pengaturan umum                                                                                                                                                                                                                                                                                                                       | `http://localhost:4318/v1/logs`                                                                                                        |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Header autentikasi untuk OTLP                                                                                                                                                                                                                                                                                                                                       | `Authorization=Bearer token`                                                                                                           |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Kunci klien untuk autentikasi mTLS                                                                                                                                                                                                                                                                                                                                  | Jalur ke file kunci klien                                                                                                              |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Sertifikat klien untuk autentikasi mTLS                                                                                                                                                                                                                                                                                                                             | Jalur ke file sertifikat klien                                                                                                         |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Interval ekspor dalam milidetik (default: 60000)                                                                                                                                                                                                                                                                                                                    | `5000`, `60000`                                                                                                                        |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Interval ekspor log dalam milidetik (default: 5000)                                                                                                                                                                                                                                                                                                                 | `1000`, `10000`                                                                                                                        |
| `OTEL_LOG_USER_PROMPTS`                             | Aktifkan pencatatan konten prompt pengguna (default: dinonaktifkan)                                                                                                                                                                                                                                                                                                 | `1` untuk mengaktifkan                                                                                                                 |
| `OTEL_LOG_TOOL_DETAILS`                             | Aktifkan pencatatan parameter alat dan argumen input dalam acara alat dan atribut span trace: perintah Bash, nama server MCP dan alat, nama skill, dan input alat. Juga mengaktifkan nama perintah custom, plugin, dan MCP pada acara `user_prompt` (default: dinonaktifkan)                                                                                        | `1` untuk mengaktifkan                                                                                                                 |
| `OTEL_LOG_TOOL_CONTENT`                             | Aktifkan pencatatan konten input dan output alat dalam acara span (default: dinonaktifkan). Memerlukan [tracing](#traces-beta). Konten dipotong pada 60 KB                                                                                                                                                                                                          | `1` untuk mengaktifkan                                                                                                                 |
| `OTEL_LOG_RAW_API_BODIES`                           | Emit badan permintaan dan respons JSON API Anthropic Messages lengkap sebagai acara log `api_request_body` / `api_response_body` (default: dinonaktifkan). Badan mencakup seluruh riwayat percakapan. Mengaktifkan ini menyiratkan persetujuan untuk semua yang akan diungkapkan oleh `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, dan `OTEL_LOG_TOOL_CONTENT` | `1` untuk badan inline dipotong pada 60 KB, atau `file:<dir>` untuk badan tidak dipotong di disk dengan pointer `body_ref` dalam acara |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Preferensi temporalitas metrik (default: `delta`). Atur ke `cumulative` jika backend Anda mengharapkan temporalitas kumulatif                                                                                                                                                                                                                                       | `delta`, `cumulative`                                                                                                                  |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Interval untuk menyegarkan header dinamis (default: 1740000ms / 29 menit)                                                                                                                                                                                                                                                                                           | `900000`                                                                                                                               |

### Kontrol kardinalitas metrik

Variabel lingkungan berikut mengontrol atribut mana yang disertakan dalam metrik untuk mengelola kardinalitas:

| Variabel Lingkungan                 | Deskripsi                                                             | Nilai Default | Contoh untuk Menonaktifkan |
| ----------------------------------- | --------------------------------------------------------------------- | ------------- | -------------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Sertakan atribut session.id dalam metrik                              | `true`        | `false`                    |
| `OTEL_METRICS_INCLUDE_VERSION`      | Sertakan atribut app.version dalam metrik                             | `false`       | `true`                     |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Sertakan atribut user.account\_uuid dan user.account\_id dalam metrik | `true`        | `false`                    |

Variabel-variabel ini membantu mengontrol kardinalitas metrik, yang mempengaruhi persyaratan penyimpanan dan kinerja kueri di backend metrik Anda. Kardinalitas yang lebih rendah umumnya berarti kinerja yang lebih baik dan biaya penyimpanan yang lebih rendah tetapi data yang kurang granular untuk analisis.

### Traces (beta)

Distributed tracing mengekspor spans yang menghubungkan setiap prompt pengguna ke permintaan API dan eksekusi alat yang dipicunya, sehingga Anda dapat melihat permintaan lengkap sebagai satu trace di backend tracing Anda.

Tracing dimatikan secara default. Untuk mengaktifkannya, atur `CLAUDE_CODE_ENABLE_TELEMETRY=1` dan `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, kemudian atur `OTEL_TRACES_EXPORTER` untuk memilih tempat spans dikirim. Traces menggunakan kembali [konfigurasi OTLP umum](#common-configuration-variables) untuk titik akhir, protokol, dan header.

| Variabel Lingkungan                   | Deskripsi                                                                          | Nilai Contoh                         |
| ------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Aktifkan span tracing (diperlukan). `ENABLE_ENHANCED_TELEMETRY_BETA` juga diterima | `1`                                  |
| `OTEL_TRACES_EXPORTER`                | Jenis pengekspor traces, dipisahkan koma. Gunakan `none` untuk menonaktifkan       | `console`, `otlp`, `none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | Protokol untuk traces, menimpa `OTEL_EXPORTER_OTLP_PROTOCOL`                       | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | Titik akhir traces OTLP, menimpa `OTEL_EXPORTER_OTLP_ENDPOINT`                     | `http://localhost:4318/v1/traces`    |
| `OTEL_TRACES_EXPORT_INTERVAL`         | Interval ekspor batch span dalam milidetik (default: 5000)                         | `1000`, `10000`                      |

Spans menyunting teks prompt pengguna, detail input alat, dan konten alat secara default. Atur `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1`, dan `OTEL_LOG_TOOL_CONTENT=1` untuk menyertakannya.

Saat tracing aktif, subproses Bash dan PowerShell secara otomatis mewarisi variabel lingkungan `TRACEPARENT` yang berisi konteks trace W3C dari span eksekusi alat yang aktif. Ini memungkinkan subproses apa pun yang membaca `TRACEPARENT` untuk membuat parent spans-nya di bawah trace yang sama, memungkinkan distributed tracing end-to-end melalui skrip dan perintah yang dijalankan Claude.

Dalam sesi Agent SDK dan non-interaktif yang dimulai dengan `-p`, Claude Code juga membaca `TRACEPARENT` dan `TRACESTATE` dari lingkungannya sendiri saat memulai setiap span interaksi. Ini memungkinkan proses embedding untuk melewatkan konteks trace W3C aktifnya ke dalam subproses sehingga spans Claude Code muncul sebagai anak dari distributed trace pemanggil. Sesi interaktif mengabaikan `TRACEPARENT` inbound untuk menghindari secara tidak sengaja mewarisi nilai ambient dari lingkungan CI atau container.

#### Hierarki span

Setiap prompt pengguna memulai span root `claude_code.interaction`. Panggilan API, panggilan alat, dan eksekusi hook dicatat sebagai anak-anaknya. Spans alat memiliki dua span anak mereka sendiri: satu untuk waktu yang dihabiskan menunggu keputusan izin dan satu untuk eksekusi itu sendiri. Ketika alat Task menghasilkan subagent, spans API dan alat subagent bersarang di bawah span `claude_code.tool` induk.

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (memerlukan detailed beta tracing)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (Task tool) subagent claude_code.llm_request / claude_code.tool spans
```

Dalam sesi Agent SDK dan `claude -p`, `claude_code.interaction` itu sendiri menjadi anak dari span pemanggil saat `TRACEPARENT` diatur dalam lingkungan.

#### Atribut span

Setiap span membawa [atribut standar](#standard-attributes) ditambah atribut `span.type` yang cocok dengan namanya. Tabel di bawah mencantumkan atribut tambahan yang diatur pada setiap span. Spans `llm_request`, `tool.execution`, dan `hook` menetapkan status OpenTelemetry `ERROR` saat mereka mencatat kegagalan; span lainnya selalu berakhir dengan status `UNSET`.

**`claude_code.interaction`**

| Atribut                   | Deskripsi                                                  | Gated by                |
| ------------------------- | ---------------------------------------------------------- | ----------------------- |
| `user_prompt`             | Teks prompt. Nilai adalah `<REDACTED>` kecuali gate diatur | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length`      | Panjang prompt dalam karakter                              |                         |
| `interaction.sequence`    | Penghitung berbasis 1 dari interaksi dalam sesi ini        |                         |
| `interaction.duration_ms` | Durasi wall-clock dari giliran                             |                         |

**`claude_code.llm_request`**

| Atribut                          | Deskripsi                                                                                                               | Gated by |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------- |
| `model`                          | Pengidentifikasi model                                                                                                  |          |
| `gen_ai.system`                  | Selalu `anthropic`. Konvensi semantik GenAI OpenTelemetry                                                               |          |
| `gen_ai.request.model`           | Nilai yang sama dengan `model`. Konvensi semantik GenAI OpenTelemetry                                                   |          |
| `query_source`                   | Subsistem yang mengeluarkan permintaan, seperti `repl_main_thread` atau nama subagent                                   |          |
| `speed`                          | `fast` atau `normal`                                                                                                    |          |
| `llm_request.context`            | `interaction`, `tool`, atau `standalone` tergantung pada span induk                                                     |          |
| `duration_ms`                    | Durasi wall-clock termasuk retry                                                                                        |          |
| `ttft_ms`                        | Waktu ke token pertama dalam milidetik                                                                                  |          |
| `input_tokens`                   | Jumlah token input dari blok penggunaan API                                                                             |          |
| `output_tokens`                  | Jumlah token output                                                                                                     |          |
| `cache_read_tokens`              | Token yang dibaca dari prompt cache                                                                                     |          |
| `cache_creation_tokens`          | Token yang ditulis ke prompt cache                                                                                      |          |
| `request_id`                     | ID permintaan API Anthropic dari header respons `request-id`                                                            |          |
| `gen_ai.response.id`             | Nilai yang sama dengan `request_id`. Konvensi semantik GenAI OpenTelemetry                                              |          |
| `client_request_id`              | `x-client-request-id` yang dihasilkan klien dari upaya terakhir                                                         |          |
| `attempt`                        | Total upaya yang dilakukan untuk permintaan ini                                                                         |          |
| `success`                        | `true` atau `false`                                                                                                     |          |
| `status_code`                    | Kode status HTTP saat permintaan gagal                                                                                  |          |
| `error`                          | Pesan kesalahan saat permintaan gagal                                                                                   |          |
| `response.has_tool_call`         | `true` saat respons berisi blok tool-use                                                                                |          |
| `stop_reason`                    | API response `stop_reason`, seperti `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn`, atau `refusal` |          |
| `gen_ai.response.finish_reasons` | Nilai yang sama dengan `stop_reason`, dibungkus dalam array string. Konvensi semantik GenAI OpenTelemetry               |          |

Setiap upaya retry juga dicatat sebagai acara span `gen_ai.request.attempt` dengan atribut `attempt` dan `client_request_id`.

**`claude_code.tool`**

| Atribut         | Deskripsi                                           | Gated by                |
| --------------- | --------------------------------------------------- | ----------------------- |
| `tool_name`     | Nama alat                                           |                         |
| `duration_ms`   | Durasi wall-clock termasuk tunggu izin dan eksekusi |                         |
| `result_tokens` | Ukuran token perkiraan dari hasil alat              |                         |
| `file_path`     | Jalur file target untuk alat Read, Edit, dan Write  | `OTEL_LOG_TOOL_DETAILS` |
| `full_command`  | String perintah untuk alat Bash                     | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name`    | Nama skill untuk alat Skill                         | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Jenis subagent untuk alat Task                      | `OTEL_LOG_TOOL_DETAILS` |

Saat `OTEL_LOG_TOOL_CONTENT=1`, span ini juga mencatat acara span `tool.output` yang atributnya berisi badan input dan output alat, dipotong pada 60 KB per atribut.

**`claude_code.tool.blocked_on_user`**

| Atribut       | Deskripsi                                                                        | Gated by |
| ------------- | -------------------------------------------------------------------------------- | -------- |
| `duration_ms` | Waktu yang dihabiskan menunggu keputusan izin                                    |          |
| `decision`    | `accept` atau `reject`                                                           |          |
| `source`      | Sumber keputusan, cocok dengan acara [Tool decision event](#tool-decision-event) |          |

**`claude_code.tool.execution`**

| Atribut       | Deskripsi                                                                                                                                                 | Gated by                |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `duration_ms` | Waktu yang dihabiskan menjalankan badan alat                                                                                                              |                         |
| `success`     | `true` atau `false`                                                                                                                                       |                         |
| `error`       | String kategori kesalahan saat eksekusi gagal, seperti `Error:ENOENT` atau `ShellError`. Berisi pesan kesalahan lengkap sebagai gantinya saat gate diatur | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**

Span ini dipancarkan hanya saat detailed beta tracing aktif, yang memerlukan `ENABLE_BETA_TRACING_DETAILED=1` dan `BETA_TRACING_ENDPOINT` selain konfigurasi pengekspor trace di atas. Dalam sesi CLI interaktif, ini juga memerlukan organisasi Anda untuk berada dalam daftar putih untuk fitur ini. Sesi Agent SDK dan non-interaktif `-p` tidak gated. Ini tidak dipancarkan saat hanya `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` yang diatur.

| Atribut                  | Deskripsi                                         | Gated by                |
| ------------------------ | ------------------------------------------------- | ----------------------- |
| `hook_event`             | Jenis acara hook, seperti `PreToolUse`            |                         |
| `hook_name`              | Nama hook lengkap, seperti `PreToolUse:Write`     |                         |
| `num_hooks`              | Jumlah perintah hook yang cocok dieksekusi        |                         |
| `hook_definitions`       | Konfigurasi hook yang diserialisasi JSON          | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms`            | Durasi wall-clock dari semua hook yang cocok      |                         |
| `num_success`            | Jumlah hook yang selesai dengan sukses            |                         |
| `num_blocking`           | Jumlah hook yang mengembalikan keputusan blocking |                         |
| `num_non_blocking_error` | Jumlah hook yang gagal tanpa blocking             |                         |
| `num_cancelled`          | Jumlah hook yang dibatalkan sebelum selesai       |                         |

<Note>
  Atribut tambahan yang mengandung konten seperti `new_context`, `system_prompt_preview`, `user_system_prompt`, `tool_input`, dan `response.model_output` dipancarkan hanya saat detailed beta tracing aktif. Mereka bukan bagian dari skema span yang stabil. `user_system_prompt` juga memerlukan `OTEL_LOG_USER_PROMPTS=1`. Ini membawa hanya teks prompt sistem yang Anda berikan melalui opsi SDK `systemPrompt` atau flag `--system-prompt` dan `--append-system-prompt`, dipotong pada 60 KB, dan dipancarkan sekali per sesi daripada per permintaan.
</Note>

### Header dinamis

Untuk lingkungan perusahaan yang memerlukan autentikasi dinamis, Anda dapat mengonfigurasi skrip untuk menghasilkan header secara dinamis:

#### Konfigurasi pengaturan

Tambahkan ke `.claude/settings.json` Anda:

```json theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Persyaratan skrip

Skrip harus menampilkan JSON yang valid dengan pasangan kunci-nilai string yang mewakili header HTTP:

```bash theme={null}
#!/bin/bash
# Contoh: Header ganda
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Perilaku penyegaran

Skrip pembantu header berjalan saat startup dan secara berkala setelahnya untuk mendukung penyegaran token. Secara default, skrip berjalan setiap 29 menit. Sesuaikan interval dengan variabel lingkungan `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Dukungan organisasi multi-tim

Organisasi dengan beberapa tim atau departemen dapat menambahkan atribut khusus untuk membedakan antara kelompok yang berbeda menggunakan variabel lingkungan `OTEL_RESOURCE_ATTRIBUTES`:

```bash theme={null}
# Tambahkan atribut khusus untuk identifikasi tim
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Atribut khusus ini akan disertakan dalam semua metrik dan acara, memungkinkan Anda untuk:

* Filter metrik berdasarkan tim atau departemen
* Lacak biaya per pusat biaya
* Buat dasbor khusus tim
* Atur peringatan untuk tim tertentu

<Warning>
  **Persyaratan pemformatan penting untuk OTEL\_RESOURCE\_ATTRIBUTES:**

  Variabel lingkungan `OTEL_RESOURCE_ATTRIBUTES` menggunakan pasangan kunci=nilai yang dipisahkan koma dengan persyaratan pemformatan yang ketat:

  * **Tidak ada spasi yang diizinkan**: Nilai tidak dapat berisi spasi. Misalnya, `user.organizationName=My Company` tidak valid
  * **Format**: Harus berupa pasangan kunci=nilai yang dipisahkan koma: `key1=value1,key2=value2`
  * **Karakter yang diizinkan**: Hanya karakter US-ASCII yang tidak termasuk karakter kontrol, spasi, tanda kutip ganda, koma, titik koma, dan garis miring terbalik
  * **Karakter khusus**: Karakter di luar rentang yang diizinkan harus dikodekan persen

  **Contoh:**

  ```bash theme={null}
  # ❌ Tidak valid - berisi spasi
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Valid - gunakan garis bawah atau camelCase sebagai gantinya
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Valid - kodekan persen karakter khusus jika diperlukan
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Catatan: membungkus nilai dalam tanda kutip tidak menghindari spasi. Misalnya, `org.name="My Company"` menghasilkan nilai literal `"My Company"` (dengan tanda kutip disertakan), bukan `My Company`.
</Warning>

### Konfigurasi contoh

Atur variabel lingkungan ini sebelum menjalankan `claude`. Setiap blok menunjukkan konfigurasi lengkap untuk pengekspor atau skenario penerapan yang berbeda:

```bash theme={null}
# Debugging konsol (interval 1 detik)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Pengekspor ganda
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Titik akhir/backend berbeda untuk metrik dan log
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Hanya metrik (tanpa acara/log)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Hanya acara/log (tanpa metrik)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Metrik dan acara yang tersedia

### Atribut standar

Semua metrik dan acara berbagi atribut standar ini:

| Atribut             | Deskripsi                                                                                                              | Dikendalikan Oleh                                   |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `session.id`        | Pengidentifikasi sesi unik                                                                                             | `OTEL_METRICS_INCLUDE_SESSION_ID` (default: true)   |
| `app.version`       | Versi Claude Code saat ini                                                                                             | `OTEL_METRICS_INCLUDE_VERSION` (default: false)     |
| `organization.id`   | UUID organisasi (saat diautentikasi)                                                                                   | Selalu disertakan saat tersedia                     |
| `user.account_uuid` | UUID akun (saat diautentikasi)                                                                                         | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true) |
| `user.account_id`   | ID akun dalam format yang ditandai sesuai dengan API admin Anthropic (saat diautentikasi), seperti `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true) |
| `user.id`           | Pengidentifikasi perangkat/instalasi anonim, dihasilkan per instalasi Claude Code                                      | Selalu disertakan                                   |
| `user.email`        | Alamat email pengguna (saat diautentikasi melalui OAuth)                                                               | Selalu disertakan saat tersedia                     |
| `terminal.type`     | Jenis terminal, seperti `iTerm.app`, `vscode`, `cursor`, atau `tmux`                                                   | Selalu disertakan saat terdeteksi                   |

Acara juga menyertakan atribut berikut. Ini tidak pernah dilampirkan pada metrik karena akan menyebabkan kardinalitas tak terbatas:

* `prompt.id`: UUID yang menghubungkan prompt pengguna dengan semua acara berikutnya hingga prompt berikutnya. Lihat [Atribut korelasi acara](#event-correlation-attributes).
* `workspace.host_paths`: direktori ruang kerja host yang dipilih di aplikasi desktop, sebagai array string

### Metrik

Claude Code mengekspor metrik berikut:

| Nama Metrik                           | Deskripsi                                  | Unit   |
| ------------------------------------- | ------------------------------------------ | ------ |
| `claude_code.session.count`           | Jumlah sesi CLI yang dimulai               | count  |
| `claude_code.lines_of_code.count`     | Jumlah baris kode yang dimodifikasi        | count  |
| `claude_code.pull_request.count`      | Jumlah permintaan tarik yang dibuat        | count  |
| `claude_code.commit.count`            | Jumlah komit git yang dibuat               | count  |
| `claude_code.cost.usage`              | Biaya sesi Claude Code                     | USD    |
| `claude_code.token.usage`             | Jumlah token yang digunakan                | tokens |
| `claude_code.code_edit_tool.decision` | Jumlah keputusan izin alat pengeditan kode | count  |
| `claude_code.active_time.total`       | Total waktu aktif dalam detik              | s      |

### Detail metrik

Setiap metrik mencakup atribut standar yang tercantum di atas. Metrik dengan atribut khusus konteks tambahan dicatat di bawah ini.

#### Penghitung sesi

Ditingkatkan pada awal setiap sesi.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `start_type`: Bagaimana sesi dimulai. Salah satu dari `"fresh"`, `"resume"`, atau `"continue"`

#### Penghitung baris kode

Ditingkatkan saat kode ditambahkan atau dihapus.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `type`: (`"added"`, `"removed"`)

#### Penghitung permintaan tarik

Ditingkatkan saat membuat permintaan tarik melalui Claude Code.

**Atribut**:

* Semua [atribut standar](#standard-attributes)

#### Penghitung komit

Ditingkatkan saat membuat komit git melalui Claude Code.

**Atribut**:

* Semua [atribut standar](#standard-attributes)

#### Penghitung biaya

Ditingkatkan setelah setiap permintaan API.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `model`: Pengidentifikasi model (misalnya, "claude-sonnet-4-6")
* `query_source`: Kategori subsistem yang mengeluarkan permintaan. Salah satu dari `"main"`, `"subagent"`, atau `"auxiliary"`
* `speed`: `"fast"` saat permintaan menggunakan mode cepat. Tidak ada sebaliknya
* `effort`: [Tingkat effort](/id/model-config#adjust-effort-level) yang diterapkan pada permintaan: `"low"`, `"medium"`, `"high"`, `"xhigh"`, atau `"max"`. Tidak ada saat model tidak mendukung effort.

#### Penghitung token

Ditingkatkan setelah setiap permintaan API.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Pengidentifikasi model (misalnya, "claude-sonnet-4-6")
* `query_source`: Kategori subsistem yang mengeluarkan permintaan. Salah satu dari `"main"`, `"subagent"`, atau `"auxiliary"`
* `speed`: `"fast"` saat permintaan menggunakan mode cepat. Tidak ada sebaliknya
* `effort`: [Tingkat effort](/id/model-config#adjust-effort-level) yang diterapkan pada permintaan. Lihat [Penghitung biaya](#cost-counter) untuk detail.

#### Penghitung keputusan alat pengeditan kode

Ditingkatkan saat pengguna menerima atau menolak penggunaan alat Edit, Write, atau NotebookEdit.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `tool_name`: Nama alat (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Keputusan pengguna (`"accept"`, `"reject"`)
* `source`: Sumber keputusan. Salah satu dari `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, atau `"user_reject"`. Lihat [Acara keputusan alat](#tool-decision-event) untuk mengetahui apa arti setiap nilai.
* `language`: Bahasa pemrograman file yang diedit, seperti `"TypeScript"`, `"Python"`, `"JavaScript"`, atau `"Markdown"`. Mengembalikan `"unknown"` untuk ekstensi file yang tidak dikenali.

#### Penghitung waktu aktif

Melacak waktu aktual yang dihabiskan secara aktif menggunakan Claude Code, tidak termasuk waktu idle. Metrik ini ditingkatkan selama interaksi pengguna (mengetik, membaca respons) dan selama pemrosesan CLI (eksekusi alat, pembuatan respons AI).

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `type`: `"user"` untuk interaksi keyboard, `"cli"` untuk eksekusi alat dan respons AI

### Acara

Claude Code mengekspor acara berikut melalui log/acara OpenTelemetry (saat `OTEL_LOGS_EXPORTER` dikonfigurasi):

#### Atribut korelasi acara

Saat pengguna mengirimkan prompt, Claude Code dapat membuat beberapa panggilan API dan menjalankan beberapa alat. Atribut `prompt.id` memungkinkan Anda menghubungkan semua acara tersebut kembali ke prompt tunggal yang memicunya.

| Atribut     | Deskripsi                                                                                                      |
| ----------- | -------------------------------------------------------------------------------------------------------------- |
| `prompt.id` | Pengidentifikasi UUID v4 yang menghubungkan semua acara yang dihasilkan saat memproses prompt pengguna tunggal |

Untuk melacak semua aktivitas yang dipicu oleh prompt tunggal, filter acara Anda berdasarkan nilai `prompt.id` tertentu. Ini mengembalikan acara user\_prompt, acara api\_request apa pun, dan acara tool\_result apa pun yang terjadi saat memproses prompt tersebut.

<Note>
  `prompt.id` sengaja dikecualikan dari metrik karena setiap prompt menghasilkan ID unik, yang akan membuat jumlah deret waktu terus bertambah. Gunakan untuk analisis tingkat acara dan jejak audit saja.
</Note>

#### Acara prompt pengguna

Dicatat saat pengguna mengirimkan prompt.

**Nama Acara**: `claude_code.user_prompt`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `prompt_length`: Panjang prompt
* `prompt`: Konten prompt (diredaksi secara default, aktifkan dengan `OTEL_LOG_USER_PROMPTS=1`)
* `command_name`: Nama perintah saat prompt memanggil satu. Nama perintah built-in dan bundled seperti `compact` atau `debug` dipancarkan apa adanya; alias seperti `reset` dipancarkan sebagai yang diketik daripada nama kanonik. Nama perintah custom, plugin, dan MCP runtuh menjadi `custom` atau `mcp` kecuali `OTEL_LOG_TOOL_DETAILS=1` diatur
* `command_source`: Asal perintah saat ada: `builtin`, `custom`, atau `mcp`. Perintah yang disediakan plugin melaporkan sebagai `custom`

#### Acara hasil alat

Dicatat saat alat menyelesaikan eksekusi.

**Nama Acara**: `claude_code.tool_result`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `tool_name`: Nama alat
* `tool_use_id`: Pengidentifikasi unik untuk invokasi alat ini. Cocok dengan `tool_use_id` yang diteruskan ke hooks, memungkinkan korelasi antara acara OTel dan data yang ditangkap hook.
* `success`: `"true"` atau `"false"`
* `duration_ms`: Waktu eksekusi dalam milidetik
* `error_type`: String kategori kesalahan saat alat gagal, seperti `"Error:ENOENT"` atau `"ShellError"`
* `error` (saat `OTEL_LOG_TOOL_DETAILS=1`): Pesan kesalahan lengkap saat alat gagal
* `decision_type`: Baik `"accept"` atau `"reject"`
* `decision_source`: Sumber keputusan. Salah satu dari `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, atau `"user_reject"`. Lihat [Acara keputusan alat](#tool-decision-event) untuk mengetahui apa arti setiap nilai.
* `tool_input_size_bytes`: Ukuran input alat yang diserialisasi JSON dalam byte
* `tool_result_size_bytes`: Ukuran hasil alat dalam byte
* `mcp_server_scope`: Pengidentifikasi cakupan server MCP (untuk alat MCP)
* `tool_parameters` (saat `OTEL_LOG_TOOL_DETAILS=1`): String JSON yang berisi parameter khusus alat:
  * Untuk alat Bash: mencakup `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox`, dan `git_commit_id` (SHA komit, saat perintah `git commit` berhasil)
  * Untuk alat MCP: mencakup `mcp_server_name`, `mcp_tool_name`
  * Untuk alat Skill: mencakup `skill_name`
  * Untuk alat Task: mencakup `subagent_type`
* `tool_input` (saat `OTEL_LOG_TOOL_DETAILS=1`): Argumen alat yang diserialisasi JSON. Nilai individual di atas 512 karakter dipotong, dan muatan penuh dibatasi hingga \~4 K karakter. Berlaku untuk semua alat termasuk alat MCP.

#### Acara permintaan API

Dicatat untuk setiap permintaan API ke Claude.

**Nama Acara**: `claude_code.api_request`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `model`: Model yang digunakan (misalnya, "claude-sonnet-4-6")
* `cost_usd`: Biaya perkiraan dalam USD
* `duration_ms`: Durasi permintaan dalam milidetik
* `input_tokens`: Jumlah token input
* `output_tokens`: Jumlah token output
* `cache_read_tokens`: Jumlah token yang dibaca dari cache
* `cache_creation_tokens`: Jumlah token yang digunakan untuk pembuatan cache
* `request_id`: ID permintaan API Anthropic dari header `request-id` respons, seperti `"req_011..."`. Hadir hanya saat API mengembalikan satu.
* `speed`: `"fast"` atau `"normal"`, menunjukkan apakah mode cepat aktif
* `query_source`: Subsistem yang mengeluarkan permintaan, seperti `"repl_main_thread"`, `"compact"`, atau nama subagent
* `effort`: [Tingkat effort](/id/model-config#adjust-effort-level) yang diterapkan pada permintaan: `"low"`, `"medium"`, `"high"`, `"xhigh"`, atau `"max"`. Tidak ada saat model tidak mendukung effort.

#### Acara kesalahan API

Dicatat saat permintaan API ke Claude gagal.

**Nama Acara**: `claude_code.api_error`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `model`: Model yang digunakan (misalnya, "claude-sonnet-4-6")
* `error`: Pesan kesalahan
* `status_code`: Kode status HTTP sebagai angka. Tidak ada untuk kesalahan non-HTTP seperti kegagalan koneksi.
* `duration_ms`: Durasi permintaan dalam milidetik
* `attempt`: Jumlah total upaya yang dilakukan, termasuk permintaan awal (`1` berarti tidak ada retry yang terjadi)
* `request_id`: ID permintaan API Anthropic dari header `request-id` respons, seperti `"req_011..."`. Hadir hanya saat API mengembalikan satu.
* `speed`: `"fast"` atau `"normal"`, menunjukkan apakah mode cepat aktif
* `query_source`: Subsistem yang mengeluarkan permintaan, seperti `"repl_main_thread"`, `"compact"`, atau nama subagent
* `effort`: [Tingkat effort](/id/model-config#adjust-effort-level) yang diterapkan pada permintaan. Tidak ada saat model tidak mendukung effort.

#### Acara badan permintaan API

Dicatat untuk setiap upaya permintaan API saat `OTEL_LOG_RAW_API_BODIES` diatur. Satu acara dipancarkan per upaya, jadi retry dengan parameter yang disesuaikan masing-masing menghasilkan acara mereka sendiri.

**Nama Acara**: `claude_code.api_request_body`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"api_request_body"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `body`: Parameter permintaan Messages API yang diserialisasi JSON (system prompt, messages, tools, dll.), dipotong pada 60 KB. Konten extended-thinking dalam giliran asisten sebelumnya diredaksi. Dipancarkan hanya dalam mode inline (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Jalur absolut ke file `<dir>/<uuid>.request.json` yang berisi badan yang tidak dipotong. Dipancarkan hanya dalam mode file (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Panjang badan yang tidak dipotong. Byte UTF-8 saat `OTEL_LOG_RAW_API_BODIES=file:<dir>`, atau unit kode UTF-16 saat `=1`
* `body_truncated`: `"true"` saat pemotongan inline terjadi. Tidak ada dalam mode file dan saat tidak ada pemotongan yang terjadi.
* `model`: Pengidentifikasi model dari parameter permintaan
* `query_source`: Subsistem yang mengeluarkan permintaan (misalnya, `"compact"`)

#### Acara badan respons API

Dicatat untuk setiap respons API yang berhasil saat `OTEL_LOG_RAW_API_BODIES` diatur.

**Nama Acara**: `claude_code.api_response_body`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"api_response_body"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `body`: Respons Messages API yang diserialisasi JSON (id, content blocks, usage, stop reason), dipotong pada 60 KB. Konten extended-thinking diredaksi. Dipancarkan hanya dalam mode inline (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Jalur absolut ke file `<dir>/<request_id>.response.json` yang berisi badan yang tidak dipotong. Dipancarkan hanya dalam mode file (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Panjang badan yang tidak dipotong. Byte UTF-8 saat `OTEL_LOG_RAW_API_BODIES=file:<dir>`, atau unit kode UTF-16 saat `=1`
* `body_truncated`: `"true"` saat pemotongan inline terjadi. Tidak ada dalam mode file dan saat tidak ada pemotongan yang terjadi.
* `model`: Pengidentifikasi model
* `query_source`: Subsistem yang mengeluarkan permintaan
* `request_id`: ID permintaan API Anthropic dari header `request-id` respons, seperti `"req_011..."`. Hadir hanya saat API mengembalikan satu.

#### Acara keputusan alat

Dicatat saat keputusan izin alat dibuat (terima/tolak).

**Nama Acara**: `claude_code.tool_decision`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `tool_name`: Nama alat (misalnya, "Read", "Edit", "Write", "NotebookEdit")
* `tool_use_id`: Pengidentifikasi unik untuk invokasi alat ini. Cocok dengan `tool_use_id` yang diteruskan ke hooks, memungkinkan korelasi antara acara OTel dan data yang ditangkap hook.
* `decision`: Baik `"accept"` atau `"reject"`
* `source`: Sumber keputusan:
  * `"config"`: Diputuskan secara otomatis tanpa diminta, berdasarkan pengaturan proyek, kebijakan terkelola perusahaan, flag `--allowedTools` atau `--disallowedTools`, mode izin aktif, atau karena alat itu aman secara inheren.
  * `"hook"`: Hook `PreToolUse` atau `PermissionRequest` mengembalikan keputusan.
  * `"user_permanent"`: Dipancarkan saat pengguna memilih "Selalu izinkan" saat diminta, menyimpan aturan ke pengaturan pribadi mereka. Juga dipancarkan untuk panggilan nanti yang cocok dengan aturan tersimpan itu. Diperlakukan sebagai penerimaan.
  * `"user_temporary"`: Dipancarkan saat pengguna memilih "Ya" atau "Ya, untuk sesi ini" saat diminta, tanpa menyimpan aturan. Juga dipancarkan untuk panggilan nanti dalam sesi yang sama yang cocok dengan izin berskop sesi itu. Diperlakukan sebagai penerimaan.
  * `"user_abort"`: Dipancarkan saat pengguna menutup prompt izin tanpa menjawab. Diperlakukan sebagai penolakan.
  * `"user_reject"`: Dipancarkan saat pengguna memilih "Tidak" saat diminta, atau panggilan cocok dengan aturan penolakan dalam pengaturan pribadi mereka. Diperlakukan sebagai penolakan.

#### Acara mode izin berubah

Dicatat saat mode izin berubah, misalnya dari siklus Shift+Tab, keluar dari plan mode, atau pemeriksaan gate mode otomatis.

**Nama Acara**: `claude_code.permission_mode_changed`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"permission_mode_changed"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `from_mode`: Mode izin sebelumnya, misalnya `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, atau `"bypassPermissions"`
* `to_mode`: Mode izin baru
* `trigger`: Apa yang menyebabkan perubahan. Salah satu dari `"shift_tab"`, `"exit_plan_mode"`, `"auto_gate_denied"`, atau `"auto_opt_in"`. Tidak ada saat transisi berasal dari SDK atau bridge

#### Acara auth

Dicatat saat `/login` atau `/logout` selesai.

**Nama Acara**: `claude_code.auth`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"auth"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `action`: `"login"` atau `"logout"`
* `success`: `"true"` atau `"false"`
* `auth_method`: Metode autentikasi, seperti `"oauth"`
* `error_category`: Jenis kesalahan kategori saat tindakan gagal. Pesan kesalahan mentah tidak pernah disertakan
* `status_code`: Kode status HTTP sebagai string saat tindakan gagal dengan kesalahan HTTP

#### Acara koneksi server MCP

Dicatat saat server MCP terhubung, terputus, atau gagal terhubung.

**Nama Acara**: `claude_code.mcp_server_connection`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"mcp_server_connection"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `status`: `"connected"`, `"failed"`, atau `"disconnected"`
* `transport_type`: Transport server, seperti `"stdio"`, `"sse"`, atau `"http"`
* `server_scope`: Cakupan server dikonfigurasi di, seperti `"user"`, `"project"`, atau `"local"`
* `duration_ms`: Durasi upaya koneksi dalam milidetik
* `error_code`: Kode kesalahan saat koneksi gagal
* `server_name` (saat `OTEL_LOG_TOOL_DETAILS=1`): Nama server yang dikonfigurasi
* `error` (saat `OTEL_LOG_TOOL_DETAILS=1`): Pesan kesalahan lengkap saat koneksi gagal

#### Acara kesalahan internal

Dicatat saat Claude Code menangkap kesalahan internal yang tidak terduga. Hanya nama kelas kesalahan dan kode gaya errno yang dicatat. Pesan kesalahan dan stack trace tidak pernah disertakan. Acara ini tidak dipancarkan saat berjalan terhadap Bedrock, Vertex, atau Foundry, atau saat `DISABLE_ERROR_REPORTING` diatur.

**Nama Acara**: `claude_code.internal_error`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"internal_error"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `error_name`: Nama kelas kesalahan, seperti `"TypeError"` atau `"SyntaxError"`
* `error_code`: Kode errno Node.js seperti `"ENOENT"` saat ada pada kesalahan

#### Acara plugin terinstal

Dicatat saat plugin selesai menginstal, dari perintah CLI `claude plugin install` dan UI interaktif `/plugin`.

**Nama Acara**: `claude_code.plugin_installed`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"plugin_installed"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `marketplace.is_official`: `"true"` jika marketplace adalah marketplace Anthropic resmi, `"false"` sebaliknya
* `install.trigger`: `"cli"` atau `"ui"`
* `plugin.name`: Nama plugin yang diinstal. Untuk marketplace pihak ketiga ini disertakan hanya saat `OTEL_LOG_TOOL_DETAILS=1`
* `plugin.version`: Versi plugin saat dideklarasikan dalam entri marketplace. Untuk marketplace pihak ketiga ini disertakan hanya saat `OTEL_LOG_TOOL_DETAILS=1`
* `marketplace.name`: Marketplace plugin diinstal dari. Untuk marketplace pihak ketiga ini disertakan hanya saat `OTEL_LOG_TOOL_DETAILS=1`

#### Acara skill diaktifkan

Dicatat saat skill dipanggil, baik Claude memanggilnya melalui alat Skill atau Anda menjalankannya sebagai perintah `/`.

**Nama Acara**: `claude_code.skill_activated`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"skill_activated"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `skill.name`: Nama skill. Untuk skill yang ditentukan pengguna dan plugin pihak ketiga nilainya adalah placeholder `"custom_skill"` kecuali `OTEL_LOG_TOOL_DETAILS=1`
* `invocation_trigger`: Bagaimana skill dipicu (`"user-slash"`, `"claude-proactive"`, atau `"nested-skill"`)
* `skill.source`: Tempat skill dimuat dari (misalnya, `"bundled"`, `"userSettings"`, `"projectSettings"`, `"plugin"`)
* `plugin.name` (saat `OTEL_LOG_TOOL_DETAILS=1` atau plugin dari marketplace resmi): Nama plugin pemilik saat skill disediakan oleh plugin
* `marketplace.name` (saat `OTEL_LOG_TOOL_DETAILS=1` atau plugin dari marketplace resmi): Marketplace plugin pemilik diinstal dari, saat skill disediakan oleh plugin

#### Acara mention @

Dicatat saat Claude Code menyelesaikan mention `@` dalam prompt. Tidak setiap mention memancarkan acara: jalur early-exit seperti penolakan izin, file berukuran besar, lampiran referensi PDF, dan kegagalan listing direktori kembali tanpa logging.

**Nama Acara**: `claude_code.at_mention`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"at_mention"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `mention_type`: Jenis mention (`"file"`, `"directory"`, `"agent"`, `"mcp_resource"`)
* `success`: Apakah mention berhasil diselesaikan (`"true"` atau `"false"`)

#### Acara retry API habis

Dicatat sekali saat permintaan API gagal setelah lebih dari satu upaya. Dipancarkan bersama acara `api_error` terakhir.

**Nama Acara**: `claude_code.api_retries_exhausted`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"api_retries_exhausted"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `model`: Model yang digunakan
* `error`: Pesan kesalahan terakhir
* `status_code`: Kode status HTTP sebagai angka. Tidak ada untuk kesalahan non-HTTP.
* `total_attempts`: Jumlah total upaya yang dilakukan
* `total_retry_duration_ms`: Total waktu wall-clock di semua upaya
* `speed`: `"fast"` atau `"normal"`

#### Acara mulai eksekusi hook

Dicatat saat satu atau lebih hooks mulai dieksekusi untuk acara hook.

**Nama Acara**: `claude_code.hook_execution_start`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"hook_execution_start"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `hook_event`: Jenis acara hook, seperti `"PreToolUse"` atau `"PostToolUse"`
* `hook_name`: Nama hook lengkap termasuk matcher, seperti `"PreToolUse:Write"`
* `num_hooks`: Jumlah perintah hook yang cocok
* `managed_only`: `"true"` saat hanya hooks kebijakan terkelola yang diizinkan
* `hook_source`: `"policySettings"` atau `"merged"`
* `hook_definitions`: Konfigurasi hook yang diserialisasi JSON. Disertakan hanya saat detailed beta tracing dan `OTEL_LOG_TOOL_DETAILS=1` keduanya diaktifkan

#### Acara eksekusi hook selesai

Dicatat saat semua hooks untuk acara hook selesai.

**Nama Acara**: `claude_code.hook_execution_complete`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"hook_execution_complete"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `hook_event`: Jenis acara hook
* `hook_name`: Nama hook lengkap termasuk matcher
* `num_hooks`: Jumlah perintah hook yang cocok
* `num_success`: Jumlah yang selesai dengan sukses
* `num_blocking`: Jumlah yang mengembalikan keputusan blocking
* `num_non_blocking_error`: Jumlah yang gagal tanpa blocking
* `num_cancelled`: Jumlah dibatalkan sebelum selesai
* `total_duration_ms`: Durasi wall-clock dari semua hooks yang cocok
* `managed_only`: `"true"` saat hanya hooks kebijakan terkelola yang diizinkan
* `hook_source`: `"policySettings"` atau `"merged"`
* `hook_definitions`: Konfigurasi hook yang diserialisasi JSON. Disertakan hanya saat detailed beta tracing dan `OTEL_LOG_TOOL_DETAILS=1` keduanya diaktifkan

#### Acara pemadatan

Dicatat saat pemadatan percakapan selesai.

**Nama Acara**: `claude_code.compaction`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"compaction"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `trigger`: `"auto"` atau `"manual"`
* `success`: `"true"` atau `"false"`
* `duration_ms`: Durasi pemadatan
* `pre_tokens`: Jumlah token perkiraan sebelum pemadatan
* `post_tokens`: Jumlah token perkiraan setelah pemadatan
* `error`: Pesan kesalahan saat pemadatan gagal

## Menafsirkan data metrik dan acara

Metrik dan acara yang diekspor mendukung berbagai analisis:

### Pemantauan penggunaan

| Metrik                                                        | Peluang Analisis                                                      |
| ------------------------------------------------------------- | --------------------------------------------------------------------- |
| `claude_code.token.usage`                                     | Pecahkan berdasarkan `type` (input/output), pengguna, tim, atau model |
| `claude_code.session.count`                                   | Lacak adopsi dan keterlibatan dari waktu ke waktu                     |
| `claude_code.lines_of_code.count`                             | Ukur produktivitas dengan melacak penambahan/penghapusan kode         |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Pahami dampak pada alur kerja pengembangan                            |

### Pemantauan biaya

Metrik `claude_code.cost.usage` membantu dengan:

* Melacak tren penggunaan di seluruh tim atau individu
* Mengidentifikasi sesi penggunaan tinggi untuk optimasi

<Note>
  Metrik biaya adalah perkiraan. Untuk data penagihan resmi, lihat penyedia API Anda (Claude Console, Amazon Bedrock, atau Google Cloud Vertex).
</Note>

### Peringatan dan segmentasi

Peringatan umum untuk dipertimbangkan:

* Lonjakan biaya
* Konsumsi token yang tidak biasa
* Volume sesi tinggi dari pengguna tertentu

Semua metrik dapat disegmentasikan berdasarkan `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model`, dan `app.version`.

### Deteksi kelelahan retry

Claude Code mencoba ulang permintaan API yang gagal secara internal dan hanya memancarkan acara `claude_code.api_error` tunggal setelah menyerah, jadi acara itu sendiri adalah sinyal terminal untuk permintaan tersebut. Upaya retry perantara tidak dicatat sebagai acara terpisah.

Atribut `attempt` pada acara mencatat berapa banyak upaya yang dilakukan secara total. Nilai yang lebih besar dari `CLAUDE_CODE_MAX_RETRIES` (default `10`) menunjukkan permintaan menghabiskan semua retry pada kesalahan transien. Nilai yang lebih rendah menunjukkan kesalahan yang tidak dapat dicoba ulang seperti respons `400`.

Untuk membedakan sesi yang pulih dari sesi yang terhenti, kelompokkan acara berdasarkan `session.id` dan periksa apakah acara `api_request` yang lebih baru ada setelah kesalahan.

### Analisis acara

Data acara memberikan wawasan terperinci tentang interaksi Claude Code:

**Pola Penggunaan Alat**: analisis acara hasil alat untuk mengidentifikasi:

* Alat yang paling sering digunakan
* Tingkat keberhasilan alat
* Waktu eksekusi alat rata-rata
* Pola kesalahan berdasarkan jenis alat

**Pemantauan Kinerja**: lacak durasi permintaan API dan waktu eksekusi alat untuk mengidentifikasi hambatan kinerja.

## Pertimbangan backend

Pilihan backend metrik, log, dan traces Anda menentukan jenis analisis yang dapat Anda lakukan:

### Untuk metrik

* **Database deret waktu (misalnya, Prometheus)**: Perhitungan laju, metrik agregat
* **Toko kolumnar (misalnya, ClickHouse)**: Kueri kompleks, analisis pengguna unik
* **Platform observabilitas lengkap (misalnya, Honeycomb, Datadog)**: Kueri lanjutan, visualisasi, peringatan

### Untuk acara/log

* **Sistem agregasi log (misalnya, Elasticsearch, Loki)**: Pencarian teks lengkap, analisis log
* **Toko kolumnar (misalnya, ClickHouse)**: Analisis acara terstruktur
* **Platform observabilitas lengkap (misalnya, Honeycomb, Datadog)**: Korelasi antara metrik dan acara

### Untuk traces

Pilih backend yang mendukung penyimpanan distributed trace dan korelasi span:

* **Sistem distributed tracing (misalnya, Jaeger, Zipkin, Grafana Tempo)**: Visualisasi span, request waterfalls, analisis latensi
* **Platform observabilitas lengkap (misalnya, Honeycomb, Datadog)**: Pencarian trace dan korelasi dengan metrik dan log

Untuk organisasi yang memerlukan metrik Pengguna Aktif Harian/Mingguan/Bulanan (DAU/WAU/MAU), pertimbangkan backend yang mendukung kueri nilai unik yang efisien.

## Informasi layanan

Semua metrik dan acara diekspor dengan atribut sumber daya berikut:

* `service.name`: `claude-code`
* `service.version`: Versi Claude Code saat ini
* `os.type`: Jenis sistem operasi (misalnya, `linux`, `darwin`, `windows`)
* `os.version`: String versi sistem operasi
* `host.arch`: Arsitektur host (misalnya, `amd64`, `arm64`)
* `wsl.version`: Nomor versi WSL (hanya ada saat berjalan di Windows Subsystem for Linux)
* Nama Meter: `com.anthropic.claude_code`

## Sumber daya pengukuran ROI

Untuk panduan komprehensif tentang mengukur pengembalian investasi untuk Claude Code, termasuk pengaturan telemetri, analisis biaya, metrik produktivitas, dan pelaporan otomatis, lihat [Panduan Pengukuran ROI Claude Code](https://github.com/anthropics/claude-code-monitoring-guide). Repositori ini menyediakan konfigurasi Docker Compose siap pakai, pengaturan Prometheus dan OpenTelemetry, dan template untuk menghasilkan laporan produktivitas yang terintegrasi dengan alat seperti Linear.

## Keamanan dan privasi

* Ekspor OpenTelemetry ke backend Anda adalah opt-in dan memerlukan konfigurasi eksplisit. Untuk telemetri operasional terpisah Anthropic dan cara menonaktifkannya, lihat [Penggunaan data](/id/data-usage#telemetry-services)
* Konten file mentah dan cuplikan kode tidak disertakan dalam metrik atau acara. Trace spans adalah jalur data terpisah: lihat poin `OTEL_LOG_TOOL_CONTENT` di bawah
* Saat diautentikasi melalui OAuth, `user.email` disertakan dalam atribut telemetri. Jika ini menjadi perhatian bagi organisasi Anda, bekerja dengan backend telemetri Anda untuk memfilter atau menyunting bidang ini
* Konten prompt pengguna tidak dikumpulkan secara default. Hanya panjang prompt yang dicatat. Untuk menyertakan konten prompt, atur `OTEL_LOG_USER_PROMPTS=1`
* Argumen input alat dan parameter tidak dicatat secara default. Untuk menyertakannya, atur `OTEL_LOG_TOOL_DETAILS=1`. Saat diaktifkan, acara `tool_result` menyertakan atribut `tool_parameters` dengan perintah Bash, nama server MCP dan alat, dan nama skill, ditambah atribut `tool_input` dengan jalur file, URL, pola pencarian, dan argumen lainnya. Acara `user_prompt` menyertakan `command_name` verbatim untuk perintah custom, plugin, dan MCP. Trace spans menyertakan atribut `tool_input` yang sama dan atribut yang diturunkan dari input seperti `file_path`. Nilai individual di atas 512 karakter dipotong dan total dibatasi hingga \~4 K karakter, tetapi argumen mungkin masih berisi nilai sensitif. Konfigurasikan backend telemetri Anda untuk memfilter atau menyunting atribut ini sesuai kebutuhan
* Konten input dan output alat tidak dicatat dalam trace spans secara default. Untuk menyertakannya, atur `OTEL_LOG_TOOL_CONTENT=1`. Saat diaktifkan, acara span menyertakan konten input dan output alat lengkap dipotong pada 60 KB per span. Ini dapat mencakup konten file mentah dari hasil alat Read dan output perintah Bash. Konfigurasikan backend telemetri Anda untuk memfilter atau menyunting atribut ini sesuai kebutuhan
* Badan permintaan dan respons API Anthropic Messages mentah tidak dicatat secara default. Untuk menyertakannya, atur `OTEL_LOG_RAW_API_BODIES`. Dengan `=1`, setiap panggilan API memancarkan acara log `api_request_body` dan `api_response_body` yang atribut `body`-nya adalah muatan yang diserialisasi JSON, dipotong pada 60 KB. Dengan `=file:<dir>`, badan yang tidak dipotong ditulis ke file `.request.json` dan `.response.json` di bawah direktori tersebut dan acara membawa jalur `body_ref` sebagai gantinya dari badan inline. Kirim direktori dengan pengumpul log atau sidecar daripada melalui aliran telemetri. Dalam kedua mode, badan berisi riwayat percakapan lengkap (system prompt, setiap giliran pengguna dan asisten sebelumnya, hasil alat), jadi mengaktifkan ini menyiratkan persetujuan untuk semua yang akan diungkapkan oleh flag konten `OTEL_LOG_*` lainnya. Konten extended-thinking Claude selalu diredaksi dari badan ini terlepas dari pengaturan lain

## Memantau Claude Code di Amazon Bedrock

Untuk panduan pemantauan penggunaan Claude Code terperinci untuk Amazon Bedrock, lihat [Implementasi Pemantauan Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
