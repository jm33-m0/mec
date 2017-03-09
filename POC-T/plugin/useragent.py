#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

"""
Functions to get user-agent string
edit by cdxy [i@cdxy.me]
May 9 Mon, 2016

usage:
from lib.util.useragent import *
str1 = get_random_agent()
str2 = firefox()
str3 = iphone()
str4 = google_bot()
...

tips:
init_UAlist(),get_random_agent()
these 2 methods should be called after [path-init-method] in lib.core.common
"""

import random
from lib.core.data import conf, th, paths, logger
from lib.core.common import getFileItems


def _init_UAlist(path):
    infoMsg = "loading HTTP User-Agent header(s) from "
    infoMsg += "file '%s'" % path
    logger.info(infoMsg)

    # TODO 此处 conf.RANDOM_UA 在其他地方暂时没有用到
    conf.RANDOM_UA = True
    th.UA_LIST = getFileItems(path)

    successMsg = "Total: %d" % len(th.UA_LIST)
    logger.info(successMsg)


def get_random_agent(path=paths.UA_LIST_PATH):
    if "UA_LIST" not in th:
        _init_UAlist(path)
    try:
        return random.sample(th.UA_LIST, 1)[0]
    except IOError, e:
        warnMsg = "unable to read HTTP User-Agent header "
        warnMsg += "file '%s'" % path
        logger.warning(warnMsg)
        return


def firefox():
    return 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'


def ie():
    return 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)'


def chrome():
    return 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30'


def opera():
    return 'Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50'


def iphone():
    return 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'


def google_bot():
    return 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


def msn_bot():
    return 'msnbot/1.1 (+http://search.msn.com/msnbot.htm)'


def yahoo_bot():
    return 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'
