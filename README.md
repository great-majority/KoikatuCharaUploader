# KoikatuUploadServer
コイカツのキャラクターアップローダーを自前で用意できるようにするもの.

# ゲーム中からアクセスする
```
@echo off
set HTTP_PROXY=(サーバのアドレス):(ポート)
Koikatu.exe
```
このようなバッチファイルを `Koikatu.exe` があるフォルダにいれて保存し実行すればOK
念の為 `UserData/save/netUID.dat` を公式ロダのとは違うのにしておくといいかも

# 使い方
```
$ git clone https://github.com/106-/koikatu
$ cd koikatu
$ pip install -r requirements.txt
$ docker-compose up -d
$ ./main.py
```