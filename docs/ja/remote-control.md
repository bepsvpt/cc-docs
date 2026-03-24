> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 任意のデバイスからローカルセッションを続行する Remote Control

> Remote Control を使用して、電話、タブレット、または任意のブラウザから Claude Code のローカルセッションを続行します。claude.ai/code と Claude モバイルアプリで動作します。

<Note>
  Remote Control はすべてのプランで利用可能です。Team および Enterprise 管理者は、まず [管理設定](https://claude.ai/admin-settings/claude-code) で Claude Code を有効にする必要があります。
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

* **サブスクリプション**: Pro、Max、Team、および Enterprise プランで利用可能です。Team および Enterprise 管理者は、まず [管理設定](https://claude.ai/admin-settings/claude-code) で Claude Code を有効にする必要があります。API キーはサポートされていません。
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

リモートセッションは、`--name` 引数（または `/remote-control` に渡された名前）、最後のメッセージ、`/rename` 値、または会話履歴がない場合は「Remote Control session」から名前を取得します。環境に既にアクティブなセッションがある場合は、それを続行するか新しいセッションを開始するかを尋ねられます。

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

## 関連リソース

* [Web 上の Claude Code](/ja/claude-code-on-the-web): マシン上ではなく Anthropic が管理するクラウド環境でセッションを実行します
* [認証](/ja/authentication): `/login` をセットアップし、claude.ai の認証情報を管理します
* [CLI リファレンス](/ja/cli-reference): `claude remote-control` を含むフラグとコマンドの完全なリスト
* [セキュリティ](/ja/security): Remote Control セッションが Claude Code セキュリティモデルにどのように適合するか
* [データ使用](/ja/data-usage): ローカルおよびリモートセッション中に Anthropic API を通じてどのようなデータが流れるか
