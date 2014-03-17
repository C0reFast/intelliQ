#!/usr/bin/env python
# encoding: utf-8

""" 基本定义
"""
import collections
import requests
import chardet
from splinter import Browser


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
                self.encoding = chardet.detect(_content)['encoding']
        return _content
    requests.models.Response.content = property(content)


def get_links(url):
    """@todo: Docstring for get_links.

    :url: @todo
    :returns: @todo

    """
    with Browser("phantomjs", load_images=False, wait_time=10) as browser:
        browser.visit(url)
        browser.is_element_present_by_tag('a', wait_time=6)
        link_list = browser.find_by_xpath('//a[@href]')
        result = []
        for link in link_list:
            try:
                if len(link.text) > 10:
                    result.append(Link(link.__getitem__('href'), link.text))
            except:
                pass
        return result

# 网页链接定义
Link = collections.namedtuple('Link', 'url title')
# 论文定义
Paper = collections.namedtuple('Paper',
                               'id path title author abstract keywords\
                                classification category update_time')
# 新闻定义
News = collections.namedtuple('News', 'url title content category update_time')
