#!/usr/bin/env python
# encoding: utf-8

import html2text


def extract(page_content):
    h = html2text.HTML2Text(bodywidth=0)
    h.ignore_links = True
    h.ignore_images = True
    split_text = h.handle(page_content).split('\n')
    return '\n'.join([x for x in split_text if len(x) > 65])
