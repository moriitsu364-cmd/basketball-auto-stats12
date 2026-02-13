"""バスケットボール統計管理システム - メインアプリケーション"""
import streamlit as st
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

# 必要なモジュールのインポート
try:
    from src.config import *
    from src.database import StatsDatabase
    from src.auth import check_password
    from src.styles import apply_custom_css
    
    # ページモジュールのインポート
    from src.pages import (
        season_stats,
        player_stats,
        game_stats,
        compare,
        team_info,
        opponent_stats,
        data_input,
        admin_settings
    )
except ImportError as e:
    st.error(f"モジュールのインポートに失敗しました: {e}")
    st.stop()


def initialize_session_state():
    """セッション状態の初期化"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "シーズン統計"
    if 'db' not in st.session_state:
        try:
            st.session_state.db = StatsDatabase()
        except Exception as e:
            st.error(f"データベースの初期化に失敗しました: {e}")
            st.session_state.db = None


def render_sidebar(db):
    """サイドバーを表示"""
    with st.sidebar:
        # タイトル
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #1d428a; margin: 0;">🏀</h1>
            <h2 style="color: #c8102e; margin: 0;">Basketball Stats</h2>
            <p style="color: #888; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                筑波大学附属高等学校
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ナビゲーション
        st.markdown("### 📊 メニュー")
        
        pages = {
            "シーズン統計": "📈",
            "選手統計": "👤", 
            "試合統計": "🏀",
            "比較分析": "📊",
            "チーム情報": "👥",
            "対戦相手統計": "🎯",
            "データ入力": "📝",
            "設定": "⚙️"
        }
        
        for page_name, icon in pages.items():
            if st.button(
                f"{icon} {page_name}",
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == page_name else "secondary"
            ):
                st.session_state.current_page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # データベース統計
        if db and db.df is not None and len(db.df) > 0:
            st.markdown("### 📊 データ統計")
            
            total_games = len(db.df['GameDate'].unique()) if 'GameDate' in db.df.columns else 0
            total_players = len(db.df['PlayerName'].unique()) if 'PlayerName' in db.df.columns else 0
            total_records = len(db.df)
            
            st.metric("総試合数", f"{total_games} 試合")
            st.metric("登録選手数", f"{total_players} 名")
            st.metric("総レコード数", f"{total_records} 件")
        else:
            st.info("データがまだ登録されていません")
        
        st.markdown("---")
        
        # フッター
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.8rem;">
            <p>Basketball Stats Manager</p>
            <p>v3.0</p>
        </div>
        """, unsafe_allow_html=True)


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
        elif current_page == "対戦相手統計":
            opponent_stats.render(db)
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
        initial_sidebar_state="expanded"
    )
    
    # カスタムCSSを適用
    try:
        apply_custom_css()
    except Exception as e:
        if DEBUG_MODE:
            st.warning(f"CSSの適用に失敗しました: {e}")
    
    # セッション状態の初期化
    initialize_session_state()
    
    # データベースの取得
    db = st.session_state.get('db')
    
    if db is None:
        st.error("❌ データベースの初期化に失敗しました")
        st.info("アプリケーションを再読み込みしてください")
        st.stop()
    
    # サイドバーとメインコンテンツを表示
    render_sidebar(db)
    render_main_content(db)


if __name__ == "__main__":
    main()
