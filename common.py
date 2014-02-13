#!/usr/bin/env python
# encoding: utf-8

""" Common Definitions
"""
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

    """Paper Entity.
    """

    def __init__(self, paper_id, company_ids, path, title, author, abstract, keywords, paper_class):
        """@todo: to be defined1.

        :paper_id: id of a paper
        :company_ids: conpanies of a paper
        :path: path of a paper
        :title: title of a paper
        :author: author of a paper
        :abstract: @todo
        :keywords: @todo
        :paper_class: @todo

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
        """solr_doc.
        :returns: A dict contains paper info.

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
        """@todo: Docstring for add_company.

        :company_id: compand_id to add

        """
        if company_id not in self._company_ids:
            self._company_ids.append(company_id)
