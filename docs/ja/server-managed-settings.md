> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# サーバー管理設定を構成する（パブリックベータ版）

> デバイス管理インフラストラクチャを必要とせずに、Claude.ai 上のウェブベースインターフェースを通じて、組織全体で Claude Code を一元的に構成します。

サーバー管理設定により、管理者は Claude.ai 上のウェブベースインターフェースを通じて Claude Code を一元的に構成できます。Claude Code クライアントは、ユーザーが組織の認証情報で認証すると、これらの設定を自動的に受け取ります。

このアプローチは、デバイス管理インフラストラクチャが導入されていない組織、または管理されていないデバイス上のユーザーの設定を管理する必要がある組織向けに設計されています。

<Note>
  サーバー管理設定はパブリックベータ版であり、[Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) および [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise) カスタマー向けに利用可能です。一般提供前に機能が変更される可能性があります。
</Note>

## 要件

サーバー管理設定を使用するには、以下が必要です。

* Claude for Teams または Claude for Enterprise プラン
* Claude for Teams の場合はバージョン 2.1.38 以降、Claude for Enterprise の場合はバージョン 2.1.30 以降の Claude Code
* `api.anthropic.com` へのネットワークアクセス

## サーバー管理設定とエンドポイント管理設定の選択

Claude Code は、一元的な構成のための 2 つのアプローチをサポートしています。サーバー管理設定は Anthropic のサーバーから構成を配信します。[エンドポイント管理設定](/ja/settings#settings-files)は、ネイティブ OS ポリシー（macOS 管理設定、Windows レジストリ）または管理設定ファイルを通じてデバイスに直接配置されます。

| アプローチ                                          | 最適な用途                           | セキュリティモデル                                          |
| :--------------------------------------------- | :------------------------------ | :------------------------------------------------- |
| **サーバー管理設定**                                   | MDM がない組織、または管理されていないデバイス上のユーザー | 認証時に Anthropic のサーバーから配信される設定                      |
| **[エンドポイント管理設定](/ja/settings#settings-files)** | MDM またはエンドポイント管理がある組織           | MDM 構成プロファイル、レジストリポリシー、または管理設定ファイルを通じてデバイスに配置される設定 |

デバイスが MDM またはエンドポイント管理ソリューションに登録されている場合、エンドポイント管理設定はより強力なセキュリティ保証を提供します。これは、設定ファイルが OS レベルでユーザーの変更から保護される可能性があるためです。

## サーバー管理設定を構成する

<Steps>
  <Step title="管理コンソールを開く">
    [Claude.ai](https://claude.ai) で、**Admin Settings > Claude Code > Managed settings** に移動します。
  </Step>

  <Step title="設定を定義する">
    構成を JSON として追加します。`settings.json` で利用可能な[すべての設定](/ja/settings#available-settings)がサポートされており、[hooks](/ja/hooks)、[環境変数](/ja/env-vars)、および `allowManagedPermissionRulesOnly` などの[管理専用設定](/ja/permissions#managed-only-settings)も含まれます。

    この例は、権限拒否リストを適用し、ユーザーが権限をバイパスするのを防ぎます。

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      }
    }
    ```

    hooks は `settings.json` と同じ形式を使用します。

    この例は、組織全体のすべてのファイル編集後に監査スクリプトを実行します。

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    [auto mode](/ja/permission-modes#eliminate-prompts-with-auto-mode) 分類器を構成して、組織が信頼するリポジトリ、バケット、ドメインを認識させるには、以下のようにします。

    ```json  theme={null}
    {
      "autoMode": {
        "environment": [
          "Source control: github.example.com/acme-corp and all repos under it",
          "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
          "Trusted internal domains: *.corp.example.com"
        ]
      }
    }
    ```

    hooks はシェルコマンドを実行するため、ユーザーは適用される前に[セキュリティ承認ダイアログ](#security-approval-dialogs)を表示します。`autoMode` エントリが分類器がブロックする内容にどのように影響するか、および `allow` フィールドと `soft_deny` フィールドに関する重要な警告については、[auto mode 分類器を構成する](/ja/permissions#configure-the-auto-mode-classifier)を参照してください。
  </Step>

  <Step title="保存してデプロイする">
    変更を保存します。Claude Code クライアントは、次回の起動時または 1 時間ごとのポーリングサイクルで更新された設定を受け取ります。
  </Step>
</Steps>

### 設定配信の確認

設定が適用されていることを確認するには、ユーザーに Claude Code を再起動するよう依頼します。構成に[セキュリティ承認ダイアログ](#security-approval-dialogs)をトリガーする設定が含まれている場合、ユーザーは起動時に管理設定を説明するプロンプトを表示します。また、ユーザーに `/permissions` を実行して有効な権限ルールを表示させることで、管理権限ルールがアクティブであることを確認することもできます。

### アクセス制御

以下のロールがサーバー管理設定を管理できます。

* **Primary Owner**
* **Owner**

設定の変更は組織内のすべてのユーザーに適用されるため、信頼できる担当者へのアクセスを制限してください。

### 現在の制限事項

サーバー管理設定には、ベータ期間中に以下の制限があります。

* 設定は組織内のすべてのユーザーに均一に適用されます。グループごとの構成はまだサポートされていません。
* [MCP サーバー構成](/ja/mcp#managed-mcp-configuration)は、サーバー管理設定を通じて配布することはできません。

## 設定配信

### 設定の優先順位

サーバー管理設定と[エンドポイント管理設定](/ja/settings#settings-files)は、Claude Code [設定階層](/ja/settings#settings-precedence)の最上位を占めます。コマンドライン引数を含む他の設定レベルはこれらをオーバーライドできません。両方が存在する場合、サーバー管理設定が優先され、エンドポイント管理設定は使用されません。

### フェッチとキャッシング動作

Claude Code は起動時に Anthropic のサーバーから設定をフェッチし、アクティブなセッション中は 1 時間ごとに更新をポーリングします。

**キャッシュされた設定なしの初回起動：**

* Claude Code は非同期で設定をフェッチします
* フェッチが失敗した場合、Claude Code は管理設定なしで続行します
* 設定が読み込まれるまでの短い期間があり、その間は制限が適用されません

**キャッシュされた設定での後続の起動：**

* キャッシュされた設定は起動時に直ちに適用されます
* Claude Code はバックグラウンドで新しい設定をフェッチします
* キャッシュされた設定はネットワーク障害を通じて保持されます

Claude Code は設定の更新を自動的に適用します。ただし、OpenTelemetry 構成などの高度な設定は、有効にするために完全な再起動が必要です。

### セキュリティ承認ダイアログ

セキュリティリスクをもたらす可能性のある特定の設定には、適用される前に明示的なユーザー承認が必要です。

* **シェルコマンド設定**：シェルコマンドを実行する設定
* **カスタム環境変数**：既知の安全なホワイトリストにない変数
* **フック構成**：任意のフック定義

これらの設定が存在する場合、ユーザーは構成されている内容を説明するセキュリティダイアログを表示します。ユーザーは続行するために承認する必要があります。ユーザーが設定を拒否した場合、Claude Code は終了します。

<Note>
  `-p` フラグを使用した非対話モードでは、Claude Code はセキュリティダイアログをスキップし、ユーザー承認なしで設定を適用します。
</Note>

## プラットフォームの可用性

サーバー管理設定は `api.anthropic.com` への直接接続が必要であり、サードパーティのモデルプロバイダーを使用する場合は利用できません。

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* `ANTHROPIC_BASE_URL` または [LLM ゲートウェイ](/ja/llm-gateway)を通じたカスタム API エンドポイント

## 監査ログ

設定変更の監査ログイベントは、コンプライアンス API または監査ログエクスポートを通じて利用可能です。アクセスについては、Anthropic アカウントチームにお問い合わせください。

監査イベントには、実行されたアクションのタイプ、アクションを実行したアカウントとデバイス、および前の値と新しい値への参照が含まれます。

## セキュリティに関する考慮事項

サーバー管理設定は一元的なポリシー適用を提供しますが、クライアント側の制御として機能します。管理されていないデバイスでは、管理者またはスーパーユーザーアクセス権を持つユーザーは、Claude Code バイナリ、ファイルシステム、またはネットワーク構成を変更できます。

| シナリオ                                     | 動作                                                         |
| :--------------------------------------- | :--------------------------------------------------------- |
| ユーザーがキャッシュされた設定ファイルを編集する                 | 改ざんされたファイルは起動時に適用されますが、次のサーバーフェッチで正しい設定が復元されます             |
| ユーザーがキャッシュされた設定ファイルを削除する                 | 初回起動動作が発生します。設定は非同期でフェッチされ、短い未適用ウィンドウがあります                 |
| API が利用不可                                | キャッシュされた設定が利用可能な場合は適用されます。そうでない場合、管理設定は次の成功したフェッチまで適用されません |
| ユーザーが別の組織で認証する                           | 管理対象組織外のアカウントには設定が配信されません                                  |
| ユーザーがデフォルト以外の `ANTHROPIC_BASE_URL` を設定する | サードパーティの API プロバイダーを使用する場合、サーバー管理設定はバイパスされます               |

ランタイム構成の変更を検出するには、[`ConfigChange` フック](/ja/hooks#configchange)を使用して、変更をログに記録するか、変更が有効になる前に不正な変更をブロックします。

より強力な適用保証については、MDM ソリューションに登録されているデバイスで[エンドポイント管理設定](/ja/settings#settings-files)を使用してください。

## 関連項目

Claude Code 構成を管理するための関連ページ。

* [Settings](/ja/settings)：すべての利用可能な設定を含む完全な構成リファレンス
* [Endpoint-managed settings](/ja/settings#settings-files)：IT によってデバイスに配置される管理設定
* [Authentication](/ja/authentication)：Claude Code へのユーザーアクセスのセットアップ
* [Security](/ja/security)：セキュリティ保護とベストプラクティス
