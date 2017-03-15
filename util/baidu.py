#!/usr/bin/python3
# by jm33_m0

import sys
import os
import time
import requests
import threading
import subprocess
from bs4 import BeautifulSoup
from . import console
from . import colors
from . import vwrite
from . import wc


def getAndParse(url, page):
    try:
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        }
        url += str(page)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find_all(tpl='www_normal')
        for l in div:
            result = l.get('data-log', '')
            a = eval(result)
            vwrite.writeToFile(a['mu'], 'result.txt')
    except:
        pass


def spider(keyword, count):
    url = 'https://m.baidu.com/s?word={}&pn='.format(keyword)
    if not os.path.exists('result.txt'):
        os.system('touch result.txt')
    status = threading.Thread(target=wc.progress, args=('result.txt',))
    status.setDaemon(True)
    status.start()
    try:
        threads = []
        jobs = 0
        for page in range(1, count):
            threads.append(
                threading.Thread(target=getAndParse, args=(url, page,)))
        for t in threads:
            t.setDaemon(True)
            t.start()
            if jobs == 30:
                jobs = 0
                t.join()
            jobs += 1
    except Exception as e:
        console.print_error('[-] Error with crawler: ' + str(e))
    else:
        pass
