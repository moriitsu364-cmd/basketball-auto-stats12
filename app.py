import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ========================================
# ページ設定と初期化
# ========================================
st.set_page_config(
    page_title="TSUKUBA HS Basketball Stats Analyzer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    /* メインカラースキーム */
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #004E89;
        --accent-color: #F7931E;
        --bg-dark: #1A1A2E;
        --bg-light: #16213E;
    }
    
    /* ヘッダースタイル */
    .main-header {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* カードスタイル */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #FF6B35;
        margin-bottom: 1rem;
    }
    
    .stat-card h3 {
        color: #004E89;
        margin-top: 0;
    }
    
    /* メトリクススタイル */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* テーブルスタイル */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* サイドバースタイル */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A1A2E 0%, #16213E 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* ボタンスタイル */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255,107,53,0.4);
    }
    
    /* タブスタイル */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #004E89;
        font-weight: 600;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #FF6B35;
        color: #FF6B35;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース初期化
# ========================================
def init_database():
    """データベースの初期化"""
    if 'database' not in st.session_state:
        st.session_state['database'] = pd.DataFrame(columns=[
            'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
            '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
            'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
            'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
        ])
    
    if 'seasons' not in st.session_state:
        st.session_state['seasons'] = []
    
    if 'players' not in st.session_state:
        st.session_state['players'] = set()

# ========================================
# Gemini API設定
# ========================================
@st.cache_resource
def setup_gemini():
    """Gemini APIのセットアップ"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None, None
    
    try:
        genai.configure(api_key=api_key)
        
        # 利用可能なモデルを検索
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # 優先順位でモデルを選択
        priority_models = [
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash',
            'models/gemini-pro-vision'
        ]
        
        model_name = None
        for preferred in priority_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        if not model_name and available_models:
            model_name = available_models[0]
        
        if model_name:
            model = genai.GenerativeModel(model_name)
            return model, model_name
        
        return None, None
        
    except Exception as e:
        st.error(f"Gemini APIのセットアップエラー: {e}")
        return None, None

# ========================================
# 統計計算関数
# ========================================
def calculate_per_game_stats(df):
    """試合ごとの平均統計を計算"""
    numeric_cols = ['PTS', '3PM', '3PA', '2PM', '2PA', 'FTM', 'FTA', 
                    'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'PF']
    
    stats = {}
    for col in numeric_cols:
        if col in df.columns:
            stats[f'{col}_avg'] = df[col].mean()
            stats[f'{col}_total'] = df[col].sum()
    
    stats['games_played'] = len(df)
    
    # シュート成功率の計算
    if '3PA' in df.columns and df['3PA'].sum() > 0:
        stats['3P%_avg'] = (df['3PM'].sum() / df['3PA'].sum() * 100)
    if '2PA' in df.columns and df['2PA'].sum() > 0:
        stats['2P%_avg'] = (df['2PM'].sum() / df['2PA'].sum() * 100)
    if 'FTA' in df.columns and df['FTA'].sum() > 0:
        stats['FT%_avg'] = (df['FTM'].sum() / df['FTA'].sum() * 100)
    
    return stats

def create_player_chart(player_data):
    """選手の統計チャートを作成"""
    # ゲームごとの得点推移
    fig_points = go.Figure()
    fig_points.add_trace(go.Scatter(
        x=player_data['GameDate'],
        y=player_data['PTS'],
        mode='lines+markers',
        name='得点',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=10)
    ))
    fig_points.update_layout(
        title='試合ごとの得点推移',
        xaxis_title='試合日',
        yaxis_title='得点',
        template='plotly_white',
        height=400
    )
    
    return fig_points

def create_stats_radar(stats):
    """レーダーチャートを作成"""
    categories = ['得点', 'リバウンド', 'アシスト', 'スティール', 'ブロック']
    values = [
        stats.get('PTS_avg', 0),
        stats.get('TOT_avg', 0),
        stats.get('AST_avg', 0),
        stats.get('STL_avg', 0),
        stats.get('BLK_avg', 0)
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 107, 53, 0.3)',
        line=dict(color='#FF6B35', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(values) * 1.2])
        ),
        showlegend=False,
        height=400,
        title='平均スタッツ'
    )
    
    return fig

# ========================================
# メイン画面
# ========================================
def main():
    init_database()
    
    # ヘッダー
    st.markdown("""
    <div class="main-header">
        <h1>🏀 Pro Basketball Stats Analyzer</h1>
        <p style="color: white; margin: 0; font-size: 1.1rem;">プロフェッショナルバスケットボール統計管理システム</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gemini APIのセットアップ
    model, model_name = setup_gemini()
    
    # サイドバー
    with st.sidebar:
        st.markdown("### 📊 ナビゲーション")
        menu = st.radio(
            "",
            ["🎯 スコアシート解析", "📈 選手分析", "🏆 シーズン統計", "⚙️ データ管理"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        if model_name:
            st.success(f"✅ AI モデル接続済")
            st.caption(f"使用モデル: {model_name.split('/')[-1]}")
        else:
            st.error("❌ APIキー未設定")
        
        st.divider()
        
        # データベース統計
        st.markdown("### 📚 データベース情報")
        total_games = len(st.session_state['database'])
        total_players = len(st.session_state['database']['PlayerName'].unique()) if total_games > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("試合数", total_games)
        with col2:
            st.metric("選手数", total_players)
    
    # ========================================
    # メニュー1: スコアシート解析
    # ========================================
    if menu == "🎯 スコアシート解析":
        st.markdown("## 📸 スコアシート画像解析")
        
        if not model:
            st.error("⚠️ Gemini APIキーが設定されていません。Secretsに`GEMINI_API_KEY`を追加してください。")
            return
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 試合情報入力")
            game_date = st.date_input("📅 試合日", datetime.now())
            season = st.selectbox("🏆 シーズン", 
                                ["2023-24", "2024-25", "2025-26", "2026-27"],
                                index=1)
            opponent = st.text_input("🆚 対戦相手", "")
            
            col_score1, col_score2 = st.columns(2)
            with col_score1:
                team_score = st.number_input("自チームスコア", min_value=0, value=0)
            with col_score2:
                opponent_score = st.number_input("相手スコア", min_value=0, value=0)
            
            st.divider()
            
            uploaded_file = st.file_uploader(
                "📁 スコアシート画像をアップロード",
                type=['png', 'jpg', 'jpeg', 'webp'],
                help="PNG, JPG, JPEG, WEBP形式に対応"
            )
        
        with col2:
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.markdown("### 📷 アップロード画像")
                st.image(image, use_container_width=True)
                
                if st.button("🚀 AI解析を実行", use_container_width=True):
                    with st.spinner("🤖 AIが画像を解析中..."):
                        try:
                            # 詳細なプロンプト
                            prompt = """
この画像からバスケットボールのスコアシートデータを抽出してください。
以下の形式のCSVで出力してください（ヘッダー行を含む）：

No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN

注意事項：
- GSは先発選手の場合「●」があれば1、なければ0
- パーセンテージは数値のみ（%記号不要）
- MINは「32:38」のような形式で
- 数値がない場合は0を入力
- Team/Coachesの行は除外
- TOTALSの行は除外

CSVのみを出力し、説明文は不要です。
"""
                            
                            response = model.generate_content([prompt, image])
                            
                            # CSVデータの抽出
                            csv_text = response.text
                            csv_text = csv_text.replace('```csv', '').replace('```', '').strip()
                            
                            # データフレームに変換
                            df = pd.read_csv(io.StringIO(csv_text))
                            
                            # 試合情報を追加
                            df['GameDate'] = str(game_date)
                            df['Season'] = season
                            df['Opponent'] = opponent
                            df['TeamScore'] = team_score
                            df['OpponentScore'] = opponent_score
                            
                            st.session_state['current_stats'] = df
                            st.success("✅ 解析完了！")
                            
                        except Exception as e:
                            st.error(f"❌ エラーが発生しました: {str(e)}")
                            st.info("画像が不鮮明な場合や、フォーマットが異なる場合はエラーになることがあります。")
        
        # 解析結果の表示と編集
        if 'current_stats' in st.session_state:
            st.divider()
            st.markdown("## ✏️ 解析結果の確認・修正")
            
            edited_df = st.data_editor(
                st.session_state['current_stats'],
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("💾 データベースに保存", use_container_width=True):
                    st.session_state['database'] = pd.concat(
                        [st.session_state['database'], edited_df],
                        ignore_index=True
                    )
                    
                    # 選手リストの更新
                    st.session_state['players'].update(edited_df['PlayerName'].unique())
                    
                    st.success("✅ データベースに保存しました！")
                    del st.session_state['current_stats']
                    st.rerun()
            
            with col2:
                if st.button("🗑️ キャンセル", use_container_width=True):
                    del st.session_state['current_stats']
                    st.rerun()
    
    # ========================================
    # メニュー2: 選手分析
    # ========================================
    elif menu == "📈 選手分析":
        st.markdown("## 👤 選手別詳細分析")
        
        if st.session_state['database'].empty:
            st.info("📭 まだデータがありません。スコアシート解析からデータを追加してください。")
            return
        
        db = st.session_state['database']
        players = sorted(db['PlayerName'].unique())
        
        selected_player = st.selectbox("🎯 選手を選択", players)
        
        if selected_player:
            player_data = db[db['PlayerName'] == selected_player].copy()
            player_data = player_data.sort_values('GameDate')
            
            # 統計計算
            stats = calculate_per_game_stats(player_data)
            
            # 基本情報
            st.markdown(f"### 📊 {selected_player} のスタッツ")
            
            # メトリクス表示
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("試合数", f"{stats['games_played']}試合")
            with col2:
                st.metric("平均得点", f"{stats.get('PTS_avg', 0):.1f}点")
            with col3:
                st.metric("平均リバウンド", f"{stats.get('TOT_avg', 0):.1f}本")
            with col4:
                st.metric("平均アシスト", f"{stats.get('AST_avg', 0):.1f}本")
            with col5:
                st.metric("総得点", f"{stats.get('PTS_total', 0):.0f}点")
            
            st.divider()
            
            # タブで詳細表示
            tab1, tab2, tab3, tab4 = st.tabs(["📈 推移グラフ", "🎯 シュート統計", "📋 試合一覧", "🔍 詳細データ"])
            
            with tab1:
                # 得点推移グラフ
                fig_points = create_player_chart(player_data)
                st.plotly_chart(fig_points, use_container_width=True)
                
                # レーダーチャート
                col1, col2 = st.columns(2)
                with col1:
                    fig_radar = create_stats_radar(stats)
                    st.plotly_chart(fig_radar, use_container_width=True)
                
                with col2:
                    # シュート成功率の推移
                    if '3P%' in player_data.columns:
                        fig_shooting = go.Figure()
                        fig_shooting.add_trace(go.Scatter(
                            x=player_data['GameDate'],
                            y=player_data['3P%'],
                            mode='lines+markers',
                            name='3P成功率',
                            line=dict(color='#004E89')
                        ))
                        fig_shooting.update_layout(
                            title='3ポイント成功率推移',
                            yaxis_title='成功率(%)',
                            height=400,
                            template='plotly_white'
                        )
                        st.plotly_chart(fig_shooting, use_container_width=True)
            
            with tab2:
                st.markdown("### 🎯 シュート統計詳細")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 3ポイント")
                    if stats.get('3P%_avg'):
                        st.metric("成功率", f"{stats['3P%_avg']:.1f}%")
                    st.metric("成功数", f"{stats.get('3PM_total', 0):.0f}")
                    st.metric("試投数", f"{stats.get('3PA_total', 0):.0f}")
                
                with col2:
                    st.markdown("#### 2ポイント")
                    if stats.get('2P%_avg'):
                        st.metric("成功率", f"{stats['2P%_avg']:.1f}%")
                    st.metric("成功数", f"{stats.get('2PM_total', 0):.0f}")
                    st.metric("試投数", f"{stats.get('2PA_total', 0):.0f}")
                
                with col3:
                    st.markdown("#### フリースロー")
                    if stats.get('FT%_avg'):
                        st.metric("成功率", f"{stats['FT%_avg']:.1f}%")
                    st.metric("成功数", f"{stats.get('FTM_total', 0):.0f}")
                    st.metric("試投数", f"{stats.get('FTA_total', 0):.0f}")
            
            with tab3:
                st.markdown("### 📋 全試合データ")
                display_cols = ['GameDate', 'Opponent', 'PTS', '3PM', '3PA', '2PM', '2PA', 
                               'FTM', 'FTA', 'TOT', 'AST', 'STL', 'BLK', 'TO', 'PF', 'MIN']
                st.dataframe(
                    player_data[display_cols],
                    use_container_width=True,
                    hide_index=True
                )
            
            with tab4:
                st.markdown("### 🔍 完全データ")
                st.dataframe(player_data, use_container_width=True, hide_index=True)
    
    # ========================================
    # メニュー3: シーズン統計
    # ========================================
    elif menu == "🏆 シーズン統計":
        st.markdown("## 🏆 シーズン別統計")
        
        if st.session_state['database'].empty:
            st.info("📭 まだデータがありません。")
            return
        
        db = st.session_state['database']
        seasons = sorted(db['Season'].unique(), reverse=True)
        
        selected_season = st.selectbox("📅 シーズンを選択", seasons)
        
        if selected_season:
            season_data = db[db['Season'] == selected_season]
            
            # シーズンサマリー
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("総試合数", len(season_data['GameDate'].unique()))
            with col2:
                st.metric("参加選手数", season_data['PlayerName'].nunique())
            with col3:
                total_points = season_data['PTS'].sum()
                st.metric("総得点", f"{total_points:.0f}点")
            with col4:
                avg_points = season_data.groupby('GameDate')['PTS'].sum().mean()
                st.metric("平均チーム得点", f"{avg_points:.1f}点")
            
            st.divider()
            
            # 選手ランキング
            st.markdown("### 🏅 選手ランキング")
            
            tab1, tab2, tab3, tab4 = st.tabs(["得点王", "リバウンド王", "アシスト王", "総合"])
            
            with tab1:
                pts_ranking = season_data.groupby('PlayerName')['PTS'].agg(['sum', 'mean', 'count'])
                pts_ranking = pts_ranking.sort_values('sum', ascending=False).head(10)
                pts_ranking.columns = ['総得点', '平均得点', '試合数']
                st.dataframe(pts_ranking, use_container_width=True)
            
            with tab2:
                reb_ranking = season_data.groupby('PlayerName')['TOT'].agg(['sum', 'mean', 'count'])
                reb_ranking = reb_ranking.sort_values('sum', ascending=False).head(10)
                reb_ranking.columns = ['総リバウンド', '平均リバウンド', '試合数']
                st.dataframe(reb_ranking, use_container_width=True)
            
            with tab3:
                ast_ranking = season_data.groupby('PlayerName')['AST'].agg(['sum', 'mean', 'count'])
                ast_ranking = ast_ranking.sort_values('sum', ascending=False).head(10)
                ast_ranking.columns = ['総アシスト', '平均アシスト', '試合数']
                st.dataframe(ast_ranking, use_container_width=True)
            
            with tab4:
                # 総合スタッツテーブル
                player_stats = season_data.groupby('PlayerName').agg({
                    'PTS': ['sum', 'mean'],
                    'TOT': ['sum', 'mean'],
                    'AST': ['sum', 'mean'],
                    'STL': 'sum',
                    'BLK': 'sum',
                    'GameDate': 'count'
                }).round(1)
                
                player_stats.columns = ['総得点', '平均得点', '総REB', '平均REB', 
                                       '総AST', '平均AST', 'STL', 'BLK', '試合数']
                player_stats = player_stats.sort_values('総得点', ascending=False)
                
                st.dataframe(player_stats, use_container_width=True)
    
    # ========================================
    # メニュー4: データ管理
    # ========================================
    elif menu == "⚙️ データ管理":
        st.markdown("## ⚙️ データベース管理")
        
        tab1, tab2, tab3 = st.tabs(["📊 全データ表示", "📥 エクスポート", "🗑️ データ削除"])
        
        with tab1:
            st.markdown("### 📚 全データベース")
            if not st.session_state['database'].empty:
                st.dataframe(
                    st.session_state['database'],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("データがありません")
        
        with tab2:
            st.markdown("### 📥 データのエクスポート")
            if not st.session_state['database'].empty:
                # CSV形式でダウンロード
                csv = st.session_state['database'].to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 CSVファイルでダウンロード",
                    data=csv,
                    file_name=f"basketball_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                # JSON形式でダウンロード
                json_str = st.session_state['database'].to_json(orient='records', force_ascii=False)
                st.download_button(
                    label="📥 JSONファイルでダウンロード",
                    data=json_str,
                    file_name=f"basketball_stats_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.info("エクスポートするデータがありません")
        
        with tab3:
            st.markdown("### 🗑️ データの削除")
            st.warning("⚠️ この操作は取り消せません！")
            
            if st.button("🗑️ 全データを削除", use_container_width=True):
                st.session_state['database'] = pd.DataFrame(columns=st.session_state['database'].columns)
                st.session_state['players'] = set()
                st.success("全データを削除しました")
                st.rerun()

if __name__ == "__main__":
    main()
