import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
DATA_FILE = os.path.join(DATA_DIR, "ingredients.json")


# 食材を読み込む関数
def load_ingredients():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# 食材を保存する関数
def save_ingredients(ingredients):
    os.makedirs(DATA_DIR, exist_ok=True)  # フォルダがなければ作成
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)
