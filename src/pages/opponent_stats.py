"""対戦相手統計ページ - 完全リニューアル版（相手チームデータ・比較機能付き）"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from components import section_header, stat_card
from charts import create_bar_chart, create_pie_chart, create_comparison_chart
from config import NBA_COLORS


def render(db: StatsDatabase):
    """対戦相手統計ページを表示（リニューアル版）
    
    Args:
        db: データベースインスタンス
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #c8102e 0%, #1d428a 100%); padding: 2.5rem 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            🎯 対戦相手分析
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">
            OPPONENT ANALYSIS / 相手チームスタッツ・試合比較
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if db.df.empty:
        st.info("📊 現在データがありません / No data available.\n\nデータ入力タブからデータを追加してください。")
        return
    
    # モード選択
    analysis_mode = st.radio(
        "分析モードを選択 / Select Analysis Mode",
        ["対戦成績サマリー / Head-to-Head Summary", 
         "個別試合比較 / Game-by-Game Comparison",
         "相手チーム詳細 / Opponent Team Details"],
        horizontal=True
    )
    
    if analysis_mode == "対戦成績サマリー / Head-to-Head Summary":
        render_head_to_head_summary(db)
    elif analysis_mode == "個別試合比較 / Game-by-Game Comparison":
        render_game_comparison(db)
    else:
        render_opponent_details(db)


def render_head_to_head_summary(db: StatsDatabase):
    """対戦成績サマリーを表示"""
    section_header("HEAD-TO-HEAD SUMMARY", "対戦成績サマリー")
    
    seasons = db.get_all_seasons()
    
    if not seasons:
        st.warning("⚠️ データがありません")
        return
    
    # シーズン選択
    selected_season = st.selectbox(
        "シーズンを選択 / Select Season",
        ["全シーズン / ALL"] + seasons,
        key='opponent_season'
    )
    
    if selected_season == "全シーズン / ALL":
        season_data = db.df
    else:
        season_data = db.get_season_data(selected_season)
    
    if season_data.empty:
        st.warning("⚠️ データがありません")
        return
    
    # 対戦相手ごとの統計を計算
    opponent_stats = calculate_opponent_stats(season_data)
    
    if opponent_stats.empty:
        st.warning("⚠️ 対戦相手データがありません")
        return
    
    # サマリーカード
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
        win_rate = (total_wins/total_games*100) if total_games > 0 else 0
        stat_card("Win Rate", f"{win_rate:.1f}%", "勝率", "primary", "勝率")
    
    with col5:
        stat_card("Avg Points", f"{avg_pts_for:.1f}", "平均得点", "", "平均得点")
    
    st.markdown("---")
    
    # 対戦成績一覧
    section_header("RECORDS BY OPPONENT", "対戦相手別成績")
    
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
    st.markdown("---")
    section_header("VISUAL ANALYSIS", "ビジュアル分析")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_wins = create_bar_chart(
            opponent_stats.head(10),
            "対戦相手別勝利数 / Wins by Opponent",
            'Opponent',
            'Wins',
            title_jp="Top 10 Most Played Opponents"
        )
        st.plotly_chart(fig_wins, use_container_width=True)
    
    with chart_col2:
        if len(opponent_stats) > 0:
            fig_pie = create_pie_chart(
                ['勝利', '敗北'],
                [total_wins, total_losses],
                "勝敗比率 / Win-Loss Ratio",
                "Overall Record"
            )
            st.plotly_chart(fig_pie, use_container_width=True)


def render_game_comparison(db: StatsDatabase):
    """個別試合比較を表示"""
    section_header("GAME-BY-GAME COMPARISON", "個別試合比較")
    
    st.markdown("""
    この機能では、特定の試合における自チームと相手チームのスタッツを比較できます。
    """)
    
    # シーズン選択
    seasons = db.get_all_seasons()
    if not seasons:
        st.warning("⚠️ データがありません")
        return
    
    selected_season = st.selectbox(
        "シーズンを選択 / Select Season",
        seasons,
        key='game_comp_season'
    )
    
    season_data = db.get_season_data(selected_season)
    
    if season_data.empty:
        st.warning("⚠️ データがありません")
        return
    
    # 試合リストを取得
    games = season_data.groupby(['GameDate', 'Opponent']).size().reset_index()[['GameDate', 'Opponent']]
    game_options = [f"{row['GameDate']} vs {row['Opponent']}" for _, row in games.iterrows()]
    
    if not game_options:
        st.warning("⚠️ 試合データがありません")
        return
    
    selected_game = st.selectbox(
        "試合を選択 / Select Game",
        game_options,
        key='comp_game_select'
    )
    
    # 選択された試合のデータを取得
    game_date = selected_game.split(" vs ")[0]
    opponent = selected_game.split(" vs ")[1]
    
    game_data = season_data[
        (season_data['GameDate'] == game_date) & 
        (season_data['Opponent'] == opponent)
    ]
    
    if game_data.empty:
        st.warning("⚠️ 試合データがありません")
        return
    
    # 試合情報表示
    team_score = game_data['TeamScore'].iloc[0]
    opp_score = game_data['OpponentScore'].iloc[0]
    
    st.markdown(f"""
    ### 📅 {game_date}
    ### 🏀 筑波大学附属高校 **{team_score}** - **{opp_score}** {opponent}
    """)
    
    result = "勝利 🎉" if team_score > opp_score else "敗北 😔"
    st.markdown(f"**試合結果:** {result}")
    
    st.markdown("---")
    
    # チーム統計比較
    section_header("TEAM STATS COMPARISON", "チーム統計比較")
    
    # 自チームのスタッツ
    team_pts = game_data['PTS'].sum()
    team_reb = game_data['TOT'].sum()
    team_ast = game_data['AST'].sum()
    team_stl = game_data.get('STL', pd.Series([0])).sum()
    team_blk = game_data.get('BLK', pd.Series([0])).sum()
    
    team_fgm = game_data['2PM'].sum() + game_data['3PM'].sum()
    team_fga = game_data['2PA'].sum() + game_data['3PA'].sum()
    team_fg_pct = (team_fgm / team_fga * 100) if team_fga > 0 else 0
    
    # 比較テーブル
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 筑波大学附属高校")
        stat_card("Total Points", team_pts, "総得点", "primary")
        stat_card("Total Rebounds", team_reb, "総リバウンド")
        stat_card("Total Assists", team_ast, "総アシスト")
        stat_card("FG%", f"{team_fg_pct:.1f}%", "FG成功率")
    
    with col2:
        st.markdown(f"#### {opponent}")
        st.info("""
        💡 **相手チームの詳細データを表示するには:**
        
        データ入力タブで相手チームのスタッツを登録してください。
        相手チーム選手の個人スタッツも記録できます。
        """)
        
        # もし相手チームデータがあれば表示
        # （将来的な拡張ポイント）
        stat_card("Total Points", opp_score, "総得点", "secondary")
        st.markdown("*詳細データは未登録*")
    
    st.markdown("---")
    
    # 個人スタッツ（自チーム）
    section_header("PLAYER STATS", "選手別スタッツ（筑波大附属）")
    
    display_cols = ['PlayerName', 'PTS', 'TOT', 'AST', 'STL', 'BLK', '3PM', 'FTM']
    available_cols = [col for col in display_cols if col in game_data.columns]
    
    st.dataframe(
        game_data[available_cols].sort_values('PTS', ascending=False),
        use_container_width=True,
        hide_index=True,
        height=400
    )


def render_opponent_details(db: StatsDatabase):
    """相手チーム詳細を表示"""
    section_header("OPPONENT TEAM DETAILS", "相手チーム詳細")
    
    st.info("""
    ### 🚀 相手チーム詳細機能について
    
    この機能は、相手チームの選手データを登録・分析するためのものです。
    
    **使い方:**
    1. データ入力タブで「相手チーム」を選択
    2. 相手チーム名と選手データを入力
    3. このページで相手チームの詳細分析が可能に
    
    **できること:**
    - 相手チーム選手の個人スタッツ閲覧
    - 相手チームのシーズン成績分析
    - 自チーム vs 相手チームの詳細比較
    """)
    
    # 将来的な実装ポイント:
    # - 相手チームデータベースの実装
    # - 相手チーム選手の個人スタッツ管理
    # - より詳細な比較分析


def calculate_opponent_stats(season_data: pd.DataFrame) -> pd.DataFrame:
    """対戦相手ごとの統計を計算"""
    if season_data.empty:
        return pd.DataFrame()
    
    opponent_stats = []
    
    for opponent in season_data['Opponent'].unique():
        opp_games = season_data[season_data['Opponent'] == opponent]
        
        games_played = len(opp_games['GameDate'].unique())
        
        # 勝敗を計算
        game_results = opp_games.groupby('GameDate').agg({
            'TeamScore': 'first',
            'OpponentScore': 'first'
        })
        
        wins = len(game_results[game_results['TeamScore'] > game_results['OpponentScore']])
        losses = games_played - wins
        
        # 統計を集計
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
