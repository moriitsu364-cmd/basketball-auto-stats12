import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="Tsukuba Stats Pro",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# NBA風・超レスポンシブCSS
# ========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');

    .stApp {
        background: #051c2c; /* NBAダークネイビー */
        background-attachment: fixed;
    }

    /* レスポンシブコンテナ */
    @media (max-width: 768px) {
        .stat-card-nba {
            margin-bottom: 10px !important;
        }
        .nba-header h1 {
            font-size: 1.8rem !important;
        }
    }

    .nba-header {
        background: linear-gradient(90deg, #1d428a 0%, #000000 50%, #c8102e 100%);
        padding: 3rem 1rem;
        text-align: center;
        border-bottom: 5px solid #ffb81c;
        margin-bottom: 2rem;
    }

    .nba-header h1 {
        font-family: 'Oswald', sans-serif;
        font-size: 4rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }

    /* 選手カード (NBA公式風) */
    .player-hero {
        background: linear-gradient(135deg, #1d428a 0%, #081629 100%);
        border-radius: 20px;
        padding: 40px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 30px;
    }

    .player-image-container {
        flex: 0 0 250px;
        height: 250px;
        background: radial-gradient(circle, #2d2d2d 0%, #000 100%);
        border-radius: 50%;
        border: 4px solid #ffb81c;
        overflow: hidden;
        margin-right: 40px;
    }

    .player-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* トーナメントブラケット */
    .bracket {
        display: flex;
        overflow-x: auto;
        padding: 20px;
        gap: 20px;
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
    }
    .matchup {
        background: #1d1d1d;
        border-left: 4px solid #c8102e;
        padding: 10px;
        width: 180px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .matchup-win { border-left-color: #ffb81c; }

    /* ステータスバッジ */
    .stat-badge {
        background: rgba(255,215,0,0.15);
        border: 1px solid #ffb81c;
        padding: 2px 8px;
        border-radius: 4px;
        color: #ffb81c;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# 補助関数
# ========================================
def init_database():
    if 'database' not in st.session_state:
        # デモ用データを入れる（空だと寂しいため）
        st.session_state['database'] = pd.DataFrame([
            {'No': '23', 'PlayerName': 'Sample Player', 'PTS': 25, 'TOT': 10, 'AST': 8, 'STL': 2, 'BLK': 1, 
             '3PM': 3, '3PA': 6, '2PM': 7, '2PA': 10, 'FTM': 2, 'FTA': 2, 'MIN': 32,
             'GameDate': '2024-02-12', 'Season': '2024-25', 'Opponent': 'Kyoto HS', 'TeamScore': 88, 'OpponentScore': 82}
        ])

def calculate_stats(df, player_name=None):
    if player_name:
        df = df[df['PlayerName'] == player_name]
    if df.empty: return {k: 0 for k in ['GP', 'PTS', 'REB', 'AST', 'FG%', 'FT%']}
    
    stats = {
        'GP': len(df),
        'PTS': df['PTS'].mean(),
        'REB': df['TOT'].mean(),
        'AST': df['AST'].mean(),
        'FG%': (df['3PM'].sum() + df['2PM'].sum()) / (df['3PA'].sum() + df['2PA'].sum() + 0.1) * 100,
        'FT%': df['FTM'].sum() / (df['FTA'].sum() + 0.1) * 100,
    }
    return stats

# ========================================
# メイン
# ========================================
def main():
    init_database()
    
    # NBA ヘッダー
    st.markdown("""
    <div class="nba-header">
        <h1>TSUKUBA STATS PRO</h1>
        <div style="color: #ffb81c; font-weight: bold; letter-spacing: 2px;">OFFICIAL PERFORMANCE TRACKER</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 SEASON", "👤 PLAYER", "📊 GAMES", "⚔️ BRACKET", "📥 INPUT"])

    db
