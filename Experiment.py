import qAgent
import json
import os
import matplotlib.pyplot as plt
from SimulationEnvironment import SimulationEnvironment
from PhysicalEnvironment import PhysicalEnvironment

class Experiment:
	def __init__(self,isSimulation):
		self.filepath = './ExperimentData/'
		#if no data in ExperimentData create new Qtable and metadata
		if os.listdir(self.filepath)==[]:
			self.initMetaData()
			self.saveExperimentData()
		else:
			self.loadExperimentData()
		#Initialize experiment parameters from the config file.
		self.loadExperimentParameters()
		#create a simulation or physical environment class
		if isSimulation:
			self.environment = SimulationEnvironment(self.NUM_PARTITIONS)
		else:
			self.environment = PhysicalEnvironment(self.NUM_PARTITIONS)
		#create agent type
		self.agent = qAgent.QAgent(True,'balanced')

	#reads from config file './ExperimentData/config.json'. This determines the actions,
	# the number of partitions, and the constraints on servo angles.
	def loadExperimentParameters(self):
		with open(self.filepath+'config.json','r') as f:
			parameters = json.load(f)
			self.ACTIONS = parameters['Experiment']['actions']
			self.BASE_MIN = parameters['Experiment']['base_min']
			self.BASE_MAX = parameters['Experiment']['base_max']
			self.ARM_MIN = parameters['Experiment']['arm_min']
			self.ARM_MAX = parameters['Experiment']['arm_max']
			self.NUM_PARTITIONS = parameters['Experiment']['partitions']
	#creates a new qtable, episodedata, and metadata files.
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

	def learn(self,state):
		action = self.agent.selectAction(state)
		#This returns a new state as a result of taking the given action.
		outcomeState,_ = self.environment.executeAction(state,action)
		#reward the new state. actions must be passed to evaluate striking rewards.
		reward = self.environment.getReward(outcomeState,action)
		#Used to measure convergence to optimal policy.
		cumulativeReward = cumulativeReward+reward
		#increment frequency, and update qvalues
		self.agent.update(state,action,reward)
		return outcomeState
	def runEpisode(self, maxIter):
		#This only allows for a stationary target seeded at the beginning of an episode. 
		target = self.environment.getTarget()
		state = self.agent.getRandomState(target)
		print state
		i=0
		cumulativeReward=0
		for i in range(maxIter):
			state=self.learn(state)
		self.appendEpisodeData(cumulativeReward,i)

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
	exp = Experiment(True)
	exp.runExperiment(20,1)
	exp.experimentVisualizations()

if __name__ == '__main__':
	#uncomment after running tests
	#main()
	run()