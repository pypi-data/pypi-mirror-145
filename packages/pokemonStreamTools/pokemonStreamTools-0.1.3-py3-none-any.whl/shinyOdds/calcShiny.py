import scipy.stats as stats
import functools
from typing import Tuple


@functools.lru_cache(maxsize=128)
def probShiny(nEncounters: float, odds: float, nShines: int) -> float:
    """
    Calculate the percentage of trials that have found the shinies by nEncounters
    :param nEncounters: The number of enocunters
    :param odds: The base odds of finding a shiny
    :param nShines: The number of shines that you're hunting
    :return: The percentage of trials that have found the shinies by nEncounters
    """
    return 1 - stats.binom.cdf(k=nShines - 1, n=nEncounters, p=odds)


@functools.lru_cache(maxsize=128)
def findProb(wantedP, odds, nShinies) -> Tuple[int, float]:
    """
    Calculate the number of encounters needed for a certain percentage
    :param wantedP: The wanted probability
    :param odds: The base odds of finding a shiny
    :param nShinies: The number of shinies that are being hunted
    :return: The number of encounters and the actual probability
    """
    minVal = 0
    maxVal = 2 ** 30  # About 1 billion, but this will have the same runtime
    n = int((minVal + maxVal) / 2)
    while not (probShiny(n - 1, odds, nShinies) < wantedP <= probShiny(n, odds, nShinies)):

        if probShiny(n, odds, nShinies) > wantedP:
            maxVal = min(maxVal, n)

        else:
            minVal = max(minVal, n)

        n = int((minVal + maxVal) / 2)

    return n, probShiny(n, odds, nShinies)
