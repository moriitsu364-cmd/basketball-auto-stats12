"""メインアプリケーション - NBA.com風デザイン（改善版）"""
import streamlit as st
import sys
from pathlib import Path

# パスの設定
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

# モジュールのインポート
from database import StatsDatabase
from config import *
from styles import load_css

# ページモジュールを個別にインポート
from pages import season_stats, player_stats, game_stats, data_input
from pages import team_info, opponent_stats, compare, admin_settings


# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="🏀 Tsukuba Basketball Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def initialize_session_state():
    """セッション状態の初期化"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_page = 'SEASON'
        st.session_state.admin_logged_in = False
        st.session_state.login_attempts = 0
        st.session_state.last_activity = None


def check_dependencies():
    """必要な依存関係のチェック"""
    required_modules = ['pandas', 'plotly', 'PIL']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        st.error(f"必要なモジュールがインストールされていません: {', '.join(missing)}")
        st.info("以下のコマンドを実行してください:")
        st.code("pip install -r requirements.txt")
        return False
    
    return True


def main():
    """メインアプリケーション"""
    # セッション状態の初期化
    initialize_session_state()
    
    # 依存関係のチェック
    if not check_dependencies():
        st.stop()
    
    # CSSを読み込み
    try:
        load_css()
    except Exception as e:
        st.warning(f"CSSの読み込みに失敗しました: {e}")
    
    # データベース初期化
    try:
        db = StatsDatabase()
        
        # データベース情報を表示（デバッグ用）
        if hasattr(db, 'get_stats_summary'):
            stats = db.get_stats_summary()
            # サイドバーに統計情報を表示
            with st.sidebar:
                st.markdown("### 📊 データベース統計")
                st.metric("総試合数", stats['total_games'])
                st.metric("総選手数", stats['total_players'])
                st.metric("シーズン数", stats['total_seasons'])
                st.metric("総レコード数", stats['total_records'])
    except Exception as e:
        st.error(f"データベースの初期化に失敗しました: {e}")
        st.stop()
    
    # ヘッダー
    st.markdown("""
    <div class="nba-header">
        <h1>🏀 TSUKUBA BASKETBALL STATS</h1>
        <p class="subtitle">筑波大学附属高校 男子バスケットボール統計システム / Advanced Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # タブ
    try:
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
            try:
                season_stats.render(db)
            except Exception as e:
                st.error(f"シーズン統計の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[1]:
            try:
                player_stats.render(db)
            except Exception as e:
                st.error(f"選手統計の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[2]:
            try:
                game_stats.render(db)
            except Exception as e:
                st.error(f"試合統計の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[3]:
            try:
                compare.render(db)
            except Exception as e:
                st.error(f"比較ページの表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[4]:
            try:
                team_info.render(db)
            except Exception as e:
                st.error(f"チーム情報の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[5]:
            try:
                opponent_stats.render(db)
            except Exception as e:
                st.error(f"対戦相手統計の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[6]:
            try:
                data_input.render(db)
            except Exception as e:
                st.error(f"データ入力の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
        
        with tabs[7]:
            try:
                admin_settings.render()
            except Exception as e:
                st.error(f"管理者設定の表示エラー: {e}")
                if DEBUG_MODE:
                    st.exception(e)
    
    except Exception as e:
        st.error(f"アプリケーションエラー: {e}")
        if DEBUG_MODE:
            st.exception(e)
    
    # フッター
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; color: #666;">
        <p>🏀 Tsukuba Basketball Stats System v2.0</p>
        <p>Powered by Streamlit & Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"アプリケーションの起動に失敗しました: {e}")
        st.exception(e)
