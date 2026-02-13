"""選手統計ページ - リニューアル版（チーム情報連携）"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from ..database import StatsDatabase
from ..stats import calculate_stats
from ..charts import create_nba_chart, create_bar_chart, create_radar_chart
from ..components import stat_card, section_header, player_card
from ..config import NBA_COLORS


def render(db: StatsDatabase):
    """選手統計ページを表示（リニューアル版）
    
    Args:
        db: データベースインスタンス
    """
    if db.df.empty:
        st.info("📊 現在データがありません / No data available.")
        return
    
    # シーズン選択
    seasons = db.get_all_seasons()
    if not seasons:
        st.info("📊 現在データがありません")
        return
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        selected_season = st.selectbox(
            "シーズン選択 / SELECT SEASON",
            ["全シーズン / ALL SEASONS"] + seasons,
            key='player_season_select'
        )
    
    # 選手リスト取得
    if selected_season == "全シーズン / ALL SEASONS":
        players = db.get_all_players()
        season_filter = None
    else:
        players = db.get_all_players(season=selected_season)
        season_filter = selected_season
    
    if not players:
        st.warning("⚠️ 選手データがありません")
        return
    
    with col2:
        selected_player = st.selectbox(
            "選手選択 / SELECT PLAYER", 
            players, 
            key='player_select'
        )
    
    if not selected_player:
        return
    
    # 選手データ取得
    player_data = db.get_player_data(selected_player, season=season_filter)
    
    if player_data.empty:
        st.warning(f"⚠️ {selected_player}のデータがありません")
        return
    
    # 選手情報カード
    stats = calculate_stats(db.df if season_filter is None else db.get_season_data(season_filter), selected_player)
    player_number = player_data['No'].iloc[0] if len(player_data) > 0 else "N/A"
    
    player_card(selected_player, player_number)
    
    # チーム情報ページへの遷移ボタン
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button(
            f"👥 {selected_player}のチーム情報ページを見る / View Team Info", 
            use_container_width=True,
            type="primary"
        ):
            # セッション状態に選手情報を保存してチーム情報ページに遷移
            st.session_state['navigate_to_team_info'] = True
            st.session_state['team_info_player'] = selected_player
            st.info(f"💡 チーム情報タブに移動して、{selected_player}の詳細を確認してください")
    
    st.markdown("---")
    
    # 主要スタッツ
    section_header("シーズン平均スタッツ / Season Averages")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        stat_card("PPG", f"{stats['PTS']:.1f}", "Points", "primary")
    
    with col2:
        stat_card("RPG", f"{stats['REB']:.1f}", "Rebounds")
    
    with col3:
        stat_card("APG", f"{stats['AST']:.1f}", "Assists")
    
    with col4:
        stat_card("FG%", f"{stats['FG%']:.1f}", "Field Goal")
    
    with col5:
        stat_card("GP", stats['GP'], "Games", "primary")
    
    # 追加スタッツ
    st.markdown("---")
    col6, col7, col8, col9, col10 = st.columns(5)
    
    with col6:
        stat_card("SPG", f"{stats['STL']:.1f}", "Steals", "secondary")
    
    with col7:
        stat_card("BPG", f"{stats['BLK']:.1f}", "Blocks", "secondary")
    
    with col8:
        stat_card("3P%", f"{stats['3P%']:.1f}", "3-Point", "primary")
    
    with col9:
        stat_card("FT%", f"{stats['FT%']:.1f}", "Free Throw")
    
    with col10:
        stat_card("TO", f"{stats.get('TO', 0):.1f}", "Turnovers", "secondary")
    
    # パフォーマンスチャート
    section_header("パフォーマンスチャート / Performance Charts")
    
    chart_type = st.radio(
        "グラフタイプ選択",
        ["時系列推移", "カテゴリ別比較", "総合レーダーチャート"],
        horizontal=True
    )
    
    if chart_type == "時系列推移":
        render_time_series_charts(player_data)
    elif chart_type == "カテゴリ別比較":
        render_category_comparison(stats, selected_player)
    else:
        render_radar_chart_analysis(stats, selected_player)
    
    # ゲームログ
    section_header("ゲームログ / Game Log")
    
    display_cols = ['GameDate', 'Opponent', 'PTS', '3PM', '3PA', '3P%', 
                   'FTM', 'FTA', 'FT%', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'MIN']
    
    # 利用可能なカラムのみを表示
    available_cols = [col for col in display_cols if col in player_data.columns]
    
    st.dataframe(
        player_data[available_cols].sort_values('GameDate', ascending=False),
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # ゲームログダウンロード
    csv = player_data.to_csv(index=False)
    st.download_button(
        label="📥 ゲームログをダウンロード / Download Game Log",
        data=csv,
        file_name=f"{selected_player}_game_log.csv",
        mime="text/csv"
    )


def render_time_series_charts(player_data):
    """時系列推移チャートを表示"""
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_pts = create_nba_chart(
            player_data, 
            '得点推移 / POINTS TREND', 
            'GameDate', 
            'PTS'
        )
        st.plotly_chart(fig_pts, use_container_width=True)
    
    with chart_col2:
        fig_reb = create_nba_chart(
            player_data, 
            'リバウンド推移 / REBOUNDS TREND', 
            'GameDate', 
            'TOT', 
            color=NBA_COLORS['secondary']
        )
        st.plotly_chart(fig_reb, use_container_width=True)
    
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        fig_ast = create_nba_chart(
            player_data, 
            'アシスト推移 / ASSISTS TREND', 
            'GameDate', 
            'AST',
            color='#FDB927'
        )
        st.plotly_chart(fig_ast, use_container_width=True)
    
    with chart_col4:
        if 'STL' in player_data.columns:
            fig_stl = create_nba_chart(
                player_data, 
                'スティール推移 / STEALS TREND', 
                'GameDate', 
                'STL',
                color='#552583'
            )
            st.plotly_chart(fig_stl, use_container_width=True)


def render_category_comparison(stats, player_name):
    """カテゴリ別比較チャートを表示"""
    # スタッツデータを準備
    categories = ['PPG', 'RPG', 'APG', 'SPG', 'BPG']
    values = [
        stats.get('PTS', 0),
        stats.get('REB', 0),
        stats.get('AST', 0),
        stats.get('STL', 0),
        stats.get('BLK', 0)
    ]
    
    comparison_df = pd.DataFrame({
        'Category': categories,
        'Value': values
    })
    
    fig = create_bar_chart(
        comparison_df,
        f'{player_name} - カテゴリ別平均スタッツ',
        'Category',
        'Value',
        title_jp='Category Averages'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # シューティング成功率
    shooting_categories = ['FG%', '3P%', 'FT%']
    shooting_values = [
        stats.get('FG%', 0),
        stats.get('3P%', 0),
        stats.get('FT%', 0)
    ]
    
    shooting_df = pd.DataFrame({
        'Category': shooting_categories,
        'Percentage': shooting_values
    })
    
    fig2 = create_bar_chart(
        shooting_df,
        f'{player_name} - シューティング成功率',
        'Category',
        'Percentage',
        title_jp='Shooting Percentages'
    )
    st.plotly_chart(fig2, use_container_width=True)


def render_radar_chart_analysis(stats, player_name):
    """レーダーチャート分析を表示"""
    categories = ['得点', 'リバウンド', 'アシスト', 'スティール', 'ブロック']
    
    # 正規化（0-100スケール）
    max_vals = {
        'PTS': 30, 'REB': 15, 'AST': 10, 'STL': 3, 'BLK': 3
    }
    
    values = [
        min(stats.get('PTS', 0) / max_vals['PTS'] * 100, 100),
        min(stats.get('REB', 0) / max_vals['REB'] * 100, 100),
        min(stats.get('AST', 0) / max_vals['AST'] * 100, 100),
        min(stats.get('STL', 0) / max_vals['STL'] * 100, 100),
        min(stats.get('BLK', 0) / max_vals['BLK'] * 100, 100)
    ]
    
    fig = create_radar_chart(
        categories,
        [values],
        [player_name],
        f"{player_name} - 総合能力分析",
        "Overall Performance Analysis"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 能力評価コメント
    st.markdown("### 📊 能力評価")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 強み / Strengths")
        strengths = []
        if stats.get('PTS', 0) >= 15:
            strengths.append("✅ 高い得点力")
        if stats.get('REB', 0) >= 8:
            strengths.append("✅ 優れたリバウンド能力")
        if stats.get('AST', 0) >= 5:
            strengths.append("✅ 優秀なプレイメイク")
        if stats.get('STL', 0) >= 2:
            strengths.append("✅ 高いスティール能力")
        if stats.get('BLK', 0) >= 1.5:
            strengths.append("✅ 優れたブロック力")
        
        if strengths:
            for strength in strengths:
                st.markdown(strength)
        else:
            st.markdown("バランス型の選手です")
    
    with col2:
        st.markdown("#### シューティング評価")
        if stats.get('FG%', 0) >= 50:
            st.markdown("✅ 優秀なFG%")
        if stats.get('3P%', 0) >= 35:
            st.markdown("✅ 良好な3P%")
        if stats.get('FT%', 0) >= 75:
            st.markdown("✅ 高いFT%")
