import simpy
import sys
import os
import multiprocessing
from logging import Logger
from gate import Gate

def makeLogger(q):
	logger = Logger(q)
	logger.run()

def makeLogging():
	queue = multiprocessing.Queue()
	p = multiprocessing.Process(target=makeLogger, args=(queue,))
	p.start()
	return queue
		
def main(stop):
	env = simpy.Environment()
	sendqueue = makeLogging()
	Gate(env,sendqueue,'GA',0.05,100)
	env.run(until=stop)
	sendqueue.put('HALT')

if __name__ == "__main__":
	if len(sys.argv) > 1:
		stopTime = int(sys.argv[1])
		original = sys.stdout
		if len(sys.argv) > 2:
			fname = sys.argv[2]
			if os.path.exists(fname):
				os.remove(fname)
			original = open(fname,"w")
		main(stopTime)
		sys.stdout = original
	else:
		usage = sys.argv[0] + ' stoptime logfilename'
		print(usage)