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


### 画面定義 ###
# --- レシピ検索画面 ---
def suggest_recipes(user_id):
    st.subheader("レシピ検索")

    # 検索モード選択
    mode = st.selectbox("検索モードを選択（レシピ/弁当）", ["レシピ", "弁当"])
    # 食材リストの使用有無
    checked_ingredients = st.checkbox(
        "「食材管理」でチェックされた食材を使用する", value=True
    )
    # レシピの提案数選択
    num_pairs = st.selectbox("レシピの提案数選択", list(range(1, 8)))

    # 自由入力 食材一つ固定
    fix_ingredient = st.text_input(
        "食材を一つ指定（任意）", placeholder="例：鶏肉、卵、トマト"
    )

    # --- レシピ検索 ---
    if st.button("レシピを検索する"):
        query = (
            supabase.table("ingredients_sorted").select("name").eq("user_id", user_id)
        )
        if checked_ingredients:
            # 「チェックされた食材を使用する」にチェックが付いていれば checked=True で絞り込み
            query = query.eq("checked", True)
        response = query.execute()
        # DBから取得するデータ例
        # response.data = [ 0:{"name":"ウインナー"} 1:{"name":"うどん"} ]
        # ↓
        # ingredients = [ 0:"ウインナー" 1:"うどん" ]
        ingredients = [item["name"] for item in response.data]

        if fix_ingredient:
            # fix_ingredient を必ず使う
            # ingredients に重複して入っていたら除外
            ingredients = [ing for ing in ingredients if ing != fix_ingredient]

        if len(ingredients) == 0:
            st.warning("食材が不足しています。")
        else:
            pairs = []

            if fix_ingredient:
                # fix_ingredient + 他の食材をランダムにペア
                available = ingredients.copy()
                random.shuffle(available)

                for ing in available[:num_pairs]:
                    pairs.append((fix_ingredient, ing))

            else:
                # 食材ごとの使用回数を管理
                usage_count = Counter({ingredient: 0 for ingredient in ingredients})

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
