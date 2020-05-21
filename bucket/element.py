from bucket.failure import TooSimpleRepairable

class SimpleElement(TooSimpleRepairable):
	def __init__(self,eenv,qqueue,nname,ttime,ffProb,mmttr):
		super().__init__(eenv,qqueue,nname,ffProb,mmttr)
		self.time = ttime
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


