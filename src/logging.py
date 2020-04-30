import datetime
import time

class Loggable():
	def __init__(self,nname,qqueue):
		self.name = nname
		self.queue = qqueue

	def log(self,message):
		tosend = self.name + message
		self.queue.put(tosend)

class Logger:
	def __init__(self,qqueue):
		self.queue = qqueue
		self.running = True

	def manage(self,message):
		if (message == 'HALT'):
			self.running = False
		else:
			self.log(message)

	def log(self,message):
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		print(st + '\t' + message)

	def run(self):
		while (self.running == True):
			m = self.queue.get()
			self.manage(m)

