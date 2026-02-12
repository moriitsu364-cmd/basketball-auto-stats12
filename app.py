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
import os

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
# モダンでレスポンシブなカスタムCSS
# ========================================
st.markdown("""
<style>
    /* 全体の背景 - グラデーション */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        background-attachment: fixed;
    }
    
    /* メインコンテナ */
    .main {
        background: transparent;
        padding: 0;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* ヘッダー部分 - アニメーション付き */
    .app-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .app-header-content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .app-header h1 {
        color: #ffffff;
        font-size: clamp(1.5rem, 4vw, 2.8rem);
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
        text-transform: uppercase;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    .app-header .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: clamp(0.85rem, 2vw, 1.1rem);
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    
    .header-icon {
        font-size: clamp(2rem, 5vw, 3.5rem);
        filter: drop-shadow(2px 2px 8px rgba(0,0,0,0.3));
    }
    
    /* ナビゲーションタブ - モダンデザイン */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
        font-size: clamp(0.75rem, 2vw, 0.95rem);
        padding: clamp(0.8rem, 2vw, 1rem) clamp(1rem, 3vw, 1.5rem);
        border: none;
        border-radius: 8px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* データテーブル - グラスモーフィズム */
    .dataframe {
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px;
        overflow: hidden;
        font-size: clamp(0.75rem, 1.5vw, 0.9rem);
    }
    
    .dataframe th {
        background: rgba(30, 41, 59, 0.9) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: clamp(0.7rem, 1.5vw, 0.85rem);
        letter-spacing: 0.5px;
        padding: clamp(0.8rem, 2vw, 1rem) !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    .dataframe td {
        background: rgba(30, 41, 59, 0.4) !important;
        color: #e0e0e0 !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.2) !important;
        padding: clamp(0.7rem, 2vw, 0.9rem) !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(59, 130, 246, 0.2) !important;
    }
    
    /* 統計カード - グラスモーフィズム */
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(30, 41, 59, 0.6) 100%);
        backdrop-filter: blur(10px);
        padding: clamp(1.2rem, 3vw, 1.8rem);
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.3);
        border-color: #3b82f6;
    }
    
    .stat-card .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: clamp(0.75rem, 1.5vw, 0.85rem);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .stat-card .stat-value {
        color: #ffffff;
        font-size: clamp(2rem, 5vw, 2.8rem);
        font-weight: 700;
        line-height: 1;
        background: linear-gradient(135deg, #ffffff 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-card .stat-subtitle {
        color: #3b82f6;
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* セレクトボックス */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #ffffff;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3b82f6;
    }
    
    /* 日付入力 */
    .stDateInput > div > div {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #ffffff;
        border-radius: 8px;
    }
    
    /* ボタン - グラデーション */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: clamp(0.8rem, 2vw, 1rem) clamp(1.5rem, 3vw, 2rem);
        font-weight: 700;
        font-size: clamp(0.85rem, 2vw, 1rem);
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.6);
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }
    
    /* プレイヤーカード */
    .player-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(30, 41, 59, 0.7) 100%);
        backdrop-filter: blur(10px);
        padding: clamp(1.5rem, 3vw, 2rem);
        border-radius: 20px;
        border: 2px solid rgba(59, 130, 246, 0.4);
        margin-bottom: 2rem;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .player-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
    }
    
    .player-card .player-name {
        color: #ffffff;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .player-card .player-number {
        color: #3b82f6;
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        font-weight: 700;
    }
    
    /* ランキングテーブル */
    .ranking-row {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        padding: clamp(1rem, 2vw, 1.2rem);
        border-radius: 12px;
        margin-bottom: 0.8rem;
        border-left: 4px solid rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .ranking-row:hover {
        background: rgba(59, 130, 246, 0.2);
        border-left-color: #3b82f6;
        transform: translateX(8px);
    }
    
    .ranking-row.rank-1 {
        border-left-color: #ffd700;
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.15) 0%, rgba(30, 41, 59, 0.6) 100%);
    }
    
    .ranking-row.rank-2 {
        border-left-color: #c0c0c0;
        background: linear-gradient(90deg, rgba(192, 192, 192, 0.15) 0%, rgba(30, 41, 59, 0.6) 100%);
    }
    
    .ranking-row.rank-3 {
        border-left-color: #cd7f32;
        background: linear-gradient(90deg, rgba(205, 127, 50, 0.15) 0%, rgba(30, 41, 59, 0.6) 100%);
    }
    
    .ranking-left {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex: 1;
        min-width: 150px;
    }
    
    .ranking-right {
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
        flex-shrink: 0;
    }
    
    /* セクションヘッダー */
    .section-header {
        color: #ffffff;
        font-size: clamp(1.3rem, 3vw, 1.8rem);
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
    }
    
    .section-header::before {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    /* ファイルアップローダー */
    .stFileUploader > div {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 2px dashed rgba(59, 130, 246, 0.4);
        border-radius: 12px;
        padding: 2rem;
    }
    
    .stFileUploader > div:hover {
        border-color: #3b82f6;
        background: rgba(59, 130, 246, 0.1);
    }
    
    /* 入力フィールド */
    .stTextInput > div > div,
    .stNumberInput > div > div {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #ffffff;
        border-radius: 8px;
    }
    
    .stTextInput > div > div:focus-within,
    .stNumberInput > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }
    
    /* メッセージ */
    .stSuccess {
        background: rgba(16, 185, 129, 0.15);
        border-left: 4px solid #10b981;
        color: #ffffff;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        color: #ffffff;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.15);
        border-left: 4px solid #3b82f6;
        color: #ffffff;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    /* Plotlyグラフ */
    .js-plotly-plot {
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
    }
    
    /* スクロールバー */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3b82f6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2563eb;
    }
    
    /* レスポンシブ調整 */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .app-header {
            padding: 1.5rem 1rem;
            margin: -1rem -1rem 1.5rem -1rem;
        }
        
        .app-header-content {
            flex-direction: column;
            text-align: center;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
        
        .ranking-row {
            flex-direction: column;
            align-items: flex-start;
        }
        
        .ranking-right {
            width: 100%;
            justify-content: space-between;
        }
    }
    
    /* データエディター */
    [data-testid="stDataFrameResizable"] {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
    }
    
    /* 比較カード */
    .compare-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.3);
        margin-bottom: 1rem;
    }
    
    /* ローディングスピナー */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース関連の関数
# ========================================
DATA_FILE = "basketball_stats.csv"

def init_database():
    """データベースの初期化"""
    if 'database' not in st.session_state:
        # ファイルから読み込み
        if os.path.exists(DATA_FILE):
            try:
                st.session_state['database'] = pd.read_csv(DATA_FILE)
            except Exception as e:
                st.error(f"データ読み込みエラー: {e}")
                st.session_state['database'] = create_empty_dataframe()
        else:
            st.session_state['database'] = create_empty_dataframe()

def create_empty_dataframe():
    """空のデータフレームを作成"""
    return pd.DataFrame(columns=[
        'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
        '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
        'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
        'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
        'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
    ])

def save_database():
    """データベースをCSVに保存"""
    try:
        st.session_state['database'].to_csv(DATA_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"保存エラー: {e}")
        return False

# ========================================
# Gemini API設定
# ========================================
@st.cache_resource
def setup_gemini():
    """Gemini APIのセットアップ"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None, None
    
    try:
        genai.configure(api_key=api_key)
        
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        priority_models = [
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash',
            'models/gemini-pro-vision'
        ]
        
        model_name = None
        for preferred in priority_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        if not model_name and available_models:
            model_name = available_models[0]
        
        if model_name:
            model = genai.GenerativeModel(model_name)
            return model, model_name
        
        return None, None
        
    except Exception as e:
        st.error(f"Gemini APIのセットアップエラー: {e}")
        return None, None

# ========================================
# 統計計算関数
# ========================================
def calculate_stats(df, player_name=None):
    """統計を計算"""
    if player_name:
        df = df[df['PlayerName'] == player_name]
    
    if len(df) == 0:
        return {
            'GP': 0, 'PTS': 0, 'REB': 0, 'AST': 0, 'STL': 0, 'BLK': 0,
            'FG%': 0, '3P%': 0, 'FT%': 0, 'TO': 0, 'PF': 0
        }
    
    stats = {
        'GP': len(df),
        'PTS': df['PTS'].mean(),
        'REB': df['TOT'].mean(),
        'AST': df['AST'].mean(),
        'STL': df['STL'].mean(),
        'BLK': df['BLK'].mean(),
        'TO': df['TO'].mean(),
        'PF': df['PF'].mean(),
        'FG%': (df['3PM'].sum() + df['2PM'].sum()) / (df['3PA'].sum() + df['2PA'].sum()) * 100 if (df['3PA'].sum() + df['2PA'].sum()) > 0 else 0,
        '3P%': df['3PM'].sum() / df['3PA'].sum() * 100 if df['3PA'].sum() > 0 else 0,
        'FT%': df['FTM'].sum() / df['FTA'].sum() * 100 if df['FTA'].sum() > 0 else 0,
    }
    return stats

def create_modern_chart(data, title, x_col, y_col, color='#3b82f6', show_area=True):
    """モダンなチャートを作成"""
    fig = go.Figure()
    
    if show_area:
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines+markers',
            line=dict(color=color, width=3),
            marker=dict(
                size=10, 
                color=color,
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            fill='tozeroy',
            fillcolor=f'rgba(59, 130, 246, 0.2)',
            name=y_col
        ))
    else:
        fig.add_trace(go.Bar(
            x=data[x_col],
            y=data[y_col],
            marker=dict(
                color=color,
                line=dict(color='white', width=1)
            ),
            name=y_col
        ))
    
    fig.update_layout(
        title=dict(
            text=title, 
            font=dict(size=20, color='white', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='rgba(30, 41, 59, 0.4)',
        paper_bgcolor='rgba(30, 41, 59, 0.4)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.2)',
            showgrid=True,
            zeroline=False,
            tickangle=-45
        ),
        yaxis=dict(
            gridcolor='rgba(59, 130, 246, 0.2)',
            showgrid=True,
            zeroline=False
        ),
        hovermode='x unified',
        margin=dict(l=40, r=40, t=60, b=80),
        height=400,
        showlegend=False
    )
    
    return fig

def create_comparison_chart(player1_data, player2_data, player1_name, player2_name):
    """選手比較チャート"""
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG%']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[player1_data.get(cat, 0) for cat in categories],
        theta=categories,
        fill='toself',
        name=player1_name,
        line=dict(color='#3b82f6', width=2),
        fillcolor='rgba(59, 130, 246, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[player2_data.get(cat, 0) for cat in categories],
        theta=categories,
        fill='toself',
        name=player2_name,
        line=dict(color='#8b5cf6', width=2),
        fillcolor='rgba(139, 92, 246, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor='rgba(59, 130, 246, 0.2)',
                color='white'
            ),
            bgcolor='rgba(30, 41, 59, 0.4)',
            angularaxis=dict(
                gridcolor='rgba(59, 130, 246, 0.2)',
                color='white'
            )
        ),
        paper_bgcolor='rgba(30, 41, 59, 0.4)',
        plot_bgcolor='rgba(30, 41, 59, 0.4)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(59, 130, 246, 0.3)',
            borderwidth=1
        ),
        height=500
    )
    
    return fig

# ========================================
# メイン画面
# ========================================
def main():
    init_database()
    
    # ヘッダー
    st.markdown("""
    <div class="app-header">
        <div class="app-header-content">
            <div class="header-icon">🏀</div>
            <div>
                <h1>TSUKUBA HIGHSCHOOL STATS</h1>
                <p class="subtitle">筑波大学附属高校男バススタッツ記録システム</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    model, model_name = setup_gemini()
    
    # メインタブ
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 SEASON", 
        "👤 PLAYER", 
        "📊 GAME", 
        "⚖️ COMPARE",
        "📥 INPUT"
    ])
    
    # ========================================
    # タブ1: シーズン統計
    # ========================================
    with tab1:
        st.markdown('<div class="section-header">Season Overview</div>', unsafe_allow_html=True)
        
        if st.session_state['database'].empty:
            st.info("📭 データがまだありません。INPUTタブからデータを追加してください。")
        else:
            db = st.session_state['database']
            seasons = sorted(db['Season'].unique(), reverse=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                selected_season = st.selectbox("シーズンを選択", seasons, key='season_select')
            with col2:
                # エクスポートボタン
                if st.button("📊 データをエクスポート", use_container_width=True):
                    csv = db[db['Season'] == selected_season].to_csv(index=False)
                    st.download_button(
                        label="💾 CSVダウンロード",
                        data=csv,
                        file_name=f"stats_{selected_season}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            if selected_season:
                season_data = db[db['Season'] == selected_season]
                
                # サマリーメトリクス
                col1, col2, col3, col4, col5 = st.columns(5)
                
                games = len(season_data['GameDate'].unique())
                players = season_data['PlayerName'].nunique()
                avg_pts = season_data.groupby('GameDate')['PTS'].sum().mean()
                wins = len(season_data[season_data['TeamScore'] > season_data['OpponentScore']]['GameDate'].unique())
                losses = len(season_data[season_data['TeamScore'] < season_data['OpponentScore']]['GameDate'].unique())
                
                metrics = [
                    ("Games", games, "試合数"),
                    ("Players", players, "選手数"),
                    ("Avg PPG", f"{avg_pts:.1f}", "平均得点"),
                    ("Wins", wins, "勝利"),
                    ("Losses", losses, "敗北")
                ]
                
                for col, (label, value, subtitle) in zip([col1, col2, col3, col4, col5], metrics):
                    with col:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{label}</div>
                            <div class="stat-value">{value}</div>
                            <div class="stat-subtitle">{subtitle}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # チームトレンド
                st.markdown('<div class="section-header">Team Performance Trend</div>', unsafe_allow_html=True)
                
                game_stats = season_data.groupby('GameDate').agg({
                    'PTS': 'sum',
                    'TOT': 'sum',
                    'AST': 'sum'
                }).reset_index()
                
                trend_col1, trend_col2 = st.columns(2)
                
                with trend_col1:
                    fig_pts = create_modern_chart(game_stats, 'Points Per Game', 'GameDate', 'PTS')
                    st.plotly_chart(fig_pts, use_container_width=True)
                
                with trend_col2:
                    fig_ast = create_modern_chart(game_stats, 'Assists Per Game', 'GameDate', 'AST', color='#8b5cf6')
                    st.plotly_chart(fig_ast, use_container_width=True)
                
                # ランキング
                st.markdown('<div class="section-header">League Leaders</div>', unsafe_allow_html=True)
                
                ranking_tab1, ranking_tab2, ranking_tab3, ranking_tab4 = st.tabs(
                    ["🏅 POINTS", "🏅 REBOUNDS", "🏅 ASSISTS", "🏅 OVERALL"]
                )
                
                with ranking_tab1:
                    pts_leaders = season_data.groupby('PlayerName').agg({
                        'PTS': ['sum', 'mean', 'count']
                    }).round(1)
                    pts_leaders.columns = ['Total', 'PPG', 'GP']
                    pts_leaders = pts_leaders.sort_values('Total', ascending=False).head(10)
                    
                    for idx, (player, row) in enumerate(pts_leaders.iterrows(), 1):
                        rank_class = f"rank-{idx}" if idx <= 3 else ""
                        st.markdown(f"""
                        <div class="ranking-row {rank_class}">
                            <div class="ranking-left">
                                <span style="color: #3b82f6; font-size: clamp(1.2rem, 3vw, 1.5rem); font-weight: 700;">#{idx}</span>
                                <span style="color: white; font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 600;">{player}</span>
                            </div>
                            <div class="ranking-right">
                                <span style="color: #3b82f6; font-size: clamp(1.3rem, 3vw, 1.5rem); font-weight: 700;">{row['PPG']:.1f}</span>
                                <span style="color: rgba(255,255,255,0.7); font-size: clamp(0.8rem, 2vw, 0.9rem);">PPG ({row['GP']:.0f} GP)</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with ranking_tab2:
                    reb_leaders = season_data.groupby('PlayerName').agg({
                        'TOT': ['sum', 'mean', 'count']
                    }).round(1)
                    reb_leaders.columns = ['Total', 'RPG', 'GP']
                    reb_leaders = reb_leaders.sort_values('Total', ascending=False).head(10)
                    
                    for idx, (player, row) in enumerate(reb_leaders.iterrows(), 1):
                        rank_class = f"rank-{idx}" if idx <= 3 else ""
                        st.markdown(f"""
                        <div class="ranking-row {rank_class}">
                            <div class="ranking-left">
                                <span style="color: #8b5cf6; font-size: clamp(1.2rem, 3vw, 1.5rem); font-weight: 700;">#{idx}</span>
                                <span style="color: white; font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 600;">{player}</span>
                            </div>
                            <div class="ranking-right">
                                <span style="color: #8b5cf6; font-size: clamp(1.3rem, 3vw, 1.5rem); font-weight: 700;">{row['RPG']:.1f}</span>
                                <span style="color: rgba(255,255,255,0.7); font-size: clamp(0.8rem, 2vw, 0.9rem);">RPG ({row['GP']:.0f} GP)</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with ranking_tab3:
                    ast_leaders = season_data.groupby('PlayerName').agg({
                        'AST': ['sum', 'mean', 'count']
                    }).round(1)
                    ast_leaders.columns = ['Total', 'APG', 'GP']
                    ast_leaders = ast_leaders.sort_values('Total', ascending=False).head(10)
                    
                    for idx, (player, row) in enumerate(ast_leaders.iterrows(), 1):
                        rank_class = f"rank-{idx}" if idx <= 3 else ""
                        st.markdown(f"""
                        <div class="ranking-row {rank_class}">
                            <div class="ranking-left">
                                <span style="color: #ec4899; font-size: clamp(1.2rem, 3vw, 1.5rem); font-weight: 700;">#{idx}</span>
                                <span style="color: white; font-size: clamp(1rem, 2.5vw, 1.2rem); font-weight: 600;">{player}</span>
                            </div>
                            <div class="ranking-right">
                                <span style="color: #ec4899; font-size: clamp(1.3rem, 3vw, 1.5rem); font-weight: 700;">{row['APG']:.1f}</span>
                                <span style="color: rgba(255,255,255,0.7); font-size: clamp(0.8rem, 2vw, 0.9rem);">APG ({row['GP']:.0f} GP)</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with ranking_tab4:
                    overall_stats = season_data.groupby('PlayerName').agg({
                        'PTS': 'mean',
                        'TOT': 'mean',
                        'AST': 'mean',
                        'STL': 'mean',
                        'BLK': 'mean',
                        'GameDate': 'count'
                    }).round(1)
                    overall_stats.columns = ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'GP']
                    overall_stats = overall_stats.sort_values('PPG', ascending=False)
                    
                    st.dataframe(
                        overall_stats,
                        use_container_width=True,
                        height=600
                    )
    
    # ========================================
    # タブ2: 選手統計
    # ========================================
    with tab2:
        st.markdown('<div class="section-header">Player Statistics</div>', unsafe_allow_html=True)
        
        if st.session_state['database'].empty:
            st.info("📭 データがまだありません。")
        else:
            db = st.session_state['database']
            players = sorted(db['PlayerName'].unique())
            
            selected_player = st.selectbox("選手を選択", players, key='player_select')
            
            if selected_player:
                player_data = db[db['PlayerName'] == selected_player].copy()
                player_data = player_data.sort_values('GameDate')
                
                # 選手情報カード
                stats = calculate_stats(db, selected_player)
                player_number = player_data['No'].iloc[0] if len(player_data) > 0 else "N/A"
                
                st.markdown(f"""
                <div class="player-card">
                    <div class="player-number">#{player_number}</div>
                    <div class="player-name">{selected_player}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 主要スタッツ
                col1, col2, col3, col4, col5 = st.columns(5)
                
                stat_items = [
                    ("PPG", stats['PTS'], "Points"),
                    ("RPG", stats['REB'], "Rebounds"),
                    ("APG", stats['AST'], "Assists"),
                    ("FG%", stats['FG%'], "Field Goal"),
                    ("GP", stats['GP'], "Games")
                ]
                
                for col, (label, value, subtitle) in zip([col1, col2, col3, col4, col5], stat_items):
                    with col:
                        display_value = f"{value:.1f}" if isinstance(value, float) else str(value)
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{label}</div>
                            <div class="stat-value">{display_value}</div>
                            <div class="stat-subtitle">{subtitle}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # グラフ
                st.markdown('<div class="section-header">Performance Charts</div>', unsafe_allow_html=True)
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    fig_pts = create_modern_chart(player_data, 'Points Per Game', 'GameDate', 'PTS')
                    st.plotly_chart(fig_pts, use_container_width=True)
                
                with chart_col2:
                    fig_reb = create_modern_chart(player_data, 'Rebounds Per Game', 'GameDate', 'TOT', color='#8b5cf6')
                    st.plotly_chart(fig_reb, use_container_width=True)
                
                # 追加統計
                st.markdown('<div class="section-header">Additional Stats</div>', unsafe_allow_html=True)
                
                add_col1, add_col2, add_col3, add_col4 = st.columns(4)
                
                add_stats = [
                    ("SPG", stats['STL'], "Steals"),
                    ("BPG", stats['BLK'], "Blocks"),
                    ("3P%", stats['3P%'], "3-Point"),
                    ("FT%", stats['FT%'], "Free Throw")
                ]
                
                for col, (label, value, subtitle) in zip([add_col1, add_col2, add_col3, add_col4], add_stats):
                    with col:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{label}</div>
                            <div class="stat-value">{value:.1f}</div>
                            <div class="stat-subtitle">{subtitle}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # 詳細データ
                st.markdown('<div class="section-header">Game Log</div>', unsafe_allow_html=True)
                
                display_cols = ['GameDate', 'Opponent', 'PTS', '3PM', '3PA', '3P%', 
                               'FTM', 'FTA', 'FT%', 'TOT', 'AST', 'STL', 'BLK', 'MIN']
                
                st.dataframe(
                    player_data[display_cols],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
    
    # ========================================
    # タブ3: 試合統計
    # ========================================
    with tab3:
        st.markdown('<div class="section-header">Game Statistics</div>', unsafe_allow_html=True)
        
        if st.session_state['database'].empty:
            st.info("📭 データがまだありません。")
        else:
            db = st.session_state['database']
            games = sorted(db['GameDate'].unique(), reverse=True)
            
            selected_game = st.selectbox("試合を選択", games, key='game_select')
            
            if selected_game:
                game_data = db[db['GameDate'] == selected_game]
                
                # 試合情報
                opponent = game_data['Opponent'].iloc[0] if len(game_data) > 0 else "N/A"
                team_score = game_data['TeamScore'].iloc[0] if len(game_data) > 0 else 0
                opp_score = game_data['OpponentScore'].iloc[0] if len(game_data) > 0 else 0
                result = "WIN" if team_score > opp_score else "LOSS" if team_score < opp_score else "TIE"
                result_color = "#10b981" if result == "WIN" else "#ef4444" if result == "LOSS" else "#f59e0b"
                
                st.markdown(f"""
                <div class="player-card" style="text-align: center;">
                    <div style="color: rgba(255,255,255,0.7); font-size: clamp(1rem, 2vw, 1.2rem); margin-bottom: 1rem;">
                        {selected_game}
                    </div>
                    <div style="font-size: clamp(1.3rem, 3vw, 2rem); color: white; margin-bottom: 1rem;">
                        筑波大附属 vs {opponent}
                    </div>
                    <div style="font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; color: white;">
                        {team_score} - {opp_score}
                    </div>
                    <div style="color: {result_color}; font-size: clamp(1.2rem, 3vw, 1.5rem); font-weight: 700; margin-top: 1rem;">
                        {result}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # チームスタッツ
                st.markdown('<div class="section-header">Team Statistics</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                total_pts = game_data['PTS'].sum()
                total_reb = game_data['TOT'].sum()
                total_ast = game_data['AST'].sum()
                fg_pct = (game_data['3PM'].sum() + game_data['2PM'].sum()) / (game_data['3PA'].sum() + game_data['2PA'].sum()) * 100 if (game_data['3PA'].sum() + game_data['2PA'].sum()) > 0 else 0
                
                team_stats = [
                    ("Total Points", total_pts, "得点"),
                    ("Total Rebounds", total_reb, "リバウンド"),
                    ("Total Assists", total_ast, "アシスト"),
                    ("FG%", f"{fg_pct:.1f}%", "シュート率")
                ]
                
                for col, (label, value, subtitle) in zip([col1, col2, col3, col4], team_stats):
                    with col:
                        st.markdown(f"""
                        <div class="stat-card">
                            <div class="stat-label">{label}</div>
                            <div class="stat-value">{value}</div>
                            <div class="stat-subtitle">{subtitle}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # プレイヤースタッツ
                st.markdown('<div class="section-header">Player Box Score</div>', unsafe_allow_html=True)
                
                display_cols = ['No', 'PlayerName', 'PTS', '3PM', '3PA', '2PM', '2PA', 
                               'FTM', 'FTA', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'PF', 'MIN']
                
                st.dataframe(
                    game_data[display_cols].sort_values('PTS', ascending=False),
                    use_container_width=True,
                    hide_index=True,
                    height=500
                )
    
    # ========================================
    # タブ4: 比較機能
    # ========================================
    with tab4:
        st.markdown('<div class="section-header">Player Comparison</div>', unsafe_allow_html=True)
        
        if st.session_state['database'].empty:
            st.info("📭 データがまだありません。")
        else:
            db = st.session_state['database']
            players = sorted(db['PlayerName'].unique())
            
            col1, col2 = st.columns(2)
            
            with col1:
                player1 = st.selectbox("選手1を選択", players, key='compare_player1')
            
            with col2:
                remaining_players = [p for p in players if p != player1]
                player2 = st.selectbox("選手2を選択", remaining_players, key='compare_player2') if remaining_players else None
            
            if player1 and player2:
                stats1 = calculate_stats(db, player1)
                stats2 = calculate_stats(db, player2)
                
                # 比較レーダーチャート
                st.markdown('<div class="section-header">Stats Comparison</div>', unsafe_allow_html=True)
                
                # スタッツを正規化（0-100スケール）
                max_pts = max(stats1['PTS'], stats2['PTS'], 1)
                max_reb = max(stats1['REB'], stats2['REB'], 1)
                max_ast = max(stats1['AST'], stats2['AST'], 1)
                max_stl = max(stats1['STL'], stats2['STL'], 1)
                max_blk = max(stats1['BLK'], stats2['BLK'], 1)
                
                normalized_stats1 = {
                    'PTS': (stats1['PTS'] / max_pts) * 100,
                    'REB': (stats1['REB'] / max_reb) * 100,
                    'AST': (stats1['AST'] / max_ast) * 100,
                    'STL': (stats1['STL'] / max_stl) * 100,
                    'BLK': (stats1['BLK'] / max_blk) * 100,
                    'FG%': stats1['FG%']
                }
                
                normalized_stats2 = {
                    'PTS': (stats2['PTS'] / max_pts) * 100,
                    'REB': (stats2['REB'] / max_reb) * 100,
                    'AST': (stats2['AST'] / max_ast) * 100,
                    'STL': (stats2['STL'] / max_stl) * 100,
                    'BLK': (stats2['BLK'] / max_blk) * 100,
                    'FG%': stats2['FG%']
                }
                
                fig_compare = create_comparison_chart(normalized_stats1, normalized_stats2, player1, player2)
                st.plotly_chart(fig_compare, use_container_width=True)
                
                # 詳細比較テーブル
                st.markdown('<div class="section-header">Detailed Comparison</div>', unsafe_allow_html=True)
                
                comparison_data = {
                    'Stat': ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG%', '3P%', 'FT%', 'GP'],
                    player1: [
                        f"{stats1['PTS']:.1f}",
                        f"{stats1['REB']:.1f}",
                        f"{stats1['AST']:.1f}",
                        f"{stats1['STL']:.1f}",
                        f"{stats1['BLK']:.1f}",
                        f"{stats1['FG%']:.1f}",
                        f"{stats1['3P%']:.1f}",
                        f"{stats1['FT%']:.1f}",
                        f"{stats1['GP']}"
                    ],
                    player2: [
                        f"{stats2['PTS']:.1f}",
                        f"{stats2['REB']:.1f}",
                        f"{stats2['AST']:.1f}",
                        f"{stats2['STL']:.1f}",
                        f"{stats2['BLK']:.1f}",
                        f"{stats2['FG%']:.1f}",
                        f"{stats2['3P%']:.1f}",
                        f"{stats2['FT%']:.1f}",
                        f"{stats2['GP']}"
                    ]
                }
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True, hide_index=True, height=400)
                
                # シーズン比較
                st.markdown('<div class="section-header">Season Performance</div>', unsafe_allow_html=True)
                
                player1_data = db[db['PlayerName'] == player1].sort_values('GameDate')
                player2_data = db[db['PlayerName'] == player2].sort_values('GameDate')
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=player1_data['GameDate'],
                    y=player1_data['PTS'],
                    mode='lines+markers',
                    name=player1,
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(size=8)
                ))
                
                fig.add_trace(go.Scatter(
                    x=player2_data['GameDate'],
                    y=player2_data['PTS'],
                    mode='lines+markers',
                    name=player2,
                    line=dict(color='#8b5cf6', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title=dict(text='Points Per Game Comparison', font=dict(size=20, color='white')),
                    plot_bgcolor='rgba(30, 41, 59, 0.4)',
                    paper_bgcolor='rgba(30, 41, 59, 0.4)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(59, 130, 246, 0.2)', showgrid=True),
                    yaxis=dict(gridcolor='rgba(59, 130, 246, 0.2)', showgrid=True),
                    hovermode='x unified',
                    height=400,
                    legend=dict(
                        bgcolor='rgba(30, 41, 59, 0.8)',
                        bordercolor='rgba(59, 130, 246, 0.3)',
                        borderwidth=1
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # ========================================
    # タブ5: データ入力
    # ========================================
    with tab5:
        st.markdown('<div class="section-header">Data Input</div>', unsafe_allow_html=True)
        
        if not model:
            st.error("⚠️ Gemini APIキーが設定されていません。secrets.tomlファイルにGEMINI_API_KEYを設定してください。")
        else:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### 📋 試合情報")
                game_date = st.date_input("試合日", datetime.now())
                season = st.selectbox("シーズン", ["2023-24", "2024-25", "2025-26", "2026-27"], index=1)
                opponent = st.text_input("対戦相手", "")
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    team_score = st.number_input("筑波大附属", min_value=0, value=0)
                with col_s2:
                    opponent_score = st.number_input("相手スコア", min_value=0, value=0)
                
                st.markdown("#### 📷 スコアシート画像")
                uploaded_file = st.file_uploader(
                    "画像をアップロード",
                    type=['png', 'jpg', 'jpeg', 'webp']
                )
            
            with col2:
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image, use_container_width=True, caption="アップロードされた画像")
                    
                    if st.button("🚀 AI解析実行", use_container_width=True, type="primary"):
                        with st.spinner("AI解析中..."):
                            try:
                                prompt = """
この画像からバスケットボールのスコアシートデータを抽出してください。
以下の形式のCSVで出力してください（ヘッダー行を含む）:

No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN

注意事項:
- GSは先発選手の場合「●」があれば1、なければ0
- パーセンテージは数値のみ（%記号不要）
- MINは「32:38」のような形式で
- 数値がない場合は0を入力
- Team/Coachesの行は除外
- TOTALSの行は除外
- 選手名は正確に抽出

CSVのみを出力し、説明文は不要です。
"""
                                
                                response = model.generate_content([prompt, image])
                                csv_text = response.text.replace('```csv', '').replace('```', '').strip()
                                
                                df = pd.read_csv(io.StringIO(csv_text))
                                df['GameDate'] = str(game_date)
                                df['Season'] = season
                                df['Opponent'] = opponent
                                df['TeamScore'] = team_score
                                df['OpponentScore'] = opponent_score
                                
                                st.session_state['current_stats'] = df
                                st.success("✅ AI解析完了！データを確認してください。")
                                
                            except Exception as e:
                                st.error(f"❌ エラーが発生しました: {str(e)}")
                                st.info("画像が不鮮明な場合や、フォーマットが異なる場合はエラーが発生する可能性があります。")
        
        # 解析結果の編集
        if 'current_stats' in st.session_state:
            st.markdown('<div class="section-header">データ確認・編集</div>', unsafe_allow_html=True)
            
            st.info("💡 データを確認し、必要に応じて編集してください。問題がなければ保存ボタンを押してください。")
            
            edited_df = st.data_editor(
                st.session_state['current_stats'],
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("💾 データを保存", use_container_width=True, type="primary"):
                    st.session_state['database'] = pd.concat(
                        [st.session_state['database'], edited_df],
                        ignore_index=True
                    )
                    if save_database():
                        st.success("✅ データを保存しました！")
                        del st.session_state['current_stats']
                        st.rerun()
                    else:
                        st.error("❌ 保存に失敗しました。")
            
            with col2:
                if st.button("🗑️ キャンセル", use_container_width=True):
                    del st.session_state['current_stats']
                    st.rerun()
        
        # データ管理
        st.markdown('<div class="section-header">データ管理</div>', unsafe_allow_html=True)
        
        manage_col1, manage_col2, manage_col3 = st.columns(3)
        
        with manage_col1:
            st.markdown("#### 📤 エクスポート")
            if not st.session_state['database'].empty:
                csv = st.session_state['database'].to_csv(index=False)
                st.download_button(
                    label="💾 全データをCSVダウンロード",
                    data=csv,
                    file_name=f"basketball_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info("データがありません")
        
        with manage_col2:
            st.markdown("#### 📥 インポート")
            import_file = st.file_uploader("CSVファイルをアップロード", type=['csv'], key='import_csv')
            if import_file:
                try:
                    import_df = pd.read_csv(import_file)
                    if st.button("📥 データをインポート", use_container_width=True):
                        st.session_state['database'] = pd.concat(
                            [st.session_state['database'], import_df],
                            ignore_index=True
                        )
                        if save_database():
                            st.success("✅ インポート成功！")
                            st.rerun()
                except Exception as e:
                    st.error(f"❌ インポートエラー: {e}")
        
        with manage_col3:
            st.markdown("#### 🗑️ データ削除")
            if st.button("⚠️ 全データを削除", use_container_width=True):
                if 'confirm_delete' not in st.session_state:
                    st.session_state['confirm_delete'] = True
                    st.warning("もう一度押すと全データが削除されます")
                else:
                    st.session_state['database'] = create_empty_dataframe()
                    if save_database():
                        st.success("全データを削除しました")
                        del st.session_state['confirm_delete']
                        st.rerun()

if __name__ == "__main__":
    main()
