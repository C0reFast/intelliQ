#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from urlparse import urlsplit
from pyquery import PyQuery as pq
from common import Link
import spider
import analyzer
import urlset


def get_links(url, page_content):
    """@todo: Docstring for get_links.

    :url: @todo
    :page_content: @todo
    :returns: @todo

    """
    host = urlsplit(url).netloc
    p = pq(page_content)
    p.make_links_absolute(url)
    links = []
    for a in p('a'):
        href = a.attrib['href']
        url = urlsplit(href)
        if url.netloc == host and not urlset.has_url(host, url.path):
            links.append(Link(url=href, text=a.text))
    return links


def parser(url, page_content):
    """docstring for page_parser"""
    pass


if __name__ == '__main__':
    pass
