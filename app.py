import streamlit as st
import google.generativeai as genai
from PIL import Image

# ページ設定
st.set_page_config(page_title="バスケスタッツ解析", layout="wide")
st.title("🏀 バスケスコア自動解析 (Gemini直結版)")

# 1. ここでSecretsからキーを読み込んでいます
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    # 2. Google専用の設定
    genai.configure(api_key=api_key)
    
    # 3. 今、最も確実に動くモデル名
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("スコアシートの写真をアップロード", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="解析する画像", use_container_width=True)

        if st.button("AI解析を実行"):
            with st.spinner("AIが画像の内容を読み取っています..."):
                try:
                    # 指示（プロンプト）
                    prompt = "画像からバスケのスタッツ（選手名、得点、AS、REB）を抽出し、表形式で出力してください。"
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("解析結果")
                    st.write(response.text)
                    st.success("成功しました！")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
else:
    st.warning("StreamlitのSecretsに 'GEMINI_API_KEY' を設定してください。設定しないとAIは動きません。")
