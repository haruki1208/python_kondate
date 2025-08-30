import streamlit as st
from supabase import create_client, Client

### Supabase接続設定 ###
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

### 関数定義 ###
# # セッションステート初期化
# if "user" not in st.session_state:
#     st.session_state["user"] = None


# --- 新規登録処理 ---
def sign_up(email, password):
    return supabase.auth.sign_up({"email": email, "password": password})


# --- ログイン処理 ---
def sign_in(email, password):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


# --- ログアウト処理 ---
def sign_out():
    supabase.auth.sign_out()
    st.session_state.clear()


### 画面定義 ###
# --- ログインページ ---
def login_signup_page():
    st.title("ログイン / 新規登録")
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])

    with tab1:
        email = st.text_input("メールアドレス", key="login_email")
        password = st.text_input("パスワード", type="password", key="login_password")
        if st.button("ログイン"):
            try:
                res = sign_in(email, password)
                st.session_state.user = res.user
                st.success("ログインに成功しました")
                st.rerun()
            except Exception as e:
                st.error(f"ログインに失敗しました: {str(e)}")

    with tab2:
        new_email = st.text_input("メールアドレス", key="signup_email")
        new_password = st.text_input(
            "パスワード", type="password", key="signup_password"
        )
        if st.button("新規登録"):
            try:
                res = sign_up(new_email, new_password)
                st.success(
                    "アカウントが作成されました。メールを確認してアカウントを有効化してください。"
                )
            except Exception as e:
                st.error(f"新規登録に失敗しました: {str(e)}")
