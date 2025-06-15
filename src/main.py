import streamlit as st
import random

from recipes import search_youtube
from ingredients_manager import load_ingredients, save_ingredients
from favorite_recipes_manager import load_favorite_recipes, save_favorite_recipes

st.title("🍳 今日何作る？")

ingredients = load_ingredients()

from collections import defaultdict

# 食材リストをグループごとにまとめる
grouped_ingredients = defaultdict(list)
for item in ingredients:
    group = item.get("group", "その他")
    grouped_ingredients[group].append(item)

# グループごとに区切りを入れた食材名リストを作成（グループ名は選択不可）
grouped_options = []
for group, items in grouped_ingredients.items():
    if items:
        # grouped_options.append(f"--- {group} ---")  # 区切りとして表示
        grouped_options.extend([item["name"] for item in items])


# グループ名で始まるものは選択不可にする
def filter_options(options):
    return [opt for opt in options if not opt.startswith("---")]


selectable_options = filter_options(grouped_options)

# --- 全選択・全解除ボタン ---
col1, col2 = st.columns(2)
with col1:
    if st.button("全選択"):
        for item in ingredients:
            item["checked"] = True
        save_ingredients(ingredients)
with col2:
    if st.button("全解除"):
        for item in ingredients:
            item["checked"] = False
        save_ingredients(ingredients)

# --- グループごとに表示 ---
st.subheader("🧾 現在の食材リスト")
selected_ingredients = []

for group, items in grouped_ingredients.items():
    if not items:
        continue
    with st.expander(group, expanded=True):
        for item in items:
            checked = st.checkbox(
                item.get("name"),
                value=item.get("checked", True),
                key=f"{group}_{item.get('name')}",
            )
            if checked != item.get("checked", True):
                item["checked"] = checked
                save_ingredients(ingredients)
            if checked:
                selected_ingredients.append(item.get("name"))

# YouTube動画を表示
st.markdown("---")
st.subheader("🍽️ 献立提案")
if st.button("選択した食材でYouTube検索"):
    if len(selected_ingredients) == 0:
        st.warning("食材を1つ以上選択してください。")
    else:
        if len(selected_ingredients) == 1:
            selected = selected_ingredients
        else:
            selected = random.sample(selected_ingredients, 2)
        query = " ".join(selected)
        st.info(f"検索ワード: {query}")
        results = search_youtube(query)
        if results:
            for title, url in results:
                st.markdown(f"{title}")
                st.video(url)
        else:
            st.error("YouTube動画が見つかりませんでした。")

# --- お気に入りレシピから検索 ---
st.markdown("---")
st.subheader("⭐ お気に入りレシピから検索")

favorite_recipes = load_favorite_recipes()
if st.button("選択した食材でお気に入りレシピ検索"):
    if not selected_ingredients:
        st.warning("食材を1つ以上選択してください。")
    else:
        found = False
        for recipe_name, recipe_ingredients in favorite_recipes.items():
            # 選択中の食材が1つでも含まれていれば表示
            if any(
                ingredient in recipe_ingredients for ingredient in selected_ingredients
            ):
                st.markdown(f"**{recipe_name}**")
                st.markdown("使う食材：" + ", ".join(recipe_ingredients))
                found = True
        if not found:
            st.info("選択した食材を含むお気に入りレシピはありません。")

# --- お気に入りレシピ登録フォーム ---
st.markdown("---")
st.subheader("⭐ お気に入りレシピ登録")

with st.form("favorite_recipe_form"):
    recipe_name = st.text_input("レシピ名（必須）")
    selected_ingredients = st.multiselect(
        "使う食材（複数選択・必須）",
        options=selectable_options,
        default=[],
        help="グループ名で区切られています。食材名で検索もできます。",
    )
    recipe_url = st.text_input("レシピURL（任意）")
    submitted = st.form_submit_button("お気に入りレシピを登録")

    if submitted:
        if not recipe_name:
            st.error("レシピ名は必須です。")
        elif not selected_ingredients:
            st.error("使う食材を1つ以上選択してください。")
        else:
            favorite_recipes = load_favorite_recipes()
            # レシピ名が重複しないように
            if recipe_name in favorite_recipes:
                st.warning("同じレシピ名がすでに登録されています。")
            else:
                favorite_recipes[recipe_name] = {
                    "ingredients": selected_ingredients,
                    "url": recipe_url,
                }
                save_favorite_recipes(favorite_recipes)
                st.success("お気に入りレシピを登録しました！")


# 新しい食材の追加
st.markdown("---")
with st.expander("➕ 食材追加", expanded=True):
    new_ingredient = st.text_input("食材を入力して追加", "")
    group = st.selectbox(
        "グループを選択", list(grouped_ingredients.keys()) + ["その他"]
    )

    if st.button("追加"):
        if new_ingredient and all(new_ingredient != i["name"] for i in ingredients):
            ingredients.append(
                {"name": new_ingredient, "group": group, "checked": True}
            )
            save_ingredients(ingredients)
            st.success(
                f"「{new_ingredient}」を追加しました！ページを再読み込みしてください。"
            )
        elif any(new_ingredient == i["name"] for i in ingredients):
            st.warning("その食材はすでに登録されています。")
        else:
            st.error("食材を入力してください。")

# --- 食材削除機能（リスト下部に設置） ---
st.markdown("---")
delete_targets: list[str] = []
with st.expander("🗑️ 食材を削除", expanded=True):
    if selectable_options:
        delete_targets = st.multiselect(
            "削除したい食材を選択（複数選択可）",
            options=selectable_options,
            default=[],
            help="削除したい食材を複数選択できます。",
            key="delete_multiselect",
        )
        if st.button("選択した食材を削除"):
            ingredients = [
                i for i in ingredients if i.get("name", "") not in delete_targets
            ]
            save_ingredients(ingredients)
            st.success(
                f"{', '.join(delete_targets)} を削除しました。ページを再読み込みしてください。"
            )
    else:
        st.info("削除できる食材がありません。")
