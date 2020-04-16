from statemachine import StateBasedItem


class Gate(StateBasedItem):
	def __init__(self,eenv,qqueue,nname,ffProb,mmttr):
		super().__init__(eenv,qqueue,nname,ffProb,mmttr)
	
	def populate(self):
		

	def 

	def run(self):
		while True:
			yield self.env.process(self.step())
