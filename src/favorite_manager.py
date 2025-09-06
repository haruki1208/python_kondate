import streamlit as st
from supabase import create_client, Client

### 初期設定 ###
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
# Supabase接続設定
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### 関数定義 ###


### select * from favorite_recipes where ingredients @> ARRAY['卵']::text[];


### 画面定義 ###
# --- お気に入りレシピ管理画面 ---
def favorite_manager(user_id):
    st.subheader("お気に入りレシピ管理")

    # --- 食材候補の取得 ---
    ing_response = (
        supabase.table("ingredients")
        .select("id, name, group")
        .eq("user_id", user_id)
        .order("group")
        .execute()
    )
    all_ingredients = [i["name"] for i in ing_response.data]

    # --- お気に入り追加フォーム ---
    with st.expander("➕ お気に入りレシピ追加", expanded=False):
        recipe_name = st.text_input("レシピ名")
        recipe_url = st.text_input("レシピURL (YouTubeやブログ記事など)")

        # 🔽 複数食材をまとめて選択（リストで保持）
        recipe_ingredients = st.multiselect(
            "食材リストを選択",
            options=all_ingredients,
            placeholder="食材名を検索して選んでください",
        )

        if st.button("お気に入りに追加"):
            if not recipe_name:
                st.error("レシピ名は必須です")
            else:
                data = {
                    "user_id": user_id,
                    "name": recipe_name,
                    "url": recipe_url,
                    "ingredients": recipe_ingredients,  # ← TEXT[] にそのまま渡す
                }
                supabase.table("favorite_recipes").insert(data).execute()
                st.success(f'"{recipe_name}" をお気に入りに追加しました！')
                st.rerun()

    # --- お気に入りレシピ一覧 ---
    response = (
        supabase.table("favorite_recipes")
        .select("*")
        .eq("user_id", user_id)
        .order("id", desc=True)
        .execute()
    )
    recipes = response.data

    if not recipes:
        st.info("お気に入りのレシピがありません。上のフォームから追加してください。")
        return

    st.write("📖 登録済みお気に入りレシピ")
    for recipe in recipes:
        # with st.expander(f"🍴 {recipe['name']}", expanded=False):
        # st.write(f"🍴 {recipe['name']}")
        st.markdown(f" 🍴 **{recipe['name']}**")
        (
            # URLがYouTubeなら動画埋め込み表示
            st.video(recipe["url"])
            if recipe["url"] and "youtube.com" and "youtu.be" in recipe["url"]
            # YouTube以外のURLはリンク表示
            else st.markdown(
                f"**URL:** [{recipe['url']}]({recipe['url']})"
                if recipe["url"]
                else "URLなし"
            )
        )

        # TEXT[] は Python でリストとして返る
        st.markdown(
            f"**食材リスト:** {', '.join(recipe['ingredients']) if recipe['ingredients'] else '未登録'}"
        )

        # --- 編集フォーム ---
        with st.expander(f"編集({recipe['name']})", expanded=False):
            new_name = st.text_input(
                "レシピ名を編集", value=recipe["name"], key=f"name_{recipe['id']}"
            )
            new_url = st.text_input(
                "URLを編集", value=recipe["url"] or "", key=f"url_{recipe['id']}"
            )

            new_ingredients = st.multiselect(
                "食材リストを編集",
                options=all_ingredients,
                default=recipe["ingredients"] or [],
                key=f"ing_{recipe['id']}",
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 更新", key=f"update_{recipe['id']}"):
                    supabase.table("favorite_recipes").update(
                        {
                            "name": new_name,
                            "url": new_url,
                            "ingredients": new_ingredients,  # ← リストで保存
                        }
                    ).eq("id", recipe["id"]).execute()
                    st.success(f'"{new_name}" を更新しました！')
                    st.rerun()

            with col2:
                if st.button("🗑️ 削除", key=f"delete_{recipe['id']}"):
                    supabase.table("favorite_recipes").delete().eq(
                        "id", recipe["id"]
                    ).execute()
                    st.success(f'"{recipe["name"]}" を削除しました！')
                    st.rerun()
