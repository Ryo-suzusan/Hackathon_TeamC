import streamlit as st
import base64
from pathlib import Path

def get_base64_image(image_path):
    """画像をbase64エンコードする関数"""
    try:
        # パスの存在確認
        path_obj = Path(image_path)
        st.write(f"デバッグ: 指定パス = {image_path}")
        st.write(f"デバッグ: 絶対パス = {path_obj.absolute()}")
        st.write(f"デバッグ: ファイル存在 = {path_obj.exists()}")
        
        if not path_obj.exists():
            st.error(f"画像ファイルが見つかりません: {image_path}")
            # 現在のディレクトリの中身を表示
            current_dir = Path(".")
            st.write("現在のディレクトリの中身:")
            for item in current_dir.iterdir():
                st.write(f"  - {item.name} ({'ディレクトリ' if item.is_dir() else 'ファイル'})")
            return None
            
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            st.success(f"画像の読み込み成功: {len(encoded)} bytes")
            return encoded
    except Exception as e:
        st.error(f"エラー: {str(e)}")
        return None

def create_image_button_v2(image_path, button_key, width=100, height=100):
    """イラストボタンを作成する関数（改良版2）"""
    
    # 画像をbase64エンコード
    img_base64 = get_base64_image(image_path)
    
    if img_base64 is None:
        return False
    
    # 画像形式を判定
    if image_path.lower().endswith('.png'):
        img_format = 'png'
    elif image_path.lower().endswith(('.jpg', '.jpeg')):
        img_format = 'jpeg'
    else:
        img_format = 'png'
    
    # より強力なCSSセレクタを使用
    button_style = f"""
    <style>
    /* 全てのstreamlit buttonに適用 */
    .stButton > button[data-baseweb="button"][key="{button_key}"],
    .stButton > button[key="{button_key}"],
    .stButton button[aria-label*="{button_key}"],
    .stButton button:has-text(" "),
    .stButton button {{
        background-image: url('data:image/{img_format};base64,{img_base64}') !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        border: none !important;
        border-radius: 10px !important;
        width: {width}px !important;
        height: {height}px !important;
        min-width: {width}px !important;
        min-height: {height}px !important;
        max-width: {width}px !important;
        max-height: {height}px !important;
        cursor: pointer !important;
        transition: transform 0.2s !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        color: transparent !important;
        font-size: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        text-indent: -9999px !important;
        overflow: hidden !important;
    }}
    
    .stButton > button[data-baseweb="button"][key="{button_key}"]:hover,
    .stButton > button[key="{button_key}"]:hover,
    .stButton button:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
    }}
    </style>
    """
    
    # CSSを適用
    st.markdown(button_style, unsafe_allow_html=True)
    
    # 空のボタンを作成
    return st.button(" ", key=button_key, help="クリックしてください")

def create_image_button_v3(image_path, button_key, width=100, height=100):
    """イラストボタンを作成する関数（st.imageとst.buttonの組み合わせ）"""
    
    # 画像をbase64エンコード
    img_base64 = get_base64_image(image_path)
    
    if img_base64 is None:
        return False
    
    # 画像形式を判定
    if image_path.lower().endswith('.png'):
        img_format = 'png'
    elif image_path.lower().endswith(('.jpg', '.jpeg')):
        img_format = 'jpeg'
    else:
        img_format = 'png'
    
    # 透明なボタンを上に重ねるスタイル
    overlay_style = f"""
    <style>
    .image-button-container-{button_key} {{
        position: relative;
        display: inline-block;
        width: {width}px;
        height: {height}px;
    }}
    
    .image-button-{button_key} {{
        width: {width}px;
        height: {height}px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s;
        cursor: pointer;
    }}
    
    .image-button-{button_key}:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }}
    </style>
    """
    
    st.markdown(overlay_style, unsafe_allow_html=True)
    
    # 画像を表示
    img_html = f"""
    <div class="image-button-container-{button_key}">
        <img src="data:image/{img_format};base64,{img_base64}" 
             class="image-button-{button_key}"
             width="{width}" height="{height}">
    </div>
    """
    st.markdown(img_html, unsafe_allow_html=True)
    
    # その直後に透明なボタンを配置
    transparent_button_style = f"""
    <style>
    .stButton > button[key="{button_key}"] {{
        position: relative;
        top: -{height + 10}px;
        background: transparent !important;
        border: none !important;
        width: {width}px !important;
        height: {height}px !important;
        color: transparent !important;
        font-size: 0 !important;
        cursor: pointer !important;
        margin-bottom: -{height + 10}px !important;
    }}
    </style>
    """
    st.markdown(transparent_button_style, unsafe_allow_html=True)
    
    return st.button(" ", key=button_key, help="クリックしてください")

# メイン部分
st.title("イラストボタンのサンプル")

# 画像ファイルのパスをいくつか試してみる
image_paths_to_try = [
    "MyPet/esa_button.png",
    "./MyPet/esa_button.png", 
    "MyPet\\esa_button.png",  # Windows形式
]

st.write("## パステスト")
working_path = None
for path in image_paths_to_try:
    st.write(f"### パス: {path}")
    if Path(path).exists():
        st.success("✅ このパスは存在します")
        working_path = path
        break
    else:
        st.error("❌ このパスは存在しません")

if working_path:
    image_path = working_path
    st.write(f"使用するパス: {image_path}")
else:
    st.error("有効なパスが見つかりませんでした")
    image_path = "MyPet/esa_button.png"  # デフォルト

# 複数の方法を試す
st.write("## 方法1: 改良版CSS")
if create_image_button_v2(image_path, "btn_v2", width=120, height=120):
    st.success("方法1のボタンがクリックされました！")

st.write("## 方法2: 画像+透明ボタン重ね")
if create_image_button_v3(image_path, "btn_v3", width=120, height=120):
    st.success("方法2のボタンがクリックされました！")

st.write("## 方法3: シンプルな画像+ボタンの組み合わせ")
col1, col2 = st.columns([1, 2])
with col1:
    # 画像を表示
    img_base64 = get_base64_image(image_path)
    if img_base64:
        img_format = 'png' if image_path.lower().endswith('.png') else 'jpeg'
        st.markdown(f"""
        <img src="data:image/{img_format};base64,{img_base64}" 
             width="120" height="120" 
             style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        """, unsafe_allow_html=True)

with col2:
    if st.button("🎯 このボタンをクリック", key="btn_simple"):
        st.success("方法3のボタンがクリックされました！")
        st.balloons()  # 成功の演出

# 代替方法：HTMLボタンで直接確認
st.write("## 代替方法（HTML直接）")
img_base64 = get_base64_image(image_path)
if img_base64:
    # 画像形式を判定
    if image_path.lower().endswith('.png'):
        img_format = 'png'
    elif image_path.lower().endswith(('.jpg', '.jpeg')):
        img_format = 'jpeg'
    else:
        img_format = 'png'
    
    html_button = f"""
    <div style="text-align: center;">
        <img src="data:image/{img_format};base64,{img_base64}" 
             width="120" height="120" 
             style="cursor: pointer; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"
             onclick="alert('HTMLボタンがクリックされました！')">
        <p>↑ HTMLで直接表示した画像（クリック可能）</p>
    </div>
    """
    st.markdown(html_button, unsafe_allow_html=True)

st.write("---")

# 複数のボタンの例
col1, col2, col3 = st.columns(3)
"""
with col1:
    if create_image_button("button1.png", "btn_left", width=100, height=100):
        st.write("左のボタンがクリックされました")

with col2:
    if create_image_button("button2.png", "btn_center", width=100, height=100):
        st.write("中央のボタンがクリックされました")

with col3:
    if create_image_button("button3.png", "btn_right", width=100, height=100):
        st.write("右のボタンがクリックされました")
"""