#!/usr/bin/env python
# encoding: utf-8


def analyze(source, pattern):
    words = pattern.split(',')
    for item in words:
        if not item in source:
            return False
    return True
