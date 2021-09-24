"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (HLR)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to be optimally solvable
by reaching the Upper Bound.
"""

from DataDelivery import DataDelivery, upperBound
from DDLP_Random import randomRobotGenerator
from DensityPlot_EDL import plotLayout, parseArgs
from DDLP_ReverseHeuristic import reverseHeuristic
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from random import shuffle

__author__ = 'Caleb Andrade'

#******************************************************************************
# SIMULATION
#******************************************************************************

def densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, plot_name, reverse = True, hyperbole = True):
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
	trials: for each pair (n,r), trials refers to the number of random instances generated with (n,r)
	reverse: interchanges white with black in the plot
	hyperbole: displays the hyperbole r = 6/n
	plot_name: to distinguish file naming.
	"""

	robots_range = max_number_robots - min_number_robots
	rows = cols = robots_range
	source = epsilon
	target = width - epsilon
	z = np.empty((rows, cols), float)

	for i in range(rows):
		radius = min_radius + (i+1)*float(max_radius)/rows
		print "********************************* number of robots ********************************************** ", i+1
		for j in range(cols):
			z[i][j] = experiment(source, target, width, radius, j + min_number_robots, trials)

	plotLayout(z, width, min_radius, max_radius, min_number_robots, max_number_robots, trials, plot_name, reverse, hyperbole)


def experiment(source, target, width, radius, n, trials):
	"""
	Experiment
	"""
	
	robots = randomRobotGenerator(width, radius, n)
	upper_bound = float(upperBound(robots))

	for i in range(n):

		index = n-i
		target = (index*upper_bound)/n		
		certificate, targets = reverseHeuristic(robots, 'hlr', radius, target)

		if len(certificate) > 0:
			return float(index)/n
			
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
	trials = int(args.infile6)
	epsilon = float(args.infile7)

	densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, 'HLR_OPT', hyperbole = False)

	
if __name__ == '__main__':	
	main() 