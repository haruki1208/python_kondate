import streamlit as st
from supabase import create_client, Client

#######################
## ログインモジュール
## login.py
#######################
## 画面：ログイン / 新規登録
## 機能：認証、ユーザ情報取得
#######################

### Supabase接続設定 ###
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

### 関数定義 ###
# # セッションステート初期化
# if "user" not in st.session_state:
#     st.session_state["user"] = None


# --- ユーザ名取得 ---
def get_user_name():
    if "user" in st.session_state and st.session_state.user is not None:
        user_id = st.session_state.user.id
        user_profile = (
            supabase.table("profiles")
            .select("name")
            .eq("user_id", user_id)
            .execute()
            .data
        )
        if user_profile:
            return user_profile[0]["name"]
    return "ゲスト"


# --- 新規登録処理 ---
def sign_up(email, password, username):
    # 1. Auth に登録
    res = supabase.auth.sign_up({"email": email, "password": password})
    user = res.user
    if user is not None:
        # profiles テーブルに username 登録
        supabase.table("profiles").insert(
            {"user_id": user.id, "name": username}  # auth.users の id  # ユーザー名
        ).execute()
    return res


# --- ログイン処理 ---
def sign_in(email, password):
    return supabase.auth.sign_in_with_password({"email": email, "password": password})


# --- ログアウト処理 ---
def sign_out():
    supabase.auth.sign_out()
    st.session_state.clear()
