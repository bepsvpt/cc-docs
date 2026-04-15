> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Temukan dan instal plugin yang sudah dibuat melalui marketplace

> Temukan dan instal plugin dari marketplace untuk memperluas Claude Code dengan perintah, agen, dan kemampuan baru.

Plugin memperluas Claude Code dengan skills, agen, hooks, dan MCP servers. Plugin marketplace adalah katalog yang membantu Anda menemukan dan menginstal ekstensi ini tanpa membuatnya sendiri.

Mencari cara membuat dan mendistribusikan marketplace Anda sendiri? Lihat [Buat dan distribusikan plugin marketplace](/id/plugin-marketplaces).

## Cara kerja marketplace

Marketplace adalah katalog plugin yang telah dibuat dan dibagikan oleh orang lain. Menggunakan marketplace adalah proses dua langkah:

<Steps>
  <Step title="Tambahkan marketplace">
    Ini mendaftarkan katalog dengan Claude Code sehingga Anda dapat menjelajahi apa yang tersedia. Tidak ada plugin yang diinstal lagi.
  </Step>

  <Step title="Instal plugin individual">
    Jelajahi katalog dan instal plugin yang Anda inginkan.
  </Step>
</Steps>

Anggap saja seperti menambahkan app store: menambahkan toko memberi Anda akses untuk menjelajahi koleksinya, tetapi Anda masih memilih aplikasi mana yang akan diunduh secara individual.

## Official Anthropic marketplace

Official Anthropic marketplace (`claude-plugins-official`) secara otomatis tersedia saat Anda memulai Claude Code. Jalankan `/plugin` dan buka tab **Discover** untuk menjelajahi apa yang tersedia, atau lihat katalog di [claude.com/plugins](https://claude.com/plugins).

Untuk menginstal plugin dari official marketplace, gunakan `/plugin install <name>@claude-plugins-official`. Misalnya, untuk menginstal integrasi GitHub:

```shell theme={null}
/plugin install github@claude-plugins-official
```

<Note>
  Official marketplace dikelola oleh Anthropic. Untuk mengirimkan plugin ke official marketplace, gunakan salah satu formulir pengajuan dalam aplikasi:

  * **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  Untuk mendistribusikan plugin secara independen, [buat marketplace Anda sendiri](/id/plugin-marketplaces) dan bagikan dengan pengguna.
</Note>

Official marketplace mencakup beberapa kategori plugin:

### Code intelligence

Plugin code intelligence mengaktifkan alat LSP bawaan Claude Code, memberikan Claude kemampuan untuk melompat ke definisi, menemukan referensi, dan melihat kesalahan tipe segera setelah edit. Plugin ini mengonfigurasi koneksi [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), teknologi yang sama yang mendukung code intelligence VS Code.

Plugin ini memerlukan binary language server untuk diinstal di sistem Anda. Jika Anda sudah memiliki language server yang diinstal, Claude mungkin akan meminta Anda untuk menginstal plugin yang sesuai saat Anda membuka proyek.

| Language   | Plugin              | Binary required              |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

Anda juga dapat [membuat plugin LSP Anda sendiri](/id/plugins-reference#lsp-servers) untuk bahasa lain.

<Note>
  Jika Anda melihat `Executable not found in $PATH` di tab `/plugin` Errors setelah menginstal plugin, instal binary yang diperlukan dari tabel di atas.
</Note>

#### Apa yang Claude dapatkan dari plugin code intelligence

Setelah plugin code intelligence diinstal dan binary language server-nya tersedia, Claude mendapatkan dua kemampuan:

* **Automatic diagnostics**: setelah setiap edit file yang dilakukan Claude, language server menganalisis perubahan dan melaporkan kesalahan dan peringatan secara otomatis. Claude melihat kesalahan tipe, impor yang hilang, dan masalah sintaks tanpa perlu menjalankan compiler atau linter. Jika Claude memperkenalkan kesalahan, itu akan menyadari dan memperbaiki masalah dalam giliran yang sama. Ini tidak memerlukan konfigurasi apa pun selain menginstal plugin. Anda dapat melihat diagnostik secara inline dengan menekan **Ctrl+O** saat indikator "diagnostics found" muncul.
* **Code navigation**: Claude dapat menggunakan language server untuk melompat ke definisi, menemukan referensi, mendapatkan informasi tipe saat hover, membuat daftar simbol, menemukan implementasi, dan melacak hierarki panggilan. Operasi ini memberikan Claude navigasi yang lebih presisi daripada pencarian berbasis grep, meskipun ketersediaan mungkin berbeda menurut bahasa dan lingkungan.

Jika Anda mengalami masalah, lihat [Code intelligence troubleshooting](#code-intelligence-issues).

### External integrations

Plugin ini menggabungkan [MCP servers](/id/mcp) yang sudah dikonfigurasi sebelumnya sehingga Anda dapat menghubungkan Claude ke layanan eksternal tanpa setup manual:

* **Source control**: `github`, `gitlab`
* **Project management**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infrastructure**: `vercel`, `firebase`, `supabase`
* **Communication**: `slack`
* **Monitoring**: `sentry`

### Development workflows

Plugin yang menambahkan perintah dan agen untuk tugas pengembangan umum:

* **commit-commands**: Git commit workflows termasuk commit, push, dan pembuatan PR
* **pr-review-toolkit**: Agen khusus untuk meninjau pull request
* **agent-sdk-dev**: Tools untuk membangun dengan Claude Agent SDK
* **plugin-dev**: Toolkit untuk membuat plugin Anda sendiri

### Output styles

Sesuaikan cara Claude merespons:

* **explanatory-output-style**: Wawasan edukatif tentang pilihan implementasi
* **learning-output-style**: Mode pembelajaran interaktif untuk membangun skill

## Coba: tambahkan demo marketplace

Anthropic juga memelihara [demo plugins marketplace](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) dengan plugin contoh yang menunjukkan apa yang mungkin dengan sistem plugin. Tidak seperti official marketplace, Anda perlu menambahkan ini secara manual.

<Steps>
  <Step title="Tambahkan marketplace">
    Dari dalam Claude Code, jalankan perintah `plugin marketplace add` untuk marketplace `anthropics/claude-code`:

    ```shell theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Ini mengunduh katalog marketplace dan membuat plugin-nya tersedia untuk Anda.
  </Step>

  <Step title="Jelajahi plugin yang tersedia">
    Jalankan `/plugin` untuk membuka plugin manager. Ini membuka antarmuka bertab dengan empat tab yang dapat Anda siklus menggunakan **Tab** (atau **Shift+Tab** untuk mundur):

    * **Discover**: jelajahi plugin yang tersedia dari semua marketplace Anda
    * **Installed**: lihat dan kelola plugin yang diinstal
    * **Marketplaces**: tambah, hapus, atau perbarui marketplace yang ditambahkan
    * **Errors**: lihat kesalahan pemuatan plugin apa pun

    Buka tab **Discover** untuk melihat plugin dari marketplace yang baru saja Anda tambahkan.
  </Step>

  <Step title="Instal plugin">
    Pilih plugin untuk melihat detailnya, kemudian pilih cakupan instalasi:

    * **User scope**: instal untuk diri sendiri di semua proyek
    * **Project scope**: instal untuk semua kolaborator di repositori ini
    * **Local scope**: instal untuk diri sendiri di repositori ini saja

    Misalnya, pilih **commit-commands** (plugin yang menambahkan perintah alur kerja git) dan instal ke cakupan pengguna Anda.

    Anda juga dapat menginstal langsung dari baris perintah:

    ```shell theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    Lihat [Configuration scopes](/id/settings#configuration-scopes) untuk mempelajari lebih lanjut tentang cakupan.
  </Step>

  <Step title="Gunakan plugin baru Anda">
    Setelah menginstal, jalankan `/reload-plugins` untuk mengaktifkan plugin. Perintah plugin diberi namespace oleh nama plugin, jadi **commit-commands** menyediakan perintah seperti `/commit-commands:commit`.

    Coba dengan membuat perubahan pada file dan menjalankan:

    ```shell theme={null}
    /commit-commands:commit
    ```

    Ini menampilkan perubahan Anda, menghasilkan pesan commit, dan membuat commit.

    Setiap plugin bekerja berbeda. Periksa deskripsi plugin di tab **Discover** atau homepage-nya untuk mempelajari perintah dan kemampuan apa yang disediakan.
  </Step>
</Steps>

Sisa panduan ini mencakup semua cara Anda dapat menambahkan marketplace, menginstal plugin, dan mengelola konfigurasi Anda.

## Tambahkan marketplace

Gunakan perintah `/plugin marketplace add` untuk menambahkan marketplace dari sumber yang berbeda.

<Tip>
  **Shortcuts**: Anda dapat menggunakan `/plugin market` sebagai ganti `/plugin marketplace`, dan `rm` sebagai ganti `remove`.
</Tip>

* **GitHub repositories**: format `owner/repo` (misalnya, `anthropics/claude-code`)
* **Git URLs**: URL repositori git apa pun (GitLab, Bitbucket, self-hosted)
* **Local paths**: direktori atau jalur langsung ke file `marketplace.json`
* **Remote URLs**: URL langsung ke file `marketplace.json` yang dihosting

### Tambahkan dari GitHub

Tambahkan repositori GitHub yang berisi file `.claude-plugin/marketplace.json` menggunakan format `owner/repo`—di mana `owner` adalah nama pengguna atau organisasi GitHub dan `repo` adalah nama repositori.

Misalnya, `anthropics/claude-code` merujuk ke repositori `claude-code` yang dimiliki oleh `anthropics`:

```shell theme={null}
/plugin marketplace add anthropics/claude-code
```

### Tambahkan dari host Git lainnya

Tambahkan repositori git apa pun dengan memberikan URL lengkap. Ini bekerja dengan host Git apa pun, termasuk GitLab, Bitbucket, dan server self-hosted:

Menggunakan HTTPS:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Menggunakan SSH:

```shell theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Untuk menambahkan cabang atau tag tertentu, tambahkan `#` diikuti oleh ref:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Tambahkan dari jalur lokal

Tambahkan direktori lokal yang berisi file `.claude-plugin/marketplace.json`:

```shell theme={null}
/plugin marketplace add ./my-marketplace
```

Anda juga dapat menambahkan jalur langsung ke file `marketplace.json`:

```shell theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Tambahkan dari URL jarak jauh

Tambahkan file `marketplace.json` jarak jauh melalui URL:

```shell theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  Marketplace berbasis URL memiliki beberapa keterbatasan dibandingkan dengan marketplace berbasis Git. Jika Anda mengalami kesalahan "path not found" saat menginstal plugin, lihat [Troubleshooting](/id/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Instal plugin

Setelah Anda menambahkan marketplace, Anda dapat menginstal plugin secara langsung (menginstal ke cakupan pengguna secara default):

```shell theme={null}
/plugin install plugin-name@marketplace-name
```

Untuk memilih [cakupan instalasi](/id/settings#configuration-scopes) yang berbeda, gunakan UI interaktif: jalankan `/plugin`, buka tab **Discover**, dan tekan **Enter** pada plugin. Anda akan melihat opsi untuk:

* **User scope** (default): instal untuk diri sendiri di semua proyek
* **Project scope**: instal untuk semua kolaborator di repositori ini (menambahkan ke `.claude/settings.json`)
* **Local scope**: instal untuk diri sendiri di repositori ini saja (tidak dibagikan dengan kolaborator)

Anda juga dapat melihat plugin dengan cakupan **managed**—ini diinstal oleh administrator melalui [managed settings](/id/settings#settings-files) dan tidak dapat dimodifikasi.

Jalankan `/plugin` dan buka tab **Installed** untuk melihat plugin Anda dikelompokkan menurut cakupan.

<Warning>
  Pastikan Anda mempercayai plugin sebelum menginstalnya. Anthropic tidak mengontrol MCP servers, file, atau perangkat lunak lain apa yang disertakan dalam plugin dan tidak dapat memverifikasi bahwa mereka bekerja seperti yang dimaksudkan. Periksa homepage setiap plugin untuk informasi lebih lanjut.
</Warning>

## Kelola plugin yang diinstal

Jalankan `/plugin` dan buka tab **Installed** untuk melihat, mengaktifkan, menonaktifkan, atau menghapus plugin Anda. Ketik untuk memfilter daftar berdasarkan nama atau deskripsi plugin.

Anda juga dapat mengelola plugin dengan perintah langsung.

Nonaktifkan plugin tanpa menghapusnya:

```shell theme={null}
/plugin disable plugin-name@marketplace-name
```

Aktifkan kembali plugin yang dinonaktifkan:

```shell theme={null}
/plugin enable plugin-name@marketplace-name
```

Hapus plugin sepenuhnya:

```shell theme={null}
/plugin uninstall plugin-name@marketplace-name
```

Opsi `--scope` memungkinkan Anda menargetkan cakupan tertentu dengan perintah CLI:

```shell theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Terapkan perubahan plugin tanpa restart

Saat Anda menginstal, mengaktifkan, atau menonaktifkan plugin selama sesi, jalankan `/reload-plugins` untuk mengambil semua perubahan tanpa restart:

```shell theme={null}
/reload-plugins
```

Claude Code memuat ulang semua plugin aktif dan menampilkan hitungan untuk plugin, skills, agen, hooks, server MCP plugin, dan server LSP plugin.

## Kelola marketplace

Anda dapat mengelola marketplace melalui antarmuka `/plugin` interaktif atau dengan perintah CLI.

### Gunakan antarmuka interaktif

Jalankan `/plugin` dan buka tab **Marketplaces** untuk:

* Lihat semua marketplace yang ditambahkan dengan sumber dan statusnya
* Tambahkan marketplace baru
* Perbarui daftar marketplace untuk mengambil plugin terbaru
* Hapus marketplace yang tidak lagi Anda butuhkan

### Gunakan perintah CLI

Anda juga dapat mengelola marketplace dengan perintah langsung.

Daftar semua marketplace yang dikonfigurasi:

```shell theme={null}
/plugin marketplace list
```

Segarkan daftar plugin dari marketplace:

```shell theme={null}
/plugin marketplace update marketplace-name
```

Hapus marketplace:

```shell theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  Menghapus marketplace akan menghapus instalasi plugin apa pun yang Anda instal darinya.
</Warning>

### Konfigurasi auto-updates

Claude Code dapat secara otomatis memperbarui marketplace dan plugin yang diinstal saat startup. Saat auto-update diaktifkan untuk marketplace, Claude Code menyegarkan data marketplace dan memperbarui plugin yang diinstal ke versi terbaru mereka. Jika ada plugin yang diperbarui, Anda akan melihat notifikasi yang meminta Anda untuk menjalankan `/reload-plugins`.

Alihkan auto-update untuk marketplace individual melalui UI:

1. Jalankan `/plugin` untuk membuka plugin manager
2. Pilih **Marketplaces**
3. Pilih marketplace dari daftar
4. Pilih **Enable auto-update** atau **Disable auto-update**

Official Anthropic marketplace memiliki auto-update diaktifkan secara default. Marketplace pihak ketiga dan pengembangan lokal memiliki auto-update dinonaktifkan secara default.

Untuk menonaktifkan semua pembaruan otomatis sepenuhnya untuk Claude Code dan semua plugin, atur variabel lingkungan `DISABLE_AUTOUPDATER`. Lihat [Auto updates](/id/setup#auto-updates) untuk detail.

Untuk menjaga plugin auto-updates tetap diaktifkan sambil menonaktifkan Claude Code auto-updates, atur `FORCE_AUTOUPDATE_PLUGINS=1` bersama dengan `DISABLE_AUTOUPDATER`:

```bash theme={null}
export DISABLE_AUTOUPDATER=1
export FORCE_AUTOUPDATE_PLUGINS=1
```

Ini berguna saat Anda ingin mengelola pembaruan Claude Code secara manual tetapi masih menerima pembaruan plugin otomatis.

## Konfigurasi team marketplace

Admin tim dapat menyiapkan instalasi marketplace otomatis untuk proyek dengan menambahkan konfigurasi marketplace ke `.claude/settings.json`. Saat anggota tim mempercayai folder repositori, Claude Code meminta mereka untuk menginstal marketplace dan plugin ini.

Tambahkan `extraKnownMarketplaces` ke `.claude/settings.json` proyek Anda:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Untuk opsi konfigurasi lengkap termasuk `extraKnownMarketplaces` dan `enabledPlugins`, lihat [Plugin settings](/id/settings#plugin-settings).

## Security

Plugin dan marketplace adalah komponen yang sangat dipercaya yang dapat menjalankan kode arbitrer di mesin Anda dengan hak istimewa pengguna Anda. Hanya instal plugin dan tambahkan marketplace dari sumber yang Anda percayai. Organisasi dapat membatasi marketplace mana yang diizinkan pengguna untuk ditambahkan menggunakan [managed marketplace restrictions](/id/plugin-marketplaces#managed-marketplace-restrictions).

## Troubleshooting

### /plugin command not recognized

Jika Anda melihat "unknown command" atau perintah `/plugin` tidak muncul:

1. **Periksa versi Anda**: Jalankan `claude --version` untuk melihat apa yang diinstal.
2. **Perbarui Claude Code**:
   * **Homebrew**: `brew upgrade claude-code`
   * **npm**: `npm update -g @anthropic-ai/claude-code`
   * **Native installer**: Jalankan kembali perintah install dari [Setup](/id/setup)
3. **Restart Claude Code**: Setelah memperbarui, restart terminal Anda dan jalankan `claude` lagi.

### Common issues

* **Marketplace not loading**: Verifikasi URL dapat diakses dan bahwa `.claude-plugin/marketplace.json` ada di jalur
* **Plugin installation failures**: Periksa bahwa URL sumber plugin dapat diakses dan repositori bersifat publik (atau Anda memiliki akses)
* **Files not found after installation**: Plugin disalin ke cache, jadi jalur yang mereferensikan file di luar direktori plugin tidak akan berfungsi
* **Plugin skills not appearing**: Hapus cache dengan `rm -rf ~/.claude/plugins/cache`, restart Claude Code, dan instal ulang plugin.

Untuk troubleshooting terperinci dengan solusi, lihat [Troubleshooting](/id/plugin-marketplaces#troubleshooting) dalam panduan marketplace. Untuk tools debugging, lihat [Debugging and development tools](/id/plugins-reference#debugging-and-development-tools).

### Code intelligence issues

* **Language server not starting**: verifikasi binary diinstal dan tersedia di `$PATH` Anda. Periksa tab `/plugin` Errors untuk detail.
* **High memory usage**: language server seperti `rust-analyzer` dan `pyright` dapat mengonsumsi memori signifikan pada proyek besar. Jika Anda mengalami masalah memori, nonaktifkan plugin dengan `/plugin disable <plugin-name>` dan andalkan tools pencarian bawaan Claude sebagai gantinya.
* **False positive diagnostics in monorepos**: language server mungkin melaporkan kesalahan impor yang tidak terselesaikan untuk paket internal jika workspace tidak dikonfigurasi dengan benar. Ini tidak mempengaruhi kemampuan Claude untuk mengedit kode.

## Next steps

* **Build your own plugins**: Lihat [Plugins](/id/plugins) untuk membuat skills, agen, dan hooks
* **Create a marketplace**: Lihat [Create a plugin marketplace](/id/plugin-marketplaces) untuk mendistribusikan plugin ke tim atau komunitas Anda
* **Technical reference**: Lihat [Plugins reference](/id/plugins-reference) untuk spesifikasi lengkap
