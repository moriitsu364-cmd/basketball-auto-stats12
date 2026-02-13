"""シーズン統計ページ - 完全刷新版"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from stats import calculate_season_overview, get_leaders
from charts import create_nba_chart, create_bar_chart, create_pie_chart
from components import stat_card, section_header, ranking_row
from config import NBA_COLORS, PLAYER_IMAGES_DIR


def render(db: StatsDatabase):
    """シーズン統計ページを表示（完全刷新版）
    
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
    
    # 詳細ボタン（目立つように配置）
    col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
    with col_btn_center:
        if st.button("📊 シーズン詳細データを見る / View Season Details", use_container_width=True, type="primary"):
            st.session_state['show_season_details'] = not st.session_state.get('show_season_details', False)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 詳細データ表示（展開式）
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
        
        # メイングラフ（2つ）
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
        
        # パフォーマンス詳細ボタン（目立つように配置）
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
    
    # 全ランキング詳細ボタン（目立つように配置）
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
    """リーダーセクションをレンダリング（名前表示修正版）"""
    leaders = get_leaders(season_data, stat_col)
    
    if leaders.empty:
        st.info(f"{stat_name}のデータがありません / No {stat_name} data available")
        return
    
    for idx, (player, row) in enumerate(leaders.iterrows(), 1):
        if idx > 5:  # TOP5まで
            break
        
        # 選手名を確実に表示
        player_name = str(player) if player else "Unknown Player"
        
        player_image = None
        image_path = PLAYER_IMAGES_DIR / f"{player_name}.png"
        if image_path.exists():
            player_image = str(image_path)
        
        # 選手番号を取得
        player_data = season_data[season_data['PlayerName'] == player_name]
        player_number = ""
        if not player_data.empty:
            if 'PlayerNumber' in player_data.columns:
                player_number = str(player_data['PlayerNumber'].iloc[0])
            elif 'No' in player_data.columns:
                player_number = str(player_data['No'].iloc[0])
        
        # スタッツ値を取得
        stat_value = row.get(avg_label, 0)
        if pd.isna(stat_value):
            stat_value = 0
        
        ranking_row(
            rank=idx,
            player=player_name,
            player_number=player_number,
            stat_value=stat_value,
            stat_label=avg_label,
            color=NBA_COLORS[color],
            image_path=player_image
        )


def render_detailed_season_stats(season_data, overview):
    """シーズン詳細統計を表示（改善版）"""
    st.markdown("### 📊 シーズン詳細統計 / Detailed Season Statistics")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # チーム全体の統計
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("選手数 / Total Players", overview['players'])
        st.metric("総得点 / Total Points", f"{season_data['PTS'].sum():.0f}")
    
    with col2:
        avg_pts = season_data.groupby('GameDate')['PTS'].sum().mean()
        st.metric("平均得点 / Avg PTS", f"{avg_pts:.1f}" if not pd.isna(avg_pts) else "N/A")
        avg_reb = season_data.groupby('GameDate')['TOT'].sum().mean()
        st.metric("平均リバウンド / Avg REB", f"{avg_reb:.1f}" if not pd.isna(avg_reb) else "N/A")
    
    with col3:
        avg_ast = season_data.groupby('GameDate')['AST'].sum().mean()
        st.metric("平均アシスト / Avg AST", f"{avg_ast:.1f}" if not pd.isna(avg_ast) else "N/A")
        avg_stl = season_data.groupby('GameDate')['STL'].sum().mean()
        st.metric("平均スティール / Avg STL", f"{avg_stl:.1f}" if not pd.isna(avg_stl) else "N/A")
    
    with col4:
        avg_blk = season_data.groupby('GameDate')['BLK'].sum().mean()
        st.metric("平均ブロック / Avg BLK", f"{avg_blk:.1f}" if not pd.isna(avg_blk) else "N/A")
        avg_to = season_data.groupby('GameDate')['TO'].sum().mean()
        st.metric("平均ターンオーバー / Avg TO", f"{avg_to:.1f}" if not pd.isna(avg_to) else "N/A")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### シュート効率 / Shooting Efficiency")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_2pm = season_data['2PM'].sum()
        total_2pa = season_data['2PA'].sum()
        fg2_pct = (total_2pm / total_2pa * 100) if total_2pa > 0 else 0
        st.metric("2ポイント成功率 / 2P%", f"{fg2_pct:.1f}%")
        st.caption(f"成功: {total_2pm:.0f} / 試投: {total_2pa:.0f}")
    
    with col2:
        total_3pm = season_data['3PM'].sum()
        total_3pa = season_data['3PA'].sum()
        fg3_pct = (total_3pm / total_3pa * 100) if total_3pa > 0 else 0
        st.metric("3ポイント成功率 / 3P%", f"{fg3_pct:.1f}%")
        st.caption(f"成功: {total_3pm:.0f} / 試投: {total_3pa:.0f}")
    
    with col3:
        total_ftm = season_data['FTM'].sum()
        total_fta = season_data['FTA'].sum()
        ft_pct = (total_ftm / total_fta * 100) if total_fta > 0 else 0
        st.metric("フリースロー成功率 / FT%", f"{ft_pct:.1f}%")
        st.caption(f"成功: {total_ftm:.0f} / 試投: {total_fta:.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 総合シュート効率 / Overall Shooting")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_fgm = total_2pm + total_3pm
        total_fga = total_2pa + total_3pa
        fg_pct = (total_fgm / total_fga * 100) if total_fga > 0 else 0
        st.metric("総合FG% / Overall FG%", f"{fg_pct:.1f}%")
    
    with col2:
        # eFG% = (FGM + 0.5 * 3PM) / FGA
        efg_pct = ((total_fgm + 0.5 * total_3pm) / total_fga * 100) if total_fga > 0 else 0
        st.metric("実効FG% / eFG%", f"{efg_pct:.1f}%")
    
    with col3:
        # True Shooting % = PTS / (2 * (FGA + 0.44 * FTA))
        total_pts = season_data['PTS'].sum()
        ts_denominator = 2 * (total_fga + 0.44 * total_fta)
        ts_pct = (total_pts / ts_denominator * 100) if ts_denominator > 0 else 0
        st.metric("真のシュート率 / TS%", f"{ts_pct:.1f}%")


def render_detailed_performance_charts(game_stats):
    """詳細パフォーマンスグラフを表示（拡張版）"""
    st.markdown("### 📉 詳細パフォーマンスチャート / Detailed Performance Charts")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # リバウンド & スティール
    st.markdown("#### ディフェンス関連統計 / Defensive Stats")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_reb = create_nba_chart(
            game_stats, 
            'リバウンド推移 / Rebounds Trend', 
            'GameNumber', 
            'TOT',
            color=NBA_COLORS['secondary']
        )
        st.plotly_chart(fig_reb, use_container_width=True)
    
    with chart_col2:
        fig_stl = create_nba_chart(
            game_stats, 
            'スティール推移 / Steals Trend', 
            'GameNumber', 
            'STL',
            color='#FDB927'
        )
        st.plotly_chart(fig_stl, use_container_width=True)
    
    # ブロック & 複合ディフェンス
    chart_col3, chart_col4 = st.columns(2)
    
    with chart_col3:
        fig_blk = create_nba_chart(
            game_stats, 
            'ブロック推移 / Blocks Trend', 
            'GameNumber', 
            'BLK',
            color='#552583'
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
        # トータルパフォーマンス指標（仮想スコア）
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
    """全選手の詳細ランキングを表示（改善版）"""
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
    
    # 平均スタッツを計算
    player_stats['PPG'] = (player_stats['PTS'] / player_stats['GP']).round(1)
    player_stats['RPG'] = (player_stats['TOT'] / player_stats['GP']).round(1)
    player_stats['APG'] = (player_stats['AST'] / player_stats['GP']).round(1)
    player_stats['SPG'] = (player_stats['STL'] / player_stats['GP']).round(1)
    player_stats['BPG'] = (player_stats['BLK'] / player_stats['GP']).round(1)
    
    # シュート率を計算
    player_stats['FG%'] = ((player_stats['2PM'] + player_stats['3PM']) / 
                           (player_stats['2PA'] + player_stats['3PA']) * 100).round(1)
    player_stats['3P%'] = (player_stats['3PM'] / player_stats['3PA'] * 100).round(1)
    player_stats['FT%'] = (player_stats['FTM'] / player_stats['FTA'] * 100).round(1)
    
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
    """ランキングテーブルを表示（改善版）"""
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
    
    # 最低試投数のフィルタ（5試投以上）
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
