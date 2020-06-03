#!/usr/bin/python3
# pylint: disable=too-few-public-methods,too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except,too-many-arguments,unused-argument

'''
handles user commands
'''
import os
import sys
from multiprocessing import Manager, Process

import requests

from lib.cli import colors, console, futil
from lib.tools import baidu, censys, scan, zoomeye


class Command:
    """
    holds a command along with its documentation, and helper

    params
    =====

    names: tuple of names - ("name1", "name2")
    doc: documentation, single line - "this is a documentation"
    helper: a function - command_1()
    """

    def __init__(self, names, doc, session, helper):
        """
        init this command
        """
        self.helper = helper
        self.names = names
        self.doc = doc
        self.session = session

    def run(self, args):
        """
        run this command
        """
        self.helper(session=self.session, args=args)


# Initialize commands
COMMANDS = {}


def run_masscan(**kwargs):
    """
    run masscan external tool, mass scale internet scanner
    """
    session = kwargs.get("session", None)
    # check root, as masscan requires root privilege

    if not session.is_root:
        console.print_error(
            "[-] Please run mec as root in order to run masscan")

        return

    ports = console.input_check(
        "[?] What ports do you want to scan (eg. 80 443)? ").split()

    try:
        scan.masscan(ports)
    except KeyboardInterrupt:
        console.print_warning("[-] masscan exited")


def run_set(**kwargs):
    """
    set mec config, you can write whatever opt:val you like
    """
    session = kwargs.get("session", None)

    if session is None:
        console.print_error("[-] session not exist")

        return

    try:
        opt = kwargs.get("args")[0]
        val = kwargs.get("args")[1]
    except IndexError:
        console.print_error("[-] Set what?")

        return

    # read old configs
    new_config_lines = []

    if os.path.isfile(session.config_file):
        for line in open(session.config_file).readlines():
            line = line.strip().lower()

            if line.startswith(opt):
                continue
            new_config_lines.append(line)

    new_setting = f"{opt}: {val}"

    if len(new_config_lines) == 0:
        new_setting = f"{opt}: {val}\n"
    new_config_lines.append(new_setting)
    futil.write_file(text='\n'.join(new_config_lines),
                     filepath=session.config_file, append=True)
    session.read_config()
    console.print_success(f"[+] {opt} has been set to {val}")


def run_check_proxy_pool(**kwargs):
    """
    check if proxy_pool is usable
    """
    session = kwargs.get("session", None)
    # update via user config file
    session.read_config()
    # check tor
    tor_status = "Unknown"

    def check_tor():
        # also check tor
        try:
            requests.get("http://ifconfig.me", timeout=10,
                         proxies=dict(http='socks5://127.0.0.1:9050',
                                      https='socks5://127.0.0.1:9050'))
        except BaseException:
            return False

        return True

    def run_check(res):
        res['tor_status'] = "DISCONNECTED"

        if check_tor():
            res['tor_status'] = "OK"

        if session is None:
            console.print_error("[-] info: session not exist")

            return

        # check proxy chain
        res['proxy_status'] = "DISCONNECTED"

        if session.test_proxy():
            res['proxy_status'] = "OK"

    if session.proxy_pool_api == '':
        console.print_warning("[!] proxy_pool_api not configured")
    else:
        res = Manager().dict()
        proc = Process(target=run_check, args=(res,))
        proc.start()
        console.print_status(
            "[*] please wait while checking proxy chain connectivity...",
            proc
        )
        proc.join()
        tor_status = res['tor_status']
        session.proxy_status = res['proxy_status']
        colors.colored_print(f"""
proxy
-----

[*] proxy_pool API: {session.proxy_pool_api}
[*] tor connectivity: {tor_status}
[*] proxy chain connectivity: {session.proxy_status}
""", colors.CYAN)


def run_info(**kwargs):
    """
    mec status
    """
    session = kwargs.get("session", None)
    # update via user config file
    session.read_config()

    colors.colored_print(f'''
session
-------

[*] Auto-Update: {session.auto_update}
[*] Current directory: {os.getcwd()}
[*] Root directory: {session.init_dir}
[*] Log file: {session.logfile}
[*] Target: {session.ip_list}
''', colors.CYAN)


def run_init(**kwargs):
    """
    Return to init directory
    """
    session = kwargs.get("session")

    colors.colored_print('[*] Going back to init_dir...', colors.BLUE)
    os.chdir(session.init_dir)


def run_baidu(**kwargs):
    """
    Search via m.baidu.com
    """
    session = kwargs.get("session")
    command = kwargs.get("args")

    try:
        dork = command[0]
        count = int(command[1])
        os.chdir(session.out_dir)
        colors.colored_print('[*] Searching on Baidu...', colors.PURPLE)
        baidu.spider(dork, count)

        if console.yes_no("\n[?] Use collected URLs as target?"):
            session.ip_list = session.out_dir + "/result.txt"

    except (EOFError, KeyboardInterrupt, SystemExit):
        console.print_warning("[-] Interrupted")
        return
    except BaseException as exc:
        console.print_error(f"[-] Error: {exc}")
        console.debug_except()


def run_target(**kwargs):
    """
    Change target list
    """
    session = kwargs.get("session")
    try:
        target = kwargs.get("args")[0]
    except IndexError:
        console.print_error("[-] What target?")
        return

    if target not in os.listdir(session.init_dir + '/data'):
        console.print_error("[-] Target list file not found")

        return
    colors.colored_print(
        '[i] Target list changed to {}'.format(target), colors.BLUE)
    session.ip_list = session.init_dir + \
        '/data/' + target


def run_zoomeye(**kwargs):
    """
    Crawler for ZoomEye
    """

    try:
        console.print_warning(
            "[*] ZoomEye now asks for phone verification (+86 only)")
        zoomeye.run()
    except (EOFError, KeyboardInterrupt, SystemExit):
        return
    except BaseException:
        console.debug_except()


def run_censys(**kwargs):
    """
    Crawler for Censys.io
    """
    session = kwargs.get("session", None)

    try:
        output = censys.start()

        # if out file is none
        if output == "":
            return

        if console.yes_no("\n[?] Use collected URLs as target?"):
            session.ip_list = session.init_dir + "/" + output
            colors.colored_print(
                '[i] Target changed to {}'.format(
                    session.ip_list), colors.BLUE)

    except BaseException:
        return


def run_attack(**kwargs):
    """
    start a mass-exploit job
    """
    session = kwargs.get("session", None)

    try:
        session.attack()
    except (EOFError, KeyboardInterrupt, SystemExit):
        return
    except BaseException:
        console.debug_except()


def run_exploits(**kwargs):
    """
    List all usable exploits
    """
    do_print = kwargs.get("do_print", True)
    exp_list = futil.list_exp()

    if len(exp_list) == 0:
        console.print_error(
            "[-] No exploits found")
        if console.yes_no("[?] Perhaps you need to check `info`?"):
            run_info(session=kwargs.get("session"))

    if not do_print:
        return exp_list

    colors.colored_print(
        f"[+] {len(exp_list)} available exploits: ", colors.CYAN)

    for poc in exp_list:
        colors.colored_print(poc, colors.BLUE)
    return None


def run_clear(**kwargs):
    """
    clear screen
    """
    os.system("clear")
    session = kwargs.get("session")
    console.print_banner(ver=session.version, exp_cnt=len(futil.list_exp()))


def run_quit(**kwargs):
    """
    Quit mec
    """
    futil.check_kill_process('ss-proxy')
    sys.exit(0)


def run_reset(**kwargs):
    """
    Terminal reset
    """
    os.system("reset")
    session = kwargs.get("session")
    console.print_banner(ver=session.version, exp_cnt=len(futil.list_exp()))


def run_help(**kwargs):
    """
    Display this help info
    """
    help_entries = ['\n', "Command"+' '*20+"Description",

                    '-'*len("Command")+' '*20+'-'*len("Description"),
                    '\n']

    for key, val in COMMANDS.items():
        percmd = key
        if len(val.names) > 1:
            percmd = key + f" ({', '.join(val.names[1:])})"
        help_entries.append(percmd +
                            ' '*(27-len(percmd)) +
                            val.doc)

    help_entries.append("(others)"+' '*(27-len('(others)')) +
                        "Treated as shell commands")
    help_info = colors.CYAN + '\n'.join(help_entries) + colors.END

    print(help_info)


def run_update(**kwargs):
    """
    run core.call_update() to manually check update from GitHub
    """
    session = kwargs.get("session")
    session.call_update()


def cmds_init(session):
    """
    generate COMMANDS dict
    """
    # masscan
    masscan_cmd = Command(names=["masscan", "ms"],
                          doc="Run masscan to collect target hosts, requires root",
                          session=session,
                          helper=run_masscan)
    COMMANDS.update({"masscan": masscan_cmd})

    # check_proxy_pool
    check_proxy_pool_cmd = Command(names=["check_proxy_pool", "check", "test_proxy"],
                                   doc="Current mec settings, and proxy status",
                                   session=session,
                                   helper=run_check_proxy_pool)
    COMMANDS.update({"check_proxy_pool": check_proxy_pool_cmd})

    # info
    info_cmd = Command(names=["info", "i"],
                       doc="Current mec settings, and proxy status",
                       session=session,
                       helper=run_info)
    COMMANDS.update({"info": info_cmd})

    # set
    set_cmd = Command(names=["set", "s"],
                      doc=f"Set an option in {session.config_file}: `set <opt> <val>`",
                      session=session,
                      helper=run_set)
    COMMANDS.update({"set": set_cmd})

    # target
    target_cmd = Command(names=["target", "t"],
                         doc="Change target list: `target <ip_list>`",
                         session=session,
                         helper=run_target)
    COMMANDS.update({"target": target_cmd})

    # init
    init_cmd = Command(names=["init"],
                       doc="Return to mec root directory",
                       session=session,
                       helper=run_init)
    COMMANDS.update({"init": init_cmd})

    # baidu
    baidu_cmd = Command(names=["baidu"],
                        doc="Search via m.baidu.com",
                        session=session,
                        helper=run_baidu)
    COMMANDS.update({"baidu": baidu_cmd})

    # attack
    attack_cmd = Command(names=["start", "a", "attack"],
                         doc="Start a mass-exploit job",
                         session=session,
                         helper=run_attack)
    COMMANDS.update({"start": attack_cmd})

    # zoomeye
    zoomeye_cmd = Command(names=["zoomeye"],
                          doc="Crawler for ZoomEye",
                          session=session,
                          helper=run_zoomeye)
    COMMANDS.update({"zoomeye": zoomeye_cmd})

    # censys
    censys_cmd = Command(names=["censys"],
                         doc="Crawler for Censys.io",
                         session=session,
                         helper=run_censys)
    COMMANDS.update({"censys": censys_cmd})

    # exploits
    exploits_cmd = Command(names=["ls_exploits", "exploits"],
                           doc="List all usable exploits",
                           session=session,
                           helper=run_exploits)
    COMMANDS.update({"ls_exploits": exploits_cmd})

    # reset
    reset_cmd = Command(names=["reset", "x"],
                        doc="Terminal reset",
                        session=session,
                        helper=run_reset)
    COMMANDS.update({"reset": reset_cmd})

    # clear
    clear_cmd = Command(names=["clear", "c"],
                        doc="Clear screen",
                        session=session,
                        helper=run_clear)
    COMMANDS.update({"clear": clear_cmd})

    # help
    help_cmd = Command(names=["help", "h", "?"],
                       doc="Display this help info",
                       session=session,
                       helper=run_help)
    COMMANDS.update({"help": help_cmd})

    # update
    update_cmd = Command(names=["update", "up", "u"],
                         doc="Manually check for updates from GitHub",
                         session=session,
                         helper=run_update)
    COMMANDS.update({"update": update_cmd})

    # quit
    quit_cmd = Command(names=["quit", "exit", "q"],
                       doc="Quit mec",
                       session=session,
                       helper=run_quit)
    COMMANDS.update({"quit": quit_cmd})

    return COMMANDS


def cmd_handler(session, user_cmd):
    '''
    handles user input in console
    '''
    if user_cmd == '':
        return

    # parse user_cmd
    try:
        split_cmd = str(user_cmd).lower().strip().split()
        user_cmd = split_cmd[0]
        args = split_cmd[1:]
    except IndexError:
        console.print_error("[-] ???")
        return

    # COMMANDS
    cmds_init(session)
    cmd_obj = COMMANDS.get(user_cmd, None)
    # aliases
    if cmd_obj is None:
        for _, percmd in COMMANDS.items():
            if user_cmd in percmd.names:
                cmd_obj = percmd

    if cmd_obj is not None:
        cmd_obj.run(args)
        return

    # shell command
    try:
        shellcmd = ' '.join(split_cmd)
        print(
            colors.BLUE +
            colors.BOLD +
            "[*] Exec: " +
            colors.END,
            colors.PURPLE +
            shellcmd, colors.END)
        os.system(shellcmd)
    except (EOFError, KeyboardInterrupt, SystemExit):
        return
