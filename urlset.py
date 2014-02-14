#!/usr/bin/env python
#-*- coding:utf-8 -*-

import hashlib
import redis
import config

r = redis.StrictRedis(host=config.redis_host,
                      port=config.redis_port,
                      db=config.redis_db)


def has_url(set_name, url):
    """@todo: Docstring for has_url.

    :set_name: @todo
    :url: @todo
    :returns: @todo

    """
    m = hashlib.md5()
    m.update(url)
    if r.sismember(set_name, m.hexdigest()):
        return True
    else:
        r.sadd(set_name, m.hexdigest())
        return False
