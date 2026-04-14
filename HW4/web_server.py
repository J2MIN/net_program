from socket import *

HOST = ''
PORT = 80
BUF_SIZE = 1024

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

print(f'Web server is running on port {PORT}...')

while True:
    client_socket, addr = server_socket.accept()
    print('Connection from:', addr)

    try:
        # 1) HTTP 요청 받기
        data = client_socket.recv(BUF_SIZE)
        if not data:
            client_socket.close()
            continue

        # 2) 바이트 -> 문자열
        msg = data.decode('utf-8', errors='ignore')
        print('----- Request Message -----')
        print(msg)

        # 3) 첫 번째 줄(요청 라인)만 추출
        req = msg.split('\r\n')
        request_line = req[0]
        print('Request Line:', request_line)

        # 예: GET /index.html HTTP/1.1
        parts = request_line.split()

        # 요청 형식이 이상하면 404 처리
        if len(parts) < 2:
            response = 'HTTP/1.1 404 Not Found\r\n\r\n'
            response += '<HTML><HEAD><TITLE>Not Found</TITLE></HEAD>'
            response += '<BODY>Not Found</BODY></HTML>'
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
            continue

        method = parts[0]
        path = parts[1]           # /index.html
        filename = path.lstrip('/')  # index.html

        # 루트("/")로 들어오면 index.html로 처리하고 싶으면 아래 사용 가능
        # if filename == '':
        #     filename = 'index.html'

        print('Requested file:', filename)

        # 4) 지원 가능한 파일인지 확인하고 열기
        if filename == 'index.html':
            f = open(filename, 'r', encoding='utf-8')
            mimeType = 'text/html; charset=utf-8'
            file_data = f.read()
            f.close()

            # 5) 200 OK 응답 전송
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += 'Content-Type: ' + mimeType + '\r\n'
            response_header += '\r\n'

            client_socket.send(response_header.encode('utf-8'))
            client_socket.send(file_data.encode('utf-8'))

        elif filename == 'iot.png':
            f = open(filename, 'rb')
            mimeType = 'image/png'
            file_data = f.read()
            f.close()

            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += 'Content-Type: ' + mimeType + '\r\n'
            response_header += '\r\n'

            client_socket.send(response_header.encode('utf-8'))
            client_socket.send(file_data)

        elif filename == 'favicon.ico':
            f = open(filename, 'rb')
            mimeType = 'image/x-icon'
            file_data = f.read()
            f.close()

            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += 'Content-Type: ' + mimeType + '\r\n'
            response_header += '\r\n'

            client_socket.send(response_header.encode('utf-8'))
            client_socket.send(file_data)

        else:
            # 6) 없는 파일이면 404 Not Found
            response = 'HTTP/1.1 404 Not Found\r\n'
            response += '\r\n'
            response += '<HTML><HEAD><TITLE>Not Found</TITLE></HEAD>'
            response += '<BODY>Not Found</BODY></HTML>'

            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print('Error:', e)

    finally:
        client_socket.close()