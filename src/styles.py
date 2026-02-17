"""NBA.com inspired sophisticated design with enhanced readability - Tsukuba Basketball (FIXED VERSION)"""
import streamlit as st


def load_css():
    """Load sophisticated CSS styles with maximum readability and visual icons"""
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
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        }
        
        .main {
            background: #ffffff;
            border-radius: 0;
            box-shadow: 0 0 80px rgba(0,0,0,0.4);
        }
        
        .block-container {
            padding: 2rem 3rem;
            max-width: 1600px;
            background: #ffffff;
        }
        
        /* ============================================
           Header - Dark with Icons
           ============================================ */
        .nba-header {
            background: 
                linear-gradient(135deg, rgba(0,0,0,0.95) 0%, rgba(26,26,26,0.95) 100%),
                url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="2" fill="white" opacity="0.1"/><circle cx="50" cy="50" r="2" fill="white" opacity="0.1"/><circle cx="90" cy="10" r="2" fill="white" opacity="0.1"/><circle cx="30" cy="70" r="2" fill="white" opacity="0.1"/><circle cx="70" cy="30" r="2" fill="white" opacity="0.1"/></svg>');
            background-size: cover, 100px 100px;
            padding: 2.5rem 2rem;
            margin: -2rem -3rem 1.5rem -3rem;
            position: relative;
            overflow: hidden;
            border-bottom: 4px solid;
            border-image: linear-gradient(90deg, #1d428a 0%, #c8102e 100%) 1;
            z-index: 1;
        }
        
        .nba-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(200, 16, 46, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(29, 66, 138, 0.2) 0%, transparent 50%);
            animation: pulse 8s ease-in-out infinite;
            z-index: 0;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        .nba-header h1 {
            color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3.5rem;
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
            text-shadow: 0 4px 20px rgba(255,255,255,0.1);
        }
        
        .nba-header .subtitle {
            color: rgba(255, 255, 255, 0.85);
            font-size: 1rem;
            margin-top: 0.8rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        /* Basketball icon in header */
        .nba-header::after {
            content: '';
            position: absolute;
            right: 5%;
            top: 50%;
            transform: translateY(-50%);
            width: 200px;
            height: 200px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="none" stroke="white" stroke-width="1" opacity="0.15"/><path d="M 50 5 Q 70 50 50 95" fill="none" stroke="white" stroke-width="1" opacity="0.15"/><path d="M 50 5 Q 30 50 50 95" fill="none" stroke="white" stroke-width="1" opacity="0.15"/><path d="M 5 50 Q 50 30 95 50" fill="none" stroke="white" stroke-width="1" opacity="0.15"/><path d="M 5 50 Q 50 70 95 50" fill="none" stroke="white" stroke-width="1" opacity="0.15"/></svg>') center/contain no-repeat;
            opacity: 0.6;
            z-index: 0;
        }
        
        /* ============================================
           Navigation Tabs - Enhanced Contrast (FIXED FOR CLICKABILITY)
           ============================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: linear-gradient(180deg, #f0f2f5 0%, #ffffff 100%);
            border-bottom: 3px solid #dee2e6;
            padding: 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            position: relative !important;
            z-index: 999 !important;
            overflow-x: auto;
            overflow-y: visible;
            min-height: 60px;
            display: flex;
            align-items: center;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #1a1a1a;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 1.2rem 2rem;
            border: none;
            border-bottom: 4px solid transparent;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative !important;
            z-index: 1000 !important;
            cursor: pointer !important;
            pointer-events: auto !important;
            white-space: nowrap;
            overflow: visible;
        }
        
        .stTabs [data-baseweb="tab"]::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%) scaleX(0);
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            pointer-events: none !important;
            z-index: -1;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #c8102e;
            background: linear-gradient(180deg, rgba(200, 16, 46, 0.05) 0%, transparent 100%);
            cursor: pointer !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover::after {
            transform: translateX(-50%) scaleX(1);
        }
        
        .stTabs [aria-selected="true"] {
            color: #c8102e;
            background: linear-gradient(180deg, rgba(200, 16, 46, 0.08) 0%, transparent 100%);
            font-weight: 900;
            pointer-events: auto !important;
        }
        
        .stTabs [aria-selected="true"]::after {
            transform: translateX(-50%) scaleX(1);
        }
        
        /* Ensure tabs container doesn't block clicks */
        .stTabs {
            position: relative !important;
            z-index: 998 !important;
        }
        
        .stTabs > div {
            pointer-events: auto !important;
        }
        
        /* Override any potential blocking elements */
        .stTabs [role="tablist"] {
            pointer-events: auto !important;
            z-index: 999 !important;
        }
        
        .stTabs button[role="tab"] {
            pointer-events: auto !important;
            cursor: pointer !important;
            z-index: 1000 !important;
        }
        
        /* ============================================
           Statistics Cards - Maximum Contrast
           ============================================ */
        .stat-card {
            background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
            padding: 3rem 2.5rem;
            border-radius: 20px;
            border: 3px solid #e8eaed;
            box-shadow: 0 6px 25px rgba(0,0,0,0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 2rem;
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
            height: 5px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
        }
        
        .stat-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 50px rgba(200, 16, 46, 0.2);
            border-color: rgba(200, 16, 46, 0.4);
        }
        
        .stat-card .stat-label {
            color: #495057;
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 1.2rem;
        }
        
        .stat-card .stat-value {
            color: #000000;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 4.5rem;
            font-weight: 400;
            line-height: 1;
            letter-spacing: 3px;
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
            font-size: 1rem;
            margin-top: 1.2rem;
            font-weight: 600;
        }
        
        /* Icon decoration for stat cards */
        .stat-card::after {
            content: '';
            position: absolute;
            right: 1.5rem;
            bottom: 1.5rem;
            width: 60px;
            height: 60px;
            opacity: 0.08;
            background-size: contain;
            background-repeat: no-repeat;
        }
        
        /* ============================================
           Player Cards - Enhanced Typography
           ============================================ */
        .player-card {
            background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
            padding: 4rem 3rem;
            border-radius: 24px;
            border: 3px solid #e8eaed;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .player-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
        }
        
        .player-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 60px rgba(200, 16, 46, 0.25);
        }
        
        .player-card .player-number {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 8rem;
            font-weight: 400;
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin-bottom: 1.5rem;
            letter-spacing: 5px;
        }
        
        .player-card .player-name {
            color: #000000;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3.5rem;
            font-weight: 400;
            margin-bottom: 1.5rem;
            letter-spacing: 8px;
            text-transform: uppercase;
        }
        
        .player-card .player-position {
            color: #495057;
            font-size: 1rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 3rem;
        }
        
        .player-card .player-stats {
            display: flex;
            justify-content: space-around;
            margin-top: 3rem;
            padding-top: 3rem;
            border-top: 3px solid #e8eaed;
        }
        
        .player-card .player-stat-item {
            text-align: center;
        }
        
        .player-card .player-stat-value {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3rem;
            color: #1d428a;
            font-weight: 400;
            letter-spacing: 3px;
        }
        
        .player-card .player-stat-label {
            color: #6c757d;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 0.8rem;
        }
        
        /* ============================================
           Data Tables - Bold & Clear
           ============================================ */
        .dataframe {
            font-family: 'Space Grotesk', 'Noto Sans JP', sans-serif;
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 25px rgba(0,0,0,0.1);
            border: 3px solid #e8eaed;
        }
        
        .dataframe thead th {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            color: white;
            padding: 1.8rem 1.5rem;
            font-weight: 800;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            text-align: left;
            border: none;
        }
        
        .dataframe tbody tr {
            transition: all 0.3s ease;
            border-bottom: 2px solid #f0f2f5;
        }
        
        .dataframe tbody tr:hover {
            background: linear-gradient(90deg, rgba(200, 16, 46, 0.06) 0%, transparent 100%);
            transform: scale(1.01);
        }
        
        .dataframe tbody td {
            padding: 1.8rem 1.5rem;
            color: #1a1a1a;
            font-size: 1rem;
            font-weight: 600;
            border: none;
        }
        
        .dataframe tbody tr:last-child {
            border-bottom: none;
        }
        
        /* Alternating row colors */
        .dataframe tbody tr:nth-child(even) {
            background: #fafbfc;
        }
        
        /* ============================================
           Buttons - High Visibility
           (メインコンテンツ内のボタン：ナビバーより後に読み込まれるので上書きできる)
           ============================================ */
        section[data-testid="stVerticalBlock"] .stButton > button,
        div[data-testid="column"] .stButton > button {
            background: linear-gradient(135deg, #c8102e 0%, #1d428a 100%) !important;
            color: white !important;
            border: none !important;
            padding: 1.2rem 3.5rem !important;
            font-size: 1rem !important;
            font-weight: 800 !important;
            border-radius: 50px !important;
            text-transform: uppercase !important;
            letter-spacing: 3px !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 8px 25px rgba(200, 16, 46, 0.3) !important;
        }
        
        section[data-testid="stVerticalBlock"] .stButton > button:hover,
        div[data-testid="column"] .stButton > button:hover {
            transform: translateY(-5px) !important;
            box-shadow: 0 15px 40px rgba(200, 16, 46, 0.5) !important;
            background: linear-gradient(135deg, #e01434 0%, #4169e1 100%) !important;
        }
        
        section[data-testid="stVerticalBlock"] .stButton > button:active,
        div[data-testid="column"] .stButton > button:active {
            transform: translateY(-2px) !important;
        }
        
        /* ============================================
           Input Fields
           ============================================ */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            border: 3px solid #e8eaed;
            border-radius: 12px;
            padding: 1.2rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #c8102e;
            box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.15);
            outline: none;
        }
        
        /* ============================================
           Dividers
           ============================================ */
        hr {
            border: none;
            height: 3px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
            margin: 3.5rem 0;
            border-radius: 3px;
        }
        
        /* ============================================
           Section Headers
           ============================================ */
        h1, h2, h3 {
            font-family: 'Bebas Neue', sans-serif;
            color: #000000;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 5px;
        }
        
        h1 {
            font-size: 4rem;
            margin-bottom: 2.5rem;
        }
        
        h2 {
            font-size: 3rem;
            margin-bottom: 2rem;
            border-bottom: 4px solid;
            border-image: linear-gradient(90deg, #1d428a 0%, #c8102e 100%) 1;
            padding-bottom: 1.5rem;
        }
        
        h3 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: #1d428a;
        }
        
        /* ============================================
           Game Cards
           ============================================ */
        .game-card {
            background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
            padding: 4rem 3rem;
            border-radius: 24px;
            border: 3px solid #e8eaed;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
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
            height: 5px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
        }
        
        .game-card .game-date {
            color: #495057;
            font-size: 0.95rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 2.5rem;
            letter-spacing: 3px;
        }
        
        .game-card .teams {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3rem;
            color: #000000;
            font-weight: 400;
            margin-bottom: 2.5rem;
            letter-spacing: 5px;
        }
        
        .game-card .score {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 6rem;
            font-weight: 400;
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 2.5rem 0;
            letter-spacing: 5px;
        }
        
        .game-card .result {
            font-size: 1.4rem;
            font-weight: 800;
            padding: 1.2rem 3rem;
            border-radius: 50px;
            display: inline-block;
            margin-top: 2.5rem;
            text-transform: uppercase;
            letter-spacing: 4px;
        }
        
        .game-card .result.win {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
        }
        
        .game-card .result.loss {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white;
            box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
        }
        
        /* ============================================
           File Uploader
           ============================================ */
        .stFileUploader > div {
            background: #ffffff;
            border: 4px dashed #adb5bd;
            border-radius: 16px;
            padding: 3.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stFileUploader > div:hover {
            border-color: #c8102e;
            background: rgba(200, 16, 46, 0.03);
        }
        
        /* ============================================
           Messages - High Contrast
           ============================================ */
        .stSuccess {
            background: rgba(40, 167, 69, 0.12);
            border-left: 5px solid #28a745;
            color: #155724;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .stError {
            background: rgba(220, 53, 69, 0.12);
            border-left: 5px solid #dc3545;
            color: #721c24;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .stInfo {
            background: rgba(23, 162, 184, 0.12);
            border-left: 5px solid #17a2b8;
            color: #0c5460;
            border-radius: 12px;
            font-weight: 600;
        }
        
        .stWarning {
            background: rgba(255, 193, 7, 0.12);
            border-left: 5px solid #ffc107;
            color: #856404;
            border-radius: 12px;
            font-weight: 600;
        }
        
        /* ============================================
           Sidebar Styling
           ============================================ */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f0f2f5 0%, #ffffff 100%);
            border-right: 3px solid #dee2e6;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #000000;
            font-weight: 600;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #000000;
            font-weight: 800;
            font-size: 1.1rem;
        }
        
        /* ============================================
           Metric Components
           ============================================ */
        [data-testid="stMetricValue"] {
            color: #000000;
            font-size: 2rem;
            font-weight: 800;
        }
        
        [data-testid="stMetricLabel"] {
            color: #495057;
            font-weight: 700;
            font-size: 0.9rem;
        }
        
        /* ============================================
           Responsive Design (FIXED)
           ============================================ */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem;
            }
            
            .nba-header {
                margin: -1rem -1rem 1rem -1rem;
                padding: 2rem 1.5rem;
            }
            
            .nba-header h1 {
                font-size: 2.5rem;
                letter-spacing: 4px;
            }
            
            .nba-header .subtitle {
                font-size: 0.9rem;
                letter-spacing: 1px;
            }
            
            .stat-card .stat-value {
                font-size: 2.5rem;
            }
            
            .player-card .player-name {
                font-size: 2rem;
            }
            
            .player-card .player-number {
                font-size: 4rem;
            }
            
            .game-card .score { /* FIXED: Added proper selector */
                font-size: 3.5rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 0.8rem 1rem;
                font-size: 0.7rem;
                letter-spacing: 0.5px;
            }
        }
        
        /* ============================================
           Custom Scrollbar
           ============================================ */
        ::-webkit-scrollbar {
            width: 14px;
            height: 14px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f0f2f5;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #c8102e 0%, #1d428a 100%);
            border-radius: 7px;
            border: 3px solid #f0f2f5;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #e01434 0%, #4169e1 100%);
        }
        
        /* ============================================
           Print Styles
           ============================================ */
        @media print {
            .nba-header {
                background: white !important;
                border-bottom: 3px solid #000;
            }
            
            .nba-header h1 {
                color: #000 !important;
                -webkit-text-fill-color: #000 !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
