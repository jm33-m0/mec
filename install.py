#!/usr/bin/python3

'''
install script for massExpConsole:
    dest: ~/.mec
    exe: /usr/local/bin/mec
'''

import os
import sys
from importlib import util

from lib.cli import colors

# distro check and initial packages
DIST = "debian"
try:
    import distro
except ModuleNotFoundError:
    if os.system("python3 -m pip install distro --user") != 0:
        colors.colored_print("Please install pip first !!!", colors.RED)
        sys.exit(1)
    if mod_exists("distro"):
        import distro
try:
    DIST = distro.linux_distribution(full_distribution_name=False)[0]
except NameError:
    import platform
    # pylint: disable=deprecated-method
    DIST = platform.linux_distribution(full_distribution_name=0)[0].lower()


def pkg_install(pkg_mgr, pkg):
    '''
    install package via system package manager
    '''
    if os.system("{} {} -y".format(pkg_mgr, pkg)) != 0:
        colors.colored_print(
            "Could not install {}, some pypi packages might fail to install".format(
                pkg),
            colors.RED)


if DIST in["ubuntu", "debian", "linuxmint", "kali"]:
    pkg_install("sudo apt install", "python3-pip")
    pkg_install("sudo apt install", "python3-dev")
    pkg_install("sudo apt install", "virtualenv")
    pkg_install("sudo apt install", "libncurses5-dev")
elif DIST in["fedora", "rhel", "centos"]:
    pkg_install("sudo yum install", "python3-pip")
    pkg_install("sudo yum install", "python3-devel")
    pkg_install("sudo yum install", "virtualenv")
    pkg_install("sudo yum install", "libncurses5-devel")
elif DIST in["arch"]:
    pkg_install("sudo pacman -S --noconfirm", "python-pip")
    pkg_install("sudo pacman -S --noconfirm", "python-dev")
    pkg_install("sudo pacman -S --noconfirm", "virtualenv")
    pkg_install("sudo pacman -S --noconfirm", "ncurses")
else:
    colors.colored_print("{} is not recognized,".format(DIST) +
                         " please install python3 dev package manually",
                         colors.RED)

# modules used by install.py
# password input
try:
    import getpass
except ModuleNotFoundError:
    os.system("python3 -m pip install getpass --user")
    import getpass
# censys config
try:
    import json
except ModuleNotFoundError:
    os.system("python3 -m pip install json --user")
    import json


def mod_exists(modulename):
    '''
    check if a module exists without importing it
    '''
    mod_spec = util.find_spec(modulename)
    return mod_spec is not None


def pip_install(venv_py, pkg):
    '''
    python3 -m pip install pkg
    '''
    colors.colored_print("Installing {} ... ".format(pkg), colors.BLUE)
    os.system('{} -m pip install {}'.format(venv_py, pkg))


def start_install():
    '''
    installation procedure
    '''
    # virtualenv
    os.system('mkdir ~/.mec')
    os.system('cp -R ./* ~/.mec')
    if not os.path.isdir("~/.mec/.venv"):
        if os.system("virtualenv -p /usr/bin/python3 ~/.mec/.venv") != 0:
            colors.colored_print("Error setting up virtualenv", colors.RED)
            sys.exit(1)

    venv_py = "~/.mec/.venv/bin/python3"

    # use requirements.txt
    pip_install(venv_py, '-r requirements.txt')

    print(
        colors.BLUE +
        "Done installing dependencies, now copying files." +
        colors.END)

    # clean temp files.
    os.system('rm -rf ~/.mec/mec')
    os.system('rm -rf ~/.mec/install.py')

    # zoomeye account:
    zoomeye = str(input('Would you like to use zoomeye? (yes/No) ')).lower()
    if zoomeye in ('yes', 'y'):
        user = str(input('Username: '))
        password = str(getpass.getpass('Password: '))
        conf = open(MECROOT + '/conf/zoomeye.conf', "w")
        conf.write("user:" + user + "\n")
        conf.write("password:" + password + "\n")
    censys = str(input('Would you like to use censys? (yes/No) ')).lower()
    if censys in ('yes', 'y'):
        uid = str(input('API ID: '))
        sec = str(getpass.getpass('Secret: '))
        conf2 = open(MECROOT + '/conf/censys.conf', "w")
        key = {
            "uid": uid,
            "sec": sec
        }
        conf2.write(json.dumps(key))

    if not os.path.isfile("/usr/local/bin/mec"):
        # add mec to $PATH
        os.system('sudo cp mec /usr/local/bin/')

        # fix permissions
        os.system('sudo chmod +x /usr/local/bin/mec && chmod +x ~/.mec/mec.py')

    print(
        colors.GREEN +
        colors.BOLD +
        "Installation completed. try: $ mec" +
        colors.END)


INTRO = colors.CYAN + colors.BOLD + r'''
 ███▄ ▄███▓▓█████  ▄████▄
▓██▒▀█▀ ██▒▓█   ▀ ▒██▀ ▀█
▓██    ▓██░▒███   ▒▓█    ▄
▒██    ▒██ ▒▓█  ▄ ▒▓▓▄ ▄██▒
▒██▒   ░██▒░▒████▒▒ ▓███▀ ░
░ ▒░   ░  ░░░ ▒░ ░░ ░▒ ▒  ░
░  ░      ░ ░ ░  ░  ░  ▒
░      ░      ░   ░
       ░      ░  ░░ ░
                  ░
''' + colors.END + colors.GREEN + colors.BOLD + '''
    by jm33_m0
    https://github.com/jm33-m0/mec
    type h or help for help\n''' + colors.END


MECROOT = os.path.join(os.path.expanduser("~"), ".mec")
DEST = os.path.join(os.path.expanduser("~"), ".mec/mec.py")

os.system('clear')
print(INTRO)

if os.path.exists(DEST):
    try:
        # MEC already installed
        print(colors.BLUE + 'MEC is already installed.' + colors.END)

        # Choose action
        ACT = str(
            input('What can i do ? ([U]ninstall/[R]einstall/[N]othing) ')).lower()

        # uninstall MEC
        if ACT == "u":
            # delete files
            print(colors.RED + "Uninstalling MEC." + colors.END)
            os.system('rm -rf ~/.mec')
            os.system('sudo rm -rf /usr/local/bin/mec')
            sys.exit(0)

        # reinstall MEC
        elif ACT == "r":
            # removeing files.
            print('Uninstalling MEC.')
            os.system('rm -rf ~/.mec')

            print('Done. now reinstalling.')
            start_install()
            sys.exit(0)
        elif ACT == "n":
            sys.exit(0)

    except KeyboardInterrupt:
        print(colors.RED + "Installation aborted." + colors.END)
else:
    try:
        INST = str(
            input(
                (colors.BLUE +
                 "installing MEC, are you sure? (Yes/no) " +
                 colors.END))).lower()
        if INST in ("no", "n"):
            sys.exit(0)

        start_install()
    except KeyboardInterrupt:
        print(colors.RED + 'Installation aborted.' + colors.END)
