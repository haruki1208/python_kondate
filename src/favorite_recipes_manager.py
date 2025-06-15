from json_control import load_json, save_json

# お気に入りレシピ管理Jsonファイル名
json_file = "favorite_recipes.json"


# お気に入りレシピを読み込む関数
def load_favorite_recipes():
    return load_json(json_file)


# お気に入りレシピを保存する関数
def save_favorite_recipes(favorite_recipes):
    save_json(favorite_recipes, json_file)
