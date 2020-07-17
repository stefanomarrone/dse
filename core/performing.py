from core.components import Component
from core.gates import Gate, OrGate
from core.boards import Configuration
from simpy import Interrupt
from core.log import Loggable
from core.measures import Recorder

class Behaviour(Loggable):
    def __init__(self, nname):
        super().__init__(nname)
        self.onrun = True
        self.infinite = Configuration().get('stoptime')
        self.process = self.env.process(self.run())

    def do(self):
        pass

    def boot(self):
        pass

    def run(self):
        self.boot()
        while True:
            try:
                if (self.onrun == True):
                    yield self.env.process(self.do())
                else:
                    yield self.env.timeout(self.infinite)
            except Interrupt as i:
                self.onrun = not self.onrun


class SimpleBehaviour(Behaviour):
    def __init__(self, nname, dettime):
        super().__init__(nname)
        self.deltatime = dettime

    def do(self):
        yield self.env.timeout(self.deltatime)
        if (self.onrun == True):
            self.log('is working;;',1)


class Performing(Component):
    def __init__(self, nname, bbehaviours, mmtbf=0, mmttr=0):
        super().__init__(nname, mmtbf, mmttr)
        temp = bbehaviours
        if isinstance(temp,list) == False:
            temp = list()
            temp.append(bbehaviours)
        self.behaviours = temp

    def addBehaviour(self, behave):
        self.behaviours.append(behave)

    def faultPropagation(self):
        super().faultPropagation()
        for b in self.behaviours:
            b.process.interrupt()

    def repairPropagation(self):
        super().repairPropagation()
        for b in self.behaviours:
            b.process.interrupt()

#todo refactoring of the classes to exploit multiple inheritance
class TopPerforming(OrGate):
    def __init__(self, nname, bbehaviours, mmtbf=0, mmttr=0, listeners = list()):
        super().__init__(nname, mmtbf, mmttr)
        temp = bbehaviours
        self.lastuptime = 0
        if isinstance(temp,list) == False:
            temp = list()
            temp.append(bbehaviours)
        self.behaviours = temp
        self.listeners = listeners

    def addBehaviour(self, behave):
        self.behaviours.append(behave)

    def faultPropagation(self):
        self.warning('breaking;;')
        self.lastuptime = self.env.now
        self.notify()
        super().faultPropagation()
        for b in self.behaviours:
            b.process.interrupt()

    def repairPropagation(self):
        self.warning('repairing;;')
        self.notify()
        Recorder().add(self.getMeasureName(),self.env.now - self.lastuptime)
        super().repairPropagation()
        for b in self.behaviours:
            b.process.interrupt()

    def getMeasureName(self):
        retval = self.name + '_downtime'
        return retval

    def notify(self):
        for l in self.listeners:
            l.put(self.name)