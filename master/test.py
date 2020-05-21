import simpy
import sys
import os
import multiprocessing
from core.blackboard import Blackboard
from core.log import Logger
from core.components import *
from core.gates import *
from core.performing import *


#Test functions
def core_01():
    Component('GA', 1000, 10)
    Component('GB', 1000)

def core_02():
    topABCD = Component('TopABCD', 0, 10)
    middleAB = Component('MiddleAB', 0, 0)
    middleCD = Component('MiddleCD', 0, 0)
    leafA = Component('LeafA', 1000, 0)
    leafB = Component('LeafB', 10, 0)
    leafC = Component('LeafC', 10, 0)
    leafD = Component('LeafD', 100, 0)
    leafA.setOwner(middleAB)
    leafB.setOwner(middleAB)
    leafC.setOwner(middleCD)
    leafD.setOwner(middleCD)
    middleCD.setOwner(topABCD)
    middleAB.setOwner(topABCD)
    topABCD.setSubcomponents([middleCD, middleAB])
    middleCD.setSubcomponents([leafC, leafD])
    middleAB.setSubcomponents([leafA, leafB])

def core_03():
    topABCD = OrGate('TopABCD',0,10)
    middleAB = AndGate('MiddleAB',0,0)
    middleCD = AndGate('MiddleCD',0,0)
    leafA = Component('LeafA',1000,0)
    leafB = Component('LeafB',10,0)
    leafC = Component('LeafC',10,0)
    leafD = Component('LeafD',100,0)
    leafA.setOwner(middleAB)
    leafB.setOwner(middleAB)
    leafC.setOwner(middleCD)
    leafD.setOwner(middleCD)
    middleCD.setOwner(topABCD)
    middleAB.setOwner(topABCD)
    topABCD.setSubcomponents([middleCD, middleAB])
    middleCD.setSubcomponents([leafC, leafD])
    middleAB.setSubcomponents([leafA, leafB])

def core_04():
    behav = SimpleBehaviour('workerbehaviour', 3)
    worker = Performing('worker',behav,10,10)

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
    board.put('enviro',env)
    board.put('logqueue',sendqueue)
    board.put('stoptime',stop)
    board.put('debugLevel',1)
    fdict[fcode]()
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
