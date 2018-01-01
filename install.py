#!/usr/bin/python3
import os
import sys

try:
    import getpass
except BaseException:
    os.system("python3 -m pip install getpass")
    import getpass
try:
    import json
except BaseException:
    os.system("python3 -m pip install json")
    import json


from lib.cli import colors

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
    https://github.com/jm33-m0/massExpConsole
    type h or help for help\n''' + colors.END


MECROOT = os.path.join(os.path.expanduser("~"), ".mec")
DEST = os.path.join(os.path.expanduser("~"), ".mec/mec.py")


def start_install():

    # install readline if not already installed
    try:
        import readline
        print(colors.BLUE + "readline already installed." + colors.END)
    except BaseException:
        print(
            colors.RED,
            "readline not installed... ",
            colors.END,
            colors.BLUE,
            "installing it for you" + colors.END)
        os.system('python3 -m pip install readlines')

    # install requests if not already installed
    try:
        import requests
        print(colors.BLUE + "requests already installed." + colors.END)
    except BaseException:
        print(
            colors.RED +
            "requests not installed... " + colors.END +
            colors.BLUE +
            "installing it for you" + colors.END)
        os.system('python3 -m pip install requests')

    # install beatifulsoup4 if not already installed
    try:
        import bs4
        print(colors.BLUE + "bs4 already installed." + colors.END)
    except BaseException:
        print(
            colors.RED +
            "bs4 not installed... " + colors.END +
            colors.BLUE +
            "installing it for you" + colors.END)
        os.system('python3 -m pip install bs4')

    # install HTML5lib if not already installed
    try:
        import html5lib
        print(colors.BLUE + "html5lib already installed." + colors.END)
    except BaseException:
        print(
            colors.RED +
            "html5lib not installed... " + colors.END +
            colors.BLUE +
            "installing it for you" + colors.END)
        os.system('python3 -m pip install html5')

    # install docopt if not already installed
    try:
        import docopt
        print(colors.BLUE + "docopt already installed." + colors.END)
    except BaseException:
        print(
            colors.RED +
            "docopt not installed... " + colors.END +
            colors.BLUE +
            "installing it for you" + colors.END)
        os.system('python3 -m pip install docopt')

    # install python-nmap if not already installed
    try:
        import nmap
        print(colors.BLUE + "python-nmap already installed." + colors.END)
    except BaseException:
        print(
            colors.RED +
            "python-nmap not installed... " + colors.END +
            colors.BLUE +
            "installing it for you" + colors.END)
        os.system('python3 -m pip install nmap')

    # install psutil if not already installed
    try:
        import psutil
        print(colors.BLUE + "psutil already installed." + colors.END)
    except BaseException:
        print(
            colors.RED + colors.END +
            "psutil not installed... " +
            colors.BLUE +
            "installing it for you" + colors.END)
        os.system('python3 -m pip install psutil')

    print(
        colors.BLUE +
        "Done installing dependencies, now copying files." +
        colors.END)

    # copy all files to ~/.mec
    os.system('mkdir ~/.mec')
    os.system('cp -R * ~/.mec')

    # ask to delete installation files
    answer = str(
        input('would you delete installation files? (yes/No) ')).lower()
    if((answer == "yes") or (answer == "y")):
        os.system('rm -rf *')

    # clean temp files.
    os.system('rm -rf ~/.mec/mec')
    os.system('rm -rf ~/.mec/install.py')

    # zoomeye account:
    zoomeye = str(input('Would you like to use zoomeye? (yes/No) ')).lower()
    if((zoomeye == 'yes') or (zoomeye == 'y')):
        user = str(input('Username: '))
        password = str(getpass.getpass('Password: '))
        conf = open(MECROOT + '/conf/zoomeye.conf', "w")
        conf.write("user:" + user + "\n")
        conf.write("password:" + password + "\n")
    censys = str(input('Would you like to use censys? (yes/No) ')).lower()
    if((censys == 'yes') or (censys == 'y')):
        uid = str(input('Api ID: '))
        sec = str(getpass.getpass('Secret: '))
        conf2 = open(MECROOT + '/conf/censys.conf', "w")
        key = {
            "uid": uid,
            "sec": sec
        }
        conf2.write(json.dumps(key))

    # add mec to $PATH
    os.system('sudo cp mec /usr/local/bin/')

    # fix permissions
    os.system('sudo chmod +x /usr/local/bin/mec && chmod +x ~/.mec/mec.py')

    print(
        colors.GREEN +
        colors.BOLD +
        "Installation completed. try: $ mec" +
        colors.END)


os.system('clear')
print(INTRO)

# # check root
# if (os.geteuid() != 0):
#     print(colors.RED, "[-] Please run me as root", colors.END)
#     sys.exit(1)

if os.path.exists(DEST):

    try:

        # MEC already installed
        print(colors.BLUE + 'MEC is already installed.' + colors.END)

        # Choose action
        action = str(
            input('What can i do ? ([U]ninstall/[R]einstall/[N]othing) ')).lower()

        # uninstall MEC
        if action == "u":

            # delete files
            print(colors.RED + "Uninstalling MEC." + colors.END)
            os.system('rm -rf ~/.mec')
            os.system('sudo rm -rf /usr/local/bin/mec')
            sys.exit(0)

        # reinstall MEC
        elif action == "r":

            # removeing files.
            print('Uninstalling MEC.')
            os.system('rm -rf ~/.mec')
            # os.system('sudo rm -rf /usr/local/bin/mec')

            print('Done. now reinstalling.')
            start_install()
            sys.exit(0)
        elif action == "n":
            sys.exit(0)

    except KeyboardInterrupt:
        print(colors.RED + "Installation aborted." + colors.END)

else:
    try:
        install = str(
            input(
                (colors.BLUE +
                 "installing MEC, are you sure? (Yes/no) " +
                 colors.END))).lower()
        if(install == "no" or install == "n"):
            sys.exit(0)
        start_install()

    except KeyboardInterrupt:
        print(colors.RED + 'Installation aborted.' + colors.END)
