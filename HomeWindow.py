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

if 'level' not in st.session_state:
    st.session_state.level = 0

levelup = [20, 30, 40, 50]

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
    # プログレスバー
    st.subheader(f"Lv.{st.session_state.level + 1}")
    if st.session_state.level != 3:
        st.progress(st.session_state.energy / levelup[st.session_state.level + 1])
        st.write(f"レベルアップまで: {levelup[st.session_state.level] - st.session_state.energy}/{levelup[st.session_state.level]}")
    else:
        st.progress(1 / 1)
        st.write(f"レベルMAX")
        
    file_ = open(f"MyPet/Idle{st.session_state.level}.gif", "rb")
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
    button_path = "MyPet/esa_button.png"
    
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
    # メインタイトルとメニューに戻るボタンを横並びで配置
    title_col, button_col = st.columns([6, 1])
    with title_col:
        st.title("📊 統計")
    with button_col:
        st.write("")
        st.write("")
        if st.button('← メニューに戻る', key="back_to_menu_top"):
            st.session_state.current_page = 'main'
            st.rerun()
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎮 ゲーム統計")
        st.metric("現在のLevel", st.session_state.level+1)
        st.metric("現在のエネルギー", st.session_state.energy)
        if st.session_state.level != 3:
            progress_percentage = (st.session_state.energy / levelup[st.session_state.level]) * 100
            st.metric("次のレベルまでの進捗", f"{progress_percentage:.1f}%")
        
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


def help_page():
    """ヘルプページ"""
    st.title("❓ ヘルプ")
    st.markdown("---")
    
    st.subheader("🐾 「育てて達成！マイペット」とは？")
    st.write("""
    タスク管理とペット育成を組み合わせた楽しいブラウザアプリです！
    タスクを完了してエサをゲットし、ペットを育ててあげましょう。
    """)
    
    st.subheader("📖 使い方")
    
    with st.expander("📝 タスク管理"):
        st.write("""
        **タスク追加**: 新しいタスクを追加できます
        - 締め切りの日付と時刻を指定してタスクを登録
        - カレンダーでタスクの確認が可能
        
        **タスク一覧**: 登録済みのタスクを一覧表示
        - すべてのタスクを時系列で確認
        - 達成を選択することで、エサがゲットできる
        - タスクを早く終わらせるほど、ランクの高いエサを得られる
        """)
    
    with st.expander("🍖 ペット育成"):
        st.write("""
        **エサ箱**: ペットに餌をあげてエネルギーを増やそう
        - 4種類の餌から選択可能
        - 餌をあげるとエネルギーが溜まる
        - エネルギーが一定値に達するとレベルアップ！
        """)
    
    with st.expander("📊 統計機能"):
        st.write("""
        **統計**: ゲームの進捗状況を確認
        - 現在のエネルギーとレベル進捗
        - タスクと餌やりの統計
        - 最近の活動履歴
        """)
    
    if st.button('← メニューに戻る'):
        st.session_state.current_page = 'main'
        st.rerun()

def feed_box_page():
    """エサ箱ページ"""

    # セッション状態の初期化
    if 'feed_inventory' not in st.session_state:
        st.session_state.feed_inventory = {
            #あとでHomeWindow.pyに修正
            "野菜": {"count": 15, "icon": "🥕", "rank": 1},
            "果物": {"count": 12, "icon": "🍎", "rank": 2},
            "肉": {"count": 8, "icon": "🍖", "rank": 5},
            "特上肉": {"count": 3, "icon": "🥩", "rank": 10}
        }

    if 'feeding_log' not in st.session_state:
        st.session_state.feeding_log = []

    if 'confirm_feed' not in st.session_state:
        st.session_state.confirm_feed = None

    if 'show_feed_result' not in st.session_state:
        st.session_state.show_feed_result = False

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
        
            if st.session_state.energy < levelup[st.session_state.level]:
                if st.session_state.level != 3:
                    st.success(f"レベルアップまで：{levelup[st.session_state.level] - st.session_state.energy}")
            else:
                st.session_state.energy -= levelup[st.session_state.level]
                st.session_state.level += 1
                st.success(f"レベルアップ！レベルが{st.session_state.level + 1}になった！")
            
            file_ = open(f"MyPet/Walk{st.session_state.level}.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()

            st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
            unsafe_allow_html=True,
            )

    def show_confirmation_dialog(feed_name):
        """確認ダイアログを表示"""
        st.session_state.confirm_feed = feed_name

    # メインタイトルとメニューに戻るボタンを横並びで配置
    title_col, button_col = st.columns([6, 1])
    with title_col:
        st.title("🐾 餌やりコーナー")
    with button_col:
        st.write("")
        st.write("")
        if st.button('← メニューに戻る', key="back_to_menu_top"):
            st.session_state.current_page = 'main'
            st.rerun()
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
            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{feed_name}(+{feed_data['rank']})</div>", 
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
                    #下2行HomeWindow.pyに追加
                    st.session_state.confirm_feed = None
                    st.session_state.show_feed_result = False
                    st.rerun()
            with col_cancel:
                if st.button("❌ キャンセル", use_container_width=True):
                    st.session_state.confirm_feed = None
                    st.rerun()

    # 餌やり履歴
    if st.session_state.feeding_log:
        st.markdown("---")
        st.subheader("📋 餌やり履歴")
    
        # 最新の5件を表示
        recent_logs = st.session_state.feeding_log[-5:]
        for i, log in enumerate(reversed(recent_logs)):
            st.write(f"{len(recent_logs) - i}. {log}")
    

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
            # サブヘッダーとボタンを横並びで配置
            header_col, btn_col = st.columns([2.4, 1])
            with header_col:
                st.subheader("📝 タスク追加")
            with btn_col:
                st.write("")
                if st.button('← メニューに戻る'):
                    st.session_state.current_page = 'main'
                    st.rerun()

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


def change_task_page():
    """タスク編集"""
    # 左半分にコンテンツを表示
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title('✏️ タスク編集')
        
        if "edit_index" not in st.session_state or st.session_state.edit_index is None:
            st.error("編集するタスクが選択されていません")
            if st.button('← 一覧に戻る'):
                st.session_state.current_page = 'task_list'
                st.rerun()
            return
        
        # 編集対象のタスクを取得
        edit_event = st.session_state.events[st.session_state.edit_index]
        
        # 編集フォーム
        title = st.text_input("タスク名", value=edit_event['title'])
        # 既存の終了時刻から日付と時刻を分離
        end_datetime = datetime.datetime.fromisoformat(edit_event['end'])
        
        event_date = st.date_input("日付", value=end_datetime.date())
        end_time = st.time_input("終了時刻", value=end_datetime.time())
        
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button("💾 保存"):
                if title.strip():
                    # タスクを更新
                    updated_event = {
                        "id": edit_event['id'],
                        "title": title.strip(),
                        "start": edit_event['start'],
                        "end": datetime.datetime.combine(event_date, end_time).isoformat(),
                    }
                    
                    st.session_state.events[st.session_state.edit_index] = updated_event
                    st.success("✅ タスクを更新しました！")
                    
                    # 編集状態をクリア
                    st.session_state.edit_index = None
                    st.session_state.current_page = 'task_list'
                    st.rerun()
                else:
                    st.error("❌ 正しいタスク名を入力してください。")
        
        with button_col2:
            if st.button("❌ キャンセル"):
                st.session_state.edit_index = None
                st.session_state.current_page = 'task_list'
                st.rerun()
    
    with col2:
        # 右半分は空にするか、必要に応じて他のコンテンツを配置
        st.empty()

def delete_task_page():
    """タスク削除確認"""
    # 左半分にコンテンツを表示
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.title('🗑️ タスク削除')
        
        if "edit_index" not in st.session_state or st.session_state.edit_index is None:
            st.error("削除するタスクが選択されていません")
            if st.button('← 一覧に戻る'):
                st.session_state.current_page = 'task_list'
                st.rerun()
            return
        
        # 削除対象のタスクを取得
        delete_event = st.session_state.events[st.session_state.edit_index]
        
        # 終了時刻から日付と時刻を分離
        end_datetime = datetime.datetime.fromisoformat(delete_event['end'])
        date_str = end_datetime.strftime('%Y年%m月%d日')
        time_str = end_datetime.strftime('%H:%M')
        
        # 確認画面のスタイル
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            border: 2px solid #ff6b6b;
            text-align: center;
        ">
            <h2 style="margin-top: 0; color: white;">⚠️ このタスクを削除しますか？</h2>
            <div style="background: rgba(255, 255, 255, 0.2); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <div style="font-size: 20px; margin: 15px 0;">
                    <strong>📅 日付:</strong> {date_str}
                </div>
                <div style="font-size: 20px; margin: 15px 0;">
                    <strong>📋 タスク名:</strong> {delete_event['title']}
                </div>
                <div style="font-size: 20px; margin: 15px 0;">
                    <strong>🕐 終了時刻:</strong> {time_str}
                </div>
            </div>
            <p style="font-size: 16px; opacity: 0.9; margin-bottom: 0;">
                ※ 削除したタスクは元に戻せません
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 削除とキャンセルボタン
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            if st.button("🗑️ 削除", type="primary", use_container_width=True):
                # タスクを削除
                deleted_task_title = st.session_state.events[st.session_state.edit_index]['title']
                st.session_state.events.pop(st.session_state.edit_index)
                
                # 削除メッセージを設定
                st.session_state.done_message = f"🗑️「{deleted_task_title}」を削除しました"
                
                # 編集状態をクリア
                st.session_state.edit_index = None
                st.session_state.current_page = 'task_list'
                st.rerun()
        
        with button_col2:
            if st.button("❌ キャンセル", use_container_width=True):
                st.session_state.edit_index = None
                st.session_state.current_page = 'task_list'
                st.rerun()
    
    with col2:
        # 右半分は空にするか、必要に応じて他のコンテンツを配置
        st.empty()


def task_list_page():
    """タスク一覧"""
    # メインタイトルとメニューに戻るボタンを横並びで配置
    title_col, button_col = st.columns([6, 1])
    with title_col:
        st.title('📋 タスク一覧')
    with button_col:
        st.write("")
        st.write("")
        if st.button('← メニューに戻る'):
            if "done_message" in st.session_state:
                del st.session_state["done_message"]

            st.session_state.current_page = 'main'
            st.rerun()
    st.markdown("---")

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
            col1, col2, col3, col4 = st.columns([6, 1, 1, 1])  # タイトル + 編集 + 完了

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
                    st.session_state.current_page = 'change_task'
                    st.session_state.edit_index = i  # 例: 編集対象を保存
                    st.rerun()

            with col3:  
                if st.button("✅", key=f"done_{event['id']}"):
                    st.session_state.events.pop(i)
                    st.session_state.done_message = f"✅「{event['title']}」を完了しました！お疲れ様！"
                    st.rerun()

            with col4:
                if st.button("❌", key=f"delete_{event['id']}"):
                    st.session_state.current_page = 'delete_task'
                    st.session_state.edit_index = i
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
elif st.session_state.current_page == 'statistics':
    statistics_page()
elif st.session_state.current_page == 'help':
    help_page()
elif st.session_state.current_page == 'change_task':
    change_task_page()
elif st.session_state.current_page == 'delete_task':
    delete_task_page()