from core.boards import Configuration
from ertms.subsystems import Hardware
from core.performing import Behaviour

def mergeMTTRS(components):
    #fixme complete
    pass

class RBCLogic(Behaviour):
    def __init__(self,nname,nnretry,ttrestore,ttretry,nnvcontact):
        super().__init__(nname)
        self.channel = None
        self.nvcontact = nnvcontact
        self.nretry = nnretry
        self.trestore = ttrestore
        self.tretry = ttretry

    def setChannel(self,ch):
        self.channel = ch

    def do(self):
        yield self.env.timeout(10)

class RBC():
    def __init__(self, nname):
        conf = Configuration()
        comp = conf.get('[evc]structure')
        mttr = conf.get('[rbc]top_mttr')
        mergeMTTRS(comp)
        nretry = conf.get('[comm]num_retry')
        trestore = conf.get('[comm]t_restore')
        tretry = conf.get('[comm]t_retry')
        nvcontact = conf.get('[comm]tnv')
        self.logic = RBCLogic(nname + '_logic',nretry,trestore,tretry,nvcontact)
        self.structure = Hardware(nname, comp, mttr, self.logic)

    def setChannel(self, channel):
        self.logic.setChannel(channel)