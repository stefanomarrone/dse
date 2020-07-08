from simpy import Resource
from core.boards import Blackboard

class MaintainersFactroy():
    @staticmethod
    def generate(numbers):
        env = Blackboard().get('enviro')
        retval = Resource(env,numbers)
        return retval