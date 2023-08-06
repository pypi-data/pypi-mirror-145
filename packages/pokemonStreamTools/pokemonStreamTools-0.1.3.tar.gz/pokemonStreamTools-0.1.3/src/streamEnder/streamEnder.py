#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from obswebsocket import obsws, requests
import argparse
import os
import getpass


def parse_args() -> argparse.Namespace:
    """
    Function for parsing the arguments
    :return: The args passed in
    """
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


def run(host: str, port: int, password: str, fileName: str, timeout: float, endStreamTime: float, endStreamName: str):
    """
    Function to run the server shutdown and file monerating
    :param host: The hostname of the OBS instance (usually localhost)
    :param port: The port of the OBS instance
    :param password: The password for the OBS instance
    :param fileName: The filename of the encounters file
    :param timeout: The time (in seconds) for how long the encounters file can go unmodified before the shutdown process begins
    :param endStreamTime: The time (in seconds) to wait on the stream ending scene
    :param endStreamName: The name of th scene ending scene
    :return:
    """
    ws = obsws(host, port, password)

    ws.connect()

    # check if the file's last modified time is past the timeout if not, then sleep for the remainder of the time in
    # the timeout Only 2 checks need to be done for an unmodified file in the worst case because the program sleeps
    # until the timeout is 0
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
    """
    The main function
    :return:
    """
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
