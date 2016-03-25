import math

# Use when having a more detailed discretization
#ACTION_BANK = ['base_10', 'base_-10', 'arm_10', 'arm_-10', 'fire']
ACTION_BANK = ['left', 'right', 'up', 'down', 'fire']
numPartitions = 9

#These definitions are also defined in Turret.py
BASE_MIN = 0.837758
BASE_MAX = 2.3
ARM_MIN = 1.0
ARM_MAX = 2.1416
DELTA_BASE = round((BASE_MAX-BASE_MIN)/math.sqrt(numPartitions),5)
DELTA_ARM = round((ARM_MAX-ARM_MIN)/math.sqrt(numPartitions),5)



increment = math.pi/180 
#code for more complicated physical agent states
baseList = [round(x*DELTA_BASE+BASE_MIN+0.5*DELTA_BASE,5) for x in range(int(math.sqrt(numPartitions)))]
armList = [round(x*DELTA_ARM+ARM_MIN+0.5*DELTA_ARM,5) for x in range(int(math.sqrt(numPartitions)))]

# Only works for 2x2 space partition
#baseList = [BASE_MIN,BASE_MAX]
#armList = [ARM_MIN,ARM_MAX]

filename = 'QTable.csv'
f = open(filename,'w')
for base in baseList:
	for arm in armList:
		for target in range(0,numPartitions):
			for action in ACTION_BANK:
				row = "{0},{1},{2},{3},{4},{5}\n".format(base,arm,target,action,'0','0')
				f.write(row)
f.close()