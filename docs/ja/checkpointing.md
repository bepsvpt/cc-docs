> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Claude の編集を自動的に追跡し、不要な変更から素早く復旧するために以前の状態に巻き戻します。

Claude Code は、作業中に Claude のファイル編集を自動的に追跡し、何か問題が発生した場合に変更を素早く取り消し、以前の状態に巻き戻すことができます。

## Checkpointing の仕組み

Claude と作業する際、checkpointing は各編集の前にコードの状態を自動的にキャプチャします。このセーフティネットにより、野心的で大規模なタスクを実行する際に、いつでも以前のコード状態に戻ることができるという安心感を持って作業できます。

### 自動追跡

Claude Code は、ファイル編集ツールによって行われたすべての変更を追跡します：

* ユーザープロンプトごとに新しい checkpoint が作成されます
* Checkpoint はセッション間で保持されるため、再開された会話でアクセスできます
* セッションとともに 30 日後に自動的にクリーンアップされます（設定可能）

### 変更の巻き戻し

`Esc` キーを 2 回（`Esc` + `Esc`）押すか、`/rewind` コマンドを使用して rewind メニューを開きます。以下のいずれかを復元することを選択できます：

* **会話のみ**: ユーザーメッセージに巻き戻しながらコード変更を保持します
* **コードのみ**: 会話を保持しながらファイル変更を元に戻します
* **コードと会話の両方**: セッション内の以前の時点に両方を復元します

## 一般的なユースケース

Checkpoint は以下の場合に特に有用です：

* **代替案の検討**: 開始点を失わずに異なる実装アプローチを試します
* **ミスからの復旧**: バグを導入したり機能を破損させた変更を素早く取り消します
* **機能の反復**: 動作する状態に戻すことができることを知りながら、バリエーションを試験します

## 制限事項

### Bash コマンドの変更は追跡されません

Checkpointing は bash コマンドによって変更されたファイルを追跡しません。例えば、Claude Code が以下を実行する場合：

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

これらのファイル変更は rewind を通じて取り消すことはできません。Claude のファイル編集ツールを通じて行われた直接的なファイル編集のみが追跡されます。

### 外部の変更は追跡されません

Checkpointing は、現在のセッション内で編集されたファイルのみを追跡します。Claude Code の外部で手動で行ったファイルの変更と、他の同時セッションからの編集は、通常はキャプチャされません。ただし、現在のセッションと同じファイルを変更する場合は除きます。

### バージョン管理の代替ではありません

Checkpoint はセッションレベルの迅速な復旧のために設計されています。永続的なバージョン履歴とコラボレーションのために：

* バージョン管理（例：Git）を引き続き使用してコミット、ブランチ、長期履歴を管理します
* Checkpoint は適切なバージョン管理を補完しますが、置き換えるものではありません
* Checkpoint を「ローカルアンドゥ」、Git を「永続履歴」と考えてください

## 関連項目

* [Interactive mode](/ja/interactive-mode) - キーボードショートカットとセッション制御
* [Built-in commands](/ja/interactive-mode#built-in-commands) - `/rewind` を使用した checkpoint へのアクセス
* [CLI reference](/ja/cli-reference) - コマンドラインオプション
