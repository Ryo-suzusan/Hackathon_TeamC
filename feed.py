import streamlit as st

# ページ設定
st.set_page_config(
    page_title="餌やりシステム",
    page_icon="🐾",
    layout="wide"
)

# セッション状態の初期化
if 'feed_inventory' not in st.session_state:
    st.session_state.feed_inventory = {
        "魚": {"count": 10, "icon": "🐟"},
        "肉": {"count": 8, "icon": "🍖"},
        "野菜": {"count": 15, "icon": "🥕"},
        "果物": {"count": 12, "icon": "🍎"},
        "特別餌": {"count": 3, "icon": "✨"}
    }

if 'feeding_log' not in st.session_state:
    st.session_state.feeding_log = []

if 'confirm_feed' not in st.session_state:
    st.session_state.confirm_feed = None

def feed_pet(feed_name):
    """ペットに餌を与える処理"""
    if st.session_state.feed_inventory[feed_name]["count"] > 0:
        st.session_state.feed_inventory[feed_name]["count"] -= 1
        st.session_state.feeding_log.append(f"{feed_name}を与えました！")
        st.success(f"🎉 {feed_name}を与えました！ペットが喜んでいます！")
        st.balloons()
    else:
        st.error(f"❌ {feed_name}の在庫がありません")
    st.session_state.confirm_feed = None

def show_confirmation_dialog(feed_name):
    """確認ダイアログを表示"""
    st.session_state.confirm_feed = feed_name

# メインタイトル
st.title("🐾 餌やりコーナー")
st.markdown("---")

# 餌の在庫表示と餌やりボタン
st.subheader("🍽️ 餌の在庫")

# 餌を横並びで表示
cols = st.columns(len(st.session_state.feed_inventory))

for i, (feed_name, feed_data) in enumerate(st.session_state.feed_inventory.items()):
    with cols[i]:
        # 餌のアイコンと名前
        st.markdown(f"<div style='text-align: center; font-size: 3em;'>{feed_data['icon']}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-weight: bold;'>{feed_name}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; color: #666;'>在庫: {feed_data['count']}個</div>", 
                   unsafe_allow_html=True)
        
        # 餌やりボタン（在庫がある場合のみ有効）
        if st.button(
            f"{feed_data['icon']} 与える", 
            key=f"feed_{feed_name}",
            disabled=feed_data['count'] == 0,
            use_container_width=True
        ):
            show_confirmation_dialog(feed_name)

# 確認ダイアログ
if st.session_state.confirm_feed:
    feed_name = st.session_state.confirm_feed
    feed_icon = st.session_state.feed_inventory[feed_name]["icon"]
    
    st.markdown("---")
    st.subheader("🤔 確認")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div style='text-align: center; font-size: 2em;'>{feed_icon}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; font-size: 1.2em;'>この<strong>{feed_name}</strong>をあげますか？</div>", 
                   unsafe_allow_html=True)
        
        col_ok, col_cancel = st.columns(2)
        with col_ok:
            if st.button("✅ OK", use_container_width=True, type="primary"):
                feed_pet(feed_name)
        with col_cancel:
            if st.button("❌ キャンセル", use_container_width=True):
                st.session_state.confirm_feed = None

# 餌やり履歴
if st.session_state.feeding_log:
    st.markdown("---")
    st.subheader("📋 餌やり履歴")
    
    # 最新の5件を表示
    recent_logs = st.session_state.feeding_log[-5:]
    for i, log in enumerate(reversed(recent_logs)):
        st.write(f"{len(recent_logs) - i}. {log}")

# サイドバーに統計情報
with st.sidebar:
    st.header("📊 統計")
    
    # 総在庫数
    total_inventory = sum(feed_data["count"] for feed_data in st.session_state.feed_inventory.values())
    st.metric("総在庫数", f"{total_inventory}個")
    
    # 餌やり回数
    total_feedings = len(st.session_state.feeding_log)
    st.metric("餌やり回数", f"{total_feedings}回")
    
    st.markdown("---")
    st.subheader("🔧 管理")
    
    # 在庫補充ボタン
    if st.button("📦 在庫補充", use_container_width=True):
        for feed_name in st.session_state.feed_inventory:
            st.session_state.feed_inventory[feed_name]["count"] += 5
        st.success("在庫を補充しました！")
        st.rerun()
    
    # リセットボタン
    if st.button("🔄 データリセット", use_container_width=True, type="secondary"):
        st.session_state.feed_inventory = {
            "魚": {"count": 10, "icon": "🐟"},
            "肉": {"count": 8, "icon": "🍖"},
            "野菜": {"count": 15, "icon": "🥕"},
            "果物": {"count": 12, "icon": "🍎"},
            "特別餌": {"count": 3, "icon": "✨"}
        }
        st.session_state.feeding_log = []
        st.session_state.confirm_feed = None
        st.success("データをリセットしました！")
        st.rerun()

# フッター
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>🐾 タスク管理＆育成ゲーム - 餌やりシステム 🐾</div>", 
           unsafe_allow_html=True)