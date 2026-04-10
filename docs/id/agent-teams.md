> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Koordinasikan tim Claude Code sessions

> Koordinasikan beberapa instance Claude Code yang bekerja bersama sebagai tim, dengan tugas bersama, pesan antar-agent, dan manajemen terpusat.

<Warning>
  Tim agent bersifat eksperimental dan dinonaktifkan secara default. Aktifkan dengan menambahkan `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` ke [settings.json](/id/settings) atau environment Anda. Tim agent memiliki [keterbatasan yang diketahui](#limitations) seputar resumption session, koordinasi tugas, dan perilaku shutdown.
</Warning>

Tim agent memungkinkan Anda mengoordinasikan beberapa instance Claude Code yang bekerja bersama. Satu session bertindak sebagai team lead, mengoordinasikan pekerjaan, menugaskan tugas, dan mensintesis hasil. Rekan tim bekerja secara independen, masing-masing dalam context window-nya sendiri, dan berkomunikasi langsung satu sama lain.

Tidak seperti [subagents](/id/sub-agents), yang berjalan dalam satu session dan hanya dapat melaporkan kembali ke agent utama, Anda juga dapat berinteraksi dengan rekan tim individual secara langsung tanpa melalui lead.

<Note>
  Tim agent memerlukan Claude Code v2.1.32 atau lebih baru. Periksa versi Anda dengan `claude --version`.
</Note>

Halaman ini mencakup:

* [Kapan menggunakan tim agent](#when-to-use-agent-teams), termasuk use case terbaik dan bagaimana perbandingannya dengan subagents
* [Memulai tim](#start-your-first-agent-team)
* [Mengendalikan rekan tim](#control-your-agent-team), termasuk mode tampilan, penugasan tugas, dan delegasi
* [Best practices untuk pekerjaan paralel](#best-practices)

## Kapan menggunakan tim agent

Tim agent paling efektif untuk tugas di mana eksplorasi paralel menambah nilai nyata. Lihat [contoh use case](#use-case-examples) untuk skenario lengkap. Use case terkuat adalah:

* **Penelitian dan review**: beberapa rekan tim dapat menyelidiki aspek berbeda dari masalah secara bersamaan, kemudian berbagi dan menantang temuan satu sama lain
* **Modul atau fitur baru**: rekan tim dapat masing-masing memiliki bagian terpisah tanpa saling mengganggu
* **Debugging dengan hipotesis bersaing**: rekan tim menguji teori berbeda secara paralel dan berkumpul pada jawaban lebih cepat
* **Koordinasi lintas-layer**: perubahan yang mencakup frontend, backend, dan test, masing-masing dimiliki oleh rekan tim berbeda

Tim agent menambah overhead koordinasi dan menggunakan token secara signifikan lebih banyak daripada satu session. Mereka bekerja paling baik ketika rekan tim dapat beroperasi secara independen. Untuk tugas sekuensial, edit file yang sama, atau pekerjaan dengan banyak dependensi, satu session atau [subagents](/id/sub-agents) lebih efektif.

### Bandingkan dengan subagents

Baik tim agent maupun [subagents](/id/sub-agents) memungkinkan Anda memparalelkan pekerjaan, tetapi mereka beroperasi berbeda. Pilih berdasarkan apakah pekerja Anda perlu berkomunikasi satu sama lain:

<Frame caption="Subagents hanya melaporkan hasil kembali ke agent utama dan tidak pernah berbicara satu sama lain. Dalam tim agent, rekan tim berbagi daftar tugas, mengklaim pekerjaan, dan berkomunikasi langsung satu sama lain.">
  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-light.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=2f8db9b4f3705dd3ab931fbe2d96e42a" className="dark:hidden" alt="Diagram membandingkan arsitektur subagent dan tim agent. Subagents dihasilkan oleh agent utama, melakukan pekerjaan, dan melaporkan hasil kembali. Tim agent berkoordinasi melalui daftar tugas bersama, dengan rekan tim berkomunikasi langsung satu sama lain." width="4245" height="1615" data-path="images/subagents-vs-agent-teams-light.png" />

  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-dark.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=d573a037540f2ada6a9ae7d8285b46fd" className="hidden dark:block" alt="Diagram membandingkan arsitektur subagent dan tim agent. Subagents dihasilkan oleh agent utama, melakukan pekerjaan, dan melaporkan hasil kembali. Tim agent berkoordinasi melalui daftar tugas bersama, dengan rekan tim berkomunikasi langsung satu sama lain." width="4245" height="1615" data-path="images/subagents-vs-agent-teams-dark.png" />
</Frame>

|                   | Subagents                                              | Tim agent                                                      |
| :---------------- | :----------------------------------------------------- | :------------------------------------------------------------- |
| **Context**       | Context window sendiri; hasil kembali ke pemanggil     | Context window sendiri; sepenuhnya independen                  |
| **Komunikasi**    | Melaporkan hasil kembali ke agent utama saja           | Rekan tim saling mengirim pesan secara langsung                |
| **Koordinasi**    | Agent utama mengelola semua pekerjaan                  | Daftar tugas bersama dengan self-coordination                  |
| **Terbaik untuk** | Tugas terfokus di mana hanya hasil yang penting        | Pekerjaan kompleks yang memerlukan diskusi dan kolaborasi      |
| **Biaya token**   | Lebih rendah: hasil diringkas kembali ke context utama | Lebih tinggi: setiap rekan tim adalah instance Claude terpisah |

Gunakan subagents ketika Anda membutuhkan pekerja cepat dan terfokus yang melaporkan kembali. Gunakan tim agent ketika rekan tim perlu berbagi temuan, menantang satu sama lain, dan berkoordinasi sendiri.

## Aktifkan tim agent

Tim agent dinonaktifkan secara default. Aktifkan dengan mengatur variabel environment `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` ke `1`, baik di environment shell Anda atau melalui [settings.json](/id/settings):

```json settings.json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Mulai tim agent pertama Anda

Setelah mengaktifkan tim agent, beri tahu Claude untuk membuat tim agent dan jelaskan tugas dan struktur tim yang Anda inginkan dalam bahasa alami. Claude membuat tim, menelurkan rekan tim, dan mengoordinasikan pekerjaan berdasarkan prompt Anda.

Contoh ini bekerja dengan baik karena tiga peran independen dan dapat mengeksplorasi masalah tanpa menunggu satu sama lain:

```text  theme={null}
Saya merancang alat CLI yang membantu developer melacak komentar TODO di seluruh
codebase mereka. Buat tim agent untuk mengeksplorasi ini dari sudut berbeda: satu
rekan tim pada UX, satu pada arsitektur teknis, satu memainkan devil's advocate.
```

Dari sana, Claude membuat tim dengan [daftar tugas bersama](/id/interactive-mode#task-list), menelurkan rekan tim untuk setiap perspektif, membuat mereka mengeksplorasi masalah, mensintesis temuan, dan mencoba [membersihkan tim](#clean-up-the-team) ketika selesai.

Terminal lead mencantumkan semua rekan tim dan apa yang mereka kerjakan. Gunakan Shift+Down untuk bersiklus melalui rekan tim dan kirim pesan kepada mereka secara langsung. Setelah rekan tim terakhir, Shift+Down membungkus kembali ke lead.

Jika Anda ingin setiap rekan tim di split pane-nya sendiri, lihat [Pilih mode tampilan](#choose-a-display-mode).

## Kontrol tim agent Anda

Beri tahu lead apa yang Anda inginkan dalam bahasa alami. Ini menangani koordinasi tim, penugasan tugas, dan delegasi berdasarkan instruksi Anda.

### Pilih mode tampilan

Tim agent mendukung dua mode tampilan:

* **In-process**: semua rekan tim berjalan di dalam terminal utama Anda. Gunakan Shift+Down untuk bersiklus melalui rekan tim dan ketik untuk mengirim pesan kepada mereka secara langsung. Bekerja di terminal apa pun, tidak ada setup tambahan yang diperlukan.
* **Split panes**: setiap rekan tim mendapat pane-nya sendiri. Anda dapat melihat output semua orang sekaligus dan klik ke dalam pane untuk berinteraksi secara langsung. Memerlukan tmux, atau iTerm2.

<Note>
  `tmux` memiliki keterbatasan yang diketahui pada sistem operasi tertentu dan secara tradisional bekerja paling baik di macOS. Menggunakan `tmux -CC` di iTerm2 adalah entrypoint yang disarankan ke `tmux`.
</Note>

Default adalah `"auto"`, yang menggunakan split panes jika Anda sudah berjalan di dalam session tmux, dan in-process sebaliknya. Pengaturan `"tmux"` mengaktifkan mode split-pane dan auto-detects apakah akan menggunakan tmux atau iTerm2 berdasarkan terminal Anda. Untuk mengganti, atur `teammateMode` di [global config](/id/settings#global-config-settings) Anda di `~/.claude.json`:

```json  theme={null}
{
  "teammateMode": "in-process"
}
```

Untuk memaksa mode in-process untuk satu session, teruskan sebagai flag:

```bash  theme={null}
claude --teammate-mode in-process
```

Mode split-pane memerlukan baik [tmux](https://github.com/tmux/tmux/wiki) atau iTerm2 dengan [`it2` CLI](https://github.com/mkusaka/it2). Untuk menginstal secara manual:

* **tmux**: instal melalui package manager sistem Anda. Lihat [tmux wiki](https://github.com/tmux/tmux/wiki/Installing) untuk instruksi spesifik platform.
* **iTerm2**: instal [`it2` CLI](https://github.com/mkusaka/it2), kemudian aktifkan Python API di **iTerm2 → Settings → General → Magic → Enable Python API**.

### Tentukan rekan tim dan model

Claude memutuskan jumlah rekan tim untuk dihasilkan berdasarkan tugas Anda, atau Anda dapat menentukan dengan tepat apa yang Anda inginkan:

```text  theme={null}
Buat tim dengan 4 rekan tim untuk refactor modul-modul ini secara paralel.
Gunakan Sonnet untuk setiap rekan tim.
```

### Perlukan persetujuan rencana untuk rekan tim

Untuk tugas kompleks atau berisiko, Anda dapat memerlukan rekan tim untuk merencanakan sebelum mengimplementasikan. Rekan tim bekerja dalam mode rencana read-only sampai lead menyetujui pendekatan mereka:

```text  theme={null}
Hasilkan rekan tim architect untuk refactor modul autentikasi.
Perlukan persetujuan rencana sebelum mereka membuat perubahan apa pun.
```

Ketika rekan tim selesai merencanakan, mereka mengirim permintaan persetujuan rencana ke lead. Lead meninjau rencana dan baik menyetujuinya atau menolaknya dengan umpan balik. Jika ditolak, rekan tim tetap dalam mode rencana, merevisi berdasarkan umpan balik, dan mengirimkan kembali. Setelah disetujui, rekan tim keluar dari mode rencana dan mulai implementasi.

Lead membuat keputusan persetujuan secara otonom. Untuk mempengaruhi penilaian lead, berikan kriteria dalam prompt Anda, seperti "hanya setujui rencana yang mencakup test coverage" atau "tolak rencana yang memodifikasi skema database."

### Berbicara dengan rekan tim secara langsung

Setiap rekan tim adalah session Claude Code penuh dan independen. Anda dapat mengirim pesan ke rekan tim mana pun secara langsung untuk memberikan instruksi tambahan, mengajukan pertanyaan lanjutan, atau mengalihkan pendekatan mereka.

* **Mode in-process**: gunakan Shift+Down untuk bersiklus melalui rekan tim, kemudian ketik untuk mengirim pesan kepada mereka. Tekan Enter untuk melihat session rekan tim, kemudian Escape untuk mengganggu giliran mereka saat ini. Tekan Ctrl+T untuk toggle daftar tugas.
* **Mode split-pane**: klik ke dalam pane rekan tim untuk berinteraksi dengan session mereka secara langsung. Setiap rekan tim memiliki tampilan penuh dari terminal mereka sendiri.

### Tetapkan dan klaim tugas

Daftar tugas bersama mengoordinasikan pekerjaan di seluruh tim. Lead membuat tugas dan rekan tim mengerjakannya. Tugas memiliki tiga status: pending, in progress, dan completed. Tugas juga dapat bergantung pada tugas lain: tugas pending dengan dependensi yang tidak terselesaikan tidak dapat diklaim sampai dependensi tersebut selesai.

Lead dapat menugaskan tugas secara eksplisit, atau rekan tim dapat self-claim:

* **Lead menugaskan**: beri tahu lead tugas mana yang diberikan kepada rekan tim mana
* **Self-claim**: setelah menyelesaikan tugas, rekan tim mengambil tugas unassigned, unblocked berikutnya sendiri

Klaim tugas menggunakan file locking untuk mencegah race conditions ketika beberapa rekan tim mencoba mengklaim tugas yang sama secara bersamaan.

### Matikan rekan tim

Untuk mengakhiri session rekan tim dengan baik:

```text  theme={null}
Minta rekan tim peneliti untuk shutdown
```

Lead mengirim permintaan shutdown. Rekan tim dapat menyetujui, keluar dengan baik, atau menolak dengan penjelasan.

### Bersihkan tim

Ketika Anda selesai, minta lead untuk membersihkan:

```text  theme={null}
Bersihkan tim
```

Ini menghapus sumber daya tim bersama. Ketika lead menjalankan cleanup, ia memeriksa rekan tim aktif dan gagal jika ada yang masih berjalan, jadi matikan mereka terlebih dahulu.

<Warning>
  Selalu gunakan lead untuk membersihkan. Rekan tim tidak boleh menjalankan cleanup karena konteks tim mereka mungkin tidak terselesaikan dengan benar, berpotensi meninggalkan sumber daya dalam keadaan tidak konsisten.
</Warning>

### Terapkan quality gates dengan hooks

Gunakan [hooks](/id/hooks) untuk menerapkan aturan ketika rekan tim menyelesaikan pekerjaan atau tugas dibuat atau diselesaikan:

* [`TeammateIdle`](/id/hooks#teammateidle): berjalan ketika rekan tim akan idle. Keluar dengan kode 2 untuk mengirim umpan balik dan membuat rekan tim tetap bekerja.
* [`TaskCreated`](/id/hooks#taskcreated): berjalan ketika tugas sedang dibuat. Keluar dengan kode 2 untuk mencegah pembuatan dan mengirim umpan balik.
* [`TaskCompleted`](/id/hooks#taskcompleted): berjalan ketika tugas ditandai selesai. Keluar dengan kode 2 untuk mencegah penyelesaian dan mengirim umpan balik.

## Bagaimana tim agent bekerja

Bagian ini mencakup arsitektur dan mekanik di balik tim agent. Jika Anda ingin mulai menggunakannya, lihat [Kontrol tim agent Anda](#control-your-agent-team) di atas.

### Bagaimana Claude memulai tim agent

Ada dua cara tim agent dimulai:

* **Anda meminta tim**: berikan Claude tugas yang menguntungkan dari pekerjaan paralel dan secara eksplisit minta tim agent. Claude membuat satu berdasarkan instruksi Anda.
* **Claude mengusulkan tim**: jika Claude menentukan tugas Anda akan menguntungkan dari pekerjaan paralel, mungkin menyarankan membuat tim. Anda mengonfirmasi sebelum melanjutkan.

Dalam kedua kasus, Anda tetap mengendalikan. Claude tidak akan membuat tim tanpa persetujuan Anda.

### Arsitektur

Tim agent terdiri dari:

| Komponen         | Peran                                                                                            |
| :--------------- | :----------------------------------------------------------------------------------------------- |
| **Team lead**    | Session Claude Code utama yang membuat tim, menelurkan rekan tim, dan mengoordinasikan pekerjaan |
| **Rekan tim**    | Instance Claude Code terpisah yang masing-masing bekerja pada tugas yang ditugaskan              |
| **Daftar tugas** | Daftar item pekerjaan bersama yang diklaim dan diselesaikan rekan tim                            |
| **Mailbox**      | Sistem pesan untuk komunikasi antar agent                                                        |

Lihat [Pilih mode tampilan](#choose-a-display-mode) untuk opsi konfigurasi tampilan. Pesan rekan tim tiba di lead secara otomatis.

Sistem mengelola dependensi tugas secara otomatis. Ketika rekan tim menyelesaikan tugas yang tugas lain bergantung padanya, tugas yang diblokir membuka tanpa intervensi manual.

Tim dan tugas disimpan secara lokal:

* **Konfigurasi tim**: `~/.claude/teams/{team-name}/config.json`
* **Daftar tugas**: `~/.claude/tasks/{team-name}/`

Claude Code menghasilkan keduanya secara otomatis ketika Anda membuat tim dan memperbarui mereka saat rekan tim bergabung, idle, atau pergi. Konfigurasi tim menyimpan status runtime seperti session IDs dan tmux pane IDs, jadi jangan mengeditnya dengan tangan atau pre-author: perubahan Anda ditimpa pada update status berikutnya.

Untuk mendefinisikan peran rekan tim yang dapat digunakan kembali, gunakan [subagent definitions](#use-subagent-definitions-for-teammates) sebagai gantinya.

Konfigurasi tim berisi array `members` dengan nama setiap rekan tim, agent ID, dan tipe agent. Rekan tim dapat membaca file ini untuk menemukan anggota tim lainnya.

Tidak ada padanan tingkat proyek dari konfigurasi tim. File seperti `.claude/teams/teams.json` di direktori proyek Anda tidak dikenali sebagai konfigurasi; Claude memperlakukannya sebagai file biasa.

### Gunakan subagent definitions untuk rekan tim

Ketika menelurkan rekan tim, Anda dapat mereferensikan tipe [subagent](/id/sub-agents) dari [subagent scope](/id/sub-agents#choose-the-subagent-scope) apa pun: proyek, pengguna, plugin, atau CLI-defined. Rekan tim mewarisi system prompt, tools, dan model subagent itu. Ini memungkinkan Anda mendefinisikan peran sekali, seperti security-reviewer atau test-runner, dan menggunakannya kembali baik sebagai subagent yang didelegasikan maupun sebagai rekan tim agent team.

Untuk menggunakan subagent definition, sebutkan berdasarkan nama ketika meminta Claude untuk menelurkan rekan tim:

```text  theme={null}
Hasilkan rekan tim menggunakan tipe agent security-reviewer untuk mengaudit modul auth.
```

### Izin

Rekan tim dimulai dengan pengaturan izin lead. Jika lead berjalan dengan `--dangerously-skip-permissions`, semua rekan tim juga demikian. Setelah dihasilkan, Anda dapat mengubah mode rekan tim individual, tetapi Anda tidak dapat mengatur mode per-rekan tim pada waktu spawn.

### Context dan komunikasi

Setiap rekan tim memiliki context window-nya sendiri. Ketika dihasilkan, rekan tim memuat konteks proyek yang sama seperti session reguler: CLAUDE.md, MCP servers, dan skills. Mereka juga menerima spawn prompt dari lead. Riwayat percakapan lead tidak terbawa.

**Bagaimana rekan tim berbagi informasi:**

* **Pengiriman pesan otomatis**: ketika rekan tim mengirim pesan, mereka dikirimkan secara otomatis ke penerima. Lead tidak perlu polling untuk update.
* **Notifikasi idle**: ketika rekan tim selesai dan berhenti, mereka secara otomatis memberi tahu lead.
* **Daftar tugas bersama**: semua agent dapat melihat status tugas dan mengklaim pekerjaan yang tersedia.

**Pesan rekan tim:**

* **message**: kirim pesan ke satu rekan tim spesifik
* **broadcast**: kirim ke semua rekan tim secara bersamaan. Gunakan dengan hemat, karena biaya skala dengan ukuran tim.

### Penggunaan token

Tim agent menggunakan token secara signifikan lebih banyak daripada satu session. Setiap rekan tim memiliki context window-nya sendiri, dan penggunaan token skala dengan jumlah rekan tim aktif. Untuk penelitian, review, dan pekerjaan fitur baru, token tambahan biasanya berharga. Untuk tugas rutin, satu session lebih cost-effective. Lihat [biaya token tim agent](/id/costs#agent-team-token-costs) untuk panduan penggunaan.

## Contoh use case

Contoh-contoh ini menunjukkan bagaimana tim agent menangani tugas di mana eksplorasi paralel menambah nilai.

### Jalankan code review paralel

Seorang reviewer tunggal cenderung tertarik pada satu jenis masalah pada satu waktu. Membagi kriteria review menjadi domain independen berarti keamanan, kinerja, dan test coverage semuanya mendapat perhatian menyeluruh secara bersamaan. Prompt menugaskan setiap rekan tim lensa yang berbeda sehingga mereka tidak tumpang tindih:

```text  theme={null}
Buat tim agent untuk review PR #142. Hasilkan tiga reviewer:
- Satu fokus pada implikasi keamanan
- Satu memeriksa dampak kinerja
- Satu memvalidasi test coverage
Buat mereka masing-masing review dan laporkan temuan.
```

Setiap reviewer bekerja dari PR yang sama tetapi menerapkan filter berbeda. Lead mensintesis temuan di ketiga setelah mereka selesai.

### Investigasi dengan hipotesis bersaing

Ketika akar penyebab tidak jelas, satu agent cenderung menemukan satu penjelasan yang masuk akal dan berhenti mencari. Prompt melawan ini dengan membuat rekan tim secara eksplisit adversarial: pekerjaan setiap orang bukan hanya menyelidiki teori mereka sendiri tetapi menantang yang lain.

```text  theme={null}
Pengguna melaporkan aplikasi keluar setelah satu pesan alih-alih tetap terhubung.
Hasilkan 5 rekan tim agent untuk menyelidiki hipotesis berbeda. Buat mereka berbicara
satu sama lain untuk mencoba membantah teori satu sama lain, seperti debat
ilmiah. Perbarui dokumen temuan dengan konsensus apa pun yang muncul.
```

Struktur debat adalah mekanisme kunci di sini. Investigasi sekuensial menderita dari anchoring: setelah satu teori dieksplorasi, investigasi berikutnya bias terhadapnya.

Dengan beberapa investigator independen secara aktif mencoba membantah satu sama lain, teori yang bertahan jauh lebih mungkin menjadi akar penyebab sebenarnya.

## Best practices

### Berikan rekan tim konteks yang cukup

Rekan tim memuat konteks proyek secara otomatis, termasuk CLAUDE.md, MCP servers, dan skills, tetapi mereka tidak mewarisi riwayat percakapan lead. Lihat [Context dan komunikasi](#context-and-communication) untuk detail. Sertakan detail spesifik tugas dalam spawn prompt:

```text  theme={null}
Hasilkan rekan tim security reviewer dengan prompt: "Review modul autentikasi
di src/auth/ untuk kerentanan keamanan. Fokus pada penanganan token, manajemen
session, dan validasi input. Aplikasi menggunakan token JWT yang disimpan di
httpOnly cookies. Laporkan masalah apa pun dengan rating severity."
```

### Pilih ukuran tim yang sesuai

Tidak ada batas keras pada jumlah rekan tim, tetapi batasan praktis berlaku:

* **Biaya token skala linear**: setiap rekan tim memiliki context window-nya sendiri dan mengkonsumsi token secara independen. Lihat [biaya token tim agent](/id/costs#agent-team-token-costs) untuk detail.
* **Overhead koordinasi meningkat**: lebih banyak rekan tim berarti lebih banyak komunikasi, koordinasi tugas, dan potensi konflik
* **Diminishing returns**: di luar titik tertentu, rekan tim tambahan tidak mempercepat pekerjaan secara proporsional

Mulai dengan 3-5 rekan tim untuk sebagian besar workflow. Ini menyeimbangkan pekerjaan paralel dengan koordinasi yang dapat dikelola. Contoh-contoh dalam panduan ini menggunakan 3-5 rekan tim karena rentang itu bekerja dengan baik di berbagai jenis tugas.

Memiliki 5-6 [tasks](/id/agent-teams#architecture) per rekan tim membuat semua orang produktif tanpa context switching yang berlebihan. Jika Anda memiliki 15 tugas independen, 3 rekan tim adalah titik awal yang baik.

Skala naik hanya ketika pekerjaan benar-benar menguntungkan dari rekan tim bekerja secara bersamaan. Tiga rekan tim terfokus sering mengungguli lima yang tersebar.

### Ukuran tugas dengan tepat

* **Terlalu kecil**: overhead koordinasi melebihi manfaat
* **Terlalu besar**: rekan tim bekerja terlalu lama tanpa check-in, meningkatkan risiko usaha yang terbuang
* **Tepat**: unit self-contained yang menghasilkan deliverable yang jelas, seperti fungsi, file test, atau review

<Tip>
  Lead memecah pekerjaan menjadi tugas dan menugaskan mereka ke rekan tim secara otomatis. Jika tidak membuat cukup tugas, minta untuk membagi pekerjaan menjadi potongan yang lebih kecil. Memiliki 5-6 tugas per rekan tim membuat semua orang produktif dan memungkinkan lead untuk menugaskan kembali pekerjaan jika seseorang terjebak.
</Tip>

### Tunggu rekan tim selesai

Kadang-kadang lead mulai mengimplementasikan tugas sendiri alih-alih menunggu rekan tim. Jika Anda memperhatikan ini:

```text  theme={null}
Tunggu rekan tim Anda menyelesaikan tugas mereka sebelum melanjutkan
```

### Mulai dengan penelitian dan review

Jika Anda baru mengenal tim agent, mulai dengan tugas yang memiliki batas yang jelas dan tidak memerlukan penulisan kode: review PR, penelitian library, atau investigasi bug. Tugas-tugas ini menunjukkan nilai eksplorasi paralel tanpa tantangan koordinasi yang datang dengan implementasi paralel.

### Hindari konflik file

Dua rekan tim mengedit file yang sama menyebabkan overwrites. Pecah pekerjaan sehingga setiap rekan tim memiliki set file berbeda.

### Monitor dan kemudi

Periksa kemajuan rekan tim, alihkan pendekatan yang tidak berfungsi, dan sintesis temuan saat tiba. Membiarkan tim berjalan tanpa diawasi terlalu lama meningkatkan risiko usaha yang terbuang.

## Troubleshooting

### Rekan tim tidak muncul

Jika rekan tim tidak muncul setelah Anda meminta Claude untuk membuat tim:

* Dalam mode in-process, rekan tim mungkin sudah berjalan tetapi tidak terlihat. Tekan Shift+Down untuk bersiklus melalui rekan tim aktif.
* Periksa bahwa tugas yang Anda berikan Claude cukup kompleks untuk menjamin tim. Claude memutuskan apakah akan menelurkan rekan tim berdasarkan tugas.
* Jika Anda secara eksplisit meminta split panes, pastikan tmux diinstal dan tersedia di PATH Anda:
  ```bash  theme={null}
  which tmux
  ```
* Untuk iTerm2, verifikasi `it2` CLI diinstal dan Python API diaktifkan di preferensi iTerm2.

### Terlalu banyak permission prompts

Permintaan izin rekan tim naik ke lead, yang dapat menciptakan gesekan. Pre-approve operasi umum di [pengaturan izin](/id/permissions) Anda sebelum menelurkan rekan tim untuk mengurangi gangguan.

### Rekan tim berhenti pada error

Rekan tim dapat berhenti setelah mengalami error alih-alih pulih. Periksa output mereka menggunakan Shift+Down dalam mode in-process atau dengan mengklik pane dalam mode split, kemudian baik:

* Berikan instruksi tambahan kepada mereka secara langsung
* Hasilkan rekan tim pengganti untuk melanjutkan pekerjaan

### Lead shutdown sebelum pekerjaan selesai

Lead dapat memutuskan tim selesai sebelum semua tugas benar-benar selesai. Jika ini terjadi, beri tahu untuk terus. Anda juga dapat memberi tahu lead untuk menunggu rekan tim selesai sebelum melanjutkan jika mulai melakukan pekerjaan alih-alih mendelegasikan.

### Orphaned tmux sessions

Jika session tmux bertahan setelah tim berakhir, mungkin tidak sepenuhnya dibersihkan. Daftar session dan bunuh yang dibuat oleh tim:

```bash  theme={null}
tmux ls
tmux kill-session -t <session-name>
```

## Keterbatasan

Tim agent bersifat eksperimental. Keterbatasan saat ini untuk diketahui:

* **Tidak ada session resumption dengan rekan tim in-process**: `/resume` dan `/rewind` tidak mengembalikan rekan tim in-process. Setelah melanjutkan session, lead dapat mencoba mengirim pesan ke rekan tim yang tidak lagi ada. Jika ini terjadi, beri tahu lead untuk menelurkan rekan tim baru.
* **Status tugas dapat tertinggal**: rekan tim kadang-kadang gagal menandai tugas sebagai selesai, yang memblokir tugas dependen. Jika tugas tampak terjebak, periksa apakah pekerjaan benar-benar selesai dan perbarui status tugas secara manual atau beri tahu lead untuk mendorong rekan tim.
* **Shutdown dapat lambat**: rekan tim menyelesaikan permintaan atau tool call saat ini sebelum shutdown, yang dapat memakan waktu.
* **Satu tim per session**: lead hanya dapat mengelola satu tim pada satu waktu. Bersihkan tim saat ini sebelum memulai yang baru.
* **Tidak ada tim bersarang**: rekan tim tidak dapat menelurkan tim atau rekan tim mereka sendiri. Hanya lead yang dapat mengelola tim.
* **Lead tetap**: session yang membuat tim adalah lead seumur hidupnya. Anda tidak dapat mempromosikan rekan tim ke lead atau mentransfer kepemimpinan.
* **Izin ditetapkan pada spawn**: semua rekan tim dimulai dengan mode izin lead. Anda dapat mengubah mode rekan tim individual setelah spawn, tetapi Anda tidak dapat mengatur mode per-rekan tim pada waktu spawn.
* **Split panes memerlukan tmux atau iTerm2**: mode in-process default bekerja di terminal apa pun. Mode split-pane tidak didukung di integrated terminal VS Code, Windows Terminal, atau Ghostty.

<Tip>
  **`CLAUDE.md` bekerja secara normal**: rekan tim membaca file `CLAUDE.md` dari direktori kerja mereka. Gunakan ini untuk memberikan panduan spesifik proyek ke semua rekan tim.
</Tip>

## Langkah berikutnya

Jelajahi pendekatan terkait untuk pekerjaan paralel dan delegasi:

* **Delegasi ringan**: [subagents](/id/sub-agents) menelurkan agent pembantu untuk penelitian atau verifikasi dalam session Anda, lebih baik untuk tugas yang tidak memerlukan koordinasi inter-agent
* **Session paralel manual**: [Git worktrees](/id/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) memungkinkan Anda menjalankan beberapa session Claude Code sendiri tanpa koordinasi tim otomatis
* **Bandingkan pendekatan**: lihat perbandingan [subagent vs tim agent](/id/features-overview#compare-similar-features) untuk rincian side-by-side
