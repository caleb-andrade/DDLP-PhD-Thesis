"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (EDL)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to be solvable in
k random samples.
"""

from DataDelivery import dataTriangle, DataDelivery
from DensityPlot_EDL import plotLayout, densityPlot
from DDLP_Random import randomRobotGenerator
from DDLP_Heuristic import greedyHeuristic
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from random import shuffle

__author__ = 'Caleb Andrade'

# Global variables
LEAVES = 0

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def recursiveDDLP(ddlp_instance, certificate, target, robots_available):
	"""
	Recursively applies DFS to build a certificate for ddlp instance.
	"""

	global LEAVES

	data = ddlp_instance.data()
	robots_index = ddlp_instance.robotsList()
	
	# Check if target has been reached, output current certificate
	if data >= target:
		# The last is an affirmative leaf
		LEAVES += 1
		return certificate
	
	# Otherwise, continue searching
	else:
		left_triangle, right_triangle = dataTriangle(data, robots_available)
		active_robots = left_triangle + right_triangle
		shuffle(active_robots)

		if len(active_robots) == 0:
			# This is a negative leaf
			LEAVES += 1

		# Explore children with recursion
		for robot in active_robots:
			robots_copy = list(robots_available)
			ddlp_instance.move(robot)
			index = robots_index.index(robot)
			certificate.append(index)
			robots_copy.remove(robot)

			certificate = recursiveDDLP(ddlp_instance, certificate, target, robots_copy)

			if ddlp_instance.data() >= target:
				return certificate

			else:
				# Undo changes in ddlp_instance
				ddlp_instance.data_position = data
				ddlp_instance.empty_energy[robot] = False
				certificate.pop()

	return certificate


def parseArgs():
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument('infile1', help = 'width')
		parser.add_argument('infile2', help = 'min_radius')
		parser.add_argument('infile3', help = 'max_radius')
		parser.add_argument('infile4', help = 'min_number_robots')
		parser.add_argument('infile5', help = 'max_number_robots')
		parser.add_argument('infile6', help = 'epsilon')
		
		return parser.parse_args()

#******************************************************************************
# SIMULATION
#******************************************************************************

def experiment_1(source, target, width, radius, n, trials):
	"""
	Experiment
	"""
	
	robots = randomRobotGenerator(width, radius, n)
	ddlp_instance = DataDelivery(robots, data = source)
	global LEAVES
	LEAVES = 0
	certificate = recursiveDDLP(ddlp_instance, [], target, robots)
	if len(certificate) > 0:
		return 1.0/float(LEAVES)
	return 0.0


def experiment_2(source, target, width, radius, n, trials):
	"""
	Experiment
	"""

	leaf = 0
	robots = randomRobotGenerator(width, radius, n)
	ddlp_instance = DataDelivery(robots, data = source)

	for i in range(100):	
		leaf += 1
		certificate, data = greedyHeuristic(ddlp_instance, 'random_sampling')
		if data < target:
			certificate = []
		
		if len(certificate) > 0:
			return 1.0/float(leaf)
	return 0.0


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
	epsilon = float(args.infile6)

	densityPlot(experiment_1, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, 1, 'Leaf_percentage_BT', hyperbole = False)
	densityPlot(experiment_2, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, 1, 'Leaf_percentage_RS', hyperbole = False)
	
if __name__ == '__main__':	
	main() 





