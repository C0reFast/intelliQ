#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import pysolr
from urlparse import urlsplit
import spider
from pyquery import PyQuery as pq
import helpers
import analyzer


def parser(url, page_content):
    """docstring for page_parser"""
    p = pq(page_content)
    p



# keyword = '%28Keyword_C%3D%E9%94%82%E7%94%B5%E6%B1%A0%2BTitle_\
#        C%3D%E9%94%82%E7%94%B5%E6%B1%A0%29'
# sp = VipPaperUrlSpider(company_id=1, keyword=keyword)
# sp.crawl([Request(url=sp.SUB_URL % (sp.keyword, 1, sp.keyword), parser=sp.seed_parser)])
