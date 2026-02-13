"""対戦相手統計ページ - シーズン別対戦相手分析"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from components import section_header, stat_card
from charts import create_bar_chart, create_pie_chart
from config import NBA_COLORS


def calculate_opponent_stats(db: StatsDatabase, season: str) -> pd.DataFrame:
    """対戦相手ごとの統計を計算
    
    Args:
        db: データベースインスタンス
        season: シーズン
    
    Returns:
        対戦相手統計のデータフレーム
    """
    season_data = db.get_season_data(season)
    
    if season_data.empty:
        return pd.DataFrame()
    
    # 対戦相手ごとに集計
    opponent_stats = []
    
    for opponent in season_data['Opponent'].unique():
        opp_games = season_data[season_data['Opponent'] == opponent]
        
        games_played = len(opp_games['GameDate'].unique())
        wins = len(opp_games[opp_games['TeamScore'] > opp_games['OpponentScore']]['GameDate'].unique())
        losses = games_played - wins
        
        # 集計
        team_pts = opp_games.groupby('GameDate')['PTS'].sum().mean()
        opp_pts = opp_games.groupby('GameDate')['OpponentScore'].first().mean()
        team_reb = opp_games.groupby('GameDate')['TOT'].sum().mean()
        team_ast = opp_games.groupby('GameDate')['AST'].sum().mean()
        
        opponent_stats.append({
            'Opponent': opponent,
            'GamesPlayed': games_played,
            'Wins': wins,
            'Losses': losses,
            'WinRate': (wins / games_played * 100) if games_played > 0 else 0,
            'AvgPtsFor': team_pts,
            'AvgPtsAgainst': opp_pts,
            'AvgRebFor': team_reb,
            'AvgAstFor': team_ast,
            'PtsDiff': team_pts - opp_pts
        })
    
    return pd.DataFrame(opponent_stats).sort_values('GamesPlayed', ascending=False)


def render(db: StatsDatabase):
    """対戦相手統計ページを表示
    
    Args:
        db: データベースインスタンス
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #c8102e 0%, #1d428a 100%); padding: 2.5rem 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            🎯 対戦相手統計
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">
            OPPONENT STATISTICS / シーズン別対戦分析
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if db.df.empty:
        st.info("データがありません。DATA INPUTタブからデータを追加してください。")
        return
    
    seasons = db.get_all_seasons()
    
    # シーズン選択
    col1, col2 = st.columns([2, 3])
    with col1:
        selected_season = st.selectbox(
            "シーズンを選択 / Select Season",
            seasons,
            key='opponent_season'
        )
    
    if not selected_season:
        return
    
    # 対戦相手統計を計算
    opponent_stats = calculate_opponent_stats(db, selected_season)
    
    if opponent_stats.empty:
        st.warning(f"{selected_season}シーズンのデータがありません。")
        return
    
    # サマリー
    section_header("SEASON SUMMARY", "シーズンサマリー")
    
    total_games = opponent_stats['GamesPlayed'].sum()
    total_wins = opponent_stats['Wins'].sum()
    total_losses = opponent_stats['Losses'].sum()
    avg_pts_for = opponent_stats['AvgPtsFor'].mean()
    avg_pts_against = opponent_stats['AvgPtsAgainst'].mean()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        stat_card("Total Games", total_games, "試合", "primary", "総試合数")
    
    with col2:
        stat_card("Wins", total_wins, "勝", "primary", "勝利")
    
    with col3:
        stat_card("Losses", total_losses, "敗", "secondary", "敗北")
    
    with col4:
        stat_card("Win Rate", f"{(total_wins/total_games*100):.1f}%", "勝率", "primary", "勝率")
    
    with col5:
        stat_card("Avg Points", f"{avg_pts_for:.1f}", "平均得点", "", "平均得点")
    
    # 対戦成績一覧
    section_header("HEAD-TO-HEAD RECORDS", "対戦成績一覧")
    
    # テーブル表示
    display_df = opponent_stats[['Opponent', 'GamesPlayed', 'Wins', 'Losses', 'WinRate', 
                                  'AvgPtsFor', 'AvgPtsAgainst', 'PtsDiff']].copy()
    display_df.columns = ['対戦相手', '試合数', '勝', '敗', '勝率(%)', 
                          '平均得点', '平均失点', '得失点差']
    display_df = display_df.round(1)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # グラフ
    section_header("VISUAL ANALYSIS", "ビジュアル分析")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # 対戦成績棒グラフ
        fig_wins = create_bar_chart(
            opponent_stats.head(10),
            "WINS BY OPPONENT",
            'Opponent',
            'Wins',
            title_jp="対戦相手別勝利数（上位10チーム）"
        )
        st.plotly_chart(fig_wins, use_container_width=True)
    
    with chart_col2:
        # 勝率円グラフ
        if len(opponent_stats) > 0:
            # 勝敗の内訳
            fig_pie = create_pie_chart(
                ['勝利', '敗北'],
                [total_wins, total_losses],
                "WIN-LOSS RATIO",
                "勝敗比率"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # 個別相手詳細
    section_header("DETAILED OPPONENT ANALYSIS", "個別対戦相手詳細分析")
    
    selected_opponent = st.selectbox(
        "対戦相手を選択 / Select Opponent",
        opponent_stats['Opponent'].tolist(),
        key='detail_opponent'
    )
    
    if selected_opponent:
        opp_info = opponent_stats[opponent_stats['Opponent'] == selected_opponent].iloc[0]
        
        # 詳細情報カード
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            stat_card("Games", int(opp_info['GamesPlayed']), "試合数", "primary")
        
        with col2:
            stat_card("Record", f"{int(opp_info['Wins'])}-{int(opp_info['Losses'])}", "勝敗", "")
        
        with col3:
            stat_card("Win Rate", f"{opp_info['WinRate']:.1f}%", "勝率", "primary")
        
        with col4:
            diff_color = "primary" if opp_info['PtsDiff'] > 0 else "secondary"
            stat_card("Pt Diff", f"{opp_info['PtsDiff']:+.1f}", "得失点差", diff_color)
        
        # 試合履歴
        st.markdown("#### 試合履歴 / Game History")
        
        season_data = db.get_season_data(selected_season)
        opp_games = season_data[season_data['Opponent'] == selected_opponent]
        
        game_history = opp_games.groupby('GameDate').agg({
            'TeamScore': 'first',
            'OpponentScore': 'first',
            'PTS': 'sum',
            'TOT': 'sum',
            'AST': 'sum'
        }).reset_index()
        
        game_history['Result'] = game_history.apply(
            lambda x: '勝利' if x['TeamScore'] > x['OpponentScore'] else '敗北',
            axis=1
        )
        game_history.columns = ['日付', 'チームスコア', '相手スコア', '総得点', '総リバウンド', '総アシスト', '結果']
        
        st.dataframe(
            game_history,
            use_container_width=True,
            hide_index=True
        )
