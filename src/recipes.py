import os
from dotenv import load_dotenv
import requests
import random  # ランダム選択のために追加

# .envファイルから環境変数を読み込み
load_dotenv()

# APIキーを取得
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# YouTube動画を検索する関数
def search_youtube(query, max_results=1):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query + " レシピ",
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


# 献立候補を表示する関数
def display_recipes(recipes):
    """献立候補をターミナルに表示"""
    print("\n--- 献立候補 ---")
    for idx, recipe in enumerate(recipes, 1):
        print(f"{idx}. {recipe['title']}\n   {recipe['link']}\n")
