#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pysolr
from common import Paper
import config

solr_paper = pysolr.Solr(config.solr_url_paper)


def add_paper(paper):
    """添加一篇论文到Solr

    :paper: 要添加的论文

    """
    solr_paper.add([paper.solr_doc])


def find_paper(paper_id):
    """根据论文Id查找论文

    :paper_id: 需要查找的论文Id
    :returns: 论文实体或者None

    """
    result = solr_paper.search('id:{paper_id}'.format(paper_id=paper_id))
    if result.hits:
        return Paper(paper_id=result.docs[0]['id'],
                     company_ids=result.docs[0]['company_id'],
                     path=result.docs[0]['path'],
                     title=result.docs[0]['title'],
                     author=result.docs[0]['author'],
                     abstract=result.docs[0]['abstract'],
                     keywords=result.docs[0]['keywords'],
                     paper_class=result.docs[0]['class'])
    return None
