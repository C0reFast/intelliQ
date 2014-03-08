#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""配置文件"""


db_host = 'localhost'       # 数据库地址
db_user = 'webmining'       # 数据库用户名
db_password = 'webmining'   # 数据库密码
db_database = 'intelliQ'    # 数据库名称
db_port = 3306              # 数据库端口号

redis_host = 'localhost'    # Redis地址
redis_port = 6379           # Redis端口
redis_db = 0                # Redis数据库编号

solr_url_paper = 'http://localhost:8983/solr/papers/'   # Solr论文库地址
solr_url_news = 'http://localhost:8983/solr/news/'   # Solr新闻库地址
