import csv

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
		csvfile.close()

	def writeTable(self,filename='QTable.csv'):
		#Write QTable from memory to 'QTable.csv' in current directory.
		with open(filename,'wb') as csvfile:
			for row in self.qtable:
				csvfile.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
		csvfile.close()

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