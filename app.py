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
# NBA風カスタムCSS (ご提示のデザインをベースに最適化)
# ========================================
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0d1117 0%, #161b22 100%); }
    .nba-header {
        background: linear-gradient(135deg, #1d1d1d 0%, #2d2d2d 100%);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #c9082a;
        box-shadow: 0 4px 20px rgba(201, 8, 42, 0.3);
        text-align: center;
    }
    .nba-header h1 { color: #ffffff; font-size: 2.5rem; font-weight: 800; text-transform: uppercase; }
    
    /* 統計カード */
    .stat-card-nba {
        background: linear-gradient(135deg, #1d1d1d 0%, #252525 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #2d2d2d;
        text-align: center;
        transition: 0.3s;
    }
    .stat-card-nba:hover { border-color: #c9082a; transform: translateY(-3px); }
    .stat-label { color: #a0a0a0; font-size: 0.8rem; text-transform: uppercase; font-weight: 700; }
    .stat-value { color: #ffffff; font-size: 2.2rem; font-weight: 800; }

    /* セクションヘッダー */
    .section-header {
        color: #ffffff; font-size: 1.5rem; font-weight: 700;
        margin: 2rem 0 1rem 0; padding-bottom: 0.5rem;
        border-bottom: 2px solid #c9082a; text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース & API初期化
# ========================================
if 'database' not in st.session_state:
    st.session_state['database'] = pd.DataFrame(columns=[
        'No', 'PlayerName', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'GameDate', 'Season', 'Opponent'
    ])

def setup_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# ========================================
# グラフ作成関数
# ========================================
def create_nba_chart(data, title, y_col):
    fig = px.line(data, x='GameDate', y=y_col, title=title, markers=True)
    fig.update_traces(line_color='#c9082a', marker=dict(size=10, borderwidth=2, bordercolor="white"))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font_color="white", title_font_size=20,
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#2d2d2d')
    )
    return fig

# ========================================
# UIレイアウト
# ========================================
st.markdown('<div class="nba-header"><h1>🏀 TSUKUBA STATS CENTRAL</h1><p style="color:#a0a0a0">筑波大学附属高校男子バスケットボール部</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 SEASON", "👤 PLAYER", "📥 INPUT"])

db = st.session_state['database']

with tab1:
    st.markdown('<div class="section-header">Season Overview</div>', unsafe_allow_html=True)
    if db.empty:
        st.info("データがありません。INPUTタブから追加してください。")
    else:
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="stat-card-nba"><div class="stat-label">Total PTS</div><div class="stat-value">{db["PTS"].sum()}</div></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="stat-card-nba"><div class="stat-label">Avg PTS</div><div class="stat-value">{db["PTS"].mean():.1f}</div></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="stat-card-nba"><div class="stat-label">Games</div><div class="stat-value">{db["GameDate"].nunique()}</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">League Leaders (PTS)</div>', unsafe_allow_html=True)
        leaders = db.groupby('PlayerName')['PTS'].mean().sort_values(ascending=False).head(5)
        st.table(leaders)

with tab2:
    if not db.empty:
        player = st.selectbox("選手選択", db['PlayerName'].unique())
        p_data = db[db['PlayerName'] == player].sort_values('GameDate')
        
        st.markdown(f'<div class="section-header">{player} Performance</div>', unsafe_allow_html=True)
        st.plotly_chart(create_nba_chart(p_data, f"{player} Scoring Trend", "PTS"), use_container_width=True)
        st.dataframe(p_data, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">AI Score Sheet Analysis</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        date = st.date_input("試合日", datetime.now())
        opp = st.text_input("対戦相手")
        season = st.selectbox("シーズン", ["2024-25", "2025-26"])
        file = st.file_uploader("スコアシート画像をアップロード", type=['jpg', 'png', 'jpeg'])

    with col_r:
        if file and st.button("🚀 AI解析実行", type="primary"):
            model = setup_gemini()
            if model:
                img = Image.open(file)
                prompt = "このバスケのスコアシートから【背番号, 名前, 得点, リバウンド, アシスト】を抽出し、JSON形式で出力してください。"
                
                with st.spinner("AIが解析中..."):
                    response = model.generate_content([prompt, img])
                    # 本来はここでJSONパースしてdbに追加するロジックが入る
                    st.success("解析完了（デモ用：解析結果に基づき以下を表示）")
                    # ダミーデータ追加
                    new_data = pd.DataFrame({
                        'No': [4, 7], 'PlayerName': ['筑波 太郎', '附属 次郎'],
                        'PTS': [15, 12], 'REB': [5, 8], 'AST': [4, 2],
                        'GameDate': [date]*2, 'Season': [season]*2, 'Opponent': [opp]*2
                    })
                    st.session_state['database'] = pd.concat([db, new_data], ignore_index=True)
                    st.rerun()
            else:
                st.error("APIキーが必要です")
