# 貢献ガイドライン

Instapaper Bookmark Organizer への貢献に興味を持っていただき、ありがとうございます！

## 貢献方法

### バグ報告

バグを見つけた場合は、以下の情報を含めて Issue を作成してください：

- 問題の簡潔な説明
- 再現手順
- 期待される動作
- 実際の動作
- 環境情報（Python バージョン、OS など）

### 機能リクエスト

新機能の提案は大歓迎です！Issue を作成して、以下を含めてください：

- 機能の説明
- ユースケース
- 可能であれば、実装のアイデア

### プルリクエスト

1. リポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

#### コーディング規約

- PEP 8 スタイルガイドに従ってください
- 型ヒントを使用してください（Python 3.7+）
- docstring を追加してください
- 既存のコードスタイルと一貫性を保ってください

#### コミットメッセージ

- 明確で簡潔なメッセージを書いてください
- 現在形を使用してください（"Add feature" not "Added feature"）
- 必要に応じて、詳細な説明を含めてください

## 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/instapaper-bookmark-organizer.git
cd instapaper-bookmark-organizer

# uvのインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係をインストール
uv sync

# 開発用の追加パッケージ（オプション）
uv add --dev black flake8 mypy pytest
```

## テスト

変更を加えた場合は、動作確認を行ってください：

```bash
# 基本的な動作確認
uv run python main.py

# コードスタイルチェック（オプション）
uv run flake8 main.py
uv run black --check main.py
uv run mypy main.py
```

## 質問

質問がある場合は、遠慮なく Issue を作成してください！

## 行動規範

- 敬意を持って接してください
- 建設的なフィードバックを提供してください
- オープンで包括的なコミュニティを維持しましょう

ご協力ありがとうございます！
