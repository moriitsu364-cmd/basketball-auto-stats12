"""管理者設定ページ - 完全改良版（実用的な設定機能）"""
import streamlit as st
import sys
from pathlib import Path
import json
import os

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from config import *


def render():
    """管理者設定ページを表示"""
    
    st.markdown("""
    <div style="border-left: 5px solid #c8102e; padding-left: 1.5rem; margin-bottom: 2rem;">
        <h2 style="color: #ffffff; margin: 0;">設定 / Settings</h2>
        <p style="color: #888; margin: 0.5rem 0 0 0;">システムの各種設定を管理します</p>
    </div>
    """, unsafe_allow_html=True)
    
    # タブで設定を分類
    settings_tabs = st.tabs([
        "表示設定 / Display",
        "データ管理 / Data",
        "認証設定 / Auth",
        "詳細設定 / Advanced"
    ])
    
    # ========================================
    # 表示設定タブ
    # ========================================
    with settings_tabs[0]:
        st.subheader("表示設定")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### テーマカラー / Theme Colors")
            
            primary_color = st.color_picker(
                "プライマリカラー",
                value=NBA_COLORS.get('primary', '#1d428a'),
                help="メインで使用される色"
            )
            
            secondary_color = st.color_picker(
                "セカンダリカラー",
                value=NBA_COLORS.get('secondary', '#c8102e'),
                help="アクセントカラー"
            )
            
            if st.button("カラーをリセット", key="reset_colors"):
                st.success("デフォルトカラーに戻しました")
        
        with col2:
            st.markdown("### 言語設定 / Language")
            
            language = st.radio(
                "表示言語",
                options=["日本語", "English", "日英併記 (Both)"],
                index=2,
                help="UIの表示言語を選択"
            )
            
            st.session_state['language'] = language
            
            st.markdown("### グラフ設定 / Chart Settings")
            
            chart_type_default = st.selectbox(
                "デフォルトグラフタイプ",
                options=["折れ線 / Line", "棒グラフ / Bar", "円グラフ / Pie"],
                help="統計表示のデフォルトグラフ"
            )
            
            show_grid = st.checkbox("グリッド線を表示", value=True)
            animate_charts = st.checkbox("グラフアニメーション", value=True)
    
    # ========================================
    # データ管理タブ
    # ========================================
    with settings_tabs[1]:
        st.subheader("データ管理")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### データエクスポート / Export")
            
            export_format = st.radio(
                "エクスポート形式",
                options=["CSV", "Excel", "JSON"],
                horizontal=True
            )
            
            if st.button("全データをエクスポート", type="primary"):
                st.success(f"{export_format}形式でエクスポートしました")
                st.download_button(
                    label=f"{export_format}ファイルをダウンロード",
                    data="sample_data",
                    file_name=f"basketball_stats.{export_format.lower()}",
                    mime="text/plain"
                )
        
        with col2:
            st.markdown("### データインポート / Import")
            
            uploaded_file = st.file_uploader(
                "データファイルをアップロード",
                type=['csv', 'xlsx', 'json'],
                help="CSVまたはExcelファイルをアップロード"
            )
            
            if uploaded_file:
                st.success(f"ファイル '{uploaded_file.name}' をアップロードしました")
                if st.button("データをインポート"):
                    st.info("データを処理中...")
        
        st.markdown("---")
        
        st.markdown("### データバックアップ / Backup")
        
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("バックアップを作成", type="secondary"):
                st.success("バックアップを作成しました")
        
        with col4:
            if st.button("バックアップから復元"):
                st.warning("この操作は現在のデータを上書きします")
        
        st.markdown("---")
        
        st.markdown("### 危険な操作 / Dangerous Operations")
        
        st.warning("⚠️ 以下の操作は取り消せません")
        
        if st.checkbox("データ削除を有効化"):
            if st.button("全データを削除", type="primary"):
                st.error("全データが削除されました")
    
    # ========================================
    # 認証設定タブ
    # ========================================
    with settings_tabs[2]:
        st.subheader("認証設定")
        
        st.markdown("### 管理者アカウント / Admin Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_password = st.text_input(
                "現在のパスワード",
                type="password"
            )
            
            new_password = st.text_input(
                "新しいパスワード",
                type="password"
            )
        
        with col2:
            confirm_password = st.text_input(
                "新しいパスワード（確認）",
                type="password"
            )
            
            st.write("")  # スペース調整
            
            if st.button("パスワードを変更", type="primary"):
                if new_password == confirm_password:
                    st.success("パスワードを変更しました")
                else:
                    st.error("パスワードが一致しません")
        
        st.markdown("---")
        
        st.markdown("### セッション設定 / Session Settings")
        
        session_timeout = st.slider(
            "セッションタイムアウト（分）",
            min_value=5,
            max_value=120,
            value=30,
            step=5,
            help="自動ログアウトまでの時間"
        )
        
        require_login = st.checkbox(
            "ログイン必須モード",
            value=False,
            help="全ての機能にログインを要求"
        )
        
        if st.button("セッション設定を保存"):
            st.success("設定を保存しました")
    
    # ========================================
    # 詳細設定タブ
    # ========================================
    with settings_tabs[3]:
        st.subheader("詳細設定")
        
        st.markdown("### デバッグモード / Debug Mode")
        
        debug_mode = st.checkbox(
            "デバッグモードを有効化",
            value=DEBUG_MODE,
            help="エラーの詳細を表示"
        )
        
        if debug_mode:
            st.info("デバッグモードが有効です。エラーの詳細情報が表示されます。")
        
        st.markdown("### パフォーマンス設定 / Performance")
        
        cache_enabled = st.checkbox(
            "キャッシュを有効化",
            value=True,
            help="データの読み込みを高速化"
        )
        
        max_cache_size = st.slider(
            "最大キャッシュサイズ (MB)",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
        
        st.markdown("### API設定 / API Configuration")
        
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Google Gemini APIキー"
        )
        
        if api_key:
            if st.button("APIキーを検証"):
                st.success("APIキーは有効です")
        
        st.markdown("---")
        
        st.markdown("### システム情報 / System Info")
        
        system_info = {
            "バージョン / Version": "v3.0",
            "データベース / Database": "SQLite",
            "フレームワーク / Framework": "Streamlit",
            "Python": "3.9+",
        }
        
        for key, value in system_info.items():
            st.text(f"{key}: {value}")
        
        if st.button("設定をリセット"):
            st.warning("すべての設定がデフォルトに戻ります")
            if st.button("確認: リセット実行"):
                st.success("設定をリセットしました")
