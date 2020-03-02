#!/usr/bin/python3
# pylint: disable=too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
mass exploit console
by jm33-ng
'''

import os
import subprocess
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

    update_job = Process(target=update,)
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


def update():
    '''
    check updates from https://github.com/jm33-m0/mec
    '''
    os.chdir(core.MECROOT)

    # refresh local git repo
    try:
        check = "git remote -v update"
        out = subprocess.check_output(
            ["/bin/sh", "-c", check],
            stderr=subprocess.STDOUT, timeout=30)
    except subprocess.CalledProcessError as exc:
        console.print_error(
            f"[-] Failed to check for updates: {exc}, press enter to continue...")

        return

    if "[up to date]" in out.decode("utf-8"):

        return

    # pull if needed
    pull = "git pull; echo '[mec-update-success]'"
    try:
        out = subprocess.check_output(
            ["/bin/sh", "-c", pull],
            stderr=subprocess.STDOUT,
            timeout=30)
    except subprocess.CalledProcessError as exc:
        console.print_error(f"[-] Failed to update mec: {exc}")

        return

    if "[mec-update-success]" in out.decode("utf-8"):
        if not "error:" in out.decode("uft-8"):
            console.print_success(
                "[+] mec has been updated, press enter to continue...")

            return

        console.print_error(
            f"[-] Failed to update mec: {exc}, press enter to continue...")
