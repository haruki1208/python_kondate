import streamlit as st

### 自作モジュール ###
from login_page import login_signup_page
from main_app import main_app

st.title("🍳 献立提案アプリ")


### コントロール ###
# --- 画面切り替え ---
if "user" not in st.session_state:
    login_signup_page()
else:
    main_app()
