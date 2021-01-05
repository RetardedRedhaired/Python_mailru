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
from functools import partial


class UrlCounter:
    def __init__(self):
        self.num = 0


class Config:
    def __init__(self, config):
        self.port = int(config['Server']['Port'])
        self.log_path = config['Server']['Log_path']
        self.ip = config['Server']['IP']
        self.timeout = int(config['Server']['Timeout'])
        self.max_conn = int(config['Server']['Max_conn'])
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
        pipeline.put(conn)
    if event.is_set():
        print('MASTER EVENT')
        sock.close()


def worker(pipeline, event, n, url_counter):
    while not event.is_set() or not pipeline.empty():
        conn = pipeline.get()
        url = url_parsing(conn)
        logging.info("Worker got url: %s", url)
        answr = site_parser(url, n)
        logging.info(
            "Worker storing message: %s (size=%d)", url, pipeline.qsize()
        )
        logging.info("SEND %s TO %s", url, conn)
        conn.sendall(answr.encode('utf-8'))
        url_counter.num += 1
        conn.close()
    if event.is_set():
        print('WORKER EVENT')


def sig_handler(signal_name, frame, event, url_counter, sock):
    event.set()
    sock.close()
    print(f'total urls parsed: {url_counter.num}')
    signal.raise_signal(signal.SIGKILL)
    sys.exit(1)


if __name__ == '__main__':
    print(os.getpid())
    config = Config(config_parsing())
    form = "%(asctime)s: %(message)s"
    logging.basicConfig(filename=config.log_path, format=form, level=logging.INFO,
                        datefmt="%H:%M:%S")
    sock = create_connection(config)
    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    url_counter = UrlCounter()
    master = threading.Thread(target=master, args=(sock, config, pipeline, event))
    master.start()
    workers = [
        threading.Thread(target=worker, args=(pipeline, event, config.n, url_counter))
        for _ in range(config.max_conn)
    ]
    signal.signal(signal.SIGUSR1,
                  partial(sig_handler, event=event, url_counter=url_counter, sock=sock))
    for wrkr in workers:
        wrkr.start()
    for wrkr in workers:
        wrkr.join()
    master.join()
