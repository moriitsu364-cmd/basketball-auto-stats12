"""メインアプリケーション - NBA.com風デザイン"""
import streamlit as st
from database import StatsDatabase
from styles import load_css
from pages import season_stats, player_stats, game_stats, data_input
from pages import team_info, opponent_stats, compare, admin_settings


# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="Tsukuba Basketball Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSSを読み込み
load_css()


def main():
    """メインアプリケーション"""
    # データベース初期化
    db = StatsDatabase()
    
    # ヘッダー
    st.markdown("""
    <div class="nba-header">
        <h1>TSUKUBA BASKETBALL STATS</h1>
        <p class="subtitle">筑波大学附属高校 男子バスケットボール統計システム / Advanced Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # タブ
    tabs = st.tabs([
        "🏆 SEASON",
        "👤 PLAYER", 
        "📋 GAME",
        "📊 COMPARE",
        "🏀 TEAM INFO",
        "🎯 OPPONENTS",
        "📥 DATA INPUT",
        "⚙️ ADMIN"
    ])
    
    with tabs[0]:
        season_stats.render(db)
    
    with tabs[1]:
        player_stats.render(db)
    
    with tabs[2]:
        game_stats.render(db)
    
    with tabs[3]:
        compare.render(db)
    
    with tabs[4]:
        team_info.render(db)
    
    with tabs[5]:
        opponent_stats.render(db)
    
    with tabs[6]:
        data_input.render(db)
    
    with tabs[7]:
        admin_settings.render()


if __name__ == "__main__":
    main()
