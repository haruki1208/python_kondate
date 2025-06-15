from json_control import load_json, save_json

# 食材管理Jsonファイル名
json_file = "ingredients.json"


# 食材を読み込む関数
def load_ingredients():
    return load_json(json_file)


# 食材を保存する関数
def save_ingredients(data):
    save_json(data, json_file)
