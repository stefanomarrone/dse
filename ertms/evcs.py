from core.performing import *
from ertms.subsystems import Hardware

class EVCLogic(Behaviour):
    def __init__(self, nname, pprtime, cchannel):
        super().__init__(nname)
        self.channel = cchannel
        self.prtime = pprtime

    def do(self):
        yield self.env.timeout(self.prtime)
        self.channel.put('ping')

class EVC():
    def __init__(self, nname, cchannel):
        conf = Configuration()
        mttr = conf.get('[evc]mttr')
        comp = conf.get('[evc]structure')
        prtime = conf.get('[comm]pr_time')
        self.logic = EVCLogic(nname + '_logic', prtime, cchannel)
        self.structure = Hardware(nname, comp, mttr, self.logic)