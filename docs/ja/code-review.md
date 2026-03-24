> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> マルチエージェント分析を使用してコードベース全体を検査し、ロジックエラー、セキュリティ脆弱性、リグレッションを検出する自動化された PR レビューを設定します

<Note>
  Code Review はリサーチプレビュー段階であり、[Teams および Enterprise](https://claude.ai/admin-settings/claude-code) サブスクリプションで利用可能です。[Zero Data Retention](/ja/zero-data-retention) が有効になっている組織では利用できません。
</Note>

Code Review は GitHub プルリクエストを分析し、コードの問題が見つかった行にインラインコメントとして結果を投稿します。特化したエージェントのフリートがコード変更をコードベース全体のコンテキストで検査し、ロジックエラー、セキュリティ脆弱性、壊れたエッジケース、微妙なリグレッションを探します。

結果は重大度でタグ付けされ、PR を承認またはブロックしないため、既存のレビューワークフローはそのまま機能します。リポジトリに `CLAUDE.md` または `REVIEW.md` ファイルを追加することで、Claude がフラグを立てる内容をカスタマイズできます。

Claude を管理サービスではなく独自の CI インフラストラクチャで実行する場合は、[GitHub Actions](/ja/github-actions) または [GitLab CI/CD](/ja/gitlab-ci-cd) を参照してください。

このページでは以下をカバーしています：

* [レビューの仕組み](#how-reviews-work)
* [セットアップ](#set-up-code-review)
* [`CLAUDE.md` と `REVIEW.md` を使用した](#customize-reviews)レビューのカスタマイズ
* [料金](#pricing)

## レビューの仕組み

管理者が組織の Code Review を[有効にする](#set-up-code-review)と、リポジトリの設定された動作に応じて、PR が開かれたとき、すべてのプッシュ時、または手動でリクエストされたときにレビューがトリガーされます。PR で `@claude review` と[コメントすると](#manually-trigger-reviews)、任意のモードでレビューが開始されます。

レビューが実行されると、複数のエージェントが Anthropic インフラストラクチャ上で並行して diff と周囲のコードを分析します。各エージェントは異なるクラスの問題を探し、その後、検証ステップが候補を実際のコード動作に対してチェックして、偽陽性を除外します。結果は重複排除され、重大度でランク付けされ、問題が見つかった特定の行にインラインコメントとして投稿されます。問題が見つからない場合、Claude は PR に短い確認コメントを投稿します。

レビューはコストが PR のサイズと複雑さに応じてスケーリングされ、平均 20 分で完了します。管理者は[分析ダッシュボード](#view-usage)を通じてレビューアクティビティと支出を監視できます。

### 重大度レベル

各結果は重大度レベルでタグ付けされます：

| マーカー | 重大度          | 意味                             |
| :--- | :----------- | :----------------------------- |
| 🔴   | Normal       | マージ前に修正すべきバグ                   |
| 🟡   | Nit          | 軽微な問題、修正する価値があるがブロッキングではない     |
| 🟣   | Pre-existing | コードベースに存在するが、この PR で導入されなかったバグ |

結果には、展開可能な拡張推論セクションが含まれており、Claude がなぜ問題をフラグ立てしたのか、どのように問題を検証したのかを理解するために展開できます。

### Code Review がチェックする内容

デフォルトでは、Code Review は正確性に焦点を当てています：フォーマット設定の好みやテストカバレッジの欠落ではなく、本番環境を壊すバグです。リポジトリに[ガイダンスファイルを追加](#customize-reviews)することで、チェック内容を拡張できます。

## Code Review のセットアップ

管理者が組織に対して Code Review を 1 回有効にし、含めるリポジトリを選択します。

<Steps>
  <Step title="Claude Code 管理設定を開く">
    [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) にアクセスして、Code Review セクションを見つけます。Claude 組織への管理者アクセスと GitHub 組織に GitHub Apps をインストールする権限が必要です。
  </Step>

  <Step title="セットアップを開始する">
    **Setup** をクリックします。これにより GitHub App インストールフローが開始されます。
  </Step>

  <Step title="Claude GitHub App をインストールする">
    プロンプトに従って、Claude GitHub App を GitHub 組織にインストールします。アプリは以下のリポジトリ権限をリクエストします：

    * **Contents**: 読み取りと書き込み
    * **Issues**: 読み取りと書き込み
    * **Pull requests**: 読み取りと書き込み

    Code Review は contents への読み取りアクセスと pull requests への書き込みアクセスを使用します。より広い権限セットは、後で有効にする場合、[GitHub Actions](/ja/github-actions) もサポートします。
  </Step>

  <Step title="リポジトリを選択する">
    Code Review を有効にするリポジトリを選択します。リポジトリが表示されない場合は、インストール中に Claude GitHub App にアクセス権を付与したことを確認してください。後でリポジトリを追加できます。
  </Step>

  <Step title="リポジトリごとにレビュートリガーを設定する">
    セットアップが完了すると、Code Review セクションはリポジトリをテーブルに表示します。各リポジトリについて、**Review Behavior** ドロップダウンを使用してレビューが実行されるタイミングを選択します：

    * **Once after PR creation**: PR が開かれるか ready for review としてマークされたときにレビューが 1 回実行されます
    * **After every push**: PR ブランチへのすべてのプッシュでレビューが実行され、PR が進化するにつれて新しい問題をキャッチし、フラグが立てられた問題を修正するとスレッドを自動解決します
    * **Manual**: [PR で `@claude review` とコメント](#manually-trigger-reviews)したときのみレビューが開始されます。その後、その PR へのプッシュは自動的にレビューされます

    すべてのプッシュでレビューすると、最も多くのレビューが実行され、最もコストがかかります。Manual モードは、特定の PR をレビューにオプトインしたい高トラフィックリポジトリ、または PR が ready になったら PR のレビューを開始したい場合に便利です。
  </Step>
</Steps>

リポジトリテーブルは、最近のアクティビティに基づいて各リポジトリの平均レビューコストも表示します。行アクションメニューを使用して、リポジトリごとに Code Review をオンまたはオフにするか、リポジトリを完全に削除します。

セットアップを確認するには、テスト PR を開きます。自動トリガーを選択した場合、**Claude Code Review** という名前のチェック実行が数分以内に表示されます。Manual を選択した場合は、PR で `@claude review` とコメントして最初のレビューを開始します。チェック実行が表示されない場合は、リポジトリが管理設定に一覧表示されていることと、Claude GitHub App がアクセス権を持っていることを確認してください。

## レビューを手動でトリガーする

プルリクエストで `@claude review` とコメントしてレビューを開始し、その PR をプッシュトリガーレビューにオプトインします。これはリポジトリの設定されたトリガーに関係なく機能します：Manual モードで特定の PR をレビューにオプトインするか、他のモードで即座に再レビューを取得するために使用します。どちらの場合でも、その PR へのプッシュはそれ以降トリガーレビューを実行します。

コメントがレビューをトリガーするには：

* トップレベルの PR コメントとして投稿し、diff 行のインラインコメントではない
* コメントの開始に `@claude review` を配置する
* リポジトリへのオーナー、メンバー、またはコラボレーターアクセス権を持つ必要があります
* PR は開いていて、ドラフトではない必要があります

レビューがその PR で既に実行されている場合、リクエストは進行中のレビューが完了するまでキューに入ります。PR のチェック実行を通じて進捗を監視できます。

## レビューをカスタマイズする

Code Review はリポジトリから 2 つのファイルを読み取り、フラグを立てる内容をガイドします。どちらもデフォルトの正確性チェックの上に追加されます：

* **`CLAUDE.md`**: Claude Code がすべてのタスク（レビューだけではなく）に使用する共有プロジェクト指示。ガイダンスが対話的な Claude Code セッションにも適用される場合に使用します。
* **`REVIEW.md`**: レビューのみのガイダンス、コードレビュー中にのみ読み取られます。レビュー中にフラグを立てるか、スキップするかについての厳密なルールで、一般的な `CLAUDE.md` を乱雑にするルールに使用します。

### CLAUDE.md

Code Review はリポジトリの `CLAUDE.md` ファイルを読み取り、新しく導入された違反を nit レベルの結果として扱います。これは双方向に機能します：PR が `CLAUDE.md` ステートメントを古くする方法でコードを変更する場合、Claude はドキュメントを更新する必要があることをフラグ立てします。

Claude はディレクトリ階層のすべてのレベルで `CLAUDE.md` ファイルを読み取るため、サブディレクトリの `CLAUDE.md` のルールはそのパスの下のファイルにのみ適用されます。`CLAUDE.md` の仕組みの詳細については、[memory ドキュメント](/ja/memory)を参照してください。

一般的な Claude Code セッションに適用したくないレビュー固有のガイダンスについては、代わりに[`REVIEW.md`](#review-md)を使用します。

### REVIEW\.md

レビュー固有のルールについては、リポジトリルートに `REVIEW.md` ファイルを追加します。以下をエンコードするために使用します：

* 会社またはチームのスタイルガイドライン：「ネストされた条件付きよりも早期リターンを優先する」
* リンターでカバーされていない言語またはフレームワーク固有の規約
* Claude が常にフラグを立てるべきもの：「新しい API ルートには対応する統合テストが必要」
* Claude がスキップすべきもの：「`/gen/` の下の生成されたコードのフォーマットについてコメントしない」

`REVIEW.md` の例：

```markdown  theme={null}
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude はリポジトリルートで `REVIEW.md` を自動検出します。設定は不要です。

## 使用状況を表示する

[claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) にアクセスして、組織全体の Code Review アクティビティを確認します。ダッシュボードは以下を表示します：

| セクション                | 表示内容                              |
| :------------------- | :-------------------------------- |
| PRs reviewed         | 選択した時間範囲でレビューされたプルリクエストの日次カウント    |
| Cost weekly          | Code Review の週次支出                 |
| Feedback             | 開発者が問題に対処したため自動解決されたレビューコメントのカウント |
| Repository breakdown | リポジトリごとのレビューされた PR とコメント解決のカウント   |

管理設定のリポジトリテーブルは、各リポジトリの平均レビューコストも表示します。

## 料金

Code Review はトークン使用量に基づいて請求されます。レビューは平均 \$15～25 で、PR サイズ、コードベースの複雑さ、検証が必要な問題の数に応じてスケーリングされます。Code Review の使用は[extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)を通じて個別に請求され、プランの含まれた使用量にはカウントされません。

選択するレビュートリガーは総コストに影響します：

* **Once after PR creation**: PR ごとに 1 回実行されます
* **After every push**: 各プッシュで実行され、プッシュ数でコストが乗算されます
* **Manual**: PR で誰かが `@claude review` とコメントするまでレビューはありません

どのモードでも、`@claude review` と[コメント](#manually-trigger-reviews)すると、PR がプッシュトリガーレビューにオプトインされるため、そのコメント後のプッシュごとに追加コストが発生します。

コストは、組織が他の Claude Code 機能に AWS Bedrock または Google Vertex AI を使用しているかどうかに関係なく、Anthropic の請求書に表示されます。Code Review の月次支出上限を設定するには、[claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) にアクセスして、Claude Code Review サービスの制限を設定します。

[analytics](#view-usage) の週次コストチャートまたは管理設定のリポジトリごとの平均コスト列を通じて支出を監視します。

## 関連リソース

Code Review は Claude Code の残りの部分と連携するように設計されています。PR を開く前にローカルでレビューを実行したい場合、自己ホスト型セットアップが必要な場合、または `CLAUDE.md` がツール全体で Claude の動作をどのように形成するかについてさらに詳しく知りたい場合、これらのページは次の良い停止点です：

* [Plugins](/ja/discover-plugins): プッシュ前にローカルでオンデマンドレビューを実行するための `code-review` プラグインを含むプラグインマーケットプレイスを参照
* [GitHub Actions](/ja/github-actions): コードレビューを超えたカスタム自動化のための独自の GitHub Actions ワークフローで Claude を実行
* [GitLab CI/CD](/ja/gitlab-ci-cd): GitLab パイプライン用の自己ホスト型 Claude 統合
* [Memory](/ja/memory): Claude Code 全体で `CLAUDE.md` ファイルがどのように機能するか
* [Analytics](/ja/analytics): コードレビューを超えた Claude Code 使用状況を追跡
