#!/usr/bin/python3

"""
Handles console related stuff
"""

import os
import readline
import atexit
from . import colors


intro = colors.CYAN + colors.BOLD + '''
 _ __ ___   ___  ___
| '_ ` _ \ / _ \/ __|
| | | | | |  __/ (__
|_| |_| |_|\___|\___|

''' + colors.END + colors.GREEN + '''
    by jm33_m0
    https://github.com/jm33-m0/massExpConsole
    type h or help for help\n''' + colors.END

help_info = '''
 * Any command that cannot be understood will be executed as a shell command
 * attack / e : Start exploiter (guided)
 * exploits : List all executables inside the root directory of your exploits, eg. witbe/witbe.py
 * info : Display current config info
 * target <ip_list> : Change target list, eg. "target ip_list.txt"
 * proxy : Start ss-proxy (listens on local port 1099, will be used later in our mass exploit)
 * baidu <keyword> <page count> : Search via m.baidu.com
 * zoomeye / z : Run Zoomeye script to generate an IP list matching your query, google 'zoomeye' to know more
 * webshell : Simple webshell manager
 * jexboss <command> : Run jexboss: a JBoss exploitation toolkit (type `jexboss --help` to see help info)
 * redis : Run redis exploit to get root from unauthed redis servers
 * google <dork> : Fetch URLs from Google using custom dork, requires gecko driver and Firefox
 * clear / x : Clear screen
 * reset / c : Same as clear but wipes previous output
 * init / i : Return to init directory
 * help / ? : Show this help
 * quit / ^C : Quit'''

built_in = colors.GREEN + '''
 [0] Weblogic Java deserialization exploit (get reverse shell)
 [1] Joomla RCE (reverse shell)
 [2] Redis unauth root (write crontab or authorized_keys)
 [3] Struts2 S2-045 exploit (command exec)
 [4] Witbe RCE exploit (get reverse shell)
''' + colors.END


commands = [
    'attack',
    'exploits',
    'info',
    'init',
    'target',
    'baidu',
    'proxy',
    'zoomeye',
    'redis',
    'jexboss',
    'google',
    'clear',
    'reset',
    'help',
    'webshell',
    'inurl:""'
    'quit']

histfile = os.path.join(os.path.expanduser("~"), ".python_history")
if not os.path.exists(histfile):
    os.system('touch {}'.format(histfile))
with open(histfile) as f:
    for line in f:
        for item in line.strip().split():
            commands.append(item)

# List ./data
for item in os.listdir('data'):
    commands.append(item)

# make our console more usable


def completer(text, state):
    '''
    completer for readline, used in console
    '''
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


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
