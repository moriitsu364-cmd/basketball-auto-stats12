"""予定・出欠管理ページ - 統合カレンダー"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json

# データファイルのパス
SCHEDULE_FILE = Path(__file__).parent.parent.parent / "data" / "schedule.json"
ATTENDANCE_FILE = Path(__file__).parent.parent.parent / "data" / "attendance.json"

# チームメンバーリスト
TEAM_MEMBERS = [
    "田中太郎", "佐藤次郎", "鈴木三郎", "高橋四郎", "伊藤五郎",
    "山本六郎", "中村七郎", "小林八郎", "加藤九郎", "吉田十郎",
    "渡辺十一郎", "山田十二郎", "佐々木十三郎", "松本十四郎", "井上十五郎"
]


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


def load_attendance_data():
    """出欠データを読み込み"""
    try:
        ATTENDANCE_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if ATTENDANCE_FILE.exists():
            with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"attendance": {}}
    except Exception as e:
        st.error(f"出欠データの読み込みエラー: {e}")
        return {"attendance": {}}


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


def save_attendance_data(data):
    """出欠データを保存"""
    try:
        ATTENDANCE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"出欠データの保存エラー: {e}")
        return False


def render(db):
    """予定・出欠管理ページをレンダリング"""
    
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
    
    .attendance-summary {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        margin-top: 12px;
        border-left: 3px solid #28a745;
    }
    
    .attendance-absent {
        color: #dc3545;
        font-weight: 600;
    }
    
    .attendance-present {
        color: #28a745;
        font-weight: 600;
    }
    
    .attendance-maybe {
        color: #ffc107;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # データ読み込み
    schedule_data = load_schedule_data()
    schedules = schedule_data.get("schedules", [])
    attendance_data = load_attendance_data()
    attendance_records = attendance_data.get("attendance", {})
    
    # ヘッダー
    st.markdown("## 📅 予定・出欠管理カレンダー")
    st.markdown("チームの予定を確認し、出欠を登録できます")
    
    st.markdown("---")
    
    # タブで表示切り替え
    tab1, tab2, tab3 = st.tabs(["📋 予定一覧・出欠登録", "📊 カレンダー表示", "👥 出欠状況一覧"])
    
    with tab1:
        # 予定を日付順にソート（未来の予定を優先）
        sorted_schedules = sorted(schedules, key=lambda x: x["date"])
        
        # フィルター
        col1, col2 = st.columns(2)
        
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
                schedule_id = str(schedule['id'])
                
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
                
                # 出欠登録フォーム（予定の場合のみ）
                if is_upcoming:
                    with st.expander("✍️ 出欠を登録する", expanded=False):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            member_name = st.selectbox(
                                "名前を選択",
                                options=[""] + TEAM_MEMBERS,
                                key=f"member_select_{schedule_id}"
                            )
                        
                        with col2:
                            attendance_status = st.selectbox(
                                "出欠を選択",
                                options=["出席", "欠席", "未定"],
                                key=f"status_select_{schedule_id}"
                            )
                        
                        with col3:
                            st.write("")
                            st.write("")
                            if st.button("登録", key=f"submit_{schedule_id}", type="primary", use_container_width=True):
                                if member_name:
                                    if schedule_id not in attendance_records:
                                        attendance_records[schedule_id] = {}
                                    
                                    attendance_records[schedule_id][member_name] = attendance_status
                                    attendance_data["attendance"] = attendance_records
                                    
                                    if save_attendance_data(attendance_data):
                                        st.success(f"✅ {member_name}さんの出欠を登録しました")
                                        st.rerun()
                                    else:
                                        st.error("❌ 出欠の保存に失敗しました")
                                else:
                                    st.warning("⚠️ 名前を選択してください")
                
                # 出欠状況サマリー
                if schedule_id in attendance_records and attendance_records[schedule_id]:
                    responses = attendance_records[schedule_id]
                    present = sum(1 for status in responses.values() if status == "出席")
                    absent = sum(1 for status in responses.values() if status == "欠席")
                    maybe = sum(1 for status in responses.values() if status == "未定")
                    
                    absent_members = [name for name, status in responses.items() if status == "欠席"]
                    maybe_members = [name for name, status in responses.items() if status == "未定"]
                    
                    st.markdown(f"""
                    <div class="attendance-summary">
                        <strong>📊 出欠状況:</strong> 
                        <span class="attendance-present">出席 {present}名</span> | 
                        <span class="attendance-absent">欠席 {absent}名</span> | 
                        <span class="attendance-maybe">未定 {maybe}名</span>
                        <br>
                        {f'<span class="attendance-absent">⚠️ 欠席: {", ".join(absent_members)}</span><br>' if absent_members else ''}
                        {f'<span class="attendance-maybe">❓ 未定: {", ".join(maybe_members)}</span>' if maybe_members else ''}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
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
                schedule_id = str(schedule['id'])
                
                # 出欠状況を集計
                absent_count = 0
                if schedule_id in attendance_records:
                    responses = attendance_records[schedule_id]
                    absent_count = sum(1 for status in responses.values() if status == "欠席")
                
                calendar_data.append({
                    "日付": schedule["date"],
                    "時刻": schedule.get("time", "未定"),
                    "イベント": schedule["event"],
                    "種類": type_names.get(schedule["type"], schedule["type"]),
                    "場所": schedule["location"],
                    "欠席者数": absent_count
                })
            
            df = pd.DataFrame(calendar_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info(f"📭 {selected_month.year}年{selected_month.month}月の予定はありません")
    
    with tab3:
        st.markdown("### 👥 全体出欠状況")
        
        # 全メンバーの出欠状況を集計
        member_stats = {}
        for member in TEAM_MEMBERS:
            member_stats[member] = {"出席": 0, "欠席": 0, "未定": 0}
        
        for schedule_id, responses in attendance_records.items():
            for member, status in responses.items():
                if member in member_stats:
                    member_stats[member][status] += 1
        
        # データフレームに変換
        stats_data = []
        for member, stats in member_stats.items():
            total = sum(stats.values())
            if total > 0:
                stats_data.append({
                    "名前": member,
                    "出席": stats["出席"],
                    "欠席": stats["欠席"],
                    "未定": stats["未定"],
                    "回答数": total
                })
        
        if stats_data:
            df_stats = pd.DataFrame(stats_data)
            st.dataframe(df_stats, use_container_width=True, hide_index=True)
        else:
            st.info("📭 まだ出欠登録がありません")
