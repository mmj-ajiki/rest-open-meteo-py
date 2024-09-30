# rest-open-meteo-py

## サンプルRESTサーバー

このサンプルのRESTサーバーは、Open-Meteo ([https://open-meteo.com/](https://open-meteo.com/))という無償でも利用できる天気予報APIにアクセスする。そのPython版である。

### Pythonをインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)からPythonをインストールする。

### 必要なパッケージのインストール

コマンドプロンプト上で、次のコマンドを実行し、必要なPythonのパッケージをインストールする。

```bash
pip install -r requirements.txt
```

### 環境変数の設定

環境変数はファイル env.batあるいはenv.shに定義する。コマンドプロンプトからバッチファイルあるいはシェルファイルを実行し、環境変数を設定する。

Windows環境:

```bash
env.bat
```

Linux環境:

```bash
env.sh
```

### サーバーを起動する

コマンドプロンプトから次のコマンドを実行し、サーバーを起動する。

開発版（ソースコード編集内容が自動的に反映される）:

```bash
uvicorn main:app --reload
```

本番環境:

```bash
uvicorn main:app
```

デフォルトのポート番号は8000。ポート番号を指定するときは --port [ポート番号] を後ろに付与する。

### サーバーへアクセスする

Webブラウザを開き、次のURLへアクセスする（ポート番号が8000の場合）。

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

トップページが現れる。

### 環境件数

このサーバーは起動時に環境変数を参照する。環境変数は env.batあるいはenv.shに設定されている。

|  環境変数名 |  説明  |
| ---- | ---- |
|  OPENMETEO_REST_URL  | Open Meteo REST APIへアクセスするルートURL |

### REST APIs

このサーバーが提供するREST APIエンドポイントは、ある定型的なJSON構造を返却する。その構造は、株式会社MetaMoJiの製品 **eYACHO** および **GEMBA Note**の開発者オプションのアグリゲーション検索条件を構成する **RESTコネクタ** の仕様に基づく。

REST用アグリゲーションの出力構造：

```bash
{
   'keys': ['key1', 'key2', ... 'keyN'], # recordsの中で用いるキーの一覧
   'records': [
       {'key1': value-11, 'key2': value-21, ... 'keyN': value-N1}, 
       {'key1': value-12, 'key2': value-22, ... 'keyN': value-N2}, 
       ...,
       {'key1': value-1m, 'key2': value-2m, ... 'keyN': value-Nm}, 
   ],
   'message': エラーメッセージ or null(success)
}
```

#### /rest/temperature

指定した緯度と経度からその地点の気温の予測データを取得する。

リクエストの仕様：

|  メソッド |  リクエスト1  |  リクエスト2  |
| ---- | ---- | ---- |
|  GET | latitude | longitude |
|  説明 | 予測する地点の緯度（必須）| 予測する地点の経度（必須）|

レスポンスの仕様:

|  キー  | 説明  |
| ---- | ---- |
| datetime | 予測日時（UNIXタイムスタンプ） |
| temperature | 指定した地点の予測気温 |

レスポンス例:

```bash
{
   'keys': ['datetime', 'temperature'], 
   'records': [
       {'datetime': 1724943600, 'temperature': 28.5},  
       {'datetime': 1724947200, 'temperature': 29.2},  
       ...
   ],
   'message': null
}
```

#### /rest/test

サーバーが起動しているか確認するテストのエンドポイント

リクエストの仕様：

|  メソッド |  リクエスト |
| ---- | ---- |
|  GET | なし |

レスポンスの仕様:

|  キー  | 説明  |
| ---- | ---- |
| city | 都市名 |
| latitude | その都市の（都庁や府庁所在地の）緯度 |
| longitude | その都市の（都庁や府庁所在地の）経度 |

レスポンス例:

```bash
{
   'keys': ['city', 'latitude', 'longitude'], 
   'records': [
       {'city': 'tokyo', 'latitude': 35.6895014, 'longitude': 139.6917337}, 
       {'city': 'osaka', 'latitude': 34.686344, 'longitude': 135.520037} 
       ...
   ],
   'message': null
}
```

### Webブラウザでのテスト

サーバーを起動した後で、Webブラウザを開き、次のURLへアクセスしてみる[1]。

[http://localhost:8000/rest/test](http://localhost:8000/rest/test)

[http://localhost:8000/rest/temperature?latitude=35.6785&longitude=139.6823](http://localhost:8000/rest/temperature?latitude=35.6785&longitude=139.6823)

[1] サーバーのポート番号を変更した場合は、アクセスするURLのポート番号も変更する

### eYACHO/GEMBA Noteとのデータ連携テスト

- packageフォルダ以下にある開発パッケージのバックアップファイル（Open_Meteo__<バージョン>__backup.gncproj）をeYACHO/GEMBA Noteに復元する
- サーバーが起動していることを確認する
- 開発パッケージフォルダ上にある「天気予測」ノートを開く
- 「最新に更新」ボタンをクリックし、本日の気温予測が一覧表示されることを確認する[2]

[2] サーバーのポート番号を変更した場合は、アグリゲーション検索条件「forecastTemperature」のコネクタ定義にある **URL** を変更する。

### 更新履歴

- 2024-09-30 - 初回リリース
