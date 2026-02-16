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
    """上部ナビゲーションバーを表示（NBA風）"""
    # ヘッダー部分
    st.markdown("""
    <style>
    /* ヘッダーとナビゲーションバーのスタイル */
    .top-header {
        background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%);
        padding: 1rem 2rem;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .top-header-title {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: white;
    }
    
    .top-header-logo {
        font-size: 2.5rem;
    }
    
    .top-header-text h1 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
    }
    
    .top-header-text p {
        margin: 0;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .top-stats {
        display: flex;
        gap: 2rem;
        color: white;
    }
    
    .top-stat-item {
        text-align: center;
    }
    
    .top-stat-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .top-stat-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    /* ナビゲーションバーのスタイル */
    .nav-bar {
        background: white;
        padding: 0;
        margin: 0 -1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-bottom: 1px solid #e0e0e0;
    }
    
    /* Streamlitのデフォルトpaddingを調整 */
    .block-container {
        padding-top: 1rem !important;
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
    <div class="top-header">
        <div class="top-header-title">
            <div class="top-header-logo">🏀</div>
            <div class="top-header-text">
                <h1>Basketball Stats Manager</h1>
                <p>筑波大学附属高等学校</p>
            </div>
        </div>
        <div class="top-stats">
            <div class="top-stat-item">
                <div class="top-stat-value">{total_games}</div>
                <div class="top-stat-label">試合</div>
            </div>
            <div class="top-stat-item">
                <div class="top-stat-value">{total_players}</div>
                <div class="top-stat-label">選手</div>
            </div>
            <div class="top-stat-item">
                <div class="top-stat-value">{total_records}</div>
                <div class="top-stat-label">記録</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ナビゲーションバー
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    
    pages = {
        "シーズン統計": "📈",
        "選手統計": "👤", 
        "試合統計": "🏀",
        "比較分析": "📊",
        "チーム情報": "👥",
        "対戦相手": "🎯",
        "予定管理": "📅",
        "出欠管理": "✓",
        "データ入力": "📝",
        "設定": "⚙️"
    }
    
    cols = st.columns(len(pages))
    
    for idx, (page_name, icon) in enumerate(pages.items()):
        with cols[idx]:
            button_text = f"{icon} {page_name}"
            if st.button(
                button_text,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == page_name else "secondary"
            ):
                st.session_state.current_page = page_name
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")


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
