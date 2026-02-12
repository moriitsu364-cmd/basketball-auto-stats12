# 🏀 Tsukuba Basketball Stats

筑波大学附属高校 男子バスケットボール統計システム

NBA.comスタイルの洗練されたUIで、試合統計を管理・分析するWebアプリケーションです。

## ✨ 機能

### 📊 統計分析
- **シーズン統計**: チーム全体のパフォーマンス、勝敗記録、平均得点
- **選手統計**: 個人のシーズン平均、パフォーマンスグラフ、ゲームログ
- **試合統計**: 試合ごとのボックススコア、チーム統計
- **選手比較**: 2選手間の詳細な統計比較

### 🤖 AI機能
- Gemini AIによるスコアシート画像の自動読み取り
- CSV形式でのデータ自動抽出

### 📈 可視化
- Plotlyによるインタラクティブなグラフ
- リーダーボード（得点王、リバウンド王、アシスト王）
- パフォーマンストレンド分析

## 🚀 セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/moriitsu364-cmd/basketball-auto-stats12.git
cd basketball-auto-stats12
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. シークレット設定

```bash
# .streamlitディレクトリを作成（存在しない場合）
mkdir -p .streamlit

# secrets.tomlを作成
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml`を編集してAPIキーを設定：

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
ADMIN_PASSWORD_HASH = "your-password-hash"
```

### 4. dataディレクトリを作成

```bash
mkdir -p data
touch data/.gitkeep
```

### 5. アプリを起動

```bash
streamlit run src/app.py
```

ブラウザで `http://localhost:8501` にアクセス

## 📁 プロジェクト構造

```
basketball-auto-stats12/
├── .streamlit/
│   ├── config.toml              # Streamlit設定
│   └── secrets.toml.example     # シークレット設定例
├── src/
│   ├── pages/                   # 各タブのページ
│   │   ├── __init__.py
│   │   ├── season_stats.py     # シーズン統計
│   │   ├── player_stats.py     # 選手統計
│   │   ├── game_stats.py       # 試合統計
│   │   ├── compare.py          # 選手比較
│   │   └── data_input.py       # データ入力
│   ├── app.py                   # メインアプリ
│   ├── config.py                # 設定定数
│   ├── database.py              # データベース操作
│   ├── stats.py                 # 統計計算
│   ├── charts.py                # グラフ作成
│   ├── components.py            # UIコンポーネント
│   ├── auth.py                  # 認証
│   ├── ai.py                    # AI機能
│   └── styles.py                # CSSスタイル
├── data/
│   ├── .gitkeep
│   └── basketball_stats.csv     # 統計データ（自動生成）
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔑 環境変数

### Gemini APIキー

1. [Google AI Studio](https://makersuite.google.com/app/apikey)でAPIキーを取得
2. `.streamlit/secrets.toml`に設定

```toml
GEMINI_API_KEY = "your-api-key"
```

### 管理者パスワード

デフォルトパスワード: `tsukuba1872`

カスタムパスワードを設定する場合：

```bash
# パスワードのハッシュを生成
python -c "import hashlib; print(hashlib.sha256('your-password'.encode()).hexdigest())"
```

生成されたハッシュを`secrets.toml`に設定：

```toml
ADMIN_PASSWORD_HASH = "generated-hash"
```

## 📖 使い方

### データ入力

1. **DATA INPUT**タブに移動
2. 管理者パスワードを入力（デフォルト: `tsukuba1872`）
3. 試合情報を入力（日付、シーズン、対戦相手、スコア）
4. スコアシート画像をアップロード
5. **ANALYZE WITH AI**をクリック
6. 抽出されたデータを確認・編集
7. **SAVE DATA**をクリック

### 統計の閲覧

- **SEASON STATS**: シーズンを選択して全体統計を表示
- **PLAYER STATS**: 選手を選択して個人統計を表示
- **GAME STATS**: 試合を選択してボックススコアを表示
- **COMPARE**: 2選手を選択して比較

### データのエクスポート/インポート

- **エクスポート**: DATA INPUTタブの「DOWNLOAD ALL DATA」
- **インポート**: DATA INPUTタブでCSVファイルをアップロード

## 🎨 デザイン

- NBA.com風の洗練されたUI
- レスポンシブデザイン対応
- インタラクティブなグラフとチャート
- 直感的なナビゲーション

## 🛠️ 技術スタック

- **フレームワーク**: Streamlit
- **AI**: Google Gemini API
- **データ処理**: Pandas
- **可視化**: Plotly
- **画像処理**: Pillow

## 📝 データ形式

CSVファイルには以下のカラムが含まれます：

```
No, PlayerName, GS, PTS, 3PM, 3PA, 3P%, 2PM, 2PA, 2P%, DK, 
FTM, FTA, FT%, OR, DR, TOT, AST, STL, BLK, TO, PF, TF, OF, 
FO, DQ, MIN, GameDate, Season, Opponent, TeamScore, OpponentScore
```

## 🤝 貢献

プルリクエストを歓迎します！大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## 📄 ライセンス

MIT

## 👨‍💻 作者

- GitHub: [@moriitsu364-cmd](https://github.com/moriitsu364-cmd)

## 🙏 謝辞

- デザインインスピレーション: NBA.com
- AI技術: Google Gemini API
- フレームワーク: Streamlit

---

**質問や問題がある場合は、[Issues](https://github.com/moriitsu364-cmd/basketball-auto-stats12/issues)を開いてください。**
