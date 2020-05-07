class DependabilityException(Exception):
    def __init__(self,*args):
        self.interrupter = (' by ' + args[0]) if (args) else ''
        self.setKind()

    def setKind(self):
        self.kind = 'Dependability'

    def __str__(self):
        return self.kind + ' Exception' + self.interrupter


class ReliabilityException(DependabilityException):
    def __init__(self, *args):
        super().__init__()

    def setKind(self):
        self.kind = 'Reliability'


class MaintainabilityException(DependabilityException):
    def __init__(self, *args):
        super().__init__()

    def setKind(self):
        self.kind = 'Maintainability'
