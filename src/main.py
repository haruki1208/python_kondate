import streamlit as st
import random

from recipes import search_youtube
from ingredients_manager import load_ingredients, save_ingredients

st.title("🍳 今日何作る？")

ingredients = load_ingredients()

from collections import defaultdict

grouped_ingredients = defaultdict(list)
for item in ingredients:
    group = item.get("group", "その他")
    grouped_ingredients[group].append(item)

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
st.subheader("🧾 現在の食材リスト（グループ別）")
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

# 新しい食材の追加
new_ingredient = st.text_input("食材を入力して追加", "")
group = st.selectbox("グループを選択", list(grouped_ingredients.keys()) + ["その他"])
if st.button("追加"):
    if new_ingredient and all(new_ingredient != i["name"] for i in ingredients):
        ingredients.append({"name": new_ingredient, "group": group, "checked": True})
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
st.subheader("🗑️ 食材を削除")

ingredient_names = [item.get("name") for item in ingredients]
if ingredient_names:
    delete_target = st.selectbox(
        "削除したい食材を選択", ingredient_names, key="delete_select"
    )
    if st.button("選択した食材を削除"):
        ingredients = [i for i in ingredients if i.get("name") != delete_target]
        save_ingredients(ingredients)
        st.success(
            f"「{delete_target}」を削除しました。ページを再読み込みしてください。"
        )
else:
    st.info("削除できる食材がありません。")
