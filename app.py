import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="バスケ解析(決定版)", layout="wide")
st.title("🏀 バスケスコア自動解析")

# Secretsの確認
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # 404対策：複数のモデル候補を順に試す
    # 2026年現在、最も通りやすい名前のリストです
    model_candidates = [
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash', 
        'gemini-2.0-flash-exp'
    ]

    uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="解析対象", use_container_width=True)

        if st.button("AI解析を実行"):
            success = False
            for model_name in model_candidates:
                try:
                    with st.spinner(f"モデル {model_name} で試行中..."):
                        model = genai.GenerativeModel(model_name)
                        prompt = "画像からバスケのスタッツ（選手名、得点、AS、REB）を抽出し、表形式で出力してください。"
                        response = model.generate_content([prompt, image])
                        
                        st.subheader("解析結果")
                        st.write(response.text)
                        st.success(f"成功モデル: {model_name}")
                        success = True
                        break # 成功したらループを抜ける
                except Exception as e:
                    continue # ダメなら次のモデルへ
            
            if not success:
                st.error("現在、お使いのAPIキーで利用可能なモデルが見つかりませんでした。")
                st.info("Google AI Studioで新しいAPIキーを作成し直すと解決する場合があります。")
else:
    st.error("Streamlit Secretsに 'GEMINI_API_KEY' が設定されていません。")
