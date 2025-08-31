import streamlit as st
from supabase import create_client, Client
import requests
import random
from collections import Counter


### 初期設定 ###
SUPABASE_URL = st.secrets["SUPABASE"]["URL"]
SUPABASE_KEY = st.secrets["SUPABASE"]["KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API"]["KEY"]
# Supabase接続設定
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


### 関数定義 ###
# YouTube動画を検索する関数
def search_youtube(query, mode, max_results=1):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query + " " + mode,
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json().get("items", [])
        results = []
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            results.append((title, video_url))
        return results
    else:
        return []


# # 食材のチェックステータス変更
# def update_checked(ingredient_id, checked):
#     supabase.table("ingredients").update({"checked": checked}).eq(
#         "id", ingredient_id
#     ).execute()


# # 削除用ダイアログ定義
# @st.dialog("削除確認")
# def confirm_delete(ingredient_id, name):
#     st.warning(f'"{name}" を削除しますか？')
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("はい、削除する", key="confirm_delete"):
#             supabase.table("ingredients").delete().eq("id", ingredient_id).execute()
#             st.success(f"{name} を削除しました！")
#             st.rerun()
#     with col2:
#         if st.button("キャンセル", key="cancel_delete"):
#             st.rerun()


### 画面定義 ###
# --- レシピ検索画面 ---
def suggest_recipes(user_id):
    st.subheader("レシピ検索")

    # 検索モード選択
    mode = st.selectbox("検索モードを選択（レシピ/弁当）", ["レシピ", "弁当"])
    # 食材リストの使用有無
    use_ingredients = st.checkbox(
        "「食材管理」でチェックされた食材を使用する", value=True
    )
    # レシピの提案数選択
    num_pairs = st.selectbox("レシピの提案数選択", list(range(1, 8)))

    # --- レシピ検索 ---
    if st.button("レシピを検索する"):
        query = (
            supabase.table("ingredients_sorted").select("name").eq("user_id", user_id)
        )
        if use_ingredients:
            # 「チェックされた食材を使用する」にチェックが付いていれば checked=True で絞り込み
            query = query.eq("checked", True)
        response = query.execute()
        # DBから取得するデータ例
        # response.data = [ 0:{"name":"ウインナー"} 1:{"name":"うどん"} ]
        # ↓
        # ingredients = [ 0:"ウインナー" 1:"うどん" ]
        ingredients = [item["name"] for item in response.data]

        if response.count == 0:
            st.warning("食材を1つ以上選択してください。")
        else:
            if response.count == 1:
                pairs.append(tuple(ingredients))
            else:
                # 食材ごとの使用回数を管理
                usage_count = Counter({ingredient: 0 for ingredient in ingredients})

                pairs = []

                while len(pairs) < num_pairs:
                    # 使用回数が2未満の食材だけを候補にする
                    available = [ing for ing, count in usage_count.items() if count < 2]

                    # 候補が2つ未満ならもう作れない
                    if len(available) < 2:
                        break

                    # ランダムに2つ選んでペアを作る
                    chosen = random.sample(available, 2)
                    pairs.append(tuple(chosen))

                    # 使用回数を更新
                    for ing in chosen:
                        usage_count[ing] += 1

            # 作りたい数に届かなかった場合の通知
            if len(pairs) < num_pairs:
                st.write(f"⚠️ 食材が足りないため、{len(pairs)}組しか作れませんでした。")

            # 完成したペアの出力
            for i, pair in enumerate(pairs, 1):
                query = " ".join(pair)
                st.info(f"検索ワード: {query} {mode}")
                results = search_youtube(query, mode)
                if results:
                    for title, url in results:
                        st.markdown(f"{title}")
                        st.video(url)
                else:
                    st.error("YouTube動画が見つかりませんでした。")

    # with st.expander("➕ 食材追加", expanded=False):
    #     # 既存のグループ名を取得
    #     response = (
    #         supabase.table("ingredients")
    #         .select("group")
    #         .eq("user_id", user_id)
    #         .order("group")
    #         .execute()
    #     )
    #     groups = list({item["group"] for item in response.data})  # 重複削除

    #     # 食材名入力
    #     name = st.text_input("追加する食材名")

    #     # グループ選択 or 入力
    #     group_choice = st.selectbox(
    #         "既存グループを選択（または「新規」）", ["新規"] + groups
    #     )
    #     if group_choice == "新規":
    #         group = st.text_input("新しいグループ名")
    #     else:
    #         group = group_choice

    #     # 追加ボタン
    #     if st.button("追加"):
    #         if name and group:
    #             ingredient = {"user_id": user_id, "name": name, "group": group}
    #             supabase.table("ingredients").insert(ingredient).execute()
    #             st.success(f"{name} を {group} グループに追加しました！")
    #         else:
    #             st.error("食材名とグループを入力してください")

    # # --- 食材リスト ---
    # with st.expander("🧾 食材リスト", expanded=True):
    #     response = (
    #         supabase.table("ingredients_sorted")
    #         .select("*")
    #         .eq("user_id", user_id)
    #         .execute()
    #     )
    #     ingredients = response.data

    #     grouped = {}
    #     for ingredient in ingredients:
    #         group = ingredient["group"]
    #         if group not in grouped:
    #             grouped[group] = []
    #         grouped[group].append(ingredient)

    #     for group, items in grouped.items():
    #         st.write(f"### {group}")
    #         for ingredient in items:
    #             cols = st.columns([0.7, 0.3])
    #             with cols[0]:
    #                 st.checkbox(
    #                     ingredient["name"],
    #                     value=ingredient["checked"],
    #                     key=f"chk_{ingredient['id']}",
    #                     on_change=update_checked,
    #                     args=(
    #                         ingredient["id"],
    #                         not ingredient["checked"],
    #                     ),  # チェック状態を反転した値をDB更新関数に渡す
    #                 )
    #             with cols[1]:
    #                 st.button(
    #                     "🗑️",
    #                     key=f"del_{ingredient['id']}",
    #                     on_click=confirm_delete,
    #                     args=(ingredient["id"], ingredient["name"]),
    #                 )
