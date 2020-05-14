import utils
import simpy

from blackboard import Blackboard
from log import Loggable
from exceptions import DependabilityException


class Component(Loggable):

    def __init__(self, nname, qqueue, eenv, mmtbf=0, mmttr=0):
        super().__init__(nname, qqueue, eenv)
        self.owner = None
        self.subcomponents = list()
        self.mtbf = mmtbf
        self.mttr = mmttr
        board = Blackboard()
        self.finalTime = board.get('stoptime')
        self.debugLevel = board.get('debugLevel')
        self.process = self.env.process(self.run())

    def setSubcomponents(self, ssubcomponents):
        self.subcomponents = ssubcomponents

    def addSubcomponent(self, ssubcomponent):
        self.subcomponents.append(ssubcomponent)

    def setOwner(self, oowner):
        self.owner = oowner

    def waitForEvent(self, beta):
        guess = self.finalTime if (beta == 0) else utils.expGuess(beta)
        yield self.env.timeout(guess)

    def faultPropagation(self,cause=''):
        self.downFaultPropagation(cause)
        self.upFaultPropagation(cause)

    def repairPropagation(self):
        for sub in self.subcomponents:
            if (self.debugLevel == True):
                self.log('is restoring;' + sub.getName() + ';')
            sub.process.interrupt(self.getName())

    def fail(self):
        yield self.env.process(self.waitForEvent(self.mtbf))

    def repair(self):
        yield self.env.process(self.waitForEvent(self.mttr))

    def boot(self):
        pass

    def run(self):
        self.boot()
        while True:
            faultCause = ''
            self.log('is working;;')
            try:
                yield self.env.process(self.fail())
                self.log('has failed by itself;;')
            except simpy.Interrupt as i:
                faultCause = i.cause
                self.log('is interrupted by;' + faultCause + ';')
            finally:
                self.faultPropagation(faultCause)
            self.log('is down;;')
            try:
                yield self.env.process(self.waitForEvent(self.mtbf))
            except simpy.Interrupt as i:
                pass
            finally:
                self.log('has been repaired;;')
                self.repairPropagation()

    def downFaultPropagation(self, cause):
        for sub in self.subcomponents:
            candidate = sub.getName()
            if (candidate != cause):
                if (self.debugLevel == True):
                    self.log('is breaking;' + sub.getName() + ';')
                sub.process.interrupt(self.getName())

    def upFaultPropagation(self,cause):
        if (self.owner is not None) and (self.owner.getName() != cause):
            if (self.debugLevel == True):
                self.log('is breaking;' + self.owner.getName() + ';')
            self.owner.process.interrupt(self.getName())
