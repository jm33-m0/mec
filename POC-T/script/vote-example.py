#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
上海大学生戏剧节-刷票脚本

POST /phpapp/polling.php HTTP/1.1
Host: www.kankanews.com
Content-Length: 44
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://www.kankanews.com
Upgrade-Insecure-Requests: 1
User-Agent:
Content-Type: application/x-www-form-urlencoded
Referer: http://www.kankanews.com/z/dhj13th/index.shtml
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8
Cookie:

classid=9401&f_6339_c_8969_b_2_%5B%5D=844622

"""

import requests

base_url = "http://www.kankanews.com/z/dhj13th/index.shtml"
post_url = "http://www.kankanews.com/phpapp/polling.php"


def poc():
    d = {
        'classid': '9401',
        'f_6339_c_8969_b_2_%5B%5D': '844621'
    }
    h = {
        'Referer': 'http://www.kankanews.com/z/dhj13th/index.shtml',
        'Cookie': '',
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64)',
    }
    r = requests.post(post_url, timeout=10, data=d, headers=h)
    if 'success' in r.content:
        return True
    return False
