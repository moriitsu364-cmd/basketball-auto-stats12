# 🏀 筑波バスケットボール統計システム
## Tsukuba Basketball Statistics System

NBA.comとBリーグのデザインを融合したプロフェッショナルなバスケットボール統計管理システム

---

## 🎯 主な機能

### 1. **NBA風デザイン**
- NBA.com/Bリーグ風のモダンなUI
- 日本語・英語バイリンガル対応
- レスポンシブデザイン
- プロフェッショナルなカラースキーム（筑波ブルー #1d428a & レッド #c8102e）

### 2. **新機能**

#### データ管理
- ✅ クォーター数対応（4Q公式戦/2Q練習試合）
- ✅ シーズン別データ管理
- ✅ 対戦相手統計分析
- ✅ 詳細な試合履歴

#### チーム情報
- ✅ 選手プロフィール（画像・ポジション・身体情報）
- ✅ スタッフ情報管理
- ✅ シーズン別チーム情報

#### データ比較
- ✅ 複数選手比較（2-5人）
- ✅ レーダーチャート
- ✅ シーズン間比較
- ✅ チーム戦績比較（4Q vs 2Q）

#### グラフ改善
- ✅ 棒グラフ（見やすいデザイン）
- ✅ 円グラフ（貢献度表示）
- ✅ 折れ線グラフ（推移分析）
- ✅ レーダーチャート（能力比較）

### 3. **セキュリティ強化**
- ✅ 2段階権限（エディター/管理者）
- ✅ 画像アップロード認証
- ✅ データ管理権限制御

---

## 📦 必要なパッケージ

```bash
pip install streamlit
pip install google-generativeai
pip install pillow
pip install pandas
pip install plotly
```

---

## ⚙️ セットアップ

### 1. secrets.toml の設定

`.streamlit/secrets.toml` ファイルを作成:

```toml
# Gemini API Key (必須)
GEMINI_API_KEY = "your-gemini-api-key-here"

# パスワード設定（オプション）
# エディター権限（データ入力可能）
EDITOR_PASSWORD_HASH = "ハッシュ値"  # デフォルト: tsukuba1872

# 管理者権限（全機能利用可能）
ADMIN_PASSWORD_HASH = "ハッシュ値"  # デフォルト: admin2024
```

### 2. パスワードハッシュの生成

```python
import hashlib

# エディター用
password = "your-editor-password"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(f"EDITOR_PASSWORD_HASH = \"{hash_value}\"")

# 管理者用
admin_password = "your-admin-password"
admin_hash = hashlib.sha256(admin_password.encode()).hexdigest()
print(f"ADMIN_PASSWORD_HASH = \"{admin_hash}\"")
```

### 3. アプリケーション起動

```bash
streamlit run basketball_stats_complete.py
```

---

## 📊 データ構造

### スコアシートデータ (basketball_stats.csv)
```csv
No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,
OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN,
GameDate,Season,Opponent,TeamScore,OpponentScore,QuarterType
```

### 選手情報 (player_info.json)
```json
{
  "選手名": {
    "name_en": "PLAYER NAME",
    "position": "PG",
    "height": "180",
    "weight": "70",
    "image": "base64_encoded_image"
  }
}
```

### チーム情報 (team_info.json)
```json
{
  "2024-25": {
    "description": "シーズン概要",
    "achievements": ["大会名"]
  }
}
```

---

## 🎨 カスタマイズ

### カラースキーム変更

CSSセクションで以下の値を変更:

```css
/* メインカラー */
--primary-color: #1d428a;  /* 筑波ブルー */
--secondary-color: #c8102e; /* 筑波レッド */

/* アクセントカラー */
--accent-blue: #2563eb;
--accent-red: #dc2626;
```

### チーム名変更

ヘッダー部分を編集:

```python
st.markdown("""
<div class="nba-header">
    <h1>🏀 あなたのチーム名</h1>
    <p class="subtitle">Your Team Name</p>
</div>
""", unsafe_allow_html=True)
```

---

## 🔐 権限レベル

### エディター (Editor)
- データ入力
- 試合記録追加
- データエクスポート/インポート
- 個別試合削除

### 管理者 (Admin)
- エディター権限 + 以下
- 選手情報編集（画像アップロード含む）
- スタッフ情報管理
- システム設定変更

---

## 📱 使い方

### 1. シーズン統計
- シーズン選択
- 試合形式フィルター（4Q/2Q）
- リーダーボード表示
- チーム統計グラフ

### 2. 選手統計
- 選手選択
- シーズンフィルター
- 個人成績表示
- パフォーマンスグラフ

### 3. 試合統計
- 試合選択
- ボックススコア
- 貢献度分析
- チーム統計

### 4. データ比較
- **選手比較**: 2-5人の選手を比較
- **シーズン比較**: 複数シーズンの成績比較
- **チーム比較**: 4Q vs 2Q戦績分析

### 5. チーム紹介
- 選手一覧（画像付き）
- スタッフ情報
- シーズン情報

### 6. 対戦相手分析
- 相手別戦績
- 対戦履歴
- 得点推移

### 7. データ入力
- AI画像解析（Gemini使用）
- 手動データ編集
- CSVインポート/エクスポート

---

## 🖼️ 画像管理

### 推奨画像サイズ

- **選手画像**: 800x800px (正方形)
- **スタッフ画像**: 600x600px (正方形)
- **ランキングアイコン**: 200x200px (正方形)

### 画像形式
- PNG (推奨・透過対応)
- JPEG
- WebP

---

## 🚀 パフォーマンス最適化

### データ量が多い場合

```python
# データフィルタリング
@st.cache_data
def load_filtered_data(season, quarter_type):
    df = pd.read_csv(DATA_FILE)
    if season != "All":
        df = df[df['Season'] == season]
    if quarter_type != "All":
        df = df[df['QuarterType'] == quarter_type]
    return df
```

### 画像圧縮

```python
from PIL import Image

def compress_image(image_file, max_size=(800, 800)):
    img = Image.open(image_file)
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    return img
```

---

## 📝 データバックアップ

### 自動バックアップ（推奨）

```python
import shutil
from datetime import datetime

def backup_data():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy('basketball_stats.csv', f'backup/stats_{timestamp}.csv')
    shutil.copy('player_info.json', f'backup/player_{timestamp}.json')
```

---

## 🐛 トラブルシューティング

### よくある問題

**Q: Gemini APIエラーが出る**
```
A: secrets.tomlにGEMINI_API_KEYが正しく設定されているか確認
```

**Q: 画像が表示されない**
```
A: Base64エンコードが正しいか、画像サイズが大きすぎないか確認
```

**Q: データが保存されない**
```
A: ファイル書き込み権限があるか確認
```

**Q: パスワードが合わない**
```
A: ハッシュ値を再生成し、secrets.tomlを更新
```

---

## 📄 ライセンス

このプロジェクトは教育目的で作成されています。

---

## 🙏 謝辞

- NBA.com - デザインインスピレーション
- Bリーグ - UIレイアウト参考
- Streamlit - フレームワーク
- Google Gemini - AI画像解析

---

## 📞 サポート

問題が発生した場合は、以下を確認してください:

1. Streamlitバージョン: `streamlit --version`
2. Pythonバージョン: `python --version`
3. エラーログの確認
4. secrets.toml設定の確認

---

**開発者**: Claude AI Assistant  
**バージョン**: 2.0 Pro  
**最終更新**: 2024年

🏀 Let's Go Tsukuba! 🏀
