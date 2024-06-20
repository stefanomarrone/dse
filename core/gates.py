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

    def upCaseidPropagation(self):
        if (self.owner and self.owner.caseid<self.caseid):
            self.owner.caseid = self.caseid
            self.owner.caseidPropagation()

    def downCaseidPropagation(self):
        for s in self.subcomponents:
            if(s.caseid<self.caseid):
                s.caseid=self.caseid
                s.caseidPropagation()

    def caseidPropagation(self):
        self.upCaseidPropagation()
        self.downCaseidPropagation()

    def downFaultPropagation(self):
        for sub in self.subcomponents:
            if (sub.working == True):
                #yield self.env.timeout(1)
                sub.process.interrupt(str(self.caseid)+';'+self.getName() + '(F)')

    def isStillWorking(self,s):
        retval = False
        if (self.owner == None) or (s != self.owner.getName()):
            retval = not self.thresholdReached()
        return retval

    def repairPropagation(self):
        #for sub in self.subcomponents:
            #if (sub.working == False):
                #self.debug(str(self.caseid)+';'+'is restoring;' + sub.getName() )
                #yield self.env.timeout(1)
                #sub.process.interrupt(self.getName() + '(R)')
        if (self.owner != None):
            if (self.owner.canWork() == True):
                #self.debug(str(self.caseid)+';'+'Its recovery makes the owner up;' + self.owner.getName() + ';')
                #yield self.env.timeout(1)
                self.owner.process.interrupt(self.getName() + '(R)')


    def canWork(self):
        return not self.thresholdReached()

    def run(self):
        self.boot()
        while True:
            while (self.working == True):
                try:

                    #self.info(str(self.caseid)+';'+self.state+';;')
                    yield self.env.process(self.fail())
                    self.info(str(self.caseid)+';'+'failed by itself;;')
                    yield self.env.timeout(1)
                    self.state='is down'
                    self.faultCounter+=1
                    self.info(str(self.caseid)+';'+self.state+';;')
                    self.working = False
                    yield self.env.timeout(1)
                    self.faultPropagation()
                    self.caseid = self.caseid + 1
                    self.caseidPropagation()
                    yield self.env.process(self.repair(self.repairman))
                    self.state='is up'
                    self.working=True
                    self.info(str(self.caseid-1) + ';' + self.state + ';;')
                    yield self.env.timeout(1)
                    self.repairPropagation()



                except simpy.Interrupt as i:
                    (kind, sender) = utils.unpack_interrupt(i.cause)
                    #self.warning(str(self.caseid)+';''is receiving an interrupt;' + str(i.cause) )
                    if(kind=='F'):
                        self.working = self.isStillWorking(sender)
                        #self.debug(str(self.caseid)+';'+'will continue?;' + str(self.working))
                        if(self.working==False):
                            yield self.env.timeout(1)
                            self.state='is down'
                            self.faultCounter+=1
                            self.info(str(self.caseid-1)+';'+self.state+';;')
                            yield self.env.timeout(1)
                            self.faultPropagation()
                            wait=self.env.event()
                            while True:
                                try:
                                    yield wait  # Attesa indefinita fino a un nuovo interrupt
                                except simpy.Interrupt as i:
                                    kind, sender = utils.unpack_interrupt(i.cause)
                                    #self.warning(str(self.caseid)+';'+f'is receiving an interrupt; {str(i.cause)}')
                                    self.working=self.canWork()
                                    if kind == 'R' and self.working:
                                        self.state='is up'
                                        self.info(str(self.caseid-1) + ';' + self.state + ';;')
                                        yield self.env.timeout(1)
                                        self.repairPropagation()
                                        break
                        else:
                            self.state='is failing'
                            #yield self.env.timeout(1)
                            self.info(str(self.caseid-1)+';'+self.state+';;')



                    else:
                        self.state = 'is up'
                        self.info(str(self.caseid-1) + ';' + self.state + ';;')
                        self.working=True





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


