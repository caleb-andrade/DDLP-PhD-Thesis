"""
This code is to experimentally test Scheinerman's Theorem about
the connectivity threshold for random interval graphs.
"""

from DDLP_Connectivity import IntervalGraph, simmetricIntervals
from DDLP_Random import randomRobotGenerator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from random import shuffle

__author__ = 'Caleb Andrade'


#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def experiment(width, radius, n, trials):
	"""
	Experiment
	"""
	connected_instances = 0

	for i in range(trials):

		robots = randomRobotGenerator(width, radius, n)
		intervals = simmetricIntervals(robots)
		interval_graph = IntervalGraph(intervals)

		if interval_graph.isConnected():
			connected_instances += 1
			
	return connected_instances
	

def parse_args():
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument('infile1', help = 'Width')
		parser.add_argument('infile2', help = 'min_radius')
		parser.add_argument('infile3', help = 'max_radius')
		parser.add_argument('infile4', help = 'min_number_robots')
		parser.add_argument('infile5', help = 'max_number_robots')
		parser.add_argument('infile6', help = 'Trials')
		
		return parser.parse_args()


def main():
	"""
	Main method.
	"""

	args = parse_args()    
	width = float(args.infile1)
	min_radius = float(args.infile2)
	max_radius = float(args.infile3)
	min_number_robots = int(args.infile4)
	max_number_robots = int(args.infile5)
	trials = int(args.infile6)

	robots_range = max_number_robots - min_number_robots

	rows = cols = robots_range

	z = np.empty((rows, cols), int)

	for i in range(rows):
		radius = min_radius + (i+1)*float(max_radius)/rows
		print "********************************* number of robots ********************************************** ", i+1
		for j in range(cols):
			z[i][j] = experiment(width, radius, j + min_number_robots, trials)

	# Creating plot
	font = {'fontname':'Times New Roman', 'size':'16'}
	f = plt.figure()
	points = np.arange(min_number_robots+1, max_number_robots, robots_range/1000.0)
	plt.plot(points, 1*np.reciprocal(points)*np.log(points),'red', linestyle = 'dashdot', linewidth = 2.5)
	plt.plot(points, 6*np.reciprocal(points),'green', linewidth = 2.5)
	plt.xlabel('Robots', **font)
	plt.ylabel('Valor de r', **font)
	plt.title('Scheinerman' + '   Ensayos: '+ str(trials) + '   s = ' + str(0)+ '  t = ' + str(1), **font)
	plt.imshow(z, origin='lower', extent=(min_number_robots, max_number_robots, min_radius, max_radius), aspect = 'auto', interpolation='nearest', cmap=cm.binary_r)
	cbar = plt.colorbar()
	cbar.set_label(label='Probabilidad', family='Times New Roman', size = 16)
	cbar.set_ticks([0, trials])
	cbar.set_ticklabels(['0','1'])
	plt.show()
	# Saving plot
	f.savefig('width='+str(width)+' max_radius='+str(max_radius)+' max_n='+str(max_number_robots)+' trials='+str(trials)+' rows='+str(rows)+' cols='+str(cols)+'_Scheinerman.pdf', bbox_inches='tight')

	
if __name__ == '__main__':	
	main() 





