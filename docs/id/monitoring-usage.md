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

| Variabel Lingkungan                                 | Deskripsi                                                                                                                                                           | Nilai Contoh                            |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Mengaktifkan pengumpulan telemetri (diperlukan)                                                                                                                     | `1`                                     |
| `OTEL_METRICS_EXPORTER`                             | Jenis pengekspor metrik, dipisahkan koma. Gunakan `none` untuk menonaktifkan                                                                                        | `console`, `otlp`, `prometheus`, `none` |
| `OTEL_LOGS_EXPORTER`                                | Jenis pengekspor log/acara, dipisahkan koma. Gunakan `none` untuk menonaktifkan                                                                                     | `console`, `otlp`, `none`               |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protokol untuk pengekspor OTLP, berlaku untuk semua sinyal                                                                                                          | `grpc`, `http/json`, `http/protobuf`    |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | Titik akhir pengumpul OTLP untuk semua sinyal                                                                                                                       | `http://localhost:4317`                 |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protokol untuk metrik, menimpa pengaturan umum                                                                                                                      | `grpc`, `http/json`, `http/protobuf`    |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | Titik akhir metrik OTLP, menimpa pengaturan umum                                                                                                                    | `http://localhost:4318/v1/metrics`      |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protokol untuk log, menimpa pengaturan umum                                                                                                                         | `grpc`, `http/json`, `http/protobuf`    |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | Titik akhir log OTLP, menimpa pengaturan umum                                                                                                                       | `http://localhost:4318/v1/logs`         |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Header autentikasi untuk OTLP                                                                                                                                       | `Authorization=Bearer token`            |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Kunci klien untuk autentikasi mTLS                                                                                                                                  | Jalur ke file kunci klien               |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Sertifikat klien untuk autentikasi mTLS                                                                                                                             | Jalur ke file sertifikat klien          |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Interval ekspor dalam milidetik (default: 60000)                                                                                                                    | `5000`, `60000`                         |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Interval ekspor log dalam milidetik (default: 5000)                                                                                                                 | `1000`, `10000`                         |
| `OTEL_LOG_USER_PROMPTS`                             | Aktifkan pencatatan konten prompt pengguna (default: dinonaktifkan)                                                                                                 | `1` untuk mengaktifkan                  |
| `OTEL_LOG_TOOL_DETAILS`                             | Aktifkan pencatatan parameter alat dan argumen input dalam acara alat: perintah Bash, nama server MCP dan alat, nama skill, dan input alat (default: dinonaktifkan) | `1` untuk mengaktifkan                  |
| `OTEL_LOG_TOOL_CONTENT`                             | Aktifkan pencatatan konten input dan output alat dalam acara span (default: dinonaktifkan). Memerlukan [tracing](#traces-beta). Konten dipotong pada 60 KB          | `1` untuk mengaktifkan                  |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Preferensi temporalitas metrik (default: `delta`). Atur ke `cumulative` jika backend Anda mengharapkan temporalitas kumulatif                                       | `delta`, `cumulative`                   |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Interval untuk menyegarkan header dinamis (default: 1740000ms / 29 menit)                                                                                           | `900000`                                |

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

Spans menyunting teks prompt pengguna dan konten alat secara default. Atur `OTEL_LOG_USER_PROMPTS=1` dan `OTEL_LOG_TOOL_CONTENT=1` untuk menyertakannya.

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

#### Penghitung token

Ditingkatkan setelah setiap permintaan API.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Pengidentifikasi model (misalnya, "claude-sonnet-4-6")

#### Penghitung keputusan alat pengeditan kode

Ditingkatkan saat pengguna menerima atau menolak penggunaan alat Edit, Write, atau NotebookEdit.

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `tool_name`: Nama alat (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Keputusan pengguna (`"accept"`, `"reject"`)
* `source`: Sumber keputusan - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, atau `"user_reject"`
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

#### Acara hasil alat

Dicatat saat alat menyelesaikan eksekusi.

**Nama Acara**: `claude_code.tool_result`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `tool_name`: Nama alat
* `success`: `"true"` atau `"false"`
* `duration_ms`: Waktu eksekusi dalam milidetik
* `error`: Pesan kesalahan (jika gagal)
* `decision_type`: Baik `"accept"` atau `"reject"`
* `decision_source`: Sumber keputusan - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, atau `"user_reject"`
* `tool_result_size_bytes`: Ukuran hasil alat dalam byte
* `mcp_server_scope`: Pengidentifikasi cakupan server MCP (untuk alat MCP)
* `tool_parameters` (saat `OTEL_LOG_TOOL_DETAILS=1`): String JSON yang berisi parameter khusus alat:
  * Untuk alat Bash: mencakup `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox`, dan `git_commit_id` (SHA komit, saat perintah `git commit` berhasil)
  * Untuk alat MCP: mencakup `mcp_server_name`, `mcp_tool_name`
  * Untuk alat Skill: mencakup `skill_name`
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
* `speed`: `"fast"` atau `"normal"`, menunjukkan apakah mode cepat aktif

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
* `status_code`: Kode status HTTP sebagai string, atau `"undefined"` untuk kesalahan non-HTTP
* `duration_ms`: Durasi permintaan dalam milidetik
* `attempt`: Nomor upaya (untuk permintaan yang dicoba ulang)
* `speed`: `"fast"` atau `"normal"`, menunjukkan apakah mode cepat aktif

#### Acara keputusan alat

Dicatat saat keputusan izin alat dibuat (terima/tolak).

**Nama Acara**: `claude_code.tool_decision`

**Atribut**:

* Semua [atribut standar](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Stempel waktu ISO 8601
* `event.sequence`: penghitung yang meningkat secara monoton untuk mengurutkan acara dalam sesi
* `tool_name`: Nama alat (misalnya, "Read", "Edit", "Write", "NotebookEdit")
* `decision`: Baik `"accept"` atau `"reject"`
* `source`: Sumber keputusan - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, atau `"user_reject"`

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
  Metrik biaya adalah perkiraan. Untuk data penagihan resmi, lihat penyedia API Anda (Claude Console, AWS Bedrock, atau Google Cloud Vertex).
</Note>

### Peringatan dan segmentasi

Peringatan umum untuk dipertimbangkan:

* Lonjakan biaya
* Konsumsi token yang tidak biasa
* Volume sesi tinggi dari pengguna tertentu

Semua metrik dapat disegmentasikan berdasarkan `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model`, dan `app.version`.

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

* Telemetri adalah opt-in dan memerlukan konfigurasi eksplisit
* Konten file mentah dan cuplikan kode tidak disertakan dalam metrik atau acara. Trace spans adalah jalur data terpisah: lihat poin `OTEL_LOG_TOOL_CONTENT` di bawah
* Saat diautentikasi melalui OAuth, `user.email` disertakan dalam atribut telemetri. Jika ini menjadi perhatian bagi organisasi Anda, bekerja dengan backend telemetri Anda untuk memfilter atau menyunting bidang ini
* Konten prompt pengguna tidak dikumpulkan secara default. Hanya panjang prompt yang dicatat. Untuk menyertakan konten prompt, atur `OTEL_LOG_USER_PROMPTS=1`
* Argumen input alat dan parameter tidak dicatat secara default. Untuk menyertakannya, atur `OTEL_LOG_TOOL_DETAILS=1`. Saat diaktifkan, acara `tool_result` menyertakan atribut `tool_parameters` dengan perintah Bash, nama server MCP dan alat, dan nama skill, ditambah atribut `tool_input` dengan jalur file, URL, pola pencarian, dan argumen lainnya. Nilai individual di atas 512 karakter dipotong dan total dibatasi hingga \~4 K karakter, tetapi argumen mungkin masih berisi nilai sensitif. Konfigurasikan backend telemetri Anda untuk memfilter atau menyunting atribut ini sesuai kebutuhan
* Konten input dan output alat tidak dicatat dalam trace spans secara default. Untuk menyertakannya, atur `OTEL_LOG_TOOL_CONTENT=1`. Saat diaktifkan, acara span menyertakan konten input dan output alat lengkap dipotong pada 60 KB per span. Ini dapat mencakup konten file mentah dari hasil alat Read dan output perintah Bash. Konfigurasikan backend telemetri Anda untuk memfilter atau menyunting atribut ini sesuai kebutuhan

## Memantau Claude Code di Amazon Bedrock

Untuk panduan pemantauan penggunaan Claude Code terperinci untuk Amazon Bedrock, lihat [Implementasi Pemantauan Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
