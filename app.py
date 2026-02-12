import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io

# --- ③ デザインの設定 (スタイリング) ---
st.set_page_config(page_title="Pro Basket Stats Analyzer", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #1e3a8a; border-bottom: 2px solid #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏀 Pro Basket Stats Analyzer")

# APIキーの設定
api_key = st.secrets.get("GEMINI_API_KEY")

# --- ② データベースのシミュレーション ---
# 本来はDBを使いますが、今回は簡易的にセッション(一時保存)とCSVで管理します
if 'database' not in st.session_state:
    st.session_state['database'] = pd.DataFrame()

# サイドメニュー
menu = st.sidebar.selectbox("メニュー", ["画像解析・記録", "シーズン集計・選手分析"])

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

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
                with st.spinner("AIが全スタッツを抽出中..."):
                    # プロンプトを強化（②のために構造化データを要求）
                    prompt = """
                    このバスケのスコアシートから全員分のスタッツを抽出し、以下のCSV形式で出力してください。
                    No,選手名,PTS,3PM,3PA,2PM,2PA,FTM,FTA,OR,DR,TOT,AST,STL,BLK,TO,PF,MIN
                    ※ヘッダーのみで、説明文は不要です。
                    """
                    response = model.generate_content([prompt, image])
                    
                    try:
                        # 解析結果をDataFrameに変換
                        df = pd.read_csv(io.StringIO(response.text))
                        df['試合日'] = game_date
                        df['シーズン'] = season
                        st.session_state['current_stats'] = df
                    except Exception as e:
                        st.error("解析データの形式変換に失敗しました。もう一度お試しください。")
                        st.write(response.text)

        # 解析結果の編集と保存
        if 'current_stats' in st.session_state:
            st.subheader("解析結果の確認・修正")
            edited_df = st.data_editor(st.session_state['current_stats'], num_rows="dynamic")
            
            if st.button("この試合のスタッツをデータベースに記録"):
                st.session_state['database'] = pd.concat([st.session_state['database'], edited_df], ignore_index=True)
                st.success("データベースに保存しました！")

    elif menu == "シーズン集計・選手分析":
        st.header("② シーズン・選手別データ分析")
        
        if st.session_state['database'].empty:
            st.warning("まだデータが記録されていません。解析ページからデータを追加してください。")
        else:
            db = st.session_state['database']
            
            # フィルター
            target_season = st.selectbox("シーズン選択", db['シーズン'].unique())
            target_player = st.selectbox("選手選択", db['選手名'].unique())
            
            # --- 年間通算スタッツ ---
            st.subheader(f"📊 {target_player} 選手の {target_season} シーズン通算")
            player_season_data = db[(db['選手名'] == target_player) & (db['シーズン'] == target_season)]
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("総得点", player_season_data['PTS'].sum())
            m2.metric("平均得点", round(player_season_data['PTS'].mean(), 1))
            m3.metric("総リバウンド", player_season_data['TOT'].sum())
            m4.metric("総アシスト", player_season_data['AST'].sum())
            
            # --- 試合ごとの推移 ---
            st.subheader("📅 試合ごとのスタッツ履歴")
            st.table(player_season_data[['試合日', 'PTS', 'AST', 'TOT', 'STL', 'BLK', 'MIN']])
            
            # 全体データのダウンロード
            csv = db.to_csv(index=False).encode('utf-8-sig')
            st.download_button("全データをCSVでエクスポート", csv, "all_stats.csv", "text/csv")

else:
    st.error("APIキーを設定してください。")
