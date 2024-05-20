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
                self.debug('is restoring;' + sub.getName() + ';')
                sub.process.interrupt(self.getName() + '(R)')
        if (self.owner != None):
            if (self.owner.canWork() == True):
                self.debug('Its recovery makes the owner up;' + self.owner.getName() + ';')
                self.owner.process.interrupt(self.getName() + '(R)')


    def canWork(self):
        return not self.thresholdReached()

    def run(self):
        self.boot()
        while True:
            while (self.working == True):
                try:
                    self.info(self.state+';;')
                    yield self.env.process(self.fail())
                    self.info('has failed by itself;;')
                    self.state='is down'
                    self.info(self.state+';;')
                    self.working = False
                    self.faultPropagation()
                    yield self.env.process(self.repair(self.repairman))
                    self.state='is up'
                    self.working=True
                    self.repairPropagation()
                except simpy.Interrupt as i:
                    (kind, sender) = utils.unpack_interrupt(i.cause)
                    self.warning('is receiving an interrupt;' + str(i.cause) + ';')
                    if(kind=='F'):
                        self.working = self.isStillWorking(sender)
                        self.debug('will continue?;' + str(self.working) + ';')
                        if(self.working==False):
                            self.state='is down'
                            self.info(self.state+';;')
                            self.faultPropagation()
                            wait=self.env.event()
                            while True:
                                try:
                                    yield wait  # Attesa indefinita fino a un nuovo interrupt
                                except simpy.Interrupt as i:
                                    kind, sender = utils.unpack_interrupt(i.cause)
                                    self.warning(f'is receiving an interrupt; {str(i.cause)}')
                                    self.working=self.canWork()
                                    if kind == 'R' and self.working:
                                        self.state='is up;;'
                                        self.repairPropagation()
                                        break
                        else:
                            self.state='is failing'
                            self.info(self.state+';;')




'''
STEFANO VERSION

  def run(self):
        self.boot()
        while True:
            self.working = True
            while (self.working == True):
                try:
                    self.info('is up;;')
                    yield self.env.process(self.fail())
                    self.info('has failed by itself;;')
                    self.working = False
                except simpy.Interrupt as i:
                    (kind, sender) = utils.unpack_interrupt(i.cause)
                    if (self.name == 'X_C3s' and sender == 'X_top'):
                        print('hey')
                    if (self.name == 'X_top' and sender == 'X_C2s'):
                        print('hey')
                    if (self.name == 'X_top' and sender == 'X_C3s'):
                        print('hey')
                        if (self.name == 'X_top' and sender == 'X_C1s'):
                            print('hey')

                    self.warning('is receiving an interrupt;' + str(i.cause) + ';')
                    self.working = self.isStillWorking(sender)
                    self.info('will continue?;' + str(self.working) + ';')
                finally:
                    if (self.working == False):
                        self.faultPropagation()
            while self.working == False:
                try:
                    self.error('is down;;')
                    yield self.env.process(self.repair(self.repairman))
                except simpy.Interrupt as i:
                    # gestire qua dentro sia quando sono stato rotto dalle subcomponent sia quando sono stato rotto dalle top component
                    (kind, sender) = utils.unpack_interrupt(i.cause)
                finally:
                    self.working = True
                    self.repairPropagation()




'''




class AndGate(Gate):
    def __init__(self, nname, mmtbf=0, mmttr=0):
        super().__init__(nname, 0, mmtbf, mmttr)

    def setSubcomponents(self, ssubcomponents):
        self.subcomponents = ssubcomponents
        self.threshold = len(self.subcomponents)

    def addSubcomponent(self, ssubcomponent):
        self.subcomponents.append(ssubcomponent)
        self.threshold = len(self.subcomponents)


class KooNGate(Gate):
    def __init__(self, nname, k, mmtbf=0, mmttr=0):
        super().__init__(nname, k, mmtbf, mmttr)

class OrGate(Gate):
    def __init__(self, nname, mmtbf=0, mmttr=0):
        super().__init__(nname, 1, mmtbf, mmttr)


