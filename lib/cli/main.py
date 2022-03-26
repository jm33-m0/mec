#!/usr/bin/python3
# pylint: disable=too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
mass exploit console
by jm33-ng
'''

import os
import shutil
import sys

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

    futil.write_file(text=f"{os.getpid()}", filepath=SESSION.pidfile)

    while True:
        try:
            if os.getcwd() != core.MECROOT:
                os.chdir(core.MECROOT)
            input_cmd = rlinit.prompt(session=SESSION)

            try:
                cmd.cmd_handler(SESSION, input_cmd)
            except (KeyboardInterrupt, EOFError, SystemExit):
                sys.exit(0)

        except FileNotFoundError:
            console.print_error(f"[-] {core.MECROOT} not found???")
            sys.exit(1)

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

        if not os.path.isdir(core.MECROOT):
            try:
                # copy mec data from /usr/share, if installed via BlackArch package
                shutil.copytree("/usr/share/massexpconsole", core.MECROOT)
            except FileNotFoundError:
                pass
            except BaseException:
                console.debug_except()

        os.chdir(core.MECROOT)
        console.print_banner(ver=core.get_version(),
                             exp_cnt=len(futil.list_exp()))
        main()
    except (EOFError, KeyboardInterrupt, SystemExit):
        console.print_error('[-] Exiting...')
    except FileNotFoundError:
        console.debug_except()
        sys.exit(1)
    except BaseException:
        console.print_error(
            "[-] Seems like you've encountered an unhandled exception")
        console.debug_except()
