#!/usr/bin/python3

'''
multi-threaded scanner for server fingerprinting
'''

import nmap
import requests

from util import vwrite, wc

NMAP = nmap.PortScanner()


class FingerprintScanner:

    '''
    identify targets and save to file
    '''

    import time  # output file naming
    NOW_TIME = time.strftime('%Y-%m-%d-%H_%M_%S')

    def __init__(self, host):
        self.target = host

    def port_scan(self, host, port):
        '''
        TCP only
        is this port open?
        '''
        NMAP.scan(host, port)

        # return true if port is open
        if NMAP[host]['tcp'][port]['state'] == 'open':
            return True
        return False

    def weblogic_scan(self):
        '''
        weblogic application server
        '''
        host = self.target
        for port in [7001, 7002, 80, 443, 8000, 8001, 9001]:
            if self.port_scan(host, port):
                url = 'http://' + self.target + ':' + port
                req_get = requests.get(url)
                if 'X-Powered-By: Servlet/2.5 JSP/2.1' in req_get.text:
                    vwrite.write_to_file(host + ':' + port,
                                         'weblogic_scan-{}.txt'.format(self.NOW_TIME))

    def jboss_scan(self):
        '''
        jboss fingerprinting
        '''
        pass

    def joomla_scan(self):
        '''
        joomla fingerprinting
        '''
        pass

    def websphere_scan(self):
        '''
        websphere fingerprinting
        '''
        pass


def batch_scan(list_file):
    '''
    put things together
    '''

    from concurrent import futures
