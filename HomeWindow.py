import streamlit as st
import streamlit_calendar as st_calendar

# セッション状態の初期化
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

if 'energy' not in st.session_state:
    st.session_state.energy = 0

levelup = 10

#アプリケーションのタイトル
st.title('育てて達成！マイペット')

col1, col2 = st.columns(2)  # 2列のコンテナを用意する
with col1:
    #画面左
    st_calendar.calendar()
with col2:
    #画面右
    st.image("MyPet/1.png")

def main_page():
    """メインページ（育成画面）"""
    st.title('育成')
    
    # 他のボタンも追加可能
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('タスク追加'):
            st.session_state.current_page = 'add_tasks'
            st.rerun()  # ページを再読み込み
        
    with col2:
        if st.button('タスク一覧'):
            st.session_state.current_page = 'task_list'
            st.rerun()

    with col3:
        if st.button('エサ箱'):
            st.session_state.current_page = 'feed_box'
            st.rerun()

def feed_box_page():
    """エサ箱ページ"""
    st.title('🍎 エサ箱')
    
    st.write("ペットにあげるエサを選んでください:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('🍎 りんご\n(+1)', use_container_width=True):
            st.success("りんごをあげました！")
            st.session_state.energy += 1
            if st.session_state.energy < levelup:
                st.image("MyPet/0.png")
                st.success(f"レベルアップまで：{levelup - st.session_state.energy}")
            else:
                st.image("MyPet/1.png")
                st.success("レベルアップ！")
    
    with col2:
        if st.button('🥕 にんじん\n(+2)', use_container_width=True):
            st.success("にんじんをあげました！")
            st.session_state.energy += 2
            if st.session_state.energy < levelup:
                st.image("MyPet/0.png")
                st.success(f"レベルアップまで：{levelup - st.session_state.energy}")
            else:
                st.image("MyPet/1.png")
                st.success("レベルアップ！")
    
    with col3:
        if st.button('🍖 肉\n(+3)', use_container_width=True):
            st.success("お肉をあげました！")
            st.session_state.energy += 3
            if st.session_state.energy < levelup:
                st.image("MyPet/0.png")
                st.success(f"レベルアップまで：{levelup - st.session_state.energy}")
            else:
                st.image("MyPet/1.png")
                st.success("レベルアップ！")
    
    if st.session_state.energy > levelup:
        st.session_state.energy = levelup

    st.markdown("---")
    
    # メインページに戻るボタン
    if st.button('← メインに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def task_list_page():
    """ステータスページ"""
    st.title('📊 ペットのステータス')
    
    # ペットの基本情報
    st.subheader("基本情報")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("レベル", "5", "↑1")
        st.metric("体力", "85/100", "↑10")
    with col2:
        st.metric("賢さ", "42", "↑5")
        st.metric("筋力", "38", "↑15")
    
    if st.button('← メインに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def add_tasks_page():
    """ショップページ"""
    st.title('🛒 ショップ')
    
    st.write("アイテムを購入できます:")
    
    items = [
        {"name": "高級エサ", "price": 100, "effect": "全ステータス+20"},
        {"name": "おもちゃ", "price": 50, "effect": "幸福度+30"},
        {"name": "薬", "price": 80, "effect": "体力完全回復"}
    ]
    
    for item in items:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"**{item['name']}** - {item['effect']}")
        with col2:
            st.write(f"{item['price']} コイン")
        with col3:
            st.button(f"購入", key=f"buy_{item['name']}")
    
    if st.button('← メインに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

# ページルーティング
if st.session_state.current_page == 'main':
    main_page()
elif st.session_state.current_page == 'feed_box':
    feed_box_page()
elif st.session_state.current_page == 'add_tasks':
    add_tasks_page()
elif st.session_state.current_page == 'task_list':
    task_list_page()

# プログレスバー
st.subheader("経験値")
st.progress(st.session_state.energy/levelup, f"経験値: {st.session_state.energy}/{levelup}")