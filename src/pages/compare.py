"""改良版比較ページ - 複数選手・シーズン比較対応"""
import streamlit as st
import pandas as pd
from database import StatsDatabase
from stats import calculate_stats
from charts import create_comparison_chart, create_radar_chart, create_bar_chart
from components import section_header, comparison_table
from config import NBA_COLORS, STAT_CATEGORIES


def render(db: StatsDatabase):
    """比較ページを表示
    
    Args:
        db: データベースインスタンス
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%); padding: 2.5rem 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            📊 データ比較
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">
            DATA COMPARISON / 選手・チーム・シーズン比較分析
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if db.df.empty:
        st.info("データがありません。")
        return
    
    # 比較モード選択
    compare_mode = st.radio(
        "比較モードを選択 / Select Comparison Mode",
        ["選手間比較 / Player vs Player", 
         "シーズン比較 / Season Comparison",
         "チーム vs 個人 / Team vs Individual"],
        horizontal=True
    )
    
    if compare_mode == "選手間比較 / Player vs Player":
        render_player_comparison(db)
    elif compare_mode == "シーズン比較 / Season Comparison":
        render_season_comparison(db)
    else:
        render_team_individual_comparison(db)


def render_player_comparison(db: StatsDatabase):
    """選手間比較を表示"""
    section_header("PLAYER COMPARISON", "選手間比較")
    
    players = db.get_all_players()
    
    # 複数選手選択
    st.markdown("### 比較する選手を選択（2〜4人）")
    
    col1, col2, col3, col4 = st.columns(4)
    
    selected_players = []
    
    with col1:
        p1 = st.selectbox("選手 1", [""] + players, key='cmp_p1')
        if p1:
            selected_players.append(p1)
    
    with col2:
        remaining = [p for p in players if p not in selected_players]
        p2 = st.selectbox("選手 2", [""] + remaining, key='cmp_p2')
        if p2:
            selected_players.append(p2)
    
    with col3:
        remaining = [p for p in players if p not in selected_players]
        p3 = st.selectbox("選手 3（オプション）", [""] + remaining, key='cmp_p3')
        if p3:
            selected_players.append(p3)
    
    with col4:
        remaining = [p for p in players if p not in selected_players]
        p4 = st.selectbox("選手 4（オプション）", [""] + remaining, key='cmp_p4')
        if p4:
            selected_players.append(p4)
    
    if len(selected_players) < 2:
        st.warning("⚠️ 少なくとも2人の選手を選択してください")
        return
    
    # 統計データ取得
    stats_list = [calculate_stats(db.df, player) for player in selected_players]
    
    # 比較テーブル
    section_header("STATISTICS COMPARISON", "統計比較")
    
    comparison_data = {
        'STAT / 項目': ['PPG / 平均得点', 'RPG / 平均リバウンド', 'APG / 平均アシスト', 
                       'SPG / 平均スティール', 'BPG / 平均ブロック', 
                       'FG% / FG成功率', '3P% / 3P成功率', 'FT% / FT成功率', 'GP / 試合数']
    }
    
    for i, (player, stats) in enumerate(zip(selected_players, stats_list)):
        comparison_data[player] = [
            f"{stats['PTS']:.1f}",
            f"{stats['REB']:.1f}",
            f"{stats['AST']:.1f}",
            f"{stats['STL']:.1f}",
            f"{stats['BLK']:.1f}",
            f"{stats['FG%']:.1f}%",
            f"{stats['3P%']:.1f}%",
            f"{stats['FT%']:.1f}%",
            str(stats['GP'])
        ]
    
    comparison_table(comparison_data)
    
    # グラフ比較
    section_header("VISUAL COMPARISON", "ビジュアル比較")
    
    chart_type = st.radio(
        "グラフタイプ",
        ["折れ線グラフ（推移）", "レーダーチャート（総合比較）", "棒グラフ（項目別）"],
        horizontal=True
    )
    
    if chart_type == "折れ線グラフ（推移）":
        # 時系列推移
        stat_to_compare = st.selectbox(
            "比較する統計項目",
            ['PTS', 'TOT', 'AST', 'STL', 'BLK'],
            format_func=lambda x: STAT_CATEGORIES[x]['label']
        )
        
        player_data_list = [db.get_player_data(p) for p in selected_players]
        
        fig = create_comparison_chart(
            player_data_list,
            selected_players,
            'GameDate',
            stat_to_compare,
            f"{STAT_CATEGORIES[stat_to_compare]['label']} COMPARISON",
            f"{STAT_CATEGORIES[stat_to_compare]['label']}の推移比較"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "レーダーチャート（総合比較）":
        # レーダーチャート
        categories = ['得点', 'リバウンド', 'アシスト', 'スティール', 'ブロック']
        
        values_list = []
        for stats in stats_list:
            # 正規化（0-100スケール）
            max_vals = {
                'PTS': 30, 'REB': 15, 'AST': 10, 'STL': 3, 'BLK': 3
            }
            values = [
                min(stats['PTS'] / max_vals['PTS'] * 100, 100),
                min(stats['REB'] / max_vals['REB'] * 100, 100),
                min(stats['AST'] / max_vals['AST'] * 100, 100),
                min(stats['STL'] / max_vals['STL'] * 100, 100),
                min(stats['BLK'] / max_vals['BLK'] * 100, 100)
            ]
            values_list.append(values)
        
        fig = create_radar_chart(
            categories,
            values_list,
            selected_players,
            "OVERALL STATS COMPARISON",
            "総合スタッツ比較"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # 棒グラフ
        stat_to_compare = st.selectbox(
            "比較する統計項目",
            ['PTS', 'TOT', 'AST', 'STL', 'BLK', 'FG%', '3P%'],
            format_func=lambda x: STAT_CATEGORIES.get(x, {'label': x})['label'],
            key='bar_stat'
        )
        
        bar_data = pd.DataFrame({
            'Player': selected_players,
            'Value': [stats[stat_to_compare] for stats in stats_list]
        })
        
        fig = create_bar_chart(
            bar_data,
            f"{STAT_CATEGORIES.get(stat_to_compare, {'label': stat_to_compare})['label']} COMPARISON",
            'Player',
            'Value',
            title_jp=f"{STAT_CATEGORIES.get(stat_to_compare, {'label': stat_to_compare})['label']}比較"
        )
        st.plotly_chart(fig, use_container_width=True)


def render_season_comparison(db: StatsDatabase):
    """シーズン比較を表示"""
    section_header("SEASON COMPARISON", "シーズン比較")
    
    seasons = db.get_all_seasons()
    
    if len(seasons) < 2:
        st.warning("⚠️ 比較するには2つ以上のシーズンデータが必要です")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        season1 = st.selectbox("シーズン 1", seasons, key='season_cmp1')
    
    with col2:
        remaining_seasons = [s for s in seasons if s != season1]
        season2 = st.selectbox("シーズン 2", remaining_seasons, key='season_cmp2')
    
    if season1 and season2:
        data1 = db.get_season_data(season1)
        data2 = db.get_season_data(season2)
        
        # チーム統計比較
        team_stats1 = {
            'games': len(data1['GameDate'].unique()),
            'wins': len(data1[data1['TeamScore'] > data1['OpponentScore']]['GameDate'].unique()),
            'avg_pts': data1.groupby('GameDate')['PTS'].sum().mean(),
            'avg_reb': data1.groupby('GameDate')['TOT'].sum().mean(),
            'avg_ast': data1.groupby('GameDate')['AST'].sum().mean()
        }
        
        team_stats2 = {
            'games': len(data2['GameDate'].unique()),
            'wins': len(data2[data2['TeamScore'] > data2['OpponentScore']]['GameDate'].unique()),
            'avg_pts': data2.groupby('GameDate')['PTS'].sum().mean(),
            'avg_reb': data2.groupby('GameDate')['TOT'].sum().mean(),
            'avg_ast': data2.groupby('GameDate')['AST'].sum().mean()
        }
        
        # 比較テーブル
        comparison_data = {
            'STAT / 項目': ['試合数', '勝利数', '平均得点', '平均リバウンド', '平均アシスト'],
            season1: [
                team_stats1['games'],
                team_stats1['wins'],
                f"{team_stats1['avg_pts']:.1f}",
                f"{team_stats1['avg_reb']:.1f}",
                f"{team_stats1['avg_ast']:.1f}"
            ],
            season2: [
                team_stats2['games'],
                team_stats2['wins'],
                f"{team_stats2['avg_pts']:.1f}",
                f"{team_stats2['avg_reb']:.1f}",
                f"{team_stats2['avg_ast']:.1f}"
            ]
        }
        
        comparison_table(comparison_data, highlight_max=False)


def render_team_individual_comparison(db: StatsDatabase):
    """チーム vs 個人比較を表示"""
    section_header("TEAM vs INDIVIDUAL", "チーム vs 個人比較")
    
    st.info("この機能は今後実装予定です")
