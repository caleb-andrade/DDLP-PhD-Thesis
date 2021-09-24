"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (EDL)

This code is a graphic visualization of the empirical probability of a
randomly generated instance, with parameters (n,r), to be solvable.
"""

from DataDelivery import dataTriangle, DataDelivery
from DDLP_Random import randomRobotGenerator
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm
from random import shuffle

__author__ = 'Caleb Andrade'

# Global variables
NODES_EXPLORED = 0
LIMIT = float('inf')

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def leftTriangleStrategy(ddlp_instance, robots_available, robots_index):
	"""
	Returns a certificate with the left triangle strategy.
	"""
	certificate = []
	data = ddlp_instance.data()
	boolean = True
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

	return certificate, data, robots


def recursiveDDLP(ddlp_instance, certificate, target, robots_available):
	"""
	Recursively applies DFS to build a certificate for ddlp instance.
	"""

	global LIMIT, NODES_EXPLORED

	data = ddlp_instance.data()
	robots_index = ddlp_instance.robotsList()
	
	# Node counting
	NODES_EXPLORED += 1

	# Check if number of NODES surpases the LIMIT
	if NODES_EXPLORED > LIMIT:
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

			certificate = recursiveDDLP(ddlp_instance, certificate, target, robots_copy)

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
	z = np.empty((rows, cols))

	for i in range(rows):
		radius = min_radius + (i+1)*float(max_radius)/rows
		print "********************************* number of robots ********************************************** ", i+1
		for j in range(cols):
			z[i][j] = experiment(source, target, width, radius, j + min_number_robots, trials)

	plotLayout(z, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, plot_name, reverse, hyperbole)


def plotLayout(z, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, plot_name, reverse, hyperbole):
	"""
	Formatting plot.
	"""
	
	robots_range = max_number_robots - min_number_robots
	rows = cols = robots_range
	font = {'fontname':'Times New Roman', 'size':'16'}
	
	# Creating plot
	f = plt.figure()
	# "points" is the partition to compute values to aproximate a curve's plot
	points = np.arange(min_number_robots + 1, max_number_robots, robots_range/1000.0)
	plt.plot(points, 1*np.reciprocal(points)*np.log(points),'red', linestyle = 'dashdot', linewidth = 2.5)
	plt.plot(points, 2*np.reciprocal(points)*np.log(points),'blue', linestyle = 'dashed', linewidth = 2.5)
	if hyperbole:
		plt.plot(points, 6*np.reciprocal(points),'green', linewidth = 2.5)
	plt.xlabel('Robots', **font)
	plt.ylabel('Valor de r', **font)
	plt.title(plot_name + '   Ensayos: '+ str(trials) + '   s = ' + str(epsilon)+ '  t = ' + str(width - epsilon), **font)
	# to plot rainbow colors use: cmap=cm.gist_rainbow)
	if reverse:
		plt.imshow(z, origin='lower', extent=(min_number_robots, max_number_robots, min_radius, max_radius), aspect = 'auto', interpolation='nearest', cmap=cm.binary_r)
	else:
		plt.imshow(z, origin='lower', extent=(min_number_robots, max_number_robots, min_radius, max_radius), aspect = 'auto', interpolation='nearest', cmap=cm.binary)

	cbar = plt.colorbar()
	cbar.set_label(label='Probabilidad', family='Times New Roman', size = 16)
	cbar.set_ticks([0, trials])
	cbar.set_ticklabels(['0','1'])
	plt.show()
	f.savefig('width='+str(width)+' max_radius='+str(max_radius)+' max_n='+str(max_number_robots)+' trials='+str(trials)+' rows='+str(rows)+' cols='+str(cols)+'_'+plot_name+'.pdf', bbox_inches='tight')
	

def parseArgs():
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument('infile1', help = 'width')
		parser.add_argument('infile2', help = 'min_radius')
		parser.add_argument('infile3', help = 'max_radius')
		parser.add_argument('infile4', help = 'min_number_robots')
		parser.add_argument('infile5', help = 'max_number_robots')
		parser.add_argument('infile6', help = 'trials')
		parser.add_argument('infile7', help = 'epsilon')
		
		return parser.parse_args()

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
		global NODES_EXPLORED
		NODES_EXPLORED = 0
		certificate = recursiveDDLP(ddlp_instance, [], target, robots)

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

	densityPlot(experiment, width, epsilon, min_radius, max_radius, min_number_robots, max_number_robots, trials, 'EDL')

	
if __name__ == '__main__':	
	main() 





