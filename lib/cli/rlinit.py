#!/usr/bin/python3

"""
readline init script
"""

import os
import sys

from prompt_toolkit import ANSI
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import PromptSession

from lib.cli.cmd import cmds_init, run_exploits

from . import colors

HISTFILE = os.path.join(os.path.expanduser("~"), ".mec_history")


def readline_init(session):
    """
    init readline settings
    """
    cmds_dict = cmds_init(session)
    command_list = []
    for _, percmd in cmds_dict.items():
        command_list += percmd.names

    # add other keywords
    command_list += ["/tmp/", "attack", "quit", "reset", "clear",
                     "app:", "port:", "ip:", "cidr:", "country:", "city:",
                     "subdivisions:", "device:", "ver:"]
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

    return list(dict.fromkeys(command_list))


def prompt(session):
    '''
    mec prompt
    '''
    cmd_list = readline_init(session)
    completion_dict = dict.fromkeys(cmd_list)
    completion_dict["target"] = dict.fromkeys(os.listdir("./data"))

    mec_completer = NestedCompleter.from_nested_dict(completion_dict)
    mec_ps = ANSI(colors.CYAN + colors.BOLD + "\nmec > " + colors.END)

    return PromptSession(message=mec_ps,
                         mouse_support=True,
                         history=FileHistory(HISTFILE),
                         completer=mec_completer,
                         complete_while_typing=True,
                         auto_suggest=AutoSuggestFromHistory()).prompt()
