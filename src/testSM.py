#!/usr/bin/python3
import simpy
import sys
import os
import multiprocessing
from pydispatch import dispatcher
from logging import Logger
from gate import Gate

def makeLogger(l,q):
	logger = Logger(l,q)
	logger.run()

def makeLogging(logname):
	queue = multiprocessing.Queue()
	p = multiprocessing.Process(target=makeLogger, args=(logname,queue,))
	p.start()
	return queue
		
def main(fname,stop):
	env = simpy.Environment()
	sendqueue = makeLogging(fname)
	Gate(env,sendqueue,'GA',0.05,100)
	env.run(until=stop)
	sendqueue.put('HALT')

if __name__ == "__main__":
	if len(sys.argv) > 2:
		fname = sys.argv[1]
		stopTime = int(sys.argv[2])
		if os.path.exists(fname):
			os.remove(fname)
		main(fname,stopTime)
	else:
		usage = sys.argv[0] + ' logname stoptime' 
		print(usage)
