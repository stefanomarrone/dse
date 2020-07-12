from core.performing import *
from ertms.subsystems import Hardware
from core.measures import Recorder

class EVCLogic(Behaviour):
    def __init__(self, nname, nnretry, ttretry, nnvcontact, cchannel):
        super().__init__(nname)
        self.channel = cchannel
        self.nvcontact = nnvcontact
        self.nretry = nnretry
        self.tretry = ttretry

    def do(self):
        if self.onrun == True:
            time = self.env.now
            msg = yield self.env.process(self.channel.get())
            time = self.env.now - time
            if self.check(time) == True:
                self.down(time)

    def check(self, time):
        totaldowntime = self.nretry * self.tretry + self.nvcontact
        return time > totaldowntime

    def down(self, time):
        self.warning('commdown;' + str(time) + ';')
        Recorder().add(self.name,time)


class EVC():
    def __init__(self, nname, cchannel):
        conf = Configuration()
        mttr = conf.get('[evc]mttr')
        comp = conf.get('[evc]structure')
        nretry = conf.get('[comm]num_retry')
        tretry = conf.get('[comm]t_retry')
        nvcontact = conf.get('[comm]tnv')
        self.logic = EVCLogic(nname + '_logic', nretry, tretry, nvcontact, cchannel)
        self.structure = Hardware(nname, comp, mttr, self.logic)