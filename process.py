from scipy.interpolate import griddata
import numpy as np
import random
from cst_data import location, read_nonlinear_observer_data, read_linear_observer_data, read_port_timedepth
from visual import show_prob_data, show_port_location, simple_plot


def compute_observer(observer_idx, interp_ratio):

	"""
	TODO: documentation by Denis
	"""

	time, current = read_port_timedepth()
	simple_plot(time, current, 'Source timedep', 'time, sec', 'Normed current')

	index, time, func = read_nonlinear_observer_data(observer_idx)
	show_prob_data(observer_idx)
	index, time, func = timerange_sync(index, time, func)
	port_location, prob_time, prob_func = mirror_and_interpol5D(index, time, func, interp_ratio)
	show_port_location(port_location)
	nonlinear_time, nonlinear_Ex = filed_superpose(prob_time, prob_func)
	simple_plot(nonlinear_time, nonlinear_Ex, 'Nonlinear amendment for radiation', 'time, sec', 'Ex, A/m')

	linear_time, linear_Ex = read_linear_observer_data(observer_idx)
	simple_plot(linear_time, linear_Ex, 'Nonlinear amendment for radiation', 'time, sec', 'Ex, A/m')

	time = [linear_time, nonlinear_time]
	field = [linear_Ex, nonlinear_Ex]
	_, time, func = timerange_sync(None, time, func)

	time, field = filed_superpose(time, field)
	simple_plot(time, field, 'Superposition for linear and nonlinear field', 'time, sec', 'Ex, A/m')


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

	new_time, new_func = time, func
	max_allowed_time = min(i[-1] for i in new_time)
	for i in range(len(new_time)):
		new_time[i] = new_time[i][new_time[i] <= max_allowed_time]
		new_func[i] = new_func[i][:new_time[i].shape[0]]

	return index, new_time, new_func


def mirror_point3D(plus_point):

	"""
	TODO: documentation by Denis
	"""

	plus_point = np.abs(plus_point)
	x, y, z  = plus_point[0], plus_point[1], plus_point[2]
	res = [
		np.array([x, y, z]),
		np.array([-x, y, z]),
		np.array([x, -y, z]),
		np.array([-x, -y, z])
	]
	return res


def get_max_time_step_intex(time):

	"""
	TODO: documentation by Denis
	"""

	time_step = []
	for t in time:
		time_step.append(t[1]-t[0])
	lowest_density_index = time_step.index(max(time_step))
	return lowest_density_index


def rand_conical_grid(points_number):

	"""
	TODO: documentation by Denis
	"""

	min_rho = min([location(i).x**2 + location(i).y**2 for i in range(1,27)])
	min_rho = 1.05 * np.sqrt(min_rho)
	max_rho = lambda z: 0.85 * np.sqrt(2) * z / np.pi
	max_phi = 0.95 * np.pi / 2
	min_z = min([location(i).z for i in range(1,27)])
	max_z = max([location(i).z for i in range(1,27)])

	points = []
	for _ in range(points_number):
		rand_z = random.uniform(min_z, max_z)
		rand_rho = random.uniform(min_rho, max_rho(rand_z))
		rand_phi = random.uniform(0, max_phi)
		rand_pt = np.array([rand_rho * np.cos(rand_phi), rand_rho * np.sin(rand_phi), rand_z])
		points.append(rand_pt)
	return points


def mirror_and_interpol5D(index, time, func, ratio):

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
		cart_pose (list on nd.array). The position of coresponding
			port (real or interporated).
		res_time (list of nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to time of 
			filed propagation.
		res_func (list of nd.array). Array of arrays with sorted 
			floating point numbers that coresponds to magnitude of recived filed
	"""

	cart_pose, res_time, res_func = [], [], []

	points, values = [], []
	for port_idx, prob_time, prob_val in zip(index,time,func):
		port = location(port_idx)
		space = np.array([port.x, port.y, port.z])
		space = mirror_point3D(space)
		cart_pose.extend(space)
		res_time.extend(4 * [prob_time])
		res_func.extend(4 * [prob_val])
		for pt in space:
			for t, f in zip(prob_time, prob_val):
				arg = np.array([t, pt[0], pt[1], pt[2]])
				points.append(arg)
				values.append(f)

	if ratio != 0:
		rand_cart_pose = rand_conical_grid(ratio * len(func))
		all_is_nan_of = lambda nparray: np.argwhere(np.isnan(nparray)).shape[0] == nparray.shape[0]
		lowest_density_index = get_max_time_step_intex(time)
		max_time = time[lowest_density_index][-1]
		dlt_time = time[lowest_density_index][1]
		for pt in rand_cart_pose:
			prob_time = np.arange(0,max_time, dlt_time)
			request = [np.array([t, pt[0], pt[1], pt[2]]) for t in prob_time]
			prob_val = griddata(points, values, request)
			if not all_is_nan_of(prob_val):
				prob_val[0] = 0
				cart_pose.extend(mirror_point3D(pt))
				res_time.extend(4 * [prob_time])
				res_func.extend(4 * [prob_val])
			else:
				print('[WW] Interpolation failed for point:', pt[0], pt[1], pt[2])

	return cart_pose, res_time, res_func


def filed_superpose(time, func):

	"""
	TODO: documentation by Denis
	"""

	lowest_density_index = get_max_time_step_intex(time)

	res_time = time[lowest_density_index]
	tmp_func = [[] for i in range(res_time.shape[0])]
	for tm, fn in zip(time, func):
		for t, f in zip(tm, fn):
			nearest_idx = np.abs(res_time - t).argmin()
			tmp_func[nearest_idx].append(f)

	res_func = np.array([sum(i)/len(i) for i in tmp_func])
	return res_time, res_func
