"""試合統計ページ"""
import streamlit as st
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from stats import calculate_team_stats
from components import stat_card, section_header, game_card


def render(db: StatsDatabase):
    """試合統計ページを表示
    
    Args:
        db: データベースインスタンス
    """
    if db.df.empty:
        st.info("No data available.")
        return
    
    games = db.get_all_games()
    
    selected_game = st.selectbox("SELECT GAME", games, key='game_select')
    
    if not selected_game:
        return
    
    game_data = db.get_game_data(selected_game)
    
    # 試合情報
    opponent = game_data['Opponent'].iloc[0]
    team_score = game_data['TeamScore'].iloc[0]
    opp_score = game_data['OpponentScore'].iloc[0]
    
    game_card(selected_game, opponent, team_score, opp_score)
    
    # チーム統計
    section_header("Team Statistics")
    
    team_stats = calculate_team_stats(game_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stat_card("Total Points", team_stats['total_pts'], card_type="primary")
    
    with col2:
        stat_card("Total Rebounds", team_stats['total_reb'])
    
    with col3:
        stat_card("Total Assists", team_stats['total_ast'])
    
    with col4:
        stat_card("FG%", f"{team_stats['fg_pct']:.1f}%")
    
    # プレイヤーボックススコア
    section_header("Player Box Score")
    
    display_cols = ['No', 'PlayerName', 'PTS', '3PM', '3PA', '2PM', '2PA', 
                   'FTM', 'FTA', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'PF', 'MIN']
    
    st.dataframe(
        game_data[display_cols].sort_values('PTS', ascending=False),
        use_container_width=True,
        hide_index=True,
        height=500
    )
