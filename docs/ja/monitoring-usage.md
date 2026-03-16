> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 監視

> Claude Code の OpenTelemetry を有効にして設定する方法を学びます。

Claude Code は、監視と可観測性のための OpenTelemetry (OTel) メトリクスとイベントをサポートしています。

すべてのメトリクスは OpenTelemetry の標準メトリクスプロトコルを介してエクスポートされる時系列データであり、イベントは OpenTelemetry のログ/イベントプロトコルを介してエクスポートされます。メトリクスとログのバックエンドが適切に設定されており、集約の粒度が監視要件を満たしていることを確認するのはユーザーの責任です。

## クイックスタート

環境変数を使用して OpenTelemetry を設定します:

```bash  theme={null}
# 1. テレメトリを有効にする
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. エクスポーターを選択する (両方はオプション - 必要なものだけを設定してください)
export OTEL_METRICS_EXPORTER=otlp       # オプション: otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # オプション: otlp, console

# 3. OTLP エンドポイントを設定する (OTLP エクスポーター用)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. 認証を設定する (必要な場合)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. デバッグ用: エクスポート間隔を短縮する
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 秒 (デフォルト: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 秒 (デフォルト: 5000ms)

# 6. Claude Code を実行する
claude
```

<Note>
  デフォルトのエクスポート間隔は、メトリクスが 60 秒、ログが 5 秒です。セットアップ中は、デバッグ目的で短い間隔を使用することをお勧めします。本番環境での使用に向けてこれらをリセットすることを忘れないでください。
</Note>

完全な設定オプションについては、[OpenTelemetry 仕様](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options)を参照してください。

## 管理者設定

管理者は、[管理設定ファイル](/ja/settings#settings-files)を通じてすべてのユーザーの OpenTelemetry 設定を設定できます。これにより、組織全体のテレメトリ設定を一元管理できます。設定がどのように適用されるかについては、[設定の優先順位](/ja/settings#settings-precedence)を参照してください。

管理設定の設定例:

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

<Note>
  管理設定は MDM (Mobile Device Management) または他のデバイス管理ソリューションを通じて配布できます。管理設定ファイルで定義された環境変数は優先度が高く、ユーザーによってオーバーライドすることはできません。
</Note>

## 設定の詳細

### 一般的な設定変数

| 環境変数                                            | 説明                                         | 例の値                                  |
| ----------------------------------------------- | ------------------------------------------ | ------------------------------------ |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                  | テレメトリ収集を有効にする (必須)                         | `1`                                  |
| `OTEL_METRICS_EXPORTER`                         | メトリクスエクスポーターのタイプ (カンマ区切り)                  | `console`, `otlp`, `prometheus`      |
| `OTEL_LOGS_EXPORTER`                            | ログ/イベントエクスポーターのタイプ (カンマ区切り)                | `console`, `otlp`                    |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                   | OTLP エクスポーターのプロトコル (すべてのシグナル)              | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                   | OTLP コレクターエンドポイント (すべてのシグナル)               | `http://localhost:4317`              |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`           | メトリクスのプロトコル (一般的な設定をオーバーライド)               | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`           | OTLP メトリクスエンドポイント (一般的な設定をオーバーライド)         | `http://localhost:4318/v1/metrics`   |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`              | ログのプロトコル (一般的な設定をオーバーライド)                  | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`              | OTLP ログエンドポイント (一般的な設定をオーバーライド)            | `http://localhost:4318/v1/logs`      |
| `OTEL_EXPORTER_OTLP_HEADERS`                    | OTLP の認証ヘッダー                               | `Authorization=Bearer token`         |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`         | mTLS 認証用のクライアントキー                          | クライアントキーファイルへのパス                     |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | mTLS 認証用のクライアント証明書                         | クライアント証明書ファイルへのパス                    |
| `OTEL_METRIC_EXPORT_INTERVAL`                   | エクスポート間隔 (ミリ秒単位、デフォルト: 60000)              | `5000`, `60000`                      |
| `OTEL_LOGS_EXPORT_INTERVAL`                     | ログエクスポート間隔 (ミリ秒単位、デフォルト: 5000)             | `1000`, `10000`                      |
| `OTEL_LOG_USER_PROMPTS`                         | ユーザープロンプトコンテンツのログを有効にする (デフォルト: 無効)        | `1` で有効化                             |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`   | 動的ヘッダーを更新するための間隔 (デフォルト: 1740000ms / 29 分) | `900000`                             |

### メトリクスカーディナリティ制御

以下の環境変数は、カーディナリティを管理するためにメトリクスに含まれる属性を制御します:

| 環境変数                                | 説明                               | デフォルト値  | 無効化する例  |
| ----------------------------------- | -------------------------------- | ------- | ------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | メトリクスに session.id 属性を含める         | `true`  | `false` |
| `OTEL_METRICS_INCLUDE_VERSION`      | メトリクスに app.version 属性を含める        | `false` | `true`  |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | メトリクスに user.account\_uuid 属性を含める | `true`  | `false` |

これらの変数は、メトリクスのカーディナリティを制御するのに役立ちます。これはメトリクスバックエンドのストレージ要件とクエリパフォーマンスに影響します。カーディナリティが低いほど、一般的にパフォーマンスが向上し、ストレージコストが低くなりますが、分析用のより詳細なデータは少なくなります。

### 動的ヘッダー

動的認証が必要なエンタープライズ環境では、ヘッダーを動的に生成するスクリプトを設定できます:

#### 設定ファイルの設定

`.claude/settings.json` に追加します:

```json  theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### スクリプト要件

スクリプトは HTTP ヘッダーを表す文字列キーと値のペアを持つ有効な JSON を出力する必要があります:

```bash  theme={null}
#!/bin/bash
# 例: 複数のヘッダー
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### リフレッシュ動作

ヘッダーヘルパースクリプトはスタートアップ時に実行され、その後定期的に実行されてトークンリフレッシュをサポートします。デフォルトでは、スクリプトは 29 分ごとに実行されます。`CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` 環境変数で間隔をカスタマイズします。

### マルチチーム組織サポート

複数のチームまたは部門を持つ組織は、`OTEL_RESOURCE_ATTRIBUTES` 環境変数を使用してカスタム属性を追加し、異なるグループを区別できます:

```bash  theme={null}
# チーム識別用のカスタム属性を追加する
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

これらのカスタム属性はすべてのメトリクスとイベントに含まれ、以下のことが可能になります:

* チームまたは部門別にメトリクスをフィルタリングする
* コストセンターごとのコストを追跡する
* チーム固有のダッシュボードを作成する
* 特定のチームのアラートを設定する

<Warning>
  **OTEL\_RESOURCE\_ATTRIBUTES の重要なフォーマット要件:**

  `OTEL_RESOURCE_ATTRIBUTES` 環境変数は [W3C Baggage 仕様](https://www.w3.org/TR/baggage/)に従い、厳密なフォーマット要件があります:

  * **スペースは許可されません**: 値にスペースを含めることはできません。例えば、`user.organizationName=My Company` は無効です
  * **フォーマット**: カンマ区切りのキー=値ペアである必要があります: `key1=value1,key2=value2`
  * **許可される文字**: 制御文字、空白、ダブルクォート、カンマ、セミコロン、バックスラッシュを除く US-ASCII 文字のみ
  * **特殊文字**: 許可された範囲外の文字はパーセントエンコードする必要があります

  **例:**

  ```bash  theme={null}
  # ❌ 無効 - スペースを含む
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ 有効 - アンダースコアまたはキャメルケースを代わりに使用する
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ 有効 - 必要に応じて特殊文字をパーセントエンコードする
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  注: 値をクォートで囲むことはスペースをエスケープしません。例えば、`org.name="My Company"` は `My Company` ではなく、リテラル値 `"My Company"` (クォート付き) になります。
</Warning>

### 設定例

```bash  theme={null}
# コンソールデバッグ (1 秒間隔)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# 複数のエクスポーター
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# メトリクスとログの異なるエンドポイント/バックエンド
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

# メトリクスのみ (イベント/ログなし)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# イベント/ログのみ (メトリクスなし)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## 利用可能なメトリクスとイベント

### 標準属性

すべてのメトリクスとイベントは、これらの標準属性を共有します:

| 属性                  | 説明                                                    | 制御者                                               |
| ------------------- | ----------------------------------------------------- | ------------------------------------------------- |
| `session.id`        | 一意のセッション識別子                                           | `OTEL_METRICS_INCLUDE_SESSION_ID` (デフォルト: true)   |
| `app.version`       | 現在の Claude Code バージョン                                 | `OTEL_METRICS_INCLUDE_VERSION` (デフォルト: false)     |
| `organization.id`   | 組織 UUID (認証時)                                         | 利用可能な場合は常に含まれます                                   |
| `user.account_uuid` | アカウント UUID (認証時)                                      | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (デフォルト: true) |
| `terminal.type`     | ターミナルタイプ (例: `iTerm.app`, `vscode`, `cursor`, `tmux`) | 検出された場合は常に含まれます                                   |

### メトリクス

Claude Code は以下のメトリクスをエクスポートします:

| メトリクス名                                | 説明                    | 単位     |
| ------------------------------------- | --------------------- | ------ |
| `claude_code.session.count`           | 開始された CLI セッションの数     | count  |
| `claude_code.lines_of_code.count`     | 変更されたコード行の数           | count  |
| `claude_code.pull_request.count`      | 作成されたプルリクエストの数        | count  |
| `claude_code.commit.count`            | 作成された git コミットの数      | count  |
| `claude_code.cost.usage`              | Claude Code セッションのコスト | USD    |
| `claude_code.token.usage`             | 使用されたトークンの数           | tokens |
| `claude_code.code_edit_tool.decision` | コード編集ツールの権限決定の数       | count  |
| `claude_code.active_time.total`       | 合計アクティブ時間 (秒単位)       | s      |

### メトリクスの詳細

#### セッションカウンター

各セッションの開始時にインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)

#### コード行カウンター

コードが追加または削除されたときにインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)
* `type`: (`"added"`, `"removed"`)

#### プルリクエストカウンター

Claude Code を介してプルリクエストを作成するときにインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)

#### コミットカウンター

Claude Code を介して git コミットを作成するときにインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)

#### コストカウンター

各 API リクエスト後にインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)
* `model`: モデル識別子 (例: "claude-sonnet-4-5-20250929")

#### トークンカウンター

各 API リクエスト後にインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: モデル識別子 (例: "claude-sonnet-4-5-20250929")

#### コード編集ツール決定カウンター

ユーザーが Edit、Write、または NotebookEdit ツールの使用を受け入れるか拒否するときにインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)
* `tool`: ツール名 (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: ユーザーの決定 (`"accept"`, `"reject"`)
* `language`: 編集されたファイルのプログラミング言語 (例: `"TypeScript"`, `"Python"`, `"JavaScript"`, `"Markdown"`)。認識されないファイル拡張子の場合は `"unknown"` を返します。

#### アクティブ時間カウンター

Claude Code を積極的に使用している実際の時間を追跡します (アイドル時間ではありません)。このメトリクスは、プロンプトの入力や応答の受信などのユーザーインタラクション中にインクリメントされます。

**属性**:

* すべての[標準属性](#standard-attributes)

### イベント

Claude Code は、OpenTelemetry ログ/イベント経由で以下のイベントをエクスポートします (`OTEL_LOGS_EXPORTER` が設定されている場合):

#### ユーザープロンプトイベント

ユーザーがプロンプトを送信するときにログされます。

**イベント名**: `claude_code.user_prompt`

**属性**:

* すべての[標準属性](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: ISO 8601 タイムスタンプ
* `prompt_length`: プロンプトの長さ
* `prompt`: プロンプトコンテンツ (デフォルトではマスク、`OTEL_LOG_USER_PROMPTS=1` で有効化)

#### ツール結果イベント

ツールが実行を完了するときにログされます。

**イベント名**: `claude_code.tool_result`

**属性**:

* すべての[標準属性](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: ISO 8601 タイムスタンプ
* `tool_name`: ツールの名前
* `success`: `"true"` または `"false"`
* `duration_ms`: 実行時間 (ミリ秒単位)
* `error`: エラーメッセージ (失敗した場合)
* `decision`: `"accept"` または `"reject"`
* `source`: 決定ソース - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, または `"user_reject"`
* `tool_parameters`: ツール固有のパラメーターを含む JSON 文字列 (利用可能な場合)
  * Bash ツールの場合: `bash_command`, `full_command`, `timeout`, `description`, `sandbox` を含む

#### API リクエストイベント

Claude への各 API リクエストについてログされます。

**イベント名**: `claude_code.api_request`

**属性**:

* すべての[標準属性](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: ISO 8601 タイムスタンプ
* `model`: 使用されたモデル (例: "claude-sonnet-4-5-20250929")
* `cost_usd`: 推定コスト (USD)
* `duration_ms`: リクエスト期間 (ミリ秒単位)
* `input_tokens`: 入力トークンの数
* `output_tokens`: 出力トークンの数
* `cache_read_tokens`: キャッシュから読み取られたトークンの数
* `cache_creation_tokens`: キャッシュ作成に使用されたトークンの数

#### API エラーイベント

Claude への API リクエストが失敗するときにログされます。

**イベント名**: `claude_code.api_error`

**属性**:

* すべての[標準属性](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: ISO 8601 タイムスタンプ
* `model`: 使用されたモデル (例: "claude-sonnet-4-5-20250929")
* `error`: エラーメッセージ
* `status_code`: HTTP ステータスコード (該当する場合)
* `duration_ms`: リクエスト期間 (ミリ秒単位)
* `attempt`: 試行番号 (再試行されたリクエストの場合)

#### ツール決定イベント

ツール権限決定 (受け入れ/拒否) が行われるときにログされます。

**イベント名**: `claude_code.tool_decision`

**属性**:

* すべての[標準属性](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: ISO 8601 タイムスタンプ
* `tool_name`: ツールの名前 (例: "Read", "Edit", "Write", "NotebookEdit")
* `decision`: `"accept"` または `"reject"`
* `source`: 決定ソース - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, または `"user_reject"`

## メトリクスとイベントデータの解釈

Claude Code によってエクスポートされるメトリクスは、使用パターンと生産性に関する貴重な洞察を提供します。作成できる一般的な可視化と分析は次のとおりです:

### 使用状況監視

| メトリクス                                                         | 分析の機会                              |
| ------------------------------------------------------------- | ---------------------------------- |
| `claude_code.token.usage`                                     | `type` (入力/出力)、ユーザー、チーム、またはモデル別に分類 |
| `claude_code.session.count`                                   | 時間経過に伴う採用と関与を追跡                    |
| `claude_code.lines_of_code.count`                             | コード追加/削除を追跡して生産性を測定                |
| `claude_code.commit.count` & `claude_code.pull_request.count` | 開発ワークフローへの影響を理解                    |

### コスト監視

`claude_code.cost.usage` メトリクスは以下に役立ちます:

* チームまたは個人全体の使用トレンドを追跡する
* 最適化のための高使用セッションを特定する

<Note>
  コストメトリクスは概算です。公式な請求データについては、API プロバイダー (Claude Console、AWS Bedrock、または Google Cloud Vertex) を参照してください。
</Note>

### アラートとセグメンテーション

検討すべき一般的なアラート:

* コストスパイク
* 異常なトークン消費
* 特定のユーザーからの高いセッションボリューム

すべてのメトリクスは、`user.account_uuid`、`organization.id`、`session.id`、`model`、および `app.version` でセグメント化できます。

### イベント分析

イベントデータは Claude Code インタラクションに関する詳細な洞察を提供します:

**ツール使用パターン**: ツール結果イベントを分析して以下を特定します:

* 最も頻繁に使用されるツール
* ツール成功率
* 平均ツール実行時間
* ツールタイプ別のエラーパターン

**パフォーマンス監視**: API リクエスト期間とツール実行時間を追跡して、パフォーマンスボトルネックを特定します。

## バックエンドに関する考慮事項

メトリクスとログバックエンドの選択により、実行できる分析のタイプが決まります:

### メトリクスの場合

* **時系列データベース (例: Prometheus)**: レート計算、集約メトリクス
* **カラムナーストア (例: ClickHouse)**: 複雑なクエリ、一意のユーザー分析
* **フル機能の可観測性プラットフォーム (例: Honeycomb、Datadog)**: 高度なクエリ、可視化、アラート

### イベント/ログの場合

* **ログ集約システム (例: Elasticsearch、Loki)**: 全文検索、ログ分析
* **カラムナーストア (例: ClickHouse)**: 構造化イベント分析
* **フル機能の可観測性プラットフォーム (例: Honeycomb、Datadog)**: メトリクスとイベント間の相関

日次/週次/月次アクティブユーザー (DAU/WAU/MAU) メトリクスが必要な組織の場合は、効率的な一意値クエリをサポートするバックエンドを検討してください。

## サービス情報

すべてのメトリクスとイベントは、以下のリソース属性でエクスポートされます:

* `service.name`: `claude-code`
* `service.version`: 現在の Claude Code バージョン
* `os.type`: オペレーティングシステムタイプ (例: `linux`, `darwin`, `windows`)
* `os.version`: オペレーティングシステムバージョン文字列
* `host.arch`: ホストアーキテクチャ (例: `amd64`, `arm64`)
* `wsl.version`: WSL バージョン番号 (Windows Subsystem for Linux で実行している場合のみ存在)
* メーター名: `com.anthropic.claude_code`

## ROI 測定リソース

テレメトリセットアップ、コスト分析、生産性メトリクス、自動レポート生成を含む Claude Code の投資収益率 (ROI) 測定に関する包括的なガイドについては、[Claude Code ROI 測定ガイド](https://github.com/anthropics/claude-code-monitoring-guide)を参照してください。このリポジトリは、すぐに使用できる Docker Compose 設定、Prometheus と OpenTelemetry セットアップ、Linear などのツールと統合された生産性レポート生成テンプレートを提供します。

## セキュリティ/プライバシーに関する考慮事項

* テレメトリはオプトインであり、明示的な設定が必要です
* API キーやファイルコンテンツなどの機密情報は、メトリクスやイベントに含まれることはありません
* ユーザープロンプトコンテンツはデフォルトではマスクされます - プロンプト長のみが記録されます。ユーザープロンプトログを有効にするには、`OTEL_LOG_USER_PROMPTS=1` を設定します

## Amazon Bedrock での Claude Code の監視

Amazon Bedrock での Claude Code 使用状況監視ガイダンスの詳細については、[Claude Code 監視実装 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md) を参照してください。
