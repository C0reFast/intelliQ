#!/usr/bin/env python
# encoding: utf-8

import sys
import MySQLdb
from spider import Spider
from spider import Request
import parser
import config

arg_config = {'paper': 'paper_search_exp',
              'patent': 'patent_search_exp',
              'news': 'news_seed_url'}

if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print 'usage: run.py corename'
        sys.exit(0)
    conn = MySQLdb.connect(host=config.db_host,
                           user=config.db_user,
                           passwd=config.db_password,
                           db=config.db_database,
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute('select configValue from t_spider_config where configKey=%s',
                   (arg_config.get(sys.argv[1]),))
    config_values = [row[0] for row in cursor.fetchall()]
    if sys.argv[1] == 'paper':
        spider_paper = Spider('paper')
        for search_exp in config_values:
            reqs = parser.paper_page_parser(search_exp)
            for req in reqs:
                spider_paper.add_request(req)
        spider_paper.crawl()

    if sys.argv[1] == 'news':
        spider_news = Spider('news')
        for seed_url in config_values:
            spider_news.add_request(Request(arg=seed_url,
                                    parser=parser.news_parser))
        spider_news.crawl()

    if sys.argv[1] == 'patent':
        spider_patent = Spider('patent')
        for search_exp in config_values:
            spider_news.add_request(Request(arg=search_exp,
                                    parser=parser.patent_parser))
        spider_news.crawl()
