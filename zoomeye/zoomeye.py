#!/usr/bin/python2

# -*- coding: UTF-8 -*-

# coding: utf-8
# author  : evilclay
# datetime: 20160330
# modified by: jm33_m0
# http://www.cnblogs.com/anka9080/p/ZoomEyeAPI.html

import time
import os
import requests
import json
import threading
import atexit
import sys
import colors
import console

access_token = ''


def login():
    user = raw_input('[*] enter username :')
    passwd = raw_input('[*] and password :')
    print '''
    [*] Also, use curl to obtain your token:
    curl -XPOST https://api.zoomeye.org/user/login -d'{
        "username": "username",
        "password": "password"
    }'
    '''
    data = {
        'username': user,
        'password': passwd
    }
    data_encoded = json.dumps(data)
    try:
        r = requests.post(
            url='https://api.zoomeye.org/user/login',
            data=data_encoded)
        r_decoded = json.loads(r.text)
        global access_token
        access_token = r_decoded['access_token']
    except Exception as e:
        print '[-] invalid username or password, try again with curl'
        exit()


def saveStrToFile(file, str):
    if not os.path.exists(file):
        os.system('touch {}'.format(file))
    # check if we are writing duplicate lines to the file
    f = open(file)
    for l in f:
        if l.strip() == str:
            return
    # write line to file
    with open(file, 'a') as output:
        output.write(str + '\n')
        output.close()


def progress(file):
    lc = 0
    if not os.path.exists(outfile):
        os.system('touch {}'.format(outfile))
    while True:
        lc = sum(1 for line in open(file))
        sys.stdout.write(
            colors.CYAN + '\r[+] Found ' + str(
                lc) + ' hosts' + colors.END)
        sys.stdout.flush()
        time.sleep(.5)


def crawler(qry, amnt, page, headers):
    try:
        r = requests.get(
            url='https://api.zoomeye.org/host/search?query=' +
            qry +
            '&facet=app,os&page=' +
            str(page),
            headers=headers)
        r_decoded = json.loads(r.text)
        for x in r_decoded['matches']:
            saveStrToFile(outfile, x['ip'])
    except Exception as e:
        # console.print_error('[-] Error: ' + str(e))
        pass


def apiTest():
    amnt = int(
        raw_input("[*] How many results do you want? (10 IPs on each page) ").strip())
    global access_token
    threads = []
    with open('access_token.txt', 'r') as input:
        access_token = input.read()
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    status = threading.Thread(target=progress, args=(outfile,))
    status.setDaemon(True)
    status.start()
    limit = 0
    for page in range(1, amnt / 10):
        t = threading.Thread(target=crawler, args=(qry, amnt, page, headers,))
        threads.append(t)
    for job in threads:
        job.setDaemon(True)
        job.start()
        if limit == 0 or limit == 10:
            limit = 0
            job.join()
        limit += 1


def main():
    if not os.path.isfile('access_token.txt'):
        print '[-] error : access_token file not found, please login to obtain your token'
        login()
        saveStrToFile('access_token.txt', access_token)
    apiTest()

if __name__ == '__main__':
    try:
        qry = raw_input("[*] Your query is: ")
        outfile = '../data/zoomeye-{}.txt'.format('-'.join(qry.split()))
        main()
        #os.system('rm access_token.txt')
    except KeyboardInterrupt:
        print '\n[*] Exiting...'
