"""バスケットボール統計管理システム - メインアプリケーション"""
import streamlit as st
import sys
import os
from pathlib import Path

# パスの設定
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = Path(__file__).parent

# sys.pathに追加
for path in [str(BASE_DIR), str(SRC_DIR)]:
    if path not in sys.path:
        sys.path.insert(0, path)

# カレントディレクトリをベースディレクトリに変更
try:
    os.chdir(BASE_DIR)
except Exception:
    pass

# 必要なモジュールのインポート
try:
    from config import *
    from database import StatsDatabase
    from auth import check_password
    from styles import load_css
    
    # ページモジュールのインポート
    from pages import (
        season_stats,
        player_stats,
        game_stats,
        compare,
        team_info,
        opponent_stats,
        data_input,
        admin_settings,
        schedule_management,
        attendance_management
    )
except ImportError as e:
    st.error(f"モジュールのインポートに失敗しました: {e}")
    st.error(f"カレントディレクトリ: {os.getcwd()}")
    st.error(f"sys.path: {sys.path}")
    import traceback
    st.code(traceback.format_exc())
    st.stop()


def show_splash_screen():
    """スプラッシュスクリーン（フェイドアウト効果付き・筑波大学附属高校）"""
    import time
    
    # スプラッシュスクリーンの表示（JavaScriptで自動削除）
    st.markdown("""
    <style>
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .splash-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeOut 1.5s ease-in-out forwards;
        animation-delay: 2s;
    }
    
    .splash-logo {
        font-size: 8rem;
        margin-bottom: 1rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .splash-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4rem;
        color: white;
        margin-bottom: 0.5rem;
        letter-spacing: 8px;
        text-transform: uppercase;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: slideUp 0.8s ease-out forwards;
    }
    
    .splash-school {
        font-size: 2rem;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 2rem;
        letter-spacing: 4px;
        font-weight: 500;
        animation: slideUp 0.8s ease-out forwards;
        animation-delay: 0.2s;
        opacity: 0;
    }
    
    .splash-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.85);
        letter-spacing: 3px;
        text-transform: uppercase;
        animation: slideUp 0.8s ease-out forwards;
        animation-delay: 0.4s;
        opacity: 0;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    </style>
    
    <div class="splash-screen" id="splashScreen">
        <div class="splash-logo">🏀</div>
        <div class="splash-title">BASKETBALL</div>
        <div class="splash-school">筑波大学附属高等学校</div>
        <div class="splash-subtitle">Statistics Manager</div>
    </div>
    
    <script>
    // 3.5秒後にスプラッシュスクリーンを完全に削除
    setTimeout(function() {
        var splash = document.getElementById('splashScreen');
        if (splash) {
            splash.remove();
        }
    }, 3500);
    </script>
    """, unsafe_allow_html=True)
    
    # スプラッシュスクリーンが表示される時間だけ待つ
    time.sleep(0.1)


def initialize_session_state():
    """セッション状態の初期化"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "シーズン統計"
    if 'splash_shown' not in st.session_state:
        st.session_state.splash_shown = False
    if 'db' not in st.session_state:
        try:
            st.session_state.db = StatsDatabase()
        except Exception as e:
            st.error(f"データベースの初期化に失敗しました: {e}")
            st.session_state.db = None


def render_top_navigation(db):
    """上部ナビゲーションバーを表示（NBA風・5つのメインタブ）"""
    
    st.markdown("""
    <style>
    /* メインヘッダー（黒背景） */
    .main-header {
        background: #000000;
        padding: 0.8rem 2rem;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 3px solid #c8102e;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .header-logo {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .header-logo-icon {
        font-size: 2.5rem;
    }
    
    .header-logo-text h1 {
        margin: 0;
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
        letter-spacing: 1px;
    }
    
    .header-logo-text p {
        margin: 0;
        font-size: 0.75rem;
        color: #c8102e;
        font-weight: 500;
    }
    
    .header-stats {
        display: flex;
        gap: 2rem;
        margin-left: 2rem;
    }
    
    .stat-box {
        text-align: center;
        padding: 0.3rem 0.8rem;
        background: rgba(200, 16, 46, 0.1);
        border-radius: 4px;
        border-left: 3px solid #c8102e;
    }
    
    .stat-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: white;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ナビゲーションバー */
    .nav-container {
        background: white;
        padding: 0;
        margin: 0 -1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-bottom: 1px solid #e0e0e0;
    }
    
    /* Streamlitのデフォルトpaddingを調整 */
    .block-container {
        padding-top: 1rem !important;
        max-width: 100% !important;
    }
    
    /* サイドバーを完全に隠す */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* セレクトボックスのスタイル調整 */
    .stSelectbox {
        margin-top: 0 !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 0 !important;
        border: none !important;
        border-right: 1px solid #e0e0e0 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ヘッダー部分
    if db and db.df is not None and len(db.df) > 0:
        total_games = len(db.df['GameDate'].unique()) if 'GameDate' in db.df.columns else 0
        total_players = len(db.df['PlayerName'].unique()) if 'PlayerName' in db.df.columns else 0
        total_records = len(db.df)
    else:
        total_games = 0
        total_players = 0
        total_records = 0
    
    st.markdown(f"""
    <div class="main-header">
        <div class="header-left">
            <div class="header-logo">
                <div class="header-logo-icon">🏀</div>
                <div class="header-logo-text">
                    <h1>BASKETBALL STATS</h1>
                    <p>筑波大学附属高等学校</p>
                </div>
            </div>
            <div class="header-stats">
                <div class="stat-box">
                    <div class="stat-value">{total_games}</div>
                    <div class="stat-label">Games</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{total_players}</div>
                    <div class="stat-label">Players</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{total_records}</div>
                    <div class="stat-label">Records</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ナビゲーションバー（5つのメインカテゴリ）
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # 5つのカラムを作成
    cols = st.columns(5)
    
    # カテゴリとそのサブページの定義
    categories = {
        "スタッツ": ["シーズン統計", "選手統計", "試合統計", "比較分析", "対戦相手"],
        "チーム情報": ["チーム情報"],
        "予定": ["予定管理", "出欠管理"],
        "データ入力": ["データ入力"],
        "設定": ["設定"]
    }
    
    # 各カテゴリのセレクトボックスを配置
    with cols[0]:
        stats_pages = categories["スタッツ"]
        current_in_stats = st.session_state.current_page in stats_pages
        default_stats = stats_pages.index(st.session_state.current_page) if current_in_stats else 0
        
        selected_stats = st.selectbox(
            "stats_label",
            stats_pages,
            index=default_stats,
            key="nav_stats",
            label_visibility="collapsed"
        )
        if selected_stats != st.session_state.current_page:
            st.session_state.current_page = selected_stats
            st.rerun()
    
    with cols[1]:
        team_pages = categories["チーム情報"]
        current_in_team = st.session_state.current_page in team_pages
        default_team = team_pages.index(st.session_state.current_page) if current_in_team else 0
        
        selected_team = st.selectbox(
            "team_label",
            team_pages,
            index=default_team,
            key="nav_team",
            label_visibility="collapsed"
        )
        if selected_team != st.session_state.current_page:
            st.session_state.current_page = selected_team
            st.rerun()
    
    with cols[2]:
        schedule_pages = categories["予定"]
        current_in_schedule = st.session_state.current_page in schedule_pages
        default_schedule = schedule_pages.index(st.session_state.current_page) if current_in_schedule else 0
        
        selected_schedule = st.selectbox(
            "schedule_label",
            schedule_pages,
            index=default_schedule,
            key="nav_schedule",
            label_visibility="collapsed"
        )
        if selected_schedule != st.session_state.current_page:
            st.session_state.current_page = selected_schedule
            st.rerun()
    
    with cols[3]:
        data_pages = categories["データ入力"]
        current_in_data = st.session_state.current_page in data_pages
        default_data = data_pages.index(st.session_state.current_page) if current_in_data else 0
        
        selected_data = st.selectbox(
            "data_label",
            data_pages,
            index=default_data,
            key="nav_data",
            label_visibility="collapsed"
        )
        if selected_data != st.session_state.current_page:
            st.session_state.current_page = selected_data
            st.rerun()
    
    with cols[4]:
        settings_pages = categories["設定"]
        current_in_settings = st.session_state.current_page in settings_pages
        default_settings = settings_pages.index(st.session_state.current_page) if current_in_settings else 0
        
        selected_settings = st.selectbox(
            "settings_label",
            settings_pages,
            index=default_settings,
            key="nav_settings",
            label_visibility="collapsed"
        )
        if selected_settings != st.session_state.current_page:
            st.session_state.current_page = selected_settings
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_sidebar(db):
    """サイドバーを表示（後方互換性のため残す）"""
    # 上部ナビゲーションに移行したため、空にする
    pass


def render_main_content(db):
    """メインコンテンツを表示"""
    current_page = st.session_state.current_page
    
    try:
        if current_page == "シーズン統計":
            season_stats.render(db)
        elif current_page == "選手統計":
            player_stats.render(db)
        elif current_page == "試合統計":
            game_stats.render(db)
        elif current_page == "比較分析":
            compare.render(db)
        elif current_page == "チーム情報":
            team_info.render(db)
        elif current_page == "対戦相手":
            opponent_stats.render(db)
        elif current_page == "予定管理":
            # マネージャー・選手・顧問のみアクセス可能
            if not st.session_state.get('management_access', False):
                st.warning("⚠️ この機能にアクセスするには認証が必要です")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("### 🔐 アクセス認証")
                    role = st.selectbox("役割を選択", ["マネージャー", "選手", "顧問"])
                    password = st.text_input("パスワード", type="password", key="management_password")
                    
                    if st.button("認証", type="primary", use_container_width=True):
                        # 簡易認証（実際の運用では適切な認証システムを使用）
                        if password == "basketball2026":
                            st.session_state.management_access = True
                            st.session_state.management_role = role
                            st.success(f"✅ {role}として認証されました")
                            st.rerun()
                        else:
                            st.error("❌ パスワードが正しくありません")
                    
                    st.info("💡 デモ用パスワード: basketball2026")
            else:
                schedule_management.render(db)
        elif current_page == "出欠管理":
            # マネージャー・選手・顧問のみアクセス可能
            if not st.session_state.get('management_access', False):
                st.warning("⚠️ この機能にアクセスするには認証が必要です")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("### 🔐 アクセス認証")
                    role = st.selectbox("役割を選択", ["マネージャー", "選手", "顧問"], key="attendance_role")
                    password = st.text_input("パスワード", type="password", key="attendance_password")
                    
                    if st.button("認証", type="primary", use_container_width=True):
                        # 簡易認証（実際の運用では適切な認証システムを使用）
                        if password == "basketball2026":
                            st.session_state.management_access = True
                            st.session_state.management_role = role
                            st.success(f"✅ {role}として認証されました")
                            st.rerun()
                        else:
                            st.error("❌ パスワードが正しくありません")
                    
                    st.info("💡 デモ用パスワード: basketball2026")
            else:
                attendance_management.render(db)
        elif current_page == "データ入力":
            data_input.render(db)
        elif current_page == "設定":
            # 管理者認証が必要
            if not st.session_state.admin_logged_in:
                st.warning("⚠️ この機能にアクセスするには管理者としてログインしてください")
                
                password = st.text_input("管理者パスワード", type="password", key="admin_password_input")
                
                if st.button("ログイン", type="primary"):
                    if check_password(password):
                        st.session_state.admin_logged_in = True
                        st.success("✅ ログインしました")
                        st.rerun()
                    else:
                        st.error("❌ パスワードが正しくありません")
            else:
                admin_settings.render(db)
                
                if st.button("ログアウト"):
                    st.session_state.admin_logged_in = False
                    st.rerun()
        else:
            st.error(f"ページ '{current_page}' が見つかりません")
    
    except Exception as e:
        st.error(f"ページの表示中にエラーが発生しました: {e}")
        if DEBUG_MODE:
            import traceback
            st.code(traceback.format_exc())


def main():
    """メインアプリケーション"""
    # ページ設定
    st.set_page_config(
        page_title="Basketball Stats Manager",
        page_icon="🏀",
        layout="wide",
        initial_sidebar_state="collapsed"  # サイドバーを折りたたむ
    )
    
    # セッション状態の初期化
    initialize_session_state()
    
    # スプラッシュスクリーンを表示（初回のみ）
    if not st.session_state.splash_shown:
        show_splash_screen()
        st.session_state.splash_shown = True
        st.rerun()  # 再度追加 - これがないとコンテンツが表示されない
        return
    
    # カスタムCSSを適用
    try:
        load_css()
    except Exception as e:
        if DEBUG_MODE:
            st.warning(f"CSSの適用に失敗しました: {e}")
    
    # データベースの取得
    db = st.session_state.get('db')
    
    if db is None:
        st.error("❌ データベースの初期化に失敗しました")
        st.info("アプリケーションを再読み込みしてください")
        st.stop()
    
    # 上部ナビゲーションバーとメインコンテンツを表示
    render_top_navigation(db)
    render_main_content(db)


if __name__ == "__main__":
    main()
