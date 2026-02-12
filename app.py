import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image
import io
import json

# ページ設定
st.set_page_config(page_title="バスケスタッツ自動記録", layout="wide")
st.title("🏀 バスケスコアシート解析システム")

# SecretsからAPIキーを取得
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 画像アップロード
    uploaded_file = st.file_uploader("スコアシートの画像をアップロード", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロード画像", use_container_width=True)
        
        if st.button("AIで解析開始"):
            with st.spinner("高精度AIが読み取り中..."):
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                
                prompt = """
                このバスケのスコアシートから選手名、得点、アシスト(AS)、リバウンド(REB)を抽出してください。
                以下のJSON形式のみで返してください。余計な説明は不要です。
                [{"選手名": "名前", "得点": 0, "AS": 0, "REB": 0}]
                """
                
                try:
                    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": img_byte_arr.getvalue()}])
                    # JSON部分だけを抽出
                    raw_text = response.text.strip().replace('```json', '').replace('```', '')
                    st.session_state['data'] = json.loads(raw_text)
                except Exception as e:
                    st.error(f"解析エラー: {e}")

    # 編集エリア
    if 'data' in st.session_state:
        st.subheader("スタッツの修正・確定")
        df = pd.DataFrame(st.session_state['data'])
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("CSVで保存"):
            csv = edited_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("ダウンロード", csv, "stats.csv", "text/csv")
else:
    st.error("StreamlitのSecretsに 'GOOGLE_API_KEY' が設定されていません。")
