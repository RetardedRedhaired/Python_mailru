#!/usr/bin/env python3

import socket
from sys import argv


def create_connection():
    sock = socket.socket()
    sock.settimeout(2)
    port = 10001
    sock.connect(('127.0.0.1', port))
    return sock


def request(sock, params):
    sock.sendall(params.encode('utf-8'))
    data = b''
    while True:
        try:
            chunk = sock.recv(1024)
            if not chunk:
                break
            data += chunk
        except socket.error:
            sock.close()
            break
        if not chunk:
            break
    print(data.decode('utf-8'))
    sock.close()


if __name__ == '__main__':
    conn = create_connection()
    try:
        params = argv[1]
    except IndexError:
        print('Parameters not found')
        conn.close()
    else:
        request(conn, params)
