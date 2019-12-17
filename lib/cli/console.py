#!/usr/bin/python3

"""
Handles console related stuff
"""

import atexit
import os
import readline
import sys
import traceback
from ipaddress import ip_address

import psutil

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

HELP_INFO = colors.CYAN + '''
Core Commands
=============

    Command                       Description
    -------                       -----------

    clear (c)                     Clear screen
    reset (x)                     Terminal reset
    init (i)                      Return to init directory
    help (?)                      Display this help info
    quit (^C)                     Quit
    attack (e)                    Start (guided)
    exploits                      List all usable exploits
    info                          Display current config
    target <ip_list>              Change target list,
    proxy                         Start ss-proxy on port 1099
    baidu <keyword> <page count>  Search via m.baidu.com
    google <dork>                 Fetch URLs from Google using custom dork
    zoomeye (z)                   Crawler for ZoomEye
    censys                        Crawler for Censys.io
    masscan                       masscan port scanning
    (others)                      Treated as shell command''' + colors.END

BUILT_IN = colors.GREEN + '''
 [0] SSH bruteforcer
 [1] Weblogic Java deserialization exploit (get reverse shell)
 [2] Joomla RCE (reverse shell)
 [3] Redis unauth root (write crontab or authorized_keys)
 [4] Struts2 S2-045 exploit (command exec)
 [5] Witbe RCE exploit (get reverse shell)
''' + colors.END


COMMANDS = [
    'attack',
    'exploits',
    'info',
    'init',
    'target',
    'baidu',
    'proxy',
    'zoomeye',
    'censys',
    'masscan',
    'redis',
    'google',
    'clear',
    'reset',
    'help',
    'webshell',
    'inurl:"',
    'quit']

HISTFILE = os.path.join(os.path.expanduser("~"), ".python_history")
if not os.path.exists(HISTFILE):
    os.system('touch {}'.format(HISTFILE))
with open(HISTFILE) as f:
    for line in f:
        for item in line.strip().split():
            COMMANDS.append(item)


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


# List ./data
try:
    DATAPATH = os.path.join(os.path.expanduser("~"), ".mec/data")
    for item in os.listdir(DATAPATH):
        COMMANDS.append(item)
except FileNotFoundError:
    print_error("[-] Please run install.py first")
    sys.exit(1)


def completer(text, state):
    '''
    completer for readline, used in console
    '''
    options = [i for i in COMMANDS if i.startswith(text)]
    if state < len(options):
        return options[state]

    return None


readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

try:
    readline.read_history_file(HISTFILE)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, HISTFILE)


# pylint: disable=too-few-public-methods
class ScannerArgs():

    '''

    for scanner_args

        scanner_args = (
            work_path,
            exec_path,
            custom_args,
            jobs)
    '''

    def __init__(self, work_path, exec_path, custom_args, jobs):
        self.work_path = work_path
        self.exec_path = exec_path
        self.custom_args = custom_args
        self.jobs = jobs


# kill process by name
def check_kill_process(pstring):
    '''
    cross-platform way of killing process by name
    '''

    for proc in psutil.process_iter():
        if pstring in str(proc.cmdline):
            proc.kill()


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
