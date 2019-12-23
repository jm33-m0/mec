#!/usr/bin/python3

'''
Shadowsocks proxy
'''

# pylint: disable=too-few-public-methods,too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except
import subprocess
import json

from lib.cli import console


class ShadowsocksProxy:
    '''
    holds Shadowsocks config details, starts Shadowsocks
    '''

    def __init__(self, ss_bin, config_file):
        self.ss_bin = ss_bin
        self.config_file = config_file

        # parse ss json config
        jsonf = open(self.config_file)
        config = json.load(jsonf)
        cipher = config.get('method')
        password = config.get('password')
        server_address = config.get('server')
        server_port = config.get('server_port')
        self.ss_url = f"ss://{cipher}:{password}@{server_address}:{server_port}"

        jsonf.close()

    def start_ss_proxy(self):
        '''
        go-shadowsocks2 -c 'ss://AEAD_CHACHA20_POLY1305:your-password@[server_address]:8488' \
                    -verbose -socks :1080 -u
        '''
        try:
            subprocess.Popen(
                [self.ss_bin,
                 '-c',
                 self.ss_url,
                 '-socks',
                 ':1099',
                 '-u'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        except BaseException as err:
            console.print_error(
                '[-] Error starting Shadowsocks proxy: ' + str(err))
            console.debug_except()
