import streamlit as st
from supabase import create_client, Client

st.title("タイトル（テスト）")

# 環境変数を取得
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
# YOUTUBE_API_KEY = st.secrets["YOUTUBE_API"]["KEY"]

# st.write("SUPABASE_URL:", SUPABASE_URL)
# st.write("ANON_KEY:", ANON_KEY)
# st.write("YOUTUBE_API_KEY:", YOUTUBE_API_KEY)

# st.write("=== secrets の中身 ===")
# for key, value in st.secrets.items():
#     st.write(f"{key} = {value}")

# Supabase接続設定
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


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


# -------------------------------------


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


# --- ログイン画面 ---
# def login_page():
#     st.title("ログイン / 新規登録")
#     email = st.text_input("📧 メールアドレス")
#     password = st.text_input("🔑 パスワード", type="password")

#     if st.button("新規登録"):
#         try:
#             user = supabase.auth.sign_up({"email": email, "password": password})
#             st.success(f"新規登録成功: {email}")
#             st.info("確認メールが届くので、本人確認を実施してください")
#         except Exception as e:
#             st.error(f"新規登録失敗: {e}")

#     if st.button("ログイン"):
#         try:
#             user = supabase.auth.sign_in_with_password(
#                 {"email": email, "password": password}
#             )
#             if user.user.confirmed_at is None:
#                 st.warning("本人確認が必要です。メールをチェックしてください。")
#             else:
#                 st.session_state["user"] = user
#         except Exception as e:
#             st.error(f"ログイン失敗: {e}")


# --- 画面切り替え ---
if "user" not in st.session_state:
    login_signup_page()
else:
    main_app()
