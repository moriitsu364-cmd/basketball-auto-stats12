import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="バスケ解析(確定版)", layout="wide")
st.title("🏀 バスケスコア解析 (Gemini無料版)")

# SecretsからAPIキーを取得
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash') # 爆速で画像が読めるモデル

    uploaded_file = st.file_uploader("スコアシート画像をアップ", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="解析対象", use_container_width=True)

        if st.button("AIで解析開始"):
            with st.spinner("AIが画像を見ています..."):
                try:
                    # AIへの指示
                    prompt = "Extract basketball stats (Player Name, Points, Assists, Rebounds) from this image. Return a table-like text."
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("解析結果")
                    st.write(response.text)
                    st.success("解析完了！")
                except Exception as e:
                    st.error(f"エラー: {e}")
else:
    st.warning("Streamlit Secretsに 'GEMINI_API_KEY' を設定してください。")
