import streamlit as st

# セッション状態の初期化
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

def main_page():
    """メインページ（育成画面）"""
    st.title('育成')
    
    if st.button('エサ箱'):
        st.session_state.current_page = 'feed_box'
        st.rerun()  # ページを再読み込み
    
    # 他のボタンも追加可能
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('ステータス'):
            st.session_state.current_page = 'status'
            st.rerun()
    with col2:
        if st.button('ショップ'):
            st.session_state.current_page = 'shop'
            st.rerun()
    with col3:
        if st.button('ミニゲーム'):
            st.session_state.current_page = 'minigame'
            st.rerun()

def feed_box_page():
    """エサ箱ページ"""
    st.title('🍎 エサ箱')
    
    st.write("ペットにあげるエサを選んでください:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('🍎 りんご\n(体力+10)', use_container_width=True):
            st.success("りんごをあげました！体力が10回復しました。")
    
    with col2:
        if st.button('🥕 にんじん\n(賢さ+5)', use_container_width=True):
            st.success("にんじんをあげました！賢さが5上がりました。")
    
    with col3:
        if st.button('🍖 肉\n(筋力+15)', use_container_width=True):
            st.success("お肉をあげました！筋力が15上がりました。")
    
    st.markdown("---")
    
    # メインページに戻るボタン
    if st.button('← メインに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def status_page():
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
    
    # プログレスバー
    st.subheader("経験値")
    st.progress(0.7, "経験値: 70/100")
    
    if st.button('← メインに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def shop_page():
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

def minigame_page():
    """ミニゲームページ"""
    st.title('🎮 ミニゲーム')
    
    st.write("ミニゲームで経験値を稼ごう！")
    
    game_choice = st.selectbox(
        "ゲームを選んでください:",
        ["じゃんけん", "数当てゲーム", "記憶ゲーム"]
    )
    
    if game_choice == "じゃんけん":
        st.subheader("🪨📄✂️ じゃんけんゲーム")
        choice = st.selectbox("あなたの選択:", ["グー", "チョキ", "パー"])
        if st.button("じゃんけんぽん！"):
            import random
            computer_choice = random.choice(["グー", "チョキ", "パー"])
            st.write(f"コンピューター: {computer_choice}")
            # 勝敗判定ロジックをここに追加
    
    if st.button('← メインに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

# ページルーティング
if st.session_state.current_page == 'main':
    main_page()
elif st.session_state.current_page == 'feed_box':
    feed_box_page()
elif st.session_state.current_page == 'status':
    status_page()
elif st.session_state.current_page == 'shop':
    shop_page()
elif st.session_state.current_page == 'minigame':
    minigame_page()