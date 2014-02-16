#!/usr/bin/env python
#-*- coding:utf-8 -*-

import hashlib
import redis
import config

r = redis.StrictRedis(host=config.redis_host,
                      port=config.redis_port,
                      db=config.redis_db)


def has_url(set_name, url):
    """查找集合中是否存在Url，存在返回True，不存在添加并返回False

    :set_name: 集合名称
    :url: @todo要检测的Url
    :returns: True或者False

    """
    m = hashlib.md5()
    m.update(url)
    if r.sismember(set_name, m.hexdigest()):
        return True
    else:
        r.sadd(set_name, m.hexdigest())
        return False
