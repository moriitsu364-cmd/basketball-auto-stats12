"""NBA.com + Bリーグ風の高度なスタイル定義"""
import streamlit as st


def load_css():
    """CSSスタイルを読み込む"""
    st.markdown("""
    <style>
        /* ============================================
           グローバル設定
           ============================================ */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Roboto:wght@400;500;700;900&display=swap');
        
        * {
            font-family: 'Roboto', 'Noto Sans JP', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        .main {
            background: transparent;
        }
        
        .block-container {
            padding: 1rem 2rem;
            max-width: 1600px;
        }
        
        /* ============================================
           ヘッダー - NBA.com風
           ============================================ */
        .nba-header {
            background: linear-gradient(135deg, #000000 0%, #1d428a 50%, #c8102e 100%);
            padding: 3rem 2rem;
            margin: -1rem -2rem 2rem -2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
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
            background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="40" fill="white" opacity="0.02"/></svg>');
            background-size: 100px 100px;
            animation: slide 20s linear infinite;
        }
        
        @keyframes slide {
            0% { background-position: 0 0; }
            100% { background-position: 100px 100px; }
        }
        
        .nba-header h1 {
            color: white;
            font-size: 3.5rem;
            font-weight: 900;
            margin: 0;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            position: relative;
            z-index: 1;
        }
        
        .nba-header .subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2rem;
            margin-top: 1rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }
        
        /* ============================================
           ナビゲーションタブ - モダンデザイン
           ============================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
            border-bottom: 3px solid #c8102e;
            padding: 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #212529;
            font-weight: 700;
            font-size: 1rem;
            padding: 1.2rem 2.5rem;
            border: none;
            border-bottom: 4px solid transparent;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .stTabs [data-baseweb="tab"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(180deg, transparent 0%, rgba(29, 66, 138, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #c8102e;
            border-bottom-color: #c8102e;
        }
        
        .stTabs [data-baseweb="tab"]:hover::before {
            opacity: 1;
        }
        
        .stTabs [aria-selected="true"] {
            color: #ffffff;
            border-bottom-color: #c8102e;
            background: linear-gradient(180deg, rgba(29, 66, 138, 0.8) 0%, rgba(200, 16, 46, 0.7) 100%);
        }
        
        /* ============================================
           統計カード - NBA.com風
           ============================================ */
        .stat-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2rem 1.5rem;
            border-radius: 8px;
            border: 2px solid #dee2e6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            margin-bottom: 1rem;
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
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(200, 16, 46, 0.2);
            border-color: #c8102e;
        }
        
        .stat-card .stat-label {
            color: #6c757d;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.8rem;
        }
        
        .stat-card .stat-value {
            color: #212529;
            font-size: 3rem;
            font-weight: 900;
            line-height: 1;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stat-card.primary .stat-value {
            background: linear-gradient(135deg, #1d428a 0%, #4169e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-card.secondary .stat-value {
            background: linear-gradient(135deg, #c8102e 0%, #ff4757 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-card .stat-subtitle {
            color: #6c757d;
            font-size: 0.9rem;
            margin-top: 0.8rem;
            font-weight: 500;
        }
        
        /* ============================================
           選手カード - 半透明画像背景
           ============================================ */
        .player-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 3rem 2rem;
            border-radius: 12px;
            border: 2px solid #dee2e6;
            margin-bottom: 2rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .player-card::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            bottom: 0;
            width: 50%;
            background: linear-gradient(90deg, transparent 0%, rgba(29, 66, 138, 0.03) 100%);
        }
        
        .player-card-image {
            position: absolute;
            right: -50px;
            top: 50%;
            transform: translateY(-50%);
            width: 400px;
            height: 400px;
            opacity: 0.08;
            filter: grayscale(30%);
            z-index: 0;
        }
        
        .player-card-content {
            position: relative;
            z-index: 1;
        }
        
        .player-card .player-name {
            color: #212529;
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .player-card .player-number {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 6rem;
            font-weight: 900;
            line-height: 1;
            display: inline-block;
        }
        
        /* ============================================
           ランキング行 - 画像アイコン付き
           ============================================ */
        .ranking-row {
            background: linear-gradient(90deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1.2rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 0.8rem;
            border: 2px solid #dee2e6;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }
        
        .ranking-row::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            background: #adb5bd;
        }
        
        .ranking-row:hover {
            transform: translateX(8px);
            box-shadow: 0 4px 20px rgba(200, 16, 46, 0.2);
            border-color: #c8102e;
        }
        
        .ranking-row.rank-1::before {
            background: linear-gradient(180deg, #ffd700 0%, #ffed4e 100%);
        }
        
        .ranking-row.rank-2::before {
            background: linear-gradient(180deg, #c0c0c0 0%, #e8e8e8 100%);
        }
        
        .ranking-row.rank-3::before {
            background: linear-gradient(180deg, #cd7f32 0%, #e8a87c 100%);
        }
        
        .ranking-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 3px solid #dee2e6;
            margin-right: 1rem;
            object-fit: cover;
        }
        
        .ranking-row.rank-1 .ranking-avatar {
            border-color: #ffd700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }
        
        .ranking-row.rank-2 .ranking-avatar {
            border-color: #c0c0c0;
        }
        
        .ranking-row.rank-3 .ranking-avatar {
            border-color: #cd7f32;
        }
        
        /* ============================================
           セクションヘッダー - 日英バイリンガル
           ============================================ */
        .section-header {
            color: #212529;
            font-size: 2rem;
            font-weight: 900;
            margin: 3rem 0 1.5rem 0;
            padding-bottom: 1rem;
            border-bottom: 3px solid #c8102e;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
        }
        
        .section-header::before {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 100px;
            height: 3px;
            background: #1d428a;
        }
        
        .section-header-jp {
            font-size: 1rem;
            color: #6c757d;
            font-weight: 500;
            margin-top: 0.5rem;
            letter-spacing: 1px;
        }
        
        /* ============================================
           データテーブル - ダークテーマ
           ============================================ */
        .dataframe {
            background: #ffffff !important;
            border: 2px solid #dee2e6 !important;
            border-radius: 8px;
            font-size: 0.95rem;
        }
        
        .dataframe th {
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%) !important;
            color: #212529 !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
            padding: 1.2rem 1rem !important;
            border-bottom: 2px solid #c8102e !important;
        }
        
        .dataframe td {
            background: #ffffff !important;
            color: #212529 !important;
            border-bottom: 1px solid #dee2e6 !important;
            padding: 1rem !important;
        }
        
        .dataframe tr:hover td {
            background: #f8f9fa !important;
        }
        
        /* ============================================
           入力フィールド - ダークテーマ
           ============================================ */
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stDateInput > div > div {
            background: #ffffff;
            border: 2px solid #dee2e6;
            color: #212529;
            border-radius: 6px;
        }
        
        .stSelectbox > div > div:focus,
        .stTextInput > div > div:focus,
        .stNumberInput > div > div:focus,
        .stDateInput > div > div:focus {
            border-color: #c8102e;
            box-shadow: 0 0 10px rgba(200, 16, 46, 0.2);
        }
        
        /* ============================================
           ボタン - NBA風
           ============================================ */
        .stButton > button {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 1rem 2rem;
            font-weight: 700;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(200, 16, 46, 0.5);
        }
        
        .stButton > button[kind="secondary"] {
            background: transparent;
            border: 2px solid #c8102e;
            color: #c8102e;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(200, 16, 46, 0.1);
        }
        
        /* ============================================
           グラフコンテナ
           ============================================ */
        .js-plotly-plot {
            border-radius: 8px;
            background: #ffffff;
            border: 2px solid #dee2e6;
            padding: 1rem;
        }
        
        /* ============================================
           ゲームカード
           ============================================ */
        .game-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2.5rem 2rem;
            border-radius: 12px;
            border: 2px solid #dee2e6;
            margin-bottom: 2rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .game-card .game-date {
            color: #6c757d;
            font-size: 1rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 1.5rem;
            letter-spacing: 2px;
        }
        
        .game-card .teams {
            font-size: 2rem;
            color: #212529;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }
        
        .game-card .score {
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 1.5rem 0;
        }
        
        .game-card .result {
            font-size: 1.5rem;
            font-weight: 900;
            padding: 0.8rem 2rem;
            border-radius: 50px;
            display: inline-block;
            margin-top: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .game-card .result.win {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);
        }
        
        .game-card .result.loss {
            background: linear-gradient(135deg, #dc3545 0%, #f8d7da 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
        }
        
        /* ============================================
           ファイルアップローダー
           ============================================ */
        .stFileUploader > div {
            background: #ffffff;
            border: 3px dashed #adb5bd;
            border-radius: 8px;
            padding: 3rem;
            transition: all 0.3s ease;
        }
        
        .stFileUploader > div:hover {
            border-color: #c8102e;
            background: #f8f9fa;
        }
        
        /* ============================================
           メッセージ - ダークテーマ
           ============================================ */
        .stSuccess {
            background: rgba(40, 167, 69, 0.1);
            border-left: 4px solid #28a745;
            color: #155724;
            border-radius: 6px;
        }
        
        .stError {
            background: rgba(220, 53, 69, 0.1);
            border-left: 4px solid #dc3545;
            color: #721c24;
            border-radius: 6px;
        }
        
        .stInfo {
            background: rgba(23, 162, 184, 0.1);
            border-left: 4px solid #17a2b8;
            color: #0c5460;
            border-radius: 6px;
        }
        
        /* ============================================
           レスポンシブ
           ============================================ */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
            
            .nba-header h1 {
                font-size: 2rem;
            }
            
            .stat-card .stat-value {
                font-size: 2rem;
            }
            
            .player-card .player-name {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
