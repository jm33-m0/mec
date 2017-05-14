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
import traceback

import requests

import colors
import console


class ZoomEyeAPI:

    '''
    gain API key
    '''

    QRY = ""
    OUTFILE = '../data/zoomeye-{}.txt'.format('-'.join(QRY.split()))

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
        print(data)
        data_encoded = json.dumps(data)
        try:
            r_post = requests.post(
                url='https://api.zoomeye.org/user/login',
                data=data_encoded)
            r_decoded = json.loads(r_post.text)
            return r_decoded['access_token']
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass
        else:
            console.print_error(
                '[-] invalid username or password, try again with curl')
        sys.exit(1)


def debug_traceback():
    '''
    display traceback info
    '''
    answ = console.input_check("[?] Display traceback? [y/n] ",
                               choices=['y', 'n'])
    if answ == 'y':
        console.print_error(traceback.format_exc())


def save_str_to_file(file, string):
    '''
    save str to file
    '''
    if not os.path.exists(file):
        open(file, 'w').close()
    # check if we are writing duplicate lines to the file
    f_hand = open(file)
    for line in f_hand:
        if line.strip() == string:
            return
    # write line to file
    with open(file, 'a') as output:
        output.write(string + '\n')
        output.close()


def progress(file):
    '''
    display progress
    '''
    l_count = 0
    if not os.path.exists(file):
        open(file, 'w').close()
    while True:
        l_count = sum(1 for line in open(file))
        sys.stdout.write(
            colors.CYAN + '\r[+] Found ' + str(
                l_count) + ' hosts' + colors.END)
        sys.stdout.flush()
        time.sleep(.5)


def crawler(qery, _, page, headers):
    '''
    fetch result from zoomeye
    '''
    try:
        r_get = requests.get(
            url='https://api.zoomeye.org/host/search?query=' +
            qery +
            '&facet=app,os&page=' +
            str(page),
            headers=headers)
        r_decoded = json.loads(r_get.text)
        for item in r_decoded['matches']:
            save_str_to_file(ZoomEyeAPI.OUTFILE, item['ip'])
    except BaseException:
        pass


def api_test():
    '''
    get verified with zoomeye
    '''
    amnt = int(
        console.input_check(
            "[*] How many results do you want? (10 IPs on each page) ",
            check_type=int).strip())
    threads = []
    api = ZoomEyeAPI('zoomeye.conf')
    access_token = api.login()
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    status = threading.Thread(target=progress, args=(ZoomEyeAPI.OUTFILE,))
    status.setDaemon(True)
    status.start()
    limit = 0
    for page in range(1, int(amnt / 10)):
        thd = threading.Thread(
            target=crawler, args=(ZoomEyeAPI.QRY, amnt, page, headers,))
        threads.append(thd)
    for job in threads:
        job.setDaemon(True)
        job.start()
        if limit == 0 or limit == 10:
            limit = 0
            job.join()
        limit += 1


def main():
    '''
    put things together
    '''
    try:
        api_test()
    except (EOFError, KeyboardInterrupt, SystemExit):
        pass
    else:
        console.print_error('[-] Error with api_test')
        debug_traceback()

    try:
        ZoomEyeAPI.QRY = console.input_check(
            "[*] Your query is: ", allow_blank=False)
        ZoomEyeAPI.OUTFILE = '../data/zoomeye-{}.txt'.format(
            '-'.join(ZoomEyeAPI.QRY.split()))
        main()
    except KeyboardInterrupt:
        print('\n[*] Exiting...')
    else:
        debug_traceback()
