#!/usr/bin/env python
# encoding: utf-8

import hashlib
import redis
from .. import config
from .. import urlset

r = redis.StrictRedis(host=config.redis_host,
                      port=config.redis_port,
                      db=config.redis_db)


def setup_function(function):
    m = hashlib.md5()
    m.update('www.baidu.com')
    r.sadd('test', m.hexdigest())


def teardown_function(function):
    r.delete('test')


def test_redis_set():
    assert urlset.has_url('test', 'www.baidu.com')
    assert not urlset.has_url('test', 'www.qq.com')
    assert urlset.has_url('test', 'www.qq.com')
