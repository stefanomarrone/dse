from simpy import Interrupt
import core.utils as utils
from core.boards import Configuration
from core.log import Loggable
from core.performing import Behaviour


class Condition(Loggable):
    def __init__(self, ssignal, cconditionstring, llisteners):
        # name
        self.signal = ssignal
        self.conditionstring = cconditionstring
        # function
        payload = 'self.conditionevaluator = lambda t, ' + self.signal.name + ' : ' + self.conditionstring
        self.conditionevaluator = 0
        _locals = locals()
        exec('import math')
        exec(payload, _locals)
        # listeners
        self.listeners = llisteners

    def execute(self, time, value):
        flag = self.conditionevaluator(time, value)
        if flag:
            #self.signal.onrun = False
            #self.signal.process.interrupt(self.signal.name + '(F)')
            self.signal.caseid=self.signal.caseid+1
            self.caseidPropagation()
            for l in self.listeners:
                if(l.working==True):
                    l.process.interrupt(self.signal.name + '(F)')

    def caseidPropagation(self):
        for l in self.listeners:
            l.caseid=self.signal.caseid
            l.caseidPropagation()


'''
    def restartWorking(self):

        self.signal.onrun=all(llisteners.working for llisteners in self.listeners)
        if(self.signal.onrun==True):
            self.signal.process.interrupt(self.signal.name+'(R)')



'''


class Signal(Behaviour):
    def __init__(self, nname, ffunction, cconditiondb):
        super().__init__(nname)
        conf = Configuration()
        self.deltatime = conf.get('deltatime')
        # signal generator and value
        self.signalgenerator = 0
        _locals = locals()
        exec('import math')
        exec('self.signalgenerator = lambda t,a : ' + ffunction, _locals)
        self.value = 0
        # conditions and hooks
        self.conditions = list()
        self.caseid=0
        for cconditionstring, components in cconditiondb:
            cond = Condition(self,cconditionstring,components)
            self.conditions.append(cond)

    def update(self):
        delta=list()
        counter=list()
        for c in self.conditions:
            for l in c.listeners:
                delta.append(l.faultStartTime)
                counter.append(l.faultCounter)
            self.caseid=l.caseid

        delta_time=max(delta)
        counter_max=max(counter)
        self.value = round(self.signalgenerator(self.env.now-delta_time,counter_max),5)
        self.value_acquired(str(self.caseid)+';'+'value update;' + str(self.value) )

    def do(self):
        yield self.env.timeout(self.deltatime)
        if self.onrun:
            self.update()
            for c in self.conditions:
                c.execute(self.env.now,self.value)



    '''cancella da qua in poi'''




'''
    def rework(self):
        for c in self.conditions:
            c.restartWorking()

    def run(self):
        self.boot()
        while True:
            while(self.onrun):
                try:
                    yield self.env.process(self.do())

                except Interrupt as i:
                    kind, source = utils.unpack_interrupt(i.cause)
                    self.onrun = False

            while(not self.onrun):
                try:

                    yield self.env.process(self.rework())
                except Interrupt as i:
                    (kind, source) = utils.unpack_interrupt(i.cause)



'''