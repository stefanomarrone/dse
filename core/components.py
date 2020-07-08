import core.utils as utils
from simpy import Interrupt
from core.boards import Configuration, Blackboard
from core.log import Loggable


class Component(Loggable):
    def __init__(self, nname, mmtbf=0, mmttr=0):
        super().__init__(nname)
        self.owner = None
        self.mtbf = mmtbf
        self.mttr = mmttr
        conf = Configuration()
        self.finalTime = conf.get('stoptime')
        self.working = True
        self.process = self.env.process(self.run())
        self.faultStartTime = self.env.now
        self.repairStartTime = self.env.now
        conf = Configuration()
        self.repairman = Blackboard().get('maintainers')
        #self.priority = ppriority

    def setOwner(self, oowner):
        self.owner = oowner

    def setRepairman(self, rrepairman):
        self.repairman = rrepairman

    def waitForRepair(self, beta):
        temp = self.finalTime if (beta == 0) else utils.expGuess(beta)
        self.repairStartTime = self.env.now
        yield self.env.timeout(temp)

    def waitForFault(self, beta):
        temp = self.finalTime if (beta == 0) else utils.expGuess(beta)
        self.guess = temp - self.repairStartTime + self.faultStartTime
        self.faultStartTime = self.env.now
        if (self.guess < 1):
            self.lastGuess = temp
            yield self.env.timeout(temp)
        else:
            self.lastGuess = self.guess
            yield self.env.timeout(self.guess)

    def faultPropagation(self):
        self.upFaultPropagation()
        self.downFaultPropagation()

    def fail(self):
        yield self.env.process(self.waitForFault(self.mtbf))

    def repair(self,repairman):
        if (self.mttr > 0):
            self.request = repairman.request()
            #self.request = repairer.request(priority=self.priority)
            self.info('calling the repairman;;')
            yield self.request
            if (self.working == False):
                yield self.env.process(self.waitForRepair(self.mttr))
            repairman.release(self.request)
        else:
            yield self.env.process(self.waitForRepair(self.mttr))


    def boot(self):
        pass

    def run(self):
        self.boot()
        while True:
            while (self.working == True):
                try:
                    self.info('is working;;')
                    yield self.env.process(self.fail())
                    self.info('has failed by itself;;')
                    self.working = False
                    self.faultPropagation()
                except Interrupt as i:
                    kind, source = utils.unpack_interrupt(i.cause)
                    self.working = not (kind == 'F')
            while (self.working == False):
                try:
                    self.info('is down;;')
                    yield self.env.process(self.repair(self.repairman))
                except Interrupt as i:
                    (kind, source) = utils.unpack_interrupt(i.cause)
                    self.info('repaired by extern;' + str((kind, source)))
                finally:
                    self.working = True

    def upFaultPropagation(self):
        if (self.owner != None):
            if (self.owner.working == True):
                self.info('is breaking;' + self.owner.getName() + ';')
                self.owner.process.interrupt(self.getName() + '(F)')

    def downFaultPropagation(self):
        pass
