import random
import numpy


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
    while ((not found) and (counter < maxnum)):
        found = guess <= cumulative[counter]
        counter = counter + 1
    return counter - 1

def expGuess(beta):
    guess = numpy.random.exponential(beta)
    return guess

def unpack_interrupt(cause):
    kind = cause[-2]
    sender = cause[0:-3]
    return (kind, sender)