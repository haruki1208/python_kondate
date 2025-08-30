import streamlit as st
from supabase import create_client, Client

### 初期設定 ###
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
# Supabase接続設定
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### 関数定義 ###
# 食材のチェックステータス変更
def update_checked(ingredient_id, checked):
    supabase.table("ingredients").update({"checked": checked}).eq(
        "id", ingredient_id
    ).execute()


# 削除用ダイアログ定義
@st.dialog("削除確認")
def confirm_delete(ingredient_id, name):
    st.warning(f'"{name}" を削除しますか？')
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい、削除する", key="confirm_delete"):
            supabase.table("ingredients").delete().eq("id", ingredient_id).execute()
            st.success(f"{name} を削除しました！")
            st.rerun()
    with col2:
        if st.button("キャンセル", key="cancel_delete"):
            st.rerun()


### 画面定義 ###
# --- 食材管理画面 ---
def ingredients_manager(user_id):
    st.subheader("食材管理")

    # --- 食材追加フォーム ---
    with st.expander("➕ 食材追加", expanded=False):
        # 既存のグループ名を取得
        response = (
            supabase.table("ingredients")
            .select("group")
            .eq("user_id", user_id)
            .order("group")
            .execute()
        )
        groups = list({item["group"] for item in response.data})  # 重複削除

        # 食材名入力
        name = st.text_input("追加する食材名")

        # グループ選択 or 入力
        group_choice = st.selectbox(
            "既存グループを選択（または「新規」）", ["新規"] + groups
        )
        if group_choice == "新規":
            group = st.text_input("新しいグループ名")
        else:
            group = group_choice

        # 追加ボタン
        if st.button("追加"):
            if name and group:
                ingredient = {"user_id": user_id, "name": name, "group": group}
                supabase.table("ingredients").insert(ingredient).execute()
                st.success(f"{name} を {group} グループに追加しました！")
            else:
                st.error("食材名とグループを入力してください")

    # --- 食材リスト ---
    with st.expander("🧾 食材リスト", expanded=True):
        response = (
            supabase.table("ingredients_sorted")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        ingredients = response.data

        grouped = {}
        for ingredient in ingredients:
            group = ingredient["group"]
            if group not in grouped:
                grouped[group] = []
            grouped[group].append(ingredient)

        for group, items in grouped.items():
            st.write(f"### {group}")
            for ingredient in items:
                cols = st.columns([0.7, 0.3])
                with cols[0]:
                    st.checkbox(
                        ingredient["name"],
                        value=ingredient["checked"],
                        key=f"chk_{ingredient['id']}",
                        on_change=update_checked,
                        args=(
                            ingredient["id"],
                            not ingredient["checked"],
                        ),  # チェック状態を反転した値をDB更新関数に渡す
                    )
                with cols[1]:
                    st.button(
                        "🗑️",
                        key=f"del_{ingredient['id']}",
                        on_click=confirm_delete,
                        args=(ingredient["id"], ingredient["name"]),
                    )
