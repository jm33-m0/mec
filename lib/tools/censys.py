#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# pylint: disable=broad-except, missing-docstring
import json
import sys

import requests

import lib.cli.colors as colors
from lib.cli.console import debug_except, input_check, print_error
from lib.cli.core import MECROOT


class CensysSearch:
    def __init__(self):
        try:
            self.key = json.loads(open(f"{MECROOT}/conf/censys.conf", "r").read())
        except FileNotFoundError:
            print_error("[-] Censys: config file not found\n")

            return

        self.search_api = "https://censys.io/api/v1/search/ipv4"
        self.account_api = "https://censys.io/api/v1/account"

    def make_request(self, api_url, data):
        ret = {}  # response in JSON format
        try:
            if data != "":
                data_encoded = json.dumps(data)
                results = requests.post(
                    url=api_url,
                    data=data_encoded, auth=(self.key['uid'], self.key['sec']))
            else:
                results = requests.get(
                    url=api_url,
                    auth=(self.key['uid'], self.key['sec']))
            ret = json.loads(results.text)

            if results.status_code != 200:
                try:
                    if ret['status'] == "error":
                        print_error("[-] Censys: "+ret['error'])
                    ret = {'error': "Known error"}
                except KeyError:
                    print_error(f"[-] Censys: Unknown error: {results.text}")
                    ret = {'error': "Unknown"}

        except KeyError:
            print_error("[-] Censys: API error")
            ret = {'error': "API"}

        except requests.exceptions.RequestException as exc:
            print_error(f"[-] Censys: request failed: {exc}")
            ret = {'error': exc}

        except BaseException:
            print_error("[-] Oops something went wrong.")
            ret = {'error': "debug_except"}
            debug_except()

        return ret

    def search_hosts(self, query, page):
        data = {
            'query': query,
            'page': page,
            'feilds': "ip,protocols"
        }
        hosts = []
        results_list = self.make_request(self.search_api, data)

        if "error" in results_list.keys():
            print_error(results_list['error'])

            return hosts

        for host in results_list['results']:
            hosts.append((str(host['ip']) + ":" +
                          str(host['protocols'][0].split("/")[0])))

        return hosts

    def query_account(self):
        resp = self.make_request(self.account_api, "")

        if "error" in resp.keys():
            print_error(resp['error'])

            return ""

        name = resp["email"]
        used = resp['quota']['used']
        resets_at = resp['quota']['resets_at']
        allowance = resp['quota']['allowance']

        return f"[*] Welcome {name}, you have used {used} of {allowance}," +\
                f"the limit resets at {resets_at}"


def run_search(query, pages):

    i = 0
    hosts = []
    censys_search = CensysSearch()

    # check account
    account_info = censys_search.query_account()

    if account_info == "":
        return ""
    colors.colored_print(account_info, colors.BLUE)

    while i <= int(pages):
        i += 1
        sys.stdout.flush()
        sys.stdout.write(f"{colors.BLUE}[+] Crawling page {i}...{colors.END}\r")

        # multi thread causes temp ban.
        hosts = hosts + censys_search.search_hosts(query, i)
    print()

    out_name = query + ".txt"

    for special_ch in ['"', "'", ':', '!', '\\', '/']:
        if special_ch in out_name:
            out_name = out_name.replace(special_ch, '-')
    file = 'data/censys_' + out_name
    out = open(file, "a")
    print(str(len(hosts)) + " Host found.")
    out.write("\n".join(str(x) for x in hosts))

    return file


def start():
    query = input_check("[?] Search query: ", allow_blank=False)
    pages = input_check("[?] Pages to crawl: ", check_type=int)

    return run_search(query, pages)
