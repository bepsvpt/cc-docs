> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# ターミナルセットアップを最適化する

> Claude Codeはターミナルが適切に設定されているときに最適に機能します。これらのガイドラインに従って、エクスペリエンスを最適化してください。

### テーマと外観

Claudeはターミナルのテーマを制御することはできません。これはターミナルアプリケーションによって処理されます。`/config`コマンドを使用して、いつでもClaude Codeのテーマをターミナルに合わせることができます。

Claude Codeインターフェース自体のさらなるカスタマイズについては、[カスタムステータスライン](/ja/statusline)を設定して、ターミナルの下部に現在のモデル、作業ディレクトリ、またはgitブランチなどのコンテキスト情報を表示することができます。

### 改行

Claude Codeに改行を入力するためのいくつかのオプションがあります：

* **クイックエスケープ**：`\`の後にEnterキーを押して改行を作成します
* **Shift+Enter**：iTerm2、WezTerm、Ghostty、およびKittyではそのまま機能します
* **キーボードショートカット**：他のターミナルで改行を挿入するためのキーバインディングを設定します

**他のターミナルでShift+Enterを設定する**

Claude Code内で`/terminal-setup`を実行して、VS Code、Alacritty、Zed、およびWarpのShift+Enterを自動的に設定します。

<Note>
  `/terminal-setup`コマンドは、手動設定が必要なターミナルにのみ表示されます。iTerm2、WezTerm、Ghostty、またはKittyを使用している場合、Shift+Enterはすでにネイティブに機能するため、このコマンドは表示されません。
</Note>

**Option+Enter（VS Code、iTerm2、またはmacOS Terminal.app）を設定する**

**Mac Terminal.appの場合：**

1. 設定 → プロファイル → キーボードを開く
2. 「OptionキーをMetaキーとして使用」をチェックする

**iTerm2およびVS Codeターミナルの場合：**

1. 設定 → プロファイル → キーを開く
2. 「一般」で、左右のOptionキーを「Esc+」に設定する

### 通知設定

適切な通知設定でClaudeがタスクを完了したときを見逃さないようにしてください：

#### iTerm 2システム通知

iTerm 2でタスク完了時にアラートを表示する場合：

1. iTerm 2の環境設定を開く
2. プロファイル → ターミナルに移動する
3. 「ベルを消音」を有効にし、フィルターアラート → 「エスケープシーケンスで生成されたアラートを送信」を選択する
4. 希望する通知遅延を設定する

これらの通知はiTerm 2に固有であり、デフォルトのmacOS Terminalでは利用できないことに注意してください。

#### カスタム通知フック

高度な通知処理については、[通知フック](/ja/hooks#notification)を作成して独自のロジックを実行できます。

### 大量入力の処理

広範なコードまたは長い指示を扱う場合：

* **直接貼り付けを避ける**：Claude Codeは非常に長い貼り付けコンテンツで問題が発生する可能性があります
* **ファイルベースのワークフローを使用する**：コンテンツをファイルに書き込み、Claudeに読み込むよう依頼します
* **VS Codeの制限に注意する**：VS Codeターミナルは特に長い貼り付けを切り詰める傾向があります

### Vimモード

Claude Codeは`/vim`で有効にするか、`/config`経由で設定できるVimキーバインディングのサブセットをサポートしています。

サポートされているサブセットには以下が含まれます：

* モード切り替え：`Esc`（NORMAL）、`i`/`I`、`a`/`A`、`o`/`O`（INSERT）
* ナビゲーション：`h`/`j`/`k`/`l`、`w`/`e`/`b`、`0`/`$`/`^`、`gg`/`G`、`f`/`F`/`t`/`T`（`;`/`,`リピート付き）
* 編集：`x`、`dw`/`de`/`db`/`dd`/`D`、`cw`/`ce`/`cb`/`cc`/`C`、`.`（リピート）
* ヤンク/ペースト：`yy`/`Y`、`yw`/`ye`/`yb`、`p`/`P`
* テキストオブジェクト：`iw`/`aw`、`iW`/`aW`、`i"`/`a"`、`i'`/`a'`、`i(`/`a(`、`i[`/`a[`、`i{`/`a{`
* インデント：`>>`/`<<`
* 行操作：`J`（行を結合）

完全なリファレンスについては、[インタラクティブモード](/ja/interactive-mode#vim-editor-mode)を参照してください。
