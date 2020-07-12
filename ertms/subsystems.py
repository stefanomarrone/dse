from core.gates import KooNGate
from core.performing import *

class Hardware():
    def __init__(self, systemname, components, mttr, programs = list()):
        self.components = dict()
        middles = list()
        # creating subgroups
        for c in components:
            tag, number, koon, mtbf, c_mttr = self.extractInformation(c)
            names = systemname + '_' + tag + 's'
            subs = list()
            self.components[names] = KooNGate(names,koon)
            middles.append(self.components[names])
            for i in range(0,number):
                name = systemname + '_' + tag + str(i)
                self.components[name] = Component(name,mtbf,c_mttr)
                self.components[name].setOwner(self.components[names])
                subs.append(self.components[name])
            self.components[names].setSubcomponents(subs)
        # creating top group
        self.topname = systemname + '_' + 'top'
        self.components[self.topname] = TopPerforming(self.topname,programs,0,mttr)
        self.components[self.topname].setSubcomponents(middles)
        for m in middles:
            m.setOwner(self.components[self.topname])

    def extractInformation(self, component):
        tag, number, koon, mtbf = component
        return tag, number, koon, mtbf, 0

    def addBehaviour(self, behaviour):
        self.components[self.topname].addBehaviour(behaviour)



class RHardware(Hardware):
    def __init__(self, systemname, components, mttr, programs = list()):
        super().__init__(systemname, components, mttr, programs)

    def extractInformation(self, component):
        tag, number, koon, mtbf, c_mttr = component
        return tag, number, koon, mtbf, c_mttr
