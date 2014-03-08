#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import time
import urllib2
import requests
from urlparse import urlsplit
from pyquery import PyQuery as pq
import common
from common import Paper
from spider import Request
import solr
import urlset
from text_extractor import extract


common.monkey_patch_requests()

PAPER_PATH_RE = re.compile('href="(/qk/.+?.html)"')
PAPER_ID_RE = re.compile('/(\d+)\.html')
NUM_RE = re.compile('search_jg2">(\d+)')
SUB_URL = ('http://lib.cqvip.com/zk/search.aspx?E={search_exp}&M=&P={page}'
           '&CP=&CC=&LC=&H={search_exp}&Entry=M&S=1&SJ=&ZJ=&GC=&Type=')
PAPER_URL = 'http://lib.cqvip.com{path}'
PAPER_ID_RE = re.compile('/(\d+)\.html')


def page_parser(search_exp):
    """docstring for seed_parser"""
    search_exp = urllib2.quote(search_exp.encode('utf-8'))
    page_content = requests.get(SUB_URL.format(search_exp=search_exp, page=1)).text
    page_count = int(NUM_RE.search(page_content).group(1)) / 20 + 2
    result = []
    for i in xrange(1, page_count):
        result.append(Request(url=SUB_URL.format(search_exp=search_exp, page=i),
                              parser=paper_parser))
    return result


def paper_parser(url):
    """docstring for content_parser"""
    page_content = requests.get(url).text
    paths = PAPER_PATH_RE.findall(page_content)
    paper_list = []
    for path in paths:
        if urlset.has_url('paper', path):
            print path, 'old'    # @todo logs
        else:
            p = pq(PAPER_URL.format(path=path))
            paper_list.append(Paper(id=PAPER_ID_RE.search(path).group(1),
                                    path=urlsplit(url).path,
                                    title=p('h1').text() or 'null',
                                    author=(p('.author a').text() or '').split(),
                                    abstract=p('.abstrack').remove('strong').text() or '',
                                    keywords=(p('.keywords a').text() or '').split(),
                                    classification=p('#wxClass').attr.value or 'null',
                                    update_time=time.strftime('%Y-%m-%dT%XZ')))
            print path, 'new'    # @todo logs
    try:
        solr.add('paper', paper_list)
    except:
        'err adding paper'


def news_parser(url):
    """新闻解析器，从指定Url中获取新闻存入Solr"""
    links = common.get_links(url)
    news_list = []
    for link in links:
        if not urlset.has_url('news', link.url):
            news_list.append(common.News(url=link.url,
                                         title=link.title,
                                         content=extract(requests.get(link.url).text),
                                         update_time=time.strftime('%Y-%m-%dT%XZ')))
            print 'content', link.url
    solr.add('news', news_list)

if __name__ == '__main__':
    pass
