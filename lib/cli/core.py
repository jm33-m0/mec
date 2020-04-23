#!/usr/bin/python3
# pylint: disable=too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except,too-few-public-methods,too-many-arguments,too-many-return-statements

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
from multiprocessing import Manager, Process

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
        # PID file
        self.pidfile = "/tmp/mec.pid"
        # config file
        self.config_file = self.init_dir + "/conf/mec.conf"
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
        # whether to update automatically
        self.auto_update = False
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

        # version
        self.version = get_version()

        # are we root?
        self.is_root = os.geteuid() == 0
        # update via user config file
        self.read_config()

    def read_config(self):
        """
        read ~/.mec/conf/mec.conf
        """
        def handle_config(line):
            opt = line.strip().split(':')[0]
            val = line.strip().split(':')[1]

            if opt == "auto-update":
                if val.lower() in ("false", "no", "0"):
                    self.auto_update = False
                else:
                    self.auto_update = True

        try:
            conf = open(self.config_file)

            for line in conf.readlines():
                handle_config(line)

        except (FileNotFoundError, IndexError):
            self.auto_update = False
        finally:
            try:
                self.version = get_version()
            except BaseException:
                self.version = "Unknown"

            if self.auto_update:
                self.call_update(silent=True)

    def call_update(self, silent=False):
        """
        update mec
        record update result and act accordingly
        """

        if self.auto_update:
            console.print_success("[-] auto-update is enabled")

        def update(res):
            '''
            check updates from https://github.com/jm33-m0/mec
            '''
            # current version
            old_ver = get_version()

            if old_ver == "":
                res['status'] = "[-] cannot get version"

                return

            os.chdir(MECROOT)

            # refresh local git repo
            try:
                check = "git remote -v update"
                out = subprocess.check_output(
                    ["/bin/sh", "-c", check],
                    stderr=subprocess.STDOUT, timeout=30)
                check_res = out.decode("utf-8")
            except KeyboardInterrupt:
                return
            except BaseException:
                res['status'] = f"[-] Failed to check for updates:\n{traceback.format_exc()}"

                return

            if "[up to date]" in check_res:

                res['status'] = "[+] already up to date"

                return

            # pull if needed
            pull = "git pull --depth=1 --tags"
            try:
                out = subprocess.check_output(
                    ["/bin/sh", "-c", pull],
                    stderr=subprocess.STDOUT,
                    timeout=30)
                pull_res = out.decode("utf-8")
            except KeyboardInterrupt:
                return
            except BaseException:
                res['status'] = f"[-] Failed to update mec: {traceback.format_exc()}"

                return

            if "error:" in pull_res:
                res['status'] = f"[-] Failed to update mec:\n{pull_res}, press enter to continue..."

                return

            res['status'] = f"[+] mec has been updated:\n{old_ver}->{get_version()}"

            return

        # update in child process
        if silent:
            res = {}
            update_job = Process(target=update, args=(res,))
            update_job.start()

            return

        # check for result
        res = Manager().dict()
        update_job = Process(target=update, args=(res,))
        update_job.start()
        # print status
        console.print_status(
            "[*] fetching updates from github...", update_job)

        update_job.join()

        # wait for result
        try:
            status = res['status']
        except BaseException:
            status = ""

        if "[+]" in status:
            console.print_success(status)

            if "already up to date" in status:
                return

            if console.yes_no("[?] Exit mec (to apply updates) ?"):
                sys.exit(0)
        elif "[-]" in status:
            console.print_error(status)

    def command(self, user_cmd):
        '''
        passes to cmd handler
        '''
        cmd.cmd_handler(self, user_cmd)

    def attack(self):
        '''
        handles attack command
        '''
        self.use_proxy = console.yes_no(
            '[?] Do you wish to use proxychains?')

        if self.use_proxy:
            if shutil.which("proxychains4") is None:
                console.print_error("proxychains4 not found")

                return
            cmd.cmd_handler(self, "proxy")

        # sleep between two subprocess open
        sleep_seconds = console.input_check("\n[?] Wait how many seconds" +
                                            " before each process launch?\n" +
                                            " (Set it to 0 when you want to use 100% CPU" +
                                            " / bandwidth\nRecommened value: 0.1)\n" +
                                            "\n[=] Your input: ",
                                            check_type=float)
        answ = console.input_check(
            '\n[?] Do you wish to use\
            \n\n    [1] built-in exploits\
            \n    [2] or launch your own manually?\
            \n\n[=] Your choice: ',
            choices=['1', '2', 'built-in', 'manually'])

        if answ in ['1', 'built-in']:
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

                scanner_instance.sleep_seconds = sleep_seconds
                scanner_instance.scan()

                return

            except (EOFError, KeyboardInterrupt, SystemExit):
                return

        # run custom exploits
        print(
            colors.CYAN +
            colors.UNDERLINE +
            colors.BOLD +
            "\nWelcome, in here you can call your own exploit\n" +
            colors.END)
        cmd.run_exploits()

        exploit = console.input_check(
            "\n[*] Enter the path (eg. test/test) to your exploit: ",
            choices=futil.list_exp())

        jobs = int(
            console.input_check("[?] How many processes each time? ", check_type=int))

        custom_args = console.input_check(
            "[*] Addtional args for this exploit (other than `-t <target>`): ").strip().split()

        # parse user's exploit name
        exec_path = exploit.split('/')[1:]
        work_path = exploit.split('/')[:-1]
        exec_path = '/'.join(exec_path)
        work_path = '/'.join(work_path)

        # args as parameter for scanner
        scanner_instance = Scanner(work_path, exec_path,
                                   custom_args,
                                   jobs, sleep_seconds, self)
        # start scanner
        scanner_instance.scan()


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
                 sleep_seconds,
                 session):

        self.work_path = work_path
        self.exec_path = exec_path
        self.custom_args = custom_args
        self.jobs = jobs
        self.sleep_seconds = sleep_seconds
        self.session = session

    def scan(self):
        '''
        Execute exploit against given ip list
        '''

        try:
            int(self.jobs)
        except BaseException:
            console.print_error("[-] Invalid config")

            return

        if self.session.use_proxy:
            e_args = [
                'proxychains4',
                '-f',
                self.session.proxy_conf,
                './' + self.exec_path]
        else:
            e_args = ['./' + self.exec_path]

        # add custom arguments for different exploits
        e_args += self.custom_args
        # the last argument is target host
        e_args += ['-t']

        try:
            target_list = open(self.session.ip_list)
        except BaseException as exc:
            console.print_error('[-] Error occured: {}\n'.format(exc))
            console.debug_except()

            return

        try:
            os.chdir('./exploits/' + self.work_path)
        except FileNotFoundError:
            console.print_error("[-] Can't chdir to " + self.work_path)
            console.debug_except()
        console.print_warning(
            '\n[!] DEBUG: ' + str(e_args) + '\nWorking in ' + os.getcwd() +
            f"\nWait {self.sleep_seconds} seconds before each exploit")

        # you might want to cancel the scan to correct some errors

        if not console.yes_no('[?] Proceed?'):
            os.chdir(self.session.init_dir)

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

                # sleep sleep_seconds
                time.sleep(float(self.sleep_seconds))

                # process pool

                if count == self.jobs:
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


def get_version():
    '''
    print current version
    '''
    try:
        os.chdir(MECROOT)
        check = "git describe --tags"
        out = subprocess.check_output(
            ["/bin/sh", "-c", check],
            stderr=subprocess.STDOUT, timeout=3)
    except KeyboardInterrupt:
        return ""
    except BaseException:
        check = "git describe --always"
        out = subprocess.check_output(
            ["/bin/sh", "-c", check],
            stderr=subprocess.STDOUT, timeout=3)

        return ""

    return out.decode("utf-8")


def actions(act="start"):
    """
    start/stop/restart MEC
    """
    os.system(f"mec {act}")
