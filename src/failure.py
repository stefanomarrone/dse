import random
import time
from logging import Loggable

class Repairable(Loggable):
	def __init__(self,eenv,qqueue,nname,ffProb,mmttr):
		super().__init__(nname,qqueue)
		self.fProb = ffProb
		self.mttr = mmttr
		self.env = eenv

	def fail(self):
		self.log(' has failed @' + str(self.env.now))
	
	def repair(self):
		yield self.env.timeout(self.mttr)
		self.log(' has been repaired @' + str(self.env.now))
	
	def step(self):
		guess = (random.random() < self.fProb)
		if (guess):
			self.fail()
			yield self.env.process(self.repair()) 
		else:
			self.do()
