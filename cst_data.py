import os, sys, csv
import numpy as np


def location(port_idx, b=0.127):

    """
    TODO: documentation by Denis
    """

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


def cst_data_exporter(file_path):

    """
    TODO: documentation by Denis
    """

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

