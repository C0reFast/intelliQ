#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pysolr
import config

solr_instances = {}
solr_instances['paper'] = pysolr.Solr(config.solr_url_paper)
solr_instances['news'] = pysolr.Solr(config.solr_url_news)
solr_instances['patent'] = pysolr.Solr(config.solr_url_patent)


def add(core, docs):
    """添加文档到指定Solr Core
    """
    solr_instances[core].add([doc._asdict() for doc in docs])
