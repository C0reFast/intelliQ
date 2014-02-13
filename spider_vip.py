#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from urlparse import urlsplit
from pyquery import PyQuery as pq
from common import Paper
import spider
import solr


PAPER_PATH_RE = re.compile('href="(/qk/.+?.html)"')
PAPER_ID_RE = re.compile('/(\d+)\.html')
NUM_RE = re.compile('search_jg2">(\d+)')
SUB_URL = ('http://lib.cqvip.com/zk/search.aspx?E=%s&M=&P=%d'
           '&CP=&CC=&LC=&H=%s&Entry=M&S=1&SJ=&ZJ=&GC=&Type=')
PAPER_URL = 'http://lib.cqvip.com%s'
PAPER_ID_RE = re.compile('/(\d+)\.html')
keyword = '%28Keyword_C%3D%E6%98%8E%E7%9F%BE%2BTitle_C%3D%E6%98%8E%E7%9F%BE%29'
company_id = 1


def page_parser(url, page_content):
    """docstring for page_parser"""
    paths = PAPER_PATH_RE.findall(page_content)
    for path in paths:
        try:
            paper_id = PAPER_ID_RE.search(path).group(1)
            paper = solr.find_paper(paper_id)
            if paper:
                paper.add_company(company_id)
                solr.add_paper(paper)
                print PAPER_ID_RE.search(path).group(1), 'old'
            else:
                spider.queue.put(spider.Request(url=PAPER_URL % (path),
                                                parser=content_parser))
        except Exception:
            print 'err', path


def seed_parser(url, page_content):
    """docstring for seed_parser"""
    page_count = int(NUM_RE.search(page_content).group(1)) / 20 + 2
    for i in xrange(1, page_count):
        spider.queue.put(spider.Request(url=SUB_URL % (keyword, i, keyword), parser=page_parser))


def content_parser(url, page_content):
    """docstring for content_parser"""
    p = pq(page_content)
    paper = Paper(paper_id=PAPER_ID_RE.search(url).group(1),
                  company_ids=[company_id],
                  path=urlsplit(url).path,
                  title=p('h1').text() or 'null',
                  author=(p('.author a').text() or '').split(),
                  abstract=p('.abstrack').remove('strong').text() or '',
                  keywords=(p('.keywords a').text() or '').split(),
                  paper_class=p('#wxClass').attr.value or 'null'
                  )
    try:
        solr.add_paper(paper)
        print paper._path, 'new'
    except:
        'err adding', paper._path

if __name__ == '__main__':
    seed = spider.Request(url=SUB_URL % (keyword, company_id, keyword), parser=seed_parser)
    spider.queue.put(seed)
    spider.crawl()
