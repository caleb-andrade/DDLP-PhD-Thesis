"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (DDLP)

This code contains "reverse" approximation algorithms to solve DDLP.

Created: July 6th 2019
Last update: December 13th 2020
February 25th 2021
"""

import random
from DataDelivery import DataDelivery, readFile, objectiveValue, upperBound
#from DDLP_Drawing import drawHLR
from DDLP_Random import randomRobotGenerator
from Tkinter import Tk, Canvas

__author__ = 'Caleb Andrade'

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def criterion(robot_1, robot_2, value_1, value_2, criterion):
	"""
	Selects best robot depending on criterion (max or min).
	"""

	if criterion == "max":
		if value_1 >= value_2:
			return robot_1, value_1
		else:
			return robot_2, value_2

	if criterion == "min":
		if value_1 <= value_2:
			return robot_1, value_1
		else:
			return robot_2, value_2


def difference(robot, target):
	"""
	Computes the capacity that a robot has to go back to data and move it to target.
	"""
	return (robot[0] + robot[1] - target)/2.0

#******************************************************************************
# HEURISTIC
#******************************************************************************

def reverseHeuristic(robots, heuristic_type, source, target):
	"""
	Solves a DataDelivery instance constructively by selecting robots in
	reverse order, according to four different criteria.
	Returns certificate and targets.
	"""

#	print "Criterion: ", heuristic_type

	finish = False
	available_robots = list(robots)
#	print "Available robots: ", available_robots
	certificate = []
	targets = []

	while not finish:
		candidates = []
		
		for robot in available_robots:
			# We round so as to deal with floating point arithmetic error
			lower_reach = round(robot[0] - robot[1],10)
			upper_reach = round(robot[0] + robot[1],10)
			if  lower_reach < round(target,10) <= upper_reach:
				candidates.append(robot)

		if len(candidates) == 0:
#			print "No more candidates! There is no certificate!"
			return [],[]

		# Initialize values for comparison
		max_x_robot = min_x_robot = max_s_robot = min_s_robot = hlr_robot = candidates[0]
		max_x = min_x = candidates[0][0]
		max_s = min_s = difference(candidates[0], target)
		hlr = hlr_robot[0] - hlr_robot[1]

		for robot in candidates:
			s = difference(robot, target)
#			print "Candidate robot: ", robot,
#			print "S difference: ", s

			max_x_robot, max_x = criterion(max_x_robot, robot, max_x, robot[0], "max")
			min_x_robot, min_x = criterion(min_x_robot, robot, min_x, robot[0], "min")
			max_s_robot, max_s = criterion(max_s_robot, robot, max_s, s, "max")
			min_s_robot, min_s = criterion(min_s_robot, robot, min_s, s, "min")
			if robot[0] - robot[1] >= hlr:
				hlr = robot[0] - robot[1]
				hlr_robot = robot

		if heuristic_type == "max_x":
			best_robot = max_x_robot
		if heuristic_type == "min_x":
			best_robot = min_x_robot
		if heuristic_type == "max_s":
			best_robot = max_s_robot
		if heuristic_type == "min_s":
			best_robot = min_s_robot
		if heuristic_type == "hlr":
			best_robot = hlr_robot

#		print "Best robot: ",best_robot

		target = best_robot[0] - difference(best_robot, target)
		certificate.append(best_robot)
		targets.append(target)
#		print "New target: ", target
		available_robots.remove(best_robot)
#		print "Available robots: ", available_robots

		if target <= source:
#			print "Solved! last target: ", target
			# reverse order
			certificate.reverse()
			targets.reverse()
#			print "certificate: ", certificate
#			print "\n"
			return certificate, targets


#******************************************************************************
# MAIN METHOD FOR TESTING
#******************************************************************************

def main():
	"""
	Testing methods.
	"""

	# Test greedy heuristics
	# n = 15
	# width = 1
	# source = radius = 0.4
	# target = width + source
	# robots = randomRobotGenerator(width + 2*radius, radius, n)

	# n = 3
	# width = 1.0
	# source = 0
	# radius = 1.2
	# target = width + source
	# robots = [(0.5,0.75),(0.65,0.6),(0.75,0.75)]

	# n = 4
	# width = 0.8
	# source = 0.2
	# radius = 1.2
	# target = width + source
	# robots = [(1,0.6),(1,1),(1,1.1),(0.5,0.1)]

	# Chalopins example
	# n = 7
	# width = 2.2
	# source = 0
	# radius = 2.2
	# target = width + source
	# robots = [(0.2,0.3),(0.7,0.2),(1.1,0.3),(1.2,0.5),(1.5,1.6),(1.6,1.0),(1.8,2.0)]

	# n = 3
	# width = 1.4
	# source = 0.6
	# radius = 2
	# target = width + source
	# robots = [(1.6,1.4),(1.8,1.8),(0.8,0.2)]
	# drawHLR(robots,[0.5,0.8,1],[(1.6,1.4),(0.8,0.2),(1.8,1.8)], source, target, radius)

	# Federico's example
	n = 4
	width = 1.0
	source = 0.0
	radius = 0.7
	target = 0.8
	robots = [(0.1,0.1), (0.2,0.1), (0.3,0.4), (0.4,0.6)]

	ddlp_instance = DataDelivery(robots)
	certificates = []

	print "Source: ", source
	print "Target: ", target
	print "\n"
	
	for heuristic in ['max_x','min_x','max_s','min_s','hlr']:
		certificate, targets = reverseHeuristic(robots, heuristic, source, target)
		objective_value = objectiveValue(ddlp_instance, certificate)
		upper_bound = upperBound(robots)
		print "\nHeuristic: ", heuristic
		print "certificate: ", certificate
		print "Objective value: ", objective_value
#		drawHLR(robots, targets, certificate, source, target, radius)


if __name__ == '__main__':	
	main() 