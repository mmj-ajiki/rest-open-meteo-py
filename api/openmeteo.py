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
import urllib.parse
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# 環境変数からOPEN METEOのREST URLを取得する
restURL = os.environ.get("OPENMETEO_REST_URL")
if restURL == None:
    print("[ERROR] OPENMETEO_REST_URL not specified.")
    restURL = ""

# 環境変数からタイムゾーンを取得する
timeZone = os.environ.get("OPENMETEO_TZ")
if timeZone == None:
    print("[ERROR] OPENMETEO_TZ not specified.")
    timeZone = ""
else:
    timeZone = urllib.parse.quote(timeZone)

#
# [FUNCTION] convertWeatherCode()
#
# [DESCRIPTION]
#  Open Meteoの天気コードを文字列に変換する
#
# [INPUTS]
#  weatherCode - 天気コード
# 
# [OUTPUTS]
#  コードに相当する日本語文字列
# 
# [NOTE]
#  参考：https://www.jodc.go.jp/data_format/weather-code_j.html
#
def convertWeatherCode(weatherCode):
  weather = '不明'
  if weatherCode == 0:
    weather = '快晴'    # 0 : Clear Sky
  elif weatherCode == 1:
    weather = '晴れ'    # 1 : Mainly Clear
  elif weatherCode == 2:
    weather = '一部曇'  # 2 : Partly Cloudy
  elif weatherCode == 3:
    weather = '曇り'    # 3 : Overcast
  elif weatherCode <= 49:
    weather = '霧'      # 45, 48 : Fog And Depositing Rime Fog
  elif  weatherCode <= 59:
    weather = '霧雨'    # 51, 53, 55 : Drizzle Light, Moderate And Dense Intensity ・ 56, 57 : Freezing Drizzle Light And Dense Intensity
  elif weatherCode <= 69:
    weather = '雨'  # 61, 63, 65 : Rain Slight, Moderate And Heavy Intensity ・66, 67 : Freezing Rain Light And Heavy Intensity
  elif weatherCode <= 79:
    weather = '雪'  # 71, 73, 75 : Snow Fall Slight, Moderate And Heavy Intensity ・ 77 : Snow Grains
  elif weatherCode <= 84:
    weather = '俄か雨'  # 80, 81, 82 : Rain Showers Slight, Moderate And Violent
  elif weatherCode <= 94:
    weather = '雪・雹'  # 85, 86 : Snow Showers Slight And Heavy
  elif weatherCode <= 99:
    weather = '雷雨'    # 95 : Thunderstorm Slight Or Moderate ・ 96, 99 : Thunderstorm With Slight And Heavy Hail

  return weather

#
# HISTORY
# [1] 2024-10-11 - Initial version
#
 
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
# [FUNCTION] getForecastWeather()
#
# [DESCRIPTION]
#  指定した緯度と経度の地点での一週間分の予測する天気を返す
#
# [INPUTS]
#  latitude  - 天気予測をする地点の緯度
#  longitude - 天気予測をする地点の経度
#
# [OUTPUTS]
#  成功: {'status':'ok', 'forecast': [{'datetime':1724943600000, 'temperature':27.1, 'weather':'快晴'},...], 'message': null}
#  失敗: {'status':"error", 'forecast': [], 'message': '[OPEN METEO] Forecast not found'}
#
# [NOTES]
#  Open Meteo REST APIアクセスの例:
#   https://api.open-meteo.com/v1/forecast?latitude=35.6785&longitude=139.6823&hourly=temperature_2m
# 
#   hourlyに「temperature_2m」というパラメータを指定すると、地上2mの気温が1週間分（1時間ごと）取得する
#
def getForecastWeather(latitude, longitude):
    # 返り値の初期値
    retVal = {'status':'error', 'forecast': [], 'message': '[OPEN METEO] Forecast not found'}

    # アクセスするURLを生成する
    url = restURL + "?latitude=" + latitude + "&longitude=" + longitude
    url += "&hourly=temperature_2m,weathercode&timezone=" + timeZone
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
        codeList = result['hourly']['weathercode']
        infoList = []
        for (dt, temp, code) in zip(datetime, tempList, codeList):
            info = {}
            info['datetime'] = formatDatetime(dt); # エポック値へ変換
            info['temperature'] = temp
            info['weather'] = convertWeatherCode(code) # コードを天気に変換
            infoList.append(info)
        retVal['forecast'] = infoList
    else:
        return retVal

    retVal['status'] = 'ok'
    retVal['message'] = None

    return retVal
#
# HISTORY
# [2] 2024-10-11 - Added weather and used time-zone
# [1] 2024-09-30 - Initial version
#