#!/usr/bin/python3
# by jm33_m0

import sys
import requests
from bs4 import BeautifulSoup
from . import console
from . import colors


def writeToFile(line, file):
    with open(file, 'a') as f:
        f.write(line + '\n')
        f.close()


def spider(keyword, count):
    # global count
    headers = {
        "User-Agent":
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
    for page in range(1, count):
        url = 'https://m.baidu.com/s?word={}&pn={}'.format(keyword, str(page))
        sys.stdout.write(
            colors.CYAN + colors.BOLD + '\r[*] Found: ' + str(
                page * 8) + ' URLs' + colors.END)
        sys.stdout.flush()
        try:
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            div = soup.find_all(tpl='www_normal')
            for l in div:
                result = l.get('data-log', '')
                a = eval(result)
                writeToFile(a['mu'], 'result.txt')
        except Exception as e:
            console.print_error('[-] Error: ' + str(e))
        else:
            pass


if __name__ == "__main__":
    try:
        keyword = input('[?] Your query is: ')
        count = int(input('[?] How many pages do you want me to crawl? '))
        spider(keyword)
        print('')
    except Exception as e:
        print('[-] Error: ' + str(e))
    except KeyboardInterrupt:
        print('[-] Exiting...')
