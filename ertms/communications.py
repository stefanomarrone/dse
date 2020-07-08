from typing import Any

from simpy.resources.store import StoreGet, StorePut
from random import random
from core.log import Loggable
from simpy import Store
from core.boards import Configuration

class Comm(Loggable,Store):
    def __init__(self,name,env):
        Loggable(name)
        Store(env)
        conf = Configuration()
        self.tcomm = conf.get('[comm]t_comm')
        self.perr = conf.get('[comm]p_err')
        self.unavail = conf.get('[comm]unavail')

    def put(  # type: ignore[override] # noqa: F821
            self, item: Any
        ) -> StorePut:
        if (random() > self.unavail):
            yield self.env.timeout(self.tcomm)
            while (random() < self.perr):
                yield self.env.timeout(self.tcomm)
            Store.put(item)
    


