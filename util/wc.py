#!/usr/bin/python3

import sys
import time
from . import colors


def progress(file):
    lc = 0
    while True:
        try:
            lc = sum(1 for line in open(file))
        except BaseException:
            lc = 0
        sys.stdout.write(
            colors.CYAN + '\r[+] Found ' + str(
                lc) + ' URLs' + colors.END)
        sys.stdout.flush()
        time.sleep(.3)
