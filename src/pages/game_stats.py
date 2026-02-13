"""試合統計ページ - リニューアル版（試合区別機能付き）"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from stats import calculate_team_stats
from components import stat_card, section_header, game_card
from charts import create_bar_chart, create_pie_chart
from config import NBA_COLORS


def render(db: StatsDatabase):
    """試合統計ページを表示（リニューアル版）
    
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
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_season = st.selectbox(
            "シーズン選択 / SELECT SEASON",
            ["全シーズン / ALL"] + seasons,
            key='game_season_select'
        )
    
    # 試合リストを取得（日付・相手・試合形式で区別）
    if selected_season == "全シーズン / ALL":
        season_data = db.df
    else:
        season_data = db.get_season_data(selected_season)
    
    if season_data.empty:
        st.warning("⚠️ データがありません")
        return
    
    # 試合を一意に識別（日付 + 相手 + 試合形式 + 連番）
    game_groups = season_data.groupby(['GameDate', 'Opponent', 'GameFormat']).size().reset_index(name='count')
    game_list = []
    
    for _, row in game_groups.iterrows():
        date = row['GameDate']
        opponent = row['Opponent']
        game_format = row['GameFormat']
        count = row['count']
        
        # 同日・同相手の試合が複数ある場合は番号を付ける
        if len(game_groups[(game_groups['GameDate'] == date) & (game_groups['Opponent'] == opponent)]) > 1:
            game_label = f"{date} vs {opponent} ({game_format})"
        else:
            game_label = f"{date} vs {opponent}"
        
        game_list.append({
            'label': game_label,
            'date': date,
            'opponent': opponent,
            'format': game_format
        })
    
    with col2:
        if not game_list:
            st.warning("⚠️ 試合データがありません")
            return
        
        selected_game_label = st.selectbox(
            "試合選択 / SELECT GAME",
            [g['label'] for g in game_list],
            key='game_select'
        )
    
    # 選択された試合の情報を取得
    selected_game_info = next(g for g in game_list if g['label'] == selected_game_label)
    
    # 試合データを取得（日付・相手・試合形式で絞り込み）
    game_data = season_data[
        (season_data['GameDate'] == selected_game_info['date']) &
        (season_data['Opponent'] == selected_game_info['opponent']) &
        (season_data['GameFormat'] == selected_game_info['format'])
    ]
    
    if game_data.empty:
        st.warning("⚠️ 試合データの取得に失敗しました")
        return
    
    # 試合情報カード
    opponent = game_data['Opponent'].iloc[0]
    team_score = game_data['TeamScore'].iloc[0] if 'TeamScore' in game_data.columns else 0
    opp_score = game_data['OpponentScore'].iloc[0] if 'OpponentScore' in game_data.columns else 0
    game_format = game_data['GameFormat'].iloc[0] if 'GameFormat' in game_data.columns else '4Q'
    
    game_card(selected_game_info['date'], opponent, team_score, opp_score)
    
    # 試合形式表示
    st.markdown(f"**試合形式 / Game Format:** `{game_format}`")
    
    st.markdown("---")
    
    # チーム統計
    section_header("チーム統計 / Team Statistics")
    
    team_stats = calculate_team_stats(game_data)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        stat_card("Total Points", team_stats['total_pts'], "総得点", "primary")
    
    with col2:
        stat_card("Total Rebounds", team_stats['total_reb'], "総リバウンド")
    
    with col3:
        stat_card("Total Assists", team_stats['total_ast'], "総アシスト")
    
    with col4:
        stat_card("FG%", f"{team_stats['fg_pct']:.1f}%", "FG成功率")
    
    with col5:
        result = "勝利 / WIN" if team_score > opp_score else "敗北 / LOSS"
        result_type = "primary" if team_score > opp_score else "secondary"
        stat_card("Result", result, "試合結果", result_type)
    
    # 追加チーム統計
    col6, col7, col8, col9 = st.columns(4)
    
    with col6:
        stat_card("Total Steals", team_stats.get('total_stl', 0), "総スティール", "secondary")
    
    with col7:
        stat_card("Total Blocks", team_stats.get('total_blk', 0), "総ブロック", "secondary")
    
    with col8:
        stat_card("3P%", f"{team_stats.get('3p_pct', 0):.1f}%", "3P成功率", "primary")
    
    with col9:
        stat_card("FT%", f"{team_stats.get('ft_pct', 0):.1f}%", "FT成功率")
    
    st.markdown("---")
    
    # ビジュアル分析
    section_header("ビジュアル分析 / Visual Analysis")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # 得点分布（選手別）
        top_scorers = game_data.nlargest(5, 'PTS')[['PlayerName', 'PTS']]
        fig_scorers = create_bar_chart(
            top_scorers,
            "トップスコアラー / Top Scorers",
            'PlayerName',
            'PTS',
            title_jp='Top 5 Point Contributors'
        )
        st.plotly_chart(fig_scorers, use_container_width=True)
    
    with chart_col2:
        # 得点分布円グラフ
        fig_pie = create_pie_chart(
            game_data['PlayerName'].tolist(),
            game_data['PTS'].tolist(),
            "得点分布 / Points Distribution",
            title_jp='Team Scoring Breakdown'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # プレイヤーボックススコア
    section_header("プレイヤーボックススコア / Player Box Score")
    
    # 表示カラムの選択
    display_cols_base = ['No', 'PlayerName', 'PTS', '3PM', '3PA', '2PM', '2PA', 
                         'FTM', 'FTA', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'PF', 'MIN']
    
    # 利用可能なカラムのみを表示
    display_cols = [col for col in display_cols_base if col in game_data.columns]
    
    # ソートオプション
    sort_by = st.selectbox(
        "並び替え / Sort by",
        ['PTS', 'TOT', 'AST', 'STL', 'BLK', 'PlayerName'],
        format_func=lambda x: {
            'PTS': '得点 / Points',
            'TOT': 'リバウンド / Rebounds',
            'AST': 'アシスト / Assists',
            'STL': 'スティール / Steals',
            'BLK': 'ブロック / Blocks',
            'PlayerName': '選手名 / Name'
        }.get(x, x),
        key='game_sort'
    )
    
    ascending = st.checkbox("昇順 / Ascending", value=False)
    
    sorted_game_data = game_data[display_cols].sort_values(sort_by, ascending=ascending)
    
    st.dataframe(
        sorted_game_data,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    # データダウンロード
    csv = game_data.to_csv(index=False)
    st.download_button(
        label="📥 試合データをダウンロード / Download Game Data",
        data=csv,
        file_name=f"game_{selected_game_info['date']}_{opponent}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # 詳細分析
    with st.expander("📊 詳細分析 / Detailed Analysis"):
        render_detailed_analysis(game_data)


def render_detailed_analysis(game_data):
    """詳細分析セクションをレンダリング"""
    st.markdown("### 🎯 個人パフォーマンス分析")
    
    # 効率性指標
    st.markdown("#### 効率性指標")
    
    efficiency_data = game_data.copy()
    
    # シューティング効率
    efficiency_data['TS%'] = efficiency_data.apply(
        lambda row: (row['PTS'] / (2 * (row['2PA'] + row['3PA'] + 0.44 * row['FTA'])) * 100)
        if (row['2PA'] + row['3PA'] + 0.44 * row['FTA']) > 0 else 0,
        axis=1
    )
    
    # 使用率（Usage Rate）の簡易計算
    total_fga = efficiency_data['2PA'].sum() + efficiency_data['3PA'].sum()
    total_fta = efficiency_data['FTA'].sum()
    
    efficiency_data['USG%'] = efficiency_data.apply(
        lambda row: ((row['2PA'] + row['3PA'] + 0.44 * row['FTA']) / 
                     (total_fga + 0.44 * total_fta) * 100)
        if (total_fga + 0.44 * total_fta) > 0 else 0,
        axis=1
    )
    
    display_eff = efficiency_data[['PlayerName', 'PTS', 'TS%', 'USG%']].copy()
    display_eff.columns = ['選手名', '得点', 'True Shooting %', '使用率 %']
    display_eff = display_eff.round(1).sort_values('得点', ascending=False)
    
    st.dataframe(display_eff, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # プラス・マイナス貢献度
    st.markdown("#### 📈 貢献度スコア")
    st.markdown("""
    **計算式:** 貢献度 = (得点 × 1.0) + (リバウンド × 1.2) + (アシスト × 1.5) + (スティール × 3.0) + (ブロック × 3.0) - (TO × 2.0)
    
    この式は、各スタッツの試合への影響度を考慮した重み付けを行っています。
    """)
    
    contribution_data = game_data.copy()
    contribution_data['Contribution'] = (
        contribution_data['PTS'] * 1.0 +
        contribution_data['TOT'] * 1.2 +
        contribution_data['AST'] * 1.5 +
        contribution_data.get('STL', 0) * 3.0 +
        contribution_data.get('BLK', 0) * 3.0 -
        contribution_data.get('TO', 0) * 2.0
    )
    
    contribution_display = contribution_data[['PlayerName', 'PTS', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'Contribution']].copy()
    contribution_display.columns = ['選手名', '得点', 'REB', 'AST', 'STL', 'BLK', 'TO', '貢献度スコア']
    contribution_display = contribution_display.sort_values('貢献度スコア', ascending=False)
    contribution_display['貢献度スコア'] = contribution_display['貢献度スコア'].round(1)
    
    st.dataframe(contribution_display, use_container_width=True, hide_index=True)
    
    # 貢献度グラフ
    fig_contrib = create_bar_chart(
        contribution_display.head(10),
        "選手別貢献度スコア / Player Contribution Score",
        '選手名',
        '貢献度スコア',
        title_jp='Top 10 Contributors'
    )
    st.plotly_chart(fig_contrib, use_container_width=True)
