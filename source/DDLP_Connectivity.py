"""
This module deals with the connectivity properties of the DDLP problem

Created: October 5th 2018
"""

__author__ = 'Caleb Andrade'

#******************************************************************************
# HELPER FUNCTIONS
#******************************************************************************

def robotIntervals(robots, a_value):
	"""
	Converts an instance of DDLP into a set of intervals for connectivity checking
	"""

	intervals = []
	for robot in robots:
		a = robot[0] - a_value*robot[1]
		b = robot[0] + (1 - 2*a_value)*robot[1]
		intervals.append((a,b))

	return intervals 


def simmetricIntervals(robots):
	"""
	Converts an instance of DDLP into a set of simetric intervals.
	"""

	intervals = []
	for robot in robots:
		a = robot[0] - robot[1]
		b = robot[0] + robot[1]
		intervals.append((a,b))

	return intervals


def backPercentage(ddlp_instance, certificate):
	"""
	Computes "a" in the asymmetric model.
	"""
	
	# Initialize
	percentages = []
	position = ddlp_instance.data()
	robots = ddlp_instance.robotsList()

	# Sanity Check
	if len(certificate) == 0:
		return percentages

	for i in certificate:
		percentage = float(robots[i][0] - position) / robots[i][1]
		# check that data is to the left, and that there is enough energy to reach the data
		if 0 <= percentage <= 1:
			percentages.append(round(percentage,2))
		else:
			percentages.append(0.0)
		ddlp_instance.move(robots[i])
		position = ddlp_instance.data()
		
	ddlp_instance.reset()

	return percentages


#******************************************************************************
# INTERVAL GRAPH CLASS OBJECT
#******************************************************************************

class IntervalGraph(object):
	"""
	Class to represent an interval graph.
	"""

	def __init__(self, intervals):
		"""
		Initializing.
		"""
		self.size = len(intervals) # number of vertices
		self.marked = [False for i in range(self.size)]
		self.component = [i for i in range(self.size)]
		self.count = 0 # number of connected components
		self.graph = [[] for i in range(self.size)] # graph initialization
		self.intervals = intervals
		self.graphInit(intervals)

	def __str__(self):
		"""
		String representation
		"""
		string = ""

		for i in range(self.size):
			string += "\n" + str(i) + ": " + str(self.graph[i])

		return string

	def graphInit (self, intervals):
		"""
		Interval Graph construction.
		"""
		event_queue = []
		for i in range(len(intervals)):
			# store intervals endpoints in queue and name them
			event_queue.append((intervals[i][0],'a', i))
			event_queue.append((intervals[i][1],'b', i))


		# sort event queue to process events
		event_queue.sort(key = lambda value: value[1])
		event_queue.sort(key = lambda value: value[0])

		intersections = set([]) # intervals that intersect with each oter
		# process events
		for event in event_queue:
			# check if event is a start point
			if event[1] == 'a':
				# create edges in adjacency list for all interval crossings
				for interval_id in intersections:	
					self.graph[event[2]].append(interval_id)
					self.graph[interval_id].append(event[2])
				
				intersections.add(event[2])

				# mark the connected components
				self.component[event[2]] = self.count
				self.marked[event[2]] = True

			# if event is an endpoint, pop interval from intersections set
			if event[1] == 'b':
				intersections.remove(event[2])

				# if intersection set becomes empty, increase count of components
				if len(intersections) == 0:
					self.count += 1

	
	def getComponents(self):
		"""
		Return components.
		"""
		return list(self.component)

	def isConnected(self):
		"""
		Is the graph connected?
		"""
		return self.count == 1

#******************************************************************************
# MAIN METHOD FOR TESTING
#******************************************************************************

def main():
	"""
	Testing.
	"""
	intervals_1 = [(0,2),(1,6),(2,5),(4,7),(7,9),(8,10)]
	intervals_2 = [(0,1),(0,2),(0,3),(0,4),(2,4),(3,5),(6,9),(7,9),(8,9)]
	intervals_3 = [(0,1),(1,2),(0,1),(1,2),(0,1),(1,2),(0,4),(4,5),(3,4),
		           (4,5),(3,4),(6,10),(9,10),(8,10),(7,10),(11,12),(11,12),(12,13),(13,14),(13,14)]
	interval_graph = IntervalGraph(intervals_1)
	print "Components: ", interval_graph.getComponents()
	print "Number of components: ", interval_graph.count
	print "Is connected?: ", interval_graph.isConnected()

	robots = [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1)]
	print "\nRobots: ", "\n", robots
	intervals = robotIntervals(robots, 1)
	print "Intervals: ", "\n", intervals
	interval_graph = IntervalGraph(intervals)
	print "Components: ", interval_graph.getComponents()
	print "Number of components: ", interval_graph.count
	print "Is connected?: ", interval_graph.isConnected()
	
if __name__ == '__main__':	
	main() 