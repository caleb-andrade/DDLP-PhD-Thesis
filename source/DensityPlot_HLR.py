"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (HLR)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to be solvable.
"""

from DataDelivery import DataDelivery
from DDLP_Random import randomRobotGenerator
from DensityPlot_EDL import densityPlot, parseArgs
from DDLP_ReverseHeuristic import reverseHeuristic
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from random import shuffle

__author__ = 'Caleb Andrade'

#******************************************************************************
# SIMULATION
#******************************************************************************

def experiment(source, target, width, radius, n, trials):
	"""
	Experiment
	"""
	yes_instances = 0

	for i in range(trials):

		robots = randomRobotGenerator(width, radius, n)
		certificate, targets = reverseHeuristic(robots, 'hlr', radius, target)

		if len(certificate) > 0:
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

	densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, 'HLR', hyperbole = False)

	
if __name__ == '__main__':	
	main() 