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
            padding: 5rem 3rem;
            margin: -2rem -3rem 3rem -3rem;
            position: relative;
            overflow: hidden;
            border-bottom: 4px solid;
            border-image: linear-gradient(90deg, #1d428a 0%, #c8102e 100%) 1;
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
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }
        
        .nba-header h1 {
            color: #ffffff;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 5.5rem;
            font-weight: 400;
            margin: 0;
            letter-spacing: 12px;
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
            font-size: 1.1rem;
            margin-top: 1.5rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
            letter-spacing: 4px;
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
           Navigation Tabs - Enhanced Contrast
           ============================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background: linear-gradient(180deg, #f0f2f5 0%, #ffffff 100%);
            border-bottom: 3px solid #dee2e6;
            padding: 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #1a1a1a;
            font-weight: 700;
            font-size: 0.9rem;
            padding: 1.8rem 3rem;
            border: none;
            border-bottom: 4px solid transparent;
            letter-spacing: 2.5px;
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
            height: 4px;
            background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #c8102e;
            background: linear-gradient(180deg, rgba(200, 16, 46, 0.05) 0%, transparent 100%);
        }
        
        .stTabs [data-baseweb="tab"]:hover::after {
            transform: translateX(-50%) scaleX(1);
        }
        
        .stTabs [aria-selected="true"] {
            color: #c8102e;
            background: linear-gradient(180deg, rgba(200, 16, 46, 0.08) 0%, transparent 100%);
            font-weight: 900;
        }
        
        .stTabs [aria-selected="true"]::after {
            transform: translateX(-50%) scaleX(1);
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
            bottom: 10px;
            right: 10px;
            width: 60px;
            height: 60px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>') center/contain no-repeat;
            opacity: 0.05;
        }
        
        /* ============================================
           Player Cards - Clean Design with Icons
           ============================================ */
        .player-card {
            background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
            padding: 3.5rem 3rem;
            border-radius: 24px;
            border: 3px solid #e8eaed;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.12);
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
            background: radial-gradient(circle at center right, rgba(200, 16, 46, 0.05) 0%, transparent 70%);
        }
        
        /* Player silhouette icon */
        .player-card::after {
            content: '';
            position: absolute;
            right: 5%;
            top: 50%;
            transform: translateY(-50%);
            width: 150px;
            height: 150px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%23c8102e" stroke-width="0.5" opacity="0.1"><circle cx="12" cy="7" r="4"/><path d="M5 21v-2a7 7 0 0 1 14 0v2"/></svg>') center/contain no-repeat;
            opacity: 0.8;
        }
        
        .player-card-content {
            position: relative;
            z-index: 1;
        }
        
        .player-card .player-name {
            color: #000000;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 4rem;
            font-weight: 400;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 5px;
        }
        
        .player-card .player-number {
            background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 7rem;
            font-weight: 400;
            line-height: 1;
            margin-bottom: 1.5rem;
        }
        
        .player-card .player-position {
            color: #495057;
            font-size: 1.3rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin-bottom: 2rem;
        }
        
        /* ============================================
           Ranking Display - High Contrast (FIXED)
           ============================================ */
        .ranking-row {
            background: linear-gradient(90deg, #ffffff 0%, #fafbfc 100%);
            padding: 2rem;
            margin-bottom: 1rem;
            border-radius: 16px;
            border: 3px solid #e8eaed;
            border-left: 5px solid transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 2rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.06);
            position: relative; /* FIXED: Added position relative for ::before positioning */
        }
        
        .ranking-row:hover {
            background: linear-gradient(90deg, rgba(200, 16, 46, 0.03) 0%, #ffffff 100%);
            border-left-color: #c8102e;
            transform: translateX(8px);
            box-shadow: 0 6px 20px rgba(200, 16, 46, 0.15);
        }
        
        .ranking-row .ranking-number {
            color: #495057;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2.5rem;
            min-width: 70px;
            text-align: center;
            font-weight: 400;
        }
        
        .ranking-row.rank-1 {
            border-left-color: #FFB800;
            background: linear-gradient(90deg, rgba(255, 184, 0, 0.05) 0%, #ffffff 100%);
        }
        
        .ranking-row.rank-1 .ranking-number {
            color: #FFB800;
            text-shadow: 0 2px 10px rgba(255, 184, 0, 0.4);
        }
        
        .ranking-row.rank-2 {
            border-left-color: #95A5A6;
        }
        
        .ranking-row.rank-2 .ranking-number {
            color: #7F8C8D;
            text-shadow: 0 2px 10px rgba(127, 140, 141, 0.4);
        }
        
        .ranking-row.rank-3 {
            border-left-color: #CD7F32;
        }
        
        .ranking-row.rank-3 .ranking-number {
            color: #CD7F32;
            text-shadow: 0 2px 10px rgba(205, 127, 50, 0.4);
        }
        
        /* Trophy icon for top 3 */
        .ranking-row.rank-1::before,
        .ranking-row.rank-2::before,
        .ranking-row.rank-3::before {
            content: '';
            position: absolute;
            left: 10px;
            width: 40px;
            height: 40px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>') center/contain no-repeat;
            opacity: 0.1;
        }
        
        /* ============================================
           Section Headers - Bold and Clear
           ============================================ */
        .section-header {
            color: #000000;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 3rem;
            font-weight: 400;
            margin: 5rem 0 2.5rem 0;
            padding-bottom: 1.5rem;
            border-bottom: 4px solid #dee2e6;
            text-transform: uppercase;
            letter-spacing: 8px;
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 150px;
            height: 4px;
            background: linear-gradient(90deg, #c8102e 0%, #1d428a 100%);
        }
        
        .section-header-jp {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 1rem;
            color: #495057;
            font-weight: 600;
            margin-top: 0.8rem;
            letter-spacing: 2px;
        }
        
        /* ============================================
           Data Tables - High Contrast
           ============================================ */
        .dataframe {
            background: #ffffff !important;
            border: 3px solid #dee2e6 !important;
            border-radius: 16px;
            font-size: 1rem;
            overflow: hidden;
        }
        
        .dataframe th {
            background: linear-gradient(180deg, #f0f2f5 0%, #ffffff 100%) !important;
            color: #000000 !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 2px;
            padding: 1.5rem 1.2rem !important;
            border-bottom: 3px solid #c8102e !important;
        }
        
        .dataframe td {
            background: #ffffff !important;
            color: #000000 !important;
            border-bottom: 2px solid #f0f2f5 !important;
            padding: 1.2rem !important;
            font-weight: 500;
        }
        
        .dataframe tr:hover td {
            background: rgba(200, 16, 46, 0.04) !important;
            font-weight: 600;
        }
        
        /* ============================================
           Input Fields - Clear Borders
           ============================================ */
        .stSelectbox > div > div,
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stDateInput > div > div {
            background: #ffffff;
            border: 3px solid #dee2e6;
            color: #000000;
            border-radius: 12px;
            font-weight: 500;
        }
        
        .stSelectbox > div > div:focus,
        .stTextInput > div > div:focus,
        .stNumberInput > div > div:focus,
        .stDateInput > div > div:focus {
            border-color: #c8102e;
            box-shadow: 0 0 0 4px rgba(200, 16, 46, 0.15);
        }
        
        /* Labels for inputs */
        label {
            color: #000000 !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }
        
        /* ============================================
           Buttons - Bold Design
           ============================================ */
        .stButton > button {
            background: linear-gradient(135deg, #c8102e 0%, #a00d26 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 1.2rem 3rem;
            font-weight: 800;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(200, 16, 46, 0.35);
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(200, 16, 46, 0.5);
            background: linear-gradient(135deg, #e01434 0%, #c8102e 100%);
        }
        
        .stButton > button[kind="secondary"] {
            background: transparent;
            border: 3px solid #c8102e;
            color: #c8102e;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(200, 16, 46, 0.08);
        }
        
        /* ============================================
           Graph Containers
           ============================================ */
        .js-plotly-plot {
            border-radius: 16px;
            background: #ffffff;
            border: 3px solid #dee2e6;
            padding: 2rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }
        
        /* ============================================
           Game Cards - Clear and Bold
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
                padding: 1.5rem;
            }
            
            .nba-header {
                margin: -1.5rem -1.5rem 2rem -1.5rem;
                padding: 3rem 2rem;
            }
            
            .nba-header h1 {
                font-size: 3.5rem;
                letter-spacing: 6px;
            }
            
            .stat-card .stat-value {
                font-size: 3rem;
            }
            
            .player-card .player-name {
                font-size: 2.5rem;
            }
            
            .player-card .player-number {
                font-size: 5rem;
            }
            
            .game-card .score { /* FIXED: Added proper selector */
                font-size: 4rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 1.2rem 1.5rem;
                font-size: 0.75rem;
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
