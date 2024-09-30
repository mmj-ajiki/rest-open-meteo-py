#
# [FILE] openmeteo.py
#
# [DESCRIPTION]
#  Open-Meteo REST APIから天気情報を取得する関数を定義する
#
# [NOTES]
#  Open-Meteoについてはこちらを参照のこと：https://open-meteo.com/
#
import os
import datetime
import requests

# 環境変数からOPEN METEOのREST URLを取得する
restURL = os.environ.get("OPENMETEO_REST_URL")
if restURL == None:
    print("[ERROR] OPENMETEO_REST_URL not specified.")

#
# [FUNCTION] formatDatetime()
#
# [DESCRIPTION]
#  日時形式 (YYYY-MM-DDThh:mm) をUNIXタイムスタンプ（エポックタイムスタンプ）に変換する
#
# [INPUTS]
#  inputDt - 変換対象の日時 (形式：YYYY-MM-DDThh:mm)
#
# [OUTPUTS]
#
# [NOTES]
#  eYACHO/GEMBA Noteでは、日付や日時をUNIXタイムスタンプとして取り扱う
#
def formatDatetime(inputDt):
    dt = datetime.datetime.strptime(inputDt, '%Y-%m-%dT%H:%M')
    timestamp = dt.timestamp()

    return timestamp
#
# HISTORY
# [1] 2024-09-30 - Initial version
#

#
# [FUNCTION] getForecastTemp()
#
# [DESCRIPTION]
#  指定した緯度と経度の地点での一週間分の予測気温を返す
#
# [INPUTS]
#  latitude  - 天気予測をする地点の緯度
#  longitude - 天気予測をする地点の経度
#
# [OUTPUTS]
#  成功: {status:"ok", 'forecast': [{"datetime":1724943600000,"temperature":27.1},...], 'message': null}
#  失敗: {status:"error", 'forecast': [], 'message': '[OPEN METEO] Forecast not found'}
#
# [NOTES]
#  Open Meteo REST APIアクセスの例:
#   https://api.open-meteo.com/v1/forecast?latitude=35.6785&longitude=139.6823&hourly=temperature_2m
# 
#   hourlyに「temperature_2m」というパラメータを指定すると、地上2mの気温が1週間分（1時間ごと）取得する
#
def getForecastTemp(latitude, longitude):
    #retVal = {'status':'error', 'forecast': [], 'message': '[OPEN METEO] Forecast not found'}
    retVal = {}

    # アクセスするURLを生成する
    url = restURL + "?latitude=" + latitude + "&longitude=" + longitude + "&hourly=temperature_2m"
    print("[URL]", url)

    # Header
    headers = { 'content-type': 'application/json' }

    # URLにGETメソッドでアクセスする
    result = None
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
    except requests.exceptions.RequestException as err:
        print("[Server Connection Error]:", err)

    if result != None:
        datetime = result['hourly']['time']
        tempList = result['hourly']['temperature_2m']
        infoList = []
        for (dt, temp) in zip(datetime, tempList):
            info = {}
            info['datetime'] = formatDatetime(dt); # エポック値へ変換
            info['temperature'] = temp
            infoList.append(info)
        retVal['forecast'] = infoList
    else:
        return retVal

    retVal['status'] = 'ok'
    retVal['message'] = None

    return retVal
#
# HISTORY
# [1] 2024-09-30 - Initial version
#