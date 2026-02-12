import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io

# ページ設定
st.set_page_config(page_title="バスケスタッツ自動記録", layout="wide")
st.title("🏀 バスケスコアシート解析・記録システム")

# サイドバーでAPIキーを設定（StreamlitのSecretsから取得、なければ入力）
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("Google API Keyを入力してください", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # 無料枠で高速なモデル
else:
    st.warning("Google API Keyを設定してください。")

# 画像アップロード
uploaded_file = st.file_uploader("スコアシートの画像をアップロードしてください", type=['png', 'jpg', 'jpeg'])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされたスコアシート", use_container_width=True)
    
    if st.button("画像を解析してスタッツを抽出"):
        with st.spinner("Geminiが画像を解析中..."):
            # 画像をバイトデータに変換
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_data = img_byte_arr.getvalue()

            prompt = """
            このバスケットボールのスコアシートから、選手ごとのスタッツを抽出して、
            以下の形式のJSONデータ（Markdownのコードブロックなし）で出力してください。
            [
              {"選手名": "名前1", "得点": 10, "AS": 2, "REB": 5, "ST": 1},
              {"選手名": "名前2", "得点": 5, "AS": 0, "REB": 3, "ST": 2}
            ]
            数値が不明な場合は0にしてください。
            """
            
            try:
                # Geminiで解析
                response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_data}])
                
                # テキストからJSON部分を抽出（簡易的な処理）
                import json
                text_response = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(text_response)
                
                st.session_state['stats_data'] = data
                st.success("解析が完了しました！内容を確認・修正してください。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# データ編集エリア
if 'stats_data' in st.session_state:
    st.subheader("スタッツの確認・修正")
    df = pd.DataFrame(st.session_state['stats_data'])
    
    # ユーザーが表を直接編集できる
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    if st.button("データを保存（CSVダウンロード）"):
        csv = edited_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("CSVファイルをダウンロード", csv, "stats.csv", "text/csv")
