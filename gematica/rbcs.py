from core.boards import Configuration
from core.subsystems import RHardware
from core.performing import Behaviour


def mergeMTTRS(components):
    retval = list()
    conf = Configuration()
    for comp in components:
        name = str(comp[0]).lower()
        mttr = conf.get('[rbc]' + name + '_mttr')
        new = (*comp,mttr)
        retval.append(new)
    return retval



class RBCLogic(Behaviour):
    def __init__(self,nname,ch):
        super().__init__(nname)
        self.channel = ch
        self.matime = Configuration().get('[comm]ma_time')

    def setChannel(self, ch):
        self.channel = ch

    def do(self):
        yield self.env.timeout(self.matime)
        yield self.env.process(self.channel.put('ping'))



class RBC():
    def __init__(self, nname, toetcs):
        conf = Configuration()
        comp = conf.get('[rbc]structure')
        mttr = conf.get('[rbc]top_mttr')
        comp = mergeMTTRS(comp)
        self.structure = RHardware(nname, comp, mttr, [toetcs])

    def addBehaviour(self, logicname, channel):
        logic = RBCLogic(logicname,channel)
        self.structure.addBehaviour(logic)
