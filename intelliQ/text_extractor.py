#!/usr/bin/env python
# encoding: utf-8

from pyquery import PyQuery as pq
from lxml.html.clean import clean_html
import re


# 需要删除的一些内联标签
DEL_TAG_RE = [re.compile('<{name}.*?>|</{name}>'.format(name=name), re.IGNORECASE)
              for name in ('span', 'b', 'u', 'i', 'a', 'font', 'strong')]


def extract(page_content):
    """根据网页源代码解析网页主体内容"""
    page_content = clean_html(page_content)
    for r in DEL_TAG_RE:
        page_content = r.sub('', page_content)
    p = pq(page_content)
    p('script').remove()
    p('style').remove()
    pags = p.text().split(' ')
    return '\n'.join([x for x in pags if len(x) > 76])
