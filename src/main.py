#!/usr/bin/python3
import simpy
import sys
import os
import multiprocessing
from log import Logger
from element import SimpleElement

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
	SimpleElement(env,sendqueue,'GA',10,0.05,100)
	SimpleElement(env,sendqueue,'GB',7,0.05,50)
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
