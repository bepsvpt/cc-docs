> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Buat dan distribusikan marketplace plugin

> Bangun dan hosting marketplace plugin untuk mendistribusikan ekstensi Claude Code di seluruh tim dan komunitas.

Sebuah **marketplace plugin** adalah katalog yang memungkinkan Anda mendistribusikan plugin kepada orang lain. Marketplace menyediakan penemuan terpusat, pelacakan versi, pembaruan otomatis, dan dukungan untuk berbagai jenis sumber (repositori git, jalur lokal, dan lainnya). Panduan ini menunjukkan cara membuat marketplace Anda sendiri untuk berbagi plugin dengan tim atau komunitas Anda.

Mencari cara memasang plugin dari marketplace yang sudah ada? Lihat [Temukan dan pasang plugin yang sudah dibuat](/id/discover-plugins).

## Ikhtisar

Membuat dan mendistribusikan marketplace melibatkan:

1. **Membuat plugin**: bangun satu atau lebih plugin dengan commands, agents, hooks, MCP servers, atau LSP servers. Panduan ini mengasumsikan Anda sudah memiliki plugin untuk didistribusikan; lihat [Buat plugin](/id/plugins) untuk detail tentang cara membuat plugin.
2. **Membuat file marketplace**: tentukan `marketplace.json` yang mencantumkan plugin Anda dan di mana menemukannya (lihat [Buat file marketplace](#create-the-marketplace-file)).
3. **Host marketplace**: dorong ke GitHub, GitLab, atau host git lainnya (lihat [Host dan distribusikan marketplace](#host-and-distribute-marketplaces)).
4. **Bagikan dengan pengguna**: pengguna menambahkan marketplace Anda dengan `/plugin marketplace add` dan memasang plugin individual (lihat [Temukan dan pasang plugin](/id/discover-plugins)).

Setelah marketplace Anda aktif, Anda dapat memperbaruinya dengan mendorong perubahan ke repositori Anda. Pengguna menyegarkan salinan lokal mereka dengan `/plugin marketplace update`.

## Panduan: buat marketplace lokal

Contoh ini membuat marketplace dengan satu plugin: skill `/quality-review` untuk ulasan kode. Anda akan membuat struktur direktori, menambahkan skill, membuat manifest plugin dan katalog marketplace, kemudian memasang dan mengujinya.

<Steps>
  <Step title="Buat struktur direktori">
    ```bash  theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Buat skill">
    Buat file `SKILL.md` yang mendefinisikan apa yang dilakukan skill `/quality-review`.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Review code for bugs, security, and performance
    disable-model-invocation: true
    ---

    Review the code I've selected or the recent changes for:
    - Potential bugs or edge cases
    - Security concerns
    - Performance issues
    - Readability improvements

    Be concise and actionable.
    ```
  </Step>

  <Step title="Buat manifest plugin">
    Buat file `plugin.json` yang mendeskripsikan plugin. Manifest berada di direktori `.claude-plugin/`.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Adds a /quality-review skill for quick code reviews",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Buat file marketplace">
    Buat katalog marketplace yang mencantumkan plugin Anda.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Adds a /quality-review skill for quick code reviews"
        }
      ]
    }
    ```
  </Step>

  <Step title="Tambahkan dan pasang">
    Tambahkan marketplace dan pasang plugin.

    ```shell  theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Coba">
    Pilih beberapa kode di editor Anda dan jalankan perintah baru Anda.

    ```shell  theme={null}
    /quality-review
    ```
  </Step>
</Steps>

Untuk mempelajari lebih lanjut tentang apa yang dapat dilakukan plugin, termasuk hooks, agents, MCP servers, dan LSP servers, lihat [Plugins](/id/plugins).

<Note>
  **Cara plugin dipasang**: Ketika pengguna memasang plugin, Claude Code menyalin direktori plugin ke lokasi cache. Ini berarti plugin tidak dapat mereferensikan file di luar direktorinya menggunakan jalur seperti `../shared-utils`, karena file tersebut tidak akan disalin.

  Jika Anda perlu berbagi file di seluruh plugin, gunakan symlink (yang diikuti selama penyalinan). Lihat [Plugin caching and file resolution](/id/plugins-reference#plugin-caching-and-file-resolution) untuk detail.
</Note>

## Buat file marketplace

Buat `.claude-plugin/marketplace.json` di root repositori Anda. File ini mendefinisikan nama marketplace Anda, informasi pemilik, dan daftar plugin dengan sumbernya.

Setiap entri plugin memerlukan minimal `name` dan `source` (di mana mengambilnya). Lihat [skema lengkap](#marketplace-schema) di bawah untuk semua field yang tersedia.

```json  theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Skema marketplace

### Field yang diperlukan

| Field     | Type   | Deskripsi                                                                                                                                                                | Contoh         |
| :-------- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| `name`    | string | Identifier marketplace (kebab-case, tanpa spasi). Ini menghadap publik: pengguna melihatnya saat memasang plugin (misalnya, `/plugin install my-tool@your-marketplace`). | `"acme-tools"` |
| `owner`   | object | Informasi pengelola marketplace ([lihat field di bawah](#owner-fields))                                                                                                  |                |
| `plugins` | array  | Daftar plugin yang tersedia                                                                                                                                              | Lihat di bawah |

<Note>
  **Nama yang dicadangkan**: Nama marketplace berikut dicadangkan untuk penggunaan resmi Anthropic dan tidak dapat digunakan oleh marketplace pihak ketiga: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Nama yang meniru marketplace resmi (seperti `official-claude-plugins` atau `anthropic-tools-v2`) juga diblokir.
</Note>

### Field pemilik

| Field   | Type   | Diperlukan | Deskripsi                    |
| :------ | :----- | :--------- | :--------------------------- |
| `name`  | string | Ya         | Nama pengelola atau tim      |
| `email` | string | Tidak      | Email kontak untuk pengelola |

### Metadata opsional

| Field                  | Type   | Deskripsi                                                                                                                                                                               |
| :--------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | Deskripsi marketplace singkat                                                                                                                                                           |
| `metadata.version`     | string | Versi marketplace                                                                                                                                                                       |
| `metadata.pluginRoot`  | string | Direktori dasar yang ditambahkan ke jalur sumber plugin relatif (misalnya, `"./plugins"` memungkinkan Anda menulis `"source": "formatter"` alih-alih `"source": "./plugins/formatter"`) |

## Entri plugin

Setiap entri plugin dalam array `plugins` mendeskripsikan plugin dan di mana menemukannya. Anda dapat menyertakan field apa pun dari [skema manifest plugin](/id/plugins-reference#plugin-manifest-schema) (seperti `description`, `version`, `author`, `commands`, `hooks`, dll.), ditambah field khusus marketplace ini: `source`, `category`, `tags`, dan `strict`.

### Field yang diperlukan

| Field    | Type           | Deskripsi                                                                                                                                                 |
| :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Identifier plugin (kebab-case, tanpa spasi). Ini menghadap publik: pengguna melihatnya saat memasang (misalnya, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Di mana mengambil plugin (lihat [Plugin sources](#plugin-sources) di bawah)                                                                               |

### Field plugin opsional

**Field metadata standar:**

| Field         | Type    | Deskripsi                                                                                                                            |
| :------------ | :------ | :----------------------------------------------------------------------------------------------------------------------------------- |
| `description` | string  | Deskripsi plugin singkat                                                                                                             |
| `version`     | string  | Versi plugin                                                                                                                         |
| `author`      | object  | Informasi penulis plugin (`name` diperlukan, `email` opsional)                                                                       |
| `homepage`    | string  | URL homepage atau dokumentasi plugin                                                                                                 |
| `repository`  | string  | URL repositori kode sumber                                                                                                           |
| `license`     | string  | Identifier lisensi SPDX (misalnya, MIT, Apache-2.0)                                                                                  |
| `keywords`    | array   | Tag untuk penemuan dan kategorisasi plugin                                                                                           |
| `category`    | string  | Kategori plugin untuk organisasi                                                                                                     |
| `tags`        | array   | Tag untuk kemudahan pencarian                                                                                                        |
| `strict`      | boolean | Mengontrol apakah `plugin.json` adalah otoritas untuk definisi komponen (default: true). Lihat [Strict mode](#strict-mode) di bawah. |

**Field konfigurasi komponen:**

| Field        | Type           | Deskripsi                                         |
| :----------- | :------------- | :------------------------------------------------ |
| `commands`   | string\|array  | Jalur kustom ke file atau direktori command       |
| `agents`     | string\|array  | Jalur kustom ke file agent                        |
| `hooks`      | string\|object | Konfigurasi hooks kustom atau jalur ke file hooks |
| `mcpServers` | string\|object | Konfigurasi MCP server atau jalur ke config MCP   |
| `lspServers` | string\|object | Konfigurasi LSP server atau jalur ke config LSP   |

## Plugin sources

Plugin sources memberitahu Claude Code di mana mengambil setiap plugin individual yang tercantum di marketplace Anda. Ini diatur dalam field `source` dari setiap entri plugin di `marketplace.json`.

Setelah plugin diklon atau disalin ke mesin lokal, plugin disalin ke cache plugin lokal yang diversi di `~/.claude/plugins/cache`.

| Source        | Type                                | Fields                             | Catatan                                                                                         |
| ------------- | ----------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| Relative path | `string` (misalnya `"./my-plugin"`) | none                               | Direktori lokal dalam repo marketplace. Harus dimulai dengan `./`                               |
| `github`      | object                              | `repo`, `ref?`, `sha?`             |                                                                                                 |
| `url`         | object                              | `url`, `ref?`, `sha?`              | Sumber URL Git                                                                                  |
| `git-subdir`  | object                              | `url`, `path`, `ref?`, `sha?`      | Subdirektori dalam repo git. Mengklon secara sparse untuk meminimalkan bandwidth untuk monorepo |
| `npm`         | object                              | `package`, `version?`, `registry?` | Dipasang via `npm install`                                                                      |

<Note>
  **Marketplace sources vs plugin sources**: Ini adalah konsep berbeda yang mengontrol hal berbeda.

  * **Marketplace source** — di mana mengambil katalog `marketplace.json` itu sendiri. Diatur ketika pengguna menjalankan `/plugin marketplace add` atau dalam pengaturan `extraKnownMarketplaces`. Mendukung `ref` (branch/tag) tetapi bukan `sha`.
  * **Plugin source** — di mana mengambil plugin individual yang tercantum di marketplace. Diatur dalam field `source` dari setiap entri plugin di dalam `marketplace.json`. Mendukung baik `ref` (branch/tag) maupun `sha` (commit yang tepat).

  Misalnya, marketplace yang dihosting di `acme-corp/plugin-catalog` (marketplace source) dapat mencantumkan plugin yang diambil dari `acme-corp/code-formatter` (plugin source). Marketplace source dan plugin source menunjuk ke repositori berbeda dan disematkan secara independen.
</Note>

### Jalur relatif

Untuk plugin di repositori yang sama, gunakan jalur yang dimulai dengan `./`:

```json  theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Jalur diselesaikan relatif terhadap root marketplace, yang merupakan direktori yang berisi `.claude-plugin/`. Dalam contoh di atas, `./plugins/my-plugin` menunjuk ke `<repo>/plugins/my-plugin`, meskipun `marketplace.json` berada di `<repo>/.claude-plugin/marketplace.json`. Jangan gunakan `../` untuk keluar dari `.claude-plugin/`.

<Note>
  Jalur relatif hanya berfungsi ketika pengguna menambahkan marketplace Anda melalui Git (GitHub, GitLab, atau URL git). Jika pengguna menambahkan marketplace Anda melalui URL langsung ke file `marketplace.json`, jalur relatif tidak akan terselesaikan dengan benar. Untuk distribusi berbasis URL, gunakan sumber GitHub, npm, atau URL git sebagai gantinya. Lihat [Troubleshooting](#plugins-with-relative-paths-fail-in-url-based-marketplaces) untuk detail.
</Note>

### Repositori GitHub

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Anda dapat menyematkan ke branch, tag, atau commit tertentu:

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Field  | Type   | Deskripsi                                                                        |
| :----- | :----- | :------------------------------------------------------------------------------- |
| `repo` | string | Diperlukan. Repositori GitHub dalam format `owner/repo`                          |
| `ref`  | string | Opsional. Branch atau tag Git (default ke branch default repositori)             |
| `sha`  | string | Opsional. SHA commit git 40-karakter penuh untuk menyematkan ke versi yang tepat |

### Repositori Git

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Anda dapat menyematkan ke branch, tag, atau commit tertentu:

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Field | Type   | Deskripsi                                                                                                                                                  |
| :---- | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Diperlukan. URL repositori git lengkap (`https://` atau `git@`). Akhiran `.git` opsional, jadi URL Azure DevOps dan AWS CodeCommit tanpa akhiran berfungsi |
| `ref` | string | Opsional. Branch atau tag Git (default ke branch default repositori)                                                                                       |
| `sha` | string | Opsional. SHA commit git 40-karakter penuh untuk menyematkan ke versi yang tepat                                                                           |

### Subdirektori Git

Gunakan `git-subdir` untuk menunjuk ke plugin yang berada di dalam subdirektori repositori git. Claude Code menggunakan klon parsial dan sparse untuk mengambil hanya subdirektori, meminimalkan bandwidth untuk monorepo besar.

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Anda dapat menyematkan ke branch, tag, atau commit tertentu:

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

Field `url` juga menerima shorthand GitHub (`owner/repo`) atau URL SSH (`git@github.com:owner/repo.git`).

| Field  | Type   | Deskripsi                                                                                        |
| :----- | :----- | :----------------------------------------------------------------------------------------------- |
| `url`  | string | Diperlukan. URL repositori Git, shorthand GitHub `owner/repo`, atau URL SSH                      |
| `path` | string | Diperlukan. Jalur subdirektori dalam repo yang berisi plugin (misalnya, `"tools/claude-plugin"`) |
| `ref`  | string | Opsional. Branch atau tag Git (default ke branch default repositori)                             |
| `sha`  | string | Opsional. SHA commit git 40-karakter penuh untuk menyematkan ke versi yang tepat                 |

### Paket npm

Plugin yang didistribusikan sebagai paket npm dipasang menggunakan `npm install`. Ini berfungsi dengan paket apa pun di registry npm publik atau registry pribadi yang dihosting tim Anda.

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Untuk menyematkan ke versi tertentu, tambahkan field `version`:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Untuk memasang dari registry pribadi atau internal, tambahkan field `registry`:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Field      | Type   | Deskripsi                                                                              |
| :--------- | :----- | :------------------------------------------------------------------------------------- |
| `package`  | string | Diperlukan. Nama paket atau paket scoped (misalnya, `@org/plugin`)                     |
| `version`  | string | Opsional. Versi atau rentang versi (misalnya, `2.1.0`, `^2.0.0`, `~1.5.0`)             |
| `registry` | string | Opsional. URL registry npm kustom. Default ke registry npm sistem (biasanya npmjs.org) |

### Entri plugin lanjutan

Contoh ini menunjukkan entri plugin menggunakan banyak field opsional, termasuk jalur kustom untuk commands, agents, hooks, dan MCP servers:

```json  theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Hal-hal penting untuk diperhatikan:

* **`commands` dan `agents`**: Anda dapat menentukan beberapa direktori atau file individual. Jalur relatif terhadap root plugin.
* **`${CLAUDE_PLUGIN_ROOT}`**: Gunakan variabel ini dalam hooks dan config MCP server untuk mereferensikan file dalam direktori instalasi plugin. Ini diperlukan karena plugin disalin ke lokasi cache saat dipasang. Untuk dependensi atau state yang harus bertahan pembaruan plugin, gunakan [`${CLAUDE_PLUGIN_DATA}`](/id/plugins-reference#persistent-data-directory) sebagai gantinya.
* **`strict: false`**: Karena ini diatur ke false, plugin tidak memerlukan `plugin.json` sendiri. Entri marketplace mendefinisikan semuanya. Lihat [Strict mode](#strict-mode) di bawah.

### Strict mode

Field `strict` mengontrol apakah `plugin.json` adalah otoritas untuk definisi komponen (commands, agents, hooks, skills, MCP servers, output styles).

| Value            | Perilaku                                                                                                                                                      |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `true` (default) | `plugin.json` adalah otoritas. Entri marketplace dapat melengkapinya dengan komponen tambahan, dan kedua sumber digabungkan.                                  |
| `false`          | Entri marketplace adalah definisi lengkap. Jika plugin juga memiliki `plugin.json` yang mendeklarasikan komponen, itu adalah konflik dan plugin gagal dimuat. |

**Kapan menggunakan setiap mode:**

* **`strict: true`**: plugin memiliki `plugin.json` sendiri dan mengelola komponennya sendiri. Entri marketplace dapat menambahkan commands atau hooks tambahan di atas. Ini adalah default dan berfungsi untuk sebagian besar plugin.
* **`strict: false`**: operator marketplace menginginkan kontrol penuh. Repo plugin menyediakan file mentah, dan entri marketplace mendefinisikan file mana yang diekspos sebagai commands, agents, hooks, dll. Berguna ketika marketplace merestruktur atau mengkurasi komponen plugin secara berbeda dari yang dimaksudkan penulis plugin.

## Host dan distribusikan marketplace

### Host di GitHub (direkomendasikan)

GitHub menyediakan metode distribusi paling mudah:

1. **Buat repositori**: Siapkan repositori baru untuk marketplace Anda
2. **Tambahkan file marketplace**: Buat `.claude-plugin/marketplace.json` dengan definisi plugin Anda
3. **Bagikan dengan tim**: Pengguna menambahkan marketplace Anda dengan `/plugin marketplace add owner/repo`

**Manfaat**: Kontrol versi bawaan, pelacakan masalah, dan fitur kolaborasi tim.

### Host di layanan git lainnya

Layanan hosting git apa pun berfungsi, seperti GitLab, Bitbucket, dan server yang dihosting sendiri. Pengguna menambahkan dengan URL repositori lengkap:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Repositori pribadi

Claude Code mendukung pemasangan plugin dari repositori pribadi. Untuk instalasi manual dan pembaruan, Claude Code menggunakan helper kredensial git yang ada. Jika `git clone` berfungsi untuk repositori pribadi di terminal Anda, itu berfungsi di Claude Code juga. Helper kredensial umum termasuk `gh auth login` untuk GitHub, Keychain macOS, dan `git-credential-store`.

Pembaruan otomatis latar belakang berjalan saat startup tanpa helper kredensial, karena prompt interaktif akan memblokir Claude Code dari startup. Untuk mengaktifkan pembaruan otomatis untuk marketplace pribadi, atur token autentikasi yang sesuai di lingkungan Anda:

| Provider  | Variabel lingkungan            | Catatan                                    |
| :-------- | :----------------------------- | :----------------------------------------- |
| GitHub    | `GITHUB_TOKEN` atau `GH_TOKEN` | Token akses pribadi atau token GitHub App  |
| GitLab    | `GITLAB_TOKEN` atau `GL_TOKEN` | Token akses pribadi atau token proyek      |
| Bitbucket | `BITBUCKET_TOKEN`              | Sandi aplikasi atau token akses repositori |

Atur token dalam konfigurasi shell Anda (misalnya, `.bashrc`, `.zshrc`) atau teruskan saat menjalankan Claude Code:

```bash  theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Untuk lingkungan CI/CD, konfigurasikan token sebagai variabel lingkungan rahasia. GitHub Actions secara otomatis menyediakan `GITHUB_TOKEN` untuk repositori dalam organisasi yang sama.
</Note>

### Uji secara lokal sebelum distribusi

Uji marketplace Anda secara lokal sebelum berbagi:

```shell  theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Untuk rangkaian lengkap perintah add (GitHub, URL Git, jalur lokal, URL jarak jauh), lihat [Tambahkan marketplace](/id/discover-plugins#add-marketplaces).

### Wajibkan marketplace untuk tim Anda

Anda dapat mengonfigurasi repositori Anda sehingga anggota tim secara otomatis diminta untuk memasang marketplace Anda ketika mereka mempercayai folder proyek. Tambahkan marketplace Anda ke `.claude/settings.json`:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Anda juga dapat menentukan plugin mana yang harus diaktifkan secara default:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Untuk opsi konfigurasi lengkap, lihat [Plugin settings](/id/settings#plugin-settings).

<Note>
  Jika Anda menggunakan sumber `directory` atau `file` lokal dengan jalur relatif, jalur diselesaikan terhadap checkout utama repositori Anda. Ketika Anda menjalankan Claude Code dari git worktree, jalur masih menunjuk ke checkout utama, jadi semua worktrees berbagi lokasi marketplace yang sama. Status marketplace disimpan sekali per pengguna di `~/.claude/plugins/known_marketplaces.json`, bukan per proyek.
</Note>

### Pra-isi plugin untuk container

Untuk image container dan lingkungan CI, Anda dapat pra-isi direktori plugin saat waktu build sehingga Claude Code dimulai dengan marketplace dan plugin yang sudah tersedia, tanpa mengklon apa pun saat runtime. Atur variabel lingkungan `CLAUDE_CODE_PLUGIN_SEED_DIR` untuk menunjuk ke direktori ini.

Untuk melapisi beberapa direktori seed, pisahkan jalur dengan `:` di Unix atau `;` di Windows. Claude Code mencari setiap direktori secara berurutan, dan seed pertama yang berisi marketplace atau cache plugin yang diberikan menang.

Direktori seed mencerminkan struktur `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

Cara paling sederhana untuk membangun direktori seed adalah menjalankan Claude Code sekali selama image build, memasang plugin yang Anda butuhkan, kemudian menyalin direktori `~/.claude/plugins` yang dihasilkan ke image Anda dan menunjuk `CLAUDE_CODE_PLUGIN_SEED_DIR` ke sana.

Saat startup, Claude Code mendaftarkan marketplace yang ditemukan di `known_marketplaces.json` seed ke dalam konfigurasi utama, dan menggunakan cache plugin yang ditemukan di bawah `cache/` di tempat tanpa mengklon ulang. Ini berfungsi dalam mode interaktif dan mode non-interaktif dengan flag `-p`.

Detail perilaku:

* **Read-only**: direktori seed tidak pernah ditulis. Pembaruan otomatis dinonaktifkan untuk marketplace seed karena git pull akan gagal di filesystem read-only.
* **Entri seed mengambil prioritas**: marketplace yang dideklarasikan dalam seed menimpa entri yang cocok apa pun dalam konfigurasi pengguna di setiap startup. Untuk opt out dari plugin seed, gunakan `/plugin disable` daripada menghapus marketplace.
* **Resolusi jalur**: Claude Code menemukan konten marketplace dengan menyelidiki `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` saat runtime, bukan dengan mempercayai jalur yang disimpan di dalam JSON seed. Ini berarti seed berfungsi dengan benar bahkan ketika dipasang di jalur berbeda dari tempat dibangun.
* **Komposisi dengan pengaturan**: jika `extraKnownMarketplaces` atau `enabledPlugins` mendeklarasikan marketplace yang sudah ada di seed, Claude Code menggunakan salinan seed alih-alih mengklon.

### Pembatasan marketplace yang dikelola

Untuk organisasi yang memerlukan kontrol ketat atas sumber plugin, administrator dapat membatasi marketplace plugin mana yang diizinkan pengguna untuk tambahkan menggunakan pengaturan [`strictKnownMarketplaces`](/id/settings#strictknownmarketplaces) dalam pengaturan yang dikelola.

Ketika `strictKnownMarketplaces` dikonfigurasi dalam pengaturan yang dikelola, perilaku pembatasan tergantung pada nilainya:

| Value                       | Perilaku                                                                                |
| --------------------------- | --------------------------------------------------------------------------------------- |
| Tidak terdefinisi (default) | Tidak ada pembatasan. Pengguna dapat menambahkan marketplace apa pun                    |
| Array kosong `[]`           | Lockdown lengkap. Pengguna tidak dapat menambahkan marketplace baru apa pun             |
| Daftar sumber               | Pengguna hanya dapat menambahkan marketplace yang cocok dengan daftar izin secara tepat |

#### Konfigurasi umum

Nonaktifkan semua penambahan marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Izinkan marketplace tertentu saja:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Izinkan semua marketplace dari server git internal menggunakan pencocokan pola regex pada host. Ini adalah pendekatan yang direkomendasikan untuk [GitHub Enterprise Server](/id/github-enterprise-server#plugin-marketplaces-on-ghes) atau instance GitLab yang dihosting sendiri:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Izinkan marketplace berbasis filesystem dari direktori tertentu menggunakan pencocokan pola regex pada jalur:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Gunakan `".*"` sebagai `pathPattern` untuk mengizinkan jalur filesystem apa pun sambil tetap mengontrol sumber jaringan dengan `hostPattern`.

<Note>
  `strictKnownMarketplaces` membatasi apa yang dapat ditambahkan pengguna, tetapi tidak mendaftarkan marketplace dengan sendirinya. Untuk membuat marketplace yang diizinkan tersedia secara otomatis tanpa pengguna menjalankan `/plugin marketplace add`, pasangkan dengan [`extraKnownMarketplaces`](/id/settings#extraknownmarketplaces) dalam `managed-settings.json` yang sama. Lihat [Menggunakan keduanya bersama-sama](/id/settings#strictknownmarketplaces).
</Note>

#### Cara pembatasan bekerja

Pembatasan divalidasi awal dalam proses instalasi plugin, sebelum permintaan jaringan atau operasi filesystem apa pun terjadi. Ini mencegah upaya akses marketplace yang tidak sah.

Daftar izin menggunakan pencocokan tepat untuk sebagian besar jenis sumber. Agar marketplace diizinkan, semua field yang ditentukan harus cocok secara tepat:

* Untuk sumber GitHub: `repo` diperlukan, dan `ref` atau `path` juga harus cocok jika ditentukan dalam daftar izin
* Untuk sumber URL: URL lengkap harus cocok secara tepat
* Untuk sumber `hostPattern`: host marketplace dicocokkan dengan pola regex
* Untuk sumber `pathPattern`: jalur filesystem marketplace dicocokkan dengan pola regex

Karena `strictKnownMarketplaces` diatur dalam [pengaturan yang dikelola](/id/settings#settings-files), konfigurasi pengguna individual dan proyek tidak dapat mengganti pembatasan ini.

Untuk detail konfigurasi lengkap termasuk semua jenis sumber yang didukung dan perbandingan dengan `extraKnownMarketplaces`, lihat [referensi strictKnownMarketplaces](/id/settings#strictknownmarketplaces).

### Resolusi versi dan saluran rilis

Versi plugin menentukan jalur cache dan deteksi pembaruan. Anda dapat menentukan versi dalam manifest plugin (`plugin.json`) atau dalam entri marketplace (`marketplace.json`).

<Warning>
  Jika memungkinkan, hindari menetapkan versi di kedua tempat. Manifest plugin selalu menang secara diam-diam, yang dapat menyebabkan versi marketplace diabaikan. Untuk plugin jalur relatif, atur versi dalam entri marketplace. Untuk semua sumber plugin lainnya, atur dalam manifest plugin.
</Warning>

#### Siapkan saluran rilis

Untuk mendukung saluran rilis "stable" dan "latest" untuk plugin Anda, Anda dapat menyiapkan dua marketplace yang menunjuk ke refs atau SHA berbeda dari repo yang sama. Anda kemudian dapat menetapkan dua marketplace ke grup pengguna berbeda melalui [pengaturan yang dikelola](/id/settings#settings-files).

<Warning>
  `plugin.json` plugin harus mendeklarasikan `version` berbeda di setiap ref atau commit yang disematkan. Jika dua refs atau commits memiliki versi manifest yang sama, Claude Code memperlakukannya sebagai identik dan melewati pembaruan.
</Warning>

##### Contoh

```json  theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json  theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Tetapkan saluran ke grup pengguna

Tetapkan setiap marketplace ke grup pengguna yang sesuai melalui pengaturan yang dikelola. Misalnya, grup stabil menerima:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

Grup early-access menerima `latest-tools` sebagai gantinya:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Validasi dan pengujian

Uji marketplace Anda sebelum berbagi.

Validasi sintaks JSON marketplace Anda:

```bash  theme={null}
claude plugin validate .
```

Atau dari dalam Claude Code:

```shell  theme={null}
/plugin validate .
```

Tambahkan marketplace untuk pengujian:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace
```

Pasang plugin uji untuk memverifikasi semuanya berfungsi:

```shell  theme={null}
/plugin install test-plugin@marketplace-name
```

Untuk alur kerja pengujian plugin lengkap, lihat [Uji plugin Anda secara lokal](/id/plugins#test-your-plugins-locally). Untuk troubleshooting teknis, lihat [Plugins reference](/id/plugins-reference).

## Troubleshooting

### Marketplace tidak memuat

**Gejala**: Tidak dapat menambahkan marketplace atau melihat plugin darinya

**Solusi**:

* Verifikasi URL marketplace dapat diakses
* Periksa bahwa `.claude-plugin/marketplace.json` ada di jalur yang ditentukan
* Pastikan sintaks JSON valid dan frontmatter terbentuk dengan baik menggunakan `claude plugin validate` atau `/plugin validate`
* Untuk repositori pribadi, konfirmasi Anda memiliki izin akses

### Kesalahan validasi marketplace

Jalankan `claude plugin validate .` atau `/plugin validate .` dari direktori marketplace Anda untuk memeriksa masalah. Validator memeriksa `plugin.json`, frontmatter skill/agent/command, dan `hooks/hooks.json` untuk kesalahan sintaks dan skema. Kesalahan umum:

| Kesalahan                                         | Penyebab                                               | Solusi                                                                                                          |
| :------------------------------------------------ | :----------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | Manifest hilang                                        | Buat `.claude-plugin/marketplace.json` dengan field yang diperlukan                                             |
| `Invalid JSON syntax: Unexpected token...`        | Kesalahan sintaks JSON dalam marketplace.json          | Periksa koma yang hilang, koma ekstra, atau string yang tidak dikutip                                           |
| `Duplicate plugin name "x" found in marketplace`  | Dua plugin berbagi nama yang sama                      | Berikan setiap plugin nilai `name` yang unik                                                                    |
| `plugins[0].source: Path contains ".."`           | Jalur sumber berisi `..`                               | Gunakan jalur relatif terhadap root marketplace tanpa `..`. Lihat [Jalur relatif](#relative-paths)              |
| `YAML frontmatter failed to parse: ...`           | YAML tidak valid dalam file skill, agent, atau command | Perbaiki sintaks YAML dalam blok frontmatter. Saat runtime file ini dimuat tanpa metadata.                      |
| `Invalid JSON syntax: ...` (hooks.json)           | `hooks/hooks.json` yang tidak terbentuk dengan baik    | Perbaiki sintaks JSON. `hooks/hooks.json` yang tidak terbentuk dengan baik mencegah seluruh plugin dari dimuat. |

**Peringatan** (non-blocking):

* `Marketplace has no plugins defined`: tambahkan setidaknya satu plugin ke array `plugins`
* `No marketplace description provided`: tambahkan `metadata.description` untuk membantu pengguna memahami marketplace Anda
* `Plugin name "x" is not kebab-case`: nama plugin berisi huruf besar, spasi, atau karakter khusus. Ubah nama menjadi huruf kecil, digit, dan tanda hubung saja (misalnya, `my-plugin`). Claude Code menerima bentuk lain, tetapi sinkronisasi marketplace Claude.ai menolaknya.

### Kegagalan instalasi plugin

**Gejala**: Marketplace muncul tetapi instalasi plugin gagal

**Solusi**:

* Verifikasi URL sumber plugin dapat diakses
* Periksa bahwa direktori plugin berisi file yang diperlukan
* Untuk sumber GitHub, pastikan repositori publik atau Anda memiliki akses
* Uji sumber plugin secara manual dengan mengklon/mengunduh

### Autentikasi repositori pribadi gagal

**Gejala**: Kesalahan autentikasi saat memasang plugin dari repositori pribadi

**Solusi**:

Untuk instalasi manual dan pembaruan:

* Verifikasi Anda diautentikasi dengan penyedia git Anda (misalnya, jalankan `gh auth status` untuk GitHub)
* Periksa bahwa helper kredensial Anda dikonfigurasi dengan benar: `git config --global credential.helper`
* Coba klon repositori secara manual untuk memverifikasi kredensial Anda berfungsi

Untuk pembaruan otomatis latar belakang:

* Atur token yang sesuai di lingkungan Anda: `echo $GITHUB_TOKEN`
* Periksa bahwa token memiliki izin yang diperlukan (akses baca ke repositori)
* Untuk GitHub, pastikan token memiliki scope `repo` untuk repositori pribadi
* Untuk GitLab, pastikan token memiliki setidaknya scope `read_repository`
* Verifikasi token belum kedaluwarsa

### Marketplace updates fail in offline environments

**Gejala**: Marketplace `git pull` gagal dan Claude Code menghapus cache yang ada, menyebabkan plugin menjadi tidak tersedia.

**Penyebab**: Secara default, ketika `git pull` gagal, Claude Code menghapus klon yang sudah usang dan mencoba mengklon ulang. Di lingkungan offline atau airgapped, mengklon ulang gagal dengan cara yang sama, meninggalkan direktori marketplace kosong.

**Solusi**: Atur `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` untuk menyimpan cache yang ada ketika pull gagal alih-alih menghapusnya:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

Dengan variabel ini diatur, Claude Code mempertahankan klon marketplace yang sudah usang pada kegagalan `git pull` dan terus menggunakan status terakhir yang diketahui baik. Untuk deployment yang sepenuhnya offline di mana repositori tidak akan pernah dapat dijangkau, gunakan [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers) untuk pra-isi direktori plugin saat waktu build sebagai gantinya.

### Git operations time out

**Gejala**: Instalasi plugin atau pembaruan marketplace gagal dengan kesalahan timeout seperti "Git clone timed out after 120s" atau "Git pull timed out after 120s".

**Penyebab**: Claude Code menggunakan timeout 120 detik untuk semua operasi git, termasuk mengklon repositori plugin dan menarik pembaruan marketplace. Repositori besar atau koneksi jaringan lambat mungkin melebihi batas ini.

**Solusi**: Tingkatkan timeout menggunakan variabel lingkungan `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. Nilainya dalam milidetik:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutes
```

### Plugins with relative paths fail in URL-based marketplaces

**Gejala**: Menambahkan marketplace melalui URL (seperti `https://example.com/marketplace.json`), tetapi plugin dengan sumber jalur relatif seperti `"./plugins/my-plugin"` gagal dipasang dengan kesalahan "path not found".

**Penyebab**: Marketplace berbasis URL hanya mengunduh file `marketplace.json` itu sendiri. Mereka tidak mengunduh file plugin dari server. Jalur relatif dalam entri marketplace mereferensikan file di server jarak jauh yang tidak diunduh.

**Solusi**:

* **Gunakan sumber eksternal**: Ubah entri plugin untuk menggunakan sumber GitHub, npm, atau URL git alih-alih jalur relatif:
  ```json  theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Gunakan marketplace berbasis Git**: Host marketplace Anda di repositori Git dan tambahkan dengan URL git. Marketplace berbasis Git mengklon seluruh repositori, membuat jalur relatif berfungsi dengan benar.

### Files not found after installation

**Gejala**: Plugin dipasang tetapi referensi ke file gagal, terutama file di luar direktori plugin

**Penyebab**: Plugin disalin ke direktori cache daripada digunakan di tempat. Jalur yang mereferensikan file di luar direktori plugin (seperti `../shared-utils`) tidak akan berfungsi karena file tersebut tidak disalin.

**Solusi**: Lihat [Plugin caching and file resolution](/id/plugins-reference#plugin-caching-and-file-resolution) untuk solusi termasuk symlink dan restruktur direktori.

Untuk alat debugging tambahan dan masalah umum, lihat [Debugging and development tools](/id/plugins-reference#debugging-and-development-tools).

## Lihat juga

* [Temukan dan pasang plugin yang sudah dibuat](/id/discover-plugins) - Memasang plugin dari marketplace yang ada
* [Plugins](/id/plugins) - Membuat plugin Anda sendiri
* [Plugins reference](/id/plugins-reference) - Spesifikasi teknis lengkap dan skema
* [Plugin settings](/id/settings#plugin-settings) - Opsi konfigurasi plugin
* [strictKnownMarketplaces reference](/id/settings#strictknownmarketplaces) - Pembatasan marketplace yang dikelola
