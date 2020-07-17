import sys
from ertms.ertms_sim import ERTMSSimulation, ERTMSConfigurationFactory

if __name__ == "__main__":
    if len(sys.argv) > 4:
        config = sys.argv[1]
        maint = sys.argv[2]
        log = sys.argv[3]
        indices = sys.argv[4]
        confFactory = ERTMSConfigurationFactory()
        simulator = ERTMSSimulation([config, maint], log, indices, confFactory)
        simulator.run()
    else:
        usage = sys.argv[0] + ' configuration maintenance logs indices'
        print(usage)
