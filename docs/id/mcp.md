> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hubungkan Claude Code ke alat melalui MCP

> Pelajari cara menghubungkan Claude Code ke alat Anda dengan Model Context Protocol.

export const MCPServersTable = ({platform = "all"}) => {
  const ifYouAreAnAiAgentReadingThisYouShouldInsteadFetch = 'https://api.anthropic.com/mcp-registry/docs';
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    const fetchServers = async () => {
      try {
        setLoading(true);
        const allServers = [];
        let cursor = null;
        do {
          const url = new URL('https://api.anthropic.com/mcp-registry/v0/servers');
          url.searchParams.set('version', 'latest');
          url.searchParams.set('visibility', 'commercial');
          url.searchParams.set('limit', '100');
          if (cursor) {
            url.searchParams.set('cursor', cursor);
          }
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`Failed to fetch MCP registry: ${response.status}`);
          }
          const data = await response.json();
          allServers.push(...data.servers);
          cursor = data.metadata?.nextCursor || null;
        } while (cursor);
        const transformedServers = allServers.map(item => {
          const server = item.server;
          const meta = item._meta?.['com.anthropic.api/mcp-registry'] || ({});
          const worksWith = meta.worksWith || [];
          const availability = {
            claudeCode: worksWith.includes('claude-code'),
            mcpConnector: worksWith.includes('claude-api'),
            claudeDesktop: worksWith.includes('claude-desktop')
          };
          const remotes = server.remotes || [];
          const httpRemote = remotes.find(r => r.type === 'streamable-http');
          const sseRemote = remotes.find(r => r.type === 'sse');
          const preferredRemote = httpRemote || sseRemote;
          const remoteUrl = preferredRemote?.url || meta.url;
          const remoteType = preferredRemote?.type;
          const isTemplatedUrl = remoteUrl?.includes('{');
          let setupUrl;
          if (isTemplatedUrl && meta.requiredFields) {
            const urlField = meta.requiredFields.find(f => f.field === 'url');
            setupUrl = urlField?.sourceUrl || meta.documentation;
          }
          const urls = {};
          if (!isTemplatedUrl) {
            if (remoteType === 'streamable-http') {
              urls.http = remoteUrl;
            } else if (remoteType === 'sse') {
              urls.sse = remoteUrl;
            }
          }
          let envVars = [];
          if (server.packages && server.packages.length > 0) {
            const npmPackage = server.packages.find(p => p.registryType === 'npm');
            if (npmPackage) {
              urls.stdio = `npx -y ${npmPackage.identifier}`;
              if (npmPackage.environmentVariables) {
                envVars = npmPackage.environmentVariables;
              }
            }
          }
          return {
            name: meta.displayName || server.title || server.name,
            description: meta.oneLiner || server.description,
            documentation: meta.documentation,
            urls: urls,
            envVars: envVars,
            availability: availability,
            customCommands: meta.claudeCodeCopyText ? {
              claudeCode: meta.claudeCodeCopyText
            } : undefined,
            setupUrl: setupUrl
          };
        });
        setServers(transformedServers);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching MCP registry:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchServers();
  }, []);
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode;
    }
    const serverSlug = server.name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    if (server.urls.http) {
      return `claude mcp add ${serverSlug} --transport http ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add ${serverSlug} --transport sse ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.envVars && server.envVars.length > 0 ? server.envVars.map(v => `--env ${v.name}=YOUR_${v.name}`).join(' ') : '';
      const baseCommand = `claude mcp add ${serverSlug} --transport stdio`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  if (loading) {
    return <div>Loading MCP servers...</div>;
  }
  if (error) {
    return <div>Error loading MCP servers: {error}</div>;
  }
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>

      <div className="cards-container">
        {filteredServers.map(server => {
    const claudeCodeCommand = generateClaudeCodeCommand(server);
    const mcpUrl = server.urls.http || server.urls.sse;
    const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
    return <div key={server.name} className="server-card">
              <div>
                {server.documentation ? <a href={server.documentation}>
                    <strong>{server.name}</strong>
                  </a> : <strong>{server.name}</strong>}
              </div>

              <p style={{
      margin: '0.5rem 0',
      fontSize: '0.9rem'
    }}>
                {server.description}
              </p>

              {server.setupUrl && <p style={{
      margin: '0.25rem 0',
      fontSize: '0.8rem',
      fontStyle: 'italic',
      opacity: 0.7
    }}>
                  Requires user-specific URL.{' '}
                  <a href={server.setupUrl} style={{
      textDecoration: 'underline'
    }}>
                    Get your URL here
                  </a>.
                </p>}

              {commandToShow && !server.setupUrl && <>
                <p style={{
      display: 'block',
      fontSize: '0.75rem',
      fontWeight: 500,
      minWidth: 'fit-content',
      marginTop: '0.5rem',
      marginBottom: 0
    }}>
                  {platform === "claudeCode" ? "Command" : "URL"}
                </p>
                <div className="command-row">
                  <code>
                    {commandToShow}
                  </code>
                </div>
              </>}
            </div>;
  })}
      </div>
    </>;
};

Claude Code dapat terhubung ke ratusan alat eksternal dan sumber data melalui [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), standar sumber terbuka untuk integrasi AI-alat. Server MCP memberikan Claude Code akses ke alat, database, dan API Anda.

## Apa yang dapat Anda lakukan dengan MCP

Dengan server MCP yang terhubung, Anda dapat meminta Claude Code untuk:

* **Menerapkan fitur dari pelacak masalah**: "Tambahkan fitur yang dijelaskan dalam masalah JIRA ENG-4521 dan buat PR di GitHub."
* **Menganalisis data pemantauan**: "Periksa Sentry dan Statsig untuk memeriksa penggunaan fitur yang dijelaskan dalam ENG-4521."
* **Menanyakan database**: "Temukan email 10 pengguna acak yang menggunakan fitur ENG-4521, berdasarkan database PostgreSQL kami."
* **Mengintegrasikan desain**: "Perbarui template email standar kami berdasarkan desain Figma baru yang diposting di Slack"
* **Mengotomatisasi alur kerja**: "Buat draf Gmail mengundang 10 pengguna ini ke sesi umpan balik tentang fitur baru."
* **Bereaksi terhadap peristiwa eksternal**: Server MCP juga dapat bertindak sebagai [saluran](/id/channels) yang mendorong pesan ke dalam sesi Anda, sehingga Claude bereaksi terhadap pesan Telegram, obrolan Discord, atau peristiwa webhook saat Anda sedang pergi.

## Server MCP populer

Berikut adalah beberapa server MCP yang umum digunakan yang dapat Anda hubungkan ke Claude Code:

<Warning>
  Gunakan server MCP pihak ketiga dengan risiko Anda sendiri - Anthropic belum memverifikasi
  kebenaran atau keamanan semua server ini.
  Pastikan Anda mempercayai server MCP yang Anda instal.
  Berhati-hatilah terutama saat menggunakan server MCP yang dapat mengambil konten
  yang tidak dipercaya, karena ini dapat mengekspos Anda ke risiko injeksi prompt.
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **Membutuhkan integrasi spesifik?** [Temukan ratusan server MCP lainnya di GitHub](https://github.com/modelcontextprotocol/servers), atau buat server Anda sendiri menggunakan [MCP SDK](https://modelcontextprotocol.io/quickstart/server).
</Note>

## Menginstal server MCP

Server MCP dapat dikonfigurasi dengan tiga cara berbeda tergantung pada kebutuhan Anda:

### Opsi 1: Tambahkan server HTTP jarak jauh

Server HTTP adalah opsi yang direkomendasikan untuk terhubung ke server MCP jarak jauh. Ini adalah transport yang paling banyak didukung untuk layanan berbasis cloud.

```bash  theme={null}
# Sintaks dasar
claude mcp add --transport http <name> <url>

# Contoh nyata: Hubungkan ke Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Contoh dengan token Bearer
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Opsi 2: Tambahkan server SSE jarak jauh

<Warning>
  Transport SSE (Server-Sent Events) sudah usang. Gunakan server HTTP sebagai gantinya, jika tersedia.
</Warning>

```bash  theme={null}
# Sintaks dasar
claude mcp add --transport sse <name> <url>

# Contoh nyata: Hubungkan ke Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Contoh dengan header autentikasi
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Opsi 3: Tambahkan server stdio lokal

Server stdio berjalan sebagai proses lokal di mesin Anda. Mereka ideal untuk alat yang memerlukan akses sistem langsung atau skrip khusus.

```bash  theme={null}
# Sintaks dasar
claude mcp add [options] <name> -- <command> [args...]

# Contoh nyata: Tambahkan server Airtable
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **Penting: Urutan opsi**

  Semua opsi (`--transport`, `--env`, `--scope`, `--header`) harus datang **sebelum** nama server. `--` (tanda hubung ganda) kemudian memisahkan nama server dari perintah dan argumen yang diteruskan ke server MCP.

  Sebagai contoh:

  * `claude mcp add --transport stdio myserver -- npx server` → menjalankan `npx server`
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → menjalankan `python server.py --port 8080` dengan `KEY=value` di lingkungan

  Ini mencegah konflik antara flag Claude dan flag server.
</Note>

### Mengelola server Anda

Setelah dikonfigurasi, Anda dapat mengelola server MCP Anda dengan perintah ini:

```bash  theme={null}
# Daftar semua server yang dikonfigurasi
claude mcp list

# Dapatkan detail untuk server tertentu
claude mcp get github

# Hapus server
claude mcp remove github

# (dalam Claude Code) Periksa status server
/mcp
```

### Pembaruan alat dinamis

Claude Code mendukung notifikasi `list_changed` MCP, memungkinkan server MCP untuk secara dinamis memperbarui alat, prompt, dan sumber daya yang tersedia tanpa memerlukan Anda untuk memutuskan dan menghubungkan kembali. Ketika server MCP mengirim notifikasi `list_changed`, Claude Code secara otomatis menyegarkan kemampuan yang tersedia dari server tersebut.

### Dorong pesan dengan saluran

Server MCP juga dapat mendorong pesan langsung ke dalam sesi Anda sehingga Claude dapat bereaksi terhadap peristiwa eksternal seperti hasil CI, peringatan pemantauan, atau pesan obrolan. Untuk mengaktifkan ini, server Anda mendeklarasikan kemampuan `claude/channel` dan Anda memilihnya dengan flag `--channels` saat startup. Lihat [Saluran](/id/channels) untuk menggunakan saluran yang didukung secara resmi, atau [Referensi saluran](/id/channels-reference) untuk membangun saluran Anda sendiri.

<Tip>
  Tips:

  * Gunakan flag `--scope` untuk menentukan di mana konfigurasi disimpan:
    * `local` (default): Hanya tersedia untuk Anda di proyek saat ini (disebut `project` di versi yang lebih lama)
    * `project`: Dibagikan dengan semua orang di proyek melalui file `.mcp.json`
    * `user`: Tersedia untuk Anda di semua proyek (disebut `global` di versi yang lebih lama)
  * Atur variabel lingkungan dengan flag `--env` (misalnya, `--env KEY=value`)
  * Konfigurasi waktu tunggu startup server MCP menggunakan variabel lingkungan MCP\_TIMEOUT (misalnya, `MCP_TIMEOUT=10000 claude` menetapkan waktu tunggu 10 detik)
  * Claude Code akan menampilkan peringatan ketika output alat MCP melebihi 10.000 token. Untuk meningkatkan batas ini, atur variabel lingkungan `MAX_MCP_OUTPUT_TOKENS` (misalnya, `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Gunakan `/mcp` untuk autentikasi dengan server jarak jauh yang memerlukan autentikasi OAuth 2.0
</Tip>

<Warning>
  **Pengguna Windows**: Pada Windows asli (bukan WSL), server MCP lokal yang menggunakan `npx` memerlukan pembungkus `cmd /c` untuk memastikan eksekusi yang tepat.

  ```bash  theme={null}
  # Ini membuat command="cmd" yang dapat dieksekusi Windows
  claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
  ```

  Tanpa pembungkus `cmd /c`, Anda akan mengalami kesalahan "Connection closed" karena Windows tidak dapat langsung menjalankan `npx`. (Lihat catatan di atas untuk penjelasan parameter `--`.)
</Warning>

### Server MCP yang disediakan plugin

[Plugin](/id/plugins) dapat menggabungkan server MCP, secara otomatis menyediakan alat dan integrasi ketika plugin diaktifkan. Server MCP plugin bekerja identik dengan server yang dikonfigurasi pengguna.

**Cara kerja server MCP plugin**:

* Plugin menentukan server MCP dalam `.mcp.json` di root plugin atau inline dalam `plugin.json`
* Ketika plugin diaktifkan, server MCP-nya dimulai secara otomatis
* Alat MCP plugin muncul bersama alat MCP yang dikonfigurasi secara manual
* Server plugin dikelola melalui instalasi plugin (bukan perintah `/mcp`)

**Contoh konfigurasi MCP plugin**:

Dalam `.mcp.json` di root plugin:

```json  theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

Atau inline dalam `plugin.json`:

```json  theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Fitur MCP plugin**:

* **Siklus hidup otomatis**: Pada startup sesi, server untuk plugin yang diaktifkan terhubung secara otomatis. Jika Anda mengaktifkan atau menonaktifkan plugin selama sesi, jalankan `/reload-plugins` untuk menghubungkan atau memutuskan server MCP-nya
* **Variabel lingkungan**: gunakan `${CLAUDE_PLUGIN_ROOT}` untuk file plugin bundel dan `${CLAUDE_PLUGIN_DATA}` untuk [status persisten](/id/plugins-reference#persistent-data-directory) yang bertahan pembaruan plugin
* **Akses lingkungan pengguna**: Akses ke variabel lingkungan yang sama seperti server yang dikonfigurasi secara manual
* **Jenis transport berganda**: Dukungan transport stdio, SSE, dan HTTP (dukungan transport dapat bervariasi menurut server)

**Melihat server MCP plugin**:

```bash  theme={null}
# Dalam Claude Code, lihat semua server MCP termasuk yang dari plugin
/mcp
```

Server plugin muncul dalam daftar dengan indikator yang menunjukkan mereka berasal dari plugin.

**Manfaat server MCP plugin**:

* **Distribusi bundel**: Alat dan server dikemas bersama
* **Pengaturan otomatis**: Tidak perlu konfigurasi MCP manual
* **Konsistensi tim**: Semua orang mendapatkan alat yang sama ketika plugin diinstal

Lihat [referensi komponen plugin](/id/plugins-reference#mcp-servers) untuk detail tentang penggabungan server MCP dengan plugin.

## Cakupan instalasi MCP

Server MCP dapat dikonfigurasi pada tiga tingkat cakupan yang berbeda, masing-masing melayani tujuan yang berbeda untuk mengelola aksesibilitas server dan berbagi. Memahami cakupan ini membantu Anda menentukan cara terbaik untuk mengonfigurasi server sesuai kebutuhan spesifik Anda.

### Cakupan lokal

Server dengan cakupan lokal mewakili tingkat konfigurasi default dan disimpan dalam `~/.claude.json` di bawah jalur proyek Anda. Server ini tetap pribadi untuk Anda dan hanya dapat diakses saat bekerja dalam direktori proyek saat ini. Cakupan ini ideal untuk server pengembangan pribadi, konfigurasi eksperimental, atau server yang berisi kredensial sensitif yang tidak boleh dibagikan.

<Note>
  Istilah "cakupan lokal" untuk server MCP berbeda dari pengaturan lokal umum. Server MCP dengan cakupan lokal disimpan dalam `~/.claude.json` (direktori home Anda), sementara pengaturan lokal umum menggunakan `.claude/settings.local.json` (di direktori proyek). Lihat [Pengaturan](/id/settings#settings-files) untuk detail tentang lokasi file pengaturan.
</Note>

```bash  theme={null}
# Tambahkan server dengan cakupan lokal (default)
claude mcp add --transport http stripe https://mcp.stripe.com

# Tentukan cakupan lokal secara eksplisit
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Cakupan proyek

Server dengan cakupan proyek memungkinkan kolaborasi tim dengan menyimpan konfigurasi dalam file `.mcp.json` di direktori root proyek Anda. File ini dirancang untuk diperiksa ke dalam kontrol versi, memastikan semua anggota tim memiliki akses ke alat dan layanan MCP yang sama. Ketika Anda menambahkan server dengan cakupan proyek, Claude Code secara otomatis membuat atau memperbarui file ini dengan struktur konfigurasi yang sesuai.

```bash  theme={null}
# Tambahkan server dengan cakupan proyek
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

File `.mcp.json` yang dihasilkan mengikuti format standar:

```json  theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

Untuk alasan keamanan, Claude Code meminta persetujuan sebelum menggunakan server dengan cakupan proyek dari file `.mcp.json`. Jika Anda perlu mengatur ulang pilihan persetujuan ini, gunakan perintah `claude mcp reset-project-choices`.

### Cakupan pengguna

Server dengan cakupan pengguna disimpan dalam `~/.claude.json` dan menyediakan aksesibilitas lintas proyek, menjadikannya tersedia di semua proyek di mesin Anda sambil tetap pribadi untuk akun pengguna Anda. Cakupan ini bekerja dengan baik untuk server utilitas pribadi, alat pengembangan, atau layanan yang sering Anda gunakan di berbagai proyek.

```bash  theme={null}
# Tambahkan server pengguna
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Memilih cakupan yang tepat

Pilih cakupan Anda berdasarkan:

* **Cakupan lokal**: Server pribadi, konfigurasi eksperimental, atau kredensial sensitif khusus untuk satu proyek
* **Cakupan proyek**: Server bersama tim, alat khusus proyek, atau layanan yang diperlukan untuk kolaborasi
* **Cakupan pengguna**: Utilitas pribadi yang diperlukan di berbagai proyek, alat pengembangan, atau layanan yang sering digunakan

<Note>
  **Di mana server MCP disimpan?**

  * **Cakupan pengguna dan lokal**: `~/.claude.json` (dalam field `mcpServers` atau di bawah jalur proyek)
  * **Cakupan proyek**: `.mcp.json` di root proyek Anda (diperiksa ke dalam kontrol sumber)
  * **Dikelola**: `managed-mcp.json` di direktori sistem (lihat [Konfigurasi MCP yang dikelola](#managed-mcp-configuration))
</Note>

### Hierarki cakupan dan prioritas

Konfigurasi server MCP mengikuti hierarki prioritas yang jelas. Ketika server dengan nama yang sama ada di berbagai cakupan, sistem menyelesaikan konflik dengan memprioritaskan server dengan cakupan lokal terlebih dahulu, diikuti oleh server dengan cakupan proyek, dan akhirnya server dengan cakupan pengguna. Desain ini memastikan bahwa konfigurasi pribadi dapat mengganti yang dibagikan jika diperlukan.

### Ekspansi variabel lingkungan dalam `.mcp.json`

Claude Code mendukung ekspansi variabel lingkungan dalam file `.mcp.json`, memungkinkan tim untuk berbagi konfigurasi sambil mempertahankan fleksibilitas untuk jalur spesifik mesin dan nilai sensitif seperti kunci API.

**Sintaks yang didukung:**

* `${VAR}` - Berkembang menjadi nilai variabel lingkungan `VAR`
* `${VAR:-default}` - Berkembang menjadi `VAR` jika diatur, jika tidak menggunakan `default`

**Lokasi ekspansi:**
Variabel lingkungan dapat berkembang dalam:

* `command` - Jalur executable server
* `args` - Argumen baris perintah
* `env` - Variabel lingkungan yang diteruskan ke server
* `url` - Untuk jenis server HTTP
* `headers` - Untuk autentikasi server HTTP

**Contoh dengan ekspansi variabel:**

```json  theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Jika variabel lingkungan yang diperlukan tidak diatur dan tidak memiliki nilai default, Claude Code akan gagal mengurai konfigurasi.

## Contoh praktis

{/* ### Contoh: Otomatisasi pengujian browser dengan Playwright

  ```bash
  claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
  ```

  Kemudian tulis dan jalankan tes browser:

  ```text
  Test if the login flow works with test@example.com
  ```
  ```text
  Take a screenshot of the checkout page on mobile
  ```
  ```text
  Verify that the search feature returns results
  ``` */}

### Contoh: Pantau kesalahan dengan Sentry

```bash  theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Autentikasi dengan akun Sentry Anda:

```text  theme={null}
/mcp
```

Kemudian debug masalah produksi:

```text  theme={null}
What are the most common errors in the last 24 hours?
```

```text  theme={null}
Show me the stack trace for error ID abc123
```

```text  theme={null}
Which deployment introduced these new errors?
```

### Contoh: Hubungkan ke GitHub untuk tinjauan kode

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Autentikasi jika diperlukan dengan memilih "Authenticate" untuk GitHub:

```text  theme={null}
/mcp
```

Kemudian bekerja dengan GitHub:

```text  theme={null}
Review PR #456 and suggest improvements
```

```text  theme={null}
Create a new issue for the bug we just found
```

```text  theme={null}
Show me all open PRs assigned to me
```

### Contoh: Tanyakan database PostgreSQL Anda

```bash  theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Kemudian tanyakan database Anda secara alami:

```text  theme={null}
What's our total revenue this month?
```

```text  theme={null}
Show me the schema for the orders table
```

```text  theme={null}
Find customers who haven't made a purchase in 90 days
```

## Autentikasi dengan server MCP jarak jauh

Banyak server MCP berbasis cloud memerlukan autentikasi. Claude Code mendukung OAuth 2.0 untuk koneksi yang aman.

<Steps>
  <Step title="Tambahkan server yang memerlukan autentikasi">
    Sebagai contoh:

    ```bash  theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Gunakan perintah /mcp dalam Claude Code">
    Dalam Claude Code, gunakan perintah:

    ```text  theme={null}
    /mcp
    ```

    Kemudian ikuti langkah-langkah di browser Anda untuk login.
  </Step>
</Steps>

<Tip>
  Tips:

  * Token autentikasi disimpan dengan aman dan disegarkan secara otomatis
  * Gunakan "Clear authentication" dalam menu `/mcp` untuk mencabut akses
  * Jika browser Anda tidak terbuka secara otomatis, salin URL yang disediakan dan buka secara manual
  * Jika pengalihan browser gagal dengan kesalahan koneksi setelah autentikasi, tempel URL callback lengkap dari bilah alamat browser Anda ke prompt URL yang muncul di Claude Code
  * Autentikasi OAuth bekerja dengan server HTTP
</Tip>

### Gunakan port callback OAuth tetap

Beberapa server MCP memerlukan URI pengalihan tertentu yang terdaftar sebelumnya. Secara default, Claude Code memilih port acak yang tersedia untuk callback OAuth. Gunakan `--callback-port` untuk memperbaiki port sehingga cocok dengan URI pengalihan yang telah terdaftar sebelumnya dalam bentuk `http://localhost:PORT/callback`.

Anda dapat menggunakan `--callback-port` sendiri (dengan pendaftaran klien dinamis) atau bersama dengan `--client-id` (dengan kredensial yang telah dikonfigurasi sebelumnya).

```bash  theme={null}
# Port callback tetap dengan pendaftaran klien dinamis
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Gunakan kredensial OAuth yang telah dikonfigurasi sebelumnya

Beberapa server MCP tidak mendukung pengaturan OAuth otomatis melalui Dynamic Client Registration. Jika Anda melihat kesalahan seperti "Incompatible auth server: does not support dynamic client registration," server memerlukan kredensial yang telah dikonfigurasi sebelumnya. Claude Code juga mendukung server yang menggunakan Client ID Metadata Document (CIMD) alih-alih Dynamic Client Registration, dan menemukan ini secara otomatis. Jika penemuan otomatis gagal, daftarkan aplikasi OAuth melalui portal pengembang server terlebih dahulu, kemudian berikan kredensial saat menambahkan server.

<Steps>
  <Step title="Daftarkan aplikasi OAuth dengan server">
    Buat aplikasi melalui portal pengembang server dan catat ID klien dan rahasia klien Anda.

    Banyak server juga memerlukan URI pengalihan. Jika demikian, pilih port dan daftarkan URI pengalihan dalam format `http://localhost:PORT/callback`. Gunakan port yang sama dengan `--callback-port` di langkah berikutnya.
  </Step>

  <Step title="Tambahkan server dengan kredensial Anda">
    Pilih salah satu metode berikut. Port yang digunakan untuk `--callback-port` dapat berupa port apa pun yang tersedia. Itu hanya perlu cocok dengan URI pengalihan yang Anda daftarkan di langkah sebelumnya.

    <Tabs>
      <Tab title="claude mcp add">
        Gunakan `--client-id` untuk meneruskan ID klien aplikasi Anda. Flag `--client-secret` meminta rahasia dengan input yang disembunyikan:

        ```bash  theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Sertakan objek `oauth` dalam konfigurasi JSON dan teruskan `--client-secret` sebagai flag terpisah:

        ```bash  theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (callback port only)">
        Gunakan `--callback-port` tanpa ID klien untuk memperbaiki port sambil menggunakan pendaftaran klien dinamis:

        ```bash  theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / env var">
        Atur rahasia melalui variabel lingkungan untuk melewati prompt interaktif:

        ```bash  theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Autentikasi di Claude Code">
    Jalankan `/mcp` di Claude Code dan ikuti alur login browser.
  </Step>
</Steps>

<Tip>
  Tips:

  * Rahasia klien disimpan dengan aman di keychain sistem Anda (macOS) atau file kredensial, bukan di konfigurasi Anda
  * Jika server menggunakan klien OAuth publik tanpa rahasia, gunakan hanya `--client-id` tanpa `--client-secret`
  * `--callback-port` dapat digunakan dengan atau tanpa `--client-id`
  * Flag ini hanya berlaku untuk transport HTTP dan SSE. Mereka tidak berpengaruh pada server stdio
  * Gunakan `claude mcp get <name>` untuk memverifikasi bahwa kredensial OAuth dikonfigurasi untuk server
</Tip>

### Ganti penemuan metadata OAuth

Jika server MCP Anda mengembalikan kesalahan pada endpoint metadata OAuth standar (`/.well-known/oauth-authorization-server`) tetapi mengekspos endpoint OIDC yang berfungsi, Anda dapat memberi tahu Claude Code untuk mengambil metadata OAuth langsung dari URL yang Anda tentukan, melewati rantai penemuan standar.

Atur `authServerMetadataUrl` dalam objek `oauth` dari konfigurasi server Anda di `.mcp.json`:

```json  theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL harus menggunakan `https://`. Opsi ini memerlukan Claude Code v2.1.64 atau lebih baru.

### Gunakan header dinamis untuk autentikasi khusus

Jika server MCP Anda menggunakan skema autentikasi selain OAuth (seperti Kerberos, token berumur pendek, atau SSO internal), gunakan `headersHelper` untuk menghasilkan header permintaan pada waktu koneksi. Claude Code menjalankan perintah dan menggabungkan outputnya ke dalam header koneksi.

```json  theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

Perintah juga dapat inline:

```json  theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Persyaratan:**

* Perintah harus menulis objek JSON dari pasangan kunci-nilai string ke stdout
* Perintah berjalan dalam shell dengan waktu tunggu 10 detik
* Header dinamis mengganti `headers` statis apa pun dengan nama yang sama

Helper berjalan segar pada setiap koneksi (pada startup sesi dan pada reconnect). Tidak ada caching, jadi skrip Anda bertanggung jawab untuk penggunaan kembali token apa pun.

<Note>
  `headersHelper` mengeksekusi perintah shell arbitrer. Ketika ditentukan pada cakupan proyek atau lokal, itu hanya berjalan setelah Anda menerima dialog kepercayaan ruang kerja.
</Note>

## Tambahkan server MCP dari konfigurasi JSON

Jika Anda memiliki konfigurasi JSON untuk server MCP, Anda dapat menambahkannya secara langsung:

<Steps>
  <Step title="Tambahkan server MCP dari JSON">
    ```bash  theme={null}
    # Sintaks dasar
    claude mcp add-json <name> '<json>'

    # Contoh: Menambahkan server HTTP dengan konfigurasi JSON
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Contoh: Menambahkan server stdio dengan konfigurasi JSON
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # Contoh: Menambahkan server HTTP dengan kredensial OAuth yang telah dikonfigurasi sebelumnya
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="Verifikasi server ditambahkan">
    ```bash  theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Pastikan JSON diloloskan dengan benar di shell Anda
  * JSON harus sesuai dengan skema konfigurasi server MCP
  * Anda dapat menggunakan `--scope user` untuk menambahkan server ke konfigurasi pengguna Anda alih-alih yang spesifik proyek
</Tip>

## Impor server MCP dari Claude Desktop

Jika Anda telah mengonfigurasi server MCP di Claude Desktop, Anda dapat mengimpornya:

<Steps>
  <Step title="Impor server dari Claude Desktop">
    ```bash  theme={null}
    # Sintaks dasar 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Pilih server mana yang akan diimpor">
    Setelah menjalankan perintah, Anda akan melihat dialog interaktif yang memungkinkan Anda memilih server mana yang ingin Anda impor.
  </Step>

  <Step title="Verifikasi server diimpor">
    ```bash  theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Fitur ini hanya bekerja di macOS dan Windows Subsystem for Linux (WSL)
  * Ini membaca file konfigurasi Claude Desktop dari lokasi standarnya di platform tersebut
  * Gunakan flag `--scope user` untuk menambahkan server ke konfigurasi pengguna Anda
  * Server yang diimpor akan memiliki nama yang sama seperti di Claude Desktop
  * Jika server dengan nama yang sama sudah ada, mereka akan mendapatkan akhiran numerik (misalnya, `server_1`)
</Tip>

## Gunakan server MCP dari Claude.ai

Jika Anda telah masuk ke Claude Code dengan akun [Claude.ai](https://claude.ai), server MCP yang telah Anda tambahkan di Claude.ai secara otomatis tersedia di Claude Code:

<Steps>
  <Step title="Konfigurasi server MCP di Claude.ai">
    Tambahkan server di [claude.ai/settings/connectors](https://claude.ai/settings/connectors). Pada paket Tim dan Enterprise, hanya admin yang dapat menambahkan server.
  </Step>

  <Step title="Autentikasi server MCP">
    Selesaikan langkah autentikasi yang diperlukan di Claude.ai.
  </Step>

  <Step title="Lihat dan kelola server di Claude Code">
    Di Claude Code, gunakan perintah:

    ```text  theme={null}
    /mcp
    ```

    Server Claude.ai muncul dalam daftar dengan indikator yang menunjukkan mereka berasal dari Claude.ai.
  </Step>
</Steps>

Untuk menonaktifkan server MCP claude.ai di Claude Code, atur variabel lingkungan `ENABLE_CLAUDEAI_MCP_SERVERS` ke `false`:

```bash  theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Gunakan Claude Code sebagai server MCP

Anda dapat menggunakan Claude Code itu sendiri sebagai server MCP yang dapat terhubung oleh aplikasi lain:

```bash  theme={null}
# Mulai Claude sebagai server MCP stdio
claude mcp serve
```

Anda dapat menggunakan ini di Claude Desktop dengan menambahkan konfigurasi ini ke claude\_desktop\_config.json:

```json  theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **Mengonfigurasi jalur executable**: Field `command` harus mereferensikan executable Claude Code. Jika perintah `claude` tidak ada di PATH sistem Anda, Anda perlu menentukan jalur lengkap ke executable.

  Untuk menemukan jalur lengkap:

  ```bash  theme={null}
  which claude
  ```

  Kemudian gunakan jalur lengkap dalam konfigurasi Anda:

  ```json  theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  Tanpa jalur executable yang benar, Anda akan mengalami kesalahan seperti `spawn claude ENOENT`.
</Warning>

<Tip>
  Tips:

  * Server menyediakan akses ke alat Claude seperti View, Edit, LS, dll.
  * Di Claude Desktop, coba minta Claude untuk membaca file di direktori, membuat edit, dan lainnya.
  * Perhatikan bahwa server MCP ini hanya mengekspos alat Claude Code ke klien MCP Anda, jadi klien Anda sendiri bertanggung jawab untuk menerapkan konfirmasi pengguna untuk panggilan alat individual.
</Tip>

## Batas output MCP dan peringatan

Ketika alat MCP menghasilkan output besar, Claude Code membantu mengelola penggunaan token untuk mencegah membanjiri konteks percakapan Anda:

* **Ambang batas peringatan output**: Claude Code menampilkan peringatan ketika output alat MCP apa pun melebihi 10.000 token
* **Batas yang dapat dikonfigurasi**: Anda dapat menyesuaikan token output MCP maksimum yang diizinkan menggunakan variabel lingkungan `MAX_MCP_OUTPUT_TOKENS`
* **Batas default**: Maksimum default adalah 25.000 token

Untuk meningkatkan batas untuk alat yang menghasilkan output besar:

```bash  theme={null}
# Atur batas lebih tinggi untuk output alat MCP
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Ini sangat berguna saat bekerja dengan server MCP yang:

* Menanyakan dataset atau database besar
* Menghasilkan laporan atau dokumentasi terperinci
* Memproses file log atau informasi debugging yang luas

<Warning>
  Jika Anda sering mengalami peringatan output dengan server MCP tertentu, pertimbangkan untuk meningkatkan batas atau mengonfigurasi server untuk membuat halaman atau memfilter responsnya.
</Warning>

## Tanggapi permintaan elicitasi MCP

Server MCP dapat meminta input terstruktur dari Anda di tengah tugas menggunakan elicitasi. Ketika server memerlukan informasi yang tidak dapat diperolehnya sendiri, Claude Code menampilkan dialog interaktif dan meneruskan respons Anda kembali ke server. Tidak ada konfigurasi yang diperlukan di pihak Anda: dialog elicitasi muncul secara otomatis ketika server memintanya.

Server dapat meminta input dengan dua cara:

* **Mode formulir**: Claude Code menampilkan dialog dengan field formulir yang ditentukan oleh server (misalnya, prompt nama pengguna dan kata sandi). Isi field dan kirim.
* **Mode URL**: Claude Code membuka URL browser untuk autentikasi atau persetujuan. Selesaikan alur di browser, kemudian konfirmasi di CLI.

Untuk merespons otomatis permintaan elicitasi tanpa menampilkan dialog, gunakan [hook `Elicitation`](/id/hooks#elicitation).

Jika Anda membangun server MCP yang menggunakan elicitasi, lihat [spesifikasi elicitasi MCP](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) untuk detail protokol dan contoh skema.

## Gunakan sumber daya MCP

Server MCP dapat mengekspos sumber daya yang dapat Anda referensikan menggunakan penyebutan @, mirip dengan cara Anda mereferensikan file.

### Referensikan sumber daya MCP

<Steps>
  <Step title="Daftar sumber daya yang tersedia">
    Ketik `@` dalam prompt Anda untuk melihat sumber daya yang tersedia dari semua server MCP yang terhubung. Sumber daya muncul bersama file dalam menu pelengkapan otomatis.
  </Step>

  <Step title="Referensikan sumber daya tertentu">
    Gunakan format `@server:protocol://resource/path` untuk mereferensikan sumber daya:

    ```text  theme={null}
    Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```text  theme={null}
    Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="Referensi sumber daya berganda">
    Anda dapat mereferensikan beberapa sumber daya dalam satu prompt:

    ```text  theme={null}
    Compare @postgres:schema://users with @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Sumber daya secara otomatis diambil dan disertakan sebagai lampiran saat direferensikan
  * Jalur sumber daya dapat dicari fuzzy dalam pelengkapan otomatis penyebutan @
  * Claude Code secara otomatis menyediakan alat untuk membuat daftar dan membaca sumber daya MCP ketika server mendukungnya
  * Sumber daya dapat berisi jenis konten apa pun yang disediakan server MCP (teks, JSON, data terstruktur, dll.)
</Tip>

## Skala dengan Pencarian Alat MCP

Ketika Anda memiliki banyak server MCP yang dikonfigurasi, definisi alat dapat mengonsumsi sebagian besar jendela konteks Anda. Pencarian Alat MCP menyelesaikan ini dengan memuat alat secara dinamis sesuai permintaan alih-alih memuat semuanya sebelumnya.

### Cara kerjanya

Claude Code secara otomatis mengaktifkan Pencarian Alat ketika deskripsi alat MCP Anda akan mengonsumsi lebih dari 10% jendela konteks. Anda dapat [menyesuaikan ambang batas ini](#configure-tool-search) atau menonaktifkan pencarian alat sepenuhnya. Ketika dipicu:

1. Alat MCP ditangguhkan daripada dimuat ke konteks sebelumnya
2. Claude menggunakan alat pencarian untuk menemukan alat MCP yang relevan saat diperlukan
3. Hanya alat yang benar-benar dibutuhkan Claude yang dimuat ke konteks
4. Alat MCP terus bekerja persis seperti sebelumnya dari perspektif Anda

### Untuk penulis server MCP

Jika Anda membangun server MCP, field instruksi server menjadi lebih berguna dengan Pencarian Alat yang diaktifkan. Instruksi server membantu Claude memahami kapan harus mencari alat Anda, mirip dengan cara [skills](/id/skills) bekerja.

Tambahkan instruksi server yang jelas dan deskriptif yang menjelaskan:

* Kategori tugas apa yang ditangani alat Anda
* Kapan Claude harus mencari alat Anda
* Kemampuan utama yang disediakan server Anda

### Konfigurasi pencarian alat

Pencarian alat diaktifkan secara default: alat MCP ditangguhkan dan ditemukan sesuai permintaan. Ketika `ANTHROPIC_BASE_URL` menunjuk ke host non-pihak pertama, pencarian alat dinonaktifkan secara default karena sebagian besar proxy tidak meneruskan blok `tool_reference`. Atur `ENABLE_TOOL_SEARCH` secara eksplisit jika proxy Anda melakukannya. Fitur ini memerlukan model yang mendukung blok `tool_reference`: Sonnet 4 dan lebih baru, atau Opus 4 dan lebih baru. Model Haiku tidak mendukung pencarian alat.

Kontrol perilaku pencarian alat dengan variabel lingkungan `ENABLE_TOOL_SEARCH`:

| Nilai          | Perilaku                                                                                           |
| :------------- | :------------------------------------------------------------------------------------------------- |
| (tidak diatur) | Diaktifkan secara default. Dinonaktifkan ketika `ANTHROPIC_BASE_URL` adalah host non-pihak pertama |
| `true`         | Selalu diaktifkan, termasuk untuk `ANTHROPIC_BASE_URL` non-pihak pertama                           |
| `auto`         | Diaktifkan ketika alat MCP melebihi 10% konteks                                                    |
| `auto:<N>`     | Diaktifkan pada ambang batas khusus, di mana `<N>` adalah persentase (misalnya, `auto:5` untuk 5%) |
| `false`        | Dinonaktifkan, semua alat MCP dimuat sebelumnya                                                    |

```bash  theme={null}
# Gunakan ambang batas khusus 5%
ENABLE_TOOL_SEARCH=auto:5 claude

# Nonaktifkan pencarian alat sepenuhnya
ENABLE_TOOL_SEARCH=false claude
```

Atau atur nilai dalam [field `env` settings.json](/id/settings#available-settings) Anda.

Anda juga dapat menonaktifkan alat MCPSearch secara khusus menggunakan pengaturan `disallowedTools`:

```json  theme={null}
{
  "permissions": {
    "deny": ["MCPSearch"]
  }
}
```

## Gunakan prompt MCP sebagai perintah

Server MCP dapat mengekspos prompt yang menjadi tersedia sebagai perintah di Claude Code.

### Jalankan prompt MCP

<Steps>
  <Step title="Temukan prompt yang tersedia">
    Ketik `/` untuk melihat semua perintah yang tersedia, termasuk yang dari server MCP. Prompt MCP muncul dengan format `/mcp__servername__promptname`.
  </Step>

  <Step title="Jalankan prompt tanpa argumen">
    ```text  theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Jalankan prompt dengan argumen">
    Banyak prompt menerima argumen. Teruskan mereka dipisahkan spasi setelah perintah:

    ```text  theme={null}
    /mcp__github__pr_review 456
    ```

    ```text  theme={null}
    /mcp__jira__create_issue "Bug in login flow" high
    ```
  </Step>
</Steps>

<Tip>
  Tips:

  * Prompt MCP ditemukan secara dinamis dari server yang terhubung
  * Argumen diurai berdasarkan parameter yang ditentukan prompt
  * Hasil prompt disuntikkan langsung ke dalam percakapan
  * Nama server dan prompt dinormalisasi (spasi menjadi garis bawah)
</Tip>

## Konfigurasi MCP yang dikelola

Untuk organisasi yang memerlukan kontrol terpusat atas server MCP, Claude Code mendukung dua opsi konfigurasi:

1. **Kontrol eksklusif dengan `managed-mcp.json`**: Terapkan set server MCP tetap yang tidak dapat dimodifikasi atau diperluas pengguna
2. **Kontrol berbasis kebijakan dengan daftar putih/daftar hitam**: Izinkan pengguna menambahkan server mereka sendiri, tetapi batasi server mana yang diizinkan

Opsi ini memungkinkan administrator IT untuk:

* **Kontrol server MCP mana yang dapat diakses karyawan**: Terapkan set server MCP yang disetujui secara standar di seluruh organisasi
* **Cegah server MCP yang tidak sah**: Batasi pengguna dari menambahkan server MCP yang tidak disetujui
* **Nonaktifkan MCP sepenuhnya**: Hapus fungsionalitas MCP sepenuhnya jika diperlukan

### Opsi 1: Kontrol eksklusif dengan managed-mcp.json

Ketika Anda menerapkan file `managed-mcp.json`, file tersebut mengambil **kontrol eksklusif** atas semua server MCP. Pengguna tidak dapat menambahkan, memodifikasi, atau menggunakan server MCP apa pun selain yang ditentukan dalam file ini. Ini adalah pendekatan paling sederhana untuk organisasi yang menginginkan kontrol penuh.

Administrator sistem menerapkan file konfigurasi ke direktori sistem:

* macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux dan WSL: `/etc/claude-code/managed-mcp.json`
* Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

<Note>
  Ini adalah jalur sistem (bukan direktori home pengguna seperti `~/Library/...`) yang memerlukan hak istimewa administrator. Mereka dirancang untuk diterapkan oleh administrator IT.
</Note>

File `managed-mcp.json` menggunakan format yang sama seperti file `.mcp.json` standar:

```json  theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Opsi 2: Kontrol berbasis kebijakan dengan daftar putih dan daftar hitam

Alih-alih mengambil kontrol eksklusif, administrator dapat mengizinkan pengguna mengonfigurasi server MCP mereka sendiri sambil memberlakukan pembatasan pada server mana yang diizinkan. Pendekatan ini menggunakan `allowedMcpServers` dan `deniedMcpServers` dalam [file pengaturan yang dikelola](/id/settings#settings-files).

<Note>
  **Memilih antara opsi**: Gunakan Opsi 1 (`managed-mcp.json`) ketika Anda ingin menerapkan set server tetap tanpa kustomisasi pengguna. Gunakan Opsi 2 (daftar putih/daftar hitam) ketika Anda ingin mengizinkan pengguna menambahkan server mereka sendiri dalam batasan kebijakan.
</Note>

#### Opsi pembatasan

Setiap entri dalam daftar putih atau daftar hitam dapat membatasi server dengan tiga cara:

1. **Berdasarkan nama server** (`serverName`): Cocok dengan nama server yang dikonfigurasi
2. **Berdasarkan perintah** (`serverCommand`): Cocok dengan perintah dan argumen yang tepat yang digunakan untuk memulai server stdio
3. **Berdasarkan pola URL** (`serverUrl`): Cocok dengan URL server jarak jauh dengan dukungan wildcard

**Penting**: Setiap entri harus memiliki tepat satu dari `serverName`, `serverCommand`, atau `serverUrl`.

#### Contoh konfigurasi

```json  theme={null}
{
  "allowedMcpServers": [
    // Izinkan berdasarkan nama server
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Izinkan berdasarkan perintah yang tepat (untuk server stdio)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Izinkan berdasarkan pola URL (untuk server jarak jauh)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Blokir berdasarkan nama server
    { "serverName": "dangerous-server" },

    // Blokir berdasarkan perintah yang tepat (untuk server stdio)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Blokir berdasarkan pola URL (untuk server jarak jauh)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### Cara kerja pembatasan berbasis perintah

**Pencocokan yang tepat**:

* Array perintah harus cocok **persis** - baik perintah maupun semua argumen dalam urutan yang benar
* Contoh: `["npx", "-y", "server"]` akan TIDAK cocok dengan `["npx", "server"]` atau `["npx", "-y", "server", "--flag"]`

**Perilaku server stdio**:

* Ketika daftar putih berisi **entri** `serverCommand` apa pun, server stdio **harus** cocok dengan salah satu perintah tersebut
* Server stdio tidak dapat lulus berdasarkan nama saja ketika pembatasan perintah ada
* Ini memastikan administrator dapat memberlakukan perintah mana yang diizinkan untuk dijalankan

**Perilaku server non-stdio**:

* Server jarak jauh (HTTP, SSE, WebSocket) menggunakan pencocokan berbasis URL ketika entri `serverUrl` ada dalam daftar putih
* Jika tidak ada entri URL, server jarak jauh kembali ke pencocokan berbasis nama
* Pembatasan perintah tidak berlaku untuk server jarak jauh

#### Cara kerja pembatasan berbasis URL

Pola URL mendukung wildcard menggunakan `*` untuk mencocokkan urutan karakter apa pun. Ini berguna untuk mengizinkan seluruh domain atau subdomain.

**Contoh wildcard**:

* `https://mcp.company.com/*` - Izinkan semua jalur di domain tertentu
* `https://*.example.com/*` - Izinkan subdomain apa pun dari example.com
* `http://localhost:*/*` - Izinkan port apa pun di localhost

**Perilaku server jarak jauh**:

* Ketika daftar putih berisi **entri** `serverUrl` apa pun, server jarak jauh **harus** cocok dengan salah satu pola URL tersebut
* Server jarak jauh tidak dapat lulus berdasarkan nama saja ketika pembatasan URL ada
* Ini memastikan administrator dapat memberlakukan endpoint jarak jauh mana yang diizinkan

<Accordion title="Contoh: Daftar putih hanya URL">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.company.com/*" },
      { "serverUrl": "https://*.internal.corp/*" }
    ]
  }
  ```

  **Hasil**:

  * Server HTTP di `https://mcp.company.com/api`: ✅ Diizinkan (cocok dengan pola URL)
  * Server HTTP di `https://api.internal.corp/mcp`: ✅ Diizinkan (cocok dengan wildcard subdomain)
  * Server HTTP di `https://external.com/mcp`: ❌ Diblokir (tidak cocok dengan pola URL apa pun)
  * Server stdio dengan perintah apa pun: ❌ Diblokir (tidak ada entri nama atau perintah untuk dicocokkan)
</Accordion>

<Accordion title="Contoh: Daftar putih hanya perintah">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Hasil**:

  * Server stdio dengan `["npx", "-y", "approved-package"]`: ✅ Diizinkan (cocok dengan perintah)
  * Server stdio dengan `["node", "server.js"]`: ❌ Diblokir (tidak cocok dengan perintah)
  * Server HTTP bernama "my-api": ❌ Diblokir (tidak ada entri nama untuk dicocokkan)
</Accordion>

<Accordion title="Contoh: Daftar putih nama dan perintah campuran">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Hasil**:

  * Server stdio bernama "local-tool" dengan `["npx", "-y", "approved-package"]`: ✅ Diizinkan (cocok dengan perintah)
  * Server stdio bernama "local-tool" dengan `["node", "server.js"]`: ❌ Diblokir (entri perintah ada tetapi tidak cocok)
  * Server stdio bernama "github" dengan `["node", "server.js"]`: ❌ Diblokir (server stdio harus cocok dengan perintah ketika entri perintah ada)
  * Server HTTP bernama "github": ✅ Diizinkan (cocok dengan nama)
  * Server HTTP bernama "other-api": ❌ Diblokir (nama tidak cocok)
</Accordion>

<Accordion title="Contoh: Daftar putih hanya nama">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  **Hasil**:

  * Server stdio bernama "github" dengan perintah apa pun: ✅ Diizinkan (tidak ada pembatasan perintah)
  * Server stdio bernama "internal-tool" dengan perintah apa pun: ✅ Diizinkan (tidak ada pembatasan perintah)
  * Server HTTP bernama "github": ✅ Diizinkan (cocok dengan nama)
  * Server apa pun bernama "other": ❌ Diblokir (nama tidak cocok)
</Accordion>

#### Perilaku daftar putih (`allowedMcpServers`)

* `undefined` (default): Tidak ada pembatasan - pengguna dapat mengonfigurasi server MCP apa pun
* Array kosong `[]`: Penguncian lengkap - pengguna tidak dapat mengonfigurasi server MCP apa pun
* Daftar entri: Pengguna hanya dapat mengonfigurasi server yang cocok berdasarkan nama, perintah, atau pola URL

#### Perilaku daftar hitam (`deniedMcpServers`)

* `undefined` (default): Tidak ada server yang diblokir
* Array kosong `[]`: Tidak ada server yang diblokir
* Daftar entri: Server yang ditentukan secara eksplisit diblokir di semua cakupan

#### Catatan penting

* **Opsi 1 dan Opsi 2 dapat digabungkan**: Jika `managed-mcp.json` ada, file tersebut memiliki kontrol eksklusif dan pengguna tidak dapat menambahkan server. Daftar putih/daftar hitam masih berlaku untuk server yang dikelola itu sendiri.
* **Daftar hitam mengambil prioritas absolut**: Jika server cocok dengan entri daftar hitam (berdasarkan nama, perintah, atau URL), server akan diblokir bahkan jika ada di daftar putih
* Pembatasan berbasis nama, berbasis perintah, dan berbasis URL bekerja bersama: server lulus jika cocok dengan **entri** nama, entri perintah, atau pola URL (kecuali diblokir oleh daftar hitam)

<Note>
  **Saat menggunakan `managed-mcp.json`**: Pengguna tidak dapat menambahkan server MCP melalui `claude mcp add` atau file konfigurasi. Pengaturan `allowedMcpServers` dan `deniedMcpServers` masih berlaku untuk memfilter server yang dikelola mana yang benar-benar dimuat.
</Note>
