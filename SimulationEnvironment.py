from Environment import Environment
import detectCollision
import random
import math
import copy

class SimulationEnvironment(Environment):
	def __init__(self,partitions):
		self.NUM_PARTITIONS=partitions

	def getTarget(self,debug=False):
		random.seed()
		self.targetRealX = random.uniform(10,50)
		self.targetRealY = random.uniform(20,40)
		self.targetRealZ = random.uniform(10,30)

		xPartition = int(math.floor(self.targetRealX / (60.0/self.NUM_PARTITIONS)))
		yPartition = int(math.floor(self.targetRealY/ (40.0/self.NUM_PARTITIONS)))
		
		#print 'Target: {0} {1} {2}'.format(self.targetRealX,self.targetRealY,self.targetRealZ)
		target = xPartition+yPartition*self.NUM_PARTITIONS
		
		if debug:
			import matplotlib.pyplot as plt
			plt.scatter(self.targetRealX,self.targetRealY)
			plt.xlim(0,60)
			plt.ylim(0,40)
			plt.grid(True)
			plt.show()
		return target

	def isHit(self,state):
		#print state
		return detectCollision.detectCollision(state.base,state.arm,self.targetRealX,self.targetRealY,self.targetRealZ,debug=False)

	def getReward(self,state,action,dist):
		if action == 'fire' and state.fire==1:
			return (1/dist)*1000
		else:
			return -1

	def executeAction(self,state,action):
		success = 0
		dist = 1
		newState = copy.copy(state)
		if action == 'fire':
			if self.isSim==True:
				(hit, dist) = self.isHit(state)
				if hit:
					#The target was hit
					newState.fire= 1 	
					print 'Target hit'
					#time.sleep(0.2)
				else:
					#missed the target
					newState.fire=0
			else:
				newState.fire = 0 	
		elif action =='up':
			delta = self.actionValues['up']
			newArm = round(newState.arm + delta,5) 
			if newArm >= ARM_MAX:
				#keep same value
				newState.arm =newState.arm
			else:
				newState.arm = newArm
				
		elif action =='down':
			delta = self.actionValues['down']
			newArm = round(newState.arm + delta,5) 
			if newArm <= ARM_MIN:
				newState.arm =newState.arm
			else:
				newState.arm=newArm
				
		elif action =='left':
			delta = self.actionValues['left']
			newBase = round(newState.base + delta,5)
			if newBase <= BASE_MIN:
				newState.base =newState.base
			else:
				newState.base = newBase
				
		elif action =='right':
			delta = self.actionValues['right']
			newBase = round(newState.base + delta,5)
			if newBase >= BASE_MAX:
				newState.base =newState.base
			else:
				newState.base = newBase
				
		else:
			print 'ERROR: Action not found.'
			return
		return (newState, dist)
