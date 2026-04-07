import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9000))

msg = sock.recv(1024)
print(msg.decode())

name = '김지민'
sock.send(name.encode())

data = sock.recv(4)
student_id = int.from_bytes(data, 'big')
print('student id:', student_id)

sock.close()