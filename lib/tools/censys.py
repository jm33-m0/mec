#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json

import requests
from lib.cli.console import debug_except


def search_hosts(query, page):
    key = json.loads(open("/usr/share/mec/conf/censys.conf", "r").read())
    API_URL = "https://censys.io/api/v1/search/ipv4"
    data = {
        'query': query,
        'page': page,
        'feilds': "ip,protocols"
    }

    data_encoded = json.dumps(data)
    try:
        results = requests.post(
            url=API_URL,
            data=data_encoded, auth=(key['uid'], key['sec']))
        results_list = json.loads(results.text)
        hosts = []
        for host in results_list['results']:
            hosts.append((str(host['ip']) + ":" +
                          str(host['protocols'][0].split("/")[0])))
        return hosts
    except BaseException:
        print("Oops something went wrong. check logs.")
        debug_except()


# def search_websites(query, page):
#     # soon :)
#     pass


def run(query, pages):

    i = 0
    hosts = []
    while i <= int(pages):
        i += 1

        # multi thread causes temp ban.
        hosts = hosts + search_hosts(query, i)

    out_name = query

    for special_ch in ['"', "'", ':', '!', '\\', '/']:
        if special_ch in out_name:
            out_name = out_name.replace(special_ch, ' ')
    file = 'data/censys_' + out_name
    out = open(file, "a")
    print(str(len(hosts)) + " Host found.")
    out.write("\n".join(str(x) for x in hosts))
    return file


def start():
    query = input("Search query: ")
    pages = input("Pages to crawl: ")
    return run(query, pages)
