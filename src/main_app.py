import streamlit as st

### 自作モジュール ###
from login_page import sign_out

### 関数定義 ###


### 画面定義 ###
# --- メイン画面 ---
def main_app():
    st.title("メインアプリケーション")
    st.write(f"ようこそ、{st.session_state.user.email}さん！")

    menu = ["ホーム", "コンテンツ"]
    choice = st.sidebar.selectbox("メニュー", menu)

    if choice == "ホーム":
        st.subheader("ホーム")
        st.write("ホームです。")

    elif choice == "コンテンツ":
        st.subheader("コンテンツ")
        st.write("ここにコンテンツを表示できます。")

    if st.sidebar.button("ログアウト"):
        sign_out()
        st.rerun()
