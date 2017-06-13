#!/usr/bin/python3

'''
multi-threaded scanner for server fingerprinting
'''

import nmap
import requests

from lib.cli import console, vwrite, wc

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
                    return True
            return False

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
    # display progress
    import threading
    outfile = '{}.txt'.format(FingerprintScanner.NOW_TIME)
    status = threading.Thread(target=wc.progress(outfile))
    status.setDaemon(True)
    status.start()

    # parallel exec
    from concurrent import futures
    with futures.ThreadPoolExecutor(max_workers=100) as executor:
        list_open = open(list_file)
        future_targets = {}
        for line in list_open:
            host = line.strip()
            scanner = FingerprintScanner(host)
            future_targets.update(
                {executor.submit(scanner.weblogic_scan): host})
        for future in futures.as_completed(future_targets):
            job = future_targets[future]
            try:
                ret_val = future.result()  # return value of app scanner method
                if ret_val:
                    vwrite.write_to_file(job, outfile)
            except (EOFError, KeyboardInterrupt, SystemExit):
                pass
            else:
                console.debug_except()
