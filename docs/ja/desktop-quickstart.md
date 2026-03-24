> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# デスクトップアプリを始める

> Claude Code をデスクトップにインストールして、最初のコーディングセッションを開始します

デスクトップアプリは、グラフィカルインターフェース付きの Claude Code を提供します。ビジュアル diff レビュー、ライブアプリプレビュー、GitHub PR 監視と自動マージ、Git worktree 分離による並列セッション、スケジュール済みタスク、リモートでタスクを実行する機能があります。ターミナルは不要です。

このページでは、アプリのインストールと最初のセッションの開始について説明します。既にセットアップが完了している場合は、[Claude Code Desktop を使用する](/ja/desktop)で完全なリファレンスを参照してください。

<Frame>
  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce" className="block dark:hidden" alt="Code タブが選択されている Claude Code Desktop インターフェースを示しており、プロンプトボックス、権限モードセレクター（'Ask permissions'に設定）、モデルピッカー、フォルダセレクター、Local environment オプションが表示されています" width="2500" height="1376" data-path="images/desktop-code-tab-light.png" />

  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8" className="hidden dark:block" alt="ダークモードの Claude Code Desktop インターフェースを示しており、Code タブが選択されている状態で、プロンプトボックス、権限モードセレクター（'Ask permissions'に設定）、モデルピッカー、フォルダセレクター、Local environment オプションが表示されています" width="2504" height="1374" data-path="images/desktop-code-tab-dark.png" />
</Frame>

デスクトップアプリには 3 つのタブがあります。

* **Chat**: ファイルアクセスなしの一般的な会話。claude.ai と同様です。
* **Cowork**: クラウド VM で独自の環境を持つ自律型バックグラウンドエージェント。あなたが他の作業をしている間も独立して実行できます。
* **Code**: ローカルファイルへの直接アクセスを備えたインタラクティブなコーディングアシスタント。各変更をリアルタイムでレビューして承認します。

Chat と Cowork は [Claude Desktop サポート記事](https://support.claude.com/en/collections/16163169-claude-desktop)で説明されています。このページは **Code** タブに焦点を当てています。

<Note>
  Claude Code には [Pro、Max、Teams、または Enterprise サブスクリプション](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing)が必要です。
</Note>

## インストール

<Steps>
  <Step title="アプリをダウンロードする">
    お使いのプラットフォーム用に Claude をダウンロードしてください。

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Intel と Apple Silicon 用のユニバーサルビルド
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        x64 プロセッサ用
      </Card>
    </CardGroup>

    Windows ARM64 の場合は、[ここからダウンロード](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs)してください。

    Linux は現在サポートされていません。
  </Step>

  <Step title="サインインする">
    Applications フォルダ（macOS）または Start メニュー（Windows）から Claude を起動します。Anthropic アカウントでサインインしてください。
  </Step>

  <Step title="Code タブを開く">
    上部中央の **Code** タブをクリックします。Code をクリックするとアップグレードを促すメッセージが表示される場合は、最初に[有料プランにサブスクライブ](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_upgrade)する必要があります。オンラインでサインインするよう促すメッセージが表示される場合は、サインインを完了してアプリを再起動してください。403 エラーが表示される場合は、[認証のトラブルシューティング](/ja/desktop#403-or-authentication-errors-in-the-code-tab)を参照してください。
  </Step>
</Steps>

デスクトップアプリには Claude Code が含まれています。Node.js または CLI を別途インストールする必要はありません。ターミナルから `claude` を使用するには、CLI を別途インストールしてください。[CLI を始める](/ja/quickstart)を参照してください。

## 最初のセッションを開始する

Code タブを開いた状態で、プロジェクトを選択して Claude に何かをさせます。

<Steps>
  <Step title="環境とフォルダを選択する">
    **Local** を選択して、Claude をマシン上で実行し、ファイルを直接使用します。**Select folder** をクリックして、プロジェクトディレクトリを選択します。

    <Tip>
      よく知っている小さなプロジェクトから始めてください。Claude Code が何ができるかを見るための最速の方法です。Windows では、ローカルセッションが機能するために [Git](https://git-scm.com/downloads/win)がインストールされている必要があります。ほとんどの Mac にはデフォルトで Git が含まれています。
    </Tip>

    以下も選択できます。

    * **Remote**: Anthropic のクラウドインフラストラクチャでセッションを実行します。アプリを閉じても続行します。リモートセッションは [Claude Code on the web](/ja/claude-code-on-the-web)と同じインフラストラクチャを使用します。
    * **SSH**: SSH 経由でリモートマシンに接続します（独自のサーバー、クラウド VM、または dev コンテナー）。Claude Code はリモートマシンにインストールされている必要があります。
  </Step>

  <Step title="モデルを選択する">
    送信ボタンの横のドロップダウンからモデルを選択します。Opus、Sonnet、Haiku の比較については、[モデル](/ja/model-config#available-models)を参照してください。セッション開始後はモデルを変更できません。
  </Step>

  <Step title="Claude に何をするかを伝える">
    Claude にしてほしいことを入力します。

    * `TODO コメントを見つけて修正する`
    * `メイン関数のテストを追加する`
    * `このコードベースの指示を含む CLAUDE.md を作成する`

    [セッション](/ja/desktop#work-in-parallel-with-sessions)は、コードについて Claude との会話です。各セッションは独自のコンテキストと変更を追跡するため、複数のタスクに取り組む際に相互に干渉することなく作業できます。
  </Step>

  <Step title="変更をレビューして受け入れる">
    デフォルトでは、Code タブは [Ask permissions モード](/ja/desktop#choose-a-permission-mode)で開始されます。このモードでは、Claude が変更を提案し、適用する前にあなたの承認を待ちます。以下が表示されます。

    1. 各ファイルで何が変わるかを正確に示す [diff ビュー](/ja/desktop#review-changes-with-diff-view)
    2. 各変更を承認または拒否する Accept/Reject ボタン
    3. Claude があなたのリクエストを処理する際のリアルタイム更新

    変更を拒否すると、Claude は別の方法で進めたいかを尋ねます。あなたが受け入れるまで、ファイルは変更されません。
  </Step>
</Steps>

## 次は何をしますか？

最初の編集が完了しました。Desktop ができることすべての完全なリファレンスについては、[Claude Code Desktop を使用する](/ja/desktop)を参照してください。次に試すべきことをいくつか紹介します。

**割り込みと操舵。** Claude をいつでも割り込むことができます。間違った方向に進んでいる場合は、停止ボタンをクリックするか、修正を入力して **Enter** を押します。Claude は何をしているかを停止し、あなたの入力に基づいて調整します。完了を待つか、最初からやり直す必要はありません。

**Claude により多くのコンテキストを提供する。** プロンプトボックスに `@filename` と入力して特定のファイルを会話に取り込み、添付ボタンを使用して画像と PDF を添付するか、ファイルをプロンプトに直接ドラッグアンドドロップします。Claude が持つコンテキストが多いほど、結果は良くなります。[ファイルとコンテキストを追加する](/ja/desktop#add-files-and-context-to-prompts)を参照してください。

**繰り返し可能なタスクにスキルを使用する。** `/` を入力するか、**+** → **Slash commands** をクリックして、[組み込みコマンド](/ja/commands)、[カスタムスキル](/ja/skills)、およびプラグインスキルを参照します。スキルは、コードレビューチェックリストやデプロイメント手順など、必要なときに呼び出すことができる再利用可能なプロンプトです。

**コミット前に変更をレビューする。** Claude がファイルを編集した後、`+12 -1` インジケーターが表示されます。それをクリックして [diff ビュー](/ja/desktop#review-changes-with-diff-view)を開き、ファイルごとに変更をレビューし、特定の行にコメントします。Claude はあなたのコメントを読んで修正します。**Review code** をクリックして、Claude に diff を評価させ、インライン提案を残させます。

**コントロール量を調整する。** [権限モード](/ja/desktop#choose-a-permission-mode)は、バランスを制御します。Ask permissions（デフォルト）は、すべての編集の前に承認が必要です。Auto accept edits は、ファイル編集を自動的に受け入れて、より高速な反復を実現します。Plan mode では、Claude がファイルに触れずにアプローチをマップアウトできます。これは大規模なリファクタリング前に便利です。

**プラグインを追加してさらに多くの機能を追加する。** プロンプトボックスの横の **+** ボタンをクリックして **Plugins** を選択し、スキル、エージェント、MCP servers などを追加する [プラグイン](/ja/desktop#install-plugins)を参照してインストールします。

**アプリをプレビューする。** **Preview** ドロップダウンをクリックして、デスクトップで直接開発サーバーを実行します。Claude は実行中のアプリを表示し、エンドポイントをテストし、ログを検査し、見たものに対して反復できます。[アプリをプレビューする](/ja/desktop#preview-your-app)を参照してください。

**プルリクエストを追跡する。** PR を開いた後、Claude Code は CI チェック結果を監視し、失敗を自動的に修正するか、すべてのチェックが成功したら PR をマージできます。[プルリクエストステータスを監視する](/ja/desktop#monitor-pull-request-status)を参照してください。

**Claude をスケジュールに配置する。** [スケジュール済みタスク](/ja/desktop#schedule-recurring-tasks)を設定して、Claude を定期的に自動実行します。毎朝のコードレビュー、週次の依存関係監査、または接続されたツールから取得する概要です。

**準備ができたらスケールアップする。** サイドバーから [並列セッション](/ja/desktop#work-in-parallel-with-sessions)を開いて、複数のタスクに同時に取り組みます。各タスクは独自の Git worktree にあります。[長時間実行される作業をクラウドに送信](/ja/desktop#run-long-running-tasks-remotely)して、アプリを閉じても続行するか、タスクが予想より長くかかる場合は [web またはあなたの IDE でセッションを続行](/ja/desktop#continue-in-another-surface)します。[GitHub、Slack、Linear などの外部ツールを接続](/ja/desktop#extend-claude-code)して、ワークフローをまとめます。

## CLI から来ましたか？

Desktop は、グラフィカルインターフェース付きの CLI と同じエンジンを実行します。同じプロジェクトで両方を同時に実行でき、設定（CLAUDE.md ファイル、MCP servers、hooks、スキル、設定）を共有します。機能、フラグの同等物、Desktop で利用できないものの完全な比較については、[CLI 比較](/ja/desktop#coming-from-the-cli)を参照してください。

## 次のステップ

* [Claude Code Desktop を使用する](/ja/desktop): 権限モード、並列セッション、diff ビュー、コネクター、エンタープライズ設定
* [トラブルシューティング](/ja/desktop#troubleshooting): 一般的なエラーとセットアップの問題の解決策
* [ベストプラクティス](/ja/best-practices): 効果的なプロンプトを書き、Claude Code を最大限に活用するためのヒント
* [一般的なワークフロー](/ja/common-workflows): デバッグ、リファクタリング、テストなどのチュートリアル
