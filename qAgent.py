import random
import copy
from collections import defaultdict
import math
import time

#import detectCollision
import workingPort as ssc
import colorTracking
from QTable import *

ACTION_BANK = ['left', 'right', 'up', 'down', 'fire']
PARTITION = [[0 ,2], [1,3]]
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

#############################################################################################
#	Helper Functions

def radian2Pwm(rad):
	pwm = 600 + rad*(1800/math.pi)
	return pwm

def imgHash(x, y):
	#This is dependent on the camera
	imgHeight = 480
	imgWidth = 640
	#number of img divisions
	partitions=2
	hashX = x/(imgWidth/partitions)
	hashY = y/(imgHeight/partitions)
	print x,y
	print hashX,hashY
	return PARTITION[hashX][hashY]


#############################################################################################
class QAgent:
	def __init__(self,isSim1,agentType):
		self.qtable = QTable('QTable.csv')
		self.isSim = isSim1
		self.initState = State(self.qtable.qtable[0][0],self.qtable.qtable[0][1],0,0)
		if self.isSim:
			#Matlab requires the 'physical' location of the target
			self.targetRealX = None
			self.targetRealY = None
			self.targetRealZ = None
			target = self.generateTarget()
		else:
			#Read target position from camera and pass to initialization state
			(rawTargetX,rawTargetY) = colorTracking.trackGreenTarget()
			self.initState.target=imgHash(rawTargetX,rawTargetY)
			self.ssc32 = ssc.SSC32()
			
		#IMPORTANT - What should these values be? They determine many things about convergence
		self.r = 0
		self.discount = 0.8	
		self.learningRate = 0.2
		self.personality = agentType
		
	def generateTarget(self):
		random.seed()
		#known to work [22 13 20] x y z
		self.targetRealX = random.uniform(0,55)
		self.targetRealY = random.uniform(0,35)
		self.targetRealZ = random.uniform(0,20)
		xPartition = int(self.targetRealX / 28)
		yPartition = int(self.targetRealY / 18)
		print 'Target: {0} {1} {2}'.format(self.targetRealX,self.targetRealY,self.targetRealZ)
		target = PARTITION[xPartition][yPartition]
		return target

	def isHit(self,state):
		print state
		if self.isSim==True:
			return self.matlabEng.detectCollision(state.base,state.arm,self.targetRealX,self.targetRealY,self.targetRealZ)
		else:
			while (1):
				ans = input('Enter 1 if target was hit else enter 0')
				ans = int(ans)
				if ( (ans==0) or (ans ==1)):
					return ans
				else:
					print 'Invalid input.'

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
			if self.isSim==True:
				if self.isHit(state):
					#The target was hit
					newState.fire= 1 	
				else:
					#missed the target
					newState.fire=0
			else:
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

	'''
	The format for ssc32 commands is #<channel><command type><arguement>
	In this case moving the servo to a new position requires command type P and arguement of PWM
	ex: #0P1500 -> move servo on ch:0 to position 1500 i.e. center position
	'''
	def getSSC32Command(self,state,action):
		if( (action=='up') or (action == 'down')):
			pwm = radian2Pwm(state.arm)
			#arm servo is on channel 1
			return '#1P{0}'.format(pwm)
		elif( (action=='left') or (action == 'right')):
			pwm = radian2Pwm(state.base)
			#base servo is on channel 0
			return '#0P{0}'.format(pwm)
		else:
			#should really throw an error
			print 'ERROR: Command not supported or bad format.'

	def executePhysicalAction(self,state,action):
		newState = copy.copy(state)
		#Not sure if I should get the state from software or query the servo controller
		newState = self.executeVirtualAction(newState,action)
		if(action== 'fire'):
			self.ssc32.executeSingleCommand('#7H')
			time.sleep(1)
			newState.fire=self.isHit(newState)
			self.ssc32.executeSingleCommand('#7L')
			time.sleep(1)
		else:
			command = self.getSSC32Command(newState,action)
			time.sleep(0.1)
			self.ssc32.executeSingleCommand(command)
		return newState

	def executeAction(self,state, action):
		if self.isSim == 1:
			return self.executeVirtualAction(state,action)
		else:
			return self.executePhysicalAction(state,action)

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
agent.qLearning(10)

#TO DO
'''
put qtable in a diffrent file, should change the data structure eventually
BEGIN TESTING!!!!!!

Not sure if the below thing needs to be done???
Map targets actual position to pixels
		focalD = 25;
		Projected = [1,0,0,0;0,1,0,0;0,0,-1/focalD,0]*targets(1)
'''