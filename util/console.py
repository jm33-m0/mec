#!/usr/bin/python3
from . import colors
import subprocess
import sys
import os
import readline
import atexit


intro = colors.CYAN + colors.BOLD + '''
 _      ___  _        _           ___  _
| |__  / _ \| |_     | |__  _ __ / _ \| | ___ __
| '_ \| | | | __|____| '_ \| '__| | | | |/ / '__|
| |_) | |_| | ||_____| |_) | |  | |_| |   <| |
|_.__/ \___/ \__|    |_.__/|_|   \___/|_|\_\_|
''' + colors.END + colors.GREEN + '''
    by jm33_m0
    https://github.com/jm33-m0/b0t-br0kr
    type h or help for help\n''' + colors.END

help = '''
 - Any command that cannot be understood will be executed as a shell command
 - exp / e : Start exploiter (guided)
 - exploit / exp : `tree -f ./exploits`
 - info : Display current config info
 - target <ip_list> : Change target list, eg. "target ip_list.txt"
 - proxy : Start ss-proxy (listens on local port 1099, will be used later in our mass exploit)
 - baidu <keyword> <page count> : Search via m.baidu.com
 - zoomeye / z : Run Zoomeye script to generate an IP list matching your query, google 'zoomeye' to know more
 - webshell : Simple webshell manager
 - jexboss <command> : Run jexboss - a JBoss exploitation toolkit (type `jexboss --help` to see help info)
 - redis : Run redis exploit to get root from unauthed redis servers
 - google <dork> : Fetch URLs from Google using custom dork, requires gecko driver and Firefox
 - clear / x : Clear screen
 - reset / c : Same as clear but wipes previous output
 - init / i : Return to init directory
 - h / ? : Show this help
 - q / ^C : Quit'''

built_in = colors.GREEN + '''
 [0] Weblogic Java deserialization exploit (get reverse shell)
 [1] Joomla RCE (reverse shell)
 [2] Redis unauth root (write crontab or authorized_keys)
 [3] Struts2 S2-045 exploit (command exec)
''' + colors.END


# make our console more usable
histfile = os.path.join(os.path.expanduser("~"), ".python_history")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


def print_and_flush(message, same_line=False):
    if same_line:
        print (message),
    else:
        print (message)
    if not sys.stdout.isatty():
        sys.stdout.flush()


def print_error(msg):
    print(colors.RED, msg, colors.END)


def print_warning(msg):
    print(colors.YELLOW, msg, colors.END)


def print_success(msg):
    print(colors.GREEN + colors.BOLD, msg, colors.END)
