"""
This module deals with the generation of random instances of DDLP

Created: 
Last update: February 25th 2021
"""

__author__ = 'Caleb Andrade'

import random
import math

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def randomRobotGenerator(width, radius, number_robots):
	"""
	Generates number_robots robots with uniform distribution in a rectangle
	of size width x radius. 
	Output: sorted list of robots with respect to x_i - rho_i
	"""
		
	robots = []
	for index in range(number_robots):
		position = width*(random.random())
		energy = radius*(random.random())
		robots.append((position, energy))

	# sort robots with respect to x_i - rho_i
	robots.sort(key = lambda robot: robot[0] - robot[1])

	return robots


def robotDisplacement(ddlp_instance, certificate, radius):
	"""
	Computes robot displacement as a percentage of r (radius).
	"""

	displacements = []
	positions = [ddlp_instance.data()]
	robots = ddlp_instance.robotsList()

	# Sanity check
	if len(certificate) == 0:
		return displacements

	for i in certificate:
		ddlp_instance.move(robots[i])
		new_position = ddlp_instance.data()
		displacement = new_position - positions[-1]
		displacements.append(round(displacement / radius, 2))
		positions.append(new_position)

	ddlp_instance.reset()

	return displacements


def variance(data, ddof=0):
	n = len(data)
	mean = sum(data) / float(n)
	return sum((x - mean) ** 2 for x in data) / (n - ddof)


def stdev(data):
	var = variance(data)
	std_dev = math.sqrt(var)
	return std_dev