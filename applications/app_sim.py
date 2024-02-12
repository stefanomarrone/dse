from core.simulations import Simulation, AbstractArgumentFactory
from applications.configurations import ConfigurationFactory
from core.boards import Configuration
from simpy import Store
from core.signals import Signal
from core.subsystems import Hardware

class AppConfigurationFactory(AbstractArgumentFactory):

    def setup(self,iifiles,iindices):
        cfile = iifiles[0]
        mfile = iifiles[1]
        conf = ConfigurationFactory()
        subs = conf.loadConfiguration(cfile)
        conf.loadMaintenance(mfile, subs)
        conf = Configuration()
        conf.put('indices', iindices)




class AppSimulation(Simulation):
    def __init__(self, infiles, logs, iindices, factory):
        super().__init__(infiles, logs, iindices, factory)

    def loadScenario(self,enviro):
        applicationstorage = Store(enviro)
        signals = list()
        conf = Configuration()
        submodels = dict()
        for subname in conf.get('submodels'):
            key = '[' + subname + ']'
            substructure = conf.get(key + 'structure')
            mttr = conf.get(key + 'top_mttr')
            submodel = Hardware(subname, substructure, mttr, [applicationstorage])
            submodels[subname] = submodel
        for signame in conf.get('signals'):
            key = '[' + signame + ']'
            sigfunction = conf.get(key + 'function')
            sigcondition = conf.get(key + 'conditions')
            conditionDB = self.fiteringListners(sigcondition, submodels)
            #todo: testare se il meccanismo di filtering è ok
            signal = Signal(signame, sigfunction, conditionDB)
            signals.append(signal)

    def fiteringListners(self, conditions, models):
        retval = list()
        for c in conditions:
            temp = list(c)
            temp.extend([None])
            module = temp[0].split('_')[0]
            comps = models[module].components.keys()
            comps = list(filter(lambda x: x.startswith(temp[0]),comps))
            comps = list(filter(lambda x: not x.endswith('s'),comps))
            temp[2] = [models[module].components.get(x) for x in comps]
            del temp[0]
            retval.append(temp)
        return retval
