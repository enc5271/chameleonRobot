from Environment import Environment
import detectCollision

class PhysicalEnvironment(Environment):
	def __init__(self,partitions):
		self.NUM_PARTITIONS = partitions

	def getTarget(self):
		#This is dependent on the camera
		imgHeight = 480
		imgWidth = 640
		
		hashX = x/(imgWidth/self.NUM_PARTITIONS)
		hashY = y/(imgHeight/self.NUM_PARTITIONS)
		print x,y
		print hashX,hashY
		# FIX - partition = xhash+yhash*5
		target = hashX+hashY*self.NUM_PARTITIONS
		return target

	
	def isHit(self):
		while (1):
			ans = input('Enter 1 if target was hit else enter 0:\n')
			ans = int(ans)
			if ( (ans==0) or (ans ==1)):
				return ans
			else:
				print 'Invalid input.'

	
	def getReward(self,state,action,dist):
		if action == 'fire' and state.fire==1:
			return (1/dist)*1000
		else:
			return -1
	
	def radian2Pwm(self,rad):
		pwm = 600 + rad*(1800/math.pi)
		return pwm

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

	#This method relies on the simulator to get the next state. This should be changed but idk how.
	def executeAction(self,state,action):
		newState = copy.copy(state)
		#Not sure if I should get the state from software or query the servo controller
		(newState,_) = self.executeVirtualAction(newState,action)
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
