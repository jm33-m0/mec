#!/usr/bin/python3

'''
measure file length, and display progress
'''

import sys
import time

from . import colors


def progress(file):
    '''
    display progress
    '''
    l_count = 0
    while True:
        try:
            l_count = sum(1 for line in open(file))
        except BaseException:
            l_count = 0
        sys.stdout.write(
            colors.CYAN + '\r[+] Found ' + str(
                l_count) + ' URLs' + colors.END)
        sys.stdout.flush()
        time.sleep(.3)
