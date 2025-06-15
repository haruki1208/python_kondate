import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")


# Jsonファイルを読み込む関数
def load_json(json_file):
    data_file = os.path.join(DATA_DIR, json_file)
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# jsonファイルを書き込む関数
def save_json(data, json_file):
    data_file = os.path.join(DATA_DIR, json_file)
    os.makedirs(DATA_DIR, exist_ok=True)  # フォルダがなければ作成
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
