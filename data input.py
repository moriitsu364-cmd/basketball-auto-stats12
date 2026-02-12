"""データ入力ページ"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
from PIL import Image
from database import StatsDatabase
from auth import check_password
from ai import setup_gemini, analyze_scoresheet
from components import section_header
from config import SEASONS


def render(db: StatsDatabase):
    """データ入力ページを表示
    
    Args:
        db: データベースインスタンス
    """
    if not check_password():
        return
    
    section_header("Data Input")
    
    model, model_name = setup_gemini()
    
    if not model:
        st.error("⚠️ Gemini API key not configured. Please set GEMINI_API_KEY in secrets.toml")
        return
    
    # データ入力フォーム
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Game Information")
        game_date = st.date_input("Game Date", datetime.now())
        season = st.selectbox("Season", SEASONS, index=1)
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
                        csv_text = analyze_scoresheet(model, image)
                        
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
        section_header("Review & Edit Data")
        
        edited_df = st.data_editor(
            st.session_state['current_stats'],
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("SAVE DATA", use_container_width=True, type="primary"):
                db.add_game(edited_df)
                if db.save():
                    st.success("✅ Data saved!")
                    del st.session_state['current_stats']
                    st.rerun()
        
        with col2:
            if st.button("CANCEL", use_container_width=True):
                del st.session_state['current_stats']
                st.rerun()
    
    # データ管理
    section_header("Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Export")
        if not db.df.empty:
            csv = db.df.to_csv(index=False)
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
                db.add_game(import_df)
                if db.save():
                    st.success("✅ Import successful!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col3:
        st.markdown("#### Delete Individual Records")
        if not db.df.empty:
            games_list = db.df.groupby(['GameDate', 'Opponent']).size().reset_index()[['GameDate', 'Opponent']]
            game_options = [f"{row['GameDate']} vs {row['Opponent']}" for _, row in games_list.iterrows()]
            
            if game_options:
                selected_game_to_delete = st.selectbox("Select game to delete", [""] + game_options)
                
                if selected_game_to_delete and st.button("DELETE SELECTED GAME", type="secondary"):
                    game_date_str = selected_game_to_delete.split(" vs ")[0]
                    opponent_str = selected_game_to_delete.split(" vs ")[1]
                    
                    db.delete_game(game_date_str, opponent_str)
                    
                    if db.save():
                        st.success(f"✅ Deleted game: {selected_game_to_delete}")
                        st.rerun()
