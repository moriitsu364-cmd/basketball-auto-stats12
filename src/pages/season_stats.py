"""シーズン統計ページ - 完全刷新版"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from ..database import StatsDatabase
from ..stats import calculate_season_overview, get_leaders
from ..charts import create_nba_chart, create_bar_chart, create_pie_chart
from ..components import stat_card, section_header, ranking_row
from ..config import NBA_COLORS, PLAYER_IMAGES_DIR


def render(db: StatsDatabase):
    """シーズン統計ページを表示(完全刷新版)
    
    Args:
        db: データベースインスタンス
    """
    # データチェック
    if db.df.empty:
        st.info("現在データがありません / No data available")
        st.markdown("""
        <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; text-align: center; margin-top: 2rem;">
            <h3 style="color: white; margin-bottom: 1rem;">データを追加してください</h3>
            <p style="color: rgba(255,255,255,0.9);">データ入力タブからシーズンデータを登録できます</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    seasons = db.get_all_seasons()
    
    if not seasons:
        st.info("現在データがありません / No data available")
        st.markdown("""
        <div style="padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 10px; text-align: center; margin-top: 2rem;">
            <h3 style="color: white; margin-bottom: 1rem;">データを追加してください</h3>
            <p style="color: rgba(255,255,255,0.9);">データ入力タブからシーズンデータを登録できます</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
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
    
    if season_data.empty:
        st.warning(f"{selected_season}シーズンのデータがありません")
        st.markdown("""
        <div style="padding: 2rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 10px; text-align: center; margin-top: 2rem;">
            <h3 style="color: white; margin-bottom: 1rem;">このシーズンにはまだデータがありません</h3>
            <p style="color: rgba(255,255,255,0.9);">データ入力タブから試合データを追加してください</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # ===== セクション1: シーズンサマリー =====
    section_header("🏆 シーズンサマリー / Season Summary")
    
    overview = calculate_season_overview(season_data)
    win_rate = (overview['wins'] / overview['games'] * 100) if overview['games'] > 0 else 0
    
    # メインサマリーカード
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stat_card("試合数", overview['games'], card_type="primary", label_jp="Games")
    with col2:
        stat_card("勝利数", overview['wins'], card_type="primary", label_jp="Wins")
    with col3:
        stat_card("敗北数", overview['losses'], card_type="secondary", label_jp="Losses")
    with col4:
        stat_card("勝率", f"{win_rate:.1f}%", card_type="primary", label_jp="Win Rate")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 詳細ボタン(目立つように配置)
    col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
    with col_btn_center:
        if st.button("📊 シーズン詳細データを見る / View Season Details", use_container_width=True, type="primary"):
            st.session_state['show_season_details'] = not st.session_state.get('show_season_details', False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 詳細データ表示(展開式)
    if st.session_state.get('show_season_details', False):
        st.markdown("---")
        render_detailed_season_stats(season_data, overview)
        st.markdown("---")
    
    # ===== セクション2: チームパフォーマンス =====
    section_header("📈 チームパフォーマンス / Team Performance")
    
    # ゲームごとの統計を集計
    game_stats = season_data.groupby('GameDate').agg({
        'PTS': 'sum',
        'TOT': 'sum',
        'AST': 'sum',
        'STL': 'sum',
        'BLK': 'sum',
        'GameDate': 'first'
    }).reset_index(drop=True)
    
    if game_stats.empty:
        st.info("パフォーマンスデータがありません / No performance data available")
    else:
        game_stats = game_stats.sort_values('GameDate')
        game_stats['GameNumber'] = range(1, len(game_stats) + 1)
        
        # メイングラフ(2つ)
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            fig_pts = create_nba_chart(
                game_stats, 
                '試合ごとの得点 / Points Per Game', 
                'GameNumber', 
                'PTS'
            )
            st.plotly_chart(fig_pts, use_container_width=True)
        
        with chart_col2:
            fig_ast = create_nba_chart(
                game_stats, 
                '試合ごとのアシスト / Assists Per Game', 
                'GameNumber', 
                'AST', 
                color=NBA_COLORS['secondary']
            )
            st.plotly_chart(fig_ast, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # パフォーマンス詳細ボタン(目立つように配置)
        col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
        with col_btn_center:
            if st.button("📉 詳細グラフページへ / View All Performance Charts", use_container_width=True, type="primary"):
                st.session_state['show_performance_details'] = not st.session_state.get('show_performance_details', False)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 詳細グラフ表示
        if st.session_state.get('show_performance_details', False):
            st.markdown("---")
            render_detailed_performance_charts(game_stats)
            st.markdown("---")
    
    # ===== セクション3: チームリーダーランキング =====
    section_header("👑 チームリーダー / Team Leaders (TOP 5)")
    
    leader_tab1, leader_tab2, leader_tab3, leader_tab4, leader_tab5 = st.tabs([
        "🏀 得点 / POINTS", 
        "📦 リバウンド / REBOUNDS", 
        "🎯 アシスト / ASSISTS",
        "🖐️ スティール / STEALS",
        "🚫 ブロック / BLOCKS"
    ])
    
    with leader_tab1:
        render_leader_section(season_data, 'PTS', 'PPG', 'Points Per Game', 'primary')
    
    with leader_tab2:
        render_leader_section(season_data, 'TOT', 'RPG', 'Rebounds Per Game', 'secondary')
    
    with leader_tab3:
        render_leader_section(season_data, 'AST', 'APG', 'Assists Per Game', 'primary')
    
    with leader_tab4:
        render_leader_section(season_data, 'STL', 'SPG', 'Steals Per Game', 'secondary')
    
    with leader_tab5:
        render_leader_section(season_data, 'BLK', 'BPG', 'Blocks Per Game', 'primary')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 全ランキング詳細ボタン(目立つように配置)
    col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
    with col_btn_center:
        if st.button("🏅 全選手ランキング詳細 / Full Player Rankings", use_container_width=True, type="primary"):
            st.session_state['show_full_rankings'] = not st.session_state.get('show_full_rankings', False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 全ランキング表示
    if st.session_state.get('show_full_rankings', False):
        st.markdown("---")
        render_full_rankings(season_data)
        st.markdown("---")


def render_leader_section(season_data, stat_col, avg_label, stat_name, color):
    """リーダーセクションをレンダリング(名前表示修正版)"""
    leaders = get_leaders(season_data, stat_col, n=5)
    
    if leaders.empty:
        st.info(f"{stat_name}のデータがありません / No {stat_name} data available")
        return
    
    # 選手名を確実に取得し、インデックスとして設定
    leaders = leaders.reset_index()
    leaders['PlayerName'] = leaders['PlayerName'].fillna('Unknown Player')
    leaders['PlayerName'] = leaders['PlayerName'].astype(str)
    
    # カラム名をわかりやすく変更
    column_names = list(leaders.columns)
    if len(column_names) >= 4:
        leaders.columns = ['選手名 / Player', 'Total', avg_label, 'GP']
    
    # TOP 5選手を表示
    for idx, row in leaders.head(5).iterrows():
        player_name = row['選手名 / Player']
        avg_val = row[avg_label]
        gp = row['GP']
        
        # ランキング行を表示
        ranking_row(
            rank=idx + 1,
            player_name=player_name,
            stat_value=f"{avg_val:.1f}",
            games=int(gp),
            card_type=color
        )


def render_detailed_season_stats(season_data, overview):
    """詳細シーズン統計を表示"""
    st.markdown("### 📋 シーズン詳細統計 / Detailed Season Statistics")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### チーム統計 / Team Stats")
        stat_card("総得点", int(season_data['PTS'].sum()), card_type="primary", label_jp="Total Points")
        stat_card("平均得点", f"{overview['avg_pts']:.1f}", card_type="secondary", label_jp="Avg Points")
        stat_card("総リバウンド", int(season_data['TOT'].sum()), card_type="primary", label_jp="Total Rebounds")
    
    with col2:
        st.markdown("#### 登録選手 / Players")
        stat_card("登録選手数", overview['players'], card_type="primary", label_jp="Total Players")
        active_players = len(season_data.groupby('PlayerName'))
        stat_card("出場選手数", active_players, card_type="secondary", label_jp="Active Players")
        
    with col3:
        st.markdown("#### その他 / Others")
        stat_card("総アシスト", int(season_data['AST'].sum()), card_type="primary", label_jp="Total Assists")
        stat_card("総スティール", int(season_data['STL'].sum()), card_type="secondary", label_jp="Total Steals")
        stat_card("総ブロック", int(season_data['BLK'].sum()), card_type="primary", label_jp="Total Blocks")


def render_detailed_performance_charts(game_stats):
    """詳細パフォーマンスグラフを表示"""
    st.markdown("### 📊 詳細パフォーマンスグラフ / Detailed Performance Charts")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ディフェンス統計
    st.markdown("#### ディフェンス統計 / Defensive Stats")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_reb = create_nba_chart(
            game_stats, 
            '試合ごとのリバウンド / Rebounds Per Game', 
            'GameNumber', 
            'TOT',
            color='#00471B'
        )
        st.plotly_chart(fig_reb, use_container_width=True)
    
    with chart_col2:
        fig_stl = create_nba_chart(
            game_stats, 
            '試合ごとのスティール / Steals Per Game', 
            'GameNumber', 
            'STL',
            color='#006BB6'
        )
        st.plotly_chart(fig_stl, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 追加統計
    st.markdown("#### 追加統計 / Additional Stats")
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        fig_blk = create_nba_chart(
            game_stats, 
            '試合ごとのブロック / Blocks Per Game', 
            'GameNumber', 
            'BLK',
            color='#860038'
        )
        st.plotly_chart(fig_blk, use_container_width=True)
    
    with chart_col4:
        # 複合スタッツ
        combined_df = game_stats.copy()
        combined_df['Total_Defensive'] = combined_df['STL'] + combined_df['BLK']
        fig_def = create_nba_chart(
            combined_df, 
            'ディフェンス貢献 (STL+BLK) / Defensive Impact', 
            'GameNumber', 
            'Total_Defensive',
            color='#CE1141'
        )
        st.plotly_chart(fig_def, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # オフェンス統計の組み合わせチャート
    st.markdown("#### オフェンス関連統計 / Offensive Stats")
    chart_col5, chart_col6 = st.columns(2)
    
    with chart_col5:
        # 得点とアシストの相関
        combined_df2 = game_stats.copy()
        combined_df2['PTS_AST_Ratio'] = combined_df2['PTS'] / (combined_df2['AST'] + 1)  # +1でゼロ除算回避
        fig_ratio = create_nba_chart(
            combined_df2,
            '得点/アシスト比 / Points per Assist Ratio',
            'GameNumber',
            'PTS_AST_Ratio',
            color='#007A33'
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    with chart_col6:
        # トータルパフォーマンス指標(仮想スコア)
        combined_df3 = game_stats.copy()
        combined_df3['Performance_Score'] = (
            combined_df3['PTS'] + 
            combined_df3['AST'] * 2 + 
            combined_df3['TOT'] * 1.5 + 
            combined_df3['STL'] * 2 + 
            combined_df3['BLK'] * 2
        )
        fig_perf = create_nba_chart(
            combined_df3,
            'トータルパフォーマンススコア / Total Performance Score',
            'GameNumber',
            'Performance_Score',
            color='#F58426'
        )
        st.plotly_chart(fig_perf, use_container_width=True)


def render_full_rankings(season_data):
    """全選手の詳細ランキングを表示(改善版)"""
    st.markdown("### 🏅 全選手統計ランキング / Full Player Rankings")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 選手ごとの平均スタッツを計算
    player_stats = season_data.groupby('PlayerName').agg({
        'PTS': 'sum',
        'TOT': 'sum',
        'AST': 'sum',
        'STL': 'sum',
        'BLK': 'sum',
        'GameDate': 'count',  # 試合数
        '2PM': 'sum',
        '2PA': 'sum',
        '3PM': 'sum',
        '3PA': 'sum',
        'FTM': 'sum',
        'FTA': 'sum'
    }).rename(columns={'GameDate': 'GP'})
    
    if player_stats.empty:
        st.info("ランキングデータがありません / No ranking data available")
        return
    
    # すべてのカラムを数値型に変換
    numeric_columns = ['PTS', 'TOT', 'AST', 'STL', 'BLK', 'GP', '2PM', '2PA', '3PM', '3PA', 'FTM', 'FTA']
    for col in numeric_columns:
        player_stats[col] = pd.to_numeric(player_stats[col], errors='coerce').fillna(0)
    
    # 平均スタッツを計算
    player_stats['PPG'] = (player_stats['PTS'] / player_stats['GP'].replace(0, 1)).round(1)
    player_stats['RPG'] = (player_stats['TOT'] / player_stats['GP'].replace(0, 1)).round(1)
    player_stats['APG'] = (player_stats['AST'] / player_stats['GP'].replace(0, 1)).round(1)
    player_stats['SPG'] = (player_stats['STL'] / player_stats['GP'].replace(0, 1)).round(1)
    player_stats['BPG'] = (player_stats['BLK'] / player_stats['GP'].replace(0, 1)).round(1)
    
    # シュート率を計算
    player_stats['FG%'] = ((player_stats['2PM'] + player_stats['3PM']) / 
                           (player_stats['2PA'] + player_stats['3PA']).replace(0, 1) * 100).round(1)
    player_stats['3P%'] = (player_stats['3PM'] / player_stats['3PA'].replace(0, 1) * 100).round(1)
    player_stats['FT%'] = (player_stats['FTM'] / player_stats['FTA'].replace(0, 1) * 100).round(1)
    
    # NaN を 0 に置換
    player_stats = player_stats.fillna(0)
    
    # タブで各カテゴリのランキングを表示
    rank_tab1, rank_tab2, rank_tab3, rank_tab4, rank_tab5, rank_tab6 = st.tabs([
        "🏀 得点 PPG", 
        "📦 リバウンド RPG", 
        "🎯 アシスト APG", 
        "🖐️ スティール SPG", 
        "🚫 ブロック BPG",
        "🎲 シュート効率"
    ])
    
    with rank_tab1:
        display_ranking_table(player_stats.sort_values('PPG', ascending=False), 'PPG', '平均得点', show_games=True)
    
    with rank_tab2:
        display_ranking_table(player_stats.sort_values('RPG', ascending=False), 'RPG', '平均リバウンド', show_games=True)
    
    with rank_tab3:
        display_ranking_table(player_stats.sort_values('APG', ascending=False), 'APG', '平均アシスト', show_games=True)
    
    with rank_tab4:
        display_ranking_table(player_stats.sort_values('SPG', ascending=False), 'SPG', '平均スティール', show_games=True)
    
    with rank_tab5:
        display_ranking_table(player_stats.sort_values('BPG', ascending=False), 'BPG', '平均ブロック', show_games=True)
    
    with rank_tab6:
        display_shooting_rankings(player_stats)


def display_ranking_table(stats_df, stat_col, stat_name, show_games=True):
    """ランキングテーブルを表示(改善版)"""
    st.markdown(f"#### {stat_name}ランキング / {stat_name} Rankings")
    
    if stats_df.empty:
        st.info(f"{stat_name}のデータがありません / No {stat_name} data available")
        return
    
    if show_games:
        display_df = stats_df.reset_index()[['PlayerName', 'GP', stat_col]].copy()
        display_df.columns = ['選手名 / Player', '試合数 / GP', stat_name]
    else:
        display_df = stats_df.reset_index()[['PlayerName', stat_col]].copy()
        display_df.columns = ['選手名 / Player', stat_name]
    
    # 選手名が空でないことを確認
    display_df['選手名 / Player'] = display_df['選手名 / Player'].fillna('Unknown Player')
    display_df['選手名 / Player'] = display_df['選手名 / Player'].astype(str)
    
    display_df.insert(0, '順位 / Rank', range(1, len(display_df) + 1))
    
    # スタイリング付きでデータフレームを表示
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={
            '順位 / Rank': st.column_config.NumberColumn(
                '順位 / Rank',
                width='small'
            ),
            stat_name: st.column_config.NumberColumn(
                stat_name,
                format='%.1f'
            )
        }
    )


def display_shooting_rankings(player_stats):
    """シュート効率ランキングを表示"""
    st.markdown("#### シュート効率ランキング / Shooting Efficiency Rankings")
    
    # 最低試投数のフィルタ(5試投以上)
    min_attempts = 5
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### FG% (総合シュート率)")
        fg_qualified = player_stats[(player_stats['2PA'] + player_stats['3PA']) >= min_attempts].copy()
        fg_qualified = fg_qualified.sort_values('FG%', ascending=False)
        
        if not fg_qualified.empty:
            display_df = fg_qualified.reset_index()[['PlayerName', 'FG%']].copy()
            display_df.columns = ['選手名', 'FG%']
            display_df.insert(0, '順位', range(1, len(display_df) + 1))
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)
        else:
            st.info("データなし / No data")
    
    with col2:
        st.markdown("##### 3P% (3ポイント率)")
        fg3_qualified = player_stats[player_stats['3PA'] >= min_attempts].copy()
        fg3_qualified = fg3_qualified.sort_values('3P%', ascending=False)
        
        if not fg3_qualified.empty:
            display_df = fg3_qualified.reset_index()[['PlayerName', '3P%']].copy()
            display_df.columns = ['選手名', '3P%']
            display_df.insert(0, '順位', range(1, len(display_df) + 1))
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)
        else:
            st.info("データなし / No data")
    
    with col3:
        st.markdown("##### FT% (フリースロー率)")
        ft_qualified = player_stats[player_stats['FTA'] >= min_attempts].copy()
        ft_qualified = ft_qualified.sort_values('FT%', ascending=False)
        
        if not ft_qualified.empty:
            display_df = ft_qualified.reset_index()[['PlayerName', 'FT%']].copy()
            display_df.columns = ['選手名', 'FT%']
            display_df.insert(0, '順位', range(1, len(display_df) + 1))
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=300)
        else:
            st.info("データなし / No data")
    
    st.caption(f"※ 最低{min_attempts}試投以上の選手のみ表示 / Minimum {min_attempts} attempts required")
