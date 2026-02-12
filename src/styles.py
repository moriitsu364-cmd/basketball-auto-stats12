"""スタイル定義"""
import streamlit as st


def load_css():
    """CSSスタイルを読み込む"""
    st.markdown("""
    <style>
        /* 全体の背景 */
        .stApp {
            background: #f5f5f5;
        }
        
        /* メインコンテナ */
        .main {
            background: #f5f5f5;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* ヘッダー - NBAスタイル */
        .nba-header {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            padding: 2rem 3rem;
            margin: -2rem -3rem 2rem -3rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .nba-header h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
            font-family: 'Arial Black', sans-serif;
        }
        
        .nba-header .subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            margin-top: 0.5rem;
            font-weight: 400;
        }
        
        /* ナビゲーションタブ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: white;
            border-bottom: 2px solid #e5e5e5;
            padding: 0 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #6c757d;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 1rem 2rem;
            border: none;
            border-bottom: 3px solid transparent;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            transition: all 0.2s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #1d428a;
            border-bottom-color: #1d428a;
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
            border-radius: 4px;
            font-size: 0.9rem;
        }
        
        .dataframe th {
            background: #f8f9fa !important;
            color: #212529 !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
            padding: 1rem 0.75rem !important;
            border-bottom: 2px solid #e5e5e5 !important;
        }
        
        .dataframe td {
            background: white !important;
            color: #212529 !important;
            border-bottom: 1px solid #f0f0f0 !important;
            padding: 0.875rem 0.75rem !important;
        }
        
        .dataframe tr:hover td {
            background: #f8f9fa !important;
        }
        
        /* 統計カード */
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 4px;
            border: 1px solid #e5e5e5;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
            margin-bottom: 1rem;
            text-align: center;
        }
        
        .stat-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .stat-card .stat-label {
            color: #6c757d;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        
        .stat-card .stat-value {
            color: #212529;
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1;
        }
        
        .stat-card.primary .stat-value {
            color: #1d428a;
        }
        
        .stat-card.secondary .stat-value {
            color: #c8102e;
        }
        
        .stat-card .stat-subtitle {
            color: #6c757d;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        /* セレクトボックス */
        .stSelectbox > div > div {
            background: white;
            border: 1px solid #e5e5e5;
            color: #212529;
            border-radius: 4px;
        }
        
        /* 入力フィールド */
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stDateInput > div > div {
            background: white;
            border: 1px solid #e5e5e5;
            color: #212529;
            border-radius: 4px;
        }
        
        /* ボタン */
        .stButton > button {
            background: #1d428a;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background: #17396e;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-1px);
        }
        
        .stButton > button[kind="secondary"] {
            background: white;
            color: #1d428a;
            border: 1px solid #1d428a;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: #f8f9fa;
        }
        
        /* プレイヤーカード */
        .player-card {
            background: white;
            padding: 2rem;
            border-radius: 4px;
            border: 1px solid #e5e5e5;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .player-card .player-name {
            color: #212529;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .player-card .player-number {
            color: #1d428a;
            font-size: 1.25rem;
            font-weight: 700;
        }
        
        /* ランキング行 */
        .ranking-row {
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            border: 1px solid #e5e5e5;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .ranking-row:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transform: translateX(4px);
        }
        
        .ranking-row.rank-1 {
            border-left: 4px solid #ffd700;
            background: linear-gradient(90deg, rgba(255, 215, 0, 0.05) 0%, white 100%);
        }
        
        .ranking-row.rank-2 {
            border-left: 4px solid #c0c0c0;
            background: linear-gradient(90deg, rgba(192, 192, 192, 0.05) 0%, white 100%);
        }
        
        .ranking-row.rank-3 {
            border-left: 4px solid #cd7f32;
            background: linear-gradient(90deg, rgba(205, 127, 50, 0.05) 0%, white 100%);
        }
        
        /* セクションヘッダー */
        .section-header {
            color: #212529;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e5e5e5;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* ファイルアップローダー */
        .stFileUploader > div {
            background: white;
            border: 2px dashed #e5e5e5;
            border-radius: 4px;
            padding: 2rem;
        }
        
        .stFileUploader > div:hover {
            border-color: #1d428a;
            background: #f8f9fa;
        }
        
        /* メッセージ */
        .stSuccess {
            background: #d4edda;
            border-left: 4px solid #28a745;
            color: #155724;
            border-radius: 4px;
        }
        
        .stError {
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            color: #721c24;
            border-radius: 4px;
        }
        
        .stInfo {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            color: #0c5460;
            border-radius: 4px;
        }
        
        .stWarning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            color: #856404;
            border-radius: 4px;
        }
        
        /* Plotlyグラフ */
        .js-plotly-plot {
            border-radius: 4px;
            background: white;
            border: 1px solid #e5e5e5;
        }
        
        /* データエディター */
        [data-testid="stDataFrameResizable"] {
            background: white;
            border: 1px solid #e5e5e5;
            border-radius: 4px;
        }
        
        /* ゲームカード */
        .game-card {
            background: white;
            padding: 2rem;
            border-radius: 4px;
            border: 1px solid #e5e5e5;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        .game-card .game-date {
            color: #6c757d;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        
        .game-card .teams {
            font-size: 1.5rem;
            color: #212529;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .game-card .score {
            font-size: 3rem;
            font-weight: 700;
            color: #212529;
            margin: 1rem 0;
        }
        
        .game-card .result {
            font-size: 1.25rem;
            font-weight: 700;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            display: inline-block;
            margin-top: 1rem;
        }
        
        .game-card .result.win {
            background: #d4edda;
            color: #28a745;
        }
        
        .game-card .result.loss {
            background: #f8d7da;
            color: #dc3545;
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
                font-size: 1.75rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 0.75rem 1rem;
                font-size: 0.85rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
