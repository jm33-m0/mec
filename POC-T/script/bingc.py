#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
基于Bing搜索引擎的 IP反查域名(默认为不使用API，开启API请在源码中配置)

Usage:
  查询C段域名  - python POC-T.py -s bingc -iN 139.24.102.0/24 -t 20
  批量反查域名 - python POC-T.py -s bingc -iF ip.txt -t 20

"""
import requests
import re
import urllib
import urllib2
import base64
from plugin.extracts import getTitle

try:
    import json
except ImportError:
    import simplejson as json

# 如果使用API请将此项修改为自己的key(申请方法 https://github.com/Xyntax/BingC)
accountKey = 'JaDRZblJ6OhxxxxxxxxxxxxxxxxxaWx8OThobZoRA'
# 如果使用API请将此项修改为True
ENABLE_API = False
top = 50
skip = 0


def info():
    return __doc__


def BingSearch(query):
    payload = {}
    payload['$top'] = top
    payload['$skip'] = skip
    payload['$format'] = 'json'
    payload['Query'] = "'" + query + "'"
    url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + urllib.urlencode(payload)
    sAuth = 'Basic ' + base64.b64encode(':' + accountKey)

    headers = {}
    headers['Authorization'] = sAuth
    try:
        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        data = json.loads(the_page)
        return data
    except Exception:
        pass


def poc(ip):
    domains = set()
    if ENABLE_API:
        ans_obj = BingSearch("ip:" + ip)
        for each in ans_obj['d']['results']:
            domains.add(each['Url'].split('://')[-1].split('/')[0])
    else:
        if '://' in ip:
            ip = ip.split('://')[-1].split(':')[0]
        q = "https://www.bing.com/search?q=ip%3A" + ip
        c = requests.get(q, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}).content
        p = re.compile(r'<cite>(.*?)</cite>')
        l = re.findall(p, c)
        for each in l:
            domain = each.split('://')[-1].split('/')[0]
            domains.add(domain)

    title = getTitle(ip)
    if not title and not domains:
        return False
    else:
        return '[%s]' % ip + '|'.join(domains) + (' (%s)' % title if title else '')
