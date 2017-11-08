#!/usr/bin/python3

'''
some frequently-used colors
'''

PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def colored_print(msg, color_code):
    '''
    print message with color
    '''
    try:
        print(color_code + msg + END)
    except BaseException:
        print("\n[-] Error printing with color {}\n".format(color_code) + msg)
