import json
import os

DATA_FILE = "../data/ingredients.json"


def load_ingredients():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_ingredients(ingredients):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, ensure_ascii=False, indent=2)
