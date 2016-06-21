#!/usr/bin/python3

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
    def __init__ (self, conn) :
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        tcp_connect(self.conn)

def tcp_connect(conn) : 
    while True:
        data = conn.recv(1024)
        data = data.decode('utf-8')
        if not data:
            break
        print(data)       
 
        '''
        respond(self,conn,data).getResponse()
        flag = validate_request(data)
        if not flag:
            conn.sendall(bytes('LOL', 'utf-8'))     
        '''

        filename = 'index.html'
        file_object = open(filename)
        body = file_object.read()
        
        '''body = '<html>\r\n\t<head>\r\n\t\t<title>hello</title>\r\n\t</head>\r\n\t<body>\r\n\t\tLOL\r\n\t</body>\r\n</html>\r\n'''

        length = str(len(body))
        reply = 'HTTP/1.1 200 OK\r\nServer : Python/0.1.0 (Custom)\r\nContent-Type : text/html\r\nContent-Length : '+length+'\r\n\r\n'+body
        conn.sendall(bytes(reply, 'utf-8'))
    
    conn.close()

while 1:
    conn, addr = s.accept()
    print('Connected with ',addr[0],' : ',str(addr[1]))
    myThread(conn).start()

s.close()
