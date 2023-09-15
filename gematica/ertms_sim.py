from core.simulations import Simulation, AbstractArgumentFactory
from ertms.etcs import ETCS
from ertms.configurations import ConfigurationFactory
from ertms.communications import Comm
from ertms.evcs import EVC
from ertms.rbcs import RBC
from core.boards import Configuration
from simpy import Store

class ERTMSConfigurationFactory(AbstractArgumentFactory):

    def setup(self,iifiles,iindices):
        cfile = iifiles[0]
        mfile = iifiles[1]
        conf = ConfigurationFactory()
        subs = conf.loadConfiguration(cfile)
        conf.loadMaintenance(mfile, subs)
        conf = Configuration()
        conf.put('indices', iindices)



class ERTMSSimulation(Simulation):
    def __init__(self, infiles, logs, iindices, factory):
        super().__init__(infiles, logs, iindices, factory)

    def loadScenario(self,enviro):
        numberOfEvcs = Configuration().get('[ertms]evcs')
        numberOfRbcs = Configuration().get('[ertms]rbcs')
        toETCS = Store(enviro)
        rbcs = list()
        comms = list()
        evcs = list()
        for i in range(0, numberOfRbcs):
            rname = 'RBC_' + str(i)
            rbc = RBC(rname,toETCS)
            rbcs.append(rbc)
        rbcCounter = 0
        for i in range(0, numberOfEvcs):
            cname = 'COMM_' + str(i)
            comm = Comm(cname, enviro)
            comms.append(comm)
            ename = 'EVC_' + str(i)
            evc = EVC(ename, comm, toETCS)
            evcs.append(evc)
            logicname = 'LOGIC_' + str(rbcCounter) + '_to_' + str(i)
            rbcs[rbcCounter].addBehaviour(logicname,comm)
            rbcCounter = (rbcCounter + 1) % numberOfRbcs
        etcs = ETCS('ETCS',toETCS,numberOfRbcs,numberOfEvcs)