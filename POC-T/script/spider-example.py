#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
bilibili用户签名档爬虫，存入数据库
详见：
http://www.cdxy.me/python/bilibili-2000w%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E7%88%AC%E5%8F%96/

依赖 MySQLdb
需在下方代码修改数据库配置
"""

import requests
import json
import sys

try:
    import MySQLdb
except ImportError, e:
    sys.exit(e)


def poc(str):
    url = 'http://space.bilibili.com/ajax/member/GetInfo?mid=' + str
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
    }

    jscontent = requests.get(url, headers=head, verify=False).content
    jsDict = json.loads(jscontent)
    if jsDict['status'] and jsDict['data']['sign']:
        jsData = jsDict['data']
        mid = jsData['mid']
        name = jsData['name']
        sign = jsData['sign']
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='', port=3306, charset='utf8')
            cur = conn.cursor()
            conn.select_db('bilibili')
            cur.execute(
                'INSERT INTO bilibili_user_info VALUES (%s,%s,%s,%s)', [mid, mid, name, sign])
            return True

        except MySQLdb.Error, e:
            pass
            # print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        # print "Pass: " + url
        pass
    return False
