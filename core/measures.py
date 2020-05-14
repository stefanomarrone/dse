import csv
import functools


class Metric():
    def __init__(self, nname):
        self.name = nname

    def compute(self,handle):
        pass

    def print(self):
        pass


class Downtime(Metric):
    def __init__(self, nname, eelement, uupStartEvent, ddownStartEvent):
        super().__init__(nname)
        self.uptimes = list()
        self.downtimes = list()
        self.downStartEvent = ddownStartEvent
        self.upStartEvent = uupStartEvent
        self.element = eelement

    def compute(self,handle):
        temp = 0
        for row in handle:
            if (row[1] == self.element):
                if (row[2] == self.upStartEvent):
                    temp = float(row[0]) - temp
                    self.uptimes.append(temp)
                    temp = float(row[0])
                if (row[2] == self.downStartEvent):
                    temp = float(row[0]) - temp
                    self.downtimes.append(temp)
                    temp = float(row[0])
        self.uptimes = list(filter(lambda t: t != 0, self.uptimes))
        self.downtimes = list(filter(lambda t: t != 0, self.downtimes))

    def report(self):
        retval = 'Metric: ' + self.name + '\n'
        up = sum(self.uptimes)
        retval += 'Uptime = ' + str(up) + '\n'
        down = sum(self.downtimes)
        retval += 'Downtime = ' + str(down) + '\n'
        retval += 'Availability = ' + str(up / (up + down)) + '\n'
        return retval


class MetricAnalyser:
    def __init__(self):
        self.metrics = list()

    def addMetric(self,metric):
        self.metrics.append(metric)

    def compute(self,csvfilename):
        csvhandle = open(csvfilename)
        csvReader = csv.reader(csvhandle,delimiter=';')
        for m in self.metrics:
            m.compute(csvReader)

    def report(self):
        retval = ''
        for m in self.metrics:
            retval += str(m.report())
        return retval