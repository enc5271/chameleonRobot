import qAgent
import json
import os
import matplotlib.pyplot as plt

class Experiment:
	def __init__(self):
		self.filepath = './ExperimentData/'
		if os.listdir(self.filepath)==[]:
			self.initMetaData()
			self.saveExperimentData()
		else:
			self.loadExperimentData()
		self.agent = qAgent.QAgent(True,'balanced')



	def initNewExperiment(self):
		qAgent.QTable.QTable()
		self.initMetaData()

	def initMetaData(self):
		self.episodeCount = 0
		self.metaData = {'episodeCount':self.episodeCount}
		self.episodeData = []

	def appendEpisodeData(self,reward,iterations):
		episodenum = len(self.episodeData)
		self.episodeData.append({'episode':episodenum, 'cumulativeReward':reward, 'iterations':iterations})

	def runEpisode(self, maxIter):
		cumulativeReward,iterations = self.agent.qLearning(maxIter)
		self.appendEpisodeData(cumulativeReward,iterations)

	def runExperiment(self,maxIter,numEpisodes):
		for i in range(numEpisodes):
			print 'Episode',i
			self.runEpisode(maxIter)
		self.saveExperimentData()

	def loadExperimentData(self):
		with open(self.filepath+'metaData.json','r') as f:
			self.metaData = json.load(f)

		with open(self.filepath+'episodes.json','r') as f:
			self.episodeData = json.load(f)

	def saveExperimentData(self):
		with open(self.filepath+'metaData.json','w') as f:
			json.dump(self.metaData,f)

		with open(self.filepath+'episodes.json','w') as f:
			json.dump(self.episodeData,f)
	#show total reward for each episode.
	def experimentVisualizations(self):
		#print self.episodeData
		x = []
		y = []
		totalReward = 0.0
		for index, episode in enumerate(self.episodeData):
			print episode['cumulativeReward']
			x.append(index)
			episodicReward = episode['cumulativeReward']
			totalReward = totalReward + episodicReward
			y.append(totalReward)
		#episodeNumber = self.episodeData[:,0]
		#reward = self.episodeData[:,1]

		fig = plt.figure()
		plt.plot(x, y)
		plt.title('Total Reward over Time')
		plt.xlabel('Episodes Seen')
		plt.ylabel('Total Reward')
		plt.show()

#handles command line arguements.
def main():
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

def run():
	exp = Experiment()
	exp.runExperiment(20,10000)
	exp.experimentVisualizations()

if __name__ == '__main__':
	#uncomment after running tests
	#main()
	run()