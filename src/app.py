"""メインアプリケーション - 改良版（スプラッシュ画面、日英対応）"""
import streamlit as st
import sys
from pathlib import Path
import time

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
    page_title="Tsukuba Basketball Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def show_splash_screen():
    """スプラッシュ画面を表示"""
    splash_html = """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    .splash-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #000000 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeOut 0.5s ease-out 2s forwards;
    }
    .splash-title {
        font-size: 5rem;
        font-weight: 900;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.3rem;
        animation: fadeIn 1s ease-out;
        text-shadow: 0 0 30px rgba(200, 16, 46, 0.5);
        margin-bottom: 1rem;
    }
    .splash-subtitle {
        font-size: 1.5rem;
        color: #c8102e;
        font-weight: 600;
        animation: fadeIn 1.5s ease-out;
        letter-spacing: 0.1rem;
    }
    </style>
    <div class="splash-screen" id="splash">
        <div class="splash-title">TSUKUBA BASKETBALL</div>
        <div class="splash-subtitle">Advanced Analytics Platform</div>
    </div>
    <script>
        setTimeout(function() {
            document.getElementById('splash').style.display = 'none';
        }, 2500);
    </script>
    """
    st.markdown(splash_html, unsafe_allow_html=True)


def initialize_session_state():
    """セッション状態の初期化"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_page = 'SEASON'
        st.session_state.admin_logged_in = False
        st.session_state.login_attempts = 0
        st.session_state.last_activity = None
        st.session_state.show_splash = True
        st.session_state.language = 'ja'  # デフォルトは日本語


def check_dependencies():
    """必要な依存関係のチェック"""
    required_modules = {
        'pandas': 'pandas',
        'plotly': 'plotly',
        'PIL': 'Pillow'
    }
    missing = []
    
    for import_name, package_name in required_modules.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
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
    
    # スプラッシュ画面表示（初回のみ）
    if st.session_state.show_splash:
        show_splash_screen()
        st.session_state.show_splash = False
        time.sleep(2.5)
    
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
                st.markdown("### データベース統計")
                st.metric("試合数", stats['total_games'])
                st.metric("選手数", stats['total_players'])
                st.metric("シーズン数", stats['total_seasons'])
                st.metric("総レコード数", stats['total_records'])
    except Exception as e:
        st.error(f"データベースの初期化に失敗しました: {e}")
        st.stop()
    
    # コンパクトなヘッダー（スプラッシュ後）
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1d428a 0%, #c8102e 100%); padding: 1.5rem 2rem; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="color: #ffffff; margin: 0; font-weight: 900; font-size: 2rem; letter-spacing: 0.1rem;">TSUKUBA BASKETBALL</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem; font-weight: 500;">Advanced Analytics Platform / 筑波大学附属高校 男子バスケットボール部</p>
    </div>
    """, unsafe_allow_html=True)
    
    # タブ（絵文字削除）
    try:
        tabs = st.tabs([
            "シーズン / SEASON",
            "選手 / PLAYER", 
            "試合 / GAME",
            "比較 / COMPARE",
            "チーム / TEAM",
            "対戦相手 / OPPONENTS",
            "データ入力 / INPUT",
            "設定 / SETTINGS"
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
        <p>Tsukuba Basketball Analytics System v3.0</p>
        <p>Powered by Streamlit & Advanced Analytics</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"アプリケーションの起動に失敗しました: {e}")
        st.exception(e)
