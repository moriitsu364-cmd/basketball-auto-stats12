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
    page_title="Tsukuba Highschool Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# NBA風カスタムCSS
# ========================================
st.markdown("""
<style>
    /* 全体の背景 */
    .stApp {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    }
    
    /* メインコンテナ */
    .main {
        background: transparent;
    }
    
    /* ヘッダー部分 */
    .nba-header {
        background: linear-gradient(135deg, #1d1d1d 0%, #2d2d2d 100%);
        padding: 2.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #c9082a;
        box-shadow: 0 4px 20px rgba(201, 8, 42, 0.3);
    }
    
    .nba-header h1 {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
        text-transform: uppercase;
    }
    
    .nba-header .subtitle {
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        letter-spacing: 1px;
    }
    
    /* ナビゲーションタブ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #1d1d1d;
        border-radius: 0;
        padding: 0;
        border-bottom: 2px solid #2d2d2d;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #a0a0a0;
        font-weight: 600;
        font-size: 1rem;
        padding: 1.2rem 2.5rem;
        border: none;
        border-bottom: 3px solid transparent;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #ffffff;
        border-bottom: 3px solid #c9082a;
    }
    
    /* データテーブル */
    .dataframe {
        background: #1d1d1d !important;
        color: #ffffff !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: #2d2d2d !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        padding: 1rem !important;
        border-bottom: 2px solid #c9082a !important;
    }
    
    .dataframe td {
        background: #1d1d1d !important;
        color: #e0e0e0 !important;
        border-bottom: 1px solid #2d2d2d !important;
        padding: 0.9rem !important;
        font-size: 0.95rem;
    }
    
    .dataframe tr:hover td {
        background: #252525 !important;
    }
    
    /* 統計カード */
    .stat-card-nba {
        background: linear-gradient(135deg, #1d1d1d 0%, #2d2d2d 100%);
        padding: 1.8rem;
        border-radius: 12px;
        border: 1px solid #2d2d2d;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .stat-card-nba:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(201, 8, 42, 0.2);
        border-color: #c9082a;
    }
    
    .stat-card-nba .stat-label {
        color: #a0a0a0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .stat-card-nba .stat-value {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1;
    }
    
    .stat-card-nba .stat-subtitle {
        color: #c9082a;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* セレクトボックス */
    .stSelectbox > div > div {
        background: #1d1d1d;
        border: 1px solid #2d2d2d;
        color: #ffffff;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #c9082a;
    }
    
    /* 日付入力 */
    .stDateInput > div > div {
        background: #1d1d1d;
        border: 1px solid #2d2d2d;
        color: #ffffff;
    }
    
    /* ボタン */
    .stButton > button {
        background: linear-gradient(135deg, #c9082a 0%, #a00622 100%);
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.8rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(201, 8, 42, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(201, 8, 42, 0.5);
        background: linear-gradient(135deg, #e00a30 0%, #c9082a 100%);
    }
    
    /* メトリック */
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a0a0a0;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    /* プレイヤーカード */
    .player-card {
        background: linear-gradient(135deg, #1d1d1d 0%, #252525 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #2d2d2d;
        margin-bottom: 2rem;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
    }
    
    .player-card .player-name {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .player-card .player-number {
        color: #c9082a;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* ランキングテーブル */
    .ranking-row {
        background: #1d1d1d;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        border-left: 4px solid #2d2d2d;
        transition: all 0.3s ease;
    }
    
    .ranking-row:hover {
        background: #252525;
        border-left-color: #c9082a;
        transform: translateX(8px);
    }
    
    .ranking-row.rank-1 {
        border-left-color: #ffd700;
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.1) 0%, #1d1d1d 100%);
    }
    
    .ranking-row.rank-2 {
        border-left-color: #c0c0c0;
        background: linear-gradient(90deg, rgba(192, 192, 192, 0.1) 0%, #1d1d1d 100%);
    }
    
    .ranking-row.rank-3 {
        border-left-color: #cd7f32;
        background: linear-gradient(90deg, rgba(205, 127, 50, 0.1) 0%, #1d1d1d 100%);
    }
    
    /* セクションヘッダー */
    .section-header {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 2px solid #2d2d2d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ファイルアップローダー */
    .stFileUploader > div {
        background: #1d1d1d;
        border: 2px dashed #2d2d2d;
        border-radius: 8px;
        padding: 2rem;
    }
    
    .stFileUploader > div:hover {
        border-color: #c9082a;
        background: #252525;
    }
    
    /* 入力フィールド */
    .stTextInput > div > div {
        background: #1d1d1d;
        border: 1px solid #2d2d2d;
        color: #ffffff;
    }
    
    .stNumberInput > div > div {
        background: #1d1d1d;
        border: 1px solid #2d2d2d;
        color: #ffffff;
    }
    
    /* スピナー */
    .stSpinner > div {
        border-top-color: #c9082a !important;
    }
    
    /* サクセスメッセージ */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1);
        border-left: 4px solid #00ff00;
        color: #ffffff;
    }
    
    /* エラーメッセージ */
    .stError {
        background: rgba(201, 8, 42, 0.1);
        border-left: 4px solid #c9082a;
        color: #ffffff;
    }
    
    /* インフォメッセージ */
    .stInfo {
        background: rgba(100, 149, 237, 0.1);
        border-left: 4px solid #6495ed;
        color: #ffffff;
    }
    
    /* Plotlyグラフ */
    .js-plotly-plot {
        border-radius: 12px;
        background: #1d1d1d;
    }
    
    /* スクロールバー */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1d1d1d;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c9082a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #e00a30;
    }
    
    /* データエディター */
    [data-testid="stDataFrameResizable"] {
        background: #1d1d1d;
        border: 1px solid #2d2d2d;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース初期化
# ========================================
def init_database():
    """データベースの初期化"""
    if 'database' not in st.session_state:
        st.session_state['database'] = pd.DataFrame(columns=[
            'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
            '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
            'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
            'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
        ])

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
    
    stats = {
        'GP': len(df),  # Games Played
        'PTS': df['PTS'].mean() if len(df) > 0 else 0,
        'REB': df['TOT'].mean() if len(df) > 0 else 0,
        'AST': df['AST'].mean() if len(df) > 0 else 0,
        'STL': df['STL'].mean() if len(df) > 0 else 0,
        'BLK': df['BLK'].mean() if len(df) > 0 else 0,
        'FG%': (df['3PM'].sum() + df['2PM'].sum()) / (df['3PA'].sum() + df['2PA'].sum()) * 100 if (df['3PA'].sum() + df['2PA'].sum()) > 0 else 0,
        '3P%': df['3PM'].sum() / df['3PA'].sum() * 100 if df['3PA'].sum() > 0 else 0,
        'FT%': df['FTM'].sum() / df['FTA'].sum() * 100 if df['FTA'].sum() > 0 else 0,
    }
    return stats

def create_nba_style_chart(data, title, x_col, y_col, color='#c9082a'):
    """NBA風のチャートを作成"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=10, color=color, line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor=f'rgba(201, 8, 42, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white', family='Arial Black')),
        plot_bgcolor='#1d1d1d',
        paper_bgcolor='#1d1d1d',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='#2d2d2d',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='#2d2d2d',
            showgrid=True,
            zeroline=False
        ),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=60, b=20),
        height=400
    )
    
    return fig

# ========================================
# メイン画面
# ========================================
def main():
    init_database()
    
    # ヘッダー
    st.markdown("""
    <div class="nba-header">
        <h1>🏀 TSUKUBA HIGHSCHOOL STATS</h1>
        <p class="subtitle">筑波大学附属高校男バススタッツ</p>
    </div>
    """, unsafe_allow_html=True)
    
    model, model_name = setup_gemini()
    
    # メインタブ（シーズン、選手、試合の順）
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 SEASON STATS", "👤 PLAYER STATS", "📊 GAME STATS", "📥 DATA INPUT"])
    
    # ========================================
    # タブ1: シーズン統計
    # ========================================
    with tab1:
        st.markdown('<div class="section-header">Season Statistics</div>', unsafe_allow_html=True)
        
        if st.session_state['database'].empty:
            st.info("📭 データがまだありません。DATA INPUTタブからデータを追加してください。")
        else:
            db = st.session_state['database']
            seasons = sorted(db['Season'].unique(), reverse=True)
            
            selected_season = st.selectbox("シーズンを選択", seasons, key='season_select')
            
            if selected_season:
                season_data = db[db['Season'] == selected_season]
                
                # サマリーメトリクス
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    games = len(season_data['GameDate'].unique())
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Games</div>
                        <div class="stat-value">{games}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    players = season_data['PlayerName'].nunique()
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Players</div>
                        <div class="stat-value">{players}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    avg_pts = season_data.groupby('GameDate')['PTS'].sum().mean()
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Avg PPG</div>
                        <div class="stat-value">{avg_pts:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    wins = len(season_data[season_data['TeamScore'] > season_data['OpponentScore']]['GameDate'].unique())
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Wins</div>
                        <div class="stat-value">{wins}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    losses = len(season_data[season_data['TeamScore'] < season_data['OpponentScore']]['GameDate'].unique())
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Losses</div>
                        <div class="stat-value">{losses}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('<div class="section-header">League Leaders</div>', unsafe_allow_html=True)
                
                # ランキング表示
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
                            <span style="color: #c9082a; font-size: 1.5rem; font-weight: 700; margin-right: 1rem;">#{idx}</span>
                            <span style="color: white; font-size: 1.2rem; font-weight: 600;">{player}</span>
                            <span style="float: right;">
                                <span style="color: #c9082a; font-size: 1.5rem; font-weight: 700;">{row['PPG']:.1f}</span>
                                <span style="color: #a0a0a0; font-size: 0.9rem;"> PPG ({row['GP']:.0f} GP)</span>
                            </span>
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
                            <span style="color: #c9082a; font-size: 1.5rem; font-weight: 700; margin-right: 1rem;">#{idx}</span>
                            <span style="color: white; font-size: 1.2rem; font-weight: 600;">{player}</span>
                            <span style="float: right;">
                                <span style="color: #c9082a; font-size: 1.5rem; font-weight: 700;">{row['RPG']:.1f}</span>
                                <span style="color: #a0a0a0; font-size: 0.9rem;"> RPG ({row['GP']:.0f} GP)</span>
                            </span>
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
                            <span style="color: #c9082a; font-size: 1.5rem; font-weight: 700; margin-right: 1rem;">#{idx}</span>
                            <span style="color: white; font-size: 1.2rem; font-weight: 600;">{player}</span>
                            <span style="float: right;">
                                <span style="color: #c9082a; font-size: 1.5rem; font-weight: 700;">{row['APG']:.1f}</span>
                                <span style="color: #a0a0a0; font-size: 0.9rem;"> APG ({row['GP']:.0f} GP)</span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                
                with ranking_tab4:
                    # 総合ランキングテーブル
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
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">PPG</div>
                        <div class="stat-value">{stats['PTS']:.1f}</div>
                        <div class="stat-subtitle">Points</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">RPG</div>
                        <div class="stat-value">{stats['REB']:.1f}</div>
                        <div class="stat-subtitle">Rebounds</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">APG</div>
                        <div class="stat-value">{stats['AST']:.1f}</div>
                        <div class="stat-subtitle">Assists</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">FG%</div>
                        <div class="stat-value">{stats['FG%']:.1f}</div>
                        <div class="stat-subtitle">Field Goal</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">GP</div>
                        <div class="stat-value">{stats['GP']}</div>
                        <div class="stat-subtitle">Games</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # グラフ
                st.markdown('<div class="section-header">Performance Charts</div>', unsafe_allow_html=True)
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    fig_pts = create_nba_style_chart(
                        player_data, 
                        'Points Per Game', 
                        'GameDate', 
                        'PTS'
                    )
                    st.plotly_chart(fig_pts, use_container_width=True)
                
                with chart_col2:
                    fig_reb = create_nba_style_chart(
                        player_data, 
                        'Rebounds Per Game', 
                        'GameDate', 
                        'TOT',
                        color='#17408B'
                    )
                    st.plotly_chart(fig_reb, use_container_width=True)
                
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
                result_color = "#00ff00" if result == "WIN" else "#c9082a" if result == "LOSS" else "#ffa500"
                
                st.markdown(f"""
                <div class="player-card" style="text-align: center;">
                    <div style="color: #a0a0a0; font-size: 1.2rem; margin-bottom: 1rem;">
                        {selected_game}
                    </div>
                    <div style="font-size: 2rem; color: white; margin-bottom: 1rem;">
                        筑波大附属 vs {opponent}
                    </div>
                    <div style="font-size: 3rem; font-weight: 800; color: white;">
                        {team_score} - {opp_score}
                    </div>
                    <div style="color: {result_color}; font-size: 1.5rem; font-weight: 700; margin-top: 1rem;">
                        {result}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # チームスタッツ
                st.markdown('<div class="section-header">Team Statistics</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    total_pts = game_data['PTS'].sum()
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Total Points</div>
                        <div class="stat-value">{total_pts}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    total_reb = game_data['TOT'].sum()
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Total Rebounds</div>
                        <div class="stat-value">{total_reb}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    total_ast = game_data['AST'].sum()
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">Total Assists</div>
                        <div class="stat-value">{total_ast}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    fg_pct = (game_data['3PM'].sum() + game_data['2PM'].sum()) / (game_data['3PA'].sum() + game_data['2PA'].sum()) * 100 if (game_data['3PA'].sum() + game_data['2PA'].sum()) > 0 else 0
                    st.markdown(f"""
                    <div class="stat-card-nba">
                        <div class="stat-label">FG%</div>
                        <div class="stat-value">{fg_pct:.1f}%</div>
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
    # タブ4: データ入力
    # ========================================
    with tab4:
        st.markdown('<div class="section-header">Data Input</div>', unsafe_allow_html=True)
        
        if not model:
            st.error("⚠️ Gemini APIキーが設定されていません。")
            return
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 試合情報")
            game_date = st.date_input("試合日", datetime.now())
            season = st.selectbox("シーズン", ["2023-24", "2024-25", "2025-26", "2026-27"], index=1)
            opponent = st.text_input("対戦相手", "")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                team_score = st.number_input("筑波大附属", min_value=0, value=0)
            with col_s2:
                opponent_score = st.number_input("相手スコア", min_value=0, value=0)
            
            st.markdown("#### スコアシート画像")
            uploaded_file = st.file_uploader(
                "画像をアップロード",
                type=['png', 'jpg', 'jpeg', 'webp']
            )
        
        with col2:
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)
                
                if st.button("🚀 AI解析実行", use_container_width=True, type="primary"):
                    with st.spinner("解析中..."):
                        try:
                            prompt = """
この画像からバスケットボールのスコアシートデータを抽出してください。
以下の形式のCSVで出力してください（ヘッダー行を含む）：

No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN

注意事項：
- GSは先発選手の場合「●」があれば1、なければ0
- パーセンテージは数値のみ（%記号不要）
- MINは「32:38」のような形式で
- 数値がない場合は0を入力
- Team/Coachesの行は除外
- TOTALSの行は除外

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
                            st.success("✅ 解析完了")
                            
                        except Exception as e:
                            st.error(f"❌ エラー: {str(e)}")
        
        # 解析結果の編集
        if 'current_stats' in st.session_state:
            st.markdown('<div class="section-header">データ確認・編集</div>', unsafe_allow_html=True)
            
            edited_df = st.data_editor(
                st.session_state['current_stats'],
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("💾 保存", use_container_width=True, type="primary"):
                    st.session_state['database'] = pd.concat(
                        [st.session_state['database'], edited_df],
                        ignore_index=True
                    )
                    st.success("✅ 保存完了")
                    del st.session_state['current_stats']
                    st.rerun()
            
            with col2:
                if st.button("🗑️ キャンセル", use_container_width=True):
                    del st.session_state['current_stats']
                    st.rerun()

if __name__ == "__main__":
    main()
