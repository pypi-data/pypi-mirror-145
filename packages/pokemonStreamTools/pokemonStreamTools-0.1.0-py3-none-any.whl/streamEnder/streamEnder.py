#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from obswebsocket import obsws, requests
import argparse
import os
import getpass


def parse_args():
    parser = argparse.ArgumentParser(description='Stream Ender.')
    parser.add_argument('encounter_fname', metavar='Encounters.txt', type=str,
                        help='The file location for the number of encounters')
    parser.add_argument('hostname', metavar='OBS_IP', type=str,
                        help='The IP of the OBS instance')
    parser.add_argument('port', metavar='PORT', type=int,
                        help='The port for the OBS instance')
    parser.add_argument('--password', nargs='?', type=str, default=None,
                        help='The password for the OBS instance')
    parser.add_argument('--timeout', nargs='?', const=300, type=float, default=300,
                        help='The time (in seconds) to start the \"End Stream\" screen')
    parser.add_argument('--EndStreamTime', nargs='?', const=60, type=float, default=60,
                        help='The time (in seconds) to wait on the end screen')
    parser.add_argument('--EndStreamName', nargs=1, type=str,
                        help='The name for the end stream scene')
    return parser.parse_args()


def run(host, port, password, fileName, timeout, endStreamTime, endStreamName):
    ws = obsws(host, port, password)
    # ws = obsws(host, port)
    ws.connect()

    while time.time() - os.path.getmtime(fileName) < timeout:
        time.sleep(timeout - (time.time() - os.path.getmtime(fileName)))

    try:
        print("Switching Scenes")
        ws.call(requests.SetCurrentScene(endStreamName))
        print("Waiting to end stream")
        time.sleep(endStreamTime)
        print("Stopping Streaming")
        ws.call(requests.StopStreaming())
        print("Streaming Stopped")
    except Exception as e:
        print(e)
    finally:
        ws.disconnect()


def main():
    args = parse_args()
    host = args.hostname
    port = args.port
    if args.password is None:
        password = getpass.getpass()
    else:
        password = args.password

    run(host, port, password, args.encounter_fname, args.timeout, args.EndStreamTime, args.EndStreamName)


if __name__ == "__main__":
    main()
