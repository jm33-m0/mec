#!/usr/bin/python3

'''
multi-threaded baidu crawler
by jm33_m0
'''

import os
import threading

import requests
from bs4 import BeautifulSoup

from lib.cli import console, vwrite, wc


def get_and_parse(url, page):
    '''
    fetch baidu result and parse
    '''
    try:
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.1) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        }
        url += str(page)
        rget = requests.get(url, headers=headers)
        soup = BeautifulSoup(rget.text, "html.parser")
        div = soup.find_all(tpl='www_normal')
        for line in div:
            result = line.get('data-log', '')
            res = eval(result)
            vwrite.write_to_file(res['mu'], 'result.txt')
    except BaseException:
        pass


def spider(keyword, count):
    '''
    spider method
    '''
    url = 'https://m.baidu.com/s?word={}&pn='.format(keyword)
    if not os.path.exists('result.txt'):
        os.system('touch result.txt')
    from multiprocessing import Process
    status = Process(target=wc.progress, args=('result.txt',))
    status.start()
    try:
        threads = []
        jobs = 0
        for page in range(1, count):
            threads.append(
                threading.Thread(target=get_and_parse, args=(url, page,)))
        for thd in threads:
            thd.setDaemon(True)
            thd.start()
            if jobs == 30 or jobs == 0:
                jobs = 0
                thd.join()
            jobs += 1
    except (EOFError, KeyboardInterrupt, SystemExit):
        status.terminate()
        return
    else:
        pass

    # exit progress monitoring when we are done
    status.terminate()
