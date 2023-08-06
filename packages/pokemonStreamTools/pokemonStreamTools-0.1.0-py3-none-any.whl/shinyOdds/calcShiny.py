import scipy.stats as stats
import functools


@functools.lru_cache(maxsize=128)
def probShiny(nEncounters, odds, nShines):
    return 1 - stats.binom.cdf(k=nShines - 1, n=nEncounters, p=odds)


@functools.lru_cache(maxsize=128)
def findProb(wantedP, odds, nShinies):
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
