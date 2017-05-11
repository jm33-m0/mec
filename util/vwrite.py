#!/usr/bin/python3

'''
verified write
'''

import os


def write_to_file(line, file):
    '''
    write to file and check if there are duplicate lines
    '''
    if not os.path.exists(file):
        os.system('touch {}'.format(file))
    write_file = open(file)
    for ori_line in write_file:
        if ori_line.strip() == line:
            return
    with open(file, 'a') as output:
        output.write(line + '\n')
        output.close()
