from cProfile import Profile
import sys
from simpy import Environment
from core.measures import Recorder, Analyser
from core.boards import Configuration, Blackboard
from core.log import LoggerFactory
from ertms.configurations import ConfigurationFactory
from ertms.communications import Comm
from ertms.evcs import EVC
from ertms.rbcs import RBC
from core.maintenance import MaintainersFactroy
from math import isnan
from utils import mean

def configurationSetup(cfile, mfile, ifile):
    conf = ConfigurationFactory()
    subs = conf.loadConfiguration(cfile)
    conf.loadMaintenance(mfile, subs)
    conf = Configuration()
    conf.put('indices', ifile)


def loadScenario(enviro):
    numberOfEvcs = Configuration().get('[ertms]evcs')
    numberOfRbcs = Configuration().get('[ertms]rbcs')
    rbcs = list()
    comms = list()
    evcs = list()
    for i in range(0, numberOfRbcs):
        rname = 'RBC_' + str(i)
        rbc = RBC(rname)
        rbcs.append(rbc)
    rbcCounter = 0
    for i in range(0, numberOfEvcs):
        cname = 'COMM_' + str(i)
        comm = Comm(cname, enviro)
        comms.append(comm)
        ename = 'EVC_' + str(i)
        evc = EVC(ename, comm)
        evcs.append(evc)
        logicname = 'LOGIC_' + str(rbcCounter) + '_to_' + str(i)
        rbcs[rbcCounter].addBehaviour(logicname,comm)
        rbcCounter = (rbcCounter + 1) % numberOfRbcs


def main(stop, log):
    # logger setup
    ecounter = Blackboard().get('experimentcounter')
    LoggerFactory.setup(log + '.' + str(ecounter))
    Blackboard().put('experimentcounter', ecounter + 1)
    # environment setup
    enviro = Environment()
    Blackboard().put('enviro', enviro)
    # start recorder
    record = Recorder()
    record.reset()
    # setup maintenance
    maintainers = MaintainersFactroy.generate(Configuration().get('[main]maintainers'))
    Blackboard().put('maintainers', maintainers)
    # setup of the simulation
    loadScenario(enviro)
    # start the simulation
    enviro.run(until=stop)
    # closing and post processing
    LoggerFactory.shutdown()
    retval = record.generateRecord()
    return retval


def experiment(stop, iters, eps, log):
    pr = Profile()
    retval = Analyser()
    stopcondition = False
    counter = 0
    while (not stopcondition):
        #pr.enable()
        record = main(stop, log)
        #pr.disable()
        retval.add(record)
        temp = retval.confidence95()
        temp = list(filter(lambda x: not (isnan(x[1][0]) or isnan(x[1][1])), temp.items()))
        if len(temp)>0:
            diffs = list(map(lambda x: x[1][1] - x[1][0],temp))
            mids = list(map(lambda x: (x[1][0] + x[1][1])/2,temp))
            deltas = [diffs[i]/mids[i] for i in range(0,len(diffs))]
            delta = mean(deltas)
            counter += 1
            stopcondition = (counter == iters) or (delta < eps)
            #print(str(counter) + ' ' + str(delta))
    # after your program ends
    #pr.print_stats()
    return retval


def getRunParameters():
    c = Configuration()
    st = c.get('stoptime')
    ex = c.get('experiments')
    eps = c.get('epsilon')
    return st, ex, eps


def root(config, maint, log, indices):
    # loading configuration files
    configurationSetup(config, maint, indices)
    Blackboard().put('experimentcounter', 0)
    # setting up logging parameters
    st, ex, eps = getRunParameters()
    ret = experiment(st, ex, eps, log)
    report = ret.mean()
    report = ret.tocsv(report)
    fhandle = open(indices, 'w')
    fhandle.write(report)
    fhandle.close()


if __name__ == "__main__":
    if len(sys.argv) > 4:
        config = sys.argv[1]
        maint = sys.argv[2]
        log = sys.argv[3]
        indices = sys.argv[4]
        root(config, maint, log, indices)
        LoggerFactory.shutdown()
    else:
        usage = sys.argv[0] + ' configuration maintenance logs indices'
        print(usage)
