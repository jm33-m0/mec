#!/usr/bin/python3
# pylint: disable=too-few-public-methods,too-many-instance-attributes,too-many-statements,too-many-branches,too-many-locals,too-many-nested-blocks,broad-except

'''
Shadowsocks proxy
'''

import json
import subprocess

import requests

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
        self.local_port = config.get('local_port')
        self.ss_url = f"ss://{cipher}:{password}@{server_address}:{server_port}"
        jsonf.close()

        self.proxychains_conf = f'''
strict_chain
quiet_mode
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5  127.0.0.1 {self.local_port}
        '''

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
                 f':{self.local_port}',
                 '-u'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        except BaseException as err:
            console.print_error(
                '[-] Error starting Shadowsocks proxy: ' + str(err))
            console.debug_except()

    def is_usable(self):
        '''
        check connectivity
        '''
        resp = requests.get('http://google.com',
                            proxies=dict(http=f'socks5://127.0.0.1:{self.local_port}',
                                         https=f'socks5://127.0.0.1:{self.local_port}'))
        return resp.status_code == 200
