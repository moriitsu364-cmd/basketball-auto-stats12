"""シーズン統計ページ - 改良版（日英対応、ランキング修正）"""
import streamlit as st
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from stats import calculate_season_overview, get_leaders
from charts import create_nba_chart, create_bar_chart, create_pie_chart
from components import stat_card, section_header, ranking_row
from config import NBA_COLORS, PLAYER_IMAGES_DIR
import pandas as pd


def render(db: StatsDatabase):
    """シーズン統計ページを表示
    
    Args:
        db: データベースインスタンス
    """
    if db.df.empty:
        st.info("データがありません。データ入力タブからデータを追加してください。 / No data available. Please add data in the DATA INPUT tab.")
        return
    
    seasons = db.get_all_seasons()
    
    # シーズン選択
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        selected_season = st.selectbox(
            "シーズン選択 / SELECT SEASON", 
            seasons, 
            key='season_select'
        )
    with col2:
        st.write("")
    with col3:
        if st.button("データエクスポート / EXPORT"):
            csv = db.get_season_data(selected_season).to_csv(index=False)
            st.download_button(
                label="CSV ダウンロード",
                data=csv,
                file_name=f"stats_{selected_season}.csv",
                mime="text/csv"
            )
    
    if not selected_season:
        return
    
    season_data = db.get_season_data(selected_season)
    
    # シーズン概要
    section_header("シーズン概要 / Season Overview")
    
    overview = calculate_season_overview(season_data)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        stat_card("試合数", overview['games'], card_type="primary", label_jp="Games Played")
    
    with col2:
        stat_card("選手数", overview['players'], label_jp="Players")
    
    with col3:
        stat_card("平均得点", f"{overview['avg_pts']:.1f}", card_type="primary", label_jp="Avg Points")
    
    with col4:
        stat_card("勝利", overview['wins'], label_jp="Wins")
    
    with col5:
        stat_card("敗北", overview['losses'], card_type="secondary", label_jp="Losses")
    
    # チームパフォーマンス
    section_header("チームパフォーマンス / Team Performance")
    
    # ゲームごとの統計を正しく集計
    game_stats = season_data.groupby('GameDate').agg({
        'PTS': 'sum',
        'TOT': 'sum',
        'AST': 'sum',
        'GameDate': 'first'
    }).reset_index(drop=True)
    
    # 日付でソート
    game_stats = game_stats.sort_values('GameDate')
    game_stats['GameNumber'] = range(1, len(game_stats) + 1)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # 折れ線グラフ（試合番号を横軸に）
        fig_pts = create_nba_chart(
            game_stats, 
            '試合ごとの得点', 
            'GameNumber', 
            'PTS',
            title_jp='Points Per Game'
        )
        st.plotly_chart(fig_pts, use_container_width=True)
    
    with chart_col2:
        # 折れ線グラフ（アシスト）
        fig_ast = create_nba_chart(
            game_stats, 
            '試合ごとのアシスト', 
            'GameNumber', 
            'AST', 
            color=NBA_COLORS['secondary'],
            title_jp='Assists Per Game'
        )
        st.plotly_chart(fig_ast, use_container_width=True)
    
    # グラフの追加セクション
    section_header("詳細統計 / Detailed Statistics")
    
    graph_col1, graph_col2 = st.columns(2)
    
    with graph_col1:
        # 棒グラフ: トップ5得点者
        top_scorers = season_data.groupby('PlayerName')['PTS'].sum().sort_values(ascending=False).head(5)
        top_scorers_df = pd.DataFrame({
            'PlayerName': top_scorers.index,
            'TotalPoints': top_scorers.values
        })
        
        fig_bar = create_bar_chart(
            top_scorers_df,
            'トップスコアラー',
            'PlayerName',
            'TotalPoints',
            title_jp='Top Scorers'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with graph_col2:
        # 円グラフ: 得点分布
        total_points_by_player = season_data.groupby('PlayerName')['PTS'].sum().sort_values(ascending=False).head(8)
        
        fig_pie = create_pie_chart(
            labels=total_points_by_player.index.tolist(),
            values=total_points_by_player.values.tolist(),
            title='得点分布',
            title_jp='Points Distribution'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # リーダーボード（改良版）
    section_header("リーダーボード / League Leaders")
    
    leader_tab1, leader_tab2, leader_tab3 = st.tabs([
        "得点 / POINTS", 
        "リバウンド / REBOUNDS", 
        "アシスト / ASSISTS"
    ])
    
    with leader_tab1:
        pts_leaders = get_leaders(season_data, 'PTS')
        
        for idx, (player, row) in enumerate(pts_leaders.iterrows(), 1):
            # 選手画像のパスを取得
            player_image = None
            image_path = PLAYER_IMAGES_DIR / f"{player}.png"
            if image_path.exists():
                player_image = str(image_path)
            
            # 選手番号を取得（データベースから）
            player_data = season_data[season_data['PlayerName'] == player]
            player_number = ""
            if 'PlayerNumber' in player_data.columns and not player_data.empty:
                player_number = str(player_data['PlayerNumber'].iloc[0])
            
            ranking_row(
                rank=idx,
                player=player,
                player_number=player_number,
                stat_value=row['PPG'],
                stat_label='PPG',
                color=NBA_COLORS['primary'],
                image_path=player_image
            )
    
    with leader_tab2:
        reb_leaders = get_leaders(season_data, 'TOT')
        
        for idx, (player, row) in enumerate(reb_leaders.iterrows(), 1):
            player_image = None
            image_path = PLAYER_IMAGES_DIR / f"{player}.png"
            if image_path.exists():
                player_image = str(image_path)
            
            player_data = season_data[season_data['PlayerName'] == player]
            player_number = ""
            if 'PlayerNumber' in player_data.columns and not player_data.empty:
                player_number = str(player_data['PlayerNumber'].iloc[0])
            
            ranking_row(
                rank=idx,
                player=player,
                player_number=player_number,
                stat_value=row['RPG'],
                stat_label='RPG',
                color=NBA_COLORS['secondary'],
                image_path=player_image
            )
    
    with leader_tab3:
        ast_leaders = get_leaders(season_data, 'AST')
        
        for idx, (player, row) in enumerate(ast_leaders.iterrows(), 1):
            player_image = None
            image_path = PLAYER_IMAGES_DIR / f"{player}.png"
            if image_path.exists():
                player_image = str(image_path)
            
            player_data = season_data[season_data['PlayerName'] == player]
            player_number = ""
            if 'PlayerNumber' in player_data.columns and not player_data.empty:
                player_number = str(player_data['PlayerNumber'].iloc[0])
            
            ranking_row(
                rank=idx,
                player=player,
                player_number=player_number,
                stat_value=row['APG'],
                stat_label='APG',
                color=NBA_COLORS['primary'],
                image_path=player_image
            )
