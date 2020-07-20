from core.boards import *
from configparser import ConfigParser
from core.executors import ExecutorFactory

class ConfigurationFactory(AbstractBoardFactory):
    def __init__(self):
        super().__init__()
        self.mapping['hwconf'] = self.hardware

    def hardware(self,value):
        retval = eval('list(' + value + ')')
        return retval

    def loadMaintenance(self,inifile,submodels):
        conf = Configuration()
        reader = ConfigParser()
        reader.read(inifile)
        try:
            temp = reader['main']['maintainers']
            value = self.process(temp) if (self.processable(temp)) else None
            conf.put('[main]maintainers', value)
            for s in submodels:
                options = reader.options(s)
                for o in options:
                    lst = reader[s][o].split(';')
                    if len(lst) == 2:
                        mttr, priority = tuple(reader[s][o].split(';'))
                        if self.processable(mttr):
                            value = self.process(mttr)
                        conf.put('[' + s + ']' + o + '_mttr',value)
                        if self.processable(priority):
                            value = self.process(priority)
                        conf.put('[' + s + ']' + o + '_priority',value)
                    else:
                        if self.processable(reader[s][o]):
                            value = self.process(reader[s][o])
                        conf.put('[' + s + ']' + o,value)
        except Exception as s:
            print(s)

    def loadConfiguration(self,inifile):
        conf = Configuration()
        print(conf)
        reader = ConfigParser()
        reader.read(inifile)
        try:
            temp = reader['main']['experiments']
            conf.put('experiments', int(temp))
            temp = reader['main']['epsilon']
            conf.put('epsilon', float(temp))
            temp = reader['main']['logginglevel']
            conf.put('logginglevel', temp)
            temp = reader['main']['executor']
            conf.put('executor', ExecutorFactory.generate(temp))
            temp = reader['main'].get('slaves',1)
            conf.put('slaves', int(temp))
            temp = reader['main']['stoptime']
            temp = self.process(temp)
            conf.put('stoptime', temp)
            # loading the numbers of the elements
            temp = self.loadSection(reader,'ertms')
            conf.merge(temp)
            submodels = self.tolist(reader['main']['submodels'])
            conf.put('submodels', submodels)
            for s in submodels:
                temp = self.loadSection(reader,s)
                conf.merge(temp)
        except Exception as s:
            print(s)
        return submodels