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
	index, time, func = time_sync(index, time, func)
	t, Ex = filed_superpose(time, func)
	plot.plot(t,4*Ex)
	plot.show()



def filed_superpose(time, func):

	"""
	TODO: documentation by Denis
	"""

	time_step = []
	for t in time:
		time_step.append(t[1]-t[0])
	lowest_density_index = time_step.index(max(time_step))

	res_time = time[lowest_density_index]
	res_func = func[lowest_density_index]
	for idx, tm, fn in zip(range(0,len(time)), time, func):
		if idx == lowest_density_index: continue
		for t, f in zip(tm, fn):
			nearest_idx = np.abs(res_time - t).argmin()
			res_func[nearest_idx] += f

	return res_time, res_func / len(time)


def time_sync(index, time, func):

	"""
	Syncronization of time for different prob data arrays
	acording to speriacal wave propagation pattern

	Args:
		index (nd.array). Array of intagers that shows index
			of a port (one of 27).
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


# def interpolate_point():
# points = np.array([])
# values = np.array([])
# request = np.array([])
# result = griddata(points, values, request)
