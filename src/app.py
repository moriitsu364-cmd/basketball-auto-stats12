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
        animation: fadeOut 2s ease-in-out forwards;
        animation-delay: 6s;
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
    // 8秒後にスプラッシュスクリーンを完全に削除
    setTimeout(function() {
        var splash = document.getElementById('splashScreen');
        if (splash) {
            splash.remove();
        }
    }, 8000);
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
        st.session_state.current_page = "予定・出欠管理"
    if 'splash_shown' not in st.session_state:
        st.session_state.splash_shown = False
    if 'db' not in st.session_state:
        try:
            st.session_state.db = StatsDatabase()
        except Exception as e:
            st.error(f"データベースの初期化に失敗しました: {e}")
            st.session_state.db = None


def render_top_navigation(db):
    """統合ナビゲーションバーを表示（ヘッダー＋ナビゲーション一体型）"""
    
    # データ集計
    if db and db.df is not None and len(db.df) > 0:
        total_games = len(db.df['GameDate'].unique()) if 'GameDate' in db.df.columns else 0
        total_players = len(db.df['PlayerName'].unique()) if 'PlayerName' in db.df.columns else 0
        total_records = len(db.df)
    else:
        total_games = 0
        total_players = 0
        total_records = 0
    
    st.markdown(f"""
    <style>
    /* ================================================
       統合ヘッダー＋ナビゲーションバー
       ================================================ */
    
    /* サイドバーを完全に隠す */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    /* ページ上部の余白をリセット */
    .block-container {{
        padding-top: 0.5rem !important;
        max-width: 100% !important;
    }}
    
    /* ===== 統合バー本体（黒背景） ===== */
    .unified-bar {{
        background: #000000;
        margin: -1rem -1rem 0 -1rem;
        border-bottom: 3px solid #c8102e;
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    
    /* ===== 上段：ロゴ＋統計 ===== */
    .bar-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 2rem;
        border-bottom: 1px solid rgba(200, 16, 46, 0.3);
    }}
    
    .bar-logo {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    
    .bar-logo-icon {{
        font-size: 2rem;
        line-height: 1;
    }}
    
    .bar-logo-text h1 {{
        margin: 0;
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        letter-spacing: 2px;
        text-transform: uppercase;
    }}
    
    .bar-logo-text p {{
        margin: 0;
        font-size: 0.7rem;
        color: #c8102e;
        font-weight: 600;
        letter-spacing: 1px;
    }}
    
    .bar-metrics {{
        display: flex;
        gap: 1.5rem;
    }}
    
    .bar-metric {{
        text-align: center;
        padding: 0.2rem 0.8rem;
        background: rgba(200, 16, 46, 0.1);
        border-radius: 4px;
        border-left: 3px solid #c8102e;
    }}
    
    .bar-metric-value {{
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        line-height: 1.2;
    }}
    
    .bar-metric-label {{
        font-size: 0.6rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* ===== 下段：ナビゲーション ===== */
    .bar-nav {{
        padding: 0 1rem;
        display: flex;
        align-items: stretch;
        gap: 0;
    }}
    
    /* ナビボタン共通スタイル */
    .stButton button {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        border-bottom: 3px solid transparent !important;
        padding: 0.7rem 1.2rem !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.7) !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
        margin-bottom: 0 !important;
    }}
    
    .stButton button:hover {{
        color: white !important;
        background: rgba(200, 16, 46, 0.1) !important;
        border-bottom-color: #c8102e !important;
        transform: none !important;
    }}
    
    .stButton button[kind="primary"] {{
        color: white !important;
        background: rgba(200, 16, 46, 0.15) !important;
        border-bottom: 3px solid #c8102e !important;
        font-weight: 700 !important;
    }}
    
    .stButton button[kind="secondary"] {{
        color: rgba(255,255,255,0.7) !important;
    }}
    
    /* ナビ内セレクトボックス */
    .stSelectbox {{
        margin: 0 !important;
    }}
    
    .stSelectbox > div > div {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        border-bottom: 3px solid transparent !important;
        padding: 0.7rem 1.2rem !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.7) !important;
        cursor: pointer !important;
        min-height: unset !important;
    }}
    
    .stSelectbox > div > div:hover {{
        color: white !important;
        background: rgba(200, 16, 46, 0.1) !important;
        border-bottom-color: #c8102e !important;
    }}
    
    /* アクティブなセレクトボックス */
    div[data-active-nav="true"] .stSelectbox > div > div {{
        color: white !important;
        background: rgba(200, 16, 46, 0.15) !important;
        border-bottom: 3px solid #c8102e !important;
        font-weight: 700 !important;
    }}
    
    .stSelectbox svg {{
        color: #c8102e !important;
        opacity: 0.8;
    }}
    
    /* ドロップダウンオプション */
    .stSelectbox [data-baseweb="popover"] {{
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
    }}
    
    .stSelectbox li {{
        color: white !important;
        background: #1a1a1a !important;
    }}
    
    .stSelectbox li:hover {{
        background: rgba(200, 16, 46, 0.2) !important;
    }}
    </style>
    
    <div class="unified-bar">
        <!-- 上段：ロゴ＋統計情報 -->
        <div class="bar-top">
            <div class="bar-logo">
                <div class="bar-logo-icon">🏀</div>
                <div class="bar-logo-text">
                    <h1>Basketball Stats</h1>
                    <p>筑波大学附属高等学校</p>
                </div>
            </div>
            <div class="bar-metrics">
                <div class="bar-metric">
                    <div class="bar-metric-value">{total_games}</div>
                    <div class="bar-metric-label">Games</div>
                </div>
                <div class="bar-metric">
                    <div class="bar-metric-value">{total_players}</div>
                    <div class="bar-metric-label">Players</div>
                </div>
                <div class="bar-metric">
                    <div class="bar-metric-value">{total_records}</div>
                    <div class="bar-metric-label">Records</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== 下段ナビゲーション（Streamlitコンポーネント） =====
    st.markdown('<div class="bar-nav">', unsafe_allow_html=True)
    
    # カテゴリーとページのマッピング
    # ※「対戦相手」を統計に移動、「チーム情報」カテゴリーはチーム情報のみ
    categories = {
        "統計": ["シーズン統計", "選手統計", "試合統計", "対戦相手", "比較分析"],
        "チーム情報": ["チーム情報"],
        "予定・出欠": ["予定・出欠管理"],
        "データ入力": ["データ入力"],
        "設定": ["設定"]
    }
    
    def get_current_category(page):
        for cat, pages in categories.items():
            if page in pages:
                return cat
        return "統計"
    
    current_category = get_current_category(st.session_state.current_page)
    
    cols = st.columns(5)
    
    for idx, (category_name, pages_in_category) in enumerate(categories.items()):
        with cols[idx]:
            if len(pages_in_category) == 1:
                if st.button(
                    category_name,
                    key=f"cat_{category_name}",
                    use_container_width=True,
                    type="primary" if current_category == category_name else "secondary"
                ):
                    st.session_state.current_page = pages_in_category[0]
                    st.rerun()
            else:
                options = pages_in_category
                current_index = options.index(st.session_state.current_page) if st.session_state.current_page in options else 0
                
                selected = st.selectbox(
                    category_name,
                    options,
                    index=current_index,
                    key=f"select_{category_name}",
                    label_visibility="collapsed"
                )
                
                if selected != st.session_state.current_page:
                    st.session_state.current_page = selected
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
        elif current_page == "予定・出欠管理":
            # パスワード不要で誰でもアクセス可能
            schedule_management.render(db)
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
