#!/usr/bin/python2

# -*- coding: UTF-8 -*-

# coding: utf-8
# author  : evilclay
# datetime: 20160330
# http://www.cnblogs.com/anka9080/p/ZoomEyeAPI.html

import os
import requests
import json
import atexit
import sys
import colors
import console

access_token = ''
ip_list = []


def login():
    user = raw_input('[*] enter username :')
    passwd = raw_input('[*] and password :')
    print '''
    [*] Also, curl is the best way to obtain your token:
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
    with open(file, 'w') as output:
        output.write(str)


def saveListToFile(file, list):
    s = '\n'.join(list)
    with open(file, 'w') as output:
        output.write(s)


def apiTest():
    qry = raw_input("[*] Your query is: ")
    amnt = int(
        raw_input("[*] How many results do you want? (10 IPs on each page) ").strip())
    page = 1
    global access_token
    with open('access_token.txt', 'r') as input:
        access_token = input.read()
    headers = {
        'Authorization': 'JWT ' + access_token,
    }
    # print headers
    while(True):
        try:
            r = requests.get(
                url='https://api.zoomeye.org/host/search?query=' +
                qry +
                '&facet=app,os&page=' +
                str(page),
                headers=headers)
            r_decoded = json.loads(r.text)
            for x in r_decoded['matches']:
                ip_list.append(x['ip'])
                sys.stdout.write('\r' + colors.BOLD + colors.CYAN +
                                 '{} targets found'.format(str(page * 10)) + colors.END)
                sys.stdout.flush()

        except Exception as e:
            console.print_error(
                '\nError: Please check if your API key is valid and you have enough credits')
            console.print_error('Error message: ' + str(e))
            break
        else:
            if page == (amnt / 10):
                console.print_success(
                    "\n[+] All done, ip_list.txt has been written")
                break
            page += 1


def main():
    if not os.path.isfile('access_token.txt'):
        print '[-] error : access_token file not found, please login to obtain your token'
        login()
        saveStrToFile('access_token.txt', access_token)

    apiTest()
    saveListToFile('ip_list.txt', ip_list)

if __name__ == '__main__':
    try:
        main()
        os.system('rm access_token.txt')
    except KeyboardInterrupt:
        print '\n[*] Exiting...'
