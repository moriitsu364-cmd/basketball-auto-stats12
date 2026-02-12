
from PIL import Image
import io
import json
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from auth import check_password
from stats import calculate_stats
from charts import create_bar_chart
from ai import setup_gemini
from styles import load_css

# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="Tsukuba Basketball Stats",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ========================================
# データベース関連
# ========================================
DATA_FILE = "basketball_stats.csv"

def init_database():
    """データベースの初期化"""
    if 'database' not in st.session_state:
        if os.path.exists(DATA_FILE):
            try:
                st.session_state['database'] = pd.read_csv(DATA_FILE)
            except Exception as e:
                st.error(f"Data loading error: {e}")
                st.session_state['database'] = create_empty_dataframe()
        else:
            st.session_state['database'] = create_empty_dataframe()

def create_empty_dataframe():
    """空のデータフレームを作成"""
    return pd.DataFrame(columns=[
        'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
        '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
        'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
        'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
        'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
    ])

def save_database():
    """データベースを保存"""
    try:
        st.session_state['database'].to_csv(DATA_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
        return False
# ========================================
# メイン画面
# ========================================
def main():
    init_database()
    
    # ヘッダー
    st.markdown("""
    <div class="nba-header">
        <h1>TSUKUBA BASKETBALL STATS</h1>
        <p class="subtitle">筑波大学附属高校 男子バスケットボール統計システム</p>
    </div>
    """, unsafe_allow_html=True)
    
    model, model_name = setup_gemini()
    
    # メインタブ
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "SEASON STATS", 
        "PLAYER STATS", 
        "GAME STATS",
        "COMPARE",
        "DATA INPUT"
    ])
    
    # ========================================
    # タブ1: シーズン統計
    # ========================================
    with tab1:
        if st.session_state['database'].empty:
            st.info("No data available. Please add data in the DATA INPUT tab.")
        else:
            db = st.session_state['database']
            seasons = sorted(db['Season'].unique(), reverse=True)
            
            # シーズン選択
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                selected_season = st.selectbox("SELECT SEASON", seasons, key='season_select')
            with col2:
                st.write("")
            with col3:
                if st.button("EXPORT DATA"):
                    csv = db[db['Season'] == selected_season].to_csv(index=False)
                    st.download_button(
                        label="DOWNLOAD CSV",
                        data=csv,
                        file_name=f"stats_{selected_season}.csv",
                        mime="text/csv"
                    )
            
            if selected_season:
                season_data = db[db['Season'] == selected_season]
                
                st.markdown('<div class="section-header">Season Overview</div>', unsafe_allow_html=True)
                
                # サマリーメトリクス
                col1, col2, col3, col4, col5 = st.columns(5)
                
                games = len(season_data['GameDate'].unique())
                players = season_data['PlayerName'].nunique()
                avg_pts = season_data.groupby('GameDate')['PTS'].sum().mean()
                wins = len(season_data[season_data['TeamScore'] > season_data['OpponentScore']]['GameDate'].unique())
                losses = len(season_data[season_data['TeamScore'] < season_data['OpponentScore']]['GameDate'].unique())
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card primary">
                        <div class="stat-label">Games Played</div>
                        <div class="stat-value">{games}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Players</div>
                        <div class="stat-value">{players}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-card primary">
                        <div class="stat-label">Avg Points</div>
                        <div class="stat-value">{avg_pts:.1f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Wins</div>
                        <div class="stat-value">{wins}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    st.markdown(f"""
                    <div class="stat-card secondary">
                        <div class="stat-label">Losses</div>
                        <div class="stat-value">{losses}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # チームパフォーマンス
                st.markdown('<div class="section-header">Team Performance</div>', unsafe_allow_html=True)
                
                game_stats = season_data.groupby('GameDate').agg({
                    'PTS': 'sum',
                    'TOT': 'sum',
                    'AST': 'sum'
                }).reset_index()
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    fig_pts = create_nba_chart(game_stats, 'POINTS PER GAME', 'GameDate', 'PTS')
                    st.plotly_chart(fig_pts, use_container_width=True)
                
                with chart_col2:
                    fig_ast = create_nba_chart(game_stats, 'ASSISTS PER GAME', 'GameDate', 'AST', color='#c8102e')
                    st.plotly_chart(fig_ast, use_container_width=True)
                
                # リーダーボード
                st.markdown('<div class="section-header">League Leaders</div>', unsafe_allow_html=True)
                
                leader_tab1, leader_tab2, leader_tab3 = st.tabs([
                    "POINTS", "REBOUNDS", "ASSISTS"
                ])
                
                with leader_tab1:
                    pts_leaders = season_data.groupby('PlayerName').agg({
                        'PTS': ['sum', 'mean', 'count']
                    }).round(1)
                    pts_leaders.columns = ['Total', 'PPG', 'GP']
                    pts_leaders = pts_leaders.sort_values('PPG', ascending=False).head(10)
                    
                    for idx, (player, row) in enumerate(pts_leaders.iterrows(), 1):
                        rank_class = f"rank-{idx}" if idx <= 3 else ""
                        st.markdown(f"""
                        <div class="ranking-row {rank_class}">
                            <div>
                                <span style="color: #1d428a; font-size: 1.25rem; font-weight: 700; margin-right: 1rem;">#{idx}</span>
                                <span style="color: #212529; font-size: 1.1rem; font-weight: 600;">{player}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: #1d428a; font-size: 1.5rem; font-weight: 700;">{row['PPG']:.1f}</span>
                                <span style="color: #6c757d; font-size: 0.9rem; margin-left: 0.5rem;">PPG</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with leader_tab2:
                    reb_leaders = season_data.groupby('PlayerName').agg({
                        'TOT': ['sum', 'mean', 'count']
                    }).round(1)
                    reb_leaders.columns = ['Total', 'RPG', 'GP']
                    reb_leaders = reb_leaders.sort_values('RPG', ascending=False).head(10)
                    
                    for idx, (player, row) in enumerate(reb_leaders.iterrows(), 1):
                        rank_class = f"rank-{idx}" if idx <= 3 else ""
                        st.markdown(f"""
                        <div class="ranking-row {rank_class}">
                            <div>
                                <span style="color: #c8102e; font-size: 1.25rem; font-weight: 700; margin-right: 1rem;">#{idx}</span>
                                <span style="color: #212529; font-size: 1.1rem; font-weight: 600;">{player}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: #c8102e; font-size: 1.5rem; font-weight: 700;">{row['RPG']:.1f}</span>
                                <span style="color: #6c757d; font-size: 0.9rem; margin-left: 0.5rem;">RPG</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with leader_tab3:
                    ast_leaders = season_data.groupby('PlayerName').agg({
                        'AST': ['sum', 'mean', 'count']
                    }).round(1)
                    ast_leaders.columns = ['Total', 'APG', 'GP']
                    ast_leaders = ast_leaders.sort_values('APG', ascending=False).head(10)
                    
                    for idx, (player, row) in enumerate(ast_leaders.iterrows(), 1):
                        rank_class = f"rank-{idx}" if idx <= 3 else ""
                        st.markdown(f"""
                        <div class="ranking-row {rank_class}">
                            <div>
                                <span style="color: #1d428a; font-size: 1.25rem; font-weight: 700; margin-right: 1rem;">#{idx}</span>
                                <span style="color: #212529; font-size: 1.1rem; font-weight: 600;">{player}</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: #1d428a; font-size: 1.5rem; font-weight: 700;">{row['APG']:.1f}</span>
                                <span style="color: #6c757d; font-size: 0.9rem; margin-left: 0.5rem;">APG</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ========================================
    # タブ2: 選手統計
    # ========================================
    with tab2:
        if st.session_state['database'].empty:
            st.info("No data available.")
        else:
            db = st.session_state['database']
            players = sorted(db['PlayerName'].unique())
            
            selected_player = st.selectbox("SELECT PLAYER", players, key='player_select')
            
            if selected_player:
                player_data = db[db['PlayerName'] == selected_player].copy()
                player_data = player_data.sort_values('GameDate')
                
                # 選手情報
                stats = calculate_stats(db, selected_player)
                player_number = player_data['No'].iloc[0] if len(player_data) > 0 else "N/A"
                
                st.markdown(f"""
                <div class="player-card">
                    <div class="player-number">#{player_number}</div>
                    <div class="player-name">{selected_player}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 主要スタッツ
                st.markdown('<div class="section-header">Season Averages</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card primary">
                        <div class="stat-label">PPG</div>
                        <div class="stat-value">{stats['PTS']:.1f}</div>
                        <div class="stat-subtitle">Points</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">RPG</div>
                        <div class="stat-value">{stats['REB']:.1f}</div>
                        <div class="stat-subtitle">Rebounds</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">APG</div>
                        <div class="stat-value">{stats['AST']:.1f}</div>
                        <div class="stat-subtitle">Assists</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">FG%</div>
                        <div class="stat-value">{stats['FG%']:.1f}</div>
                        <div class="stat-subtitle">Field Goal</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col5:
                    st.markdown(f"""
                    <div class="stat-card primary">
                        <div class="stat-label">GP</div>
                        <div class="stat-value">{stats['GP']}</div>
                        <div class="stat-subtitle">Games</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # グラフ
                st.markdown('<div class="section-header">Performance Charts</div>', unsafe_allow_html=True)
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    fig_pts = create_nba_chart(player_data, 'POINTS PER GAME', 'GameDate', 'PTS')
                    st.plotly_chart(fig_pts, use_container_width=True)
                
                with chart_col2:
                    fig_reb = create_nba_chart(player_data, 'REBOUNDS PER GAME', 'GameDate', 'TOT', color='#c8102e')
                    st.plotly_chart(fig_reb, use_container_width=True)
                
                # ゲームログ
                st.markdown('<div class="section-header">Game Log</div>', unsafe_allow_html=True)
                
                display_cols = ['GameDate', 'Opponent', 'PTS', '3PM', '3PA', '3P%', 
                               'FTM', 'FTA', 'FT%', 'TOT', 'AST', 'STL', 'BLK', 'MIN']
                
                st.dataframe(
                    player_data[display_cols],
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
    
    # ========================================
    # タブ3: 試合統計
    # ========================================
    with tab3:
        if st.session_state['database'].empty:
            st.info("No data available.")
        else:
            db = st.session_state['database']
            games = sorted(db['GameDate'].unique(), reverse=True)
            
            selected_game = st.selectbox("SELECT GAME", games, key='game_select')
            
            if selected_game:
                game_data = db[db['GameDate'] == selected_game]
                
                # 試合情報
                opponent = game_data['Opponent'].iloc[0]
                team_score = game_data['TeamScore'].iloc[0]
                opp_score = game_data['OpponentScore'].iloc[0]
                result = "WIN" if team_score > opp_score else "LOSS"
                result_class = "win" if result == "WIN" else "loss"
                
                st.markdown(f"""
                <div class="game-card">
                    <div class="game-date">{selected_game}</div>
                    <div class="teams">TSUKUBA vs {opponent}</div>
                    <div class="score">{team_score} - {opp_score}</div>
                    <div class="result {result_class}">{result}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # チーム統計
                st.markdown('<div class="section-header">Team Statistics</div>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                total_pts = game_data['PTS'].sum()
                total_reb = game_data['TOT'].sum()
                total_ast = game_data['AST'].sum()
                fg_pct = (game_data['3PM'].sum() + game_data['2PM'].sum()) / (game_data['3PA'].sum() + game_data['2PA'].sum()) * 100 if (game_data['3PA'].sum() + game_data['2PA'].sum()) > 0 else 0
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card primary">
                        <div class="stat-label">Total Points</div>
                        <div class="stat-value">{total_pts}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Total Rebounds</div>
                        <div class="stat-value">{total_reb}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Total Assists</div>
                        <div class="stat-value">{total_ast}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">FG%</div>
                        <div class="stat-value">{fg_pct:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # プレイヤーボックススコア
                st.markdown('<div class="section-header">Player Box Score</div>', unsafe_allow_html=True)
                
                display_cols = ['No', 'PlayerName', 'PTS', '3PM', '3PA', '2PM', '2PA', 
                               'FTM', 'FTA', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'PF', 'MIN']
                
                st.dataframe(
                    game_data[display_cols].sort_values('PTS', ascending=False),
                    use_container_width=True,
                    hide_index=True,
                    height=500
                )
    
    # ========================================
    # タブ4: 比較
    # ========================================
    with tab4:
        if st.session_state['database'].empty:
            st.info("No data available.")
        else:
            db = st.session_state['database']
            players = sorted(db['PlayerName'].unique())
            
            st.markdown('<div class="section-header">Player Comparison</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                player1 = st.selectbox("PLAYER 1", players, key='compare_p1')
            
            with col2:
                remaining = [p for p in players if p != player1]
                player2 = st.selectbox("PLAYER 2", remaining, key='compare_p2') if remaining else None
            
            if player1 and player2:
                stats1 = calculate_stats(db, player1)
                stats2 = calculate_stats(db, player2)
                
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
                st.markdown('<div class="section-header">Performance Comparison</div>', unsafe_allow_html=True)
                
                player1_data = db[db['PlayerName'] == player1].sort_values('GameDate')
                player2_data = db[db['PlayerName'] == player2].sort_values('GameDate')
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=player1_data['GameDate'],
                    y=player1_data['PTS'],
                    mode='lines+markers',
                    name=player1,
                    line=dict(color='#1d428a', width=3),
                    marker=dict(size=8)
                ))
                
                fig.add_trace(go.Scatter(
                    x=player2_data['GameDate'],
                    y=player2_data['PTS'],
                    mode='lines+markers',
                    name=player2,
                    line=dict(color='#c8102e', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title='POINTS PER GAME COMPARISON',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#212529'),
                    xaxis=dict(gridcolor='#f0f0f0', showgrid=True),
                    yaxis=dict(gridcolor='#f0f0f0', showgrid=True),
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # ========================================
    # タブ5: データ入力（編集者権限必要）
    # ========================================
    with tab5:
        if not check_password():
            return
        
        st.markdown('<div class="section-header">Data Input</div>', unsafe_allow_html=True)
        
        if not model:
            st.error("⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in secrets.toml")
        else:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("#### Game Information")
                game_date = st.date_input("Game Date", datetime.now())
                season = st.selectbox("Season", ["2023-24", "2024-25", "2025-26", "2026-27"], index=1)
                opponent = st.text_input("Opponent", "")
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    team_score = st.number_input("Tsukuba Score", min_value=0, value=0)
                with col_s2:
                    opponent_score = st.number_input("Opponent Score", min_value=0, value=0)
                
                st.markdown("#### Score Sheet Image")
                uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg', 'webp'])
            
            with col2:
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image, use_container_width=True)
                    
                    if st.button("ANALYZE WITH AI", use_container_width=True, type="primary"):
                        with st.spinner("Analyzing..."):
                            try:
                                prompt = """
Extract basketball scoresheet data from this image in CSV format with headers:

No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN

Rules:
- GS: 1 if starter (●), 0 otherwise
- Percentages: numbers only (no % symbol)
- MIN: format like "32:38"
- Use 0 for missing values
- Exclude Team/Coaches rows
- Exclude TOTALS row
- Extract player names accurately

Output CSV only, no explanations.
"""
                                
                                response = model.generate_content([prompt, image])
                                csv_text = response.text.replace('```csv', '').replace('```', '').strip()
                                
                                df = pd.read_csv(io.StringIO(csv_text))
                                df['GameDate'] = str(game_date)
                                df['Season'] = season
                                df['Opponent'] = opponent
                                df['TeamScore'] = team_score
                                df['OpponentScore'] = opponent_score
                                
                                st.session_state['current_stats'] = df
                                st.success("✅ Analysis complete!")
                                
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
        
        # データ編集
        if 'current_stats' in st.session_state:
            st.markdown('<div class="section-header">Review & Edit Data</div>', unsafe_allow_html=True)
            
            edited_df = st.data_editor(
                st.session_state['current_stats'],
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("SAVE DATA", use_container_width=True, type="primary"):
                    st.session_state['database'] = pd.concat(
                        [st.session_state['database'], edited_df],
                        ignore_index=True
                    )
                    if save_database():
                        st.success("✅ Data saved!")
                        del st.session_state['current_stats']
                        st.rerun()
            
            with col2:
                if st.button("CANCEL", use_container_width=True):
                    del st.session_state['current_stats']
                    st.rerun()
        
        # データ管理
        st.markdown('<div class="section-header">Data Management</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Export")
            if not st.session_state['database'].empty:
                csv = st.session_state['database'].to_csv(index=False)
                st.download_button(
                    label="DOWNLOAD ALL DATA",
                    data=csv,
                    file_name=f"stats_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.markdown("#### Import")
            import_file = st.file_uploader("Upload CSV", type=['csv'], key='import')
            if import_file and st.button("IMPORT DATA"):
                try:
                    import_df = pd.read_csv(import_file)
                    st.session_state['database'] = pd.concat(
                        [st.session_state['database'], import_df],
                        ignore_index=True
                    )
                    if save_database():
                        st.success("✅ Import successful!")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        with col3:
            st.markdown("#### Delete Individual Records")
            if not st.session_state['database'].empty:
                games_list = st.session_state['database'].groupby(['GameDate', 'Opponent']).size().reset_index()[['GameDate', 'Opponent']]
                game_options = [f"{row['GameDate']} vs {row['Opponent']}" for _, row in games_list.iterrows()]
                
                if game_options:
                    selected_game_to_delete = st.selectbox("Select game to delete", [""] + game_options)
                    
                    if selected_game_to_delete and st.button("DELETE SELECTED GAME", type="secondary"):
                        game_date_str = selected_game_to_delete.split(" vs ")[0]
                        opponent_str = selected_game_to_delete.split(" vs ")[1]
                        
                        st.session_state['database'] = st.session_state['database'][
                            ~((st.session_state['database']['GameDate'] == game_date_str) & 
                              (st.session_state['database']['Opponent'] == opponent_str))
                        ]
                        
                        if save_database():
                            st.success(f"✅ Deleted game: {selected_game_to_delete}")
                            st.rerun()

if __name__ == "__main__":
    main()

