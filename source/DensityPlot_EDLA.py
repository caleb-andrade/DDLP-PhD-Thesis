"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (EDLA)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to be solvable.
"""

from DataDelivery import dataTriangle, DataDelivery
from DDLP_Random import randomRobotGenerator
from DensityPlot_EDL import densityPlot, parseArgs
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm

__author__ = 'Caleb Andrade'

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def polinomialEDLA(ddlp_instance, robots_available, target):
	"""
	Returns a certificate with the left triangle strategy.
	"""
	certificate = []
	data = ddlp_instance.data()
	boolean = True
	robots_index = ddlp_instance.robotsList()
	robots = list(robots_available)

	while boolean:
		# select robots in the triangle
		left_triangle, right_triangle = dataTriangle(data, robots)
		
		
		if len(left_triangle) > 0:
			robot = left_triangle[0]
		else:
			boolean = False
			break
		
		index = robots_index.index(robot)
		certificate.append(index)
		ddlp_instance.move(robot)
		data = ddlp_instance.data()
		robots.remove(robot)

	if ddlp_instance.data() < target:
		certificate = []

	return certificate

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
		ddlp_instance = DataDelivery(robots, data = source)
		certificate = polinomialEDLA(ddlp_instance, robots, target)

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

	densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, 'EDLA')

	
if __name__ == '__main__':	
	main() 





