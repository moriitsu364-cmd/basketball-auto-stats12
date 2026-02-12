"""シーズン統計ページ"""
import streamlit as st
from database import StatsDatabase
from stats import calculate_season_overview, get_leaders
from charts import create_nba_chart
from components import stat_card, section_header, ranking_row
from config import NBA_COLORS


def render(db: StatsDatabase):
    """シーズン統計ページを表示
    
    Args:
        db: データベースインスタンス
    """
    if db.df.empty:
        st.info("No data available. Please add data in the DATA INPUT tab.")
        return
    
    seasons = db.get_all_seasons()
    
    # シーズン選択
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        selected_season = st.selectbox("SELECT SEASON", seasons, key='season_select')
    with col2:
        st.write("")
    with col3:
        if st.button("EXPORT DATA"):
            csv = db.get_season_data(selected_season).to_csv(index=False)
            st.download_button(
                label="DOWNLOAD CSV",
                data=csv,
                file_name=f"stats_{selected_season}.csv",
                mime="text/csv"
            )
    
    if not selected_season:
        return
    
    season_data = db.get_season_data(selected_season)
    
    # シーズン概要
    section_header("Season Overview")
    
    overview = calculate_season_overview(season_data)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        stat_card("Games Played", overview['games'], card_type="primary")
    
    with col2:
        stat_card("Players", overview['players'])
    
    with col3:
        stat_card("Avg Points", f"{overview['avg_pts']:.1f}", card_type="primary")
    
    with col4:
        stat_card("Wins", overview['wins'])
    
    with col5:
        stat_card("Losses", overview['losses'], card_type="secondary")
    
    # チームパフォーマンス
    section_header("Team Performance")
    
    game_stats = season_data.groupby('GameDate').agg({
        'PTS': 'sum',
        'TOT': 'sum',
        'AST': 'sum'
    }).reset_index()
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_pts = create_nba_chart(game_stats, 'POINTS PER GAME', 'GameDate', 'PTS')
        st.plotly_chart(fig_pts, use_container_width=True)
    
    with chart_col2:
        fig_ast = create_nba_chart(
            game_stats, 
            'ASSISTS PER GAME', 
            'GameDate', 
            'AST', 
            color=NBA_COLORS['secondary']
        )
        st.plotly_chart(fig_ast, use_container_width=True)
    
    # リーダーボード
    section_header("League Leaders")
    
    leader_tab1, leader_tab2, leader_tab3 = st.tabs([
        "POINTS", "REBOUNDS", "ASSISTS"
    ])
    
    with leader_tab1:
        pts_leaders = get_leaders(season_data, 'PTS')
        
        for idx, (player, row) in enumerate(pts_leaders.iterrows(), 1):
            ranking_row(idx, player, row['PPG'], 'PPG', NBA_COLORS['primary'])
    
    with leader_tab2:
        reb_leaders = get_leaders(season_data, 'TOT')
        
        for idx, (player, row) in enumerate(reb_leaders.iterrows(), 1):
            ranking_row(idx, player, row['RPG'], 'RPG', NBA_COLORS['secondary'])
    
    with leader_tab3:
        ast_leaders = get_leaders(season_data, 'AST')
        
        for idx, (player, row) in enumerate(ast_leaders.iterrows(), 1):
            ranking_row(idx, player, row['APG'], 'APG', NBA_COLORS['primary'])
