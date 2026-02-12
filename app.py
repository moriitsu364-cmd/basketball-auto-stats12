import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="バスケ解析", layout="wide")
st.title("🏀 バスケスコア自動解析")

# キーの読み込み
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 404が出にくい「最新のフルネーム」で指定
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

        uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="解析対象", use_container_width=True)

            if st.button("AI解析を実行"):
                with st.spinner("AIが読み取り中..."):
                    # シンプルな英語指示の方が通る場合があります
                    prompt = "Extract basketball stats (Player Name, Points, AS, REB) from this image. Show as a table."
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("解析結果")
                    st.markdown(response.text)
                    st.success("成功しました！")
    except Exception as e:
        # エラーメッセージをさらに詳しく表示
        st.error(f"詳細エラー: {e}")
else:
    st.error("Secretsに 'GEMINI_API_KEY' が見つかりません。")
