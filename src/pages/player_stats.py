"""選手統計ページ"""
import streamlit as st
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from stats import calculate_stats
from charts import create_nba_chart
from components import stat_card, section_header, player_card
from config import NBA_COLORS


def render(db: StatsDatabase):
    """選手統計ページを表示
    
    Args:
        db: データベースインスタンス
    """
    if db.df.empty:
        st.info("No data available.")
        return
    
    players = db.get_all_players()
    
    selected_player = st.selectbox("SELECT PLAYER", players, key='player_select')
    
    if not selected_player:
        return
    
    player_data = db.get_player_data(selected_player)
    
    # 選手情報
    stats = calculate_stats(db.df, selected_player)
    player_number = player_data['No'].iloc[0] if len(player_data) > 0 else "N/A"
    
    player_card(selected_player, player_number)
    
    # 主要スタッツ
    section_header("Season Averages")
    
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
    
    # グラフ
    section_header("Performance Charts")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_pts = create_nba_chart(player_data, 'POINTS PER GAME', 'GameDate', 'PTS')
        st.plotly_chart(fig_pts, use_container_width=True)
    
    with chart_col2:
        fig_reb = create_nba_chart(
            player_data, 
            'REBOUNDS PER GAME', 
            'GameDate', 
            'TOT', 
            color=NBA_COLORS['secondary']
        )
        st.plotly_chart(fig_reb, use_container_width=True)
    
    # ゲームログ
    section_header("Game Log")
    
    display_cols = ['GameDate', 'Opponent', 'PTS', '3PM', '3PA', '3P%', 
                   'FTM', 'FTA', 'FT%', 'TOT', 'AST', 'STL', 'BLK', 'MIN']
    
    st.dataframe(
        player_data[display_cols],
        use_container_width=True,
        hide_index=True,
        height=400
    )
