#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  Sample Server for generating notes using the Custom URL Scheme
# 
# [NOTES]
#
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.openmeteo import getForecastTemp
    
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#
# [FUNCTION] is_reload_enabled()
#
# [DESCRIPTION]
#  実行するコマンドに--reloadが含まれるか判定する
#
# [INPUTS] None
#
# [OUTPUTS]
#  True: 含まれる False: 含まれない
#
# [NOTES]
#  Trueの場合はデバッグ実行とみなし、JSONデータをコンソール上に表示する
#
def is_reload_enabled():
    return "--reload" in sys.argv
#
# HISTORY
# [1] 2024-09-30 - Initial version
#

#
# GET Method
# End Point: /
#
# [DESCRIPTION]
#  トップページを開く
#
# [INPUTS]
#  Request - リクエスト
# 
# [OUTPUTS]
# 
# [NOTES]
#  Web画面上に単に、"Open-Meteo REST Server"と表示するのみ
#
@app.get("/", response_class=HTMLResponse)
async def topPage(request: Request):
    
    return templates.TemplateResponse("top.html", {"request": request, "title": "Open-Meteo REST Server"})
#
# HISTORY
# [1] 2024-09-30 - Initial version
#

#
# GET Method
# End Point: /rest/temperature
#
# [DESCRIPTION]
#  緯度と経度からその地点の気温の予測データを取得する
#
# [INPUTS] 
#  Request - リクエスト
# 
# [OUTPUTS]
# {
#   'keys': ['datetime', 'temperature'], 
#   'records': [
#       {'datetime': 1724943600, 'temperature': 28.5},  
#       {'datetime': 1724947200, 'temperature': 29.2},  
#       ...
#   ],
#   'message': null
# }
# 
# [NOTES]
#  datetimeの値はエポック時間
#
@app.get("/rest/temperature")
def getTemperature(request: Request): 
    results = {'keys':[], 'records':[], 'message':'緯度あるいは経度がありません'};
    lat = 0
    lon = 0
  
    # 緯度の取得
    lat = request.query_params.get('latitude')

    # 経度の取得
    lon = request.query_params.get('longitude')

    # 緯度と経度の存在チェック
    if lat == None or lon == None or lat == 0 or lon == 0:
        return results

    results['keys'] = ['datetime', 'temperature']

    info = getForecastTemp(lat, lon)

    results['records'] = info['forecast']
    results['message'] = info['message']
  
    if is_reload_enabled():
        print("[JSON]", results)

    return results
#
# HISTORY
# [1] 2024-09-30 - Initial version
#

#
# GET Method
# End Point: /rest/test
#
# [DESCRIPTION]
#  REST APIが起動できるかテストするメソッド
#
# [INPUTS] 
#  None
# 
# [OUTPUTS]
#  都庁、府庁、県庁の緯度と経度
#  {
#    "keys": ["city", "latitude", "longitude"],
#    "records": [{'city':'tokyo', 'latitude':35.6895014, 'longitude':139.6917337}, ...],
#    "message": None
#  }
# 
# [NOTES]
#
@app.get("/rest/test")
def getTest():
    results = {}
    results['keys'] = ['city', 'latitude', 'longitude']
    list = []
    elements = {'city': 'tokyo', 'latitude': 35.6895014, 'longitude': 139.6917337}
    list.append(elements)
    elements = {'city':'osaka', 'latitude': 34.686344, 'longitude': 135.520037}
    list.append(elements)
    results['records'] = list
    results['message'] = None

    if is_reload_enabled():
        print("[JSON]", results)

    return results
#
# HISTORY
# [1] 2024-09-30 - Initial version
#