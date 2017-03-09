#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import random
import hashlib
import requests
import socket
import re
from string import ascii_lowercase, digits
from urlparse import urlparse


def randomString(length=8):
    """
    生成随机字母串

    :param length:生成字符串长度
    :return 字母串
    """
    return ''.join([random.choice(ascii_lowercase) for _ in range(length)])


def randomDigits(length=8):
    """
    生成随机数字串

    :param length:生成字符串长度
    :return 数字串
    """
    return ''.join([random.choice(digits) for _ in range(length)])


def randomMD5(length=1, hex=True):
    """
    生成随机MD5键值对

    :param length:指定明文长度
    :param hex:指定密文长度为32位
    :returns 原文，密文(32位或16位)
    """
    plain = randomDigits(length)
    m = hashlib.md5()
    m.update(plain)
    cipher = m.hexdigest() if hex else m.hexdigest()[8:-8]
    return [plain, cipher]


def redirectURL(url, timeout=3):
    """
    获取跳转后的真实URL

    :param url:原始URL
    :param timeout:超时时间
    :return 跳转后的真实URL
    """
    try:
        url = url if '://' in url else 'http://' + url
        r = requests.get(url, allow_redirects=False, timeout=timeout)
        return r.headers.get('location') if r.status_code == 302 else url
    except Exception:
        return url


def host2IP(url):
    """
    URL转IP

    :param url:原始URL
    :return IP:PORT
    :except 返回原始URL
    """
    for offset in url:
        if offset.isalpha():
            break
    else:
        return url
    try:
        url = url if '://' in url else 'http://' + url  # to get netloc
        url = urlparse(url).netloc
        ans = [i for i in socket.getaddrinfo(url.split(':')[0], None)[0][4] if i != 0][0]
        if ':' in url:
            ans += ':' + url.split(':')[1]
        return ans
    except Exception:
        return url


def IP2domain(base, timeout=3):
    """
    IP转域名

    :param base:原始IP
    :param timeout:超时时间
    :return 域名 / False
    :except 返回False
    """
    try:
        domains = set()
        ip = base.split(':')[0] if ':' in base else base
        q = "https://www.bing.com/search?q=ip%3A" + ip
        c = requests.get(url=q,
                         headers={
                             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
                         timeout=timeout
                         ).content
        p = re.compile(r'<cite>(.*?)</cite>')
        l = re.findall(p, c)
        for each in l:
            domain = each.split('://')[-1].split('/')[0]
            domains.add(domain)
        if len(domains) > 0:
            ans_1 = base + ' -> '
            for each in domains:
                ans_1 += '|' + each
            return ans_1
        else:
            return False
    except Exception:
        return False


def checkPortTcp(target, port, timeout=3):
    """
    检查端口是否开放

    :param target:目标IP
    :param port:目标端口
    :param timeout:超时时间
    :return True / False
    :except 返回False
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(timeout)
    try:
        sk.connect((target, port))
        return True
    except Exception:
        return False
