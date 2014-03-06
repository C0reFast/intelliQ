#!/usr/bin/env python
# encoding: utf-8


from spider import Spider
from spider import Request
import parser


if __name__ == '__main__':
    spider_vip = Spider('vip_papers')
    spider_news = Spider('news')
    search_exp = u'(Keyword_C=明矾+Title_C=明矾)'
    reqs = parser.page_parser(search_exp)
    print reqs
    for req in reqs:
        spider_vip.add_request(req)
    spider_news.add_request(Request(url='http://tech.sina.com.cn/',
                                    parser=parser.news_parser))
    spider_news.add_request(Request(url='http://jtt.zj.gov.cn/col/col16/index.html',
                                    parser=parser.news_parser))
    spider_news.crawl()
    spider_vip.crawl()
