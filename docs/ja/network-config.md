> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# エンタープライズネットワーク設定

> プロキシサーバー、カスタム認証局（CA）、相互 Transport Layer Security（mTLS）認証を使用して、エンタープライズ環境向けに Claude Code を設定します。

Claude Code は、環境変数を通じてさまざまなエンタープライズネットワークおよびセキュリティ設定をサポートしています。これには、企業プロキシサーバーを経由したトラフィックのルーティング、カスタム認証局（CA）の信頼、およびセキュリティ強化のための相互 Transport Layer Security（mTLS）証明書による認証が含まれます。

<Note>
  このページに表示されているすべての環境変数は、[`settings.json`](/ja/settings) でも設定できます。
</Note>

## プロキシ設定

### 環境変数

Claude Code は標準的なプロキシ環境変数に対応しています。

```bash  theme={null}
# HTTPS プロキシ（推奨）
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP プロキシ（HTTPS が利用できない場合）
export HTTP_PROXY=http://proxy.example.com:8080

# 特定のリクエストのプロキシをバイパス - スペース区切り形式
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# 特定のリクエストのプロキシをバイパス - カンマ区切り形式
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# すべてのリクエストのプロキシをバイパス
export NO_PROXY="*"
```

<Note>
  Claude Code は SOCKS プロキシをサポートしていません。
</Note>

### 基本認証

プロキシが基本認証を必要とする場合は、プロキシ URL に認証情報を含めます。

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  スクリプトにパスワードをハードコーディングすることは避けてください。代わりに環境変数またはセキュアな認証情報ストレージを使用してください。
</Warning>

<Tip>
  高度な認証（NTLM、Kerberos など）が必要なプロキシの場合は、認証方法をサポートする LLM Gateway サービスの使用を検討してください。
</Tip>

## カスタム CA 証明書

エンタープライズ環境で HTTPS 接続用のカスタム CA を使用している場合（プロキシ経由でも直接 API アクセスでも）、Claude Code をそれらを信頼するように設定します。

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 認証

クライアント証明書認証が必要なエンタープライズ環境の場合：

```bash  theme={null}
# 認証用のクライアント証明書
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# クライアント秘密鍵
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# オプション：暗号化された秘密鍵のパスフレーズ
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## ネットワークアクセス要件

Claude Code は以下の URL へのアクセスが必要です。

* `api.anthropic.com`：Claude API エンドポイント
* `claude.ai`：claude.ai アカウント用の認証
* `platform.claude.com`：Anthropic Console アカウント用の認証

これらの URL がプロキシ設定とファイアウォールルールでホワイトリストに登録されていることを確認してください。これは、Claude Code をコンテナ化された環境または制限されたネットワーク環境で使用する場合に特に重要です。

## その他のリソース

* [Claude Code 設定](/ja/settings)
* [環境変数リファレンス](/ja/settings#environment-variables)
* [トラブルシューティングガイド](/ja/troubleshooting)
