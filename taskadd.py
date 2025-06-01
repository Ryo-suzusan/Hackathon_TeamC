import streamlit as st
import datetime
import uuid

# ✅ 指定日のイベントだけ抽出
def get_events_for_date(events, target_date):
    daily_events = []
    for event in events:
        event_date = datetime.datetime.fromisoformat(event['end']).date()
        if event_date == target_date:
            daily_events.append(event)
    return daily_events

# ✅ 時刻フォーマット
def format_time(datetime_str):
    dt = datetime.datetime.fromisoformat(datetime_str)
    return dt.strftime("%H:%M")

# ✅ 初期化（セッション）
if "events" not in st.session_state:
    st.session_state.events = []

if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.date.today()

# 左半分にレイアウト
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("📝 イベント追加")

    # 選択中の日付をデフォルトに
    event_date = st.date_input("日付", st.session_state.selected_date, key="event_date_input")
    # 日付が変更されたら選択日付も更新
    if event_date != st.session_state.selected_date:
        st.session_state.selected_date = event_date
        st.rerun()
    
    title = st.text_input("イベント名")
    end_time = st.time_input("終了時刻")

    if st.button("➕ 追加"):
        if title.strip():
            end_datetime = datetime.datetime.combine(event_date, end_time)
            
            new_event = {
                "id": str(uuid.uuid4()),
                "title": title.strip(),
                "end": end_datetime.isoformat(),
            }
            
            st.session_state.events.append(new_event)
            st.success("✅ イベントを追加しました！")
            st.rerun()
        else:
            st.error("❌ 正しいイベント名を入力してください。")

    st.subheader(f"📅 {st.session_state.selected_date.strftime('%Y年%m月%d日')} の予定")

    daily_events = get_events_for_date(st.session_state.events, st.session_state.selected_date)

    if daily_events:
        for event in daily_events:
            end_time = format_time(event['end'])
            
            with st.container():
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 12px;
                    margin-bottom: 20px;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
                ">
                    <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
                        {event['title']}
                    </div>
                    <div style="font-size: 16px; opacity: 0.9;">
                        🕐 {end_time}まで
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("この日に予定はありません。")