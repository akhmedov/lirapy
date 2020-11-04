from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import axes3d 
from matplotlib import pyplot as plot
from scipy.linalg import norm
import numpy as np
import os
from scipy.constants import speed_of_light as C
from cst_data import OBSERVERS, PORTS, observer, location, read_observer_data


def compute_observer(observer_idx):

	"""
	TODO: documentation by Denis
	"""

	index, time, func = read_observer_data(observer_idx)
	index, time, func = timerange_sync(index, time, func)
	location, time, func = interpol5D(index, time, func, 3)
	t, Ex = filed_superpose(time, func)
	plot.plot(t,4*Ex)
	plot.show()


def timerange_sync(index, time, func):

	"""
	Syncronization of time for different prob data arrays
	acording to speriacal wave propagation pattern

	Args:
		index (nd.array). Array of intagers that shows index
			of a port (one of 26).
		time (nd.array). Array of arrays with sorted floating 
			point numbers that coresponds to time of filed 
			propagation. This's data from CST CSV file.
		func (nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to 
			magnitude of recived filed. This's data from 
			CST CSV file.

	Returns:
		Copy of time and filed data, but with the 
		syncronized time. The lenth of data must be eual
		for each prob.
	"""

	new_time, new_func = [], []

	for idx, tm, fn in zip(index, time, func):
		port = location(idx)
		time_dlt = np.sqrt(port.x**2 + port.y**2 + port.z**2) / C
		new_tm, new_fn = tm, fn
		new_tm += time_dlt
		tm_head = np.arange(0, time_dlt, tm[1]-tm[0])
		fn_head = np.zeros(tm_head.shape, dtype=float) 
		np.insert(new_tm, 0, tm_head)
		np.insert(new_fn, 0, fn_head)
		new_time.append(new_tm)
		new_func.append(new_fn)

	max_allowed_time = min(i[-1] for i in new_time)
	for tm, fn in zip(new_time, new_func):
		tm = tm[tm <= max_allowed_time]
		fn = fn[:tm.shape[0]]

	return index, new_time, new_func

def interpol5D(index, time, func, ratio):

	"""
	Prob magnitute values interpolation on time and port location (OX, OY, OZ).

	Args:
		index (list). Array of intagers that shows index
			of a port (one of 26).
		time (list of nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to time of 
			filed propagation. This's data from CST CSV file. 
			Data after timerange_sync sync.
		func (list of nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to 
			magnitude of recived filed. This's data from 
			CST CSV file. Data after timerange_sync sync.
		ratio (int). factor of interpolation, the ration of 
			number of ports between output and input valsue,
			ratio == len(res_func) / len(func)

	Returns:
		location (list on nd.array). The position of coresponding
			port (real or interporated).
		res_time (list of nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to time of 
			filed propagation.
		res_func (list of nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to magnitude of recived filed
	"""

	# points = np.array([[t0,x0,y0,z0], [t1,x0,y0,z0], ...])
	# values = np.array([f1, f2, ...])
	# request = np.array([[tn,xn,yn,zn], ...])
	# result = griddata(points, values, request)
	return None, time, func

def filed_superpose(time, func):

	"""
	TODO: documentation by Denis
	"""

	time_step = []
	for t in time:
		time_step.append(t[1]-t[0])
	lowest_density_index = time_step.index(max(time_step))

	res_time = time[lowest_density_index]
	tmp_func = [[] for i in range(res_time.shape[0])]
	for tm, fn in zip(time, func):
		for t, f in zip(tm, fn):
			nearest_idx = np.abs(res_time - t).argmin()
			tmp_func[nearest_idx].append(f)

	res_func = np.array([sum(i)/len(i) for i in tmp_func])
	return res_time, res_func
