from core.performing import Behaviour
from threading import Timer
from simpy import Event
from core.boards import Configuration, Blackboard

class WatchDogFactory():
    @staticmethod
    def generate():
        conf = Configuration()
        ttimeout = conf.get('watchdog[period]')
        rratio = conf.get('watchdog[monitorperiod]')
        rratioFlag = conf.get('watchdog[monitorflag]')
        finalTime = conf.get('stoptime')
        ttimeoutFlag = ttimeout != 0
        period = rratio * finalTime
        enviro = Blackboard().get('enviro')
        wd = WatchDog(ttimeoutFlag,ttimeout,period,rratioFlag,enviro)
        return wd



class WatchDog():
    def __init__(self,ttimeoutFlag,timeout,vverbosityPeriod,vverbosity,enviro):
        self.terminating = Event(enviro)
        w = WatchDogTimer(ttimeoutFlag,timeout,self.terminating)
        m = Monitor(vverbosity,vverbosityPeriod,w)

    def getTrigger(self):
        return self.terminating



class Monitor(Behaviour):
    def __init__(self,printflag,pperiod,watchdog):
        super().__init__('Monitor')
        self.period = pperiod
        self.flag = printflag
        self.wdt = watchdog

    def run(self):
        while True:
            yield self.env.timeout(self.period)
            self.wdt.reset()
            if self.flag:
                ratio = float(self.env.now) / float(self.infinite)
                print('Percentage ' + str(ratio * 100) + "%")



class WatchDogTimer:
    def __init__(self, flag, ttimeout, eevent):  # timeout in seconds
        self.timeout = ttimeout
        self.event = eevent
        trigger = self.alarm if flag else lambda: 0
        self.timer = Timer(self.timeout, trigger)
        self.timer.start()

    def alarm(self):
        self.event.succeed()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.alarm)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self