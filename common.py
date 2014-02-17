#!/usr/bin/env python
# encoding: utf-8

""" 基本定义
"""
import collections
import requests


def monkey_patch_requests():
    """requests库中文乱码补丁
    """
    prop = requests.models.Response.content

    def content(self):
        _content = prop.fget(self)
        if self.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(_content)
            if encodings:
                self.encoding = encodings[0]
            else:
                self.encoding = self.apparent_encoding
            _content = _content.decode(self.encoding, 'replace').encode('utf8', 'replace')
            self._content = _content
        return _content
    requests.models.Response.content = property(content)


class Paper(object):

    """ Paper 实体类
    """

    def __init__(self, paper_id, company_ids, path, title, author, abstract, keywords, paper_class):
        """ Paper类构造函数

        :paper_id: 论文Id
        :company_ids: 论文属于的公司
        :path: 论文的网页路径
        :title: 论文标题
        :author: 论文作者
        :abstract: 论文摘要
        :keywords: 论文关键词
        :paper_class: 论文分类

        """
        self._paper_id = paper_id
        self._company_ids = company_ids
        self._path = path
        self._title = title
        self._author = author
        self._abstract = abstract
        self._keywords = keywords
        self._paper_class = paper_class

    @property
    def solr_doc(self):
        """获取Solr文档字典

        :returns: 一个包含论文信息的字典

        """
        doc = {}
        doc['id'] = self._paper_id
        doc['path'] = self._path
        doc['title'] = self._title
        doc['author'] = self._author
        doc['abstract'] = self._abstract
        doc['keywords'] = self._keywords
        doc['class'] = self._paper_class
        doc['company_id'] = self._company_ids
        return doc

    def add_company(self, company_id):
        """添加一个公司

        :company_id: 需要添加的公司Id
        :returns: 若Id已存在，返回False，否则返回True
        """
        if company_id not in self._company_ids:
            self._company_ids.append(company_id)
            return True
        return False

# 网页链接定义
Link = collections.namedtuple('Link', 'url text')
