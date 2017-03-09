#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
DNS Zone Transfer PoC

只能运行在linux环境下
系统需具备两个命令:nslookup,dig(kali里面已有)

输入格式: 不带协议名，不带目录名
[ok]    cdxy.me
[ok]    www.cdxy.me
[ok]    app.air.cdxy.me
[wrong] http://cdxy.me
[wrong] cdxy.me/index.html

会产生以下两种报错(可忽略):
list index out of range
couldn't get address for 'xxx.xxx.xxx.': not found

"""

import os
import re
import subprocess
import time
import sys


def poc(domain):
    try:
        if subprocess.mswindows:
            print '[Error] This script only for linux/unix, please quit with [Ctrl-C]'
            time.sleep(10000)
            return False
        if '-C' in sys.argv:
            print '[Error] This script only for muti-threading mode, please quit with [Ctrl-C] and use [-eT] in your command.'
            time.sleep(10000)
            return False
        domain = domain.split('.')[-2].strip(' ') + '.' + domain.split('.')[-1].strip(' ')
        cmd_res = os.popen('nslookup -type=ns ' + domain).read()  # fetch DNS Server List
        dns_servers = re.findall('nameserver = (.*?)\n', cmd_res)
        for server in dns_servers:
            cmd_res = os.popen('dig @%s axfr %s' % (server, domain)).read()
            if cmd_res.find('Transfer failed.') < 0 and \
                            cmd_res.find('connection timed out') < 0 and \
                            cmd_res.find('XFR size') > 0:
                return True
        return False
    except Exception, e:
        return False
