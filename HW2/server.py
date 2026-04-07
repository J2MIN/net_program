import socket

student_id = 20201536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 9000))
s.listen(2)

while True:
    client, addr = s.accept()
    print('Connection from', addr)

    client.send(b'Hello ' + addr[0].encode())

    name = client.recv(1024).decode()
    print('name:', name)

    client.send(student_id.to_bytes(4, 'big'))

    client.close()