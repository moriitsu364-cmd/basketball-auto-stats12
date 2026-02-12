"""選手比較ページ"""
import streamlit as st
import pandas as pd
from database import StatsDatabase
from stats import calculate_stats
from charts import create_comparison_chart
from components import section_header


def render(db: StatsDatabase):
    """選手比較ページを表示
    
    Args:
        db: データベースインスタンス
    """
    if db.df.empty:
        st.info("No data available.")
        return
    
    players = db.get_all_players()
    
    section_header("Player Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("PLAYER 1", players, key='compare_p1')
    
    with col2:
        remaining = [p for p in players if p != player1]
        player2 = st.selectbox("PLAYER 2", remaining, key='compare_p2') if remaining else None
    
    if not player1 or not player2:
        return
    
    stats1 = calculate_stats(db.df, player1)
    stats2 = calculate_stats(db.df, player2)
    
    # 比較テーブル
    comparison_data = {
        'STAT': ['PPG', 'RPG', 'APG', 'SPG', 'BPG', 'FG%', '3P%', 'FT%', 'GP'],
        player1: [
            f"{stats1['PTS']:.1f}", f"{stats1['REB']:.1f}", f"{stats1['AST']:.1f}",
            f"{stats1['STL']:.1f}", f"{stats1['BLK']:.1f}", f"{stats1['FG%']:.1f}",
            f"{stats1['3P%']:.1f}", f"{stats1['FT%']:.1f}", f"{stats1['GP']}"
        ],
        player2: [
            f"{stats2['PTS']:.1f}", f"{stats2['REB']:.1f}", f"{stats2['AST']:.1f}",
            f"{stats2['STL']:.1f}", f"{stats2['BLK']:.1f}", f"{stats2['FG%']:.1f}",
            f"{stats2['3P%']:.1f}", f"{stats2['FT%']:.1f}", f"{stats2['GP']}"
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True, height=400)
    
    # パフォーマンス比較グラフ
    section_header("Performance Comparison")
    
    player1_data = db.get_player_data(player1)
    player2_data = db.get_player_data(player2)
    
    fig = create_comparison_chart(player1_data, player2_data, player1, player2, 'GameDate', 'PTS')
    st.plotly_chart(fig, use_container_width=True)
