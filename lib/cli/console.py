#!/usr/bin/python3

# pylint: disable=broad-except

"""
Handles console related stuff
"""

import sys
import traceback
from ipaddress import ip_address

from . import colors

INTRO = colors.CYAN + colors.BOLD + r'''
 ███▄ ▄███▓▓█████  ▄████▄
▓██▒▀█▀ ██▒▓█   ▀ ▒██▀ ▀█
▓██    ▓██░▒███   ▒▓█    ▄
▒██    ▒██ ▒▓█  ▄ ▒▓▓▄ ▄██▒
▒██▒   ░██▒░▒████▒▒ ▓███▀ ░
░ ▒░   ░  ░░░ ▒░ ░░ ░▒ ▒  ░
░  ░      ░ ░ ░  ░  ░  ▒
░      ░      ░   ░
       ░      ░  ░░ ░
                  ░
''' + colors.END + colors.GREEN + colors.BOLD + '''
    by jm33_m0
    https://github.com/jm33-m0/mec
    type h or help for help\n''' + colors.END


# util functions

def print_error(msg):
    '''
    print error msg in red
    '''
    print(colors.END)
    print(colors.RED + msg + colors.END)


def print_warning(msg):
    '''
    print warning msg in yellow
    '''
    print(colors.END)
    print(colors.YELLOW, msg, colors.END)


def print_success(msg):
    '''
    print success msg in green
    '''
    print(colors.END)
    print(colors.GREEN + colors.BOLD, msg, colors.END)


def debug_except():
    '''
    display traceback info
    '''
    tcbk = traceback.format_exc()

    if 'NoneType' in tcbk:
        return
    answ = input_check("[?] Display traceback? [y/n] ",
                       choices=['y', 'n'])

    if answ == 'y':
        print_error(tcbk)

    sys.exit(1)


def input_check(prompt, allow_blank=True, check_type=None, ip_check=False, choices=None):
    '''
    checks user input
    '''

    while True:
        user_input = str(
            input(
                colors.BLUE +
                prompt +
                colors.END)).strip().lower()
        try:
            if allow_blank is False and user_input == '':
                continue

            if choices is not None:
                if user_input not in choices:
                    print_error("[-] Invalid input")

                    continue

                if check_type is None:
                    return user_input

                return str(check_type(user_input))

            if check_type is not None and choices is None:
                return str(check_type(user_input))

            if ip_check is True:
                try:
                    ip_address(user_input)
                except ValueError:
                    print_error("[-] Not an IP address")

                    continue

            return user_input
        # pylint: disable=broad-except
        except BaseException:
            print_error("[-] Invalid input")

            continue


def yes_no(quest):
    '''
    ask a yes_no question
    '''

    res = str(input(quest + " (Yes/no) ")).lower()

    if res in ("yes", "y"):
        return True

    return False


def tail(filepath):
    '''
    tail -f to peek the stdout of your exploit
    '''
    last_lines = ""

    try:
        filed = open(filepath)
        last_lines = ''.join(filed.readlines()[-20:])
        filed.close()
    except IndexError:
        pass
    except BaseException:
        debug_except()

    return last_lines
