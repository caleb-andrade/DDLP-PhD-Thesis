"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (Node Counting)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to have a large number of nodes
to be explored by the Backtrack algorithm.
"""

from DataDelivery import DataDelivery, dataTriangle
from DDLP_Random import randomRobotGenerator
from DensityPlot_EDL import leftTriangleStrategy, parseArgs, densityPlot
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from random import shuffle
from math import log

__author__ = 'Caleb Andrade'

# Global variables
NODES_EXPLORED = 0

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def recursiveDDLP(ddlp_instance, certificate, target, robots_available, limit):
	"""
	Recursively applies DFS to build a certificate for ddlp instance.
	"""

	data = ddlp_instance.data()
	robots_index = ddlp_instance.robotsList()
	
	# Node counting
	global NODES_EXPLORED
	NODES_EXPLORED += 1

	# Check if number of NODES surpases the limit
	if NODES_EXPLORED > limit:
		return certificate
	
	# Check if target has been reached, output current certificate
	if data >= target:
		return certificate
	
	# Otherwise, continue searching
	else:
		# Check connected component
		idx_robots_fijos, data_max, robots = leftTriangleStrategy(ddlp_instance, robots_available, robots_index)
		certificate = certificate + idx_robots_fijos
		if ddlp_instance.data() >= target:
				return certificate
		left_triangle, right_triangle = dataTriangle(data_max, robots)
		shuffle(right_triangle)

		# Explore children with recursion
		for robot in right_triangle:
			robots_copy = list(robots)
			ddlp_instance.move(robot)
			index = robots_index.index(robot)
			certificate.append(index)
			robots_copy.remove(robot)

			certificate = recursiveDDLP(ddlp_instance, certificate, target, robots_copy, limit)

			if ddlp_instance.data() >= target:
				return certificate

			else:
				# Undo changes in ddlp_instance
				ddlp_instance.data_position = data_max
				ddlp_instance.empty_energy[robot] = False
				certificate.pop()

		# Undo changes EDLA
		for i in range(len(idx_robots_fijos)):
			idx = certificate.pop()
			ddlp_instance.empty_energy[robots_index[idx]] = False
		
		ddlp_instance.data_position = data

		
	return certificate

#******************************************************************************
# SIMULATION
#******************************************************************************

def experiment(source, target, width, radius, n, trials):
	"""
	Experiment
	"""
	yes_instances = 0
	limit = (log(100))*(3.0*width)/radius

	for i in range(trials):

		robots = randomRobotGenerator(width, radius, n)
		ddlp_instance = DataDelivery(robots, data = source)
		global NODES_EXPLORED
		NODES_EXPLORED = 0
		certificate = recursiveDDLP(ddlp_instance, [], target, robots, limit)
		if NODES_EXPLORED > limit:
			yes_instances += 1
			
	return yes_instances
	

def main():
	"""
	Main method.
	"""

	args = parseArgs()    
	width = float(args.infile1)
	min_radius = float(args.infile2)
	max_radius = float(args.infile3)
	min_number_robots = int(args.infile4)
	max_number_robots = int(args.infile5)
	trials = int(args.infile6)
	epsilon = float(args.infile7)

	densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, 'Conteo de Nodos', reverse = False, hyperbole = False)

	
if __name__ == '__main__':	
	main() 