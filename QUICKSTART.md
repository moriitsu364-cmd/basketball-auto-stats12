# 🚀 クイックセットアップガイド

## 最速で起動する方法

### 1. ファイルをダウンロード
すべてのファイルをダウンロードして、プロジェクトフォルダに配置してください。

### 2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### 3. シークレット設定（必須）
```bash
# .streamlitディレクトリが既にあります
# secrets.toml.exampleをコピーしてsecretsファイルを作成
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml`を編集：
```toml
GEMINI_API_KEY = "ここにGemini APIキーを入力"
```

### 4. 起動
```bash
streamlit run src/app.py
```

## 📝 重要なポイント

### Gemini APIキーの取得
1. https://makersuite.google.com/app/apikey にアクセス
2. 「Create API key」をクリック
3. 生成されたキーを`.streamlit/secrets.toml`に貼り付け

### デフォルト管理者パスワード
- パスワード: `tsukuba1872`
- DATA INPUTタブで入力が必要です

### ディレクトリ構成
```
basketball-auto-stats12/
├── .streamlit/          # Streamlit設定（必須）
│   ├── config.toml
│   └── secrets.toml     # 自分で作成
├── src/                 # ソースコード
│   ├── pages/
│   └── ...
├── data/                # データ保存先
└── requirements.txt
```

## ⚠️ トラブルシューティング

### Gemini APIエラーが出る
→ `.streamlit/secrets.toml`が正しく設定されているか確認

### データが保存されない
→ `data/`ディレクトリが存在するか確認

### モジュールが見つからない
→ `pip install -r requirements.txt`を実行

## 🎯 次のステップ

1. アプリを起動
2. DATA INPUTタブで試合データを入力
3. 他のタブで統計を確認

詳細は`README.md`を参照してください。
