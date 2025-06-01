import streamlit as st
import base64
from pathlib import Path

def get_base64_image(image_path):
    """画像をbase64エンコードする関数"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"画像ファイルが見つかりません: {image_path}")
        return None

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

# メイン処理
st.title("ペット画像ボタン")

# 画像パスを指定
image_path = "MyPet/esa_button.png"

# 画像ボタンを作成
if create_compact_image_button(image_path, "🎾 遊ぶ", "play_btn", width=120, height=120):
    st.success("🐾 わーい！遊ぼう遊ぼう！")
    st.snow()