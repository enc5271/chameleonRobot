class State:
	def __init__(self, base1,arm1,fire1,target):
		self.base = base1
		self.arm = arm1
		# Fire is not actually a state but an easy way to denote if the target was hit
		self.fire = fire1
		self.target = target
		
	def __str__(self):
		return "({0},{1},{2},{3})".format(self.base,self.arm,self.fire,self.target)
