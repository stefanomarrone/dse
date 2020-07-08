from core.gates import KooNGate
from core.performing import *

class Hardware():
    def __init__(self, systemname, components, mttr, programs):
        self.components = dict()
        middles = list()
        # creating subgroups
        for c in components:
            tag, number, koon, mtbf = c
            names = systemname + '_' + tag + 's'
            subs = list()
            self.components[names] = KooNGate(names,koon)
            middles.append(self.components[names])
            for i in range(0,number):
                name = systemname + '_' + tag + str(i)
                self.components[name] = Component(name,mtbf,0)
                self.components[names].setOwner(self.components[name])
                subs.append(self.components[name])
            self.components[names].setSubcomponents(subs)
        # creating top group
        self.components['top'] = TopPerforming(systemname + '_' + 'top',programs,0,mttr)
        self.components['top'].setSubcomponents(middles)
        for m in middles:
            m.setOwner(self.components['top'])