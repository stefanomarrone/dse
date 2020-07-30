import sys
from ertms.ertms_sim import ERTMSSimulation, ERTMSConfigurationFactory
import subprocess
import multiprocessing
import sys
import os


def core(inifile, maintfile, logfile, indicesfile):
    list_files = subprocess.call(["python3", "dse.py", inifile, maintfile, logfile, indicesfile])


if __name__ == "__main__":
    if len(sys.argv) == 5:
        config = sys.argv[1]
        maint = sys.argv[2]
        log = sys.argv[3]
        indices = sys.argv[4]
        confFactory = ERTMSConfigurationFactory()
        simulator = ERTMSSimulation([config, maint], log, indices, confFactory)
        simulator.run()
    elif len(sys.argv) == 2:
        directory = sys.argv[1]
        filenames = list(filter(lambda x: x.endswith('.ini'), os.listdir(directory)))
        filenames = list(map(lambda x: x[:-4],filenames))
        jobs = list()
        for fn in filenames:
            cn = directory + fn + '.ini'
            mn = directory + fn + '.mnt'
            ln = directory + fn + '.log'
            xn = directory + fn + '.ind'
            p = multiprocessing.Process(target=core, args=(cn, mn, ln, xn))
            jobs.append(p)
            p.start()
    else:
        usage = sys.argv[0] + ' configuration maintenance logs indices'
        usage += 'or'
        usage += sys.argv[0] + ' directory'
        print(usage)
