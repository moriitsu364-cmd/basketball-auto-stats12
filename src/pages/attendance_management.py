"""予定管理ページ - マネージャー・選手・顧問専用"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json

# データファイルのパス
SCHEDULE_FILE = Path(__file__).parent.parent.parent / "data" / "schedule.json"


def load_schedule_data():
    """予定データを読み込み"""
    try:
        SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if SCHEDULE_FILE.exists():
            with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            # 初期データ
            return {
                "schedules": [
                    {
                        "id": 1,
                        "date": "2026-02-20",
                        "event": "練習試合 vs 開成高校",
                        "location": "本校体育館",
                        "type": "practice",
                        "time": "15:00",
                        "notes": ""
                    },
                    {
                        "id": 2,
                        "date": "2026-02-23",
                        "event": "関東大会 1回戦",
                        "location": "駒沢体育館",
                        "type": "tournament",
                        "time": "13:00",
                        "notes": "集合時刻: 11:00"
                    }
                ]
            }
    except Exception as e:
        st.error(f"予定データの読み込みエラー: {e}")
        return {"schedules": []}


def save_schedule_data(data):
    """予定データを保存"""
    try:
        SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"予定データの保存エラー: {e}")
        return False


def render(db):
    """予定管理ページをレンダリング"""
    
    st.markdown("""
    <style>
    .schedule-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #1d428a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .schedule-date {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1d428a;
        margin-bottom: 8px;
    }
    
    .schedule-event {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 8px;
    }
    
    .schedule-details {
        color: #666;
        font-size: 0.95rem;
    }
    
    .schedule-type-practice {
        background: #e3f2fd;
        color: #1976d2;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .schedule-type-tournament {
        background: #fce4ec;
        color: #c2185b;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .schedule-type-training {
        background: #f3e5f5;
        color: #7b1fa2;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-upcoming {
        background: #e8f5e9;
        color: #2e7d32;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .status-completed {
        background: #f5f5f5;
        color: #757575;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # データ読み込み
    schedule_data = load_schedule_data()
    schedules = schedule_data.get("schedules", [])
    
    # ヘッダー
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("## 📅 予定管理表")
        st.markdown("チームの練習・試合スケジュールを管理します")
    
    with col2:
        if st.button("➕ 新規予定追加", type="primary", use_container_width=True):
            st.session_state.show_schedule_form = True
    
    st.markdown("---")
    
    # 新規予定追加フォーム
    if st.session_state.get('show_schedule_form', False):
        with st.expander("新規予定を追加", expanded=True):
            with st.form("new_schedule_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_name = st.text_input("イベント名 *", placeholder="例: 練習試合 vs 開成高校")
                    event_date = st.date_input("日付 *", min_value=datetime.now().date())
                    event_time = st.time_input("時刻", value=datetime.strptime("15:00", "%H:%M").time())
                
                with col2:
                    event_type = st.selectbox("種類 *", ["practice", "tournament", "training"], 
                                             format_func=lambda x: {"practice": "練習試合", "tournament": "公式戦", "training": "練習"}[x])
                    event_location = st.text_input("場所 *", placeholder="例: 本校体育館")
                    event_notes = st.text_area("備考", placeholder="集合時刻などの追加情報")
                
                col1, col2, col3 = st.columns([1, 1, 4])
                
                with col1:
                    if st.form_submit_button("追加", type="primary", use_container_width=True):
                        if event_name and event_date and event_location:
                            new_schedule = {
                                "id": max([s["id"] for s in schedules], default=0) + 1,
                                "date": event_date.strftime("%Y-%m-%d"),
                                "event": event_name,
                                "location": event_location,
                                "type": event_type,
                                "time": event_time.strftime("%H:%M"),
                                "notes": event_notes
                            }
                            schedules.append(new_schedule)
                            schedule_data["schedules"] = schedules
                            
                            if save_schedule_data(schedule_data):
                                st.success("✅ 予定を追加しました")
                                st.session_state.show_schedule_form = False
                                st.rerun()
                            else:
                                st.error("❌ 予定の保存に失敗しました")
                        else:
                            st.error("必須項目を入力してください")
                
                with col2:
                    if st.form_submit_button("キャンセル", use_container_width=True):
                        st.session_state.show_schedule_form = False
                        st.rerun()
    
    # タブで表示切り替え
    tab1, tab2 = st.tabs(["📋 予定一覧", "📊 カレンダー表示"])
    
    with tab1:
        # 予定を日付順にソート
        sorted_schedules = sorted(schedules, key=lambda x: x["date"], reverse=True)
        
        # フィルター
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.selectbox("種類で絞り込み", 
                                      ["全て", "練習試合", "公式戦", "練習"],
                                      key="schedule_filter_type")
        
        with col2:
            filter_status = st.selectbox("ステータスで絞り込み",
                                        ["全て", "予定", "完了"],
                                        key="schedule_filter_status")
        
        # フィルタリング
        filtered_schedules = sorted_schedules
        
        if filter_type != "全て":
            type_map = {"練習試合": "practice", "公式戦": "tournament", "練習": "training"}
            filtered_schedules = [s for s in filtered_schedules if s["type"] == type_map[filter_type]]
        
        if filter_status != "全て":
            today = datetime.now().date()
            if filter_status == "予定":
                filtered_schedules = [s for s in filtered_schedules if datetime.strptime(s["date"], "%Y-%m-%d").date() >= today]
            else:
                filtered_schedules = [s for s in filtered_schedules if datetime.strptime(s["date"], "%Y-%m-%d").date() < today]
        
        st.markdown(f"### 表示中: {len(filtered_schedules)} 件")
        
        # 予定カードを表示
        if filtered_schedules:
            for schedule in filtered_schedules:
                schedule_date = datetime.strptime(schedule["date"], "%Y-%m-%d").date()
                is_upcoming = schedule_date >= datetime.now().date()
                
                # 種類の表示名
                type_names = {"practice": "練習試合", "tournament": "公式戦", "training": "練習"}
                type_name = type_names.get(schedule["type"], schedule["type"])
                
                # カードのHTML
                status_class = "status-upcoming" if is_upcoming else "status-completed"
                status_text = "予定" if is_upcoming else "完了"
                type_class = f"schedule-type-{schedule['type']}"
                
                st.markdown(f"""
                <div class="schedule-card">
                    <div class="schedule-date">📅 {schedule['date']} ({schedule.get('time', '未定')})</div>
                    <div class="schedule-event">{schedule['event']}</div>
                    <div class="schedule-details">
                        📍 {schedule['location']} | 
                        <span class="{type_class}">{type_name}</span> | 
                        <span class="{status_class}">{status_text}</span>
                    </div>
                    {f'<div class="schedule-details" style="margin-top: 8px;">📝 {schedule.get("notes", "")}</div>' if schedule.get("notes") else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # 編集・削除ボタン
                col1, col2, col3 = st.columns([1, 1, 8])
                
                with col1:
                    if st.button("✏️ 編集", key=f"edit_{schedule['id']}", use_container_width=True):
                        st.session_state.editing_schedule = schedule['id']
                
                with col2:
                    if st.button("🗑️ 削除", key=f"delete_{schedule['id']}", use_container_width=True):
                        schedules = [s for s in schedules if s['id'] != schedule['id']]
                        schedule_data["schedules"] = schedules
                        if save_schedule_data(schedule_data):
                            st.success("✅ 予定を削除しました")
                            st.rerun()
                
                # 編集フォーム
                if st.session_state.get('editing_schedule') == schedule['id']:
                    with st.expander("予定を編集", expanded=True):
                        with st.form(f"edit_form_{schedule['id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                edit_event = st.text_input("イベント名", value=schedule['event'])
                                edit_date = st.date_input("日付", value=datetime.strptime(schedule['date'], "%Y-%m-%d"))
                                edit_time = st.time_input("時刻", value=datetime.strptime(schedule.get('time', '15:00'), "%H:%M").time())
                            
                            with col2:
                                edit_type = st.selectbox("種類", ["practice", "tournament", "training"],
                                                        index=["practice", "tournament", "training"].index(schedule['type']),
                                                        format_func=lambda x: {"practice": "練習試合", "tournament": "公式戦", "training": "練習"}[x])
                                edit_location = st.text_input("場所", value=schedule['location'])
                                edit_notes = st.text_area("備考", value=schedule.get('notes', ''))
                            
                            col1, col2, col3 = st.columns([1, 1, 4])
                            
                            with col1:
                                if st.form_submit_button("保存", type="primary", use_container_width=True):
                                    for s in schedules:
                                        if s['id'] == schedule['id']:
                                            s['event'] = edit_event
                                            s['date'] = edit_date.strftime("%Y-%m-%d")
                                            s['location'] = edit_location
                                            s['type'] = edit_type
                                            s['time'] = edit_time.strftime("%H:%M")
                                            s['notes'] = edit_notes
                                            break
                                    
                                    schedule_data["schedules"] = schedules
                                    if save_schedule_data(schedule_data):
                                        st.success("✅ 予定を更新しました")
                                        st.session_state.editing_schedule = None
                                        st.rerun()
                            
                            with col2:
                                if st.form_submit_button("キャンセル", use_container_width=True):
                                    st.session_state.editing_schedule = None
                                    st.rerun()
        else:
            st.info("📭 表示する予定がありません")
    
    with tab2:
        st.markdown("### 📆 月間カレンダー")
        
        # 月選択
        selected_month = st.date_input("表示する月", value=datetime.now().date(), key="calendar_month")
        
        # その月の予定を抽出
        month_schedules = [s for s in schedules 
                          if datetime.strptime(s["date"], "%Y-%m-%d").month == selected_month.month
                          and datetime.strptime(s["date"], "%Y-%m-%d").year == selected_month.year]
        
        if month_schedules:
            # カレンダー表示用のデータフレーム作成
            calendar_data = []
            for schedule in sorted(month_schedules, key=lambda x: x["date"]):
                type_names = {"practice": "練習試合", "tournament": "公式戦", "training": "練習"}
                calendar_data.append({
                    "日付": schedule["date"],
                    "時刻": schedule.get("time", "未定"),
                    "イベント": schedule["event"],
                    "種類": type_names.get(schedule["type"], schedule["type"]),
                    "場所": schedule["location"]
                })
            
            df = pd.DataFrame(calendar_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(f"📭 {selected_month.year}年{selected_month.month}月の予定はありません")
