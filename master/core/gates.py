import simpy
import core.utils as utils
from core.components import Component


class Gate(Component):
    def __init__(self, nname, kk, mmtbf=0, mmttr=0):
        super().__init__(nname, mmtbf, mmttr)
        self.threshold = kk
        self.subcomponents = list()

    def addSubComponent(self,component):
        self.subcomponents.append(component)

    def setSubcomponents(self,subs):
        self.subcomponents = subs

    def setFailureThreshold(self, kk):
        self.threshold = kk

    def getBrokenNumber(self):
        temp = list(filter(lambda x: x.working == False,self.subcomponents))
        return len(temp)

    def thresholdReached(self):
        return (self.getBrokenNumber() >= self.threshold)

    def downFaultPropagation(self):
        for sub in self.subcomponents:
            if (sub.working == True):
                sub.process.interrupt(self.getName() + '(F)')

    def isStillWorking(self,s):
        retval = False
        if (self.owner == None) or (s != self.owner.getName()):
            retval = not self.thresholdReached()
        return retval

    def repairPropagation(self):
        for sub in self.subcomponents:
            if (sub.working == False):
                self.log('is restoring;' + sub.getName() + ';',0)
                sub.process.interrupt(self.getName() + '(R)')

    def run(self):
        self.boot()
        while True:
            self.working = True
            while (self.working == True):
                try:
                    self.log('is up;;',2)
                    yield self.env.process(self.fail())
                    self.log('has failed by itself;;',0)
                    self.working = False
                except simpy.Interrupt as i:
                    (kind, sender) = utils.unpack_interrupt(i.cause)
                    self.log('is receiving an interrupt;' + str(i.cause) + ';',0)
                    self.working = self.isStillWorking(sender)
                    self.log('will continue?;' + str(self.working) + ';',0)
                finally:
                    if (self.working == False):
                        self.faultPropagation()
            while self.working == False:
                try:
                    self.log('is down;;',2)
                    yield self.env.process(self.repair())
                except simpy.Interrupt as i:
                    (kind, sender) = utils.unpack_interrupt(i.cause)
                finally:
                    self.working = True
                    self.repairPropagation()


class AndGate(Gate):
    def __init__(self, nname, mmtbf=0, mmttr=0):
        super().__init__(nname, 0, mmtbf, mmttr)

    def setSubcomponents(self, ssubcomponents):
        self.subcomponents = ssubcomponents
        self.threshold = len(ssubcomponents)

    def addSubcomponent(self, ssubcomponent):
        self.subcomponents.append(ssubcomponent)
        self.threshold += 1


class KooNGate(Gate):
    def __init__(self, nname, k, mmtbf=0, mmttr=0):
        super().__init__(nname, k, mmtbf, mmttr)

class OrGate(Gate):
    def __init__(self, nname, mmtbf=0, mmttr=0):
        super().__init__(nname, 1, mmtbf, mmttr)


