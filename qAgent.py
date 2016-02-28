import csv
import random
import copy
from collections import defaultdict
import math

#import detectCollision
import workingPort as ssc
import colorTracking

#ACTION_BANK = ['base_10', 'base_-10', 'arm_10', 'arm_-10', 'fire']
ACTION_BANK = ['left', 'right', 'up', 'down', 'fire']
#These definitions are also defined in Turret.py
#These are the true values
'''
BASE_MIN = round(math.pi/4,5)
BASE_MAX = round(3*math.pi/4,5)
ARM_MIN = round(5*math.pi/12,5)
ARM_MAX = round(7*math.pi/12,5)
'''
#These are the value for the simplified case. I should really reorganize these as class members.
BASE_MIN = 0.837758
BASE_MAX = 2.3
ARM_MIN = 1.0
ARM_MAX = 2.1416

class State:
	def __init__(self, base1,arm1,fire1,target):
		self.base = base1
		self.arm = arm1
		self.fire = fire1
		self.target = target
		
	def __str__(self):
		return "({0},{1},{2},{3})".format(self.base,self.arm,self.fire,self.target)

class Action:
	def __init__(self,actionName):
		self.action = actionName

class QTable:
	def __init__(self,filename=''):
		self.qtable = []
		if filename == '':
			print 'Creating new QTable.'
		else:
			self.loadTable(filename)

	def loadTable(self,filename):
		with open(filename,'rb') as csvfile:
			qreader = csv.reader(csvfile)
			for row in qreader:
				row[0] = float(row[0])
				row[1] = float(row[1])
				row[2] = int(row[2])
				row[3] = int(row[3])
				row[4] = row[4]
				row[5] = float(row[5])
				row[6] = int(row[6])
				self.qtable.append(row)

	def writeTable(self,filename='QTable.csv'):
		#Write QTable from memory to 'QTable.csv' in current directory.
		with open(filename,'r+') as csvfile:
			for row in self.qtable:
				csvfile.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

	def getQValue(self,state,action1):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.fire:
						if row[3]==state.target:
							if row[4]==action1:
								return row[5]
		print 'ERROR: In getQValue Table entry not found.'
		
	def setQValue(self,state,action1,newReward):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.fire:
						if row[3]==state.target:
							if row[4]==action1:
								row[5] = newReward
								row[6] = row[6] + 1
								return
		print 'ERROR: In setQValue Table entry not Found.'

	def getFreq(self,state,action1):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.fire:
						if row[3]==state.target:
							if row[4]==action1:
								return row[6]
		print 'ERROR: In getFreq Table entry not Found.'

	def incrementFreq(self,state,action1):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.fire:
						if row[3]==state.target:
							if row[4]==action1:
								row[6] = row[6]+1
								return
		print 'ERROR: In incrementFreq Table entry not Found.'

	def getQActionPairs(self,state):
		qvalues = []
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.fire:
						if row[3]==state.target:
							qvalues.append([row[4],row[5]])
		if len(qvalues)==0:
			print 'ERROR: In getQActionPairs Table entry not Found.'
		return qvalues			 

	def getMaxQ(self,state):
		pairs = self.getQActionPairs(state)
		if(len(pairs)>0):
			maxQ = pairs[0]
			for pair in pairs:
				if maxQ[1] < pair[1]:
					maxQ = pair
			#Note that maxQ is the tuple (state, action)
			return maxQ
		else:
			print "This case should never happen, and is only left here for debugging. Remove me before program is shipped out!"
			return -1000	#IMPORTANT - What should be done in the case that this state has not been visited

#############################################################################################
class QAgent:
	def __init__(self,isSim1,agentType):
		self.qtable = QTable('QTable.csv')
		self.isSim = isSim1
		self.initState = State(self.qtable.qtable[0][0],self.qtable.qtable[0][1],0,0)
		if self.isSim:
			#self.matlabEng = matlab.engine.start_matlab()
			#Matlab requires the 'physical' location of the target
			self.targetRealX = None
			self.targetRealY = None
			self.targetRealZ = None
			target = self.generateTarget()
		else:
			self.ssc32 = ssc.SSC32()
			
		#IMPORTANT - What should these values be? They determine many things about convergence
		self.r = 0
		self.discount = 0.8	
		self.learningRate = 0.2
		self.personality = agentType
		######################################################################################
		
		
		
		
	def generateTarget(self):
		random.seed()
		partitionBank = [[0 ,2], [1,3]]
		#known to work [22 13 20] x y z
		self.targetRealX = random.uniform(0,55)
		self.targetRealY = random.uniform(0,35)
		self.targetRealZ = random.uniform(0,20)
		xPartition = int(self.targetRealX / 28)
		yPartition = int(self.targetRealY / 18)
		print 'Target: {0} {1} {2}'.format(self.targetRealX,self.targetRealY,self.targetRealZ)
		target = partitionBank[xPartition][yPartition]
		return target
		'''Map targets actual position to pixels
		focalD = 25;
		Projected = [1,0,0,0;0,1,0,0;0,0,-1/focalD,0]*targets(1)
		'''

	def isHit(self,state):
		print state
		return self.matlabEng.detectCollision(state.base,state.arm,self.targetRealX,self.targetRealY,self.targetRealZ)

	def selectRandomAction(self):
		random.seed()
		selector = random.randint(0,4)
		return ACTION_BANK[selector]

	def getReward(self,state):
		if state.fire==1:
			return 100
		else:
			return 0

	def greedyAction(self,state):
		return self.qtable.getMaxQ(state)[0]

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

	def executeVirtualAction(self,state,action):
		success = 0
		newState = copy.copy(state)
		action = action.split('_') #check that this remove the under score and returns the action descriptor and degrees
		if action[0] == 'base':
			angleChange = float(action[1])
			newAngle = (state.base + angleChange)
			if BASE_MIN  <= newAngle <= BASE_MAX:
				newState.base = newAngle

		elif action[0] =='arm':
			angleChange = float(action[1])
			newAngle = (state.arm + angleChange)
			if ARM_MIN  <= newAngle <= ARM_MAX:
				newState.arm = newAngle
		elif action[0] == 'fire':
			if self.isHit(state):
				#The target was hit
				newState.fire= 1 	
			else:
				#missed the target
				newState.fire = 0 	
		elif action[0]=='up':
			if state.arm == ARM_MAX:
				newState.arm =newState.arm
			elif state.arm < ARM_MAX:
				newState.arm = ARM_MAX 
		elif action[0]=='down':
			if state.arm == ARM_MIN:
				newState.arm =newState.arm
			elif state.arm > ARM_MIN:
				newState.arm = ARM_MIN 
		elif action[0]=='left':
			if state.base == BASE_MIN:
				newState.base =newState.base
			elif state.base > BASE_MIN:
				newState.base = BASE_MIN 
		elif action[0]=='right':
			if state.base == BASE_MAX:
				newState.base =newState.base
			elif state.base < BASE_MAX:
				newState.base = BASE_MAX 
		else:
			print 'ERROR: Action not found.'
			return
		return newState

	def getSSC32Command(self,state,action):


	def executePhysicalAction(state,action):
		newState = copy.copy(state)
		#Not sure if I should get the state from software or query the servo controller
		newState = self.executeVirtualAction(newState)
		if(action== 'fire'):
			self.ssc32.executeSingleCommand('#7H')
			sleep(1)
			self.ssc32.executeSingleCommand('#7L')
		else:
			command = self.getSSC32Command(newState)
			self.ssc32.executeSingleCommand(command)
		return newState

	def executeAction(self,state, action):
		#The move command for the physical agent should also be added
		
		if self.isSim == 1:
			return executeVirtualAction(state,action)
		
		else:
			return executePhysicalAction(state,action)

	#targetZ is depth and only used for the simulation
	def qLearning(self,maxIterations,startState=''):
		if startState=='':
			state = self.initState
		else:
			state = startState
		iterations = 0
		while (not(state.fire) and iterations<maxIterations):
			action = self.selectAction(state)	#see function for exploration schemes
			#take action observe outcome
			print 'In state: {0}\nTook action: {1}'.format(state,action)
			nextState = self.executeAction(state,action)
			reward = self.getReward(nextState)
			curQ = self.qtable.getQValue(state,action)
			(maxQAction,maxQ) = self.qtable.getMaxQ(nextState)
			#update old q value
			newQ = curQ + self.learningRate*(reward + self.discount*maxQ - curQ)
			self.qtable.setQValue(state,action,newQ)
			state = nextState
			iterations = iterations + 1
			
		if(state.fire):
			print 'Target was hit in state {0} on iteration {1}'.format(state,iterations)
		self.qtable.writeTable();

########################################################################################
#	Main #

agent = QAgent(False,'curious')
agent.qLearning(2)

#TO DO
'''
put qtable in a diffrent file, should change the data structure eventually
Fix detectCollision 
BEGIN TESTING!!!!!!
'''