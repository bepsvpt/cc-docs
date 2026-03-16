> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code GitHub Actions

> Pelajari tentang integrasi Claude Code ke dalam alur kerja pengembangan Anda dengan Claude Code GitHub Actions

Claude Code GitHub Actions membawa otomasi bertenaga AI ke alur kerja GitHub Anda. Dengan penyebutan `@claude` sederhana di PR atau issue apa pun, Claude dapat menganalisis kode Anda, membuat pull request, mengimplementasikan fitur, dan memperbaiki bug - semuanya sambil mengikuti standar proyek Anda. Untuk ulasan otomatis yang diposting di setiap PR tanpa pemicu, lihat [GitHub Code Review](/id/code-review).

<Note>
  Claude Code GitHub Actions dibangun di atas [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview), yang memungkinkan integrasi programatik Claude Code ke dalam aplikasi Anda. Anda dapat menggunakan SDK untuk membangun alur kerja otomasi kustom di luar GitHub Actions.
</Note>

<Info>
  **Claude Opus 4.6 sekarang tersedia.** Claude Code GitHub Actions default ke Sonnet. Untuk menggunakan Opus 4.6, konfigurasikan [parameter model](#breaking-changes-reference) untuk menggunakan `claude-opus-4-6`.
</Info>

## Mengapa menggunakan Claude Code GitHub Actions?

* **Pembuatan PR instan**: Jelaskan apa yang Anda butuhkan, dan Claude membuat PR lengkap dengan semua perubahan yang diperlukan
* **Implementasi kode otomatis**: Ubah issue menjadi kode yang berfungsi dengan satu perintah
* **Mengikuti standar Anda**: Claude menghormati panduan `CLAUDE.md` Anda dan pola kode yang ada
* **Penyiapan sederhana**: Mulai dalam hitungan menit dengan installer dan kunci API kami
* **Aman secara default**: Kode Anda tetap berada di runner Github

## Apa yang dapat dilakukan Claude?

Claude Code menyediakan GitHub Action yang kuat yang mengubah cara Anda bekerja dengan kode:

### Claude Code Action

GitHub Action ini memungkinkan Anda menjalankan Claude Code dalam alur kerja GitHub Actions Anda. Anda dapat menggunakannya untuk membangun alur kerja kustom apa pun di atas Claude Code.

[Lihat repositori →](https://github.com/anthropics/claude-code-action)

## Penyiapan

## Penyiapan cepat

Cara termudah untuk menyiapkan action ini adalah melalui Claude Code di terminal. Cukup buka claude dan jalankan `/install-github-app`.

Perintah ini akan memandu Anda melalui penyiapan aplikasi GitHub dan rahasia yang diperlukan.

<Note>
  * Anda harus menjadi admin repositori untuk menginstal aplikasi GitHub dan menambahkan rahasia
  * Aplikasi GitHub akan meminta izin baca & tulis untuk Contents, Issues, dan Pull requests
  * Metode quickstart ini hanya tersedia untuk pengguna Claude API langsung. Jika Anda menggunakan AWS Bedrock atau Google Vertex AI, silakan lihat bagian [Using with AWS Bedrock & Google Vertex AI](#using-with-aws-bedrock-%26-google-vertex-ai).
</Note>

## Penyiapan manual

Jika perintah `/install-github-app` gagal atau Anda lebih suka penyiapan manual, silakan ikuti instruksi penyiapan manual ini:

1. **Instal aplikasi Claude GitHub** ke repositori Anda: [https://github.com/apps/claude](https://github.com/apps/claude)

   Aplikasi Claude GitHub memerlukan izin repositori berikut:

   * **Contents**: Baca & tulis (untuk memodifikasi file repositori)
   * **Issues**: Baca & tulis (untuk merespons issue)
   * **Pull requests**: Baca & tulis (untuk membuat PR dan push perubahan)

   Untuk detail lebih lanjut tentang keamanan dan izin, lihat [dokumentasi keamanan](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).
2. **Tambahkan ANTHROPIC\_API\_KEY** ke rahasia repositori Anda ([Pelajari cara menggunakan rahasia di GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions))
3. **Salin file workflow** dari [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) ke dalam direktori `.github/workflows/` repositori Anda

<Tip>
  Setelah menyelesaikan penyiapan cepat atau manual, uji action dengan menandai `@claude` dalam komentar issue atau PR.
</Tip>

## Upgrade dari Beta

<Warning>
  Claude Code GitHub Actions v1.0 memperkenalkan perubahan breaking yang memerlukan pembaruan file workflow Anda untuk upgrade ke v1.0 dari versi beta.
</Warning>

Jika Anda saat ini menggunakan versi beta Claude Code GitHub Actions, kami merekomendasikan untuk memperbarui workflow Anda agar menggunakan versi GA. Versi baru menyederhanakan konfigurasi sambil menambahkan fitur baru yang kuat seperti deteksi mode otomatis.

### Perubahan penting

Semua pengguna beta harus membuat perubahan ini pada file workflow mereka untuk upgrade:

1. **Perbarui versi action**: Ubah `@beta` menjadi `@v1`
2. **Hapus konfigurasi mode**: Hapus `mode: "tag"` atau `mode: "agent"` (sekarang terdeteksi otomatis)
3. **Perbarui input prompt**: Ganti `direct_prompt` dengan `prompt`
4. **Pindahkan opsi CLI**: Konversi `max_turns`, `model`, `custom_instructions`, dll. ke `claude_args`

### Breaking Changes Reference

| Old Beta Input        | New v1.0 Input                        |
| --------------------- | ------------------------------------- |
| `mode`                | *(Removed - auto-detected)*           |
| `direct_prompt`       | `prompt`                              |
| `override_prompt`     | `prompt` with GitHub variables        |
| `custom_instructions` | `claude_args: --append-system-prompt` |
| `max_turns`           | `claude_args: --max-turns`            |
| `model`               | `claude_args: --model`                |
| `allowed_tools`       | `claude_args: --allowedTools`         |
| `disallowed_tools`    | `claude_args: --disallowedTools`      |
| `claude_env`          | `settings` JSON format                |

### Contoh Sebelum dan Sesudah

**Versi beta:**

```yaml  theme={null}
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    custom_instructions: "Follow our coding standards"
    max_turns: "10"
    model: "claude-sonnet-4-6"
```

**Versi GA (v1.0):**

```yaml  theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: |
      --append-system-prompt "Follow our coding standards"
      --max-turns 10
      --model claude-sonnet-4-6
```

<Tip>
  Action sekarang secara otomatis mendeteksi apakah akan dijalankan dalam mode interaktif (merespons penyebutan `@claude`) atau mode otomasi (berjalan segera dengan prompt) berdasarkan konfigurasi Anda.
</Tip>

## Contoh kasus penggunaan

Claude Code GitHub Actions dapat membantu Anda dengan berbagai tugas. Direktori [examples](https://github.com/anthropics/claude-code-action/tree/main/examples) berisi workflow siap pakai untuk skenario berbeda.

### Workflow dasar

```yaml  theme={null}
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

### Menggunakan skills

```yaml  theme={null}
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this pull request for code quality, correctness, and security. Analyze the diff, then post your findings as review comments."
          claude_args: "--max-turns 5"
```

### Otomasi kustom dengan prompt

```yaml  theme={null}
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model opus"
```

### Kasus penggunaan umum

Dalam komentar issue atau PR:

```text  theme={null}
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

Claude akan secara otomatis menganalisis konteks dan merespons dengan tepat.

## Praktik terbaik

### Konfigurasi CLAUDE.md

Buat file `CLAUDE.md` di root repositori Anda untuk mendefinisikan panduan gaya kode, kriteria ulasan, aturan khusus proyek, dan pola yang disukai. File ini memandu pemahaman Claude tentang standar proyek Anda.

### Pertimbangan keamanan

<Warning>Jangan pernah commit kunci API langsung ke repositori Anda.</Warning>

Untuk panduan keamanan komprehensif termasuk izin, autentikasi, dan praktik terbaik, lihat [dokumentasi keamanan Claude Code Action](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).

Selalu gunakan GitHub Secrets untuk kunci API:

* Tambahkan kunci API Anda sebagai rahasia repositori bernama `ANTHROPIC_API_KEY`
* Referensikan dalam workflow: `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* Batasi izin action hanya untuk apa yang diperlukan
* Tinjau saran Claude sebelum merge

Selalu gunakan GitHub Secrets (misalnya, `${{ secrets.ANTHROPIC_API_KEY }}`) daripada hardcoding kunci API langsung dalam file workflow Anda.

### Mengoptimalkan kinerja

Gunakan template issue untuk memberikan konteks, jaga `CLAUDE.md` Anda ringkas dan terfokus, dan konfigurasikan timeout yang sesuai untuk workflow Anda.

### Biaya CI

Saat menggunakan Claude Code GitHub Actions, waspadai biaya terkait:

**Biaya GitHub Actions:**

* Claude Code berjalan di runner yang dihosting GitHub, yang mengonsumsi menit GitHub Actions Anda
* Lihat [dokumentasi penagihan GitHub](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions) untuk harga terperinci dan batas menit

**Biaya API:**

* Setiap interaksi Claude mengonsumsi token API berdasarkan panjang prompt dan respons
* Penggunaan token bervariasi menurut kompleksitas tugas dan ukuran codebase
* Lihat [halaman harga Claude](https://claude.com/platform/api) untuk tarif token saat ini

**Tips optimasi biaya:**

* Gunakan perintah `@claude` spesifik untuk mengurangi panggilan API yang tidak perlu
* Konfigurasikan `--max-turns` yang sesuai dalam `claude_args` untuk mencegah iterasi berlebihan
* Atur timeout tingkat workflow untuk menghindari pekerjaan yang tidak terkontrol
* Pertimbangkan menggunakan kontrol concurrency GitHub untuk membatasi run paralel

## Contoh konfigurasi

Claude Code Action v1 menyederhanakan konfigurasi dengan parameter terpadu:

```yaml  theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Your instructions here" # Optional
    claude_args: "--max-turns 5" # Optional CLI arguments
```

Fitur utama:

* **Antarmuka prompt terpadu** - Gunakan `prompt` untuk semua instruksi
* **Skills** - Panggil [skills](/id/skills) yang terinstal langsung dari prompt
* **Passthrough CLI** - Argumen Claude Code CLI apa pun melalui `claude_args`
* **Pemicu fleksibel** - Bekerja dengan event GitHub apa pun

Kunjungi [direktori examples](https://github.com/anthropics/claude-code-action/tree/main/examples) untuk file workflow lengkap.

<Tip>
  Saat merespons komentar issue atau PR, Claude secara otomatis merespons penyebutan @claude. Untuk event lainnya, gunakan parameter `prompt` untuk memberikan instruksi.
</Tip>

## Menggunakan dengan AWS Bedrock & Google Vertex AI

Untuk lingkungan enterprise, Anda dapat menggunakan Claude Code GitHub Actions dengan infrastruktur cloud Anda sendiri. Pendekatan ini memberi Anda kontrol atas residensi data dan penagihan sambil mempertahankan fungsionalitas yang sama.

### Prasyarat

Sebelum menyiapkan Claude Code GitHub Actions dengan penyedia cloud, Anda memerlukan:

#### Untuk Google Cloud Vertex AI:

1. Proyek Google Cloud dengan Vertex AI diaktifkan
2. Workload Identity Federation dikonfigurasi untuk GitHub Actions
3. Akun layanan dengan izin yang diperlukan
4. Aplikasi GitHub (direkomendasikan) atau gunakan GITHUB\_TOKEN default

#### Untuk AWS Bedrock:

1. Akun AWS dengan Amazon Bedrock diaktifkan
2. GitHub OIDC Identity Provider dikonfigurasi di AWS
3. Peran IAM dengan izin Bedrock
4. Aplikasi GitHub (direkomendasikan) atau gunakan GITHUB\_TOKEN default

<Steps>
  <Step title="Buat aplikasi GitHub kustom (Direkomendasikan untuk Penyedia Pihak Ketiga)">
    Untuk kontrol dan keamanan terbaik saat menggunakan penyedia pihak ketiga seperti Vertex AI atau Bedrock, kami merekomendasikan membuat aplikasi GitHub Anda sendiri:

    1. Buka [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
    2. Isi informasi dasar:
       * **GitHub App name**: Pilih nama unik (misalnya, "YourOrg Claude Assistant")
       * **Homepage URL**: Website organisasi Anda atau URL repositori
    3. Konfigurasikan pengaturan aplikasi:
       * **Webhooks**: Hapus centang "Active" (tidak diperlukan untuk integrasi ini)
    4. Atur izin yang diperlukan:
       * **Repository permissions**:
         * Contents: Read & Write
         * Issues: Read & Write
         * Pull requests: Read & Write
    5. Klik "Create GitHub App"
    6. Setelah pembuatan, klik "Generate a private key" dan simpan file `.pem` yang diunduh
    7. Catat App ID Anda dari halaman pengaturan aplikasi
    8. Instal aplikasi ke repositori Anda:
       * Dari halaman pengaturan aplikasi Anda, klik "Install App" di sidebar kiri
       * Pilih akun atau organisasi Anda
       * Pilih "Only select repositories" dan pilih repositori spesifik
       * Klik "Install"
    9. Tambahkan kunci pribadi sebagai rahasia ke repositori Anda:
       * Buka Settings → Secrets and variables → Actions repositori Anda
       * Buat rahasia baru bernama `APP_PRIVATE_KEY` dengan isi file `.pem`
    10. Tambahkan App ID sebagai rahasia:

    * Buat rahasia baru bernama `APP_ID` dengan ID aplikasi GitHub Anda

    <Note>
      Aplikasi ini akan digunakan dengan action [actions/create-github-app-token](https://github.com/actions/create-github-app-token) untuk menghasilkan token autentikasi dalam workflow Anda.
    </Note>

    **Alternatif untuk Claude API atau jika Anda tidak ingin menyiapkan aplikasi Github Anda sendiri**: Gunakan aplikasi Anthropic resmi:

    1. Instal dari: [https://github.com/apps/claude](https://github.com/apps/claude)
    2. Tidak ada konfigurasi tambahan yang diperlukan untuk autentikasi
  </Step>

  <Step title="Konfigurasikan autentikasi penyedia cloud">
    Pilih penyedia cloud Anda dan siapkan autentikasi aman:

    <AccordionGroup>
      <Accordion title="AWS Bedrock">
        **Konfigurasikan AWS untuk memungkinkan GitHub Actions mengautentikasi dengan aman tanpa menyimpan kredensial.**

        > **Security Note**: Gunakan konfigurasi khusus repositori dan berikan hanya izin minimum yang diperlukan.

        **Required Setup**:

        1. **Enable Amazon Bedrock**:
           * Minta akses ke model Claude di Amazon Bedrock
           * Untuk model lintas region, minta akses di semua region yang diperlukan

        2. **Set up GitHub OIDC Identity Provider**:
           * Provider URL: `https://token.actions.githubusercontent.com`
           * Audience: `sts.amazonaws.com`

        3. **Create IAM Role for GitHub Actions**:
           * Trusted entity type: Web identity
           * Identity provider: `token.actions.githubusercontent.com`
           * Permissions: `AmazonBedrockFullAccess` policy
           * Configure trust policy for your specific repository

        **Required Values**:

        Setelah penyiapan, Anda akan memerlukan:

        * **AWS\_ROLE\_TO\_ASSUME**: ARN dari peran IAM yang Anda buat

        <Tip>
          OIDC lebih aman daripada menggunakan kunci akses AWS statis karena kredensial bersifat sementara dan secara otomatis dirotasi.
        </Tip>

        Lihat [dokumentasi AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) untuk instruksi penyiapan OIDC terperinci.
      </Accordion>

      <Accordion title="Google Vertex AI">
        **Konfigurasikan Google Cloud untuk memungkinkan GitHub Actions mengautentikasi dengan aman tanpa menyimpan kredensial.**

        > **Security Note**: Gunakan konfigurasi khusus repositori dan berikan hanya izin minimum yang diperlukan.

        **Required Setup**:

        1. **Enable APIs** di proyek Google Cloud Anda:
           * IAM Credentials API
           * Security Token Service (STS) API
           * Vertex AI API

        2. **Create Workload Identity Federation resources**:
           * Buat Workload Identity Pool
           * Tambahkan penyedia OIDC GitHub dengan:
             * Issuer: `https://token.actions.githubusercontent.com`
             * Attribute mappings untuk repositori dan pemilik
             * **Security recommendation**: Gunakan kondisi atribut khusus repositori

        3. **Create a Service Account**:
           * Berikan hanya peran `Vertex AI User`
           * **Security recommendation**: Buat akun layanan khusus per repositori

        4. **Configure IAM bindings**:
           * Izinkan Workload Identity Pool untuk menyamar sebagai akun layanan
           * **Security recommendation**: Gunakan set principal khusus repositori

        **Required Values**:

        Setelah penyiapan, Anda akan memerlukan:

        * **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**: Nama sumber daya penyedia lengkap
        * **GCP\_SERVICE\_ACCOUNT**: Alamat email akun layanan

        <Tip>
          Workload Identity Federation menghilangkan kebutuhan untuk kunci akun layanan yang dapat diunduh, meningkatkan keamanan.
        </Tip>

        Untuk instruksi penyiapan terperinci, konsultasikan [dokumentasi Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
      </Accordion>
    </AccordionGroup>
  </Step>

  <Step title="Tambahkan Rahasia yang Diperlukan">
    Tambahkan rahasia berikut ke repositori Anda (Settings → Secrets and variables → Actions):

    #### Untuk Claude API (Langsung):

    1. **Untuk Autentikasi API**:
       * `ANTHROPIC_API_KEY`: Kunci Claude API Anda dari [console.anthropic.com](https://console.anthropic.com)

    2. **Untuk Aplikasi GitHub (jika menggunakan aplikasi Anda sendiri)**:
       * `APP_ID`: ID Aplikasi GitHub Anda
       * `APP_PRIVATE_KEY`: Konten kunci pribadi (.pem)

    #### Untuk Google Cloud Vertex AI

    1. **Untuk Autentikasi GCP**:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER`
       * `GCP_SERVICE_ACCOUNT`

    2. **Untuk Aplikasi GitHub (jika menggunakan aplikasi Anda sendiri)**:
       * `APP_ID`: ID Aplikasi GitHub Anda
       * `APP_PRIVATE_KEY`: Konten kunci pribadi (.pem)

    #### Untuk AWS Bedrock

    1. **Untuk Autentikasi AWS**:
       * `AWS_ROLE_TO_ASSUME`

    2. **Untuk Aplikasi GitHub (jika menggunakan aplikasi Anda sendiri)**:
       * `APP_ID`: ID Aplikasi GitHub Anda
       * `APP_PRIVATE_KEY`: Konten kunci pribadi (.pem)
  </Step>

  <Step title="Buat file workflow">
    Buat file workflow GitHub Actions yang terintegrasi dengan penyedia cloud Anda. Contoh di bawah menunjukkan konfigurasi lengkap untuk AWS Bedrock dan Google Vertex AI:

    <AccordionGroup>
      <Accordion title="Workflow AWS Bedrock">
        **Prasyarat:**

        * Akses AWS Bedrock diaktifkan dengan izin model Claude
        * GitHub dikonfigurasi sebagai penyedia identitas OIDC di AWS
        * Peran IAM dengan izin Bedrock yang mempercayai GitHub Actions

        **Rahasia GitHub yang diperlukan:**

        | Secret Name          | Description                                                 |
        | -------------------- | ----------------------------------------------------------- |
        | `AWS_ROLE_TO_ASSUME` | ARN dari peran IAM untuk akses Bedrock                      |
        | `APP_ID`             | ID Aplikasi GitHub Anda (dari pengaturan aplikasi)          |
        | `APP_PRIVATE_KEY`    | Kunci pribadi yang Anda hasilkan untuk Aplikasi GitHub Anda |

        ```yaml  theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            env:
              AWS_REGION: us-west-2
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  claude_args: '--model us.anthropic.claude-sonnet-4-6 --max-turns 10'
        ```

        <Tip>
          Format ID model untuk Bedrock mencakup awalan region (misalnya, `us.anthropic.claude-sonnet-4-6`).
        </Tip>
      </Accordion>

      <Accordion title="Workflow Google Vertex AI">
        **Prasyarat:**

        * Vertex AI API diaktifkan di proyek GCP Anda
        * Workload Identity Federation dikonfigurasi untuk GitHub
        * Akun layanan dengan izin Vertex AI

        **Rahasia GitHub yang diperlukan:**

        | Secret Name                      | Description                                                 |
        | -------------------------------- | ----------------------------------------------------------- |
        | `GCP_WORKLOAD_IDENTITY_PROVIDER` | Nama sumber daya penyedia identitas workload                |
        | `GCP_SERVICE_ACCOUNT`            | Email akun layanan dengan akses Vertex AI                   |
        | `APP_ID`                         | ID Aplikasi GitHub Anda (dari pengaturan aplikasi)          |
        | `APP_PRIVATE_KEY`                | Kunci pribadi yang Anda hasilkan untuk Aplikasi GitHub Anda |

        ```yaml  theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  trigger_phrase: "@claude"
                  use_vertex: "true"
                  claude_args: '--model claude-sonnet-4@20250514 --max-turns 10'
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
                  VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
        ```

        <Tip>
          ID proyek secara otomatis diambil dari langkah autentikasi Google Cloud, jadi Anda tidak perlu hardcode.
        </Tip>
      </Accordion>
    </AccordionGroup>
  </Step>
</Steps>

## Troubleshooting

### Claude tidak merespons perintah @claude

Verifikasi aplikasi GitHub terinstal dengan benar, periksa bahwa workflow diaktifkan, pastikan kunci API diatur dalam rahasia repositori, dan konfirmkan komentar berisi `@claude` (bukan `/claude`).

### CI tidak berjalan pada commit Claude

Pastikan Anda menggunakan aplikasi GitHub atau aplikasi kustom (bukan pengguna Actions), periksa pemicu workflow mencakup event yang diperlukan, dan verifikasi izin aplikasi mencakup pemicu CI.

### Kesalahan autentikasi

Konfirmkan kunci API valid dan memiliki izin yang cukup. Untuk Bedrock/Vertex, periksa konfigurasi kredensial dan pastikan rahasia dinamai dengan benar dalam workflow.

## Konfigurasi lanjutan

### Parameter action

Claude Code Action v1 menggunakan konfigurasi yang disederhanakan:

| Parameter           | Description                                                       | Required |
| ------------------- | ----------------------------------------------------------------- | -------- |
| `prompt`            | Instruksi untuk Claude (teks biasa atau nama [skill](/id/skills)) | No\*     |
| `claude_args`       | Argumen CLI yang diteruskan ke Claude Code                        | No       |
| `anthropic_api_key` | Kunci Claude API                                                  | Yes\*\*  |
| `github_token`      | Token GitHub untuk akses API                                      | No       |
| `trigger_phrase`    | Frasa pemicu kustom (default: "@claude")                          | No       |
| `use_bedrock`       | Gunakan AWS Bedrock alih-alih Claude API                          | No       |
| `use_vertex`        | Gunakan Google Vertex AI alih-alih Claude API                     | No       |

\*Prompt opsional - saat dihilangkan untuk komentar issue/PR, Claude merespons frasa pemicu\
\*\*Diperlukan untuk Claude API langsung, bukan untuk Bedrock/Vertex

#### Teruskan argumen CLI

Parameter `claude_args` menerima argumen Claude Code CLI apa pun:

```yaml  theme={null}
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

Argumen umum:

* `--max-turns`: Maksimum conversation turns (default: 10)
* `--model`: Model yang digunakan (misalnya, `claude-sonnet-4-6`)
* `--mcp-config`: Path ke konfigurasi MCP
* `--allowed-tools`: Daftar tools yang diizinkan dipisahkan koma
* `--debug`: Aktifkan output debug

### Metode integrasi alternatif

Meskipun perintah `/install-github-app` adalah pendekatan yang direkomendasikan, Anda juga dapat:

* **Custom GitHub App**: Untuk organisasi yang memerlukan nama pengguna bermerek atau alur autentikasi kustom. Buat aplikasi GitHub Anda sendiri dengan izin yang diperlukan (contents, issues, pull requests) dan gunakan action actions/create-github-app-token untuk menghasilkan token dalam workflow Anda.
* **Manual GitHub Actions**: Konfigurasi workflow langsung untuk fleksibilitas maksimal
* **MCP Configuration**: Pemuatan dinamis server Model Context Protocol

Lihat [dokumentasi Claude Code Action](https://github.com/anthropics/claude-code-action/blob/main/docs) untuk panduan terperinci tentang autentikasi, keamanan, dan konfigurasi lanjutan.

### Menyesuaikan perilaku Claude

Anda dapat mengonfigurasi perilaku Claude dengan dua cara:

1. **CLAUDE.md**: Tentukan standar coding, kriteria ulasan, dan aturan khusus proyek dalam file `CLAUDE.md` di root repositori Anda. Claude akan mengikuti panduan ini saat membuat PR dan merespons permintaan. Lihat [dokumentasi Memory](/id/memory) kami untuk detail lebih lanjut.
2. **Custom prompts**: Gunakan parameter `prompt` dalam file workflow untuk memberikan instruksi khusus workflow. Ini memungkinkan Anda menyesuaikan perilaku Claude untuk workflow atau tugas berbeda.

Claude akan mengikuti panduan ini saat membuat PR dan merespons permintaan.
