#!/usr/bin/env python3

from sys import argv
import socket
import requests
from json import dumps
import configparser
import time
import argparse
import logging


class Config():
    def __init__(self, config):
        self.port = int(config['Server']['Port'])
        self.log_path = config['Server']['Log_path']
        self.ip = config['Server']['IP']
        self.demon = int(config['Server']['Demon'])
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


def transform_time(time_c):
    return time.strftime('%X', time.gmtime(time_c))


def log(config, start_time, end_time, con_len):
    logging.basicConfig(filename=config.log_path, level=logging.INFO)
    logging.info(f'Start time: {transform_time(start_time)}, end time: {transform_time(end_time)}, work time: {transform_time(end_time - start_time)}, content lenght: {con_len} bytes')


def error_log(config, error):
    logging.basicConfig(filename=config.log_path, level=logging.INFO)
    logging.error(f'{transform_time(time.time())} {error} ')


def create_connection(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (config.ip, config.port)
    try:
        sock.bind(addr)
    except OSError:
        error_log(config, 'This port is already in use')
    else:
        return sock


def listen_mod(sock, config):
    while True:
        sock.listen(config.max_conn)
        conn, addr = sock.accept()
        start_time = time.time()
        print(f'connected: {addr}, port: {config.port}')
        params = conn.recv(1024).decode('utf-8')
        response = req(params, config)
        conn.sendall(response[0].encode('utf-8'))
        log(config, start_time, time.time(), response[1].get('Content-Length'))
    conn.close()


def req(params, config):
    url = 'https://the-one-api.dev/v2/'
    headers = {'Authorization': config.auth_key}
    timeout = config.timeout
    response = requests.get(url+params, headers=headers, timeout=timeout)
    try:
        answer = response.json()
    except ValueError:
        error_log(config, response.status_code)
        return (str(response.status_code), response.headers)
    else:
        return (dumps(answer, sort_keys=True, indent=4), response.headers)


if __name__ == '__main__':
    config = Config(config_parsing())
    sock = create_connection(config)
    listen_mod(sock, config)
