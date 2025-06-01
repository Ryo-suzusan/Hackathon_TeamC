import streamlit as st
import streamlit_calendar as st_calendar
import datetime
import uuid
import base64
import streamlit.components.v1 as stc
from pathlib import Path


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

def get_base64_image(image_path):
    """画像をbase64エンコードする関数"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"画像ファイルが見つかりません: {image_path}")
        return None

# 画像のパス
image_path = "MyPet/bg_natural_flower.jpg"
encoded_img = get_base64_bg(image_path)

def create_compact_image_button(image_path, button_text, button_key, width=120, height=120):
    """コンパクトな画像ボタン（画像の下にボタン）"""
    
    img_base64 = get_base64_image(image_path)
    if img_base64 is None:
        return False
    
    # 画像形式を判定
    img_format = 'png' if image_path.lower().endswith('.png') else 'jpeg'
    
    # 中央配置のコンテナ
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 10px;">
        <img src="data:image/{img_format};base64,{img_base64}" 
             width="{width}" height="{height}" 
             style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
                    transition: transform 0.2s;"
             onmouseover="this.style.transform='scale(1.05)'"
             onmouseout="this.style.transform='scale(1)'">
    </div>
    """, unsafe_allow_html=True)
    
    # ボタンを中央配置（調整版）
    st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return st.button(button_text, key=button_key, type="primary")

def create_enhanced_image_button(image_path, button_text, button_key, width=120, height=120, fallback_emoji="📱"):
    """画像ボタン（画像が見つからない場合は絵文字を表示）"""
    
    img_base64 = get_base64_image(image_path)
    
    if img_base64 is not None:
        # 画像形式を判定
        img_format = 'png' if image_path.lower().endswith('.png') else 'jpeg'
        
        # 画像を表示
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px;">
            <img src="data:image/{img_format};base64,{img_base64}" 
                 width="{width}" height="{height}" 
                 style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
                        transition: transform 0.2s;"
                 onmouseover="this.style.transform='scale(1.05)'"
                 onmouseout="this.style.transform='scale(1)'">
        </div>
        """, unsafe_allow_html=True)
    else:
        # 画像が見つからない場合は絵文字を表示
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px;">
            <div style="width: {width}px; height: {height}px; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 10px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        font-size: 48px;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        transition: transform 0.2s;
                        margin: 0 auto;"
                 onmouseover="this.style.transform='scale(1.05)'"
                 onmouseout="this.style.transform='scale(1)'">{fallback_emoji}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ボタンを中央配置
    st.markdown("""
    <style>
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)
    
    return st.button(button_text, key=button_key, type="primary")

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
    
    # 新しい多様な画像ボタンレイアウト
    st.subheader("🎮 アクションメニュー")
    
    # 第1行：メイン機能
    col1, col2, col3 = st.columns(3)
    with col1:
        if create_enhanced_image_button("MyPet/task_add.png", "タスク追加", "add_task_btn", width=120, height=120, fallback_emoji="➕"):
            st.session_state.current_page = 'add_tasks'
            st.rerun()
        
    with col2:
        if create_enhanced_image_button("MyPet/book.png", "タスク一覧", "task_list_btn", width=120, height=120, fallback_emoji="📋"):
            st.session_state.current_page = 'task_list'
            st.rerun()

    with col3:
        if create_enhanced_image_button("MyPet/esa_button.png", "エサ箱", "feed_box_btn", width=120, height=120, fallback_emoji="🍖"):
            st.session_state.current_page = 'feed_box'
            st.rerun()
    
    # 第2行：追加機能
    st.subheader("🔧 その他の機能")
    col5, col6 = st.columns(2)
    
    with col5:
        if create_enhanced_image_button("MyPet/tokei.png", "統計", "stats_btn", width=120, height=120, fallback_emoji="📊"):
            st.session_state.current_page = 'statistics'
            st.rerun()
    
    with col6:
        if create_enhanced_image_button("MyPet/help.png", "ヘルプ", "help_btn", width=120, height=120, fallback_emoji="❓"):
            st.session_state.current_page = 'help'
            st.rerun()

def statistics_page():
    """統計ページ"""
    st.title("📊 統計")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎮 ゲーム統計")
        st.metric("現在のエネルギー", st.session_state.energy)
        progress_percentage = (st.session_state.energy / levelup) * 100
        st.metric("レベル進捗", f"{progress_percentage:.1f}%")
        
        # タスク統計
        if 'events' in st.session_state:
            total_tasks = len(st.session_state.events)
            st.metric("総タスク数", total_tasks)
        
    with col2:
        st.subheader("🍽️ 餌やり統計")
        if 'feeding_log' in st.session_state:
            total_feedings = len(st.session_state.feeding_log)
            st.metric("総餌やり回数", total_feedings)
        
        if 'feed_inventory' in st.session_state:
            total_inventory = sum(feed_data["count"] for feed_data in st.session_state.feed_inventory.values())
            st.metric("総在庫数", f"{total_inventory}個")
    
    # 最近の活動
    st.subheader("📈 最近の活動")
    if 'feeding_log' in st.session_state and st.session_state.feeding_log:
        st.write("最近の餌やり:")
        for log in st.session_state.feeding_log[-3:]:
            st.write(f"• {log}")
    else:
        st.info("まだ餌やりの記録がありません")
    
    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def help_page():
    """ヘルプページ"""
    st.title("❓ ヘルプ")
    st.markdown("---")
    
    st.subheader("🐾 育てて達成！マイペットについて")
    st.write("""
    このアプリは、タスク管理とペット育成を組み合わせた楽しいアプリです！
    タスクを完了したり、ペットに餌をあげたりしてペットを育てましょう。
    """)
    
    st.subheader("📖 使い方")
    
    with st.expander("📝 タスク管理"):
        st.write("""
        **タスク追加**: 新しいタスクを追加できます
        - 日付と時刻を指定してタスクを登録
        - カレンダーでタスクの確認が可能
        
        **タスク一覧**: 登録済みのタスクを一覧表示
        - すべてのタスクを時系列で確認
        """)
    
    with st.expander("🍖 ペット育成"):
        st.write("""
        **エサ箱**: ペットに餌をあげてエネルギーを増やそう
        - 5種類の餌から選択可能
        - 餌をあげるとエネルギーが1増加
        - エネルギーが一定値に達するとレベルアップ！
        """)
    
    with st.expander("📊 統計機能"):
        st.write("""
        **統計**: ゲームの進捗状況を確認
        - 現在のエネルギーとレベル進捗
        - タスクと餌やりの統計
        - 最近の活動履歴
        """)
    
    with st.expander("⚙️ 設定"):
        st.write("""
        **設定**: ゲームの各種設定を変更
        - レベルアップ必要エネルギーの調整
        - データのリセット機能
        """)
    
    st.subheader("💡 ヒント")
    st.info("""
    - 定期的にタスクを追加して、計画的に進めましょう
    - ペットの餌やりを忘れずに！エネルギーがたまるとレベルアップします
    - 統計画面で進捗を確認して、モチベーションを保ちましょう
    """)
    
    if st.button('← メニューに戻る'):
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
                end_datetime = datetime.datetime.combine(event_date, end_time)
                
                new_event = {
                    "id": str(uuid.uuid4()),
                    "title": title.strip(),
                    "end": end_datetime.isoformat(),
                }
                
                st.session_state.events.append(new_event)
                st.success("✅ タスクを追加しました！")
                st.rerun()
            else:
                st.error("❌ 正しいタスク名を入力してください。")

        st.subheader(f"📅 {st.session_state.selected_date.strftime('%Y年%m月%d日')} が期限のタスク")

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
            st.info("この日が期限のタスクはありません。")

    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def task_list_page():
    """タスク一覧"""
    st.title('📋 タスク一覧')

    #eventsの初期化
    if "events" not in st.session_state:
        st.session_state.events = []

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
            🕒 {event.get('start', '未設定')} 〜 {event['end']}
        </div>
        """, unsafe_allow_html=True)
    
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
elif st.session_state.current_page == 'settings':
    settings_page()
elif st.session_state.current_page == 'statistics':
    statistics_page()
elif st.session_state.current_page == 'help':
    help_page()

# プログレスバー
st.subheader("エネルギー")
st.progress(st.session_state.energy / levelup)
st.write(f"レベルアップまで: {st.session_state.energy}/{levelup}")