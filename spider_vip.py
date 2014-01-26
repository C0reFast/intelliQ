#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import pysolr
from urlparse import urlsplit
import spider
from pyquery import PyQuery as pq
import helpers


PAPER_PATH_RE = re.compile('href="(/qk/.+?.html)"')
PAPER_ID_RE = re.compile('/(\d+)\.html')
NUM_RE = re.compile('search_jg2">(\d+)')
SUB_URL = ('http://202.195.136.17/zk/search.aspx?E=%s&M=&P=%d'
           '&CP=&CC=&LC=&H=%s&Entry=M&S=1&SJ=&ZJ=&GC=&Type=')
PAPER_ID_RE = re.compile('/(\d+)\.html')
solr = pysolr.Solr('http://localhost:8983/solr/vip_papers/')


def page_parser(url, page_content):
    """docstring for page_parser"""
    paths = PAPER_PATH_RE.findall(page_content)
    for i in paths:
        try:
            print PAPER_ID_RE.search(i).group(1), i
        except Exception:
            pass


def seed_parser(url, page_content):
    """docstring for seed_parser"""
    page_count = int(NUM_RE.search(page_content).group(1)) / 20 + 2
    for i in xrange(1, page_count):
        pass


def content_parser(url, page_content):
    """docstring for content_parser"""
    doc = {}
    p = pq(page_content)
    doc['id'] = '4' + PAPER_ID_RE.search(url).group(1)
    doc['path'] = urlsplit(url).path
    doc['title'] = p('h1').text() or 'null'
    doc['author'] = p('.author a').text() or 'null'
    doc['abstract'] = p('.abstrack').remove('strong').text() or 'null'
    doc['keywords'] = p('.keywords a').text() or 'null'
    doc['class'] = p('#wxClass').attr.value or 'null'
    doc['company_id'] = '4'
    try:
        solr.add((doc,))
        print doc['id']
    except:
        pass


# keyword = '%28Keyword_C%3D%E9%94%82%E7%94%B5%E6%B1%A0%2BTitle_\
#        C%3D%E9%94%82%E7%94%B5%E6%B1%A0%29'
# sp = VipPaperUrlSpider(company_id=1, keyword=keyword)
# sp.crawl([Request(url=sp.SUB_URL % (sp.keyword, 1, sp.keyword), parser=sp.seed_parser)])
