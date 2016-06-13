#! /usr/bin/python3

import socket
import sys
import threading

exitFlag = 0

HOST = ''
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ', str(msg[0]) ,' Message ', msg[1])
s.listen(10)


class myThread (threading.Thread) : 
    def __init__ (self, conn):
        threading.Thread.__init__(self)
        self.conn = conn      
    def run(self):
        tcp_connect(self.conn)


def tcp_connect(conn) : 

    while True:
        data = conn.recv(1024)
        reply = 'OK...' + data.decode('utf-8')
        if not data:
            break
        conn.sendall(bytes(reply, 'utf-8'))
    
    conn.close()

while 1:
    conn, addr = s.accept()
    print('Connected with ',addr[0],' : ',str(addr[1]))
    myThread(conn).start()

s.close()
