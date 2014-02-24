import Queue
import threading
import requests
from common import monkey_patch_requests

monkey_patch_requests()


class Request(object):
    def __init__(self, url, parser, fetcher=None, retries=3):
        self._url = url
        self._parser = parser
        self._fetcher = fetcher or (lambda url: (requests.get(url).text))
        self._retries = retries

    def parse(self):
        if self._retries > 0:
            self._retries -= 1
            self._parser(self._url, self._fetcher(self._url))

queue = Queue.Queue(maxsize=0)
thread_number = 5
thread_pool = []


def work():
    while True:
        req = queue.get()
        try:
            req.parse()
        except Exception:
            queue.put(req)
        finally:
            queue.task_done()


def crawl():
    for i in xrange(thread_number):
        t = threading.Thread(target=work)
        t.setDaemon(True)
        thread_pool.append(t)
        t.start()
    queue.join()
