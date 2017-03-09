#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
探测网站是否使用CDN/云WAF (多节点Get)

奇云测 ce.cloud.360.cn

用例:
  python POC-T.py -s realip -iS www.cdxy.me

结果(未使用):
  http://www.cdxy.me Nodes:92 IP(1):139.129.132.156
结果(使用):
  http://www.baidu.com [CDN Found!] Nodes:84 IP(14):111.13.100.91 14.215.177.38 119.75.218.70 115.239.210.27 180.97.33.107 119.75.217.109 115.239.211.112 180.97.33.108 14.215.177.37 111.206.223.173 111.206.223.172 220.181.111.188 103.235.46.39 220.181.112.244
结果(无法解析):
  http://mail.baidu.com [Target Unknown]
"""

import requests
import re
import time
from plugin.urlparser import get_domain
from bs4 import BeautifulSoup


def _get_static_post_attr(page_content):
    """
    Get params from <input type='hidden'>

    :param page_content:html-content
    :return dict contains "hidden" parameters in <form>
    """
    _dict = {}
    soup = BeautifulSoup(page_content, "html.parser")
    for each in soup.find_all('input'):
        if 'value' in each.attrs and 'name' in each.attrs:
            _dict[each['name']] = each['value']
    return _dict


def checkCDN(url):
    """
    Detect if the website is using CDN or cloud-based web application firewall

    :param url: Target URL or Domain
    :return True / False
    """
    url = 'http://' + url if '://' not in url else url
    url = get_domain(url)

    dest = 'http://ce.cloud.360.cn/'

    s = requests.session()

    data1 = _get_static_post_attr(s.get(dest).content)
    data1['domain'] = url
    s.post('http://ce.cloud.360.cn/task', data=data1)

    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    s.post('http://ce.cloud.360.cn/Tasks/detect', data=data1, headers=headers)

    time.sleep(5)  # 5 sec delay for nodes to detect

    data = 'domain=' + url + '&type=get&ids%5B%5D=1&ids%5B%5D=2&ids%5B%5D=3&ids%5B%5D=4&ids%5B%5D=5&ids%5B%5D=6&ids%5B%5D=7&ids%5B%5D=8&ids%5B%5D=9&ids%5B%5D=16&ids%5B%5D=18&ids%5B%5D=22&ids%5B%5D=23&ids%5B%5D=41&ids%5B%5D=45&ids%5B%5D=46&ids%5B%5D=47&ids%5B%5D=49&ids%5B%5D=50&ids%5B%5D=54&ids%5B%5D=57&ids%5B%5D=58&ids%5B%5D=61&ids%5B%5D=62&ids%5B%5D=64&ids%5B%5D=71&ids%5B%5D=78&ids%5B%5D=79&ids%5B%5D=80&ids%5B%5D=93&ids%5B%5D=99&ids%5B%5D=100&ids%5B%5D=101&ids%5B%5D=103&ids%5B%5D=104&ids%5B%5D=106&ids%5B%5D=110&ids%5B%5D=112&ids%5B%5D=114&ids%5B%5D=116&ids%5B%5D=117&ids%5B%5D=118&ids%5B%5D=119&ids%5B%5D=120&ids%5B%5D=121&ids%5B%5D=122&user_ip_list='
    r = s.post('http://ce.cloud.360.cn/GetData/getTaskDatas', data=data, headers=headers)

    ips = re.findall('"ip":"(.*?)"', r.content)
    ans = list(set(ips))
    msg = url

    if not len(ips):
        msg += ' [Target Unknown]'
        return msg

    msg += ' [CDN Found!]' if len(ans) > 1 else ''
    msg += ' Nodes:' + str(len(ips))
    msg += ' IP(%s):' % str(len(ans)) + ' '.join(ans)
    return msg


def poc(url):
    try:
        return checkCDN(url)
    except Exception:
        return url + ' [Error]'
