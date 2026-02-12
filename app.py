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
import hashlib
import base64
from pathlib import Path

# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="Tsukuba Basketball Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# 画像管理ディレクトリ
# ========================================
IMAGES_DIR = Path("player_images")
IMAGES_DIR.mkdir(exist_ok=True)

# ========================================
# 認証機能（強化版）
# ========================================
def check_admin_password():
    """管理者権限の確認"""
    def password_entered():
        if hashlib.sha256(st.session_state["admin_password"].encode()).hexdigest() == st.secrets.get("ADMIN_PASSWORD_HASH", hashlib.sha256("tsukuba1872admin".encode()).hexdigest()):
            st.session_state["admin_authenticated"] = True
            del st.session_state["admin_password"]
        else:
            st.session_state["admin_authenticated"] = False

    if st.session_state.get("admin_authenticated", False):
        return True

    st.markdown("""
    <div style="max-width: 500px; margin: 100px auto; padding: 40px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color: #1d428a; text-align: center; margin-bottom: 30px;">🔒 ADMIN ACCESS REQUIRED</h2>
        <p style="text-align: center; color: #6c757d;">This section requires administrator privileges</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "Enter Admin Password",
            type="password",
            on_change=password_entered,
            key="admin_password",
        )
        if "admin_authenticated" in st.session_state and not st.session_state["admin_authenticated"]:
            st.error("❌ Incorrect password")
        
        st.info("💡 Default password: tsukuba1872admin")
        st.caption("Set ADMIN_PASSWORD_HASH in secrets.toml for custom password")
    
    return False

# ========================================
# NBA.comスタイルのカスタムCSS（強化版）
# ========================================
def load_css():
    st.markdown("""
    <style>
        /* 全体の背景 */
        .stApp {
            background: #f5f5f5;
        }
        
        /* メインコンテナ */
        .main {
            background: #f5f5f5;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .block-container {
            padding: 2rem 3rem;
            max-width: 1600px;
        }
        
        /* ヘッダー - NBA.comスタイル */
        .nba-header {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            padding: 2.5rem 3rem;
            margin: -2rem -3rem 2rem -3rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            position: relative;
            overflow: hidden;
        }
        
        .nba-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.03)"/></svg>');
            background-size: 200px;
            opacity: 0.5;
        }
        
        .nba-header h1 {
            color: white;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            letter-spacing: -1px;
            font-family: 'Arial Black', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }
        
        .nba-header .subtitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.1rem;
            margin-top: 0.5rem;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }
        
        /* ナビゲーションタブ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: white;
            border-bottom: 3px solid #e5e5e5;
            padding: 0 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #6c757d;
            font-weight: 700;
            font-size: 0.95rem;
            padding: 1.2rem 2rem;
            border: none;
            border-bottom: 4px solid transparent;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #1d428a;
            border-bottom-color: rgba(29, 66, 138, 0.3);
            background: rgba(29, 66, 138, 0.03);
        }
        
        .stTabs [aria-selected="true"] {
            color: #1d428a;
            border-bottom-color: #1d428a;
            background: transparent;
        }
        
        /* データテーブル */
        .dataframe {
            background: white !important;
            border: 1px solid #e5e5e5 !important;
            border-radius: 8px;
            font-size: 0.9rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .dataframe th {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%) !important;
            color: #212529 !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
            padding: 1.2rem 1rem !important;
            border-bottom: 2px solid #dee2e6 !important;
        }
        
        .dataframe td {
            background: white !important;
            color: #212529 !important;
            border-bottom: 1px solid #f0f0f0 !important;
            padding: 1rem !important;
            font-weight: 500;
        }
        
        .dataframe tr:hover td {
            background: #f8f9fa !important;
            transition: all 0.2s ease;
        }
        
        /* 統計カード */
        .stat-card {
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stat-card:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-4px);
        }
        
        .stat-card:hover::before {
            opacity: 1;
        }
        
        .stat-card .stat-label {
            color: #6c757d;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 0.8rem;
        }
        
        .stat-card .stat-value {
            color: #212529;
            font-size: 3rem;
            font-weight: 800;
            line-height: 1;
            margin: 0.5rem 0;
        }
        
        .stat-card.primary .stat-value {
            background: linear-gradient(135deg, #1d428a 0%, #2563eb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-card.secondary .stat-value {
            background: linear-gradient(135deg, #c8102e 0%, #dc2626 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-card .stat-subtitle {
            color: #6c757d;
            font-size: 0.85rem;
            margin-top: 0.5rem;
            font-weight: 500;
        }
        
        /* プレイヤーカード（画像付き） */
        .player-card {
            background: white;
            padding: 0;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            margin-bottom: 2rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            overflow: hidden;
            position: relative;
        }
        
        .player-card-header {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            padding: 3rem 2rem 6rem 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .player-card-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.05)"/></svg>');
            background-size: 150px;
        }
        
        .player-image-container {
            position: absolute;
            right: 2rem;
            bottom: -2rem;
            width: 200px;
            height: 200px;
            opacity: 0.3;
            filter: brightness(1.2);
        }
        
        .player-image-container img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        
        .player-card .player-number {
            color: white;
            font-size: 1.5rem;
            font-weight: 800;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .player-card .player-name {
            color: white;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0.5rem 0;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .player-card-body {
            padding: 2rem;
        }
        
        /* ランキング行（画像付き） */
        .ranking-row {
            background: white;
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 0.8rem;
            border: 1px solid #e5e5e5;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .ranking-row:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateX(8px);
            border-color: #1d428a;
        }
        
        .ranking-row.rank-1 {
            border-left: 5px solid #ffd700;
            background: linear-gradient(90deg, rgba(255, 215, 0, 0.08) 0%, white 100%);
        }
        
        .ranking-row.rank-2 {
            border-left: 5px solid #c0c0c0;
            background: linear-gradient(90deg, rgba(192, 192, 192, 0.08) 0%, white 100%);
        }
        
        .ranking-row.rank-3 {
            border-left: 5px solid #cd7f32;
            background: linear-gradient(90deg, rgba(205, 127, 50, 0.08) 0%, white 100%);
        }
        
        .ranking-player-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .ranking-player-image {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #e5e5e5;
        }
        
        /* セクションヘッダー */
        .section-header {
            color: #212529;
            font-size: 1.8rem;
            font-weight: 800;
            margin: 3rem 0 1.5rem 0;
            padding-bottom: 1rem;
            border-bottom: 3px solid #1d428a;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 100px;
            height: 3px;
            background: #c8102e;
        }
        
        /* ボタン */
        .stButton > button {
            background: linear-gradient(135deg, #1d428a 0%, #17396e 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.9rem 2rem;
            font-weight: 700;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(29, 66, 138, 0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #17396e 0%, #1d428a 100%);
            box-shadow: 0 6px 20px rgba(29, 66, 138, 0.4);
            transform: translateY(-2px);
        }
        
        /* ゲームカード */
        .game-card {
            background: white;
            padding: 2.5rem;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            margin-bottom: 2rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .game-card:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-4px);
        }
        
        .game-card .game-date {
            color: #6c757d;
            font-size: 0.95rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 1.5rem;
            letter-spacing: 1px;
        }
        
        .game-card .teams {
            font-size: 1.8rem;
            color: #212529;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        
        .game-card .score {
            font-size: 3.5rem;
            font-weight: 800;
            color: #212529;
            margin: 1.5rem 0;
            font-family: 'Arial Black', sans-serif;
        }
        
        .game-card .result {
            font-size: 1.3rem;
            font-weight: 800;
            padding: 0.8rem 2rem;
            border-radius: 8px;
            display: inline-block;
            margin-top: 1rem;
            letter-spacing: 2px;
        }
        
        .game-card .result.win {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        }
        
        .game-card .result.loss {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
        }
        
        /* フィルターカード */
        .filter-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #e5e5e5;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* チャートコンテナ */
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
        }
        
        /* 比較カード */
        .comparison-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #e5e5e5;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* レスポンシブ */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
            
            .nba-header {
                padding: 1.5rem 1rem;
                margin: -1rem -1rem 1.5rem -1rem;
            }
            
            .nba-header h1 {
                font-size: 2rem;
            }
            
            .stat-card .stat-value {
                font-size: 2rem;
            }
            
            .player-image-container {
                width: 120px;
                height: 120px;
            }
        }
        
        /* 画像アップロード */
        .image-upload-zone {
            border: 3px dashed #1d428a;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            background: rgba(29, 66, 138, 0.02);
            transition: all 0.3s ease;
        }
        
        .image-upload-zone:hover {
            background: rgba(29, 66, 138, 0.05);
            border-color: #c8102e;
        }
    </style>
    """, unsafe_allow_html=True)

# ========================================
# データベース関連（拡張版）
# ========================================
DATA_FILE = "basketball_stats.csv"
TEAM_INFO_FILE = "team_info.json"
PLAYER_INFO_FILE = "player_info.json"

def init_database():
    """データベースの初期化"""
    if 'database' not in st.session_state:
        if os.path.exists(DATA_FILE):
            try:
                st.session_state['database'] = pd.read_csv(DATA_FILE)
            except Exception as e:
                st.error(f"Data loading error: {e}")
                st.session_state['database'] = create_empty_dataframe()
        else:
            st.session_state['database'] = create_empty_dataframe()
    
    # チーム情報の初期化
    if 'team_info' not in st.session_state:
        if os.path.exists(TEAM_INFO_FILE):
            try:
                with open(TEAM_INFO_FILE, 'r', encoding='utf-8') as f:
                    st.session_state['team_info'] = json.load(f)
            except:
                st.session_state['team_info'] = {}
        else:
            st.session_state['team_info'] = {}
    
    # 選手情報の初期化
    if 'player_info' not in st.session_state:
        if os.path.exists(PLAYER_INFO_FILE):
            try:
                with open(PLAYER_INFO_FILE, 'r', encoding='utf-8') as f:
                    st.session_state['player_info'] = json.load(f)
            except:
                st.session_state['player_info'] = {}
        else:
            st.session_state['player_info'] = {}

def create_empty_dataframe():
    """空のデータフレームを作成"""
    return pd.DataFrame(columns=[
        'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
        '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
        'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
        'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
        'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore',
        'QuarterSystem'  # 新規追加: 2Q, 4Q など
    ])

def save_database():
    """データベースを保存"""
    try:
        st.session_state['database'].to_csv(DATA_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
        return False

def save_team_info():
    """チーム情報を保存"""
    try:
        with open(TEAM_INFO_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state['team_info'], f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Team info save error: {e}")
        return False

def save_player_info():
    """選手情報を保存"""
    try:
        with open(PLAYER_INFO_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state['player_info'], f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Player info save error: {e}")
        return False

def get_player_image_base64(player_name, image_type="pose"):
    """選手画像をBase64で取得"""
    image_path = IMAGES_DIR / f"{player_name}_{image_type}.png"
    if image_path.exists():
        try:
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except:
            pass
    return None

def save_player_image(player_name, image_file, image_type="pose"):
    """選手画像を保存"""
    try:
        image = Image.open(image_file)
        image_path = IMAGES_DIR / f"{player_name}_{image_type}.png"
        image.save(image_path)
        return True
    except Exception as e:
        st.error(f"Image save error: {e}")
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
            'models/gemini-1.5-flash'
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
        st.error(f"Gemini API setup error: {e}")
        return None, None

# ========================================
# 統計計算関数（拡張版）
# ========================================
def calculate_stats(df, player_name=None, season=None):
    """統計を計算"""
    if player_name:
        df = df[df['PlayerName'] == player_name]
    if season:
        df = df[df['Season'] == season]
    
    if len(df) == 0:
        return {
            'GP': 0, 'PTS': 0, 'REB': 0, 'AST': 0, 'STL': 0, 'BLK': 0,
            'FG%': 0, '3P%': 0, 'FT%': 0, 'TO': 0, 'PF': 0,
            'MPG': 0, 'OR': 0, 'DR': 0
        }
    
    stats = {
        'GP': len(df),
        'PTS': df['PTS'].mean(),
        'REB': df['TOT'].mean(),
        'OR': df['OR'].mean(),
        'DR': df['DR'].mean(),
        'AST': df['AST'].mean(),
        'STL': df['STL'].mean(),
        'BLK': df['BLK'].mean(),
        'TO': df['TO'].mean(),
        'PF': df['PF'].mean(),
        'FG%': (df['3PM'].sum() + df['2PM'].sum()) / (df['3PA'].sum() + df['2PA'].sum()) * 100 if (df['3PA'].sum() + df['2PA'].sum()) > 0 else 0,
        '3P%': df['3PM'].sum() / df['3PA'].sum() * 100 if df['3PA'].sum() > 0 else 0,
        'FT%': df['FTM'].sum() / df['FTA'].sum() * 100 if df['FTA'].sum() > 0 else 0,
        'MPG': df['MIN'].apply(lambda x: convert_min_to_seconds(x) / 60 if pd.notna(x) else 0).mean()
    }
    return stats

def convert_min_to_seconds(min_str):
    """MIN形式（MM:SS）を秒に変換"""
    try:
        if isinstance(min_str, str) and ':' in min_str:
            parts = min_str.split(':')
            return int(parts[0]) * 60 + int(parts[1])
        return 0
    except:
        return 0

def create_bar_chart(data, x, y, title, color='#1d428a'):
    """棒グラフを作成"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data[x],
        y=data[y],
        marker=dict(
            color=color,
            line=dict(color=color, width=1)
        ),
        text=data[y].round(1),
        textposition='outside',
        textfont=dict(size=12, color='#212529', family='Arial', weight='bold')
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='#212529', family='Arial', weight='bold')),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#212529'),
        xaxis=dict(
            gridcolor='#f0f0f0',
            showgrid=False,
            zeroline=False,
            title=None
        ),
        yaxis=dict(
            gridcolor='#f0f0f0',
            showgrid=True,
            zeroline=False,
            title=None
        ),
        margin=dict(l=40, r=40, t=60, b=80),
        height=400
    )
    
    return fig

def create_pie_chart(labels, values, title):
    """円グラフを作成"""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=['#1d428a', '#c8102e', '#2563eb', '#dc2626', '#059669']),
        textinfo='label+percent',
        textfont=dict(size=14, color='white', family='Arial', weight='bold')
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='#212529', family='Arial', weight='bold')),
        paper_bgcolor='white',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_line_chart(data, x, y_cols, title, colors=None):
    """複数系列の折れ線グラフを作成"""
    if colors is None:
        colors = ['#1d428a', '#c8102e', '#2563eb', '#dc2626', '#059669']
    
    fig = go.Figure()
    
    for idx, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=data[x],
            y=data[y_col],
            mode='lines+markers',
            name=y_col,
            line=dict(color=colors[idx % len(colors)], width=3),
            marker=dict(size=8, color=colors[idx % len(colors)])
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color='#212529', family='Arial', weight='bold')),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#212529'),
        xaxis=dict(
            gridcolor='#f0f0f0',
            showgrid=True,
            zeroline=False,
            title=None
        ),
        yaxis=dict(
            gridcolor='#f0f0f0',
            showgrid=True,
            zeroline=False,
            title=None
        ),
        hovermode='x unified',
