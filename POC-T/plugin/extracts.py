#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me


import re
import requests


def getIP(content, remove_duplicate=True, remove_private=False):
    """
    Functions to extract IP from content string

    parameters：
     content
     remove_duplicate  (default:true)
     remove_private    (default:False)

    usage:
     from lib.util.extracts import *
     ip_list = getIP(content)

    private address:
     10.0.0.0 - 10.255.255.255
     172.16.0.0 - 172.31.255.255
     192.168.0.0 - 192.168.255.255
     127.0.0.0 - 127.255.255.255

    example:
     > print getIP('ffeac12.2.2.2asf^&10.10\n.1.1ffa2\n')
     ['12.2.2.2','10.10.1.1']

    """

    def _isPrivateIP(strict_IP):
        p1 = re.compile(r'^10\.|^172\.(?:1[6789]|2\d|31)\.|^192\.168\.|^127\.')
        return True if re.match(p1, strict_IP) else False

    content = content.replace('\n', ',')
    p = re.compile(r'(?:(?:2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(?:2[0-4]\d|25[0-5]|[01]?\d\d?)')
    _ = re.findall(p, content)
    ans = list(set(_)) if remove_duplicate else _

    if remove_private:
        for each in ans:
            if _isPrivateIP(each):
                ans.remove(each)

    return ans


def getTitle(input):
    """
    Get title from html-content/ip/url

    :param input:html-content OR ip OR url
    :return text in <title>
    :except return string:'NULL'
    """
    try:
        if '<title>' in input:
            content = input
        else:
            url = 'http://' + input if '://' not in input else input
            content = requests.get(url,timeout=3).content
        return re.findall('<title>([\s\S]*)</title>', content)[0].strip()
    except Exception:
        return ''
