import streamlit as st
import random

from recipes import search_youtube
from ingredients_manager import load_ingredients, save_ingredients

st.title("🍳 今日何作る？")

# 現在の食材を読み込み
# リスト型
ingredients = load_ingredients()

# 新しい食材の追加
new_ingredient = st.text_input("食材を入力して追加", "")

if st.button("追加"):
    if new_ingredient and new_ingredient not in ingredients:
        ingredients.append(new_ingredient)
        save_ingredients(ingredients)
        st.success(f"「{new_ingredient}」を追加しました！")
    elif new_ingredient in ingredients:
        st.warning("その食材はすでに登録されています。")
    else:
        st.error("食材を入力してください。")

# 食材リスト表示
if ingredients:
    st.subheader("🧾 現在の食材リスト")
    for item in ingredients:
        st.markdown(f"- {item}")
else:
    st.info("まだ食材が登録されていません。")

# YouTube動画を表示
if st.button("ランダム食材でYouTube検索"):
    if len(ingredients) < 2:
        st.warning("食材が2つ以上必要です。")
    else:
        selected = random.sample(ingredients, 2)
        query = " ".join(selected)
        st.info(f"検索ワード: {query}")
        results = search_youtube(query)
        if results:
            for title, url in results:
                st.markdown(f"{title}")
                st.video(url)
        else:
            st.error("YouTube動画が見つかりませんでした。")
