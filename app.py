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
# ページ設定 & CSS (提供されたNBA風デザイン)
# ========================================
st.set_page_config(page_title="Tsukuba Highschool Stats", page_icon="🏀", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0d1117 0%, #161b22 100%); }
    .nba-header {
        background: linear-gradient(135deg, #1d1d1d 0%, #2d2d2d 100%);
        padding: 2rem; margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #c9082a;
        box-shadow: 0 4px 20px rgba(201, 8, 42, 0.3);
    }
    .nba-header h1 { color: #ffffff; font-size: 2.5rem; font-weight: 800; margin: 0; }
    .stat-card-nba {
        background: linear-gradient(135deg, #1d1d1d 0%, #2d2d2d 100%);
        padding: 1.5rem; border-radius: 12px; border: 1px solid #2d2d2d;
        text-align: center; margin-bottom: 1rem;
    }
    .stat-label { color: #a0a0a0; font-size: 0.8rem; text-transform: uppercase; }
    .stat-value { color: #ffffff; font-size: 2rem; font-weight: 700; }
    .section-header { color: #ffffff; font-size: 1.5rem; font-weight: 700; border-bottom: 2px solid #c9082a; padding-bottom: 5px; margin: 20px 0; }
</style>
""", unsafe_allow_html=True)

# ========================================
# データベース初期化
# ========================================
if 'database' not in st.session_state:
    st.session_state['database'] = pd.DataFrame(columns=[
        'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
        '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
        'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
        'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
        'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
    ])

# ========================================
# Gemini API 設定 & 解析ロジック
# ========================================
def setup_gemini():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("APIキーが設定されていません。")
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def analyze_score_sheet(image, model):
    """スコアシート画像を解析してJSONとして返す"""
    prompt = """
    バスケットボールのスコアシートを解析し、以下のJSONフォーマットで各選手のスタッツを出力してください。
    数値が読み取れない場合は0としてください。
    
    JSON形式:
    [
      {
        "No": "背番号",
        "PlayerName": "名前",
        "PTS": 得点,
        "3PM": 3P成功, "3PA": 3P試投,
        "2PM": 2P成功, "2PA": 2P試投,
        "FTM": フリースロー成功, "FTA": フリースロー試投,
        "TOT": リバウンド合計, "AST": アシスト, "STL": スティール, "BLK": ブロック,
        "TO": ターンオーバー, "PF": ファウル, "MIN": 出場時間
      }
    ]
    """
    try:
        response = model.generate_content([prompt, image])
        # JSON部分を抽出
        text = response.text
        start = text.find('[')
        end = text.rfind(']') + 1
        return json.loads(text[start:end])
    except Exception as e:
        st.error(f"解析失敗: {e}")
        return None

# ========================================
# ヘルパー関数
# ========================================
def create_nba_style_chart(data, title, x_col, y_col, color='#c9082a'):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data[x_col], y=data[y_col], mode='lines+markers', line=dict(color=color, width=3), fill='tozeroy'))
    fig.update_layout(title=title, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=300)
    return fig

# ========================================
# メイン画面
# ========================================
st.markdown('<div class="nba-header"><h1>🏀 TSUKUBA STATS CENTRAL</h1><p style="color:gray">筑波大学附属高校男子バスケットボール部</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏆 SEASON", "👤 PLAYER", "📊 GAME", "📥 INPUT"])

# --- タブ4: データ入力 (ここが重要) ---
with tab4:
    st.markdown('<div class="section-header">Upload Score Sheet</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        game_date = st.date_input("試合日", datetime.now())
        season = st.selectbox("シーズン", ["2024-25", "2025-26", "2026-27"])
        opponent = st.text_input("対戦相手")
        t_score = st.number_input("筑波スコア", min_value=0)
        o_score = st.number_input("相手スコア", min_value=0)
        uploaded_file = st.file_uploader("スコアシート画像を選択", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        with col2:
            st.image(image, caption="アップロード画像", use_container_width=True)
            if st.button("🚀 画像からスタッツを抽出"):
                model = setup_gemini()
                if model:
                    with st.spinner("AIがスタッツを読み取っています..."):
                        results = analyze_score_sheet(image, model)
                        if results:
                            # 抽出データを一時的にDataFrame化して確認
                            new_df = pd.DataFrame(results)
                            new_df['GameDate'] = str(game_date)
                            new_df['Season'] = season
                            new_df['Opponent'] = opponent
                            new_df['TeamScore'] = t_score
                            new_df['OpponentScore'] = o_score
                            
                            st.session_state['temp_df'] = new_df
                            st.success("読み取り完了！内容を確認して保存してください。")

    if 'temp_df' in st.session_state:
        st.markdown("### 読み取り結果プレビュー")
        edited_df = st.data_editor(st.session_state['temp_df'])
        if st.button("✅ データベースに保存"):
            st.session_state['database'] = pd.concat([st.session_state['database'], edited_df], ignore_index=True)
            st.success("データを保存しました！")
            del st.session_state['temp_df']

# --- タブ1: シーズン統計 (簡易版) ---
with tab1:
    db = st.session_state['database']
    if db.empty:
        st.info("データがありません。")
    else:
        st.markdown('<div class="section-header">Season Leaders</div>', unsafe_allow_html=True)
        leaders = db.groupby('PlayerName')['PTS'].mean().sort_values(ascending=False).head(5)
        cols = st.columns(len(leaders))
        for i, (name, val) in enumerate(leaders.items()):
            with cols[i]:
                st.markdown(f'<div class="stat-card-nba"><div class="stat-label">{name}</div><div class="stat-value">{val:.1f}</div><div style="color:#c9082a">PPG</div></div>', unsafe_allow_html=True)
        st.dataframe(db, use_container_width=True)

# --- タブ2: 選手スタッツ ---
with tab2:
    if not db.empty:
        p_name = st.selectbox("選手名を選択", db['PlayerName'].unique())
        p_data = db[db['PlayerName'] == p_name].sort_values('GameDate')
        
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(create_nba_style_chart(p_data, "Points Progression", 'GameDate', 'PTS'), use_container_width=True)
        with c2:
            st.plotly_chart(create_nba_style_chart(p_data, "Rebounds Progression", 'GameDate', 'TOT', '#17408B'), use_container_width=True)
