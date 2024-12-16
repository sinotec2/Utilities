## module m
## 讀取儲存的json文件回傳list[dist]

import json


def from_json_to_list(filepath: str):
    """
    從文件中讀取 已從CSV轉為JSON之員工list[dict]資料
    """
    # 開啟文件
    with open(filepath, "r") as file:
        # 從文件中讀取 JSON 格式的資料
        jsonlist: list[dict] = json.load(file)
        return jsonlist
