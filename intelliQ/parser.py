#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import time
import urllib2
import requests
from pyquery import PyQuery as pq
import common
from common import Paper, News, Patent
from spider import Request
import solr
import urlset
from text_extractor import extract


common.monkey_patch_requests()

PAPER_PATH_RE = re.compile('href="(/qk/.+?.html)"')
PAPER_ID_RE = re.compile('/(\d+)\.html')
NUM_RE = re.compile('search_jg2">(\d+)')
PAPER_ID_RE = re.compile('/(\d+)\.html')

PATENT_CATEGORY_RE = re.compile('/IPC/Code/(.+?)')
PATENT_PATH_RE = re.compile('/Patent/\d+\?lx=\w+')
PATENT_ID_RE = re.compile('/Patent/(\d+)')
PATENT_COUNT_RE = re.compile('ttl="(\d+)"')

PAPER_SEARCH_URL = ('http://lib.cqvip.com/zk/search.aspx?E={search_exp}&M=&P={page}'
                    '&CP=&CC=&LC=&H={search_exp}&Entry=M&S=1&SJ=&ZJ=&GC=&Type=')
PAPER_URL = 'http://lib.cqvip.com{path}'
PATENT_SEARCH_URL = ('http://www.soopat.com/Home/Result?SearchWord={search_key}'
                     '&FMSQ=Y&PatentIndex={index}&View=7')
PATENT_URL = 'http://www.soopat.com{path}'


def paper_page_parser(search_exp):
    """docstring for paper_page_parser"""
    search_exp = urllib2.quote(search_exp.encode('utf-8'))
    page_content = requests.get(PAPER_SEARCH_URL.format(search_exp=search_exp, page=1)).text
    page_count = int(NUM_RE.search(page_content).group(1)) / 20 + 2
    result = []
    for i in xrange(1, page_count):
        result.append(Request(url=PAPER_SEARCH_URL.format(search_exp=search_exp, page=i),
                              parser=paper_parser))
    return result


def paper_parser(url):
    """docstring for content_parser"""
    page_content = requests.get(url).text
    paths = PAPER_PATH_RE.findall(page_content)
    paper_list = []
    for path in paths:
        if urlset.has_url('paper', path):
            pass
            #print path, 'old'    # @todo logs
        else:
            p = pq(PAPER_URL.format(path=path))
            paper_list.append(Paper(id=PAPER_ID_RE.search(path).group(1),
                                    path=path,
                                    title=p('h1').text() or 'null',
                                    author=(p('.author a').text() or '').split(),
                                    abstract=p('.abstrack').remove('strong').text() or '',
                                    keywords=(p('.keywords a').text() or '').split(),
                                    classification=p('#wxClass').attr.value or 'null',
                                    category=u'默认',
                                    update_time=time.strftime('%Y-%m-%dT%XZ', time.gmtime())))
            print path, 'new'    # @todo logs
    try:
        solr.add('paper', paper_list)
    except:
        'err adding paper'


def news_parser(url):
    """新闻解析器，从指定Url中获取新闻存入Solr"""
    links = common.get_links(url)
    news_list = []
    for link in reversed(links):
        if not urlset.has_url('news', link.url):
            try:
                news_list.append(News(url=link.url,
                                 title=link.title,
                                 content=extract(requests.get(link.url).text),
                                 category=u'默认',
                                 update_time=time.strftime('%Y-%m-%dT%XZ', time.gmtime())))
            except:
                print 'error adding', link.url
            print 'content', link.url
    try:
        solr.add('news', news_list)
    except:
        print 'error adding news'


def patent_page_parser(search_key):
    """@todo: Docstring for patent_page_parser.
    """
    search_key = urllib2.quote(search_key.encode('utf-8'))
    page_content = requests.get(PATENT_SEARCH_URL.format(search_key=search_key, index=0)).text
    count = int(PATENT_COUNT_RE.search(page_content).group(1))
    print count
    result = []
    for index in [30 * x for x in range(count / 30 + 1)]:
        result.append(Request(url=PATENT_SEARCH_URL.format(search_key=search_key, index=index),
                              parser=patent_parser))
    return result


def patent_parser(url):
    """@todo: Docstring for patent_parser.
    """
    page_content = requests.get(url).text
    paths = PATENT_PATH_RE.findall(page_content)
    patent_list = []
    for path in paths:
        if urlset.has_url('patent', path):
            pass
            #print path, 'old'    # @todo logs
        else:
            try:
                p = pq(PATENT_URL.format(path=path))
                patent = Patent(id=PATENT_ID_RE.search(path).group(1),
                                path=path,
                                title=p('h1').text().split()[0],
                                abstract=p('.datainfo td').eq(0).remove('b').text(),
                                inventor=p('.datainfo td').eq(3).remove('b').text().split(),
                                applicant=p('.datainfo td').eq(1).remove('b').text(),
                                category=p('.datainfo td').eq(5).remove('b').text().split(),
                                update_time=time.strftime('%Y-%m-%dT%XZ', time.gmtime()))
                patent_list.append(patent)
                print path, 'new'    # @todo logs
            except:
                print p.text()
    try:
        solr.add('patent', patent_list)
    except:
        'err adding patent'


if __name__ == '__main__':
    pass
