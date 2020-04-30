import random
import numpy
from log import Loggable


class TooSimpleRepairable(Loggable):
    def __init__(self, eenv, qqueue, nname, ffProb, mmttr):
        super().__init__(nname, qqueue)
        self.fProb = ffProb
        self.mttr = mmttr
        self.env = eenv

    def fail(self):
        self.log(' has failed @' + str(self.env.now))

    def repair(self):
        yield self.env.timeout(self.mttr)
        self.log(' has been repaired @' + str(self.env.now))

    def step(self):
        guess = (random.random() < self.fProb)
        if (guess):
            self.fail()
            yield self.env.process(self.repair())
        else:
            yield self.env.process(self.do())


class Fault(Loggable):
    def __init__(self, eenv, qqueue, nname, mmtbf, mmttr):
        super().__init__(nname, qqueue)
        self.mtbf = mmtbf
        self.mttr = mmttr
        self.env = eenv
        self.env.process(self.run())

    def waitForEvent(self, beta, message):
        guess = numpy.random.exponential(beta)
        yield self.env.timeout(guess)
        self.log(message + str(self.env.now))

    def fail(self):
        yield self.waitForEvent(self.mtbf, ' has failed @')

    def repair(self):
        yield self.waitForEvent(self.mttr, ' has been repaired @')

    def run(self):
        while True:
            yield self.env.process(self.fail())
            yield self.env.process(self.repair())
