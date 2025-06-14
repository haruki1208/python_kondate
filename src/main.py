import streamlit as st
import json
import os

# 保存ファイル名
DATA_FILE = "ingredients.json"


# 食材データの読み込み
def load_ingredients():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# 食材データの保存
def save_ingredients(ingredients):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)


# Streamlit UI
st.title("🍳 食材リスト管理")

# 現在の食材を読み込み
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
