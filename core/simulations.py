from simpy import Environment
from core.measures import Recorder
from core.boards import Configuration, Blackboard
from core.maintenance import MaintainersFactroy
from core.progresses import Progressor


class AbstractArgumentFactory():
    def setup(self,iifiles,iindices):
        pass


class Simulation():
    def __init__(self, infiles, logs, iindices, factory):
        self.inifiles = infiles
        self.logTemplate = logs
        self.indices = iindices
        self.executor = None
        self.argumentFactory = factory

    def run(self):
        # loading configuration files
        self.argumentFactory.setup(self.inifiles,self.indices)
        # running executor
        self.executor = Configuration().get('executor')
        ret = self.executor.execute(self)
        # Post running
        report = ret.mean()
        report = ret.tocsv(report)
        self.writeIntoIndices(report)

    def writeIntoIndices(self, rep):
        fhandle = open(self.indices, 'w')
        fhandle.write(rep)
        fhandle.close()

    def main(self, stop):
        # environment setup
        enviro = Environment()
        print('Unforgiven II')
        Blackboard().put('enviro', enviro)
        # start recorder
        record = Recorder()
        record.reset()
        p = Progressor()
        # setup maintenance
        maintainers = MaintainersFactroy.generate(Configuration().get('[main]maintainers'))
        Blackboard().put('maintainers', maintainers)
        # setup of the simulation
        self.loadScenario(enviro)
        # start the simulation
        enviro.run(until=stop)
        retval = record.generateRecord()
        return retval
