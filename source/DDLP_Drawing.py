"""
DATA DELIVERY BY ENERGY CONSTRAINED MOBILE AGENTS ON A LINE PROBLEM (DDLP)

This code is for drawing DDLP instances.
Last update: 18/12/2020
"""

from Tkinter import Tk, Canvas
from DataDelivery import DataDelivery
import random
import time
from PIL import Image

__author__ = 'Caleb Andrade'


def drawInstance(ddlp_instance, data, width, radius):
	"""
	Draws an instance of Data Delivery, and the active region of a specified
	point by the data location.
	"""

	# initialize canvas
	root = Tk()
	canvas = Canvas(root, width = 10 + 10*width, height = 10 + 10*radius, background = "white")
	canvas.pack()

	# draw box
	canvas.create_rectangle(5, 5, 5 + 10*width, 5 + 10*radius)
	
	# draw robots as dots and labels
	robots = ddlp_instance.robotsList()
	for i in range(len(robots)):
		robot = robots[i]
		x = 5 + 10*robot[0]
		y = 5 + 10*(radius - robot[1])
		canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill='red', width = 3)
		canvas.create_text((x + 7, y), text = str(i), font = ("Helvetica", 9))

	# draw active zone
	canvas.create_line(5 + 10*(data - radius), 5, 5 + 10*data, 5 + 10*radius, fill = 'blue', width = 1.5)
	canvas.create_line(5 + 10*data, 5 + 10*radius, 5 + 10*(data + radius), 5, fill = 'blue', width = 1.5)

	root.mainloop()


def rangeLimits(robots):
	"""
	Returns the x_range and y_range to graph a data instance in the
	(position, position) plane
	"""
	
	min_limit = max_limit = max_radius = 0
	for robot in robots:
		if robot[0] - robot[1] < min_limit:
			min_limit = robot[0] - robot[1]
		if robot[0] + robot[1] > max_limit:
			max_limit = robot[0] + robot[1]
		if robot[1] > max_radius:
			max_radius = robot[1]

	return min_limit, max_limit, max_radius


def robotTriangle(robots):
	"""
	Returns a list of pairs of tuples, representing line segments that build
	triangles that represent the position displacement related to each robot in 
	the (position, position) plane
	"""

	segments = []

	for robot in robots:
		vertex_a = (robot[0] - robot[1], robot[0] - robot[1])
		vertex_b = (robot[0], robot[0] + robot[1])
		vertex_c = (robot[0] + robot[1], robot[0] + robot[1])
		segments.extend([[vertex_a, vertex_b], [vertex_b, vertex_c]])

	return segments


def dataTrajectory(ddlp_instance, certificate):
	"""
	Returns a list of pairs of tuples, representing line segments that build
	the data's position trajectory given a certificate in the (position, position) plane
	"""

	segments = []
	data = ddlp_instance.data()

	for robot in certificate:
		vertex_a = (data, data)
		ddlp_instance.move(robot) # move data
		temp_data = data
		data = ddlp_instance.data()
		vertex_b = (temp_data, data)
		vertex_c = (data, data)
		segments.extend([[vertex_a, vertex_b], [vertex_b, vertex_c]])

	ddlp_instance.reset()

	return segments


def drawcertificate(ddlp_instance, certificate, size, heuristic):
	"""
	Draws a certificate in the (position, position) plane as a trajectory
	"""
	# create line segments
	trajectory = dataTrajectory(ddlp_instance, certificate)
	robot_triangle = robotTriangle(ddlp_instance.robotsList())
	
	# initialize canvas
	root = Tk()
	canvas = Canvas(root, width = size + 5, height = size + 5, background = "white")
	canvas.pack()
	
	# set vertical and horizontal range
	x_range = y_range = rangeLimits(ddlp_instance.robotsList())
	delta = x_range[1] - x_range[0]
	ratio = float(size)/delta
	
	# draw robot triangle lines
	for index in range(len(robot_triangle)/2):
	
		# generate random color
		R = random.randint(0, 255)
		G = random.randint(0, 255)
		B = random.randint(0, 255)
		
		line_color = "#%02x%02x%02x" %(R, G, B) # set color in RGB mode
		
		line1 = robot_triangle[2*index]
		line2 = robot_triangle[2*index + 1]
		
		canvas.create_line((line1[0][0]-x_range[0])*ratio, size + 5 - (line1[0][1]-y_range[0])*ratio, 
						   (line1[1][0]-x_range[0])*ratio, size + 5 - (line1[1][1]-y_range[0])*ratio, 
						   fill = line_color, width = 1)

		canvas.create_line((line2[0][0]-x_range[0])*ratio, size + 5 - (line2[0][1]-y_range[0])*ratio, 
						   (line2[1][0]-x_range[0])*ratio, size + 5 - (line2[1][1]-y_range[0])*ratio, 
						   fill = line_color, width = 1)

	# draw trajectory lines
	for line in trajectory:
		canvas.create_line((line[0][0]-x_range[0])*ratio, size + 5 - (line[0][1]-y_range[0])*ratio, 
						   (line[1][0]-x_range[0])*ratio, size + 5 - (line[1][1]-y_range[0])*ratio, 
						   fill = 'red', width = 1.5)

	# draw axes and identity
	canvas.create_line(0, size + 5 , size, 5, fill = 'black', width = 1)

	# draw text
	canvas.create_text((300, 15), text = heuristic, font = ("Helvetica", 15))

	root.mainloop()


def saveAsPNG(canvas,fileName):
    # save postscipt image 
    canvas.postscript(file = fileName + '.eps') 
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    img.save(fileName + '.png', 'png') 


def drawHLR(robots, targets, certificate, source, target, radius):
	"""
	Draws an instance of Data Delivery, and the certificate obtained by HLR.
	"""

	min_limit = source - radius
	max_limit = target + radius
	width = max_limit - min_limit
	
	# initialize canvas
	root = Tk()
	canvas = Canvas(root, width = 10 + 200*width, height = 20 + 200*radius, background = "white")
	canvas.pack()

	# draw box
	canvas.create_rectangle(5, 5, 5 + 200*width, 5 + 200*radius)
	
	# draw source and target
	s = 5 + 200*(source + abs(min_limit))
	t = 5 + 200*(target + abs(min_limit))
	canvas.create_text((s, 200*radius+12), text = str(source), font = ("Helvetica", 11))
	canvas.create_text((t, 200*radius+12), text = str(target), font = ("Helvetica", 11))

	# draw active zones
	for i in range(len(targets)):

		# generate random color
		R = random.randint(0, 255)
		G = random.randint(0, 255)
		B = random.randint(0, 255)
		
		line_color = "#%02x%02x%02x" %(R, G, B) # set color in RGB mode

		robot = certificate[i]
		x = 5 + 200*(abs(min_limit) + robot[0])
		y = 5 + 200*(radius - robot[1])
		data = 5 + 200*(targets[i] + abs(min_limit))
		delta = x - data
		# draw trajectories		
		canvas.create_line(x, y, x - delta, y + delta, fill = line_color, width = 1.5)
		canvas.create_line(x - delta, y + delta, x - delta, 5 + 200*radius, fill = line_color, width = 1.5)
		# draw active zones
		canvas.create_line(data - 200*radius, 5, data, 5 + 200*radius, fill = line_color, width = 1)
		canvas.create_line(data, 5 + 200*radius, data + 200*radius, 5, fill = line_color, width = 1)

	# draw robots as dots and labels
	i = 0
	for robot in robots:
		i = i + 1
		x = 5 + 200*(abs(min_limit) + robot[0])
		y = 5 + 200*(radius - robot[1])
		canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='black', width = 1)
		canvas.create_text((x + 7, y + 7), text = str(i), font = ("Helvetica", 9))

	# draw A(t)
	data = 5 + 200*(target + abs(min_limit))
	canvas.create_line(data - 200*radius, 5, data, 5 + 200*radius, fill = 'black', width = 1)
	canvas.create_line(data, 5 + 200*radius, data + 200*radius, 5, fill = 'black', width = 1)

	file_name = str(time.time())
#	saveAsPNG(canvas,file_name)

	root.mainloop()


def main():
	"""
	Testing methods.
	"""

	robots = [(-0.2,0.2),(-0.2,0.1),(-0.2,0),(-0.1,0.1),(-0.1,0.2),(-0.05,0.3),(0,0.2),(0.1,0.1),(0.4,0.2),(0.2,0.2),(0.2,0.1),(0.5,0.2),(0.6,0.2)]

	# Test robotTriangle method
	print "\nTesting robotTriangle"
	print robotTriangle(robots)

	# Test dataTrajectory
	print "\nTesting dataTrajectory"
	ddlp_instance = DataDelivery(robots)
	print dataTrajectory(ddlp_instance, [(0.2,0.2), (0.5,0.2), (0.6,0.2)])

	# Test drawHLR
	print "\nTesting drawHLR"
	certificate = [(0, 0.2), (0.1, 0.1), (0.2, 0.1), (0.2, 0.2), (0.4, 0.2), (0.5, 0.2), (0.6, 0.2)]
	targets = [-0.06796875, 0.0640625, 0.128125, 0.15625, 0.3125, 0.425, 0.55]
	source = 0
	target = 0.7
	radius = 0.3
	print "robots: ", robots
	print "source: ", source
	print "target: ", target
	print "certificate: ", certificate
	drawHLR(robots, targets, certificate, source, target, radius)

	# Example of Theorem: EDL is in P
	print "\nEDL is in P"
	robots = [(0.5,0.75),(0.65,0.6),(0.75,0.75)]
	certificate = []
	targets = []
	source = 0
	target = 1.0
	radius = 0.8
	print "robots: ", robots
	print "source: ", source
	print "target: ", target
	print "certificate: ", certificate
	drawHLR(robots, targets, certificate, source, target, radius)

if __name__ == '__main__':	
	main() 


