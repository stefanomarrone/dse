import random
import numpy
import statistics
from scipy.stats import sem, t


def lottery(probabilities):
    ssum = 0
    cumulative = list()
    for p in probabilities:
        ssum = ssum + p
        cumulative.append(ssum)
    guess = random.random()
    counter = 0
    maxnum = len(probabilities)
    found = False
    while (not found) and (counter < maxnum):
        found = guess <= cumulative[counter]
        counter = counter + 1
    return counter - 1

def uniform(min,max):
    guess = numpy.random.random() * (max-min) + min
    return guess

def expGuess(beta):
    guess = numpy.random.exponential(beta)
    return guess

def unpack_interrupt(cause):
    kind = cause[-2]
    sender = cause[0:-3]
    return (kind, sender)

def mean(data):
    return statistics.mean(data)

def std(data):
    return statistics.stdev(data)

def confidence(data, conflevel):
    n = len(data)
    m = mean(data)
    std_err = sem(data)
    h = std_err * t.ppf((1 + conflevel) / 2, n - 1)
    start = m - h
    end = m + h
    return start, end

def confidence95(data):
    return confidence(data,0.95)

def confidence99(data):
    return confidence(data,0.99)

def zero(arg):
    return 0