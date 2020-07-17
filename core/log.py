import logging
from core.boards import Blackboard, Configuration
import sys

class LoggerFactory():
    diction = {
        'info': logging.INFO,
        'critical': logging.CRITICAL,
        'debug': logging.DEBUG,
        'error': logging.ERROR,
        'warning': logging.WARNING
    }

    @staticmethod
    def setup(logname):
        lvl = Configuration().get('logginglevel')
        lvl = LoggerFactory.diction[lvl]
        logging.basicConfig(filename=logname, filemode='w', level=lvl, format="%(name)s;%(levelname)s;%(message)s")

    @staticmethod
    def shutdown():
        logging.shutdown()



class Loggable():
    def __init__(self, nname):
        self.name = nname
        self.logger = logging.getLogger(nname)
        #self.ch = logging.StreamHandler()
        #formatter = logging.Formatter("%(name)s;%(levelname)s;%(message)s")
        #self.ch.setFormatter(formatter)
        #self.logger.addHandler(self.ch)
        self.env = Blackboard().get('enviro')

    def getName(self):
        return self.name

    def info(self,msg):
        tosend = str(self.env.now) + ';' + msg
        if sys.is_finalizing() == False:
            self.logger.info(tosend)

    def warning(self,msg):
        tosend = str(self.env.now) + ';' + msg
        if sys.is_finalizing() == False:
            self.logger.warning(tosend)

    def critical(self,msg):
        tosend = str(self.env.now) + ';' + msg
        if sys.is_finalizing() == False:
            self.logger.critical(tosend)

    def debug(self,msg):
        tosend = str(self.env.now) + ';' + msg
        if sys.is_finalizing() == False:
            self.logger.debug(tosend)

    def error(self,msg):
        tosend = str(self.env.now) + ';' + msg
        if sys.is_finalizing() == False:
            self.logger.error(tosend)