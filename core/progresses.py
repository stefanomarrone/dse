from core.performing import Behaviour

class Progressor(Behaviour):
    def __init__(self):
        super().__init__('Progressor')
        self.period = self.infinite / 1000

    def run(self):
        while True:
            yield self.env.timeout(self.period)
            ratio = float(self.env.now) / float(self.infinite)
            print('Percentage ' + str(ratio * 100) + "%")