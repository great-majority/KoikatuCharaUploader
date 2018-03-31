#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import tornado
import logging
from tornado.web import HostMatches
from uploader import Uploader
from check import Check
from settings import APP_PORT

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=logging.DEBUG)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = tornado.web.Application([
        #(HostMatches("up.illusion.jp"),[("/koikatu_upload/chara/master/unity/koikatu_getChara.php", Uploader)]),
        #(HostMatches("www.illusion.jp"),[("/check/koikatu/check.php", Check)])
        (HostMatches("up.illusion.jp"),[(".*", Uploader)]),
        (HostMatches("www.illusion.jp"),[(".*", Check)])
        # ("/koikatu_upload/chara/master/unity/koikatu_getChara.php", Uploader),
        # (".*", Check)
    ])
    app.listen(APP_PORT)

    try:
        logging.info("server is up.")
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("interrupted.")

if __name__=='__main__':
    main()