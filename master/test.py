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
    topABCD = Gate('TopABCD', 0, 10)
    middleAB = Gate('MiddleAB', 0, 0)
    middleCD = Gate('MiddleCD', 0, 0)
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
    topABCD = OrGate('TopABCD',0,0)
    middleAB = AndGate('MiddleAB',0,10)
    middleCD = AndGate('MiddleCD',0,10)
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

def core_05():
    global_top = OrGate('Global',0 ,10 )

    piesse = AndGate('PS',0 ,0 )
    piesse.setOwner(global_top)

    piesse1 = Component('PS1',0 ,10 )
    piesse2 = Component('PS2',10 , 10)
    piesse3 = Component('PS3',0 , 0)
    piesse1.setOwner(piesse)
    piesse2.setOwner(piesse)
    piesse3.setOwner(piesse)
    
    bus = AndGate('BUS',10 ,10 )
    bus.setOwner(global_top)

    bus1 = Component('BUS1',0 ,0 )
    bus2 = Component('BUS2', 0,0 )
    bus1.setOwner(bus)
    bus2.setOwner(bus)

    tmr = OrGate('TMR', 0,0 )
    tmr.setOwner(global_top)

    voter = AndGate('Voter',10 ,0)
    voter.setOwner(tmr)

    voter1 = Component('Voter1',0 ,10 )
    voter2 = Component('Voter2', 10,10 )
    voter1.setOwner(voter)
    voter2.setOwner(voter)

    cpu = AndGate('CPU',0 , 0)
    cpu.setOwner(tmr)

    cpu1 = Component('CPU1', 0,0 )
    cpu2 = Component('CPU2',0 ,0 )
    cpu3 = Component('CPU3',0 ,0 )
    cpu1.setOwner(cpu)
    cpu2.setOwner(cpu)
    cpu3.setOwner(cpu)

    btm = AndGate('BTM',0 ,0 )
    btm.setOwner(global_top)

    btm1 = Component('BTM1', 0,10 )
    btm2 = Component('BTM2',10 ,0 )
    btm1.setOwner(btm)
    btm2.setOwner(btm)

    mmi = AndGate('MMI',10 ,0 )
    mmi.setOwner(global_top)

    mmi1 = Component('MMI1', 10,0 )
    mmi2 = Component('MMI2',10 ,0 )
    mmi1.setOwner(mmi)
    mmi2.setOwner(mmi)

    tiu = AndGate('TIU',0 ,0 )
    tiu.setOwner(global_top)

    tiu1 = Component('TIU1',10 ,0 )
    tiu2 = Component('TIU2',10 ,0 )
    tiu1.setOwner(tiu)
    tiu2.setOwner(tiu)

    odo = AndGate('ODO',10 ,10 )
    odo.setOwner(global_top)

    odo1 = Component('ODO1',0 ,0 )
    odo2 = Component('ODO2', 0, 0)
    odo1.setOwner(odo)
    odo2.setOwner(odo)

    rtm = AndGate('RTM', 0, 0)
    rtm.setOwner(global_top)

    rtm1 = Component('RTM1', 10,0 )
    rtm2 = Component('RTM2', 0, 0)
    rtm1.setOwner(rtm)
    rtm2.setOwner(rtm)

    global_top.setSubcomponents([piesse,bus,tmr,btm,mmi,tiu,odo,rtm])
    piesse.setSubcomponents([piesse1,piesse2,piesse3])
    bus.setSubcomponents([bus1,bus2])
    tmr.setSubcomponents([voter,cpu])
    voter.setSubcomponents([voter1,voter2])
    cpu.setSubcomponents([cpu1,cpu2,cpu3])
    btm.setSubcomponents([btm1,btm2])
    mmi.setSubcomponents([mmi1,mmi2])
    tiu.setSubcomponents([tiu1,tiu2])
    odo.setSubcomponents([odo1,odo2])
    rtm.setSubcomponents([rtm1,rtm2])

def core_06():
    global_top = OrGate('Global',0,30)

    piesse = AndGate('PS',0 ,0)
    piesse.setOwner(global_top)

    piesse1 = Component('PS1',3300000,10)
    piesse2 = Component('PS2',3300000,10)
    piesse3 = Component('PS3',3300000,10)
    piesse1.setOwner(piesse)
    piesse2.setOwner(piesse)
    piesse3.setOwner(piesse)
    
    bus = AndGate('BUS',0 ,0)
    bus.setOwner(global_top)

    bus1 = Component('BUS1',13500000,15)
    bus2 = Component('BUS2',13500000,15)
    bus1.setOwner(bus)
    bus2.setOwner(bus)

    tmr = OrGate('TMR',0,0)
    tmr.setOwner(global_top)

    voter = AndGate('Voter',10,0)
    voter.setOwner(tmr)

    voter1 = Component('Voter1',20000000000,15)
    voter2 = Component('Voter2',20000000000,15)
    voter1.setOwner(voter)
    voter2.setOwner(voter)

    cpu = AndGate('CPU',0 , 0)
    cpu.setOwner(tmr)

    cpu1 = Component('CPU1',8100000, 10)
    cpu2 = Component('CPU2',8100000 ,10)
    cpu3 = Component('CPU3',8100000 ,10)
    cpu1.setOwner(cpu)
    cpu2.setOwner(cpu)
    cpu3.setOwner(cpu)

    wan = AndGate('WAN',0 ,0 )
    wan.setOwner(global_top)

    wan1 = Component('WAN1',24000000,10 )
    wan2 = Component('WAN2',24000000,10 )
    wan1.setOwner(wan)
    wan2.setOwner(wan)

    gsm = AndGate('GSM-R',0 ,0 )
    gsm.setOwner(global_top)

    gsm1 = Component('GSM-R1',10500000,10 )
    gsm2 = Component('GSM-R2',10500000,10 )
    gsm1.setOwner(gsm)
    gsm2.setOwner(gsm)

    global_top.setSubcomponents([piesse,bus,tmr,wan,gsm])
    piesse.setSubcomponents([piesse1,piesse2,piesse3])
    bus.setSubcomponents([bus1,bus2])
    tmr.setSubcomponents([voter,cpu])
    voter.setSubcomponents([voter1,voter2])
    cpu.setSubcomponents([cpu1,cpu2,cpu3])
    wan.setSubcomponents([wan1,wan2])
    gsm.setSubcomponents([gsm1,gsm2])
    
def core_07():
    global_top = OrGate('Global',0,30)

    piesse = AndGate('PS',0 ,0)
    piesse.setOwner(global_top)

    piesse1 = Component('PS1',3300000,10)
    piesse2 = Component('PS2',3300000,10)
    piesse3 = Component('PS3',3300000,10)
    piesse1.setOwner(piesse)
    piesse2.setOwner(piesse)
    piesse3.setOwner(piesse)
    
    bus = AndGate('BUS',0 ,0)
    bus.setOwner(global_top)

    bus1 = Component('BUS1',13500000,15)
    bus2 = Component('BUS2',13500000,15)
    bus1.setOwner(bus)
    bus2.setOwner(bus)

    tmr = OrGate('TMR',0,0)
    tmr.setOwner(global_top)

    voter = AndGate('Voter',10,0)
    voter.setOwner(tmr)

    voter1 = Component('Voter1',20000000000,15)
    voter2 = Component('Voter2',20000000000,15)
    voter1.setOwner(voter)
    voter2.setOwner(voter)

    cpu = AndGate('CPU',0 , 0)
    cpu.setOwner(tmr)

    cpu1 = Component('CPU1',8100000, 10)
    cpu2 = Component('CPU2',8100000 ,10)
    cpu3 = Component('CPU3',8100000 ,10)
    cpu1.setOwner(cpu)
    cpu2.setOwner(cpu)
    cpu3.setOwner(cpu)

    wan = AndGate('WAN',0 ,0 )
    wan.setOwner(global_top)

    wan1 = Component('WAN1',24000000,10 )
    wan2 = Component('WAN2',24000000,10 )
    wan1.setOwner(wan)
    wan2.setOwner(wan)

    gsm = AndGate('GSM-R',0 ,0 )
    gsm.setOwner(global_top)

    gsm1 = Component('GSM-R1',10500000,10 )
    gsm2 = Component('GSM-R2',10500000,10 )
    gsm1.setOwner(gsm)
    gsm2.setOwner(gsm)

    global_top.setSubcomponents([piesse,bus,tmr,wan,gsm])
    piesse.setSubcomponents([piesse1,piesse2,piesse3])
    bus.setSubcomponents([bus1,bus2])
    tmr.setSubcomponents([voter,cpu])
    voter.setSubcomponents([voter1,voter2])
    cpu.setSubcomponents([cpu1,cpu2,cpu3])
    wan.setSubcomponents([wan1,wan2])
    gsm.setSubcomponents([gsm1,gsm2])
    

fdict = {
    'simple': core_01,
    'structured': core_02,
    'gate_fault': core_03,
    'performing': core_04,
    'on_board': core_05,
    'onb_repair': core_06,
    'onb_repairman': core_07
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
    repairman = simpy.Resource(env,1)
    #logging block
    sendqueue = makeLogging()
    board = Blackboard()
    board.put('enviro',env)
    board.put('repairer',repairman)
    board.put('logqueue',sendqueue)
    board.put('stoptime',stop)
    #board.put('debugLevel',1)
    board.put('debugLevel',0)
    
    #la funzione definisce l'ambiente
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
