# -*- coding:utf-8 -*-

import tornado.web

class Check(tornado.web.RequestHandler):
    def get(self):
        self.write("2\tネットワークサービスの情報を特定出来ませんでした。")
    def post(self):
        self.write("0\tただいまアクセスが集中し、大変込み合っております。\nネットワークの接続に失敗した場合は恐れ入りますが\n時間を空けて再度ご利用いただけますようお願いします。")
