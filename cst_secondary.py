import os, sys, csv
import cv2 as cv
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
import argparse


def double_mirror_data(x, y, f):
    x = np.hstack([x, -x,  x, -x])
    y = np.hstack([y, -y, -y,  y])
    f = np.hstack([f,  f,  f,  f])
    return x, y, f


def polar_slice_interpolate(x, y, fnc, max_rho, num_rho, num_phi):
    dist = interpolate.interp2d(x, y, fnc, kind='linear')
    rho = np.linspace(0, max_rho, num=num_rho)
    phi = np.linspace(0, 2 * np.pi, num=num_phi)
    rho_grid, phi_grid = np.meshgrid(rho, phi)
    x_grid = rho_grid * np.cos(phi_grid)
    y_grid = rho_grid * np.sin(phi_grid)
    f_grid = np.empty(shape=x_grid.shape)
    for i in range(f_grid.shape[0]):
        for j in range(f_grid.shape[1]):
            f_grid[i][j] = dist(x_grid[i][j], y_grid[i][j])
    return x_grid, y_grid, f_grid


def cst_probsdata_position(file_path):
    contents = open(file_path, 'r').readlines()
    x = float(contents[0].split()[0][2:])
    y = float(contents[0].split()[1][2:])
    z = float(contents[0].split()[2][2:])
    return x, y, z


def cst_probsdata_value(file_path):
    contents = open(file_path, 'r').readlines()
    for i in range(len(contents)):
        if len(contents[i]) > 5:
            if contents[i].split()[0].find('-----') != -1:
                contents = contents[i+1:]
                break
    time, func = [], []
    for line in contents:
        if len(line) > 1:
            time.append(float(line.split()[0]))
            func.append(float(line.split()[1]))
    return np.array(time), np.array(func)


def save_ascii_table(x, y, title):
    with open(title, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=['time, sec', 'current, A'])
        for i in range(x.shape[0]):
            writer.writerow({'time, sec': x[i], 'current, A': y[i]})


# X = np.array([1, 2, 3])
# Y = np.array([1, 2, 3])
# Z = np.array([1, 2, 3])
# X, Y, Z = double_mirror_data(X, Y, Z)
# X_GRID, Y_GRID, Z_GRID = polar_slice_interpolate(X, Y, Z, 3.5, 6, 30)
# plot.pcolormesh(X_GRID, Y_GRID, Z_GRID)
# plot.show()


def location(port_idx, b=0.127):
    port_location_data = {
        1:  dict(x=b / 4, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        2:  dict(x=b / 8, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        3:  dict(x=b / 3, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        4:  dict(x=b / 3, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        5:  dict(x=b / 4, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        6:  dict(x=b / 8, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        7:  dict(x=b / 2, y=.1 * np.sin(2 * np.pi / 20),   z=.1 * np.cos(2 * np.pi / 20) + b),
        8:  dict(x=b / 2, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        9:  dict(x=b / 3, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        10: dict(x=b / 4, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        11: dict(x=b / 8, y=.1 * np.sin(3 * np.pi / 20),   z=.1 * np.cos(3 * np.pi / 20) + b),
        12: dict(x=b / 2, y=.1 * np.sin(np.pi / 20),       z=.1 * np.cos(np.pi / 20) + b),
        13: dict(x=b / 8, y=.1 * np.sin(4 * np.pi / 20),   z=.1 * np.cos(4 * np.pi / 20) + b),
        14: dict(x=b / 4, y=.1 * np.sin(4 * np.pi / 20),   z=.1 * np.cos(4 * np.pi / 20) + b),
        15: dict(x=b / 8, y=.05 * np.sin(np.pi / 20),      z=.05 * np.cos(np.pi / 20) + b),
        16: dict(x=b / 3, y=.05 * np.sin(np.pi / 20),      z=.05 * np.cos(np.pi / 20) + b),
        17: dict(x=b / 2, y=.05 * np.sin(np.pi / 20),      z=.05 * np.cos(np.pi / 20) + b),
        18: dict(x=b / 8, y=.05 * np.sin(4 * np.pi / 20),  z=.05 * np.cos(4 * np.pi / 20) + b),
        19: dict(x=b / 3, y=.05 * np.sin(4 * np.pi / 20),  z=.05 * np.cos(4 * np.pi / 20) + b),
        20: dict(x=b / 2, y=.05 * np.sin(4 * np.pi / 20),  z=.05 * np.cos(4 * np.pi / 20) + b),
        21: dict(x=b / 8, y=.05 * np.sin(8 * np.pi / 20),  z=.05 * np.cos(8 * np.pi / 20) + b),
        22: dict(x=b / 4, y=.05 * np.sin(8 * np.pi / 20),  z=.05 * np.cos(8 * np.pi / 20) + b),
        23: dict(x=b / 8, y=.01 * np.sin(np.pi / 20),      z=.01 * np.cos(np.pi / 20) + b),
        24: dict(x=b / 3, y=.01 * np.sin(np.pi / 20),      z=.01 * np.cos(np.pi / 20) + b),
        25: dict(x=b / 8, y=.001 * np.sin(8 * np.pi / 20), z=.001 * np.cos(8 * np.pi / 20) + b),
        26: dict(x=b / 3, y=.001 * np.sin(8 * np.pi / 20), z=.001 * np.cos(8 * np.pi / 20) + b),
    }
    return type("", (), port_location_data[port_idx])()


def main():

    parser = argparse.ArgumentParser(description='Kerr amendment calculator for LIRA internal antenna problem')
    parser.add_argument('--probe', type=str, help='Probe data dirictory path')
    args = parser.parse_args()

    x, y, z = [], [], []

    for port in os.listdir(args.probe):

        index = int(os.path.splitext(port)[0][7:])
        x.append(location(index).z)
        y.append(location(index).y)
        z.append(location(index).x)


    fig = plot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('OX')
    ax.set_ylabel('OY')
    ax.set_zlabel('OZ')
    plot.show()


            # path_ex = 'probdata/P' + str(prob) + 'x' + '.txt'
            #
            # if os.path.exists(path_ex) and os.path.exists(path_ey) and os.path.exists(path_ez):
            #
            #     # x, y, z = cst_probsdata_position(path_ex)
            #     tx, ex = cst_probsdata_value(path_ex)
            #     ty, ey = cst_probsdata_value(path_ey)
            #     tz, ez = cst_probsdata_value(path_ez)
            #
            #     print(path_ex, tx.shape[0])
            #
            #     # if tx.all() is not ty.all() is not tz.all():
            #     #    print('[EE] time is not equal at ', x, y, z)
            #     #    sys.exit(-1)
            #
            #     jx = 1e-16 * np.gradient((ex**2 + ey**2 + ez**2) * ex, tx)
            #     jy = 1e-16 * np.gradient((ex**2 + ey**2 + ez**2) * ey, ty)
            #     jz = 1e-16 * np.gradient((ex**2 + ey**2 + ez**2) * ez, tz)
            #
            #     # jy_path = 'portdata/jy_' + str(prob) + '.txt'
            #     # jz_path = 'portdata/jz_' + str(prob) + '.txt'
            #
            #     save_ascii_table(tx, jx, 'portdata/j' + str(prob) + 'x.txt')
            #     save_ascii_table(tx, jy, 'portdata/j' + str(prob) + 'y.txt')
            #     save_ascii_table(tx, jz, 'portdata/j' + str(prob) + 'z.txt')
            #
            #     plot.plot(tx, jx, color='red',   label='jx, A/m')
            #     plot.plot(ty, jy, color='green', label='jy, A/m')
            #     plot.plot(tz, jz, color='blue',  label='jz, A/m')
            #     plot.legend()
            #     plot.show()

            # else:
            #    print('[WW] component does not exists at ', x, y, z)


if __name__ == '__main__':
    main()
