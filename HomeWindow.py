import streamlit as st
import streamlit_calendar as st_calendar

#投稿内容を保存するリストを作成
if 'posts' not in st.session_state:
    st.session_state.posts = []

#アプリケーションのタイトル
st.title('育てて達成！マイペット')

#画面左

#投稿ボタンを押すと
if st.button('投稿する'):
    if post_content: #投稿内容が空でないなら 
        st.success('投稿が完了しました！') #投稿完了の通知
        st.session_state.posts.append(post_content) #リストに保存
    else: #投稿内容が空の場合
        st.warning('なにも書いてないよ') #アラートを表示

#投稿内容を表示
for post in st.session_state.posts:
    st.text_area('投稿内容', post)