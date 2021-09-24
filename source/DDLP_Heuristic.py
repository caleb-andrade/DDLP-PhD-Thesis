"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (DDLP)

This code contains approximation algorithms.
Created: April 24th 2018
Last update: January 6th 2019
Last update: Decembr 13th 2020
"""

import random
from DataDelivery import DataDelivery, readFile, objectiveValue, dataTriangle
from Tkinter import Tk, Canvas

__author__ = 'Caleb Andrade'

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def closestRobot(data, robots):
	"""
	Returns the closest robot to the data.
	"""

	# initialize best robot and minimum distance
	best_robot = robots[0]
	min_distance = abs(data - best_robot[0])

	for robot in robots:
		distance = abs(data - robot[0])
		if distance < min_distance:
			best_robot = robot
			min_distance = distance

	return best_robot


def highestCapacity(data, robots):
	"""
	Returns the robot with highest capacity to move data.
	"""

	# initialize best robot
	best_robot = robots[0]
	distance = abs(data - best_robot[0])
	best_capacity = best_robot[1] - distance 

	for robot in robots:
		distance = abs(data - robot[0])
		capacity = robot[1] - distance
		if capacity > best_capacity:
			best_robot = robot
			best_capacity = capacity

	return best_robot


def lessCapacity(data, robots):
	"""
	Returns the robot with less capacity to move data.
	"""

	# initialize best robot
	best_robot = robots[0]
	distance = abs(data - best_robot[0])
	best_capacity = best_robot[1] - distance 

	for robot in robots:
		distance = abs(data - robot[0])
		capacity = robot[1] - distance
		if capacity < best_capacity:
			best_robot = robot
			best_capacity = capacity

	return best_robot


def lowestReach(robots):
	"""
	Returns the robot with lowest x_i + y_i
	"""
	
	lowest_reach = robots[0][0] + robots[0][1]
	lowest_robot = robots[0]

	for robot in robots:
		reach = robot[0] + robot[1]
		if reach < lowest_reach:
			lowest_reach = reach
			lowest_robot = robot

	return lowest_robot


def quotientHeuristic(robots, data):
	"""
	Selects greedily y-(x-d)/x-d
	"""
	best_robot = None
	best_quotient = 0

	for robot in robots:
		delta = abs(robot[0] - data)
 		if delta > 0:
			quotient = (robot[1] - delta)/delta
			if quotient > best_quotient:
				best_robot = robot
				best_quotient = quotient

	return best_robot


def remainingCapacity(robot, robots, data):
	"""
	Computes the remaining capacities for all active robots after a robot
	moves the data.
	Output: list of remaining capacities
	"""
	remaining_capacities = []
	# move data
	new_data = data + robot[1] - abs(robot[0] - data)
	# build list of active robots
	left, right = dataTriangle(new_data, robots)
	active_robots = left + right

	# loop through active robots
	for active_robot in active_robots:
		if active_robot != robot:
			remaining_capacity = active_robot[1] - abs(active_robot[0] - new_data)
			remaining_capacities.append(remaining_capacity)

	return remaining_capacities


def bestRobot(triangle, robots, data):
	"""
	Computes the robot that maximizes the remaining capacities of the
	active robots after moving the ddlp_instance
	"""
	best_robot = None
	max_value = 0

	for robot in triangle:
		remaining_capacities = remainingCapacity(robot, robots, data)
		new_data = data + robot[1] - abs(robot[0] - data)
		value = sum(remaining_capacities) + new_data
		# check for best value
		if value > max_value:
			best_robot = robot
			max_value = value

	return best_robot


def twoRobots(robot_i, robot_j, data):
	"""
	Evaluates robot i, robot j and viceversa
	"""

	data_i = data + robot_i[1] - abs(robot_i[0] - data)
	data_j = data + robot_j[1] - abs(robot_j[0] - data)

	data_ij = data_i + robot_j[1] - abs(robot_j[0] - data_i)
	data_ji = data_j + robot_i[1] - abs(robot_i[0] - data_j)

	return data_ij, data_ji


def isBetter(robot_i, robot_j, data):
	"""
	Is better robot_i than robot_j to go first?
	"""
	# sanity check
	if robot_i == robot_j:
		return False
		
	data_ij, data_ji = twoRobots(robot_i, robot_j, data)

	if data_ij > data_ji: 
		return True
	else:
		return False


def pairHeuristic(triangle, data):
	"""
	Returns the best robot of triangle, assuming transitivity
	"""
	# select first best robot arbitrarily
	best_robot = triangle[0]
	# loop through all robots
	for robot in triangle:
		# is robot better?
		if isBetter(robot, best_robot, data):
			best_robot = robot
			
	return best_robot


def brutePair(triangle, data):
	"""
	Returns the best robot of triangle, comparing every pair in brute force
	"""
	best_robot = triangle[0]
	best_value = 0
	for robot_i in triangle:
		for robot_j in triangle:
			# sanity check
			if robot_i != robot_j:
				data_ij, data_ji = twoRobots(robot_i, robot_j, data)
				if data_ij > best_value:
					best_robot = robot_i
					best_value = data_ij

	return best_robot
	

#******************************************************************************
# HEURISTIC
#******************************************************************************

def greedyHeuristic(ddlp_instance, heuristic):
	"""
	Returns a greedy certificate, according to different strategies.
	"""
	certificate = []
	robots = ddlp_instance.robotsList()
	data = ddlp_instance.data()
	finish = False

	while not finish:
		# select robots in the triangle
		left_triangle, right_triangle = dataTriangle(data, robots)
		# random sampling
		if heuristic == 'random_sampling':
			active_region = left_triangle + right_triangle
			if len(active_region) > 0:
				robot = random.choice(active_region)
			else:
				finish = True
				break
		# process robots to the left
		elif len(left_triangle) > 0:
			robot = highestCapacity(data, left_triangle)
		# process robots to the right
		elif len(right_triangle) > 0:
			if heuristic == 'closest_robot':
				robot = closestRobot(data, right_triangle)
			if heuristic == 'lowest_reach':
				robot = lowestReach(right_triangle)
			if heuristic == 'highest_capacity':
				robot = highestCapacity(data, right_triangle)
			if heuristic == 'less_capacity':
				robot = lessCapacity(data, right_triangle)
		else:
			# if both triangles are empty, finish
			finish = True
			break

		certificate.append(robot)
		ddlp_instance.move(robot)
		data = ddlp_instance.data()
		robots.remove(robot)
	
	ddlp_instance.reset()

	return certificate, data


#******************************************************************************
# MAIN METHOD FOR TESTING
#******************************************************************************

def main():
	"""
	Testing methods.
	"""

	# small test instance
	robots = [(-2,2),(-2,1),(-2,0),(-1,1),(-1,2),(-0.5,3),(0,0),(0,2),(1,1),(1,2),(2,2),(2,1),(5,2),(6,2)]
	# sort robots with respect to x_i - rho_i
	robots.sort(key = lambda robot: robot[0] - robot[1])
	print "Sorted robots: ", robots

	# test highestCapacity method
	print "\nTesting highestCapacity. Expected output: "
	print "(-0.5, 3)"
	print highestCapacity(0, robots)

	# Test dataTriangle method
	left_triangle, right_triangle = dataTriangle(0, robots)
	print "\nTesting dataTriangle"
	print "Expected output left triangle: "
	print "[(-1, 2), (-0.5, 3), (0, 2)]"
	print left_triangle
	print "Expected output right triangle: "
	print "[(1, 2)]"
	print right_triangle

	# Test lowestReach
	print "\nTesting lowestReach([(1, 2), (3, 4), (2, 3), (5, 3), (1, 1)])"
	print lowestReach([(1, 2), (3, 4), (2, 3), (5, 3), (1, 1)])

	# Test isBetter method
	print "\nTesting isBetter((5, 37), (13, 32), 0). Expected output: True"
	print isBetter((5, 37), (13, 32), 0)
	print "\nTesting isBetter((2, 4), (2, 3), 0). Expected output: True"
	print isBetter((2, 4), (2, 3), 0)

	# Test closest robot heuristic
	robots = [(-2,2),(-2,1),(-2,0),(-1,1),(-1,2),(-0.5,3),(0,0),(0,2),(1,1),(1,2),(2,2),(2,1),(5,2),(6,2)]
	# sort robots with respect to x_i - rho_i
	robots.sort(key = lambda robot: robot[0] - robot[1])
	print "Sorted robots: ", robots
	ddlp_instance =  DataDelivery(robots)
	print "\nTesting greedyHeuristic. Expected output: "
	print "[(-0.5,3), (2,2), (5,2), (6,2)]"
	print greedyHeuristic(ddlp_instance, 'closest_robot')

	print "\nTesting brute pair"
	robots = [(6,3), (6,5), (4,3), (1,4), (5,4)]
	# sort robots with respect to x_i - rho_i
	robots.sort(key = lambda robot: robot[0] - robot[1])
	ddlp_instance = DataDelivery(robots)
	print greedyHeuristic(ddlp_instance, 'brutePair')

	print "\nTesting pair heuristic"
	print greedyHeuristic(ddlp_instance, 'pairHeuristic')


if __name__ == '__main__':	
	main() 