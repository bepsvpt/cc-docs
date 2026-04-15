> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ikhtisar penyebaran enterprise

> Pelajari bagaimana Claude Code dapat terintegrasi dengan berbagai layanan pihak ketiga dan infrastruktur untuk memenuhi persyaratan penyebaran enterprise.

Organisasi dapat menyebarkan Claude Code melalui Anthropic secara langsung atau melalui penyedia cloud. Halaman ini membantu Anda memilih konfigurasi yang tepat.

## Bandingkan opsi penyebaran

Untuk sebagian besar organisasi, Claude for Teams atau Claude for Enterprise memberikan pengalaman terbaik. Anggota tim mendapatkan akses ke Claude Code dan Claude di web dengan satu langganan, penagihan terpusat, dan tidak ada setup infrastruktur yang diperlukan.

**Claude for Teams** adalah self-service dan mencakup fitur kolaborasi, alat admin, dan manajemen penagihan. Terbaik untuk tim yang lebih kecil yang perlu memulai dengan cepat.

**Claude for Enterprise** menambahkan SSO dan domain capture, izin berbasis peran, akses API kepatuhan, dan pengaturan kebijakan terkelola untuk menyebarkan konfigurasi Claude Code di seluruh organisasi. Terbaik untuk organisasi yang lebih besar dengan persyaratan keamanan dan kepatuhan.

Pelajari lebih lanjut tentang [rencana Tim](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) dan [rencana Enterprise](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

Jika organisasi Anda memiliki persyaratan infrastruktur khusus, bandingkan opsi di bawah ini:

<table>
  <thead>
    <tr>
      <th>Fitur</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Terbaik untuk</td>
      <td>Sebagian besar organisasi (direkomendasikan)</td>
      <td>Pengembang individual</td>
      <td>Penyebaran native AWS</td>
      <td>Penyebaran native GCP</td>
      <td>Penyebaran native Azure</td>
    </tr>

    <tr>
      <td>Penagihan</td>
      <td><strong>Teams:</strong> \$150/seat (Premium) dengan PAYG tersedia<br /><strong>Enterprise:</strong> <a href="https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise">Hubungi Penjualan</a></td>
      <td>PAYG</td>
      <td>PAYG melalui AWS</td>
      <td>PAYG melalui GCP</td>
      <td>PAYG melalui Azure</td>
    </tr>

    <tr>
      <td>Wilayah</td>
      <td>[Negara](https://www.anthropic.com/supported-countries) yang didukung</td>
      <td>[Negara](https://www.anthropic.com/supported-countries) yang didukung</td>
      <td>[Wilayah](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) AWS yang beragam</td>
      <td>[Wilayah](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) GCP yang beragam</td>
      <td>[Wilayah](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) Azure yang beragam</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
      <td>Diaktifkan secara default</td>
    </tr>

    <tr>
      <td>Autentikasi</td>
      <td>Claude.ai SSO atau email</td>
      <td>Kunci API</td>
      <td>Kunci API atau kredensial AWS</td>
      <td>Kredensial GCP</td>
      <td>Kunci API atau Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Pelacakan biaya</td>
      <td>Dashboard penggunaan</td>
      <td>Dashboard penggunaan</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Termasuk Claude di web</td>
      <td>Ya</td>
      <td>Tidak</td>
      <td>Tidak</td>
      <td>Tidak</td>
      <td>Tidak</td>
    </tr>

    <tr>
      <td>Fitur enterprise</td>
      <td>Manajemen tim, SSO, pemantauan penggunaan</td>
      <td>Tidak ada</td>
      <td>Kebijakan IAM, CloudTrail</td>
      <td>Peran IAM, Cloud Audit Logs</td>
      <td>Kebijakan RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

Pilih opsi penyebaran untuk melihat instruksi setup:

* [Claude for Teams atau Enterprise](/id/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/id/authentication#claude-console-authentication)
* [Amazon Bedrock](/id/amazon-bedrock)
* [Google Vertex AI](/id/google-vertex-ai)
* [Microsoft Foundry](/id/microsoft-foundry)

## Konfigurasi proxy dan gateway

Sebagian besar organisasi dapat menggunakan penyedia cloud secara langsung tanpa konfigurasi tambahan. Namun, Anda mungkin perlu mengonfigurasi proxy perusahaan atau gateway LLM jika organisasi Anda memiliki persyaratan jaringan atau manajemen khusus. Ini adalah konfigurasi berbeda yang dapat digunakan bersama:

* **Corporate proxy**: Merutekan lalu lintas melalui proxy HTTP/HTTPS. Gunakan ini jika organisasi Anda memerlukan semua lalu lintas keluar untuk melewati server proxy untuk pemantauan keamanan, kepatuhan, atau penegakan kebijakan jaringan. Konfigurasi dengan variabel lingkungan `HTTPS_PROXY` atau `HTTP_PROXY`. Pelajari lebih lanjut di [Konfigurasi jaringan enterprise](/id/network-config).
* **LLM Gateway**: Layanan yang berada di antara Claude Code dan penyedia cloud untuk menangani autentikasi dan perutean. Gunakan ini jika Anda memerlukan pelacakan penggunaan terpusat di seluruh tim, pembatasan laju kustom atau anggaran, atau manajemen autentikasi terpusat. Konfigurasi dengan variabel lingkungan `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, atau `ANTHROPIC_VERTEX_BASE_URL`. Pelajari lebih lanjut di [Konfigurasi gateway LLM](/id/llm-gateway).

Contoh berikut menunjukkan variabel lingkungan yang harus diatur di shell atau profil shell Anda (`.bashrc`, `.zshrc`). Lihat [Pengaturan](/id/settings) untuk metode konfigurasi lainnya.

### Amazon Bedrock

<Tabs>
  <Tab title="Corporate proxy">
    Rutekan lalu lintas Bedrock melalui proxy perusahaan Anda dengan mengatur [variabel lingkungan](/id/env-vars) berikut:

    ```bash theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=us-east-1

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM Gateway">
    Rutekan lalu lintas Bedrock melalui gateway LLM Anda dengan mengatur [variabel lingkungan](/id/env-vars) berikut:

    ```bash theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1

    # Configure LLM gateway
    export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
    export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
    ```
  </Tab>
</Tabs>

### Microsoft Foundry

<Tabs>
  <Tab title="Corporate proxy">
    Rutekan lalu lintas Foundry melalui proxy perusahaan Anda dengan mengatur [variabel lingkungan](/id/env-vars) berikut:

    ```bash theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1
    export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
    export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Or omit for Entra ID auth

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM Gateway">
    Rutekan lalu lintas Foundry melalui gateway LLM Anda dengan mengatur [variabel lingkungan](/id/env-vars) berikut:

    ```bash theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1

    # Configure LLM gateway
    export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
    export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # If gateway handles Azure auth
    ```
  </Tab>
</Tabs>

### Google Vertex AI

<Tabs>
  <Tab title="Corporate proxy">
    Rutekan lalu lintas Vertex AI melalui proxy perusahaan Anda dengan mengatur [variabel lingkungan](/id/env-vars) berikut:

    ```bash theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM Gateway">
    Rutekan lalu lintas Vertex AI melalui gateway LLM Anda dengan mengatur [variabel lingkungan](/id/env-vars) berikut:

    ```bash theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1

    # Configure LLM gateway
    export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
    export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
    ```
  </Tab>
</Tabs>

<Tip>
  Gunakan `/status` di Claude Code untuk memverifikasi bahwa konfigurasi proxy dan gateway Anda diterapkan dengan benar.
</Tip>

## Praktik terbaik untuk organisasi

### Investasi dalam dokumentasi dan memori

Kami sangat merekomendasikan investasi dalam dokumentasi sehingga Claude Code memahami basis kode Anda. Organisasi dapat menyebarkan file CLAUDE.md di berbagai tingkat:

* **Seluruh organisasi**: Sebarkan ke direktori sistem seperti `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) untuk standar perusahaan
* **Tingkat repositori**: Buat file `CLAUDE.md` di akar repositori yang berisi arsitektur proyek, perintah build, dan panduan kontribusi. Periksa ini ke dalam kontrol sumber sehingga semua pengguna mendapat manfaat

Pelajari lebih lanjut di [Memori dan file CLAUDE.md](/id/memory).

### Sederhanakan penyebaran

Jika Anda memiliki lingkungan pengembangan kustom, kami menemukan bahwa membuat cara "satu klik" untuk menginstal Claude Code adalah kunci untuk meningkatkan adopsi di seluruh organisasi.

### Mulai dengan penggunaan terpandu

Dorong pengguna baru untuk mencoba Claude Code untuk Q\&A basis kode, atau pada perbaikan bug yang lebih kecil atau permintaan fitur. Minta Claude Code untuk membuat rencana. Periksa saran Claude dan berikan umpan balik jika tidak sesuai. Seiring waktu, ketika pengguna memahami paradigma baru ini dengan lebih baik, mereka akan lebih efektif dalam membiarkan Claude Code berjalan lebih agentik.

### Versi model pin untuk penyedia cloud

Jika Anda menyebarkan melalui [Bedrock](/id/amazon-bedrock), [Vertex AI](/id/google-vertex-ai), atau [Foundry](/id/microsoft-foundry), pin versi model tertentu menggunakan `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, dan `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Tanpa pinning, alias Claude Code menyelesaikan versi terbaru, yang dapat merusak pengguna ketika Anthropic merilis model baru yang belum diaktifkan di akun Anda. Lihat [Konfigurasi model](/id/model-config#pin-models-for-third-party-deployments) untuk detail.

### Konfigurasi kebijakan keamanan

Tim keamanan dapat mengonfigurasi izin terkelola untuk apa yang Claude Code diizinkan dan tidak diizinkan untuk lakukan, yang tidak dapat ditimpa oleh konfigurasi lokal. [Pelajari lebih lanjut](/id/security).

### Manfaatkan MCP untuk integrasi

MCP adalah cara yang bagus untuk memberikan Claude Code lebih banyak informasi, seperti menghubungkan ke sistem manajemen tiket atau log kesalahan. Kami merekomendasikan bahwa satu tim pusat mengonfigurasi server MCP dan memeriksa konfigurasi `.mcp.json` ke dalam basis kode sehingga semua pengguna mendapat manfaat. [Pelajari lebih lanjut](/id/mcp).

Di Anthropic, kami mempercayai Claude Code untuk mendorong pengembangan di seluruh setiap basis kode Anthropic. Kami harap Anda menikmati menggunakan Claude Code sebanyak yang kami lakukan.

## Langkah berikutnya

Setelah Anda memilih opsi penyebaran dan mengonfigurasi akses untuk tim Anda:

1. **Luncurkan ke tim Anda**: Bagikan instruksi instalasi dan minta anggota tim [menginstal Claude Code](/id/setup) dan autentikasi dengan kredensial mereka.
2. **Atur konfigurasi bersama**: Buat [file CLAUDE.md](/id/memory) di repositori Anda untuk membantu Claude Code memahami basis kode dan standar pengkodean Anda.
3. **Konfigurasi izin**: Tinjau [pengaturan keamanan](/id/security) untuk menentukan apa yang dapat dan tidak dapat dilakukan Claude Code di lingkungan Anda.
