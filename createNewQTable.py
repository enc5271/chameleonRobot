import math

# Use when having a more detailed discretization
#ACTION_BANK = ['base_10', 'base_-10', 'arm_10', 'arm_-10', 'fire']
ACTION_BANK = ['left', 'right', 'up', 'down', 'fire']
numPartitions = 4

#These definitions are also defined in Turret.py
BASE_MIN = 0.837758
BASE_MAX = 2.3
ARM_MIN = 1.0
ARM_MAX = 2.1416

increment = math.pi/180 
#code for more complicated physical agent states
#baseList = [round(x*increment,5) for x in [45,135]]
#armList = [round(x*increment,5) for x in  [75,105]]

baseList = [BASE_MIN,BASE_MAX]
armList = [ARM_MIN,ARM_MAX]

filename = 'QTable.csv'
f = open(filename,'w')
for base in baseList:
	for arm in armList:
		for fire in range(2):
			for target in range(0,numPartitions):
				for action in ACTION_BANK:
					row = "{0},{1},{2},{3},{4},{5},{6}\n".format(base,arm,fire,target,action,'0','0')
					f.write(row)
f.close()