# -*- coding:utf-8 -*-

import tornado.web
import logging
import base64
import io
from db_client import db_client
from PIL import Image
from settings import THUMBNAIL_SIZE

required_b64 = ["birthday", "chara_name", "nickname", "handlename", "products_description"]
charadata_order = ["id", "sex", "height", "bust", "hair", "personality", "blood", "birthday", "club", "chara_name", "nickname", "handlename", "products_description", "uid", "download_num","weekly_download_num"]
charadata =       ["sex", "height", "bust", "hair", "personality", "blood", "birthday", "club", "chara_name", "nickname", "handlename", "products_description", "uid"]

class Uploader(tornado.web.RequestHandler):
    def get(self):
        self.write("nothing here.")

    def post(self):
        mode = None
        try:
            mode = int(self.get_argument('mode'))
        except tornado.web.MissingArgumentError:
            pass

        # ランキングの全取得
        if mode == 1:
            self.write(self._get_all_charas())
        # サムネイルをダウンロード
        elif mode == 2:
            ids = self.get_argument("pid").split("\n")
            self.write(self._download_thumb(ids))
        # 画像のアップロード
        elif mode == 3:
            c = {}
            for i in charadata:
                c[i] = self.get_argument(i)
            for i in required_b64:
                c[i] = base64.b64decode(c[i]).decode("utf-8")
            image = self.request.files["png"][0]["body"]
            self.write(str(self._upload_image(c, image)))
        # 画像本体をダウンロード
        elif mode == 4:
            id = int(self.get_argument("pid"))
            self.write(self._image_download(id))
        # 画像の削除
        elif mode == 5:
            id = int(self.get_argument("pid"))
            uid = self.get_argument("uid")
            self._delete_image(id, uid)
            self.write("")

    def _get_all_charas(self):
        db = db_client()
        charas = db.get_data()
        charas_line = []
        for i,c in enumerate(charas):
            charas[i] = self._chara_b64encode(charas[i])
            charadata_list = []
            for k in charadata_order:
                charadata_list.append(charas[i][k])
            charas_line.append("\t".join(charadata_list))
        txt = "\n".join(charas_line)
        return txt
    
    def _upload_image(self, c, png):
        db = db_client()
        # 画像の圧縮
        orig_img = io.BytesIO(png)
        resized_img = io.BytesIO()
        Image.open(orig_img).resize(THUMBNAIL_SIZE, Image.BICUBIC).save(resized_img, "PNG")
        thumb_img = base64.b64encode(resized_img.getvalue())
        return db.add(c, png, thumb_img)

    def _download_thumb(self, ids):
        db = db_client()
        text = []
        for i in ids:
            text.append(db.get_thumb(i))
        return "\n".join(text)

    def _image_download(self, id):
        db = db_client()
        db.incr_down_count(id)
        return base64.b64encode(db.get_image(id)).decode("utf-8")

    def _delete_image(self, id, uid):
        db = db_client()
        img_data = db.get_data([id])
        if img_data[0]["uid"] == uid:
            db.delete(id)

    def _chara_b64encode(self, c):
        for i in required_b64:
            c[i] = base64.b64encode(c[i].encode("utf-8")).decode("utf-8")
        return c