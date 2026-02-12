import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="バスケ解析", layout="wide")
st.title("🏀 バスケスコア自動解析")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 2026年現在、最も安定しているモデル名に固定
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="解析対象", use_container_width=True)

            if st.button("AI解析を実行"):
                with st.spinner("AIが解析中..."):
                    prompt = "Extract basketball stats (Player Name, Points, AS, REB) from this image and show as a table in Japanese."
                    response = model.generate_content([prompt, image])
                    st.subheader("解析結果")
                    st.write(response.text)
                    st.success("解析成功！")
    except Exception as e:
        st.error(f"エラー: {e}")
else:
    st.error("Secretsにキーが設定されていません。")
