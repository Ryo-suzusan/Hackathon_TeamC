import streamlit as st
import streamlit_calendar as st_calendar

def write_calendar(event_list) {# イベントを表示するカレンダーを作成
    cal = st_calendar.calendar(events=event_list)
    st.write(cal)
}

