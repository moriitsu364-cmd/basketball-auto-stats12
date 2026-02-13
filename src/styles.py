"""NBA.com inspired sophisticated design - Tsukuba Basketball"""
import streamlit as st


def load_css():
    """Load sophisticated CSS styles inspired by NBA.com"""
    st.markdown("""
    <style>
        /* ============================================
           Global Configuration
           ============================================ */
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700;900&display=swap');
        
        * {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
        }
        
        .stApp {
            background: #000000;
        }
        
        .main {
            background: transparent;
        }
        
        .block-container {
            padding: 1rem 2rem;
            max-width: 1800px;
        }
        
        /* ============================================
           Header - Premium Dark Design
           ============================================ */
        .nba-header {
            background: linear-gradient(180deg, #000000 0%, #0a0a0a 50%, #1a1a1a 100%);
            padding: 4rem 2rem;
            margin: -1rem -2rem 2rem -2rem;
            position: relative;
            overflow: hidden;
            border-bottom: 1px solid #2a2a2a;
        }
        
        .nba-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(200, 16, 46, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(29, 66, 138, 0.15) 0%, transparent 50%);
            animation: pulse 8s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }
        
        .nba-header h1 {
            color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 5rem;
            font-weight: 400;
            margin: 0;
            letter-spacing: 8px;
            text-transform: uppercase;
            position: relative;
            z-index: 1;
            background: linear-gradient(135deg, #ffffff 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nba-header .subtitle {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1rem;
            margin-top: 1rem;
            font-weight: 400;
            position: relative;
            z-index: 1;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        
        /* ============================================
           Navigation Tabs - Modern Dark Theme
           ============================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
            border-bottom: 1px solid #2a2a2a;
            padding: 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: rgba(255, 255, 255, 0.5);
            font-weight: 600;
            font-size: 0.85rem;
            padding: 1.5rem 2.5rem;
            border: none;
            border-bottom: 2px solid transparent;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        
        .stTabs [data-baseweb="tab"]::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%) scaleX(0);
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: rgba(255, 255, 255, 0.9);
        }
        
        .stTabs [data-baseweb="tab"]:hover::after {
            transform: translateX(-50%) scaleX(1);
        }
        
        .stTabs [aria-selected="true"] {
            color: #ffffff;
            background: rgba(200, 16, 46, 0.1);
        }
        
        .stTabs [aria-selected="true"]::after {
            transform: translateX(-50%) scaleX(1);
        }
        
        /* ============================================
           Statistics Cards - Premium Design
           ============================================ */
        .stat-card {
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
            padding: 2.5rem 2rem;
            border-radius: 12px;
            border: 1px solid #2a2a2a;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #c8102e 50%, transparent 100%);
        }
        
        .stat-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 16px 48px rgba(200, 16, 46, 0.3);
            border-color: rgba(200, 16, 46, 0.5);
        }
        
        .stat-card .stat-label {
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 1rem;
        }
        
        .stat-card .stat-value {
            color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 4rem;
            font-weight: 400;
            line-height: 1;
            letter-spacing: 2px;
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
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9rem;
            margin-top: 1rem;
            font-weight: 400;
        }
        
        /* ============================================
           Player Cards - Sophisticated Layout
           ============================================ */
        .player-card {
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
            padding: 3rem 2.5rem;
            border-radius: 16px;
            border: 1px solid #2a2a2a;
            margin-bottom: 2rem;
            box-shadow: 0 12px 40px rgba(0,0,0,0.6);
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
            background: radial-gradient(circle at center right, rgba(200, 16, 46, 0.08) 0%, transparent 70%);
        }
        
        .player-card-content {
            position: relative;
            z-index: 1;
        }
        
        .player-card .player-name {
            color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3.5rem;
            font-weight: 400;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 4px;
        }
        
        .player-card .player-number {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 6rem;
            font-weight: 400;
            line-height: 1;
            margin-bottom: 1rem;
        }
        
        .player-card .player-position {
            color: rgba(255, 255, 255, 0.6);
            font-size: 1.2rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 2rem;
        }
        
        /* ============================================
           Ranking Display
           ============================================ */
        .ranking-row {
            background: linear-gradient(90deg, rgba(15, 15, 15, 0.8) 0%, rgba(26, 26, 26, 0.6) 100%);
            padding: 1.5rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            border-left: 3px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        
        .ranking-row:hover {
            background: rgba(200, 16, 46, 0.1);
            border-left-color: #c8102e;
            transform: translateX(5px);
        }
        
        .ranking-row .ranking-number {
            color: rgba(255, 255, 255, 0.4);
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2rem;
            min-width: 60px;
            text-align: center;
        }
        
        .ranking-row.rank-1 .ranking-number {
            color: #FFD700;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }
        
        .ranking-row.rank-2 .ranking-number {
            color: #C0C0C0;
            text-shadow: 0 0 20px rgba(192, 192, 192, 0.5);
        }
        
        .ranking-row.rank-3 .ranking-number {
            color: #CD7F32;
            text-shadow: 0 0 20px rgba(205, 127, 50, 0.5);
        }
        
        /* ============================================
           Section Headers - Clean Typography
           ============================================ */
        .section-header {
            color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2.5rem;
            font-weight: 400;
            margin: 4rem 0 2rem 0;
            padding-bottom: 1rem;
            border-bottom: 1px solid #2a2a2a;
            text-transform: uppercase;
            letter-spacing: 6px;
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 0;
            width: 120px;
            height: 1px;
            background: linear-gradient(90deg, #c8102e 0%, transparent 100%);
        }
        
        .section-header-jp {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.4);
            font-weight: 400;
            margin-top: 0.5rem;
            letter-spacing: 2px;
        }
        
        /* ============================================
           Data Tables - Dark Theme
           ============================================ */
        .dataframe {
            background: #0a0a0a !important;
            border: 1px solid #2a2a2a !important;
            border-radius: 12px;
            font-size: 0.95rem;
        }
        
        .dataframe th {
            background: linear-gradient(180deg, #0f0f0f 0%, #0a0a0a 100%) !important;
            color: rgba(255, 255, 255, 0.8) !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 2px;
            padding: 1.2rem 1rem !important;
            border-bottom: 1px solid #c8102e !important;
        }
        
        .dataframe td {
            background: #0a0a0a !important;
            color: rgba(255, 255, 255, 0.9) !important;
            border-bottom: 1px solid #1a1a1a !important;
            padding: 1rem !important;
        }
        
        .dataframe tr:hover td {
            background: rgba(200, 16, 46, 0.05) !important;
        }
        
        /* ============================================
           Input Fields - Dark Theme
           ============================================ */
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stDateInput > div > div {
            background: #0f0f0f;
            border: 1px solid #2a2a2a;
            color: #ffffff;
            border-radius: 8px;
        }
        
        .stSelectbox > div > div:focus,
        .stTextInput > div > div:focus,
        .stNumberInput > div > div:focus,
        .stDateInput > div > div:focus {
            border-color: #c8102e;
            box-shadow: 0 0 20px rgba(200, 16, 46, 0.3);
        }
        
        /* ============================================
           Buttons - Premium Style
           ============================================ */
        .stButton > button {
            background: linear-gradient(135deg, #c8102e 0%, #a00d26 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 1rem 2.5rem;
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(200, 16, 46, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(200, 16, 46, 0.6);
            background: linear-gradient(135deg, #e01434 0%, #c8102e 100%);
        }
        
        .stButton > button[kind="secondary"] {
            background: transparent;
            border: 1px solid #c8102e;
            color: #c8102e;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(200, 16, 46, 0.1);
        }
        
        /* ============================================
           Graph Containers
           ============================================ */
        .js-plotly-plot {
            border-radius: 12px;
            background: #0a0a0a;
            border: 1px solid #2a2a2a;
            padding: 1.5rem;
        }
        
        /* ============================================
           Game Cards
           ============================================ */
        .game-card {
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
            padding: 3rem 2.5rem;
            border-radius: 16px;
            border: 1px solid #2a2a2a;
            margin-bottom: 2rem;
            box-shadow: 0 12px 40px rgba(0,0,0,0.6);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .game-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent 0%, #c8102e 50%, transparent 100%);
        }
        
        .game-card .game-date {
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 2rem;
            letter-spacing: 3px;
        }
        
        .game-card .teams {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2.5rem;
            color: #ffffff;
            font-weight: 400;
            margin-bottom: 2rem;
            letter-spacing: 4px;
        }
        
        .game-card .score {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 5rem;
            font-weight: 400;
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 2rem 0;
            letter-spacing: 4px;
        }
        
        .game-card .result {
            font-size: 1.2rem;
            font-weight: 700;
            padding: 1rem 2.5rem;
            border-radius: 50px;
            display: inline-block;
            margin-top: 2rem;
            text-transform: uppercase;
            letter-spacing: 3px;
        }
        
        .game-card .result.win {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            box-shadow: 0 4px 20px rgba(40, 167, 69, 0.5);
        }
        
        .game-card .result.loss {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white;
            box-shadow: 0 4px 20px rgba(220, 53, 69, 0.5);
        }
        
        /* ============================================
           File Uploader
           ============================================ */
        .stFileUploader > div {
            background: #0f0f0f;
            border: 2px dashed #2a2a2a;
            border-radius: 12px;
            padding: 3rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stFileUploader > div:hover {
            border-color: #c8102e;
            background: rgba(200, 16, 46, 0.05);
        }
        
        /* ============================================
           Messages - Dark Theme
           ============================================ */
        .stSuccess {
            background: rgba(40, 167, 69, 0.15);
            border-left: 3px solid #28a745;
            color: #4ade80;
            border-radius: 8px;
        }
        
        .stError {
            background: rgba(220, 53, 69, 0.15);
            border-left: 3px solid #dc3545;
            color: #fb7185;
            border-radius: 8px;
        }
        
        .stInfo {
            background: rgba(23, 162, 184, 0.15);
            border-left: 3px solid #17a2b8;
            color: #67e8f9;
            border-radius: 8px;
        }
        
        /* ============================================
           Sidebar Styling
           ============================================ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
            border-right: 1px solid #2a2a2a;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: rgba(255, 255, 255, 0.8);
        }
        
        /* ============================================
           Responsive Design
           ============================================ */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
            
            .nba-header h1 {
                font-size: 3rem;
                letter-spacing: 4px;
            }
            
            .stat-card .stat-value {
                font-size: 2.5rem;
            }
            
            .player-card .player-name {
                font-size: 2.5rem;
            }
            
            .player-card .player-number {
                font-size: 4rem;
            }
        }
        
        /* ============================================
           Custom Scrollbar
           ============================================ */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #0a0a0a;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #c8102e 0%, #1d428a 100%);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #e01434 0%, #4169e1 100%);
        }
    </style>
    """, unsafe_allow_html=True)
