#!/usr/bin/env python
# encoding: utf-8

import redis
from .. import config

r = redis.StrictRedis(host=config.redis_host,
                      port=config.redis_port,
                      db=config.redis_db)


def setup_function(function):
    r.sadd('test', 'a', 'b')


def teardown_function(function):
    r.delete('test')


def test_redis_set():
    assert r.sismember('test', 'a')
    assert not r.sismember('test', 'c')
