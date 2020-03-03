#!/usr/bin/python3
# pylint: disable=too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
mass exploit console
by jm33-ng
'''

import os
import sys
from multiprocessing import Process

from lib.cli import cmd, colors, console, core, futil, rlinit

# Needed for scanner session later
SESSION = core.Session()


def main():
    '''
    handles user interface
    '''
    colors.colored_print(
        "[*] Default target list is ./data/ip_list.txt", colors.CYAN)
    SESSION.ip_list = SESSION.init_dir + '/data/ip_list.txt'

    update_job = Process(target=core.update,)
    update_job.start()

    while True:
        try:
            input_cmd = rlinit.prompt(session=SESSION)

            try:
                cmd.cmd_handler(SESSION, input_cmd)
            except (KeyboardInterrupt, EOFError, SystemExit):
                sys.exit(0)

        except KeyboardInterrupt:
            answ = console.yes_no(
                "\n[?] Are you sure to exit?")

            if answ:
                futil.check_kill_process('ss-proxy')
                sys.exit(0)
            else:
                continue


def run():
    '''
    start mec
    '''
    try:
        os.system('clear')
        os.chdir(core.MECROOT)
        console.INTRO = console.INTRO.replace("v2.0", core.get_version())
        console.INTRO = console.INTRO.replace(
            "0 exploits", f"{len(futil.list_exp())-1} exploits")
        print(console.INTRO)
        main()
    except (EOFError, KeyboardInterrupt, SystemExit):
        console.print_error('[-] Exiting...')
    except FileNotFoundError:
        console.debug_except()
        console.print_error("[-] Please run install.py first")
        sys.exit(1)
    except BaseException:
        console.print_error(
            "[-] Seems like you've encountered an unhandled exception")
        console.debug_except()
