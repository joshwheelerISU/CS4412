#!/usr/bin/python3

from which_pyqt import PYQT_VER
import numpy as np
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
# elif PYQT_VER == 'PYQT4':
# 	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

	
# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment

	def align( self, sequences, table, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		results = []

		bigolarray = []
		for x in range(align_length + 1):
			bigolarray.append([])
			for y in range(align_length + 1):
				bigolarray[x].append(("none", 0))

		for i in range(len(sequences)):
			jresults = []
			for j in range(len(sequences)):

				if(j < i):
					s = {}
				else:
					print(i,j)
					if(banded == True):
						out = self.banded_needleman_kn(sequences[i], sequences[j], align_length, 3)  # , bigolarray)
						# out = self.banded_needleman(sequences[i], sequences[j], align_length, 3, bigolarray)
					else:
						out = self.unbanded_needleman(sequences[i], sequences[j], align_length)
					score = out[0]
					alignment1 = out[1]
					alignment2 = out[2]
					s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
					table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
					table.update()	
				jresults.append(s)
			results.append(jresults)
		return results

	def unbanded_needleman(self, a, b, alignlength):
		resultmatrix = []  # O(1)
		topsequence = "-"  # O(1)
		vertsequence = "-"  # O(1)
		topsequence = topsequence + a  # O(1)
		vertsequence = vertsequence + b  # O(1)
		horizon = len(topsequence)  # O(1)
		vert = len(vertsequence)  # O(1)
		yval = min(vert, alignlength+1)  # O(1)
		xval = min(horizon, alignlength+1)  # O(1)

		for x in range (xval): 																		    # O(xval * yval)
			resultmatrix.append([])  # O(1)
			for y in range(yval):                                                                              # O(yval)
				resultmatrix[x].append(("done", 0))  # O(1)
		# perform base case fill
		for y in range(1, yval):                                                                               # O(yval)
			resultmatrix[0][y] = ("up", resultmatrix[0][y-1][1] + INDEL)  # O(1)
		for x in range(1, xval):  																			   # O(xval)
			resultmatrix[x][0] = ("left", resultmatrix[x-1][0][1] + INDEL)  # O(1)
		xwalk = 1  # O(1)
		# standard case
		for y in range(1, yval):                                                                  # O(yval-1 * xval - 1)
			for x in range (1, min(y+1, xval)):                                                            # O(xval - 1)
				up = resultmatrix[x][y - 1][1] + INDEL  # O(1)
				left = resultmatrix[x - 1][y][1] + INDEL  # O(1)
				diag = resultmatrix[x - 1][y - 1][1] + SUB  # O(1)

				if topsequence[x] == vertsequence[y]:  # O(1)
					diag = resultmatrix[x - 1][y - 1][1] + MATCH  # O(1)

				bestchoice = ("left", left)
				if up < left:  # O(1)
					bestchoice = ("up", up)  # O(1)
				if diag < up and diag < left:  # O(1)
					bestchoice = ("diag", diag)  # O(1)

				resultmatrix[x][y] = bestchoice  # O(1)
			xwalk = xwalk + 1  # O(1)
		# extract the proper alignments - > up is - into top, left is insert - into left, diag is align on that value
		backx = xval - 1  # O(1)
		backy = yval - 1  # O(1)
		topoutalign = topsequence  # O(1)
		sideoutalign = vertsequence  # O(1)
		currentsquare = resultmatrix[backx][backy]  # O(1)
		while currentsquare != resultmatrix[0][0]:                                                 # worst case O(m + n)
			if currentsquare[0] == "up":  # O(1)
				topoutalign = topoutalign[:backx] + "-" + topoutalign[backx:]  # O(1)
				backy = backy - 1  # O(1)
			elif currentsquare[0] == "left":  # O(1)
				sideoutalign = sideoutalign[:backy] + "-" + sideoutalign[backy:]  # O(1)
				backx = backx - 1  # O(1)
			elif currentsquare[0] == "diag":  # O(1)
				if(currentsquare[1] - resultmatrix[backx-1][backy-1][1] != -3):
					upchar = topoutalign[backx]
					sideoutalign = sideoutalign[:backy - 1] + upchar + sideoutalign[backy - 1:]
				# sideoutalign[backy] = topoutalign[backx]  # O(1)
				backx = backx - 1  # O(1)
				backy = backy - 1  # O(1)
			currentsquare = resultmatrix[backx][backy]  # O(1)
		return resultmatrix[xval-1][yval-1][1], topoutalign[:100], sideoutalign[:100]  # O(1)

	def banded_needleman_kn(self, a, b, alignlength, bandsize):
		resultmatrix = []  # O(1)
		topsequence = "-"  # O(1)
		vertsequence = "-"  # O(1)
		topsequence = topsequence + a  # O(1)
		vertsequence = vertsequence + b  # O(1)
		horizon = len(topsequence)  # O(1)
		vert = len(vertsequence)  # O(1)
		yval = min(vert, alignlength + 1)  # O(1)
		xval = min(horizon, alignlength + 1)  # O(1)

		band = 2 * bandsize + 1  # O(1)

		for x in range(band+1):                                                                                # O(band)
			resultmatrix.append([])  # O(1)
			for y in range(yval):                                                                           # O(max(m,n)
				resultmatrix[x].append(("none", 0))  # O(1)

		posx = math.floor(band/2)  # O(1)
		posy = 0  # O(1)
		# case across moves laterally
		# case down moves horizontally
		for x in range(bandsize, band + 1):                                                         # O(band - bandsize)
			resultmatrix[x][0] = ("left", resultmatrix[x-1][0][1] + INDEL)  # O(1)
		xwalk = bandsize-1  # O(1)
		for y in range(1, bandsize + 1):                                                               # O(bandsize - 1)
			resultmatrix[xwalk][y] = ("diag", resultmatrix[xwalk+1][y-1][1] + INDEL)  # O(1)
			xwalk = xwalk-1  # O(1)
		resultmatrix[bandsize][0] = ("home", 0)  # O(1)
		# typical case, start with x=bandsize, y = 2
		cury = 1  # O(1)
		xcount = 0  # O(1)
		while cury < yval and cury < xval:                                                  # O(min(yval, xval) * 2band)
			xcount = 0  # O(1)
			for x in range(bandsize, band + 1):                                                                # O(band)
				if cury + xcount < xval:  # O(1)
					if(x+1 >= band):  # O(1)
						newdiag = float('inf')  # O(1)
					else:  # O(1)
						newdiag = resultmatrix[x+1][cury - 1][1] + INDEL  # O(1)
					left = resultmatrix[x - 1][cury][1] + INDEL  # O(1)
					newup = resultmatrix[x][cury - 1][1] + SUB  # O(1)
					if topsequence[cury + xcount] == vertsequence[cury]:  # O(1)
						newup = resultmatrix[x][cury - 1][1] + MATCH  # O(1)
					bestchoice = ("left", left)  # O(1)
					if newup < left:  # O(1)
						bestchoice = ("up", newup)  # O(1)
					if newdiag < newup and newdiag < left:  # O(1)
						bestchoice = ("diag", newdiag)  # O(1)
					resultmatrix[x][cury] = bestchoice  # O(1)
					xcount = xcount + 1  # O(1)
				else:
					resultmatrix[x][cury] = ("exceededxlength", math.inf)  # O(1)
			xwalk = bandsize - 1  # O(1)
			for y in range(cury + 1, min(yval, (cury + bandsize + 2))):                                        # O(band)
				if (xwalk + 1 >= band):  # O(1)
					newdiag = float('inf')  # O(1)
				else:
					newdiag = resultmatrix[xwalk + 1][y - 1][1] + INDEL  # O(1)
				if(xwalk - 1 < 0):  # O(1)
					left = float('inf')  # O(1)
				else:
					left = resultmatrix[xwalk - 1][y][1] + INDEL  # O(1)
				newup = resultmatrix[xwalk][y - 1][1] + SUB  # O(1)
				if topsequence[bandsize - xwalk] == vertsequence[cury]:  # O(1)
					newup = resultmatrix[xwalk][y - 1][1] + MATCH  # O(1)
				bestchoice = ("left", left)  # O(1)
				if newup < left:  # O(1)
					bestchoice = ("up", newup)  # O(1)
				if newdiag < newup and newdiag < left:  # O(1)
					bestchoice = ("diag", newdiag)  # O(1)
				resultmatrix[xwalk][y] = bestchoice  # O(1)
				xwalk = xwalk - 1  # O(1)
			cury = cury + 1  # O(1)
		if resultmatrix[bandsize][yval-2][0] == "none":  # O(1)
			return math.inf, "test", "test"  # O(1)
		else:
			return resultmatrix[bandsize][min(xval-1, yval-1)][1], "test", "test"  # O(1)


	def banded_needleman(self, a, b, alignlength, bandsize, bigolarray):
		resultmatrix = [] 																						  # O(1)
		topsequence = "-"  															                              # O(1)
		vertsequence = "-" 															                              # O(1)
		topsequence = topsequence + a 															                  # O(1)
		vertsequence = vertsequence + b  															              # O(1)
		horizon = len(topsequence)  															                  # O(1)
		vert = len(vertsequence)  															                      # O(1)
		yval = min(vert, alignlength+1) 															              # O(1)
		xval = min(horizon, alignlength+1)  															          # O(1)

		band = 2 * bandsize + 1 															                      # O(1)

		# for x in range (xval):
		# 	resultmatrix.append([])
		# 	for y in range(yval):
		# 		resultmatrix[x].append(("none", 0))

		resultmatrix = bigolarray 															                      # O(1)
		# perform base case fill
		for y in range(1, band + 1):  															               # O(band)
			resultmatrix[0][y] = ("up", resultmatrix[0][y-1][1] + INDEL)  										  # O(1)
		for x in range(1, band + 1):   																		   # O(band)
			resultmatrix[x][0] = ("left", resultmatrix[x-1][0][1] + INDEL)  									  # O(1)
		# standard case
		currentsrc = resultmatrix[1][1] 																		  # O(1)
		curx = 1 																								  # O(1)
		cury = 1 																							      # O(1)
		while curx != xval and cury != yval:  														 # O(min(xval, yval)
			for x in range(curx, min(curx+bandsize + 1, xval)): 										   # O(bandsize)
				up = resultmatrix[x][cury-1][1] + INDEL  														  # O(1)
				left = resultmatrix[x-1][cury][1] + INDEL 														  # O(1)
				diag = resultmatrix[x-1][cury-1][1] + SUB 														  # O(1)
				if topsequence[x] == vertsequence[cury]: 														  # O(1)
					diag = resultmatrix[x-1][cury-1][1] + MATCH  												  # O(1)
				bestchoice = ("left", left)  															          # O(1)
				if up < left: 															 						  # O(1)
					bestchoice = ("up", up) 															  		  # O(1)
				if diag < up and diag < left:  																      # O(1)
					bestchoice = ("diag", diag)  															      # O(1)
				resultmatrix[x][cury] = bestchoice 															      # O(1)
			for y in range(cury, min(cury+bandsize + 1, yval)): 									       # O(bandsize)
				up = resultmatrix[curx][y - 1][1] + INDEL 													      # O(1)
				left = resultmatrix[curx - 1][y][1] + INDEL 													  # O(1)
				diag = resultmatrix[curx - 1][y - 1][1] + SUB 													  # O(1)
				if topsequence[curx] == vertsequence[y]: 													      # O(1)
					diag = resultmatrix[curx - 1][y - 1][1] + MATCH 									   		  # O(1)
				bestchoice = ("left", left) 															 		  # O(1)
				if up < left: 															 						  # O(1)
					bestchoice = ("up", up)  																	  # O(1)
				if diag < up and diag < left: 															 		  # O(1)
					bestchoice = ("diag", diag) 															 	  # O(1)
				resultmatrix[curx][y] = bestchoice  															  # O(1)
			curx = curx+1 															                              # O(1)
			cury = cury+1 																						  # O(1)

		if resultmatrix[xval-1][yval-1][0] == "none":  															  # O(1)
			return float('inf'), "No Alignment Possible", "No Alignment Possible"  # O(1)
		else:
			backx = xval - 1 																					  # O(1)
			backy = yval - 1  																					  # O(1)
			topoutalign = topsequence  																		      # O(1)
			sideoutalign = vertsequence 																		  # O(1)
			currentsquare = resultmatrix[backx][backy] 															  # O(1)
			while currentsquare != resultmatrix[0][0]: 											# about O(sqrt(n^2+m^2))
				if currentsquare[0] == "up":  																	  # O(1)
					topoutalign = topoutalign[:backx] + "-" + topoutalign[backx:]								  # O(1)
					backy = backy - 1  																		      # O(1)
				elif currentsquare[0] == "left": 																  # O(1)
					sideoutalign = sideoutalign[:backy] + "-" + sideoutalign[backy:]  						      # O(1)
					backx = backx - 1  																   			  # O(1)
				elif currentsquare[0] == "diag":  																  # O(1)
					# sideoutalign[backy] = topoutalign[backx]
					backx = backx - 1 															 				  # O(1)
					backy = backy - 1 															 				  # O(1)
				currentsquare = resultmatrix[backx][backy]  													  # O(1)
			return resultmatrix[xval - 1][yval - 1][1], topoutalign[:100], sideoutalign[:100]  					  # O(1)

