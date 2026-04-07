from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 9000))
s.listen(5)
print('waiting...')

while True:
    client, addr = s.accept()
    print('connection from', addr)

    while True:
        data = client.recv(1024)
        if not data:
            break

        expr = data.decode().replace(' ', '')

        try:
            op = None
            for ch in ['+', '-', '*', '/']:
                if ch in expr:
                    op = ch
                    break

            if op is None:
                result = 'Try again'
            else:
                left, right = expr.split(op)
                left = int(left)
                right = int(right)

                if op == '+':
                    result = str(left + right)
                elif op == '-':
                    result = str(left - right)
                elif op == '*':
                    result = str(left * right)
                elif op == '/':
                    result = f'{left / right:.1f}'

        except:
            result = 'Try again'

        client.send(result.encode())

    client.close()