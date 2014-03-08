#!/usr/bin/env python
# encoding: utf-8


import Queue
import threading


class Request(object):
    def __init__(self, url, parser, retries=3):
        self._url = url
        self._parser = parser
        self._retries = retries

    def parse(self):
        if self._retries > 0:
            self._retries -= 1
            self._parser(self._url)


class Spider(object):

    """网络爬虫类"""

    def __init__(self, name, thread_number=5):
        """构造函数
        :name: 名字
        :thread_number: 最大线程数
        """
        self._name = name
        self._thread_number = thread_number
        self._queue = Queue.Queue(maxsize=0)
        self._thread_pool = []

    def __work(self):
        """工作函数，处理队列中请求
        """
        while True:
            req = self._queue.get()
            try:
                req.parse()
            except Exception as e:
                self._queue.put(req)
                print e
            finally:
                self._queue.task_done()

    def crawl(self):
        """初始化线程，爬取数据
        """
        for i in xrange(self._thread_number):
            t = threading.Thread(target=self.__work)
            t.setDaemon(True)
            self._thread_pool.append(t)
            t.start()
        self._queue.join()

    def add_request(self, req):
        """添加请求
        :req: 要添加的请求
        """
        self._queue.put(req)
