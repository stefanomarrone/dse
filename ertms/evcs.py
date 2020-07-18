from simpy import Resource
from core.performing import *
from core.subsystems import Hardware
from core.measures import Recorder
from core.boards import Blackboard

class PrivateArea(Resource):
    def __init__(self,env,capacity):
        super().__init__(env,capacity)
        self.lasttime = 0
        self.fresh = True

    def setTime(self):
        self.lasttime = self._env.now
        self.fresh = True

    def getTime(self):
        temp = self.fresh
        self.fresh = False
        return temp, self.lasttime


class EVCLogic(Behaviour):
    def __init__(self, nname, nnretry, ttretry, nnvcontact, privatearea, listeners):
        super().__init__(nname)
        self.private = privatearea
        self.nvcontact = nnvcontact
        self.nretry = nnretry
        self.tretry = ttretry
        self.listeners = listeners
        self.lastFreshness = True
        self.error = False

    def do(self):
        if self.onrun == True:
            yield self.env.timeout(1)
            with self.private.request() as req:
                yield req
                freshness, vitality = self.private.getTime()
                downtime = self.env.now - self.lastFreshness - self.tolerance()
                if freshness:
                    if self.error:
                        Recorder().add(self.name, downtime)
                        self.error = False
                        self.notify()
                    self.lastFreshness = vitality
                else:
                    if downtime > 0:
                        if self.error == False:
                            self.notify()
                        self.error = True


    def tolerance(self):
        return self.nretry * self.tretry + self.nvcontact

    def down(self, time):
        self.warning('commdown;' + str(time) + ';')
        self.notify()
        Recorder().add(self.name,time)

    def notify(self):
        for l in self.listeners:
            l.put(self.name)



class EVCServer(Behaviour):
    def __init__(self, nname, cchannel, sshared):
        super().__init__(nname)
        self.channel = cchannel
        self.shared = sshared

    def do(self):
        if self.onrun == True:
            msg = yield self.env.process(self.channel.get())
            with self.shared.request() as req:
                yield req
                self.shared.setTime()



class EVC():
    def __init__(self, nname, cchannel, toetcs):
        black = Blackboard()
        env = black.get('enviro')
        conf = Configuration()
        mttr = conf.get('[evc]mttr')
        comp = conf.get('[evc]structure')
        nretry = conf.get('[comm]num_retry')
        tretry = conf.get('[comm]t_retry')
        nvcontact = conf.get('[comm]tnv')
        private = PrivateArea(env,1)
        self.server = EVCServer(nname + '_server',cchannel, private)
        self.logic = EVCLogic(nname + '_logic', nretry, tretry, nvcontact, private, [toetcs])
        self.structure = Hardware(nname, comp, mttr, [toetcs], self.logic)