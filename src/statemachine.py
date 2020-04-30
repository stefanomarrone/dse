from failure import TooSimpleRepairable
from utils import lottery

class State:
	def __init__(self,ttransitions,ssojourn,aaction):
		self.sojourn = ssojourn
		self.action = aaction
		self.transitions = ttransitions

	def getAction(self):
		return self.action
		
	def getSojourn(self):
		return self.sojourn

	def getNext(self):
		probs = list(map(lambda x: x[1],self.transitions))
		index = lottery(probs)
		nextState = self.transitions[index][0]
		return nextState


class StateBasedItem(TooSimpleRepairable):
	def __init__(self,eenv,qqueue,nname,ffProb,mmttr):
		super().__init__(eenv,qqueue,nname,ffProb,mmttr)
		self.stateMachine = self.populate()
		self.current = self.reset()
		self.env.process(self.run())

	def do(self):
		nextstate = self.stateMachine[self.current].getNext()
		self.log(' starting from ' +  self.current + ' to ' + nextstate + ' @' + str(self.env.now))
		time = self.stateMachine[nextstate].getSojourn()
		yield self.env.timeout(time) 
		self.stateMachine[nextstate].getAction()()
		self.current = nextstate
		self.log(' ending from ' +  self.current + ' to ' + nextstate + ' @' + str(self.env.now))

	def run(self):
		while True:
			yield self.env.process(self.step())
