#!/usr/bin/python3

import socket
import sys
import threading
import re
import mimetypes
import os.path

exitFlag = 0

HOST = 'localhost'
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

class respond () :

    methods = ['GET', 'HEAD']
    response_lines = {'200' : b'HTTP/1.1 200 OK\r\n', '404' : b'HTTP/1.1 404 Not Found\r\n', '400' : b'HTTP/1.1 400 Bad Request\r\n'} 
    

    def __init__ (self,conn,data) :
        self.conn = conn
        self.data = data
        self.body = b''
        self.request = {'method' : '', 'path' : '', 'status_code' : ''}
        self.header = b'Server : Python/0.1.0 (Custom)\r\nConnection: close\r\n'
        self.main_respond()
        
    def main_respond(self) : 
        partials = self.data.split('\r\n')

        if not self.validate_request(partials):
            reply = self.error_response() 
        else:                       
            self.parse_request(partials)            
            self.set_status_code()
            reply = respond.response_methods[self.request['status_code']](self)

        self.conn.sendall(reply)

    def validate_request(self, partials) :
        regex = r'^(' + r'|'.join(respond.methods) + r')(\s\/[A-Za-z1-9\/.]*)(\sHTTP\/1.1)$'
        return re.match(regex, partials[0])

    def parse_request(self, partials) : 

        method_regex = r'^[A-Z]{1,}(?= )'
        path_regex = r'\/.*(?= )'
        
        self.request['path'] = re.search(path_regex, partials[0]).group(0)
        if re.match(r'^.*\/$', self.request['path']) :    
            self.request['path'] = self.request['path']+'index.html'
        self.request['path'] = self.request['path'][1:]        
        
        self.request['method'] = re.search(method_regex, partials[0]).group(0)

    def readfile(self, path) :
        file_object = open(path, 'rb')
        buf = file_object.read()
        return buf
    
    def set_status_code(self) :
        
        if not self.request['method'] in respond.methods :
            self.request['status_code'] = '400'

        if os.path.isfile(self.request['path']) :
            self.request['status_code'] = '200'
        else :
            self.request['status_code'] = '404'

    def set_header(self, stream, status_code) :
        length = bytes(str(len(stream)), 'latin-1')
        ctype = mimetypes.guess_type(self.request['path'])[0].encode('latin-1')
        self.header = respond.response_lines[status_code] + self.header + b'Content-Length : '+ length + b'\r\n'
        if status_code == '200' :
            self.header = self.header + b'Content-Type : ' + ctype + b'\r\n'
        else :
            self.header = self.header + b'Content-Type : text/html\r\n'
        self.header = self.header + b'\r\n'

    def set_body(self, stream) : 
        self.body = stream
 
    def error_response(self) : 
        stream = b'<html><head><title>400 Bad Request</title></head><body>400 Bad Request</body></html>'
        self.set_header(stream, self.request['status_code'])
        self.set_body(stream)  

        if self.request['method'] == 'HEAD' :
            reply = self.header
        else :
            reply = self.header + self.body            
        
        return reply

    def notfound_response(self) :
        stream = b'<html><head><title>404 Not Found</title></head><body>404 Not Found</body></html>'
        self.set_header(stream, self.request['status_code'])
        self.set_body(stream)        
        
        if self.request['method'] == 'HEAD' :
            reply = self.header
        else :
            reply = self.header + self.body

        return reply    

    def response(self) :
        stream = self.readfile(self.request['path'])
        self.set_header(stream, self.request['status_code'])
        self.set_body(stream)

        if self.request['method'] == 'HEAD' :
            reply = self.header
        else :
            reply = self.header + self.body

        return reply

    response_methods = {'200' : response,  '404' : notfound_response, '400' : error_response}

def tcp_connect(conn) : 
    data = conn.recv(1024)
    data = data.decode('latin-1')
    print(data)       
    respond(conn,data)
    conn.close()

while 1:
    conn, addr = s.accept()
    print('Connected with ',addr[0],' : ',str(addr[1]))
    myThread(conn).start()

s.close()
