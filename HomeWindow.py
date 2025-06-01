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
    'initialView': 'dayGridMonth',
    'headerToolbar': {
        'left': 'today prev,next',
        'center': 'title',
        'right': 'dayGridMonth,timeGridWeek,listWeek',
    },
    'titleFormat': {
            'year': 'numeric', 'month': '2-digit', 'day': '2-digit'
        },
        'buttonText': {
            'today': '今日',
            'month': '月ごと',
            'week': '週ごと',
            'day': '日ごと',
            'list': 'リスト'
        },
        'locale': 'ja', # 日本語化する
        'firstDay': '1', # 週の最初を月曜日(1)にする。デフォルトは日曜日(0)
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
    
    # 確認画面の状態管理
    if "show_confirmation" not in st.session_state:
        st.session_state.show_confirmation = False
    
    if "temp_task" not in st.session_state:
        st.session_state.temp_task = {}

    # 通常のタスク追加画面のレイアウト
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # 確認画面が表示されている場合
        if st.session_state.show_confirmation:
            st.subheader("🔍 タスク追加の確認")
            
            # 確認画面のスタイル
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: #333;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                border: 2px solid #ff9a9e;
            ">
                <h3 style="margin-top: 0; color: #d63384;">📝 以下の内容で追加しますか？</h3>
                <div style="font-size: 18px; margin: 15px 0;">
                    <strong>📅 日付:</strong> {st.session_state.temp_task['date_str']}
                </div>
                <div style="font-size: 18px; margin: 15px 0;">
                    <strong>📋 タスク名:</strong> {st.session_state.temp_task['title']}
                </div>
                <div style="font-size: 18px; margin: 15px 0;">
                    <strong>🕐 終了時刻:</strong> {st.session_state.temp_task['end_time_str']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 確認とキャンセルボタン
            conf_col1, conf_col2 = st.columns(2)
            
            with conf_col1:
                if st.button("✅ 確認・追加", type="primary", use_container_width=True):
                    # タスクを実際に追加
                    start_datetime = datetime.datetime.now()
                    new_event = {
                        "id": str(uuid.uuid4()),
                        "title": st.session_state.temp_task['title'],
                        "start": start_datetime.isoformat(),
                        "end": st.session_state.temp_task['end_datetime'].isoformat(),
                    }
                    
                    st.session_state.events.append(new_event)
                    st.success("✅ タスクを追加しました！")
                    
                    # 確認画面を閉じる
                    st.session_state.show_confirmation = False
                    st.session_state.temp_task = {}
                    st.rerun()
            
            with conf_col2:
                if st.button("❌ キャンセル", use_container_width=True):
                    # 確認画面を閉じる
                    st.session_state.show_confirmation = False
                    st.session_state.temp_task = {}
                    st.rerun()
        
        else:
            # 通常のタスク追加フォーム
            st.subheader("📝 タスク追加")

            # 選択中の日付をデフォルトに
            event_date = st.date_input("日付", st.session_state.selected_date, key="event_date_input")
            # 日付が変更されたら選択日付も更新
            if event_date != st.session_state.selected_date:
                st.session_state.selected_date = event_date
                st.rerun()
            
            title = st.text_input("タスク名")
            end_time = st.time_input("終了時刻")

            if st.button("➕ 追加"):
                if title.strip():
                    # 確認画面用の一時データを保存
                    end_datetime = datetime.datetime.combine(event_date, end_time)
                    
                    st.session_state.temp_task = {
                        "title": title.strip(),
                        "date_str": event_date.strftime('%Y年%m月%d日'),
                        "end_time_str": end_time.strftime('%H:%M'),
                        "end_datetime": end_datetime
                    }
                    
                    # 確認画面を表示
                    st.session_state.show_confirmation = True
                    st.rerun()
                else:
                    st.error("❌ 正しいタスク名を入力してください。")

        # タスク一覧表示（確認画面でも通常画面でも表示）
        st.subheader(f"📅 {st.session_state.selected_date.strftime('%Y年%m月%d日')} が期限のタスク")

        daily_events = get_events_for_date(st.session_state.events, st.session_state.selected_date)

        if daily_events:
            for event in daily_events:
                end_time_display = format_time(event['end'])
                
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
                            🕐 {end_time_display}まで
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("この日が期限のタスクはありません。")

    # 右側のカラムは空のまま（必要に応じて他のコンテンツを追加可能）
    with right_col:
        st.empty()  # 右側は空にしておく

    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def task_list_page():
    """タスク一覧"""
    st.title('📋 タスク一覧')

    # 完了メッセージの表示（ページ上部）
    if "done_message" in st.session_state:
        st.success(st.session_state.done_message)

    #eventsの初期化
    if "events" not in st.session_state:
        st.session_state.events = []

    #for event in st.session_state.events:
        #key=f"text_area_{event['id']}"  # 一意なkeyを使用
        #st.metric(event["title"], event["start"], event["end"])

    if not st.session_state.events:
        st.info("タスクがありません")
    else:
        for i, event in enumerate(st.session_state.events):
            col1, col2, col3 = st.columns([6, 1, 1])  # タイトル + 編集 + 完了

            with col1:
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

            with col2:
                if st.button("✏️", key=f"edit_{event['id']}"):
                    # 編集処理
                    st.session_state.edit_index = i  # 例: 編集対象を保存
                    st.rerun()

            with col3:  
                if st.button("✅", key=f"done_{event['id']}"):
                    st.session_state.events.pop(i)
                    st.session_state.done_message = f"✅「{event['title']}」を完了しました！お疲れ様！"
                    st.rerun()

                
    if st.button('← メニューに戻る'):
        if "done_message" in st.session_state:
            del st.session_state["done_message"]

        st.session_state.current_page = 'main'
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