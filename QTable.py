import csv
import math
import pandas as pd
from State import State

ACTION_BANK = ['left', 'right', 'up', 'down', 'fire']
#These definitions are also defined in qAgent.py
BASE_MIN = 0.837758
BASE_MAX = 2.3
ARM_MIN = 1.0
ARM_MAX = 2.1416

numPartitions = 25

partitionServoangle=(BASE_MAX-BASE_MIN)/math.sqrt(numPartitions)
DELTA_BASE = round(partitionServoangle,5)
DELTA_ARM = round((ARM_MAX-ARM_MIN)/math.sqrt(numPartitions),5)

increment = math.pi/180 
#Create servo position list for base and arm 
baseList = [round(x*DELTA_BASE+BASE_MIN+0.5*DELTA_BASE,5) for x in range(int(math.sqrt(numPartitions)))]
armList = [round(x*DELTA_ARM+ARM_MIN+0.5*DELTA_ARM,5) for x in range(int(math.sqrt(numPartitions)))]


class QTable():
	def __init__(self,filename=''):
		if filename == '':
			print 'Creating new QTable.'
			#numPartitions=int(raw_input('How many partitions?'))
			self.createNewTable(numPartitions)
			self.writeTable()
		else:
			self.qtable=pd.read_csv(filename)
			self.baseHashTable = {str(base): counter for counter,base in enumerate(baseList)}		
			self.armHashTable = {str(arm): counter for counter,arm in enumerate(armList)}


	def createNewTable(self, numPartitions):
		#assign each servo position an index. Used for state hashcode.
		self.baseHashTable = {str(base): counter for counter,base in enumerate(baseList)}		
		self.armHashTable = {str(arm): counter for counter,arm in enumerate(armList)}

		filename = 'QTable.csv'
		#names for each field in qtable.csv
		columnNames=['base','arm','target','action','hashcode','qvalue','frequency']
		#This is a temporary 2d list to convert to a pandas dataFrame.
		pythonList = []
		#Both counters are being used to create a hashcode for each state. 
		#Hashcode: base_arm_target
		for baseCounter, base in enumerate(baseList):
			for armCounter, arm in enumerate(armList):
				for target in range(0,numPartitions):
					for action in ACTION_BANK:
						stateHashCode = '{0}_{1}_{2}'.format(baseCounter,armCounter,target)
						row = [base,arm,target,action,stateHashCode,'0','0']
						pythonList.append(row)
		self.qtable = pd.DataFrame(pythonList, columns=columnNames)

	def writeTable(self,filename='QTable.csv'):
		#Write QTable from memory to 'QTable.csv' in current directory.
		self.qtable.to_csv(filename,index=False)

	def getStateHashCode(self, state):
		baseHash = self.baseHashTable[str(state.base)]
		armHash = self.armHashTable[str(state.arm)]
		hashcode = '{0}_{1}_{2}'.format(baseHash,armHash,state.target)
		return hashcode

	def getQValue(self,state,action1):
		hashcode = self.getStateHashCode(state)
		#get the corresponding state in the qtable.Returns the entire row.
		qRow = self.qtable[(self.qtable['hashcode']==hashcode) & (self.qtable['action']==action1)]
		if qRow.empty:
			print 'ERROR: In getQValue Table entry not found.'
		else:
			return qRow['qvalue'].item()
		
	def setQValue(self,state,action1,newQValue):
		hashcode = self.getStateHashCode(state)
		qRow = self.qtable[(self.qtable['hashcode']==hashcode) & (self.qtable['action']==action1)]
		if qRow.empty:
			print 'ERROR: In setQValue, Table entry not Found.'
		else:
			self.qtable.set_value(qRow.index, 'qvalue',newQValue)
			qRow['qvalue']=newQValue

	def getFreq(self,state,action1):
		hashcode = self.getStateHashCode(state)
		qRow = self.qtable[self.qtable['hashcode']==hashcode 
			& self.qtable['action']==action1]
		if qRow.empty:
			print 'ERROR: In getFreq Table entry not Found.'
		else:
			return qRow['frequency'].item()

	def getRandomState(self, target=None):
		if target ==None:
			qRow = self.qtable.sample(n=1)
			return State(qRow.base,qRow.arm,0,qRow.target)
		else:
			qRow =self.qtable[self.qtable['target']==target]
			randRow = qRow.sample(n=1)
			return State(randRow.base.item(), randRow.arm.item(),0, randRow.target.item())
	def incrementFreq(self,state,action1):
		hashcode = self.getStateHashCode(state)
		qRow = self.qtable[(self.qtable['hashcode']==hashcode) & (self.qtable['action']==action1)]
		if qRow.empty:
			print 'ERROR: In incrementFreq Table entry not Found.'
		else:
			#self.qtable.loc[qRow.index,'frequency'] = 1
			self.qtable.set_value(qRow.index, 'frequency',(qRow['frequency']+1))

	#Return the action with the maximum q value.
	def getMaxAction(self,state):
		hashcode = self.getStateHashCode(state)
		qRow = self.qtable[self.qtable['hashcode'] == hashcode]
		maxQ = qRow.ix[qRow.qvalue.idxmax()]
		return maxQ.action

	#Returns the state-action pair with the max q value.
	def getMaxQ(self,state):
		hashcode = self.getStateHashCode(state)
		qRow = self.qtable[self.qtable['hashcode'] == hashcode]
		maxQ = qRow.ix[qRow.qvalue.idxmax()]
		if not(maxQ.empty):
			return maxQ.action,maxQ.qvalue
		else:
			print "This case should never happen, and is only left here for debugging. Remove me before program is shipped out!"
			return -1000	#IMPORTANT - What should be done in the case that this state has not been visited
	
	def getStats(self):
		print self.qtable.describe()


if __name__=='__main__':
	table = QTable('QTable.csv')
	#table.getStats()
	print table.qtable.head()