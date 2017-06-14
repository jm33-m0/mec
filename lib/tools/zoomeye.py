#!/usr/bin/python3

'''
# -*- coding: UTF-8 -*-

# coding: utf-8
# author  : evilclay
# datetime: 20160330
# modified by: jm33_m0
# http://www.cnblogs.com/anka9080/p/ZoomEyeAPI.html
'''

import json
import os
import sys
import threading
import time

import requests

from lib.cli import colors, console


class ZoomEyeAPI:

    '''
    gain API key
    '''

    QRY = ""
    OUTFILE = ""
    SEARCH_TYPE = ""

    def __init__(self, conf):
        try:
            cred_file = open(conf)
            for line in cred_file:
                line = line.strip()
                if line.startswith('user'):
                    self.user = line.split(':')[1]
                elif line.startswith('password'):
                    self.passwd = line.split(':')[1]
        except FileNotFoundError:
            console.print_error('[-] Please look into zoomeye.conf first')
        else:
            pass

    def login(self):
        '''
        login using given username and password
        '''

        data = {
            'username': self.user,
            'password': self.passwd
        }
        data_encoded = json.dumps(data)
        try:
            r_post = requests.post(
                url='https://api.zoomeye.org/user/login',
                data=data_encoded)
            r_decoded = json.loads(r_post.text)
            return r_decoded['access_token']
        except KeyError:
            return
        else:
            pass


def save_str_to_file(target_file, string):
    '''
    save str to file
    '''
    if not os.path.exists(target_file):
        os.system('touch {}'.format(target_file))
    # check if we are writing duplicate lines to the file
    f_hand = open(target_file)
    for line in f_hand:
        if line.strip() == string:
            return
    # write line to file
    with open(target_file, 'a') as output:
        output.write(string + '\n')
        output.close()


def progress(target_file):
    '''
    display progress
    '''
    l_count = 0
    if not os.path.exists(target_file):
        os.system('touch {}'.format(target_file))
    while True:
        l_count = sum(1 for line in open(target_file))
        sys.stdout.write(
            colors.CYAN + '\r[+] Found ' + str(
                l_count) + ' hosts' + colors.END)
        sys.stdout.flush()
        time.sleep(.5)


def crawler(qery, page, headers):
    '''
    fetch result from zoomeye
    '''
    if ZoomEyeAPI.SEARCH_TYPE == 'h':
        url = 'https://api.zoomeye.org/host/search?query=' + \
            qery + \
            '&facet=app,os&page=' + \
            str(page)
    else:  # for web service search
        url = 'https://api.zoomeye.org/web/search?query=' + \
            qery + \
            '&facet=app,os&page=' + \
            str(page)
    try:
        r_get = requests.get(
            url=url,
            headers=headers)
        r_decoded = json.loads(r_get.text)
        # returns error message
        if 'message' in r_get.text:
            return r_decoded['message']
        for item in r_decoded['matches']:
            if ZoomEyeAPI.SEARCH_TYPE == 'h':
                save_str_to_file(ZoomEyeAPI.OUTFILE, item['ip'])
                return
            # web service search, saves url instead
            save_str_to_file(ZoomEyeAPI.OUTFILE, item['webapp'][0]['url'])
    except BaseException:
        pass


def login_and_crawl():
    '''
    get verified with zoomeye, and start thread pool for crawling
    '''
    amnt = int(
        console.input_check(
            "[*] How many pages to crawl? (10 IPs on each page) ",
            check_type=int).strip())
    threads = []
    api = ZoomEyeAPI('zoomeye.conf')
    try:
        print(colors.BLUE +
              '[*] Crawling fetched pages from ZoomEye...' + colors.END)
        access_token = api.login()
        headers = {
            'Authorization': 'JWT ' + access_token,
        }
    except TypeError:
        console.print_error('[-] Invalid access token')
        return
    # test if we have permission to zoomeye api
    test_crawl = crawler(ZoomEyeAPI.QRY, 1, headers)
    if test_crawl != None and test_crawl != '':
        console.print_error(test_crawl)
        return
    from multiprocessing import Process
    status = Process(target=progress, args=(ZoomEyeAPI.OUTFILE,))
    status.start()

    limit = 0
    for page in range(1, int(amnt)):
        thd = threading.Thread(
            target=crawler, args=(ZoomEyeAPI.QRY, page, headers,))
        threads.append(thd)
    try:
        for job in threads:
            job.setDaemon(True)
            job.start()
            if limit == 0 or limit == 10:
                limit = 0
                job.join()
            limit += 1
    except (EOFError, KeyboardInterrupt, SystemExit):
        status.terminate()
        return
    else:
        pass

    # stop progress monitoring when we are done
    status.terminate()


def main():
    '''
    put things together
    '''
    try:
        login_and_crawl()
        print('\n')
    except BaseException:
        pass


def run():
    '''
    run this script
    '''
    try:
        ZoomEyeAPI.QRY = console.input_check(
            "[*] Your query is: ", allow_blank=False)
        ZoomEyeAPI.SEARCH_TYPE = console.input_check(
            "[?] Search for public devices (h) or web services (w)? [h/w] ",
            choices=['h', 'w']
        )
        # remove special characters that may cause naming problem
        outfile_name = ZoomEyeAPI.QRY
        for special_ch in ['"', "'", ':', '!', '\\', '/']:
            if special_ch in outfile_name:
                outfile_name = outfile_name.replace(special_ch, ' ')
        ZoomEyeAPI.OUTFILE = './data/zoomeye-{}.txt'.format(
            '-'.join(outfile_name.split()))
        main()
    except (EOFError, KeyboardInterrupt, SystemExit):
        print('\n[*] Exiting...')
    else:
        console.debug_except()
