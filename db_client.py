# -*- coding:utf-8 -*-

import threading
import redis
from settings import ID_INITIAL_VALUE, REDIS_HOST, REDIS_PORT

# 存在するidのset
redis_chara_set_key = "koikatu:chara"
# キャラ単体の情報を入れてくhashmap
redis_chara_key = "koikatu:chara:{}"
# 画像本体
redis_image_key = "koikatu:chara:{}:image"
redis_thumb_b64_key = "koikatu:chara:{}:thumb"
redis_thumb_key = "koikatu:chara:{}:thumb"

class db_client:
    _instance = None
    _redis = None
    _lock = threading.Lock()

    def __new__(self):
        if not self._instance:
            self._lock.acquire()
            self._instance = super().__new__(self)
            self._redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, charset="utf-8")
            self._lock.release()
        return self._instance

    def add(self, chara, image, thumb):
        if not self._redis.exists("koikatu:next_id"):
            self._redis.set("koikatu:next_id", ID_INITIAL_VALUE)
        id = self._redis.incr("koikatu:next_id")
        c = {
            "id":id,
            "download_num": 0,
            "weekly_download_num": 0,
        }
        chara.update(c)
        self._redis.sadd(redis_chara_set_key, id)
        self._redis.hmset(redis_chara_key.format(id), chara)
        self._redis.set(redis_image_key.format(id), image)
        self._redis.set(redis_thumb_key.format(id), thumb)
        return id
    
    def get_data(self, ids=None):
        if ids==None:
            ids = self._redis.smembers(redis_chara_set_key)
        charas = []
        for id in ids:
            chara_bin = self._redis.hgetall(redis_chara_key.format(int(id)))
            c = {}
            for i in chara_bin:
                if not hasattr(i, "decode"):
                    continue
                c[i.decode("utf-8")] = chara_bin[i].decode("utf-8")
            charas.append(c)
        return charas

    def get_thumb(self, id):
        if self._redis.exists(redis_thumb_key.format(id)):
            return self._redis.get(redis_thumb_key.format(id)).decode("utf-8")
        else:
            return None

    def get_image(self, id):
        if self._redis.exists(redis_image_key.format(id)):
            return self._redis.get(redis_image_key.format(id))
        else:
            return None
    
    def incr_down_count(self, id):
        if self._redis.exists(redis_chara_key.format(id)):
            self._redis.hincrby(redis_chara_key.format(id), "download_num", 1)
            

    def delete(self, id):
        self._redis.delete(redis_chara_key.format(id))
        self._redis.delete(redis_image_key.format(id))
        self._redis.delete(redis_thumb_key.format(id))
        self._redis.srem(redis_chara_set_key, id)