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

コマンドの説明:

| コマンドの要素 | 説明 |
| ---- | ---- |
| uvicorn | FastAPIベースの非同期Python Webアプリケーションを実行する |
| main:app | Pythonファイルmain.pyの中で、FastAPIが生成する変数がapp |
| --reload | 実行中にソースコードが変更されたとき、サーバーが自動的にリロードされる |

デフォルトのポート番号は **8000**。  
ポート番号を指定するときは **--port [ポート番号]** を後ろに付与する。

### サーバーへアクセスする

Webブラウザを開き、次のURLへアクセスする（ポート番号が8000の場合）。

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

トップページが現れる。

### 環境件数

このサーバーは起動時に以下の環境変数を参照する。環境変数は **env.tpl** に定義されている。サーバーを起動する前に、プログラムが読み込めるようにこのファイル名を **.env** に変更する。

| 環境変数名 | 説明 |
| ---- | ---- |
| OPENMETEO_REST_URL | Open Meteo REST APIへアクセスするルートURL |
| OPENMETEO_TZ | Open Meteo REST APIへ渡すタイムゾーン（例：Asia/Tokyo） |

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

#### /rest/cities

いくつかの都庁、府庁、県庁の緯度と経度を取得する。サーバーが起動しているか確認するテストのエンドポイント

リクエストの仕様：

| メソッド | リクエスト |
| ---- | ---- |
| GET | なし |

レスポンスの仕様:

| キー | 説明 |
| ---- | ---- |
| city | 都市名 |
| latitude | その都市の（都庁や府庁所在地の）緯度 |
| longitude | その都市の（都庁や府庁所在地の）経度 |

レスポンス例:

```bash
{
   'keys': ['city', 'latitude', 'longitude'], 
   'records': [
       {'city': '新宿区', 'latitude': 35.689501, 'longitude': 139.691722}, 
       {'city': '大阪市', 'latitude': 34.686344, 'longitude': 135.520037} 
       ...
   ],
   'message': null
}
```

#### /rest/server_info

このサーバーが何者かを提示するメソッド。eYACHO/GEMBA Noteアプリ上でダイアログにメッセージを表示する例。

リクエストボディの仕様：

| メソッド | ボディ |
| ---- | ---- |
| POST | 特に不要 |
| 説明 | 存在すればコンソール上に表示 |

レスポンスの仕様:

| キー | 説明 |
| ---- | ---- |
| message | 表示するメッセージ |

レスポンス例:

```bash
{
  'message': 'Hello, I am a Python server!'
}
```

#### /rest/weather

指定した緯度と経度からその地点の天気と気温の予測データを1週間分（1時間ごと）取得する。

リクエストの仕様：

| メソッド | リクエスト1 | リクエスト2 |
| ---- | ---- | ---- |
| GET | latitude | longitude |
| 説明 | 予測する地点の緯度（必須） | 予測する地点の経度（必須） |

レスポンスの仕様:

| キー | 説明 |
| ---- | ---- |
| datetime | 予測日時（UNIXタイムスタンプ） |
| temperature | 指定した地点の予測気温 |
| weather | 指定した地点の予測天気 |

レスポンス例:

```bash
{
   'keys': ['datetime', 'temperature', 'weather'], 
   'records': [
       {'datetime': 1724943600, 'temperature': 28.5, 'weather': '晴れ'},  
       {'datetime': 1724947200, 'temperature': 29.2, 'weather': '快晴'},  
       ...
   ],
   'message': null
}
```

### Webブラウザでのテスト

サーバーを起動した後で、Webブラウザを開き、次のURLへアクセスしてみる[1]。

[http://localhost:8000/rest/cities](http://localhost:8000/rest/cities)

[http://localhost:8000/rest/weather?latitude=35.6785&longitude=139.6823](http://localhost:8000/rest/weather?latitude=35.6785&longitude=139.6823)

[1] サーバーのポート番号を変更した場合は、アクセスするURLのポート番号も変更する

### eYACHO/GEMBA Noteとのデータ連携テスト

- packageフォルダ以下にある開発パッケージのバックアップファイル（Open_Meteo__<バージョン>__backup.gncproj）をeYACHO/GEMBA Noteに復元する。
- サーバーが起動していることを確認する。
  - Windowsアプリからローカルサーバーにアクセスする場合は、管理者モードで利用対象アプリのループバックを有効にする → [Windowsで開発する際の注意点](./NoticesForWindows.md)
- 開発パッケージフォルダ上にある **天気予測** ノートを開く。
- アグリゲーション検索条件 **forecastWeather** のコネクタ定義にある **URL** を確認する。
  - 起動したサーバーと異なる場合は修正する。
- 自由ページにある **天気予測** ページ上の **更新** ボタンをクリックする
  - 現日時以降の気温と天気の予測が24時間分（1時間おき）一覧表示されることを確認する。
- 同ページ右上にある **サーバー情報** をクリックするとダイアログ上にメッセージが表示される。

### 更新履歴

- 2026-04-22 Starlette仕様変更に伴う改修
- 2025-10-23 V7に伴う修正
- 2025-04-24 python-dotenvによる環境変数の参照
- 2024-10-11 天気を追加、ループバック有効を追記
- 2024-09-30 初回リリース
