import Queue
import threading
import requests


class Request(object):
    def __init__(self, url, parser, fetcher=None):
        self._url = url
        self._parser = parser
        self._fetcher = fetcher or (lambda url: (requests.get(url).text))

    def parse(self):
        self._parser(self._url, self._fetcher(self._url))

queue = Queue.Queue(maxsize=0)
thread_number = 5
thread_pool = []


def work():
    while True:
        req = queue.get()
        try:
            req.parse()
        except Exception, e:
            raise e
        finally:
            queue.task_done()


def crawl():
    for i in xrange(thread_number):
        t = threading.Thread(target=work)
        t.setDaemon(True)
        thread_pool.append(t)
        t.start()
    queue.join()
