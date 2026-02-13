# 🏀 Tsukuba Basketball Stats - Advanced Analytics Platform

筑波大学附属高校 男子バスケットボール統計システム

NBA.com + Bリーグ風の洗練されたダークテーマUIで、試合統計を管理・分析する高度なWebアプリケーションです。

## ✨ 主な機能

### 📊 統計分析（7つの分析ページ）
1. **シーズン統計**: チーム全体のパフォーマンス、勝敗記録、リーダーボード
2. **選手統計**: 個人のシーズン平均、パフォーマンスグラフ、背景画像付き選手カード
3. **試合統計**: 試合ごとのボックススコア、チーム統計
4. **データ比較**: 
   - 複数選手比較（2-4人同時比較）
   - シーズン間比較
   - レーダーチャート、折れ線グラフ、棒グラフ
5. **チーム情報**: シーズン別チーム情報、コーチ・マネージャー紹介（写真付き）
6. **対戦相手統計**: シーズン別対戦相手分析、対戦成績、平均スタッツ
7. **管理者設定**: 画像管理、セキュリティ設定、システム統括

### 🎨 デザイン特徴
- **NBA.com + Bリーグ風**: ダークテーマ、グラデーション、アニメーション
- **バイリンガル対応**: 英語・日本語併記
- **半透明背景画像**: 選手カードに格好良い背景画像
- **小アイコン**: ランキングに選手写真表示
- **多様なグラフ**: 折れ線、棒、円、レーダーチャート

### 🤖 AI機能
- Gemini AIによるスコアシート画像の自動読み取り
- CSV形式でのデータ自動抽出

### 🎮 試合形式対応
- 4クォーター制
- 2クォーター制（練習試合）
- その他の形式

### 🔒 セキュリティ
- 強化された管理者認証システム
- ログイン試行回数制限（5回）
- 自動ロックアウト（15分）
- セッションタイムアウト（1時間）
- 画像アップロードも管理者権限必要

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

### 3. ディレクトリ構造を作成

```bash
mkdir -p data/images/players
mkdir -p data/images/staff
```

### 4. シークレット設定

```bash
# secrets.tomlを作成
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

`.streamlit/secrets.toml`を編集：

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
ADMIN_PASSWORD_HASH = "your-password-hash"
```

### 5. アプリを起動

```bash
streamlit run src/app_new.py
```

ブラウザで `http://localhost:8501` にアクセス

## 📁 プロジェクト構造

```
basketball-auto-stats12/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
├── src/
│   ├── pages/
│   │   ├── season_stats.py       # シーズン統計
│   │   ├── player_stats.py       # 選手統計
│   │   ├── game_stats.py         # 試合統計
│   │   ├── compare_new.py        # 比較（複数選手対応）
│   │   ├── team_info.py          # チーム情報
│   │   ├── opponent_stats.py     # 対戦相手統計
│   │   ├── data_input.py         # データ入力
│   │   └── admin_settings.py     # 管理者設定
│   ├── app_new.py                # メインアプリ
│   ├── config.py                 # 設定
│   ├── database.py               # DB操作
│   ├── stats.py                  # 統計計算
│   ├── charts_new.py             # グラフ（棒・円・レーダー）
│   ├── components_new.py         # UIコンポーネント
│   ├── auth.py                   # 認証
│   ├── ai.py                     # AI機能
│   └── styles_new.py             # NBA風CSS
├── data/
│   ├── images/
│   │   ├── players/              # 選手画像
│   │   └── staff/                # スタッフ画像
│   ├── basketball_stats.csv
│   ├── team_info.csv
│   └── opponent_stats.csv
├── requirements.txt
└── README.md
```

## 🎨 画像アップロード方法

### 選手画像
1. **管理者設定**タブに移動
2. 管理者パスワードでログイン
3. **画像管理** → **選手画像**タブ
4. 選手名を入力し、画像をアップロード
5. 背景透過PNG推奨（格好良く表示されます）

### スタッフ画像
1. **管理者設定**タブ → **画像管理** → **スタッフ画像**
2. スタッフ名・役職を入力し、画像をアップロード

### 画像の表示場所
- **選手カード**: 背景に半透明で大きく表示
- **ランキング**: 小さいアイコンとして表示
- **スタッフ紹介**: カード形式で表示

## 📊 データ入力方法

### 通常の試合データ
1. **DATA INPUT**タブに移動
2. 試合情報を入力：
   - 試合日
   - シーズン
   - 対戦相手
   - スコア
   - **試合形式**（4Q / 2Q / その他）← NEW!
3. スコアシート画像をアップロード
4. **ANALYZE WITH AI**をクリック
5. データを確認・編集
6. **SAVE DATA**

### チーム情報の入力
1. **TEAM INFO**タブに移動
2. シーズンを選択
3. チーム情報を入力/編集：
   - ヘッドコーチ
   - アシスタントコーチ
   - マネージャー
   - ホーム体育館
   - チームモットー
   - シーズン目標

## 📈 比較機能の使い方

### 複数選手比較（2-4人）
1. **COMPARE**タブ → **選手間比較**
2. 最大4人の選手を選択
3. グラフタイプを選択：
   - 折れ線グラフ（推移）
   - レーダーチャート（総合比較）
   - 棒グラフ（項目別）

### シーズン比較
1. **COMPARE**タブ → **シーズン比較**
2. 2つのシーズンを選択
3. チーム統計を比較

## 🔐 セキュリティ設定

### デフォルトパスワード
- パスワード: `tsukuba1872`

### カスタムパスワードの設定
```bash
# パスワードのハッシュを生成
python -c "import hashlib; print(hashlib.sha256('your-password'.encode()).hexdigest())"
```

生成されたハッシュを`.streamlit/secrets.toml`に設定

### セキュリティ機能
- 最大ログイン試行: 5回
- ロックアウト時間: 15分
- セッションタイムアウト: 1時間

## 🎯 新機能

### v2.0で追加された機能
✅ **NBA.com + Bリーグ風デザイン**
✅ **バイリンガル対応**（英語・日本語）
✅ **選手・スタッフ画像対応**
✅ **チーム情報ページ**
✅ **対戦相手統計ページ**
✅ **複数選手比較**（2-4人）
✅ **試合形式対応**（4Q/2Q/その他）
✅ **改良されたグラフ**（棒・円・レーダー）
✅ **強化されたセキュリティ**
✅ **管理者統括設定**

## 🛠️ 技術スタック

- **フレームワーク**: Streamlit
- **AI**: Google Gemini API
- **データ処理**: Pandas
- **可視化**: Plotly
- **画像処理**: Pillow, Base64
- **認証**: hashlib, session management

## 📝 ライセンス

MIT

## 👨‍💻 作者

- GitHub: [@moriitsu364-cmd](https://github.com/moriitsu364-cmd)

## 🙏 デザインインスピレーション

- NBA.com - スタッツページデザイン
- Bリーグ公式サイト - バイリンガル対応

---

**質問や問題がある場合は、[Issues](https://github.com/moriitsu364-cmd/basketball-auto-stats12/issues)を開いてください。**
