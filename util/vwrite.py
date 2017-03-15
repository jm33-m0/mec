#!/usr/bin/python3

import os


def writeToFile(line, file):
    if not os.path.exists(file):
        os.system('touch {}'.format(file))
    f = open(file)
    for l in f:
        if l.strip() == line:
            return
    with open(file, 'a') as output:
        output.write(line + '\n')
        output.close()
