import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="Tsukuba Highschool Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# NBA風カスタムCSS (修正版)
# ========================================
st.markdown("""
<style>
    /* ベース背景を強制的にダークに */
    .stApp {
        background-color: #0d1117;
        color: #ffffff;
    }
    
    /* ヘッダー */
    .nba-header {
        background: linear-gradient(135deg, #1d1d1d 0%, #2d2d2d 100%);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 4px solid #c9082a;
        text-align: center;
    }
    
    .nba-header h1 {
        color: #ffffff !important;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-transform: uppercase;
    }

    /* セクションの見出し */
    .section-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        border-left: 6px solid #c9082a;
        padding-left: 1rem;
    }

    /* 統計カード */
    .stat-card-nba {
        background: #1c2128;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #30363d;
        text-align: center;
        transition: 0.3s;
    }
    .stat-card-nba:hover {
        border-color: #c9082a;
    }
    .stat-label { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; }
    .stat-value { color: #ffffff; font-size: 2.2rem; font-weight: 700; }

    /* タブの文字色修正 */
    .stTabs [data-baseweb="tab"] {
        color: #8b949e !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #c9082a !important;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース機能
# ========================================
def init_database():
    if 'database' not in st.session_state:
        # サンプルデータ作成（最初は空でもOK）
        st.session_state['database'] = pd.DataFrame(columns=[
            'No', 'PlayerName', 'PTS', 'TOT', 'AST', 'STL', 'BLK', '3PM', '3PA', '2PM', '2PA', 'FTM', 'FTA',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore', 'MIN'
        ])

def add_data_to_db(new_df):
    st.session_state['database'] = pd.concat([st.session_state['database'], new_df], ignore_index=True)
    st.success("✅ データベースに保存されました！")

# ========================================
# Gemini API設定
# ========================================
def setup_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.warning("⚠️ Secretsに GEMINI_API_KEY を設定してください。")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# ========================================
# チャート作成
# ========================================
def create_nba_style_chart(data, title, x_col, y_col, color='#c9082a'):
    fig = px.line(data, x=x_col, y=y_col, title=title, markers=True)
    fig.update_traces(line_color=color, marker=dict(size=10, borderwidth=2, bordercolor="white"))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color="white", title_font_size=20
    )
    return fig

# ========================================
# メイン
# ========================================
def main():
    init_database()
    
    st.markdown('<div class="nba-header"><h1>🏀 TSUKUBA STATS</h1><p>筑波大学附属高校男子バスケットボール部</p></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🏆 SEASON", "👤 PLAYER", "📊 GAME", "📥 INPUT"])

    # --- INPUT TAB ---
    with tab4:
        st.markdown('<div class="section-header">Data Input (AI Analysis)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            game_date = st.date_input("試合日", datetime.now())
            season = st.selectbox("シーズン", ["2024-25", "2025-26"])
            opponent = st.text_input("対戦相手")
            t_score = st.number_input("筑附スコア", min_value=0)
            o_score = st.number_input("相手スコア", min_value=0)
            
            uploaded_file = st.file_uploader("スコアシート画像をアップロード", type=['png', 'jpg', 'jpeg'])
            
        with col2:
            if uploaded_file and st.button("🚀 AI解析実行"):
                model = setup_gemini()
                if model:
                    img = Image.open(uploaded_file)
                    st.image(img, caption="解析対象", use_container_width=True)
                    
                    prompt = """
                    このバスケットボールのスコアシートからスタッツを抽出し、以下のJSON形式で出力してください。
                    {"stats": [{"No": 4, "PlayerName": "名前", "PTS": 10, "3PM": 2, "3PA": 5, "2PM": 2, "2PA": 4, "FTM": 0, "FTA": 0, "TOT": 5, "AST": 3, "STL": 1, "BLK": 0, "MIN": "15:00"}]}
                    """
                    with st.spinner("AIが読み取り中..."):
                        response = model.generate_content([prompt, img])
                        try:
                            # JSON抽出の簡易処理
                            json_str = response.text.replace('```json', '').replace('```', '').strip()
                            data = json.loads(json_str)
                            df_new = pd.DataFrame(data['stats'])
                            
                            # 共通情報の付与
                            df_new['GameDate'] = game_date.strftime('%Y-%m-%d')
                            df_new['Season'] = season
                            df_new['Opponent'] = opponent
                            df_new['TeamScore'] = t_score
                            df_new['OpponentScore'] = o_score
                            
                            st.write("### 解析結果のプレビュー")
                            st.dataframe(df_new)
                            
                            if st.button("💾 データベースへ保存"):
                                add_data_to_db(df_new)
                        except:
                            st.error("AIの解析に失敗しました。もう一度試すか、手動で入力してください。")

    # --- SEASON TAB ---
    with tab1:
        db = st.session_state['database']
        if db.empty:
            st.info("データがありません。INPUTタブから追加してください。")
        else:
            st.markdown('<div class="section-header">Season Overview</div>', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.markdown(f'<div class="stat-card-nba"><div class="stat-label">Games</div><div class="stat-value">{len(db["GameDate"].unique())}</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="stat-card-nba"><div class="stat-label">Total PTS</div><div class="stat-value">{db["PTS"].sum()}</div></div>', unsafe_allow_html=True)
            m3.markdown(f'<div class="stat-card-nba"><div class="stat-label">Top Scorer</div><div class="stat-value">{db.groupby("PlayerName")["PTS"].sum().idxmax()}</div></div>', unsafe_allow_html=True)
            
            st.markdown("### Player Leaderboard")
            leaderboard = db.groupby("PlayerName")[["PTS", "TOT", "AST", "STL", "BLK"]].mean().sort_values("PTS", ascending=False)
            st.dataframe(leaderboard.style.highlight_max(axis=0, color='#c9082a'), use_container_width=True)

    # --- PLAYER TAB ---
    with tab2:
        if not db.empty:
            player = st.selectbox("選手名を選択", db["PlayerName"].unique())
            p_data = db[db["PlayerName"] == player].sort_values("GameDate")
            
            st.markdown(f'<div class="section-header">{player} Stats Log</div>', unsafe_allow_html=True)
            fig = create_nba_style_chart(p_data, "Points per Game", "GameDate", "PTS")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(p_data, use_container_width=True)

    # --- GAME TAB ---
    with tab3:
        if not db.empty:
            g_date = st.selectbox("試合日を選択", db["GameDate"].unique())
            g_data = db[db["GameDate"] == g_date]
            st.markdown(f'<div class="section-header">VS {g_data["Opponent"].iloc[0]} ({g_date})</div>', unsafe_allow_html=True)
            st.dataframe(g_data.sort_values("PTS", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
