#!/home/stefano/Scrivania/simpy/dse/enviro/bin/python
import simpy
import sys
import os
import multiprocessing
from blackboard import Blackboard
from log import Logger
from components import *
from gates import *
from performing import *


#Test functions
def core_01(sendqueue,env):
    Component('GA', sendqueue, env, 1000, 10)
    Component('GB', sendqueue, env, 1000)

def core_02(sendqueue,env):
    topABCD = Component('TopABCD',sendqueue, env, 0, 10)
    middleAB = Component('MiddleAB',sendqueue, env, 0, 0)
    middleCD = Component('MiddleCD',sendqueue, env, 0, 0)
    leafA = Component('LeafA', sendqueue, env, 1000, 0)
    leafB = Component('LeafB', sendqueue, env, 10, 0)
    leafC = Component('LeafC', sendqueue, env, 10, 0)
    leafD = Component('LeafD', sendqueue, env, 100, 0)
    leafA.setOwner(middleAB)
    leafB.setOwner(middleAB)
    leafC.setOwner(middleCD)
    leafD.setOwner(middleCD)
    middleCD.setOwner(topABCD)
    middleAB.setOwner(topABCD)
    topABCD.setSubcomponents([middleCD, middleAB])
    middleCD.setSubcomponents([leafC, leafD])
    middleAB.setSubcomponents([leafA, leafB])

def core_03(sendqueue,env):
    topABCD = Gate('TopABCD',sendqueue,env,0,10,1)
    middleAB = Gate('MiddleAB',sendqueue,env,0,0,2)
    middleCD = Gate('MiddleCD',sendqueue,env,0,0,2)
    leafA = Component('LeafA',sendqueue,env,1000,0)
    leafB = Component('LeafB',sendqueue,env,10,0)
    leafC = Component('LeafC',sendqueue,env,10,0)
    leafD = Component('LeafD',sendqueue,env,100,0)
    leafA.setOwner(middleAB)
    leafB.setOwner(middleAB)
    leafC.setOwner(middleCD)
    leafD.setOwner(middleCD)
    middleCD.setOwner(topABCD)
    middleAB.setOwner(topABCD)
    topABCD.setSubcomponents([middleCD, middleAB])
    middleCD.setSubcomponents([leafC, leafD])
    middleAB.setSubcomponents([leafA, leafB])

def core_04(sendqueue,env):
    behav = SimpleBehaviour('workerbehaviour', sendqueue, env, 3)
    worker = Performing('worker',sendqueue,env,behav,10,10)

fdict = {
    'simple': core_01,
    'structured': core_02,
    'gate_fault': core_03,
    'performing': core_04
}


#main block

def makeLogger(q):
    logger = Logger(q)
    logger.run()


def makeLogging():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=makeLogger, args=(queue,))
    p.start()
    return queue


def main(stop,fcode):
    env = simpy.Environment()
    sendqueue = makeLogging()
    board = Blackboard()
    board.put('stoptime',stop)
    board.put('debugLevel',False)
    fdict[fcode](sendqueue,env)
    env.run(until=stop)
    sendqueue.put('HALT')


if __name__ == "__main__":
    if len(sys.argv) > 2:
        fcode = sys.argv[1]
        stopTime = int(sys.argv[2])
        original = sys.stdout
        if len(sys.argv) > 3:
            fname = sys.argv[3]
            if os.path.exists(fname):
                os.remove(fname)
            sys.stdout = open(fname, "w")
        main(stopTime,fcode)
        sys.stdout = original
        print('Simulation completed')
    else:
        usage = sys.argv[0] + ' testcode stoptime logfilename'
        print(usage)