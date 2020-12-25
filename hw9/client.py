#!/usr/bin/env python3

import socket
import threading
import concurrent.futures
from sys import argv
import queue


def create_connection():
    sock = socket.socket()
    sock.settimeout(2)
    port = 10001
    sock.connect(('127.0.0.1', port))
    return sock


def urls_pars(addr, pipeline):
    with open(addr, 'r') as f:
        for line in f:
            pipeline.put(line.rstrip('\n'))


def request(pipeline):
    while not pipeline.empty():
        conn = create_connection()
        url = pipeline.get()
        conn.sendall(url.encode('utf-8'))
        data = b''
        while True:
            try:
                print("TEST recv error")
                chunk = conn.recv(1024)
                print(chunk)
                if not chunk:
                    break
                data += chunk
            except socket.error:
                print("TEST socket error")
                conn.close()
                break
            if not chunk:
                print("TEST")
                break
        #print(data.decode('utf-8'))
        conn.close()


if __name__ == '__main__':
    try:
        addr = argv[1]
        n_threads = int(argv[2])
    except IndexError:
        print('Parameters not found')
    else:
        pipeline = queue.Queue(maxsize=100)
        urls_pars(addr, pipeline)
        workers = [
            threading.Thread(target=request, args=(pipeline,))
            for _ in range(n_threads)
        ]
        for wrkr in workers:
            wrkr.start()
        for wrkr in workers:
            wrkr.join()
