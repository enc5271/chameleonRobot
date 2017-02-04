import random
import copy
from collections import defaultdict
import math
import time
import sys, getopt



from State import State
#import workingPort as ssc
#import colorTracking
from QTable import *


##########################################################

# All of these should be moved to the experiment class


##########################################################

#############################################################################################
class QAgent:
	def __init__(self,isSim1,agentType):
		self.qtable = QTable('QTable.csv')
		#IMPORTANT - What should these values be? They determine many things about convergence
		self.r = 0
		self.discount = 0.8	
		self.learningRate = 0.25
		self.personality = agentType
	
	def initState(self):
		initTarget = None
		if self.isSim:
			#Matlab requires the 'physical' location of the target
			self.targetRealX = None
			self.targetRealY = None
			self.targetRealZ = None
			initTarget = self.getTarget()
		else:
			#Read target position from camera and pass to initialization state
			(rawTargetX,rawTargetY) = colorTracking.trackGreenTarget()
			initTarget=imgHash(rawTargetX,rawTargetY)
			self.ssc32 = ssc.SSC32()
		#Get a random state with the correct target partition.
		randBase,randArm,randTarget= self.qtable.getRandomState(initTarget)
		return State(randBase,randArm,0,randTarget)

	def getRandomState(self,target=None):
		return self.qtable.getRandomState(target)

	def selectRandomAction(self):
		random.seed()
		selector = random.randint(0,4)
		return ACTION_BANK[selector]

	def greedyAction(self,state):
		return self.qtable.getMaxAction(state)

	#this is the average implementation.. not sure what it is called but 30% of the time it takes a random action
	#The remaining 70% it will choose the action that maximizes the qvalue.
	def selectAction(self,state):
		if self.personality == 'curious':
			return self.selectRandomAction()
		elif self.personality =='greedy':
			return self.greedyAction(state)
		elif self.personality =='balanced':
			random.seed()
			rand = random.randint(0,10)
			if rand < 3:
				return self.selectRandomAction()
			else:
				return self.greedyAction(state)

	def softMaxSelection(self,state):
		temperature = 0.5 # How should I set this value?
		total = 0
		for a in ACTION_BANK:
			total = total + exp(self.qtable.getQValue(state,a)/temperature)
		softMaxList = []
		for a in ACTION_BANK:
			softMaxList.append( a, exp(self.qtable.getQValue(state,a)/temperature)/total )

	def update(self,state,outcomeState,action,reward):
		self.qtable.incrementFreq(state,action)
		curQ = self.qtable.getQValue(state,action)
		(maxQAction,maxQ) = self.qtable.getMaxQ(outcomeState)
		#update old q value. THIS SHOULD NOT BE DONE FOR EXPLORATORY STEPS!!!
		newQ = curQ + self.learningRate*(reward + self.discount*maxQ - curQ)
		self.qtable.setQValue(state,action,newQ)

	#targetZ is depth and only used for the simulation
	def qLearning(self,maxIterations,debug=False):
		state = self.initState()
		iterations = 0
		cumulativeReward = 0.0
		while (not(state.fire) and iterations<maxIterations):
			if not self.isSim:
				#gets new target position from camera, and returns the center of the largest green blob.
				(rawTargetX,rawTargetY) = colorTracking.trackGreenTarget()
				#
				state.target=imgHash(rawTargetX,rawTargetY)
			action = self.selectAction(state)	#see function for exploration schemes
			#take action observe outcome
			#print 'In state: {0}\nTook action: {1}'.format(state,action)
			#the distance between the affector end and the target can be used to scale the reward received.
			dist = 1
			nextState = None
			if action == 'fire':
				(nextState, dist) = self.executeAction(state,action)
			else:
				nextState,dist = self.executeAction(state,action)

			reward = self.getReward(nextState,action,dist)

			cumulativeReward = cumulativeReward + reward

			state = nextState
			iterations = iterations + 1
		if(state.fire):
			print 'Target was hit in state {0} on iteration {1}'.format(state,iterations)
			#time.sleep(.5)
		#Write the qtable to file
		self.qtable.writeTable()
		return cumulativeReward,iterations

########################################################################################

#	Main #
if __name__ == '__main__':
	argue = sys.argv[1:]
	isSim = True
	maxIter=0
	numSessions = 0
	debug = False
	try:
		opts, args = getopt.getopt(argue,"i:t:r:",['maxIter=','sess=','whateva'])
	except getopt.GetoptError:
		print 'QAgent.py -i <maxIterations> -t <numSessions> -r <runPhysicalTrial?>'
	for opt, arg in opts:
		if opt in ('-i'):
			maxIter = arg
		elif opt == '-t':
			numSessions = arg
		elif opt == '-r':
			isSim = False
		elif opt =='-d':
			debug = True
	if debug:
		runTest()
	elif isSim:
		maxIter = int(maxIter)
		numSessions = int(numSessions)	
		runTrainingSession(maxIter,numSessions)
	else:
		maxIter = int(maxIter)
		agent = QAgent(False,'greedy')
		agent.qLearning(maxIter)
