# KoikatuUploadServer
an alternative character upload server for Koikatu.
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
python 3.xとdocker-composeが使える環境が必要
```
$ git clone https://github.com/great-majority/KoikatuUploadServer
$ cd KoikatuUploadServer
$ pip install -r requirements.txt
$ docker-compose up -d
$ ./main.py
```
