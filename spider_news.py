#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from urlparse import urlsplit
from pyquery import PyQuery as pq
from common import Link
import spider
import analyzer
import urlset


def get_links(host, page_content):
    """@todo: Docstring for get_links.

    :host: @todo
    :page_content: @todo
    :returns: @todo

    """
    p = pq(page_content)
    p.make_links_absolute()
    links = []
    for a in p('a'):
        url = urlsplit(a.attrib['href'])
        if url.netloc == host:
            links.append(Link(host=url.netloc, path=url.path, text=a.text))
    return links


def parser(url, page_content):
    """docstring for page_parser"""
    pass


if __name__ == '__main__':
    pass
