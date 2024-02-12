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
            for l in self.listeners:
                l.process.interrupt(self.signal.name + '(F)')

class Signal(Behaviour):
    def __init__(self, nname, ffunction, cconditiondb):
        super().__init__(nname)
        conf = Configuration()
        self.deltatime = conf.get('deltatime')
        # signal generator and value
        self.signalgenerator = 0
        _locals = locals()
        exec('import math')
        exec('self.signalgenerator = lambda t : ' + ffunction, _locals)
        self.value = 0
        # conditions and hooks
        self.conditions = list()
        for cconditionstring, components in cconditiondb:
            cond = Condition(self,cconditionstring,components)
            self.conditions.append(cond)

    def update(self):
        self.value = self.signalgenerator(self.env.now)
        self.info('value update;' + str(self.value) + ';')

    def do(self):
        yield self.env.timeout(self.deltatime)
        if self.onrun:
            self.update()
            for c in self.conditions:
                c.execute(self.env.now,self.value)