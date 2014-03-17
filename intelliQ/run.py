#!/usr/bin/env python
# encoding: utf-8


from spider import Spider
from spider import Request
import parser


if __name__ == '__main__':
    spider_paper = Spider('paper')
    spider_news = Spider('news')
    search_exp = u'(Keyword_C=数据挖掘+Title_C=数据挖掘)'
    reqs = parser.page_parser(search_exp)
    for req in reqs:
        spider_paper.add_request(req)
    spider_news.add_request(Request(url='http://roll.tech.sina.com.cn/s/channel.php#col=96',
                                    parser=parser.news_parser))
    spider_news.add_request(Request(url='http://jtt.zj.gov.cn/col/col16/index.html',
                                    parser=parser.news_parser))
    spider_news.crawl()
    spider_paper.crawl()
