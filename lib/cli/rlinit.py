#!/usr/bin/python3

"""
readline init script
"""

import atexit
import os
import readline
import sys

from lib.cli.cmd import cmds_init

from . import colors


HISTFILE = os.path.join(os.path.expanduser("~"), ".python_history")
CMD_LIST = []


def completer(text, state):
    '''
    completer for readline, used in console
    '''
    options = [i for i in CMD_LIST if i.startswith(text)]

    if state < len(options):
        return options[state]

    return None


def readline_init(session):
    """
    init readline settings
    """
    command_list = list(cmds_init(session).keys())

    # add other keywords
    command_list += ["tomcat", "jboss", "jenkins", "weblogic", "/tmp/", "attack",
                     "reset", "clear", "quit", "redis", "ssh_bruteforcer", "witbe"]

    if not os.path.exists(HISTFILE):
        os.system('touch {}'.format(HISTFILE))
    with open(HISTFILE) as histf:
        for line in histf:
            for item in line.strip().split():
                command_list.append(item)

    # List ./data
    try:
        data_path = os.path.join(os.path.expanduser("~"), ".mec/data")

        for item in os.listdir(data_path):
            command_list.append(item)
    except FileNotFoundError:
        colors.colored_print("[-] Please run install.py first", colors.RED)
        sys.exit(1)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)

    try:
        readline.read_history_file(HISTFILE)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, HISTFILE)

    return command_list
