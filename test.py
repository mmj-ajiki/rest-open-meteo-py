#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] test.py
#
# [DESCRIPTION]
#  サンプルRESTサーバーをテストするPythonプログラム
#
# [NOTES]
#
import sys
import requests

# 実行環境に応じて変更する
rest_url = 'http://localhost:8000/rest'
print("[REST URL]", rest_url)

# Header
headers = {
    'content-type': 'application/json'
}

# citiesメソッドにアクセスする
res_data = None
try:
    response = requests.get(rest_url + "/cities", headers=headers)
    res_data = response.json()
except requests.exceptions.RequestException as err:
    print("[Server Connection Error]:", err)

if res_data != None:
    print("----- Results from /cities -----")
    print(res_data)
else:
    sys.exit()

# 指定した地点の気温と天気の予測データを取得する
# {'city': '新宿区', 'latitude': 35.689501, 'longitude': 139.691722};
# {'city':'大阪市', 'latitude': 34.686344, 'longitude': 135.520037};
lat = '35.689501'
lon = '139.691722'
url = rest_url+"/weather?latitude=" + lat + "&longitude=" + lon
res_data = None
try:
    response = requests.get(url, headers=headers)
    res_data = response.json()
except requests.exceptions.RequestException as err:
    print("[Server Connection Error]:", err)

if res_data != None:
    print("----- Results from /weather -----")
    print(res_data)

#
# HISTORY
# [2] 2024-10-11 - Changed /rest/temperature to /rest/weather
# [1] 2024-09-30 - First release
#