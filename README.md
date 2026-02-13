# Instapaper Bookmark Organizer

Instapaperの未読ブックマークを効率的に整理するためのCLIツールです。ドメインベースのルール学習機能により、ブックマークを自動的に適切なフォルダに振り分けることができます。

## 特徴

- 🔐 **セキュアな認証**: xAuth方式で初回のみ認証、以降はトークンを安全に保存
- 🤖 **自動振り分け**: ドメインベースのルールで自動的にフォルダへ移動
- 📚 **ルール学習**: 手動で振り分けたドメインを自動的に記憶
- ⌨️ **シンプルなUI**: キーボードだけで素早く操作可能

## インストール

### 必要要件

- Python 3.7以上
- Instapaper アカウント
- Instapaper API キー（Consumer Key/Secret）

### uvのインストール

まず、uvをインストールします：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

またはHomebrewを使用：

```bash
brew install uv
```

### 依存パッケージのインストール

```bash
uv sync
```

## セットアップ

### 1. Instapaper API キーの取得

1. [Instapaper API](https://www.instapaper.com/api) にアクセス
2. Consumer Key と Consumer Secret を取得

### 2. 環境変数の設定

**必須（常に必要）:**
```bash
export INSTAPAPER_CONSUMER_KEY="your_consumer_key"
export INSTAPAPER_CONSUMER_SECRET="your_consumer_secret"
```

**初回実行時のみ必要:**
```bash
export INSTAPAPER_USERNAME="your_email@example.com"
export INSTAPAPER_PASSWORD="your_password"
```

> 💡 初回実行後は認証トークンが `~/.config/instapaper-cli/credentials.json` に保存されるため、ユーザー名とパスワードは不要になります。

### 3. Instapaperでフォルダを作成

ツールを使用する前に、Instapaperのウェブサイトまたはアプリで整理用のフォルダを作成してください。

## 使い方

### 基本的な使い方

```bash
uv run python main.py
```

または、インストール済みのスクリプトとして：

```bash
uv run instapaper-organize
```

### 操作方法

ツールを起動すると、未読ブックマークが1件ずつ表示されます：

```
Folders (1..9):
  1: Tech (id=123456)
  2: News (id=234567)
  3: Blog (id=345678)

Controls: [1-9]=move  [a]=auto(move by rule)  [s]=save rule for domain  [n]=skip  [q]=quit

[12345] Example Article Title
  example.com
  suggestion: Tech
>
```

#### コマンド一覧

| キー | 動作 |
|------|------|
| `1-9` | 対応する番号のフォルダに移動 |
| `a` | ルールに基づいて自動移動（ルールがある場合） |
| `s` | 現在のドメインに対してフォルダルールを保存 |
| `n` | スキップ（次のブックマークへ） |
| `q` | 終了 |

### ルールの仕組み

- **自動学習**: 数字キー（1-9）でフォルダに移動すると、そのドメインが自動的に記憶されます
- **明示的な保存**: `s` キーで特定のドメインとフォルダの組み合わせを保存できます
- **サブドメイン対応**: `.example.com` のようなルールで、すべてのサブドメインに対応できます
- **ルール保存場所**: `~/.config/instapaper-cli/rules.json`

## ファイル構成

```
~/.config/instapaper-cli/
├── credentials.json  # 認証トークン（パーミッション: 600）
└── rules.json        # ドメイン振り分けルール
```

## トラブルシューティング

### 認証エラーが発生する

- Consumer Key/Secret が正しいか確認してください
- 初回実行時は `INSTAPAPER_USERNAME` と `INSTAPAPER_PASSWORD` が設定されているか確認してください
- `~/.config/instapaper-cli/credentials.json` を削除して再認証してみてください

### フォルダが表示されない

- Instapaperのウェブサイトまたはアプリで、少なくとも1つのフォルダを作成してください

### API レート制限

- ツールには自動リトライ機能（指数バックオフ）が組み込まれています
- エラーが続く場合は、しばらく待ってから再実行してください

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 貢献

プルリクエストや Issue の報告を歓迎します！

## API ドキュメント

- [Instapaper API Documentation](https://www.instapaper.com/api)
