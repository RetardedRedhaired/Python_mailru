#!/usr/bin/env python3
import queue
import json
import signal
import socket
import sys
import threading
import os
import requests
import configparser
import argparse
import logging
import bs4
from urllib.parse import urlparse
from collections import Counter



class Config():
    def __init__(self, config):
        self.port = int(config['Server']['Port'])
        self.log_path = config['Server']['Log_path']
        self.ip = config['Server']['IP']
        self.timeout = int(config['Server']['Timeout'])
        self.max_conn = int(config['Server']['Max_conn'])
        self.auth_key = config['Server']['Authorization']
        self.n = int(config['Server']['N'])


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
            chunk = None
        except socket.error:
            conn.close()
            break
        if not chunk:
            break
    return url.decode('utf-8')


def site_parser(url, n):
    words = Counter()
    response = requests.get(url)
    site = urlparse(response.url).netloc + urlparse(response.url).path
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    raw = soup.get_text().replace('\n', ' ').split(' ')
    for s in raw:
        if s.isalpha():
            words[s] += 1
    top_n_words = dict(words.most_common(n))
    top_n_words['site'] = site
    return json.dumps(top_n_words)


def master(sock, config, pipeline, event):
    while not event.is_set():
        sock.listen(config.max_conn)
        conn, addr = sock.accept()
        logging.info('connected: %s, port: %s', addr, config.port)
        url = url_parsing(conn)
        logging.info('GOT %s FROM %s', url, conn)
        pipeline.put((url, conn))
        logging.info("Master got url: %s", url)


def worker(pipeline, event, n):
    while not event.is_set() or not pipeline.empty():
        url, conn = pipeline.get()
        answr = site_parser(url, n)
        logging.info(
            "Worker storing message: %s (size=%d)", url, pipeline.qsize()
        )
        logging.info("SEND %s TO %s", url, conn)
        conn.sendall(answr.encode('utf-8'))
        conn.close()


def sig_handler(signal_name, frame):
    sys.exit(0)
    sys,exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGUSR1, sig_handler)
    print(os.getpid())
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
        threading.Thread(target=worker, args=(pipeline, event, config.n))
        for _ in range(config.max_conn)
    ]
    for wrkr in workers:
        wrkr.start()
    for wrkr in workers:
        wrkr.join()
    master.join()
