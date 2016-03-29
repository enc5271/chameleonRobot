import csv
import matplotlib.pyplot as pyplot

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
				row[3] = row[3]
				row[4] = float(row[4])
				row[5] = int(row[5])
				self.qtable.append(row)
		csvfile.close()

	def writeTable(self,filename='QTable.csv'):
		#Write QTable from memory to 'QTable.csv' in current directory.
		with open(filename,'wb') as csvfile:
			for row in self.qtable:
				csvfile.write('{0},{1},{2},{3},{4},{5}\n'.format(row[0],row[1],row[2],row[3],row[4],row[5]))
		csvfile.close()

	def getQValue(self,state,action1):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.target:
						if row[3]==action1:
							return row[4]
		print 'ERROR: In getQValue Table entry not found.'
		
	def setQValue(self,state,action1,newReward):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.target:
						if row[3]==action1:
							row[4] = newReward
							row[5] = row[5] + 1
							return
		print 'ERROR: In setQValue Table entry not Found.'

	def getFreq(self,state,action1):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.target:
						if row[3]==action1:
							return row[5]
		print 'ERROR: In getFreq Table entry not Found.'

	def incrementFreq(self,state,action1):
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.target:
						if row[3]==action1:
							row[5] = row[5]+1
							return
		print 'ERROR: In incrementFreq Table entry not Found.'

	def getQActionPairs(self,state):
		qvalues = []
		#print "The state in getQActionPairs:"
		#print state
		for row in self.qtable:
			if row[0]==state.base:
				if row[1]==state.arm:
					if row[2]==state.target:
						qvalues.append([row[3],row[4]])
		if len(qvalues)==0:
			print 'ERROR: In getQActionPairs Table entry not Found.'
		return qvalues			 

	def getMaxQ(self,state):
		pairs = self.getQActionPairs(state)
		#print pairs
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
	
	def getStats(self):
		for row in self.qtable:
			if row[4] >0:
				print row
		(action, state) = (None, None)
		Max = float('-inf') 
		for i in range (0,len(self.qtable)):
			row = self.qtable[i]
			Q = row[4]
			if Q > Max:
				Max = Q
				action = row[3]
				state = row[0],row[1],row[2]
			if (i+1) % 5 == 0:
				print 'State: {0} \nAction: {1}\nQ: {2}\n'.format(state,action,Q)
				(action, state) = (None, None)
				Max = float('-inf')


if __name__=='__main__':
	table = QTable('QTable.csv')
	table.getStats()