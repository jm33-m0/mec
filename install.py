#!/usr/bin/python3
import os
import sys
import os.path
try:
	import getpass
except:
	os.system("python3 -m pip install getpass")
	import getpass
try:
    import json
except:
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
    type h or help for help\n'''



def start_install():

    # install readline if not already installed
    try:
        import readline
        print(colors.BLUE+"readline already installed.")
    except:
        print(colors.RED+"readline not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install readlines')
    
    
    # install requests if not already installed
    try:    
        import requests
        print(colors.BLUE+"requests already installed.")
    except:
        print(colors.RED+"requests not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install requests')
    

    # install beatifulsoup4 if not already installed
    try:
        import bs4
        print(colors.BLUE+"bs4 already installed.")
    except:
        print(colors.RED+"bs4 not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install bs4')


    # install HTML5lib if not already installed
    try:
        import html5lib
        print(colors.BLUE+"html5lib already installed.")
    except:
        print(colors.RED+"html5lib not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install html5')

    # install docopt if not already installed
    try:
        import docopt
        print(colors.BLUE+"docopt already installed.")
    except:
        print(colors.RED+"docopt not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install docopt')

    # install python-nmap if not already installed
    try:
        import nmap
        print(colors.BLUE+"python-nmap already installed.")
    except:
        print(colors.RED+"python-nmap not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install nmap')

    # install psutil if not already installed
    try:
        import psutil
        print(colors.BLUE+"psutil already installed.")
    except:
        print(colors.RED+"psutil not installed... "+colors.BLUE+"installing it for you")
        os.system('python3 -m pip install psutil')
    

    print(colors.BLUE+"Done installing dependencies, now copying files.")
    
    # copy all files to /usr/share/mec
    os.system('mkdir /usr/share/mec')
    os.system('cp -R * /usr/share/mec')


    # add mec.
    os.system('cp mec /usr/bin/')


    # fix permissions
    os.system('chmod +x /usr/bin/mec && chmod +x /usr/share/mec/mec.py')


    # ask to delete installation files
    answer = str(input('would you delete installation files? (yes/No) ')).lower()
    if((answer == "yes") or (answer == "y")):
        os.system('rm -rf *')

    # clean temp files.
    os.system('rm -rf /usr/share/mec/mec')
    os.system('rm -rf /usr/share/mec/install.py')
    

    # zoomeye account:
    zoomeye = str(input('Would you like to use zoomeye? (yes/No) ')).lower()
    if((zoomeye == 'yes') or (zoomeye == 'y')):
    	user = str(input('Username: '))
    	password = str(getpass.getpass('Password: '))
    	conf = open('/usr/share/mec/conf/zoomeye.conf', "w")
    	conf.write("user:"+user+"\n")
    	conf.write("password:"+password+"\n")
    censys = str(input('Would you like to use censys? (yes/No) ')).lower()
    if((censys == 'yes') or (censys == 'y')):
        uid = str(input('Api ID: '))
        sec = str(input('Secret: '))
        conf2 = open('/usr/share/mec/conf/censys.conf', "w")
        key = {
            "uid": uid,
            "sec": sec
        }
        conf2.write(json.dumps(key))


    print(colors.BLUE+"Installation completed. try: $ mec")

    return;





os.system('clear')
print(INTRO)
if os.path.exists('/usr/share/mec/mec.py')==True:

	# MEC already installed
    print(colors.BLUE+'MEC is already installed.')



    # Choose action
    action = str(input('What can i do ? ([U]ninstall/[R]einstall/[N]othing) ')).lower()

    # uninstall MEC
    if(action == "u"):

    	# delete files
    	print(colors.RED+"Uninstalling MEC.")
    	os.system('rm -rf /usr/bin/mec')
    	os.system('rm -rf /usr/share/mec')
    	sys.exit(0)

    # reinstall MEC
    elif(action == "r"):
    	
    	# removeing files.
    	print('Uninstalling MEC.')
    	os.system('rm -rf /usr/bin/mec')
    	os.system('rm -rf /usr/share/mec')

    	print('Done. now reinstalling.')
    	start_install()
    	sys.exit(0)
    elif(action == "n"):
        sys.exit(0)

else:
    try:
        install = str(input((colors.BLUE+"installing MEC, are you sure? (Yes/no) "))).lower()
        if(install == "no" or install == "n"):
            sys.exit(0)
        start_install()




    except KeyboardInterrupt:
        print(colors.RED+'Installation aborted.')