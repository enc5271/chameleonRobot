from abc import ABCMeta, abstractmethod

class Environment:
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		raise NotImplementedError()

	@abstractmethod
	def getTarget(self):
		raise NotImplementedError()

	@abstractmethod
	def isHit(self):
		raise NotImplementedError()

	@abstractmethod
	def getReward(self):
		raise NotImplementedError()

	@abstractmethod
	def executeAction(self):
		raise NotImplementedError()
	




