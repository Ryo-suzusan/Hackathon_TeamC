import streamlit as st
import streamlit_calendar as st_calendar
import datetime
import uuid
import base64
import streamlit.components.v1 as stc

# セッション状態の初期化
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

if 'energy' not in st.session_state:
    st.session_state.energy = 0

levelup = 20

# ページ設定
st.set_page_config(
    page_title="育てて達成！マイペット",
    page_icon="🐾",
    layout="wide"
)
st.title('育てて達成！マイペット')

# 画像をbase64エンコードしてCSSに埋め込む関数
def get_base64_bg(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 画像のパス
image_path = "MyPet/bg_natural_flower.jpg"
encoded_img = get_base64_bg(image_path)

# 背景スタイルを設定
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)  # 2列のコンテナを用意する
with col1:
    #画面左
    # オプションを指定
    options = {
        'initialView': 'dayGridMonth'
    }
    def write_calendar(event_list):# イベントを表示するカレンダーを作成
        st_calendar.calendar(events = event_list, options = options)

    if "events" not in st.session_state:
        st_calendar.calendar()
    else:
        write_calendar(st.session_state.events)

with col2:
    #画面右
    file_ = open("MyPet/1.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
        )

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

            st.session_state.energy += 1
            if st.session_state.energy < levelup:
                st.image("MyPet/0.png")
                st.success(f"レベルアップまで：{levelup - st.session_state.energy}")
            else:
                st.image("MyPet/1.png")
                st.success("レベルアップ！")
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
        
        if st.button("✅ OK", use_container_width=True, type="primary"):
                    feed_pet(feed_name)
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

    """
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
    """
    
    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def add_tasks_page():
    """タスク追加"""

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

    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def task_list_page():
    """タスク一覧"""
    st.title('📋 タスク一覧')

    #eventsの初期化
    if "events" not in st.session_state:
        st.session_state.events = []

    #for event in st.session_state.events:
        #key=f"text_area_{event['id']}"  # 一意なkeyを使用
        #st.metric(event["title"], event["start"], event["end"])

    for event in st.session_state.events:
        st.markdown(f"""
        <div style="
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        ">
            <strong>{event['title']}</strong><br>
            🕒 {event['start']} 〜 {event['end']}
        </div>
        """, unsafe_allow_html=True)
    
    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def feed_box_page():
    """エサ箱ページ"""

    # セッション状態の初期化
    if 'feed_inventory' not in st.session_state:
        st.session_state.feed_inventory = {
            #あとでHomeWindow.pyに修正
            "魚": {"count": 10, "icon": "🐟", "rank": 1},
            "肉": {"count": 8, "icon": "🍖", "rank": 2},
            "野菜": {"count": 15, "icon": "🥕", "rank": 3},
            "果物": {"count": 12, "icon": "🍎", "rank": 4},
            "特別餌": {"count": 3, "icon": "✨", "rank": 5}
        }

    if 'feeding_log' not in st.session_state:
        st.session_state.feeding_log = []

    if 'confirm_feed' not in st.session_state:
        st.session_state.confirm_feed = None

    #あとでHomeWindow.pyに修正
    def feed_pet(feed_name):
        """ペットに餌を与える処理"""
        if st.session_state.feed_inventory[feed_name]["count"] > 0:
            st.session_state.feed_inventory[feed_name]["count"] -= 1
            rank = st.session_state.feed_inventory[feed_name]["rank"]
            st.session_state.feeding_log.append(f"{feed_name}を与えました！")
            st.success(f"🎉 {feed_name}を与えました！ペットが喜んでいます！")
            st.balloons()

            # 餌のランクに応じてエネルギーを増加
            st.session_state.energy += rank
        
            if st.session_state.energy < levelup:
                st.image("MyPet/0.png")
                st.success(f"レベルアップまで：{levelup - st.session_state.energy}")
            else:
                st.image("MyPet/1.png")
                st.success("レベルアップ！")

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

    # 確認ダイアログ(あとでHomeWindow.pyに修正)
    if st.session_state.confirm_feed:
        feed_name = st.session_state.confirm_feed
        feed_icon = st.session_state.feed_inventory[feed_name]["icon"]
    
        st.markdown("---")
        st.subheader("🤔 確認")
    
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<div style='text-align: center; font-size: 2em;'>{feed_icon}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 1.2em;'>この<strong>{feed_name}</strong>をあげますか？</div>", unsafe_allow_html=True)
        
            col_ok, col_cancel = st.columns(2)
            with col_ok:
                if st.button("✅ OK", use_container_width=True, type="primary"):
                    feed_pet(feed_name)
                    # 3秒後に更新
                    import time
                    time.sleep(3)
                    st.rerun()
            with col_cancel:
                if st.button("❌ キャンセル", use_container_width=True):
                    st.session_state.confirm_feed = None
                    # 3秒後に更新
                    import time
                    time.sleep(3)
                    st.rerun()

    # 餌やり履歴
    if st.session_state.feeding_log:
        st.markdown("---")
        st.subheader("📋 餌やり履歴")
    
        # 最新の5件を表示
        recent_logs = st.session_state.feeding_log[-5:]
        for i, log in enumerate(reversed(recent_logs)):
            st.write(f"{len(recent_logs) - i}. {log}")

    """
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
    """
    
    if st.button('← メニューに戻る'):
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
st.subheader("エネルギー")
st.progress(st.session_state.energy / levelup)
st.write(f"レベルアップまで: {st.session_state.energy}/{levelup}")