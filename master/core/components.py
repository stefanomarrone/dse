import core.utils as utils
import simpy
from core.blackboard import Blackboard
from core.log import Loggable


class Component(Loggable):

    def __init__(self, nname, mmtbf=0, mmttr=0):
        super().__init__(nname)
        self.owner = None
        self.mtbf = mmtbf
        self.mttr = mmttr
        board = Blackboard()
        self.finalTime = board.get('stoptime')
        self.debugLevel = board.get('debugLevel')
        self.working = True
        self.process = self.env.process(self.run())

    def setOwner(self, oowner):
        self.owner = oowner

    def waitForEvent(self, beta):
        guess = self.finalTime if (beta == 0) else utils.expGuess(beta)
        yield self.env.timeout(guess)

    def faultPropagation(self):
        self.upFaultPropagation()
        self.downFaultPropagation()

    def fail(self):
        yield self.env.process(self.waitForEvent(self.mtbf))

    def repair(self):
        yield self.env.process(self.waitForEvent(self.mttr))

    def boot(self):
        pass

    def run(self):
        self.boot()
        while True:
            while (self.working == True):
                try:
                    self.log('is working;;',2)
                    yield self.env.process(self.fail())
                    self.log('has failed by itself;;',0)
                    self.working = False
                    self.faultPropagation()
                except simpy.Interrupt as i:
                    kind, source = utils.unpack_interrupt(i.cause)
                    self.working = not (kind == 'F')
            while (self.working == False):
                try:
                    self.log('is down;;',2)
                    yield self.env.process(self.repair())
                except simpy.Interrupt as i:
                    (kind, source) = utils.unpack_interrupt(i.cause)
                    self.log('repaired by extern;' + str((kind, source)),0)
                finally:
                    self.working = True

    def upFaultPropagation(self):
        if (self.owner != None):
            if (self.owner.working == True):
                self.log('is breaking;' + self.owner.getName() + ';',0)
                self.owner.process.interrupt(self.getName() + '(F)')

    def downFaultPropagation(self):
        pass
