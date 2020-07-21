from core.boards import Configuration
from core.measures import Analyser
from core.utils import mean
from multiprocessing import Pool
import logging


class Executor():
    def execute(self,simulator):
        return None

    def mark(self,tag,counter):
        toprint = tag + ';' + str(counter) + ';'
        logging.critical(toprint)
        print(toprint)



class SerialExecutor(Executor):
    def computeStopCondition(self,iteration,values):
        iters = Configuration().get('experiments')
        stopcondition = (iteration == iters)
        return stopcondition

    def execute(self,simulator):
        retval = Analyser()
        c = Configuration()
        stop = c.get('stoptime')
        stopcondition = False
        counter = 0
        while (not stopcondition):
            #self.mark('ITERATION',counter)
            logname = c.get('logtemplate') + '.' + str(counter)
            record = simulator.main(logname,stop)
            retval.add(record)
            stopcondition = self.computeStopCondition(counter,retval)
            counter += 1
        return retval



class ConvergenceExecutor(SerialExecutor):
    def computeStopCondition(self,iteration,values):
        eps = Configuration().get('epsilon')
        stopcondition = super().computeStopCondition(iteration,values)
        dim = values.size()
        if not stopcondition and dim > 5:
            temp = values.confidence95()
            diffs = list(map(lambda x: x[1][1] - x[1][0], temp.items()))
            mids = list(map(lambda x: (x[1][0] + x[1][1]) / 2, temp.items()))
            deltas = [diffs[i] / mids[i] for i in range(0, len(diffs))]
            delta = mean(deltas)
            stopcondition = (delta < eps)
        return stopcondition


class ParallelExecutor(Executor):
    def core(self,payload):
        simulator, oldconf, counter = payload
        conf = Configuration()
        conf.mergeBoard(oldconf)
        stop = conf.get('stoptime')
        logname = conf.get('logtemplate') + '.' + str(counter)
        record = simulator.main(logname,stop)
        return record

    def execute(self,simulator):
        retval = Analyser()
        conf = Configuration()
        slaves = conf.get('slaves')
        iters = conf.get('experiments')
        counters = range(0,iters)
        counters = list(map(lambda cnt: (simulator,conf,cnt),counters))
        p = Pool(slaves)
        temps = p.map(self.core, counters)
        p.close()
        for t in temps:
            retval.add(t)
        return retval


class ExecutorFactory():
    mapping = {
        'serial': SerialExecutor,
        'convergence': ConvergenceExecutor,
        'parallel': ParallelExecutor
    }

    @staticmethod
    def generate(executorKind):
        f = ExecutorFactory.mapping[executorKind]
        retval = f()
        return retval