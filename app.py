import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io

# --- デザイン設定 ---
st.set_page_config(page_title="Pro Basket Stats Analyzer", layout="wide")
st.title("🏀 Pro Basket Stats Analyzer")

api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    
    # 【404対策】利用可能なモデルを自動取得する関数
    @st.cache_resource
    def get_working_model():
        # あなたのキーで使えるモデルを探す
        for m in genai.list_models():
            # 画像解析(vision)ができて、かつ最新のflashモデルを探す
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return m.name
        return "models/gemini-1.5-flash" # 見つからない場合のフォールバック

    target_model = get_working_model()
    model = genai.GenerativeModel(target_model)

    # --- セッション状態の初期化 ---
    if 'database' not in st.session_state:
        st.session_state['database'] = pd.DataFrame()

    menu = st.sidebar.selectbox("メニュー", ["画像解析・記録", "シーズン集計・選手分析"])

    if menu == "画像解析・記録":
        st.header("① スコアシート画像解析")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            game_date = st.date_input("試合日")
            season = st.selectbox("シーズン", ["2023-24", "2024-25", "2025-26"])
            uploaded_file = st.file_uploader("スコアシートをアップ", type=['png', 'jpg', 'jpeg'])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="アップロード画像", use_container_width=True)

            if st.button("AI解析を実行"):
                with st.spinner(f"モデル {target_model} で解析中..."):
                    try:
                        # 確実に出力させるためのプロンプト
                        prompt = "Extract all player stats from this basketball score sheet. Return only CSV format with headers: No,PlayerName,PTS,3PM,3PA,2PM,2PA,FTM,FTA,OR,DR,TOT,AST,STL,BLK,TO,PF,MIN"
                        response = model.generate_content([prompt, image])
                        
                        # CSVとして読み込み
                        csv_data = response.text.replace('```csv', '').replace('```', '').strip()
                        df = pd.read_csv(io.StringIO(csv_data))
                        df['試合日'] = str(game_date)
                        df['シーズン'] = season
                        st.session_state['current_stats'] = df
                    except Exception as e:
                        st.error(f"解析エラー: {e}")
                        st.info("※APIの通信でエラーが発生しました。時間を置いて試してください。")

        if 'current_stats' in st.session_state:
            st.subheader("解析結果の確認・修正")
            edited_df = st.data_editor(st.session_state['current_stats'], num_rows="dynamic")
            
            if st.button("データベースに記録"):
                st.session_state['database'] = pd.concat([st.session_state['database'], edited_df], ignore_index=True)
                st.success("データベースに保存しました！")

    elif menu == "シーズン集計・選手分析":
        st.header("② シーズン・選手別データ分析")
        if st.session_state['database'].empty:
            st.info("まだデータがありません。")
        else:
            db = st.session_state['database']
            target_player = st.selectbox("選手選択", db['PlayerName'].unique())
            player_data = db[db['PlayerName'] == target_player]
            st.write(f"### {target_player} 選手のスタッツ履歴")
            st.dataframe(player_data)

else:
    st.error("APIキーをSecretsに設定してください。")
