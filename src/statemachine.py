from failure import Repairable

class State:
	def __init__(self,nname,ttransitions,ssojourn,aaction):
		self.
		


class StateBasedItem(Repairable):
	def __init__(self,eenv,qqueue,nname,ffProb,mmttr):
		super().__init__(eenv,qqueue,nname,ffProb,mmttr)
		self.stateMachine = self.populate()
		self.currentState = self.reset()
		self.env.process(self.run())

	def do(self):
		self.log(' has done @' + str(self.env.now))
		yield self.env.process(self.wait()) 
	
	def wait(self):
		self.log(' started waiting @' + str(self.env.now))
		yield self.env.timeout(self.time) 
		self.log(' finished waiting @' + str(self.env.now))

	def run(self):
		while True:
			yield self.env.process(self.step())
