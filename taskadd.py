import streamlit as st
import datetime
import uuid

import streamlit as st
import streamlit_calendar as st_calendar

# オプションを指定
options = {
    'initialView': 'dayGridMonth'
}
def write_calendar(event_list):# イベントを表示するカレンダーを作成
    st_calendar.calendar(events = event_list, options = options)

st.title("タスク登録")

if "events" not in st.session_state:
    st.session_state.events = []

# ✅ カレンダーを全幅表示
st.subheader("カレンダー")
write_calendar(st.session_state.events)

# ✅ イベント入力フォームを下に配置
st.subheader("イベント追加")
event_date = st.date_input("日付", datetime.date.today())
title = st.text_input("イベント名")
start_time = st.time_input("開始時刻")
end_time = st.time_input("終了時刻")

if st.button("追加"):
    if title.strip() and start_time < end_time:
        start_datetime = datetime.datetime.combine(event_date, start_time)
        end_datetime = datetime.datetime.combine(event_date, end_time)

        new_event = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "start": start_datetime.isoformat(),
            "end": end_datetime.isoformat(),

        }
        st.session_state.events.append(new_event)
        st.success("イベントを追加しました！")
        st.rerun()
    else:
        st.error("正しいイベント名と時刻を入力してください。")
