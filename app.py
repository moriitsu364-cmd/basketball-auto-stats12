import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="バスケ解析(最新2.0版)", layout="wide")
st.title("🏀 バスケスコア解析 (最新AI搭載)")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # 2026年最新の 2.0 モデルを指定
    # もしこれでも404なら 'gemini-1.5-flash-8b' に変更してください
    model_name = 'gemini-2.0-flash-exp' 
    
    try:
        model = genai.GenerativeModel(model_name)
        
        uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="解析対象画像", use_container_width=True)

            if st.button("最新AIで解析開始"):
                with st.spinner(f"最新モデル {model_name} で解析中..."):
                    prompt = "このバスケのスコアシートを解析し、選手ごとの得点、アシスト、リバウンドを抽出して日本語の表にしてください。"
                    # 画像解析の実行
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("解析結果")
                    st.markdown(response.text)
                    st.success("最新AIによる解析が完了しました！")
                    
    except Exception as e:
        st.error(f"モデル起動エラー: {e}")
        st.info("※このエラーが出る場合は、モデル名を 'gemini-1.5-flash-8b' に書き換えてください。")
else:
    st.error("APIキーが設定されていません。")
