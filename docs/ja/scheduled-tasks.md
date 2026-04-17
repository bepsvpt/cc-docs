> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# スケジュールに従ってプロンプトを実行する

> /loop と cron スケジューリングツールを使用して、Claude Code セッション内でプロンプトを繰り返し実行したり、ステータスをポーリングしたり、1 回限りのリマインダーを設定したりします。

<Note>
  スケジュール済みタスクには Claude Code v2.1.72 以降が必要です。`claude --version` でバージョンを確認してください。
</Note>

スケジュール済みタスクを使用すると、Claude は一定の間隔でプロンプトを自動的に再実行できます。デプロイメントをポーリングしたり、PR を監視したり、長時間実行されるビルドをチェックバックしたり、後でセッション内で何かを実行するようにリマインダーを設定したりするために使用します。イベントが発生したときにポーリングする代わりに反応するには、[Channels](/ja/channels) を参照してください。CI はセッションに直接失敗をプッシュできます。

タスクはセッションスコープです。現在の Claude Code プロセスに存在し、終了すると消えます。再起動後も存在する永続的なスケジューリングについては、[Routines](/ja/routines)、[Desktop スケジュール済みタスク](/ja/desktop-scheduled-tasks)、または [GitHub Actions](/ja/github-actions) を使用してください。

## スケジューリングオプションを比較する

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## /loop で定期的にプロンプトを実行する

`/loop` [バンドルスキル](/ja/commands) は、セッションが開いている間、プロンプトを繰り返し実行する最速の方法です。間隔とプロンプトの両方はオプションであり、提供する内容によってループの動作が決まります。

| 提供する内容       | 例                           | 動作                                                                                       |
| :----------- | :-------------------------- | :--------------------------------------------------------------------------------------- |
| 間隔とプロンプト     | `/loop 5m check the deploy` | プロンプトは[固定スケジュール](#run-on-a-fixed-interval)で実行されます                                        |
| プロンプトのみ      | `/loop check the deploy`    | プロンプトは各反復で[Claude が選択した間隔](#let-claude-choose-the-interval)で実行されます                       |
| 間隔のみ、または何もなし | `/loop`                     | [組み込みメンテナンスプロンプト](#run-the-built-in-maintenance-prompt)が実行されるか、存在する場合は `loop.md` が実行されます |

別のコマンドをプロンプトとして渡すこともできます。例えば `/loop 20m /review-pr 1234` は、各反復でパッケージ化されたワークフローを再実行します。

### 固定間隔で実行する

間隔を指定すると、Claude はそれを cron 式に変換し、ジョブをスケジュールし、頻度とジョブ ID を確認します。

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

間隔は `30m` のような裸のトークンとしてプロンプトの前に配置することも、`every 2 hours` のような句としてプロンプトの後に配置することもできます。サポートされている単位は、秒の場合は `s`、分の場合は `m`、時間の場合は `h`、日の場合は `d` です。

秒は cron が 1 分の粒度を持つため、最も近い分に切り上げられます。`7m` や `90m` など、クリーンな cron ステップにマップされない間隔は、最も近い間隔に丸められ、Claude が選択したものを通知します。

### Claude に間隔を選択させる

間隔を省略すると、Claude は固定 cron スケジュールで実行する代わりに、動的に間隔を選択します。各反復の後、観察した内容に基づいて 1 分から 1 時間の間の遅延を選択します。ビルドが完了している間または PR がアクティブな間は短い待機時間、何も保留中でない場合は長い待機時間です。選択された遅延とその理由は、各反復の終了時に出力されます。

以下の例は CI とレビューコメントをチェックし、PR が静かになると Claude がより長く反復間で待機します。

```text theme={null}
/loop check whether CI passed and address any review comments
```

動的な `/loop` スケジュールをリクエストすると、Claude は [Monitor ツール](/ja/tools-reference#monitor-tool) を直接使用する場合があります。Monitor はバックグラウンドスクリプトを実行し、各出力行をストリーミングバックします。これにより、ポーリングを完全に回避でき、プロンプトを間隔で再実行するよりも多くの場合、トークン効率が高く、応答性が高くなります。

動的にスケジュールされたループは、他のタスクと同様に[スケジュール済みタスクリスト](#manage-scheduled-tasks)に表示されるため、同じ方法でリストまたはキャンセルできます。[ジッタールール](#jitter)は適用されませんが、[7 日間の有効期限](#seven-day-expiry)は適用されます。ループは開始後 7 日で自動的に終了します。

<Note>
  Bedrock、Vertex AI、Microsoft Foundry では、間隔なしのプロンプトは固定 10 分スケジュールで実行されます。
</Note>

### 組み込みメンテナンスプロンプトを実行する

プロンプトを省略すると、Claude は提供するプロンプトの代わりに組み込みメンテナンスプロンプトを使用します。各反復で、以下を順番に処理します。

* 会話からの未完了の作業を続行する
* 現在のブランチのプルリクエストを処理する。レビューコメント、失敗した CI 実行、マージコンフリクト
* 他に何も保留中でない場合、バグハントや簡素化などのクリーンアップパスを実行する

Claude はそのスコープ外の新しいイニシアチブを開始せず、プッシュまたは削除などの取り消し不可能なアクションは、トランスクリプトが既に承認した何かを続行する場合にのみ進行します。

```text theme={null}
/loop
```

裸の `/loop` は、このプロンプトを[動的に選択された間隔](#let-claude-choose-the-interval)で実行します。例えば `/loop 15m` のように間隔を追加して、代わりに固定スケジュールで実行します。組み込みプロンプトを独自のデフォルトに置き換えるには、[loop.md でデフォルトプロンプトをカスタマイズする](#customize-the-default-prompt-with-loop-md)を参照してください。

<Note>
  Bedrock、Vertex AI、Microsoft Foundry では、プロンプトなしの `/loop` は使用メッセージを出力し、メンテナンスループを開始しません。
</Note>

### loop.md でデフォルトプロンプトをカスタマイズする

`loop.md` ファイルは、組み込みメンテナンスプロンプトを独自の指示に置き換えます。これは、裸の `/loop` の単一のデフォルトプロンプトを定義し、個別のスケジュール済みタスクのリストではなく、コマンドラインでプロンプトを指定するたびに無視されます。それと一緒に追加のプロンプトをスケジュールするには、`/loop <prompt>` を使用するか、[Claude に直接依頼してください](#manage-scheduled-tasks)。

Claude は 2 つの場所でファイルを探し、最初に見つかったものを使用します。

| パス                  | スコープ                                |
| :------------------ | :---------------------------------- |
| `.claude/loop.md`   | プロジェクトレベル。両方のファイルが存在する場合は優先されます。    |
| `~/.claude/loop.md` | ユーザーレベル。独自のファイルを定義しないプロジェクトに適用されます。 |

ファイルは必須の構造を持たないプレーン Markdown です。`/loop` プロンプトを直接入力しているかのように記述してください。以下の例は、リリースブランチを健全に保ちます。

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

`loop.md` への編集は次の反復で有効になるため、ループが実行中に指示を改善できます。どちらの場所にも `loop.md` が存在しない場合、ループは組み込みメンテナンスプロンプトにフォールバックします。ファイルは簡潔に保ってください。25,000 バイトを超えるコンテンツは切り詰められます。

## 1 回限りのリマインダーを設定する

1 回限りのリマインダーの場合は、`/loop` を使用する代わりに、自然言語で実行したい内容を説明してください。Claude は実行後に自身を削除する単一実行タスクをスケジュールします。

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude は cron 式を使用して火災時間を特定の分と時間に固定し、いつ実行されるかを確認します。

## スケジュール済みタスクを管理する

自然言語で Claude にタスクをリストまたはキャンセルするよう依頼するか、基盤となるツールを直接参照してください。

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

内部的には、Claude はこれらのツールを使用します。

| ツール          | 目的                                                                   |
| :----------- | :------------------------------------------------------------------- |
| `CronCreate` | 新しいタスクをスケジュールします。5 フィールドの cron 式、実行するプロンプト、および繰り返すか 1 回実行するかを受け入れます。 |
| `CronList`   | ID、スケジュール、プロンプトを含むすべてのスケジュール済みタスクをリストします。                            |
| `CronDelete` | ID でタスクをキャンセルします。                                                    |

各スケジュール済みタスクには、`CronDelete` に渡すことができる 8 文字の ID があります。セッションは一度に最大 50 個のスケジュール済みタスクを保持できます。

## スケジュール済みタスクの実行方法

スケジューラは毎秒期限切れのタスクをチェックし、低優先度でキューに入れます。スケジュール済みプロンプトは、Claude が応答の途中ではなく、ターン間で実行されます。タスクが期限切れになったときに Claude がビジーの場合、プロンプトは現在のターンが終了するまで待機します。

すべての時間はローカルタイムゾーンで解釈されます。`0 9 * * *` のような cron 式は、UTC ではなく、Claude Code を実行している場所の午前 9 時を意味します。

### ジッター

すべてのセッションが同じ壁時計の瞬間に API にヒットするのを避けるために、スケジューラは火災時間に小さな決定論的オフセットを追加します。

* 定期的なタスクは、その期間の最大 10% 遅く実行され、15 分でキャップされます。時間ごとのジョブは `:00` から `:06` のどこかで実行される可能性があります。
* 時間の上部または下部にスケジュールされた 1 回限りのタスクは、最大 90 秒早く実行されます。

オフセットはタスク ID から派生しているため、同じタスクは常に同じオフセットを取得します。正確なタイミングが重要な場合は、`0 9 * * *` ではなく `3 9 * * *` など、`:00` または `:30` ではない分を選択すると、1 回限りのジッターは適用されません。

### 7 日間の有効期限

定期的なタスクは作成後 7 日で自動的に期限切れになります。タスクは最後に 1 回実行され、その後自身を削除します。これにより、忘れられたループが実行できる期間が制限されます。定期的なタスクをより長く続ける必要がある場合は、期限切れになる前にキャンセルして再作成するか、永続的なスケジューリングのために [Routines](/ja/routines) または [Desktop スケジュール済みタスク](/ja/desktop-scheduled-tasks) を使用してください。

## Cron 式リファレンス

`CronCreate` は標準 5 フィールド cron 式を受け入れます。`minute hour day-of-month month day-of-week`。すべてのフィールドは、ワイルドカード（`*`）、単一値（`5`）、ステップ（`*/15`）、範囲（`1-5`）、カンマ区切りリスト（`1,15,30`）をサポートしています。

| 例              | 意味                        |
| :------------- | :------------------------ |
| `*/5 * * * *`  | 5 分ごと                     |
| `0 * * * *`    | 毎時間の時刻                    |
| `7 * * * *`    | 毎時間 7 分経過時                |
| `0 9 * * *`    | 毎日午前 9 時（ローカル）            |
| `0 9 * * 1-5`  | 平日午前 9 時（ローカル）            |
| `30 14 15 3 *` | 3 月 15 日午後 2 時 30 分（ローカル） |

曜日は日曜日の場合は `0` または `7`、土曜日の場合は `6` を使用します。`L`、`W`、`?` などの拡張構文や、`MON` や `JAN` などの名前エイリアスはサポートされていません。

月の日と曜日の両方が制約されている場合、どちらかのフィールドが一致すれば日付が一致します。これは標準の vixie-cron セマンティクスに従います。

## スケジュール済みタスクを無効にする

環境で `CLAUDE_CODE_DISABLE_CRON=1` を設定して、スケジューラ全体を無効にします。cron ツールと `/loop` は利用できなくなり、既にスケジュール済みのタスクは実行を停止します。無効化フラグの完全なリストについては、[環境変数](/ja/env-vars) を参照してください。

## 制限事項

セッションスコープのスケジューリングには固有の制約があります。

* タスクは Claude Code が実行中でアイドル状態の場合にのみ実行されます。ターミナルを閉じるか、セッションを終了すると、すべてがキャンセルされます。
* 見落とされた火災のキャッチアップはありません。タスクのスケジュール済み時間が Claude が長時間実行されるリクエストでビジーの間に経過した場合、Claude がアイドル状態になったときに 1 回実行され、見落とされた間隔ごとに 1 回ではありません。
* 再起動間での永続性はありません。Claude Code を再起動すると、すべてのセッションスコープのタスクがクリアされます。

無人で実行する必要がある cron 駆動オートメーションの場合は、以下を使用してください。

* [Routines](/ja/routines)：Anthropic 管理インフラストラクチャでスケジュールに従って実行、API 呼び出し、または GitHub イベント時に実行
* [GitHub Actions](/ja/github-actions)：CI で `schedule` トリガーを使用
* [Desktop スケジュール済みタスク](/ja/desktop-scheduled-tasks)：マシン上でローカルに実行
