import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ページ設定
st.set_page_config(page_title="バスケ解析", layout="wide")
st.title("🏀 バスケスコア自動解析")

# サイドバーに説明を追加
with st.sidebar:
    st.header("使い方")
    st.markdown("""
    1. バスケットボールのスコアシート画像をアップロード
    2. 「AI解析を実行」ボタンをクリック
    3. 選手名、得点、アシスト、リバウンドなどの統計データを取得
    """)
    st.info("💡 画像は鮮明で、文字がはっきり読める状態が理想的です")
    
    # 利用可能なモデル情報を表示（APIキー設定後）
    st.divider()

# APIキーの取得（複数の方法を試す）
api_key = None
try:
    # Streamlit Cloudの場合
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    # ローカル環境の場合、入力フォームを表示
    st.warning("⚠️ APIキーが設定されていません")
    api_key = st.text_input("Gemini APIキーを入力してください:", type="password")

if api_key:
    try:
        # API設定
        genai.configure(api_key=api_key)
        
        # 利用可能なモデルのリストを取得して、画像対応モデルを選択
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception as e:
            st.warning(f"モデルリストの取得に失敗: {e}")
        
        # 優先順位でモデルを選択
        model_name = None
        priority_models = [
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash-latest', 
            'models/gemini-1.5-flash',
            'models/gemini-pro-vision',
            'models/gemini-pro'
        ]
        
        for preferred in priority_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        if not model_name and available_models:
            # どれもマッチしない場合は最初の利用可能なモデルを使用
            model_name = available_models[0]
        
        if not model_name:
            st.error("利用可能なモデルが見つかりません")
            st.stop()
        
        st.sidebar.success(f"使用モデル: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # ファイルアップローダー
        uploaded_file = st.file_uploader(
            "スコアシート画像をアップロード", 
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="PNG, JPG, JPEG, WEBP形式の画像ファイルに対応"
        )
        
        if uploaded_file:
            # 画像を表示
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("📸 アップロードされた画像")
                st.image(image, caption="解析対象の画像", use_container_width=True)
            
            with col2:
                st.subheader("⚙️ 解析オプション")
                
                # 詳細度の選択
                detail_level = st.radio(
                    "解析の詳細度:",
                    ["基本統計のみ", "詳細統計", "フル解析（コメント付き）"],
                    help="詳細度を上げると、より多くの情報を抽出しますが時間がかかります"
                )
                
                # 言語選択
                output_lang = st.selectbox(
                    "出力言語:",
                    ["日本語", "English"],
                    help="解析結果の表示言語を選択"
                )
            
            # 解析ボタン
            if st.button("🚀 AI解析を実行", type="primary", use_container_width=True):
                with st.spinner("🤖 AIが画像を解析中... しばらくお待ちください"):
                    try:
                        # プロンプトの構築
                        if output_lang == "日本語":
                            if detail_level == "基本統計のみ":
                                prompt = """
この画像からバスケットボールの試合統計を抽出してください。
以下の情報を表形式で出力してください：
- 選手名
- 得点（Points）
- アシスト（Assists）
- リバウンド（Rebounds）

表はMarkdown形式で出力してください。
"""
                            elif detail_level == "詳細統計":
                                prompt = """
この画像からバスケットボールの詳細な試合統計を抽出してください。
以下の情報を表形式で出力してください：
- 選手名
- 得点（Points）
- フィールドゴール成功/試投（FG）
- 3ポイント成功/試投（3P）
- フリースロー成功/試投（FT）
- リバウンド（Rebounds）
- アシスト（Assists）
- スティール（Steals）
- ブロック（Blocks）
- ターンオーバー（Turnovers）

表はMarkdown形式で出力してください。
"""
                            else:  # フル解析
                                prompt = """
この画像からバスケットボールの試合統計を完全に解析してください。

1. チーム情報（チーム名、最終スコアなど）
2. 各選手の詳細統計（利用可能なすべてのデータ）
3. 試合の特徴的なポイントや注目選手のコメント

表はMarkdown形式で、見やすく整理して出力してください。
"""
                        else:  # English
                            if detail_level == "基本統計のみ":
                                prompt = """
Extract basketball game statistics from this image.
Please provide the following information in table format:
- Player Name
- Points
- Assists
- Rebounds

Output the table in Markdown format.
"""
                            elif detail_level == "詳細統計":
                                prompt = """
Extract detailed basketball game statistics from this image.
Please provide the following information in table format:
- Player Name
- Points
- Field Goals Made/Attempted (FG)
- 3-Pointers Made/Attempted (3P)
- Free Throws Made/Attempted (FT)
- Rebounds
- Assists
- Steals
- Blocks
- Turnovers

Output the table in Markdown format.
"""
                            else:  # Full analysis
                                prompt = """
Fully analyze the basketball game statistics from this image.

1. Team information (team names, final scores, etc.)
2. Detailed statistics for each player (all available data)
3. Notable points and player highlights

Output in well-organized Markdown format.
"""
                        
                        # 画像をバイト形式に変換
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format=image.format if image.format else 'PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        # API呼び出し
                        response = model.generate_content([prompt, image])
                        
                        # 結果の表示
                        st.divider()
                        st.subheader("📊 解析結果")
                        
                        if response.text:
                            st.markdown(response.text)
                            st.success("✅ 解析が完了しました！")
                            
                            # 結果をダウンロード可能にする
                            st.download_button(
                                label="📥 解析結果をダウンロード",
                                data=response.text,
                                file_name="basketball_stats_analysis.md",
                                mime="text/markdown"
                            )
                        else:
                            st.warning("⚠️ 解析結果が空です。画像を確認して再度お試しください。")
                        
                    except Exception as e:
                        st.error(f"❌ エラーが発生しました: {str(e)}")
                        st.info("""
**考えられる原因:**
- 画像が不鮮明で文字が読み取れない
- スコアシートの形式が特殊
- API通信エラー
- APIキーが無効

**対処法:**
- より鮮明な画像を使用する
- 画像の向きを確認する
- APIキーが正しいか確認する
- しばらく待ってから再試行する
                        """)
                        
                        # デバッグ情報
                        with st.expander("🔍 デバッグ情報"):
                            st.write(f"エラー詳細: {e}")
                            st.write(f"画像サイズ: {image.size}")
                            st.write(f"画像フォーマット: {image.format}")
                            st.write(f"使用モデル: {model_name if 'model_name' in locals() else '未設定'}")
                            if available_models:
                                st.write(f"利用可能なモデル: {', '.join(available_models[:5])}")
                            
    except Exception as e:
        st.error(f"❌ 初期化エラー: {str(e)}")
        st.info("APIキーが正しいか確認してください。Gemini APIキーは https://makersuite.google.com/app/apikey から取得できます。")
else:
    st.info("""
### 🔑 APIキーの設定方法

**Streamlit Cloudにデプロイする場合:**
1. Streamlit Cloudのダッシュボードにアクセス
2. アプリの設定 → Secrets
3. 以下の内容を追加:
```
GEMINI_API_KEY = "your-api-key-here"
```

**ローカルで実行する場合:**
1. `.streamlit/secrets.toml` ファイルを作成
2. 以下の内容を追加:
```
GEMINI_API_KEY = "your-api-key-here"
```

または、上記の入力欄にAPIキーを直接入力してください。

**APIキーの取得:** https://makersuite.google.com/app/apikey
    """)

# フッター
st.divider()
st.caption("🏀 バスケットボールスコア自動解析システム | Powered by Google Gemini AI")
