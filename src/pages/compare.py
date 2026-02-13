"""比較ページ - 完全リニューアル版（貢献度計算機能付き）"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from ..database import StatsDatabase
from ..stats import calculate_stats
from ..charts import create_comparison_chart, create_radar_chart, create_bar_chart
from ..components import section_header, comparison_table
from ..config import NBA_COLORS, STAT_CATEGORIES


def calculate_contribution_score(stats_dict):
    """貢献度スコアを計算
    
    計算式:
    貢献度 = (得点 × 1.0) + (リバウンド × 1.2) + (アシスト × 1.5) + 
             (スティール × 3.0) + (ブロック × 3.0) - (TO × 2.0)
    
    Args:
        stats_dict: 統計データの辞書
    
    Returns:
        貢献度スコア
    """
    score = (
        stats_dict.get('PTS', 0) * 1.0 +
        stats_dict.get('REB', 0) * 1.2 +
        stats_dict.get('AST', 0) * 1.5 +
        stats_dict.get('STL', 0) * 3.0 +
        stats_dict.get('BLK', 0) * 3.0 -
        stats_dict.get('TO', 0) * 2.0
    )
    return round(score, 2)


def render(db: StatsDatabase):
    """比較ページを表示（リニューアル版）
    
    Args:
        db: データベースインスタンス
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%); padding: 2.5rem 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            📊 データ比較
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">
            DATA COMPARISON / 選手・シーズン比較分析 + 貢献度計算
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if db.df.empty:
        st.info("📊 現在データがありません / No data available.")
        return
    
    # 比較モード選択
    compare_mode = st.radio(
        "比較モードを選択 / Select Comparison Mode",
        ["選手間比較（同一シーズン）/ Player vs Player (Same Season)", 
         "同一選手の異シーズン比較 / Same Player (Different Seasons)",
         "シーズン間比較 / Season Comparison",
         "貢献度ランキング / Contribution Ranking"],
        horizontal=False
    )
    
    if compare_mode == "選手間比較（同一シーズン）/ Player vs Player (Same Season)":
        render_player_comparison(db)
    elif compare_mode == "同一選手の異シーズン比較 / Same Player (Different Seasons)":
        render_player_season_comparison(db)
    elif compare_mode == "シーズン間比較 / Season Comparison":
        render_season_comparison(db)
    else:
        render_contribution_ranking(db)


def render_player_comparison(db: StatsDatabase):
    """選手間比較（同一シーズン）を表示"""
    section_header("PLAYER COMPARISON (SAME SEASON)", "選手間比較（同一シーズン）")
    
    # シーズン選択
    seasons = db.get_all_seasons()
    if not seasons:
        st.warning("⚠️ データがありません")
        return
    
    selected_season = st.selectbox(
        "シーズン選択 / Select Season",
        seasons,
        key='comp_season'
    )
    
    players = db.get_all_players(season=selected_season)
    
    if len(players) < 2:
        st.warning("⚠️ 比較するには2人以上の選手が必要です")
        return
    
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
    season_df = db.get_season_data(selected_season)
    stats_list = [calculate_stats(season_df, player) for player in selected_players]
    
    # 貢献度スコアを計算
    for stats in stats_list:
        stats['Contribution'] = calculate_contribution_score(stats)
    
    # 比較テーブル
    section_header("STATISTICS COMPARISON", "統計比較")
    
    comparison_data = {
        'STAT / 項目': [
            'PPG / 平均得点', 'RPG / 平均リバウンド', 'APG / 平均アシスト', 
            'SPG / 平均スティール', 'BPG / 平均ブロック', 
            'FG% / FG成功率', '3P% / 3P成功率', 'FT% / FT成功率', 
            'GP / 試合数', '**貢献度スコア**'
        ]
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
            str(stats['GP']),
            f"**{stats['Contribution']:.2f}**"
        ]
    
    comparison_table(comparison_data)
    
    # 貢献度スコアの説明
    with st.expander("ℹ️ 貢献度スコアとは？"):
        st.markdown("""
        ### 📊 貢献度スコア計算式
        
        ```
        貢献度 = (得点 × 1.0) + (リバウンド × 1.2) + (アシスト × 1.5) + 
                 (スティール × 3.0) + (ブロック × 3.0) - (ターンオーバー × 2.0)
        ```
        
        #### 重み付けの理由:
        - **得点 (×1.0)**: 基本的な貢献。直接的な得点が試合結果に影響
        - **リバウンド (×1.2)**: ボール保持権の確保。次の攻撃機会を生む
        - **アシスト (×1.5)**: チームプレーの要。味方の得点機会を創出
        - **スティール (×3.0)**: 守備力の指標。相手の攻撃を阻止し速攻につなげる
        - **ブロック (×3.0)**: リム保護能力。確実な得点阻止
        - **ターンオーバー (×-2.0)**: マイナス要素。相手に攻撃機会を与える
        
        この計算式により、総合的なプレー貢献度を定量化できます。
        """)
    
    # グラフ比較
    section_header("VISUAL COMPARISON", "ビジュアル比較")
    
    render_comparison_charts(db, selected_players, stats_list, selected_season)


def render_player_season_comparison(db: StatsDatabase):
    """同一選手の異シーズン比較を表示"""
    section_header("SAME PLAYER - DIFFERENT SEASONS", "同一選手の異シーズン比較")
    
    players = db.get_all_players()
    
    if not players:
        st.warning("⚠️ データがありません")
        return
    
    selected_player = st.selectbox(
        "選手を選択 / Select Player",
        players,
        key='season_comp_player'
    )
    
    # その選手がプレーしたシーズンを取得
    player_data = db.get_player_data(selected_player)
    player_seasons = sorted(player_data['Season'].unique().tolist(), reverse=True)
    
    if len(player_seasons) < 2:
        st.warning(f"⚠️ {selected_player}は1シーズンのみのデータです")
        return
    
    st.markdown(f"### {selected_player}のシーズン比較")
    
    # シーズン選択
    col1, col2 = st.columns(2)
    
    with col1:
        season1 = st.selectbox("シーズン 1", player_seasons, key='ps1')
    
    with col2:
        remaining = [s for s in player_seasons if s != season1]
        season2 = st.selectbox("シーズン 2", remaining, key='ps2') if remaining else None
    
    if not season2:
        st.warning("⚠️ 2つ目のシーズンを選択してください")
        return
    
    # 各シーズンの統計を取得
    stats1 = calculate_stats(db.get_season_data(season1), selected_player)
    stats2 = calculate_stats(db.get_season_data(season2), selected_player)
    
    stats1['Contribution'] = calculate_contribution_score(stats1)
    stats2['Contribution'] = calculate_contribution_score(stats2)
    
    # 比較テーブル
    comparison_data = {
        'STAT / 項目': [
            'PPG / 平均得点', 'RPG / 平均リバウンド', 'APG / 平均アシスト', 
            'SPG / 平均スティール', 'BPG / 平均ブロック', 
            'FG% / FG成功率', '3P% / 3P成功率', 'FT% / FT成功率', 
            'GP / 試合数', '**貢献度スコア**'
        ],
        season1: [
            f"{stats1['PTS']:.1f}",
            f"{stats1['REB']:.1f}",
            f"{stats1['AST']:.1f}",
            f"{stats1['STL']:.1f}",
            f"{stats1['BLK']:.1f}",
            f"{stats1['FG%']:.1f}%",
            f"{stats1['3P%']:.1f}%",
            f"{stats1['FT%']:.1f}%",
            str(stats1['GP']),
            f"**{stats1['Contribution']:.2f}**"
        ],
        season2: [
            f"{stats2['PTS']:.1f}",
            f"{stats2['REB']:.1f}",
            f"{stats2['AST']:.1f}",
            f"{stats2['STL']:.1f}",
            f"{stats2['BLK']:.1f}",
            f"{stats2['FG%']:.1f}%",
            f"{stats2['3P%']:.1f}%",
            f"{stats2['FT%']:.1f}%",
            str(stats2['GP']),
            f"**{stats2['Contribution']:.2f}**"
        ]
    }
    
    comparison_table(comparison_data, highlight_max=True)
    
    # 成長分析
    st.markdown("### 📈 成長分析")
    
    improvements = {
        'PPG': stats2['PTS'] - stats1['PTS'],
        'RPG': stats2['REB'] - stats1['REB'],
        'APG': stats2['AST'] - stats1['AST'],
        'FG%': stats2['FG%'] - stats1['FG%'],
        '貢献度': stats2['Contribution'] - stats1['Contribution']
    }
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    cols = [col1, col2, col3, col4, col5]
    for col, (stat_name, change) in zip(cols, improvements.items()):
        with col:
            if change > 0:
                st.metric(stat_name, f"+{change:.1f}", delta=f"+{change:.1f}")
            else:
                st.metric(stat_name, f"{change:.1f}", delta=f"{change:.1f}")


def render_season_comparison(db: StatsDatabase):
    """シーズン間比較を表示"""
    section_header("SEASON COMPARISON", "シーズン間比較")
    
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


def render_contribution_ranking(db: StatsDatabase):
    """貢献度ランキングを表示"""
    section_header("CONTRIBUTION RANKING", "貢献度ランキング")
    
    # シーズン選択
    seasons = db.get_all_seasons()
    if not seasons:
        st.warning("⚠️ データがありません")
        return
    
    selected_season = st.selectbox(
        "シーズン選択 / Select Season",
        seasons,
        key='contrib_season'
    )
    
    season_data = db.get_season_data(selected_season)
    players = db.get_all_players(season=selected_season)
    
    # 各選手の貢献度を計算
    contrib_list = []
    
    for player in players:
        stats = calculate_stats(season_data, player)
        contribution = calculate_contribution_score(stats)
        
        contrib_list.append({
            'Player': player,
            'PPG': stats['PTS'],
            'RPG': stats['REB'],
            'APG': stats['AST'],
            'SPG': stats['STL'],
            'BPG': stats['BLK'],
            'TO': stats.get('TO', 0),
            'Contribution': contribution,
            'GP': stats['GP']
        })
    
    contrib_df = pd.DataFrame(contrib_list).sort_values('Contribution', ascending=False)
    
    # ランキング表示
    st.markdown("### 📊 シーズン貢献度ランキング")
    
    display_df = contrib_df.copy()
    display_df.insert(0, '順位', range(1, len(display_df) + 1))
    display_df.columns = ['順位', '選手名', 'PPG', 'RPG', 'APG', 'SPG', 'BPG', 'TO', '貢献度スコア', '試合数']
    display_df = display_df.round(2)
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    
    # 上位10名のグラフ
    fig = create_bar_chart(
        contrib_df.head(10),
        "トップ10 貢献度ランキング / Top 10 Contribution Ranking",
        'Player',
        'Contribution',
        title_jp='Most Impactful Players'
    )
    st.plotly_chart(fig, use_container_width=True)


def render_comparison_charts(db, players, stats_list, season):
    """比較チャートをレンダリング"""
    chart_type = st.radio(
        "グラフタイプ",
        ["レーダーチャート（総合）", "棒グラフ（項目別）", "時系列推移"],
        horizontal=True
    )
    
    if chart_type == "レーダーチャート（総合）":
        categories = ['得点', 'リバウンド', 'アシスト', 'スティール', 'ブロック']
        
        values_list = []
        for stats in stats_list:
            max_vals = {'PTS': 30, 'REB': 15, 'AST': 10, 'STL': 3, 'BLK': 3}
            values = [
            # 安全な数値変換
            pts = float(stats.get('PTS', 0)) if stats.get('PTS') is not None else 0
            reb = float(stats.get('REB', 0)) if stats.get('REB') is not None else 0
            ast = float(stats.get('AST', 0)) if stats.get('AST') is not None else 0
            stl = float(stats.get('STL', 0)) if stats.get('STL') is not None else 0
            blk = float(stats.get('BLK', 0)) if stats.get('BLK') is not None else 0
            
            values = [
                min(pts / max_vals['PTS'] * 100, 100),
                min(reb / max_vals['REB'] * 100, 100),
                min(ast / max_vals['AST'] * 100, 100),
                min(stl / max_vals['STL'] * 100, 100),
                min(blk / max_vals['BLK'] * 100, 100)
        
        fig = create_radar_chart(categories, values_list, players, "総合スタッツ比較", "Overall Stats")
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "棒グラフ（項目別）":
        stat_options = ['PTS', 'TOT', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'Contribution']
        stat_to_compare = st.selectbox(
            "比較する統計項目",
            stat_options,
            format_func=lambda x: {
                'PTS': '得点 PPG',
                'TOT': 'リバウンド RPG',
                'AST': 'アシスト APG',
                'STL': 'スティール SPG',
                'BLK': 'ブロック BPG',
                'FG%': 'FG成功率',
                '3P%': '3P成功率',
                'Contribution': '貢献度スコア'
            }.get(x, x)
        )
        
        bar_data = pd.DataFrame({
            'Player': players,
            'Value': [stats.get(stat_to_compare if stat_to_compare != 'TOT' else 'REB', 0) for stats in stats_list]
        })
        
        fig = create_bar_chart(bar_data, f"{stat_to_compare} 比較", 'Player', 'Value')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("時系列推移は実装予定です")
