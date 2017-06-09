#!/usr/bin/python3

"""
Handles console related stuff
"""

import atexit
import os
import readline
import traceback

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
    https://github.com/jm33-m0/massExpConsole
    type h or help for help\n''' + colors.END

HELP_INFO = colors.CYAN + '''
Core Commands
=============

    Command                       Description
    -------                       -----------

    clear (x)                     Clear screen
    reset (c)                     Terminal reset
    init (i)                      Return to init directory
    help (?)                      Display this help info
    quit (^C)                     Quit
    attack (e)                    Start exploiter (guided)
    exploits                      List all usable exploits
    info                          Display current config
    target <ip_list>              Change target list,
    proxy                         Start ss-proxy on port 1099
    baidu <keyword> <page count>  Search via m.baidu.com
    webshell                      Simple webshell manager (deprecated)
    google <dork>                 Fetch URLs from Google using custom dork
    zoomeye (z)                   Crawler for ZoomEye

Notice
======

    - Any command that cannot be understood will be executed as a shell command''' + colors.END

BUILT_IN = colors.GREEN + '''
 [0] Weblogic Java deserialization exploit (get reverse shell)
 [1] Joomla RCE (reverse shell)
 [2] Redis unauth root (write crontab or authorized_keys)
 [3] Struts2 S2-045 exploit (command exec)
 [4] Witbe RCE exploit (get reverse shell)
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

# List ./data
for item in os.listdir('data'):
    COMMANDS.append(item)

# make our console more usable


def completer(text, state):
    '''
    completer for readline, used in console
    '''
    options = [i for i in COMMANDS if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
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


def debug_except():
    '''
    display traceback info
    '''
    tcbk = traceback.format_exc()
    if 'NoneType: None' in tcbk:
        return
    answ = input_check("[?] Display traceback? [y/n] ",
                       choices=['y', 'n'])
    if answ == 'y':
        print_error(tcbk)


def input_check(prompt, allow_blank=True, check_type=None, choices=None):
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
            elif check_type is not None and choices is None:
                return str(check_type(user_input))
            else:
                return user_input
        except BaseException:
            print_error("[-] Invalid input")
            continue


def print_error(msg):
    print(colors.RED + msg + colors.END)


def print_warning(msg):
    print(colors.YELLOW, msg, colors.END)


def print_success(msg):
    print(colors.GREEN + colors.BOLD, msg, colors.END)
