#!/usr/bin/env python
#-*- coding:utf-8 -*-

from urlparse import urlsplit
from pyquery import PyQuery as pq
from common import Link
import text_extractor
import spider
import analyzer
import urlset


keywords = u'船'


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


def content_parser(url, page_content):
    text = text_extractor.extract(page_content)
    print url, text
    print '============================'


def parser(url, page_content):
    """docstring for page_parser"""
    links = get_links(url, page_content)
    for link in links:
        if link.text and analyzer.analyze(link.text, keywords):
            spider.queue.put(spider.Request(url=link.url, parser=content_parser))
            print 'content', link.url
        else:
            spider.queue.put(spider.Request(url=link.url, parser=parser))
            print 'page', link.url


if __name__ == '__main__':
    seed_url = 'http://www.zjt.gov.cn/'
    spider.queue.put(spider.Request(url=seed_url, parser=parser))
    spider.crawl()
