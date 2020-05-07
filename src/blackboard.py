from metaclasses import Singleton

class Blackboard(metaclass=Singleton):

    def __init__(self):
        self.board = dict()

    def get(self,key):
        return self.board[key]

    def put(self,key,value):
        self.board[key] = value

    def dump(self):
        print(self)
        print(self.board)