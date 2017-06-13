#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
    This program used for output pretty console program message    
'''
import sys
from console_width import getTerminalSize

__console_width = getTerminalSize()[0]
__console_width -= 2    # Cal width when starts up

def print_progress(msg):
    '''
        print progress message in right console window,this only use one line
    '''
    sys.stdout.write('\r' + ' ' * (__console_width -len(msg)) + msg)
    sys.stdout.flush()

def print_result(msg):
    '''
        print result output message in left console window, message output one line and to next 
    '''
    sys.stdout.write('\r' + msg + ' ' * (__console_width- len(msg)) + '\n\r')
    sys.stdout.flush()

def main():
    import time
    print_result('start test...')
    for i in range(0,10):
        print_progress('test print progress :%d%%' % (i*10)) 
        time.sleep(1)
    print_result('test finish!')

if __name__ == '__main__':
    main()
