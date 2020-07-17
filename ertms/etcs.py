from core.performing import Behaviour
from ertms.datatypes import FailureKind
from core.measures import Recorder
from math import ceil

class Subsystem():
    def __init__(self, kkind, iindex):
        self.kind = kkind
        self.index = iindex
        self.status = True

    def change(self):
        self.status = not self.status

    def isUp(self):
        return self.status

    def isDown(self):
        return not self.status

    def isRBC(self):
        return self.kind == 'RBC'


class ETCS(Behaviour):
    def __init__(self, nname, cchannel, numofrbc, numofevc):
        super().__init__(nname)
        self.channel = cchannel
        self.nrbc = numofrbc
        self.nevc = numofevc
        self.lastchangetime = 0
        self.status = FailureKind.Normal
        self.nextstatus = FailureKind.Normal
        self.dictionary = self.generateDictionary()
        event = self.env.timeout(self.infinite- self.env.now - 1)
        event.callbacks.append(self.recordStateChange)

    def generateDictionary(self):
        retval = dict()
        for i in range(0,self.nrbc):
            s = Subsystem('RBC',i)
            name = 'RBC_' + str(i) + '_top'
            retval[name] = s
        for i in range(0,self.nevc):
            s = Subsystem('EVC',i)
            name = 'EVC_' + str(i) + '_top'
            retval[name] = s
            s = Subsystem('COMM',i)
            name = 'EVC_' + str(i) + '_logic'
            retval[name] = s
        return retval

    def do(self):
        self.recordStateChange()
        event = yield self.channel.get()
        self.manageEvent(event)
        self.nextstatus = self.nextStatus()

    def nextStatus(self):
        newstatus = FailureKind.Normal
        lostTrains = self.getLostTrains()
        if lostTrains >= 2:
            newstatus = FailureKind.Immobilizing
        elif lostTrains == 1:
            newstatus = FailureKind.Service
        return newstatus

    def manageEvent(self, event):
        subsystem = self.dictionary[event]
        subsystem.change()

    def recordStateChange(self,e = None):
        tag = FailureKind.tostr(self.status)
        Recorder().add(tag,self.env.now - self.lastchangetime)
        self.status = self.nextstatus
        tag = FailureKind.tostr(self.status)
        self.warning('changed into;' + tag + ';')
        self.lastchangetime = self.env.now

    def getLostTrains(self):
        ratio = ceil(float(self.nevc) / float(self.nrbc))
        retval = 0
        keys = self.dictionary.keys()
        for k in keys:
            sub = self.dictionary[k]
            if sub.isRBC() and sub.isDown():
                retval += ratio
        items = self.dictionary.items()
        items = list(filter(lambda x: x[1].status == False,items))
        items = list(filter(lambda x: not x[1].isRBC(),items))
        items = list(map(lambda x: x[1].index,items))
        items = list(set(items))
        retval += len(items)
        return retval
