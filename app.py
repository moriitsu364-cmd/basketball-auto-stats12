import streamlit as st
import google.generativeai as genai
from PIL import Image

# ページの設定
st.set_page_config(page_title="バスケ解析(確定版)", layout="wide")
st.title("🏀 バスケスコア解析 (最新Gemini版)")

# SecretsからAPIキーを取得
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    # APIの設定
    genai.configure(api_key=api_key)
    
    # 【重要】2026年現在の最新・安定モデル名を使用
    # もし404が出る場合は 'gemini-1.5-flash' に戻してください
    model = genai.GenerativeModel('gemini-2.0-flash')

    uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロード画像", use_container_width=True)

        if st.button("AIで解析開始"):
            with st.spinner("AIが読み取り中..."):
                try:
                    # 指示出し（プロンプト）
                    prompt = """
                    このバスケのスコアシートから以下の項目を抽出して、表形式で見せてください。
                    - 選手名 (Player Name)
                    - 得点 (Points)
                    - アシスト (AS)
                    - リバウンド (REB)
                    """
                    
                    # AIに画像と文字を渡す
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("解析結果")
                    st.write(response.text)
                    st.success("解析が完了しました！")
                except Exception as e:
                    st.error(f"解析エラー: {e}")
                    st.info("※モデル名が古い可能性があります。管理者に確認してください。")
else:
    st.error("StreamlitのSecretsに 'GEMINI_API_KEY' が設定されていません。")
