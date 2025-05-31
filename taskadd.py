import streamlit as st
from my_calendar import write_calendar

st.title("カレンダー＋イベント登録")

# セッションにイベントリストがなければ初期化
if "events" not in st.session_state:
    st.session_state.events = []

# 2カラムでレイアウト（左: カレンダー、右: フォーム）
col1, col2 = st.columns([2, 1])

# 左：カレンダーを表示
with col1:
    write_calendar(st.session_state.events)

# 右：イベント入力フォーム
with col2:
    st.subheader("イベント追加")

    title = st.text_input("イベント名")
    start_time = st.time_input("開始時刻")
    end_time = st.time_input("終了時刻")

    if st.button("追加"):
        if title.strip() and start_time < end_time:
            st.session_state.events.append({
                "title": title.strip(),
                "start": start_time.strftime("%H:%M"),
                "end": end_time.strftime("%H:%M")
            })
            st.success("イベントを追加しました！")
        else:
            st.error("正しいイベント名と時刻を入力してください。")