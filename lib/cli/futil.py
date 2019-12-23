#!/usr/bin/python3

# pylint: disable=broad-except

"""
file, process
"""

import time

import psutil


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
