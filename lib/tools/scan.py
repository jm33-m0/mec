#!/usr/bin/python3

'''
a masscan wrapper
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
        '30000',
        '-oG',
        '/tmp/masscan.result'])
