import streamlit as st
import pandas as pd
import base64
from openai import OpenAI

# OpenAIの設定
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def analyze_stats_image(image_file):
    base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
    
    # この画像形式に特化したプロンプト
    prompt = """
    バスケットボールのボックススコア画像を解析してください。
    以下の項目を抽出し、JSON形式で出力してください。
    項目：選手名(選手名), PTS(得点), 3PM(3P成功数), TOT(リバウンド合計), AST(アシスト), F(ファウルPF)
    
    【ルール】
    - 「TOTALS」や「Team/Coaches」の行は除外してください。
    - 数値が空欄や「0」の場合は 0 としてください。
    - 出力例: [{"選手名": "森 一希", "PTS": 16, "3PM": 2, "TOT": 21, "AST": 1, "F": 3}]
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ],
            }
        ],
        response_format={ "type": "json_object" }
    )
    import json
    # JSONのキー名はAIが返すものに合わせる
    res_data = json.loads(response.choices[0].message.content)
    # リスト形式で返す
    return res_data.get("stats", res_data) if isinstance(res_data, dict) else res_data

# --- Streamlit UI ---
st.title("🏀 筑波大附スタッツ解析システム")

uploaded_file = st.file_uploader("節分カップのスタッツ画像をアップロード", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    st.image(uploaded_file, caption="アップロードされたスコアシート", use_column_width=True)
    
    if st.button("AI解析を実行"):
        with st.spinner("画像からデータを抽出中..."):
            try:
                extracted_data = analyze_stats_image(uploaded_file)
                # リストが辞書の中に入っている場合への対応
                if isinstance(extracted_data, dict):
                    for key in extracted_data:
                        if isinstance(extracted_data[key], list):
                            extracted_data = extracted_data[key]
                            break
                
                st.session_state['temp_df'] = pd.DataFrame(extracted_data)
                st.success("解析完了！内容を確認してください。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

if 'temp_df' in st.session_state:
    st.subheader("データの確認・修正")
    # ユーザーが手動で直せるようにする
    edited_df = st.data_editor(st.session_state['temp_df'], num_rows="dynamic")
    
    if st.button("シーズン記録に保存"):
        # ここでCSV等に保存する処理を追加可能
        st.balloons()
        st.success("保存しました！")
