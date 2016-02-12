import csv
import matlab.engine
import random
import copy
from collections import defaultdict
import math

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
								print row[5]
								return row[5]
		print 'ERROR: In getQValue Table entry not found.'
		

	def setQValue(self,state,action1,newReward):
		#print 'In set Reward'
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
							qvalues.append(row[5])
		if len(qvalues)==0:
			print 'ERROR: In getQActionPairs Table entry not Found.'
		return qvalues			 

	def getMaxQ(self,state):
		qvalues = self.getQActionPairs(state)
		if(len(qvalues)>0):
			print max(qvalues)
			return max(qvalues)
		else:
			print "This case should never happen, and is only left here for debugging. Remove me before program is shipped out!"
			return -1000	#IMPORTANT - What should be done in the case that this state has not been visited

class QAgent:
	def __init__(self,isSim1):
		self.isSim = isSim1
		if self.isSim:
			self.matlabEng = matlab.engine.start_matlab()
			#Matlab requires the 'physical' location of the target
			self.targetRealX = None
			self.targetRealY = None
			self.targetRealZ = None
			self.generateTarget()
		#IMPORTANT - What should these values be? They determine many things about convergence
		self.r = 0
		self.discount = 0.8	
		self.learningRate = 0.2
		######################################################################################
		self.initState = State(1.570796,1.570796,0,None)
		self.qtable = QTable('QTable.csv')
		
		
	def generateTarget(self):
		#Write code to generate random targets X,Y,Z
		self.target=1
		self.targetRealX = 22.0
		self.targetRealY = 13.0
		self.targetRealZ = 20.0
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

	#this is the average implementation.. not sure what it is called but 30% of the time it takes a random action
	#The remaining 70% it will choose the action that maximizes the qvalue.
	def selectAction(self):
		random.seed()
		rand = random.randint(0,10)
		if rand < 3:
			return selectRandomAction()
		else:
			broken

	def executeAction(self,state, action):
		#The move command for the physical agent should also be added
		newState = copy.copy(state)
		success = 0
		if self.isSim:
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
		else:
			print 'send action to Turret.py'

	#targetZ is depth and only used for the simulation
	def qLearning(self,startState='',maxIterations):
		if startState=='':
			state = self.initState
		else:
			state = startState
		iterations = 0
		while (not(state.fire) and iterations<maxIterations):
			#select an action
			action = self.selectRandomAction()	#there should be an exploration function or something else here but for now this is ok since the agent is far from converging on an optimal policy
			#take action observe outcome
			nextState = self.executeAction(state,action)
			reward = self.getReward(nextState)
			curQ = self.qtable.getQValue(state,action)
			maxQ = self.qtable.getMaxQ(nextState)
			#update old q value
			newQ = curQ + self.learningRate*(reward + self.discount*maxQ - curQ)
			self.qtable.setQValue(state,action,newQ)
			state = nextState
			iterations = iterations + 1
			print state
			print 'Iteration '+str(iterations)
		if(state.fire):
			print 'Target was hit in state {0}'.format(state)
		self.qtable.writeTable();

########################################################################################
#	Main #
testState = State(0.837758,1.0,0,0)
agent = QAgent(True)
agent.qLearning(testState,maxIterations)

#TO DO
'''
The simluated target X,Y location function needs to be created
Generating the Real target position should also be created
implement exploration function
implement writeTable
rename getQValue and setQValue to getQValue setqvalue
put qtable in a diffrent file, should change the data structure eventually

BEGIN TESTING!!!!!!
'''