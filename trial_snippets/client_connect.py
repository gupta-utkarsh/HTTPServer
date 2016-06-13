#!/usr/bin/python3

import socket
import sys

try:    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ',str(msg[0]),' , Error message : ',msg[1])
    sys.exit(); 

print('Socket Created')

host = 'www.google.com'
port = 80

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

print('Ip address of ',host,' is ',remote_ip)

s.connect((remote_ip , port))

print('Socket connected to ',host,' on ip ',remote_ip)

message = "GET / HTTP/1.1\r\n\r\n"

try:
    s.sendall(bytes(message,'UTF-8'))
except socket.error:
    print('Send failed')
    sys.exit()

print('Message send successfully')

reply = s.recv(4096)

print(reply.decode('unicode_escape'))

s.close()
