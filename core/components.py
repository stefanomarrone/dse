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
        self.faultCounter=0
        self.process = self.env.process(self.run())
        self.faultStartTime = self.env.now
        self.repairStartTime = self.env.now
        self.caseid=0
        self.oldcaseid=0
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
            #self.maintenance_action(str(self.caseid)+';'+'repairman called;;')
            #self.maintenance_action('busy repairman;' + str(repairman.count) + ';')
            if (self.working == False):
                yield self.env.process(self.waitForRepair(self.mttr))
                #cancella questi due
                self.working=True
                #self.maintenance_action(str(self.caseid)+';'+'is repaired;;')
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

                    #self.info(str(self.caseid)+';'+self.state+';;')
                    yield self.env.process(self.fail())
                    self.info(str(self.caseid)+';'+'failed by itself;;')
                    yield self.env.timeout(1)
                    self.state='is down'
                    if(self.owner and self.owner.state!='is failing'):
                        self.faultCounter+=1
                        self.caseid = self.caseid + 1
                        self.caseidPropagation()
                    yield self.env.timeout(1)
                    self.info(str(self.caseid-1)+';'+self.state+';;')
                    self.working = False
                    self.faultPropagation()
                except Interrupt as i:
                    kind, source = utils.unpack_interrupt(i.cause)
                    #self.debug(str(self.caseid)+';'+'is receiving an interrupt;' + str(i.cause))
                    self.working = not (kind == 'F')
                    #yield self.env.timeout(1)


                    if(kind=='R'):
                        self.state='is repaired'
                        self.info(str(self.caseid-1) + ';' + self.state + ';;')
                        self.state = 'is up'
                        self.info(str(self.caseid-1) + ';' + self.state + ';;')
                    else:

                        if(self.working):
                            #yield self.env.timeout(1)
                            self.state='is failing'
                            self.info(str(self.caseid-1)+';'+self.state + ';;')
                        else:

                            #yield self.env.timeout(1)
                            self.state = 'is down'
                            self.faultStartTime=self.env.now
                            self.faultCounter+=1
                            yield self.env.timeout(1)
                            self.info(str(self.caseid-1)+';'+self.state + ';;')
                            yield self.env.timeout(1)
                            self.faultPropagation()




            while (self.working == False):
                try:
                    yield self.env.process(self.repair(self.repairman))
                    self.state = 'is up'
                    self.info(str(self.caseid-1) + ';' + self.state + ';;')
                    self.working = True
                    yield self.env.timeout(1)
                    self.repairPropagation()
                except Interrupt as i:
                    (kind, source) = utils.unpack_interrupt(i.cause)
                    self.state = 'is up'
                    self.info(str(self.caseid-1) + ';' + self.state + ';;')
                    self.working = True
                    yield self.env.timeout(1)
                    self.repairPropagation()

                    #self.maintenance_action(str(self.caseid)+';'+'repaired by extern;' + str((kind, source)))
                    '''
                    if(str(i.cause).startswith('sig')):
                        self.maintenance_action('repaired after signals;' + str((kind, source)))
                        #self.env.process(self.repair(self.repairman))
                        #self.working = True
                    else:
                        self.maintenance_action('repaired by extern;' + str((kind, source)))
                        #cancella rigo qui
                    '''








    def upFaultPropagation(self):

        if (self.owner != None):
            if (self.owner.working == True):
                #self.debug(str(self.caseid)+';'+'is breaking;' + self.owner.getName() )
                #yield self.env.timeout(1)
                self.owner.process.interrupt(str(self.caseid)+';'+self.getName() + '(F)')


    def downFaultPropagation(self):
        pass


#cancella
    def repairPropagation(self):
        if (self.owner != None):
            if (self.owner.working == False and self.owner.canWork() == True):
                #self.debug(str(self.caseid)+';'+'Its recovery makes the owner up;' + self.owner.getName() )
                #yield self.env.timeout(1)
                self.owner.process.interrupt(str(self.caseid)+';'+self.getName() + '(R)')
            if(self.owner.state=='is failing'):
                self.owner.state='is up'
                self.owner.info(str(self.owner.caseid-1) + ';' + self.state + ';;')

    def upCaseidPropagation(self):
        if (self.owner and self.owner.caseid<self.caseid):
            self.owner.caseid = self.caseid
            self.owner.caseidPropagation()

    def downCaseidPropagation(self):
        pass

    def caseidPropagation(self):
        self.upCaseidPropagation()
        self.downCaseidPropagation()
