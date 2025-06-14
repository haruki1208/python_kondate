import streamlit as st

st.title("かんたん献立アプリ 🍳")

# セッション状態で食材を保存
if "ingredients" not in st.session_state:
    st.session_state.ingredients = []

# 食材追加欄
new_item = st.text_input("食材を入力してください")

if st.button("追加") and new_item:
    st.session_state.ingredients.append(new_item)
    st.success(f"{new_item} を追加しました")

# 現在の食材一覧
st.subheader("現在の食材リスト")
st.write(st.session_state.ingredients)

# 献立提案
if st.button("献立を提案する"):
    st.subheader("おすすめ献立")
    # 仮のレシピ提案
    st.write("🍛 カレーライス")
    st.write("🥗 野菜サラダ")
    st.write("🍜 味噌汁")
