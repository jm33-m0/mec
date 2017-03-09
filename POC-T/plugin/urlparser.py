#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me

import urlparse


def get_domain(url):
    """
    added by cdxy May 8 Sun,2016

    Use:
    get_domain('http://cdxy.me:80/cdsa/cda/aaa.jsp?id=2#')

    Return:
    'http://cdxy.me:80'
    """
    p = urlparse.urlparse(url)
    return urlparse.urlunsplit([p.scheme, p.netloc, '', '', ''])


def iterate_path(ori_str):
    """
    added by cdxy May 8 Sun,2016

    Use:
    iterate_path_to_list('http://cdxy.me:80/cdsa/cda/aaa.jsp?id=2#')

    Return:
    ['http://cdxy.me:80/cdsa/cda/aaa.jsp?id=2#',
     'http://cdxy.me:80/'
     'http://cdxy.me:80/cdsa',
     'http://cdxy.me:80/cdsa/cda',
     'http://cdxy.me:80/cdsa/cda/aaa.jsp']

    """
    parser = urlparse.urlparse(ori_str)
    _path_list = parser.path.replace('//', '/').strip('/').split('/')
    _ans_list = set()
    _ans_list.add(ori_str)

    if not _path_list[0]:
        return _ans_list

    _ans_list.add(get_domain(ori_str))
    s = ''
    for each in _path_list:
        s += '/' + each
        _ans_list.add(urlparse.urljoin(ori_str, s))
    return _ans_list


if __name__ == '__main__':
    url = 'http://cdxy.me:80/cdsa/cda/aaa.jsp?id=2#'
    print urlparse.urlparse(url)
    print get_domain(url)
    for each in iterate_path(url):
        print each
