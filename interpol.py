from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import axes3d 
from matplotlib import pyplot as plot
from scipy.linalg import norm
import numpy as np


def time_sync(possition, time, filed):

	"""
	Syncronization of time for different prob data arrays
	acording to speriacal wave propagation pattern

	Args:
		possition (nd.array). Array of arrays with 3 values
			that contains x, y, z coordiate of a port.
		time (nd.array). Array of arrays with sorted floating 
			point numbers that coresponds to time of filed 
			propagation. This's data from CST CSV file.
		filed (nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to 
			magnitude of recived filed. This's data from 
			CST CSV file.

	Returns:
		Copy of time and filed data, but with the 
		syncronized time. The lenth of data must be eual
		for each prob.
	"""

	# TODO: to implement by Denis
	pass


# def interpolate_point():
# points = np.array([])
# values = np.array([])
# request = np.array([])
# result = griddata(points, values, request)
