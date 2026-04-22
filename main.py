#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  Open-MetaoのAPIを利用したRESTメソッドを定義する
# 
# [NOTES]
#
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.openmeteo import getForecastWeather
    
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
#  request - リクエスト
# 
# [OUTPUTS]
# 
# [NOTES]
#  Web画面上に単に、"Open-Meteo REST Server"と表示するのみ
#
@app.get("/", response_class=HTMLResponse)
async def topPage(request: Request):
    
    return templates.TemplateResponse(
        name="top.html", 
        context={"request": request, "title": "Open-Meteo REST Server"},
        request=request)
#
# HISTORY
# [2] 2026-04-22 - Fixed TemplateResponse() due to the Starlette change
# [1] 2024-09-30 - Initial version
#

#
# GET Method
# End Point: /rest/cities
#
# [DESCRIPTION]
#  いくつかの都庁、府庁、県庁の緯度と経度を取得する。
#
# [INPUTS] 
#  None
# 
# [OUTPUTS]
#  都庁、府庁、県庁の緯度と経度
#  {
#    "keys": ["city", "latitude", "longitude"],
#    "records": [{'city':'新宿区', 'latitude':35.689501, 'longitude':139.691722}, ...],
#    "message": None
#  }
# 
# [NOTES]
#
@app.get("/rest/cities")
def getCities():
    results = {}
    results['keys'] = ['city', 'latitude', 'longitude']
    list = []
    elements = {'city': '新宿区', 'latitude': 35.689501, 'longitude': 139.691722}
    list.append(elements)
    elements = {'city':'大阪市', 'latitude': 34.686344, 'longitude': 135.520037}
    list.append(elements)
    elements = {'city':'福岡市', 'latitude': 33.606389, 'longitude': 130.417968}
    list.append(elements)

    results['records'] = list
    results['message'] = None

    if is_reload_enabled():
        print("[JSON]", results)

    return results
#
# HISTORY
# [2] 2024-10-11 - Added Fukuoka
# [1] 2024-09-30 - Initial version
#

#
# POST Method
# End Point: /rest/server_info
#
# [DESCRIPTION]
#   eYACHO/GEMBA Noteへメッセージを返す
#
# [INPUTS] 
#   request - bodyにクライアント（eYACHO/GEMBA Note）からの緯度経度を含んだ情報が含まれる（利用せず）
# 
# [OUTPUTS]
#   次のJSONを返す
#   { "message": <メッセージ> }
# 
# [NOTES]
#   eYACHO/GEMBA Noteのボタンアクション「サーバーへ送信」でメッセージを表示させる
#
@app.post("/rest/server_info")
async def getWho(request: Request):
    results = {}
    results['message'] = "Hello, I am a Python server!"
    
    if is_reload_enabled():
        body = await request.body()
        print("[BODY]", body)
        print("[JSON]", results)

    return results
#
# HISTORY
# [1] 2024-10-11 - Initial version
#

#
# GET Method
# End Point: /rest/weather
#
# [DESCRIPTION]
#  緯度と経度からその地点の天気と気温の予測データを取得する
#
# [INPUTS] 
#  request - Request from the method：緯度と経度を含む
# 
# [OUTPUTS]
# {
#   'keys': ['datetime', 'temperature', 'weather'], 
#   'records': [
#       {'datetime': 1724943600, 'temperature': 28.5, 'weather': '晴れ'},  
#       {'datetime': 1724947200, 'temperature': 29.2, 'weather': '快晴'},  
#       ...
#   ],
#   'message': null
# }
# 
# [NOTES]
#  datetimeの値はエポック時間
#
@app.get("/rest/weather")
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

    results['keys'] = ['datetime', 'temperature', 'weather']

    info = getForecastWeather(lat, lon)

    results['records'] = info['forecast']
    results['message'] = info['message']
  
    if is_reload_enabled():
        print("[JSON]", results)

    return results
#
# HISTORY
# [2] 2024-10-11 - Changed /rest/weather
# [1] 2024-09-30 - Initial version
#