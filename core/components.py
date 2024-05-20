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
        self.state = 'is up'
        self.process = self.env.process(self.run())
        self.faultStartTime = self.env.now
        self.repairStartTime = self.env.now
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
        #self.downFaultPropagation()

    def fail(self):
        yield self.env.process(self.waitForFault(self.mtbf))

    def repair(self,repairman):
        if (self.mttr > 0):
            self.request = repairman.request()
            #self.request = repairer.request(priority=self.priority)
            #self.maintenance_action('repairman calling;;')
            #self.maintenance_action('busy repairman;' + str(repairman.count) + ';')
            yield self.request
            self.maintenance_action('repairman called;;')
            #self.maintenance_action('busy repairman;' + str(repairman.count) + ';')
            if (self.working == False):
                yield self.env.process(self.waitForRepair(self.mttr))
                #cancella questi due
                self.working=True
                self.maintenance_action('repaired;;')
            #self.maintenance_action('repairman releasing;;')
            repairman.release(self.request)
            #self.maintenance_action('busy repairman;' + str(repairman.count) + ';')

        else:
            yield self.env.process(self.waitForRepair(self.mttr))



    def boot(self):
        pass

    def run(self):
        self.boot()
        while True:
            while (self.working == True):
                try:
                    self.info(self.state+';;')
                    yield self.env.process(self.fail())
                    self.error('has failed by itself;;')
                    self.state='is down'
                    self.info(self.state+';;')
                    self.working = False
                    self.faultPropagation()
                except Interrupt as i:
                    kind, source = utils.unpack_interrupt(i.cause)
                    self.debug('is receiving an interrupt;' + str(i.cause) + ';')
                    self.working = not (kind == 'F')
                    if(kind=='R'):
                        self.state = 'is up'
                    else:
                        if(self.working):
                            self.state='is failing'
                            self.info(self.state + ';;')
                        else:
                            self.state = 'is down'
                            self.info(self.state + ';;')
                            self.faultPropagation()



            while (self.working == False):
                try:
                    yield self.env.process(self.repair(self.repairman))
                except Interrupt as i:
                    (kind, source) = utils.unpack_interrupt(i.cause)
                    self.maintenance_action('repaired by extern;' + str((kind, source)))
                    '''
                    if(str(i.cause).startswith('sig')):
                        self.maintenance_action('repaired after signals;' + str((kind, source)))
                        #self.env.process(self.repair(self.repairman))
                        #self.working = True
                    else:
                        self.maintenance_action('repaired by extern;' + str((kind, source)))
                        #cancella rigo qui
                    '''


                finally:
                    self.working=True
                    self.state = 'is up'
                    self.repairPropagation()




    def upFaultPropagation(self):

        if (self.owner != None):
            if (self.owner.working == True):
                self.debug('is breaking;' + self.owner.getName() + ';')
                self.owner.process.interrupt(self.getName() + '(F)')


    def downFaultPropagation(self):
        pass


#cancella
    def repairPropagation(self):
        if (self.owner != None):
            if (self.owner.working == False and self.owner.canWork() == True):
                self.debug('Its recovery makes the owner up;' + self.owner.getName() + ';')
                self.owner.process.interrupt(self.getName() + '(R)')