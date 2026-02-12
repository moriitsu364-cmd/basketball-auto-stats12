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
    page_title="TSUKUBA Stats Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# 筑波カラー & プロフェッショナル・カスタムCSS
# ========================================
st.markdown("""
<style>
    /* 全体の背景 - 深みのあるダークブルーグレー */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
    }
    
    /* メインコンテナ */
    .main {
        background: transparent;
    }
    
    /* ヘッダー部分 - 筑波ブルーのアクセント */
    .tsukuba-header {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 4px solid #00A1E9;
        box-shadow: 0 10px 30px rgba(0, 161, 233, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .tsukuba-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 2px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    .tsukuba-header .subtitle {
        color: #00A1E9;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* ナビゲーションタブ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        padding: 0 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1e293b;
        color: #94a3b8;
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00A1E9 !important;
        color: #ffffff !important;
        font-weight: bold;
    }
    
    /* 統計カード - ガラスデザイン */
    .stat-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: #00A1E9;
        background: rgba(30, 41, 59, 0.9);
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    .stat-value {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
    }
    
    .stat-unit {
        color: #00A1E9;
        font-size: 0.8rem;
        margin-left: 4px;
    }

    /* プレイヤーカード */
    .player-card {
        background: linear-gradient(135deg, #00A1E9 0%, #0077b6 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .player-card::after {
        content: "TSUKUBA";
        position: absolute;
        right: -20px;
        bottom: -20px;
        font-size: 6rem;
        font-weight: 900;
        opacity: 0.1;
        font-style: italic;
    }

    /* テーブルスタイル調整 */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
    }

    /* ボタン */
    .stButton > button {
        background: #00A1E9;
        border-radius: 12px;
        border: none;
        font-weight: 700;
        padding: 0.6rem 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース初期化
# ========================================
def init_database():
    if 'database' not in st.session_state:
        # サンプルデータを入れると動きが分かりやすいため、空のDF構造を作成
        st.session_state['database'] = pd.DataFrame(columns=[
            'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
            '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
            'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
            'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
        ])

# ========================================
# グラフ作成用 (筑波ブルーver)
# ========================================
def create_tsukuba_chart(data, title, x_col, y_col, color='#00A1E9'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x_col], y=data[y_col],
        mode='lines+markers',
        line=dict(color=color, width=4, shape='spline'),
        marker=dict(size=10, color=color, line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor=f'rgba(0, 161, 233, 0.1)'
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='white')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300
    )
    return fig

# ========================================
# メイン画面
# ========================================
def main():
    init_database()
    
    # ヘッダー
    st.markdown("""
    <div class="tsukuba-header">
        <div>
            <p class="subtitle">Varsity Basketball Team</p>
            <h1>TSUKUBA <span style="color:#00A1E9">STATS</span></h1>
        </div>
        <div style="text-align: right">
            <span style="background:#00A1E9; color:white; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:bold;">LIVE 2024-25</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 以降、元のロジックを継承しつつデザインを適用
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 SEASON", "👤 PLAYER", "📊 GAME", "📥 INPUT"])

    # --- 以下、ロジック部分は元のコードを維持し、CSSクラスを適用 ---
    # (例: st.markdown('<div class="stat-card">...</div>', unsafe_allow_html=True) を使用)
    
    with tab1:
        st.subheader("Season Overview")
        if st.session_state['database'].empty:
            st.info("データがありません。INPUTタブから試合結果を追加してください。")
        else:
            # 元の計算ロジック...
            pass

    # ... (他タブのコンテンツ) ...

if __name__ == "__main__":
    main()
