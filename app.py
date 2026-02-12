import streamlit as st
import pandas as pd
from groq import Groq
from PIL import Image
import io
import base64
import json

# ページ設定
st.set_page_config(page_title="バスケスタッツ自動記録(Groq)", layout="wide")
st.title("🏀 バスケスコア解析 (Groq無料版)")

# SecretsからAPIキーを取得
api_key = st.secrets.get("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
    
    uploaded_file = st.file_uploader("スコアシートの画像をアップロード", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロード画像", use_container_width=True)
        
        if st.button("AIで高速解析開始"):
            with st.spinner("Groq AIが爆速で読み取り中..."):
                # 画像をBase64に変換
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                try:
                    # GroqのVisionモデル（Llama 3.2）を使用
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Extract basketball stats (Player Name, Points, AS, REB) from this score sheet. Return ONLY a JSON array: [{\"選手名\": \"name\", \"得点\": 0, \"AS\": 0, \"REB\": 0}]"},
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                    },
                                ],
                            }
                        ],
                        model="llama-3.2-11b-vision",
                        response_format={"type": "json_object"}
                    )
                    
                    # 結果をパース
                    raw_res = chat_completion.choices[0].message.content
                    res_json = json.loads(raw_res)
                    
                    # JSONの構造によって柔軟に対応
                    if isinstance(res_json, dict) and "stats" in res_json:
                        st.session_state['data'] = res_json["stats"]
                    elif isinstance(res_json, dict):
                        # 辞書の中身がリストならそれを使う
                        key = list(res_json.keys())[0]
                        st.session_state['data'] = res_json[key]
                    else:
                        st.session_state['data'] = res_json

                except Exception as e:
                    st.error(f"解析エラー: {e}")

    # 編集エリア
    if 'data' in st.session_state:
        st.subheader("スタッツの修正・確定")
        df = pd.DataFrame(st.session_state['data'])
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("CSVで保存"):
            csv = edited_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("ダウンロード", csv, "stats_groq.csv", "text/csv")
else:
    st.warning("StreamlitのSecretsに 'GROQ_API_KEY' を設定してください。")
