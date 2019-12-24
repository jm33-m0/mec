#!/usr/bin/python3
# pylint: disable=too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
mass exploit console
by jm33-ng
'''

import os
import sys


from lib.cli import core, cmd, colors, console, futil

# Needed for scanner session later
SESSION = core.Session()


def main():
    '''
    handles user interface
    '''

    answ = str(
        input(
            colors.CYAN +
            '[?] Use ip_list.txt as target list? [y/n] ' +
            colors.END)).strip()

    if answ.lower() == 'n':
        os.system("ls ~/.mec/data")
        SESSION.ip_list = SESSION.init_dir + '/data/' + \
            console.input_check(
                '[=] Choose your target IP list, eg. ip_list.txt ',
                choices=os.listdir(core.MECROOT + '/data'))

    while True:
        try:
            input_cmd = input(
                colors.CYAN +
                colors.BOLD +
                "\nmec > " +
                colors.END)

            try:
                cmd.cmd_handler(SESSION, input_cmd)
            except (KeyboardInterrupt, EOFError, SystemExit):
                sys.exit(0)

        except KeyboardInterrupt:

            try:
                answ = input("\n[?] Are you sure to exit? [y/n] ")
            except KeyboardInterrupt:
                print("\n[-] Okay okay, exiting immediately...")
                futil.check_kill_process('ss-proxy')
                sys.exit(0)

            if answ.lower() == 'y':
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
        print(console.INTRO)
        os.chdir(core.MECROOT)
        main()
    except (EOFError, KeyboardInterrupt, SystemExit):
        console.print_error('[-] Exiting...')
    except FileNotFoundError:
        console.debug_except()
        console.print_error("[-] Please run install.py first")
        sys.exit(1)
    except BaseException:
        console.print_error(
            "[-] Seems like you\'ve encountered an unhandled exception")
        console.debug_except()
