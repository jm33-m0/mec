#!/usr/bin/python3

'''
collecting vulnerable hosts using masscan and xmir
'''

import subprocess


def masscan(ports):
    '''
    launch masscan for large scale port/banner scan, then xmir can proccess the result
    '''

    subprocess.call([
        'masscan',
        '-p',
        ','.join(ports),
        '0.0.0.0/0',
        '--banners',
        '--exclude',
        '255.255.255.255',
        '--rate',
        '300000',
        '-oX',
        '/tmp/masscan.result'])


def xmir():
    '''
    select hackable targets from masscan result
    '''
    pass
