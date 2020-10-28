import os, sys, csv
from scipy.linalg import norm
import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import axes3d
from cst_data import location, cst_data_exporter


def vector_set(p1, p2, r):

    """
    TODO: documentation by Denis
    """

    v = p2 - p1 # vector in direction of axis
    v = v / norm(v) # unit vector in direction of axis

    # make some vector not in the same direction as v
    not_v = np.array([1, 0, 0])
    if (v == not_v).all():
        not_v = np.array([0, 1, 0])

    n1 = np.cross(v, not_v) # make vector perpendicular to v
    n1 /= norm(p2-p1) # normalize n1

    n2 = np.cross(v, n1) # make unit vector perpendicular to v and n1
    return v, n1, n2


def show_port_location():

    """
    TODO: documentation by Denis
    TODO: bug fix by Denis
    """

    point0 = np.array([0,0,3]) # point at one end
    point1 = np.array([0,0,-3]) # point at other end
    radius = 2 # radius of the base of conical surface
    vect_x, vect_y, vect_z = vector_set(point0, point1, radius)
    # vect_x=vect_z, vect_z=vect_x
    # surface ranges over t from 0 to length of axis and 0 to 2*pi
    t = np.linspace(0, norm(point1 - point0), 2)
    theta = np.linspace(0, 2*np.pi, 100)
    rsample = np.linspace(0, radius, 2)

    # use meshgrid to make 2d arrays
    t, theta2 = np.meshgrid(t, theta)
    rsample,theta = np.meshgrid(rsample, theta)
    X, Y, Z = [point0[i] + vect_x[i] * t + radius * t * np.sin(theta2) * vect_y[i] + radius * t * np.cos(theta2) * vect_z[i] for i in [0, 1, 2]]

    ax=plot.subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, color='blue', alpha=0.6)

    for i in range(1,27):
        point = location(i)
        ax.scatter(point.x, point.y, point.z, c='r', marker='o')

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plot.show()


def show_prob_data():

    """
    TODO: documentation by Denis
    """

    index, time, func = [], [], []
    parent_directory = 'observer1'

    for i in range(1,27):

        if i == 13: continue
        file_name = 'ex_port' + str(i) + '.txt'
        file_path = os.path.join(parent_directory, file_name)

        if not os.path.exists(file_path):
            print('[EE]: File with path does not exit - ', file_path)
            sys.exit()

        data = cst_data_exporter(file_path)
        index.append(i)
        time.append(data[0])
        func.append(data[1])

    fig = plot.figure()
    ax = fig.gca(projection='3d')

    for i, t, f in zip(index, time, func):
        if i < 4 or i > 7: continue
        x = np.full(t.shape, location(i).x, dtype=np.float)
        ax.plot(t, x, f, label=str(i))

    ax.set_xlabel('time')
    ax.set_ylabel('OX pose of port')
    ax.set_zlabel('Ex')
    ax.legend()
    plot.show()

