"""チーム情報ページ - シーズン別チーム情報表示"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# パスの設定
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).parent.parent))

from database import StatsDatabase
from components import section_header, staff_card
from config import TEAM_INFO_FILE, TEAM_INFO_COLUMNS, STAFF_IMAGES_DIR


def render(db: StatsDatabase):
    """チーム情報ページを表示
    
    Args:
        db: データベースインスタンス
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #000000 0%, #1d428a 50%, #c8102e 100%); padding: 2.5rem 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            🏀 チーム情報
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 0.5rem;">
            TEAM INFORMATION / 筑波大学附属高校 男子バスケットボール部
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # チーム情報ファイルの読み込み
    team_info_path = Path(TEAM_INFO_FILE)
    
    if not team_info_path.exists():
        # 初期データ作成
        team_info_df = pd.DataFrame(columns=TEAM_INFO_COLUMNS)
        team_info_df.to_csv(team_info_path, index=False)
    else:
        team_info_df = pd.read_csv(team_info_path)
    
    # シーズン選択
    if not db.df.empty:
        seasons = db.get_all_seasons()
    else:
        seasons = ["2024-25"]
    
    col1, col2 = st.columns([2, 3])
    with col1:
        selected_season = st.selectbox(
            "シーズンを選択 / Select Season",
            seasons,
            key='team_info_season'
        )
    
    if selected_season:
        # シーズン情報取得
        season_info = team_info_df[team_info_df['Season'] == selected_season]
        
        if season_info.empty:
            section_header("TEAM INFORMATION", "チーム情報")
            st.info(f"📝 {selected_season}シーズンの情報がまだ登録されていません。管理者設定から登録してください。")
            
            # 編集フォーム（管理者向け）
            if st.checkbox("➕ 新規チーム情報を追加"):
                with st.form("add_team_info"):
                    st.markdown("### 新規チーム情報入力")
                    
                    team_name = st.text_input("チーム名", "筑波大学附属高等学校")
                    head_coach = st.text_input("ヘッドコーチ")
                    assistant_coaches = st.text_area("アシスタントコーチ（カンマ区切り）")
                    managers = st.text_area("マネージャー（カンマ区切り）")
                    home_venue = st.text_input("ホーム体育館")
                    team_motto = st.text_area("チームモットー")
                    season_goals = st.text_area("シーズン目標")
                    
                    if st.form_submit_button("💾 保存"):
                        new_info = pd.DataFrame([{
                            'Season': selected_season,
                            'TeamName': team_name,
                            'HeadCoach': head_coach,
                            'AssistantCoaches': assistant_coaches,
                            'Managers': managers,
                            'HomeVenue': home_venue,
                            'TeamMotto': team_motto,
                            'SeasonGoals': season_goals
                        }])
                        
                        team_info_df = pd.concat([team_info_df, new_info], ignore_index=True)
                        team_info_df.to_csv(team_info_path, index=False)
                        st.success("✅ チーム情報を保存しました")
                        st.rerun()
        else:
            info = season_info.iloc[0]
            
            # チーム概要
            section_header("TEAM OVERVIEW", "チーム概要")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 2rem; border-radius: 12px; border: 2px solid #333; margin-bottom: 1rem;">
                    <div style="color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;">チーム名 / TEAM NAME</div>
                    <div style="color: #ffffff; font-size: 1.8rem; font-weight: 700;">{info['TeamName']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 2rem; border-radius: 12px; border: 2px solid #333; margin-bottom: 1rem;">
                    <div style="color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;">ホーム体育館 / HOME VENUE</div>
                    <div style="color: #ffffff; font-size: 1.3rem; font-weight: 600;">📍 {info['HomeVenue']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 2rem; border-radius: 12px; border: 2px solid #333; margin-bottom: 1rem;">
                    <div style="color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;">チームモットー / TEAM MOTTO</div>
                    <div style="color: #ffffff; font-size: 1.2rem; font-weight: 600; font-style: italic;">"{info['TeamMotto']}"</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 2rem; border-radius: 12px; border: 2px solid #333; margin-bottom: 1rem;">
                    <div style="color: #888; font-size: 0.9rem; margin-bottom: 0.5rem;">シーズン目標 / SEASON GOALS</div>
                    <div style="color: #ffffff; font-size: 1.1rem; font-weight: 500;">{info['SeasonGoals']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # コーチング・スタッフ
            section_header("COACHING STAFF", "コーチング・スタッフ")
            
            staff_col1, staff_col2, staff_col3 = st.columns(3)
            
            with staff_col1:
                st.markdown("#### ヘッドコーチ / HEAD COACH")
                head_coach_img = Path(STAFF_IMAGES_DIR) / f"{info['HeadCoach']}_ヘッドコーチ.png"
                staff_card(
                    info['HeadCoach'],
                    "ヘッドコーチ / Head Coach",
                    str(head_coach_img) if head_coach_img.exists() else None
                )
            
            with staff_col2:
                st.markdown("#### アシスタントコーチ / ASSISTANT COACHES")
                if pd.notna(info['AssistantCoaches']) and info['AssistantCoaches']:
                    for coach in str(info['AssistantCoaches']).split(','):
                        coach = coach.strip()
                        coach_img = Path(STAFF_IMAGES_DIR) / f"{coach}_アシスタントコーチ.png"
                        staff_card(
                            coach,
                            "アシスタントコーチ / Assistant Coach",
                            str(coach_img) if coach_img.exists() else None
                        )
                else:
                    st.info("情報なし")
            
            with staff_col3:
                st.markdown("#### マネージャー / MANAGERS")
                if pd.notna(info['Managers']) and info['Managers']:
                    for manager in str(info['Managers']).split(','):
                        manager = manager.strip()
                        manager_img = Path(STAFF_IMAGES_DIR) / f"{manager}_マネージャー.png"
                        staff_card(
                            manager,
                            "マネージャー / Manager",
                            str(manager_img) if manager_img.exists() else None
                        )
                else:
                    st.info("情報なし")
            
            # 編集ボタン
            st.markdown("---")
            if st.checkbox("✏️ チーム情報を編集"):
                with st.form("edit_team_info"):
                    st.markdown("### チーム情報編集")
                    
                    team_name = st.text_input("チーム名", value=info['TeamName'])
                    head_coach = st.text_input("ヘッドコーチ", value=info['HeadCoach'])
                    assistant_coaches = st.text_area("アシスタントコーチ（カンマ区切り）", value=info['AssistantCoaches'])
                    managers = st.text_area("マネージャー（カンマ区切り）", value=info['Managers'])
                    home_venue = st.text_input("ホーム体育館", value=info['HomeVenue'])
                    team_motto = st.text_area("チームモットー", value=info['TeamMotto'])
                    season_goals = st.text_area("シーズン目標", value=info['SeasonGoals'])
                    
                    if st.form_submit_button("💾 更新"):
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'TeamName'] = team_name
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'HeadCoach'] = head_coach
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'AssistantCoaches'] = assistant_coaches
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'Managers'] = managers
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'HomeVenue'] = home_venue
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'TeamMotto'] = team_motto
                        team_info_df.loc[team_info_df['Season'] == selected_season, 'SeasonGoals'] = season_goals
                        
                        team_info_df.to_csv(team_info_path, index=False)
                        st.success("✅ チーム情報を更新しました")
                        st.rerun()
