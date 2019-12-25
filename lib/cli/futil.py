#!/usr/bin/python3

# pylint: disable=broad-except

"""
file, process
"""

import os
import time

import psutil
from lib.cli.exploits import EXPLOIT_DICT

BUILT_IN = "\n".join(list(
    EXPLOIT_DICT.keys()
))


def proc_timer(proc):
    '''
    kill subprocess on timeout
    '''
    try:
        time.sleep(10)
        proc.kill()
    except BaseException:
        pass


def check_kill_process(pstring):
    '''
    cross-platform way of killing process by name
    '''

    for proc in psutil.process_iter():
        if pstring in str(proc.cmdline):
            proc.kill()


def list_exp():
    '''
    list all executables under the root of your exploit dir
    '''
    def is_executable(path):
        '''
        check if executable
        '''

        return os.path.isfile(path) and os.access(path, os.X_OK)

    pocs = []  # save poc in a list

    for root, _, files in os.walk('exploits'):
        paths = []

        for filename in files:
            path = './' + root + '/' + filename
            paths.append(path)

        for pathname in paths:
            poc = '/'.join(pathname.split('/')[2:])

            if len(pathname.split('/')) > 4:
                continue

            if is_executable(pathname):
                pocs.append(poc)

    return pocs
