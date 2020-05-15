from components import Component
from blackboard import Blackboard
from simpy import Interrupt
from log import Loggable


class Behaviour(Loggable):
    def __init__(self, nname, qqname, eenv, dettime):
        super().__init__(nname, qqname, eenv)
        self.deltatime = dettime
        self.onrun = True
        self.infinite = Blackboard().get('stoptime')
        self.process = self.env.process(self.run())

    def do(self):
        yield self.env.timeout(self.deltatime)
        if (self.onrun == True):
            self.log('is working;;',2)

    def run(self):
        while True:
            try:
                if (self.onrun == True):
                    yield self.env.process(self.do())
                else:
                    yield self.env.timeout(self.infinite)
            except Interrupt as i:
                self.onrun = not self.onrun


class Performing(Component):

    def __init__(self, nname, qqueue, eenv, bbehaviour, mmtbf=0, mmttr=0):
        super().__init__(nname, qqueue, eenv, mmtbf, mmttr)
        self.behaviour = bbehaviour

    def faultPropagation(self):
        super().faultPropagation()
        self.behaviour.process.interrupt()

    def repairPropagation(self):
        super().repairPropagation()
        self.behaviour.process.interrupt()