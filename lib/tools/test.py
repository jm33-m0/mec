#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import json
import sys


try:
    api = open("/usr/share/mec/conf/censys.conf", "r")
    key = json.loads(api)
except:
    print('Censys not configured, try reinstalling or use censys_init.')
#uid = key['uid']
#sec = key['sec']
uid = "e7f7f086-a79f-4c32-b5bd-2fd307c7f770"
sec = "qwinuM347oLBAkbvXvePktbSjKCm5McL"

def search_hosts(query,page):

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
            data=data_encoded)
        results_list = json.loads(results.text)
        hosts = []
        for host in results_list:
            hosts.append(host['ip']+":"+host['protocols'][0].split("\/"[0]))
        return hosts
    except:
        return False



def search_websites(query,page):
    # soon :)
    return


def run(query,pages):
    
    i = 0
    while i <= int(pages):
        i+= 1

        # multi thread causes temp ban.
        hosts = search_hosts(query,i)
    
    out_name=query
    
    for special_ch in ['"', "'", ':', '!', '\\', '/']:
        if special_ch in out_name:
            out_name = out_name.replace(special_ch, ' ')
    #file = 'data/censys_'+out_name
    #out = open(fil)

    print(hosts)
    #for host in hosts:
    #    out.write(host+"\n")
    return #file

def start():
    query = input("Search query: ")
    pages = input("Pages to crawl: ")
    return run(query,pages)
start()