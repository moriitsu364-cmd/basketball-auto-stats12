"""データ入力ページ - リニューアル版(相手チームデータ登録機能付き)"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from PIL import Image
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from ..database import StatsDatabase
from ..auth import check_password
from ..ai import setup_gemini, analyze_scoresheet
from ..components import section_header
from ..config import SEASONS, GAME_FORMATS


def render(db: StatsDatabase):
    """データ入力ページを表示(リニューアル版)
    
    Args:
        db: データベースインスタンス
    """
    if not check_password():
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%); padding: 2.5rem 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            📝 データ入力
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">
            DATA INPUT / 試合データ・相手チームデータの登録
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 入力モード選択
    input_mode = st.radio(
        "入力モードを選択 / Select Input Mode",
        ["自チームデータ / Our Team Data", "相手チームデータ / Opponent Team Data"],
        horizontal=True,
        key='input_mode'
    )
    
    if input_mode == "自チームデータ / Our Team Data":
        render_team_data_input(db)
    else:
        render_opponent_data_input(db)
    
    st.markdown("---")
    
    # データ管理セクション
    render_data_management(db)


def render_team_data_input(db: StatsDatabase):
    """自チームデータ入力"""
    section_header("OUR TEAM DATA INPUT", "自チーム試合データ入力")
    
    model, model_name = setup_gemini()
    
    if not model:
        st.error("⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in secrets.toml")
        st.info("💡 AI分析機能を使用するには、Gemini APIキーが必要です")
    
    # データ入力フォーム
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### 試合情報 / Game Information")
        game_date = st.date_input("試合日 / Game Date", datetime.now())
        season = st.selectbox("シーズン / Season", SEASONS, index=1)
        opponent = st.text_input("対戦相手 / Opponent", "")
        
        # ゲーム形式選択
        game_format = st.selectbox(
            "試合形式 / Game Format",
            list(GAME_FORMATS.keys()),
            format_func=lambda x: f"{x} - {GAME_FORMATS[x]}"
        )
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            team_score = st.number_input("筑波得点 / Tsukuba Score", min_value=0, value=0)
        with col_s2:
            opponent_score = st.number_input("相手得点 / Opponent Score", min_value=0, value=0)
        
        st.markdown("#### スコアシート画像 / Score Sheet Image")
        uploaded_file = st.file_uploader("画像アップロード / Upload Image", type=['png', 'jpg', 'jpeg', 'webp'])
    
    with col2:
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            if model and st.button("🤖 AI分析実行 / ANALYZE WITH AI", use_container_width=True, type="primary"):
                with st.spinner("分析中... / Analyzing..."):
                    try:
                        csv_text = analyze_scoresheet(model, image)
                        
                        df = pd.read_csv(io.StringIO(csv_text))
                        df['GameDate'] = str(game_date)
                        df['Season'] = season
                        df['Opponent'] = opponent
                        df['TeamScore'] = team_score
                        df['OpponentScore'] = opponent_score
                        df['GameFormat'] = game_format
                        df['DataType'] = 'OurTeam'  # データ種別を追加
                        
                        st.session_state['current_stats'] = df
                        st.success("✅ 分析完了! / Analysis complete!")
                        
                    except Exception as e:
                        st.error(f"❌ エラー / Error: {str(e)}")
        else:
            st.info("📸 スコアシート画像をアップロードしてください")
    
    # データ編集
    if 'current_stats' in st.session_state:
        section_header("データ確認・編集 / Review & Edit Data")
        
        edited_df = st.data_editor(
            st.session_state['current_stats'],
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 データ保存 / SAVE DATA", use_container_width=True, type="primary"):
                db.add_game(edited_df)
                if db.save():
                    st.success("✅ データを保存しました! / Data saved!")
                    del st.session_state['current_stats']
                    st.rerun()
        
        with col2:
            if st.button("❌ キャンセル / CANCEL", use_container_width=True):
                del st.session_state['current_stats']
                st.rerun()


def render_opponent_data_input(db: StatsDatabase):
    """相手チームデータ入力"""
    section_header("OPPONENT TEAM DATA INPUT", "相手チームデータ入力")
    
    st.info("""
    ### 📝 相手チームデータ登録について
    
    この機能では、対戦相手チームの選手データを登録できます。
    
    **登録できるデータ:**
    - 相手チーム名
    - 相手選手の個人スタッツ
    - 試合日・シーズン情報
    
    **データの分離:**
    自チームのデータと相手チームのデータは別々に管理され、混在しません。
    """)
    
    st.markdown("---")
    
    # 手動入力フォーム
    st.markdown("### 📊 相手チームデータを手動入力")
    
    col1, col2 = st.columns(2)
    
    with col1:
        opp_game_date = st.date_input("試合日 / Game Date", datetime.now(), key='opp_date')
        opp_season = st.selectbox("シーズン / Season", SEASONS, index=1, key='opp_season')
        opp_team_name = st.text_input("相手チーム名 / Opponent Team Name", "", key='opp_team')
    
    with col2:
        opp_format = st.selectbox(
            "試合形式 / Game Format",
            list(GAME_FORMATS.keys()),
            format_func=lambda x: f"{x} - {GAME_FORMATS[x]}",
            key='opp_format'
        )
        our_score = st.number_input("筑波得点 / Our Score", min_value=0, value=0, key='opp_our_score')
        their_score = st.number_input("相手得点 / Their Score", min_value=0, value=0, key='opp_their_score')
    
    st.markdown("---")
    
    # 選手データ入力
    st.markdown("### 👥 相手選手データ入力")
    
    num_players = st.number_input(
        "選手数 / Number of Players",
        min_value=1,
        max_value=15,
        value=5,
        key='opp_num_players'
    )
    
    # 選手データの入力テーブル
    st.markdown("#### 選手スタッツを入力してください")
    
    # サンプルデータフレーム
    sample_data = {
        'No': list(range(1, num_players + 1)),
        'PlayerName': [''] * num_players,
        'PTS': [0] * num_players,
        '3PM': [0] * num_players,
        '3PA': [0] * num_players,
        '2PM': [0] * num_players,
        '2PA': [0] * num_players,
        'FTM': [0] * num_players,
        'FTA': [0] * num_players,
        'TOT': [0] * num_players,
        'AST': [0] * num_players,
        'STL': [0] * num_players,
        'BLK': [0] * num_players,
        'TO': [0] * num_players,
        'PF': [0] * num_players
    }
    
    opponent_df = st.data_editor(
        pd.DataFrame(sample_data),
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key='opp_data_editor'
    )
    
    # データ保存ボタン
    if st.button("💾 相手チームデータを保存 / SAVE OPPONENT DATA", type="primary"):
        if not opp_team_name:
            st.error("❌ 相手チーム名を入力してください")
        else:
            # 必要な情報を追加
            opponent_df['GameDate'] = str(opp_game_date)
            opponent_df['Season'] = opp_season
            opponent_df['Opponent'] = 'Tsukuba High School'  # 相手視点では筑波が相手
            opponent_df['TeamScore'] = their_score
            opponent_df['OpponentScore'] = our_score
            opponent_df['GameFormat'] = opp_format
            opponent_df['DataType'] = 'OpponentTeam'  # データ種別
            opponent_df['OriginalTeam'] = opp_team_name  # 元のチーム名を保存
            
            # パーセンテージ計算(数値変換を確実に行う)
            opponent_df['3P%'] = opponent_df.apply(
                lambda row: round(pd.to_numeric(row['3PM'], errors='coerce') / pd.to_numeric(row['3PA'], errors='coerce'), 3) 
                if pd.to_numeric(row['3PA'], errors='coerce') > 0 else 0.0,
                axis=1
            )
            opponent_df['2P%'] = opponent_df.apply(
                lambda row: round(pd.to_numeric(row['2PM'], errors='coerce') / pd.to_numeric(row['2PA'], errors='coerce'), 3) 
                if pd.to_numeric(row['2PA'], errors='coerce') > 0 else 0.0,
                axis=1
            )
            opponent_df['FT%'] = opponent_df.apply(
                lambda row: round(pd.to_numeric(row['FTM'], errors='coerce') / pd.to_numeric(row['FTA'], errors='coerce'), 3) 
                if pd.to_numeric(row['FTA'], errors='coerce') > 0 else 0.0,
                axis=1
            )
            
            # その他の必須カラムを追加
            for col in ['GS', 'DK', 'OR', 'DR', 'TF', 'OF', 'FO', 'DQ', 'MIN']:
                if col not in opponent_df.columns:
                    opponent_df[col] = 0 if col != 'MIN' else '00:00'
            
            # データベースに保存
            db.add_game(opponent_df)
            if db.save():
                st.success(f"✅ {opp_team_name}のデータを保存しました!")
                st.rerun()


def render_data_management(db: StatsDatabase):
    """データ管理セクション"""
    section_header("DATA MANAGEMENT", "データ管理")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📥 エクスポート / Export")
        if not db.df.empty:
            csv = db.df.to_csv(index=False)
            st.download_button(
                label="全データダウンロード / DOWNLOAD ALL DATA",
                data=csv,
                file_name=f"stats_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("データがありません")
    
    with col2:
        st.markdown("#### 📤 インポート / Import")
        import_file = st.file_uploader("CSV Upload", type=['csv'], key='import')
        if import_file and st.button("インポート実行 / IMPORT DATA"):
            try:
                import_df = pd.read_csv(import_file)
                db.add_game(import_df)
                if db.save():
                    st.success("✅ インポート成功! / Import successful!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ エラー / Error: {e}")
    
    with col3:
        st.markdown("#### 🗑️ 削除 / Delete")
        if not db.df.empty:
            # データタイプでフィルタリング
            data_type_filter = st.selectbox(
                "データタイプ",
                ["すべて / All", "自チーム / Our Team", "相手チーム / Opponent"],
                key='delete_filter'
            )
            
            if data_type_filter == "自チーム / Our Team":
                filtered_df = db.df[db.df.get('DataType', 'OurTeam') == 'OurTeam']
            elif data_type_filter == "相手チーム / Opponent":
                filtered_df = db.df[db.df.get('DataType', 'OurTeam') == 'OpponentTeam']
            else:
                filtered_df = db.df
            
            if not filtered_df.empty:
                games_list = filtered_df.groupby(['GameDate', 'Opponent']).size().reset_index()[['GameDate', 'Opponent']]
                game_options = [f"{row['GameDate']} vs {row['Opponent']}" for _, row in games_list.iterrows()]
                
                if game_options:
                    selected_game_to_delete = st.selectbox("試合選択 / Select game", [""] + game_options, key='delete_game')
                    
                    if selected_game_to_delete and st.button("🗑️ 削除 / DELETE", type="secondary"):
                        game_date_str = selected_game_to_delete.split(" vs ")[0]
                        opponent_str = selected_game_to_delete.split(" vs ")[1]
                        
                        db.delete_game(game_date_str, opponent_str)
                        
                        if db.save():
                            st.success(f"✅ 削除完了: {selected_game_to_delete}")
                            st.rerun()
            else:
                st.info("該当データなし")
    
    # データベース統計
    st.markdown("---")
    st.markdown("### 📊 データベース統計")
    
    stats_summary = db.get_stats_summary()
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("総試合数", stats_summary['total_games'])
    
    with metric_col2:
        st.metric("総選手数", stats_summary['total_players'])
    
    with metric_col3:
        st.metric("シーズン数", stats_summary['total_seasons'])
    
    with metric_col4:
        st.metric("総レコード数", stats_summary['total_records'])
