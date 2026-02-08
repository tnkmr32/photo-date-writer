---
name: git-commit
description: 'Conventional Commit メッセージ分析、インテリジェントなステージング、メッセージ生成を使用した git commit の実行。変更をコミットする、git コミットを作成する、または "/commit" を含むリクエストがある場合に使用します。サポート機能: (1) 変更からの type と scope の自動検出、(2) diff からの Conventional Commit メッセージの生成、(3) type/scope/description のオーバーライドオプション付き対話的コミット、(4) 論理的なグループ化のためのインテリジェントなファイルステージング'
license: MIT
allowed-tools: Bash
---

# Conventional Commits を使用した Git コミット

## 概要

Conventional Commits 仕様を使用して、標準化された意味のある git コミットを作成します。実際の diff を分析して、適切な type、scope、メッセージを決定します。

## Conventional Commit フォーマット

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

以下は英語で記載してください：
- `type`
- `scope`

以下は日本語で記載してください：
- `description`
- `body`
- `footer`

## コミットタイプ

| Type       | 目的                                    |
| ---------- | --------------------------------------- |
| `feat`     | 新機能                                  |
| `fix`      | バグ修正                                |
| `docs`     | ドキュメントのみ                        |
| `style`    | フォーマット/スタイル（ロジックなし）   |
| `refactor` | コードリファクタリング（機能/修正なし） |
| `perf`     | パフォーマンス改善                      |
| `test`     | テストの追加/更新                       |
| `build`    | ビルドシステム/依存関係                 |
| `ci`       | CI/設定変更                             |
| `chore`    | メンテナンス/その他                     |
| `revert`   | コミットの取り消し                      |

## 破壊的変更

```
# type/scope の後に感嘆符
feat!: 非推奨エンドポイントを削除

# BREAKING CHANGE フッター
feat: 設定が他の設定を拡張できるようにする

BREAKING CHANGE: `extends` キーの動作が変更されました
```

## ワークフロー

### 1. Diff の分析

```bash
# ファイルがステージされている場合、ステージされた diff を使用
git diff --staged

# 何もステージされていない場合、作業ツリーの diff を使用
git diff

# ステータスも確認
git status --porcelain
```

### 2. ファイルのステージング（必要な場合）

何もステージされていない場合、または変更を異なる方法でグループ化したい場合：

```bash
# 特定のファイルをステージ
git add path/to/file1 path/to/file2

# パターンでステージ
git add *.test.*
git add src/components/*

# 対話的なステージング
git add -p
```

**決してシークレットをコミットしないでください**（.env、credentials.json、秘密鍵）。

### 3. コミットメッセージの生成

diff を分析して以下を決定します：

- **Type**: どのような種類の変更か？
- **Scope**: 影響を受ける領域/モジュールは？
- **Description**: 変更内容の1行要約（現在形、命令形、72文字未満）

### 4. コミットの実行

```bash
# 単一行
git commit -m "<type>[scope]: <description>"

# 本文/フッター付きの複数行
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<optional body>

<optional footer>
EOF
)"
```

## ベストプラクティス

- コミットごとに1つの論理的な変更
- 現在形を使用：「add」であって「added」ではない
- 命令形を使用：「fix bug」であって「fixes bug」ではない
- Issue の参照：`Closes #123`、`Refs #456`
- 説明は72文字以内に保つ

## Git 安全プロトコル

- 決して git config を更新しない
- 明示的な要求がない限り、破壊的コマンド（--force、hard reset）を実行しない
- ユーザーが要求しない限り、フック（--no-verify）をスキップしない
- 決して main/master に force push しない
- フックによりコミットが失敗した場合、修正して新しいコミットを作成する（amend しない）
