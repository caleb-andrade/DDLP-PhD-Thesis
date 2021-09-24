"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (DDLP)

This code contains a class to represent DDLP instances.

robots = mobile agents

DDLPD (decision version): given n robots with positions x_i and energies y_i, 
find a certificate for the n robots to deliver the data from source 
s to target t.

DDLPO (optimization version): given n robots with positions x_i and energies y_i, 
find a certificate for the n robots to deliver the data from source 
s to the farthest right.

Created: February 26th 2018
Last update: January 4th 2019
"""

__author__ = 'Caleb Andrade'

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def readFile(filename):
	""" 
	Reads robots file in csv format.
	"""
	
	robots = []
	with open(filename) as f:
		while True:
			line = f.readline()
			if line == '':
				break
			row = line.split(',')
			robots.append((float(row[0]), float(row[1])))
	
	print "\nLoaded", len(robots), "robots"

	# sort robots with respect to x_i - rho_i
	robots.sort(key = lambda robot: robot[0] - robot[1])
	
	return robots


def objectiveValue(ddlp_instance, certificate):
	"""
	Computes maximum reach of the data for a given certificate in the DDLPO.
	"""

	ddlp_instance.moveRobots(certificate)
	value = ddlp_instance.data()
	ddlp_instance.reset()

	return value


def upperBound(robots):
	"""
	Computes the upper bound for a ddlp instance.
	"""

	if len(robots) > 0:

		return max([robot[0] + robot[1] for robot in robots])

	else:

		return 0


def dataTriangle(data, robots):
	"""
	Returns two lists, those robots in the active region's right triangle,
	and those robots in the active region's left triangle.
	Takes as input data position, and a list of robots sorted by x_i - rho_i
	It mutates robots by removing useless robots.
	"""
	
	left_triangle = []
	right_triangle = []
	copy_robots = list(robots)

	for robot in copy_robots:
		# if robot is useless, remove it.
		if robot[0] + robot[1] <= data:
			robots.remove(robot)
		else:
			# if robot is in active region to the left of data
			if robot[0] <= data:
				left_triangle.append(robot)
			else:
				# if robot is to the right of data and is active
				if robot[0] - robot[1] < data:
					right_triangle.append(robot)
				else:
					# robot is to to the right but is inactive so the rest in the list
					break

	return left_triangle, right_triangle

#******************************************************************************
# DDLP CLASS
#******************************************************************************

class DataDelivery:
	"""
	Class to represent a DDLP instance.
	"""

	def __init__(self, robots, data = 0.0, energy = None):
		""" 
		Creates a DDLP instance.
		Input: a list of robots (x_i, y_i), data position, energy consumption.
		"""

		self.robots = list(robots)
		self.data_position = data
		self.original_data = data
		# the following dictionary is to keep track of energy consumption
		if energy == None:
			self.empty_energy = {robot:False for robot in self.robots}
		else:
			self.empty_energy = energy.copy()


	def __str__(self):
		"""
		String representation.
		"""

		string = ""
		for i in range(len(self.robots)):
			string += "\nRobot " + str(i) + ": " + str(self.robots[i]) + " Empty energy: " + str(self.empty_energy[self.robots[i]])
		
		return string

	
	def robotsList(self):
		"""
		Returns list of robots.
		"""

		return list(self.robots)

	
	def move(self, robot):
		"""
		Moves robot towards data and then to the farthest right.
		"""

		# check if robot has enough energy to reach the data
		distance = abs(self.data_position - robot[0])
		if distance < robot[1] and not self.empty_energy[robot]:
			real_energy = robot[1] - distance
			self.data_position = self.data() + real_energy
			self.empty_energy[robot] = True

	
	def moveRobots(self, certificate):
		"""
		Given a certificate of robots, move robots in such order.
		"""

		if len(certificate) > 0:
			for robot in certificate:
				self.move(robot)
		else:
			pass


	def data(self):
		"""
		Returns data's position.
		"""

		return self.data_position


	def reset(self):
		"""
		Resets data's position and robots' energies.
		"""

		self.data_position = self.original_data
		self.empty_energy = {robot:False for robot in self.robots}


	def copy(self):
		"""
		Returns a duplicate of this ddlp instance object.
		"""
		return DataDelivery(self.robots, data = self.data_position, energy = self.empty_energy)
	
#******************************************************************************
# TESTING
#******************************************************************************

def main():
	"""
	Input: List of robots in csv format followed by a permutation as string.
	"""

	args = parse_args()    
	robots = readFile(args.infile1)
	certificate = [int(digit) for digit in str(args.infile2)]
	
	#Testing examples for debugging
	ddlp_instance = DataDelivery(robots)
	print ddlp_instance
	robots = ddlp_instance.robotsList()
	
	for i in certificate:
		print "\nRobot: ", robots[i]
		ddlp_instance.move(robots[i])
		print "data's new position: ", ddlp_instance.data()

	print "\nReset"
	ddlp_instance.reset()
	ddlp_instance.moveRobots(certificate)
	print "data's final position: ", ddlp_instance.data()


def parse_args():
	"""
	Parsing arguments.
	"""

	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('infile1', help ='robots list')
	parser.add_argument('infile2', help ='certificate')
	
	return parser.parse_args()


if __name__ == '__main__':
	main() 