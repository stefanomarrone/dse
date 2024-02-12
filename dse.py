import sys
from ertms.ertms_sim import ERTMSSimulation, ERTMSConfigurationFactory
from applications.app_sim import AppSimulation, AppConfigurationFactory
import subprocess
import multiprocessing
import sys
import os


switch = {
    'ertms': (ERTMSConfigurationFactory,ERTMSSimulation),
    'signals': (AppConfigurationFactory,AppSimulation)
}

def core(switchkey, inifile, maintfile, logfile, indicesfile):
    configuratorname, simulatorname = switch[switchkey]
    confFactory = configuratorname()
    simulator = simulatorname([inifile, maintfile], logfile, indicesfile, confFactory)
    simulator.run()

if __name__ == "__main__":
    #todo: refactoring della funzione
    if len(sys.argv) == 6:
        actualswitch = sys.argv[1]
        cn = sys.argv[2]
        mn = sys.argv[3]
        ln = sys.argv[4]
        xn = sys.argv[5]
        core(actualswitch, cn, mn, ln, xn)
        #todo: dopo il refactoring eliminare le righe commentate
        # confFactory = ERTMSConfigurationFactory()
        # simulator = ERTMSSimulation([config, maint], log, indices, confFactory)
        # simulator.run()
    elif len(sys.argv) == 2:
        directory = sys.argv[1]
        filenames = list(filter(lambda x: x.endswith('.ini'), os.listdir(directory)))
        filenames = list(map(lambda x: x[:-4],filenames))
        for fn in filenames:
            cn = directory + fn + '.ini'
            mn = directory + fn + '.mnt'
            ln = directory + fn + '.log'
            xn = directory + fn + '.ind'
            core(cn, mn, ln, xn)
    else:
        usage = sys.argv[0] + ' configuration maintenance logs indices'
        usage += 'or'
        usage += sys.argv[0] + ' directory'
        print(usage)
