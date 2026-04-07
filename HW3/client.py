from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 9000))

while True:
    msg = input('Enter expression: ')
    if msg == 'q':
        break

    s.send(msg.encode())
    print('Result:', s.recv(1024).decode())

s.close()