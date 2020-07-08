from core.components import Component
from core.gates import Gate, OrGate
from core.boards import Configuration
from simpy import Interrupt
from core.log import Loggable


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
    def __init__(self, nname, bbehaviours, mmtbf=0, mmttr=0):
        super().__init__(nname, mmtbf, mmttr)
        temp = bbehaviours
        if isinstance(temp,list) == False:
            temp = list()
            temp.append(bbehaviours)
        self.behaviours = temp

    def faultPropagation(self):
        super().faultPropagation()
        for b in self.behaviours:
            b.process.interrupt()

    def repairPropagation(self):
        super().repairPropagation()
        for b in self.behaviours:
            b.process.interrupt()
