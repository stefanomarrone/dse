from simpy import Environment
from core.measures import Recorder, Analyser
from core.boards import Configuration, Blackboard
from core.log import LoggerFactory
from core.maintenance import MaintainersFactroy
from core.progresses import Progressor
from utils import mean
import logging


class AbstractArgumentFactory():
    def setup(self,iifiles,iindices):
        pass


class Simulation():
    def __init__(self, infiles, logs, iindices, factory):
        self.inifiles = infiles
        self.logTemplate = logs
        self.indices = iindices
        self.argumentFactory = factory

    def run(self):
        # loading configuration files
        self.argumentFactory.setup(self.inifiles,self.indices)
        # setting up logging parameters
        st, ex, eps = self.getRunParameters()
        ret = self.experiment(st, ex, eps)
        report = ret.mean()
        report = ret.tocsv(report)
        self.writeIntoIndices(report)

    def writeIntoIndices(self, rep):
        fhandle = open(self.indices, 'w')
        fhandle.write(rep)
        fhandle.close()

    def experiment(self, stop, iters, eps):
        LoggerFactory.setup(self.logTemplate)
        retval = Analyser()
        stopcondition = False
        counter = 0
        while (not stopcondition):
            logging.critical("ITERATION;" + str(counter) + ';')
            print("ITERATION " + str(counter))
            record = self.main(stop)
            retval.add(record)
            dim = retval.size()
            stopcondition = (counter == iters)
            if not stopcondition and dim > 5:
                temp = retval.confidence95()
                diffs = list(map(lambda x: x[1][1] - x[1][0], temp.items()))
                mids = list(map(lambda x: (x[1][0] + x[1][1]) / 2, temp.items()))
                deltas = [diffs[i] / mids[i] for i in range(0, len(diffs))]
                delta = mean(deltas)
                stopcondition = (delta < eps)
            counter += 1
        LoggerFactory.shutdown()
        return retval

    def main(self, stop):
        # environment setup
        enviro = Environment()
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

    def getRunParameters(self):
        c = Configuration()
        st = c.get('stoptime')
        ex = c.get('experiments')
        eps = c.get('epsilon')
        return st, ex, eps