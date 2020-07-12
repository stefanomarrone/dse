from random import random
from core.components import Component
from simpy import Store
from core.boards import Configuration
from core.utils import uniform

class Comm(Component):
    def __init__(self,nname,env):
        super().__init__(nname)
        conf = Configuration()
        self.queue = Store(env)
        self.tcomm = conf.get('[comm]t_comm')
        self.perr = conf.get('[comm]p_err')
        self.unavail = conf.get('[comm]unavail')

    def put(self,msg):
        guess = uniform(0,1)[0]
        if (guess > self.unavail):
            yield self.env.timeout(self.tcomm)
            while (random() < self.perr):
                yield self.env.timeout(self.tcomm)
            self.queue.put(msg)

    def get(self):
        msg = yield self.queue.get()
        return msg
