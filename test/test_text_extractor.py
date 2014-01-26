#!/usr/bin/env python
# encoding: utf-8

from ..text_extractor import extract
import requests
import chardet


def test_text_extractor():
    urls = ['http://www.jscd.gov.cn/art/2014/1/17/art_3954_803472.html',
            'http://www.zjt.gov.cn/art/2014/1/15/art_12_739599.html',
            'http://www.zjt.gov.cn/art/2014/1/16/art_25_740434.html',
            'http://news.sina.com.cn/o/2014-01-18/092629279559.shtml',
            'http://futures.hexun.com/2014-01-24/161716047.html',
            'http://tech.163.com/14/0117/10/9IPL6FKC000915BF.html'
            ]
    for url in urls:
        r = requests.get(url)
        if r.encoding.startswith('ISO'):
            r.encoding = chardet.detect(r.content)['encoding']
        text = extract(r.text)
        assert text
