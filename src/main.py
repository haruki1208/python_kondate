import streamlit as st
from ingredients_manager import load_ingredients, save_ingredients

st.title("🍳 食材リスト管理")

# 現在の食材を読み込み リスト型？
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
