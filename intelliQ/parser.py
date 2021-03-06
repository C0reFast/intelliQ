#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import time
import urllib2
import requests
from pyquery import PyQuery as pq
from splinter import Browser
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

PAPER_SEARCH_URL = ('http://lib.cqvip.com/zk/search.aspx?E={search_exp}&M=&P={page}'
                    '&CP=&CC=&LC=&H={search_exp}&Entry=M&S=1&SJ=&ZJ=&GC=&Type=')
PAPER_URL = 'http://lib.cqvip.com{path}'


def paper_page_parser(search_exp):
    """docstring for paper_page_parser"""
    search_exp = urllib2.quote(search_exp.encode('utf-8'))
    page_content = requests.get(PAPER_SEARCH_URL.format(search_exp=search_exp, page=1)).text
    page_count = int(NUM_RE.search(page_content).group(1)) / 20 + 2
    result = []
    for i in xrange(1, page_count):
        result.append(Request(arg=PAPER_SEARCH_URL.format(search_exp=search_exp, page=i),
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


def patent_parser(search_exp):
    """@todo: Docstring for patent_parser.
    """
    patent_list = []
    b = Browser("phantomjs")
    b.reload()
    b.visit('http://www.pss-system.gov.cn/sipopublicsearch/search/searchHome-searchIndex.shtml')
    b.fill('searchInfo', search_exp)
    b.click_link_by_text(u'检索')
    b.is_element_not_present_by_css('.s_c_conter', wait_time=8)
    for _ in xrange(10):
        item_list = b.find_by_css('.s_c_conter')
        for item in item_list:
            info_list = item.find_by_tag('td')
            if not urlset.has_url('patent', info_list[0].text[6:]):
                try:
                    patent = Patent(id=info_list[0].text[6:],
                                    path='~',
                                    title=info_list[4].text[6:],
                                    abstract='~',
                                    inventor=info_list[7].text[5:].split(';')[:-1],
                                    applicant=info_list[6].text[10:].split(';')[:-1],
                                    category=info_list[5].text[8:].split('; '),
                                    update_time=time.strftime('%Y-%m-%dT%XZ', time.gmtime()))
                    patent_list.append(patent)
                    print patent.id, 'new'    # @todo logs
                except:
                    print 'error patent'
        if b.is_text_present(u'下一页'):
            b.click_link_by_text(u'下一页')
            b.is_element_not_present_by_css('.s_c_conter', wait_time=8)
        else:
            break
    try:
        solr.add('patent', patent_list)
    except:
        'err adding patent'
    finally:
        b.quit()


if __name__ == '__main__':
    pass
