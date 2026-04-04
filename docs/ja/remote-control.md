> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 任意のデバイスからローカルセッションを続行する Remote Control

> Remote Control を使用して、電話、タブレット、または任意のブラウザから Claude Code のローカルセッションを続行します。claude.ai/code と Claude モバイルアプリで動作します。

<Note>
  Remote Control はすべてのプランで利用可能です。Team および Enterprise では、管理者が [Claude Code 管理設定](https://claude.ai/admin-settings/claude-code) で Remote Control トグルを有効にするまで、デフォルトではオフになっています。
</Note>

Remote Control は [claude.ai/code](https://claude.ai/code) または Claude アプリ（[iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) および [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)）をマシン上で実行されている Claude Code セッションに接続します。デスクでタスクを開始してから、ソファの電話またはコンピュータのブラウザで続行できます。

マシン上で Remote Control セッションを開始すると、Claude はローカルで実行され続けるため、クラウドに移動するものはありません。Remote Control を使用すると、以下のことができます。

* **ローカル環境全体をリモートで使用する**: ファイルシステム、[MCP サーバー](/ja/mcp)、ツール、プロジェクト設定がすべて利用可能なままです
* **両方のサーフェスから同時に作業する**: 会話はすべての接続されたデバイス間で同期されるため、ターミナル、ブラウザ、電話から相互に交換可能にメッセージを送信できます
* **中断に対応する**: ラップトップがスリープ状態になったり、ネットワークが切断されたりした場合、マシンがオンラインに戻ると、セッションは自動的に再接続されます

クラウドインフラストラクチャで実行される [Web 上の Claude Code](/ja/claude-code-on-the-web) とは異なり、Remote Control セッションはマシン上で直接実行され、ローカルファイルシステムと相互作用します。Web およびモバイルインターフェースは、そのローカルセッションへのウィンドウにすぎません。

<Note>
  Remote Control には Claude Code v2.1.51 以降が必要です。`claude --version` でバージョンを確認してください。
</Note>

このページでは、セットアップ、セッションの開始と接続方法、および Remote Control と Web 上の Claude Code の比較について説明します。

## 要件

Remote Control を使用する前に、環境が以下の条件を満たしていることを確認してください。

* **サブスクリプション**: Pro、Max、Team、および Enterprise プランで利用可能です。API キーはサポートされていません。Team および Enterprise では、管理者が [Claude Code 管理設定](https://claude.ai/admin-settings/claude-code) で Remote Control トグルを有効にする必要があります。
* **認証**: `claude` を実行し、まだサインインしていない場合は `/login` を使用して claude.ai 経由でサインインします。
* **ワークスペース信頼**: プロジェクトディレクトリで少なくとも 1 回 `claude` を実行して、ワークスペース信頼ダイアログを受け入れます。

## Remote Control セッションを開始する

専用の Remote Control サーバーを開始するか、Remote Control を有効にした対話型セッションを開始するか、既に実行されているセッションに接続できます。

<Tabs>
  <Tab title="サーバーモード">
    プロジェクトディレクトリに移動して、以下を実行します。

    ```bash  theme={null}
    claude remote-control
    ```

    プロセスはサーバーモードでターミナルで実行され続け、リモート接続を待機します。[別のデバイスから接続](#別のデバイスから接続する) するために使用できるセッション URL が表示され、スペースバーを押して電話からの高速アクセス用の QR コードを表示できます。リモートセッションがアクティブな間、ターミナルは接続ステータスとツールアクティビティを表示します。

    利用可能なフラグ:

    | フラグ                          | 説明                                                                                                                                                                                                                                                                   |
    | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`        | claude.ai/code のセッションリストに表示されるカスタムセッションタイトルを設定します。                                                                                                                                                                                                                   |
    | `--spawn <mode>`             | 同時セッションの作成方法。実行時に `w` を押してトグルします。<br />• `same-dir`（デフォルト）: すべてのセッションが現在の作業ディレクトリを共有するため、同じファイルを編集している場合は競合する可能性があります。<br />• `worktree`: オンデマンドセッションごとに独自の [git worktree](/ja/common-workflows#git-worktrees-を使用して並列-claude-code-セッションを実行する) を取得します。git リポジトリが必要です。 |
    | `--capacity <N>`             | 同時セッションの最大数。デフォルトは 32 です。                                                                                                                                                                                                                                            |
    | `--verbose`                  | 詳細な接続とセッションログを表示します。                                                                                                                                                                                                                                                 |
    | `--sandbox` / `--no-sandbox` | ファイルシステムとネットワーク分離のための [サンドボックス](/ja/sandboxing) を有効または無効にします。デフォルトではオフです。                                                                                                                                                                                            |
  </Tab>

  <Tab title="対話型セッション">
    Remote Control を有効にした通常の対話型 Claude Code セッションを開始するには、`--remote-control` フラグ（または `--rc`）を使用します。

    ```bash  theme={null}
    claude --remote-control
    ```

    オプションでセッションの名前を渡します。

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    これにより、ターミナルで完全な対話型セッションが得られ、claude.ai または Claude アプリからも制御できます。`claude remote-control`（サーバーモード）とは異なり、セッションがリモートで利用可能な間、ローカルでメッセージを入力できます。
  </Tab>

  <Tab title="既存のセッションから">
    既に Claude Code セッションにいて、それをリモートで続行したい場合は、`/remote-control`（または `/rc`）コマンドを使用します。

    ```text  theme={null}
    /remote-control
    ```

    カスタムセッションタイトルを設定するために、引数として名前を渡します。

    ```text  theme={null}
    /remote-control My Project
    ```

    これにより、現在の会話履歴を引き継ぎ、[別のデバイスから接続](#別のデバイスから接続する) するために使用できるセッション URL と QR コードを表示する Remote Control セッションが開始されます。`--verbose`、`--sandbox`、および `--no-sandbox` フラグはこのコマンドでは利用できません。
  </Tab>
</Tabs>

### 別のデバイスから接続する

Remote Control セッションがアクティブになったら、別のデバイスから接続するいくつかの方法があります。

* **セッション URL を開く** 任意のブラウザで [claude.ai/code](https://claude.ai/code) のセッションに直接移動します。`claude remote-control` と `/remote-control` の両方がターミナルにこの URL を表示します。
* **QR コードをスキャンする** セッション URL の横に表示される QR コードをスキャンして、Claude アプリで直接開きます。`claude remote-control` を使用する場合は、スペースバーを押して QR コード表示をトグルします。
* **[claude.ai/code](https://claude.ai/code) または Claude アプリを開く** セッションリストで名前でセッションを見つけます。Remote Control セッションはオンラインの場合、コンピュータアイコンと緑色のステータスドットを表示します。

リモートセッションのタイトルは、この順序で選択されます。

1. `--name`、`--remote-control`、または `/remote-control` に渡した名前
2. `/rename` で設定したタイトル
3. 既存の会話履歴の最後の意味のあるメッセージ
4. メッセージを送信した後の最初のプロンプト

環境に既にアクティブなセッションがある場合は、それを続行するか新しいセッションを開始するかを尋ねられます。

Claude アプリをまだ持っていない場合は、Claude Code 内で `/mobile` コマンドを使用して、[iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) または [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) のダウンロード QR コードを表示します。

### すべてのセッションで Remote Control を有効にする

デフォルトでは、Remote Control は `claude remote-control`、`claude --remote-control`、または `/remote-control` を明示的に実行した場合にのみアクティブになります。すべての対話型セッションで自動的に有効にするには、Claude Code 内で `/config` を実行し、**Enable Remote Control for all sessions** を `true` に設定します。無効にするには `false` に設定します。

この設定がオンの場合、各対話型 Claude Code プロセスは 1 つのリモートセッションを登録します。複数のインスタンスを実行する場合、各インスタンスは独自の環境とセッションを取得します。単一のプロセスから複数の同時セッションを実行するには、代わりに `--spawn` でサーバーモードを使用します。

## 接続とセキュリティ

ローカル Claude Code セッションは、アウトバウンド HTTPS リクエストのみを行い、マシン上のインバウンドポートを開くことはありません。Remote Control を開始すると、Anthropic API に登録され、作業をポーリングします。別のデバイスから接続すると、サーバーは Web またはモバイルクライアントとローカルセッション間のメッセージをストリーミング接続経由でルーティングします。

すべてのトラフィックは TLS 経由で Anthropic API を通じて移動し、Claude Code セッションと同じトランスポートセキュリティです。接続は複数の短命の認証情報を使用し、各認証情報は単一の目的にスコープされ、独立して有効期限が切れます。

## Remote Control と Web 上の Claude Code

Remote Control と [Web 上の Claude Code](/ja/claude-code-on-the-web) の両方が claude.ai/code インターフェースを使用します。主な違いはセッションが実行される場所です。Remote Control はマシン上で実行されるため、ローカル MCP サーバー、ツール、プロジェクト設定が利用可能なままです。Web 上の Claude Code は Anthropic が管理するクラウドインフラストラクチャで実行されます。

ローカル作業の途中で別のデバイスから続行したい場合は Remote Control を使用します。ローカルセットアップなしでタスクを開始したい場合、クローンしていないリポジトリで作業したい場合、または複数のタスクを並列で実行したい場合は Web 上の Claude Code を使用します。

## 制限事項

* **対話型プロセスごとに 1 つのリモートセッション**: サーバーモード外では、各 Claude Code インスタンスは一度に 1 つのリモートセッションをサポートします。単一のプロセスから複数の同時セッションを実行するには、`--spawn` でサーバーモードを使用します。
* **ターミナルを開いたままにする**: Remote Control はローカルプロセスとして実行されます。ターミナルを閉じるか `claude` プロセスを停止すると、セッションは終了します。新しいセッションを開始するには、`claude remote-control` を再度実行します。
* **長時間のネットワーク障害**: マシンが起動しているがおよそ 10 分以上ネットワークに到達できない場合、セッションはタイムアウトしてプロセスは終了します。新しいセッションを開始するには、`claude remote-control` を再度実行します。

## トラブルシューティング

### 「Remote Control はまだアカウントで有効になっていません」

特定の環境変数が存在する場合、適格性チェックが失敗する可能性があります。

* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` または `DISABLE_TELEMETRY`: それらを設定解除して再度試してください。
* `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_VERTEX`、または `CLAUDE_CODE_USE_FOUNDRY`: Remote Control は claude.ai 認証が必要であり、サードパーティプロバイダーでは機能しません。

これらのいずれも設定されていない場合は、`/logout` を実行してから `/login` を実行して更新します。

### 「Remote Control は組織のポリシーで無効になっています」

このエラーには 3 つの異なる原因があります。最初に `/status` を実行して、使用しているログイン方法とサブスクリプションを確認してください。

* **API キーまたは Console アカウントで認証されている**: Remote Control は claude.ai OAuth が必要です。`/login` を実行して claude.ai オプションを選択します。`ANTHROPIC_API_KEY` が環境に設定されている場合は、設定を解除します。
* **Team または Enterprise 管理者が有効にしていない**: Remote Control はこれらのプランではデフォルトでオフになっています。管理者は [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) で **Remote Control** トグルをオンにして有効にできます。これはサーバー側の組織設定であり、[管理設定のみ](/ja/permissions#managed-only-settings) キーではありません。
* **管理者トグルがグレーアウトしている**: 組織には Remote Control と互換性のないデータ保持またはコンプライアンス設定があります。これは管理パネルから変更することはできません。オプションについて説明するために Anthropic サポートに連絡してください。

### 「リモート認証情報の取得に失敗しました」

Claude Code は Anthropic API から短命の認証情報を取得して接続を確立できませんでした。`--verbose` で再度実行して完全なエラーを確認してください。

```bash  theme={null}
claude remote-control --verbose
```

一般的な原因:

* サインインしていない: `claude` を実行し、`/login` を使用して claude.ai アカウントで認証します。API キー認証は Remote Control ではサポートされていません。
* ネットワークまたはプロキシの問題: ファイアウォールまたはプロキシがアウトバウンド HTTPS リクエストをブロックしている可能性があります。Remote Control はポート 443 で Anthropic API へのアクセスが必要です。
* セッション作成に失敗: `Session creation failed — see debug log` も表示される場合、失敗はセットアップの前の段階で発生しました。サブスクリプションがアクティブであることを確認してください。

## 適切なアプローチを選択する

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                                          | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                                  | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                           | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                                      | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                                         | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop-scheduled-tasks), or [cloud](/en/web-scheduled-tasks) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## 関連リソース

* [Web 上の Claude Code](/ja/claude-code-on-the-web): マシン上ではなく Anthropic が管理するクラウド環境でセッションを実行します
* [チャネル](/ja/channels): Telegram または Discord をセッションに転送して、Claude が離席中にメッセージに反応するようにします
* [Dispatch](/ja/desktop#dispatch-からのセッション): 電話からタスクをメッセージして、Desktop セッションを生成して処理できます
* [認証](/ja/authentication): `/login` をセットアップし、claude.ai の認証情報を管理します
* [CLI リファレンス](/ja/cli-reference): `claude remote-control` を含むフラグとコマンドの完全なリスト
* [セキュリティ](/ja/security): Remote Control セッションが Claude Code セキュリティモデルにどのように適合するか
* [データ使用](/ja/data-usage): ローカルおよびリモートセッション中に Anthropic API を通じてどのようなデータが流れるか
