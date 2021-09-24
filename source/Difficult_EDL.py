"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM
(Difficult instances)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to be solved by ten
different approximation algorithms and backtrack on instances presumably
difficult.
"""

from DataDelivery import DataDelivery
from DDLP_Random import randomRobotGenerator
from DensityPlot_EDL import plotLayout, parseArgs, recursiveDDLP
from DDLP_ReverseHeuristic import reverseHeuristic
from DDLP_Heuristic import greedyHeuristic
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from random import shuffle
from math import log

__author__ = 'Caleb Andrade'

# Global variables
YES_INSTANCES = 0
NO_INSTANCES = 0

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def  densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, plot_name, reverse = True, hyperbole = True, difficult = True):
	"""
	This function displays a density plot and saves it to a pdf file.
	The density is an empirical probability.
	
	Input:

	experiment: Is a function that defines what kind of experiment is to be used. It outputs the number of afirmative instances.
	width: instances' width.
	epsilon: This defines the source = epsilon, as well as the target = width - epsilon.
	min_radius: The minimum value of r to generate random instances.
	max_radius: The maximum value of r to generate random instances.
	min_number_robots: The minimum number of robots to generate random instances.
	max_number_robots: The maximum number of robots to generate random instances.
	reverse: interchanges white with black in the plot
	hyperbole: displays the hyperbole r = 6/n
	plot_name: to distinguish file naming.
	"""

	robots_range = max_number_robots - min_number_robots
	rows = cols = robots_range
	source = epsilon
	target = width - epsilon

	z = np.zeros((rows, cols), int)

	hamming_distance = {"max_x":0, "min_x":0, "max_s":0, "min_s":0, "hlr":0,'closest_robot':0, 'lowest_reach':0, 'highest_capacity':0, 'less_capacity':0, 'random_sampling':0}


	for i in range(rows):
		radius = min_radius + (i+1)*float(max_radius)/rows
		print "********************************* number of robots ********************************************** ", i+1
		for j in range(cols):
			global YES_INSTANCES
			global NO_INSTANCES
			n = j + min_number_robots

			# Difficult instances or not?
			if difficult and n > 0:
				if radius < log(n)/n or 2*log(n)/n < radius:
					continue

			temp_vector = experiment(source, target, width, radius, n)
			z[i][j] = sum(temp_vector)
			k = 0
			for heuristic_type in ["max_x", "min_x", "max_s", "min_s", "hlr",'closest_robot', 'lowest_reach', 'highest_capacity', 'less_capacity', 'random_sampling']:
				hamming_distance[heuristic_type] = hamming_distance[heuristic_type] + temp_vector[k]
				k = k + 1

	print "\nApproximation Ratio: "
	for heuristic_type in hamming_distance.keys():
		distance = hamming_distance[heuristic_type]
		ratio = 100*(1-(float(distance)/YES_INSTANCES))
		print heuristic_type, ': ', round(ratio,2), '%'

	print "\nYES_INSTANCES: ", YES_INSTANCES
	print "NO_INSTANCES: ", NO_INSTANCES

	plotLayout(z, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, 10, plot_name, reverse, hyperbole)


def xOR(certificate_1, certificate_2):
	"""
	An xOR for two certificates.
	"""

	if len(certificate_1) > 0 and len(certificate_2) == 0:
		return 1

	if len(certificate_2) > 0 and len(certificate_1) == 0:
		return 1

	return 0

#******************************************************************************
# SIMULATION
#******************************************************************************

def experiment(source, target, width, radius, n):
	"""
	Experiment
	"""

	global YES_INSTANCES
	global NO_INSTANCES
		
	# hamming distance between Aproximation Algorithms and Backtrack
	hamming_distance = [0 for i in range(10)]

	i = 0

	robots = randomRobotGenerator(width, radius, n)
	robots_1 = list(robots)
	robots_2 = list(robots)
	ddlp_instance_1 =  DataDelivery(robots_1, data = source)
	ddlp_instance_2 =  DataDelivery(robots_2, data = source)
	certificate_1 = recursiveDDLP(ddlp_instance_1, [], target, robots_1)
	if len(certificate_1) > 0:
		YES_INSTANCES = YES_INSTANCES + 1
	else:
		NO_INSTANCES = NO_INSTANCES + 1
	
	for heuristic_type in ["max_x", "min_x", "max_s", "min_s", "hlr"]:
		certificate_2, targets = reverseHeuristic(robots_2, heuristic_type, source, target)
		hamming_distance[i] = xOR(certificate_1, certificate_2)
		i = i + 1
		
	for heuristic_type in ['closest_robot', 'lowest_reach', 'highest_capacity', 'less_capacity', 'random_sampling']:
		certificate_2, data =  greedyHeuristic(ddlp_instance_2, heuristic_type)
		if data < target:
			certificate_2 = []
		hamming_distance[i] = xOR(certificate_1, certificate_2)
		i = i + 1
	
	return hamming_distance


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
	difficult = True

	densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, 'Difficult'+str(difficult), False, True, difficult)

	
if __name__ == '__main__':	
	main() 





