import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="バスケ解析", layout="wide")
st.title("🏀 バスケスコア自動解析")

# Secretsから取得
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 【修正ポイント】
        # 一部の環境で models/ をつけると404になるため、名前だけで指定します
        # また、最新の安定版である 'gemini-1.5-flash' を使用します
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="解析対象", use_container_width=True)

            if st.button("AI解析を実行"):
                with st.spinner("AIが画像の内容を読み取っています..."):
                    # プロンプト（指示）
                    prompt = "この画像からバスケのスタッツを読み取り、選手名、得点、アシスト、リバウンドを日本語の表形式で出力してください。"
                    
                    # 実行
                    response = model.generate_content([prompt, image])
                    
                    st.subheader("解析結果")
                    st.markdown(response.text)
                    st.success("解析に成功しました！")
                    
    except Exception as e:
        # エラーが出た場合、詳細を表示して原因を特定しやすくします
        st.error(f"エラーが発生しました: {e}")
        st.info("もし404が出る場合は、APIキーが『Google AI Studio』で作られたものか再確認してください。")
else:
    st.error("StreamlitのSecretsに 'GEMINI_API_KEY' が設定されていません。")
