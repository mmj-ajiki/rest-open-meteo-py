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

# testメソッドにアクセスする
res_data = None
try:
    response = requests.get(rest_url + "/test", headers=headers)
    res_data = response.json()
except requests.exceptions.RequestException as err:
    print("[Server Connection Error]:", err)

if res_data != None:
    print("----- Results from /test -----")
    print(res_data)
else:
    sys.exit()

# 指定した地点の予測気温を取得する
# {'city': 'tokyo', 'latitude': 35.6895014, 'longitude': 139.6917337};
# {'city':'osaka', 'latitude': 34.686344, 'longitude': 135.520037};
lat = '35.6895014'
lon = '139.6917337'
url = rest_url+"/temperature?latitude=" + lat + "&longitude=" + lon
res_data = None
try:
    response = requests.get(url, headers=headers)
    res_data = response.json()
except requests.exceptions.RequestException as err:
    print("[Server Connection Error]:", err)

if res_data != None:
    print("----- Results from /temperature -----")
    print(res_data)

#
# HISTORY
# [1] 2024-09-30 - First release
#