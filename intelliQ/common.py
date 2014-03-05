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

    def __init__(self, paper_id, path, title, author,
                 abstract, keywords, paper_class, update_time):
        """ Paper类构造函数

        :paper_id: 论文Id
        :path: 论文的网页路径
        :title: 论文标题
        :author: 论文作者
        :abstract: 论文摘要
        :keywords: 论文关键词
        :paper_class: 论文分类
        :update_time: 论文更新时间

        """
        self._paper_id = paper_id
        self._path = path
        self._title = title
        self._author = author
        self._abstract = abstract
        self._keywords = keywords
        self._paper_class = paper_class
        self._update_time = update_time

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
        doc['update_time'] = self._update_time
        return doc

# 网页链接定义
Link = collections.namedtuple('Link', 'url text')
