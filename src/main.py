import streamlit as st

# ここにsupabaseはインポートしない想定

### 自作モジュール ###
from login import sign_out, sign_in, sign_up, get_user_name
from ingredients_manager import ingredients_manager
from suggest_recipes import suggest_recipes
from favorite_manager import favorite_manager


### 画面定義 ###
# --- ログインページ ---
def login_signup_page():
    st.subheader("ログイン / 新規登録")
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])

    with tab1:
        email = st.text_input("メールアドレス", key="login_email")
        password = st.text_input("パスワード", type="password", key="login_password")
        if st.button("ログイン"):
            try:
                # emailが0818の場合、テスト用アカウントでログイン
                if email == "0818":
                    email = st.secrets["TEST"]["email"]
                    password = st.secrets["TEST"]["password"]

                res = sign_in(email, password)
                st.session_state.user = res.user
                st.success("ログインに成功しました")
                st.rerun()
            except Exception as e:
                st.error(f"ログインに失敗しました: {str(e)}")

    with tab2:
        username = st.text_input("ユーザー名", key="signup_username")
        new_email = st.text_input("メールアドレス", key="signup_email")
        new_password = st.text_input(
            "パスワード", type="password", key="signup_password"
        )
        if st.button("新規登録"):
            if not username:
                st.error("ユーザー名を入力してください")
            else:
                try:
                    res = sign_up(new_email, new_password, username)
                    st.success(
                        "アカウントが作成されました。メールを確認してアカウントを有効化してください。"
                    )
                except Exception as e:
                    st.error(f"新規登録に失敗しました: {str(e)}")


# --- メイン画面 ---
def main_app():
    st.title("🍳 献立提案")

    ### ユーザ情報取得 ###
    user_id = st.session_state.user.id
    user_name = get_user_name()

    ### サイドバー ###
    st.sidebar.write(f"ログイン中：{user_name} さん")
    menu = [
        "レシピ検索",
        "食材管理",
        "お気に入りレシピ",
        "買い物リスト",
        "料理記録",
        "設定",
    ]
    choice = st.sidebar.selectbox("メニュー", menu)

    if choice == "レシピ検索":
        suggest_recipes(user_id)

    elif choice == "食材管理":
        ingredients_manager(user_id)

    elif choice == "お気に入りレシピ":
        favorite_manager(user_id)

    elif choice == "買い物リスト":
        st.write("買い物リスト画面です。")  # ここに買い物リストのコードを追加予定

    elif choice == "料理記録":
        st.write("料理記録画面です。")  # ここに料理記録のコードを追加予定

    elif choice == "設定":
        st.write("設定画面です。")  # ここに設定のコードを追加予定

    if st.sidebar.button("ログアウト"):
        sign_out()
        st.rerun()


### コントロール ###
# --- 画面切り替え ---
if "user" not in st.session_state:
    login_signup_page()
else:
    main_app()
