#!/usr/bin/python3

"""
readline init script
"""

import atexit
import os
import readline
import sys

from prompt_toolkit import ANSI
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import PromptSession

from lib.cli.cmd import cmds_init, run_exploits

from . import colors

HISTFILE = os.path.join(os.path.expanduser("~"), ".mec_history")


def readline_init(session):
    """
    init readline settings
    """
    command_list = list(cmds_init(session).keys())

    # add other keywords
    command_list += ["tomcat", "jboss", "jenkins", "weblogic", "/tmp/", "attack",
                     "reset", "clear", "quit", "redis", "ssh_bruteforcer", "witbe"]
    # add from list_exp
    command_list += run_exploits(do_print=False)

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

    try:
        readline.read_history_file(HISTFILE)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, HISTFILE)

    return command_list


def prompt(session):
    '''
    mec prompt
    '''
    cmd_list = readline_init(session)
    mec_completer = WordCompleter(cmd_list)
    mec_ps = ANSI(colors.CYAN + colors.BOLD + "\nmec > " + colors.END)

    return PromptSession(message=mec_ps,
                         mouse_support=True,
                         history=FileHistory(HISTFILE),
                         completer=mec_completer,
                         auto_suggest=AutoSuggestFromHistory()).prompt()
