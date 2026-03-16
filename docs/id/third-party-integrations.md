> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ringkasan penyebaran enterprise

> Pelajari bagaimana Claude Code dapat terintegrasi dengan berbagai layanan pihak ketiga dan infrastruktur untuk memenuhi persyaratan penyebaran enterprise.

Halaman ini memberikan gambaran umum tentang opsi penyebaran yang tersedia dan membantu Anda memilih konfigurasi yang tepat untuk organisasi Anda.

## Perbandingan penyedia

<table>
  <thead>
    <tr>
      <th>Fitur</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Wilayah</td>
      <td>Negara yang didukung [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Beberapa AWS [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Beberapa GCP [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Beberapa Azure [regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
    </tr>

    <tr>
      <td>Autentikasi</td>
      <td>Kunci API</td>
      <td>Kunci API atau kredensial AWS</td>
      <td>Kredensial GCP</td>
      <td>Kunci API atau Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Pelacakan biaya</td>
      <td>Dashboard</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Fitur enterprise</td>
      <td>Tim, pemantauan penggunaan</td>
      <td>Kebijakan IAM, CloudTrail</td>
      <td>Peran IAM, Cloud Audit Logs</td>
      <td>Kebijakan RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Penyedia cloud

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/id/amazon-bedrock">
    Gunakan model Claude melalui infrastruktur AWS dengan autentikasi berbasis kunci API atau IAM dan pemantauan asli AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/id/google-vertex-ai">
    Akses model Claude melalui Google Cloud Platform dengan keamanan dan kepatuhan tingkat enterprise
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/id/microsoft-foundry">
    Akses Claude melalui Azure dengan autentikasi kunci API atau Microsoft Entra ID dan penagihan Azure
  </Card>
</CardGroup>

## Infrastruktur korporat

<CardGroup cols={2}>
  <Card title="Enterprise Network" icon="shield" href="/id/network-config">
    Konfigurasikan Claude Code untuk bekerja dengan server proxy organisasi Anda dan persyaratan SSL/TLS
  </Card>

  <Card title="LLM Gateway" icon="server" href="/id/llm-gateway">
    Sebarkan akses model terpusat dengan pelacakan penggunaan, penganggaran, dan pencatatan audit
  </Card>
</CardGroup>

## Ringkasan konfigurasi

Claude Code mendukung opsi konfigurasi fleksibel yang memungkinkan Anda menggabungkan penyedia dan infrastruktur yang berbeda:

<Note>
  Pahami perbedaan antara:

  * **Proxy korporat**: Proxy HTTP/HTTPS untuk merutekan lalu lintas (diatur melalui `HTTPS_PROXY` atau `HTTP_PROXY`)
  * **LLM Gateway**: Layanan yang menangani autentikasi dan menyediakan endpoint yang kompatibel dengan penyedia (diatur melalui `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, atau `ANTHROPIC_VERTEX_BASE_URL`)

  Kedua konfigurasi dapat digunakan secara bersamaan.
</Note>

### Menggunakan Bedrock dengan proxy korporat

Rutekan lalu lintas Bedrock melalui proxy HTTP/HTTPS korporat:

```bash  theme={null}
# Aktifkan Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Konfigurasikan proxy korporat
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Menggunakan Bedrock dengan LLM Gateway

Gunakan layanan gateway yang menyediakan endpoint yang kompatibel dengan Bedrock:

```bash  theme={null}
# Aktifkan Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Konfigurasikan gateway LLM
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Jika gateway menangani autentikasi AWS
```

### Menggunakan Foundry dengan proxy korporat

Rutekan lalu lintas Azure melalui proxy HTTP/HTTPS korporat:

```bash  theme={null}
# Aktifkan Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Atau abaikan untuk autentikasi Entra ID

# Konfigurasikan proxy korporat
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Menggunakan Foundry dengan LLM Gateway

Gunakan layanan gateway yang menyediakan endpoint yang kompatibel dengan Azure:

```bash  theme={null}
# Aktifkan Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Konfigurasikan gateway LLM
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Jika gateway menangani autentikasi Azure
```

### Menggunakan Vertex AI dengan proxy korporat

Rutekan lalu lintas Vertex AI melalui proxy HTTP/HTTPS korporat:

```bash  theme={null}
# Aktifkan Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Konfigurasikan proxy korporat
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Menggunakan Vertex AI dengan LLM Gateway

Gabungkan model Google Vertex AI dengan gateway LLM untuk manajemen terpusat:

```bash  theme={null}
# Aktifkan Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Konfigurasikan gateway LLM
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Jika gateway menangani autentikasi GCP
```

### Konfigurasi autentikasi

Claude Code menggunakan `ANTHROPIC_AUTH_TOKEN` untuk header `Authorization` ketika diperlukan. Bendera `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) digunakan dalam skenario gateway LLM di mana gateway menangani autentikasi penyedia.

## Memilih konfigurasi penyebaran yang tepat

Pertimbangkan faktor-faktor ini saat memilih pendekatan penyebaran Anda:

### Akses penyedia langsung

Terbaik untuk organisasi yang:

* Menginginkan pengaturan paling sederhana
* Memiliki infrastruktur AWS atau GCP yang sudah ada
* Membutuhkan pemantauan asli penyedia dan kepatuhan

### Proxy korporat

Terbaik untuk organisasi yang:

* Memiliki persyaratan proxy korporat yang sudah ada
* Membutuhkan pemantauan lalu lintas dan kepatuhan
* Harus merutekan semua lalu lintas melalui jalur jaringan tertentu

### LLM Gateway

Terbaik untuk organisasi yang:

* Membutuhkan pelacakan penggunaan di seluruh tim
* Ingin beralih secara dinamis antar model
* Memerlukan pembatasan kecepatan khusus atau anggaran
* Membutuhkan manajemen autentikasi terpusat

## Debugging

Saat men-debug penyebaran Anda:

* Gunakan [perintah slash](/id/slash-commands) `claude /status`. Perintah ini memberikan visibilitas ke dalam autentikasi, proxy, dan pengaturan URL apa pun yang diterapkan.
* Atur variabel lingkungan `export ANTHROPIC_LOG=debug` untuk mencatat permintaan.

## Praktik terbaik untuk organisasi

### 1. Investasi dalam dokumentasi dan memori

Kami sangat merekomendasikan investasi dalam dokumentasi sehingga Claude Code memahami basis kode Anda. Organisasi dapat menyebarkan file CLAUDE.md di berbagai tingkat:

* **Di seluruh organisasi**: Sebarkan ke direktori sistem seperti `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) untuk standar perusahaan
* **Tingkat repositori**: Buat file `CLAUDE.md` di akar repositori yang berisi arsitektur proyek, perintah build, dan pedoman kontribusi. Periksa ini ke dalam kontrol sumber sehingga semua pengguna mendapat manfaat

  [Pelajari lebih lanjut](/id/memory).

### 2. Sederhanakan penyebaran

Jika Anda memiliki lingkungan pengembangan khusus, kami menemukan bahwa membuat cara "satu klik" untuk menginstal Claude Code adalah kunci untuk meningkatkan adopsi di seluruh organisasi.

### 3. Mulai dengan penggunaan terpandu

Dorong pengguna baru untuk mencoba Claude Code untuk Q\&A basis kode, atau pada perbaikan bug yang lebih kecil atau permintaan fitur. Minta Claude Code untuk membuat rencana. Periksa saran Claude dan berikan umpan balik jika tidak sesuai jalur. Seiring waktu, ketika pengguna memahami paradigma baru ini dengan lebih baik, mereka akan lebih efektif dalam membiarkan Claude Code berjalan lebih agentic.

### 4. Konfigurasikan kebijakan keamanan

Tim keamanan dapat mengonfigurasi izin terkelola untuk apa yang Claude Code diizinkan dan tidak diizinkan untuk dilakukan, yang tidak dapat ditimpa oleh konfigurasi lokal. [Pelajari lebih lanjut](/id/security).

### 5. Manfaatkan MCP untuk integrasi

MCP adalah cara yang bagus untuk memberikan Claude Code lebih banyak informasi, seperti menghubungkan ke sistem manajemen tiket atau log kesalahan. Kami merekomendasikan bahwa satu tim pusat mengonfigurasi server MCP dan memeriksa konfigurasi `.mcp.json` ke dalam basis kode sehingga semua pengguna mendapat manfaat. [Pelajari lebih lanjut](/id/mcp).

Di Anthropic, kami mempercayai Claude Code untuk mendorong pengembangan di seluruh setiap basis kode Anthropic. Kami harap Anda menikmati menggunakan Claude Code sebanyak yang kami lakukan.

## Langkah berikutnya

* [Siapkan Amazon Bedrock](/id/amazon-bedrock) untuk penyebaran asli AWS
* [Konfigurasikan Google Vertex AI](/id/google-vertex-ai) untuk penyebaran GCP
* [Siapkan Microsoft Foundry](/id/microsoft-foundry) untuk penyebaran Azure
* [Konfigurasikan Enterprise Network](/id/network-config) untuk persyaratan jaringan
* [Sebarkan LLM Gateway](/id/llm-gateway) untuk manajemen enterprise
* [Pengaturan](/id/settings) untuk opsi konfigurasi dan variabel lingkungan
