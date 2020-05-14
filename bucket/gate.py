from bucket.statemachine import StateBasedItem, State


class Gate(StateBasedItem):
	def __init__(self,eenv,qqueue,nname,ffProb,mmttr):
		super().__init__(eenv,qqueue,nname,ffProb,mmttr)

	def actionS1(self):
		self.log(' has done actionS1 @' + str(self.env.now))

	def actionS2(self):
		self.log(' has done actionS1 @' + str(self.env.now))

	def populate(self):
		retval = dict()
		retval['S1'] = State([('S1',0.7),('S2',0.3)],10,self.actionS1)
		retval['S2'] = State([('S1',0.5),('S2',0.5)],20,self.actionS2)
		return retval
		
	def reset(self):
		return 'S1'
