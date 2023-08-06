#!/usr/bin/env python
# coding: utf-8

import math
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import time
import matplotlib.ticker as mtick
import argparse
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from typing import List
from .calcShiny import probShiny
import re

plt.rcParams.update({'font.size': 22})


def parse_arguments():
    parser = argparse.ArgumentParser(description='Time to shiny Hunt.')
    parser.add_argument('encounter_fname', metavar='Encounters.txt', type=str,
                        help='The file location for the number of encounters')
    parser.add_argument('odds', metavar='Odds', type=str,
                        help='The odds to find a shiny (i.e. 1/4096)')

    parser.add_argument('--nShinies', nargs='?', const=1, type=int, default=1,
                        help='The number of shinies you\'re hunting for')

    return parser.parse_args()


class ShinyCounterHandler(PatternMatchingEventHandler):
    patterns: List = ["*"]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    nEncounters = -1

    def __init__(self, args):
        self.nShines = args.nShinies
        self.odds = args.odds.split('/')
        self.odds = float(self.odds[0]) / float(self.odds[1])
        self.fname = args.encounter_fname
        self.patterns[0] = self.fname
        self.n = np.array(range(int(10 * self.nShines / (self.odds))))
        self.probs = np.array([probShiny(_n, self.odds, self.nShines) for _n in self.n])
        self.comb = np.column_stack((self.n, self.probs))
        self.probs *= 100

        self.oddsStr = self.odds.as_integer_ratio()
        if self.oddsStr[1] > 1000000:
            self.oddsStr = [1, self.odds ** -1]

        self.oddsStr = f"{self.oddsStr[0]}/{self.oddsStr[1]}"
        self.lastModified = 0
        super(ShinyCounterHandler, self).__init__()

    def getEncounters(self) -> int:
        if os.path.exists(self.fname):
            with open(self.fname, 'r') as f:
                line = f.readline()
            nEncounters = int(re.findall(r'[0-9]+', line)[0])
        return nEncounters

    def on_modified(self, event):
        if time.time() - self.lastModified < .25:
            return

        folder = os.path.dirname(self.fname)
        try:
            nEncounters = self.getEncounters()
        except AttributeError:
            return
        self.lastModified = time.time()

        p = probShiny(nEncounters, self.odds, self.nShines)

        self.textFiles(p, nEncounters, folder)
        self.plot(p, nEncounters, folder)

    def textFiles(self, p, nEncounters, folder):
        print(
            f'P = {100 * p:.2f}% ({self.oddsStr} base odds) {"(" + str(self.nShines) + " total shines)" if self.nShines > 1 else ""}')
        with open(os.path.join(folder, 'odds.txt'), 'w+') as f:
            f.write(f'Current Odds: {100 * p:.2f}%')

        if p < .5:
            numToReach = self.comb[:, 0][self.comb[:, 1] > .5][0] - nEncounters
            percToReach = 50
        elif p < .75:
            numToReach = self.comb[:, 0][self.comb[:, 1] > .75][0] - nEncounters
            percToReach = 75
        elif p < .9:
            numToReach = self.comb[:, 0][self.comb[:, 1] > .9][0] - nEncounters
            percToReach = 90
        elif p < .999:
            numToReach = self.comb[:, 0][self.comb[:, 1] > .999][0] - nEncounters
            percToReach = 99.9

        with open(os.path.join(folder, 'next.txt'), 'w+') as f:
            if p < .999:
                print(f"Number of encounters until >{percToReach}%: {int(numToReach)}")
                f.write(f"Number of encounters until >{percToReach}%: {int(numToReach)}")
            else:
                f.write(f"Gotta get some better luck")

    def plot(self, p, nEncounters, folder):
        self.ax.cla()
        self.ax.plot(self.n, self.probs, label="Bimodal CDF")
        self.ax.hlines([p * 100], xmin=0, xmax=max(self.n), colors="r", label="Current Value", linestyles='dashed')
        self.ax.vlines([nEncounters], ymin=0, ymax=100, colors="r", linestyles='dashed')
        # ax.hlines([pNext], xmin=0, xmax=max(n), colors='r', linestyles='dashed', label="Next Value")
        # ax.vlines([nEncounters+intbox.value], ymin=0, ymax=1, colors='r', linestyles='dashed')
        self.ax.vlines([1 / self.odds], ymin=0, ymax=100, colors='g', linestyles='dashed', label="Odds")
        self.ax.set_xlabel("Number of Encounters")
        self.ax.set_ylabel(f"Chance to Have Gotten Shiny Mon")
        self.ax.legend()
        self.ax.grid()
        self.ax.set_xscale("log")
        self.ax.set_xlim([max(nEncounters / 10, 1), np.amax(self.n)])
        self.ax.yaxis.set_major_formatter(mtick.PercentFormatter())

        plt.tight_layout()
        plt.savefig(os.path.join(folder, 'encGraph.png'))
        os.utime(os.path.join(folder, 'encGraph.png'), (time.time(), time.time()))
        self.ax.cla()


def main():
    args = parse_arguments()
    event_handler = ShinyCounterHandler(args)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(args.encounter_fname), recursive=False)
    # observer.schedule(event_handler, path="StreamCounters/", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
