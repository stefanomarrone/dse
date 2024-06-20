from core.gates import KooNGate
from core.performing import *

class Hardware():
    def __init__(self, systemname, components, mttr, listeners, programs = list()):
        self.components = dict()
        middles = list()
        conf = Configuration()
        # creating subgroups
        for c in components:

            tag, number, koon, mtbf, c_mttr = self.extractInformation(c,systemname)

            names = systemname + '_' + tag + 's'
            key = '[' + tag + ']'
            subs = list()
            self.components[names] = KooNGate(names,koon,mtbf,c_mttr)
            middles.append(self.components[names])
            substructure = conf.get(key + 'structure')
            for sub in substructure:
                name = sub[0]
                subs_mtbf=sub[1]
                self.components[name] = Component(name,subs_mtbf,c_mttr)
                self.components[name].setOwner(self.components[names])
                subs.append(self.components[name])
            self.components[names].setSubcomponents(subs)
        # creating top group
        self.topname = systemname + '_' + 'top'
        self.components[self.topname] = TopPerforming(self.topname,programs,0,mttr,listeners)
        self.components[self.topname].setSubcomponents(middles)
        for m in middles:
            m.setOwner(self.components[self.topname])

    def extractInformation(self, component,systemname):
        tag, number, koon, mtbf = component
        conf = Configuration()
        c='['+ systemname+ ']'

        mttr=conf.get(c + component[0]+'_mttr')
        return tag, number, koon, mtbf, mttr

    def addBehaviour(self, behaviour):
        self.components[self.topname].addBehaviour(behaviour)



class RHardware(Hardware):
    def __init__(self, systemname, components, mttr, listeners, programs = list()):
        super().__init__(systemname, components, mttr, listeners, programs)

    def extractInformation(self, component):
        tag, number, koon, mtbf, c_mttr = component
        return tag, number, koon, mtbf, c_mttr
