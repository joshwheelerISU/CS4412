import copy
import math

from which_pyqt import PYQT_VER

if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
# elif PYQT_VER == 'PYQT4': # from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time

# Some global color constants that might be useful
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

	# Class constructor
	def __init__(self):
		super().__init__()
		self.pause = False

	# Some helper methods that make calls to the GUI, allowing us to send updates
	# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self, line, color):
		self.showTangent(line, color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon, color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self, polygon):
		self.view.clearLines(polygon)

	def showText(self, text):
		self.view.displayStatusText(text)

	# This is the method that gets called by the GUI and actually executes
	# the finding of the hull
	def compute_hull(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert (type(points) == list and type(points[0]) == QPointF)

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		points.sort(key=QPointF.x, reverse=False)
		hull = []
		newlist1 = []
		newlist2 = []
		t2 = time.time()
		t3 = time.time()
		ret = self.convex_hull_solver(points)
		polygon = [QLineF(ret[i], ret[(i+1)%len(ret)]) for i in range(len(ret))]
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon, RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))


	def convex_hull_solver(self, points):
		if len(points) == 1:
			return points
		elif (len(points) >=2):
			left = []
			right = []
			split = math.floor(len(points)/2)
			x = 0
			for y in points:
				if x <= split:
					left.append(y)
					x = x + 1
				else:
					right.append(y)
			return self.better_merge_hulls(left, right)

	def better_merge_hulls(self, lefthull, righthull):
		rethull = []
		# debug scenario where an empty hull is passed in
		# initial case where the hulls are single
		if (len(lefthull) == 1 and len(righthull) == 1):
			# all we do is merge the hulls and send em back up
			rethull.append(lefthull[0])
			rethull.append(righthull[0])
			return rethull
		if(len(lefthull) == 1 and len(righthull) == 2):
			# handle these 2 edge cases really quick just because it makes more sense to me to do it this way
			rethull.append(lefthull[0])
			righthull.sort(key=QPointF.y, reverse=True)  # this and the line below it should return clockwise
			rethull.append(righthull[0])
			rethull.append(righthull[1])
			return rethull
		if(len(lefthull) == 2 and len(righthull) == 1):
			# same as the last one but ascending y order on the left side with the right appended to achieve clockwise placement
			lefthull.sort(key=QPointF.y, reverse=False)
			rethull.append(lefthull[0])
			rethull.append(lefthull[1])
			rethull.append(righthull[0])
			return rethull
		if(len(lefthull) == 2 and len(righthull) == 2):
			# combine ascending y on the left side, descending y on the right
			lefthull.sort(key=QPointF.y, reverse=False)
			righthull.sort(key=QPointF.y, reverse=True)
			rethull.append(lefthull[0])
			rethull.append(lefthull[1])
			rethull.append(righthull[0])
			rethull.append(righthull[1])
			return rethull
		if(len(lefthull) == 2 and len(righthull) == 3):
			# again, just scan up the left, then back down the right | only include the middle element if the slope is negative
			lefthull.sort(key=QPointF.y, reverse=False)
			rightpreserve = copy.deepcopy(righthull)
			rightccw = copy.deepcopy(righthull)
			rightccw.reverse()
			righthull.sort(key=QPointF.x, reverse=False)
			topleftfound = lefthull[0]
			bottomleftfound = lefthull[1]
			rightstart = righthull[0]
			currentslope = (topleftfound.y() - rightstart.y()) / (topleftfound.x() - rightstart.x())
			lastslope = currentslope
			previouspoint = rightstart
			currentrightindex = rightpreserve.index(rightstart)
			while currentslope >= lastslope:
				previouspoint = rightstart
				rightstart = rightpreserve[(currentrightindex % len(righthull))]
				lastslope = currentslope
				currentslope = (topleftfound.y() - rightstart.y()) / (topleftfound.x() - rightstart.x())
				currentrightindex = currentrightindex + 1
			currentrightindex = currentrightindex - 1
			toprightfound = previouspoint
			# bottom right time
			currentslope = (bottomleftfound.y() - rightstart.y()) / (bottomleftfound.x() - rightstart.x())
			lastslope = currentslope
			previouspoint = rightstart
			currentrightindex = rightccw.index(rightstart)
			while currentslope <= lastslope:
				previouspoint = rightstart
				rightstart = rightccw[(currentrightindex % len(rightccw))]
				lastslope = currentslope
				currentslope = (bottomleftfound.y() - rightstart.y()) / (bottomleftfound.x() - rightstart.x())
				currentrightindex = currentrightindex + 1
			currentrightindex = currentrightindex - 1
			bottomrightfound = previouspoint

			#merge hulls preserving clockwise rotation
			rethull.append(bottomleftfound)
			rethull.append(topleftfound)
			startindex = rightpreserve.index(toprightfound)
			endindex = rightpreserve.index(bottomrightfound)
			for x in range(startindex, endindex + 1):
				rethull.append(rightpreserve[x])
			return rethull
		if (len(righthull) == 2 and len(lefthull) == 3):
			righthull.sort(key=QPointF.y, reverse=True)
			leftpreserve = copy.deepcopy(lefthull)
			leftccw = copy.deepcopy(lefthull)
			leftccw.reverse()
			lefthull.sort(key=QPointF.x, reverse=False)
			toprightfound = righthull[0]
			bottomrightfound = righthull[1]
			leftstart = lefthull[0]
			currentslope = (leftstart.y() - toprightfound.y()) / (leftstart.x() - toprightfound.x())
			lastslope = currentslope  # keep track of the previous slope we've seen
			# at this point we want to shift the left point counter clockwise until the slope is no longer decreasing
			# then revert to the previous point
			previouspoint = leftstart
			currentleftindex = leftccw.index(leftstart)
			while currentslope <= lastslope:
				previouspoint = leftstart
				leftstart = leftccw[(currentleftindex % len(leftccw))]
				lastslope = currentslope
				currentslope = (leftstart.y() - toprightfound.y()) / (leftstart.x() - toprightfound.x())
				currentleftindex = currentleftindex + 1
			topleftfound = previouspoint

			# find bottom left
			currentslope = (leftstart.y() - bottomrightfound.y()) / (leftstart.x() - bottomrightfound.x())
			lastslope = currentslope  # keep track of the previous slope we've seen
			# at this point we want to shift the left point clockwise until the slope is no longer increasing
			# then revert to the previous point
			previouspoint = leftstart
			currentleftindex = leftpreserve.index(leftstart)
			while currentslope >= lastslope:
				previouspoint = leftstart
				leftstart = leftpreserve[(currentleftindex % len(leftpreserve))]
				lastslope = currentslope
				currentslope = (leftstart.y() - bottomrightfound.y()) / (leftstart.x() - bottomrightfound.x())
				currentleftindex = currentleftindex + 1
			currentleftindex = currentleftindex - 1
			bottomleftfound = previouspoint

			startindex = leftpreserve.index(bottomleftfound)
			endindex = leftpreserve.index(topleftfound)
			for x in range(startindex, endindex + 1):
				rethull.append(leftpreserve[x])
			rethull.append(righthull[0])
			rethull.append(righthull[1])
			return rethull
		elif (len(lefthull) != 0) and len(righthull) != 0:
			# this is where we will do the standard algorithm for merging the hulls. anything received at this point is
			# expected to be a hull in clockwise order, and at the end of this process, we must return a clockwise hull
			# first, we find the leftmost of the right hull and the rightmost of the left hull. we should copy the arrays
			# and operate on them from there | passed in hulls are preserved as clockwise
			# useful tools for later ;)
			leftsortx = copy.deepcopy(lefthull)
			rightsortx = copy.deepcopy(righthull)
			leftccw = copy.deepcopy(lefthull)
			rightccw = copy.deepcopy(righthull)
			leftccw.reverse() # made a ccw copy of the left hull
			rightccw.reverse() # make a ccw copy of the right hull
			leftsortx.sort(key=QPointF.x, reverse=True)  # sort the left hull in direction of right to left
			rightsortx.sort(key=QPointF.x, reverse=False)  # sort the right hull left to right
			# where we start searching
			leftstart = leftsortx[0]
			rightstart = rightsortx[0]
			# find the slop between these two points
			currentslope = (leftstart.y() - rightstart.y()) / (leftstart.x() - rightstart.x())
			lastslope = currentslope # keep track of the previous slope we've seen
			# at this point we want to shift the left point counter clockwise until the slope is no longer decreasing
			# then revert to the previous point
			previouspoint = leftstart
			currentleftindex = leftccw.index(leftstart)
			while currentslope <= lastslope:
				previouspoint = leftstart
				leftstart = leftccw[(currentleftindex % len(leftccw))]
				lastslope = currentslope
				currentslope = (leftstart.y() - rightstart.y()) / (leftstart.x() - rightstart.x())
				currentleftindex = currentleftindex + 1
			topleftfound = previouspoint

			# now we need to move the right hull point clockwise until the slope stops increasing.
			currentslope = (topleftfound.y() - rightstart.y()) / (topleftfound.x() - rightstart.x())
			lastslope = currentslope
			previouspoint = rightstart
			currentrightindex = righthull.index(rightstart)
			while currentslope >= lastslope:
				previouspoint = rightstart
				rightstart = righthull[(currentrightindex % len(righthull))]
				lastslope = currentslope
				currentslope = (topleftfound.y() - rightstart.y()) / (topleftfound.x() - rightstart.x())
				currentrightindex = currentrightindex + 1
			currentrightindex = currentrightindex - 1
			toprightfound = previouspoint

			# we have found the top tangent, now we have to find the bottom. this is a similar process to above.
			leftstart = leftsortx[0]
			rightstart = rightsortx[0]
			# find the slop between these two points
			currentslope = (leftstart.y() - rightstart.y()) / (leftstart.x() - rightstart.x())
			lastslope = currentslope  # keep track of the previous slope we've seen
			# at this point we want to shift the left point clockwise until the slope is no longer increasing
			# then revert to the previous point
			previouspoint = leftstart
			currentleftindex = lefthull.index(leftstart)
			while currentslope >= lastslope:
				previouspoint = leftstart
				leftstart = lefthull[(currentleftindex % len(lefthull))]
				lastslope = currentslope
				currentslope = (leftstart.y() - rightstart.y()) / (leftstart.x() - rightstart.x())
				currentleftindex = currentleftindex + 1
			currentleftindex = currentleftindex - 1
			bottomleftfound = previouspoint

			# now we need to move the right hull point counter clockwise until the slope stops decreasing.
			currentslope = (bottomleftfound.y() - rightstart.y()) / (bottomleftfound.x() - rightstart.x())
			lastslope = currentslope
			previouspoint = rightstart
			currentrightindex = rightccw.index(rightstart)
			while currentslope <= lastslope:
				previouspoint = rightstart
				rightstart = rightccw[(currentrightindex % len(rightccw))]
				lastslope = currentslope
				currentslope = (bottomleftfound.y() - rightstart.y()) / (bottomleftfound.x() - rightstart.x())
				currentrightindex = currentrightindex + 1
			currentrightindex = currentrightindex - 1
			bottomrightfound = previouspoint

			# at this point we should have the 2 tangent lines. now we can begin connecting the dots and return the
			# clockwise result | ascend left hull, descend right hull
			startindex = lefthull.index(bottomleftfound)
			endindex = lefthull.index(topleftfound)
			for z in range(startindex, endindex + 1):
				rethull.append(lefthull[z])
			startindex = righthull.index(toprightfound)
			endindex = righthull.index(bottomrightfound)
			for z in range(startindex, endindex + 1):
				rethull.append(righthull[z])
			return rethull
		elif (len(lefthull) != 0 and len(righthull) == 0):
			# return lefthull but not righthull
			return lefthull
		elif (len(lefthull) == 0 and len(righthull) != 0):
			return righthull
		else:
			return rethull

