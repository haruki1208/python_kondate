from json_control import load_json, save_json

# お気に入りレシピ管理Jsonファイル名
json_file = "favorite_recipes.json"


# お気に入りレシピを読み込む関数
def load_favorite_recipes():
    data = load_json(json_file)
    return data if isinstance(data, dict) else {}


# お気に入りレシピを保存する関数
def save_favorite_recipes(data):
    save_json(data, json_file)
