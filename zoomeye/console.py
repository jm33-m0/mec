#!/usr/bin/python3
import colors
import subprocess
import sys
import os
import readline
import atexit

intro = colors.CYAN + u'''
 _      ___  _        _           ___  _
| |__  / _ \| |_     | |__  _ __ / _ \| | ___ __
| '_ \| | | | __|____| '_ \| '__| | | | |/ / '__|
| |_) | |_| | ||_____| |_) | |  | |_| |   <| |
|_.__/ \___/ \__|    |_.__/|_|   \___/|_|\_\_|

    by jm33

''' + colors.END

help = u'''
 - Any command starts with ` will be executed as a shell command
 - wizard / wiz : Run exploitation wizard, use Wizard or Wiz to run in new window
 - exploit / exp : Show available exploits
 - zoomeye / z : Run Zoomeye script to generate an IP list matching your query, google 'zoomeye' to know more
 - ripper : Run web app detector
 - jexboss : Run jexboss - a JBoss exploitation toolkit
 - clear / x : Clear screen
 - reset / c : Same as clear but wipes previous output
 - h / ? : Show this help
 - q / ^C : Quit'''

# make our console more usable
histfile = os.path.join(os.path.expanduser(u"~"), u".python_history")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)


def print_and_flush(message, same_line=False):
    if same_line:
        print message,
    else:
        print message
    if not sys.stdout.isatty():
        sys.stdout.flush()


def print_error(msg):
    print colors.RED, msg, colors.END


def print_warning(msg):
    print colors.YELLOW, msg, colors.END


def print_success(msg):
    print colors.GREEN + colors.BOLD, msg, colors.END
