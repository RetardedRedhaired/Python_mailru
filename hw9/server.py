#!/usr/bin/env python3
import concurrent.futures
import queue
import socket
import sys
import threading

import requests
import configparser
import argparse
import logging



class Config():
    def __init__(self, config):
        self.port = int(config['Server']['Port'])
        self.log_path = config['Server']['Log_path']
        self.ip = config['Server']['IP']
        self.timeout = int(config['Server']['Timeout'])
        self.max_conn = int(config['Server']['Max_conn'])
        self.auth_key = config['Server']['Authorization']


def config_parsing():
    parser = argparse.ArgumentParser(description='Server script')
    parser.add_argument('config_path', action="store", help="Absolute or local path to config file")
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config_path)
    return config


def create_connection(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (config.ip, config.port)
    try:
        sock.bind(addr)
    except OSError:
        print('This port is already in use')
        sys.exit(1)
    else:
        return sock


def url_parsing(conn):
    url = b''
    while True:
        try:
            chunk = conn.recv(1024)
            if not chunk:
                break
            url += chunk
        except socket.error:
            conn.close()
            break
        if not chunk:
            break
    return url.decode('utf-8')


def master(sock, config, pipeline, event):
    while not event.is_set():
        sock.listen(config.max_conn)
        conn, addr = sock.accept()
        print(f'connected: {addr}, port: {config.port}')
        url = url_parsing(conn)
        print(f'GOT {url}')
        pipeline.put((url, conn))
        logging.info("Master got url: %s", url)


def worker(pipeline, event):
    while not event.is_set() or not pipeline.empty():
        print('WORKER STARTED')
        url, conn = pipeline.get()
        print(url)
        response = requests.get(url)
        logging.info(
            "Worker storing message: %s (size=%d)", url, pipeline.qsize()
        )
        conn.sendall(url.encode('utf-8'))
        conn.close()


if __name__ == '__main__':
    config = Config(config_parsing())
    form = "%(asctime)s: %(message)s"
    logging.basicConfig(filename=config.log_path, format=form, level=logging.INFO,
                        datefmt="%H:%M:%S")
    sock = create_connection(config)
    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    master = threading.Thread(target=master, args=(sock, config, pipeline, event))
    master.start()
    workers = [
        threading.Thread(target=worker, args=(pipeline, event))
        for _ in range(config.max_conn)
    ]
    for wrkr in workers:
        wrkr.start()
    for wrkr in workers:
        wrkr.join()
    master.join()
